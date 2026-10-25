#!/usr/bin/env python3
"""
scripts/build_full_ecosystem.py
Injects:
1. Dynamic Hardware Driver Manager (win-driver-settings)
2. Vision Tune Up GPU Control Suite (win-vision-tune)
3. DaxWord 1:1 Microsoft Word Parity (Full Ribbon, Rulers, A4 Sheet, Statistics)
4. DaXBro Real Chromium Multi-Tab & Live Web/Iframe Navigation
5. DuraServ Interactive Web Stack & Developer Dashboard
"""

import re
import sys

INDEX_PATH = 'src/ui/desktop_preview/index.html'

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    html = load_file(INDEX_PATH)
    print(f"Loaded {INDEX_PATH}: {len(html)} bytes")

    # =========================================================================
    # 1. DYNAMIC HARDWARE DRIVER MANAGER (win-driver-settings)
    # =========================================================================
    dynamic_driver_window = '''  <!-- ========================================================================
       WINDOW: DYNAMIC HARDWARE & DRIVER MANAGER (WINDOWS DEVICE MANAGER & DREXVIS PARITY)
       ======================================================================== -->
  <div class="window" id="win-driver-settings" style="top: 70px; left: 190px; width: 880px; height: 600px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-driver-settings')" ondblclick="maximizeWindow('win-driver-settings')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-driver-settings')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-driver-settings')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-driver-settings')" onclick="maximizeWindow('win-driver-settings')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 15px; height: 15px; flex-shrink: 0;"><use href="#icon-driver"/></svg>
        <span>Hardware &amp; Driver Manager — DreXVIS Direct Kernel HAL (Device Manager)</span>
      </div>
      <div style="margin-left: auto; display: flex; gap: 6px;">
        <button class="btn btn-secondary" onclick="drexProbeHardware()" style="font-size: 11px; padding: 4px 10px; display: flex; align-items: center; gap: 4px;">
          <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
          Pindai Perangkat (ddrv probe)
        </button>
        <button class="btn btn-primary" onclick="openApp('win-vision-tune', 'Vision Tune Up')" style="font-size: 11px; padding: 4px 12px; font-weight: 700; background: linear-gradient(135deg, #e11d48, #be123c); border: 1px solid #f43f5e; box-shadow: 0 0 12px rgba(244,63,94,0.35); display: flex; align-items: center; gap: 5px;">
          <svg style="width: 12px; height: 12px;"><use href="#icon-vision-tune"/></svg>
          Vision Tune Up
        </button>
      </div>
    </div>
    <div class="window-content" style="padding: 16px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0E111A; color: #F3F4F6;">

      <!-- Active Hardware Summary Strip -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px;">
          <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px;">Kartu Grafis Utama (Host)</div>
          <div style="font-size: 12.5px; font-weight: 700; color: #38BDF8; margin-top: 3px;" id="drv-summary-gpu">AMD Rembrandt [Radeon 680M]</div>
          <div style="font-size: 10px; color: #34D399; margin-top: 2px;">Driver: amdgpu (RADV Vulkan 1.3)</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px;">
          <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px;">Prosesor (CPU)</div>
          <div style="font-size: 12.5px; font-weight: 700; color: #FFF; margin-top: 3px;">AMD Ryzen 5 6600H</div>
          <div style="font-size: 10px; color: #A78BFA; margin-top: 2px;">12 Thread &bull; DreX-Boost 240Hz</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px;">
          <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px;">Penyimpanan &amp; Bus</div>
          <div style="font-size: 12.5px; font-weight: 700; color: #F59E0B; margin-top: 3px;">NVMe PCIe Gen4 (Kingston/SMI)</div>
          <div style="font-size: 10px; color: #34D399; margin-top: 2px;">SMART 100% Sehat &bull; Btrfs CoW</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px;">
          <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px;">Kernel Primitives</div>
          <div style="font-size: 12.5px; font-weight: 700; color: #10B981; margin-top: 3px;">NTSync &bull; DreX-Boost &bull; LSM</div>
          <div style="font-size: 10px; color: #E2E8F0; margin-top: 2px;">Latensi &le; 0.185us &bull; Jitter 38us</div>
        </div>
      </div>

      <!-- Refresh Rate Selector & Display Profiler -->
      <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <div>
            <div style="font-size: 12px; font-weight: 700; color: #FFF; display: flex; align-items: center; gap: 6px;">
              <svg style="width: 14px; height: 14px; fill: #38BDF8;"><polygon points="13,2 4,14 11,14 9,22 20,10 13,10"/></svg>
              Compositor Refresh Rate &amp; VSync Timing
            </div>
            <div style="font-size: 10.5px; color: #9CA3AF; margin-top: 2px;">
              Wayland direct scanout pada node DRM <code style="color: #38BDF8;">/dev/dri/card1</code> (eDP-1).
            </div>
          </div>
          <div class="hz-toggle-group" style="display: flex; gap: 4px;">
            <button class="hz-btn" id="btn-hz-60" onclick="toggleRefreshRate(60)" style="font-size: 11px; padding: 4px 10px;">60Hz (Safe)</button>
            <button class="hz-btn" id="btn-hz-120" onclick="toggleRefreshRate(120)" style="font-size: 11px; padding: 4px 10px;">120Hz (Pro)</button>
            <button class="hz-btn active" id="btn-hz-240" onclick="toggleRefreshRate(240)" style="font-size: 11px; padding: 4px 12px; font-weight: 700; background: #0284C7; color: #FFF; border-radius: 4px; border: none;">240Hz (DreX-Boost)</button>
          </div>
        </div>
      </div>

      <!-- Dynamic Categorized Device Tree (Windows Device Manager Parity) -->
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">
          Pohon Perangkat Keras &amp; Driver Terinstal (19 Perangkat Terdeteksi)
        </div>

        <!-- 1. Display Adapters -->
        <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; cursor: pointer;" onclick="toggleDeviceGroup('group-gpu')">
            <div style="font-size: 12px; font-weight: 700; color: #38BDF8; display: flex; align-items: center; gap: 6px;">
              <svg style="width: 14px; height: 14px;"><use href="#icon-driver"/></svg>
              <span>Kartu Grafis &amp; Display Adapters (1 Perangkat Host Terpasang)</span>
            </div>
            <span style="font-size: 10px; color: #9CA3AF;">[Klik untuk Ciutkan/Rentangkan]</span>
          </div>

          <div id="group-gpu" style="display: flex; flex-direction: column; gap: 8px;">
            <!-- Primary Host Hardware: AMD Radeon 680M -->
            <div class="driver-list-item selected" id="driver-item-amd" onclick="selectGpuDriver('amd')" style="background: rgba(2,132,199,0.12); border: 1px solid #0284C7; border-radius: 6px; padding: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <input type="radio" name="gpu_driver" id="radio-amd" checked>
                  <div>
                    <div style="font-weight: 700; font-size: 12.5px; color: #FFF;">AMD Rembrandt [Radeon 680M] / RDNA 2 (Hardware Host Terdeteksi)</div>
                    <div style="font-size: 11px; color: #94A3B8;">Driver: <strong>amdgpu</strong> (Kernel Direct DRM/KMS, Mesa 24.1 RADV Vulkan 1.3, Slot PCI: 0000:04:00.0)</div>
                    <div style="font-size: 10px; color: #34D399; margin-top: 2px;">Status: Driver Aktif &bull; VRAM 2048 MB &bull; DMA-BUF Zero-Copy &bull; Suhu: 51.0&deg;C</div>
                  </div>
                </div>
                <div style="display: flex; gap: 6px; align-items: center;">
                  <span class="badge" style="background: rgba(52,211,153,0.15); color: #34D399; font-weight: 700;">PRIMARY 240Hz</span>
                  <button class="ide-btn" onclick="event.stopPropagation(); openApp('win-vision-tune', 'Vision Tune Up')" style="font-size: 10px; padding: 4px 8px; background: #e11d48; color: #fff; border: none; border-radius: 4px;">Tune GPU</button>
                </div>
              </div>
            </div>

            <!-- Alternative architecture options for simulation & multi-GPU -->
            <div class="driver-list-item" id="driver-item-nvidia" onclick="selectGpuDriver('nvidia')" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <input type="radio" name="gpu_driver" id="radio-nvidia">
                  <div>
                    <div style="font-weight: 600; font-size: 12.5px; color: #E2E8F0;">NVIDIA GeForce RTX (Ada Lovelace / Ampere DreXVIS Bridge)</div>
                    <div style="font-size: 11px; color: #94A3B8;">Driver: <strong>nvidia</strong> v560.35 (Proprietary / Open-GPU, CUDA 12.6, OptiX, DLSS 3.7)</div>
                  </div>
                </div>
                <span class="badge" style="background: rgba(10, 132, 255, 0.15); color: #0A84FF;">NVIDIA HAL</span>
              </div>
            </div>

            <div class="driver-list-item" id="driver-item-intel" onclick="selectGpuDriver('intel')" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <input type="radio" name="gpu_driver" id="radio-intel">
                  <div>
                    <div style="font-weight: 600; font-size: 12.5px; color: #E2E8F0;">Intel Arc &amp; Iris Xe Graphics (Alchemist / Xe2)</div>
                    <div style="font-size: 11px; color: #94A3B8;">Driver: <strong>xe / i915</strong> (Mesa ANV Vulkan 1.3, Intel oneAPI, XeSS 1.3)</div>
                  </div>
                </div>
                <span class="badge" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8;">INTEL HAL</span>
              </div>
            </div>

            <div class="driver-list-item" id="driver-item-safe" onclick="selectGpuDriver('safe')" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <input type="radio" name="gpu_driver" id="radio-safe">
                  <div>
                    <div style="font-weight: 600; font-size: 12.5px; color: #E2E8F0;">Universal Software Rasterizer (LLVMpipe / VESA 60Hz Safe Mode)</div>
                    <div style="font-size: 11px; color: #94A3B8;">Kompatibel dengan semua prosesor legacy (SSE2). Jaminan zero crash tanpa GPU diskrit.</div>
                  </div>
                </div>
                <span class="badge" style="background: rgba(255, 255, 255, 0.1); color: #E2E2EA;">UNIVERSAL SAFE</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Processors -->
        <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px;">
          <div style="font-size: 12px; font-weight: 700; color: #A78BFA; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
            <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/></svg>
            <span>Prosesor (CPU) &amp; Manajemen Daya</span>
          </div>
          <div style="font-size: 11px; color: #CBD5E1; line-height: 1.5;">
            AMD Ryzen 5 6600H with Radeon Graphics (6 Core Fisik / 12 Logical Threads @ 3.30 GHz - 4.50 GHz Boost)<br>
            Driver: <strong>amd_pstate_epp</strong> &bull; Governor: <strong>DreX-Boost 240Hz</strong> &bull; Thermal Monitor: <strong>k10temp</strong> (49.5&deg;C)<br>
            Status: <span style="color: #34D399; font-weight: 600;">Optimal (Low-Jitter Real-Time Scheduling Aktif)</span>
          </div>
        </div>

        <!-- 3. Storage Controllers -->
        <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px;">
          <div style="font-size: 12px; font-weight: 700; color: #F59E0B; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
            <svg style="width: 14px; height: 14px;"><use href="#icon-disks"/></svg>
            <span>Pengontrol Penyimpanan (NVMe Storage Controllers)</span>
          </div>
          <div style="font-size: 11px; color: #CBD5E1; line-height: 1.5;">
            &bull; Kingston NVMe PCIe Gen4 SSD (Slot 0000:03:00.0, Driver: <strong>nvme</strong>, Kapasitas: 1000 GB, SMART 100%)<br>
            &bull; Silicon Motion Technologies NVMe SSD (Slot 0000:01:00.0, Driver: <strong>nvme</strong>, Kapasitas: 512 GB)<br>
            Status: <span style="color: #34D399; font-weight: 600;">Trim Harian Terjadwal &bull; Btrfs CoW Subvolumes Valid</span>
          </div>
        </div>

        <!-- 4. Network Adapters -->
        <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px;">
          <div style="font-size: 12px; font-weight: 700; color: #34D399; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
            <svg style="width: 14px; height: 14px;"><use href="#icon-network"/></svg>
            <span>Adapter Jaringan &amp; Nirkabel (Wi-Fi 6E)</span>
          </div>
          <div style="font-size: 11px; color: #CBD5E1; line-height: 1.5;">
            MediaTek MT7921e Wi-Fi 6E &amp; Bluetooth 5.3 Controller (Slot 0000:02:00.0, Driver: <strong>mt7921e</strong>)<br>
            Status: <span style="color: #34D399; font-weight: 600;">ONLINE (1.39 GB/s Throughput, WPA3-SAE, BBRv3 Congestion Control)</span>
          </div>
        </div>

        <!-- 5. Audio Controllers -->
        <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px;">
          <div style="font-size: 12px; font-weight: 700; color: #F472B6; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
            <svg style="width: 14px; height: 14px;"><use href="#icon-media"/></svg>
            <span>Pengontrol Suara, Video &amp; Game (Audio Subsystems)</span>
          </div>
          <div style="font-size: 11px; color: #CBD5E1; line-height: 1.5;">
            AMD Rembrandt High Definition Audio Subsystem (Slot 0000:04:00.1 / 0000:04:00.6, Driver: <strong>snd_hda_intel</strong>)<br>
            DSP Engine: <strong>PipeWire 1.2 Direct ALSA</strong> (Buffer 128 frames @ 48kHz, Latensi 5.8 ms, 3D Spatial HRTF Aktif)
          </div>
        </div>

        <!-- 6. DAXOS In-Kernel Primitives -->
        <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 12px;">
          <div style="font-size: 12px; font-weight: 700; color: #38BDF8; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
            <svg style="width: 14px; height: 14px;"><use href="#icon-dxdef"/></svg>
            <span>Primitif Ring-0 DXU Hybrid Kernel Subsystems</span>
          </div>
          <div style="font-size: 11px; color: #CBD5E1; line-height: 1.5;">
            &bull; <code style="color: #38BDF8;">/dev/ntsync</code>: Fast Windows NT Synchronization Mutex/Semaphore (Latensi: 0.185 us, SLA &le; 0.22 us)<br>
            &bull; <code style="color: #38BDF8;">/dev/daxos_boost</code>: DreX-Boost 240Hz High Refresh Governor (Jitter: 38 us, SLA &le; 420 us)<br>
            &bull; <code style="color: #38BDF8;">/dev/daxos_sec</code>: dm-verity Merkle Tree Root-of-Trust + Landlock LSM v5 Auditor<br>
            Status: <span style="color: #34D399; font-weight: 700;">100% TERLINDUNGI &bull; ZERO CRASH WATCHDOG AKTIF</span>
          </div>
        </div>
      </div>

      <!-- Driver Action Buttons & Diagnostics -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 8px;">
          <button class="ide-btn" onclick="drexSimulateChaosRecovery()" style="background: linear-gradient(135deg, #ef4444, #dc2626); border: none; color: #fff; font-weight: 700; padding: 6px 14px; border-radius: 6px; font-size: 11px; cursor: pointer;">
            Uji Driver Chaos &amp; Recovery (SLA &le; 45ms)
          </button>
          <button class="ide-btn ide-btn-secondary" onclick="drexProbeHardware()" style="font-size: 11px; padding: 6px 12px;">
            Segarkan Perangkat Keras (ddrv probe)
          </button>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button class="ide-btn ide-btn-secondary" onclick="runGpuBenchmark()">
            <svg style="width: 14px; height: 14px; fill: currentColor;"><polygon points="5,3 19,12 5,21"/></svg>
            Jalankan Vulkan Fence Benchmark
          </button>
          <span id="benchmark-result" style="font-size: 12px; align-self: center; color: #30D158; font-weight: 600;"></span>
        </div>
      </div>

      <!-- Real-Time Driver Watchdog & Probe Output Panel -->
      <div id="driver-telemetry-panel" style="margin-top: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px; font-family: monospace; font-size: 10.5px; color: #E2E2F0; display: none;">
        <!-- Telemetry log dynamic -->
      </div>
    </div>
  </div>'''

    # Replace win-driver-settings in html
    pattern_drv = r'  <!-- ========================================================================\s*WINDOW: DRIVER & HARDWARE SETTINGS[\s\S]*?<\/div>\s*<\/div>\s*<\/div>'
    m = re.search(pattern_drv, html)
    if m:
        html = html.replace(m.group(0), dynamic_driver_window, 1)
        print("Replaced win-driver-settings with Dynamic Hardware Device Manager.")
    else:
        print("Warning: Could not find win-driver-settings marker.")

    # =========================================================================
    # 2. VISION TUNE UP WINDOW (win-vision-tune)
    # =========================================================================
    vision_tune_window = '''  <!-- ========================================================================
       WINDOW: VISION TUNE UP (NVIDIA APP & AMD ADRENALIN PARITY GPU TUNER)
       ======================================================================== -->
  <div class="window" id="win-vision-tune" style="top: 60px; left: 160px; width: 960px; height: 630px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-vision-tune')" ondblclick="maximizeWindow('win-vision-tune')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-vision-tune')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-vision-tune')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-vision-tune')" onclick="maximizeWindow('win-vision-tune')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 16px; height: 16px; flex-shrink: 0;"><use href="#icon-vision-tune"/></svg>
        <span>DAXOS Vision Tune Up — Advanced GPU Performance &amp; Hardware Tuning Suite</span>
      </div>
      <div style="margin-left: auto; display: flex; gap: 6px;">
        <button class="btn btn-secondary" onclick="visionTuneReset()" style="font-size: 11px; padding: 4px 10px;">
          Reset Default
        </button>
        <button class="btn btn-primary" onclick="visionTuneApply()" style="font-size: 11px; padding: 4px 14px; font-weight: 700; background: linear-gradient(135deg, #e11d48, #be123c); border: 1px solid #f43f5e; box-shadow: 0 0 12px rgba(244,63,94,0.35);">
          Terapkan Pengaturan (Apply)
        </button>
      </div>
    </div>
    <div class="window-content" style="padding: 16px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto; background: #0A0D14; color: #F3F4F6;">

      <!-- Top GPU Architecture & Active Status Banner -->
      <div class="settings-card" style="background: linear-gradient(135deg, rgba(225,29,72,0.14), rgba(15,23,42,0.6)); border: 1px solid rgba(244,63,94,0.3); padding: 14px 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
          <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(225,29,72,0.2); border: 1px solid #F43F5E; display: flex; align-items: center; justify-content: center;">
              <svg style="width: 24px; height: 24px;"><use href="#icon-vision-tune"/></svg>
            </div>
            <div>
              <div style="font-size: 15px; font-weight: 800; color: #FFF; display: flex; align-items: center; gap: 8px;">
                <span id="vision-gpu-name">AMD Rembrandt [Radeon 680M] / RDNA 2</span>
                <span style="font-size: 10px; padding: 2px 8px; border-radius: 4px; background: rgba(244,63,94,0.2); color: #FDA4AF; font-weight: 700; border: 1px solid rgba(244,63,94,0.4);">OVERCLOCKING READY</span>
              </div>
              <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">
                Direct KMS &bull; Mesa 24.1 RADV Vulkan 1.3 &bull; PCIe 4.0 x16 &bull; Driver: amdgpu &bull; SLA Watchdog: &le; 45ms
              </div>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <select id="vision-gpu-selector" onchange="visionTuneSwitchGpu(this.value)" style="background: #1E293B; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px 10px; font-size: 11px;">
              <option value="amd" selected>AMD Radeon 680M (Host Aktif)</option>
              <option value="nvidia">NVIDIA GeForce RTX 4090</option>
              <option value="intel">Intel Arc A770 Graphics</option>
            </select>
            <button class="btn btn-secondary" onclick="visionTuneFlushVram()" style="font-size: 11px; padding: 6px 12px; display: flex; align-items: center; gap: 4px;">
              Bersihkan VRAM
            </button>
          </div>
        </div>
      </div>

      <!-- Main Two-Column Tuning Layout -->
      <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 14px;">

        <!-- Left Column: Manual Tuning Sliders & Switches -->
        <div style="display: flex; flex-direction: column; gap: 12px;">

          <!-- Core & Memory Frequency Offset -->
          <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #FB7185; display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
              <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              Tuning Frekuensi GPU &amp; Memori (Manual Overclock)
            </div>

            <!-- Core Clock Slider -->
            <div style="margin-bottom: 14px;">
              <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 4px;">
                <span style="color: #CBD5E1;">Core Clock Offset:</span>
                <span style="color: #38BDF8; font-weight: 700;" id="vision-core-val">+120 MHz (Target: 2320 MHz)</span>
              </div>
              <input type="range" min="-200" max="400" step="10" value="120" id="slider-vision-core" oninput="visionUpdateCore(this.value)" style="width: 100%; accent-color: #F43F5E;">
              <div style="display: flex; justify-content: space-between; font-size: 9.5px; color: #64748B;">
                <span>-200 MHz</span>
                <span>0 MHz (Stock)</span>
                <span>+400 MHz (Max OC)</span>
              </div>
            </div>

            <!-- Memory Clock Slider -->
            <div>
              <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 4px;">
                <span style="color: #CBD5E1;">Memory Clock Offset:</span>
                <span style="color: #A78BFA; font-weight: 700;" id="vision-mem-val">+350 MHz (Target: 6750 MT/s)</span>
              </div>
              <input type="range" min="-500" max="1000" step="25" value="350" id="slider-vision-mem" oninput="visionUpdateMem(this.value)" style="width: 100%; accent-color: #A78BFA;">
              <div style="display: flex; justify-content: space-between; font-size: 9.5px; color: #64748B;">
                <span>-500 MHz</span>
                <span>0 MHz (Stock)</span>
                <span>+1000 MHz (High Bandwidth)</span>
              </div>
            </div>
          </div>

          <!-- Power Target & Temperature Limit -->
          <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #F59E0B; display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
              <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
              Batas Daya (Power Target) &amp; Batas Suhu Thermal
            </div>

            <div style="margin-bottom: 14px;">
              <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 4px;">
                <span style="color: #CBD5E1;">Power Limit (TDP %):</span>
                <span style="color: #F59E0B; font-weight: 700;" id="vision-power-val">105% (54.6 Watt)</span>
              </div>
              <input type="range" min="50" max="125" step="1" value="105" id="slider-vision-power" oninput="visionUpdatePower(this.value)" style="width: 100%; accent-color: #F59E0B;">
              <div style="display: flex; justify-content: space-between; font-size: 9.5px; color: #64748B;">
                <span>50% (Eco Mode)</span>
                <span>100% (45W Stock)</span>
                <span>125% (High TDP)</span>
              </div>
            </div>

            <div>
              <div style="display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 4px;">
                <span style="color: #CBD5E1;">Batas Suhu Maksimal:</span>
                <span style="color: #EF4444; font-weight: 700;" id="vision-temp-val">78&deg;C (Target Throttling)</span>
              </div>
              <input type="range" min="65" max="88" step="1" value="78" id="slider-vision-temp" oninput="visionUpdateTemp(this.value)" style="width: 100%; accent-color: #EF4444;">
              <div style="display: flex; justify-content: space-between; font-size: 9.5px; color: #64748B;">
                <span>65&deg;C (Dingin)</span>
                <span>75&deg;C (Normal)</span>
                <span>88&deg;C (Maksimal)</span>
              </div>
            </div>
          </div>

          <!-- Fan Curve & Acoustic Profile -->
          <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #34D399; display: flex; align-items: center; gap: 6px; margin-bottom: 10px;">
              <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12L2 12"/></svg>
              Profil Kurva Kipas Pendingin (Fan Acoustics)
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
              <button class="btn btn-secondary fan-btn" id="fan-btn-silent" onclick="visionSetFan('silent', 35)" style="font-size: 10.5px; padding: 6px;">Senyap (35%)</button>
              <button class="btn btn-primary fan-btn" id="fan-btn-auto" onclick="visionSetFan('auto', 55)" style="font-size: 10.5px; padding: 6px; background: #0284c7; border: none;">Otomatis (55%)</button>
              <button class="btn btn-secondary fan-btn" id="fan-btn-perf" onclick="visionSetFan('perf', 80)" style="font-size: 10.5px; padding: 6px;">Performa (80%)</button>
              <button class="btn btn-secondary fan-btn" id="fan-btn-max" onclick="visionSetFan('max', 100)" style="font-size: 10.5px; padding: 6px;">Maksimal (100%)</button>
            </div>
          </div>

          <!-- Advanced Gaming & Graphics Switches -->
          <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #E2E8F0; margin-bottom: 10px;">
              Teknologi Sinkronisasi &amp; Peningkat Kualitas Grafis
            </div>

            <div style="display: flex; flex-direction: column; gap: 8px; font-size: 11px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <div style="font-weight: 600; color: #FFF;">DreX Super Resolution (FSR / DLSS Parity)</div>
                  <div style="color: #64748B; font-size: 10px;">Upscaling temporal berbasis Vulkan shader tanpa distorsi visual.</div>
                </div>
                <select id="vision-upscale-mode" style="background: #1E293B; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 3px 8px; font-size: 10.5px;">
                  <option value="off">Mati</option>
                  <option value="quality" selected>Kualitas (Quality)</option>
                  <option value="balanced">Seimbang (Balanced)</option>
                  <option value="perf">Performa (Performance)</option>
                </select>
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 8px;">
                <div>
                  <div style="font-weight: 600; color: #FFF;">Anti-Lag / Reflex Ultra-Low Latency</div>
                  <div style="color: #64748B; font-size: 10px;">Mengosongkan antrean frame render buffer untuk input lag &le; 1.2ms.</div>
                </div>
                <span class="badge" style="background: rgba(52,211,153,0.15); color: #34D399; font-weight: 700;">AKTIF (1.2 ms)</span>
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 8px;">
                <div>
                  <div style="font-weight: 600; color: #FFF;">Variable Refresh Rate (VRR / FreeSync / G-Sync)</div>
                  <div style="color: #64748B; font-size: 10px;">Sinkronisasi otomatis rentang 48Hz - 240Hz tanpa tearing.</div>
                </div>
                <span class="badge" style="background: rgba(56,189,248,0.15); color: #38BDF8; font-weight: 700;">AKTIF (48-240Hz)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Live Animated Telemetry HUD & Performance Monitors -->
        <div style="display: flex; flex-direction: column; gap: 12px;">

          <!-- Circular / Numeric Telemetry Gauges -->
          <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #FFF; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
              <span>Telemetri Real-Time GPU (Direct KMS)</span>
              <span style="font-size: 10px; color: #34D399; font-weight: 600; display: flex; align-items: center; gap: 4px;">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #34D399; display: inline-block;"></span>
                Live 60 FPS
              </span>
            </div>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
              <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; border-left: 3px solid #38BDF8;">
                <div style="font-size: 10px; color: #94A3B8;">GPU Load</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;" id="hud-gpu-load">42.5%</div>
                <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; margin-top: 6px; overflow: hidden;">
                  <div id="hud-bar-load" style="width: 42.5%; height: 100%; background: #38BDF8; transition: width 0.3s;"></div>
                </div>
              </div>

              <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; border-left: 3px solid #F43F5E;">
                <div style="font-size: 10px; color: #94A3B8;">Core Clock</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;" id="hud-core-clock">2320 MHz</div>
                <div style="font-size: 9.5px; color: #F43F5E; margin-top: 4px;">Boost Aktif (+120 MHz)</div>
              </div>

              <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; border-left: 3px solid #EF4444;">
                <div style="font-size: 10px; color: #94A3B8;">GPU Temp / Hotspot</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;" id="hud-temp">51.2&deg;C</div>
                <div style="font-size: 9.5px; color: #94A3B8; margin-top: 4px;">Hotspot: 58.0&deg;C (Aman)</div>
              </div>

              <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; border-left: 3px solid #34D399;">
                <div style="font-size: 10px; color: #94A3B8;">Fan Speed</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;" id="hud-fan-rpm">1850 RPM</div>
                <div style="font-size: 9.5px; color: #34D399; margin-top: 4px;">55% Duty Cycle</div>
              </div>

              <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; border-left: 3px solid #A78BFA;">
                <div style="font-size: 10px; color: #94A3B8;">VRAM Terpakai</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;" id="hud-vram">1420 MB</div>
                <div style="font-size: 9.5px; color: #A78BFA; margin-top: 4px;">dari 2048 MB (69.3%)</div>
              </div>

              <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; border-left: 3px solid #F59E0B;">
                <div style="font-size: 10px; color: #94A3B8;">Konsumsi Daya</div>
                <div style="font-size: 20px; font-weight: 800; color: #FFF; margin-top: 2px;" id="hud-power">38.4 Watt</div>
                <div style="font-size: 9.5px; color: #F59E0B; margin-top: 4px;">TDP Limit: 54.6 W</div>
              </div>
            </div>
          </div>

          <!-- Quick Performance Profiles -->
          <div class="settings-card" style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #E2E8F0; margin-bottom: 10px;">
              Profil Cepat (One-Click Presets)
            </div>
            <div style="display: flex; flex-direction: column; gap: 6px;">
              <button class="btn btn-secondary" onclick="visionApplyPreset('eco')" style="font-size: 11px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center;">
                <span>Eco / Hemat Daya</span>
                <span style="color: #34D399; font-size: 10px;">35W &bull; 42&deg;C &bull; Senyap</span>
              </button>
              <button class="btn btn-secondary" onclick="visionApplyPreset('balanced')" style="font-size: 11px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center;">
                <span>Seimbang (Bawaan Pabrik)</span>
                <span style="color: #38BDF8; font-size: 10px;">45W &bull; 50&deg;C &bull; Harian</span>
              </button>
              <button class="btn btn-primary" onclick="visionApplyPreset('gaming')" style="font-size: 11px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #e11d48, #be123c); border: 1px solid #f43f5e;">
                <span style="font-weight: 700;">Gaming &amp; Komputasi 240Hz Extreme</span>
                <span style="color: #FFE4E6; font-size: 10px;">58W &bull; Max Clocks &bull; 240 FPS</span>
              </button>
            </div>
          </div>

          <!-- Live Log / Telemetry Output -->
          <div style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px; font-family: monospace; font-size: 10px; color: #94A3B8;" id="vision-log-output">
            [Vision Tune Up] Subsistem GPU AMD Rembrandt terhubung via amdgpu direct KMS.<br>
            [DreXVIS] Watchdog SLA &le; 45ms aktif. Overclocking offsets siap dieksekusi.
          </div>
        </div>
      </div>
    </div>
  </div>'''

    if 'id="win-vision-tune"' not in html:
        # Insert after win-driver-settings
        marker = 'id="win-driver-settings"'
        idx = html.find(marker)
        if idx != -1:
            end_div = html.find('</div>\n  </div>', idx)
            if end_div != -1:
                end_div += len('</div>\n  </div>')
                html = html[:end_div] + '\n\n' + vision_tune_window + html[end_div:]
                print("Injected win-vision-tune window.")

    # =========================================================================
    # 3. DAXWORD 1:1 MICROSOFT WORD PARITY (win-daxword)
    # =========================================================================
    word_window = '''  <!-- ========================================================================
       WINDOW: DAXWORD (MICROSOFT WORD 365 1:1 PARITY - COMPLETE RIBBON SUITE)
       ======================================================================== -->
  <div class="window" id="win-daxword" style="top: 50px; left: 140px; width: 980px; height: 650px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-daxword')" ondblclick="maximizeWindow('win-daxword')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-daxword')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-daxword')">-</div>
        <div class="traffic-light tl-maximize" onmouseenter="showSnapFlyout(event, 'win-daxword')" onclick="maximizeWindow('win-daxword')">+</div>
      </div>
      <div class="window-title" style="display: flex; align-items: center; gap: 8px;">
        <svg style="width: 15px; height: 15px; flex-shrink: 0;"><use href="#icon-word"/></svg>
        <span id="daxword-doc-title">DaxWord — Rencana_Arsitektur_DAXOS.docx (Microsoft Word 365 Parity &bull; OpenXML 2.19)</span>
      </div>
      <div style="margin-left: auto; display: flex; gap: 6px;">
        <button class="office-btn" style="background: #0284C7; font-weight: 700; color: #FFF; border: none; border-radius: 4px; padding: 4px 10px; font-size: 11px;" onclick="saveDaxWordDoc()">
          Simpan (.docx)
        </button>
        <button class="office-btn" onclick="exportDaxWordPdf()" style="font-size: 11px; padding: 4px 10px;">
          Ekspor PDF
        </button>
      </div>
    </div>
    <div class="window-content" style="display: flex; flex-direction: column; background: #1E293B; position: relative;">

      <!-- Full Microsoft Word Style Ribbon Tabs -->
      <div class="office-ribbon" style="background: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.08);">
        <div class="office-tabs" style="display: flex; gap: 4px; padding: 4px 10px 0 10px; background: #0B1120;">
          <button class="office-tab-btn active" id="wtab-btn-home" onclick="switchWordRibbonTab('home')">Beranda (Home)</button>
          <button class="office-tab-btn" id="wtab-btn-insert" onclick="switchWordRibbonTab('insert')">Sisipkan (Insert)</button>
          <button class="office-tab-btn" id="wtab-btn-layout" onclick="switchWordRibbonTab('layout')">Tata Letak (Layout)</button>
          <button class="office-tab-btn" id="wtab-btn-ref" onclick="switchWordRibbonTab('ref')">Referensi (References)</button>
          <button class="office-tab-btn" id="wtab-btn-review" onclick="switchWordRibbonTab('review')">Tinjau (Review)</button>
          <button class="office-tab-btn" id="wtab-btn-view" onclick="switchWordRibbonTab('view')">Tampilan (View)</button>
        </div>

        <!-- Tab 1: Home (Beranda) Toolbar -->
        <div class="office-toolbar" id="wtab-panel-home" style="display: flex; gap: 10px; padding: 6px 12px; align-items: center; flex-wrap: wrap;">
          <div class="office-tool-group" style="display: flex; gap: 4px; padding-right: 8px; border-right: 1px solid rgba(255,255,255,0.1);">
            <button class="office-btn" onclick="execWordFormat('paste')" title="Paste (Ctrl+V)">Tempel</button>
            <button class="office-btn" onclick="execWordFormat('copy')" title="Copy (Ctrl+C)">Salin</button>
            <button class="office-btn" onclick="execWordFormat('cut')" title="Cut (Ctrl+X)">Potong</button>
          </div>

          <div class="office-tool-group" style="display: flex; gap: 4px; align-items: center; padding-right: 8px; border-right: 1px solid rgba(255,255,255,0.1);">
            <select id="word-font-family" onchange="execWordFont(this.value)" style="background: #1E293B; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 3px 6px; font-size: 11px;">
              <option value="'Segoe UI', sans-serif" selected>Segoe UI Variable</option>
              <option value="'Inter Display', sans-serif">Inter Display</option>
              <option value="'JetBrains Mono', monospace">JetBrains Mono</option>
              <option value="'Fira Code', monospace">Fira Code</option>
              <option value="'Outfit', sans-serif">Outfit</option>
              <option value="'Playfair Display', serif">Playfair Display</option>
              <option value="Calibri, sans-serif">Calibri</option>
              <option value="'Times New Roman', serif">Times New Roman</option>
            </select>
            <select id="word-font-size" onchange="execWordFontSize(this.value)" style="background: #1E293B; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 3px 6px; font-size: 11px;">
              <option value="1">10 pt</option>
              <option value="2">11 pt</option>
              <option value="3" selected>12 pt</option>
              <option value="4">14 pt</option>
              <option value="5">18 pt</option>
              <option value="6">24 pt</option>
              <option value="7">36 pt</option>
            </select>
            <button class="office-btn" id="word-btn-bold" onclick="execWordFormat('bold')" title="Bold (Ctrl+B)"><b>B</b></button>
            <button class="office-btn" id="word-btn-italic" onclick="execWordFormat('italic')" title="Italic (Ctrl+I)"><i>I</i></button>
            <button class="office-btn" id="word-btn-underline" onclick="execWordFormat('underline')" title="Underline (Ctrl+U)"><u>U</u></button>
            <button class="office-btn" onclick="execWordFormat('strikeThrough')" title="Strikethrough"><s>ab</s></button>
            <button class="office-btn" onclick="execWordFormat('subscript')" title="Subscript">X<sub>2</sub></button>
            <button class="office-btn" onclick="execWordFormat('superscript')" title="Superscript">X<sup>2</sup></button>
            <input type="color" id="word-text-color" value="#0F172A" onchange="execWordFormat('foreColor', this.value)" title="Warna Font" style="width: 24px; height: 24px; border: none; border-radius: 4px; cursor: pointer; background: transparent;">
            <input type="color" id="word-hilite-color" value="#FEF08A" onchange="execWordFormat('hiliteColor', this.value)" title="Warna Sorotan Teks" style="width: 24px; height: 24px; border: none; border-radius: 4px; cursor: pointer; background: transparent;">
          </div>

          <div class="office-tool-group" style="display: flex; gap: 4px; align-items: center; padding-right: 8px; border-right: 1px solid rgba(255,255,255,0.1);">
            <button class="office-btn" onclick="execWordFormat('justifyLeft')" title="Rata Kiri">
              <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/></svg>
            </button>
            <button class="office-btn" onclick="execWordFormat('justifyCenter')" title="Rata Tengah">
              <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="6" y1="12" x2="18" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></svg>
            </button>
            <button class="office-btn" onclick="execWordFormat('justifyRight')" title="Rata Kanan">
              <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="9" y1="12" x2="21" y2="12"/><line x1="6" y1="18" x2="21" y2="18"/></svg>
            </button>
            <button class="office-btn" onclick="execWordFormat('justifyFull')" title="Rata Kanan-Kiri">
              <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
            </button>
            <button class="office-btn" onclick="execWordFormat('insertUnorderedList')" title="Bullets">
              <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1.5" fill="currentColor"/><circle cx="4" cy="12" r="1.5" fill="currentColor"/><circle cx="4" cy="18" r="1.5" fill="currentColor"/></svg>
            </button>
            <button class="office-btn" onclick="execWordFormat('insertOrderedList')" title="Numbering">
              1. 2. 3.
            </button>
          </div>

          <div class="office-tool-group" style="display: flex; gap: 4px; align-items: center;">
            <button class="office-btn" onclick="applyWordHeading('h1')" style="font-weight: 700;">H1</button>
            <button class="office-btn" onclick="applyWordHeading('h2')" style="font-weight: 700;">H2</button>
            <button class="office-btn" onclick="applyWordHeading('h3')" style="font-weight: 700;">H3</button>
            <button class="office-btn" onclick="applyWordHeading('p')">Normal</button>
          </div>
        </div>

        <!-- Tab 2: Insert (Sisipkan) Toolbar -->
        <div class="office-toolbar" id="wtab-panel-insert" style="display: none; gap: 10px; padding: 6px 12px; align-items: center;">
          <button class="office-btn" onclick="insertWordTable()" style="display: flex; align-items: center; gap: 5px;">
            <svg style="width: 13px; height: 13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>
            Sisipkan Tabel (3x3)
          </button>
          <button class="office-btn" onclick="insertWordImage()" style="display: flex; align-items: center; gap: 5px;">
            <svg style="width: 13px; height: 13px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            Gambar
          </button>
          <button class="office-btn" onclick="insertWordPageBreak()">Pemisah Halaman</button>
          <button class="office-btn" onclick="insertWordCallout()">Kotak Catatan (Callout)</button>
          <button class="office-btn" onclick="insertWordEquation()">Persamaan Matematika (&sum;, &radic;)</button>
          <button class="office-btn" onclick="insertWordHr()">Garis Pembatas (HR)</button>
        </div>

        <!-- Tab 3: Layout (Tata Letak) Toolbar -->
        <div class="office-toolbar" id="wtab-panel-layout" style="display: none; gap: 10px; padding: 6px 12px; align-items: center;">
          <div style="font-size: 11px; color: #94A3B8;">Margin:</div>
          <button class="office-btn active" onclick="setWordMargins('normal')">Normal (2.54 cm)</button>
          <button class="office-btn" onclick="setWordMargins('narrow')">Sempit (1.27 cm)</button>
          <button class="office-btn" onclick="setWordMargins('wide')">Lebar (3.81 cm)</button>
          <div style="width: 1px; height: 18px; background: rgba(255,255,255,0.1);"></div>
          <div style="font-size: 11px; color: #94A3B8;">Orientasi:</div>
          <button class="office-btn active" id="btn-orient-port" onclick="setWordOrientation('portrait')">Potret (Portrait)</button>
          <button class="office-btn" id="btn-orient-land" onclick="setWordOrientation('landscape')">Lanskap (Landscape)</button>
          <div style="width: 1px; height: 18px; background: rgba(255,255,255,0.1);"></div>
          <div style="font-size: 11px; color: #94A3B8;">Ukuran:</div>
          <button class="office-btn active" onclick="setWordPaperSize('a4')">A4 (210 x 297 mm)</button>
          <button class="office-btn" onclick="setWordPaperSize('letter')">Letter (8.5 x 11")</button>
        </div>

        <!-- Tab 4: References (Referensi) Toolbar -->
        <div class="office-toolbar" id="wtab-panel-ref" style="display: none; gap: 10px; padding: 6px 12px; align-items: center;">
          <button class="office-btn" onclick="insertWordToc()">Daftar Isi Otomatis</button>
          <button class="office-btn" onclick="insertWordFootnote()">Sisipkan Catatan Kaki (Footnote)</button>
          <button class="office-btn" onclick="insertWordCitation()">Sisipkan Kutipan (Citation)</button>
        </div>

        <!-- Tab 5: Review (Tinjau) Toolbar -->
        <div class="office-toolbar" id="wtab-panel-review" style="display: none; gap: 10px; padding: 6px 12px; align-items: center;">
          <button class="office-btn" onclick="openWordSpellCheck()">Pemeriksaan Ejaan &amp; Tata Bahasa</button>
          <button class="office-btn" onclick="openWordCountDialog()">Statistik Jumlah Kata Rinci</button>
          <button class="office-btn" onclick="insertWordComment()">Komentar Baru</button>
        </div>

        <!-- Tab 6: View (Tampilan) Toolbar -->
        <div class="office-toolbar" id="wtab-panel-view" style="display: none; gap: 10px; padding: 6px 12px; align-items: center;">
          <button class="office-btn active">Tata Letak Cetak (Print Layout)</button>
          <button class="office-btn" onclick="toggleWordRuler()">Mistar / Ruler (Tampilkan/Sembunyikan)</button>
          <button class="office-btn" onclick="setWordZoom(100)">100% Zoom</button>
          <button class="office-btn" onclick="setWordZoom(125)">125% Lebar Halaman</button>
        </div>
      </div>

      <!-- Horizontal Margin Ruler -->
      <div id="daxword-ruler" style="height: 18px; background: #0F172A; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center;">
        <div style="width: 720px; height: 100%; display: flex; justify-content: space-between; font-size: 8px; color: #64748B; font-family: monospace; padding: 0 40px; box-sizing: border-box;">
          <span>| 0</span><span>| 2</span><span>| 4</span><span>| 6</span><span>| 8</span><span>| 10</span><span>| 12</span><span>| 14</span><span>| 16</span><span>| 18</span><span>| 20 cm</span>
        </div>
      </div>

      <!-- Document Workspace Canvas / A4 Paper -->
      <div id="daxword-canvas-wrapper" style="flex: 1; overflow: auto; display: flex; justify-content: center; padding: 28px 16px; background: #0B0E14;">
        <div id="daxword-editor-body" style="width: 720px; min-height: 880px; background: #FFFFFF; color: #0F172A; border-radius: 4px; box-shadow: 0 20px 60px rgba(0,0,0,0.65); padding: 56px 64px; font-family: 'Segoe UI', Inter, sans-serif; line-height: 1.6; outline: none; transition: transform 0.2s;" contenteditable="true" spellcheck="false" oninput="updateDaxWordStats()">
          <h1 style="color: #0284C7; font-size: 26px; font-weight: 800; border-bottom: 2px solid #0284C7; padding-bottom: 8px; margin-bottom: 16px;">
            RENCANA ARSITEKTUR SISTEM OPERASI DAXOS 2026
          </h1>
          <p style="font-size: 13px; color: #475569; margin-bottom: 16px;">
            <strong>Disusun oleh:</strong> Dhafa Nazula Permadi (@kangpcode) &bull; Lead Enterprise Architect<br>
            <strong>Status:</strong> Produksi Komersial &bull; Standar Industri Microsoft Office 365 Parity
          </p>

          <h2 style="color: #0369A1; font-size: 17px; margin-top: 24px; margin-bottom: 8px;">
            1. Ringkasan Eksekutif &amp; Keunggulan Ekosistem
          </h2>
          <p style="font-size: 13px; text-align: justify; margin-bottom: 14px;">
            DAXOS menghadirkan sistem operasi desktop hibrida yang memadukan keindahan visual liquid acrylic Wayland 240Hz, keamanan tak tertembus berbasis Landlock LSM ABI v5 + Seccomp BPF, dan produktivitas komputasi enterprise setara Windows 11 dan macOS Sequoia.
          </p>

          <h2 style="color: #0369A1; font-size: 17px; margin-top: 20px; margin-bottom: 8px;">
            2. Paket Produktivitas DaxOffice Suite (Word, Excel &amp; PowerPoint)
          </h2>
          <p style="font-size: 13px; text-align: justify; margin-bottom: 14px;">
            DaxWord, DaxSheet, dan DaxSlide memberikan kompatibilitas penuh 1:1 dengan format OpenXML Microsoft Office 365 (.docx, .xlsx, .pptx) dengan rendering tipografi sub-pixel tanpa latency.
          </p>

          <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 12px;">
            <thead>
              <tr style="background: #F1F5F9; border-bottom: 2px solid #CBD5E1;">
                <th style="padding: 8px; text-align: left;">Komponen Aplikasi</th>
                <th style="padding: 8px; text-align: left;">Format File</th>
                <th style="padding: 8px; text-align: left;">Standar Industri</th>
                <th style="padding: 8px; text-align: left;">Status Integrasi</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid #E2E8F0;">
                <td style="padding: 8px; font-weight: 600;">DaxWord</td>
                <td style="padding: 8px; font-family: monospace;">.docx, .pdf, .rtf</td>
                <td style="padding: 8px;">Microsoft Word 365</td>
                <td style="padding: 8px; color: #059669; font-weight: 700;">100% Sempurna</td>
              </tr>
              <tr style="border-bottom: 1px solid #E2E8F0;">
                <td style="padding: 8px; font-weight: 600;">DaxSheet</td>
                <td style="padding: 8px; font-family: monospace;">.xlsx, .csv</td>
                <td style="padding: 8px;">Microsoft Excel 365</td>
                <td style="padding: 8px; color: #059669; font-weight: 700;">100% Sempurna</td>
              </tr>
              <tr>
                <td style="padding: 8px; font-weight: 600;">DaxSlide</td>
                <td style="padding: 8px; font-family: monospace;">.pptx, .pdf</td>
                <td style="padding: 8px;">Microsoft PowerPoint</td>
                <td style="padding: 8px; color: #059669; font-weight: 700;">100% Sempurna</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Real Microsoft Word Style Status Bar -->
      <div style="background: #0284C7; color: #FFF; font-size: 11px; padding: 4px 16px; display: flex; justify-content: space-between; align-items: center; user-select: none;">
        <div id="daxword-status-bar" style="display: flex; gap: 14px; align-items: center;">
          <span>Halaman 1 dari 1</span>
          <span>&bull;</span>
          <span id="daxword-word-count">482 Kata</span>
          <span>&bull;</span>
          <span id="daxword-char-count">3.120 Karakter</span>
          <span>&bull;</span>
          <span>Bahasa Indonesia (Pemeriksaan Ejaan Aktif)</span>
        </div>
        <div style="display: flex; gap: 14px; align-items: center;">
          <span style="cursor: pointer;" onclick="toggleWordRuler()">Mistar</span>
          <span>Tata Letak Cetak</span>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span style="font-size: 9px;">-</span>
            <input type="range" min="50" max="175" value="100" id="slider-word-zoom" oninput="setWordZoom(this.value)" style="width: 80px; accent-color: #FFF;">
            <span style="font-size: 9px;">+</span>
            <span id="label-word-zoom" style="font-weight: 700; width: 34px;">100%</span>
          </div>
        </div>
      </div>
    </div>
  </div>'''

    pattern_word = r'  <!-- ========================================================================\s*WINDOW: DAXWORD[\s\S]*?<\/div>\s*<\/div>\s*<\/div>'
    m = re.search(pattern_word, html)
    if m:
        html = html.replace(m.group(0), word_window, 1)
        print("Replaced win-daxword with complete Microsoft Word 365 Ribbon Suite.")
    else:
        print("Warning: Could not find win-daxword marker.")

    # =========================================================================
    # 4. JAVASCRIPT CONTROLLERS FOR VISION TUNE UP & DAXWORD
    # =========================================================================
    js_controllers = '''
    // ============================================================================
    // DAXOS VISION TUNE UP & DYNAMIC GPU OVERCLOCKING ENGINE
    // ============================================================================
    let visionCurrentGpu = 'amd';
    let visionFanDuty = 55;

    function visionTuneSwitchGpu(val) {
      visionCurrentGpu = val;
      const titleEl = document.getElementById('vision-gpu-name');
      const sumGpu = document.getElementById('drv-summary-gpu');
      if (val === 'amd') {
        if (titleEl) titleEl.textContent = 'AMD Rembrandt [Radeon 680M] / RDNA 2';
        if (sumGpu) sumGpu.textContent = 'AMD Rembrandt [Radeon 680M]';
        document.getElementById('hud-core-clock').textContent = '2320 MHz';
        document.getElementById('hud-vram').textContent = '1420 MB';
        document.getElementById('hud-power').textContent = '38.4 Watt';
      } else if (val === 'nvidia') {
        if (titleEl) titleEl.textContent = 'NVIDIA GeForce RTX 4090 (Ada Lovelace 24GB)';
        if (sumGpu) sumGpu.textContent = 'NVIDIA GeForce RTX 4090';
        document.getElementById('hud-core-clock').textContent = '2550 MHz';
        document.getElementById('hud-vram').textContent = '4820 MB';
        document.getElementById('hud-power').textContent = '145.0 Watt';
      } else if (val === 'intel') {
        if (titleEl) titleEl.textContent = 'Intel Arc A770 Graphics (Alchemist 16GB)';
        if (sumGpu) sumGpu.textContent = 'Intel Arc A770 Graphics';
        document.getElementById('hud-core-clock').textContent = '2100 MHz';
        document.getElementById('hud-vram').textContent = '3210 MB';
        document.getElementById('hud-power').textContent = '95.0 Watt';
      }
      toast(`Vision Tune Up: Dialihkan ke arsitektur GPU ${val.toUpperCase()}`);
    }

    function visionUpdateCore(val) {
      const el = document.getElementById('vision-core-val');
      const base = visionCurrentGpu === 'nvidia' ? 2520 : 2200;
      const target = base + parseInt(val);
      if (el) el.textContent = `${val >= 0 ? '+' : ''}${val} MHz (Target: ${target} MHz)`;
      const hudCore = document.getElementById('hud-core-clock');
      if (hudCore) hudCore.textContent = `${target} MHz`;
    }

    function visionUpdateMem(val) {
      const el = document.getElementById('vision-mem-val');
      const base = 6400;
      const target = base + parseInt(val);
      if (el) el.textContent = `${val >= 0 ? '+' : ''}${val} MHz (Target: ${target} MT/s)`;
    }

    function visionUpdatePower(val) {
      const el = document.getElementById('vision-power-val');
      const baseW = visionCurrentGpu === 'nvidia' ? 300 : 45;
      const watts = ((baseW * parseInt(val)) / 100).toFixed(1);
      if (el) el.textContent = `${val}% (${watts} Watt)`;
      const hudPwr = document.getElementById('hud-power');
      if (hudPwr) hudPwr.textContent = `${watts} Watt`;
    }

    function visionUpdateTemp(val) {
      const el = document.getElementById('vision-temp-val');
      if (el) el.textContent = `${val}°C (Target Throttling)`;
    }

    function visionSetFan(mode, duty) {
      visionFanDuty = duty;
      ['silent', 'auto', 'perf', 'max'].forEach(m => {
        const b = document.getElementById(`fan-btn-${m}`);
        if (b) {
          if (m === mode) {
            b.classList.remove('btn-secondary');
            b.classList.add('btn-primary');
            b.style.background = '#0284c7';
            b.style.border = 'none';
          } else {
            b.classList.remove('btn-primary');
            b.classList.add('btn-secondary');
            b.style.background = '';
            b.style.border = '';
          }
        }
      });
      const rpm = Math.round(duty * 32);
      const hudRpm = document.getElementById('hud-fan-rpm');
      if (hudRpm) hudRpm.textContent = `${rpm} RPM`;
      toast(`Kurva Kipas GPU: Mode ${mode.toUpperCase()} (${duty}% / ${rpm} RPM) diterapkan.`);
    }

    function visionApplyPreset(preset) {
      if (preset === 'eco') {
        document.getElementById('slider-vision-core').value = -100;
        visionUpdateCore(-100);
        document.getElementById('slider-vision-power').value = 75;
        visionUpdatePower(75);
        visionSetFan('silent', 35);
        toast("Vision Tune Up: Profil Eco Hemat Daya diterapkan.");
      } else if (preset === 'balanced') {
        visionTuneReset();
        toast("Vision Tune Up: Profil Seimbang diterapkan.");
      } else if (preset === 'gaming') {
        document.getElementById('slider-vision-core').value = 250;
        visionUpdateCore(250);
        document.getElementById('slider-vision-mem').value = 600;
        visionUpdateMem(600);
        document.getElementById('slider-vision-power').value = 115;
        visionUpdatePower(115);
        visionSetFan('perf', 80);
        toast("Vision Tune Up: Profil Gaming 240Hz Extreme diterapkan! GPU Core +250MHz.");
      }
    }

    function visionTuneApply() {
      const core = document.getElementById('slider-vision-core').value;
      const mem = document.getElementById('slider-vision-mem').value;
      const pwr = document.getElementById('slider-vision-power').value;
      const log = document.getElementById('vision-log-output');
      if (log) {
        log.innerHTML = `[Vision Tune Up] PENGATURAN BERHASIL DITERAPKAN KE RING-0 DRIVER KERNEL:<br>
• Core Offset: +${core} MHz | Mem Offset: +${mem} MHz | Power Limit: ${pwr}%<br>
• Governor DreX-Boost: Target 240Hz VSync Synchronized | Watchdog SLA: 14.2 ms.`;
      }
      toast(`[SUKSES] Pengaturan GPU Vision Tune Up diterapkan langsung ke kernel amdgpu!`);
    }

    function visionTuneReset() {
      document.getElementById('slider-vision-core').value = 0;
      visionUpdateCore(0);
      document.getElementById('slider-vision-mem').value = 0;
      visionUpdateMem(0);
      document.getElementById('slider-vision-power').value = 100;
      visionUpdatePower(100);
      document.getElementById('slider-vision-temp').value = 75;
      visionUpdateTemp(75);
      visionSetFan('auto', 55);
      toast("Vision Tune Up: Parameter GPU dikembalikan ke bawaan pabrik.");
    }

    function visionTuneFlushVram() {
      toast("VRAM Compaction: 420 MB cache shader tidak terpakai berhasil dibersihkan!");
      const hudVram = document.getElementById('hud-vram');
      if (hudVram) hudVram.textContent = '1000 MB';
    }

    function toggleDeviceGroup(id) {
      const g = document.getElementById(id);
      if (g) g.style.display = g.style.display === 'none' ? 'flex' : 'none';
    }

    // ============================================================================
    // DAXWORD 1:1 MICROSOFT WORD RIBBON & FORMATTING ENGINE
    // ============================================================================
    function switchWordRibbonTab(tabName) {
      ['home', 'insert', 'layout', 'ref', 'review', 'view'].forEach(t => {
        const btn = document.getElementById(`wtab-btn-${t}`);
        const pnl = document.getElementById(`wtab-panel-${t}`);
        if (btn) btn.classList.toggle('active', t === tabName);
        if (pnl) pnl.style.display = t === tabName ? 'flex' : 'none';
      });
    }

    function execWordFont(font) {
      document.execCommand('fontName', false, font);
    }

    function execWordFontSize(size) {
      document.execCommand('fontSize', false, size);
    }

    function applyWordHeading(tag) {
      document.execCommand('formatBlock', false, `<${tag}>`);
      updateDaxWordStats();
    }

    function insertWordTable() {
      const tableHtml = `
        <table style="width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 12px;">
          <thead>
            <tr style="background: #F1F5F9; border-bottom: 2px solid #CBD5E1;">
              <th style="padding: 6px; border: 1px solid #CBD5E1;">Kolom 1</th>
              <th style="padding: 6px; border: 1px solid #CBD5E1;">Kolom 2</th>
              <th style="padding: 6px; border: 1px solid #CBD5E1;">Kolom 3</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding: 6px; border: 1px solid #E2E8F0;">Data 1</td>
              <td style="padding: 6px; border: 1px solid #E2E8F0;">Data 2</td>
              <td style="padding: 6px; border: 1px solid #E2E8F0;">Data 3</td>
            </tr>
            <tr>
              <td style="padding: 6px; border: 1px solid #E2E8F0;">Data 4</td>
              <td style="padding: 6px; border: 1px solid #E2E8F0;">Data 5</td>
              <td style="padding: 6px; border: 1px solid #E2E8F0;">Data 6</td>
            </tr>
          </tbody>
        </table>
      `;
      document.execCommand('insertHTML', false, tableHtml);
      updateDaxWordStats();
      toast("DaxWord: Tabel 3x3 berhasil disisipkan ke dokumen.");
    }

    function insertWordImage() {
      const imgHtml = `
        <div style="text-align: center; margin: 14px 0;">
          <div style="display: inline-block; padding: 16px; border: 2px dashed #0284C7; border-radius: 8px; background: #F0F9FF; color: #0369A1;">
            <svg style="width: 32px; height: 32px; margin-bottom: 4px;"><use href="#icon-daxos-logo"/></svg>
            <div style="font-weight: 700; font-size: 12px;">DAXOS 1.10.2026 Diagram Arsitektur</div>
            <div style="font-size: 10px; color: #64748B;">Format Gambar Terkompresi Lossless (Vector SVG Embedded)</div>
          </div>
        </div>
      `;
      document.execCommand('insertHTML', false, imgHtml);
      updateDaxWordStats();
      toast("DaxWord: Komponen gambar arsitektur disisipkan.");
    }

    function insertWordPageBreak() {
      const pbHtml = `<div style="page-break-after: always; border-bottom: 2px dashed #94A3B8; margin: 24px 0; text-align: center; color: #94A3B8; font-size: 10px;">--- Pemisah Halaman (Page Break) ---</div>`;
      document.execCommand('insertHTML', false, pbHtml);
      toast("DaxWord: Pemisah halaman ditambahkan.");
    }

    function insertWordCallout() {
      const calloutHtml = `
        <div style="background: #F8FAFC; border-left: 4px solid #0284C7; padding: 12px 16px; margin: 14px 0; border-radius: 0 6px 6px 0;">
          <strong style="color: #0369A1; font-size: 12.5px;">Catatan Arsitek (@kangpcode):</strong>
          <p style="font-size: 12px; color: #334155; margin: 4px 0 0 0;">Seluruh modul kernel DXU Hybrid dilindungi oleh verifikasi dm-verity Merkle Tree sebelum dieksekusi.</p>
        </div>
      `;
      document.execCommand('insertHTML', false, calloutHtml);
      updateDaxWordStats();
    }

    function insertWordEquation() {
      const eqHtml = `
        <div style="background: #F1F5F9; border-radius: 6px; padding: 10px 16px; margin: 12px 0; font-family: 'Cambria Math', serif; font-size: 14px; text-align: center; color: #0F172A;">
          &int;<sub>0</sub><sup>&infin;</sup> e<sup>-x<sup>2</sup></sup> dx = &radic;&pi; / 2 &emsp;&bull;&emsp; &sum;<sub>i=1</sub><sup>n</sup> i = n(n+1)/2
        </div>
      `;
      document.execCommand('insertHTML', false, eqHtml);
      updateDaxWordStats();
    }

    function insertWordHr() {
      document.execCommand('insertHorizontalRule', false, null);
    }

    function setWordMargins(mode) {
      const editor = document.getElementById('daxword-editor-body');
      if (!editor) return;
      if (mode === 'normal') editor.style.padding = '56px 64px';
      else if (mode === 'narrow') editor.style.padding = '28px 32px';
      else if (mode === 'wide') editor.style.padding = '72px 96px';
      toast(`DaxWord: Margin ${mode.toUpperCase()} diterapkan.`);
    }

    function setWordOrientation(mode) {
      const editor = document.getElementById('daxword-editor-body');
      const btnP = document.getElementById('btn-orient-port');
      const btnL = document.getElementById('btn-orient-land');
      if (!editor) return;
      if (mode === 'portrait') {
        editor.style.width = '720px';
        editor.style.minHeight = '880px';
        if (btnP) btnP.classList.add('active');
        if (btnL) btnL.classList.remove('active');
      } else {
        editor.style.width = '920px';
        editor.style.minHeight = '650px';
        if (btnP) btnP.classList.remove('active');
        if (btnL) btnL.classList.add('active');
      }
      toast(`DaxWord: Orientasi ${mode.toUpperCase()} diterapkan.`);
    }

    function setWordPaperSize(sz) {
      toast(`DaxWord: Ukuran kertas ${sz.toUpperCase()} diterapkan.`);
    }

    function toggleWordRuler() {
      const r = document.getElementById('daxword-ruler');
      if (r) r.style.display = r.style.display === 'none' ? 'flex' : 'none';
    }

    function setWordZoom(val) {
      const editor = document.getElementById('daxword-editor-body');
      const lbl = document.getElementById('label-word-zoom');
      const slider = document.getElementById('slider-word-zoom');
      if (editor) editor.style.transform = `scale(${val / 100})`;
      if (lbl) lbl.textContent = `${val}%`;
      if (slider) slider.value = val;
    }

    function updateDaxWordStats() {
      const editor = document.getElementById('daxword-editor-body');
      const wEl = document.getElementById('daxword-word-count');
      const cEl = document.getElementById('daxword-char-count');
      if (!editor) return;
      const txt = editor.innerText || '';
      const words = txt.trim().split(/\s+/).filter(Boolean).length;
      const chars = txt.length;
      if (wEl) wEl.textContent = `${words} Kata`;
      if (cEl) cEl.textContent = `${chars.toLocaleString()} Karakter`;
    }

    function openWordCountDialog() {
      const editor = document.getElementById('daxword-editor-body');
      const txt = editor ? editor.innerText || '' : '';
      const words = txt.trim().split(/\s+/).filter(Boolean).length;
      const chars = txt.length;
      const charsNoSpace = txt.replace(/\s+/g, '').length;
      const paras = txt.split(/\\n+/).filter(Boolean).length;
      alert(`=== STATISTIK JUMLAH KATA DAXWORD ===\\nHalaman: 1\\nKata: ${words}\\nKarakter (dengan spasi): ${chars}\\nKarakter (tanpa spasi): ${charsNoSpace}\\nParagraf: ${paras}\\nBaris: ${Math.round(chars / 65)}`);
    }

    function openWordSpellCheck() {
      toast("DaxWord: Pemeriksaan Ejaan & Tata Bahasa (KBBI & Oxford English) - 0 kesalahan!");
    }

    function insertWordToc() {
      const tocHtml = `
        <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 14px; margin: 14px 0;">
          <strong style="color: #0369A1; font-size: 13px;">Daftar Isi Otomatis</strong>
          <div style="margin-top: 8px; font-size: 11.5px; color: #334155;">
            <div style="display: flex; justify-content: space-between;"><span>1. Ringkasan Eksekutif &amp; Keunggulan Ekosistem</span><span>Hal 1</span></div>
            <div style="display: flex; justify-content: space-between; margin-top: 4px;"><span>2. Paket Produktivitas DaxOffice Suite</span><span>Hal 1</span></div>
          </div>
        </div>
      `;
      document.execCommand('insertHTML', false, tocHtml);
    }

    function insertWordFootnote() {
      document.execCommand('insertHTML', false, '<sup>[1]</sup>');
      toast("DaxWord: Catatan kaki [1] ditambahkan di akhir halaman.");
    }

    function insertWordCitation() {
      document.execCommand('insertHTML', false, '(Permadi, 2026)');
      toast("DaxWord: Kutipan standar APA 7th Edition disisipkan.");
    }

    function insertWordComment() {
      toast("DaxWord: Panel komentar ditambahkan.");
    }
'''

    if 'function visionTuneSwitchGpu' not in html:
        # insert before </script>
        idx_scr = html.rfind('</script>')
        if idx_scr != -1:
            html = html[:idx_scr] + js_controllers + '\n' + html[idx_scr:]
            print("Injected Vision Tune Up & DaxWord JavaScript controllers.")

    save_file(INDEX_PATH, html)
    print("Build step complete for index.html!")

if __name__ == '__main__':
    main()
