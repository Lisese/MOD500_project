import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def markdown_to_pdf(markdown_file, pdf_file):
    # Read the Markdown file
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra'])

    # Create a simple CSS for better formatting
    css = CSS(string='''
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        h1, h2, h3 { color: #2c3e50; }
        code { background: #f4f4f4; border: 1px solid #ddd; border-radius: 4px; padding: 2px 5px; }
        img { max-width: 100%; height: auto; }
    ''')

    # Generate PDF
    font_config = FontConfiguration()
    HTML(string=html_content).write_pdf(pdf_file, stylesheets=[css], font_config=font_config)

    print(f"PDF generated: {pdf_file}")

if __name__ == "__main__":
    markdown_file = "decision_analysis_report.md"
    pdf_file = "decision_analysis_report.pdf"
    markdown_to_pdf(markdown_file, pdf_file)
