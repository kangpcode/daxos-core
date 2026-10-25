#!/usr/bin/env python3
"""
Integrate the 4 new universal applications into src/ui/desktop_preview/index.html:
1. dEdit (win-editor) - Visual Text & Code Editor
2. Disk Utility (win-disks) - GPT/Btrfs Partition & SMART Health
3. Spatial Audio Player (win-media) - 10-Band EQ & HRTF 3D Music Engine
4. DaXDrop AirShare (win-daxdrop) - Standalone Window with Radar & Optical Fist Clench Tracking
"""

import sys
from pathlib import Path

INDEX_FILE = Path("/home/kangpcode/wwwsite/daxos/src/ui/desktop_preview/index.html")

def integrate():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add SVG Symbols
    svg_symbols = '''    <!-- Editor / dEdit Icon -->
    <symbol id="icon-editor" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="editor-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0A84FF"/>
          <stop offset="100%" stop-color="#5E5CE6"/>
        </linearGradient>
      </defs>
      <rect width="128" height="128" rx="28" fill="#1C1C24"/>
      <rect x="26" y="22" width="76" height="84" rx="12" fill="none" stroke="url(#editor-grad)" stroke-width="7"/>
      <!-- Code Brackets & Pen -->
      <path d="M48 48 L40 56 L48 64" fill="none" stroke="#00D2FF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M80 48 L88 56 L80 64" fill="none" stroke="#00D2FF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="68" y1="46" x2="60" y2="66" stroke="#30D158" stroke-width="4" stroke-linecap="round"/>
      <line x1="42" y1="78" x2="86" y2="78" stroke="rgba(255,255,255,0.7)" stroke-width="4" stroke-linecap="round"/>
      <line x1="42" y1="88" x2="74" y2="88" stroke="rgba(255,255,255,0.4)" stroke-width="4" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Disk Utility / dDisk Icon -->
    <symbol id="icon-disks" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="disks-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#64D2FF"/>
          <stop offset="100%" stop-color="#0A84FF"/>
        </linearGradient>
      </defs>
      <rect width="128" height="128" rx="28" fill="#1C1C24"/>
      <rect x="24" y="32" width="80" height="64" rx="14" fill="none" stroke="url(#disks-grad)" stroke-width="7"/>
      <circle cx="64" cy="64" r="18" fill="none" stroke="#00D2FF" stroke-width="5"/>
      <circle cx="64" cy="64" r="6" fill="#30D158"/>
      <line x1="84" y1="84" x2="94" y2="84" stroke="#00D2FF" stroke-width="5" stroke-linecap="round"/>
      <line x1="34" y1="84" x2="42" y2="84" stroke="#30D158" stroke-width="5" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>

    <!-- Spatial Audio / dMedia Icon -->
    <symbol id="icon-media" viewBox="0 0 128 128">
      <defs>
        <linearGradient id="media-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FF375F"/>
          <stop offset="100%" stop-color="#BF5AF2"/>
        </linearGradient>
      </defs>
      <rect width="128" height="128" rx="28" fill="#1C1C24"/>
      <circle cx="64" cy="64" r="44" fill="none" stroke="url(#media-grad)" stroke-width="7"/>
      <!-- Radiating Soundwaves & Note -->
      <path d="M54 74 V48 C54 44 58 42 62 43 L76 46 C79 47 82 50 82 54 V70" fill="none" stroke="#00D2FF" stroke-width="5" stroke-linecap="round"/>
      <circle cx="48" cy="74" r="8" fill="#00D2FF"/>
      <circle cx="76" cy="70" r="8" fill="#FF375F"/>
      <path d="M96 50 C102 58 102 70 96 78" fill="none" stroke="#30D158" stroke-width="4" stroke-linecap="round"/>
      <rect x="1.5" y="1.5" width="125" height="125" rx="27" fill="none" stroke="url(#drex-specular-border)" stroke-width="1.8"/>
    </symbol>
'''
    if '<symbol id="icon-editor"' not in html:
        html = html.replace('<symbol id="icon-driver"', svg_symbols + '\n    <symbol id="icon-driver"')

    # 2. Add New Interactive Windows
    windows_html = '''
  <!-- ========================================================================
       WINDOW: dEdit TEXT & CODE EDITOR (org.daxos.editor)
       ======================================================================== -->
  <div class="window" id="win-editor" style="top: 80px; left: 230px; width: 840px; height: 540px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-editor')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-editor')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-editor')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-editor')">+</div>
      </div>
      <span class="window-title" id="dedit-title">dEdit Pro &bull; Untitled.rs [UTF-8]</span>
      <div style="margin-left: auto; display: flex; gap: 8px;">
        <button class="btn btn-primary" style="font-size: 11px; padding: 4px 12px;" onclick="saveDeditDoc()">Simpan (Save)</button>
        <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="insertDeditSnippet()">+ Snippet</button>
      </div>
    </div>
    <div class="window-content" style="padding: 0; display: flex; flex-direction: column; height: calc(100% - 40px); background: #0E1017;">
      <!-- Tab Bar -->
      <div style="display: flex; background: rgba(255,255,255,0.03); border-bottom: 1px solid var(--border-acrylic); padding: 6px 12px 0 12px; gap: 6px;">
        <div class="launchpad-cat-btn active" style="border-bottom: 2px solid #00D2FF; border-radius: 4px 4px 0 0; padding: 6px 14px; font-size: 11px; cursor: pointer;" id="tab-editor-1" onclick="switchEditorTab(1)">Untitled.rs</div>
        <div class="launchpad-cat-btn" style="border-radius: 4px 4px 0 0; padding: 6px 14px; font-size: 11px; cursor: pointer; color: #8E8EA0;" id="tab-editor-2" onclick="switchEditorTab(2)">main.surf</div>
        <div class="launchpad-cat-btn" style="border-radius: 4px 4px 0 0; padding: 6px 14px; font-size: 11px; cursor: pointer; color: #8E8EA0;" id="tab-editor-3" onclick="switchEditorTab(3)">config.toml</div>
      </div>
      <!-- Editor Main Area -->
      <div style="display: flex; flex: 1; overflow: hidden; position: relative;">
        <!-- Line Numbers -->
        <div style="width: 44px; background: rgba(0,0,0,0.3); color: #555566; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 20px; padding: 12px 6px; text-align: right; user-select: none; border-right: 1px solid rgba(255,255,255,0.05);" id="dedit-linenums">
          1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15
        </div>
        <!-- Textarea -->
        <textarea id="dedit-textarea" style="flex: 1; background: transparent; border: none; outline: none; color: #E6E6FA; font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 12px; line-height: 20px; padding: 12px; resize: none; overflow-y: auto;" oninput="updateDeditStats()">// ============================================================================
// DAXOS KERNEL & APPLICATION ENTRYPOINT
// Language: Rust 2024 / Surflang 1.0 (Zero-Cost Vector Runtime)
// ============================================================================

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("[DAXOS] System Initialized with Acrylic Wayland Compositor");
    println!("[DREXVIS] Hardware Acceleration Active (GPU Jitter <= 0.42 ms)");
    
    // Launch Core Desktop Environment
    daxos::desktop::launch_shell()?;
    Ok(())
}
</textarea>
      </div>
      <!-- Editor Status Bar -->
      <div style="background: rgba(0,0,0,0.4); border-top: 1px solid var(--border-acrylic); padding: 4px 14px; display: flex; justify-content: space-between; font-size: 11px; color: #8E8EA0; font-family: 'Inter', sans-serif;">
        <span id="dedit-stats">Baris: 11 &bull; Karakter: 395 &bull; Kata: 38</span>
        <span>UTF-8 &bull; Rust &bull; Acrylic Blur 32px &bull; Spasi: 4</span>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: dDisk DISK UTILITY & STORAGE MANAGER (org.daxos.disks)
       ======================================================================== -->
  <div class="window" id="win-disks" style="top: 85px; left: 210px; width: 880px; height: 560px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-disks')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-disks')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-disks')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-disks')">+</div>
      </div>
      <span class="window-title">Disk Utility &bull; GPT Partition &amp; SMART Diagnostics</span>
      <div style="margin-left: auto; display: flex; gap: 8px;">
        <button class="btn btn-primary" style="font-size: 11px; padding: 4px 12px;" onclick="runDiskFirstAid()">First Aid (SMART)</button>
        <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="alert('Partisi Btrfs siap diubah ukurannya secara dinamis.')">Partisi</button>
      </div>
    </div>
    <div class="window-content" style="padding: 0; display: flex; height: calc(100% - 40px); background: #0F1018;">
      <!-- Disk Sidebar -->
      <div style="width: 250px; background: rgba(255,255,255,0.02); border-right: 1px solid var(--border-acrylic); padding: 14px; display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 10px; font-weight: 700; color: #8E8EA0; text-transform: uppercase; letter-spacing: 0.5px;">Penyimpanan Internal</div>
        
        <div class="gaming-card active" style="padding: 10px; cursor: pointer; border-color: #00D2FF; background: rgba(0,210,255,0.08);" id="disk-item-nvme" onclick="selectDiskView('nvme')">
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg style="width: 22px; height: 22px;"><use href="#icon-disks"/></svg>
            <div>
              <div style="font-size: 12px; font-weight: 700; color: #FFF;">nvme0n1</div>
              <div style="font-size: 10px; color: #00D2FF;">DAXOS NVMe 1TB PCIe 5.0</div>
            </div>
          </div>
          <div style="font-size: 10px; color: #8E8EA0; margin-top: 4px;">1.00 TB &bull; GPT &bull; Btrfs</div>
        </div>

        <div class="gaming-card" style="padding: 10px; cursor: pointer;" id="disk-item-sata" onclick="selectDiskView('sata')">
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg style="width: 22px; height: 22px;"><use href="#icon-disks"/></svg>
            <div>
              <div style="font-size: 12px; font-weight: 700; color: #FFF;">sda</div>
              <div style="font-size: 10px; color: #8E8EA0;">Kingston Fury 500GB SSD</div>
            </div>
          </div>
          <div style="font-size: 10px; color: #8E8EA0; margin-top: 4px;">500.1 GB &bull; SATA III</div>
        </div>

        <div style="font-size: 10px; font-weight: 700; color: #8E8EA0; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 8px;">Penyimpanan Eksternal</div>
        <div class="gaming-card" style="padding: 10px; cursor: pointer;" id="disk-item-usb" onclick="selectDiskView('usb')">
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg style="width: 22px; height: 22px;"><use href="#icon-disks"/></svg>
            <div>
              <div style="font-size: 12px; font-weight: 700; color: #FFF;">sdb</div>
              <div style="font-size: 10px; color: #8E8EA0;">SanDisk Ultra Luxe USB 3.2</div>
            </div>
          </div>
          <div style="font-size: 10px; color: #8E8EA0; margin-top: 4px;">64.0 GB &bull; exFAT</div>
        </div>
      </div>

      <!-- Main Disk Details -->
      <div style="flex: 1; padding: 18px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto;">
        <!-- Disk Hero Card -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-acrylic); border-radius: 12px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <div style="font-size: 15px; font-weight: 700; color: #FFF;" id="disk-main-name">DAXOS NVMe 1TB PCIe 5.0 SSD (nvme0n1)</div>
              <div style="font-size: 11px; color: #00D2FF; margin-top: 2px;">Kapasitas Total: 1,000,204,886,016 Bytes (1.00 TB) &bull; Protokol NVMe 2.0</div>
            </div>
            <span style="font-size: 11px; font-weight: 700; color: #30D158; background: rgba(48,209,88,0.15); padding: 4px 10px; border-radius: 6px;" id="disk-smart-badge">SMART: Verified - 100% Sehat</span>
          </div>

          <!-- Partition Visualizer Bar -->
          <div style="margin-top: 14px;">
            <div style="font-size: 11px; color: #8E8EA0; margin-bottom: 6px;">Peta Alokasi Partisi GPT (A/B Atomic Rollback):</div>
            <div style="display: flex; height: 28px; border-radius: 6px; overflow: hidden; border: 1px solid rgba(255,255,255,0.15);">
              <div style="width: 5%; background: #00D2FF; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 700; color: #000;" title="EFI System (512 MB)">EFI</div>
              <div style="width: 15%; background: #0A84FF; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 700; color: #FFF;" title="DAXOS Slot A (32 GB)">Slot A</div>
              <div style="width: 15%; background: #BF5AF2; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: 700; color: #FFF;" title="DAXOS Slot B Rollback (32 GB)">Slot B</div>
              <div style="width: 65%; background: #30D158; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: #000;" title="Data Btrfs (935.5 GB)">Data / Home (Btrfs)</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 10px; color: #8E8EA0; margin-top: 4px;">
              <span>Terpakai: 284.5 GB (28.4%)</span>
              <span>Tersedia: 715.5 GB (71.6%)</span>
            </div>
          </div>
        </div>

        <!-- Telemetry & SMART Attributes -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-acrylic); border-radius: 10px; padding: 12px;">
            <div style="font-size: 11px; font-weight: 700; color: #FFF; margin-bottom: 8px;">Informasi Volume Aktif</div>
            <div style="font-size: 11px; color: #C2C2D6; line-height: 22px;">
              Titik Pasang: <span style="color: #FFF; font-weight: 600;">/sysroot (Slot A - Aktif)</span><br>
              Sistem Berkas: <span style="color: #00D2FF;">Btrfs (Kompresi ZSTD L3)</span><br>
              UUID: <span style="color: #8E8EA0; font-family: monospace;">d4x0-88af-4192-bc12</span><br>
              Status I/O: <span style="color: #30D158;">Baca/Tulis (Read-Write Asynchronous)</span>
            </div>
          </div>

          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-acrylic); border-radius: 10px; padding: 12px;">
            <div style="font-size: 11px; font-weight: 700; color: #FFF; margin-bottom: 8px;">Diagnostik Hardware NVMe SMART</div>
            <div style="font-size: 11px; color: #C2C2D6; line-height: 22px;">
              Suhu Pengontrol: <span style="color: #30D158; font-weight: 600;">38&deg;C (Optimal)</span><br>
              Sisa Umur NAND: <span style="color: #00D2FF; font-weight: 600;">99% (Sangat Baik)</span><br>
              Siklus Daya (Power Cycles): <span style="color: #FFF;">142 kali</span><br>
              Total Terbaca / Tertulis: <span style="color: #8E8EA0;">4.2 TB / 2.8 TB</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: dMedia SPATIAL AUDIO PLAYER (org.daxos.media)
       ======================================================================== -->
  <div class="window" id="win-media" style="top: 75px; left: 240px; width: 840px; height: 550px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-media')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-media')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-media')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-media')">+</div>
      </div>
      <span class="window-title">DAXOS Spatial Audio &bull; HRTF 3D &bull; Latensi 5.8 ms</span>
      <div style="margin-left: auto; display: flex; gap: 8px;">
        <button class="btn btn-primary" id="btn-spatial-toggle" style="font-size: 11px; padding: 4px 12px;" onclick="toggleSpatialAudio()">Spatial ON</button>
      </div>
    </div>
    <div class="window-content" style="padding: 18px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0E0F17;">
      <!-- Hero Now Playing Card -->
      <div style="background: linear-gradient(135deg, rgba(255,55,95,0.15), rgba(191,90,242,0.15)); border: 1px solid rgba(255,55,95,0.3); border-radius: 12px; padding: 16px; display: flex; gap: 18px; align-items: center;">
        <div style="width: 80px; height: 80px; border-radius: 10px; background: linear-gradient(45deg, #FF375F, #0A84FF); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(255,55,95,0.3);">
          <svg style="width: 40px; height: 40px;"><use href="#icon-media"/></svg>
        </div>
        <div style="flex: 1;">
          <div style="font-size: 16px; font-weight: 700; color: #FFF;">Resonance - Symphonic Glass</div>
          <div style="font-size: 12px; color: #00D2FF; margin-top: 2px;">DAXOS Audio Laboratory &bull; 96kHz / 24-bit Lossless ALAC</div>
          <div style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
            <span style="font-size: 10px; color: #8E8EA0;">01:42</span>
            <div style="flex: 1; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden; cursor: pointer;">
              <div style="width: 38%; height: 100%; background: #00D2FF;"></div>
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

      <!-- 10-Band Equalizer & DSP Engine -->
      <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-acrylic); border-radius: 12px; padding: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
          <div style="font-size: 12px; font-weight: 700; color: #FFF;">Equalizer Grafis 10-Band (DSP PipeWire Native)</div>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-secondary active" style="font-size: 10px; padding: 3px 8px;" onclick="setEqPreset('Acoustic')">Acoustic</button>
            <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="setEqPreset('Bass')">Bass Boost</button>
            <button class="btn btn-secondary" style="font-size: 10px; padding: 3px 8px;" onclick="setEqPreset('Studio')">Studio Reference</button>
          </div>
        </div>

        <!-- Slider Sliders -->
        <div style="display: flex; justify-content: space-between; align-items: flex-end; height: 110px; padding: 0 10px;">
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="2" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">32Hz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="4" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">64Hz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="1" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">125Hz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="0" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">250Hz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="-1" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">500Hz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="3" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">1kHz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="5" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">2kHz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="6" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">4kHz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="4" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">8kHz</span>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
            <input type="range" min="-12" max="12" value="3" orient="vertical" style="writing-mode: vertical-lr; height: 80px; accent-color: #00D2FF;">
            <span style="font-size: 9px; color: #8E8EA0;">16kHz</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================
       WINDOW: DaXDrop WIRELESS & AIR-GESTURE SHARING (org.daxos.daxdrop)
       ======================================================================== -->
  <div class="window" id="win-daxdrop" style="top: 70px; left: 220px; width: 840px; height: 560px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-daxdrop')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-daxdrop')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-daxdrop')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-daxdrop')">+</div>
      </div>
      <span class="window-title">DaXDrop AirShare &bull; Wi-Fi Direct &bull; Sensor V4L2</span>
      <div style="margin-left: auto; display: flex; gap: 8px;">
        <button class="btn btn-primary" id="btn-airgrab-toggle" style="font-size: 11px; padding: 4px 12px;" onclick="toggleAirGrabPose()">Simulasi Kepal Tangan</button>
      </div>
    </div>
    <div class="window-content" style="padding: 18px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0A0C14;">
      <!-- Sensor & Air-Gesture Status -->
      <div style="background: linear-gradient(135deg, rgba(0,210,255,0.15), rgba(48,209,88,0.15)); border: 1px solid rgba(0,210,255,0.3); border-radius: 12px; padding: 14px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <svg style="width: 28px; height: 28px;"><use href="#icon-daxdrop"/></svg>
          <div>
            <div style="font-size: 13px; font-weight: 700; color: #FFF;">Air-Gesture Vision Sensor (/dev/video0 Hardware V4L2)</div>
            <div style="font-size: 11px; color: #00D2FF; margin-top: 2px;">Enkripsi ChaCha20-Poly1305 &bull; Pelacakan 60 FPS Real-Time</div>
          </div>
        </div>
        <span style="font-size: 11px; font-weight: 700; color: #30D158; background: rgba(48,209,88,0.2); padding: 4px 10px; border-radius: 6px;" id="daxdrop-pose-badge">Pose: Telapak Terbuka (Ready)</span>
      </div>

      <!-- Nearby Peers Radar -->
      <div style="font-size: 12px; font-weight: 700; color: #FFF;">Perangkat DAXOS Terdekat yang Terdeteksi (P2P Wi-Fi Direct):</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
        <div class="gaming-card active" style="padding: 14px; text-align: center; cursor: pointer; border-color: #00D2FF;" id="peer-phone" onclick="selectPeer('phone')">
          <div style="font-size: 24px; margin-bottom: 4px;">&#9742;</div>
          <div style="font-size: 12px; font-weight: 700; color: #FFF;">Rhino Phone Ultra</div>
          <div style="font-size: 10px; color: #00D2FF;">RSSI -38 dBm (Sangat Kuat)</div>
          <span style="display: inline-block; font-size: 9px; color: #30D158; background: rgba(48,209,88,0.2); padding: 2px 6px; border-radius: 4px; margin-top: 6px;">Terhubung P2P</span>
        </div>

        <div class="gaming-card" style="padding: 14px; text-align: center; cursor: pointer;" id="peer-tablet" onclick="selectPeer('tablet')">
          <div style="font-size: 24px; margin-bottom: 4px;">&#9638;</div>
          <div style="font-size: 12px; font-weight: 700; color: #FFF;">DAXOS MatePad Pro</div>
          <div style="font-size: 10px; color: #8E8EA0;">RSSI -45 dBm</div>
          <span style="display: inline-block; font-size: 9px; color: #0A84FF; background: rgba(10,132,255,0.2); padding: 2px 6px; border-radius: 4px; margin-top: 6px;">Siap Transfer</span>
        </div>

        <div class="gaming-card" style="padding: 14px; text-align: center; cursor: pointer;" id="peer-station" onclick="selectPeer('station')">
          <div style="font-size: 24px; margin-bottom: 4px;">&#9641;</div>
          <div style="font-size: 12px; font-weight: 700; color: #FFF;">Studio Station Server</div>
          <div style="font-size: 10px; color: #8E8EA0;">RSSI -28 dBm</div>
          <span style="display: inline-block; font-size: 9px; color: #0A84FF; background: rgba(10,132,255,0.2); padding: 2px 6px; border-radius: 4px; margin-top: 6px;">Siap Transfer</span>
        </div>
      </div>

      <!-- Drag & Drop Air Zone -->
      <div style="border: 2px dashed rgba(0,210,255,0.4); border-radius: 12px; padding: 24px; text-align: center; background: rgba(0,210,255,0.02); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;">
        <svg style="width: 36px; height: 36px;"><use href="#icon-daxdrop"/></svg>
        <div style="font-size: 13px; font-weight: 700; color: #FFF;">Seret berkas ke sini atau kepalkan tangan di depan kamera</div>
        <div style="font-size: 11px; color: #8E8EA0;">Gestur "Kepal Tangan" (Fist Clench) akan otomatis mengikat berkas aktif dan mengirimkannya ke perangkat terpilih</div>
        <button class="btn btn-primary" style="margin-top: 8px; font-size: 11px; padding: 6px 18px;" onclick="simulateFileTransfer()">Kirim Berkas Sampel (Test Share)</button>
        <div style="width: 80%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; margin-top: 8px; display: none;" id="daxdrop-progress-bar">
          <div style="width: 0%; height: 100%; background: #30D158; transition: width 0.3s ease;" id="daxdrop-progress-inner"></div>
        </div>
      </div>
    </div>
  </div>
'''

    # Insert windows before BOTTOM ACRYLIC DOCK
    dock_marker = '  <!-- ========================================================================\n       BOTTOM ACRYLIC DOCK'
    if 'id="win-editor"' not in html:
        html = html.replace(dock_marker, windows_html + '\n' + dock_marker)

    # 3. Add Dock Icons
    new_dock_items = '''      <div class="dock-item" onclick="openApp('win-editor', 'dEdit')">
        <div class="dock-tooltip">dEdit Notes &amp; Code</div>
        <svg class="dock-icon-svg"><use href="#icon-editor"/></svg>
        <div class="dock-dot" id="dot-win-editor"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-disks', 'Disk Utility')">
        <div class="dock-tooltip">Disk Utility</div>
        <svg class="dock-icon-svg"><use href="#icon-disks"/></svg>
        <div class="dock-dot" id="dot-win-disks"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-media', 'Spatial Audio')">
        <div class="dock-tooltip">Spatial Audio</div>
        <svg class="dock-icon-svg"><use href="#icon-media"/></svg>
        <div class="dock-dot" id="dot-win-media"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-daxdrop', 'DaXDrop')">
        <div class="dock-tooltip">DaXDrop AirShare</div>
        <svg class="dock-icon-svg"><use href="#icon-daxdrop"/></svg>
        <div class="dock-dot" id="dot-win-daxdrop"></div>
      </div>

      <div class="dock-item" onclick="openApp('win-activity-monitor', 'Activity Monitor')">
        <div class="dock-tooltip">Activity Monitor</div>
        <svg class="dock-icon-svg"><use href="#icon-monitor"/></svg>
        <div class="dock-dot" id="dot-win-activity-monitor"></div>
      </div>
'''
    if "openApp('win-editor', 'dEdit')" not in html:
        # Insert before System Settings in dock
        settings_dock_marker = '      <div class="dock-item" onclick="openApp(\'win-settings\', \'System Settings\')">'
        html = html.replace(settings_dock_marker, new_dock_items + '\n' + settings_dock_marker)

    # 4. Update Launchpad Items
    if 'launchAppFromLaunchpad(\'win-editor\'' not in html:
        old_editor_lp = '''        <div class="launchpad-item" data-category="productivity" data-name="Text Editor dedit Teks Catatan Dokumen" onclick="openApp('win-terminal', 'Terminal'); runTerminal('dedit README.md'); toggleLaunchpad();">
          <svg class="launchpad-item-icon"><use href="#icon-ide"/></svg>
          <div class="launchpad-item-title">Visual Text Editor</div>
          <div class="launchpad-item-desc">Editor Teks Visual Terminal</div>
        </div>'''
        new_editor_lp = '''        <div class="launchpad-item" data-category="productivity" data-name="dEdit Text Editor Teks Catatan Dokumen Code" onclick="launchAppFromLaunchpad('win-editor', 'dEdit')">
          <svg class="launchpad-item-icon"><use href="#icon-editor"/></svg>
          <div class="launchpad-item-title">dEdit Editor</div>
          <div class="launchpad-item-desc">Editor Teks &amp; Kode Acrylic 32px</div>
        </div>

        <div class="launchpad-item" data-category="system" data-name="Disk Utility ddisk Partisi Storage GPT Btrfs SMART" onclick="launchAppFromLaunchpad('win-disks', 'Disk Utility')">
          <svg class="launchpad-item-icon"><use href="#icon-disks"/></svg>
          <div class="launchpad-item-title">Disk Utility</div>
          <div class="launchpad-item-desc">Manajer Partisi GPT &amp; SMART</div>
        </div>

        <div class="launchpad-item" data-category="media" data-name="Spatial Audio Musik Lagu Equalizer HRTF Sound" onclick="launchAppFromLaunchpad('win-media', 'Spatial Audio')">
          <svg class="launchpad-item-icon"><use href="#icon-media"/></svg>
          <div class="launchpad-item-title">Spatial Audio</div>
          <div class="launchpad-item-desc">Musik HRTF 3D &amp; Equalizer 10-Band</div>
        </div>'''
        html = html.replace(old_editor_lp, new_editor_lp)

    # Update DaXDrop in launchpad
    if 'launchAppFromLaunchpad(\'win-daxdrop\'' not in html:
        old_daxdrop_lp = 'onclick="openApp(\'win-settings\', \'System Settings\'); switchSettingsTab(\'daxdrop\'); toggleLaunchpad();"'
        new_daxdrop_lp = 'onclick="launchAppFromLaunchpad(\'win-daxdrop\', \'DaXDrop\')"'
        html = html.replace(old_daxdrop_lp, new_daxdrop_lp)

    # 5. Add JavaScript Handlers
    js_handlers = '''
    // =========================================================================
    // NEW APP INTERACTIVE HANDLERS (dEdit, dDisk, dMedia, DaXDrop)
    // =========================================================================
    function saveDeditDoc() {
      const title = document.getElementById('dedit-title');
      if (title) title.innerHTML = "dEdit Pro &bull; Untitled.rs [Tersimpan ke Btrfs]";
      alert("Dokumen berhasil disimpan ke /home/kangpcode/Untitled.rs (Btrfs Copy-on-Write).");
    }

    function insertDeditSnippet() {
      const ta = document.getElementById('dedit-textarea');
      if (ta) {
        ta.value += "\\n// DAXOS DreXUI Vector Component\\n@State var isAcrylic: Bool = true;\\n";
        updateDeditStats();
      }
    }

    function switchEditorTab(idx) {
      for (let i = 1; i <= 3; i++) {
        const tab = document.getElementById('tab-editor-' + i);
        if (tab) {
          if (i === idx) {
            tab.classList.add('active');
            tab.style.borderBottom = "2px solid #00D2FF";
            tab.style.color = "#FFF";
          } else {
            tab.classList.remove('active');
            tab.style.borderBottom = "none";
            tab.style.color = "#8E8EA0";
          }
        }
      }
      const title = document.getElementById('dedit-title');
      const ta = document.getElementById('dedit-textarea');
      if (idx === 1) {
        if (title) title.innerHTML = "dEdit Pro &bull; Untitled.rs [UTF-8]";
        if (ta) ta.value = `fn main() -> Result<(), Box<dyn std::error::Error>> {\\n    println!("[DAXOS] System Initialized with Acrylic Wayland Compositor");\\n    Ok(())\\n}`;
      } else if (idx === 2) {
        if (title) title.innerHTML = "dEdit Pro &bull; main.surf [Surflang 1.0]";
        if (ta) ta.value = `module daxos.editor;\\n\\ncomponent EditorApp: Component {\\n    @State var acrylicBlur: Float = 32.0;\\n    func body() -> ViewNode {\\n        return Card { Text("Hello from Surflang!") };\\n    }\\n}`;
      } else if (idx === 3) {
        if (title) title.innerHTML = "dEdit Pro &bull; config.toml [Config]";
        if (ta) ta.value = `[daxos.system]\\nversion = "1.10.2026"\\ncompositor = "drex-wayland"\\nrefresh_rate = 120\\npower_profile = "BalancedFlow"\\n`;
      }
      updateDeditStats();
    }

    function updateDeditStats() {
      const ta = document.getElementById('dedit-textarea');
      const stats = document.getElementById('dedit-stats');
      if (!ta || !stats) return;
      const text = ta.value;
      const lines = text.split('\\n').length;
      const chars = text.length;
      const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
      stats.innerHTML = `Baris: ${lines} &bull; Karakter: ${chars} &bull; Kata: ${words}`;

      const lineNums = document.getElementById('dedit-linenums');
      if (lineNums) {
        let numsHtml = "";
        for (let i = 1; i <= Math.max(lines, 15); i++) {
          numsHtml += i + "<br>";
        }
        lineNums.innerHTML = numsHtml;
      }
    }

    function runDiskFirstAid() {
      const badge = document.getElementById('disk-smart-badge');
      if (badge) {
        badge.innerHTML = "SMART: Memeriksa Sektor...";
        badge.style.color = "#FF9F0A";
        setTimeout(() => {
          badge.innerHTML = "SMART: Self-Test Sukses (0 Sektor Rusak)";
          badge.style.color = "#30D158";
          alert("Disk First Aid Selesai:\\n- Tabel Partisi GPT: Valid\\n- Superblock Btrfs: Konsisten\\n- TRIM & Wear-Leveling: 100% Sehat");
        }, 800);
      }
    }

    function selectDiskView(diskType) {
      ['nvme', 'sata', 'usb'].forEach(t => {
        const item = document.getElementById('disk-item-' + t);
        if (item) {
          if (t === diskType) {
            item.style.borderColor = "#00D2FF";
            item.style.background = "rgba(0,210,255,0.08)";
          } else {
            item.style.borderColor = "var(--border-acrylic)";
            item.style.background = "transparent";
          }
        }
      });
      const name = document.getElementById('disk-main-name');
      if (name) {
        if (diskType === 'nvme') name.innerText = "DAXOS NVMe 1TB PCIe 5.0 SSD (nvme0n1)";
        else if (diskType === 'sata') name.innerText = "Kingston Fury 500GB SSD (sda)";
        else if (diskType === 'usb') name.innerText = "SanDisk Ultra Luxe USB 3.2 (sdb)";
      }
    }

    function toggleSpatialAudio() {
      const btn = document.getElementById('btn-spatial-toggle');
      if (!btn) return;
      if (btn.innerText.includes("ON")) {
        btn.innerText = "Spatial OFF";
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
      } else {
        btn.innerText = "Spatial ON";
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
      }
    }

    function toggleMediaPlay() {
      const btn = document.getElementById('btn-media-play');
      if (!btn) return;
      if (btn.innerHTML === "&#9654;" || btn.innerText === "▶") {
        btn.innerHTML = "&#10074;&#10074;"; // pause
      } else {
        btn.innerHTML = "&#9654;"; // play
      }
    }

    function setEqPreset(preset) {
      alert("Preset Equalizer beralih ke: " + preset + " (DSP PipeWire diaktifkan).");
    }

    function toggleAirGrabPose() {
      const badge = document.getElementById('daxdrop-pose-badge');
      const btn = document.getElementById('btn-airgrab-toggle');
      if (!badge || !btn) return;
      if (badge.innerText.includes("Terbuka")) {
        badge.innerText = "Pose: KEPAL TANGAN (Air-Grab Mengunci)";
        badge.style.color = "#00D2FF";
        badge.style.background = "rgba(0,210,255,0.2)";
        btn.innerText = "Lepas Kepalan";
      } else {
        badge.innerText = "Pose: Telapak Terbuka (Ready)";
        badge.style.color = "#30D158";
        badge.style.background = "rgba(48,209,88,0.2)";
        btn.innerText = "Simulasi Kepal Tangan";
      }
    }

    function selectPeer(peerId) {
      ['phone', 'tablet', 'station'].forEach(p => {
        const card = document.getElementById('peer-' + p);
        if (card) {
          if (p === peerId) {
            card.style.borderColor = "#00D2FF";
            card.style.background = "rgba(0,210,255,0.08)";
          } else {
            card.style.borderColor = "var(--border-acrylic)";
            card.style.background = "rgba(255,255,255,0.02)";
          }
        }
      });
    }

    function simulateFileTransfer() {
      const pbar = document.getElementById('daxdrop-progress-bar');
      const inner = document.getElementById('daxdrop-progress-inner');
      if (!pbar || !inner) return;
      pbar.style.display = 'block';
      inner.style.width = '0%';
      let progress = 0;
      const interval = setInterval(() => {
        progress += 25;
        inner.style.width = progress + '%';
        if (progress >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            alert("Transfer Sukses! Berkas terkirim dengan enkripsi TLS 1.3 / ChaCha20-Poly1305 (Kecepatan: 142 MB/s via Wi-Fi Direct).");
            pbar.style.display = 'none';
          }, 300);
        }
      }, 200);
    }
'''
    if 'function saveDeditDoc()' not in html:
        html = html.replace('</script>\n</body>', js_handlers + '\n</script>\n</body>')

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Desktop preview updated successfully with all 4 new applications!")

if __name__ == "__main__":
    integrate()
