#!/usr/bin/env python3
import os
import sys
import email
import tempfile
from playwright.sync_api import sync_playwright

def convert_mhtml_to_pdf(mhtml_path, pdf_path):
    print(f"Converting '{mhtml_path}' -> '{pdf_path}' with high-contrast print styling...")
    if not os.path.exists(mhtml_path):
        raise FileNotFoundError(f"Source file {mhtml_path} not found.")

    with open(mhtml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)

    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True)
            break

    if not html_content:
        raise ValueError(f"No HTML part found in {mhtml_path}")

    with tempfile.NamedTemporaryFile('wb', suffix='.html', delete=False) as tmp:
        tmp.write(html_content)
        tmp_html_path = tmp.name

    inject_css = """
    @media print {
        html, body, main, div, section, article, p, span, h1, h2, h3, h4, li {
            color: #111111 !important;
            background-color: #ffffff !important;
        }
        * {
            box-shadow: none !important;
            text-shadow: none !important;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            font-size: 11pt !important;
            line-height: 1.5 !important;
        }
    }
    """

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page()
            page.goto(f"file://{tmp_html_path}", wait_until="load")
            page.add_style_tag(content=inject_css)
            page.wait_for_timeout(1000)
            page.pdf(
                path=pdf_path,
                format="A4",
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                print_background=False
            )
            browser.close()

        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            print(f"Successfully generated {pdf_path} (size: {os.path.getsize(pdf_path)} bytes)")
            return True
        else:
            print(f"Failed to generate {pdf_path}")
            return False
    finally:
        if os.path.exists(tmp_html_path):
            os.remove(tmp_html_path)

def main():
    target_files = [
        ("drifting_logs/Dryf psychogeograficzny", "drifting_logs/Dryf psychogeograficzny.pdf"),
        ("drifting_logs/Stwórz dryft Belfort Lure", "drifting_logs/Stwórz dryft Belfort Lure.pdf")
    ]
    for src, dst in target_files:
        convert_mhtml_to_pdf(src, dst)

if __name__ == "__main__":
    main()
