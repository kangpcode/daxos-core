#!/usr/bin/env python3
"""
perfect_daxos_ecosystem.py
Transforms desktop_preview/index.html to meet all ecosystem standards:
1. Solid branded colored squircle backgrounds for every app icon (zero transparent/flat gray cutouts).
2. DaxBro Chromium 132 engine & ecosystem with Blink 6.12, V8 13.2, Manifest V3 extensions, CDP devtools.
3. DaxMedia Suite 3-in-1 Default Media Player (Audio + 4K Video + Photo Gallery).
4. Direct 'ping 1.1.1.1' and IP address diagnostic support in Terminal.
"""

import sys
import re

INDEX_PATH = "src/ui/desktop_preview/index.html"

def main():
    print("[1/5] Loading src/ui/desktop_preview/index.html...")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. ADD BRANDED ICON GRADIENTS TO <defs>
    branded_gradients = """
      <!-- DAXOS SYSTEM BRANDED APP ICON GRADIENTS (SOLID VIBRANT BASES) -->
      <linearGradient id="icon-bg-finder" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#00C6FF"/>
        <stop offset="100%" stop-color="#0072FF"/>
      </linearGradient>

      <linearGradient id="icon-bg-daxbro" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1A73E8"/>
        <stop offset="50%" stop-color="#1557B0"/>
        <stop offset="100%" stop-color="#0D47A1"/>
      </linearGradient>

      <linearGradient id="icon-bg-ide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#7928CA"/>
        <stop offset="100%" stop-color="#4338CA"/>
      </linearGradient>

      <linearGradient id="icon-bg-editor" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#10B981"/>
        <stop offset="100%" stop-color="#047857"/>
      </linearGradient>

      <linearGradient id="icon-bg-terminal" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E293B"/>
        <stop offset="100%" stop-color="#0F172A"/>
      </linearGradient>

      <linearGradient id="icon-bg-media" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FF2D55"/>
        <stop offset="50%" stop-color="#E11D48"/>
        <stop offset="100%" stop-color="#8B5CF6"/>
      </linearGradient>

      <linearGradient id="icon-bg-camera" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#4B5563"/>
        <stop offset="100%" stop-color="#1F2937"/>
      </linearGradient>

      <linearGradient id="icon-bg-calculator" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#F59E0B"/>
        <stop offset="100%" stop-color="#D97706"/>
      </linearGradient>

      <linearGradient id="icon-bg-disks" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#38BDF8"/>
        <stop offset="100%" stop-color="#0284C7"/>
      </linearGradient>

      <linearGradient id="icon-bg-daxdrop" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#06B6D4"/>
        <stop offset="100%" stop-color="#0284C7"/>
      </linearGradient>

      <linearGradient id="icon-bg-monitor" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#10B981"/>
        <stop offset="100%" stop-color="#065F46"/>
      </linearGradient>

      <linearGradient id="icon-bg-settings" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#64748B"/>
        <stop offset="100%" stop-color="#334155"/>
      </linearGradient>

      <linearGradient id="icon-bg-dapstore" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#3B82F6"/>
        <stop offset="100%" stop-color="#1D4ED8"/>
      </linearGradient>

      <linearGradient id="icon-bg-dxdef" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#059669"/>
        <stop offset="100%" stop-color="#064E3B"/>
      </linearGradient>

      <linearGradient id="icon-bg-installer" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0EA5E9"/>
        <stop offset="100%" stop-color="#0369A1"/>
      </linearGradient>

      <linearGradient id="icon-bg-trash" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#475569"/>
        <stop offset="100%" stop-color="#1E293B"/>
      </linearGradient>

      <linearGradient id="icon-bg-launchpad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#4338CA"/>
        <stop offset="100%" stop-color="#1E1B4B"/>
      </linearGradient>

      <linearGradient id="icon-bg-network" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0284C7"/>
        <stop offset="100%" stop-color="#0C4A6E"/>
      </linearGradient>

      <linearGradient id="icon-bg-driver" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#059669"/>
        <stop offset="100%" stop-color="#064E3B"/>
      </linearGradient>
"""

    if 'id="icon-bg-finder"' not in content:
        content = content.replace("</defs>", branded_gradients + "\n    </defs>", 1)
        print("[OK] Injected branded icon background gradients into <defs>")

    # 2. OVERHAUL ALL SYSTEM APP ICONS TO SOLID BRANDED SQUIRCLES
    icons_replacement = """
    <!-- Finder Icon (Branded DAXOS Azure Squircle) -->
    <symbol id="icon-finder" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-finder)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Split Face -->
      <path d="M46 36 C42 42 40 50 40 64 C40 78 42 86 46 92 C56 94 72 94 82 92 C86 86 88 78 88 64 C88 50 86 42 82 36 Z" fill="#FFFFFF"/>
      <path d="M46 36 C42 42 40 50 40 64 C40 78 42 86 46 92 C56 94 64 94 64 94 V36 C64 36 56 36 46 36 Z" fill="#0284C7"/>
      <circle cx="52" cy="58" r="4.5" fill="#0C1E3D"/>
      <circle cx="76" cy="58" r="4.5" fill="#0C1E3D"/>
      <path d="M50 74 Q64 88 78 74" fill="none" stroke="#0C1E3D" stroke-width="4.5" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaXBro Chromium Browser Icon (Chromium Quadrant on Branded Blue Squircle) -->
    <symbol id="icon-daxbro" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-daxbro)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Circular White Center Plate -->
      <circle cx="64" cy="64" r="42" fill="#FFFFFF"/>
      <!-- Chromium 4-Color Pinwheel -->
      <path d="M64 24 A40 40 0 0 1 101 50 L77 50 A17 17 0 0 0 64 47 Z" fill="#EA4335"/>
      <path d="M101 50 A40 40 0 0 1 76 102 L64 79 A17 17 0 0 0 81 64 Z" fill="#FBBC05"/>
      <path d="M76 102 A40 40 0 0 1 27 78 L51 78 A17 17 0 0 0 64 81 Z" fill="#34A853"/>
      <path d="M27 78 A40 40 0 0 1 64 24 L64 47 A17 17 0 0 0 47 64 Z" fill="#4285F4"/>
      <!-- Center Core -->
      <circle cx="64" cy="64" r="15" fill="#FFFFFF"/>
      <circle cx="64" cy="64" r="11" fill="#1A73E8"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DCODX Studio Icon (Official Heavyweight IDE - Royal Indigo Squircle) -->
    <symbol id="icon-ide" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-ide)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Code Brackets < / > with Live AST Compiler Node -->
      <path d="M42 46 L26 64 L42 82" fill="none" stroke="#67E8F9" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M86 46 L102 64 L86 82" fill="none" stroke="#67E8F9" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="72" y1="38" x2="56" y2="90" stroke="#F472B6" stroke-width="7" stroke-linecap="round"/>
      <circle cx="64" cy="64" r="6" fill="#34D399"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- dEdit Notes Icon (Notepad++ & Scratchpad - Emerald Green Squircle) -->
    <symbol id="icon-editor" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-editor)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- White Note Document Sheet -->
      <rect x="32" y="26" width="64" height="76" rx="8" fill="#FFFFFF"/>
      <path d="M76 26 L96 46 H80 C77.8 46 76 44.2 76 42 Z" fill="#D1D5DB"/>
      <!-- Lined Text Lines -->
      <line x1="44" y1="46" x2="68" y2="46" stroke="#059669" stroke-width="4" stroke-linecap="round"/>
      <line x1="44" y1="58" x2="84" y2="58" stroke="#9CA3AF" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="44" y1="70" x2="84" y2="70" stroke="#9CA3AF" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="44" y1="82" x2="72" y2="82" stroke="#9CA3AF" stroke-width="3.5" stroke-linecap="round"/>
      <!-- Golden Syntax Pen -->
      <polygon points="86,88 96,62 102,68 92,94" fill="#F59E0B"/>
      <polygon points="86,88 88,96 92,94" fill="#374151"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Terminal Icon (Obsidian Charcoal Squircle) -->
    <symbol id="icon-terminal" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-terminal)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Emerald Shell Prompt > _ -->
      <path d="M34 46 L58 64 L34 82" fill="none" stroke="#34D399" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="68" y1="82" x2="94" y2="82" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaxMedia Suite Icon (Video, Audio & Photos - Magenta Fuchsia Squircle) -->
    <symbol id="icon-media" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-media)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Audio Note & Video Play Triangle Combined Reel -->
      <circle cx="64" cy="64" r="38" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="8 6"/>
      <!-- Play Triangle -->
      <polygon points="56,46 82,64 56,82" fill="#FFFFFF"/>
      <!-- Musical Stem -->
      <circle cx="88" cy="46" r="6" fill="#FDE047"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Camera Icon (Titanium Slate Squircle) -->
    <symbol id="icon-camera" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-camera)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <circle cx="64" cy="64" r="38" fill="#111827" stroke="#9CA3AF" stroke-width="5"/>
      <circle cx="64" cy="64" r="24" fill="#030712" stroke="#38BDF8" stroke-width="3"/>
      <circle cx="56" cy="56" r="7" fill="rgba(255,255,255,0.4)"/>
      <circle cx="94" cy="34" r="5" fill="#EF4444"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Calculator Icon (Warm Amber Sunset Squircle) -->
    <symbol id="icon-calculator" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-calculator)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <rect x="30" y="30" width="68" height="20" rx="5" fill="#FFFFFF"/>
      <circle cx="44" cy="72" r="8" fill="#FFFFFF"/>
      <circle cx="84" cy="72" r="8" fill="#FFFFFF"/>
      <circle cx="44" cy="96" r="8" fill="#FFFFFF"/>
      <circle cx="84" cy="96" r="8" fill="#FFFFFF"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Disk Utility Icon (Cerulean Blue Squircle) -->
    <symbol id="icon-disks" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-disks)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <rect x="24" y="32" width="80" height="64" rx="14" fill="#FFFFFF" fill-opacity="0.15" stroke="#FFFFFF" stroke-width="6"/>
      <circle cx="64" cy="64" r="18" fill="none" stroke="#FFFFFF" stroke-width="5"/>
      <circle cx="64" cy="64" r="6" fill="#34D399"/>
      <line x1="84" y1="84" x2="94" y2="84" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaXDrop Icon (Air-Grab & Sky Cyan Squircle) -->
    <symbol id="icon-daxdrop" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-daxdrop)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <circle cx="64" cy="64" r="42" fill="none" stroke="rgba(255, 255, 255, 0.4)" stroke-width="3" stroke-dasharray="4 4"/>
      <circle cx="64" cy="64" r="28" fill="none" stroke="#FFFFFF" stroke-width="3.5"/>
      <!-- Air-Grab Fist/Palm Glyph -->
      <path d="M54 48 C50 48 48 52 48 56 V72 C48 80 54 86 62 86 H68 C76 86 82 80 82 72 V62 C82 58 79 55 75 55 C73 55 71 56 70 58 C69 54 66 52 62 52 C60 52 58 53 57 55 C56 51 53 48 54 48 Z" fill="#FFFFFF"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Activity Monitor Icon (Forest Green Telemetry Squircle) -->
    <symbol id="icon-monitor" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-monitor)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- ECG Pulse Graph -->
      <path d="M22 68 H42 L52 38 L68 94 L80 52 L88 74 L94 68 H106" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="68" cy="94" r="5" fill="#FDE047"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- System Settings Icon (Satin Aluminum Slate Squircle) -->
    <symbol id="icon-settings" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-settings)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <circle cx="64" cy="64" r="22" fill="#FFFFFF"/>
      <circle cx="64" cy="64" r="10" fill="#334155"/>
      <path d="M60 22 H68 V32 H60 Z M60 96 H68 V106 H60 Z M22 60 H32 V68 H22 Z M96 60 H106 V68 H96 Z M34 34 L41 41 L35 47 L28 40 Z M87 87 L94 94 L88 100 L81 93 Z M94 34 L87 41 L81 35 L88 28 Z M41 87 L34 94 L28 88 L35 81 Z" fill="#FFFFFF"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DapStore Icon (Electric Blue Package Squircle) -->
    <symbol id="icon-dapstore" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-dapstore)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <polygon points="64,22 96,40 96,76 64,94 32,76 32,40" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
      <line x1="64" y1="94" x2="64" y2="58" stroke="#FFFFFF" stroke-width="6"/>
      <line x1="32" y1="40" x2="64" y2="58" stroke="#FFFFFF" stroke-width="6"/>
      <line x1="96" y1="40" x2="64" y2="58" stroke="#FFFFFF" stroke-width="6"/>
      <polygon points="64,98 72,112 56,112" fill="#FDE047"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DXDEF Security Center Icon (Shield Emerald Squircle) -->
    <symbol id="icon-dxdef" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-dxdef)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <path d="M64 24 L96 38 V66 C96 86 82 102 64 108 C46 102 32 86 32 66 V38 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
      <rect x="52" y="60" width="24" height="20" rx="4" fill="#FFFFFF"/>
      <path d="M57 60 V52 C57 48 61 45 64 45 C67 45 71 48 71 52 V60" fill="none" stroke="#FFFFFF" stroke-width="4"/>
      <circle cx="64" cy="70" r="2.5" fill="#064E3B"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Installer Icon (Deep Sapphire Squircle) -->
    <symbol id="icon-installer" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-installer)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <circle cx="64" cy="64" r="42" fill="none" stroke="#FFFFFF" stroke-width="7"/>
      <circle cx="64" cy="64" r="14" fill="#FFFFFF"/>
      <polygon points="64,28 76,46 52,46" fill="#FDE047"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Trash Icon (Frosted Slate Squircle) -->
    <symbol id="icon-trash" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-trash)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <path d="M42 42 H86 L80 100 H48 Z" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round"/>
      <line x1="36" y1="36" x2="92" y2="36" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
      <path d="M54 36 V28 H74 V36" fill="none" stroke="#FFFFFF" stroke-width="5"/>
      <line x1="56" y1="52" x2="58" y2="90" stroke="rgba(255,255,255,0.7)" stroke-width="4"/>
      <line x1="72" y1="52" x2="70" y2="90" stroke="rgba(255,255,255,0.7)" stroke-width="4"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Launchpad / All Apps Grid Icon (Deep Indigo Squircle) -->
    <symbol id="icon-launchpad" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-launchpad)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <circle cx="42" cy="42" r="7" fill="#00D2FF"/>
      <circle cx="64" cy="42" r="7" fill="#5856D6"/>
      <circle cx="86" cy="42" r="7" fill="#FF9500"/>
      <circle cx="42" cy="64" r="7" fill="#30D158"/>
      <circle cx="64" cy="64" r="7" fill="#FFFFFF"/>
      <circle cx="86" cy="64" r="7" fill="#FF2D55"/>
      <circle cx="42" cy="86" r="7" fill="#FFCC00"/>
      <circle cx="64" cy="86" r="7" fill="#00D2FF"/>
      <circle cx="86" cy="86" r="7" fill="#AF52DE"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>
"""

    # We will replace symbols from <!-- Finder Icon --> down to </symbol> of launchpad
    # Let's check regex replacement for symbols
    pat = re.compile(r'<!-- Finder Icon.*?<\/symbol>\s*<!-- Launchpad.*?<\/symbol>', re.DOTALL)
    if pat.search(content):
        content = pat.sub(icons_replacement.strip(), content)
        print("[OK] Overhauled all app icons to solid branded squircles")
    else:
        print("[WARN] Could not find symbols range by regex, trying targeted replace...")
        # Direct string replacement
        old_finder = '<symbol id="icon-finder"'
        if old_finder in content:
            # We can find the start of Finder Icon comment and end of Launchpad
            idx_start = content.find('<!-- Finder Icon')
            idx_end = content.find('</symbol>', content.find('id="icon-launchpad"')) + len('</symbol>')
            if idx_start != -1 and idx_end != -1:
                content = content[:idx_start] + icons_replacement.strip() + content[idx_end:]
                print("[OK] Replaced icons using slice indexing")

    # 3. UPGRADE WIN-MEDIA TO 3-IN-1 DEFAULT MEDIA SUITE
    # Let's check win-media content
    win_media_old_tag = '<div class="window" id="win-media"'
    if win_media_old_tag in content:
        start_wm = content.find(win_media_old_tag)
        end_wm = content.find('</div>\n  </div>', start_wm) + len('</div>\n  </div>')
        # Let's inspect the closing of win-media
        end_wm_marker = content.find('<!-- ========================================================================\n       BOTTOM ACRYLIC DOCK', start_wm)
        if end_wm_marker != -1:
            end_wm = content.rfind('</div>', start_wm, end_wm_marker)
            # Find the closing window tag
            end_wm = content.find('</div>\n  </div>', start_wm, end_wm_marker)
            if end_wm == -1:
                end_wm = content.find('</div>\n</div>', start_wm, end_wm_marker)

    new_media_window = """  <div class="window" id="win-media" style="top: 75px; left: 240px; width: 880px; height: 580px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-media')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-media')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-media')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-media')">+</div>
      </div>
      <span class="window-title" id="media-suite-title">DaxMedia Suite — Video Player, Spatial Audio &amp; Photo Gallery</span>
      <!-- Mode Tab Switcher -->
      <div style="margin-left: auto; display: flex; gap: 4px; background: rgba(0,0,0,0.3); border-radius: 8px; padding: 2px;">
        <button class="btn btn-secondary active" id="btn-tab-audio" style="font-size: 10px; padding: 3px 10px;" onclick="switchMediaTab('audio')">Audio DSP</button>
        <button class="btn btn-secondary" id="btn-tab-video" style="font-size: 10px; padding: 3px 10px;" onclick="switchMediaTab('video')">4K Video</button>
        <button class="btn btn-secondary" id="btn-tab-photo" style="font-size: 10px; padding: 3px 10px;" onclick="switchMediaTab('photo')">Photo Gallery</button>
      </div>
    </div>
    <div class="window-content" style="padding: 16px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0A0B10;">
      <!-- TAB 1: AUDIO DSP & HRTF -->
      <div id="media-panel-audio" style="display: flex; flex-direction: column; gap: 14px;">
        <div style="background: linear-gradient(135deg, rgba(255,45,85,0.18), rgba(139,92,246,0.18)); border: 1px solid rgba(255,45,85,0.35); border-radius: 14px; padding: 16px; display: flex; gap: 18px; align-items: center;">
          <div style="width: 84px; height: 84px; border-radius: 12px; background: linear-gradient(45deg, #FF2D55, #8B5CF6); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(255,45,85,0.35);">
            <svg style="width: 44px; height: 44px;"><use href="#icon-media"/></svg>
          </div>
          <div style="flex: 1;">
            <div style="font-size: 17px; font-weight: 700; color: #FFF;">Resonance - Symphonic Glass</div>
            <div style="font-size: 12px; color: #38BDF8; margin-top: 2px;">DAXOS Audio Laboratory &bull; 96kHz / 24-bit Lossless FLAC &bull; PipeWire 5.8 ms</div>
            <div style="display: flex; align-items: center; gap: 12px; margin-top: 10px;">
              <span style="font-size: 10px; color: #8E8EA0;">01:42</span>
              <div style="flex: 1; height: 5px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; cursor: pointer;">
                <div style="width: 42%; height: 100%; background: linear-gradient(90deg, #FF2D55, #38BDF8);"></div>
              </div>
              <span style="font-size: 10px; color: #8E8EA0;">04:18</span>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <button class="btn btn-secondary" style="font-size: 14px; width: 36px; height: 36px; padding: 0; display: flex; align-items: center; justify-content: center;">&laquo;</button>
            <button class="btn btn-primary" id="btn-media-play" style="font-size: 16px; width: 44px; height: 44px; padding: 0; display: flex; align-items: center; justify-content: center; border-radius: 22px;" onclick="toggleMediaPlay()">&#9654;</button>
            <button class="btn btn-secondary" style="font-size: 14px; width: 36px; height: 36px; padding: 0; display: flex; align-items: center; justify-content: center;">&raquo;</button>
          </div>
        </div>

        <!-- 10-Band EQ -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 12px; padding: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 12px; font-weight: 700; color: #FFF;">Equalizer Grafis 10-Band (DSP PipeWire Native) &bull; HRTF 3D Spatializer</div>
            <div style="display: flex; gap: 6px;">
              <button class="btn btn-secondary active" style="font-size: 10px; padding: 3px 8px;" onclick="setEqPreset('Acoustic')">Acoustic Clarity</button>
              <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="setEqPreset('Bass')">Bass Boost</button>
              <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="setEqPreset('Spatial')">Spatial 3D</button>
            </div>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: flex-end; height: 100px; padding: 0 10px;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="2" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">31Hz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="4" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">62Hz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="1" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">125Hz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="0" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">250Hz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="-1" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">500Hz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="2" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">1kHz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="3" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">2kHz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="2" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">4kHz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="4" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">8kHz</span></div>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;"><input type="range" min="-12" max="12" value="3" orient="vertical" style="writing-mode: vertical-lr; height: 75px; accent-color: #38BDF8;"><span style="font-size: 9px; color: #8E8EA0;">16kHz</span></div>
          </div>
        </div>
      </div>

      <!-- TAB 2: 4K VIDEO PLAYER (AV1 / HEVC HARDWARE ACCELERATED) -->
      <div id="media-panel-video" style="display: none; flex-direction: column; gap: 12px;">
        <!-- Cinema Viewport -->
        <div style="position: relative; width: 100%; height: 320px; background: #000; border-radius: 12px; overflow: hidden; display: flex; align-items: center; justify-content: center; box-shadow: 0 12px 32px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.08);">
          <div style="position: absolute; top: 12px; left: 16px; background: rgba(0,0,0,0.6); backdrop-filter: blur(8px); padding: 4px 10px; border-radius: 6px; font-size: 11px; color: #34D399; font-weight: 700; border: 1px solid rgba(52,211,153,0.3);">
            AV1 4K UHD 60 FPS &bull; HDR10+ &bull; Vulkan 1.3 Zero-Copy
          </div>
          <div style="position: absolute; top: 12px; right: 16px; display: flex; gap: 6px;">
            <span style="background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 6px; font-size: 10px; color: #38BDF8;">Dolby Atmos 7.1</span>
            <span style="background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 6px; font-size: 10px; color: #F59E0B;">Subtitles: ID/EN</span>
          </div>
          <!-- Animated Cyberpunk Scene Simulation -->
          <div style="text-align: center;">
            <div style="font-size: 48px; opacity: 0.8;">🎬</div>
            <div style="font-size: 16px; font-weight: 700; color: #FFF; margin-top: 8px;">DAXOS: The Future of Computing (2026 Trailer)</div>
            <div style="font-size: 12px; color: #8E8EA0;">3840 x 2160 &bull; Bitrate: 24.5 Mbps &bull; Hardware Decoder: DreXVIS Active</div>
          </div>
          <!-- Video Control Bar Overlay -->
          <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(0deg, rgba(0,0,0,0.9), transparent); padding: 12px 18px; display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="font-size: 10px; color: #FFF;">02:15</span>
              <div style="flex: 1; height: 5px; background: rgba(255,255,255,0.2); border-radius: 3px; cursor: pointer;">
                <div style="width: 45%; height: 100%; background: #0A84FF; border-radius: 3px;"></div>
              </div>
              <span style="font-size: 10px; color: #FFF;">05:00</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div style="display: flex; gap: 10px; align-items: center;">
                <button class="btn btn-primary" style="padding: 4px 12px; font-size: 12px;">⏸ Jeda</button>
                <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;">1.0x Speed</button>
                <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;">Subtitles [ON]</button>
              </div>
              <div style="display: flex; gap: 10px; align-items: center;">
                <span style="font-size: 11px; color: #8E8EA0;">Volume 100%</span>
                <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;">PiP</button>
                <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;">Full Screen</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: PHOTO GALLERY & IMAGE VIEWER (DISPLAY P3) -->
      <div id="media-panel-photo" style="display: none; flex-direction: column; gap: 12px;">
        <div style="display: flex; gap: 14px; height: 330px;">
          <!-- Main Canvas -->
          <div style="flex: 1; background: #000; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 12px; left: 14px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 6px; font-size: 10px; color: #38BDF8;">
              Display P3 Wide Gamut &bull; 4096x2732 &bull; 10-bit AVIF
            </div>
            <div style="text-align: center;">
              <div style="font-size: 54px;">🏔️</div>
              <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-top: 6px;">Mount Bromo Aurora Dawn.avif</div>
              <div style="font-size: 11px; color: #8E8EA0;">Sony Alpha 7R V &bull; ISO 100 &bull; f/2.8 &bull; 1/500s</div>
            </div>
            <!-- Zoom & Pan Bar -->
            <div style="position: absolute; bottom: 12px; display: flex; gap: 8px; background: rgba(0,0,0,0.7); backdrop-filter: blur(8px); padding: 4px 12px; border-radius: 20px;">
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;">Zoom In (+)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;">100%</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;">Zoom Out (-)</button>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 11px;">Rotate 90&deg;</button>
            </div>
          </div>
          <!-- EXIF & Thumbnails Pane -->
          <div style="width: 220px; background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 10px;">
            <div style="font-size: 11px; font-weight: 700; color: #FFF;">Informasi Citra (EXIF)</div>
            <div style="font-size: 10px; color: #8E8EA0; line-height: 1.6;">
              <div>Kamera: Sony Alpha 7R V</div>
              <div>Lensa: FE 24-70mm F2.8 GM II</div>
              <div>Eksposur: 1/500 detik di f/2.8</div>
              <div>Kepekaan: ISO 100</div>
              <div>Ukuran Berkas: 4.82 MB</div>
              <div>Format: AVIF (Lossless)</div>
            </div>
            <div style="font-size: 11px; font-weight: 700; color: #FFF; margin-top: 4px;">Koleksi Lainnya</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; overflow-y: auto;">
              <div style="background: rgba(255,255,255,0.06); height: 50px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer;">🌆</div>
              <div style="background: rgba(255,255,255,0.06); height: 50px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer;">🏖️</div>
              <div style="background: rgba(255,255,255,0.06); height: 50px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer;">🌌</div>
              <div style="background: rgba(255,255,255,0.06); height: 50px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer;">🌲</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>"""

    # Replace win-media
    if '<div class="window" id="win-media"' in content:
        start_wm = content.find('<div class="window" id="win-media"')
        # Find matching closing for win-media
        # It's followed by dock comment
        dock_marker = '<!-- ========================================================================\n       BOTTOM ACRYLIC DOCK'
        end_wm = content.find(dock_marker, start_wm)
        if end_wm != -1:
            # We replace from start_wm up to dock_marker
            old_block = content[start_wm:end_wm].strip()
            content = content[:start_wm] + new_media_window + "\n\n  " + content[end_wm:]
            print("[OK] Upgraded win-media to 3-in-1 DaxMedia Suite")

    # 4. ADD JAVASCRIPT FOR MEDIA TAB SWITCHER AND TERMINAL PING
    js_helpers = """
    // DaxMedia Suite Tab Switching Logic
    function switchMediaTab(tab) {
      const audioP = document.getElementById('media-panel-audio');
      const videoP = document.getElementById('media-panel-video');
      const photoP = document.getElementById('media-panel-photo');
      const bAudio = document.getElementById('btn-tab-audio');
      const bVideo = document.getElementById('btn-tab-video');
      const bPhoto = document.getElementById('btn-tab-photo');
      const title = document.getElementById('media-suite-title');

      if (!audioP || !videoP || !photoP) return;

      audioP.style.display = 'none';
      videoP.style.display = 'none';
      photoP.style.display = 'none';
      bAudio.classList.remove('active');
      bVideo.classList.remove('active');
      bPhoto.classList.remove('active');

      if (tab === 'video') {
        videoP.style.display = 'flex';
        bVideo.classList.add('active');
        if (title) title.textContent = 'DaxMedia Suite — 4K UHD AV1 Hardware Video Player';
      } else if (tab === 'photo') {
        photoP.style.display = 'flex';
        bPhoto.classList.add('active');
        if (title) title.textContent = 'DaxMedia Suite — Display P3 High-Resolution Photo Gallery';
      } else {
        audioP.style.display = 'flex';
        bAudio.classList.add('active');
        if (title) title.textContent = 'DaxMedia Suite — Spatial Audio DSP & 10-Band Equalizer';
      }
    }
"""

    if 'function switchMediaTab(tab)' not in content:
        content = content.replace("</script>", js_helpers + "\n  </script>", 1)
        print("[OK] Added switchMediaTab JavaScript helper")

    # 5. ENHANCE TERMINAL INPUT WITH PING COMMAND AND DMEDIA / DAXBRO
    # Let's search where case 'dnet' is handled and add case 'ping'
    ping_terminal_case = """        case 'ping':
          {
            const target = args[1] || '1.1.1.1';
            termHistory.textContent += `PING ${target} (${target}) 56(84) bytes of data via kernel BBRv3 stack:
64 bytes from ${target}: icmp_seq=1 ttl=58 time=8.24 ms
64 bytes from ${target}: icmp_seq=2 ttl=58 time=7.91 ms
64 bytes from ${target}: icmp_seq=3 ttl=58 time=8.05 ms
64 bytes from ${target}: icmp_seq=4 ttl=58 time=8.12 ms

--- ${target} ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 7.910/8.080/8.240/0.125 ms
[SUKSES] Latensi jaringan super cepat dan stabil untuk Developer & Network Engineer!
`;
          }
          break;
        case 'dmedia':
          if (args[1] === 'play') {
            termHistory.textContent += `DAXOS Media Engine (dmedia): Playing '${args[2] || 'sample.flac'}'
Codec: 96kHz 24-bit Lossless &bull; PipeWire Latency: 5.8 ms &bull; Spatial HRTF: ON
`;
          } else if (args[1] === 'view') {
            termHistory.textContent += `DAXOS Photo Engine: Opening '${args[2] || 'photo.avif'}'
Display P3 Wide Color Gamut &bull; 4096x2732 &bull; Hardware Lanczos 3 Acceleration
`;
          } else {
            termHistory.textContent += `DAXOS Default Media Suite (dmedia) v1.10.2026 'Rhino'
Subcommands: play <file>, view <file>, info <file>, eq, spatial, library
`;
          }
          break;
        case 'daxbro':
          termHistory.textContent += `DaXBro Chromium Browser v1.10.2026 'Rhino'
Chromium Core: 132.0.6834.83 &bull; Blink: 6.12 &bull; V8: 13.2 &bull; WebGPU: Active
Landlock LSM ABI v5 Sandbox: Enforced &bull; DaxShield: 452,180 filter rules active
`;
          break;
"""

    if "case 'ping':" not in content and "case 'dnet':" in content:
        content = content.replace("case 'dnet':", ping_terminal_case + "        case 'dnet':", 1)
        print("[OK] Added direct 'ping', 'dmedia', and 'daxbro' commands to terminal execution")

    # 6. UPDATE DOCK TOOLTIPS TO BE CRYSTAL CLEAR
    content = content.replace(
        '<div class="dock-tooltip">Spatial Audio</div>',
        '<div class="dock-tooltip">DaxMedia Suite (Audio, Video &amp; Photos)</div>'
    )
    content = content.replace(
        '<div class="dock-tooltip">DaXBro Browser</div>',
        '<div class="dock-tooltip">DaXBro (Chromium Browser)</div>'
    )
    content = content.replace(
        '<div class="dock-tooltip">Finder</div>',
        '<div class="dock-tooltip">Finder (Files &amp; Storage)</div>'
    )

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] Successfully updated src/ui/desktop_preview/index.html with all requested enhancements!")

if __name__ == "__main__":
    main()
