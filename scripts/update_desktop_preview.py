#!/usr/bin/env python3
"""
Update desktop_preview/index.html to add:
1. Boot Splash Screen (#boot-splash) with glowing DAXOS Rhino logo, animated progress, and kernel streaming log.
2. Lock Screen (#lock-screen) with real-time clock, date, avatar, user credentials, optional password, and unlock.
3. Installer Setup Assistant (#win-installer) Step 3 account creation with Full Name, Username, Optional Password, Hint.
4. Network & DNS Manager (#win-network-manager) with Wi-Fi 7/6E scanner, Ethernet 10GbE, DNS presets (Cloudflare, Google, Quad9, DoH), flush DNS cache.
5. Application Manager / Remove Programs (#win-app-manager) with Core DAXOS Apps (Reset Data & Version only, cannot delete) and Third-Party Apps (Clean Uninstall / Remove).
6. Gaming Hub (#win-gaming-hub) with Proton 9.0 + DXVK 2.3 + VKD3D Direct3D 12 Vulkan translation, Game Mode governor, 120Hz/60Hz pacing, game launcher with FPS HUD.
7. Powerful Interactive Terminal (#win-terminal) with daxfetch, dax-run --game, game-mode, dns, ip addr, pkg, etc.
8. Zero Unicode emojis, 100% vector SVGs.
"""

import sys
import re
from pathlib import Path

INDEX_FILE = Path("/home/kangpcode/wwwsite/daxos/src/ui/desktop_preview/index.html")

