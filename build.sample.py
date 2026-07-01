#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

# Name of the subdirectory where PDFs will be generated
PDF_OUTPUT_SUBDIR = "pdf"
PDF_ENGINE = "pdflatex"

# Add any directory paths to exclude from the global combined PDF
GLOBAL_PDF_IGNORED_DIRECTORIES = ["./algorithms"]


def run_pandoc(input_path, output_path, resource_path):
    """Centralized method to execute Pandoc with global configuration parameters."""
    cmd = [
        "pandoc",
        str(input_path),
        "-o",
        str(output_path),
        f"--pdf-engine={PDF_ENGINE}",
        "-V", "geometry:margin=1.5in",
        "-V", "fontsize=11pt",
        "-V", "colorlinks=false",
        "-V", "hyperrefoptions=pdfborderstyle={/S/U/W 1},pdfnewwindow=true",
        f"--resource-path={resource_path}"
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Exit status: {e.returncode}")
        return False


def sanitize_markdown(content):
    """Sanitizes Jekyll/Liquid tags so they don't break compilers."""
    # Remove YAML front matter
    content = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)

    # Convert {% link 6.004/lec1.md %} to just a regular relative path or text
    def link_replacer(match):
        return os.path.basename(match.group(1))

    return re.sub(r"\{\%\s*link\s+([^\s\%]+)\s*\%\}", link_replacer, content)


def convert_jekyll_links_to_anchors(content, link_mapping):
    """Universally converts ANY {% link <path> %} sequence to its local anchor using a provided map."""
    def link_replacer(match):
        raw_link_path = match.group(1).strip()
        lookup_key = re.sub(r"\A\./", "", raw_link_path) # Standardize format
        
        # Try full path first, then fall back to baseline file name match
        matched_anchor = link_mapping.get(lookup_key) or link_mapping.get(os.path.basename(lookup_key))
        return matched_anchor if matched_anchor else "##"

    return re.sub(r"\{\%\s*link\s+([^\s\%]+)\s*\%\}", link_replacer, content)


def generate_pandoc_id(header_text):
    """Generates a standard Pandoc identifier anchor from a header string."""
    id_str = header_text.lower().strip()
    id_str = re.sub(r"[^a-z0-9\s\-]", "", id_str)  # Remove punctuation except hyphens/spaces
    id_str = re.sub(r"\s+", "-", id_str)           # Convert spaces to hyphens
    return f"#{id_str}"


