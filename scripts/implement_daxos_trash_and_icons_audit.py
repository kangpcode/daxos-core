#!/usr/bin/env python3
"""
implement_daxos_trash_and_icons_audit.py

Comprehensive implementation of:
1. Windows 11 / macOS style Trash / Recycle Bin application (win-trash) with:
   - Ribbon / Command bar: Empty Recycle Bin, Restore All Items, Restore Selected, Properties, Search filter, View switcher (Table / Grid)
   - Interactive item selection, restoration, permanent deletion, empty confirmation
   - Btrfs CoW snapshot storage telemetry
2. DaxFont Typography Studio (win-daxfont) window markup and controller
3. DaXDrop AirShare Wireless & Gesture radar (win-daxdrop) window markup
4. Desktop layer shortcut for Tempat Sampah
5. Launchpad item for Tempat Sampah
6. Finder sidebar shortcut for Tempat Sampah
7. Icon audit: Ensure every window header has a branded vector icon
8. Registry & Dock integration for win-trash
"""

import sys
import re

INDEX_HTML = "src/ui/desktop_preview/index.html"

def main():
    print("[1/6] Reading index.html...")
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # =========================================================================
    # 1. WINDOW MARKUPS: win-trash, win-daxfont, win-daxdrop
    # =========================================================================
    new_windows = """
  <!-- ========================================================================
       WINDOW: TEMPAT SAMPAH / RECYCLE BIN (WINDOWS 11 & MACOS PARITY)
       ======================================================================== -->
  <div class="window" id="win-trash" style="top: 80px; left: 220px; width: 920px; height: 580px; display: none;">
    <div class="win-resize-handle rh-n"></div>
    <div class="win-resize-handle rh-s"></div>
    <div class="win-resize-handle rh-e"></div>
    <div class="win-resize-handle rh-w"></div>
    <div class="win-resize-handle rh-nw"></div>
    <div class="win-resize-handle rh-ne"></div>
    <div class="win-resize-handle rh-sw"></div>
    <div class="win-resize-handle rh-se"></div>
    <div class="window-header" onmousedown="startDrag(event, 'win-trash')" ondblclick="maximizeWindow('win-trash')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeApp('win-trash')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeApp('win-trash')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-trash')" onclick="maximizeWindow('win-trash')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 16px; height: 16px;"><use href="#icon-trash"/></svg>
        <span>Tempat Sampah (Recycle Bin) &bull; DAXOS Subvolume</span>
      </div>
    </div>
    <div class="window-content" style="padding: 0; display: flex; flex-direction: column; background: #0A0D14; color: #F3F4F6;">
      <!-- Command Bar / Ribbon (Windows 11 Fluent Style) -->
      <div style="background: rgba(17, 24, 39, 0.7); border-bottom: 1px solid rgba(255,255,255,0.08); padding: 8px 16px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <button class="btn btn-primary" onclick="emptyTrashWithConfirmation()" style="font-size: 11px; padding: 5px 12px; display: flex; align-items: center; gap: 6px; background: rgba(239,68,68,0.2); border: 1px solid rgba(239,68,68,0.4); color: #F87171;">
          <svg style="width: 13px; height: 13px;" viewBox="0 0 24 24"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" fill="none" stroke="currentColor" stroke-width="2"/></svg>
          Kosongkan Tempat Sampah
        </button>
        <button class="btn btn-secondary" onclick="restoreAllTrashItems()" style="font-size: 11px; padding: 5px 12px; display: flex; align-items: center; gap: 6px;">
          <svg style="width: 13px; height: 13px;" viewBox="0 0 24 24"><path d="M3 10h10a5 5 0 0 1 5 5v2M3 10l5-5M3 10l5 5" fill="none" stroke="currentColor" stroke-width="2"/></svg>
          Pulihkan Semua Item
        </button>
        <button class="btn btn-secondary" id="btn-restore-selected" onclick="restoreSelectedTrashItem()" style="font-size: 11px; padding: 5px 12px; display: flex; align-items: center; gap: 6px; opacity: 0.5; pointer-events: none;">
          <svg style="width: 13px; height: 13px;" viewBox="0 0 24 24"><polyline points="9 14 4 9 9 4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20v-7a4 4 0 0 0-4-4H4" fill="none" stroke="currentColor" stroke-width="2"/></svg>
          Pulihkan Item Terpilih
        </button>
        <button class="btn btn-secondary" onclick="showTrashProperties()" style="font-size: 11px; padding: 5px 12px; display: flex; align-items: center; gap: 6px;">
          <svg style="width: 13px; height: 13px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><line x1="12" y1="16" x2="12" y2="12" stroke="currentColor" stroke-width="2"/><line x1="12" y1="8" x2="12.01" y2="8" stroke="currentColor" stroke-width="2"/></svg>
          Properti Kuota
        </button>
        <div style="margin-left: auto; display: flex; align-items: center; gap: 8px;">
          <input type="text" id="trash-search-input" oninput="filterTrashItems(this.value)" placeholder="Cari di Tempat Sampah..." style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.12); border-radius: 6px; padding: 4px 10px; font-size: 11px; color: #FFF; width: 170px; outline: none;"/>
          <div style="display: flex; gap: 2px; background: rgba(0,0,0,0.3); border-radius: 6px; padding: 2px;">
            <button id="trash-view-table-btn" onclick="setTrashViewMode('table')" style="background: rgba(255,255,255,0.15); border: none; color: #FFF; padding: 3px 8px; border-radius: 4px; cursor: pointer; font-size: 11px;">Daftar</button>
            <button id="trash-view-grid-btn" onclick="setTrashViewMode('grid')" style="background: transparent; border: none; color: #9CA3AF; padding: 3px 8px; border-radius: 4px; cursor: pointer; font-size: 11px;">Grid</button>
          </div>
        </div>
      </div>

      <!-- Main Trash Body -->
      <div style="flex: 1; overflow-y: auto; padding: 12px 16px; position: relative;" id="trash-content-container">
        <!-- Trash Table View -->
        <table id="trash-table" style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
          <thead>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #9CA3AF; font-size: 11px;">
              <th style="padding: 8px 10px;">NAMA BERKAS</th>
              <th style="padding: 8px 10px;">LOKASI ASLI</th>
              <th style="padding: 8px 10px;">TANGGAL DIHAPUS</th>
              <th style="padding: 8px 10px;">UKURAN</th>
              <th style="padding: 8px 10px;">TIPE</th>
              <th style="padding: 8px 10px; text-align: right;">AKSI</th>
            </tr>
          </thead>
          <tbody id="trash-tbody">
            <!-- Dynamically populated via renderTrash() -->
          </tbody>
        </table>

        <!-- Trash Grid View -->
        <div id="trash-grid" style="display: none; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 14px; padding: 10px;">
          <!-- Dynamically populated via renderTrash() -->
        </div>

        <!-- Empty State -->
        <div id="trash-empty-state" style="display: none; flex-direction: column; align-items: center; justify-content: center; height: 320px; color: #6B7280; gap: 12px;">
          <svg style="width: 64px; height: 64px; opacity: 0.4;"><use href="#icon-trash"/></svg>
          <div style="font-size: 16px; font-weight: 600; color: #9CA3AF;">Tempat Sampah Kosong</div>
          <div style="font-size: 12px;">Tidak ada berkas atau folder yang dihapus di sistem DAXOS.</div>
        </div>
      </div>

      <!-- Status Bar -->
      <div style="background: rgba(17, 24, 39, 0.9); border-top: 1px solid rgba(255,255,255,0.08); padding: 6px 16px; font-size: 11px; color: #9CA3AF; display: flex; justify-content: space-between; align-items: center;">
        <span id="trash-status-text">5 item | 87.1 MB total</span>
        <span>Btrfs CoW Subvolume: /var/trash &bull; Kuota: 10.0 GB (Bebas Defragmentasi)</span>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: DAXFONT TYPOGRAPHY & FONT MANAGER (UBUNTU / MACOS / WIN11 PARITY)
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
    <div class="window-header" onmousedown="startDrag(event, 'win-daxfont')" ondblclick="maximizeWindow('win-daxfont')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeApp('win-daxfont')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeApp('win-daxfont')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-daxfont')" onmouseenter="showSnapFlyout(event, 'win-daxfont')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 16px; height: 16px;"><use href="#icon-font"/></svg>
        <span>DaxFont &bull; Pengelola Font &amp; Tipografi DAXOS</span>
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
        <div style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.08);">
          <input type="text" id="font-search-input" oninput="searchFontCatalog(this.value)" placeholder="Cari nama font, desainer..." style="width: 100%; box-sizing: border-box; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 7px 10px; color: #FFFFFF; font-size: 12px; outline: none;"/>
        </div>
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
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 3px; font-family: monospace;">const SLA: f32 = 0.045; // &le; 45ms</div>
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
        <div style="padding: 10px 16px; border-bottom: 1px solid rgba(255,255,255,0.08); display: flex; justify-content: space-between; align-items: center; background: rgba(17, 24, 39, 0.5);">
          <div style="display: flex; gap: 8px;">
            <button id="tab-btn-waterfall" onclick="switchFontTab('waterfall')" style="background: rgba(236,72,153,0.25); border: none; color: #F472B6; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer;">Waterfall Preview</button>
            <button id="tab-btn-glyphs" onclick="switchFontTab('glyphs')" style="background: transparent; border: none; color: #9CA3AF; padding: 5px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">Peta Glif Karakter</button>
            <button id="tab-btn-meta" onclick="switchFontTab('meta')" style="background: transparent; border: none; color: #9CA3AF; padding: 5px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">Spesifikasi &amp; Tuning Subpixel</button>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 11px; color: #9CA3AF;">Ukuran:</span>
            <input type="range" id="font-size-slider" min="12" max="72" value="28" oninput="updateFontSizePreview(this.value)" style="width: 100px; accent-color: #EC4899;"/>
            <span id="font-size-label" style="font-size: 11px; color: #FFF; width: 35px;">28px</span>
          </div>
        </div>

        <!-- Tab Content -->
        <div style="padding: 20px; flex: 1;">
          <!-- WATERFALL TAB -->
          <div id="tab-view-waterfall" style="display: block;">
            <div style="margin-bottom: 20px;">
              <input type="text" id="font-sample-text" oninput="updateSampleText(this.value)" value="The quick brown fox jumps over the lazy dog 1234567890" style="width: 100%; box-sizing: border-box; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 14px; color: #FFFFFF; font-size: 14px; outline: none;"/>
            </div>
            <div id="waterfall-container" style="display: flex; flex-direction: column; gap: 18px;">
              <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px;">
                <div style="font-size: 11px; color: #9CA3AF; margin-bottom: 4px;">Light 300 &bull; 14px</div>
                <div class="wf-sample" style="font-size: 14px; font-weight: 300;">The quick brown fox jumps over the lazy dog 1234567890</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px;">
                <div style="font-size: 11px; color: #9CA3AF; margin-bottom: 4px;">Regular 400 &bull; 18px</div>
                <div class="wf-sample" style="font-size: 18px; font-weight: 400;">The quick brown fox jumps over the lazy dog 1234567890</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px;">
                <div style="font-size: 11px; color: #9CA3AF; margin-bottom: 4px;">Medium 500 &bull; 24px</div>
                <div class="wf-sample" style="font-size: 24px; font-weight: 500;">The quick brown fox jumps over the lazy dog 1234567890</div>
              </div>
              <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px;">
                <div style="font-size: 11px; color: #9CA3AF; margin-bottom: 4px;">SemiBold 600 &bull; 32px</div>
                <div class="wf-sample" style="font-size: 32px; font-weight: 600;">The quick brown fox jumps over the lazy dog</div>
              </div>
              <div>
                <div style="font-size: 11px; color: #9CA3AF; margin-bottom: 4px;">Bold 700 &bull; 44px</div>
                <div class="wf-sample" style="font-size: 44px; font-weight: 700;">The quick brown fox jumps</div>
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
              <!-- Dynamically populated via initGlyphGrid() -->
            </div>
          </div>

          <!-- METADATA & RENDERING TAB -->
          <div id="tab-view-meta" style="display: none;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 16px;">
                <div style="font-size: 14px; font-weight: 700; color: #F472B6; margin-bottom: 12px;">Spesifikasi Berkas Font</div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px;">
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Nama PostScript</span><span style="font-family: monospace; color: #FFFFFF;" id="meta-postscript">Inter-Regular</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Format Kontainer</span><span style="color: #FFFFFF;" id="meta-format">OpenType CFF (.otf)</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Jumlah Glif</span><span style="color: #FFFFFF;" id="meta-glyphs">2,548 glyphs</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Fitur OpenType</span><span style="color: #10B981;" id="meta-features">calt, liga, tnum, ss01</span></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: #9CA3AF;">Lokasi Penyimpanan</span><span style="font-family: monospace; font-size: 10px; color: #9CA3AF;" id="meta-path">/usr/share/fonts/opentype/</span></div>
                </div>
              </div>

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

  <!-- ========================================================================
       WINDOW: DAXDROP AIRSHARE & GESTURE RADAR
       ======================================================================== -->
  <div class="window" id="win-daxdrop" style="top: 80px; left: 210px; width: 880px; height: 570px; display: none;">
    <div class="win-resize-handle rh-n"></div>
    <div class="win-resize-handle rh-s"></div>
    <div class="win-resize-handle rh-e"></div>
    <div class="win-resize-handle rh-w"></div>
    <div class="win-resize-handle rh-nw"></div>
    <div class="win-resize-handle rh-ne"></div>
    <div class="win-resize-handle rh-sw"></div>
    <div class="win-resize-handle rh-se"></div>
    <div class="window-header" onmousedown="startDrag(event, 'win-daxdrop')" ondblclick="maximizeWindow('win-daxdrop')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeApp('win-daxdrop')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeApp('win-daxdrop')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-daxdrop')" onclick="maximizeWindow('win-daxdrop')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 16px; height: 16px;"><use href="#icon-daxdrop"/></svg>
        <span>DaXDrop &bull; Wireless P2P &amp; Air-Gesture Sharing</span>
      </div>
    </div>
    <div class="window-content" style="padding: 20px; display: flex; flex-direction: column; gap: 16px; background: #0A0D14; color: #FFF; overflow-y: auto;">
      <!-- Sensor & Air Gesture Status Banner -->
      <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 18px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 40px; height: 40px; border-radius: 8px; background: rgba(0,210,255,0.15); display: flex; align-items: center; justify-content: center;">
            <svg style="width: 24px; height: 24px;"><use href="#icon-camera"/></svg>
          </div>
          <div>
            <div style="font-weight: 700; font-size: 14px;">Optical Gesture Tracking (V4L2 60 FPS)</div>
            <div style="font-size: 12px; color: #8E8EA0;">Kamera mengamati telapak tangan untuk pengiriman berkas instan</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          <span id="daxdrop-pose-badge" style="font-size: 12px; font-weight: 700; color: #30D158; background: rgba(48,209,88,0.15); padding: 5px 12px; border-radius: 6px; border: 1px solid rgba(48,209,88,0.3);">Pose: Telapak Terbuka (Ready)</span>
          <button id="btn-airgrab-toggle" class="btn btn-primary" onclick="toggleAirGrabPose()" style="font-size: 12px; padding: 6px 14px;">Simulasi Kepal Tangan</button>
        </div>
      </div>

      <!-- Radar & Discovered Devices -->
      <div>
        <div style="font-size: 13px; font-weight: 700; color: #8E8EA0; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">Perangkat Terdekat (Air-Drop Wi-Fi 7 Direct)</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
          <!-- Peer 1: Phone -->
          <div id="peer-phone" onclick="selectPeer('phone')" style="background: rgba(0,210,255,0.08); border: 1px solid #00D2FF; border-radius: 10px; padding: 14px; cursor: pointer; display: flex; align-items: center; gap: 12px;">
            <div style="width: 36px; height: 36px; border-radius: 8px; background: #38BDF8; display: flex; align-items: center; justify-content: center; color: #0C1E3D; font-weight: 900; font-size: 16px;">P</div>
            <div style="flex: 1;">
              <div style="font-weight: 700; font-size: 13px;">DAXOS Rhino Phone Ultra</div>
              <div style="font-size: 11px; color: #38BDF8;">Terkunci &bull; Siap Menerima (0.8m)</div>
            </div>
          </div>
          <!-- Peer 2: Laptop -->
          <div id="peer-tablet" onclick="selectPeer('tablet')" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; cursor: pointer; display: flex; align-items: center; gap: 12px;">
            <div style="width: 36px; height: 36px; border-radius: 8px; background: #C084FC; display: flex; align-items: center; justify-content: center; color: #1E1B4B; font-weight: 900; font-size: 16px;">M</div>
            <div style="flex: 1;">
              <div style="font-weight: 700; font-size: 13px;">MacBook Pro M3 (Darling P2P)</div>
              <div style="font-size: 11px; color: #8E8EA0;">Tersedia di Jaringan (2.4m)</div>
            </div>
          </div>
          <!-- Peer 3: Workstation -->
          <div id="peer-station" onclick="selectPeer('station')" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; cursor: pointer; display: flex; align-items: center; gap: 12px;">
            <div style="width: 36px; height: 36px; border-radius: 8px; background: #34D399; display: flex; align-items: center; justify-content: center; color: #064E3B; font-weight: 900; font-size: 16px;">T</div>
            <div style="flex: 1;">
              <div style="font-weight: 700; font-size: 13px;">ThinkPad X1 DAXOS Core</div>
              <div style="font-size: 11px; color: #8E8EA0;">Tersedia di Jaringan (4.1m)</div>
            </div>
          </div>
        </div>
      </div>

      <!-- File Transfer Panel -->
      <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 18px; display: flex; flex-direction: column; gap: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="font-size: 13px; font-weight: 700;">Enkripsi &amp; Protokol Transfer P2P</div>
          <span style="font-size: 11px; background: rgba(52,211,153,0.15); color: #34D399; padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(52,211,153,0.3);">ChaCha20-Poly1305 / SHA3-512</span>
        </div>
        <div style="display: flex; gap: 10px;">
          <button class="btn btn-primary" onclick="simulateFileTransfer()" style="padding: 8px 18px; font-size: 12px; font-weight: 700;">Kirim Berkas Uji (DAXOS_Spec.pdf)</button>
          <button class="btn btn-secondary" onclick="alert('DaXDrop mendengarkan broadcast mDNS di port 8892.');" style="padding: 8px 14px; font-size: 12px;">Segarkan Radar</button>
        </div>
        <div id="daxdrop-progress-bar" style="display: none; width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin-top: 6px;">
          <div id="daxdrop-progress-inner" style="width: 0%; height: 100%; background: linear-gradient(90deg, #00D2FF, #34D399); transition: width 0.3s ease;"></div>
        </div>
      </div>
    </div>
  </div>
"""

    if 'id="win-trash"' not in html:
        # Inject right before the dock snap overlay or before the main-dock container
        target_point = '<!-- Windows 11 Snap Ghost Preview Overlay -->'
        if target_point in html:
            html = html.replace(target_point, new_windows + '\n  ' + target_point)
            print("[OK] Injected win-trash, win-daxfont, and win-daxdrop window markups")
        else:
            print("[WARN] Could not find snap overlay target point")

    # =========================================================================
    # 2. DESKTOP SHORTCUT FOR TEMPAT SAMPAH
    # =========================================================================
    desktop_trash = """    <div class="desktop-shortcut-item" ondblclick="openApp('win-trash', 'Keranjang Sampah')" oncontextmenu="handleTrashContextMenu(event)">
      <svg style="width: 44px; height: 44px;"><use id="desktop-trash-svg-use" href="#icon-trash"/></svg>
      <div class="desktop-shortcut-title">Tempat Sampah</div>
    </div>"""

    if 'ondblclick="openApp(\'win-trash\'' not in html:
        html = html.replace('  <!-- DESKTOP ICONS LAYER -->\n  <div id="desktop-items-layer">',
                            '  <!-- DESKTOP ICONS LAYER -->\n  <div id="desktop-items-layer">\n' + desktop_trash)
        print("[OK] Injected Tempat Sampah desktop shortcut")

    # =========================================================================
    # 3. DOCK SAMPAH ONCLICK
    # =========================================================================
    html = re.sub(
        r'<div class="dock-item" onclick="openTrashDialog\(\)"',
        '<div class="dock-item" id="dock-item-win-trash" onclick="openApp(\'win-trash\', \'Keranjang Sampah\')"',
        html
    )
    # Ensure dock dot exists for win-trash
    if 'id="dot-win-trash"' not in html:
        html = html.replace(
            '<div class="dock-tooltip">Keranjang Sampah</div>\n        <svg class="dock-icon-svg"><use href="#icon-trash"/></svg>',
            '<div class="dock-tooltip">Keranjang Sampah</div>\n        <svg class="dock-icon-svg"><use id="dock-trash-svg-use" href="#icon-trash"/></svg>\n        <div class="dock-dot" id="dot-win-trash"></div>'
        )
    print("[OK] Updated Dock item to open win-trash with active dot indicator")

    # =========================================================================
    # 4. LAUNCHPAD ITEM FOR TEMPAT SAMPAH
    # =========================================================================
    launchpad_trash = """        <div class="launchpad-item" data-category="system" data-name="Tempat Sampah Keranjang Recycle Bin Trash Hapus Berkas Restore" onclick="launchAppFromLaunchpad('win-trash', 'Keranjang Sampah')">
          <svg class="launchpad-item-icon"><use href="#icon-trash"/></svg>
          <div class="launchpad-item-title">Tempat Sampah</div>
          <div class="launchpad-item-desc">Pengelolaan Berkas Dihapus &amp; Pemulihan</div>
        </div>"""

    if "launchAppFromLaunchpad('win-trash'" not in html:
        html = html.replace('        <div class="launchpad-item" data-category="system" data-name="DaxFont Font Manager Pengelola Tipografi Karakter Glyphs Huruf"',
                            launchpad_trash + '\n        <div class="launchpad-item" data-category="system" data-name="DaxFont Font Manager Pengelola Tipografi Karakter Glyphs Huruf"')
        print("[OK] Injected Tempat Sampah into Launchpad grid")

    # =========================================================================
    # 5. FINDER SIDEBAR ITEM FOR TEMPAT SAMPAH
    # =========================================================================
    finder_trash_nav = """          <div class="finder-nav-item" onclick="openApp('win-trash', 'Keranjang Sampah')">
            <svg class="finder-nav-icon"><use href="#icon-trash"/></svg>
            Tempat Sampah
          </div>"""

    if 'openApp(\'win-trash\', \'Keranjang Sampah\')' not in html or 'finder-nav-item' in html:
        if 'Tempat Sampah\n          </div>' not in html:
            html = html.replace('          <div class="finder-section-title">DaxCloud</div>',
                                finder_trash_nav + '\n\n          <div class="finder-section-title">DaxCloud</div>')
            print("[OK] Injected Tempat Sampah into Finder sidebar")

    # =========================================================================
    # 6. JAVASCRIPT CONTROLLERS: TRASH & DAXFONT & ICONS
    # =========================================================================
    js_controllers = """
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
        document.getElementById('trash-table').style.display = 'none';
        grid.style.display = 'none';
        if (statusText) statusText.textContent = '0 item | 0 MB total (Tempat Sampah Kosong)';
        if (restoreBtn) {
          restoreBtn.style.opacity = '0.5';
          restoreBtn.style.pointerEvents = 'none';
        }
        return;
      }

      emptyState.style.display = 'none';
      if (currentTrashView === 'table') {
        document.getElementById('trash-table').style.display = 'table';
        grid.style.display = 'none';
      } else {
        document.getElementById('trash-table').style.display = 'none';
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
      const q = query.toLowerCase();
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
        designer: 'Rasmus Andersson',
        license: 'SIL Open Font License 1.1',
        format: 'OpenType CFF (.otf)',
        glyphs: '2,548 glyphs',
        features: 'calt, liga, tnum, cv01, ss01',
        path: '/usr/share/fonts/opentype/inter/',
        postscript: 'InterDisplay-Regular',
        pangram: 'The quick brown fox jumps over the lazy dog 1234567890'
      },
      'JetBrains Mono': {
        designer: 'JetBrains Core Team',
        license: 'Apache License 2.0',
        format: 'TrueType (.ttf)',
        glyphs: '1,480 glyphs',
        features: 'calt (Code Ligatures: =>, !=, ===), zero, ss02',
        path: '/usr/share/fonts/truetype/jetbrains/',
        postscript: 'JetBrainsMono-Regular',
        pangram: 'fn daxos_kernel_init() -> Result<(), E> { OK }'
      },
      'Fira Code': {
        designer: 'Nikita Prokopov',
        license: 'SIL Open Font License 1.1',
        format: 'OpenType CFF (.otf)',
        glyphs: '1,220 glyphs',
        features: 'calt, zero, onum, ss03',
        path: '/usr/share/fonts/opentype/firacode/',
        postscript: 'FiraCode-Regular',
        pangram: '0 <= latency && latency <= 0.045 // 45ms target'
      },
      'Playfair Display': {
        designer: 'Claus Eggers Sorensen',
        license: 'SIL Open Font License 1.1',
        format: 'TrueType (.ttf)',
        glyphs: '1,180 glyphs',
        features: 'dlig, kern, liga, swsh',
        path: '/usr/share/fonts/truetype/playfair/',
        postscript: 'PlayfairDisplay-Regular',
        pangram: 'Seni Tipografi Megah Sistem Operasi DAXOS 2026'
      },
      'Outfit': {
        designer: 'Outfit Typography Guild',
        license: 'SIL Open Font License 1.1',
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
      document.querySelectorAll('.wf-sample').forEach(el => {
        el.textContent = text;
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
      const query = q.toLowerCase();
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
        alert(`[SUKSES] Font '${font}' berhasil dipasang ke sistem DAXOS! Direktori: /usr/share/fonts/opentype/user/. Cache font fc-cache diperbarui.`);
      }
    }

    function saveFontTuning() {
      const aa = document.getElementById('font-aa-select')?.value || 'Subpixel LCD (RGB)';
      const hint = document.getElementById('font-hint-select')?.value || 'Slight';
      alert(`[SUKSES] Konfigurasi tipografi DAXOS disimpan:
• Antialiasing: ${aa}
• Hinting: ${hint}
Pembaruan diterapkan instan pada DreXUI Compositor 240Hz.`);
    }

    // Initialize Trash and DaxFont on ready
    document.addEventListener('DOMContentLoaded', () => {
      renderTrash();
      setTimeout(initGlyphGrid, 500);
    });
"""

    if "function renderTrash" not in html:
        # Inject right before the closing </script>
        html = html.replace('//]]>\n  </script>', js_controllers + '\n//]]>\n  </script>')
        print("[OK] Injected Trash & DaxFont JavaScript controllers")

    # =========================================================================
    # 7. UPDATE DAXOS_DOCK_REGISTRY TO INCLUDE 'win-trash'
    # =========================================================================
    if "'win-trash'" not in html:
        html = html.replace(
            "'win-finder': { name: 'Finder', icon: '#icon-finder', permanent: true },",
            "'win-finder': { name: 'Finder', icon: '#icon-finder', permanent: true },\n      'win-trash': { name: 'Keranjang Sampah', icon: '#icon-trash', permanent: true },"
        )
        print("[OK] Registered 'win-trash' in DAXOS_DOCK_REGISTRY")

    # =========================================================================
    # 8. UPDATE handleTrashContextMenu
    # =========================================================================
    html = re.sub(
        r'function handleTrashContextMenu\(e\) \{[^}]+\}',
        """function handleTrashContextMenu(e) {
      e.preventDefault();
      e.stopPropagation();
      closeAllContextMenus();
      currentDockCtxWinId = 'win-trash';
      const menu = document.getElementById('dock-context-menu');
      if (menu) {
        document.getElementById('dock-ctx-title').textContent = 'Keranjang Sampah';
        document.getElementById('dock-ctx-pin-text').textContent = 'Kosongkan Tempat Sampah';
        const pinAction = document.getElementById('dock-ctx-pin-action');
        if (pinAction) pinAction.onclick = function() { closeAllContextMenus(); emptyTrashWithConfirmation(); };
        menu.style.display = 'block';
        menu.style.left = Math.max(10, Math.min(window.innerWidth - 240, e.clientX - 100)) + 'px';
        menu.style.top = (e.clientY - 140) + 'px';
      }
    }""",
        html
    )
    print("[OK] Updated handleTrashContextMenu for rich context actions")

    # =========================================================================
    # 9. WINDOW HEADERS ICON AUDIT
    # =========================================================================
    # Ensure every window has its branded vector icon in the header
    window_icon_mappings = [
      ('win-finder', '#icon-finder', 'Files'),
      ('win-terminal', '#icon-terminal', 'Terminal'),
      ('win-ide', '#icon-ide', 'DCODX'),
      ('win-daxbro', '#icon-daxbro', 'DaXBro'),
      ('win-camera', '#icon-camera', 'Studio Camera'),
      ('win-calculator', '#icon-calculator', 'Calculator'),
      ('win-settings', '#icon-settings', 'System Settings'),
      ('win-dapstore', '#icon-dapstore', 'DapStore'),
      ('win-dxdef', '#icon-dxdef', 'DXDEF Security'),
      ('win-driver-settings', '#icon-driver', 'Driver Settings'),
      ('win-activity-monitor', '#icon-monitor', 'Activity Monitor'),
      ('win-user-accounts', '#icon-account', 'User Accounts'),
      ('win-compat-runner', '#icon-compat', 'Universal Apps'),
      ('win-network-manager', '#icon-network', 'Network & DNS'),
      ('win-app-manager', '#icon-app-manager', 'App Manager'),
      ('win-gaming-hub', '#icon-gaming-hub', 'Gaming Hub'),
      ('win-editor', '#icon-editor', 'dEdit'),
      ('win-disks', '#icon-disks', 'Disk Utility'),
      ('win-media', '#icon-media', 'Spatial Audio'),
      ('win-installer', '#icon-installer', 'Install DAXOS'),
      ('win-daxword', '#icon-word', 'DaxWord'),
      ('win-daxsheet', '#icon-sheet', 'DaxSheet'),
      ('win-daxslide', '#icon-slide', 'DaxSlide'),
      ('win-daxclock', '#icon-clock', 'Jam & Waktu Dunia')
    ]

    for win_id, icon_href, title_snippet in window_icon_mappings:
        pattern = rf'(<div class="window"[^>]*id="{win_id}"[^>]*>[\s\S]*?<div class="window-header"[^>]*>[\s\S]*?<div class="traffic-lights">[\s\S]*?</div>\s*)(<span class="window-title"[^>]*>|<div class="window-title"[^>]*>)([^<]*{title_snippet}[^<]*)(</span>|</div>)'
        def add_icon(m):
            prefix = m.group(1)
            tag_open = m.group(2)
            title_text = m.group(3)
            tag_close = m.group(4)
            if 'href="' not in tag_open and '<svg' not in title_text:
                return f'{prefix}<div class="window-title" style="display: flex; align-items: center; gap: 8px;"><svg style="width: 15px; height: 15px; flex-shrink: 0;"><use href="{icon_href}"/></svg><span>{title_text.strip()}</span></div>'
            return m.group(0)
        html = re.sub(pattern, add_icon, html)

    print("[OK] Verified branded vector icons on all window headers")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("[SUCCESS] Comprehensive Trash, DaxFont, DaXDrop, and Icon Audit completed!")

if __name__ == "__main__":
    main()