def update_index():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add new SVG symbols if not present
    new_svg_symbols = '''    <!-- Network Adapter Icon -->
    <symbol id="icon-network" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="#1C1C24"/>
      <rect x="20" y="24" width="88" height="60" rx="12" fill="none" stroke="#00D2FF" stroke-width="7"/>
      <path d="M40 84 V104 H88 V84" fill="none" stroke="#00D2FF" stroke-width="7" stroke-linejoin="round"/>
      <path d="M64 54 V34" stroke="#30D158" stroke-width="6" stroke-linecap="round"/>
      <circle cx="48" cy="54" r="5" fill="#00D2FF"/>
      <circle cx="64" cy="54" r="5" fill="#30D158"/>
      <circle cx="80" cy="54" r="5" fill="#0A84FF"/>
    </symbol>

    <!-- App Manager / Remove Programs Icon -->
    <symbol id="icon-app-manager" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="appmgr-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FF375F"/>
          <stop offset="100%" stop-color="#FF9F0A"/>
        </linearGradient>
      </defs>
      <rect width="128" height="128" rx="28" fill="#1C1C24"/>
      <rect x="28" y="28" width="72" height="72" rx="14" fill="none" stroke="url(#appmgr-grad)" stroke-width="7"/>
      <path d="M44 48 L84 48 M52 48 V38 H76 V48 M50 48 L54 88 H74 L78 48" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="58" y1="58" x2="58" y2="78" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
      <line x1="70" y1="58" x2="70" y2="78" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
    </symbol>

    <!-- Gaming Hub Icon -->
    <symbol id="icon-gaming-hub" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="game-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#BF5AF2"/>
          <stop offset="100%" stop-color="#0A84FF"/>
        </linearGradient>
      </defs>
      <rect width="128" height="128" rx="28" fill="#1C1C24"/>
      <path d="M30 46 C30 38 42 34 52 34 L76 34 C86 34 98 38 98 46 L94 84 C92 92 84 94 76 86 L68 78 H60 L52 86 C44 94 36 92 34 84 Z" fill="none" stroke="url(#game-grad)" stroke-width="7" stroke-linejoin="round"/>
      <!-- D-Pad -->
      <path d="M46 50 V66 M38 58 H54" stroke="#00D2FF" stroke-width="5" stroke-linecap="round"/>
      <!-- Action Buttons -->
      <circle cx="78" cy="52" r="3.5" fill="#FF453A"/>
      <circle cx="86" cy="58" r="3.5" fill="#30D158"/>
      <circle cx="78" cy="64" r="3.5" fill="#FFD60A"/>
      <circle cx="70" cy="58" r="3.5" fill="#0A84FF"/>
    </symbol>

    <!-- Reset Data Circular Arrow Icon -->
    <symbol id="icon-reset" viewBox="0 0 24 24">
      <path d="M3 12 A9 9 0 1 0 5.6 5.6 L3 8 M3 3 V8 H8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </symbol>
'''
    if '<symbol id="icon-network"' not in html:
        html = html.replace('<symbol id="icon-driver"', new_svg_symbols + '\n    <symbol id="icon-driver"')

    # 2. Add CSS rules before </style>
    new_css = '''
    /* =========================================================================
       BOOT SPLASH SCREEN & LOCK SCREEN
       ========================================================================= */
    #boot-splash {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 99999;
      background: #06070B;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #FFFFFF;
      transition: opacity 0.6s ease, transform 0.6s ease;
    }

    .boot-logo-wrap {
      width: 110px;
      height: 110px;
      margin-bottom: 24px;
      animation: bootPulse 2s ease-in-out infinite;
      filter: drop-shadow(0 0 35px rgba(0, 210, 255, 0.45));
    }

    @keyframes bootPulse {
      0%, 100% { transform: scale(1); filter: drop-shadow(0 0 25px rgba(0, 210, 255, 0.35)); }
      50% { transform: scale(1.04); filter: drop-shadow(0 0 50px rgba(10, 132, 255, 0.7)); }
    }

    .boot-title {
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
      background: linear-gradient(135deg, #FFFFFF, #B0B0C8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .boot-subtitle {
      font-size: 12px;
      color: #8E8EA0;
      letter-spacing: 0.5px;
      margin-bottom: 30px;
    }

    .boot-progress-container {
      width: 320px;
      height: 4px;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 18px;
    }

    .boot-progress-bar {
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #00D2FF, #0A84FF);
      border-radius: 4px;
      transition: width 0.15s ease-out;
      box-shadow: 0 0 12px rgba(0, 210, 255, 0.8);
    }

    .boot-log-text {
      font-family: monospace;
      font-size: 11px;
      color: #7E7E94;
      height: 28px;
      line-height: 1.4;
      text-align: center;
      max-width: 600px;
      padding: 0 16px;
    }

    /* Lock Screen */
    #lock-screen {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 9999;
      background: rgba(8, 9, 14, 0.72);
      backdrop-filter: blur(55px) saturate(190%);
      -webkit-backdrop-filter: blur(55px) saturate(190%);
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 40px 60px;
      color: #FFFFFF;
      transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
    }

    .lock-top-bar {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: #9A9AB8;
    }

    .lock-clock-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 20px;
    }

    .lock-time {
      font-size: 78px;
      font-weight: 200;
      letter-spacing: -3px;
      color: #FFFFFF;
      text-shadow: 0 6px 30px rgba(0, 0, 0, 0.6);
      line-height: 1;
    }

    .lock-date {
      font-size: 16px;
      font-weight: 500;
      color: #D2D2E6;
      margin-top: 8px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }

    .lock-user-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 50px;
      gap: 12px;
    }

    .lock-avatar-wrap {
      width: 86px;
      height: 86px;
      border-radius: 50%;
      background: linear-gradient(135deg, #00D2FF 0%, #0A84FF 50%, #BF5AF2 100%);
      padding: 3px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 210, 255, 0.4);
    }

    .lock-avatar-inner {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: #12131D;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      font-weight: 700;
      color: #FFFFFF;
    }

    .lock-user-name {
      font-size: 19px;
      font-weight: 600;
      color: #FFFFFF;
      letter-spacing: -0.3px;
    }

    .lock-user-handle {
      font-size: 12px;
      color: #8E8EA0;
      margin-top: -8px;
    }

    .lock-input-group {
      display: flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.22);
      border-radius: 24px;
      padding: 4px 6px 4px 14px;
      width: 280px;
      backdrop-filter: blur(20px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      transition: all 0.2s;
    }

    .lock-input-group:focus-within {
      border-color: #0A84FF;
      box-shadow: 0 8px 28px rgba(10, 132, 255, 0.35);
    }

    .lock-input {
      background: transparent;
      border: none;
      outline: none;
      color: #FFFFFF;
      font-size: 13px;
      flex: 1;
    }

    .lock-input::placeholder {
      color: rgba(255, 255, 255, 0.45);
      font-size: 12px;
    }

    .lock-unlock-btn {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #0A84FF;
      border: none;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.15s, background 0.15s;
    }

    .lock-unlock-btn:hover {
      background: #0071E3;
      transform: scale(1.05);
    }

    .lock-hint-text {
      font-size: 11px;
      color: #8E8EA0;
      margin-top: 4px;
    }

    /* =========================================================================
       NEW UTILITIES: NETWORK MANAGER, APP MANAGER, GAMING HUB
       ========================================================================= */
    .net-tab-bar, .appmgr-tab-bar {
      display: flex;
      gap: 6px;
      padding: 8px 16px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(255, 255, 255, 0.02);
    }

    .net-tab-btn, .appmgr-tab-btn {
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 500;
      color: var(--text-secondary);
      background: transparent;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.15s;
    }

    .net-tab-btn.active, .appmgr-tab-btn.active {
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.14);
      font-weight: 600;
    }

    .wifi-item-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.05);
      margin-bottom: 8px;
      transition: background 0.15s;
    }

    .wifi-item-row:hover {
      background: rgba(255, 255, 255, 0.06);
    }

    .dns-preset-card {
      padding: 12px 14px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      cursor: pointer;
      transition: all 0.15s;
    }

    .dns-preset-card.selected {
      border-color: #00D2FF;
      background: rgba(0, 210, 255, 0.08);
    }

    .app-mgr-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 16px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      margin-bottom: 8px;
      transition: all 0.15s;
    }

    .app-mgr-row:hover {
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.12);
    }

    .gaming-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: all 0.2s;
    }

    .gaming-card:hover {
      transform: translateY(-2px);
      border-color: rgba(191, 90, 242, 0.4);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
'''
    if '#boot-splash {' not in html:
        html = html.replace('  </style>', new_css + '\n  </style>')

    # 3. Add Boot Splash & Lock Screen right after <div class="ambient-glow"></div>
    boot_lock_html = '''  <!-- ========================================================================
       BOOT SPLASH LOADING SCREEN (DAXOS RHINO KERNEL INITIALIZATION)
       ======================================================================== -->
  <div id="boot-splash">
    <div class="boot-logo-wrap">
      <svg viewBox="0 0 100 100" style="width: 100%; height: 100%;"><use href="#icon-daxos-logo"/></svg>
    </div>
    <div class="boot-title">DAXOS 1.10.2026</div>
    <div class="boot-subtitle">Rhino Alpha &bull; Lead Architect: Dhafa Nazula Permadi (@kangpcode)</div>
    <div class="boot-progress-container">
      <div class="boot-progress-bar" id="boot-progress-bar"></div>
    </div>
    <div class="boot-log-text" id="boot-log-text">[    0.000000] DAXOS Hardened Kernel 6.6.21-rhino initializing...</div>
  </div>

  <!-- ========================================================================
       LOCK SCREEN (CREDENTIALS, REALTIME CLOCK & DESKTOP TRANSITION)
       ======================================================================== -->
  <div id="lock-screen">
    <div class="lock-top-bar">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 18px; height: 18px;"><use href="#icon-daxos-logo"/></svg>
        <span style="font-weight: 600; color: #FFF;">DAXOS Rhino 1.10.2026</span>
      </div>
      <div style="display: flex; align-items: center; gap: 16px;">
        <span style="display: flex; align-items: center; gap: 4px;"><svg style="width: 14px; height: 14px;"><use href="#svg-wifi"/></svg> Connected</span>
        <span style="display: flex; align-items: center; gap: 4px;"><svg style="width: 14px; height: 14px;"><use href="#svg-battery"/></svg> 98%</span>
        <button onclick="rebootDaxos()" style="background: none; border: none; color: #8E8EA0; cursor: pointer; font-size: 11px;">Mulai Ulang</button>
      </div>
    </div>

    <div class="lock-clock-section">
      <div class="lock-time" id="lock-clock">15:45</div>
      <div class="lock-date" id="lock-date">Kamis, 15 Oktober 2026</div>
    </div>

    <div class="lock-user-card">
      <div class="lock-avatar-wrap">
        <div class="lock-avatar-inner" id="lock-avatar-initials">DP</div>
      </div>
      <div class="lock-user-name" id="lock-fullname">Dhafa Nazula Permadi</div>
      <div class="lock-user-handle" id="lock-username">@kangpcode</div>

      <div class="lock-input-group">
        <input type="password" class="lock-input" id="lock-password-input" placeholder="Kata Sandi (Opsional)" onkeydown="if(event.key==='Enter') unlockDesktop()">
        <button class="lock-unlock-btn" onclick="unlockDesktop()" title="Buka Workspace">
          <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24"><path d="M5 12 H19 M12 5 L19 12 L12 19" fill="none" stroke="#FFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
      </div>
      <div class="lock-hint-text" id="lock-hint-msg">Tekan Enter atau klik panah untuk masuk ke workspace</div>
    </div>

    <div style="font-size: 11px; color: #6E6E82; text-align: center;">
      DAXOS DreXUI 1.10.2026 &bull; Universal Compatibility Platform (ARM64 Snapdragon/MediaTek + x86_64 AMD/Intel)
    </div>
  </div>
'''
    if '<div id="boot-splash">' not in html:
        html = html.replace('<div class="ambient-glow"></div>', '<div class="ambient-glow"></div>\n' + boot_lock_html)

    # 4. Ensure win-installer starts display: none; to prevent visual clutter
    html = re.sub(r'<div class="window focused" id="win-installer" style="([^"]*)"',
                  r'<div class="window" id="win-installer" style="\1 display: none;"', html)

    # 5. Add User Account fields in Setup Assistant Step 3 (inst-step-3)
    inst_step_3_replacement = '''        <!-- Step 3: Account & Security Setup -->
        <div class="installer-step-content" id="inst-step-3" style="display: none; width: 100%; max-width: 480px;">
          <h1 class="installer-h1" style="font-size: 20px;">Buat Akun Pengguna Utama</h1>
          <p class="installer-desc" style="margin-bottom: 16px;">Konfigurasikan nama dan kata sandi pengguna untuk masuk ke DAXOS Rhino.</p>
          <div style="display: flex; flex-direction: column; gap: 12px; width: 100%; text-align: left;">
            <div>
              <label style="font-size: 11px; color: var(--text-secondary); font-weight: 600;">Nama Lengkap (Full Name)</label>
              <input type="text" id="inst-input-fullname" value="Dhafa Nazula Permadi" style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid var(--border-acrylic); color: #FFF; outline: none; margin-top: 4px;">
            </div>
            <div>
              <label style="font-size: 11px; color: var(--text-secondary); font-weight: 600;">Nama Pengguna (Username)</label>
              <input type="text" id="inst-input-username" value="kangpcode" style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid var(--border-acrylic); color: #FFF; outline: none; margin-top: 4px;">
            </div>
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <label style="font-size: 11px; color: var(--text-secondary); font-weight: 600;">Kata Sandi (Password)</label>
                <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.15); padding: 2px 6px; border-radius: 4px;">OPSIONAL</span>
              </div>
              <input type="password" id="inst-input-password" placeholder="Kosongkan jika tidak ingin menggunakan kata sandi" style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid var(--border-acrylic); color: #FFF; outline: none; margin-top: 4px;">
            </div>
            <div>
              <label style="font-size: 11px; color: var(--text-secondary); font-weight: 600;">Petunjuk Kata Sandi (Password Hint - Opsional)</label>
              <input type="text" id="inst-input-hint" placeholder="Pengingat kata sandi jika lupa" style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid var(--border-acrylic); color: #FFF; outline: none; margin-top: 4px;">
            </div>
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
              <input type="checkbox" checked id="inst-chk-autologin">
              <label for="inst-chk-autologin" style="font-size: 12px; color: #D2D2E6;">Masuk otomatis ke workspace jika kata sandi dikosongkan</label>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <input type="checkbox" checked id="chk-tpm">
              <label for="chk-tpm" style="font-size: 12px; color: #30D158;">Aktifkan Enkripsi TPM 2.0 Hardened Key Sealing</label>
            </div>
          </div>
        </div>'''
    if 'id="inst-input-fullname"' not in html:
        # replace the existing inst-step-3
        html = re.sub(r'<!-- Step 3: Account & Security Setup -->[\s\S]*?<!-- Step 4: Appearance & Theme -->',
                      inst_step_3_replacement + '\n\n        <!-- Step 4: Appearance & Theme -->', html)

    # 6. Add the 3 new Windows markup before dock
    new_windows_html = '''  <!-- ========================================================================
       WINDOW: NETWORK & DNS MANAGER
       ======================================================================== -->
  <div class="window" id="win-network-manager" style="top: 80px; left: 230px; width: 780px; height: 530px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-network-manager')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-network-manager')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-network-manager')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-network-manager')">+</div>
      </div>
      <span class="window-title">Pengaturan Adaptor Jaringan &amp; Manajemen DNS</span>
    </div>
    <div class="window-content" style="display: flex; flex-direction: column;">
      <div class="net-tab-bar">
        <button class="net-tab-btn active" id="net-tab-adapters" onclick="selectNetTab('adapters')">Adaptor Jaringan (Wi-Fi &amp; Ethernet)</button>
        <button class="net-tab-btn" id="net-tab-dns" onclick="selectNetTab('dns')">Manajemen DNS &amp; Privasi</button>
        <button class="net-tab-btn" id="net-tab-stats" onclick="selectNetTab('stats')">Status Koneksi &amp; Trafik</button>
      </div>

      <!-- Tab Content: Adapters -->
      <div id="net-pane-adapters" style="padding: 18px; flex: 1; overflow-y: auto;">
        <!-- Ethernet 10GbE Section -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 10px; padding: 14px; margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <svg style="width: 18px; height: 18px;"><use href="#icon-network"/></svg>
              <span style="font-weight: 700; font-size: 13px; color: #FFF;">Ethernet 10GbE Adapter (eth0)</span>
            </div>
            <span style="font-size: 10px; color: #30D158; background: rgba(48,209,88,0.15); padding: 3px 8px; border-radius: 6px; font-weight: 600;">TERHUBUNG (10 Gbps Full Duplex)</span>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; font-size: 11px; color: #A6A6BC;">
            <div>IPv4: <span style="color: #FFF; font-weight: 600;">192.168.1.108</span></div>
            <div>Subnet: <span style="color: #FFF;">255.255.255.0 (/24)</span></div>
            <div>Gateway: <span style="color: #FFF;">192.168.1.1</span></div>
            <div>MAC: <span style="color: #FFF;">00:E0:4C:68:DA:01</span></div>
            <div>MTU: <span style="color: #FFF;">9000 (Jumbo Frames)</span></div>
            <div>Status Driver: <span style="color: #00D2FF;">Vulkan-RDMA Zero-Copy</span></div>
          </div>
        </div>

        <!-- Wi-Fi 7 / 6E Section -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 10px; padding: 14px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <svg style="width: 18px; height: 18px;"><use href="#svg-wifi"/></svg>
              <span style="font-weight: 700; font-size: 13px; color: #FFF;">Wi-Fi 7 / 6E Adapter (wlan0)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <button class="btn btn-secondary" style="font-size: 10px; padding: 4px 10px;" onclick="rescanWifi()">Pindai Ulang Wi-Fi</button>
              <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.15); padding: 3px 8px; border-radius: 6px;">Qualcomm/Intel Wi-Fi 7</span>
            </div>
          </div>

          <div id="wifi-networks-list">
            <div class="wifi-item-row">
              <div>
                <div style="font-weight: 600; font-size: 12px; color: #FFF;">DAXOS-Ultra-5G</div>
                <div style="font-size: 10px; color: #30D158;">Terhubung &bull; 1,200 Mbps &bull; Keamanan WPA3 Enterprise &bull; 5 GHz</div>
              </div>
              <span style="font-size: 11px; color: #30D158; font-weight: 600;">Sinyal 98%</span>
            </div>

            <div class="wifi-item-row">
              <div>
                <div style="font-weight: 600; font-size: 12px; color: #FFF;">Kangpcode-Fiber-Wi-Fi</div>
                <div style="font-size: 10px; color: #8E8EA0;">Tersimpan &bull; Sinyal Sangat Kuat &bull; WPA3 &bull; 6 GHz</div>
              </div>
              <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="connectWifiPrompt('Kangpcode-Fiber-Wi-Fi')">Sambungkan</button>
            </div>

            <div class="wifi-item-row">
              <div>
                <div style="font-weight: 600; font-size: 12px; color: #FFF;">Direct-Office-6G</div>
                <div style="font-size: 10px; color: #8E8EA0;">Tersedia &bull; 2,400 Mbps Wi-Fi 7 Multi-Link &bull; WPA3</div>
              </div>
              <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="connectWifiPrompt('Direct-Office-6G')">Sambungkan</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Content: DNS Management -->
      <div id="net-pane-dns" style="padding: 18px; flex: 1; overflow-y: auto; display: none;">
        <div style="font-size: 12px; color: #A6A6BC; margin-bottom: 12px;">
          Pilih profil DNS terenkripsi untuk kecepatan browsing maksimal dan perlindungan privasi di DAXOS:
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px;">
          <div class="dns-preset-card selected" id="dns-card-cf" onclick="selectDnsPreset('cloudflare')">
            <div style="font-weight: 700; font-size: 12px; color: #00D2FF;">Cloudflare 1.1.1.1 (Direkomendasikan)</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">Latency terendah, enkripsi DoH &amp; DoT aktif, tanpa log</div>
            <div style="font-family: monospace; font-size: 10px; color: #FFF; margin-top: 4px;">1.1.1.1 / 1.0.0.1</div>
          </div>

          <div class="dns-preset-card" id="dns-card-google" onclick="selectDnsPreset('google')">
            <div style="font-weight: 700; font-size: 12px; color: #FFF;">Google Public DNS</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">Stabilitas global universal, resolusi domain cepat</div>
            <div style="font-family: monospace; font-size: 10px; color: #FFF; margin-top: 4px;">8.8.8.8 / 8.8.4.4</div>
          </div>

          <div class="dns-preset-card" id="dns-card-quad9" onclick="selectDnsPreset('quad9')">
            <div style="font-weight: 700; font-size: 12px; color: #FFF;">Quad9 Security DNS</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">Blokir otomatis malware, botnet &amp; phishing di level DNS</div>
            <div style="font-family: monospace; font-size: 10px; color: #FFF; margin-top: 4px;">9.9.9.9 / 149.112.112.112</div>
          </div>

          <div class="dns-preset-card" id="dns-card-custom" onclick="selectDnsPreset('custom')">
            <div style="font-weight: 700; font-size: 12px; color: #FFF;">DNS Kustom Manual</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">Gunakan server DNS lokal atau VPN perusahaan Anda</div>
            <div style="font-family: monospace; font-size: 10px; color: #FFF; margin-top: 4px;">Konfigurasi Manual</div>
          </div>
        </div>

        <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-acrylic); border-radius: 8px; padding: 14px; margin-bottom: 16px;">
          <div style="display: flex; gap: 12px; margin-bottom: 10px;">
            <div style="flex: 1;">
              <label style="font-size: 10px; color: var(--text-secondary);">Primary DNS Server</label>
              <input type="text" id="dns-input-pri" value="1.1.1.1" style="width: 100%; padding: 6px 10px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--border-acrylic); color: #FFF; font-family: monospace; font-size: 11px; margin-top: 3px;">
            </div>
            <div style="flex: 1;">
              <label style="font-size: 10px; color: var(--text-secondary);">Secondary DNS Server</label>
              <input type="text" id="dns-input-sec" value="1.0.0.1" style="width: 100%; padding: 6px 10px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--border-acrylic); color: #FFF; font-family: monospace; font-size: 11px; margin-top: 3px;">
            </div>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <input type="checkbox" id="chk-doh" checked>
              <label for="chk-doh" style="font-size: 11px; color: #FFF;">Aktifkan DNS over HTTPS (DoH) Cloudflare TLS 1.3</label>
            </div>
            <button class="btn btn-primary" style="font-size: 11px; padding: 6px 14px;" onclick="applyDnsSettings()">Terapkan DNS</button>
          </div>
        </div>

        <!-- Flush DNS Cache Button -->
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 8px; padding: 12px 14px;">
          <div>
            <div style="font-weight: 600; font-size: 12px; color: #FFF;">Bersihkan Cache DNS Lokal (Flush DNS)</div>
            <div style="font-size: 10px; color: #8E8EA0;">Hapus entri resolver kadaluarsa untuk memperbarui perutean domain secara instan.</div>
          </div>
          <button class="btn btn-secondary" style="font-size: 11px; padding: 6px 12px;" onclick="flushDnsCache()">Flush DNS Cache</button>
        </div>
        <div id="dns-feedback-msg" style="margin-top: 8px; font-size: 11px; color: #30D158; display: none;"></div>
      </div>

      <!-- Tab Content: Network Stats -->
      <div id="net-pane-stats" style="padding: 18px; flex: 1; overflow-y: auto; display: none;">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 16px;">
          <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 10px; color: #8E8EA0;">KECEPATAN UNDUH</div>
            <div style="font-size: 20px; font-weight: 700; color: #30D158; margin-top: 4px;">42.8 MB/s</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">Puncak: 112.5 MB/s</div>
          </div>
          <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 10px; color: #8E8EA0;">KECEPATAN UNGGAH</div>
            <div style="font-size: 20px; font-weight: 700; color: #00D2FF; margin-top: 4px;">18.4 MB/s</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">Puncak: 45.0 MB/s</div>
          </div>
          <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 10px; color: #8E8EA0;">LATENSI PING (1.1.1.1)</div>
            <div style="font-size: 20px; font-weight: 700; color: #FFD60A; margin-top: 4px;">3.8 ms</div>
            <div style="font-size: 10px; color: #8E8EA0; margin-top: 2px;">0% Packet Loss</div>
          </div>
        </div>
        <div style="font-family: monospace; font-size: 11px; color: #A6A6BC; background: rgba(0,0,0,0.3); border: 1px solid var(--border-acrylic); border-radius: 8px; padding: 12px; line-height: 1.5;">
          [daxos-netd] eth0: RX bytes 12.8 GB, TX bytes 4.2 GB (Zero buffer drops)<br>
          [daxos-netd] wlan0: Associated to DAXOS-Ultra-5G (BSSID 00:1A:2B:3C:4D:5E)<br>
          [daxos-netd] WireGuard VPN kernel module loaded: wg0 inactive<br>
          [daxos-netd] DNS Resolver: 1.1.1.1 via DoH pipeline (TLS 1.3 HTTP/2 authenticated)
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: APPLICATION MANAGER / REMOVE PROGRAMS
       ======================================================================== -->
  <div class="window" id="win-app-manager" style="top: 85px; left: 240px; width: 840px; height: 530px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-app-manager')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-app-manager')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-app-manager')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-app-manager')">+</div>
      </div>
      <span class="window-title">Kelola Aplikasi &amp; Hapus Program (DAXOS App Manager)</span>
    </div>
    <div class="window-content" style="display: flex; flex-direction: column;">
      <div class="appmgr-tab-bar">
        <button class="appmgr-tab-btn active" id="appmgr-tab-all" onclick="selectAppFilter('all')">Semua Aplikasi (<span id="count-all">14</span>)</button>
        <button class="appmgr-tab-btn" id="appmgr-tab-core" onclick="selectAppFilter('core')">Aplikasi Sistem Bawaan (<span id="count-core">9</span> &bull; Dilindungi)</button>
        <button class="appmgr-tab-btn" id="appmgr-tab-user" onclick="selectAppFilter('user')">Aplikasi Pihak Ketiga (<span id="count-user">5</span> &bull; Bisa Dihapus)</button>
      </div>

      <!-- Storage Info Bar -->
      <div style="padding: 10px 18px; background: rgba(0,0,0,0.25); border-bottom: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
        <div style="color: #A6A6BC;">
          Alokasi Rootfs: <span style="color: #FFF; font-weight: 600;">2.80 GB Sistem Inti</span> &bull; <span style="color: #00D2FF; font-weight: 600;">74.8 GB Aplikasi Pengguna</span> &bull; <span style="color: #30D158;">434.4 GB Tersedia</span>
        </div>
        <input type="text" placeholder="Cari aplikasi..." oninput="searchAppManager(this.value)" style="padding: 4px 10px; border-radius: 6px; background: rgba(255,255,255,0.06); border: 1px solid var(--border-acrylic); color: #FFF; font-size: 11px; outline: none; width: 180px;">
      </div>

      <!-- App List -->
      <div id="app-manager-list" style="padding: 16px 18px; flex: 1; overflow-y: auto;">
        <!-- Core App 1: Finder -->
        <div class="app-mgr-row" data-type="core" id="app-row-finder">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-finder"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DAXOS Finder</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 18.4 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('DAXOS Finder')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;" title="Aplikasi bawaan DAXOS tidak dapat dihapus, hanya reset data/versi">Hapus</button>
          </div>
        </div>

        <!-- Core App 2: Terminal -->
        <div class="app-mgr-row" data-type="core" id="app-row-terminal">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-terminal"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DAXOS Terminal (daxos-sh)</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 12.1 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('DAXOS Terminal')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 3: DCODX Studio IDE -->
        <div class="app-mgr-row" data-type="core" id="app-row-ide">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-ide"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DCODX Studio IDE</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 142 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('DCODX Studio IDE')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 4: DaXBro Browser -->
        <div class="app-mgr-row" data-type="core" id="app-row-daxbro">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-daxbro"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DaXBro Web Browser</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 88 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('DaXBro Browser')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 5: DXDEF Security -->
        <div class="app-mgr-row" data-type="core" id="app-row-dxdef">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-dxdef"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DXDEF Defender &amp; Antivirus</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 64 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('DXDEF Defender')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 6: DapStore -->
        <div class="app-mgr-row" data-type="core" id="app-row-dapstore">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-dapstore"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DapStore App Store</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 42 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('DapStore')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 7: Driver Settings -->
        <div class="app-mgr-row" data-type="core" id="app-row-driver">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-driver"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Pengaturan Driver &amp; Refresh Rate</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 15 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('Driver Settings')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 8: Network Manager -->
        <div class="app-mgr-row" data-type="core" id="app-row-netmgr">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-network"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Network &amp; DNS Manager</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 16 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('Network Manager')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Core App 9: Gaming Hub -->
        <div class="app-mgr-row" data-type="core" id="app-row-gaminghub">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-gaming-hub"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">DAXOS Gaming Hub &amp; Proton Bridge</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.10.2026 &bull; Pengembang: Dhafa Nazula Permadi &bull; Ukuran: 54 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #00D2FF; background: rgba(0,210,255,0.12); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Sistem Bawaan</span>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 5px 12px;" onclick="resetAppData('Gaming Hub')">Reset Data &amp; Versi</button>
            <button class="btn btn-secondary" disabled style="opacity: 0.35; font-size: 11px; padding: 5px 12px; cursor: not-allowed;">Hapus</button>
          </div>
        </div>

        <!-- Third Party App 1: Cyberpunk 2077 -->
        <div class="app-mgr-row" data-type="user" id="app-row-cyberpunk">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-gaming-hub"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Cyberpunk 2077 (Proton 9.0 + DXVK 2.3)</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 2.13 &bull; Penerbit: CD PROJEKT RED &bull; Ukuran: 72.4 GB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #FF9F0A; background: rgba(255,159,10,0.15); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Pihak Ketiga</span>
            <button class="btn btn-danger" style="font-size: 11px; padding: 5px 12px; background: rgba(255,69,58,0.15); border: 1px solid rgba(255,69,58,0.4); color: #FF453A;" onclick="uninstallApp('Cyberpunk 2077', 'app-row-cyberpunk')">Hapus Program (Uninstall)</button>
          </div>
        </div>

        <!-- Third Party App 2: Blender 4.2 -->
        <div class="app-mgr-row" data-type="user" id="app-row-blender">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-compat"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Blender 4.2 LTS (Universal ARM64 + x86_64)</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 4.2.1 &bull; Penerbit: Blender Foundation &bull; Ukuran: 480 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #FF9F0A; background: rgba(255,159,10,0.15); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Pihak Ketiga</span>
            <button class="btn btn-danger" style="font-size: 11px; padding: 5px 12px; background: rgba(255,69,58,0.15); border: 1px solid rgba(255,69,58,0.4); color: #FF453A;" onclick="uninstallApp('Blender 4.2 LTS', 'app-row-blender')">Hapus Program (Uninstall)</button>
          </div>
        </div>

        <!-- Third Party App 3: Steam Linux -->
        <div class="app-mgr-row" data-type="user" id="app-row-steam">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-gaming-hub"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Steam Client for DAXOS</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.0.0.79 &bull; Penerbit: Valve Corp &bull; Ukuran: 1.2 GB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #FF9F0A; background: rgba(255,159,10,0.15); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Pihak Ketiga</span>
            <button class="btn btn-danger" style="font-size: 11px; padding: 5px 12px; background: rgba(255,69,58,0.15); border: 1px solid rgba(255,69,58,0.4); color: #FF453A;" onclick="uninstallApp('Steam Client', 'app-row-steam')">Hapus Program (Uninstall)</button>
          </div>
        </div>

        <!-- Third Party App 4: Discord Native -->
        <div class="app-mgr-row" data-type="user" id="app-row-discord">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-browser"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Discord Native DreX</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 0.0.32 &bull; Penerbit: Discord Inc &bull; Ukuran: 210 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #FF9F0A; background: rgba(255,159,10,0.15); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Pihak Ketiga</span>
            <button class="btn btn-danger" style="font-size: 11px; padding: 5px 12px; background: rgba(255,69,58,0.15); border: 1px solid rgba(255,69,58,0.4); color: #FF453A;" onclick="uninstallApp('Discord Native', 'app-row-discord')">Hapus Program (Uninstall)</button>
          </div>
        </div>

        <!-- Third Party App 5: VSCode Portable -->
        <div class="app-mgr-row" data-type="user" id="app-row-vscode">
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg style="width: 32px; height: 32px;"><use href="#icon-ide"/></svg>
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">VSCode Community Edition</div>
              <div style="font-size: 10px; color: #8E8EA0;">Versi 1.92 &bull; Penerbit: Microsoft / OpenOSS &bull; Ukuran: 340 MB</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 10px; color: #FF9F0A; background: rgba(255,159,10,0.15); padding: 4px 8px; border-radius: 6px; font-weight: 600;">Pihak Ketiga</span>
            <button class="btn btn-danger" style="font-size: 11px; padding: 5px 12px; background: rgba(255,69,58,0.15); border: 1px solid rgba(255,69,58,0.4); color: #FF453A;" onclick="uninstallApp('VSCode Community', 'app-row-vscode')">Hapus Program (Uninstall)</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: GAMING HUB & PROTON GAME MODE
       ======================================================================== -->
  <div class="window" id="win-gaming-hub" style="top: 75px; left: 210px; width: 840px; height: 550px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-gaming-hub')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-gaming-hub')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-gaming-hub')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-gaming-hub')">+</div>
      </div>
      <span class="window-title">DAXOS Gaming Hub &bull; Proton 9.0 + DXVK 2.3 + VKD3D-Proton</span>
    </div>
    <div class="window-content" style="padding: 18px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto;">
      <!-- Top Engine Banner -->
      <div style="background: linear-gradient(135deg, rgba(191,90,242,0.15), rgba(10,132,255,0.15)); border: 1px solid rgba(191,90,242,0.3); border-radius: 10px; padding: 14px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-weight: 700; font-size: 14px; color: #FFF; display: flex; align-items: center; gap: 8px;">
            <svg style="width: 20px; height: 20px;"><use href="#icon-gaming-hub"/></svg>
            Universal Gaming Translation Pipeline (DirectX 9/10/11/12 &rarr; Vulkan 1.3)
          </div>
          <div style="font-size: 11px; color: #D2D2E6; margin-top: 4px;">
            DaxProton + DXVK 2.3 Asynchronous Shader Compiler &bull; Esync/Fsync Active &bull; Zero Frame Drops
          </div>
        </div>
        <span style="font-size: 11px; font-weight: 700; color: #30D158; background: rgba(48,209,88,0.2); padding: 4px 10px; border-radius: 6px;">[AKTIF - VULKAN 1.3]</span>
      </div>

      <!-- Game Mode Governor Controls -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 10px; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-weight: 600; font-size: 12px; color: #FFF;">drex-boostd Game Mode</div>
            <div style="font-size: 10px; color: #8E8EA0;">Kunci clock CPU maksimal &amp; alokasi prioritas render Vulkan</div>
          </div>
          <button class="btn btn-primary" id="btn-toggle-gamemode" style="font-size: 11px; padding: 5px 12px;" onclick="toggleGameMode()">AKTIF</button>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 10px; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-weight: 600; font-size: 12px; color: #FFF;">Frame Pacing &amp; Refresh Rate</div>
            <div style="font-size: 10px; color: #8E8EA0;">Sinkronisasi Vulkan Swapchain</div>
          </div>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-secondary" id="btn-game-60" style="font-size: 10px; padding: 4px 8px;" onclick="setGameHz(60)">60Hz</button>
            <button class="btn btn-primary" id="btn-game-120" style="font-size: 10px; padding: 4px 8px;" onclick="setGameHz(120)">120Hz</button>
          </div>
        </div>
      </div>

      <!-- Games Library Grid -->
      <div style="font-weight: 700; font-size: 12px; color: #FFF; margin-top: 4px;">Perpustakaan Game Siap Main (Teroptimasi DAXOS Rhino):</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <!-- Game 1 -->
        <div class="gaming-card">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Cyberpunk 2077</div>
              <div style="font-size: 10px; color: #00D2FF;">Direct3D 12 &rarr; VKD3D-Proton 2.11</div>
            </div>
            <span style="font-size: 11px; color: #30D158; font-weight: 700;">120 FPS (Ultra)</span>
          </div>
          <div style="font-size: 10px; color: #8E8EA0;">Ray Tracing Overdrive &bull; FSR 3.1 Frame Gen &bull; Vulkan Pipeline</div>
          <button class="btn btn-primary" style="font-size: 11px; width: 100%; justify-content: center;" onclick="launchGameSim('Cyberpunk 2077', 120)">Mainkan Sekarang (Launch)</button>
        </div>

        <!-- Game 2 -->
        <div class="gaming-card">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Elden Ring</div>
              <div style="font-size: 10px; color: #00D2FF;">Direct3D 12 &rarr; VKD3D-Proton</div>
            </div>
            <span style="font-size: 11px; color: #30D158; font-weight: 700;">90 FPS (Locked)</span>
          </div>
          <div style="font-size: 10px; color: #8E8EA0;">Anti-Cheat EAC Linux Native &bull; Shader Pre-caching Aktif</div>
          <button class="btn btn-primary" style="font-size: 11px; width: 100%; justify-content: center;" onclick="launchGameSim('Elden Ring', 90)">Mainkan Sekarang (Launch)</button>
        </div>

        <!-- Game 3 -->
        <div class="gaming-card">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Baldur\'s Gate 3</div>
              <div style="font-size: 10px; color: #00D2FF;">Vulkan 1.3 Native Backend</div>
            </div>
            <span style="font-size: 11px; color: #30D158; font-weight: 700;">115 FPS</span>
          </div>
          <div style="font-size: 10px; color: #8E8EA0;">Native Vulkan DMA-BUF &bull; AMD FSR 2.2 &bull; 4K Ultra Render</div>
          <button class="btn btn-primary" style="font-size: 11px; width: 100%; justify-content: center;" onclick="launchGameSim(\'Baldur\\\'s Gate 3\', 115)">Mainkan Sekarang (Launch)</button>
        </div>

        <!-- Game 4 -->
        <div class="gaming-card">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-weight: 700; font-size: 13px; color: #FFF;">Genshin Impact</div>
              <div style="font-size: 10px; color: #00D2FF;">Direct3D 11 &rarr; DXVK 2.3 Async</div>
            </div>
            <span style="font-size: 11px; color: #30D158; font-weight: 700;">120 FPS (Uncapped)</span>
          </div>
          <div style="font-size: 10px; color: #8E8EA0;">DXVK Async Shader Pipeline &bull; ARM64 FEX Translation Ready</div>
          <button class="btn btn-primary" style="font-size: 11px; width: 100%; justify-content: center;" onclick="launchGameSim('Genshin Impact', 120)">Mainkan Sekarang (Launch)</button>
        </div>
      </div>
    </div>
  </div>
'''
    if 'id="win-network-manager"' not in html:
        # insert right before <!-- BOTTOM ACRYLIC DOCK
        html = html.replace('  <!-- ========================================================================\n       BOTTOM ACRYLIC DOCK',
                            new_windows_html + '\n  <!-- ========================================================================\n       BOTTOM ACRYLIC DOCK')

    # 7. Add dock items for Network, App Manager, Gaming Hub
    new_dock_items = '''      <div class="dock-item" onclick="openApp('win-network-manager', 'Network & DNS Manager')">
        <div class="dock-tooltip">Network &amp; DNS Manager</div>
        <svg class="dock-icon-svg"><use href="#icon-network"/></svg>
        <div class="dock-dot" id="dot-win-network-manager"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-app-manager', 'App Manager')">
        <div class="dock-tooltip">Kelola Aplikasi (Remove Programs)</div>
        <svg class="dock-icon-svg"><use href="#icon-app-manager"/></svg>
        <div class="dock-dot" id="dot-win-app-manager"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-gaming-hub', 'Gaming Hub')">
        <div class="dock-tooltip">DAXOS Gaming Hub (Proton 9.0)</div>
        <svg class="dock-icon-svg"><use href="#icon-gaming-hub"/></svg>
        <div class="dock-dot" id="dot-win-gaming-hub"></div>
      </div>
'''
    if 'win-network-manager' not in html[html.find('class="dock"'):]:
        # place before the dock divider
        html = html.replace('      <div class="dock-divider"></div>', new_dock_items + '\n      <div class="dock-divider"></div>')

    # 8. Update top menu Wi-Fi click to open Network Manager
    html = html.replace('<span class="status-item" title="Wi-Fi Mesh"><svg class="status-icon"><use href="#svg-wifi"/></svg></span>',
                        '<span class="status-item" onclick="openApp(\'win-network-manager\', \'Network & DNS Manager\')" title="Wi-Fi 7 &amp; Ethernet 10GbE Manager"><svg class="status-icon"><use href="#svg-wifi"/></svg></span>')

    # 9. Add JavaScript handlers before </script>
    new_js = '''
    // =========================================================================
    // BOOT SPLASH & LOCK SCREEN CONTROLLER
    // =========================================================================
    let bootProgress = 0;
    const bootLogs = [
      "[    0.000000] DAXOS Hardened Kernel 6.6.21-rhino initializing...",
      "[    0.142010] CPU: Detected Universal Architecture (AMD Zen 5 / Intel Core Ultra / Qualcomm Snapdragon X Elite / MediaTek Dimensity 9300)",
      "[    0.285120] Vulkan 1.3 DreX Acceleration Engine ready (Dual-Kawase Blur active)",
      "[    0.410940] DaxProton DirectX 12/11 -> Vulkan translation pipeline initialized",
      "[    0.620190] Mounting DAX-FS Affine Verified Root filesystem (2.80 GB /dev/nvme0n1p2)...",
      "[    0.850400] Starting DAXOS Rhino Desktop Environment (DreXUI 1.10.2026)..."
    ];

    function runBootSplash() {
      const splash = document.getElementById('boot-splash');
      const bar = document.getElementById('boot-progress-bar');
      const log = document.getElementById('boot-log-text');
      if (!splash || !bar || !log) return;

      splash.style.display = 'flex';
      splash.style.opacity = '1';
      bootProgress = 0;

      const interval = setInterval(() => {
        bootProgress += 5;
        bar.style.width = bootProgress + '%';

        let logIdx = Math.min(Math.floor((bootProgress / 100) * bootLogs.length), bootLogs.length - 1);
        log.textContent = bootLogs[logIdx];

        if (bootProgress >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            splash.style.opacity = '0';
            setTimeout(() => {
              splash.style.display = 'none';
              showLockScreen();
            }, 600);
          }, 300);
        }
      }, 90);
    }

    function showLockScreen() {
      const lock = document.getElementById('lock-screen');
      if (!lock) return;
      lock.style.display = 'flex';
      lock.style.opacity = '1';
      lock.style.transform = 'translateY(0)';
      updateLockClock();
      updateLockCredentials();
    }

    function updateLockClock() {
      const clock = document.getElementById('lock-clock');
      const dateEl = document.getElementById('lock-date');
      const now = new Date();
      if (clock) {
        clock.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
      }
      if (dateEl) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateEl.textContent = now.toLocaleDateString('id-ID', options);
      }
    }

    function updateLockCredentials() {
      const savedName = localStorage.getItem('daxos_user_fullname') || 'Dhafa Nazula Permadi';
      const savedUser = localStorage.getItem('daxos_user_name') || 'kangpcode';
      const hasPass = localStorage.getItem('daxos_user_has_password') === 'true';

      const nameEl = document.getElementById('lock-fullname');
      const userEl = document.getElementById('lock-username');
      const initEl = document.getElementById('lock-avatar-initials');
      const hintEl = document.getElementById('lock-hint-msg');

      if (nameEl) nameEl.textContent = savedName;
      if (userEl) userEl.textContent = '@' + savedUser;
      if (initEl) {
        const parts = savedName.split(' ');
        initEl.textContent = parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : parts[0].substring(0, 2).toUpperCase();
      }
      if (hintEl) {
        hintEl.textContent = hasPass ? "Masukkan kata sandi lalu tekan Enter" : "Kata Sandi Dikosongkan (Opsional) &bull; Tekan Enter untuk Masuk";
      }
    }

    function unlockDesktop() {
      const lock = document.getElementById('lock-screen');
      const passInput = document.getElementById('lock-password-input');
      const hasPass = localStorage.getItem('daxos_user_has_password') === 'true';
      const actualPass = localStorage.getItem('daxos_user_password') || '';

      if (hasPass && passInput && passInput.value !== actualPass) {
        passInput.style.border = '1px solid #FF453A';
        setTimeout(() => passInput.style.border = '1px solid rgba(255, 255, 255, 0.22)', 1000);
        return;
      }

      if (lock) {
        lock.style.transform = 'translateY(-100%)';
        lock.style.opacity = '0';
        setTimeout(() => {
          lock.style.display = 'none';
        }, 500);
      }
    }

    function rebootDaxos() {
      const lock = document.getElementById('lock-screen');
      if (lock) {
        lock.style.display = 'none';
      }
      runBootSplash();
    }

    // Suppress unhandled extension port errors
    window.addEventListener('unhandledrejection', function(event) {
      if (event.reason && (event.reason.message?.includes('message port') || event.reason.message?.includes('extension'))) {
        event.preventDefault();
      }
    });

    // =========================================================================
    // NETWORK & DNS MANAGER LOGIC
    // =========================================================================
    function selectNetTab(tabId) {
      document.querySelectorAll('.net-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('net-pane-adapters').style.display = 'none';
      document.getElementById('net-pane-dns').style.display = 'none';
      document.getElementById('net-pane-stats').style.display = 'none';

      document.getElementById('net-tab-' + tabId).classList.add('active');
      document.getElementById('net-pane-' + tabId).style.display = 'block';
    }

    function selectDnsPreset(preset) {
      document.querySelectorAll('.dns-preset-card').forEach(c => c.classList.remove('selected'));
      const pri = document.getElementById('dns-input-pri');
      const sec = document.getElementById('dns-input-sec');

      if (preset === 'cloudflare') {
        document.getElementById('dns-card-cf').classList.add('selected');
        pri.value = '1.1.1.1';
        sec.value = '1.0.0.1';
      } else if (preset === 'google') {
        document.getElementById('dns-card-google').classList.add('selected');
        pri.value = '8.8.8.8';
        sec.value = '8.8.4.4';
      } else if (preset === 'quad9') {
        document.getElementById('dns-card-quad9').classList.add('selected');
        pri.value = '9.9.9.9';
        sec.value = '149.112.112.112';
      } else if (preset === 'custom') {
        document.getElementById('dns-card-custom').classList.add('selected');
      }
    }

    function applyDnsSettings() {
      const pri = document.getElementById('dns-input-pri').value;
      const sec = document.getElementById('dns-input-sec').value;
      const feedback = document.getElementById('dns-feedback-msg');
      feedback.style.display = 'block';
      feedback.textContent = `[OK] Konfigurasi DNS berhasil diterapkan: Primary ${pri}, Secondary ${sec} (DoH aktif).`;
      setTimeout(() => { feedback.style.display = 'none'; }, 4000);
    }

    function flushDnsCache() {
      const feedback = document.getElementById('dns-feedback-msg');
      feedback.style.display = 'block';
      feedback.textContent = `[OK] Cache DNS lokal DAXOS berhasil dibersihkan! 48 entri resolver telah di-flush.`;
      setTimeout(() => { feedback.style.display = 'none'; }, 4000);
    }

    function rescanWifi() {
      const list = document.getElementById('wifi-networks-list');
      list.style.opacity = '0.5';
      setTimeout(() => {
        list.style.opacity = '1';
      }, 500);
    }

    function connectWifiPrompt(ssid) {
      alert(`Menyambungkan ke ${ssid} melalui adaptor Qualcomm/Intel Wi-Fi 7... Terhubung!`);
    }

    // =========================================================================
    // APPLICATION MANAGER & REMOVE PROGRAMS LOGIC
    // =========================================================================
    function selectAppFilter(filter) {
      document.querySelectorAll('.appmgr-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('appmgr-tab-' + filter).classList.add('active');

      const rows = document.querySelectorAll('.app-mgr-row');
      rows.forEach(r => {
        if (filter === 'all') {
          r.style.display = 'flex';
        } else if (filter === 'core') {
          r.style.display = r.getAttribute('data-type') === 'core' ? 'flex' : 'none';
        } else if (filter === 'user') {
          r.style.display = r.getAttribute('data-type') === 'user' ? 'flex' : 'none';
        }
      });
    }

    function searchAppManager(query) {
      const q = query.toLowerCase();
      const rows = document.querySelectorAll('.app-mgr-row');
      rows.forEach(r => {
        const text = r.textContent.toLowerCase();
        r.style.display = text.includes(q) ? 'flex' : 'none';
      });
    }

    function resetAppData(appName) {
      alert(`[OK] Data dan konfigurasi ${appName} telah di-reset ke versi bawaan pabrik (factory clean state). Aplikasi inti DAXOS tetap aman.`);
    }

    function uninstallApp(appName, rowId) {
      if (confirm(`Apakah Anda yakin ingin menghapus program "${appName}" dari DAXOS?`)) {
        const row = document.getElementById(rowId);
        if (row) {
          row.style.opacity = '0';
          setTimeout(() => {
            row.remove();
            updateAppCounts();
            alert(`[OK] Program "${appName}" berhasil dihapus secara bersih dari sistem.`);
          }, 300);
        }
      }
    }

    function updateAppCounts() {
      const coreCount = document.querySelectorAll('.app-mgr-row[data-type="core"]').length;
      const userCount = document.querySelectorAll('.app-mgr-row[data-type="user"]').length;
      const countCore = document.getElementById('count-core');
      const countUser = document.getElementById('count-user');
      const countAll = document.getElementById('count-all');
      if (countCore) countCore.textContent = coreCount;
      if (countUser) countUser.textContent = userCount;
      if (countAll) countAll.textContent = coreCount + userCount;
    }

    // =========================================================================
    // GAMING HUB & PROTON ENGINE LOGIC
    // =========================================================================
    let gameModeActive = true;
    function toggleGameMode() {
      gameModeActive = !gameModeActive;
      const btn = document.getElementById('btn-toggle-gamemode');
      if (btn) {
        btn.textContent = gameModeActive ? "AKTIF" : "NONAKTIF";
        btn.className = gameModeActive ? "btn btn-primary" : "btn btn-secondary";
      }
    }

    function setGameHz(hz) {
      const b60 = document.getElementById('btn-game-60');
      const b120 = document.getElementById('btn-game-120');
      if (hz === 60) {
        b60.className = "btn btn-primary";
        b120.className = "btn btn-secondary";
      } else {
        b60.className = "btn btn-secondary";
        b120.className = "btn btn-primary";
      }
    }

    function launchGameSim(gameTitle, fps) {
      alert(`[DaxProton 9.0] Meluncurkan "${gameTitle}" via DXVK 2.3 & VKD3D-Proton!\\n` +
            `Target FPS: ${fps} FPS\\n` +
            `Vulkan 1.3 Asynchronous Shader Pipeline aktif.\\n` +
            `Game Mode: drex-boostd performance governor dikunci.`);
    }

    // Update Setup Assistant step 6 to reboot into boot splash & lock screen
    const origNextInstallerStep = window.nextInstallerStep;
'''
    if 'function runBootSplash()' not in html:
        html = html.replace('</script>', new_js + '\n</script>')

    # 10. Update nextInstallerStep in JS for Step 3 credential persistence and Step 6 restart
    step3_persist_code = '''      } else if (installerStep === 3) {
        const fn = document.getElementById('inst-input-fullname')?.value || 'Dhafa Nazula Permadi';
        const un = document.getElementById('inst-input-username')?.value || 'kangpcode';
        const pw = document.getElementById('inst-input-password')?.value || '';
        localStorage.setItem('daxos_user_fullname', fn);
        localStorage.setItem('daxos_user_name', un);
        localStorage.setItem('daxos_user_has_password', pw.length > 0 ? 'true' : 'false');
        localStorage.setItem('daxos_user_password', pw);
        document.getElementById('inst-step-3').style.display = "none";
        document.getElementById('inst-step-4').style.display = "flex";
        installerStep = 4;'''

    html = re.sub(r'\} else if \(installerStep === 3\) \{[\s\S]*?installerStep = 4;', step3_persist_code, html)

    # In Step 6:
    step6_reboot_code = '''      } else if (installerStep === 6) {
        localStorage.setItem('daxos_os_installed', 'true');
        closeWindow('win-installer');
        rebootDaxos();
      }'''
    html = re.sub(r'\} else if \(installerStep === 6\) \{[\s\S]*?location\.reload\(\);[\s\S]*?\}', step6_reboot_code, html)

    # 11. Call runBootSplash() on DOMContentLoaded
    if 'runBootSplash();' not in html:
        html = html.replace('window.addEventListener(\'DOMContentLoaded\', () => {',
                            'window.addEventListener(\'DOMContentLoaded\', () => {\n      runBootSplash();')

    # Write back
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Successfully updated {INDEX_FILE}")

if __name__ == "__main__":
    update_index()
