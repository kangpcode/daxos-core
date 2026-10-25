#!/usr/bin/env python3
"""
enhance_duraserv_centered_titles_and_dock_autohide.py

Performs major enterprise upgrades on DAXOS:
1. Centered Window Header Titles across ALL windows:
   - Ensures .window-title is centered horizontally and vertically at the top of every window header
   - Fixes inline flex alignment so icons and text sit in the exact horizontal center
   - Sets traffic lights and right-side controls to higher z-index so they remain fully interactive
2. Dock Auto-Hide & Behavior Setting (macOS + Windows 11 + Ubuntu GNOME Parity):
   - Smooth animated slide-down transition when applications are opened/active
   - Instant slide-up when cursor hovers near the bottom edge of screen
   - Settings in System Settings -> Tampilan & DreXUI with 3 modes:
     * Standar (Selalu Tampil)
     * Auto-Hide Cerdas (Sembunyi otomatis saat jendela terbuka, muncul saat kursor ke bawah)
     * Selalu Sembunyi Penuh
   - Persists preference to localStorage
3. DuraServ Web Server & Developer Stack Suite (Laragon + XAMPP + FlyEnv Parity):
   - Complete GUI window (win-duraserv)
   - Master Start All / Stop All toggle
   - Individual service ON/OFF switches with ports, PIDs, and SLAs:
     * Web Servers: Nginx (80, 443 Auto-SSL), Apache 2.4 (8080)
     * Runtimes: PHP Multiplexer (v8.1, v8.2, v8.3, v8.4 switcher, Port 9000), Node.js (3000), Golang (8081), V-Lang (8082), Python ASGI (8000)
     * Databases: MySQL 8.4 LTS (3306), MariaDB 11.4 (3307), PostgreSQL 17 (5432), Redis 7.4 (6379)
   - Quick developer actions:
     * Buka Web (http://localhost) in DaXBro
     * Database GUI Manager (Adminer)
     * Buat Virtual Host & Auto-SSL (.test / .dax)
     * Buka Terminal di Web Root (/var/www/html)
     * Edit Konfigurasi (nginx.conf, php.ini, my.cnf, redis.conf)
   - Realtime log stream console
   - DuraServ SVG vector icon, Dock icon, Launchpad item, Finder app item, and terminal integration
   - Systemd services list update
"""

from pathlib import Path
import re
import sys

INDEX_HTML = Path("src/ui/desktop_preview/index.html")

