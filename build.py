"""
Build script to convert all Markdown files into PDF files.

Specifically, this script recursively walks through all subdirectories in
the project which have an `index.md` file and generates 3 kinds of PDFs,
all using `pandoc`:

1. Converts each Markdown file it finds into a PDF file
2. For each directory with an `index.md` file, generates a combined PDF file
    with the directory name as the PDF name, containing the contents of the
    `index.md` file first, and then the contents of all other Markdown files
    in natural alphabetical order
3. Creates a "global" PDF named OCW.pdf, which contains the contents of the
    `index.md` file at the project root, then a detailed table of contents,
    and then appends the contents of all other Markdown files in natural
    alphabetical order, grouped by the directory name

In each generated PDF file, it tries hard to generate working links every time
it finds a link in the markdown, but sometimes creating a working link may not
be possible (for example if a lecture in one course refers to a lecture in
another course, it may not be possible to create a working link in the generated
lecture PDF). In such cases, it simply generates plain text.
"""
from argparse import ArgumentParser
from enum import Enum
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import NamedTemporaryFile

# PDFs will be generated in the "pdf" subdirectory in each directory
PDF_OUTPUT_SUBDIR = "pdf"
PDF_ENGINE = "pdflatex"
IGNORED_DIRECTORIES = [
    "pdf",
    ".git",
    ".github",
    ".jekyll-cache",
    ".idea",
    "_includes",
    "_pvt",
    "_sass",
    "_site",
    "media",
    "degree-paths",

    "algorithms",
    "test"
]
IGNORED_FILE_NAMES = [
    "README.md",
    "LICENSE.md"
]

# The build script should always be run from the project root
# so this should always give us the project root
PROJECT_ROOT = Path.cwd()


class ConversionType(Enum):
    SINGLE_FILE = 1
    DIRECTORY = 2
    GLOBAL = 3

    def __str__(self):
        return ["SINGLE FILE", "DIRECTORY", "GLOBAL"][self.value-1]


