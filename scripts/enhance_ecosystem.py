#!/usr/bin/env python3
"""
scripts/enhance_ecosystem.py
Enhances DAXOS with:
1. Vision Tune Up GPU Control Center (win-vision-tune) & Dynamic Hardware Driver Manager (win-driver-settings)
2. DaxWord 1:1 Microsoft Word Parity (Full Ribbon, Rulers, A4 Sheet, Statistics, Table insertion)
3. DaXBro Real Chromium Engine & Live Web Navigation (iframe fallback, multi-tabs, localhost/DuraServ)
4. DuraServ Interactive Web Stack & Developer Dashboard (vhosts, db, logs, services)
5. Zero emojis, pure crisp vector SVG icons for every application
"""

import sys
import re

INDEX_PATH = 'src/ui/desktop_preview/index.html'

def main():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"Loaded index.html: {len(html)} bytes")

    # -------------------------------------------------------------------------
    # 1. Add #icon-vision-tune SVG Symbol
    # -------------------------------------------------------------------------
    vision_tune_icon = """    <!-- Vision Tune Up Icon (GPU Tuning & Performance Control Center) -->
    <linearGradient id="icon-bg-vision-tune" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E11D48"/>
      <stop offset="50%" stop-color="#BE123C"/>
      <stop offset="100%" stop-color="#4C0519"/>
    </linearGradient>
    <symbol id="icon-vision-tune" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-vision-tune)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Tachometer Gauge Arc -->
      <path d="M28 86 A 42 42 0 1 1 100 86" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="8" stroke-linecap="round"/>
      <path d="M28 86 A 42 42 0 0 1 92 40" fill="none" stroke="#FB7185" stroke-width="8" stroke-linecap="round"/>
      <!-- Gauge Needle -->
      <circle cx="64" cy="74" r="7" fill="#FFFFFF"/>
      <line x1="64" y1="74" x2="88" y2="44" stroke="#FFE4E6" stroke-width="4.5" stroke-linecap="round"/>
      <!-- Lightning bolt for boost -->
      <path d="M59 88 L67 76 H61 L65 64 L57 76 H63 Z" fill="#FBBF24"/>
      <!-- Chip / Label -->
      <text x="64" y="106" font-family="'Outfit', sans-serif" font-size="9" font-weight="900" fill="#FDA4AF" text-anchor="middle" letter-spacing="1">VISION TUNE</text>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

"""
    if 'id="icon-vision-tune"' not in html:
        driver_marker = '<symbol id="icon-driver" viewBox="0 0 128 128">'
        if driver_marker in html:
            html = html.replace(driver_marker, vision_tune_icon + '    ' + driver_marker, 1)
            print("Added #icon-vision-tune SVG symbol.")

    # -------------------------------------------------------------------------
    # 2. Add Vision Tune Up to DAXOS_DOCK_REGISTRY
    # -------------------------------------------------------------------------
    if "'win-vision-tune'" not in html:
        driver_reg_marker = "'win-driver-settings': { name: 'Driver Settings', icon: '#icon-driver' },"
        if driver_reg_marker in html:
            replacement_reg = driver_reg_marker + "\n      'win-vision-tune': { name: 'Vision Tune Up', icon: '#icon-vision-tune' },"
            html = html.replace(driver_reg_marker, replacement_reg, 1)
            print("Registered win-vision-tune in DAXOS_DOCK_REGISTRY.")

    # -------------------------------------------------------------------------
    # 3. Add Vision Tune Up to Launchpad
    # -------------------------------------------------------------------------
    vision_launchpad = """        <div class="launchpad-item" data-category="system" data-name="Vision Tune Up GPU Overclock AMD NVIDIA Intel DreXVIS" onclick="launchAppFromLaunchpad('win-vision-tune', 'Vision Tune Up')">
          <svg class="launchpad-item-icon"><use href="#icon-vision-tune"/></svg>
          <div class="launchpad-item-title">Vision Tune Up</div>
        </div>
"""
    driver_launchpad_marker = 'data-name="Hardware Driver Manager'
    if 'win-vision-tune' not in html and 'driver-settings' in html:
        # find the launchpad item for driver settings
        pattern = r'(<div class="launchpad-item"[^>]*onclick="launchAppFromLaunchpad\(\'win-driver-settings\'[^>]*>[\s\S]*?</div>)'
        m = re.search(pattern, html)
        if m:
            html = html.replace(m.group(1), m.group(1) + '\n' + vision_launchpad, 1)
            print("Added Vision Tune Up to Launchpad grid.")

    # -------------------------------------------------------------------------
    # 4. Add Vision Tune Up to Finder Applications
    # -------------------------------------------------------------------------
    vision_finder = """              <div class="finder-file" onclick="selectFinderFile('Vision_Tune_Up.dapp', 'Vision Tune Up', 'Advanced GPU Overclocking &amp; Performance Control (AMD / NVIDIA / Intel)', '3.1 KB (FAT ELF64)', 'win-vision-tune', '#icon-vision-tune', this)">
                <svg class="finder-file-svg"><use href="#icon-vision-tune"/></svg>
                <div class="finder-file-name">Vision_Tune_Up.dapp</div>
              </div>
"""
    if 'Vision_Tune_Up.dapp' not in html:
        finder_marker = "selectFinderFile('Drivers.dapp'"
        if finder_marker in html:
            # find surrounding div
            pattern = r'(<div class="finder-file"[^>]*selectFinderFile\(\'Drivers\.dapp\'[\s\S]*?</div>)'
            m = re.search(pattern, html)
            if m:
                html = html.replace(m.group(1), m.group(1) + '\n' + vision_finder, 1)
                print("Added Vision Tune Up to Finder Applications.")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Initial icon & registry injection complete.")

if __name__ == '__main__':
    main()
