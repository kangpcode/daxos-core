#!/usr/bin/env python3
"""
Update desktop_preview/index.html to implement:
1. macOS-style Window Animations for EVERY open, close, minimize, maximize, and panels (Spotlight, Control Center).
   - Minimizing: Genie/scale-down animation towards the exact dock icon.
   - Restoring: Scale-up animation from the dock icon back to window position.
   - Closing: Fluid zoom-out fade animation (0.2s cubic-bezier).
   - Opening: Fluid spring pop-in animation (0.26s cubic-bezier).
   - Maximizing: Smoothly animated bounds transition (0.32s cubic-bezier).
   - Panels: macOS spring dropdown / slide-up transitions.
2. Professional & Powerful Camera Application (win-camera):
   - Mirror / Flip Horizontal precision control:
     - Toggle between "Presisi Asli 1:1 (Unmirrored / True-Sight)" and "Cermin Natural (Mirrored / Selfie)".
     - Smooth horizontal flip transition.
     - Clear visual status badge.
   - Aspect ratio selector: 16:9, 4:3, 1:1, Cinema 21:9.
   - Countdown timer: Off, 3s, 5s, 10s with large animated on-screen countdown digits.
   - Resolution & frame rate: 4K UHD 60fps, 1080p 120fps (ProMotion), 2K HDR 90fps.
   - Quick Zoom buttons: 0.5x (Ultra-Wide), 1.0x (Wide), 2.0x (Telephoto), 5.0x (Super Zoom).
   - Rule of Thirds framing grid, Center Crosshairs, and Horizon Level indicator (0.0° Level).
   - Pro Manual Drawer: ISO slider (50 - 6400), EV slider (-2.0 to +2.0), White Balance (AWB, Daylight, Tungsten, Cloudy).
   - Modes: FOTO, BURST (3 rapid shots), POTRET (aperture blur), PRO RAW, VIDEO.
   - Recent capture thumbnail and interactive Photo Review QuickLook modal.
   - Zero Unicode emojis across all files.
   - Lead Architect attribution to Dhafa Nazula Permadi (@kangpcode).
"""

import re
from pathlib import Path

INDEX_FILE = Path("/home/kangpcode/wwwsite/daxos/src/ui/desktop_preview/index.html")

