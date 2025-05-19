# homaker

A command-line tool to convert worksheets to handouts by merging two pages onto one A4 page and adding header/footer information with course details.

## Features

- Merges two worksheet pages onto a single handout page
- Adds customized headers and footers with:
  - Course information
  - Page numbers
  - Instructor name and institution
  - Current year
- Automatically processes all worksheet PDFs in the current directory and subdirectories
- Works cross-platform on macOS and Linux

## Requirements

- Python 3.8 or higher
- PyMuPDF (installed automatically with the package)
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

### Command Line

After installation, you can run the tool from any directory:

```bash
# Process all worksheets in current directory and subdirectories
homaker
```

### Using the Script File

For convenience, you can also use the included `homaker.command` script:

1. Double-click the `homaker.command` file in your file explorer
2. The script will automatically:
   - Run homaker in the directory where the script is located
   - Display progress information
   - Close automatically after completion

## How It Works

The tool will:

1. Find all PDF files with "-Worksheet" in the name
2. Merge pages two-by-two onto A4 pages
3. Add a frame with horizontal lines
4. Add header and footer information including:
   - Course information (OM Week X - Part Y)
   - Page numbers
   - Instructor name and institution
   - Current year
5. Save the output as a new PDF with "Handout" instead of "Worksheet" in the filename

## File Naming

For best results, name your worksheets in the format:

```
[Week]-[Part]-Worksheet.pdf
```

Example: `5-2-Worksheet.pdf` for week 5, part 2.

The week and part numbers are extracted from the filename and used in the header of the generated handout.

## License

MIT