def run_pandoc(input_path: Path, output_path: Path, resource_path: Path, mode: ConversionType) -> bool:
    """
    Run pandoc on an input Markdown file
    :param input_path: The input path for the Markdown file
    :param output_path: The output path for the PDF file
    :param resource_path: The resource path for looking up linked resources
    :param mode: The type of PDF file being generated
    :return: True if successful, False otherwise
    """
    latex_callouts_setup = (
        "\\usepackage[most]{tcolorbox}\n"
        "\\usepackage{xcolor}\n"

        # Base setup for Textbook-Style Callout Boxes
        "\\tcbset{\n"
        "  textbookbox/.style={\n"
        "    frame hidden,\n"                  # Remove top, right, bottom borders
        "    leftrule=4pt,\n"                   # Clean vertical accent bar on the left
        "    rightrule=0pt, toprule=0pt, bottomrule=0pt,\n"
        # "    arc=0pt, outer arc=0pt,\n"         # Sharp corners for a classic textbook feel
        "    left=10pt, right=10pt, top=8pt, bottom=8pt,\n" # Padding
        "    fonttitle=\\bfseries\\sffamily,\n"  # Sans-serif bold title
        "    coltitle=black,\n"
        "    attach title to upper={\\par\\vspace{2pt}},\n" # Title sits nicely above content
        "  }\n"
        "}\n"

        # 1. 'Note' or 'Remark' Box 
        "\\newtcolorbox{calloutnote}[1][Note]{"
        "  textbookbox, colback=gray!8!white, colframe=cyan!60!black, title={#1}"
        "}\n"

        # 2. 'Warning' or 'Caution' Box 
        "\\newtcolorbox{calloutwarning}[1][Warning]{"
        "  textbookbox, colback=orange!8!white, colframe=yellow!70!black, title={#1}"
        "}\n"

        # 3. 'Important' or 'Theorem / Lemma' Box
        "\\newtcolorbox{calloutimportant}[1][Important]{"
        "  textbookbox, colback=green!6!white, colframe=lime!40!black, title={#1}"
        "}\n"

        # 4. Fallback 'New' / 'Aside' Box
        "\\newtcolorbox{calloutnew}[1][Aside]{"
        "  textbookbox, colback=gray!10!white, colframe=gray!70!black, title={#1}"
        "}\n"
    )

    cmd = [
        "pandoc",
        str(input_path),
        "-o",
        str(output_path),
        f"--pdf-engine={PDF_ENGINE}",
        "-V", "geometry:margin=1.5in",
        "-V", "fontsize=11pt",
        "-V" "colorlinks=false",
        '-V', 'header-includes=\\usepackage{fancyhdr}',
        '-V', 'header-includes=\\pagestyle{fancy}',
        '-V', 'header-includes=\\fancyhf{}',
        '-V', 'header-includes=\\renewcommand{\\headrulewidth}{0pt}',
        '-V', 'header-includes=\\renewcommand{\\footrulewidth}{0.4pt}',
        '-V', 'header-includes=\\usepackage{hyperref}',
        '-V', 'header-includes=\\hypersetup{pdfborderstyle={/S/U/W 1}}',
        '-V', 'header-includes=\\lfoot{\\href{https://hrus.in/ocw}{hrus.in/ocw}}',
        '-V', f'header-includes={latex_callouts_setup}',
        '-V', 'header-includes=\\cfoot{\\thepage}'
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error generating {output_path}')
        return False


def get_anchor_from_md_heading(header_text: str) -> str:
    """Generates a standard Pandoc identifier anchor from a Markdown header string."""
    id_str = header_text.lower().strip()
    id_str = re.sub(r"[^a-z0-9\.\s\-]", "", id_str)  # Remove punctuation except hyphens/spaces
    id_str = re.sub(r"\s+", "-", id_str)           # Convert spaces to hyphens
    return f"#{id_str}"


def sanitize_markdown(content: str, file_path: Path, mode: ConversionType) -> str:
    """
    Sanitizes content and links found in any arbitrary Markdown file into content and links
    safe to be used with pandoc to generate a PDF depending on the
    file conversion mode
    :param content: The input markdown
    :param file_path: The current file's path
    :param mode: The file conversion mode
    :return: The sanitized content which should be safely and
        correctly converted by pandoc
    """
    # Combined regex pattern
    # Group 1 & 2: Text and Path for standard relative links like [text](./path)
    # Group 3, 4, & 5: Text, File Path, and Anchor (#heading-id) for Liquid links
    link_regex = re.compile(
        r'\[([^]]+)]\(\.(/[^)]+)\)'
        r'|'
        r'\[([^]]+)]\(\{%\s*link\s+([^%}\s]+)\s*%}\s*(#[^)]+)?\)'
    )

    # Get the parent directory for this Markdown file. Example:
    # 6.004/index.md -> PROJECT_ROOT / 6.004
    # In directory conversion mode or global conversion mode,
    # This will still point to the right parent directory
    # since the named temp file to store the Markdown contents
    # will be created in the right subdirectory.
    #
    # For example:
    # if converting the single file PROJECT_ROOT/6.004/lec1.md, we will
    # get PROJECT_ROOT/6.004.
    # If converting the whole directory PROJECT_ROOT/6.004, we will still
    # get PROJECT_ROOT/6.004
    # If converting globally, we will get PROJECT_ROOT
    file_dir_rel_to_root = (PROJECT_ROOT / file_path).parent

    def link_replacer(match: re.Match) -> str:
        # Matched a standard Markdown link (./media/lec1.png)
        # The conversion process is the same for all conversion modes
        if match.group(1) is not None:
            link_text = match.group(1)
            raw_path = str(match.group(2).lstrip('/'))

            if file_dir_rel_to_root != Path("."):
                root_path = file_dir_rel_to_root / raw_path
            else:
                root_path = Path(raw_path)
            return f"[{link_text}]({root_path.as_posix()})"

        # Matched a liquid style link ({% link 6.004/lec2.md %})
        else:
            link_text = match.group(3)
            link_path = Path(str(match.group(4).lstrip('/')))
            link_path_absolute = link_path.resolve()
            anchor_fragment = match.group(5) or ""
            # In single file conversion mode just remove the link and return
            # the normal text.
            if mode == ConversionType.SINGLE_FILE:
                return link_text
            # In directory conversion mode, check if the link points to a file
            # in the same directory. If so, convert it. If not, remove it.
            elif mode == ConversionType.DIRECTORY:
                if link_path_absolute.is_relative_to(file_dir_rel_to_root):
                    # The link points to a file in the same directory. Open the file
                    # to extract the first H1 in the file and return that link. This
                    # assumes that all Markdown files start with an H1, which seems
                    # like an OK assumption.
                    # If an anchor fragment exists (e.g., #specific-section), use it as a local anchor link
                    if anchor_fragment:
                        return f"[{link_text}]({anchor_fragment})"

                    # Otherwise, extract the H1 title from target file and generate Pandoc anchor
                    if link_path_absolute.exists():
                        with open(link_path_absolute, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.startswith("# "):
                                    h1_title = line.replace("# ", "").strip()
                                    anchor_id = get_anchor_from_md_heading(h1_title)  # Uses your Pandoc ID generator
                                    return f"[{link_text}]({anchor_id})"
                    return link_text
                return link_text
            # We should always be able to convert links in global mode.
            else:
                assert mode == ConversionType.GLOBAL
                # If pointing to a specific section fragment, prefer local internal link (#specific-section)
                if anchor_fragment:
                    return f"[{link_text}]({anchor_fragment})"

                # Otherwise, target the top H1 anchor of the referenced file
                if link_path_absolute.exists():
                    with open(link_path_absolute, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.startswith("# "):
                                h1_title = line.replace("# ", "").strip()
                                anchor_id = get_anchor_from_md_heading(h1_title)
                                return f"[{link_text}]({anchor_id})"

                # Fallback to just removing the link
                return link_text

    def callout_replacer(match: re.Match) -> str:
        """
        Converts Just the Docs paragraphs into LaTeX textbook environments
        """
        pre_text = match.group(1).strip()
        text = match.group(4).strip()
        callout_type = match.group(2).lower()
        custom_title = match.group(3)

        env_map = {
            "note": "calloutnote",
            "warning": "calloutwarning",
            "important": "calloutimportant",
            "new": "calloutnew"
        }
        env_name = env_map.get(callout_type, None)
        if env_name is None:
            return pre_text + '\n\n' + text
        title_str = custom_title if custom_title else callout_type.capitalize()
        return f"{pre_text}\n\\begin{{{env_name}}}[{title_str}]\n{text}\n\\end{{{env_name}}}"

    # Skip expensive regex comparison if we don't have any callouts in the content
    if "{:" in content:
        callout_regex = re.compile(
            r'([^\n]+(?:\n[^\n]+)*)\n*\{\:\s*\.([a-zA-Z0-9_-]+)(?:\s+title=["\']([^"\']+)["\'])?\s*\}\n*([^\n]+(?:\n[^\n]+)*)'
        )
        content = callout_regex.sub(callout_replacer, content)

    # If we are sanitizing Markdown for the global PDF, and we are not processing
    # an index.md file, make sure there are no H1's in this file. Reduce the heading level
    # of each heading by 1 to make sure there is no H1.
    if mode == ConversionType.GLOBAL and file_path.name != "index.md":
        content_lines = content.split('\n')
        for i in range(len(content_lines)):
            if content_lines[i].startswith("#"):
                content_lines[i] = "#" + content_lines[i]
        content = '\n'.join(content_lines)

    return link_regex.sub(link_replacer, content)

def get_ordered_markdown_files(directory: Path) -> list[Path]:
    """
    Return a list of Markdown files in the directory (and recursively all subdirectories),
    ordered by the natural sort order instead of the strict alphabetical order.
    Example: lec2.md is returned before lec10.md
    :param directory: The directory to search for Markdown files (recurses into subdirectories)
    :return: A list of `Path` objects in natural sort order
    """
    def natural_sort_key(filename):
        filename_str = str(filename)
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", filename_str)]

    files = []
    index_path = directory / "index.md"
    if index_path.exists():
        files.append(index_path)

    # Sort files naturally
    try:
        children = sorted(directory.iterdir(), key=lambda p: natural_sort_key(p.name))
    except FileNotFoundError:
        return files

    for child in children:
        if (
            child.is_file()
            and child.suffix == ".md"
            and child.name != "index.md"
            and child.name not in IGNORED_FILE_NAMES
        ):
            files.append(child)

    # Recurse into subdirectories using natural sorting
    for child in children:
        if child.is_dir() and child.name not in IGNORED_DIRECTORIES:
            files.extend(get_ordered_markdown_files(child))

    return files


def get_ordered_markdown_directories(directory: Path) -> list[Path]:
    """
    Return a list of directories (and recursively all subdirectories), that contain an index.md file
    ordered by the natural sort order instead of the strict alphabetical order.
    :param directory: The directory to search for Markdown containing subdirectories (recurses into subdirectories)
    :return: A list of `Path` objects in natural sort order
    """
    def natural_sort_key(filename):
        filename_str = str(filename)
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", filename_str)]

    directories = []
    index_path = directory / "index.md"
    if not index_path.exists():
        return directories
    if not directory.is_dir():
        return directories

    # Sort files naturally
    try:
        children = sorted(directory.iterdir(), key=lambda p: natural_sort_key(p.name))
    except FileNotFoundError:
        return directories

    for child in children:
        if (
            child.is_dir()
            and child.name not in IGNORED_DIRECTORIES
            and (child / "index.md").exists()
        ):
            directories.append(child)

    # Recurse into subdirectories using natural sorting
    for child in children:
        if (
            child.is_dir()
            and child.name not in IGNORED_DIRECTORIES
        ):
            directories.extend([x for x in get_ordered_markdown_files(child) if x.is_dir()])

    return directories


def get_markdown_for_directory(input_path: Path, mode: ConversionType) -> str:
    """
    Returns the combined content for all Markdown files in the passed `input_path`.
    First appends the contents of `index.md` if present, then the sanitized content
    of all Markdown files in the current directory (in natural alphabetical order),
    then recursively gets content for subdirectories.
    :param input_path: The directory to search for Markdown files
    :param mode: The conversion mode
    :return: Valid Markdown contents as a string
    """
    if not input_path.is_dir():
        raise ValueError("input_path must be a directory")

    result = ""
    ordered_files = get_ordered_markdown_files(input_path)

    for file in ordered_files:
        if result:
            contents = file.read_text(encoding="utf-8")
            contents = re.sub(r"^\s*---.*?---", "", contents, count=1, flags=re.DOTALL | re.MULTILINE)
            result += sanitize_markdown(contents, file, mode)
        else:
            result += sanitize_markdown(file.read_text(encoding="utf-8"), file, mode)
        result += "\n\\newpage\n\n"
    return result


def markdown_to_pdf(input_path: Path | None, mode: ConversionType) -> bool:
    """
    Reads a Markdown file or directory containing Markdown files and
    correctly converts it into a PDF depending on `mode`
    :param input_path: Can be a path to a single Markdown file or a directory.
        If `mode` is `ConversationType.SINGLE_FILE`, `input_path` must be a path to
        a single file. If `mode` is `ConversationType.DIRECTORY`, `input_path` must be
        a path to a directory containing an index.md file. If `mode` is
        `ConversationType.GLOBAL`, `input_path` must be None.
    :param mode: The type of PDF file being generated. If mode is `ConversionType.SINGLE_FILE`,
        converts a single file from Markdown to PDF. If mode is `ConversionType.DIRECTORY`,
        combines the content of all the Markdown files in the `input_path` directory (recursively
        visiting subdirectories) and generates one PDF from the combined content. If mode is
        `ConversionType.GLOBAL`, does the same operation as directory level conversion, but at
        the project root level.
    :return: True if the conversion succeeded, False otherwise
    """
    if mode == ConversionType.GLOBAL and input_path is not None:
        raise ValueError(f"input_path must be None if mode is ConversionType.GLOBAL. Got {input_path}")
    if mode == ConversionType.DIRECTORY and (input_path is None or not input_path.is_dir()):
        raise ValueError(f"input_path must be a directory if mode is ConversionType.DIRECTORY. Got {input_path or 'None'}")
    if mode == ConversionType.SINGLE_FILE and (input_path is None or not input_path.is_file()):
        raise ValueError(f"input_path must be a file if mode is ConversionType.SINGLE_FILE. Got {input_path or 'None'}")

    if mode == ConversionType.SINGLE_FILE:
        assert input_path is not None
        base_dir = input_path.parent
        output_path = base_dir / PDF_OUTPUT_SUBDIR / (input_path.stem + ".pdf")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Converting [{mode}]: {input_path} -> {output_path}")

        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # If the file is a lecture file, and it has front matter, replace
        # the title property in the front matter of this file with the
        # title property in the front matter of the index.md file in this
        # directory, if present
        index_md_path = base_dir / "index.md"
        index_title = ""
        if input_path.name.startswith("lec") and index_md_path.exists():
            with open(index_md_path, encoding="utf-8") as f:
                matches = re.findall(r"^title:\s*(.*)$", f.read(), flags=re.MULTILINE)
                if matches:
                    index_title = matches[0].strip()

        with NamedTemporaryFile(mode="w+", suffix=".md", delete=False, encoding="utf-8") as tnf:
            sanitized_content = sanitize_markdown(content, input_path, mode)

            # Replace the title inside the front matter if index_title was successfully found
            if index_title:
                # Find the front matter boundaries explicitly at the start of the sanitized content
                front_matter_match = re.match(r"\A---.*?---", sanitized_content, flags=re.DOTALL)
                if front_matter_match:
                    front_matter = front_matter_match.group(0)
                    # Safely swap out just the line beginning with "title:" inside the front matter block
                    # Safely swap out the title line, replacing any colons in the original title (\2) with a dash
                    updated_front_matter = re.sub(
                        r"(^title:\s*)(.*)$",
                        lambda match: f'{match.group(1)}{index_title} {match.group(2).replace(":", "-")}',
                        front_matter,
                        flags=re.MULTILINE
                    )
                    sanitized_content = sanitized_content.replace(front_matter, updated_front_matter, 1)

            tnf.write(sanitized_content)
            tnf.flush()
            tmp_name = tnf.name

        success = run_pandoc(Path(tmp_name), output_path, base_dir, mode)
        os.unlink(tmp_name)
        
        if not success:
            print(f"Error: failed to convert {input_path}")

    else:
        assert (mode == ConversionType.DIRECTORY or mode == ConversionType.GLOBAL)
        if mode == ConversionType.GLOBAL:
            input_path = PROJECT_ROOT

        assert input_path is not None
        output_path = input_path / PDF_OUTPUT_SUBDIR / (input_path.name + ".pdf")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Converting [{mode}]: {input_path} -> {output_path}")

        with NamedTemporaryFile(mode="w+", suffix=".md", delete=False, encoding="utf-8") as tnf:
            tnf.write(get_markdown_for_directory(input_path, mode))
            tnf.flush()
            tmp_name = tnf.name

        success = run_pandoc(Path(tmp_name), output_path, input_path, mode)
        os.unlink(tmp_name)

        if not success:
            print(f"Error: failed to convert {input_path}")
    return success


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        help="Path to the Markdown file or directory containing Markdown files. An index.md must be present if passing a directory.",
        type=str,
        nargs="*",
        default=""
    )
    parser.add_argument(
        '--test',
        help="Test the build script by running on the test/ directory",
        action="store_true"
    )
    parser.add_argument(
        "--global", '-g',
        dest="build_global",
        help="Build the global PDF only",
        action="store_true"
    )
    args = parser.parse_args()

    n_success = 0
    n_failed = 0
    def _convert(input_path: Path | None, mode: ConversionType) -> tuple[int, int]:
        """
        Thin wrapper around `markdown_to_pdf` to catch exceptions and report success
        or failure
        :param input_path: `Path` to input file or `None` if global conversion mode
        :param mode: Conversion type
        :return: A one-hot 2-tuple. The first element is 1 if conversion succeeds, the second element
            is 1 if it fails
        """
        global n_success, n_failed
        try:
            s = markdown_to_pdf(input_path, mode)
            if s:
                n_success += 1
                return 1, 0
            n_failed += 1
            return 0, 1
        except Exception as e:
            print(e)
            n_failed += 1
            return 0, 1

    if args.test:
        print(get_ordered_markdown_directories(PROJECT_ROOT))
        print('Testing')
        sys.exit(0)

    if args.build_global:
        _convert(None, ConversionType.GLOBAL)
        print(f'{n_success} conversions succeeded, {n_failed} failed.')
        sys.exit(n_failed)


    if args.input:
        for path in args.input:
            ip_path = Path(path)
            if not ip_path.exists():
                print(f"Input path {path} does not exist")
                sys.exit(1)

            if ip_path.is_dir():
                m = ConversionType.DIRECTORY
            else:
                m = ConversionType.SINGLE_FILE
            _convert(ip_path, m)

    else:
        # First convert all markdown files in single file conversion mode
        md_files = get_ordered_markdown_files(PROJECT_ROOT)
        for f in md_files:
            _convert(f, ConversionType.SINGLE_FILE)

        # Then generate the directory level PDF for all directories containing an index.md
        md_dirs = get_ordered_markdown_directories(PROJECT_ROOT)
        for d in md_dirs:
            _convert(d, ConversionType.DIRECTORY)

        # Finally, generate the global PDF
        _convert(None, ConversionType.GLOBAL)

    print(f'{n_success} conversions succeeded, {n_failed} failed.')
    sys.exit(n_failed)