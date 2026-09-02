#!/usr/bin/env python3
import os
import sys
import email
import subprocess
import tempfile

def convert_mhtml_to_pdf(mhtml_path, pdf_path):
    print(f"Converting '{mhtml_path}' -> '{pdf_path}'...")
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

    try:
        cmd = [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path}",
            tmp_html_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            print(f"Successfully generated {pdf_path} (size: {os.path.getsize(pdf_path)} bytes)")
            return True
        else:
            print(f"Chrome failed to generate PDF. Error: {res.stderr.decode()}")
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
