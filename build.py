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
        "-V", "hyperrefoptions=pdfborderstyle={/S/U/W 1},pdfnewwindow=true",
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error running pandoc on {input_path}: {e}')
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
        print(f'Getting file directory relative to root for {file_path}')
        file_dir_rel_to_root = (PROJECT_ROOT / file_path).parent
        print(f'Got {file_dir_rel_to_root}')

        def link_replacer(match: re.Match) -> str:
            if match.group(1) is not None:
                link_text = match.group(1)
                raw_path = str(match.group(2).lstrip('/'))

                if file_dir_rel_to_root != Path("."):
                    root_path = file_dir_rel_to_root / raw_path
                else:
                    root_path = Path(raw_path)
                return f"[{link_text}]({root_path.as_posix()})"
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

        with NamedTemporaryFile(mode="w+", suffix=".md", delete=False, encoding="utf-8") as tnf:
            tnf.write(sanitize_markdown(content, input_path, mode))
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
        help="Input markdown file path",
        type=str,
        default=""
    )
    args = parser.parse_args()

    if args.input:
        markdown_to_pdf(Path(args.input), ConversionType.SINGLE_FILE)