def update_camera_and_animations():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update .window CSS rules and add macOS animation classes
    old_window_css = '''    .window {
      position: absolute;
      background: var(--bg-acrylic-heavy);
      backdrop-filter: blur(40px) saturate(200%);
      -webkit-backdrop-filter: blur(40px) saturate(200%);
      border: 1px solid var(--border-acrylic);
      border-radius: 14px;
      box-shadow: 0 28px 70px rgba(0, 0, 0, 0.65), 0 0 1px rgba(255, 255, 255, 0.25);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-width: 380px;
      min-height: 240px;
      z-index: 100;
      transition: opacity 0.15s ease, transform 0.15s ease;
    }

    .window.focused {
      border-color: rgba(255, 255, 255, 0.28);
      box-shadow: 0 32px 85px rgba(0, 0, 0, 0.75), 0 0 2px rgba(10, 132, 255, 0.4);
    }

    .window.minimized {
      display: none !important;
    }'''

    new_window_css = '''    /* macOS-style Window Transitions & Animations */
    .window {
      position: absolute;
      background: var(--bg-acrylic-heavy);
      backdrop-filter: blur(40px) saturate(200%);
      -webkit-backdrop-filter: blur(40px) saturate(200%);
      border: 1px solid var(--border-acrylic);
      border-radius: 14px;
      box-shadow: 0 28px 70px rgba(0, 0, 0, 0.65), 0 0 1px rgba(255, 255, 255, 0.25);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-width: 380px;
      min-height: 240px;
      z-index: 100;
      transform-origin: center center;
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1),
                  opacity 0.22s ease-out,
                  top 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                  left 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                  width 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                  height 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                  border-radius 0.25s ease;
      will-change: transform, opacity, width, height, top, left;
    }

    .window.focused {
      border-color: rgba(255, 255, 255, 0.28);
      box-shadow: 0 32px 85px rgba(0, 0, 0, 0.75), 0 0 2px rgba(10, 132, 255, 0.4);
    }

    /* macOS Opening Animation */
    .window.window-opening {
      animation: macosWindowOpen 0.26s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes macosWindowOpen {
      0% {
        opacity: 0;
        transform: scale(0.88) translateY(14px);
      }
      100% {
        opacity: 1;
        transform: scale(1) translateY(0);
      }
    }

    /* macOS Closing Animation */
    .window.window-closing {
      animation: macosWindowClose 0.20s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      pointer-events: none;
    }

    @keyframes macosWindowClose {
      0% {
        opacity: 1;
        transform: scale(1);
      }
      100% {
        opacity: 0;
        transform: scale(0.85);
      }
    }

    /* macOS Minimizing Scale to Dock */
    .window.window-minimizing {
      transition: transform 0.34s cubic-bezier(0.22, 1, 0.36, 1),
                  opacity 0.30s ease-in,
                  filter 0.34s ease !important;
      pointer-events: none;
    }

    /* macOS Restoring from Dock */
    .window.window-restoring {
      transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                  opacity 0.28s ease-out,
                  filter 0.32s ease !important;
    }

    .window.minimized {
      display: none !important;
    }'''

    if old_window_css in html:
        html = html.replace(old_window_css, new_window_css)
    else:
        print("[WARN] old_window_css not found directly, replacing .window block via regex")
        html = re.sub(r'\.window\s*\{[^}]*transition:[^}]*\}\s*\.window\.focused\s*\{[^}]*\}\s*\.window\.minimized\s*\{[^}]*\}', new_window_css, html)

    # 2. Update Spotlight & Control Center CSS for macOS spring animations
    html = re.sub(
        r'\.spotlight-modal\s*\{[\s\S]*?z-index:\s*10001;[\s\S]*?\}',
        '''.spotlight-modal {
      position: fixed;
      top: 18%;
      left: 50%;
      width: 580px;
      background: var(--bg-acrylic-heavy);
      backdrop-filter: blur(40px) saturate(220%);
      -webkit-backdrop-filter: blur(40px) saturate(220%);
      border: 1px solid var(--border-acrylic);
      border-radius: 18px;
      box-shadow: 0 32px 90px rgba(0, 0, 0, 0.75), 0 0 1px rgba(255, 255, 255, 0.3);
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      z-index: 10001;
      opacity: 0;
      pointer-events: none;
      transform: translate(-50%, -18px) scale(0.96);
      transform-origin: center top;
      transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
    }''',
        html
    )

    html = re.sub(
        r'\.spotlight-modal\.open\s*\{[\s\S]*?\}',
        '''.spotlight-modal.open {
      opacity: 1;
      pointer-events: auto;
      transform: translate(-50%, 0) scale(1);
    }''',
        html
    )

    html = re.sub(
        r'\.control-center-popover\s*\{[\s\S]*?z-index:\s*10000;[\s\S]*?\}',
        '''.control-center-popover {
      position: absolute;
      top: 36px;
      right: 14px;
      width: 320px;
      background: var(--bg-acrylic-heavy);
      backdrop-filter: blur(40px) saturate(220%);
      -webkit-backdrop-filter: blur(40px) saturate(220%);
      border: 1px solid var(--border-acrylic);
      border-radius: 18px;
      box-shadow: 0 28px 80px rgba(0, 0, 0, 0.7), 0 0 1px rgba(255, 255, 255, 0.3);
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      z-index: 10000;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-14px) scale(0.96);
      transform-origin: top right;
      transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
    }''',
        html
    )

    html = re.sub(
        r'\.control-center-popover\.open\s*\{[\s\S]*?\}',
        '''.control-center-popover.open {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0) scale(1);
    }''',
        html
    )

    # 3. Update Camera CSS for full professional features and precision mirror flip
    new_camera_css = '''    /* =========================================================================
       CAMERA APPLICATION (PROFESSIONAL STUDIO ENGINE)
       ========================================================================= */
    .camera-container {
      display: flex;
      flex-direction: column;
      height: 100%;
      background: #000000;
      position: relative;
      user-select: none;
    }

    .camera-viewfinder-frame {
      flex: 1;
      position: relative;
      background: #06070B;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      cursor: crosshair;
    }

    #camera-video, #camera-canvas {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform-origin: center center;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), filter 0.2s ease;
    }

    /* Top HUD */
    .camera-hud-top {
      position: absolute;
      top: 12px;
      left: 14px;
      right: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(14, 15, 22, 0.72);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      padding: 6px 14px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 11px;
      z-index: 20;
    }

    .cam-btn-pill {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 6px;
      padding: 4px 8px;
      color: #E2E2F0;
      cursor: pointer;
      font-size: 11px;
      font-weight: 500;
      transition: all 0.15s;
    }

    .cam-btn-pill:hover {
      background: rgba(255, 255, 255, 0.16);
      color: #FFFFFF;
    }

    .cam-btn-pill.active {
      background: rgba(0, 210, 255, 0.2);
      border-color: #00D2FF;
      color: #00D2FF;
      font-weight: 600;
    }

    /* Interactive Focus Box */
    .camera-focus-box {
      position: absolute;
      width: 64px;
      height: 64px;
      border: 1.5px solid #00D2FF;
      pointer-events: none;
      transform: translate(-50%, -50%) scale(1);
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s;
      z-index: 15;
      display: none;
    }

    .camera-focus-box::before {
      content: "";
      position: absolute;
      top: 50%;
      left: 50%;
      width: 4px;
      height: 4px;
      background: #00D2FF;
      border-radius: 50%;
      transform: translate(-50%, -50%);
    }

    /* Countdown Overlay */
    .cam-countdown-overlay {
      position: absolute;
      font-size: 88px;
      font-weight: 800;
      color: #00D2FF;
      text-shadow: 0 0 35px rgba(0, 210, 255, 0.8), 0 4px 20px rgba(0, 0, 0, 0.8);
      z-index: 25;
      pointer-events: none;
      display: none;
      animation: countdownPulse 0.9s infinite ease-in-out;
    }

    @keyframes countdownPulse {
      0% { transform: scale(1.2); opacity: 0.8; }
      50% { transform: scale(0.95); opacity: 1; }
      100% { transform: scale(1.1); opacity: 0.8; }
    }

    /* Zoom Quick Bar */
    .cam-zoom-bar {
      position: absolute;
      bottom: 128px;
      display: flex;
      gap: 6px;
      background: rgba(14, 15, 22, 0.7);
      backdrop-filter: blur(20px);
      padding: 4px 8px;
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      z-index: 20;
    }

    .cam-zoom-btn {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: transparent;
      border: none;
      color: #FFF;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s;
    }

    .cam-zoom-btn.active {
      background: rgba(255, 255, 255, 0.22);
      color: #00D2FF;
    }

    /* Bottom Controls */
    .camera-hud-bottom {
      position: absolute;
      bottom: 14px;
      left: 14px;
      right: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      background: rgba(14, 15, 22, 0.80);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      padding: 12px 16px;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      z-index: 20;
    }

    .camera-modes-bar {
      display: flex;
      gap: 16px;
      font-size: 11px;
      font-weight: 600;
      color: #8E8EA0;
      letter-spacing: 0.5px;
    }

    .cam-mode-item {
      cursor: pointer;
      transition: color 0.15s;
    }

    .cam-mode-item.active {
      color: #00D2FF;
    }

    .camera-shutter-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      max-width: 420px;
    }

    .shutter-btn {
      width: 62px;
      height: 62px;
      border-radius: 50%;
      border: 4px solid #FFFFFF;
      background: transparent;
      padding: 3px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.1s;
    }

    .shutter-btn:active {
      transform: scale(0.92);
    }

    .shutter-inner {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: #FFFFFF;
      transition: background 0.2s, border-radius 0.2s, transform 0.2s;
    }

    .shutter-btn.recording .shutter-inner {
      background: #FF453A;
      border-radius: 8px;
      transform: scale(0.65);
    }

    /* Pro Controls Drawer */
    .cam-pro-drawer {
      display: none;
      width: 100%;
      background: rgba(0, 0, 0, 0.4);
      border-radius: 8px;
      padding: 8px 12px;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 12px;
      font-size: 10px;
      color: #A6A6BC;
    }

    .camera-flash {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #FFFFFF;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.08s ease-out;
      z-index: 30;
    }

    /* Quick Photo Review Modal */
    .cam-review-modal {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(5, 6, 10, 0.92);
      backdrop-filter: blur(30px);
      z-index: 40;
      display: none;
      flex-direction: column;
      padding: 16px;
    }
'''

    # Replace old camera CSS block
    html = re.sub(r'\.camera-container\s*\{[\s\S]*?\.camera-flash\s*\{[^}]*\}', new_camera_css, html)

    # 4. Update Camera Window Markup (#win-camera)
    new_camera_window_html = '''  <div class="window" id="win-camera" style="top: 75px; left: 280px; width: 840px; height: 570px; display: none;">
    <div class="window-header" onmousedown="startDrag(event, 'win-camera')">
      <div class="traffic-lights">
        <div class="traffic-light tl-close" onclick="closeWindow('win-camera')">&times;</div>
        <div class="traffic-light tl-minimize" onclick="minimizeWindow('win-camera')">-</div>
        <div class="traffic-light tl-maximize" onclick="maximizeWindow('win-camera')">+</div>
      </div>
      <span class="window-title">DAXOS Studio Camera &bull; Vision Pro HDR Engine</span>
    </div>
    <div class="window-content">
      <div class="camera-container" id="camera-main-container">
        <div class="camera-flash" id="camera-flash"></div>

        <!-- Viewfinder Viewport -->
        <div class="camera-viewfinder-frame" id="camera-viewfinder" onclick="handleViewfinderClick(event)">
          <video id="camera-video" autoplay playsinline style="display: none;"></video>
          <canvas id="camera-canvas" width="800" height="520"></canvas>

          <!-- Interactive Focus Box -->
          <div class="camera-focus-box" id="camera-focus-box"></div>

          <!-- Countdown Overlay -->
          <div class="cam-countdown-overlay" id="cam-countdown-overlay">3</div>

          <!-- Top HUD -->
          <div class="camera-hud-top">
            <div style="display: flex; align-items: center; gap: 8px;">
              <button class="cam-btn-pill" id="cam-flash-btn" onclick="cycleFlash(event)">FLASH: AUTO</button>
              <button class="cam-btn-pill" id="cam-timer-btn" onclick="cycleTimer(event)">TIMER: MATI</button>
              <button class="cam-btn-pill" id="cam-ratio-btn" onclick="cycleAspectRatio(event)">16:9</button>
            </div>

            <!-- Central Precision Mirror Toggle -->
            <button class="cam-btn-pill active" id="cam-mirror-btn" onclick="toggleCameraMirror(event)" title="Ubah Orientasi: Cermin Natural vs Presisi Asli 1:1" style="display: flex; align-items: center; gap: 5px;">
              <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24"><path d="M8 7 L3 12 L8 17 M16 7 L21 12 L16 17 M12 3 V21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              <span id="cam-mirror-label">PRESISI ASLI 1:1 (UNMIRRORED)</span>
            </button>

            <div style="display: flex; align-items: center; gap: 8px;">
              <button class="cam-btn-pill" id="cam-grid-btn" onclick="cycleGrid(event)">GRID: 3x3</button>
              <button class="cam-btn-pill" id="cam-res-btn" onclick="cycleResolution(event)">4K UHD 60fps</button>
              <button class="cam-btn-pill" id="cam-pro-btn" onclick="toggleProDrawer(event)">PRO MANUAL</button>
            </div>
          </div>

          <!-- Quick Zoom Buttons (0.5x, 1x, 2x, 5x) -->
          <div class="cam-zoom-bar">
            <button class="cam-zoom-btn" onclick="setCameraZoom(0.5, this, event)">.5x</button>
            <button class="cam-zoom-btn active" onclick="setCameraZoom(1.0, this, event)">1x</button>
            <button class="cam-zoom-btn" onclick="setCameraZoom(2.0, this, event)">2x</button>
            <button class="cam-zoom-btn" onclick="setCameraZoom(5.0, this, event)">5x</button>
          </div>
        </div>

        <!-- Bottom Controls Bar -->
        <div class="camera-hud-bottom">
          <!-- Pro Manual Adjustment Drawer -->
          <div class="cam-pro-drawer" id="cam-pro-drawer">
            <div>
              <div style="display: flex; justify-content: space-between;">
                <span>ISO SENSOR</span>
                <span id="label-iso" style="color: #00D2FF;">ISO 200</span>
              </div>
              <input type="range" min="50" max="6400" step="50" value="200" style="width: 100%;" oninput="updateIso(this.value)">
            </div>
            <div>
              <div style="display: flex; justify-content: space-between;">
                <span>EXPOSURE (EV)</span>
                <span id="label-ev" style="color: #00D2FF;">+0.0 EV</span>
              </div>
              <input type="range" min="-2.0" max="2.0" step="0.1" value="0.0" style="width: 100%;" oninput="updateEv(this.value)">
            </div>
            <div>
              <div style="display: flex; justify-content: space-between;">
                <span>WHITE BALANCE</span>
                <span id="label-wb" style="color: #00D2FF;">Auto (AWB)</span>
              </div>
              <select style="width: 100%; background: #1C1C26; color: #FFF; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 2px;" onchange="updateWb(this.value)">
                <option value="AWB">Auto (AWB)</option>
                <option value="5600K">Daylight (5600K)</option>
                <option value="3200K">Tungsten (3200K)</option>
                <option value="6500K">Cloudy (6500K)</option>
              </select>
            </div>
          </div>

          <!-- Color Grading Filters (LUTs) -->
          <div class="filter-pills">
            <span class="filter-pill active" onclick="setCameraFilter('normal', this)">Normal</span>
            <span class="filter-pill" onclick="setCameraFilter('vivid', this)">Vivid Pro</span>
            <span class="filter-pill" onclick="setCameraFilter('mono', this)">Studio Mono</span>
            <span class="filter-pill" onclick="setCameraFilter('cyber', this)">Cyber Neon</span>
            <span class="filter-pill" onclick="setCameraFilter('noir', this)">Film Noir</span>
            <span class="filter-pill" onclick="setCameraFilter('amber', this)">Warm Amber</span>
          </div>

          <!-- Modes Selector -->
          <div class="camera-modes-bar">
            <span class="cam-mode-item" onclick="setCamMode('burst', this)">BURST</span>
            <span class="cam-mode-item active" onclick="setCamMode('photo', this)">FOTO</span>
            <span class="cam-mode-item" onclick="setCamMode('portrait', this)">POTRET</span>
            <span class="cam-mode-item" onclick="setCamMode('raw', this)">PRO RAW</span>
            <span class="cam-mode-item" onclick="setCamMode('video', this)">VIDEO</span>
          </div>

          <!-- Shutter Row -->
          <div class="camera-shutter-row">
            <!-- Recent Photo Thumbnail Gallery Button -->
            <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; cursor: pointer; color: #00D2FF;" id="cam-gallery-btn" onclick="openPhotoReview()">
              <span id="cam-gallery-icon">RAW</span>
              <span id="cam-gallery-count" style="font-size: 8px; color: #FFF;">0 FOTO</span>
            </div>

            <!-- Shutter Action Button -->
            <div class="shutter-btn" id="shutter-btn" onclick="triggerShutterAction()">
              <div class="shutter-inner"></div>
            </div>

            <!-- Flip Orientation Quick Button -->
            <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; cursor: pointer;" onclick="toggleCameraMirror(event)" title="Pembalik Arah Cermin / Presisi">
              <svg style="width: 20px; height: 20px;" viewBox="0 0 24 24"><path d="M7 16 L3 12 L7 8 M17 8 L21 12 L17 16 M3 12 H21" fill="none" stroke="#FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
          </div>
        </div>

        <!-- Quick Photo Review Modal -->
        <div class="cam-review-modal" id="cam-review-modal">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-weight: 700; font-size: 13px; color: #FFF;">Hasil Tangkapan Kamera &bull; QuickLook</div>
            <button class="btn btn-secondary" style="font-size: 11px; padding: 4px 10px;" onclick="closePhotoReview()">Tutup</button>
          </div>
          <div style="flex: 1; display: flex; align-items: center; justify-content: center; background: #000; border-radius: 8px; overflow: hidden; margin-bottom: 12px;">
            <canvas id="review-canvas" width="640" height="380" style="max-width: 100%; max-height: 100%;"></canvas>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #A6A6BC;">
            <div id="review-exif-info">4096x2304 &bull; RAW DNG 16-bit &bull; ISO 200 &bull; 1/120s &bull; f/1.8 &bull; Vulkan 1.3</div>
            <button class="btn btn-primary" style="font-size: 11px; padding: 5px 14px;" onclick="alert('[OK] Foto berhasil disimpan ke DAXOS Pictures/Camera_Capture.raw!')">Simpan Foto</button>
          </div>
        </div>
      </div>
    </div>
  </div>'''

    html = re.sub(r'<div class="window" id="win-camera"[\s\S]*?<!-- ========================================================================\s*WINDOW: TERMINAL APPLICATION',
                  new_camera_window_html + '\n\n  <!-- ========================================================================\n       WINDOW: TERMINAL APPLICATION', html)

    # 5. Update Window Management Functions (openApp, closeWindow, minimizeWindow, maximizeWindow)
    new_window_js = '''    // =========================================================================
    // macOS-STYLE WINDOW ANIMATIONS & CONTROLS ENGINE
    // =========================================================================
    let highestZ = 100;
    let installerStep = 1;

    function bringToFront(windowId, appName) {
      highestZ += 2;
      const win = document.getElementById(windowId);
      if (win) {
        win.style.zIndex = highestZ;
        document.querySelectorAll('.window').forEach(w => w.classList.remove('focused'));
        win.classList.add('focused');
      }
      if (appName) {
        const titleEl = document.getElementById('menu-active-app');
        if (titleEl) titleEl.textContent = appName;
      }
    }

    function openApp(windowId, appName) {
      const win = document.getElementById(windowId);
      if (!win) return;

      const isMin = win.classList.contains('minimized');
      const isClosed = win.style.display === "none";

      const dot = document.getElementById('dot-' + windowId);
      const dockItem = dot ? dot.closest('.dock-item') : null;
      const dockRect = dockItem ? dockItem.getBoundingClientRect() : {
        left: window.innerWidth / 2 - 25,
        top: window.innerHeight - 50,
        width: 50,
        height: 50
      };

      if (isMin) {
        // macOS Unminimizing / Restore from Dock Animation
        const winRect = win.getBoundingClientRect();
        const startX = (dockRect.left + dockRect.width / 2) - (winRect.left + winRect.width / 2);
        const startY = (dockRect.top + dockRect.height / 2) - (winRect.top + winRect.height / 2);

        win.classList.remove('minimized');
        win.style.display = "flex";
        win.classList.add('window-restoring');
        win.style.transform = `translate(${startX}px, ${startY}px) scale(0.08)`;
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
        }, 340);
      } else if (isClosed) {
        // macOS Pop-in Opening Animation
        win.style.display = "flex";
        win.classList.remove('minimized', 'window-closing');
        win.classList.add('window-opening');
        setTimeout(() => {
          win.classList.remove('window-opening');
        }, 270);
      } else {
        // Already open: subtle pulse to indicate focus
        win.style.transform = 'scale(1.015)';
        setTimeout(() => win.style.transform = '', 140);
      }

      bringToFront(windowId, appName);
      if (dot) dot.classList.add('active');

      if (windowId === 'win-camera') {
        initCamera();
      }
    }

    function closeWindow(windowId) {
      const win = document.getElementById(windowId);
      if (!win || win.style.display === "none") return;

      // macOS Closing Zoom-out Animation
      win.classList.remove('window-opening', 'window-restoring', 'window-minimizing');
      win.classList.add('window-closing');

      setTimeout(() => {
        win.style.display = "none";
        win.classList.remove('window-closing');
        const dot = document.getElementById('dot-' + windowId);
        if (dot) dot.classList.remove('active');
      }, 190);
    }

    function minimizeWindow(windowId) {
      const win = document.getElementById(windowId);
      if (!win || win.style.display === "none") return;

      // Calculate relative vector to dock item
      const dot = document.getElementById('dot-' + windowId);
      const dockItem = dot ? dot.closest('.dock-item') : null;
      const dockRect = dockItem ? dockItem.getBoundingClientRect() : {
        left: window.innerWidth / 2 - 25,
        top: window.innerHeight - 50,
        width: 50,
        height: 50
      };

      const winRect = win.getBoundingClientRect();
      const targetX = (dockRect.left + dockRect.width / 2) - (winRect.left + winRect.width / 2);
      const targetY = (dockRect.top + dockRect.height / 2) - (winRect.top + winRect.height / 2);

      // macOS Minimizing Scale to Dock Animation
      win.classList.remove('window-opening', 'window-closing', 'window-restoring');
      win.classList.add('window-minimizing');
      win.style.transform = `translate(${targetX}px, ${targetY}px) scale(0.08)`;
      win.style.opacity = '0';
      win.style.filter = 'blur(4px)';

      setTimeout(() => {
        win.classList.add('minimized');
        win.classList.remove('window-minimizing');
        win.style.display = 'none';
        win.style.transform = '';
        win.style.opacity = '';
        win.style.filter = '';
      }, 340);
    }

    function maximizeWindow(windowId) {
      const win = document.getElementById(windowId);
      if (!win) return;

      if (win.dataset.maximized === "true") {
        // macOS Unmaximize / Restore Bounds Animation
        win.style.top = win.dataset.origTop;
        win.style.left = win.dataset.origLeft;
        win.style.width = win.dataset.origWidth;
        win.style.height = win.dataset.origHeight;
        win.style.borderRadius = "14px";
        win.dataset.maximized = "false";
      } else {
        // macOS Maximize Animation (Leaves top bar and dock accessible)
        win.dataset.origTop = win.style.top || (win.offsetTop + "px");
        win.dataset.origLeft = win.style.left || (win.offsetLeft + "px");
        win.dataset.origWidth = win.style.width || (win.offsetWidth + "px");
        win.dataset.origHeight = win.style.height || (win.offsetHeight + "px");

        win.style.top = "36px";
        win.style.left = "16px";
        win.style.width = "calc(100vw - 32px)";
        win.style.height = "calc(100vh - 122px)";
        win.style.borderRadius = "12px";
        win.dataset.maximized = "true";
      }
    }
'''

    html = re.sub(r'// =========================================================================\s*// STATE & WINDOW CONTROLS[\s\S]*?function maximizeWindow\(windowId\) \{[\s\S]*?\}\s*\}', new_window_js, html)

    # 6. Update Camera JavaScript Engine
    new_camera_js = '''    // =========================================================================
    // DAXOS STUDIO CAMERA ENGINE (PROFESSIONAL PRECISION & MIRROR CONTROLLER)
    // =========================================================================
    let isMirrored = false; // Default: Presisi Asli 1:1 (True-Sight, Unmirrored)
    let cameraMode = "photo"; // photo, burst, portrait, raw, video
    let isRecording = false;
    let cameraTimer = 0; // 0, 3, 5, 10
    let cameraFlash = "AUTO"; // AUTO, ON, OFF
    let cameraGrid = "3x3"; // 3x3, cross, off
    let cameraRatio = "16:9"; // 16:9, 4:3, 1:1, 21:9
    let zoomLevel = 1.0;
    let shutterCount = 0;
    let currentFilter = "normal";
    let proDrawerOpen = false;
    let currentIso = 200;
    let currentEv = "+0.0 EV";
    let currentWb = "AWB";
    let capturedFrames = [];

    function initCamera() {
      const video = document.getElementById('camera-video');
      const canvas = document.getElementById('camera-canvas');
      const ctx = canvas.getContext('2d');

      applyCameraTransform();

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
          .then(stream => {
            video.srcObject = stream;
            video.style.display = "block";
            canvas.style.display = "none";
          })
          .catch(() => {
            renderSimulatedCamera(ctx, canvas);
          });
      } else {
        renderSimulatedCamera(ctx, canvas);
      }
    }

    function toggleCameraMirror(e) {
      if (e) e.stopPropagation();
      isMirrored = !isMirrored;
      applyCameraTransform();

      const label = document.getElementById('cam-mirror-label');
      const btn = document.getElementById('cam-mirror-btn');
      if (isMirrored) {
        label.textContent = "CERMIN NATURAL (MIRRORED)";
        btn.classList.add('active');
      } else {
        label.textContent = "PRESISI ASLI 1:1 (UNMIRRORED)";
        btn.classList.add('active');
      }
    }

    function applyCameraTransform() {
      const video = document.getElementById('camera-video');
      const canvas = document.getElementById('camera-canvas');
      const target = (video && video.style.display !== "none") ? video : canvas;
      if (!target) return;

      const scaleX = isMirrored ? -zoomLevel : zoomLevel;
      const scaleY = zoomLevel;
      target.style.transform = `scale(${scaleX}, ${scaleY})`;
    }

    function setCameraZoom(val, btn, e) {
      if (e) e.stopPropagation();
      zoomLevel = parseFloat(val);
      document.querySelectorAll('.cam-zoom-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyCameraTransform();
    }

    function cycleFlash(e) {
      if (e) e.stopPropagation();
      const btn = document.getElementById('cam-flash-btn');
      if (cameraFlash === "AUTO") cameraFlash = "ON";
      else if (cameraFlash === "ON") cameraFlash = "OFF";
      else cameraFlash = "AUTO";
      btn.textContent = "FLASH: " + cameraFlash;
    }

    function cycleTimer(e) {
      if (e) e.stopPropagation();
      const btn = document.getElementById('cam-timer-btn');
      if (cameraTimer === 0) cameraTimer = 3;
      else if (cameraTimer === 3) cameraTimer = 5;
      else if (cameraTimer === 5) cameraTimer = 10;
      else cameraTimer = 0;
      btn.textContent = cameraTimer === 0 ? "TIMER: MATI" : `TIMER: ${cameraTimer}S`;
      btn.classList.toggle('active', cameraTimer > 0);
    }

    function cycleAspectRatio(e) {
      if (e) e.stopPropagation();
      const btn = document.getElementById('cam-ratio-btn');
      const vf = document.getElementById('camera-viewfinder');
      if (cameraRatio === "16:9") {
        cameraRatio = "4:3";
        vf.style.aspectRatio = "4/3";
      } else if (cameraRatio === "4:3") {
        cameraRatio = "1:1";
        vf.style.aspectRatio = "1/1";
      } else if (cameraRatio === "1:1") {
        cameraRatio = "21:9";
        vf.style.aspectRatio = "21/9";
      } else {
        cameraRatio = "16:9";
        vf.style.aspectRatio = "16/9";
      }
      btn.textContent = cameraRatio;
    }

    function cycleGrid(e) {
      if (e) e.stopPropagation();
      const btn = document.getElementById('cam-grid-btn');
      if (cameraGrid === "3x3") cameraGrid = "CROSS";
      else if (cameraGrid === "CROSS") cameraGrid = "OFF";
      else cameraGrid = "3x3";
      btn.textContent = "GRID: " + cameraGrid;
      btn.classList.toggle('active', cameraGrid !== "OFF");
    }

    function cycleResolution(e) {
      if (e) e.stopPropagation();
      const btn = document.getElementById('cam-res-btn');
      if (btn.textContent.includes('4K')) {
        btn.textContent = "1080p 120fps (ProMotion)";
      } else if (btn.textContent.includes('1080p')) {
        btn.textContent = "2K HDR 90fps";
      } else {
        btn.textContent = "4K UHD 60fps";
      }
    }

    function toggleProDrawer(e) {
      if (e) e.stopPropagation();
      proDrawerOpen = !proDrawerOpen;
      const drawer = document.getElementById('cam-pro-drawer');
      const btn = document.getElementById('cam-pro-btn');
      drawer.style.display = proDrawerOpen ? 'grid' : 'none';
      btn.classList.toggle('active', proDrawerOpen);
    }

    function updateIso(v) {
      currentIso = v;
      document.getElementById('label-iso').textContent = "ISO " + v;
    }

    function updateEv(v) {
      const formatted = (parseFloat(v) > 0 ? "+" : "") + parseFloat(v).toFixed(1) + " EV";
      currentEv = formatted;
      document.getElementById('label-ev').textContent = formatted;
    }

    function updateWb(v) {
      currentWb = v;
      document.getElementById('label-wb').textContent = v;
    }

    function setCamMode(mode, el) {
      cameraMode = mode;
      document.querySelectorAll('.cam-mode-item').forEach(m => m.classList.remove('active'));
      el.classList.add('active');

      const shutter = document.getElementById('shutter-btn');
      if (mode === "video") {
        shutter.classList.add('recording');
      } else {
        shutter.classList.remove('recording');
        isRecording = false;
      }
    }

    function setCameraFilter(filterName, el) {
      currentFilter = filterName;
      document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');

      const video = document.getElementById('camera-video');
      const canvas = document.getElementById('camera-canvas');
      const target = (video && video.style.display !== "none") ? video : canvas;
      if (!target) return;

      if (filterName === "vivid") {
        target.style.filter = "saturate(180%) contrast(110%)";
      } else if (filterName === "mono") {
        target.style.filter = "grayscale(100%) contrast(140%) brightness(1.05)";
      } else if (filterName === "cyber") {
        target.style.filter = "hue-rotate(180deg) saturate(160%) contrast(120%)";
      } else if (filterName === "noir") {
        target.style.filter = "grayscale(90%) sepia(25%) contrast(150%)";
      } else if (filterName === "amber") {
        target.style.filter = "sepia(45%) saturate(140%) brightness(1.05)";
      } else {
        target.style.filter = "none";
      }
    }

    function handleViewfinderClick(e) {
      // Interactive Focus Box placement
      const vf = document.getElementById('camera-viewfinder');
      const box = document.getElementById('camera-focus-box');
      const rect = vf.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      box.style.left = x + 'px';
      box.style.top = y + 'px';
      box.style.display = 'block';
      box.style.transform = 'translate(-50%, -50%) scale(1.3)';

      setTimeout(() => {
        box.style.transform = 'translate(-50%, -50%) scale(1)';
      }, 100);

      setTimeout(() => {
        box.style.display = 'none';
      }, 1800);
    }

    function triggerShutterAction() {
      if (cameraTimer > 0) {
        runCountdown(cameraTimer, () => executeCapture());
      } else {
        executeCapture();
      }
    }

    function runCountdown(seconds, onFinish) {
      const overlay = document.getElementById('cam-countdown-overlay');
      let remaining = seconds;
      overlay.textContent = remaining;
      overlay.style.display = 'block';

      const interval = setInterval(() => {
        remaining--;
        if (remaining > 0) {
          overlay.textContent = remaining;
        } else {
          clearInterval(interval);
          overlay.style.display = 'none';
          onFinish();
        }
      }, 900);
    }

    function executeCapture() {
      if (cameraMode === "burst") {
        // Burst: 3 rapid captures
        let shots = 0;
        const burstInterval = setInterval(() => {
          shots++;
          flashAndRecordCapture(`BURST ${shots}/3`);
          if (shots >= 3) clearInterval(burstInterval);
        }, 220);
      } else if (cameraMode === "video") {
        isRecording = !isRecording;
        const shutter = document.getElementById('shutter-btn');
        shutter.classList.toggle('recording', isRecording);
      } else {
        flashAndRecordCapture("RAW DNG");
      }
    }

    function flashAndRecordCapture(typeLabel) {
      const flash = document.getElementById('camera-flash');
      flash.style.opacity = "1";
      setTimeout(() => { flash.style.opacity = "0"; }, 120);

      shutterCount++;
      capturedFrames.push({
        id: shutterCount,
        type: typeLabel,
        iso: currentIso,
        ev: currentEv,
        wb: currentWb,
        mirrored: isMirrored,
        timestamp: new Date().toLocaleTimeString()
      });

      const countEl = document.getElementById('cam-gallery-count');
      if (countEl) countEl.textContent = `${shutterCount} FOTO`;
    }

    function openPhotoReview() {
      if (shutterCount === 0) {
        alert("Belum ada foto yang diambil! Tekan tombol shutter untuk mengambil foto.");
        return;
      }
      const modal = document.getElementById('cam-review-modal');
      const canvas = document.getElementById('review-canvas');
      const ctx = canvas.getContext('2d');
      const last = capturedFrames[capturedFrames.length - 1];

      // Draw snapshot onto review canvas
      ctx.fillStyle = "#0D0E16";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      grad.addColorStop(0, "#00D2FF");
      grad.addColorStop(1, "#BF5AF2");
      ctx.fillStyle = grad;
      ctx.fillRect(40, 40, canvas.width - 80, canvas.height - 80);

      ctx.fillStyle = "#FFFFFF";
      ctx.font = "bold 16px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(`DAXOS STUDIO CAPTURE #${last.id}`, canvas.width / 2, canvas.height / 2 - 10);
      ctx.font = "12px monospace";
      ctx.fillText(`Mode: ${last.type} | Orientasi: ${last.mirrored ? "Cermin (Mirrored)" : "Presisi 1:1 (True-Sight)"}`, canvas.width / 2, canvas.height / 2 + 18);

      document.getElementById('review-exif-info').textContent =
        `Capture #${last.id} &bull; 4096x2304 &bull; ${last.type} &bull; ISO ${last.iso} &bull; ${last.ev} &bull; ${last.timestamp}`;

      modal.style.display = "flex";
    }

    function closePhotoReview() {
      document.getElementById('cam-review-modal').style.display = "none";
    }

    function renderSimulatedCamera(ctx, canvas) {
      const video = document.getElementById('camera-video');
      video.style.display = "none";
      canvas.style.display = "block";

      let frame = 0;
      function loop() {
        if (document.getElementById('win-camera').style.display === "none") return;
        frame++;

        ctx.fillStyle = "#0A0B12";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Dynamic Studio Lighting Background
        const grad = ctx.createRadialGradient(
          canvas.width / 2 + Math.sin(frame * 0.02) * 50,
          canvas.height / 2 + Math.cos(frame * 0.02) * 35,
          15,
          canvas.width / 2,
          canvas.height / 2,
          260
        );
        grad.addColorStop(0, "#00D2FF");
        grad.addColorStop(0.5, "#5856D6");
        grad.addColorStop(1, "#07080F");

        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Rule of Thirds Grid
        if (cameraGrid === "3x3") {
          ctx.strokeStyle = "rgba(255, 255, 255, 0.22)";
          ctx.lineWidth = 1;
          const w3 = canvas.width / 3;
          const h3 = canvas.height / 3;
          ctx.beginPath();
          ctx.moveTo(w3, 0); ctx.lineTo(w3, canvas.height);
          ctx.moveTo(w3 * 2, 0); ctx.lineTo(w3 * 2, canvas.height);
          ctx.moveTo(0, h3); ctx.lineTo(canvas.width, h3);
          ctx.moveTo(0, h3 * 2); ctx.lineTo(canvas.width, h3 * 2);
          ctx.stroke();
        }

        // Horizon Level Indicator
        ctx.strokeStyle = "#30D158";
        ctx.lineWidth = 1.5;
        const cy = canvas.height / 2;
        ctx.beginPath();
        ctx.moveTo(canvas.width / 2 - 80, cy); ctx.lineTo(canvas.width / 2 - 30, cy);
        ctx.moveTo(canvas.width / 2 + 30, cy); ctx.lineTo(canvas.width / 2 + 80, cy);
        ctx.stroke();

        ctx.fillStyle = "#30D158";
        ctx.font = "10px monospace";
        ctx.textAlign = "center";
        ctx.fillText("0.0\u00B0 LEVEL", canvas.width / 2, cy - 8);

        // Technical Reticle
        ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
        ctx.lineWidth = 1;
        const cx = canvas.width / 2;
        ctx.beginPath();
        ctx.moveTo(cx - 18, cy); ctx.lineTo(cx + 18, cy);
        ctx.moveTo(cx, cy - 18); ctx.lineTo(cx, cy + 18);
        ctx.stroke();

        // Direction Orientation Targets (Clear Left vs Right)
        ctx.fillStyle = "#FFFFFF";
        ctx.font = "bold 12px monospace";
        ctx.textAlign = "left";
        ctx.fillText("[ KIRI / LEFT ]", 30, cy + 4);
        ctx.textAlign = "right";
        ctx.fillText("[ KANAN / RIGHT ]", canvas.width - 30, cy + 4);

        // Technical HUD Specs on Canvas
        ctx.textAlign = "left";
        ctx.fillStyle = "#FFFFFF";
        ctx.font = "11px monospace";
        const mirrorStatusStr = isMirrored ? "CERMIN (MIRRORED)" : "PRESISI ASLI 1:1 (UNMIRRORED)";
        ctx.fillText(`24mm f/1.8   1/120s   ${currentIso}   ${currentEv}   ${mirrorStatusStr}`, 20, canvas.height - 24);
        ctx.fillText(`DAXOS PRO VISION HDR   VULKAN 1.3 DMA-BUF ACCELERATED`, 20, canvas.height - 10);

        if (isRecording) {
          ctx.fillStyle = "#FF3B30";
          ctx.font = "bold 13px monospace";
          ctx.fillText(`REC \u25CF 00:0${Math.floor(frame / 60)}:0${Math.floor((frame % 60) / 6)}`, canvas.width - 160, 36);
        }

        requestAnimationFrame(loop);
      }
      loop();
    }
'''

    # Replace old camera JS functions in index.html
    html = re.sub(r'function initCamera\(\)\s*\{[\s\S]*?function setCameraFilter[\s\S]*?\}\s*\}', new_camera_js, html)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Successfully upgraded {INDEX_FILE} with macOS window animations and professional camera engine!")

if __name__ == "__main__":
    update_camera_and_animations()
