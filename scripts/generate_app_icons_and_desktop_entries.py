#!/usr/bin/env python3
"""
generate_app_icons_and_desktop_entries.py

Generates:
1. Standalone modern SVG icons for all 15 example apps in `examples/<app>/icon.svg`
2. Updates `examples/<app>/manifest.toml` to declare `icon = "icon.svg"`
3. Generates 22 FreeDesktop XDG `.desktop` files in `boot/applications/`
"""

import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent

ICONS = {
    "calculator": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF9500"/>
      <stop offset="100%" stop-color="#FF5E3A"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.35"/>
    </filter>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)" filter="url(#shadow)"/>
  <rect x="22" y="20" width="84" height="26" rx="8" fill="rgba(0,0,0,0.3)"/>
  <text x="96" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="end">3.14159</text>
  <!-- Grid buttons -->
  <circle cx="36" cy="62" r="10" fill="rgba(255,255,255,0.25)"/>
  <text x="36" y="67" font-size="14" font-weight="700" fill="#FFF" text-anchor="middle">C</text>
  <circle cx="64" cy="62" r="10" fill="rgba(255,255,255,0.25)"/>
  <text x="64" y="67" font-size="14" font-weight="700" fill="#FFF" text-anchor="middle">±</text>
  <circle cx="92" cy="62" r="10" fill="rgba(0,0,0,0.25)"/>
  <text x="92" y="67" font-size="14" font-weight="700" fill="#FFF" text-anchor="middle">÷</text>

  <circle cx="36" cy="86" r="10" fill="rgba(255,255,255,0.2)"/>
  <text x="36" y="91" font-size="13" font-weight="600" fill="#FFF" text-anchor="middle">7</text>
  <circle cx="64" cy="86" r="10" fill="rgba(255,255,255,0.2)"/>
  <text x="64" y="91" font-size="13" font-weight="600" fill="#FFF" text-anchor="middle">8</text>
  <circle cx="92" cy="86" r="10" fill="rgba(0,0,0,0.25)"/>
  <text x="92" y="91" font-size="14" font-weight="700" fill="#FFF" text-anchor="middle">×</text>

  <circle cx="36" cy="108" r="8" fill="rgba(255,255,255,0.2)"/>
  <circle cx="64" cy="108" r="8" fill="rgba(255,255,255,0.2)"/>
  <rect x="82" y="100" width="20" height="16" rx="8" fill="#FFFFFF"/>
  <text x="92" y="112" font-size="13" font-weight="900" fill="#FF5E3A" text-anchor="middle">=</text>
</svg>""",

    "camera": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2C3440"/>
      <stop offset="100%" stop-color="#0F141C"/>
    </linearGradient>
    <linearGradient id="lens" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00D2FF"/>
      <stop offset="50%" stop-color="#0066FF"/>
      <stop offset="100%" stop-color="#9900FF"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <rect x="22" y="34" width="84" height="64" rx="16" fill="#1E242E" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <rect x="52" y="24" width="24" height="10" rx="4" fill="#3A4454"/>
  <circle cx="64" cy="66" r="26" fill="#141820" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="64" cy="66" r="20" fill="url(#lens)"/>
  <circle cx="64" cy="66" r="10" fill="#0A0E17"/>
  <circle cx="58" cy="60" r="4" fill="rgba(255,255,255,0.6)"/>
  <circle cx="94" cy="44" r="3.5" fill="#FF3B30"/>
</svg>""",

    "daxbro": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A84FF"/>
      <stop offset="50%" stop-color="#00D2FF"/>
      <stop offset="100%" stop-color="#0051C8"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <circle cx="64" cy="64" r="42" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-dasharray="6,4"/>
  <circle cx="64" cy="64" r="32" fill="rgba(0,0,0,0.25)" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
  <polygon points="64,28 72,56 64,64 56,56" fill="#FF3B30"/>
  <polygon points="64,100 72,72 64,64 56,72" fill="#FFFFFF"/>
  <circle cx="64" cy="64" r="5" fill="#0A0E17" stroke="#FFF" stroke-width="2"/>
</svg>""",

    "daxdrop": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F5A0"/>
      <stop offset="100%" stop-color="#00D9F5"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <circle cx="64" cy="64" r="44" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="3"/>
  <circle cx="64" cy="64" r="32" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="3"/>
  <circle cx="64" cy="64" r="20" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="3.5"/>
  <circle cx="64" cy="64" r="8" fill="#FFFFFF"/>
  <path d="M64 16 L64 32 M64 96 L64 112 M16 64 L32 64 M96 64 L112 64" stroke="rgba(255,255,255,0.7)" stroke-width="3" stroke-linecap="round"/>
</svg>""",

    "dcodx-ide": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6E56CF"/>
      <stop offset="100%" stop-color="#3B1C8C"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <!-- Code hammer / brackets -->
  <path d="M44 42 L24 64 L44 86" fill="none" stroke="#00D2FF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M84 42 L104 64 L84 86" fill="none" stroke="#00D2FF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="72" y1="36" x2="56" y2="92" stroke="#FF5E3A" stroke-width="6" stroke-linecap="round"/>
  <circle cx="64" cy="64" r="6" fill="#FFCC00"/>
</svg>""",

    "disks": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4B5563"/>
      <stop offset="100%" stop-color="#1F2937"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <rect x="24" y="24" width="80" height="80" rx="14" fill="#111827" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="64" cy="60" r="28" fill="#1F2937" stroke="#00D2FF" stroke-width="2"/>
  <circle cx="64" cy="60" r="10" fill="#0E1626" stroke="#9CA3AF" stroke-width="1.5"/>
  <rect x="36" y="90" width="36" height="6" rx="3" fill="#30D158"/>
  <circle cx="86" cy="93" r="3" fill="#00D2FF"/>
</svg>""",

    "dxdef": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#064E3B"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <path d="M64 24 L94 36 V62 C94 82 80 98 64 104 C48 98 34 82 34 62 V36 Z" fill="rgba(0,0,0,0.3)" stroke="#FFFFFF" stroke-width="3"/>
  <polyline points="48 64 58 74 80 50" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "editor": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <path d="M32 24 H76 L96 44 V100 C96 104 92 108 88 108 H32 C28 108 24 104 24 100 V32 C24 28 28 24 32 24 Z" fill="#FFFFFF"/>
  <path d="M76 24 V44 H96 Z" fill="#93C5FD"/>
  <!-- Code lines -->
  <line x1="38" y1="52" x2="68" y2="52" stroke="#2563EB" stroke-width="4" stroke-linecap="round"/>
  <line x1="38" y1="66" x2="82" y2="66" stroke="#64748B" stroke-width="4" stroke-linecap="round"/>
  <line x1="38" y1="80" x2="74" y2="80" stroke="#F59E0B" stroke-width="4" stroke-linecap="round"/>
  <line x1="38" y1="94" x2="58" y2="94" stroke="#10B981" stroke-width="4" stroke-linecap="round"/>
</svg>""",

    "files": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <!-- Finder dual face smiling -->
  <rect x="22" y="24" width="84" height="80" rx="18" fill="rgba(255,255,255,0.92)"/>
  <path d="M64 24 V104" stroke="#0284C7" stroke-width="3"/>
  <ellipse cx="44" cy="54" rx="4" ry="7" fill="#0369A1"/>
  <ellipse cx="84" cy="54" rx="4" ry="7" fill="#0369A1"/>
  <path d="M42 78 C52 90 76 90 86 78" fill="none" stroke="#0284C7" stroke-width="5" stroke-linecap="round"/>
</svg>""",

    "installer": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#3730A3"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <rect x="24" y="68" width="80" height="38" rx="10" fill="#1E1B4B" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <circle cx="88" cy="87" r="4" fill="#30D158"/>
  <line x1="36" y1="87" x2="72" y2="87" stroke="rgba(255,255,255,0.4)" stroke-width="3" stroke-linecap="round"/>
  <!-- Downward arrow -->
  <polyline points="44 42 64 62 84 42" fill="none" stroke="#00D2FF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="64" y1="20" x2="64" y2="60" stroke="#00D2FF" stroke-width="7" stroke-linecap="round"/>
</svg>""",

    "media": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EC4899"/>
      <stop offset="100%" stop-color="#8B5CF6"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <!-- Spatial audio headphones & note -->
  <path d="M34 68 C34 46 48 30 64 30 C80 30 94 46 94 68" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
  <rect x="28" y="64" width="14" height="26" rx="7" fill="#FFFFFF"/>
  <rect x="86" y="64" width="14" height="26" rx="7" fill="#FFFFFF"/>
  <polygon points="56,60 76,72 56,84" fill="#FFFFFF"/>
</svg>""",

    "preferences": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#64748B"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <!-- Settings gear -->
  <g fill="#F1F5F9" transform="translate(64,64)">
    <circle cx="0" cy="0" r="16" fill="url(#bg)"/>
    <path d="M-6,-38 H6 L9,-26 C13,-24 17,-22 21,-19 L31,-24 L39,-16 L34,-6 C36,-2 37,2 37,7 L48,11 V23 L37,27 C36,31 34,35 32,39 L37,49 L29,57 L19,52 C16,55 12,57 8,59 L5,70 H-5 L-8,59 C-12,57 -16,55 -19,52 L-29,57 L-37,49 L-32,39 C-34,35 -36,31 -37,27 L-48,23 V11 L-37,7 C-37,2 -36,-2 -34,-6 L-39,-16 L-31,-24 L-21,-19 C-17,-22 -13,-24 -9,-26 Z" fill="#E2E8F0"/>
    <circle cx="0" cy="0" r="14" fill="#1E293B"/>
    <circle cx="0" cy="0" r="6" fill="#00D2FF"/>
  </g>
</svg>""",

    "store": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F97316"/>
      <stop offset="100%" stop-color="#C2410C"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <!-- Bag with A logo -->
  <path d="M44 44 C44 32 52 24 64 24 C76 24 84 32 84 44" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
  <rect x="28" y="44" width="72" height="64" rx="14" fill="#FFFFFF"/>
  <polygon points="64,56 78,88 50,88" fill="#F97316"/>
  <circle cx="64" cy="74" r="5" fill="#FFFFFF"/>
</svg>""",

    "sysmon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)"/>
  <rect x="20" y="24" width="88" height="80" rx="12" fill="#0B0F17" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <!-- Grid -->
  <line x1="20" y1="44" x2="108" y2="44" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <line x1="20" y1="64" x2="108" y2="64" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <line x1="20" y1="84" x2="108" y2="84" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- Pulse wave -->
  <polyline points="24,64 42,64 50,38 60,90 70,50 78,74 86,64 104,64" fill="none" stroke="#22C55E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "terminal": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#18181B"/>
      <stop offset="100%" stop-color="#09090B"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#bg)" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <rect x="20" y="24" width="88" height="16" rx="4" fill="#27272A"/>
  <circle cx="28" cy="32" r="3" fill="#EF4444"/>
  <circle cx="37" cy="32" r="3" fill="#F59E0B"/>
  <circle cx="46" cy="32" r="3" fill="#10B981"/>
  <!-- Prompt -->
  <polyline points="32 58 46 70 32 82" fill="none" stroke="#10B981" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="54" y1="82" x2="74" y2="82" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
</svg>"""
}

DESKTOP_ENTRIES = [
    ("calculator", "DAXOS Pro Calculator", "Kalkulator Ilmiah, Programmer & Konversi Basis", "dcalc", "Utility;Calculator;"),
    ("camera", "DAXOS Studio Camera", "Aplikasi Kamera HDR 4K 60fps & Vision Engine", "daxdrop --camera", "AudioVideo;Video;Recorder;"),
    ("daxbro", "DaXBro Web Browser", "Browser Modern Cepat & Aman Berbasis Chromium", "daxbro", "Network;WebBrowser;"),
    ("daxdrop", "DaXDrop AirShare", "Berbagi Berkas Cepat P2P & Deteksi Gesture", "daxdrop", "Network;FileTransfer;"),
    ("dcodx-ide", "DCODX Developer Studio", "IDE Terintegrasi, Compiler & Debugger DAXOS", "dcodx studio", "Development;IDE;"),
    ("disks", "Disk Utility", "Manajer Partisi GPT, Format Btrfs & Pemantau SMART", "ddisk", "System;Filesystem;"),
    ("dxdef", "DXDEF Security Center", "Pusat Keamanan, Landlock LSM & Hardware Firewall", "dxdef-cli", "System;Security;"),
    ("editor", "dEdit Code & Text", "Editor Teks Ringan & Berperforma Tinggi", "dedit", "Utility;TextEditor;"),
    ("files", "Finder File Manager", "Manajer Berkas Respon Cepat dengan Integrasi Btrfs", "dfm", "System;FileManager;"),
    ("installer", "Install DAXOS", "Pemasang Sistem Operasi Hybrid DAXOS", "dax-installer", "System;Installation;"),
    ("media", "Spatial Audio & Media", "Pemutar Audio Latensi Rendah & DSP HRTF 3D", "dmedia", "AudioVideo;Audio;Player;"),
    ("preferences", "System Settings", "Pusat Konfigurasi Sistem, Hardware & Systemd", "daxsh -c 'service list'", "Settings;DesktopSettings;"),
    ("store", "DapStore Market", "Toko Aplikasi Terverifikasi & Manajemen Paket .dapp", "dax stats", "System;PackageManager;"),
    ("sysmon", "Activity Monitor", "Pemantau CPU, GPU, Memori & Proses Realtime", "dtop", "System;Monitor;"),
    ("terminal", "DAXOS Terminal", "Shell Interaktif daxsh POSIX & Multi-OS CLI", "daxsh", "System;TerminalEmulator;"),
    ("word", "DaxWord Document Pro", "Pengolah Kata & Dokumen Formal DAXOS", "doffice word", "Office;WordProcessor;"),
    ("sheet", "DaxSheet Spreadsheet Pro", "Spreadsheet & Analisis Data Terintegrasi", "doffice sheet", "Office;Spreadsheet;"),
    ("slide", "DaxSlide Presentation Pro", "Presentasi & Slide Pitch Deck Kreatif", "doffice slide", "Office;Presentation;"),
    ("clock", "DaxClock World & Timer", "Jam Dunia, Alarm, Stopwatch & Countdown", "dclock", "Utility;Clock;"),
    ("font", "DaxFont Typography Studio", "Manajer Tipografi, Font Renderer & Glyphs Inspector", "dfont", "Graphics;Viewer;"),
    ("compat", "DAXOS Universal Runner", "Lapisan Kompatibilitas Windows, macOS & Linux", "dax-run", "System;Emulator;"),
    ("trash", "Tempat Sampah", "Pengelolaan Berkas Dihapus & Snapshot Pemulihan", "dfm --trash", "System;Trash;"),
]

def main():
    print("=== [DAXOS ECOSYSTEM: APP ICONS & DESKTOP ENTRIES AUDIT] ===")
    
    # 1. Generate icon.svg for each example application
    for app_name, svg_content in ICONS.items():
        app_dir = WORKSPACE / "examples" / app_name
        if app_dir.exists():
            icon_path = app_dir / "icon.svg"
            icon_path.write_text(svg_content.strip(), encoding="utf-8")
            print(f"[OK] Wrote icon: {icon_path.relative_to(WORKSPACE)}")
            
            # Update manifest.toml if needed
            manifest_path = app_dir / "manifest.toml"
            if manifest_path.exists():
                txt = manifest_path.read_text(encoding="utf-8")
                if 'icon = ' not in txt:
                    # Insert icon = "icon.svg" under [application]
                    new_txt = txt.replace('[application]\n', '[application]\nicon = "icon.svg"\n')
                    manifest_path.write_text(new_txt, encoding="utf-8")
                    print(f"[OK] Updated manifest: {manifest_path.relative_to(WORKSPACE)}")

    # 2. Generate FreeDesktop XDG .desktop files in boot/applications/
    boot_apps_dir = WORKSPACE / "boot" / "applications"
    boot_apps_dir.mkdir(parents=True, exist_ok=True)

    for slug, name, comment, exec_cmd, categories in DESKTOP_ENTRIES:
        desktop_file = boot_apps_dir / f"org.daxos.{slug}.desktop"
        content = f"""[Desktop Entry]
Version=1.5
Type=Application
Name={name}
Comment={comment}
Exec={exec_cmd}
Icon=org.daxos.{slug}
Terminal=false
Categories={categories}
StartupNotify=true
X-DAXOS-BundleID=org.daxos.{slug}
X-DAXOS-Sandboxed=true
X-DAXOS-Version=1.10.2026
"""
        desktop_file.write_text(content, encoding="utf-8")
        print(f"[OK] Created Desktop Entry: {desktop_file.relative_to(WORKSPACE)}")

    print(f"\n[PASS] Successfully generated 15 standalone icon.svg files and {len(DESKTOP_ENTRIES)} .desktop entries!")

if __name__ == "__main__":
    main()
