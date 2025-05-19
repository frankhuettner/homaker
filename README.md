# homaker

A command-line tool to convert worksheets to handouts by merging two pages onto one A4 page and adding header/footer information.

## Features

- Merges two worksheet pages onto a single handout page
- Adds customized headers and footers with course information and page numbers
- Automatically processes all worksheet PDFs in the current directory and subdirectories
- Works on macOS and Linux

## Requirements

- Python 3.8 or higher
- LexendDeca-SemiBold.ttf font installed in your system fonts:
  - macOS: `~/Library/Fonts/LexendDeca-SemiBold.ttf`
  - Linux: `~/.local/share/fonts/LexendDeca-SemiBold.ttf`

## Installation

```bash
# Install with uv (recommended)
uv tool install -e /path/to/homaker

# Or with pip
pip install -e /path/to/homaker
```

## Usage

After installation, you can run the tool from anywhere:

```bash
# Process all worksheets in current directory and subdirectories
homaker
```

The tool will:

1. Find all PDF files with "-Worksheet" in the name
2. Merge pages two-by-two onto A4 pages
3. Add header and footer information including:
   - Course information
   - Page numbers
   - Your name
   - Current year
4. Save the output as a new PDF with "Handout" instead of "Worksheet" in the filename

## File Naming

For best results, name your worksheets in the format:

```
[Week]-[Part]-Worksheet.pdf
```

Example: `5-2-Worksheet.pdf` for week 5, part 2.

## License

MIT