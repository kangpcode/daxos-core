#!/usr/bin/env python3
"""
upgrade_version_to_1_10.py
Upgrades DAXOS from 1.10.2026 (Rhino Alpha) to 1.10.2026 (Rhino Alpha)
in accordance with user roadmap instructions.
"""

import os
from pathlib import Path

WORKSPACE = Path("/home/kangpcode/wwwsite/daxos")

def main():
    print("[1/3] Scanning and updating version strings to 1.10.2026 'Rhino Alpha'...")
    updated_count = 0

    for root, dirs, files in os.walk(WORKSPACE):
        if '/target' in root or '/.git' in root or '/build' in root:
            continue
        for fname in files:
            if not fname.endswith(('.rs', '.toml', '.py', '.sh', '.md', '.html', '.sql', '.surf', '.json')):
                continue
            fpath = Path(root) / fname
            try:
                content = fpath.read_text(encoding='utf-8')
            except Exception:
                continue

            orig = content
            # Replace version strings
            content = content.replace("1.10.2026-ALPHA", "1.10.2026-ALPHA")
            content = content.replace("1.10.2026-Alpha", "1.10.2026-Alpha")
            content = content.replace("1.10.2026 (ALPHA)", "1.10.2026 (ALPHA)")
            content = content.replace("1.10.2026 'Rhino' (ALPHA)", "1.10.2026 'Rhino' (ALPHA)")
            content = content.replace("1.10.2026 'Rhino' (Alpha)", "1.10.2026 'Rhino' (Alpha)")
            content = content.replace("(ALPHA) 'Rhino'", "(ALPHA) 'Rhino'")
            content = content.replace("1.10.2026", "1.10.2026")
            content = content.replace("1_10_2026", "1_10_2026")
            content = content.replace("DAXOS_1_10_2026", "DAXOS_1_10_2026")

            # In about dialog / text if Beta is mentioned
            content = content.replace("Codename: <b>Rhino Alpha</b>", "Codename: <b>Rhino Alpha</b>")
            content = content.replace("Rhino Alpha", "Rhino Alpha")

            if content != orig:
                fpath.write_text(content, encoding='utf-8')
                updated_count += 1
                print(f"  + Updated: {fpath.relative_to(WORKSPACE)}")

    print(f"[SUCCESS] Updated {updated_count} files to DAXOS 1.10.2026 (Codename: Rhino Alpha)!")

if __name__ == "__main__":
    main()
