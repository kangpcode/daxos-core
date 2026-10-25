#!/usr/bin/env python3
from pathlib import Path

index_html = Path("src/ui/desktop_preview/index.html")
content = index_html.read_text(encoding="utf-8")

# Fix line: info.innerHTML = ;
bad_str = "info.innerHTML = ;"
good_str = 'info.innerHTML = "Glif: <b style=\\"color: #FFFFFF; font-size: 14px;\\">" + ch + "</b> | Unicode: <b>U+" + codePoint + "</b> (Disalin)";'

if bad_str in content:
    content = content.replace(bad_str, good_str)
    print("Fixed bad_str in glyph info")

# Check other broken strings
content = content.replace("sub.innerText = ` •  • `;", "sub.innerText = `${f.designer} • ${f.license} • ${f.version}`;")
content = content.replace("document.getElementById(`tab-btn-`);", "document.getElementById('tab-btn-' + t);")
content = content.replace("document.getElementById(`tab-view-`);", "document.getElementById('tab-view-' + t);")
content = content.replace("showDockToast(`Font  berhasil dipasang ke sistem DAXOS!`);", "showDockToast('Font ' + fontName + ' berhasil dipasang ke sistem DAXOS!');")
content = content.replace("showDockToast(`Tipografi:  | `);", "showDockToast('Tipografi: ' + aa + ' | ' + hint);")

index_html.write_text(content, encoding="utf-8")
print("Successfully cleaned up font JS in index.html")
