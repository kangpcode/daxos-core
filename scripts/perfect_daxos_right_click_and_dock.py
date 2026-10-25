#!/usr/bin/env python3
"""
perfect_daxos_right_click_and_dock.py
Implements:
1. Exact default dock bar items requested by user:
   - Finder
   - DaXBro
   - DCODX
   - Pengaturan (Settings)
   - All Apps (Launchpad)
   - Sampah (Trash)
   Plus dynamic running apps section for unpinned apps when opened.
2. Full Right-Click Context Menus (macOS & Windows 11 Parity):
   - Desktop Wallpaper Right-Click (Folder Baru, Dokumen Baru, Terminal, Ganti Wallpaper, Pengaturan Tampilan, Tentang DAXOS)
   - Dock Bar Item Right-Click (Buka Jendela, Simpan di Dock Bar / Hapus dari Dock Bar, Tutup Aplikasi)
   - Launchpad Item Right-Click (Buka Aplikasi, Tambahkan ke Dock Bar, Info Aplikasi)
3. Wallpaper Switcher & Desktop Folder creation simulator.
4. Clean, robust script injection before </script>.
"""

import sys
from pathlib import Path

INDEX_HTML = Path("src/ui/desktop_preview/index.html")

def main():
    print("[1/4] Reading index.html...")
    html = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Inject Context Menu CSS
    ctx_css = """
    /* ==========================================================================
       ACRYLIC CONTEXT MENUS (WINDOWS 11 & MACOS PARITY)
       ========================================================================== */
    .acrylic-context-menu {
      position: fixed;
      background: rgba(20, 22, 34, 0.94);
      backdrop-filter: blur(32px) saturate(200%);
      -webkit-backdrop-filter: blur(32px) saturate(200%);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 12px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 2px 10px rgba(0, 0, 0, 0.4);
      padding: 6px;
      min-width: 210px;
      z-index: 1000000;
      display: none;
      color: #F3F4F6;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 12.5px;
      user-select: none;
    }
    .ctx-header {
      font-size: 11px;
      font-weight: 700;
      color: #9CA3AF;
      padding: 5px 10px 4px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .ctx-item {
      padding: 7px 12px;
      border-radius: 7px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      transition: all 0.12s ease;
    }
    .ctx-item:hover {
      background: #0A84FF;
      color: #FFFFFF;
    }
    .ctx-item.danger:hover {
      background: #EF4444;
      color: #FFFFFF;
    }
    .ctx-divider {
      height: 1px;
      background: rgba(255, 255, 255, 0.1);
      margin: 4px 6px;
    }
    .ctx-icon {
      width: 15px;
      height: 15px;
      flex-shrink: 0;
      stroke: currentColor;
      fill: none;
      stroke-width: 2;
    }
    .ctx-shortcut {
      font-size: 10.5px;
      opacity: 0.6;
      font-family: monospace;
    }

    /* Desktop Items Container */
    #desktop-items-layer {
      position: absolute;
      top: 45px;
      left: 15px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      z-index: 10;
      pointer-events: none;
    }
    .desktop-shortcut-item {
      pointer-events: auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 80px;
      padding: 6px 4px;
      border-radius: 8px;
      cursor: pointer;
      text-align: center;
      transition: background 0.15s;
    }
    .desktop-shortcut-item:hover {
      background: rgba(255, 255, 255, 0.12);
    }
    .desktop-shortcut-item.selected {
      background: rgba(10, 132, 255, 0.35);
      border: 1px solid rgba(10, 132, 255, 0.6);
    }
    .desktop-shortcut-title {
      font-size: 11px;
      color: #FFFFFF;
      margin-top: 4px;
      text-shadow: 0 1px 3px rgba(0,0,0,0.8);
      word-break: break-word;
      line-height: 1.2;
    }
    """

    if ".acrylic-context-menu" not in html:
        html = html.replace("/* ==========================================================================\n       BOTTOM ACRYLIC DOCK",
                            ctx_css + "\n    /* ==========================================================================\n       BOTTOM ACRYLIC DOCK")
        print("[OK] Injected context menu & desktop CSS")

    # 2. Structure the HTML Dock and Context Menus
    # Replace dock container
    dock_target_start = '<div class="dock-container">'
    dock_target_end = '<!-- ========================================================================\n       DREXUI APPLICATION LAUNCHPAD / ALL APPS OVERLAY (macOS & UBUNTU GNOME PARITY)\n       ======================================================================== -->'

    start_pos = html.find(dock_target_start)
    end_pos = html.find(dock_target_end)

    if start_pos != -1 and end_pos != -1:
        clean_dock_markup = """<!-- DESKTOP ICONS LAYER -->
  <div id="desktop-items-layer">
    <div class="desktop-shortcut-item" ondblclick="openApp('win-disks', 'Disk Utility')">
      <svg style="width: 44px; height: 44px;"><use href="#icon-disks"/></svg>
      <div class="desktop-shortcut-title">DAXOS HD</div>
    </div>
    <div class="desktop-shortcut-item" ondblclick="openApp('win-finder', 'Finder')">
      <svg style="width: 44px; height: 44px;"><use href="#icon-finder"/></svg>
      <div class="desktop-shortcut-title">Dokumen</div>
    </div>
  </div>

  <!-- DOCK BAR (Curated Default: Finder, DaXBro, DCODX, Pengaturan, All Apps, Sampah) -->
  <div class="dock-container">
    <div class="dock" id="main-dock">
      <!-- 1. Finder -->
      <div class="dock-item" id="dock-item-win-finder" onclick="openApp('win-finder', 'Finder')" oncontextmenu="handleDockContextMenu(event, 'win-finder')">
        <div class="dock-tooltip">Finder</div>
        <svg class="dock-icon-svg"><use href="#icon-finder"/></svg>
        <div class="dock-dot active" id="dot-win-finder"></div>
      </div>

      <!-- 2. DaXBro Browser -->
      <div class="dock-item" id="dock-item-win-daxbro" onclick="openApp('win-daxbro', 'DaXBro')" oncontextmenu="handleDockContextMenu(event, 'win-daxbro')">
        <div class="dock-tooltip">DaXBro Browser</div>
        <svg class="dock-icon-svg"><use href="#icon-daxbro"/></svg>
        <div class="dock-dot" id="dot-win-daxbro"></div>
      </div>

      <!-- 3. DCODX IDE -->
      <div class="dock-item" id="dock-item-win-ide" onclick="openApp('win-ide', 'DCODX IDE')" oncontextmenu="handleDockContextMenu(event, 'win-ide')">
        <div class="dock-tooltip">DCODX Studio</div>
        <svg class="dock-icon-svg"><use href="#icon-ide"/></svg>
        <div class="dock-dot" id="dot-win-ide"></div>
      </div>

      <!-- 4. Pengaturan (System Settings) -->
      <div class="dock-item" id="dock-item-win-settings" onclick="openApp('win-settings', 'System Settings')" oncontextmenu="handleDockContextMenu(event, 'win-settings')">
        <div class="dock-tooltip">System Settings</div>
        <svg class="dock-icon-svg"><use href="#icon-settings"/></svg>
        <div class="dock-dot" id="dot-win-settings"></div>
      </div>

      <!-- Dynamic Running Apps Container -->
      <div id="dock-dynamic-running-group" style="display: contents;"></div>

      <div class="dock-divider"></div>

      <!-- 5. All Apps (Launchpad) -->
      <div class="dock-item" onclick="toggleLaunchpad()" title="Semua Aplikasi (All Apps)" oncontextmenu="handleLaunchpadDockContextMenu(event)">
        <div class="dock-tooltip">Semua Aplikasi (All Apps)</div>
        <svg class="dock-icon-svg"><use href="#icon-launchpad"/></svg>
        <div class="dock-dot" id="dot-launchpad"></div>
      </div>

      <!-- 6. Sampah (Trash) -->
      <div class="dock-item" onclick="openTrashDialog()" oncontextmenu="handleTrashContextMenu(event)">
        <div class="dock-tooltip">Tempat Sampah</div>
        <svg class="dock-icon-svg"><use href="#icon-trash"/></svg>
        <div class="dock-dot" id="dot-trash"></div>
      </div>
    </div>
  </div>

  <!-- DOCK CONTEXT MENU (macOS & Windows 11 Parity) -->
  <div id="dock-context-menu" class="acrylic-context-menu">
    <div class="ctx-header" id="dock-ctx-title">Aplikasi DAXOS</div>
    <div class="ctx-item" id="dock-ctx-open" onclick="dockCtxOpenApp()">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21"/></svg>
        <span>Buka Jendela</span>
      </div>
      <span class="ctx-shortcut">Enter</span>
    </div>
    <div class="ctx-item" id="dock-ctx-pin-toggle" onclick="dockCtxTogglePin()">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><path d="M12 2 L12 18 M5 9 L19 9"/></svg>
        <span id="dock-ctx-pin-label">Simpan di Dock Bar</span>
      </div>
    </div>
    <div class="ctx-divider"></div>
    <div class="ctx-item danger" id="dock-ctx-close" onclick="dockCtxCloseApp()">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        <span>Tutup Aplikasi</span>
      </div>
      <span class="ctx-shortcut">Cmd+Q</span>
    </div>
  </div>

  <!-- DESKTOP WALLPAPER CONTEXT MENU (macOS & Windows 11 Parity) -->
  <div id="desktop-context-menu" class="acrylic-context-menu">
    <div class="ctx-header">Desktop DAXOS 1.10.2026</div>
    <div class="ctx-item" onclick="createDesktopFolder(); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
        <span>Folder Baru</span>
      </div>
      <span class="ctx-shortcut">Shift+Cmd+N</span>
    </div>
    <div class="ctx-item" onclick="openApp('win-editor', 'dEdit'); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <span>Dokumen Teks Baru (dEdit)</span>
      </div>
    </div>
    <div class="ctx-item" onclick="openApp('win-terminal', 'Terminal'); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
        <span>Buka di Terminal (daxsh)</span>
      </div>
    </div>
    <div class="ctx-divider"></div>
    <div class="ctx-item" onclick="cycleDesktopWallpaper(); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        <span>Ganti Latar Belakang (Wallpaper)</span>
      </div>
      <span class="ctx-shortcut">Space</span>
    </div>
    <div class="ctx-item" onclick="openApp('win-settings', 'System Settings'); switchSettingsTab('display'); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        <span>Pengaturan Tampilan &amp; 240Hz...</span>
      </div>
    </div>
    <div class="ctx-item" onclick="toggleLaunchpad(); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
        <span>Semua Aplikasi (Launchpad)</span>
      </div>
      <span class="ctx-shortcut">Super+A</span>
    </div>
    <div class="ctx-divider"></div>
    <div class="ctx-item" onclick="openApp('win-about', 'About DAXOS'); closeAllContextMenus();">
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg class="ctx-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        <span>Tentang DAXOS 1.10.2026...</span>
      </div>
    </div>
  </div>

  <!-- DOCK TOAST NOTIFICATION -->
  <div id="dock-toast" style="position: fixed; bottom: 85px; left: 50%; transform: translateX(-50%) translateY(20px); background: rgba(15, 23, 42, 0.94); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 20px; padding: 8px 18px; color: #FFFFFF; font-size: 12px; font-weight: 600; opacity: 0; pointer-events: none; transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); z-index: 100000; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
    <span id="dock-toast-text">Aplikasi ditambahkan ke Dock Bar</span>
  </div>

  """
        html = html[:start_pos] + clean_dock_markup + html[end_pos:]
        print("[OK] Injected curated default dock & dual context menus (Dock + Desktop)")

    # 3. Add Comprehensive JS logic right before </script>
    full_js = """
    // ============================================================================
    // DAXOS POWERFUL CONTEXT MENUS & CURATED DOCK BAR (WINDOWS 11 & MACOS PARITY)
    // ============================================================================
    const DAXOS_DOCK_REGISTRY = {
      'win-finder': { name: 'Finder', icon: '#icon-finder', permanent: true },
      'win-daxbro': { name: 'DaXBro Browser', icon: '#icon-daxbro' },
      'win-ide': { name: 'DCODX Studio', icon: '#icon-ide' },
      'win-settings': { name: 'System Settings', icon: '#icon-settings', permanent: true },
      'win-terminal': { name: 'Terminal', icon: '#icon-terminal' },
      'win-daxword': { name: 'DaxWord', icon: '#icon-word' },
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

    // User's explicit default pinned set: Finder, DaXBro, DCODX, Pengaturan (+ Launchpad & Trash)
    const DEFAULT_PINNED_APPS = [
      'win-finder',
      'win-daxbro',
      'win-ide',
      'win-settings'
    ];

    let currentDockCtxWinId = null;

    function getPinnedDockApps() {
      try {
        const stored = localStorage.getItem('daxos_pinned_dock_v3');
        if (stored) {
          const parsed = JSON.parse(stored);
          if (Array.isArray(parsed) && parsed.length > 0) return parsed;
        }
      } catch (e) {}
      return [...DEFAULT_PINNED_APPS];
    }

    function savePinnedDockApps(arr) {
      try {
        localStorage.setItem('daxos_pinned_dock_v3', JSON.stringify(arr));
      } catch (e) {}
    }

    function isAppPinned(winId) {
      return getPinnedDockApps().includes(winId);
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
      }, 2200);
    }

    function renderDaxosDock() {
      const dock = document.getElementById('main-dock');
      if (!dock) return;

      const pinned = getPinnedDockApps();
      const dynamicGroup = document.getElementById('dock-dynamic-running-group');

      // 1. Update dot active status for pinned items in HTML
      pinned.forEach(winId => {
        let item = document.getElementById(`dock-item-${winId}`);
        const running = isAppRunning(winId);
        if (item) {
          const dot = item.querySelector('.dock-dot');
          if (dot) {
            if (running) dot.classList.add('active');
            else dot.classList.remove('active');
          }
        }
      });

      // 2. Identify running apps that are NOT pinned
      const runningUnpinned = [];
      Object.keys(DAXOS_DOCK_REGISTRY).forEach(winId => {
        if (!pinned.includes(winId) && isAppRunning(winId)) {
          runningUnpinned.push(winId);
        }
      });

      // Render running unpinned apps into dynamic group
      if (dynamicGroup) {
        if (runningUnpinned.length > 0) {
          let html = '<div class="dock-divider"></div>';
          runningUnpinned.forEach(winId => {
            const app = DAXOS_DOCK_REGISTRY[winId];
            if (!app) return;
            html += `
              <div class="dock-item" id="dock-item-${winId}" onclick="openApp('${winId}', '${app.name}')" oncontextmenu="handleDockContextMenu(event, '${winId}')">
                <div class="dock-tooltip">${app.name}</div>
                <svg class="dock-icon-svg"><use href="${app.icon}"/></svg>
                <div class="dock-dot active" id="dot-${winId}"></div>
              </div>
            `;
          });
          dynamicGroup.innerHTML = html;
        } else {
          dynamicGroup.innerHTML = '';
        }
      }
    }

    // Dock Right-Click Context Menu
    function handleDockContextMenu(e, winId) {
      e.preventDefault();
      e.stopPropagation();

      const app = DAXOS_DOCK_REGISTRY[winId];
      if (!app) return;

      currentDockCtxWinId = winId;
      closeAllContextMenus();

      const menu = document.getElementById('dock-context-menu');
      const title = document.getElementById('dock-ctx-title');
      const pinToggle = document.getElementById('dock-ctx-pin-toggle');
      const pinLabel = document.getElementById('dock-ctx-pin-label');
      const closeItem = document.getElementById('dock-ctx-close');

      if (title) title.innerText = app.name;

      const pinned = isAppPinned(winId);
      const running = isAppRunning(winId);

      if (pinToggle && pinLabel) {
        if (app.permanent) {
          pinLabel.innerText = 'Tetap di Dock (Sistem)';
          pinToggle.style.opacity = '0.5';
          pinToggle.style.pointerEvents = 'none';
        } else {
          pinToggle.style.opacity = '1';
          pinToggle.style.pointerEvents = 'auto';
          pinLabel.innerText = pinned ? 'Hapus dari Dock Bar' : 'Simpan di Dock Bar';
        }
      }

      if (closeItem) {
        closeItem.style.display = running ? 'flex' : 'none';
      }

      positionContextMenu(menu, e.clientX, e.clientY - 120);
    }

    function handleLaunchpadDockContextMenu(e) {
      e.preventDefault();
      e.stopPropagation();
      closeAllContextMenus();
      const menu = document.getElementById('dock-context-menu');
      const title = document.getElementById('dock-ctx-title');
      const pinToggle = document.getElementById('dock-ctx-pin-toggle');
      const closeItem = document.getElementById('dock-ctx-close');

      if (title) title.innerText = 'Semua Aplikasi (Launchpad)';
      if (pinToggle) pinToggle.style.display = 'none';
      if (closeItem) closeItem.style.display = 'none';

      positionContextMenu(menu, e.clientX, e.clientY - 80);
    }

    function handleTrashContextMenu(e) {
      e.preventDefault();
      e.stopPropagation();
      closeAllContextMenus();
      alert('Tempat sampah bersih (Trash is empty).');
    }

    function openTrashDialog() {
      alert('Tempat Sampah DAXOS: Tidak ada berkas yang dihapus.');
    }

    function dockCtxOpenApp() {
      closeAllContextMenus();
      if (currentDockCtxWinId) {
        const app = DAXOS_DOCK_REGISTRY[currentDockCtxWinId];
        openApp(currentDockCtxWinId, app ? app.name : 'Aplikasi');
      }
    }

    function dockCtxTogglePin() {
      closeAllContextMenus();
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
      closeAllContextMenus();
      if (currentDockCtxWinId) {
        closeWindow(currentDockCtxWinId);
      }
    }

    // Desktop Wallpaper Right-Click
    window.addEventListener('contextmenu', (e) => {
      // If clicking inside an open window or input, preserve normal behavior
      if (e.target.closest('.window') || e.target.closest('input') || e.target.closest('textarea')) {
        return;
      }

      // If clicking on dock or launchpad items, their individual handlers manage it
      if (e.target.closest('.dock-item')) {
        return;
      }
      if (e.target.closest('.launchpad-item')) {
        e.preventDefault();
        const item = e.target.closest('.launchpad-item');
        const onclickAttr = item.getAttribute('onclick') || '';
        const match = onclickAttr.match(/launchAppFromLaunchpad\\('([^']+)'/);
        if (match && match[1]) {
          handleDockContextMenu(e, match[1]);
        }
        return;
      }

      // Otherwise: DESKTOP RIGHT-CLICK!
      e.preventDefault();
      closeAllContextMenus();
      const menu = document.getElementById('desktop-context-menu');
      positionContextMenu(menu, e.clientX, e.clientY);
    });

    function positionContextMenu(menu, x, y) {
      if (!menu) return;
      menu.style.display = 'block';
      const menuWidth = menu.offsetWidth || 210;
      const menuHeight = menu.offsetHeight || 180;

      let left = x;
      let top = y;

      if (left + menuWidth > window.innerWidth - 10) {
        left = window.innerWidth - menuWidth - 10;
      }
      if (left < 10) left = 10;

      if (top + menuHeight > window.innerHeight - 10) {
        top = window.innerHeight - menuHeight - 10;
      }
      if (top < 38) top = 38;

      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
    }

    function closeAllContextMenus() {
      document.querySelectorAll('.acrylic-context-menu').forEach(m => m.style.display = 'none');
    }

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.acrylic-context-menu')) {
        closeAllContextMenus();
      }
    });

    // Wallpaper Switcher
    const DAXOS_WALLPAPERS = [
      {
        name: 'Cyberpunk Rhino (Ungu Neon)',
        style: 'radial-gradient(circle at 50% 30%, #311042 0%, #0F172A 70%, #020617 100%)'
      },
      {
        name: 'Dark Nebula (Hitam Kosmis)',
        style: 'radial-gradient(circle at 15% 20%, #ff2d55 0%, transparent 40%), radial-gradient(circle at 85% 15%, #ff9500 0%, transparent 45%), radial-gradient(circle at 50% 60%, #5856d6 0%, transparent 55%), radial-gradient(circle at 80% 85%, #007aff 0%, transparent 50%), #101018'
      },
      {
        name: 'Big Sur Glow (Biru Magis)',
        style: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 40%, #EC4899 80%, #F59E0B 100%)'
      },
      {
        name: 'Oceanic 4K (Biru Samudra)',
        style: 'linear-gradient(160deg, #022C43 0%, #053F5C 40%, #115173 100%)'
      }
    ];

    let currentWallpaperIdx = 0;
    function cycleDesktopWallpaper() {
      currentWallpaperIdx = (currentWallpaperIdx + 1) % DAXOS_WALLPAPERS.length;
      const wp = DAXOS_WALLPAPERS[currentWallpaperIdx];
      document.body.style.background = wp.style;
      showDockToast(`Wallpaper: ${wp.name}`);
    }

    let folderCount = 1;
    function createDesktopFolder() {
      const layer = document.getElementById('desktop-items-layer');
      if (!layer) return;
      const folder = document.createElement('div');
      folder.className = 'desktop-shortcut-item';
      folder.innerHTML = `
        <svg style="width: 44px; height: 44px;" viewBox="0 0 128 128">
          <rect width="128" height="128" rx="28" fill="#0284C7"/>
          <path d="M24 38 L48 38 L58 48 L104 48 C108 48 112 52 112 56 V96 C112 100 108 104 104 104 H24 C20 104 16 100 16 96 V46 C16 42 20 38 24 38 Z" fill="#FFFFFF"/>
        </svg>
        <div class="desktop-shortcut-title">Folder Baru ${folderCount++}</div>
      `;
      folder.ondblclick = () => openApp('win-finder', 'Finder');
      layer.appendChild(folder);
      showDockToast('Folder Baru dibuat di Desktop');
    }

    // Initialize Dock on DOM Load
    window.addEventListener('load', () => {
      renderDaxosDock();
    });
    """

    if "function handleDockContextMenu" not in html:
        html = html.replace("  </script>\n</body>", full_js + "\n  </script>\n</body>")
        print("[OK] Appended full JavaScript context menu and dock controller before </script>")

    INDEX_HTML.write_text(html, encoding="utf-8")
    print("[SUCCESS] Fully perfected right-click context menus and curated dock bar!")

if __name__ == "__main__":
    main()