def main():
    if not INDEX_HTML.exists():
        print(f"Error: {INDEX_HTML} not found.")
        sys.exit(1)

    html = INDEX_HTML.read_text(encoding="utf-8")
    original_len = len(html)
    print(f"Loaded {INDEX_HTML} ({original_len} bytes)")

    # -------------------------------------------------------------------------
    # 1. Centered Window Header Titles & Right-Side Actions Z-Index CSS
    # -------------------------------------------------------------------------
    # Update .window-title CSS to guarantee centering
    old_title_css = """.window-title {
      position: absolute;
      left: 0;
      right: 0;
      text-align: center;
      font-size: 13px;
      font-weight: 600;
      color: #E2E2EC;
      pointer-events: none;
    }"""

    new_title_css = """.window-title {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      gap: 8px;
      font-size: 13px;
      font-weight: 600;
      color: #E2E2EC;
      pointer-events: none;
      z-index: 1;
      text-align: center;
      margin: 0 auto;
    }
    .window-header > div:not(.traffic-lights):not(.window-title),
    .window-header > button {
      position: relative;
      z-index: 5;
      pointer-events: auto;
    }"""

    if old_title_css in html:
        html = html.replace(old_title_css, new_title_css, 1)
        print("Updated .window-title CSS to guarantee centered headers across all apps.")

    # -------------------------------------------------------------------------
    # 2. Dock Auto-Hide CSS & Hover Trigger Zone
    # -------------------------------------------------------------------------
    old_dock_container_css = """.dock-container {
      position: fixed;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9000;
    }"""

    new_dock_container_css = """.dock-container {
      position: fixed;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9000;
      transition: transform 0.38s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease;
    }
    .dock-container.dock-hidden {
      transform: translateX(-50%) translateY(calc(100% + 28px)) !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }"""

    if old_dock_container_css in html:
        html = html.replace(old_dock_container_css, new_dock_container_css, 1)
        print("Updated .dock-container CSS with auto-hide transition.")

    # Add dock trigger zone at the bottom of the body
    trigger_zone_html = """  <!-- DOCK AUTO-HIDE HOVER TRIGGER ZONE -->
  <div id="dock-trigger-zone" style="position: fixed; bottom: 0; left: 0; right: 0; height: 18px; z-index: 8999; pointer-events: auto;"></div>\n"""
    
    if '<div class="dock-container">' in html and 'id="dock-trigger-zone"' not in html:
        html = html.replace('<div class="dock-container">', trigger_zone_html + '  <div class="dock-container">', 1)
        print("Injected dock-trigger-zone element.")

    # -------------------------------------------------------------------------
    # 3. Add DuraServ SVG Icon Definition to SVG Sprite Defs
    # -------------------------------------------------------------------------
    duraserv_svg_def = """      <!-- DuraServ Application Icon -->
      <g id="icon-duraserv">
        <defs>
          <linearGradient id="duraGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0284C7"/>
            <stop offset="50%" stop-color="#0369A1"/>
            <stop offset="100%" stop-color="#047857"/>
          </linearGradient>
          <linearGradient id="bladeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#0F172A"/>
            <stop offset="100%" stop-color="#1E293B"/>
          </linearGradient>
        </defs>
        <rect width="128" height="128" rx="28" fill="url(#duraGrad)"/>
        <!-- Server Blade 1 -->
        <rect x="22" y="24" width="84" height="20" rx="5" fill="url(#bladeGrad)" stroke="rgba(56,189,248,0.5)" stroke-width="1.8"/>
        <circle cx="34" cy="34" r="3.5" fill="#38BDF8"/>
        <circle cx="44" cy="34" r="3.5" fill="#34D399"/>
        <line x1="58" y1="34" x2="94" y2="34" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>
        <!-- Server Blade 2 -->
        <rect x="22" y="52" width="84" height="20" rx="5" fill="url(#bladeGrad)" stroke="rgba(52,211,153,0.5)" stroke-width="1.8"/>
        <circle cx="34" cy="62" r="3.5" fill="#34D399"/>
        <circle cx="44" cy="62" r="3.5" fill="#F59E0B"/>
        <line x1="58" y1="62" x2="94" y2="62" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>
        <!-- Server Blade 3 -->
        <rect x="22" y="80" width="84" height="20" rx="5" fill="url(#bladeGrad)" stroke="rgba(245,158,11,0.5)" stroke-width="1.8"/>
        <circle cx="34" cy="90" r="3.5" fill="#F59E0B"/>
        <circle cx="44" cy="90" r="3.5" fill="#38BDF8"/>
        <line x1="58" y1="90" x2="94" y2="90" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>
        <!-- Fast Lightning -->
        <polygon points="68,14 62,32 70,32 64,48 78,28 70,28" fill="#FDE047"/>
      </g>\n"""

    if '<g id="icon-daxdrop">' in html and 'id="icon-duraserv"' not in html:
        html = html.replace('<g id="icon-daxdrop">', duraserv_svg_def + '      <g id="icon-daxdrop">', 1)
        print("Injected #icon-duraserv SVG definition.")

    # -------------------------------------------------------------------------
    # 4. Add DuraServ to Dock, Launchpad, and Finder Apps
    # -------------------------------------------------------------------------
    # Dock item
    duraserv_dock_item = """      <!-- DuraServ (Web Server Stack - Laragon & FlyEnv Parity) -->
      <div class="dock-item" id="dock-item-win-duraserv" onclick="openApp('win-duraserv', 'DuraServ')" oncontextmenu="handleDockContextMenu(event, 'win-duraserv')">
        <div class="dock-tooltip">DuraServ (Web Stack)</div>
        <svg class="dock-icon-svg"><use href="#icon-duraserv"/></svg>
        <div class="dock-dot" id="dot-win-duraserv"></div>
      </div>\n\n"""

    ide_dock_marker = '      <!-- 3. DCODX IDE -->'
    if ide_dock_marker in html and 'dock-item-win-duraserv' not in html:
        html = html.replace(ide_dock_marker, duraserv_dock_item + ide_dock_marker, 1)
        print("Injected DuraServ into main Dock.")

    # Launchpad item
    duraserv_launchpad_item = """        <div class="launchpad-item" data-category="dev" data-name="DuraServ Web Server Laragon XAMPP FlyEnv Nginx PHP MySQL Postgres Redis Golang Python Node" onclick="launchAppFromLaunchpad('win-duraserv', 'DuraServ')">
          <svg class="launchpad-item-icon"><use href="#icon-duraserv"/></svg>
          <div class="launchpad-item-title">DuraServ</div>
          <div class="launchpad-item-desc">Web Server &amp; Dev Stack Suite</div>
        </div>\n\n"""

    ide_launchpad_marker = '        <div class="launchpad-item" data-category="dev" data-name="DCODX IDE'
    if ide_launchpad_marker in html and 'win-duraserv' not in html:
        html = html.replace(ide_launchpad_marker, duraserv_launchpad_item + ide_launchpad_marker, 1)
        print("Injected DuraServ into Launchpad grid.")

    # Finder applications list
    duraserv_finder_item = """        <div class="finder-file" onclick="selectFinderFile('DuraServ.dapp', 'DuraServ', 'All-in-One Web Server &amp; Developer Stack (Laragon &amp; FlyEnv Parity)', '2.4 KB (FAT ELF64)', 'win-duraserv', '#icon-duraserv', this)">
          <svg class="finder-file-svg"><use href="#icon-duraserv"/></svg>
          <div class="finder-file-name">DuraServ.dapp</div>
        </div>\n"""
    
    if 'Terminal.dapp</div>' in html and 'DuraServ.dapp' not in html:
        # Insert after Terminal.dapp in both renderFinderApplications and initial html
        html = html.replace('        <div class="finder-file" onclick="selectFinderFile(\'Terminal.dapp\'', duraserv_finder_item + '        <div class="finder-file" onclick="selectFinderFile(\'Terminal.dapp\'')
        print("Injected DuraServ.dapp into Finder grid.")

    # -------------------------------------------------------------------------
    # 5. Add Dock Auto-Hide Settings Card to System Settings (Tampilan & DreXUI)
    # -------------------------------------------------------------------------
    dock_settings_card = """            <!-- Dock Behavior & Auto-Hide Setting Card -->
            <div class="settings-card">
              <div class="settings-card-title">Perilaku Dock &amp; Auto-Hide (macOS Sequoia &bull; Windows 11 &bull; GNOME Parity)</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-bottom: 12px;">Pilih bagaimana Dock bereaksi saat aplikasi sedang dibuka di desktop.</div>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
                <!-- Mode 1: Standard -->
                <div id="dock-mode-standard" onclick="setDockAutoHideMode('standard')" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; cursor: pointer; background: rgba(0,0,0,0.3); text-align: center; transition: all 0.2s;">
                  <div style="font-size: 12px; font-weight: 700; color: #FFF;">Standar (Selalu Tampil)</div>
                  <div style="font-size: 10px; color: #8E8EA0; margin-top: 4px;">Dock tetap terlihat di bawah layar</div>
                </div>
                <!-- Mode 2: Smart Auto-Hide -->
                <div id="dock-mode-smart" onclick="setDockAutoHideMode('smart')" style="border: 2px solid #00D2FF; border-radius: 10px; padding: 12px; cursor: pointer; background: rgba(0,210,255,0.1); text-align: center; transition: all 0.2s;">
                  <div style="font-size: 12px; font-weight: 700; color: #FFF;">Auto-Hide Cerdas (Rekomendasi)</div>
                  <div style="font-size: 10px; color: #34D399; margin-top: 4px;">Sembunyi otomatis saat jendela aktif / terbuka, muncul saat kursor ke bawah</div>
                </div>
                <!-- Mode 3: Always Auto-Hide -->
                <div id="dock-mode-always" onclick="setDockAutoHideMode('always')" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; cursor: pointer; background: rgba(0,0,0,0.3); text-align: center; transition: all 0.2s;">
                  <div style="font-size: 12px; font-weight: 700; color: #FFF;">Selalu Sembunyi Penuh</div>
                  <div style="font-size: 10px; color: #8E8EA0; margin-top: 4px;">Hanya muncul saat kursor menyentuh tepi bawah</div>
                </div>
              </div>
            </div>\n\n"""

    appearance_surface_marker = '<div class="settings-card">\n              <div class="settings-card-title">Profil Permukaan DreXUI'
    if appearance_surface_marker in html and 'dock-mode-smart' not in html:
        html = html.replace(appearance_surface_marker, dock_settings_card + appearance_surface_marker, 1)
        print("Injected Dock Auto-Hide configuration card into System Settings.")

    # -------------------------------------------------------------------------
    # 6. Build and Inject DuraServ Window Markup (win-duraserv)
    # -------------------------------------------------------------------------
    duraserv_window_markup = """  <!-- ========================================================================
       WINDOW: DURASERV WEB SERVER & DEVELOPER STACK SUITE (LARAGON & FLYENV PARITY)
       ======================================================================== -->
  <div class="window" id="win-duraserv" style="top: 55px; left: 150px; width: 980px; height: 640px; display: none;">
    <div class="win-resize-handle rh-n"></div>
    <div class="win-resize-handle rh-s"></div>
    <div class="win-resize-handle rh-e"></div>
    <div class="win-resize-handle rh-w"></div>
    <div class="win-resize-handle rh-nw"></div>
    <div class="win-resize-handle rh-ne"></div>
    <div class="win-resize-handle rh-sw"></div>
    <div class="win-resize-handle rh-se"></div>
    <div class="window-header" onmousedown="startDrag(event, 'win-duraserv')" ondblclick="maximizeWindow('win-duraserv')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeApp('win-duraserv')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeApp('win-duraserv')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-duraserv')" onclick="maximizeWindow('win-duraserv')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 16px; height: 16px; flex-shrink: 0;"><use href="#icon-duraserv"/></svg>
        <span>DuraServ — Enterprise Web Server &amp; Developer Stack (Laragon &amp; FlyEnv Parity)</span>
      </div>
      <div style="margin-left: auto; display: flex; gap: 6px;">
        <button class="btn btn-secondary" onclick="duraServOpenWeb()" style="font-size: 11px; padding: 4px 10px; display: flex; align-items: center; gap: 4px;">
          <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><line x1="2" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="2"/></svg>
          Web (localhost)
        </button>
        <button class="btn btn-secondary" onclick="duraServOpenDb()" style="font-size: 11px; padding: 4px 10px;">
          Database GUI
        </button>
        <button class="btn btn-primary" id="btn-duraserv-master-top" onclick="duraServToggleAll()" style="font-size: 11px; padding: 4px 12px; font-weight: 700; background: #059669;">
          Stop All
        </button>
      </div>
    </div>
    <div class="window-content" style="padding: 16px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0B0E17; color: #F3F4F6;">

      <!-- Top Master Status Banner -->
      <div class="settings-card" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.12), rgba(4, 120, 87, 0.12)); border: 1px solid rgba(56, 189, 248, 0.3); padding: 16px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
          <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(4, 120, 87, 0.2); border: 1px solid #34D399; display: flex; align-items: center; justify-content: center;">
              <div id="duraserv-pulse-dot" style="width: 16px; height: 16px; border-radius: 50%; background: #34D399; box-shadow: 0 0 14px #34D399;"></div>
            </div>
            <div>
              <div style="font-size: 16px; font-weight: 800; color: #FFF; display: flex; align-items: center; gap: 8px;">
                <span id="duraserv-global-status-text">SELURUH LAYANAN AKTIF</span>
                <span style="font-size: 11px; padding: 2px 8px; border-radius: 6px; background: rgba(52,211,153,0.15); color: #34D399; font-weight: 700;" id="duraserv-active-count-badge">5/5 Berjalan</span>
              </div>
              <div style="font-size: 11px; color: #9CA3AF; margin-top: 3px;" id="duraserv-uptime-text">
                Uptime: 04j 28m &bull; RAM: 142.4 MB &bull; CPU: 0.4% &bull; SLA Watchdog: &le; 18ms
              </div>
            </div>
          </div>

          <div style="display: flex; gap: 8px;">
            <button class="btn btn-primary" id="btn-duraserv-master" onclick="duraServToggleAll()" style="font-size: 12px; padding: 8px 22px; font-weight: 800; background: #059669; border: 1px solid #10B981; box-shadow: 0 0 16px rgba(16,185,129,0.3);">
              Stop All
            </button>
            <button class="btn btn-secondary" onclick="duraServOpenTerminalRoot()" style="font-size: 12px; padding: 8px 14px; display: flex; align-items: center; gap: 6px;">
              <svg style="width: 14px; height: 14px;"><use href="#icon-terminal"/></svg>
              Terminal Root
            </button>
          </div>
        </div>

        <!-- Telemetry Details Strip -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 11px;">
          <div><span style="color: #8E8EA0;">Web Root:</span> <span style="color: #38BDF8; font-family: monospace;">/var/www/html</span></div>
          <div><span style="color: #8E8EA0;">PHP Aktif:</span> <span style="color: #34D399; font-weight: 700;" id="duraserv-active-php-label">PHP 8.3 (JIT FPM)</span></div>
          <div><span style="color: #8E8EA0;">Virtual Hosts:</span> <span style="color: #FFF; font-weight: 600;">3 Domain (.test)</span></div>
          <div><span style="color: #8E8EA0;">Auto-SSL:</span> <span style="color: #F59E0B; font-weight: 600;">Let's Encrypt / Local CA</span></div>
        </div>
      </div>

      <!-- Quick Action Developer Bar -->
      <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        <button class="btn btn-secondary" onclick="duraServOpenWeb()" style="font-size: 11px; padding: 5px 12px;">🌐 http://localhost</button>
        <button class="btn btn-secondary" onclick="duraServOpenDb()" style="font-size: 11px; padding: 5px 12px;">🗄️ Adminer Database GUI</button>
        <button class="btn btn-secondary" onclick="duraServAddVHost()" style="font-size: 11px; padding: 5px 12px;">+ Tambah Virtual Host (.test)</button>
        <select onchange="duraServSwitchPhp(this.value)" style="background: #181D2A; color: #34D399; font-weight: 700; border: 1px solid rgba(52,211,153,0.3); border-radius: 6px; padding: 4px 10px; font-size: 11px;">
          <option value="8.4">Ganti PHP: PHP 8.4 (Alpha JIT)</option>
          <option value="8.3" selected>Ganti PHP: PHP 8.3 (Stabil)</option>
          <option value="8.2">Ganti PHP: PHP 8.2 (LTS)</option>
          <option value="8.1">Ganti PHP: PHP 8.1 (Legacy)</option>
        </select>
        <select onchange="duraServOpenConfig(this.value)" style="background: #181D2A; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 4px 10px; font-size: 11px;">
          <option value="" disabled selected>Buka File Konfigurasi...</option>
          <option value="nginx.conf">nginx.conf</option>
          <option value="php.ini">php.ini</option>
          <option value="my.cnf">my.cnf (MySQL)</option>
          <option value="postgresql.conf">postgresql.conf</option>
          <option value="redis.conf">redis.conf</option>
        </select>
      </div>

      <!-- Services Grid: Web Servers, Runtimes, Databases -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">

        <!-- 1. Nginx -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">Nginx Web Proxy</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">HTTP/2, HTTP/3 QUIC &bull; v1.26.2</div>
            </div>
            <label class="switch">
              <input type="checkbox" checked id="toggle-serv-nginx" onchange="duraServToggleService('nginx', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #00D2FF; font-weight: 700;" id="port-serv-nginx">Port 80, 443</span>
            <span style="color: #34D399; font-weight: 700;" id="badge-serv-nginx">RUNNING (PID 1120)</span>
          </div>
        </div>

        <!-- 2. Apache 2.4 -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">Apache HTTP Server</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">Event MPM &bull; .htaccess &bull; v2.4.62</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="toggle-serv-apache" onchange="duraServToggleService('apache', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #8E8EA0;" id="port-serv-apache">Port 8080</span>
            <span style="color: #6B7280; font-weight: 700;" id="badge-serv-apache">STANDBY</span>
          </div>
        </div>

        <!-- 3. PHP-FPM Multiplexer -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">PHP Runtime Engine</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">PHP-FPM OpCache JIT &bull; v8.3.12</div>
            </div>
            <label class="switch">
              <input type="checkbox" checked id="toggle-serv-php" onchange="duraServToggleService('php', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #00D2FF; font-weight: 700;" id="port-serv-php">Port 9000 (FPM)</span>
            <span style="color: #34D399; font-weight: 700;" id="badge-serv-php">RUNNING (PID 1124)</span>
          </div>
        </div>

        <!-- 4. MySQL Server -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">MySQL Database Server</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">InnoDB Cluster Ready &bull; v8.4.2 LTS</div>
            </div>
            <label class="switch">
              <input type="checkbox" checked id="toggle-serv-mysql" onchange="duraServToggleService('mysql', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #00D2FF; font-weight: 700;" id="port-serv-mysql">Port 3306</span>
            <span style="color: #34D399; font-weight: 700;" id="badge-serv-mysql">RUNNING (PID 1130)</span>
          </div>
        </div>

        <!-- 5. PostgreSQL Server -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">PostgreSQL Database</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">Enterprise ACID &bull; PostGIS &bull; v17.0</div>
            </div>
            <label class="switch">
              <input type="checkbox" checked id="toggle-serv-postgres" onchange="duraServToggleService('postgres', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #00D2FF; font-weight: 700;" id="port-serv-postgres">Port 5432</span>
            <span style="color: #34D399; font-weight: 700;" id="badge-serv-postgres">RUNNING (PID 1135)</span>
          </div>
        </div>

        <!-- 6. Redis In-Memory Cache -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">Redis Cache &amp; Queue</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">In-Memory Key-Value &bull; v7.4.1</div>
            </div>
            <label class="switch">
              <input type="checkbox" checked id="toggle-serv-redis" onchange="duraServToggleService('redis', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #00D2FF; font-weight: 700;" id="port-serv-redis">Port 6379</span>
            <span style="color: #34D399; font-weight: 700;" id="badge-serv-redis">RUNNING (PID 1140)</span>
          </div>
        </div>

        <!-- 7. Node.js & Bun Server -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">Node.js / Bun Runtime</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">PM2 Process Supervisor &bull; v22.9.0 LTS</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="toggle-serv-node" onchange="duraServToggleService('node', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #8E8EA0;" id="port-serv-node">Port 3000</span>
            <span style="color: #6B7280; font-weight: 700;" id="badge-serv-node">STANDBY</span>
          </div>
        </div>

        <!-- 8. Golang Web Server -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">Golang High-Speed Web</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">Gin / Fiber &bull; v1.23.2</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="toggle-serv-golang" onchange="duraServToggleService('golang', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #8E8EA0;" id="port-serv-golang">Port 8081</span>
            <span style="color: #6B7280; font-weight: 700;" id="badge-serv-golang">STANDBY</span>
          </div>
        </div>

        <!-- 9. V-Lang (Vweb) -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">V-Lang (Vweb Engine)</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">Zero-Cost Compiled Web &bull; v0.4.8</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="toggle-serv-vlang" onchange="duraServToggleService('vlang', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #8E8EA0;" id="port-serv-vlang">Port 8082</span>
            <span style="color: #6B7280; font-weight: 700;" id="badge-serv-vlang">STANDBY</span>
          </div>
        </div>

        <!-- 10. Python ASGI (Uvicorn / FastAPI) -->
        <div class="settings-card" style="margin: 0; padding: 14px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 13px; font-weight: 700; color: #FFF;">Python ASGI Server</div>
              <div style="font-size: 11px; color: #8E8EA0; margin-top: 2px;">Uvicorn, FastAPI &bull; v3.14.0</div>
            </div>
            <label class="switch">
              <input type="checkbox" id="toggle-serv-python" onchange="duraServToggleService('python', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; font-size: 11px;">
            <span style="font-family: monospace; color: #8E8EA0;" id="port-serv-python">Port 8000</span>
            <span style="color: #6B7280; font-weight: 700;" id="badge-serv-python">STANDBY</span>
          </div>
        </div>
      </div>

      <!-- Realtime Live Server Log Console -->
      <div class="settings-card" style="margin: 0; padding: 12px 16px; background: #06080F; border: 1px solid rgba(255,255,255,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase;">Konsol Log Akses &amp; Aktivitas Server (Real-Time)</div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary" onclick="duraServClearLogs()" style="font-size: 10px; padding: 2px 8px;">Bersihkan</button>
          </div>
        </div>
        <div id="duraserv-logs-container" style="height: 110px; overflow-y: auto; font-family: monospace; font-size: 10.5px; color: #A7F3D0; line-height: 1.5; background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px;">
          <div>[DURASERV] Daemon orchestrator initialized under slice 'daxos-system.slice'</div>
          <div>[NGINX] Listening on 0.0.0.0:80, 0.0.0.0:443 (HTTP/2 TLS 1.3 Active)</div>
          <div>[PHP-FPM] Pool 'www' ready on 127.0.0.1:9000 (OpCache JIT Enabled, 128MB)</div>
          <div>[MYSQL] Server started: /var/run/mysqld/mysqld.sock, port 3306 (InnoDB Engine OK)</div>
          <div>[POSTGRES] PostgreSQL database cluster ready to accept connections on port 5432</div>
          <div>[REDIS] Server initialized: 6379 (In-memory LRU cache ready)</div>
        </div>
      </div>
    </div>
  </div>\n\n"""

    daxdrop_win_marker = '  <!-- ========================================================================\n       WINDOW: DAXDROP'
    if daxdrop_win_marker in html and 'id="win-duraserv"' not in html:
        html = html.replace(daxdrop_win_marker, duraserv_window_markup + daxdrop_win_marker, 1)
        print("Injected win-duraserv window markup.")

    # -------------------------------------------------------------------------
    # 7. JavaScript Controllers for Dock Auto-Hide & DuraServ Subsystem
    # -------------------------------------------------------------------------
    js_controllers = """
    // =========================================================================
    // DOCK AUTO-HIDE ENGINE & PREFERENCES (macOS Sequoia & Windows 11 Parity)
    // =========================================================================
    let currentDockMode = localStorage.getItem('daxos_dock_autohide_mode') || 'smart';
    let isMouseNearBottom = false;

    function setDockAutoHideMode(mode) {
      currentDockMode = mode;
      localStorage.setItem('daxos_dock_autohide_mode', mode);
      ['standard', 'smart', 'always'].forEach(m => {
        const el = document.getElementById('dock-mode-' + m);
        if (el) {
          el.style.border = (m === mode) ? '2px solid #00D2FF' : '1px solid rgba(255,255,255,0.1)';
          el.style.background = (m === mode) ? 'rgba(0, 210, 255, 0.1)' : 'rgba(0,0,0,0.3)';
        }
      });
      updateDockVisibility();
      toast(`Perilaku Dock: ${mode === 'smart' ? 'Auto-Hide Cerdas' : mode === 'always' ? 'Selalu Sembunyi' : 'Standar (Selalu Tampil)'}`);
    }

    function hasAnyOpenVisibleWindow() {
      const windows = document.querySelectorAll('.window');
      for (const w of windows) {
        if (w.style.display !== 'none' && !w.classList.contains('minimized')) {
          return true;
        }
      }
      return false;
    }

    function updateDockVisibility() {
      const dockContainer = document.querySelector('.dock-container');
      if (!dockContainer) return;

      if (currentDockMode === 'standard') {
        dockContainer.classList.remove('dock-hidden');
        return;
      }

      if (isMouseNearBottom) {
        dockContainer.classList.remove('dock-hidden');
        return;
      }

      if (currentDockMode === 'always') {
        dockContainer.classList.add('dock-hidden');
        return;
      }

      if (currentDockMode === 'smart') {
        if (hasAnyOpenVisibleWindow()) {
          dockContainer.classList.add('dock-hidden');
        } else {
          dockContainer.classList.remove('dock-hidden');
        }
      }
    }

    // Mouse movement detection near bottom of screen
    document.addEventListener('mousemove', (e) => {
      const threshold = window.innerHeight - 36;
      const inZone = e.clientY >= threshold;
      if (inZone !== isMouseNearBottom) {
        isMouseNearBottom = inZone;
        updateDockVisibility();
      }
    });

    // Keep dock visible when hovering over the dock itself
    const dockEl = document.getElementById('main-dock');
    if (dockEl) {
      dockEl.addEventListener('mouseenter', () => {
        isMouseNearBottom = true;
        updateDockVisibility();
      });
      dockEl.addEventListener('mouseleave', () => {
        isMouseNearBottom = false;
        setTimeout(updateDockVisibility, 200);
      });
    }

    // Hook into window management functions
    const origOpenApp = openApp;
    openApp = function(appId, appName) {
      origOpenApp(appId, appName);
      setTimeout(updateDockVisibility, 50);
    };

    const origCloseWindow = closeWindow;
    closeWindow = function(windowId) {
      origCloseWindow(windowId);
      setTimeout(updateDockVisibility, 50);
    };

    const origCloseApp = closeApp;
    closeApp = function(windowId) {
      origCloseApp(windowId);
      setTimeout(updateDockVisibility, 50);
    };

    const origMinimizeWindow = minimizeWindow;
    minimizeWindow = function(windowId) {
      origMinimizeWindow(windowId);
      setTimeout(updateDockVisibility, 50);
    };

    const origMinimizeApp = minimizeApp;
    minimizeApp = function(windowId) {
      origMinimizeApp(windowId);
      setTimeout(updateDockVisibility, 50);
    };

    // Restore saved dock setting on boot
    setTimeout(() => {
      setDockAutoHideMode(currentDockMode);
    }, 100);

    // =========================================================================
    // DURASERV WEB SERVER & DEVELOPER STACK CONTROLLER (LARAGON & FLYENV PARITY)
    // =========================================================================
    const duraServState = {
      isAllRunning: true,
      activePhp: '8.3',
      services: {
        nginx: { active: true, port: 'Port 80, 443', pid: 1120, name: 'Nginx Proxy' },
        apache: { active: false, port: 'Port 8080', pid: null, name: 'Apache HTTP' },
        php: { active: true, port: 'Port 9000 (FPM)', pid: 1124, name: 'PHP-FPM' },
        mysql: { active: true, port: 'Port 3306', pid: 1130, name: 'MySQL Server' },
        postgres: { active: true, port: 'Port 5432', pid: 1135, name: 'PostgreSQL' },
        redis: { active: true, port: 'Port 6379', pid: 1140, name: 'Redis Cache' },
        node: { active: false, port: 'Port 3000', pid: null, name: 'Node.js / Bun' },
        golang: { active: false, port: 'Port 8081', pid: null, name: 'Golang Server' },
        vlang: { active: false, port: 'Port 8082', pid: null, name: 'V-Lang (Vweb)' },
        python: { active: false, port: 'Port 8000', pid: null, name: 'Python ASGI' }
      }
    };

    function duraServLog(msg) {
      const c = document.getElementById('duraserv-logs-container');
      if (!c) return;
      const time = new Date().toTimeString().split(' ')[0];
      const div = document.createElement('div');
      div.textContent = `[${time}] ${msg}`;
      c.appendChild(div);
      c.scrollTop = c.scrollHeight;
    }

    function duraServClearLogs() {
      const c = document.getElementById('duraserv-logs-container');
      if (c) c.innerHTML = `<div>[DURASERV] Log dibersihkan. Memantau koneksi aktif...</div>`;
    }

    function updateDuraServUI() {
      let activeCount = 0;
      for (const [key, serv] of Object.entries(duraServState.services)) {
        const toggle = document.getElementById('toggle-serv-' + key);
        const port = document.getElementById('port-serv-' + key);
        const badge = document.getElementById('badge-serv-' + key);

        if (toggle) toggle.checked = serv.active;
        if (serv.active) {
          activeCount++;
          if (badge) {
            badge.textContent = `RUNNING (PID ${serv.pid})`;
            badge.style.color = '#34D399';
          }
          if (port) {
            port.style.color = '#00D2FF';
            port.style.fontWeight = '700';
          }
        } else {
          if (badge) {
            badge.textContent = 'STANDBY';
            badge.style.color = '#6B7280';
          }
          if (port) {
            port.style.color = '#8E8EA0';
            port.style.fontWeight = '400';
          }
        }
      }

      const txt = document.getElementById('duraserv-global-status-text');
      const badgeCnt = document.getElementById('duraserv-active-count-badge');
      const dot = document.getElementById('duraserv-pulse-dot');
      const btnMaster = document.getElementById('btn-duraserv-master');
      const btnMasterTop = document.getElementById('btn-duraserv-master-top');

      if (activeCount > 0) {
        if (txt) txt.textContent = 'SELURUH LAYANAN AKTIF';
        if (badgeCnt) {
          badgeCnt.textContent = `${activeCount}/10 Berjalan`;
          badgeCnt.style.background = 'rgba(52,211,153,0.15)';
          badgeCnt.style.color = '#34D399';
        }
        if (dot) {
          dot.style.background = '#34D399';
          dot.style.boxShadow = '0 0 14px #34D399';
        }
        if (btnMaster) {
          btnMaster.textContent = 'Stop All';
          btnMaster.style.background = '#DC2626';
          btnMaster.style.borderColor = '#EF4444';
          btnMaster.style.boxShadow = '0 0 16px rgba(239,68,68,0.3)';
        }
        if (btnMasterTop) {
          btnMasterTop.textContent = 'Stop All';
          btnMasterTop.style.background = '#DC2626';
        }
      } else {
        if (txt) txt.textContent = 'LAYANAN NONAKTIF';
        if (badgeCnt) {
          badgeCnt.textContent = '0/10 Berjalan';
          badgeCnt.style.background = 'rgba(239,68,68,0.15)';
          badgeCnt.style.color = '#F87171';
        }
        if (dot) {
          dot.style.background = '#EF4444';
          dot.style.boxShadow = '0 0 14px #EF4444';
        }
        if (btnMaster) {
          btnMaster.textContent = 'Start All';
          btnMaster.style.background = '#059669';
          btnMaster.style.borderColor = '#10B981';
          btnMaster.style.boxShadow = '0 0 16px rgba(16,185,129,0.3)';
        }
        if (btnMasterTop) {
          btnMasterTop.textContent = 'Start All';
          btnMasterTop.style.background = '#059669';
        }
      }
    }

    function duraServToggleService(key, checked) {
      const serv = duraServState.services[key];
      if (!serv) return;

      serv.active = checked;
      if (checked) {
        serv.pid = Math.floor(Math.random() * 3000) + 1100;
        duraServLog(`[${serv.name.toUpperCase()}] Layanan dimulai pada ${serv.port} (PID ${serv.pid})`);
        toast(`Layanan '${serv.name}' aktif pada ${serv.port}`);
      } else {
        duraServLog(`[${serv.name.toUpperCase()}] Layanan dihentikan (Graceful SIGTERM)`);
        serv.pid = null;
        toast(`Layanan '${serv.name}' dinonaktifkan.`);
      }
      updateDuraServUI();
    }

    function duraServToggleAll() {
      const anyActive = Object.values(duraServState.services).some(s => s.active);
      if (anyActive) {
        // Stop all
        for (const s of Object.values(duraServState.services)) {
          s.active = false;
          s.pid = null;
        }
        duraServLog("[DURASERV] Menghentikan seluruh web server dan database...");
        toast("Seluruh layanan DuraServ dinonaktifkan.");
      } else {
        // Start core
        ['nginx', 'php', 'mysql', 'postgres', 'redis'].forEach(k => {
          duraServState.services[k].active = true;
          duraServState.services[k].pid = Math.floor(Math.random() * 3000) + 1100;
        });
        duraServLog("[DURASERV] Memulai stack utama (Nginx, PHP, MySQL, Postgres, Redis)...");
        toast("Seluruh layanan web dan database DuraServ aktif!");
      }
      updateDuraServUI();
    }

    function duraServSwitchPhp(ver) {
      duraServState.activePhp = ver;
      const lbl = document.getElementById('duraserv-active-php-label');
      if (lbl) lbl.textContent = `PHP ${ver} (JIT FPM)`;
      duraServLog(`[PHP] Versi sistem dialihkan ke PHP ${ver} (OpCache JIT)`);
      toast(`PHP versi ${ver} aktif di sistem.`);
    }

    function duraServOpenWeb() {
      openApp('win-daxbro', 'DaXBro');
      const input = document.getElementById('daxbro-url-bar');
      if (input) {
        input.value = "http://localhost";
        daxbroNavigate("http://localhost");
      }
      toast("Membuka http://localhost di DaXBro Browser");
    }

    function duraServOpenDb() {
      openApp('win-daxbro', 'DaXBro');
      const input = document.getElementById('daxbro-url-bar');
      if (input) {
        input.value = "http://localhost/adminer";
        daxbroNavigate("http://localhost/adminer");
      }
      toast("Membuka Adminer Database Manager (MySQL & PostgreSQL)");
    }

    function duraServAddVHost() {
      const name = prompt("Masukkan nama domain virtual host:", "myproject.test");
      if (!name) return;
      DaxosVFS.createFile('Documents', name + '.vhost.conf', `server {\\n    listen 80;\\n    server_name ${name};\\n    root /var/www/${name.replace('.test','')};\\n    index index.php index.html;\\n}`);
      duraServLog(`[NGINX] Virtual host '${name}' berhasil dibuat dengan Auto-SSL local CA.`);
      toast(`Domain '${name}' berhasil dibuat dan diarahkan ke ~/Sites`);
    }

    function duraServOpenTerminalRoot() {
      openApp('win-terminal', 'Terminal');
      terminalCwd = '~/Sites';
      const termHistory = document.getElementById('term-history');
      if (termHistory) {
        termHistory.textContent += `\\nkangpcode@daxos [~/Sites] $ cd /var/www/html && ls -la\\ntotal 24\\ndrwxr-xr-x 4 daxos daxos 4096 Oct 20 07:00 .\\n-rw-r--r-- 1 daxos daxos 1240 Oct 20 07:00 index.php\\n-rw-r--r-- 1 daxos daxos 3420 Oct 20 07:00 info.php\\n`;
      }
    }

    function duraServOpenConfig(cfg) {
      if (!cfg) return;
      openApp('win-editor', 'dEdit');
      const content = `# DAXOS DuraServ Configuration: ${cfg}\\n# Generated on ${new Date().toLocaleString()}\\nworker_processes auto;\\nevents { worker_connections 4096; }\\n`;
      DaxosVFS.createFile('Documents', cfg, content, 'Config File', '#icon-editor');
      const file = DaxosVFS.files.find(f => f.name === cfg);
      if (file) loadVfsFileIntoEditor(file);
      toast(`Membuka '${cfg}' di dEdit`);
    }

    // Add duraserv to window.daxosSystemdServices if present
    if (window.daxosSystemdServices && !window.daxosSystemdServices.some(s => s.unit === 'duraserv.service')) {
      window.daxosSystemdServices.unshift({
        unit: 'duraserv.service',
        desc: 'Web Server & Multi-Database Orchestrator',
        status: 'active (running)',
        pid: 1118,
        slice: 'daxos-system.slice',
        memory: '142.4 MB'
      });
      renderSystemdServicesTable();
    }
"""

    if "</script>" in html:
        html = html.replace("</script>", js_controllers + "\n  </script>", 1)
        print("Injected Dock Auto-Hide and DuraServ JavaScript controllers.")

    INDEX_HTML.write_text(html, encoding="utf-8")
    new_len = len(html)
    print(f"Successfully updated {INDEX_HTML} ({original_len} -> {new_len} bytes, +{new_len - original_len} bytes).")

if __name__ == "__main__":
    main()
