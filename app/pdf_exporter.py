from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap

def export_text_to_pdf(text, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Margin and line height
    x_margin = 50
    y_margin = 50
    line_height = 14

    # Wrap text to fit page width
    max_width = int((width - 2 * x_margin) / 7)  # 7 = char width approximation
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=max_width))
        lines.append("")  # Paragraph spacing

    # Draw lines
    y = height - y_margin
    for line in lines:
        if y < y_margin:
            c.showPage()
            y = height - y_margin
        c.drawString(x_margin, y, line)
        y -= line_height

    c.save()


