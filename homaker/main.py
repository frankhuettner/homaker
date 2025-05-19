import fitz  # PyMuPDF
from datetime import date
import os
import re
from pathlib import Path
import sys


# Define A4 dimensions and Satzspiegel margins (in points, 1 point = 1/72 inch)
A4_WIDTH, A4_HEIGHT = 595, 842
left_margin, top_margin = 14, 14
right_margin, bottom_margin = 14, 20


def load_custom_font():
    # Get user's home directory in a cross-platform way
    home = str(Path.home())

    # Define font paths for different operating systems
    font_paths = {
        "linux": ".local/share/fonts/LexendDeca-SemiBold.ttf",
        "darwin": "Library/Fonts/LexendDeca-SemiBold.ttf",
    }

    # Get current OS
    current_os = sys.platform

    # Get the appropriate path based on OS
    if current_os == "darwin":  # macOS
        font_path = os.path.join(home, font_paths["darwin"])
    else:  # Linux
        font_path = os.path.join(home, font_paths["linux"])

    return fitz.Font(fontfile=font_path)


def merge_pages(doc, page_numbers):
    # Get the pages to merge
    page1 = doc[page_numbers[0]]
    page2 = doc[page_numbers[1]]

    # A4 dimensions in points (1 inch = 72 points)
    A4_WIDTH = 595.276  # 210 mm
    A4_HEIGHT = 841.890  # 297 mm

    # Create a new document for output
    output_doc = fitz.open()

    # Create a new page with A4 dimensions
    new_page = output_doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)

    # Define margins
    MARGIN = 10  # 10 points margin

    # Calculate dimensions for each slide on A4 with margins
    slide_height = (A4_HEIGHT - 3 * MARGIN) / 2  # 3 margins: top, middle, and bottom
    slide_width = A4_WIDTH - 2 * MARGIN  # 2 margins: left and right

    # Merge the pages
    new_page.show_pdf_page(
        fitz.Rect(MARGIN, MARGIN, A4_WIDTH - MARGIN, slide_height + MARGIN),
        doc,
        page_numbers[0],
        keep_proportion=True,
    )
    new_page.show_pdf_page(
        fitz.Rect(MARGIN, slide_height + MARGIN, A4_WIDTH - MARGIN, A4_HEIGHT - MARGIN),
        doc,
        page_numbers[1],
        keep_proportion=True,
    )
    return output_doc


def create_output_doc(doc):
    output_doc = fitz.open()
    for i in range(0, len(doc), 2):
        if i + 1 < len(doc):
            merged_page_doc = merge_pages(doc, (i, i + 1))
            output_doc.insert_pdf(merged_page_doc)
    return output_doc


def add_frame(page):
    # Define line positions
    top_line_y = 1.8 * top_margin
    bottom_line_y = A4_HEIGHT - 1.6 * bottom_margin

    # Draw top horizontal line
    page.draw_line(
        fitz.Point(left_margin + 14, top_line_y),
        fitz.Point(A4_WIDTH - right_margin - 11, top_line_y),
        color=(0.6, 0.6, 0.6),
        width=0.5,
    )

    # Draw bottom horizontal line
    page.draw_line(
        fitz.Point(left_margin + 14, bottom_line_y),
        fitz.Point(A4_WIDTH - right_margin - 11, bottom_line_y),
        color=(0.6, 0.6, 0.6),
        width=0.5,
    )


def add_text(page, number_of_pages, week, part):
    # Load the custom font
    custom_font = load_custom_font()
    fontsize = 12

    # Create a new text writer
    tw = fitz.TextWriter(page.rect)

    # Set text color (light gray)
    text_color = (0.6, 0.6, 0.6)

    # Add text
    current_year = date.today().strftime("%Y")

    # Top left text
    text = f"Handout | OM {week} - {part}"
    tw.append((left_margin + 14, 22), text, fontsize=fontsize, font=custom_font)

    # Top right text (page number)
    text_page_number = f"[Page {page.number + 1}/{number_of_pages}]"
    text_width = custom_font.text_length(text_page_number, fontsize=fontsize)
    tw.append(
        (A4_WIDTH - right_margin - text_width - 11, 22),
        text_page_number,
        fontsize=fontsize,
        font=custom_font,
    )

    # Bottom left text
    text_bottom_left = f"Frank Huettner | SKK GSB"
    tw.append(
        (left_margin + 14, A4_HEIGHT - bottom_margin),
        text_bottom_left,
        fontsize=fontsize,
        font=custom_font,
    )

    # Bottom right text
    text_bottom = f"[{current_year}]"
    text_width = custom_font.text_length(text_bottom, fontsize=fontsize)
    tw.append(
        (A4_WIDTH - right_margin - text_width - 11, A4_HEIGHT - bottom_margin),
        text_bottom,
        fontsize=fontsize,
        font=custom_font,
    )

    # Write all the text to the page
    tw.write_text(page, color=text_color)


def process_document(input_filename, output_filename):
    input_doc = fitz.open(input_filename)
    output_doc = create_output_doc(input_doc)

    # Extract week and part from filename
    match = re.match(r"(?:.*/)?((\d+)(?:-(\d+))?-Worksheet)", input_filename)
    if match:
        week = int(match.group(2))
        part = (
            int(match.group(3)) if match.group(3) else 1
        )  # Changed from group(2) to group(3)
    else:
        week, part = 1, 1  # Default values if not found in filename

    number_of_pages = len(output_doc)
    for page in output_doc:
        add_frame(page)
        add_text(page, number_of_pages, week, part)

    output_doc.save(output_filename)
    input_doc.close()
    print(f"Processed {input_filename} -> {output_filename}")


def process_all_worksheets():
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk("."):
        # Filter PDF files with "-Worksheet" in the name
        pdf_files = [
            f for f in files if f.lower().endswith(".pdf") and "-worksheet" in f.lower()
        ]

        for pdf_file in pdf_files:
            input_filename = os.path.join(root, pdf_file)
            # Create output filename by replacing "Worksheet" with "Handout"
            output_filename = os.path.join(
                root,
                pdf_file.replace("Worksheet", "Handout").replace(
                    "worksheet", "Handout"
                ),
            )
            process_document(input_filename, output_filename)


# Main execution
def main():
    process_all_worksheets()


if __name__ == "__main__":
    main()