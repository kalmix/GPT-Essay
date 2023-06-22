import os
import re
from fpdf import FPDF


def sanitize_filename(filename):
    # Remove special characters, except whitespace and hyphens
    sanitized_name = re.sub(r'[^\w\s-]', '', filename)

    # Replace whitespace with underscores
    sanitized_name = sanitized_name.replace(' ', '_')

    # Trim leading and trailing whitespace
    sanitized_name = sanitized_name.strip()

    # Limit the filename to 10 words or less
    words = sanitized_name.split('_')
    if len(words) > 10:
        sanitized_name = '_'.join(words[:10])

    return sanitized_name


def save_essay_as_pdf(essay, first_line):
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.page_has_header = False

        def header(self):
            if self.page_no() == 1:
                self.page_has_header = True
                self.set_font('Arial', 'B', 16)
                self.cell(0, 10, first_line, 0, 1, 'C')

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'{self.page_no()}', 0, 0, 'C')

        def header_on_page(self):
            return self.page_has_header

    # Create the PDF folder if it doesn't exist
    output_folder = "PDF"
    os.makedirs(output_folder, exist_ok=True)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, essay.encode('utf-8').decode('latin-1'))
    filename = sanitize_filename(first_line) + ".pdf"
    output_path = os.path.join(output_folder, filename)
    pdf.output(output_path)

    return output_path
