import os
import re
import json
import base64
from bs4 import BeautifulSoup

def extract_raw_text_from_mhtml(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find quoted-printable or HTML parts
    html_parts = re.findall(r'Content-Type:\s*text/html.*?\n\n(.*?)(?=\n------=|\Z)', content, re.DOTALL)
    full_text = ""
    for part in html_parts:
        # Decode quoted printable
        decoded = re.sub(r'=\n', '', part)
        decoded = re.sub(r'=([0-9A-Fa-f]{2})', lambda m: chr(int(m.group(1), 16)), decoded)
        soup = BeautifulSoup(decoded, 'html.parser')
        full_text += soup.get_text(separator=' ') + "\n"

    if not full_text:
        soup = BeautifulSoup(content, 'html.parser')
        full_text = soup.get_text(separator=' ')

    return full_text

def chunk_text(text, max_chars=4000):
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 30]
    chunks = []
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) > max_chars:
            chunks.append(current_chunk)
            current_chunk = p
        else:
            current_chunk += "\n" + p
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

if __name__ == "__main__":
    t1 = extract_raw_text_from_mhtml("drifting_logs/Dryf psychogeograficzny")
    t2 = extract_raw_text_from_mhtml("drifting_logs/Stwórz dryft Belfort Lure")
    print(f"Log 1 raw extracted length: {len(t1)} chars")
    print(f"Log 2 raw extracted length: {len(t2)} chars")
    c1 = chunk_text(t1)
    c2 = chunk_text(t2)
    print(f"Log 1 chunks: {len(c1)}, Log 2 chunks: {len(c2)}")