def extract_h1_title(file_path):
    """Parses a markdown file to extract its main H1 title."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    return line.replace("# ", "").strip()
    except Exception:
        pass
    return None


def natural_sort_key(filename):
    """Helper to provide a natural sorting key by padding integers with leading zeros."""
    filename_str = str(filename)
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", filename_str)]


def ordered_markdown_files(directory):
    """Get a list of ordered markdown files in the directory."""
    files = []
    path = Path(directory)

    index_file = path / "index.md"
    if index_file.exists():
        files.append(str(index_file))

    # Sort files naturally
    try:
        children = sorted(path.iterdir(), key=lambda p: natural_sort_key(p.name))
    except FileNotFoundError:
        return files

    for child in children:
        if child.is_file() and child.suffix == ".md" and child.name != "index.md":
            files.append(str(child))

    # Recurse into subdirectories using natural sorting
    for child in children:
        if child.is_dir():
            files.extend(ordered_markdown_files(child))

    return files


def convert_markdown_to_pdf(md_file, base_dir):
    """Convert a markdown file to a PDF file."""
    relative_path = Path(md_file).relative_to(Path(base_dir))
    pdf_file = Path(base_dir) / PDF_OUTPUT_SUBDIR / relative_path.with_suffix(".pdf")

    pdf_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"Converting: {md_file} -> {pdf_file}")

    with open(md_file, "r", encoding="utf-8") as f:
        raw_content = f.read()

    clean_content = sanitize_markdown(raw_content)

    with NamedTemporaryFile(mode="w+", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(clean_content)
        tmp.flush()
        tmp_name = tmp.name

    success = run_pandoc(tmp_name, pdf_file, base_dir)
    os.unlink(tmp_name)

    if not success:
        print(f"ERROR: Failed to convert {md_file}")
        return False
    return True


def create_combined_pdf(base_dir):
    """Create a single PDF file containing all lecture notes with internal working links."""
    pdf_dir = Path(base_dir) / PDF_OUTPUT_SUBDIR
    pdf_dir.mkdir(parents=True, exist_ok=True)

    dirname = Path(base_dir).name
    output_pdf = pdf_dir / f"{dirname}.pdf"
    md_files = ordered_markdown_files(base_dir)

    link_mapping = {}
    for file in md_files:
        if os.path.basename(file) == "index.md":
            continue
        title = extract_h1_title(file)
        if title:
            rel_path = str(Path(file).relative_to(Path(base_dir)))
            link_mapping[rel_path] = generate_pandoc_id(title)
            link_mapping[os.path.basename(file)] = generate_pandoc_id(title)

    print(f"Creating combined PDF: {output_pdf}")

    with NamedTemporaryFile(mode="w+", suffix=".md", delete=False, encoding="utf-8") as tmp:
        for file in md_files:
            tmp.write("\n\\newpage\n\n")
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

            content = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
            content = convert_jekyll_links_to_anchors(content, link_mapping)

            # Shift header depths dynamically
            is_course_index = (os.path.basename(file) == "index.md")
            if is_course_index:
                content = re.sub(r"^(#+)(\s+)", r"\1#\2", content, flags=re.MULTILINE)
            else:
                content = re.sub(r"^(#+)(\s+)", r"\1##\2", content, flags=re.MULTILINE)

            clean_content = sanitize_markdown(content)
            tmp.write(clean_content)
        
        tmp.flush()
        tmp_name = tmp.name

    success = run_pandoc(tmp_name, output_pdf, base_dir)
    os.unlink(tmp_name)

    if not success:
        print(f"ERROR: Failed to create combined PDF for {base_dir}")
        return False
    return True


def create_global_combined_pdf():
    """Compile every markdown file across all subdirectories into a single large PDF."""
    root_pdf_dir = Path(".") / PDF_OUTPUT_SUBDIR
    root_pdf_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = root_pdf_dir / "OCW.pdf"

    normalized_ignored = [str(Path(d).cleanpath()) if hasattr(Path(d), 'cleanpath') else str(Path(d).resolve()) for d in GLOBAL_PDF_IGNORED_DIRECTORIES]
    # Simple fallback clean string representation for Python standard library compatibility
    normalized_ignored = [str(Path(d)) for d in GLOBAL_PDF_IGNORED_DIRECTORIES]

    print(f"\nGenerating master comprehensive PDF across all modules: {output_pdf}")

    # Discover all modules containing index files
    all_indices = [str(p) for p in Path(".").glob("**/index.md")]
    module_dirs = []
    for idx in all_indices:
        parent = os.path.dirname(idx)
        if parent != "." and parent != "":
            if str(Path(parent)) not in normalized_ignored:
                module_dirs.append(parent)

    module_dirs = sorted(module_dirs, key=natural_sort_key)

    all_md_files = []
    root_index = "./index.md"
    if os.path.exists(root_index):
        all_md_files.append(root_index)

    for d in module_dirs:
        all_md_files.extend(ordered_markdown_files(d))

    if not all_md_files:
        print("No module markdown files found to aggregate.")
        return False

    global_link_mapping = {}
    for file in all_md_files:
        if os.path.basename(file) == "index.md":
            continue
        title = extract_h1_title(file)
        if title:
            anchor_id = generate_pandoc_id(title)
            clean_path = re.sub(r"\A\./", "", file)
            global_link_mapping[clean_path] = anchor_id
            global_link_mapping[os.path.basename(file)] = anchor_id

    with NamedTemporaryFile(mode="w+", suffix=".md", delete=False, encoding="utf-8") as tmp:
        # Join resource paths with system specific separator (: for Unix, ; for Windows)
        path_sep = ";" if os.name == "nt" else ":"
        resource_paths = path_sep.join(["."] + module_dirs)

        for file in all_md_files:
            tmp.write("\n\\newpage\n\n")
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

            content = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
            content = convert_jekyll_links_to_anchors(content, global_link_mapping)

            is_root_index = (file == root_index)
            is_course_index = (os.path.basename(file) == "index.md" and not is_root_index)
            is_lecture_file = (not is_root_index and not is_course_index)

            if is_course_index:
                content = re.sub(r"^(#+)(\s+)", r"\1#\2", content, flags=re.MULTILINE)
            elif is_lecture_file:
                content = re.sub(r"^(#+)(\s+)", r"\1##\2", content, flags=re.MULTILINE)

            clean_content = sanitize_markdown(content)
            tmp.write(clean_content)

        tmp.flush()
        tmp_name = tmp.name

    success = run_pandoc(tmp_name, output_pdf, resource_paths)
    os.unlink(tmp_name)

    if not success:
        print("ERROR: Failed to create global master PDF")
        return False
    print(f"Master PDF built successfully at {output_pdf}!")
    return True


if __name__ == "__main__":
    # Check if a specific file path was passed via command line arguments
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        if not os.path.exists(target_file):
            print(f"ERROR: File not found: {target_file}")
            sys.exit(1)

        current_dir = os.path.dirname(target_file)
        # Traverse up to find base module path with an index file
        while current_dir != "." and not os.path.exists(os.path.join(current_dir, "index.md")):
            parent = os.path.dirname(current_dir)
            if parent == current_dir:
                break
            current_dir = parent

        base_dir = os.path.dirname(target_file) if current_dir == "." else current_dir
        print("Running single-file test mode...")
        convert_markdown_to_pdf(target_file, base_dir)
    else:
        # Standard Batch Processing Mode
        all_indices = [str(p) for p in Path(".").glob("**/index.md")]
        valid_dirs = []
        for idx in all_indices:
            parent = os.path.dirname(idx)
            if parent != "." and parent != "":
                valid_dirs.append(parent)

        for d in valid_dirs:
            print(f"\nProcessing directory: {d}")
            md_files = [str(p) for p in Path(d).glob("**/*.md")]
            md_files = sorted(md_files, key=natural_sort_key)
            
            for md_file in md_files:
                convert_markdown_to_pdf(md_file, d)
            
            create_combined_pdf(d)

        create_global_combined_pdf()

    print("\nPDF conversion complete!")