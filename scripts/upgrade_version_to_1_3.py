#!/usr/bin/env python3
"""
System-wide version upgrade script for DAXOS:
From: 1.10.2026 (Rhino Alpha)
To:   1.10.2026 (Rhino Alpha)
Lead Architect: Dhafa Nazula Permadi (@kangpcode)
"""

import os
from pathlib import Path

ROOT = Path("/home/kangpcode/wwwsite/daxos")

TARGET_EXTS = {".rs", ".toml", ".py", ".sh", ".html", ".md", ".cfg"}
EXCLUDE_DIRS = {"target", ".git", ".agents", "venv", "__pycache__"}

def upgrade_version():
    replaced_count = 0
    modified_files = []

    for root, dirs, files in os.walk(ROOT):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            path = Path(root) / file
            if path.suffix in TARGET_EXTS or file in {"grub.cfg", "manifest.toml"}:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    continue

                if "1.10.2026" in content:
                    new_content = content.replace("1.10.2026", "1.10.2026")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    replaced_count += content.count("1.10.2026")
                    modified_files.append(str(path.relative_to(ROOT)))

    print(f"[OK] Replaced {replaced_count} occurrences of 1.10.2026 with 1.10.2026 across {len(modified_files)} files.")

if __name__ == "__main__":
    upgrade_version()
