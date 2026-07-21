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

    # Get the parent directory for this markdown file. Example:
    # 6.004/index.md -> PROJECT_ROOT / 6.004
    # In directory conversion mode or global conversion mode,
    # This will still point to the right parent directory
    # since the named temp file to store the markdown contents
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
            # In single file conversion mode just remove the link and return
            # the normal text.
            if mode == ConversionType.SINGLE_FILE:
                return link_text
            # In directory conversion mode, check if the link points to a file
            # in the same directory. If so, convert it. If not, remove it.
            elif mode == ConversionType.DIRECTORY:
                link_parent_directory = match.group(4).split('/')[0]
                link_path_after_directory = '/'.join(match.group(4).split('/')[1:])
                if link_path_absolute.is_relative_to(file_dir_rel_to_root):
                    # The link points to a file in the same directory. Open the file
                    # to extract the first H1 in the file and return that link. This
                    # assumes that all Markdown files start with an H1, which sounds
                    # like an OK assumption.
                    return f"[{link_text}]({link_path.as_posix()})"
                return link_text
            # We should always be able to convert links in global mode.
            else:
                assert mode == ConversionType.GLOBAL
                return f"[{link_text}]({(PROJECT_ROOT / link_path).as_posix()})"

    return link_regex.sub(link_replacer, content)


def get_ordered_markdown_files(directory: Path) -> list[Path]:
    """
    Return a list of markdown files in the directory, ordered by the natural sort
    order instead of the strict alphabetical order. Example: lec2.md is returned before
    lec10.md
    :param directory: The directory to search for markdown files (recurses into subdirectories)
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
        if child.is_file() and child.suffix == ".md" and child.name != "index.md":
            files.append(child)

    # Recurse into subdirectories using natural sorting
    for child in children:
        if child.is_dir():
            files.extend(get_ordered_markdown_files(child))

    return files


def get_markdown_for_directory(input_path: Path, mode: ConversionType) -> str:
    """
    Returns the combined content for all markdown files in the passed `input_path`.
    First appends the contents of `index.md` if present, then the sanitized content
    of all markdown files in the current directory (in natural alphabetical order),
    then recursively gets content for subdirectories.
    :param input_path: The directory to search for markdown files
    :param mode: The conversion mode
    :return: Valid markdown contents as a string
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


def markdown_to_pdf(input_path: Path | None, mode: ConversionType) -> None:
    """
    Reads a markdown file or directory containing markdown files and
    correctly converts it into a PDF depending on `mode`
    :param input_path: Can be a path to a single markdown file or a directory.
        If `mode` is `ConversationType.SINGLE_FILE`, `input_path` must be a path to
        a single file. If `mode` is `ConversationType.DIRECTORY`, `input_path` must be
        a path to a directory containing an index.md file. If `mode` is
        `ConversationType.GLOBAL`, `input_path` must be None.
    :param mode: The type of PDF file being generated. If mode is `ConversionType.SINGLE_FILE`,
        converts a single file from Markdown to PDF. If mode is `ConversionType.DIRECTORY`,
        combines the content of all the markdown files in the `input_path` directory (recursively
        visiting subdirectories) and generates one PDF from the combined content. If mode is
        `ConversionType.GLOBAL`, does the same operation as directory level conversion, but at
        the project root level.
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
                    updated_front_matter = re.sub(r"(^title:\s*)(.*)$", r"\1" + index_title + r" \2", front_matter, flags=re.MULTILINE)
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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        help="Path to the markdown file or directory containing markdown files. An index.md must be present if passing a directory.",
        type=str,
        nargs="*",
        default=""
    )
    parser.add_argument(
        '--test',
        help="Test the build script by running on the test/ directory",
        action="store_true"
    )
    args = parser.parse_args()

    if args.test:
        print('Testing')

    if args.input:
        for path in args.input:
            ip_path = Path(path)
            if not ip_path.exists():
                print(f"Input path {path} does not exist")
                sys.exit(1)

            if ip_path.is_dir():
                markdown_to_pdf(ip_path, ConversionType.DIRECTORY)
            elif ip_path.is_file():
                markdown_to_pdf(ip_path, ConversionType.SINGLE_FILE)
