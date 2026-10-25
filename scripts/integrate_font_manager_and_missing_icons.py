#!/usr/bin/env python3
"""
integrate_font_manager_and_missing_icons.py
Adds:
1. Missing SVG symbols and gradients (gaming-hub, compat, driver, network, account, app-manager, trans, font, browser, appstore, winapp, macapp, debapp, and system glyphs svg-wifi, svg-battery, etc.)
2. DaxFont (Font Manager & Typography Studio) window markup
3. DaxFont in Dock and Launchpad
4. Binary Translator dedicated icon (#icon-trans)
5. Interactive DaxFont JS controller
"""

import sys
import re

INDEX_HTML = "src/ui/desktop_preview/index.html"

def main():
    print("[1/5] Reading index.html...")
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject SVG Gradients in <defs>
    font_gradients = """
      <!-- New App Gradients (Gaming, Compat, Driver, Network, Account, App-Manager, Trans, Font) -->
      <linearGradient id="icon-bg-gaming-hub" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#4A0E4E"/>
        <stop offset="50%" stop-color="#880E4F"/>
        <stop offset="100%" stop-color="#E91E63"/>
      </linearGradient>
      <linearGradient id="icon-bg-compat" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#1A237E"/>
        <stop offset="50%" stop-color="#3949AB"/>
        <stop offset="100%" stop-color="#7E57C2"/>
      </linearGradient>
      <linearGradient id="icon-bg-driver" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#004D40"/>
        <stop offset="50%" stop-color="#00796B"/>
        <stop offset="100%" stop-color="#00BFA5"/>
      </linearGradient>
      <linearGradient id="icon-bg-network" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#01579B"/>
        <stop offset="50%" stop-color="#0288D1"/>
        <stop offset="100%" stop-color="#00E5FF"/>
      </linearGradient>
      <linearGradient id="icon-bg-account" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#E65100"/>
        <stop offset="50%" stop-color="#F57C00"/>
        <stop offset="100%" stop-color="#FFB74D"/>
      </linearGradient>
      <linearGradient id="icon-bg-app-manager" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#1E1B4B"/>
        <stop offset="50%" stop-color="#4338CA"/>
        <stop offset="100%" stop-color="#818CF8"/>
      </linearGradient>
      <linearGradient id="icon-bg-trans" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#311042"/>
        <stop offset="50%" stop-color="#6200EA"/>
        <stop offset="100%" stop-color="#FF6D00"/>
      </linearGradient>
      <linearGradient id="icon-bg-font" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#880E4F"/>
        <stop offset="50%" stop-color="#C2185B"/>
        <stop offset="100%" stop-color="#EC4899"/>
      </linearGradient>
    """

    if 'id="icon-bg-font"' not in html:
        html = html.replace('<!-- DAXOS SYSTEM VECTOR ICONS & SQUIRCLE DEFINITIONS -->',
                            '<!-- DAXOS SYSTEM VECTOR ICONS & SQUIRCLE DEFINITIONS -->' + font_gradients)
        print("[OK] Injected new app gradients into <defs>")

    # 2. Inject Missing SVG Symbols
    new_symbols = """
    <!-- Gaming Hub Icon (Proton / Vulkan / Direct3D 12) -->
    <symbol id="icon-gaming-hub" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-gaming-hub)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Gamepad Silhouette -->
      <path d="M38 48 C28 48 24 60 24 74 C24 88 34 94 44 94 C50 94 56 90 64 82 C72 90 78 94 84 94 C94 94 104 88 104 74 C104 60 100 48 90 48 C76 48 64 54 64 54 C64 54 52 48 38 48 Z" fill="#FFFFFF" fill-opacity="0.95"/>
      <!-- D-Pad Left -->
      <path d="M40 62 H44 V66 H48 V70 H44 V74 H40 V70 H36 V66 H40 Z" fill="#701A75"/>
      <!-- Action Buttons Right (X Y A B) -->
      <circle cx="86" cy="64" r="3" fill="#EC4899"/>
      <circle cx="92" cy="70" r="3" fill="#3B82F6"/>
      <circle cx="80" cy="70" r="3" fill="#10B981"/>
      <circle cx="86" cy="76" r="3" fill="#F59E0B"/>
      <!-- Proton / Atom Rings -->
      <ellipse cx="64" cy="70" rx="38" ry="14" fill="none" stroke="#F472B6" stroke-width="2" transform="rotate(-25 64 70)"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Universal Apps / Compat Runner Icon (Wine / Darling / Debian) -->
    <symbol id="icon-compat" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-compat)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- 3 Interlocking Ecosystem Rings -->
      <circle cx="50" cy="54" r="22" fill="none" stroke="#60A5FA" stroke-width="6"/>
      <circle cx="78" cy="54" r="22" fill="none" stroke="#C084FC" stroke-width="6"/>
      <circle cx="64" cy="78" r="22" fill="none" stroke="#34D399" stroke-width="6"/>
      <circle cx="64" cy="64" r="6" fill="#FFFFFF"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Driver Settings Icon (DreXVIS GPU / DRM KMS Silicon) -->
    <symbol id="icon-driver" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-driver)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- GPU Microchip Core -->
      <rect x="36" y="36" width="56" height="56" rx="10" fill="#064E3B" stroke="#34D399" stroke-width="4"/>
      <rect x="46" y="46" width="36" height="36" rx="6" fill="#10B981"/>
      <text x="64" y="69" font-family="monospace" font-size="13" font-weight="900" fill="#FFFFFF" text-anchor="middle">GPU</text>
      <!-- Circuit Pin Traces -->
      <line x1="48" y1="26" x2="48" y2="36" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="64" y1="26" x2="64" y2="36" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="80" y1="26" x2="80" y2="36" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="48" y1="92" x2="48" y2="102" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="64" y1="92" x2="64" y2="102" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="80" y1="92" x2="80" y2="102" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="26" y1="48" x2="36" y2="48" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="26" y1="64" x2="36" y2="64" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="26" y1="80" x2="36" y2="80" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="92" y1="48" x2="102" y2="48" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="92" y1="64" x2="102" y2="64" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <line x1="92" y1="80" x2="102" y2="80" stroke="#A7F3D0" stroke-width="4" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Network & DNS Manager Icon (Wi-Fi 7 / DoH / Ethernet) -->
    <symbol id="icon-network" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-network)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Globe Latitudes / Longitudes -->
      <circle cx="64" cy="64" r="38" fill="none" stroke="#FFFFFF" stroke-width="4"/>
      <ellipse cx="64" cy="64" rx="18" ry="38" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="3"/>
      <line x1="26" y1="64" x2="102" y2="64" stroke="rgba(255,255,255,0.7)" stroke-width="3"/>
      <line x1="33" y1="46" x2="95" y2="46" stroke="rgba(255,255,255,0.5)" stroke-width="2.5"/>
      <line x1="33" y1="82" x2="95" y2="82" stroke="rgba(255,255,255,0.5)" stroke-width="2.5"/>
      <!-- Glowing Connection Beacon -->
      <circle cx="64" cy="64" r="7" fill="#00E5FF"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- User Accounts / DaxID Profile Icon -->
    <symbol id="icon-account" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-account)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- User Head & Torso with Golden Shield -->
      <circle cx="64" cy="50" r="18" fill="#FFFFFF"/>
      <path d="M34 94 C34 78 48 74 64 74 C80 74 94 78 94 94 Z" fill="#FFFFFF"/>
      <!-- Biometric Badge Ring -->
      <circle cx="92" cy="40" r="10" fill="#10B981" stroke="#FFFFFF" stroke-width="2.5"/>
      <path d="M88 40 L91 43 L96 37" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- App Manager & Uninstaller Icon -->
    <symbol id="icon-app-manager" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-app-manager)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Application Crate with Manage Badge -->
      <rect x="32" y="38" width="64" height="54" rx="8" fill="none" stroke="#FFFFFF" stroke-width="6"/>
      <line x1="32" y1="56" x2="96" y2="56" stroke="#FFFFFF" stroke-width="5"/>
      <circle cx="48" cy="47" r="3.5" fill="#F472B6"/>
      <circle cx="60" cy="47" r="3.5" fill="#FBBF24"/>
      <circle cx="72" cy="47" r="3.5" fill="#34D399"/>
      <!-- Settings/Gear Accent in Bottom Corner -->
      <circle cx="78" cy="74" r="9" fill="#818CF8" stroke="#FFFFFF" stroke-width="3"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Binary Translator dax-trans Icon (ABI Cross-Compiler) -->
    <symbol id="icon-trans" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-trans)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Architecture Translation Arrows (x86_64 <-> ARM64) -->
      <path d="M34 52 H84 L72 40" fill="none" stroke="#A78BFA" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M94 76 H44 L56 88" fill="none" stroke="#FDBA74" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="26" y="44" width="22" height="16" rx="4" fill="#38BDF8"/>
      <text x="37" y="56" font-family="monospace" font-size="9" font-weight="900" fill="#0C1E3D" text-anchor="middle">x64</text>
      <rect x="80" y="68" width="22" height="16" rx="4" fill="#34D399"/>
      <text x="91" y="80" font-family="monospace" font-size="9" font-weight="900" fill="#064E3B" text-anchor="middle">ARM</text>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaxFont Typography & Font Manager Icon (Rich Magenta Pink Squircle) -->
    <symbol id="icon-font" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-font)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Typographic 'Aa' glyph with Serif & Modern Baseline -->
      <!-- Capital 'A' -->
      <path d="M30 92 L52 36 H62 L84 92 H72 L66 76 H48 L42 92 Z M52 66 H62 L57 50 Z" fill="#FFFFFF"/>
      <!-- Small 'a' -->
      <path d="M90 62 C84 62 78 66 78 74 C78 84 85 88 92 88 C96 88 99 86 101 84 V92 H108 V64 H101 V69 C98 64 95 62 90 62 Z M92 82 C87 82 84 79 84 75 C84 70 87 67 92 67 C96 67 101 70 101 75 C101 79 97 82 92 82 Z" fill="#FCE7F3"/>
      <!-- Typographic Baseline Guides -->
      <line x1="22" y1="92" x2="108" y2="92" stroke="#F472B6" stroke-width="2" stroke-dasharray="3 3"/>
      <line x1="22" y1="36" x2="108" y2="36" stroke="#F472B6" stroke-width="2" stroke-dasharray="3 3"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Helper Compatibility Icons (Browser, AppStore, WinApp, MacApp, DebApp) -->
    <symbol id="icon-browser" viewBox="0 0 128 128">
      <use href="#icon-daxbro"/>
    </symbol>
    <symbol id="icon-appstore" viewBox="0 0 128 128">
      <use href="#icon-dapstore"/>
    </symbol>
    <symbol id="icon-winapp" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="#0078D7"/>
      <path d="M26 36 L58 31 V60 H26 Z M64 30 L102 24 V60 H64 Z M26 66 H58 V96 L26 91 Z M64 66 H102 V104 L64 98 Z" fill="#FFFFFF"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>
    <symbol id="icon-macapp" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="#475569"/>
      <circle cx="64" cy="64" r="38" fill="none" stroke="#FFFFFF" stroke-width="6"/>
      <path d="M46 76 L64 44 L82 76 Z" fill="none" stroke="#38BDF8" stroke-width="6" stroke-linejoin="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>
    <symbol id="icon-debapp" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="#A81D34"/>
      <!-- Debian Swirl -->
      <path d="M64 36 C50 36 40 46 40 58 C40 70 50 80 62 80 C70 80 76 76 78 70 C80 64 76 60 70 60 C64 60 62 64 62 66" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- System Status & UI Vector Glyphs -->
    <symbol id="svg-wifi" viewBox="0 0 24 24">
      <path d="M1 9 C7 3 17 3 23 9 M4 12 C8 7.5 16 7.5 20 12 M7 15 C10 12 14 12 17 15 M12 19 A1.5 1.5 0 1 1 12 18.9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </symbol>
    <symbol id="svg-battery" viewBox="0 0 24 24">
      <rect x="2" y="6" width="18" height="12" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>
      <path d="M22 10 V14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <rect x="4" y="8" width="12" height="8" rx="1.5" fill="#30D158"/>
    </symbol>
    <symbol id="svg-control-center" viewBox="0 0 24 24">
      <rect x="3" y="4" width="18" height="6" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
      <circle cx="8" cy="7" r="2" fill="currentColor"/>
      <rect x="3" y="14" width="18" height="6" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
      <circle cx="16" cy="17" r="2" fill="currentColor"/>
    </symbol>
    <symbol id="svg-spotlight" viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>
      <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </symbol>
    <symbol id="svg-speaker" viewBox="0 0 24 24">
      <polygon points="4,9 8,9 13,5 13,19 8,15 4,15" fill="currentColor"/>
      <path d="M16 8 C18 10 18 14 16 16 M19 5 C22 8.5 22 15.5 19 19" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </symbol>
    <symbol id="svg-shield" viewBox="0 0 24 24">
      <path d="M12 2 L20 5 V11 C20 16 16 20 12 22 C8 20 4 16 4 11 V5 Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      <polyline points="9,11 11,13 15,9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </symbol>
    <symbol id="svg-lock" viewBox="0 0 24 24">
      <rect x="5" y="10" width="14" height="11" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/>
      <path d="M8 10 V6 A4 4 0 0 1 16 6 V10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <circle cx="12" cy="15" r="1.5" fill="currentColor"/>
    </symbol>
    <symbol id="svg-sun" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="2"/>
      <line x1="12" y1="1" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="12" y1="20" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="1" y1="12" x2="4" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="20" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="4.2" y1="4.2" x2="6.4" y2="6.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="17.6" y1="17.6" x2="19.8" y2="19.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="4.2" y1="19.8" x2="6.4" y2="17.6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="17.6" y1="6.4" x2="19.8" y2="4.2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </symbol>
    <symbol id="svg-check" viewBox="0 0 24 24">
      <polyline points="20 6 9 17 4 12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </symbol>
    """

    if 'id="icon-gaming-hub"' not in html:
        html = html.replace('<!-- Launchpad / All Apps Grid Icon (Deep Indigo Squircle) -->',
                            new_symbols + '\n    <!-- Launchpad / All Apps Grid Icon (Deep Indigo Squircle) -->')
        print("[OK] Injected missing SVG symbols for Gaming, Driver, Network, Account, Font, and System Glyphs")

    # 3. Update Binary Translator in Launchpad to use #icon-trans instead of #icon-compat
    html = html.replace(
        '<div class="launchpad-item" data-category="dev" data-name="Binary Translator dax-trans Kompiler AOT JIT ABI Recompiler" onclick="openApp(\'win-terminal\', \'Terminal\'); runTerminal(\'dax-trans --help\'); toggleLaunchpad();">\n          <svg class="launchpad-item-icon"><use href="#icon-compat"/></svg>',
        '<div class="launchpad-item" data-category="dev" data-name="Binary Translator dax-trans Kompiler AOT JIT ABI Recompiler" onclick="openApp(\'win-terminal\', \'Terminal\'); runTerminal(\'dax-trans --help\'); toggleLaunchpad();">\n          <svg class="launchpad-item-icon"><use href="#icon-trans"/></svg>'
    )
    print("[OK] Updated Binary Translator icon to #icon-trans")

    # 4. Inject DaxFont Window Markup
    font_window_markup = """
  <!-- ========================================================================
       DAXFONT TYPOGRAPHY & FONT MANAGER (UBUNTU / MACOS / WINDOWS 11 PARITY)
       ======================================================================== -->
  <div class="window" id="win-daxfont" style="width: 1040px; height: 680px; top: 75px; left: 160px; display: none;">
    <div class="win-resize-handle rh-n"></div>
    <div class="win-resize-handle rh-s"></div>
    <div class="win-resize-handle rh-e"></div>
    <div class="win-resize-handle rh-w"></div>
    <div class="win-resize-handle rh-nw"></div>
    <div class="win-resize-handle rh-ne"></div>
    <div class="win-resize-handle rh-sw"></div>
    <div class="win-resize-handle rh-se"></div>
    <div class="window-header" ondblclick="maximizeWindow('win-daxfont')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeApp('win-daxfont')"></div>
        <div class="traffic-light tl-minimize" onclick="minimizeApp('win-daxfont')"></div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-daxfont')" onmouseenter="showSnapFlyout(event, 'win-daxfont')"></div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 16px; height: 16px;"><use href="#icon-font"/></svg>
        DaxFont - Pengelola Font &amp; Tipografi DAXOS
      </div>
      <div style="display: flex; gap: 8px; margin-left: auto;">
        <button class="win-header-btn" onclick="installFontPrompt()" style="background: rgba(236,72,153,0.25); border: 1px solid rgba(236,72,153,0.4); color: #F472B6; padding: 4px 10px; border-radius: 6px; font-size: 11px; cursor: pointer;">+ Pasang Font Baru</button>
      </div>
    </div>
    <div class="window-content" style="padding: 0; display: flex; flex-direction: row; height: calc(100% - 40px); background: #0B0E14; color: #F3F4F6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      
      <!-- SIDEBAR: Collections -->
      <div style="width: 220px; background: rgba(17, 24, 39, 0.7); border-right: 1px solid rgba(255, 255, 255, 0.08); padding: 14px; display: flex; flex-direction: column; gap: 6px; flex-shrink: 0;">
        <div style="font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">Koleksi Font</div>
        <div class="font-cat-item active" onclick="filterFontCategory('all', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: rgba(236,72,153,0.2); color: #F472B6; font-weight: 600;">
          <span>Semua Font</span><span style="font-size: 11px; opacity: 0.8;">128</span>
        </div>
        <div class="font-cat-item" onclick="filterFontCategory('system', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; color: #D1D5DB;">
          <span>Sistem DAXOS</span><span style="font-size: 11px; opacity: 0.6;">42</span>
        </div>
        <div class="font-cat-item" onclick="filterFontCategory('mono', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; color: #D1D5DB;">
          <span>Monospace / Kode</span><span style="font-size: 11px; opacity: 0.6;">16</span>
        </div>
        <div class="font-cat-item" onclick="filterFontCategory('sans', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; color: #D1D5DB;">
          <span>Sans-Serif</span><span style="font-size: 11px; opacity: 0.6;">38</span>
        </div>
        <div class="font-cat-item" onclick="filterFontCategory('serif', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; color: #D1D5DB;">
          <span>Serif</span><span style="font-size: 11px; opacity: 0.6;">18</span>
        </div>
        <div class="font-cat-item" onclick="filterFontCategory('display', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; color: #D1D5DB;">
          <span>Tampilan / Display</span><span style="font-size: 11px; opacity: 0.6;">14</span>
        </div>
        <div class="font-cat-item" onclick="filterFontCategory('user', this)" style="padding: 8px 12px; border-radius: 6px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; color: #D1D5DB;">
          <span>Font Pengguna</span><span style="font-size: 11px; opacity: 0.6;">12</span>
        </div>

        <div style="margin-top: auto; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 11px; color: #9CA3AF;">
          <div>FreeType: 2.13.2</div>
          <div>HarfBuzz: 8.3.0</div>
          <div>Subpixel: RGB LCD</div>
        </div>
      </div>

      <!-- MIDDLE: Font List -->
      <div style="width: 320px; border-right: 1px solid rgba(255,255,255,0.08); display: flex; flex-direction: column; flex-shrink: 0; background: rgba(15, 23, 42, 0.4);">
        <!-- Search bar -->
        <div style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.08);">
          <input type="text" id="font-search-input" oninput="searchFontCatalog(this.value)" placeholder="Cari nama font, desainer..." style="width: 100%; box-sizing: border-box; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 7px 10px; color: #FFFFFF; font-size: 12px; outline: none;"/>
        </div>
        <!-- Font List Items -->
        <div id="font-items-list" style="overflow-y: auto; flex: 1; padding: 6px;">
          <!-- Item 1: Inter Display -->
          <div class="font-list-card active" onclick="selectFontDetail('Inter Display')" data-category="sans" data-name="Inter Display" style="padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; background: rgba(236,72,153,0.15); border: 1px solid rgba(236,72,153,0.4);">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span style="font-weight: 700; font-size: 14px; color: #FFFFFF;">Inter Display</span>
              <span style="font-size: 11px; color: #F472B6;">7 bobot</span>
            </div>
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 3px; font-family: 'Inter', sans-serif;">The quick brown fox jumps over the lazy dog</div>
          </div>
          <!-- Item 2: JetBrains Mono -->
          <div class="font-list-card" onclick="selectFontDetail('JetBrains Mono')" data-category="mono" data-name="JetBrains Mono" style="padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid transparent;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span style="font-weight: 700; font-size: 14px; color: #FFFFFF;">JetBrains Mono</span>
              <span style="font-size: 11px; color: #10B981;">4 bobot</span>
            </div>
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 3px; font-family: monospace;">fn main() { daxos_boost(240); }</div>
          </div>
          <!-- Item 3: Fira Code -->
          <div class="font-list-card" onclick="selectFontDetail('Fira Code')" data-category="mono" data-name="Fira Code" style="padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid transparent;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span style="font-weight: 700; font-size: 14px; color: #FFFFFF;">Fira Code</span>
              <span style="font-size: 11px; color: #10B981;">2 bobot</span>
            </div>
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 3px; font-family: monospace;">const SLA: f32 = 0.045; // &lt;= 45ms</div>
          </div>
          <!-- Item 4: Playfair Display -->
          <div class="font-list-card" onclick="selectFontDetail('Playfair Display')" data-category="serif" data-name="Playfair Display" style="padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid transparent;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span style="font-weight: 700; font-size: 14px; color: #FFFFFF;">Playfair Display</span>
              <span style="font-size: 11px; color: #F59E0B;">3 bobot</span>
            </div>
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 3px; font-family: Georgia, serif; font-style: italic;">Kemegahan Arsitektur DAXOS Hybrid</div>
          </div>
          <!-- Item 5: Outfit -->
          <div class="font-list-card" onclick="selectFontDetail('Outfit')" data-category="display" data-name="Outfit" style="padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid transparent;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span style="font-weight: 700; font-size: 14px; color: #FFFFFF;">Outfit</span>
              <span style="font-size: 11px; color: #8B5CF6;">3 bobot</span>
            </div>
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 3px; font-family: 'Outfit', sans-serif;">DAXOS 1.10.2026 Rhino: Fast &amp; Fluid</div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Inspector & Previewer -->
      <div style="flex: 1; display: flex; flex-direction: column; overflow-y: auto;">
        <!-- Tab Bar -->
        <div style="display: flex; align-items: center; gap: 8px; padding: 10px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); background: rgba(17, 24, 39, 0.4);">
          <div id="tab-btn-waterfall" onclick="switchFontTab('waterfall')" style="padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; background: rgba(236,72,153,0.25); color: #F472B6;">Air Terjun Ukuran (Waterfall)</div>
          <div id="tab-btn-glyphs" onclick="switchFontTab('glyphs')" style="padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; color: #9CA3AF;">Peta Karakter (Unicode Glyphs)</div>
          <div id="tab-btn-meta" onclick="switchFontTab('meta')" style="padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; color: #9CA3AF;">Detail &amp; Mesin Render</div>
        </div>

        <!-- Content Area -->
        <div style="padding: 20px; flex: 1;" id="font-tab-content">
          <!-- WATERFALL TAB -->
          <div id="tab-view-waterfall">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <div>
                <h2 id="font-active-title" style="margin: 0; font-size: 20px; font-weight: 700; color: #FFFFFF;">Inter Display</h2>
                <div id="font-active-sub" style="font-size: 12px; color: #9CA3AF; margin-top: 2px;">Rasmus Andersson • SIL Open Font License 1.1 • v4.001</div>
              </div>
              <!-- Pangram text input -->
              <input type="text" id="font-custom-pangram" oninput="updateWaterfallPangram(this.value)" value="The quick brown fox jumps over the lazy dog 1234567890" style="width: 320px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px 10px; color: #FFFFFF; font-size: 12px; outline: none;"/>
            </div>

            <!-- Waterfall Lines -->
            <div id="waterfall-container" style="display: flex; flex-direction: column; gap: 14px; padding-bottom: 20px;">
              <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
                <div style="font-size: 11px; color: #F472B6; margin-bottom: 2px;">12pt (Kecil / UI Label)</div>
                <div class="wf-sample" style="font-size: 12px;">The quick brown fox jumps over the lazy dog 1234567890</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
                <div style="font-size: 11px; color: #F472B6; margin-bottom: 2px;">16pt (Teks Bacaan / Paragraf)</div>
                <div class="wf-sample" style="font-size: 16px;">The quick brown fox jumps over the lazy dog 1234567890</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
                <div style="font-size: 11px; color: #F472B6; margin-bottom: 2px;">24pt (Subjudul / Heading 3)</div>
                <div class="wf-sample" style="font-size: 24px;">The quick brown fox jumps over the lazy dog</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
                <div style="font-size: 11px; color: #F472B6; margin-bottom: 2px;">36pt (Judul Artikel / Heading 2)</div>
                <div class="wf-sample" style="font-size: 36px; font-weight: 600;">The quick brown fox jumps</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
                <div style="font-size: 11px; color: #F472B6; margin-bottom: 2px;">48pt (Judul Utama / Banner Hero)</div>
                <div class="wf-sample" style="font-size: 48px; font-weight: 700;">The quick brown</div>
              </div>
            </div>
          </div>

          <!-- GLYPHS TAB -->
          <div id="tab-view-glyphs" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
              <div style="font-size: 14px; font-weight: 600; color: #FFFFFF;">Peta Karakter Unicode (Character Map)</div>
              <div id="glyph-selected-info" style="font-size: 12px; color: #F472B6; font-family: monospace;">Klik glif untuk melihat kode hex Unicode</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(44px, 1fr)); gap: 6px;" id="glyph-grid-container">
              <!-- Dynamically populated via JS -->
            </div>
          </div>

          <!-- METADATA & RENDERING TAB -->
          <div id="tab-view-meta" style="display: none;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <!-- Meta Card -->
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 16px;">
                <div style="font-size: 14px; font-weight: 700; color: #F472B6; margin-bottom: 12px;">Spesifikasi Berkas Font</div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px;">
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Nama PostScript</span><span style="font-family: monospace; color: #FFFFFF;">Inter-Regular</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Format Kontainer</span><span style="color: #FFFFFF;">OpenType CFF (.otf)</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Jumlah Glif</span><span style="color: #FFFFFF;">2,548 glyphs</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Fitur OpenType</span><span style="color: #10B981;">calt, liga, tnum, ss01</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Lokasi Penyimpanan</span><span style="font-family: monospace; font-size: 10px; color: #9CA3AF;">/usr/share/fonts/opentype/</span></div>
                </div>
              </div>

              <!-- Rendering Tuning Card (FreeType Subpixel Parity) -->
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 16px;">
                <div style="font-size: 14px; font-weight: 700; color: #00D2FF; margin-bottom: 12px;">Konfigurasi Antialiasing Layar</div>
                <div style="display: flex; flex-direction: column; gap: 12px; font-size: 12px;">
                  <div>
                    <label style="color: #9CA3AF; display: block; margin-bottom: 4px;">Mode Antialiasing FreeType</label>
                    <select id="font-aa-select" style="width: 100%; background: #111827; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px; color: #FFFFFF; font-size: 12px;">
                      <option selected>Subpixel LCD (RGB) - Rekomendasi 4K/Retina</option>
                      <option>Grayscale (Standar)</option>
                      <option>None (Bebas Blur)</option>
                    </select>
                  </div>
                  <div>
                    <label style="color: #9CA3AF; display: block; margin-bottom: 4px;">Tingkat Hinting Tipografi</label>
                    <select id="font-hint-select" style="width: 100%; background: #111827; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px; color: #FFFFFF; font-size: 12px;">
                      <option selected>Slight (Sub-pixel Positioning Modern)</option>
                      <option>Medium</option>
                      <option>Full</option>
                      <option>None</option>
                    </select>
                  </div>
                  <button onclick="saveFontTuning()" style="background: rgba(0,210,255,0.2); border: 1px solid rgba(0,210,255,0.4); color: #00D2FF; padding: 8px 12px; border-radius: 6px; font-weight: 600; cursor: pointer; margin-top: 4px;">Terapkan Konfigurasi Tipografi</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
    """

    if 'id="win-daxfont"' not in html:
        # inject right before the launchpad container
        html = html.replace('  <!-- ========================================================================\n       LAUNCHPAD / APPLICATION GRID (macOS FULL-SCREEN ACRYLIC)\n       ======================================================================== -->',
                            font_window_markup + '\n  <!-- ========================================================================\n       LAUNCHPAD / APPLICATION GRID (macOS FULL-SCREEN ACRYLIC)\n       ======================================================================== -->')
        print("[OK] Injected DaxFont window markup")

    # 5. Inject DaxFont into Dock
    dock_font_item = """
      <div class="dock-item" onclick="openApp('win-daxfont', 'DaxFont')">
        <svg class="dock-icon"><use href="#icon-font"/></svg>
        <span class="dock-tooltip">DaxFont Tipografi</span>
      </div>"""
    
    if "openApp('win-daxfont'" not in html:
        html = html.replace("""      <div class="dock-item" onclick="openApp('win-daxclock', 'DaxClock')">
        <svg class="dock-icon"><use href="#icon-clock"/></svg>
        <span class="dock-tooltip">DaxClock Jam</span>
      </div>""",
        """      <div class="dock-item" onclick="openApp('win-daxclock', 'DaxClock')">
        <svg class="dock-icon"><use href="#icon-clock"/></svg>
        <span class="dock-tooltip">DaxClock Jam</span>
      </div>""" + dock_font_item)
        print("[OK] Injected DaxFont into Dock")

    # 6. Inject DaxFont into Launchpad Grid
    launchpad_font_item = """
        <div class="launchpad-item" data-category="system" data-name="DaxFont Font Manager Pengelola Tipografi Karakter Glyphs Huruf" onclick="launchAppFromLaunchpad('win-daxfont', 'DaxFont')">
          <svg class="launchpad-item-icon"><use href="#icon-font"/></svg>
          <div class="launchpad-item-title">DaxFont</div>
          <div class="launchpad-item-desc">Pengelola Font &amp; Tipografi</div>
        </div>"""

    if "launchAppFromLaunchpad('win-daxfont'" not in html:
        html = html.replace("""        <div class="launchpad-item" data-category="system" data-name="DaxClock Jam Alarm Timer Stopwatch Dunia Waktu" onclick="launchAppFromLaunchpad('win-daxclock', 'DaxClock')">
          <svg class="launchpad-item-icon"><use href="#icon-clock"/></svg>
          <div class="launchpad-item-title">DaxClock</div>
          <div class="launchpad-item-desc">Jam Dunia, Alarm &amp; Stopwatch</div>
        </div>""",
        """        <div class="launchpad-item" data-category="system" data-name="DaxClock Jam Alarm Timer Stopwatch Dunia Waktu" onclick="launchAppFromLaunchpad('win-daxclock', 'DaxClock')">
          <svg class="launchpad-item-icon"><use href="#icon-clock"/></svg>
          <div class="launchpad-item-title">DaxClock</div>
          <div class="launchpad-item-desc">Jam Dunia, Alarm &amp; Stopwatch</div>
        </div>""" + launchpad_font_item)
        print("[OK] Injected DaxFont into Launchpad Grid")

    # 7. Inject DaxFont JavaScript Controller
    font_js = """
    // ============================================================================
    // DAXFONT TYPOGRAPHY & FONT MANAGER CONTROLLER
    // ============================================================================
    const daxFontData = {
      'Inter Display': {
        designer: 'Rasmus Andersson',
        license: 'SIL Open Font License 1.1',
        version: 'v4.001',
        weights: '7 bobot (Thin s/d Black)',
        family: "'Inter', sans-serif",
        category: 'sans',
        format: 'OpenType CFF (.otf)',
        glyphs: 2548
      },
      'JetBrains Mono': {
        designer: 'JetBrains & Philipp Nurullin',
        license: 'Apache License 2.0',
        version: 'v2.304',
        weights: '4 bobot (Regular s/d ExtraBold)',
        family: "monospace",
        category: 'mono',
        format: 'TrueType (.ttf)',
        glyphs: 1480
      },
      'Fira Code': {
        designer: 'Nikita Prokopov',
        license: 'SIL Open Font License 1.1',
        version: 'v6.200',
        weights: '2 bobot (Regular, Bold)',
        family: "monospace",
        category: 'mono',
        format: 'OpenType CFF (.otf)',
        glyphs: 1220
      },
      'Playfair Display': {
        designer: 'Claus Eggers Sorensen',
        license: 'SIL Open Font License 1.1',
        version: 'v2.102',
        weights: '3 bobot (Regular, Bold, Black)',
        family: "Georgia, serif",
        category: 'serif',
        format: 'OpenType CFF (.otf)',
        glyphs: 1180
      },
      'Outfit': {
        designer: 'Outfit International',
        license: 'SIL Open Font License 1.1',
        version: 'v1.200',
        weights: '3 bobot (Regular, SemiBold, ExtraBold)',
        family: "'Outfit', sans-serif",
        category: 'display',
        format: 'TrueType (.ttf)',
        glyphs: 1350
      }
    };

    const daxSampleGlyphs = [
      'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
      'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
      '0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*','(',')','-','+','=','/','?',
      '∑','√','∫','∆','π','∞','≈','≠','≤','≥','±','÷','×','€','£','¥','₽','Rp','→','←','↑','↓','⇒','⇔','⌘','⌥','⇧','⏎'
    ];

    function initGlyphGrid() {
      const container = document.getElementById('glyph-grid-container');
      if (!container) return;
      container.innerHTML = '';
      daxSampleGlyphs.forEach(ch => {
        const div = document.createElement('div');
        div.style.cssText = 'height: 44px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; font-size: 18px; cursor: pointer; transition: all 0.15s;';
        div.innerText = ch;
        div.onmouseover = () => { div.style.borderColor = '#EC4899'; div.style.background = 'rgba(236,72,153,0.15)'; };
        div.onmouseout = () => { div.style.borderColor = 'rgba(255,255,255,0.08)'; div.style.background = 'rgba(255,255,255,0.03)'; };
        div.onclick = () => {
          const codePoint = ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0');
          const info = document.getElementById('glyph-selected-info');
          if (info) {
            info.innerHTML = `Glif: <b style="color: #FFFFFF; font-size: 14px;">${ch}</b> | Unicode: <b>U+${codePoint}</b> (Disalin)`;
          }
          if (navigator.clipboard) {
            navigator.clipboard.writeText(ch);
          }
        };
        container.appendChild(div);
      });
    }

    function selectFontDetail(fontName) {
      const f = daxFontData[fontName];
      if (!f) return;
      const title = document.getElementById('font-active-title');
      const sub = document.getElementById('font-active-sub');
      if (title) title.innerText = fontName;
      if (sub) sub.innerText = `${f.designer} • ${f.license} • ${f.version}`;

      // Update waterfall samples family
      document.querySelectorAll('.wf-sample').forEach(el => {
        el.style.fontFamily = f.family;
      });

      // Highlight active card
      document.querySelectorAll('.font-list-card').forEach(card => {
        if (card.getAttribute('data-name') === fontName) {
          card.classList.add('active');
          card.style.background = 'rgba(236,72,153,0.15)';
          card.style.borderColor = 'rgba(236,72,153,0.4)';
        } else {
          card.classList.remove('active');
          card.style.background = 'rgba(255,255,255,0.03)';
          card.style.borderColor = 'transparent';
        }
      });
    }

    function updateWaterfallPangram(text) {
      const val = text || 'The quick brown fox jumps over the lazy dog 1234567890';
      document.querySelectorAll('.wf-sample').forEach(el => {
        el.innerText = val;
      });
    }

    function filterFontCategory(cat, el) {
      document.querySelectorAll('.font-cat-item').forEach(item => {
        item.classList.remove('active');
        item.style.background = 'transparent';
        item.style.color = '#D1D5DB';
      });
      if (el) {
        el.classList.add('active');
        el.style.background = 'rgba(236,72,153,0.2)';
        el.style.color = '#F472B6';
      }

      document.querySelectorAll('.font-list-card').forEach(card => {
        if (cat === 'all' || card.getAttribute('data-category') === cat || (cat === 'system' && card.getAttribute('data-category') !== 'user')) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function searchFontCatalog(query) {
      const q = query.toLowerCase();
      document.querySelectorAll('.font-list-card').forEach(card => {
        const name = (card.getAttribute('data-name') || '').toLowerCase();
        if (name.includes(q)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function switchFontTab(tabName) {
      const tabs = ['waterfall', 'glyphs', 'meta'];
      tabs.forEach(t => {
        const btn = document.getElementById(`tab-btn-${t}`);
        const view = document.getElementById(`tab-view-${t}`);
        if (btn) {
          if (t === tabName) {
            btn.style.background = 'rgba(236,72,153,0.25)';
            btn.style.color = '#F472B6';
          } else {
            btn.style.background = 'transparent';
            btn.style.color = '#9CA3AF';
          }
        }
        if (view) {
          view.style.display = (t === tabName) ? 'block' : 'none';
        }
      });
      if (tabName === 'glyphs') {
        initGlyphGrid();
      }
    }

    function installFontPrompt() {
      const fontName = prompt('Masukkan nama font atau path berkas (.ttf / .otf / .woff2):', 'GeistMono-Regular.otf');
      if (fontName) {
        alert(`[SUKSES] Font '${fontName}' berhasil dipasang ke sistem DAXOS! Direktori: /usr/share/fonts/opentype/user/. Cache font fc-cache diperbarui.`);
      }
    }

    function saveFontTuning() {
      const aa = document.getElementById('font-aa-select')?.value || 'Subpixel LCD (RGB)';
      const hint = document.getElementById('font-hint-select')?.value || 'Slight';
      alert(`[SUKSES] Konfigurasi tipografi DAXOS disimpan:\\n• Antialiasing: ${aa}\\n• Hinting: ${hint}\\nPembaharuan diterapkan instan pada DreXUI Compositor 240Hz.`);
    }

    // Initialize DaxFont glyphs on load
    setTimeout(initGlyphGrid, 1000);
    """

    if "function selectFontDetail" not in html:
        html = html.replace('//]]>\n  </script>', font_js + '\n//]]>\n  </script>')
        print("[OK] Injected DaxFont JavaScript controller")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("[SUCCESS] Integrated DaxFont and all missing icons into index.html!")

if __name__ == "__main__":
    main()
