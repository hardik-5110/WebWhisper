from weasyprint import HTML

def export_text_to_pdf(text, filename):
    # Wrap the text in <pre> to preserve line breaks and spacing
    html_content = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: "Courier New", monospace;
                    padding: 20px;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            {text}
        </body>
    </html>
    """

    HTML(string=html_content).write_pdf(filename)

