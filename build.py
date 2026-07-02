"""
Build script to convert all markdown files into PDF files.

Specifically, this script recursively walks through all subdirectories in
the project which have an `index.md` file and generates 3 kinds of PDFs,
all using `pandoc`:

1. Converts each markdown file it finds into a PDF file
2. For each directory with an `index.md` file, generates a combined PDF file
    with the directory name as the PDF name, containing the contents of the
    `index.md` file first, and then the contents of all other markdown files
    in natural alphabetical order
3. Creates a "global" PDF named OCW.pdf, which contains the contents of the
    `index.md` file at the project root, then a detailed table of contents,
    and then appends the contents of all other markdown files in natural
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
    "algorithms",
    "test"
]

# The build script should always be run from the project root
# so this should always give us the project root
PROJECT_ROOT = Path.cwd()


class ConversionType(Enum):
    SINGLE_FILE = 1
    DIRECTORY = 2
    GLOBAL = 3


def run_pandoc(input_path: Path, output_path: Path, resource_path: Path, mode: ConversionType) -> bool:
    """
    Run pandoc on an input markdown file
    :param input_path: The input path for the markdown file
    :param output_path: The output path for the PDF file
    :param resource_path: The resource path for looking up linked resources
    :param mode: The type of PDF file being generated
    :return: True if successful, False otherwise
    """
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
        '-V', 'header-includes=\\cfoot{\\thepage}'
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error generating {output_path}')
        return False


def sanitize_markdown(content: str, file_path: Path, mode: ConversionType) -> str:
    """
    Sanitizes content and links found in any arbitrary markdown file into content and links
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
    # Group 3 & 4: Text and Path for Liquid tags like [text]({% link path %})
    link_regex = re.compile(
        r'\[([^]]+)]\(\.(/[^)]+)\)'
        r'|'
        r'\[([^]]+)]\(\{%\s*link\s+([^%}]+)\s*%}\)'
    )

    if mode == ConversionType.SINGLE_FILE:
        # Get the parent directory for this markdown file. Example:
        # 6.004/index.md -> PROJECT_ROOT / 6.004
        file_dir_rel_to_root = (PROJECT_ROOT / file_path).parent

        def link_replacer(match: re.Match) -> str:
            # Matched a standard Markdown link (./media/lec1.png)
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
                root_path = Path(str(match.group(4).strip()))
                return f"[{link_text}]({root_path.as_posix()})"

        return link_regex.sub(link_replacer, content)
    return content


def markdown_to_pdf(input_path: Path | None, mode: ConversionType) -> None:
    """
    Reads a markdown file or directory containing markdown files and
    correctly converts it into a PDF depending on `mode`
    :param input_path: Can be a path to a single markdown file or a directory.
        If `mode` is `ConversationType.SINGLE_FILE`, `input_path` must be a path to
        a single file. If `mode` is `ConversationType.DIRECTORY`, `input_path` must be
        a path to a directory containing an index.md file. If `mode` is
        `ConversationType.GLOBAL`, `input_path` must be None.
    :param mode: The type of PDF file being generated
    :return:
    """
    if mode == ConversionType.GLOBAL and input_path is not None:
        raise ValueError("input_path must be None if mode is ConversionType.GLOBAL")
    if mode == ConversionType.DIRECTORY and not input_path.is_dir():
        raise ValueError("input_path must be a directory if mode is ConversionType.DIRECTORY")
    if mode == ConversionType.SINGLE_FILE and not input_path.is_file():
        raise ValueError("input_path must be a file if mode is ConversionType.SINGLE_FILE")

    if mode == ConversionType.SINGLE_FILE:
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
                    updated_front_matter = re.sub(r"(^title:\s*)(.*)$", r"\1" + index_title, front_matter, flags=re.MULTILINE)
                    sanitized_content = sanitized_content.replace(front_matter, updated_front_matter, 1)

            tnf.write(sanitized_content)
            tnf.flush()
            tmp_name = tnf.name

        success = run_pandoc(Path(tmp_name), output_path, base_dir, mode)
        os.unlink(tmp_name)
        
        if not success:
            print(f"Error: failed to convert {input_path}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        help="Path to the markdown file or a directory containing markdown files. An index.md must be present if passing a directory.",
        type=str,
        default=""
    )
    args = parser.parse_args()

    if args.input:
        ip_path = Path(args.input)
        if not ip_path.exists():
            print("Input path does not exist")
            sys.exit(1)

        if ip_path.is_dir():
            markdown_to_pdf(ip_path, ConversionType.DIRECTORY)
        elif ip_path.is_file():
            markdown_to_pdf(ip_path, ConversionType.SINGLE_FILE)
