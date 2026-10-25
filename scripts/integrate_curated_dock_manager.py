#!/usr/bin/env python3
"""
integrate_curated_dock_manager.py
Implements curated, dynamic dock management (macOS & Windows 11 Parity):
- Only a few pinned apps appear in the main dock bar by default (Finder, DaXBro, DCODX, Terminal, Settings).
- Launchpad provides access to all 24+ applications.
- Running unpinned apps dynamically appear in the dock while open, and disappear when closed.
- Right-click context menu on dock items: "Simpan di Dock Bar" / "Hapus dari Dock Bar" / "Tutup".
- Right-click context menu in Launchpad: "Tambahkan ke Dock Bar" / "Buka Aplikasi".
- Full persistence in localStorage.
"""

import sys
from pathlib import Path

INDEX_HTML = Path("src/ui/desktop_preview/index.html")

def main():
    print("[1/4] Reading index.html...")
    html = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Add Dock Context Menu CSS
    dock_ctx_css = """
    /* DOCK & LAUNCHPAD CONTEXT MENU & DYNAMIC DOCK */
    .dock-context-menu {
      position: fixed;
      background: rgba(22, 24, 34, 0.94);
      backdrop-filter: blur(24px) saturate(180%);
      -webkit-backdrop-filter: blur(24px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 10px;
      box-shadow: 0 14px 38px rgba(0, 0, 0, 0.65), 0 2px 8px rgba(0, 0, 0, 0.35);
      padding: 6px;
      min-width: 180px;
      z-index: 100001;
      display: none;
      color: #FFFFFF;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 12px;
    }
    .dock-ctx-header {
      font-size: 11px;
      font-weight: 700;
      color: #9CA3AF;
      padding: 4px 8px 6px 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      margin-bottom: 4px;
    }
    .dock-ctx-item {
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: background 0.15s ease;
    }
    .dock-ctx-item:hover {
      background: rgba(10, 132, 255, 0.85);
      color: #FFFFFF;
    }
    .dock-ctx-item.danger:hover {
      background: rgba(239, 68, 68, 0.85);
    }
    """

    if ".dock-context-menu" not in html:
        html = html.replace(".dock-item {", dock_ctx_css + "\n    .dock-item {")
        print("[OK] Injected dock context menu CSS")

    # 2. Replace static dock contents with dynamic container
    old_dock_start = '<div class="dock-container">'
    old_dock_end = '<!-- ========================================================================\n       DREXUI APPLICATION LAUNCHPAD / ALL APPS OVERLAY (macOS & UBUNTU GNOME PARITY)\n       ======================================================================== -->'

    start_idx = html.find(old_dock_start)
    end_idx = html.find(old_dock_end)

    if start_idx != -1 and end_idx != -1:
        new_dock_markup = """<div class="dock-container">
    <div class="dock" id="main-dock">
      <!-- Pinned & Running Apps Rendered Dynamically by renderDaxosDock() -->
    </div>
  </div>

  <!-- DOCK CONTEXT MENU (macOS / Windows 11 Parity) -->
  <div id="dock-context-menu" class="dock-context-menu">
    <div class="dock-ctx-header" id="dock-ctx-title">Nama Aplikasi</div>
    <div class="dock-ctx-item" id="dock-ctx-open" onclick="dockCtxOpenApp()">
      <svg style="width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2;"><polygon points="5,3 19,12 5,21"/></svg>
      <span>Buka Jendela</span>
    </div>
    <div class="dock-ctx-item" id="dock-ctx-pin-toggle" onclick="dockCtxTogglePin()">
      <svg style="width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2;"><path d="M12 2 L12 18 M5 9 L19 9"/></svg>
      <span id="dock-ctx-pin-label">Simpan di Dock Bar</span>
    </div>
    <div class="dock-ctx-item danger" id="dock-ctx-close" onclick="dockCtxCloseApp()">
      <svg style="width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 2;"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      <span>Tutup Aplikasi</span>
    </div>
  </div>

  <!-- DOCK TOAST NOTIFICATION -->
  <div id="dock-toast" style="position: fixed; bottom: 85px; left: 50%; transform: translateX(-50%) translateY(20px); background: rgba(15, 23, 42, 0.94); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 20px; padding: 8px 18px; color: #FFFFFF; font-size: 12px; font-weight: 600; opacity: 0; pointer-events: none; transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); z-index: 100000; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
    <span id="dock-toast-text">Aplikasi ditambahkan ke Dock Bar</span>
  </div>

  """
        html = html[:start_idx] + new_dock_markup + html[end_idx:]
        print("[OK] Replaced static dock markup with dynamic main-dock & context menu")

    # 3. Add Dynamic Dock JavaScript Logic
    dock_js = """
    // ============================================================================
    // DAXOS DYNAMIC & CURATED DOCK BAR CONTROLLER (macOS & WINDOWS 11 PARITY)
    // ============================================================================
    const DAXOS_DOCK_REGISTRY = {
      'win-finder': { name: 'Finder', icon: '#icon-finder', permanent: true },
      'win-daxbro': { name: 'DaXBro Browser', icon: '#icon-daxbro' },
      'win-ide': { name: 'DCODX Studio', icon: '#icon-ide' },
      'win-terminal': { name: 'Terminal', icon: '#icon-terminal' },
      'win-daxword': { name: 'DaxWord', icon: '#icon-word' },
      'win-settings': { name: 'System Settings', icon: '#icon-settings' },
      'win-camera': { name: 'Studio Camera', icon: '#icon-camera' },
      'win-editor': { name: 'dEdit Notes', icon: '#icon-editor' },
      'win-disks': { name: 'Disk Utility', icon: '#icon-disks' },
      'win-media': { name: 'DaxMedia Suite', icon: '#icon-media' },
      'win-daxdrop': { name: 'DaXDrop AirShare', icon: '#icon-daxdrop' },
      'win-activity-monitor': { name: 'Activity Monitor', icon: '#icon-monitor' },
      'win-daxsheet': { name: 'DaxSheet', icon: '#icon-sheet' },
      'win-daxslide': { name: 'DaxSlide', icon: '#icon-slide' },
      'win-daxclock': { name: 'DaxClock Jam', icon: '#icon-clock' },
      'win-daxfont': { name: 'DaxFont Tipografi', icon: '#icon-font' },
      'win-calculator': { name: 'Calculator', icon: '#icon-calculator' },
      'win-dapstore': { name: 'DapStore', icon: '#icon-dapstore' },
      'win-dxdef': { name: 'DXDEF Security', icon: '#icon-dxdef' },
      'win-installer': { name: 'Install DAXOS', icon: '#icon-installer' },
      'win-gaming-hub': { name: 'Gaming Hub', icon: '#icon-gaming-hub' },
      'win-compat-runner': { name: 'Universal Apps', icon: '#icon-compat' },
      'win-driver-settings': { name: 'Driver Settings', icon: '#icon-driver' },
      'win-network-manager': { name: 'Network & DNS', icon: '#icon-network' },
      'win-user-accounts': { name: 'User Accounts', icon: '#icon-account' },
      'win-app-manager': { name: 'App Manager', icon: '#icon-app-manager' }
    };

    const DEFAULT_PINNED_APPS = [
      'win-finder',
      'win-daxbro',
      'win-ide',
      'win-terminal',
      'win-settings'
    ];

    let currentDockCtxWinId = null;

    function getPinnedDockApps() {
      try {
        const stored = localStorage.getItem('daxos_pinned_dock_apps_v2');
        if (stored) {
          const parsed = JSON.parse(stored);
          if (Array.isArray(parsed) && parsed.length > 0) return parsed;
        }
      } catch (e) {}
      return [...DEFAULT_PINNED_APPS];
    }

    function savePinnedDockApps(arr) {
      try {
        localStorage.setItem('daxos_pinned_dock_apps_v2', JSON.stringify(arr));
      } catch (e) {}
    }

    function isAppPinned(winId) {
      const pinned = getPinnedDockApps();
      return pinned.includes(winId);
    }

    function isAppRunning(winId) {
      const win = document.getElementById(winId);
      return win && win.style.display !== 'none';
    }

    function showDockToast(msg) {
      const toast = document.getElementById('dock-toast');
      const text = document.getElementById('dock-toast-text');
      if (!toast || !text) return;
      text.innerText = msg;
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(20px)';
      }, 2000);
    }

    function renderDaxosDock() {
      const dock = document.getElementById('main-dock');
      if (!dock) return;

      const pinned = getPinnedDockApps();
      let html = '';

      // 1. Render Pinned Apps
      pinned.forEach(winId => {
        const app = DAXOS_DOCK_REGISTRY[winId];
        if (!app) return;
        const running = isAppRunning(winId);
        html += `
          <div class="dock-item" id="dock-item-${winId}" onclick="openApp('${winId}', '${app.name}')" oncontextmenu="handleDockContextMenu(event, '${winId}')">
            <div class="dock-tooltip">${app.name}</div>
            <svg class="dock-icon-svg"><use href="${app.icon}"/></svg>
            <div class="dock-dot ${running ? 'active' : ''}" id="dot-${winId}"></div>
          </div>
        `;
      });

      // 2. Determine Running but Unpinned Apps
      const runningUnpinned = [];
      Object.keys(DAXOS_DOCK_REGISTRY).forEach(winId => {
        if (!pinned.includes(winId) && isAppRunning(winId)) {
          runningUnpinned.push(winId);
        }
      });

      // If there are unpinned running apps, render a subtle divider then the running apps
      if (runningUnpinned.length > 0) {
        html += '<div class="dock-divider"></div>';
        runningUnpinned.forEach(winId => {
          const app = DAXOS_DOCK_REGISTRY[winId];
          html += `
            <div class="dock-item" id="dock-item-${winId}" onclick="openApp('${winId}', '${app.name}')" oncontextmenu="handleDockContextMenu(event, '${winId}')">
              <div class="dock-tooltip">${app.name} (Berjalan)</div>
              <svg class="dock-icon-svg"><use href="${app.icon}"/></svg>
              <div class="dock-dot active" id="dot-${winId}"></div>
            </div>
          `;
        });
      }

      // 3. Permanent System Utilities (Divider + Launchpad + Trash)
      html += `
        <div class="dock-divider"></div>

        <div class="dock-item" onclick="toggleLaunchpad()" title="Semua Aplikasi (Launchpad)">
          <div class="dock-tooltip">Semua Aplikasi (Launchpad)</div>
          <svg class="dock-icon-svg"><use href="#icon-launchpad"/></svg>
          <div class="dock-dot" id="dot-launchpad"></div>
        </div>

        <div class="dock-item" onclick="alert('Tempat sampah bersih (Trash is empty).')">
          <div class="dock-tooltip">Tempat Sampah</div>
          <svg class="dock-icon-svg"><use href="#icon-trash"/></svg>
          <div class="dock-dot" id="dot-trash"></div>
        </div>
      `;

      dock.innerHTML = html;
    }

    function handleDockContextMenu(e, winId) {
      e.preventDefault();
      e.stopPropagation();

      const app = DAXOS_DOCK_REGISTRY[winId];
      if (!app) return;

      currentDockCtxWinId = winId;
      const menu = document.getElementById('dock-context-menu');
      const title = document.getElementById('dock-ctx-title');
      const pinLabel = document.getElementById('dock-ctx-pin-label');
      const closeItem = document.getElementById('dock-ctx-close');

      if (title) title.innerText = app.name;

      const pinned = isAppPinned(winId);
      const running = isAppRunning(winId);

      if (pinLabel) {
        if (app.permanent) {
          pinLabel.innerText = 'Tetap di Dock (Sistem)';
          document.getElementById('dock-ctx-pin-toggle').style.opacity = '0.5';
          document.getElementById('dock-ctx-pin-toggle').style.pointerEvents = 'none';
        } else {
          document.getElementById('dock-ctx-pin-toggle').style.opacity = '1';
          document.getElementById('dock-ctx-pin-toggle').style.pointerEvents = 'auto';
          pinLabel.innerText = pinned ? 'Hapus dari Dock Bar' : 'Simpan di Dock Bar';
        }
      }

      if (closeItem) {
        closeItem.style.display = running ? 'flex' : 'none';
      }

      // Position context menu directly above the cursor or icon
      menu.style.display = 'block';
      const menuWidth = 190;
      const menuHeight = menu.offsetHeight || 120;
      let left = e.clientX - menuWidth / 2;
      let top = e.clientY - menuHeight - 12;

      if (left < 10) left = 10;
      if (left + menuWidth > window.innerWidth - 10) left = window.innerWidth - menuWidth - 10;
      if (top < 40) top = e.clientY + 15;

      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
    }

    function dockCtxOpenApp() {
      closeDockContextMenu();
      if (currentDockCtxWinId) {
        const app = DAXOS_DOCK_REGISTRY[currentDockCtxWinId];
        openApp(currentDockCtxWinId, app ? app.name : 'Aplikasi');
      }
    }

    function dockCtxTogglePin() {
      closeDockContextMenu();
      if (!currentDockCtxWinId) return;

      const app = DAXOS_DOCK_REGISTRY[currentDockCtxWinId];
      if (app && app.permanent) return;

      let pinned = getPinnedDockApps();
      if (pinned.includes(currentDockCtxWinId)) {
        pinned = pinned.filter(id => id !== currentDockCtxWinId);
        savePinnedDockApps(pinned);
        showDockToast(`${app.name} dihapus dari Dock Bar`);
      } else {
        pinned.push(currentDockCtxWinId);
        savePinnedDockApps(pinned);
        showDockToast(`${app.name} ditambahkan ke Dock Bar`);
      }
      renderDaxosDock();
    }

    function dockCtxCloseApp() {
      closeDockContextMenu();
      if (currentDockCtxWinId) {
        closeWindow(currentDockCtxWinId);
      }
    }

    function closeDockContextMenu() {
      const menu = document.getElementById('dock-context-menu');
      if (menu) menu.style.display = 'none';
    }

    // Close menu on click anywhere
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#dock-context-menu')) {
        closeDockContextMenu();
      }
    });

    // In Launchpad, allow right clicking items to pin/unpin to dock
    document.addEventListener('contextmenu', (e) => {
      const item = e.target.closest('.launchpad-item');
      if (item) {
        const onclickAttr = item.getAttribute('onclick') || '';
        const match = onclickAttr.match(/launchAppFromLaunchpad\\('([^']+)'/);
        if (match && match[1]) {
          const winId = match[1];
          handleDockContextMenu(e, winId);
        }
      }
    });
    """

    if "function renderDaxosDock" not in html:
        html = html.replace("// ============================================================================\n    // DAXFONT TYPOGRAPHY & FONT MANAGER CONTROLLER",
                            dock_js + "\n    // ============================================================================\n    // DAXFONT TYPOGRAPHY & FONT MANAGER CONTROLLER")
        print("[OK] Injected dynamic dock manager JS controller")

    # Hook into openApp and closeWindow so dock updates dynamically
    html = html.replace("if (dot) dot.classList.add('active');",
                        "if (dot) dot.classList.add('active');\n      renderDaxosDock();")
    html = html.replace("if (dot) dot.classList.remove('active');",
                        "if (dot) dot.classList.remove('active');\n        renderDaxosDock();")
    
    # Also initialize dock on window load
    html = html.replace("window.addEventListener('load', () => {",
                        "window.addEventListener('load', () => {\n      renderDaxosDock();")

    INDEX_HTML.write_text(html, encoding="utf-8")
    print("[SUCCESS] Fully integrated curated, user-customizable dynamic dock into index.html!")

if __name__ == "__main__":
    main()
