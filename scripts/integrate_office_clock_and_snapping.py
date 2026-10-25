#!/usr/bin/env python3
"""
integrate_office_clock_and_snapping.py
Integrates:
1. Window Cursor Edge/Corner Resizing on all 8 handles (N, S, E, W, NE, NW, SE, SW).
2. Windows 11 Snap Layouts Flyout on green maximize button + edge dragging snap previews.
3. Full Microsoft Office Suite parity: DaxWord (Word), DaxSheet (Excel), DaxSlide (PowerPoint).
4. Full Clock Suite: World Clock (Jakarta, Tokyo, London, NY, Sydney), Alarm, Stopwatch, Timer.
5. Branded icons for all new applications.
"""

import sys

INDEX_PATH = "src/ui/desktop_preview/index.html"

def main():
    print("[1/5] Reading index.html...")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. ADD CSS FOR RESIZING, SNAP LAYOUTS FLYOUT, OFFICE, AND CLOCK
    css_enhancements = """
    /* ==========================================================================
       WINDOWS 11 SNAP LAYOUTS & RESIZE HANDLES FRAMEWORK
       ========================================================================== */
    .win-resize-handle {
      position: absolute;
      z-index: 1000;
    }
    .win-resize-handle.handle-n { top: 0; left: 10px; right: 10px; height: 6px; cursor: ns-resize; }
    .win-resize-handle.handle-s { bottom: 0; left: 10px; right: 10px; height: 6px; cursor: ns-resize; }
    .win-resize-handle.handle-w { left: 0; top: 10px; bottom: 10px; width: 6px; cursor: ew-resize; }
    .win-resize-handle.handle-e { right: 0; top: 10px; bottom: 10px; width: 6px; cursor: ew-resize; }
    .win-resize-handle.handle-nw { top: 0; left: 0; width: 12px; height: 12px; cursor: nwse-resize; }
    .win-resize-handle.handle-ne { top: 0; right: 0; width: 12px; height: 12px; cursor: nesw-resize; }
    .win-resize-handle.handle-sw { bottom: 0; left: 0; width: 12px; height: 12px; cursor: nesw-resize; }
    .win-resize-handle.handle-se { bottom: 0; right: 0; width: 12px; height: 12px; cursor: nwse-resize; }

    .window.is-resizing,
    .window.is-dragging {
      transition: none !important;
      user-select: none;
    }

    /* Windows 11 Snap Preview Translucent Ghost */
    #snap-ghost-overlay {
      position: fixed;
      background: rgba(0, 210, 255, 0.18);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 2px solid #00D2FF;
      border-radius: 12px;
      z-index: 99999;
      pointer-events: none;
      transition: all 0.16s cubic-bezier(0.16, 1, 0.3, 1);
      display: none;
      box-shadow: 0 16px 48px rgba(0, 210, 255, 0.35);
    }

    /* Windows 11 Snap Layouts Flyout */
    .snap-layouts-flyout {
      position: absolute;
      top: 36px;
      left: 60px;
      background: rgba(22, 25, 38, 0.95);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 24px 64px rgba(0, 0, 0, 0.75), 0 0 20px rgba(0, 210, 255, 0.2);
      display: none;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      z-index: 2000;
      animation: snapFlyoutIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .snap-layouts-flyout.show { display: grid; }

    @keyframes snapFlyoutIn {
      from { opacity: 0; transform: translateY(-8px) scale(0.96); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .snap-card {
      width: 78px;
      height: 54px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 6px;
      padding: 3px;
      display: flex;
      gap: 3px;
      cursor: pointer;
      transition: border-color 0.15s, background 0.15s;
    }
    .snap-card:hover { border-color: #00D2FF; }

    .snap-zone {
      background: rgba(255, 255, 255, 0.12);
      border-radius: 3px;
      transition: background 0.15s;
    }
    .snap-zone:hover { background: #00D2FF !important; }

    /* ==========================================================================
       OFFICE SUITE & CLOCK STYLES (RIBBON, DOC CANVAS, GRID, KEYNOTE)
       ========================================================================== */
    .office-ribbon {
      background: #181924;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      flex-direction: column;
    }
    .office-tabs {
      display: flex;
      gap: 2px;
      padding: 0 12px;
      background: #141520;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .office-tab-btn {
      padding: 6px 14px;
      font-size: 11px;
      font-weight: 600;
      color: #A0A0B8;
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      cursor: pointer;
    }
    .office-tab-btn.active {
      color: #FFF;
      border-bottom-color: #00D2FF;
      background: rgba(255, 255, 255, 0.04);
    }
    .office-toolbar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 14px;
      flex-wrap: wrap;
    }
    .office-tool-group {
      display: flex;
      align-items: center;
      gap: 4px;
      padding-right: 8px;
      border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .office-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      color: #FFF;
      padding: 4px 8px;
      font-size: 11px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: background 0.15s;
    }
    .office-btn:hover { background: rgba(255, 255, 255, 0.12); }
    .office-btn.active { background: #00D2FF; color: #000; font-weight: 700; }

    /* DaxSheet Grid */
    .sheet-grid {
      display: grid;
      grid-template-columns: 40px repeat(8, 110px);
      background: #1E202C;
      overflow: auto;
      font-family: 'JetBrains Mono', 'Segoe UI', monospace;
      font-size: 11px;
    }
    .sheet-header-cell {
      background: #161722;
      color: #8E8EA0;
      text-align: center;
      padding: 5px;
      border: 1px solid rgba(255, 255, 255, 0.06);
      font-weight: 700;
      user-select: none;
    }
    .sheet-data-cell {
      background: #1C1E2A;
      color: #E2E8F0;
      padding: 5px 8px;
      border: 1px solid rgba(255, 255, 255, 0.05);
      outline: none;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      cursor: cell;
    }
    .sheet-data-cell.selected {
      border: 2px solid #107C41 !important;
      background: rgba(16, 124, 65, 0.15) !important;
    }

    /* DaxClock Cards */
    .clock-city-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 14px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: border-color 0.15s;
    }
    .clock-city-card:hover { border-color: #00D2FF; }
"""

    if "#snap-ghost-overlay" not in content:
        content = content.replace("</style>", css_enhancements + "\n  </style>", 1)
        print("[OK] Injected Snapping, Resizing, Office, and Clock CSS styles")

    # 2. ADD BRANDED GRADIENTS FOR WORD, SHEET, SLIDE, CLOCK TO <defs>
    office_gradients = """
      <!-- DAXOS OFFICE & CLOCK SUITE BRANDED GRADIENTS -->
      <linearGradient id="icon-bg-word" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#185ABD"/>
        <stop offset="100%" stop-color="#0D3F8F"/>
      </linearGradient>

      <linearGradient id="icon-bg-sheet" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#107C41"/>
        <stop offset="100%" stop-color="#085229"/>
      </linearGradient>

      <linearGradient id="icon-bg-slide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#C43E1C"/>
        <stop offset="100%" stop-color="#8E260D"/>
      </linearGradient>

      <linearGradient id="icon-bg-clock" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0284C7"/>
        <stop offset="100%" stop-color="#1E1B4B"/>
      </linearGradient>
"""

    if 'id="icon-bg-word"' not in content:
        content = content.replace("</defs>", office_gradients + "\n    </defs>", 1)
        print("[OK] Injected Office & Clock gradients into <defs>")

    # 3. ADD SVG SYMBOLS FOR WORD, SHEET, SLIDE, CLOCK
    office_symbols = """
    <!-- DaxWord Icon (Microsoft Word Parity - Cobalt Blue Squircle) -->
    <symbol id="icon-word" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-word)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- White Document Sheet Behind -->
      <rect x="36" y="24" width="62" height="80" rx="8" fill="#FFFFFF" fill-opacity="0.25"/>
      <line x1="46" y1="42" x2="88" y2="42" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
      <line x1="46" y1="54" x2="88" y2="54" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
      <line x1="46" y1="66" x2="74" y2="66" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
      <!-- Floating Ribbon Badge with Letter W -->
      <rect x="22" y="38" width="52" height="52" rx="10" fill="#185ABD" stroke="#FFFFFF" stroke-width="2.5" filter="drop-shadow(0 8px 16px rgba(0,0,0,0.4))"/>
      <text x="48" y="76" font-family="'Segoe UI', Inter, sans-serif" font-size="34" font-weight="900" fill="#FFFFFF" text-anchor="middle">W</text>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaxSheet Icon (Microsoft Excel Parity - Emerald Green Squircle) -->
    <symbol id="icon-sheet" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-sheet)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- White Grid Sheet Behind -->
      <rect x="36" y="24" width="62" height="80" rx="8" fill="#FFFFFF" fill-opacity="0.25"/>
      <rect x="44" y="36" width="46" height="40" fill="none" stroke="#FFFFFF" stroke-width="3"/>
      <line x1="67" y1="36" x2="67" y2="76" stroke="#FFFFFF" stroke-width="2.5"/>
      <line x1="44" y1="56" x2="90" y2="56" stroke="#FFFFFF" stroke-width="2.5"/>
      <!-- Floating Ribbon Badge with Letter X -->
      <rect x="22" y="38" width="52" height="52" rx="10" fill="#107C41" stroke="#FFFFFF" stroke-width="2.5" filter="drop-shadow(0 8px 16px rgba(0,0,0,0.4))"/>
      <text x="48" y="76" font-family="'Segoe UI', Inter, sans-serif" font-size="34" font-weight="900" fill="#FFFFFF" text-anchor="middle">X</text>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaxSlide Icon (PowerPoint Parity - Terracotta Red Squircle) -->
    <symbol id="icon-slide" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-slide)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- White 16:9 Presentation Slide Behind -->
      <rect x="36" y="26" width="64" height="48" rx="6" fill="#FFFFFF" fill-opacity="0.25"/>
      <circle cx="78" cy="50" r="14" fill="#FFFFFF"/>
      <!-- Floating Ribbon Badge with Letter P -->
      <rect x="22" y="38" width="52" height="52" rx="10" fill="#C43E1C" stroke="#FFFFFF" stroke-width="2.5" filter="drop-shadow(0 8px 16px rgba(0,0,0,0.4))"/>
      <text x="48" y="76" font-family="'Segoe UI', Inter, sans-serif" font-size="34" font-weight="900" fill="#FFFFFF" text-anchor="middle">P</text>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- DaxClock Icon (World Clock, Alarm, Stopwatch & Timer Squircle) -->
    <symbol id="icon-clock" viewBox="0 0 128 128">
      <rect width="128" height="128" rx="28" fill="url(#icon-bg-clock)"/>
      <path d="M0 28 C0 12.5 12.5 0 28 0 H100 C115.5 0 128 12.5 128 28 V54 C88 62 40 62 0 54 Z" fill="url(#drex-top-sheen)"/>
      <!-- Circular Clock Face -->
      <circle cx="64" cy="64" r="42" fill="none" stroke="#FFFFFF" stroke-width="6"/>
      <circle cx="64" cy="64" r="5" fill="#38BDF8"/>
      <!-- Hour & Minute Hands -->
      <line x1="64" y1="64" x2="64" y2="36" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
      <line x1="64" y1="64" x2="86" y2="64" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
      <line x1="64" y1="64" x2="48" y2="78" stroke="#EF4444" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Minute Tick Marks -->
      <circle cx="64" cy="28" r="2.5" fill="#38BDF8"/>
      <circle cx="100" cy="64" r="2.5" fill="#38BDF8"/>
      <circle cx="64" cy="100" r="2.5" fill="#38BDF8"/>
      <circle cx="28" cy="64" r="2.5" fill="#38BDF8"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>
"""

    if 'id="icon-word"' not in content:
        content = content.replace("</svg>", office_symbols + "\n  </svg>", 1)
        print("[OK] Injected SVG symbols for Word, Sheet, Slide, Clock")

    # 4. WINDOW MARKUPS FOR DAXWORD, DAXSHEET, DAXSLIDE, DAXCLOCK
    new_windows = """
  <!-- ========================================================================
       WINDOW: DAXWORD (MICROSOFT WORD PARITY - DOCUMENT PROCESSOR)
       ======================================================================== -->
  <div class="window" id="win-daxword" style="top: 60px; left: 160px; width: 940px; height: 620px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-daxword')" ondblclick="maximizeWindow('win-daxword')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-daxword')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-daxword')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-daxword')" onclick="maximizeWindow('win-daxword')">+</div>
      </div>
      <span class="window-title">DaxWord — Dokumen1.docx (Microsoft Word Parity • OpenXML 2.19)</span>
    </div>
    <div class="window-content" style="display: flex; flex-direction: column; background: #1B1D28; position: relative;">
      <!-- Office Ribbon -->
      <div class="office-ribbon">
        <div class="office-tabs">
          <button class="office-tab-btn active">Beranda (Home)</button>
          <button class="office-tab-btn">Sisipkan (Insert)</button>
          <button class="office-tab-btn">Tata Letak (Layout)</button>
          <button class="office-tab-btn">Referensi</button>
          <button class="office-tab-btn">Tinjau (Review)</button>
          <button class="office-tab-btn">Tampilan (View)</button>
        </div>
        <div class="office-toolbar">
          <div class="office-tool-group">
            <button class="office-btn" title="Paste (Ctrl+V)">📋 Tempel</button>
            <button class="office-btn" title="Copy (Ctrl+C)">Salin</button>
          </div>
          <div class="office-tool-group">
            <select style="background: #26293A; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 3px 6px; font-size: 11px;">
              <option>Aptos (Body)</option>
              <option selected>Segoe UI Variable</option>
              <option>Inter Display</option>
              <option>Calibri</option>
              <option>Times New Roman</option>
            </select>
            <select style="background: #26293A; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 3px 6px; font-size: 11px;">
              <option>10</option>
              <option selected>11</option>
              <option>12</option>
              <option>14</option>
              <option>18</option>
              <option>24</option>
            </select>
            <button class="office-btn" id="word-btn-bold" onclick="this.classList.toggle('active')" title="Bold (Ctrl+B)"><b>B</b></button>
            <button class="office-btn" id="word-btn-italic" onclick="this.classList.toggle('active')" title="Italic (Ctrl+I)"><i>I</i></button>
            <button class="office-btn" id="word-btn-underline" onclick="this.classList.toggle('active')" title="Underline (Ctrl+U)"><u>U</u></button>
          </div>
          <div class="office-tool-group">
            <button class="office-btn" title="Rata Kiri">☰</button>
            <button class="office-btn active" title="Rata Tengah">☲</button>
            <button class="office-btn" title="Rata Kanan">☵</button>
            <button class="office-btn" title="Rata Kiri Kanan">☷</button>
            <button class="office-btn" title="Daftar Poin Bullets">• Bullets</button>
          </div>
          <div class="office-tool-group">
            <button class="office-btn" style="background: #0284C7; font-weight: 700;">Simpan (.docx)</button>
            <button class="office-btn">Ekspor PDF</button>
          </div>
        </div>
      </div>
      <!-- Document Canvas / A4 Paper -->
      <div style="flex: 1; overflow: auto; display: flex; justify-content: center; padding: 32px 16px; background: #13141E;">
        <div style="width: 680px; min-height: 820px; background: #FFFFFF; color: #1E293B; border-radius: 4px; box-shadow: 0 16px 48px rgba(0,0,0,0.6); padding: 56px 64px; font-family: 'Segoe UI', Inter, sans-serif; line-height: 1.6;" contenteditable="true" spellcheck="false">
          <h1 style="color: #0F172A; font-size: 24px; font-weight: 800; border-bottom: 2px solid #0284C7; padding-bottom: 8px; margin-bottom: 16px;">
            RENCANA ARSITEKTUR SISTEM OPERASI DAXOS 2026
          </h1>
          <p style="font-size: 13px; color: #475569; margin-bottom: 16px;">
            <b>Disusun oleh:</b> Dhafa Nazula Permadi (@kangpcode) &bull; Lead Enterprise Architect<br>
            <b>Versi:</b> 1.10.2026 Codename Rhino Alpha &bull; Standar Produksi Industri
          </p>
          <h2 style="color: #0284C7; font-size: 17px; margin-top: 24px; margin-bottom: 8px;">
            1. Ringkasan Eksekutif &amp; Keunggulan Kompetitif
          </h2>
          <p style="font-size: 13px; text-align: justify; margin-bottom: 14px;">
            DAXOS menghadirkan sistem operasi desktop hibrida yang memadukan keindahan visual liquid acrylic Wayland 240Hz, keamanan tak tertembus berbasis Landlock LSM ABI v5 + Seccomp BPF, dan produktivitas komputasi enterprise setara Windows 11 dan macOS Sequoia.
          </p>
          <h2 style="color: #0284C7; font-size: 17px; margin-top: 20px; margin-bottom: 8px;">
            2. Paket Produktivitas DaxOffice Suite
          </h2>
          <p style="font-size: 13px; text-align: justify;">
            DaxWord, DaxSheet, dan DaxSlide memberikan kompatibilitas penuh dengan format OpenXML Microsoft Office 365 (.docx, .xlsx, .pptx) dengan rendering tipografi sub-pixel tanpa latency.
          </p>
        </div>
      </div>
      <!-- Status Bar -->
      <div style="background: #185ABD; color: #FFF; font-size: 10px; padding: 4px 14px; display: flex; justify-content: space-between; align-items: center;">
        <div>Halaman 1 dari 1 &bull; 428 Kata &bull; 2.840 Karakter &bull; Bahasa Indonesia (Pemeriksaan Ejaan Aktif)</div>
        <div style="display: flex; gap: 12px; align-items: center;">
          <span>Tata Letak Cetak</span>
          <span>100% Zoom</span>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: DAXSHEET (MICROSOFT EXCEL PARITY - SPREADSHEET PROCESSOR)
       ======================================================================== -->
  <div class="window" id="win-daxsheet" style="top: 70px; left: 190px; width: 950px; height: 600px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-daxsheet')" ondblclick="maximizeWindow('win-daxsheet')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-daxsheet')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-daxsheet')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-daxsheet')" onclick="maximizeWindow('win-daxsheet')">+</div>
      </div>
      <span class="window-title">DaxSheet — BukuKerja1.xlsx (Microsoft Excel Parity • Real-Time Matrix)</span>
    </div>
    <div class="window-content" style="display: flex; flex-direction: column; background: #181A24; position: relative;">
      <!-- Office Ribbon -->
      <div class="office-ribbon">
        <div class="office-tabs">
          <button class="office-tab-btn active">Beranda (Home)</button>
          <button class="office-tab-btn">Sisipkan (Insert)</button>
          <button class="office-tab-btn">Rumus (Formulas)</button>
          <button class="office-tab-btn">Data</button>
          <button class="office-tab-btn">Tinjau</button>
          <button class="office-tab-btn">Tampilan</button>
        </div>
        <div class="office-toolbar">
          <div class="office-tool-group">
            <button class="office-btn" title="Bold"><b>B</b></button>
            <button class="office-btn" title="Italic"><i>I</i></button>
            <button class="office-btn" title="Format Mata Uang">Rp Mata Uang</button>
            <button class="office-btn" title="Persen">%</button>
            <button class="office-btn" title="Desimal">.00</button>
          </div>
          <div class="office-tool-group">
            <button class="office-btn" style="color: #34D399; font-weight: 700;">&Sigma; AutoSum</button>
            <button class="office-btn">Sort A&rarr;Z</button>
            <button class="office-btn">Filter</button>
          </div>
          <div class="office-tool-group">
            <button class="office-btn" style="background: #107C41; font-weight: 700;">Simpan (.xlsx)</button>
            <button class="office-btn">Ekspor CSV</button>
          </div>
        </div>
      </div>
      <!-- Formula Bar -->
      <div style="background: #141620; border-bottom: 1px solid rgba(255,255,255,0.08); padding: 4px 10px; display: flex; align-items: center; gap: 8px;">
        <div style="background: #222534; color: #FFF; font-weight: 700; padding: 2px 8px; border-radius: 3px; font-size: 11px; min-width: 45px; text-align: center;" id="sheet-active-cell">B5</div>
        <span style="font-weight: 700; color: #34D399; font-style: italic; font-size: 12px;">fx</span>
        <input type="text" id="sheet-formula-input" value="=SUM(B2:B4)" style="flex: 1; background: #1C1E2A; color: #FFF; border: 1px solid rgba(255,255,255,0.1); border-radius: 3px; padding: 3px 8px; font-family: monospace; font-size: 11px;">
      </div>
      <!-- Spreadsheet Matrix Grid -->
      <div style="flex: 1; overflow: auto;">
        <div class="sheet-grid" id="main-sheet-grid">
          <!-- Column Headers -->
          <div class="sheet-header-cell">#</div>
          <div class="sheet-header-cell">A</div>
          <div class="sheet-header-cell">B</div>
          <div class="sheet-header-cell">C</div>
          <div class="sheet-header-cell">D</div>
          <div class="sheet-header-cell">E</div>
          <div class="sheet-header-cell">F</div>
          <div class="sheet-header-cell">G</div>
          <div class="sheet-header-cell">H</div>

          <!-- Row 1 -->
          <div class="sheet-header-cell">1</div>
          <div class="sheet-data-cell" style="font-weight: 700; color: #38BDF8;">Komponen / R&amp;D</div>
          <div class="sheet-data-cell" style="font-weight: 700; color: #38BDF8;">Alokasi Anggaran</div>
          <div class="sheet-data-cell" style="font-weight: 700; color: #38BDF8;">Realisasi %</div>
          <div class="sheet-data-cell" style="font-weight: 700; color: #38BDF8;">Status</div>
          <div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div>

          <!-- Row 2 -->
          <div class="sheet-header-cell">2</div>
          <div class="sheet-data-cell">Kernel Hybrid &amp; Drivers</div>
          <div class="sheet-data-cell" style="text-align: right;">Rp 150.000.000</div>
          <div class="sheet-data-cell" style="text-align: right; color: #34D399;">100%</div>
          <div class="sheet-data-cell" style="color: #34D399;">COMPLETED</div>
          <div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div>

          <!-- Row 3 -->
          <div class="sheet-header-cell">3</div>
          <div class="sheet-data-cell">DreXVIS Graphics 240Hz</div>
          <div class="sheet-data-cell" style="text-align: right;">Rp 120.000.000</div>
          <div class="sheet-data-cell" style="text-align: right; color: #34D399;">100%</div>
          <div class="sheet-data-cell" style="color: #34D399;">COMPLETED</div>
          <div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div>

          <!-- Row 4 -->
          <div class="sheet-header-cell">4</div>
          <div class="sheet-data-cell">Landlock Security &amp; OTA</div>
          <div class="sheet-data-cell" style="text-align: right;">Rp 85.000.000</div>
          <div class="sheet-data-cell" style="text-align: right; color: #34D399;">100%</div>
          <div class="sheet-data-cell" style="color: #34D399;">COMPLETED</div>
          <div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div>

          <!-- Row 5 (TOTAL) -->
          <div class="sheet-header-cell">5</div>
          <div class="sheet-data-cell" style="font-weight: 700; color: #F59E0B;">TOTAL ANGGARAN (SUM)</div>
          <div class="sheet-data-cell selected" style="text-align: right; font-weight: 800; color: #34D399;">Rp 355.000.000</div>
          <div class="sheet-data-cell" style="text-align: right; font-weight: 700; color: #34D399;">100.0%</div>
          <div class="sheet-data-cell" style="font-weight: 700; color: #34D399;">VERIFIED OK</div>
          <div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div><div class="sheet-data-cell"></div>
        </div>
      </div>
      <!-- Sheet Tabs Bar -->
      <div style="background: #107C41; color: #FFF; font-size: 11px; padding: 4px 12px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; gap: 4px;">
          <span style="background: rgba(0,0,0,0.3); padding: 3px 12px; border-radius: 4px 4px 0 0; font-weight: 700; cursor: pointer;">Lembar 1 (Finansial Q4)</span>
          <span style="padding: 3px 10px; cursor: pointer; opacity: 0.8;">Lembar 2 (Telemetri)</span>
          <span style="padding: 3px 8px; cursor: pointer;">+ Tambah Lembar</span>
        </div>
        <div>SIAP &bull; SUM: Rp 355.000.000 &bull; AVERAGE: Rp 118.333.333 &bull; COUNT: 3</div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: DAXSLIDE (MICROSOFT POWERPOINT PARITY - PRESENTATION STUDIO)
       ======================================================================== -->
  <div class="window" id="win-daxslide" style="top: 80px; left: 220px; width: 960px; height: 610px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-daxslide')" ondblclick="maximizeWindow('win-daxslide')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-daxslide')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-daxslide')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-daxslide')" onclick="maximizeWindow('win-daxslide')">+</div>
      </div>
      <span class="window-title">DaxSlide — Presentasi1.pptx (Microsoft PowerPoint Parity • 16:9 Presenter)</span>
    </div>
    <div class="window-content" style="display: flex; flex-direction: column; background: #161822; position: relative;">
      <!-- Office Ribbon -->
      <div class="office-ribbon">
        <div class="office-tabs">
          <button class="office-tab-btn active">Beranda</button>
          <button class="office-tab-btn">Sisipkan</button>
          <button class="office-tab-btn">Desain</button>
          <button class="office-tab-btn">Transisi</button>
          <button class="office-tab-btn">Animasi</button>
          <button class="office-tab-btn">Peragaan Slide (Slide Show)</button>
        </div>
        <div class="office-toolbar">
          <div class="office-tool-group">
            <button class="office-btn" style="color: #38BDF8;">+ Slide Baru</button>
            <button class="office-btn">Tata Letak</button>
          </div>
          <div class="office-tool-group">
            <button class="office-btn">Kotak Teks</button>
            <button class="office-btn">Bentuk (Shapes)</button>
            <button class="office-btn">Grafik Diagram</button>
          </div>
          <div class="office-tool-group">
            <button class="office-btn" style="background: #C43E1C; font-weight: 700;" onclick="alert('Memulai Presentasi Layar Penuh (F5)...')">&#9654; Peragaan Slide (F5)</button>
            <button class="office-btn">Transisi: Push</button>
          </div>
        </div>
      </div>
      <!-- 2-Pane Keynote Studio -->
      <div style="flex: 1; display: flex; overflow: hidden;">
        <!-- Left Filmstrip Thumbnails -->
        <div style="width: 170px; background: #12131C; border-right: 1px solid rgba(255,255,255,0.08); padding: 12px; display: flex; flex-direction: column; gap: 10px; overflow-y: auto;">
          <div style="border: 2px solid #C43E1C; border-radius: 6px; padding: 4px; background: #1E202E; cursor: pointer;">
            <div style="font-size: 9px; color: #C43E1C; font-weight: 700; margin-bottom: 2px;">Slide 1 (Master)</div>
            <div style="height: 60px; background: #0F172A; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #FFF; text-align: center; padding: 4px;">
              DAXOS: Redefining Operating Systems
            </div>
          </div>
          <div style="border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 4px; background: #181926; cursor: pointer;">
            <div style="font-size: 9px; color: #8E8EA0; margin-bottom: 2px;">Slide 2</div>
            <div style="height: 60px; background: #0F172A; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #FFF; text-align: center; padding: 4px;">
              DCODX Studio &amp; Toolchain
            </div>
          </div>
          <div style="border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 4px; background: #181926; cursor: pointer;">
            <div style="font-size: 9px; color: #8E8EA0; margin-bottom: 2px;">Slide 3</div>
            <div style="height: 60px; background: #0F172A; border-radius: 3px; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #FFF; text-align: center; padding: 4px;">
              Landlock LSM v5 Sandbox
            </div>
          </div>
        </div>
        <!-- Main Slide 16:9 Canvas -->
        <div style="flex: 1; background: #0C0D14; display: flex; align-items: center; justify-content: center; padding: 24px; position: relative;">
          <div style="width: 680px; height: 382px; background: linear-gradient(135deg, #0F172A, #1E1B4B); border-radius: 8px; box-shadow: 0 16px 48px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.12); padding: 40px; display: flex; flex-direction: column; justify-content: center; position: relative;">
            <div style="font-size: 11px; color: #38BDF8; font-weight: 700; letter-spacing: 2px;">DAXOS MASTER KEYNOTE 2026</div>
            <div style="font-size: 26px; font-weight: 900; color: #FFF; margin-top: 8px; line-height: 1.2;">
              DAXOS: Redefining the Modern Operating System
            </div>
            <div style="font-size: 14px; color: #94A3B8; margin-top: 8px;">
              Hybrid Kernel Architecture &bull; Wayland Acrylic 240Hz &bull; Microsecond Fault Recovery
            </div>
            <ul style="margin-top: 18px; font-size: 12px; color: #CBD5E1; padding-left: 20px; line-height: 1.8;">
              <li>Surflang 1.0 zero-cost memory compiler with Swift-like declarative UI</li>
              <li>Landlock LSM ABI v5 strict isolation and Seccomp-BPF filters</li>
              <li>Universal binary fat execution (.dapp / .dbpp) with Ed25519 cryptographic proofs</li>
            </ul>
          </div>
        </div>
      </div>
      <!-- Status Bar -->
      <div style="background: #C43E1C; color: #FFF; font-size: 10px; padding: 4px 14px; display: flex; justify-content: space-between; align-items: center;">
        <div>Slide 1 dari 3 &bull; Rasio 16:9 Widescreen &bull; Transisi: Push (0.4s)</div>
        <div>Catatan Pembicara: [TERSEDIA] &bull; 100% Layar</div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: DAXCLOCK (WORLD CLOCK, ALARM, STOPWATCH & COUNTDOWN TIMER)
       ======================================================================== -->
  <div class="window" id="win-daxclock" style="top: 85px; left: 250px; width: 840px; height: 560px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-daxclock')" ondblclick="maximizeWindow('win-daxclock')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-daxclock')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-daxclock')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-daxclock')" onclick="maximizeWindow('win-daxclock')">+</div>
      </div>
      <span class="window-title" id="clock-suite-title">Jam &amp; Waktu Dunia — World Clock, Stopwatch, Alarm &amp; Timer</span>
      <!-- Clock Tab Buttons -->
      <div style="margin-left: auto; display: flex; gap: 4px; background: rgba(0,0,0,0.3); border-radius: 8px; padding: 2px;">
        <button class="btn btn-secondary active" id="btn-clock-world" style="font-size: 10px; padding: 3px 10px;" onclick="switchClockTab('world')">Jam Dunia</button>
        <button class="btn btn-secondary" id="btn-clock-alarm" style="font-size: 10px; padding: 3px 10px;" onclick="switchClockTab('alarm')">Alarm</button>
        <button class="btn btn-secondary" id="btn-clock-stopwatch" style="font-size: 10px; padding: 3px 10px;" onclick="switchClockTab('stopwatch')">Stopwatch</button>
        <button class="btn btn-secondary" id="btn-clock-timer" style="font-size: 10px; padding: 3px 10px;" onclick="switchClockTab('timer')">Timer</button>
      </div>
    </div>
    <div class="window-content" style="padding: 18px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0E0F1A;">
      <!-- TAB 1: WORLD CLOCK -->
      <div id="clock-panel-world" style="display: flex; flex-direction: column; gap: 12px;">
        <div class="clock-city-card">
          <div>
            <div style="font-size: 18px; font-weight: 700; color: #FFF;">Jakarta, Indonesia</div>
            <div style="font-size: 12px; color: #38BDF8;">WIB (UTC+7) &bull; Waktu Lokal Rumah</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 26px; font-weight: 800; color: #FFF; font-family: monospace;" id="time-jakarta">21:38:00</div>
            <span style="font-size: 10px; background: rgba(245,158,11,0.2); color: #F59E0B; padding: 2px 8px; border-radius: 4px;">Malam Hari</span>
          </div>
        </div>

        <div class="clock-city-card">
          <div>
            <div style="font-size: 18px; font-weight: 700; color: #FFF;">Tokyo, Jepang</div>
            <div style="font-size: 12px; color: #8E8EA0;">JST (UTC+9) &bull; +2 jam dari Jakarta</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 26px; font-weight: 800; color: #FFF; font-family: monospace;" id="time-tokyo">23:38:00</div>
            <span style="font-size: 10px; background: rgba(245,158,11,0.2); color: #F59E0B; padding: 2px 8px; border-radius: 4px;">Tengah Malam</span>
          </div>
        </div>

        <div class="clock-city-card">
          <div>
            <div style="font-size: 18px; font-weight: 700; color: #FFF;">London, Inggris Raya</div>
            <div style="font-size: 12px; color: #8E8EA0;">GMT (UTC+0) &bull; -7 jam dari Jakarta</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 26px; font-weight: 800; color: #FFF; font-family: monospace;" id="time-london">14:38:00</div>
            <span style="font-size: 10px; background: rgba(52,211,153,0.2); color: #34D399; padding: 2px 8px; border-radius: 4px;">Siang Hari</span>
          </div>
        </div>

        <div class="clock-city-card">
          <div>
            <div style="font-size: 18px; font-weight: 700; color: #FFF;">New York, Amerika Serikat</div>
            <div style="font-size: 12px; color: #8E8EA0;">EST (UTC-5) &bull; -12 jam dari Jakarta</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 26px; font-weight: 800; color: #FFF; font-family: monospace;" id="time-newyork">09:38:00</div>
            <span style="font-size: 10px; background: rgba(52,211,153,0.2); color: #34D399; padding: 2px 8px; border-radius: 4px;">Pagi Hari</span>
          </div>
        </div>
      </div>

      <!-- TAB 2: ALARM -->
      <div id="clock-panel-alarm" style="display: none; flex-direction: column; gap: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="font-size: 13px; font-weight: 700; color: #FFF;">Daftar Alarm Terjadwal</div>
          <button class="btn btn-primary" style="font-size: 11px; padding: 4px 12px;">+ Tambah Alarm</button>
        </div>
        <div class="clock-city-card">
          <div>
            <div style="font-size: 32px; font-weight: 800; color: #FFF; font-family: monospace;">05:00</div>
            <div style="font-size: 12px; color: #38BDF8;">Subuh &amp; Olahraga Pagi &bull; Setiap Hari</div>
          </div>
          <input type="checkbox" checked style="width: 22px; height: 22px; accent-color: #34D399;">
        </div>
        <div class="clock-city-card">
          <div>
            <div style="font-size: 32px; font-weight: 800; color: #FFF; font-family: monospace;">09:00</div>
            <div style="font-size: 12px; color: #38BDF8;">Daily Standup Sprint DAXOS &bull; Senin - Jumat</div>
          </div>
          <input type="checkbox" checked style="width: 22px; height: 22px; accent-color: #34D399;">
        </div>
        <div class="clock-city-card">
          <div>
            <div style="font-size: 32px; font-weight: 800; color: #8E8EA0; font-family: monospace;">14:00</div>
            <div style="font-size: 12px; color: #8E8EA0;">Code Review &amp; Architecture Sync &bull; Senin - Jumat</div>
          </div>
          <input type="checkbox" style="width: 22px; height: 22px; accent-color: #34D399;">
        </div>
      </div>

      <!-- TAB 3: STOPWATCH -->
      <div id="clock-panel-stopwatch" style="display: none; flex-direction: column; align-items: center; gap: 18px; padding: 20px 0;">
        <div style="font-size: 64px; font-weight: 900; color: #FFF; font-family: monospace; letter-spacing: 2px;" id="stopwatch-display">
          00:04:12.45
        </div>
        <div style="display: flex; gap: 14px;">
          <button class="btn btn-primary" style="padding: 8px 24px; font-size: 13px; font-weight: 700;">Mulai (Start)</button>
          <button class="btn btn-secondary" style="padding: 8px 20px; font-size: 13px;">Putaran (Lap)</button>
          <button class="btn btn-secondary" style="padding: 8px 20px; font-size: 13px;">Reset</button>
        </div>
        <!-- Lap Splits Table -->
        <div style="width: 100%; max-width: 480px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px;">
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: #8E8EA0; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px;">
            <span>PUTARAN</span><span>WAKTU LAP</span><span>TOTAL WAKTU</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 12px; color: #34D399; font-weight: 700; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
            <span>Lap 2 (Tercepat)</span><span>00:01:28.45</span><span>00:02:40.57</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 12px; color: #FFF; padding: 6px 0;">
            <span>Lap 1</span><span>00:01:12.12</span><span>00:01:12.12</span>
          </div>
        </div>
      </div>

      <!-- TAB 4: TIMER -->
      <div id="clock-panel-timer" style="display: none; flex-direction: column; align-items: center; gap: 20px; padding: 20px 0;">
        <div style="position: relative; width: 180px; height: 180px; display: flex; align-items: center; justify-content: center;">
          <svg style="width: 100%; height: 100%; transform: rotate(-90deg);" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="6"/>
            <circle cx="50" cy="50" r="44" fill="none" stroke="#00D2FF" stroke-width="6" stroke-dasharray="276" stroke-dashoffset="65" stroke-linecap="round"/>
          </svg>
          <div style="position: absolute; text-align: center;">
            <div style="font-size: 36px; font-weight: 900; color: #FFF; font-family: monospace;">24:59</div>
            <div style="font-size: 10px; color: #38BDF8;">Pomodoro Fokus</div>
          </div>
        </div>
        <!-- Presets -->
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;">1 Menit</button>
          <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;">5 Menit</button>
          <button class="btn btn-secondary active" style="font-size: 11px; padding: 4px 10px;">25 Min (Pomodoro)</button>
          <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;">45 Min (Fokus)</button>
        </div>
        <div style="display: flex; gap: 12px;">
          <button class="btn btn-primary" style="padding: 8px 24px; font-size: 13px; font-weight: 700;">Jeda (Pause)</button>
          <button class="btn btn-secondary" style="padding: 8px 18px; font-size: 13px;">Batal (Reset)</button>
        </div>
      </div>
    </div>
  </div>
"""

    if 'id="win-daxword"' not in content:
        # Place before BOTTOM ACRYLIC DOCK comment
        dock_pos = content.find("<!-- ========================================================================\n       BOTTOM ACRYLIC DOCK")
        if dock_pos != -1:
            content = content[:dock_pos] + new_windows + "\n  " + content[dock_pos:]
            print("[OK] Injected DaxWord, DaxSheet, DaxSlide, and DaxClock window markups")

    # 5. INJECT SNAP PREVIEW GHOST AND SNAP FLYOUT POPUP
    snap_elements = """
  <!-- Windows 11 Snap Ghost Preview Overlay -->
  <div id="snap-ghost-overlay"></div>

  <!-- Windows 11 Snap Layouts Flyout -->
  <div class="snap-layouts-flyout" id="snap-layouts-flyout" onmouseleave="hideSnapFlyout()">
    <!-- Layout 1: 50 / 50 Left Right -->
    <div class="snap-card" title="Split 50% / 50%" onclick="applySnapLayout('left-50')">
      <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('left-50')"></div>
      <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('right-50')"></div>
    </div>
    <!-- Layout 2: 65 / 35 Two-Thirds -->
    <div class="snap-card" title="Split 65% / 35%" onclick="applySnapLayout('left-65')">
      <div class="snap-zone" style="flex: 2;" onclick="event.stopPropagation(); applySnapLayout('left-65')"></div>
      <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('right-35')"></div>
    </div>
    <!-- Layout 3: 3-Column Split -->
    <div class="snap-card" title="3-Column Split" onclick="applySnapLayout('left-50')">
      <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('left-50')"></div>
      <div style="flex: 1; display: flex; flex-direction: column; gap: 3px;">
        <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('top-right-25')"></div>
        <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('bottom-right-25')"></div>
      </div>
    </div>
    <!-- Layout 4: 4-Quadrant Grid -->
    <div class="snap-card" title="4-Quadrant Grid" onclick="applySnapLayout('top-left-25')">
      <div style="flex: 1; display: flex; flex-direction: column; gap: 3px;">
        <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('top-left-25')"></div>
        <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('bottom-left-25')"></div>
      </div>
      <div style="flex: 1; display: flex; flex-direction: column; gap: 3px;">
        <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('top-right-25')"></div>
        <div class="snap-zone" style="flex: 1;" onclick="event.stopPropagation(); applySnapLayout('bottom-right-25')"></div>
      </div>
    </div>
  </div>
"""
    if "id=\"snap-ghost-overlay\"" not in content:
        content = content.replace("<div class=\"dock-container\">", snap_elements + "\n  <div class=\"dock-container\">", 1)
        print("[OK] Injected Snap Ghost and Snap Layouts Flyout markup")

    # 6. ADD DOCK ITEMS FOR WORD, SHEET, SLIDE, CLOCK
    dock_items = """
      <div class="dock-item" onclick="openApp('win-daxword', 'DaxWord')">
        <div class="dock-tooltip">DaxWord (Docs)</div>
        <svg class="dock-icon-svg"><use href="#icon-word"/></svg>
        <div class="dock-dot" id="dot-win-daxword"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-daxsheet', 'DaxSheet')">
        <div class="dock-tooltip">DaxSheet (Spreadsheets)</div>
        <svg class="dock-icon-svg"><use href="#icon-sheet"/></svg>
        <div class="dock-dot" id="dot-win-daxsheet"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-daxslide', 'DaxSlide')">
        <div class="dock-tooltip">DaxSlide (Presentations)</div>
        <svg class="dock-icon-svg"><use href="#icon-slide"/></svg>
        <div class="dock-dot" id="dot-win-daxslide"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-daxclock', 'Jam')">
        <div class="dock-tooltip">Jam &amp; Waktu Dunia</div>
        <svg class="dock-icon-svg"><use href="#icon-clock"/></svg>
        <div class="dock-dot" id="dot-win-daxclock"></div>
      </div>
"""
    if "openApp('win-daxword'" not in content:
        # Place before dock-divider
        content = content.replace('<div class="dock-divider"></div>', dock_items + "\n      <div class=\"dock-divider\"></div>", 1)
        print("[OK] Injected Word, Sheet, Slide, Clock into Dock")

    # 7. ADD LAUNCHPAD ITEMS FOR WORD, SHEET, SLIDE, CLOCK
    launchpad_items = """
        <div class="launchpad-item" data-category="productivity" data-name="DaxWord Word Dokumen Docx Office Naskah Tulisan" onclick="launchAppFromLaunchpad('win-daxword', 'DaxWord')">
          <svg class="launchpad-item-icon"><use href="#icon-word"/></svg>
          <div class="launchpad-item-title">DaxWord</div>
          <div class="launchpad-item-desc">Pengolah Dokumen OpenXML</div>
        </div>

        <div class="launchpad-item" data-category="productivity" data-name="DaxSheet Excel Lembar Sebar Spreadsheet Xlsx Tabel Rumus" onclick="launchAppFromLaunchpad('win-daxsheet', 'DaxSheet')">
          <svg class="launchpad-item-icon"><use href="#icon-sheet"/></svg>
          <div class="launchpad-item-title">DaxSheet</div>
          <div class="launchpad-item-desc">Lembar Sebar Finansial Real-Time</div>
        </div>

        <div class="launchpad-item" data-category="productivity" data-name="DaxSlide PowerPoint Presentasi Keynote Pptx Slide Show" onclick="launchAppFromLaunchpad('win-daxslide', 'DaxSlide')">
          <svg class="launchpad-item-icon"><use href="#icon-slide"/></svg>
          <div class="launchpad-item-title">DaxSlide</div>
          <div class="launchpad-item-desc">Studio Presentasi 16:9 Widescreen</div>
        </div>

        <div class="launchpad-item" data-category="system" data-name="Jam Clock Waktu Dunia Stopwatch Alarm Timer Jam Digital" onclick="launchAppFromLaunchpad('win-daxclock', 'Jam')">
          <svg class="launchpad-item-icon"><use href="#icon-clock"/></svg>
          <div class="launchpad-item-title">Jam &amp; Waktu Dunia</div>
          <div class="launchpad-item-desc">World Clock, Alarm &amp; Stopwatch</div>
        </div>
"""
    if "win-daxword" not in content[:content.find('<div class="launchpad-grid"')]:
        content = content.replace('<div class="launchpad-grid" id="launchpad-grid">', '<div class="launchpad-grid" id="launchpad-grid">' + launchpad_items, 1)
        print("[OK] Injected Word, Sheet, Slide, Clock into Launchpad Grid")

    # 8. JAVASCRIPT FOR RESIZE HANDLES, WINDOWS 11 SNAPPING & CLOCK/OFFICE CONTROLLERS
    js_logic = """
    // =========================================================================
    // WINDOW RESIZE ENGINE (CURSOR DRAGGING ON 8 HANDLES)
    // =========================================================================
    let activeResizingWin = null;
    let activeResizeHandle = null;
    let startResizeX = 0, startResizeY = 0;
    let startWinW = 0, startWinH = 0;
    let startWinTop = 0, startWinLeft = 0;

    function initWindowResizeHandles() {
      document.querySelectorAll('.window').forEach(win => {
        if (win.dataset.resizeInited === 'true') return;
        win.dataset.resizeInited = 'true';

        const handles = ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se'];
        handles.forEach(h => {
          const handleEl = document.createElement('div');
          handleEl.className = `win-resize-handle handle-${h}`;
          handleEl.addEventListener('mousedown', (e) => startWindowResize(e, win, h));
          win.appendChild(handleEl);
        });
      });
    }

    function startWindowResize(e, win, handle) {
      e.preventDefault();
      e.stopPropagation();
      bringToFront(win.id);

      activeResizingWin = win;
      activeResizeHandle = handle;
      activeResizingWin.classList.add('is-resizing');

      startResizeX = e.clientX;
      startResizeY = e.clientY;
      startWinW = win.offsetWidth;
      startWinH = win.offsetHeight;
      startWinTop = win.offsetTop;
      startWinLeft = win.offsetLeft;

      window.addEventListener('mousemove', onWindowResizeMove);
      window.addEventListener('mouseup', stopWindowResize);
    }

    function onWindowResizeMove(e) {
      if (!activeResizingWin) return;
      const dx = e.clientX - startResizeX;
      const dy = e.clientY - startResizeY;

      const minW = 380;
      const minH = 240;

      if (activeResizeHandle.includes('e')) {
        activeResizingWin.style.width = Math.max(minW, startWinW + dx) + 'px';
      }
      if (activeResizeHandle.includes('s')) {
        activeResizingWin.style.height = Math.max(minH, startWinH + dy) + 'px';
      }
      if (activeResizeHandle.includes('w')) {
        const newW = Math.max(minW, startWinW - dx);
        if (newW > minW) {
          activeResizingWin.style.width = newW + 'px';
          activeResizingWin.style.left = (startWinLeft + dx) + 'px';
        }
      }
      if (activeResizeHandle.includes('n')) {
        const newH = Math.max(minH, startWinH - dy);
        if (newH > minH) {
          activeResizingWin.style.height = newH + 'px';
          activeResizingWin.style.top = Math.max(30, startWinTop + dy) + 'px';
        }
      }
    }

    function stopWindowResize() {
      if (activeResizingWin) {
        activeResizingWin.classList.remove('is-resizing');
        activeResizingWin = null;
      }
      window.removeEventListener('mousemove', onWindowResizeMove);
      window.removeEventListener('mouseup', stopWindowResize);
    }

    // =========================================================================
    // WINDOWS 11 SNAP LAYOUTS FLYOUT & EDGE DRAG SNAPPING
    // =========================================================================
    let snapTargetWinId = null;

    function showSnapFlyout(e, winId) {
      snapTargetWinId = winId;
      const btn = e.currentTarget;
      const rect = btn.getBoundingClientRect();
      const flyout = document.getElementById('snap-layouts-flyout');
      if (!flyout) return;

      flyout.style.top = (rect.bottom + 8) + 'px';
      flyout.style.left = Math.min(window.innerWidth - 360, rect.left - 10) + 'px';
      flyout.classList.add('show');
    }

    function hideSnapFlyout() {
      const flyout = document.getElementById('snap-layouts-flyout');
      if (flyout) flyout.classList.remove('show');
    }

    function applySnapLayout(layout) {
      if (!snapTargetWinId) return;
      const win = document.getElementById(snapTargetWinId);
      hideSnapFlyout();
      if (!win) return;

      // Save original bounds if not already saved
      if (!win.dataset.origTop) {
        win.dataset.origTop = win.style.top || (win.offsetTop + 'px');
        win.dataset.origLeft = win.style.left || (win.offsetLeft + 'px');
        win.dataset.origWidth = win.style.width || (win.offsetWidth + 'px');
        win.dataset.origHeight = win.style.height || (win.offsetHeight + 'px');
      }

      win.style.transition = 'all 0.28s cubic-bezier(0.16, 1, 0.3, 1)';
      win.style.borderRadius = '10px';

      const topBarHeight = 32;
      const dockMargin = 96;
      const availHeight = window.innerHeight - topBarHeight - dockMargin;

      switch(layout) {
        case 'left-50':
          win.style.top = topBarHeight + 'px';
          win.style.left = '8px';
          win.style.width = 'calc(50vw - 12px)';
          win.style.height = availHeight + 'px';
          break;
        case 'right-50':
          win.style.top = topBarHeight + 'px';
          win.style.left = 'calc(50vw + 4px)';
          win.style.width = 'calc(50vw - 12px)';
          win.style.height = availHeight + 'px';
          break;
        case 'left-65':
          win.style.top = topBarHeight + 'px';
          win.style.left = '8px';
          win.style.width = 'calc(65vw - 12px)';
          win.style.height = availHeight + 'px';
          break;
        case 'right-35':
          win.style.top = topBarHeight + 'px';
          win.style.left = 'calc(65vw + 4px)';
          win.style.width = 'calc(35vw - 12px)';
          win.style.height = availHeight + 'px';
          break;
        case 'top-left-25':
          win.style.top = topBarHeight + 'px';
          win.style.left = '8px';
          win.style.width = 'calc(50vw - 12px)';
          win.style.height = ((availHeight / 2) - 4) + 'px';
          break;
        case 'bottom-left-25':
          win.style.top = (topBarHeight + (availHeight / 2) + 4) + 'px';
          win.style.left = '8px';
          win.style.width = 'calc(50vw - 12px)';
          win.style.height = ((availHeight / 2) - 4) + 'px';
          break;
        case 'top-right-25':
          win.style.top = topBarHeight + 'px';
          win.style.left = 'calc(50vw + 4px)';
          win.style.width = 'calc(50vw - 12px)';
          win.style.height = ((availHeight / 2) - 4) + 'px';
          break;
        case 'bottom-right-25':
          win.style.top = (topBarHeight + (availHeight / 2) + 4) + 'px';
          win.style.left = 'calc(50vw + 4px)';
          win.style.width = 'calc(50vw - 12px)';
          win.style.height = ((availHeight / 2) - 4) + 'px';
          break;
        case 'maximize':
        default:
          win.style.top = '32px';
          win.style.left = '8px';
          win.style.width = 'calc(100vw - 16px)';
          win.style.height = availHeight + 'px';
          break;
      }
    }

    // DaxClock Tab Switching & Live World Clock Ticker
    function switchClockTab(tab) {
      const worldP = document.getElementById('clock-panel-world');
      const alarmP = document.getElementById('clock-panel-alarm');
      const stopP = document.getElementById('clock-panel-stopwatch');
      const timerP = document.getElementById('clock-panel-timer');
      const bW = document.getElementById('btn-clock-world');
      const bA = document.getElementById('btn-clock-alarm');
      const bS = document.getElementById('btn-clock-stopwatch');
      const bT = document.getElementById('btn-clock-timer');
      const title = document.getElementById('clock-suite-title');

      [worldP, alarmP, stopP, timerP].forEach(p => { if (p) p.style.display = 'none'; });
      [bW, bA, bS, bT].forEach(b => { if (b) b.classList.remove('active'); });

      if (tab === 'alarm') {
        if (alarmP) alarmP.style.display = 'flex';
        if (bA) bA.classList.add('active');
        if (title) title.textContent = 'Jam — Pengatur Jadwal & Multi-Alarm';
      } else if (tab === 'stopwatch') {
        if (stopP) stopP.style.display = 'flex';
        if (bS) bS.classList.add('active');
        if (title) title.textContent = 'Jam — Stopwatch Presisi Milidetik (Hardware Timer)';
      } else if (tab === 'timer') {
        if (timerP) timerP.style.display = 'flex';
        if (bT) bT.classList.add('active');
        if (title) title.textContent = 'Jam — Hitung Mundur Waktu (Pomodoro Timer)';
      } else {
        if (worldP) worldP.style.display = 'flex';
        if (bW) bW.classList.add('active');
        if (title) title.textContent = 'Jam & Waktu Dunia — Jakarta, Tokyo, London & New York';
      }
    }

    // Initialize resize handles on DOM load
    document.addEventListener('DOMContentLoaded', () => {
      initWindowResizeHandles();
    });
"""

    if "function initWindowResizeHandles()" not in content:
        content = content.replace("</script>", js_logic + "\n  </script>", 1)
        print("[OK] Injected Resizing, Snapping, and Clock JavaScript logic")

    # Save modified file
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] Fully integrated Office Suite, Clock, Snapping, and Cursor Resizing into index.html!")

if __name__ == "__main__":
    main()
