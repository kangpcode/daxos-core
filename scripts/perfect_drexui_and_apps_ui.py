#!/usr/bin/env python3
"""
perfect_drexui_and_apps_ui.py

Comprehensive UI, DreXUI, and Window Management overhaul for DAXOS:
1. Fixes all broken empty getElementById() and showDockToast() calls
2. Injects full Trash application controller (renderTrash, empty, restore, properties, table/grid views)
3. Injects full DaxFont controller (waterfall, glyphs, tuning, search, catalog)
4. Adds closeApp and minimizeApp aliases
5. Implements global mousedown listener for instant window focus (anti-tumpang-tindih)
6. Implements smart staggered cascading window positioning on launch
7. Implements ultra-smooth 240Hz window dragging (.is-dragging with transition: none)
8. Adds lively Dock item launch bounce animation and fluid hover effects
9. Adds robust try/catch error boundaries around window operations (anti-crash)
"""

import sys
import re

INDEX_HTML = "src/ui/desktop_preview/index.html"

def main():
    print("[1/5] Reading index.html...")
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # =========================================================================
    # 1. ENHANCE CSS: DreXUI Liquid Acrylic Windows, Dock Bounce, Micro-Animations
    # =========================================================================
    extra_css = """
    /* ========================================================================
       DREXUI HIGH-PERFORMANCE LIQUID ACRYLIC & ANIMATION SUITE (240Hz OPTIMIZED)
       ======================================================================== */
    .window {
      transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1),
                  opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                  box-shadow 0.2s ease,
                  border-color 0.2s ease;
      will-change: transform, opacity;
    }

    .window.focused {
      border-color: rgba(0, 210, 255, 0.5) !important;
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.75), 0 0 35px rgba(0, 210, 255, 0.2), inset 1.5px 1.5px 2px rgba(255, 255, 255, 0.3) !important;
      opacity: 1 !important;
    }

    .window:not(.focused) {
      opacity: 0.96;
      border-color: rgba(255, 255, 255, 0.12);
      box-shadow: 0 16px 45px rgba(0, 0, 0, 0.55), inset 1px 1px 1.5px rgba(255, 255, 255, 0.15);
    }

    /* 240Hz Instant Drag & Resize (Zero Latency) */
    .window.is-dragging,
    .window.is-resizing {
      transition: none !important;
      user-select: none !important;
      pointer-events: auto;
      will-change: left, top, width, height;
    }

    /* Dock Item Tactile Bounce on App Launch */
    .dock-item.bouncing {
      animation: dockItemBounce 0.55s cubic-bezier(0.28, 0.84, 0.42, 1) !important;
    }

    @keyframes dockItemBounce {
      0%, 100% { transform: translateY(0) scale(1); }
      30% { transform: translateY(-22px) scale(1.18); }
      50% { transform: translateY(0) scale(0.96); }
      75% { transform: translateY(-8px) scale(1.08); }
    }

    /* Smooth Custom Scrollbars for All Windows */
    .window-content::-webkit-scrollbar,
    #trash-content-container::-webkit-scrollbar,
    #font-items-list::-webkit-scrollbar,
    #glyph-grid-container::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .window-content::-webkit-scrollbar-track,
    #trash-content-container::-webkit-scrollbar-track,
    #font-items-list::-webkit-scrollbar-track,
    #glyph-grid-container::-webkit-scrollbar-track {
      background: transparent;
    }
    .window-content::-webkit-scrollbar-thumb,
    #trash-content-container::-webkit-scrollbar-thumb,
    #font-items-list::-webkit-scrollbar-thumb,
    #glyph-grid-container::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.18);
      border-radius: 999px;
    }
    .window-content::-webkit-scrollbar-thumb:hover,
    #trash-content-container::-webkit-scrollbar-thumb:hover,
    #font-items-list::-webkit-scrollbar-thumb:hover,
    #glyph-grid-container::-webkit-scrollbar-thumb:hover {
      background: rgba(0, 210, 255, 0.45);
    }
    """

    if 'DREXUI HIGH-PERFORMANCE LIQUID ACRYLIC' not in html:
        html = html.replace('</style>', extra_css + '\n  </style>')
        print("[OK] Injected DreXUI 240Hz Animation CSS")

    # =========================================================================
    # 2. REPLACE startDrag & stopDrag FOR 240Hz ZERO-LATENCY DRAGGING
    # =========================================================================
    old_drag_pattern = r'function startDrag\(e, windowId\) \{[\s\S]*?function stopDrag\(\) \{[\s\S]*?\}'
    new_drag_code = """function startDrag(e, windowId) {
      try {
        bringToFront(windowId);
        draggingWin = document.getElementById(windowId);
        if (!draggingWin) return;

        // If window is currently maximized, restore it smoothly and center under cursor
        if (draggingWin.dataset.maximized === "true") {
          draggingWin.dataset.maximized = "false";
          const origW = parseFloat(draggingWin.dataset.origWidth) || 840;
          const origH = parseFloat(draggingWin.dataset.origHeight) || 540;
          draggingWin.style.width = origW + "px";
          draggingWin.style.height = origH + "px";
          draggingWin.style.borderRadius = "14px";
          dragOffsetX = origW / 2;
          dragOffsetY = 18;
        } else {
          const rect = draggingWin.getBoundingClientRect();
          dragOffsetX = e.clientX - rect.left;
          dragOffsetY = e.clientY - rect.top;
        }

        draggingWin.classList.add('is-dragging');
        window.addEventListener('mousemove', onDrag, { passive: false });
        window.addEventListener('mouseup', stopDrag);
      } catch (err) {
        console.warn('[DAXOS Window] Drag start error:', err);
      }
    }

    function onDrag(e) {
      if (!draggingWin) return;
      try {
        draggingWin.dataset.userMoved = "true";
        let newX = Math.max(-draggingWin.offsetWidth + 120, Math.min(window.innerWidth - 120, e.clientX - dragOffsetX));
        let newY = Math.max(32, Math.min(window.innerHeight - 80, e.clientY - dragOffsetY));
        draggingWin.style.left = newX + "px";
        draggingWin.style.top = newY + "px";
      } catch (err) {
        console.warn('[DAXOS Window] Drag move error:', err);
      }
    }

    function stopDrag() {
      if (draggingWin) {
        draggingWin.classList.remove('is-dragging');
        clampWindowPosition(draggingWin);
      }
      draggingWin = null;
      window.removeEventListener('mousemove', onDrag);
      window.removeEventListener('mouseup', stopDrag);
    }"""

    html = re.sub(old_drag_pattern, new_drag_code, html, count=1)
    print("[OK] Updated startDrag & stopDrag with 240Hz smooth dragging & bounds checking")

    # =========================================================================
    # 3. REPLACE openApp WITH SMART STAGGERED CASCADING & BOUNCE
    # =========================================================================
    old_openapp_pattern = r'function openApp\(windowId, appName\) \{[\s\S]*?if \(windowId === \'win-camera\'\) \{[\s\S]*?initCamera\(\);[\s\S]*?\}[\s\S]*?\}'
    new_openapp_code = """let cascadeSlotIndex = 0;

    function clampWindowPosition(win) {
      if (!win) return;
      const rect = win.getBoundingClientRect();
      const minTop = 32;
      const maxTop = window.innerHeight - 90;
      const minLeft = -rect.width + 120;
      const maxLeft = window.innerWidth - 120;

      let currentTop = parseFloat(win.style.top) || rect.top;
      let currentLeft = parseFloat(win.style.left) || rect.left;

      if (currentTop < minTop) win.style.top = minTop + 'px';
      if (currentTop > maxTop) win.style.top = Math.max(minTop, maxTop - 220) + 'px';
      if (currentLeft < minLeft) win.style.left = minLeft + 'px';
      if (currentLeft > maxLeft) win.style.left = Math.max(20, maxLeft - 220) + 'px';
    }

    function openApp(windowId, appName) {
      try {
        const win = document.getElementById(windowId);
        if (!win) return;

        const isMin = win.classList.contains('minimized');
        const isClosed = (win.style.display === "none" || !win.style.display);

        const dot = document.getElementById('dot-' + windowId);
        const dockItem = dot ? dot.closest('.dock-item') : document.getElementById('dock-item-' + windowId);
        
        // Trigger lively tactile dock bounce animation on launch
        if (dockItem) {
          dockItem.classList.remove('bouncing');
          void dockItem.offsetWidth;
          dockItem.classList.add('bouncing');
          setTimeout(() => dockItem.classList.remove('bouncing'), 550);
        }

        const dockRect = dockItem ? dockItem.getBoundingClientRect() : {
          left: window.innerWidth / 2 - 25,
          top: window.innerHeight - 50,
          width: 50,
          height: 50
        };

        if (isMin) {
          // macOS Unminimize / Restore from Dock Animation
          const winRect = win.getBoundingClientRect();
          const startX = (dockRect.left + dockRect.width / 2) - (winRect.left + winRect.width / 2);
          const startY = (dockRect.top + dockRect.height / 2) - (winRect.top + winRect.height / 2);

          win.classList.remove('minimized');
          win.style.display = "flex";
          win.classList.add('window-restoring');
          win.style.transform = `translate(${startX}px, ${startY}px) scale(0.1)`;
          win.style.opacity = '0';
          win.style.filter = 'blur(4px)';

          void win.offsetHeight; // force reflow

          win.style.transform = 'translate(0, 0) scale(1)';
          win.style.opacity = '1';
          win.style.filter = 'none';

          setTimeout(() => {
            win.classList.remove('window-restoring');
            win.style.transform = '';
            win.style.opacity = '';
            win.style.filter = '';
          }, 320);
        } else if (isClosed) {
          // Smart staggered non-overlapping cascade position
          if (!win.dataset.userMoved) {
            const stepX = 36;
            const stepY = 30;
            const slot = cascadeSlotIndex % 7;
            cascadeSlotIndex++;

            const targetW = win.offsetWidth || 840;
            const targetH = win.offsetHeight || 540;
            const calcLeft = Math.max(30, Math.min(window.innerWidth - targetW - 30, 140 + (slot * stepX)));
            const calcTop = Math.max(40, Math.min(window.innerHeight - targetH - 90, 60 + (slot * stepY)));

            win.style.left = calcLeft + 'px';
            win.style.top = calcTop + 'px';
          }

          win.style.display = "flex";
          win.classList.remove('minimized', 'window-closing');
          win.classList.add('window-opening');
          setTimeout(() => {
            win.classList.remove('window-opening');
          }, 260);
        } else {
          // Already open: focus pulse
          win.style.transform = 'scale(1.018)';
          setTimeout(() => win.style.transform = '', 130);
        }

        bringToFront(windowId, appName);
        if (dot) dot.classList.add('active');
        renderDaxosDock();

        // Application specific setups
        if (windowId === 'win-trash') {
          renderTrash();
        } else if (windowId === 'win-camera') {
          initCamera();
        } else if (windowId === 'win-daxfont') {
          initGlyphGrid();
        }
      } catch (err) {
        console.warn('[DAXOS openApp] Handled gracefully:', err);
      }
    }"""

    html = re.sub(old_openapp_pattern, new_openapp_code, html, count=1)
    print("[OK] Updated openApp with smart cascading, dock bounce, and anti-crash handlers")

    # =========================================================================
    # 4. FIX THE TAIL OF THE SCRIPT (REPLACE BROKEN FUNCTIONS AND ADD FULL TRASH + FONT CONTROLLERS)
    # =========================================================================
    tail_cut_target = "    function selectFontDetail(fontName) {"
    if tail_cut_target in html:
        html = html[:html.index(tail_cut_target)]

    clean_tail_controllers = """    // ============================================================================
    // APPLICATION ALIASES & WINDOW CONTROLS (ANTI-ERROR COMPATIBILITY)
    // ============================================================================
    function closeApp(windowId) {
      closeWindow(windowId);
    }

    function minimizeApp(windowId) {
      minimizeWindow(windowId);
    }

    // Global Window Click Focus (Clicking anywhere inside brings it to front)
    document.addEventListener('mousedown', (e) => {
      const win = e.target.closest('.window');
      if (win && win.id) {
        bringToFront(win.id);
      }
    }, true);

    // ============================================================================
    // TRASH / RECYCLE BIN CONTROLLER (WINDOWS 11 & MACOS PARITY)
    // ============================================================================
    let trashItems = [
      { id: 't1', name: 'Draft_Desain_UI_v1.dapp', orig: '/home/daxos/Desktop', date: '17 Okt 2026, 20:12', size: '4.2 MB', sizeBytes: 4404019, type: 'Paket .dapp', icon: '#icon-dapstore' },
      { id: 't2', name: 'Laporan_Keuangan_Q3.xlsx', orig: '/home/daxos/Documents', date: '16 Okt 2026, 14:35', size: '1.8 MB', sizeBytes: 1887436, type: 'DaxSheet (.xlsx)', icon: '#icon-sheet' },
      { id: 't3', name: 'Presentasi_Investor_Rhino.pptx', orig: '/home/daxos/Documents', date: '15 Okt 2026, 09:18', size: '12.5 MB', sizeBytes: 13107200, type: 'DaxSlide (.pptx)', icon: '#icon-slide' },
      { id: 't4', name: 'Surat_Pengunduran_Diri.docx', orig: '/home/daxos/Documents', date: '14 Okt 2026, 11:40', size: '240 KB', sizeBytes: 245760, type: 'DaxWord (.docx)', icon: '#icon-word' },
      { id: 't5', name: 'Video_Capture_Test_4K.mp4', orig: '/home/daxos/Videos', date: '12 Okt 2026, 18:22', size: '68.4 MB', sizeBytes: 71722598, type: 'Media Video (.mp4)', icon: '#icon-media' }
    ];

    let selectedTrashId = null;
    let currentTrashView = 'table';

    function renderTrash() {
      const tbody = document.getElementById('trash-tbody');
      const grid = document.getElementById('trash-grid');
      const emptyState = document.getElementById('trash-empty-state');
      const statusText = document.getElementById('trash-status-text');
      const restoreBtn = document.getElementById('btn-restore-selected');

      if (!tbody || !grid || !emptyState) return;

      if (trashItems.length === 0) {
        tbody.innerHTML = '';
        grid.innerHTML = '';
        emptyState.style.display = 'flex';
        const tbl = document.getElementById('trash-table');
        if (tbl) tbl.style.display = 'none';
        grid.style.display = 'none';
        if (statusText) statusText.textContent = '0 item | 0 MB total (Tempat Sampah Kosong)';
        if (restoreBtn) {
          restoreBtn.style.opacity = '0.5';
          restoreBtn.style.pointerEvents = 'none';
        }
        return;
      }

      emptyState.style.display = 'none';
      const tbl = document.getElementById('trash-table');
      if (currentTrashView === 'table') {
        if (tbl) tbl.style.display = 'table';
        grid.style.display = 'none';
      } else {
        if (tbl) tbl.style.display = 'none';
        grid.style.display = 'grid';
      }

      let totalBytes = trashItems.reduce((acc, it) => acc + it.sizeBytes, 0);
      let totalMB = (totalBytes / (1024 * 1024)).toFixed(1);
      if (statusText) statusText.textContent = `${trashItems.length} item | ${totalMB} MB total terpakai`;

      // Render Table Rows
      tbody.innerHTML = trashItems.map(item => {
        const isSel = (item.id === selectedTrashId);
        return `
          <tr onclick="selectTrashItem('${item.id}')" ondblclick="restoreSpecificItem('${item.id}')" style="cursor: pointer; border-bottom: 1px solid rgba(255,255,255,0.04); background: ${isSel ? 'rgba(0,210,255,0.15)' : 'transparent'};">
            <td style="padding: 10px; display: flex; align-items: center; gap: 8px;">
              <svg style="width: 20px; height: 20px; flex-shrink: 0;"><use href="${item.icon}"/></svg>
              <span style="font-weight: 600; color: #FFF;">${item.name}</span>
            </td>
            <td style="padding: 10px; color: #9CA3AF; font-family: monospace; font-size: 11px;">${item.orig}</td>
            <td style="padding: 10px; color: #9CA3AF;">${item.date}</td>
            <td style="padding: 10px; color: #38BDF8;">${item.size}</td>
            <td style="padding: 10px; color: #D1D5DB;">${item.type}</td>
            <td style="padding: 10px; text-align: right;">
              <button onclick="event.stopPropagation(); restoreSpecificItem('${item.id}')" style="background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.3); color: #34D399; font-size: 11px; padding: 3px 8px; border-radius: 4px; cursor: pointer; margin-right: 4px;">Pulihkan</button>
              <button onclick="event.stopPropagation(); deletePermanentlySpecific('${item.id}')" style="background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3); color: #F87171; font-size: 11px; padding: 3px 8px; border-radius: 4px; cursor: pointer;">Hapus</button>
            </td>
          </tr>
        `;
      }).join('');

      // Render Grid Cards
      grid.innerHTML = trashItems.map(item => {
        const isSel = (item.id === selectedTrashId);
        return `
          <div onclick="selectTrashItem('${item.id}')" ondblclick="restoreSpecificItem('${item.id}')" style="padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; background: ${isSel ? 'rgba(0,210,255,0.15)' : 'rgba(255,255,255,0.02)'}; border: 1px solid ${isSel ? '#00D2FF' : 'rgba(255,255,255,0.06)'}; display: flex; flex-direction: column; align-items: center; gap: 8px;">
            <svg style="width: 40px; height: 40px;"><use href="${item.icon}"/></svg>
            <div style="font-size: 12px; font-weight: 600; color: #FFF; word-break: break-word; line-height: 1.2;">${item.name}</div>
            <div style="font-size: 10px; color: #38BDF8;">${item.size}</div>
          </div>
        `;
      }).join('');

      if (restoreBtn) {
        if (selectedTrashId) {
          restoreBtn.style.opacity = '1';
          restoreBtn.style.pointerEvents = 'auto';
        } else {
          restoreBtn.style.opacity = '0.5';
          restoreBtn.style.pointerEvents = 'none';
        }
      }
    }

    function selectTrashItem(id) {
      selectedTrashId = id;
      renderTrash();
    }

    function setTrashViewMode(mode) {
      currentTrashView = mode;
      const tBtn = document.getElementById('trash-view-table-btn');
      const gBtn = document.getElementById('trash-view-grid-btn');
      if (tBtn && gBtn) {
        if (mode === 'table') {
          tBtn.style.background = 'rgba(255,255,255,0.15)';
          tBtn.style.color = '#FFF';
          gBtn.style.background = 'transparent';
          gBtn.style.color = '#9CA3AF';
        } else {
          gBtn.style.background = 'rgba(255,255,255,0.15)';
          gBtn.style.color = '#FFF';
          tBtn.style.background = 'transparent';
          tBtn.style.color = '#9CA3AF';
        }
      }
      renderTrash();
    }

    function restoreSpecificItem(id) {
      const item = trashItems.find(it => it.id === id);
      if (!item) return;
      trashItems = trashItems.filter(it => it.id !== id);
      selectedTrashId = null;
      renderTrash();
      showDockToast(`'${item.name}' berhasil dipulihkan ke ${item.orig}`);
    }

    function deletePermanentlySpecific(id) {
      const item = trashItems.find(it => it.id === id);
      if (!item) return;
      if (confirm(`Hapus permanen berkas '${item.name}'? Tindakan ini tidak dapat dibatalkan.`)) {
        trashItems = trashItems.filter(it => it.id !== id);
        selectedTrashId = null;
        renderTrash();
        showDockToast(`'${item.name}' dihapus permanen.`);
      }
    }

    function restoreSelectedTrashItem() {
      if (selectedTrashId) {
        restoreSpecificItem(selectedTrashId);
      }
    }

    function restoreAllTrashItems() {
      if (trashItems.length === 0) {
        alert('Tempat Sampah sudah kosong.');
        return;
      }
      const count = trashItems.length;
      trashItems = [];
      selectedTrashId = null;
      renderTrash();
      showDockToast(`Semua ${count} berkas berhasil dipulihkan ke lokasi asalnya.`);
    }

    function emptyTrashWithConfirmation() {
      if (trashItems.length === 0) {
        alert('Tempat Sampah sudah kosong.');
        return;
      }
      if (confirm(`Yakin ingin mengosongkan Tempat Sampah? Semua ${trashItems.length} item akan dihapus permanen dari subvolume Btrfs.`)) {
        trashItems = [];
        selectedTrashId = null;
        renderTrash();
        showDockToast('Tempat Sampah berhasil dikosongkan.');
      }
    }

    function showTrashProperties() {
      alert(`PROPERTI TEMPAT SAMPAH DAXOS:
• Lokasi Subvolume : /var/trash (Btrfs Copy-on-Write)
• Kapasitas Kuota  : 10.0 GB
• Terpakai Saat Ini: ${(trashItems.reduce((a,c)=>a+c.sizeBytes,0)/(1024*1024)).toFixed(2)} MB (${trashItems.length} item)
• Ruang Tersisa    : 9.91 GB
• Kebijakan Otomatis: Hapus berkas setelah 30 hari
• Enkripsi         : ChaCha20 Hardware Block Storage`);
    }

    function filterTrashItems(query) {
      const q = (query || '').toLowerCase();
      const rows = document.querySelectorAll('#trash-tbody tr');
      rows.forEach(r => {
        const text = r.textContent.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      });
    }

    // ============================================================================
    // DAXFONT TYPOGRAPHY STUDIO CONTROLLER
    // ============================================================================
    const DAX_FONT_DATA = {
      'Inter Display': {
        family: "'Inter', sans-serif",
        designer: 'Rasmus Andersson',
        license: 'SIL Open Font License 1.1',
        version: 'v4.001',
        format: 'OpenType CFF (.otf)',
        glyphs: '2,548 glyphs',
        features: 'calt, liga, tnum, cv01, ss01',
        path: '/usr/share/fonts/opentype/inter/',
        postscript: 'InterDisplay-Regular',
        pangram: 'The quick brown fox jumps over the lazy dog 1234567890'
      },
      'JetBrains Mono': {
        family: "monospace",
        designer: 'JetBrains Core Team',
        license: 'Apache License 2.0',
        version: 'v2.304',
        format: 'TrueType (.ttf)',
        glyphs: '1,480 glyphs',
        features: 'calt (Code Ligatures: =>, !=, ===), zero, ss02',
        path: '/usr/share/fonts/truetype/jetbrains/',
        postscript: 'JetBrainsMono-Regular',
        pangram: 'fn daxos_kernel_init() -> Result<(), E> { OK }'
      },
      'Fira Code': {
        family: "monospace",
        designer: 'Nikita Prokopov',
        license: 'SIL Open Font License 1.1',
        version: 'v6.2',
        format: 'OpenType CFF (.otf)',
        glyphs: '1,220 glyphs',
        features: 'calt, zero, onum, ss03',
        path: '/usr/share/fonts/opentype/firacode/',
        postscript: 'FiraCode-Regular',
        pangram: '0 <= latency && latency <= 0.045 // 45ms target'
      },
      'Playfair Display': {
        family: "Georgia, serif",
        designer: 'Claus Eggers Sorensen',
        license: 'SIL Open Font License 1.1',
        version: 'v2.102',
        format: 'TrueType (.ttf)',
        glyphs: '1,180 glyphs',
        features: 'dlig, kern, liga, swsh',
        path: '/usr/share/fonts/truetype/playfair/',
        postscript: 'PlayfairDisplay-Regular',
        pangram: 'Seni Tipografi Megah Sistem Operasi DAXOS 2026'
      },
      'Outfit': {
        family: "'Outfit', sans-serif",
        designer: 'Outfit Typography Guild',
        license: 'SIL Open Font License 1.1',
        version: 'v1.100',
        format: 'TrueType (.ttf)',
        glyphs: '1,350 glyphs',
        features: 'calt, tnum, pnum, ordn',
        path: '/usr/share/fonts/truetype/outfit/',
        postscript: 'Outfit-Regular',
        pangram: 'DAXOS 1.10.2026 Rhino: Fluid, Swift & Resilient'
      }
    };

    function selectFontDetail(fontName) {
      document.querySelectorAll('.font-list-card').forEach(c => {
        if (c.getAttribute('data-name') === fontName) {
          c.classList.add('active');
          c.style.background = 'rgba(236,72,153,0.15)';
          c.style.borderColor = 'rgba(236,72,153,0.4)';
        } else {
          c.classList.remove('active');
          c.style.background = 'rgba(255,255,255,0.03)';
          c.style.borderColor = 'transparent';
        }
      });

      const data = DAX_FONT_DATA[fontName];
      if (!data) return;

      const pPost = document.getElementById('meta-postscript');
      const pFormat = document.getElementById('meta-format');
      const pGlyphs = document.getElementById('meta-glyphs');
      const pFeat = document.getElementById('meta-features');
      const pPath = document.getElementById('meta-path');

      if (pPost) pPost.textContent = data.postscript;
      if (pFormat) pFormat.textContent = data.format;
      if (pGlyphs) pGlyphs.textContent = data.glyphs;
      if (pFeat) pFeat.textContent = data.features;
      if (pPath) pPath.textContent = data.path;

      const sampleInput = document.getElementById('font-sample-text');
      if (sampleInput) sampleInput.value = data.pangram;
      updateSampleText(data.pangram);

      document.querySelectorAll('.wf-sample').forEach(el => {
        el.style.fontFamily = data.family;
      });
    }

    function switchFontTab(tabName) {
      const tabs = ['waterfall', 'glyphs', 'meta'];
      tabs.forEach(t => {
        const btn = document.getElementById('tab-btn-' + t);
        const view = document.getElementById('tab-view-' + t);
        if (btn) {
          if (t === tabName) {
            btn.style.background = 'rgba(236,72,153,0.25)';
            btn.style.color = '#F472B6';
            btn.style.fontWeight = '600';
          } else {
            btn.style.background = 'transparent';
            btn.style.color = '#9CA3AF';
            btn.style.fontWeight = '400';
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

    function updateFontSizePreview(val) {
      const label = document.getElementById('font-size-label');
      if (label) label.textContent = val + 'px';
      document.querySelectorAll('.wf-sample').forEach(el => {
        el.style.fontSize = val + 'px';
      });
    }

    function updateSampleText(text) {
      const val = text || 'The quick brown fox jumps over the lazy dog 1234567890';
      document.querySelectorAll('.wf-sample').forEach(el => {
        el.textContent = val;
      });
    }

    function filterFontCategory(cat, el) {
      document.querySelectorAll('.font-cat-item').forEach(i => {
        i.classList.remove('active');
        i.style.background = 'transparent';
        i.style.color = '#D1D5DB';
      });
      if (el) {
        el.classList.add('active');
        el.style.background = 'rgba(236,72,153,0.2)';
        el.style.color = '#F472B6';
      }
      document.querySelectorAll('.font-list-card').forEach(card => {
        if (cat === 'all' || card.getAttribute('data-category') === cat) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function searchFontCatalog(q) {
      const query = (q || '').toLowerCase();
      document.querySelectorAll('.font-list-card').forEach(card => {
        const name = (card.getAttribute('data-name') || '').toLowerCase();
        card.style.display = name.includes(query) ? 'block' : 'none';
      });
    }

    function initGlyphGrid() {
      const container = document.getElementById('glyph-grid-container');
      if (!container || container.children.length > 0) return;
      const glyphs = [
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        '0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*','(',')','-','+','=','/','?','<','>',
        '∑','√','∫','≈','≠','≤','≥','→','←','↑','↓','⇒','⌘','⌥','⇧','⌃','⏎','⌫','✓','✗','★','●','◆','❖'
      ];
      container.innerHTML = glyphs.map(g => {
        const hex = 'U+' + g.charCodeAt(0).toString(16).toUpperCase().padStart(4, '0');
        return `
          <div onclick="selectGlyph('${g}', '${hex}')" style="height: 44px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; font-size: 18px; cursor: pointer; transition: all 0.15s ease;">
            ${g}
          </div>
        `;
      }).join('');
    }

    function selectGlyph(ch, hex) {
      const info = document.getElementById('glyph-selected-info');
      if (info) {
        info.innerHTML = `Karakter: <b>${ch}</b> &bull; Kode Hex: <b>${hex}</b> &bull; Kategori: General Unicode`;
      }
    }

    function installFontPrompt() {
      const font = prompt('Masukkan nama font atau path berkas (.ttf / .otf / .woff2):', 'GeistMono-Regular.otf');
      if (font) {
        showDockToast(`Font '${font}' berhasil dipasang ke /usr/share/fonts/`);
      }
    }

    function saveFontTuning() {
      const aa = document.getElementById('font-aa-select')?.value || 'Subpixel LCD (RGB)';
      const hint = document.getElementById('font-hint-select')?.value || 'Slight';
      showDockToast(`Konfigurasi tipografi disimpan: ${aa}, Hinting: ${hint}`);
    }

    // Initialize systems on load
    window.addEventListener('load', () => {
      try {
        renderDaxosDock();
        renderTrash();
        initWindowResizeHandles();
        setTimeout(initGlyphGrid, 600);
      } catch (e) {
        console.warn('[DAXOS Init] Window load setup:', e);
      }
    });

  </script>
</body>
</html>
"""

    html = html + clean_tail_controllers

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("[SUCCESS] Fully updated UI, DreXUI, and controllers in index.html!")

if __name__ == "__main__":
    main()
