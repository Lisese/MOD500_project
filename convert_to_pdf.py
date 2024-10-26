import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os
import sys
import logging
import contextlib

class SuppressAllOutput:
    """Context manager to suppress all output including GLib/GTK warnings"""
    def __init__(self):
        # Open null device
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for _ in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors
        self.save_fds = [os.dup(1), os.dup(2)]
        # Save original logging level
        self.log_level = logging.root.getEffectiveLevel()
        # Set environment variables to suppress GTK warnings
        self.old_environ = dict(os.environ)
        os.environ.update({
            'GTK_DEBUG': '',
            'GDK_DEBUG': '',
            'G_DEBUG': '',
            'G_MESSAGES_DEBUG': '',
            'G_ENABLE_DIAGNOSTIC': '0'
        })

    def __enter__(self):
        # Assign the null pointers to stdout and stderr
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)
        # Suppress Python-level output
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        # Suppress all logging
        logging.root.setLevel(logging.CRITICAL + 1)
        # Create null handler for GLib warnings
        logging.getLogger('weasyprint').setLevel(logging.CRITICAL + 1)
        null_handler = logging.NullHandler()
        logging.getLogger('weasyprint').addHandler(null_handler)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            try:
                os.close(fd)
            except:
                pass
        # Restore Python-level output
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        # Restore logging
        logging.root.setLevel(self.log_level)
        # Restore environment
        os.environ.clear()
        os.environ.update(self.old_environ)

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

    try:
        # Generate PDF with all output suppressed
        with SuppressAllOutput():
            font_config = FontConfiguration()
            HTML(string=html_content).write_pdf(pdf_file, stylesheets=[css], font_config=font_config)
        print(f"PDF generated: {pdf_file}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    markdown_file = "decision_analysis_report.md"
    pdf_file = "decision_analysis_report.pdf"
    markdown_to_pdf(markdown_file, pdf_file)
