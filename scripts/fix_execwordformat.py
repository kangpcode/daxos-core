#!/usr/bin/env python3
from pathlib import Path
import re

INDEX_HTML = Path("src/ui/desktop_preview/index.html")
text = INDEX_HTML.read_text(encoding="utf-8")

# Fix all execWordFormat calls
replacements = [
    ("execWordFormat('bold\\')", "execWordFormat('bold')"),
    ("execWordFormat('italic\\')", "execWordFormat('italic')"),
    ("execWordFormat('underline\\')", "execWordFormat('underline')"),
    ("execWordFormat('justifyLeft\\')", "execWordFormat('justifyLeft')"),
    ("execWordFormat('justifyCenter\\')", "execWordFormat('justifyCenter')"),
    ("execWordFormat('justifyRight\\')", "execWordFormat('justifyRight')"),
    ("execWordFormat('justifyFull\\')", "execWordFormat('justifyFull')"),
    ("execWordFormat('insertUnorderedList\\')", "execWordFormat('insertUnorderedList')"),
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        print(f"Replaced: {old} -> {new}")

INDEX_HTML.write_text(text, encoding="utf-8")
print("Done fixing execWordFormat.")
