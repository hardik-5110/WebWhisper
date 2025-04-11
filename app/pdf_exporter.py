from weasyprint import HTML, CSS
import markdown2

def export_chat_to_pdf(chat_log: str, output_file="chat_output.pdf"):
    html_content = markdown2.markdown(chat_log)
    css = CSS(string="body { text-align: justify; font-family: Arial, sans-serif; }")
    HTML(string=html_content).write_pdf(output_file, stylesheets=[css])
