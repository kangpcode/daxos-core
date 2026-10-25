#!/usr/bin/env python3
"""
enhance_system_settings_powerful.py

Upgrades DAXOS System Settings (win-settings) in src/ui/desktop_preview/index.html to be:
1. Complete & Powerful ("lengkap powerful") with 5 dedicated high-grade control centers:
   - Layanan & Systemd Daemons (spane-services): Full systemctl / cgroups v2 manager with live 15 daemons, restart, stop, journal logs
   - Performa & DreX-Boost Governor (spane-performance): Realtime CPU/GPU clock, 240Hz Extreme toggle, 85°C safety clamp, fan curves
   - Penyimpanan, Partisi & Btrfs (spane-storage): 512GB visual partition breakdown, cache purger, TRIM optimizer, Btrfs snapshot
   - Pembaruan Sistem OTA A/B (spane-updates): Dual-slot A/B status, live update download simulation, SHA3-512 verification, release channels
   - Bluetooth 5.4 & Periferal (spane-bluetooth): AirPods Max, DualSense, MX Master 3S battery stats and radar device discovery
2. Adds rich interactive JavaScript controllers:
   - restartSystemdService(serviceName)
   - toggleSystemdService(serviceName, btn)
   - viewSystemdServiceLogs(serviceName)
   - setBoostGovernorProfile(profile)
   - purifySystemStorageCache()
   - triggerOtaCheckFromSettings()
   - scheduleNvmeTrim()
   - createBtrfsSnapshotPoint()
   - toggleBluetoothDevice(name)
"""

from pathlib import Path

INDEX_HTML = Path("src/ui/desktop_preview/index.html")

NEW_NAV_ITEMS = """          <div class="settings-nav-item active" id="snav-displays" onclick="switchSettingsTab('displays')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="2"/><line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="2"/></svg>
            <span>Layar &amp; Display</span>
          </div>

          <div class="settings-nav-item" id="snav-appearance" onclick="switchSettingsTab('appearance')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3 A9 9 0 0 1 12 21 Z" fill="currentColor"/></svg>
            <span>Tampilan &amp; DreXUI</span>
          </div>

          <div class="settings-nav-item" id="snav-sound" onclick="switchSettingsTab('sound')">
            <svg style="width: 16px; height: 16px;"><use href="#svg-speaker"/></svg>
            <span>Suara &amp; Audio</span>
          </div>

          <div class="settings-nav-item" id="snav-network" onclick="switchSettingsTab('network')">
            <svg style="width: 16px; height: 16px;"><use href="#svg-wifi"/></svg>
            <span>Jaringan &amp; Wi-Fi</span>
          </div>

          <div class="settings-nav-item" id="snav-bluetooth" onclick="switchSettingsTab('bluetooth')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><path d="M6.5 6.5l11 11L12 23V1l5.5 5.5-11 11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Bluetooth &amp; Periferal</span>
          </div>

          <div class="settings-nav-item" id="snav-services" onclick="switchSettingsTab('services')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="8" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="2" y="14" width="20" height="8" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><line x1="6" y1="6" x2="6.01" y2="6" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><line x1="6" y1="18" x2="6.01" y2="18" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
            <span>Layanan &amp; Systemd</span>
            <span style="margin-left: auto; font-size: 9px; background: rgba(48,209,88,0.2); color: #30D158; padding: 2px 6px; border-radius: 8px; font-weight: 700;">15 AKTIF</span>
          </div>

          <div class="settings-nav-item" id="snav-performance" onclick="switchSettingsTab('performance')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Performa &amp; DreX-Boost</span>
          </div>

          <div class="settings-nav-item" id="snav-storage" onclick="switchSettingsTab('storage')">
            <svg style="width: 16px; height: 16px;"><use href="#icon-disks"/></svg>
            <span>Penyimpanan &amp; Btrfs</span>
          </div>

          <div class="settings-nav-item" id="snav-security" onclick="switchSettingsTab('security')">
            <svg style="width: 16px; height: 16px;"><use href="#svg-shield"/></svg>
            <span>Keamanan &amp; Landlock</span>
          </div>

          <div class="settings-nav-item" id="snav-updates" onclick="switchSettingsTab('updates')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Pembaruan Sistem OTA</span>
          </div>

          <div class="settings-nav-item" id="snav-power" onclick="switchSettingsTab('power')">
            <svg style="width: 16px; height: 16px;"><use href="#svg-battery"/></svg>
            <span>Baterai &amp; Daya</span>
          </div>

          <div class="settings-nav-item" id="snav-daxdrop" onclick="switchSettingsTab('daxdrop')">
            <svg style="width: 16px; height: 16px;"><use href="#icon-daxdrop"/></svg>
            <span>DaXDrop &amp; Air-Grab</span>
          </div>

          <div class="settings-nav-item" id="snav-datetime" onclick="switchSettingsTab('datetime')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><polyline points="12 6 12 12 16 14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            <span>Waktu &amp; Tanggal</span>
          </div>

          <div class="settings-nav-item" id="snav-about" onclick="switchSettingsTab('about')">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><line x1="12" y1="8" x2="12" y2="8" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><line x1="12" y1="12" x2="12" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            <span>Tentang &amp; Spesifikasi</span>
          </div>"""

NEW_SUBPANES = """          <!-- ========================================================================
               PANE: LAYANAN & SYSTEMD SUPERVISOR (CGROUPS V2)
               ======================================================================== -->
          <div class="settings-subpane" id="spane-services" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
              <div>
                <div style="font-size: 18px; font-weight: 700; color: #FFF; margin-bottom: 4px;">Pusat Layanan &amp; Supervisi Systemd</div>
                <div style="font-size: 12px; color: #8E8EA0;">Supervisi 15 daemon sistem DAXOS, socket activation, isolasi cgroups v2, dan journald telemetry.</div>
              </div>
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" onclick="reloadAllSystemdUnits()" style="font-size: 11px; padding: 5px 12px; display: flex; align-items: center; gap: 6px;">
                  <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24"><path d="M23 4v6h-6M1 20v-6h6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" fill="none" stroke="currentColor" stroke-width="2"/></svg>
                  daemon-reload
                </button>
                <button class="btn btn-primary" onclick="restartCompositorGlass()" style="font-size: 11px; padding: 5px 12px;">Restart Compositor</button>
              </div>
            </div>

            <!-- Systemd Telemetry Overview Card -->
            <div class="settings-card" style="background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.25); padding: 14px 18px;">
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px;">
                <div>
                  <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; font-weight: 600;">Status Target</div>
                  <div style="font-size: 14px; font-weight: 700; color: #30D158; margin-top: 2px;">daxos.target (Active)</div>
                </div>
                <div>
                  <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; font-weight: 600;">Total Unit Aktif</div>
                  <div style="font-size: 14px; font-weight: 700; color: #00D2FF; margin-top: 2px;">15 / 15 Layanan</div>
                </div>
                <div>
                  <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; font-weight: 600;">CGroup Root Slice</div>
                  <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-top: 2px;">daxos.slice (2.4% CPU)</div>
                </div>
                <div>
                  <div style="font-size: 10px; color: #9CA3AF; text-transform: uppercase; font-weight: 600;">Socket Activation</div>
                  <div style="font-size: 14px; font-weight: 700; color: #EAB308; margin-top: 2px;">2 Listeners Aktif</div>
                </div>
              </div>
            </div>

            <!-- Cgroups v2 Slices Hierarchy Card -->
            <div class="settings-card">
              <div class="settings-card-title" style="display: flex; align-items: center; gap: 8px;">
                <svg style="width: 14px; height: 14px; color: #00D2FF;" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2" fill="none" stroke="currentColor" stroke-width="2"/><polyline points="2 17 12 22 22 17" fill="none" stroke="currentColor" stroke-width="2"/><polyline points="2 12 12 17 22 12" fill="none" stroke="currentColor" stroke-width="2"/></svg>
                Hirarki Cgroups v2 &amp; Alokasi Bobot Resource
              </div>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-top: 10px;">
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; border-left: 3px solid #00D2FF;">
                  <div style="font-size: 11px; font-weight: 700; color: #FFF;">daxos-system.slice</div>
                  <div style="font-size: 10px; color: #9CA3AF;">Weight: 500 &bull; Min: 256M &bull; Core Daemons</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; border-left: 3px solid #30D158;">
                  <div style="font-size: 11px; font-weight: 700; color: #FFF;">daxos-apps.slice</div>
                  <div style="font-size: 10px; color: #9CA3AF;">Weight: 200 &bull; Max: 14G &bull; Sandboxed Apps</div>
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; border-left: 3px solid #F59E0B;">
                  <div style="font-size: 11px; font-weight: 700; color: #FFF;">daxos-drivers.slice</div>
                  <div style="font-size: 10px; color: #9CA3AF;">Weight: 800 &bull; Max: 4G &bull; DreX-Driver Ring-0/3</div>
                </div>
              </div>
            </div>

            <!-- Daemons Table -->
            <div class="settings-card" style="padding: 0; overflow: hidden;">
              <table style="width: 100%; border-collapse: collapse; font-size: 11.5px; text-align: left;">
                <thead>
                  <tr style="background: rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.08); color: #9CA3AF; font-size: 10px;">
                    <th style="padding: 10px 14px;">UNIT SYSTEMD</th>
                    <th style="padding: 10px 14px;">DESKRIPSI &amp; TANGGUNG JAWAB</th>
                    <th style="padding: 10px 14px;">STATUS</th>
                    <th style="padding: 10px 14px;">MEMORI</th>
                    <th style="padding: 10px 14px; text-align: right;">KONTROL</th>
                  </tr>
                </thead>
                <tbody id="systemd-services-tbody">
                  <!-- Populated dynamically or pre-rendered -->
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dap-registryd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">DAXOS Central System Registry Daemon</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">24.5 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dap-registryd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dap-registryd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dap-sandboxd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Application Sandbox Manager Daemon</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">32.1 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dap-sandboxd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dap-sandboxd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dap-updated.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Atomic A/B OTA Updater Daemon</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">18.4 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dap-updated.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dap-updated.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">drex-boostd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Dynamic Hardware &amp; GPU Governor</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">12.8 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('drex-boostd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('drex-boostd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">drex-compositor.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Wayland Acrylic Glass Dynamic Compositor</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">142.0 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('drex-compositor.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('drex-compositor.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-sysmon.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Realtime Telemetry &amp; System Monitor</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">14.2 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-sysmon.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-sysmon.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-netd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Network &amp; Wireless Manager Daemon</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">16.7 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-netd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-netd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-sec.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Security Center &amp; Hardware Firewall</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">21.0 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-sec.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-sec.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-audiod.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Low-Latency Audio &amp; PipeWire Mixer</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">28.6 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-audiod.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-audiod.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-disks.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Storage Automount &amp; SMART Monitor</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">11.5 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-disks.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-disks.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">daxdrop.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">DaXDrop P2P Discovery &amp; Air-Gesture</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">19.3 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('daxdrop.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('daxdrop.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dap-compat.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Mach-O dyld &amp; Proton NTSync Bridge</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">45.2 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dap-compat.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dap-compat.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-pkgd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Package Registry &amp; Repo Sync Daemon</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">22.8 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-pkgd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-pkgd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-powerd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">ACPI Power Governor &amp; Battery Health</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">8.4 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-powerd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-powerd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 9px 14px; font-family: monospace; color: #00D2FF; font-weight: 600;">dax-bluetoothd.service</td>
                    <td style="padding: 9px 14px; color: #D2D2DE;">Bluetooth 5.4 LE &amp; Spatial Peripheral</td>
                    <td style="padding: 9px 14px;"><span style="background: rgba(48,209,88,0.15); color: #30D158; padding: 2px 7px; border-radius: 6px; font-size: 10px; font-weight: 700;">active (running)</span></td>
                    <td style="padding: 9px 14px; color: #9CA3AF;">15.0 MB</td>
                    <td style="padding: 9px 14px; text-align: right;">
                      <button class="btn btn-secondary" onclick="restartSystemdService('dax-bluetoothd.service')" style="font-size: 10px; padding: 3px 8px;">Restart</button>
                      <button class="btn btn-secondary" onclick="viewSystemdServiceLogs('dax-bluetoothd.service')" style="font-size: 10px; padding: 3px 8px;">Log</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Terminal Journal Log Drawer (Collapsible) -->
            <div id="systemd-log-drawer" style="display: none; background: #0A0D14; border: 1px solid rgba(0, 210, 255, 0.3); border-radius: 10px; padding: 14px; margin-top: 14px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="font-size: 11px; font-weight: 700; color: #00D2FF; font-family: monospace;" id="systemd-log-title">journalctl -u dap-registryd.service -f</div>
                <button class="btn btn-secondary" onclick="document.getElementById('systemd-log-drawer').style.display='none'" style="font-size: 10px; padding: 2px 8px;">Tutup Log</button>
              </div>
              <pre id="systemd-log-content" style="font-family: monospace; font-size: 11px; color: #E5E7EB; margin: 0; line-height: 1.5; max-height: 160px; overflow-y: auto; background: rgba(0,0,0,0.4); padding: 10px; border-radius: 6px;"></pre>
            </div>
          </div>

          <!-- ========================================================================
               PANE: PERFORMA & DREX-BOOST HARDWARE GOVERNOR
               ======================================================================== -->
          <div class="settings-subpane" id="spane-performance" style="display: none;">
            <div style="font-size: 18px; font-weight: 700; color: #FFF; margin-bottom: 4px;">Performa Hardware &amp; DreX-Boost Governor</div>
            <div style="font-size: 12px; color: #8E8EA0; margin-bottom: 20px;">Kelola profil frekuensi clock prosesor, governor beban dinamis, batas suhu 85°C, dan refresh rate 240Hz.</div>

            <!-- Governor Selector Cards -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 16px;">
              <div class="settings-card" id="gov-card-eco" onclick="setBoostGovernorProfile('eco')" style="cursor: pointer; padding: 14px; text-align: center; border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 13px; font-weight: 700; color: #10B981;">Hemat Daya (Eco)</div>
                <div style="font-size: 10px; color: #9CA3AF; margin-top: 4px;">Maks 2.2 GHz &bull; 60Hz &bull; 15W TDP</div>
              </div>
              <div class="settings-card active" id="gov-card-balanced" onclick="setBoostGovernorProfile('balanced')" style="cursor: pointer; padding: 14px; text-align: center; border: 2px solid #00D2FF; background: rgba(0,210,255,0.08);">
                <div style="font-size: 13px; font-weight: 700; color: #00D2FF;">Seimbang (Default)</div>
                <div style="font-size: 10px; color: #9CA3AF; margin-top: 4px;">Dinamis 3.8 GHz &bull; 120Hz &bull; 35W TDP</div>
              </div>
              <div class="settings-card" id="gov-card-perf" onclick="setBoostGovernorProfile('perf')" style="cursor: pointer; padding: 14px; text-align: center; border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 13px; font-weight: 700; color: #F59E0B;">Performa Tinggi (Pro)</div>
                <div style="font-size: 10px; color: #9CA3AF; margin-top: 4px;">Boost 4.8 GHz &bull; 120Hz ProMotion &bull; 54W</div>
              </div>
              <div class="settings-card" id="gov-card-240hz" onclick="setBoostGovernorProfile('240hz')" style="cursor: pointer; padding: 14px; text-align: center; border: 1px solid rgba(255,255,255,0.08);">
                <div style="font-size: 13px; font-weight: 700; color: #EC4899;">DreX-Boost 240Hz</div>
                <div style="font-size: 10px; color: #9CA3AF; margin-top: 4px;">Jitter ≤ 0.38ms &bull; 240Hz &bull; Zero Lag</div>
              </div>
            </div>

            <!-- Hardware Telemetry Meters -->
            <div class="settings-card">
              <div class="settings-card-title">Telemetri Hardware &amp; Suhu (Safety Clamp 85°C)</div>
              <div class="settings-row">
                <span class="settings-row-label">Frekuensi CPU Saat Ini</span>
                <span style="font-size: 12px; font-weight: 700; color: #00D2FF;" id="gov-cpu-freq">3.80 GHz (12 Cores Aktif)</span>
              </div>
              <div class="settings-row">
                <span class="settings-row-label">Frekuensi GPU Engine</span>
                <span style="font-size: 12px; font-weight: 700; color: #FFF;" id="gov-gpu-freq">1,900 MHz (Radeon 660M)</span>
              </div>
              <div class="settings-row">
                <span class="settings-row-label">Suhu Paket (Package Temperature)</span>
                <span style="font-size: 12px; font-weight: 700; color: #10B981;" id="gov-temp-val">52°C (Aman &bull; Ambang Kritis: 85°C)</span>
              </div>
              <div class="settings-row">
                <span class="settings-row-label">UI Rendering Jitter (SCHED_FLAG_DREX_UI_BOOST)</span>
                <span style="font-size: 12px; font-weight: 700; color: #30D158;">0.38 ms (SLA &le; 0.42 ms)</span>
              </div>
            </div>

            <div class="settings-card">
              <div class="settings-card-title">Kurva Kipas &amp; Akustik Pendinginan</div>
              <div class="settings-row">
                <div>
                  <div class="settings-row-label">Mode Kipas Aktif</div>
                  <div class="settings-row-sub">Atur profil kebisingan sistem pendingin vapor chamber</div>
                </div>
                <select class="settings-select" onchange="toast('Profil kipas diubah ke: ' + this.value)">
                  <option value="Dinamis Cerdas">Dinamis Cerdas (Auto Curve)</option>
                  <option value="Senyap Sepenuhnya">Senyap Sepenuhnya (Silent &lt; 22 dB)</option>
                  <option value="Kinerja Penuh 100%">Kinerja Penuh 100% (Turbine Flow)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- ========================================================================
               PANE: PENYIMPANAN & BTRFS SUBVOLUMES
               ======================================================================== -->
          <div class="settings-subpane" id="spane-storage" style="display: none;">
            <div style="font-size: 18px; font-weight: 700; color: #FFF; margin-bottom: 4px;">Penyimpanan, Partisi &amp; Btrfs Subvolume</div>
            <div style="font-size: 12px; color: #8E8EA0; margin-bottom: 20px;">Kelola partisi root immutable EROFS dm-verity, subvolume data pengguna Btrfs, dan optimasi flash NVMe.</div>

            <!-- Visual Storage Bar -->
            <div class="settings-card">
              <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
                <span style="font-size: 14px; font-weight: 700; color: #FFF;">NVMe PCIe 4.0 SSD (512 GB)</span>
                <span style="font-size: 12px; color: #00D2FF; font-weight: 600;">432.4 GB Bebas dari 512 GB</span>
              </div>
              <div style="width: 100%; height: 16px; background: rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden; display: flex; margin-bottom: 12px;">
                <div style="width: 2%; background: #9333EA;" title="EROFS Rootfs (3.2 GB)"></div>
                <div style="width: 13%; background: #00D2FF;" title="Btrfs User Data (68.4 GB)"></div>
                <div style="width: 2%; background: #EAB308;" title="ZRAM Swap (8.0 GB)"></div>
                <div style="width: 83%; background: transparent;" title="Free Space (432.4 GB)"></div>
              </div>
              <div style="display: flex; gap: 16px; flex-wrap: wrap; font-size: 11px;">
                <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 8px; height: 8px; background: #9333EA; border-radius: 2px;"></div><span style="color: #9CA3AF;">EROFS Root: 3.2 GB</span></div>
                <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 8px; height: 8px; background: #00D2FF; border-radius: 2px;"></div><span style="color: #9CA3AF;">Btrfs Data: 68.4 GB</span></div>
                <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 8px; height: 8px; background: #EAB308; border-radius: 2px;"></div><span style="color: #9CA3AF;">ZRAM zstd: 8.0 GB</span></div>
                <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 8px; height: 8px; background: #374151; border-radius: 2px;"></div><span style="color: #9CA3AF;">Tersedia: 432.4 GB</span></div>
              </div>
            </div>

            <!-- Storage Maintenance Actions -->
            <div class="settings-card">
              <div class="settings-card-title">Pemeliharaan &amp; Optimasi Penyimpanan</div>
              <div class="settings-row">
                <div>
                  <div class="settings-row-label">Pembersihan Cache &amp; Berkas Sementara</div>
                  <div class="settings-row-sub">Hapus cache compiler dcodx, log lama, dan berkas sampah sistem</div>
                </div>
                <button class="btn btn-secondary" onclick="purifySystemStorageCache()" style="font-size: 11px; padding: 6px 14px;">Bersihkan Sekarang</button>
              </div>
              <div class="settings-row">
                <div>
                  <div class="settings-row-label">Jadwalkan NVMe SSD TRIM (fstrim.timer)</div>
                  <div class="settings-row-sub">Kirim sinyal TRIM blok kosong ke controller SSD untuk menjaga kecepatan baca/tulis</div>
                </div>
                <button class="btn btn-secondary" onclick="scheduleNvmeTrim()" style="font-size: 11px; padding: 6px 14px;">Jalankan TRIM</button>
              </div>
              <div class="settings-row">
                <div>
                  <div class="settings-row-label">Buat Snapshot CoW Btrfs Sistem</div>
                  <div class="settings-row-sub">Simpan snapshot atomik subvolume untuk checkpoint cadangan instan</div>
                </div>
                <button class="btn btn-primary" onclick="createBtrfsSnapshotPoint()" style="font-size: 11px; padding: 6px 14px;">Buat Snapshot</button>
              </div>
            </div>
          </div>

          <!-- ========================================================================
               PANE: PEMBARUAN SISTEM OTA (ATOMIC A/B)
               ======================================================================== -->
          <div class="settings-subpane" id="spane-updates" style="display: none;">
            <div style="font-size: 18px; font-weight: 700; color: #FFF; margin-bottom: 4px;">Pembaruan Sistem Operasi DAXOS (Atomic OTA)</div>
            <div style="font-size: 12px; color: #8E8EA0; margin-bottom: 20px;">Pembaruan partisi atomik A/B terpusat via DaXCloud dengan kriptografi SHA3-512 dan rollback otomatis GRUB 2.12.</div>

            <!-- Slot Status Card -->
            <div class="settings-card">
              <div class="settings-card-title">Status Partisi Dual-Slot GRUB 2.12</div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px;">
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 12px;">
                  <div style="font-size: 10px; color: #30D158; font-weight: 700; text-transform: uppercase;">Slot A &bull; AKTIF (RUNNING)</div>
                  <div style="font-size: 13px; font-weight: 700; color: #FFF; margin-top: 2px;">DAXOS 1.10.2026 LTS</div>
                  <div style="font-size: 10px; color: #9CA3AF; margin-top: 2px;">/dev/nvme0n1p2 &bull; dm-verity SHA3-512 Verified</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px;">
                  <div style="font-size: 10px; color: #00D2FF; font-weight: 700; text-transform: uppercase;">Slot B &bull; SIAGA (STANDBY)</div>
                  <div style="font-size: 13px; font-weight: 700; color: #FFF; margin-top: 2px;">Siap Menerima OTA Delta</div>
                  <div style="font-size: 10px; color: #9CA3AF; margin-top: 2px;">/dev/nvme0n1p3 &bull; Staging Slot Target</div>
                </div>
              </div>
            </div>

            <!-- Update Channels & Check -->
            <div class="settings-card">
              <div class="settings-card-title">Saluran Rilis Pembaruan (Release Channel)</div>
              <div class="settings-row">
                <span class="settings-row-label">Pilih Saluran Distribusi</span>
                <select class="settings-select" onchange="toast('Saluran pembaruan diubah ke: ' + this.value)">
                  <option value="Stable">Stable (Stabil &amp; Disarankan)</option>
                  <option value="Beta">Beta (Pratinjau Fitur Terverifikasi)</option>
                  <option value="Nightly">Nightly (Build Otomatis Harian)</option>
                  <option value="Canary">Canary (Eksperimental Mutakhir)</option>
                </select>
              </div>
              <div style="margin-top: 14px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                  <div style="font-size: 12px; font-weight: 600; color: #FFF;" id="ota-status-label">Sistem Operasi DAXOS Terkini &bull; Versi 1.10.2026</div>
                  <div style="font-size: 10px; color: #9CA3AF;" id="ota-last-checked">Terakhir diperiksa: Hari ini pukul 06:15</div>
                </div>
                <button class="btn btn-primary" id="btn-check-ota" onclick="triggerOtaCheckFromSettings()" style="font-size: 11px; padding: 7px 18px;">
                  Periksa Pembaruan
                </button>
              </div>
              <div id="ota-progress-bar-container" style="display: none; margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #9CA3AF; margin-bottom: 4px;">
                  <span id="ota-progress-task">Mengunduh paket delta DAXOS...</span>
                  <span id="ota-progress-pct">0%</span>
                </div>
                <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;">
                  <div id="ota-progress-fill" style="width: 0%; height: 100%; background: #00D2FF; transition: width 0.2s;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- ========================================================================
               PANE: BLUETOOTH & PERIFERAL
               ======================================================================== -->
          <div class="settings-subpane" id="spane-bluetooth" style="display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
              <div>
                <div style="font-size: 18px; font-weight: 700; color: #FFF; margin-bottom: 4px;">Bluetooth 5.4 &amp; Periferal Input</div>
                <div style="font-size: 12px; color: #8E8EA0;">Kelola headphone spatial audio, kontroler game, dan perangkat Bluetooth Low-Energy.</div>
              </div>
              <label class="switch">
                <input type="checkbox" checked onchange="toast('Bluetooth: ' + (this.checked ? 'Diaktifkan' : 'Dinonaktifkan'))">
                <span class="slider round"></span>
              </label>
            </div>

            <!-- Connected Devices List -->
            <div class="settings-card">
              <div class="settings-card-title">Perangkat Terhubung Saat Ini</div>
              <div class="settings-row">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <svg style="width: 20px; height: 20px; color: #00D2FF;" viewBox="0 0 24 24"><path d="M3 18v-6a9 9 0 0 1 18 0v6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z" fill="currentColor"/></svg>
                  <div>
                    <div style="font-size: 12px; font-weight: 700; color: #FFF;">AirPods Max &bull; Space Black</div>
                    <div style="font-size: 10px; color: #30D158;">Terhubung &bull; Spatial Audio 3D HRTF Aktif &bull; Baterai 94%</div>
                  </div>
                </div>
                <button class="btn btn-secondary" onclick="toast('AirPods Max diputuskan')" style="font-size: 10px; padding: 4px 10px;">Putuskan</button>
              </div>
              <div class="settings-row">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <svg style="width: 20px; height: 20px; color: #EC4899;" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="6" fill="none" stroke="currentColor" stroke-width="2"/><polygon points="6 12 8 10 8 14" fill="currentColor"/><circle cx="16" cy="10" r="1.5" fill="currentColor"/><circle cx="18" cy="12" r="1.5" fill="currentColor"/></svg>
                  <div>
                    <div style="font-size: 12px; font-weight: 700; color: #FFF;">DualSense Wireless Controller</div>
                    <div style="font-size: 10px; color: #30D158;">Terhubung &bull; Low Latency 1.2 ms &bull; Baterai 82%</div>
                  </div>
                </div>
                <button class="btn btn-secondary" onclick="toast('DualSense diputuskan')" style="font-size: 10px; padding: 4px 10px;">Putuskan</button>
              </div>
              <div class="settings-row">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <svg style="width: 20px; height: 20px; color: #A855F7;" viewBox="0 0 24 24"><rect x="6" y="3" width="12" height="18" rx="6" fill="none" stroke="currentColor" stroke-width="2"/><line x1="12" y1="7" x2="12" y2="11" stroke="currentColor" stroke-width="2"/></svg>
                  <div>
                    <div style="font-size: 12px; font-weight: 700; color: #FFF;">Logitech MX Master 3S</div>
                    <div style="font-size: 10px; color: #30D158;">Terhubung &bull; Sensor 8K DPI &bull; Baterai 88%</div>
                  </div>
                </div>
                <button class="btn btn-secondary" onclick="toast('Mouse diputuskan')" style="font-size: 10px; padding: 4px 10px;">Putuskan</button>
              </div>
            </div>

            <!-- Discovery Card -->
            <div class="settings-card" style="text-align: center; padding: 20px;">
              <div style="font-size: 12px; font-weight: 700; color: #FFF; margin-bottom: 4px;">Pindai Perangkat Baru</div>
              <div style="font-size: 11px; color: #9CA3AF; margin-bottom: 12px;">Pastikan perangkat Bluetooth Anda dalam mode pairing (dapat ditemukan).</div>
              <button class="btn btn-secondary" onclick="toast('Memindai perangkat Bluetooth sekitar...')" style="font-size: 11px; padding: 6px 16px;">
                Cari Perangkat Sekitar
              </button>
            </div>
          </div>"""

JS_CONTROLLERS = """
    // =========================================================================
    // POWERFUL SYSTEM SETTINGS CONTROLLER SUITE
    // =========================================================================
    function restartSystemdService(serviceName) {
      toast("Me-restart unit systemd '" + serviceName + "'...");
      setTimeout(() => {
        toast("Service '" + serviceName + "' aktif kembali (SLA < 45 ms)");
      }, 350);
    }

    function toggleSystemdService(serviceName, btn) {
      const isRunning = btn.textContent.includes('Stop');
      if (isRunning) {
        btn.textContent = 'Start';
        toast("Sinyal SIGTERM dikirim ke '" + serviceName + "'");
      } else {
        btn.textContent = 'Stop';
        toast("Service '" + serviceName + "' dijalankan di daxos-system.slice");
      }
    }

    function reloadAllSystemdUnits() {
      toast("Mengeksekusi 'systemctl daemon-reload'...");
      setTimeout(() => {
        toast("Seluruh 15 unit systemd dan cgroups dikonfigurasi ulang!");
      }, 400);
    }

    function restartCompositorGlass() {
      toast("Memuat ulang DreX-Compositor Acrylic Glass Shader...");
      setTimeout(() => {
        toast("DreX-Compositor berhasil dimuat ulang tanpa flicker!");
      }, 300);
    }

    function viewSystemdServiceLogs(serviceName) {
      const drawer = document.getElementById('systemd-log-drawer');
      const title = document.getElementById('systemd-log-title');
      const content = document.getElementById('systemd-log-content');
      if (!drawer || !title || !content) return;

      drawer.style.display = 'block';
      title.textContent = "journalctl -u " + serviceName + " -n 12 --no-pager";

      const now = new Date().toTimeString().split(' ')[0];
      content.textContent = 
        now + " daxos-node systemd[1]: Starting " + serviceName + "...\\n" +
        now + " daxos-node " + serviceName + "[1024]: [BOOT] Initialized under slice 'daxos-system.slice'\\n" +
        now + " daxos-node " + serviceName + "[1024]: [SECURITY] Landlock LSM ABI v5 enforced, 412 syscalls restricted\\n" +
        now + " daxos-node " + serviceName + "[1024]: [IPC] Bound to Unix Domain Socket /run/daxos/" + serviceName.replace('.service', '.sock') + "\\n" +
        now + " daxos-node " + serviceName + "[1024]: [HEARTBEAT] Ready for requests (Watchdog SLA <= 45ms)\\n" +
        now + " daxos-node systemd[1]: Started " + serviceName + " [OK]";
    }

    function setBoostGovernorProfile(profile) {
      ['eco', 'balanced', 'perf', '240hz'].forEach(p => {
        const c = document.getElementById('gov-card-' + p);
        if (c) {
          c.classList.remove('active');
          c.style.border = '1px solid rgba(255,255,255,0.08)';
          c.style.background = 'rgba(255,255,255,0.03)';
        }
      });
      const activeCard = document.getElementById('gov-card-' + profile);
      if (activeCard) {
        activeCard.classList.add('active');
        activeCard.style.border = '2px solid #00D2FF';
        activeCard.style.background = 'rgba(0,210,255,0.08)';
      }

      const cpuFreq = document.getElementById('gov-cpu-freq');
      const tempVal = document.getElementById('gov-temp-val');
      if (profile === 'eco') {
        if (cpuFreq) cpuFreq.textContent = "2.20 GHz (Power Saver &bull; 15W)";
        if (tempVal) tempVal.textContent = "42°C (Sangat Dingin)";
        toast("Profil DreX-Boost diubah ke: Hemat Daya (Eco)");
      } else if (profile === 'balanced') {
        if (cpuFreq) cpuFreq.textContent = "3.80 GHz (Dinamis &bull; 35W)";
        if (tempVal) tempVal.textContent = "52°C (Aman &bull; 85°C Cutoff)";
        toast("Profil DreX-Boost diubah ke: Seimbang (Balanced)");
      } else if (profile === 'perf') {
        if (cpuFreq) cpuFreq.textContent = "4.80 GHz (Full Turbo &bull; 54W)";
        if (tempVal) tempVal.textContent = "68°C (Kinerja Tinggi)";
        toast("Profil DreX-Boost diubah ke: Performa Tinggi (Pro)");
      } else if (profile === '240hz') {
        if (cpuFreq) cpuFreq.textContent = "4.95 GHz (SCHED_FLAG_DREX_UI_BOOST &bull; 65W)";
        if (tempVal) tempVal.textContent = "74°C (Gaming 240Hz &bull; Jitter <= 0.38ms)";
        toast("Profil DreX-Boost diubah ke: Ekstrem Gaming 240Hz");
      }
    }

    function purifySystemStorageCache() {
      toast("Membersihkan cache build DCODX, log lama, dan berkas sementara...");
      setTimeout(() => {
        toast("Berhasil membersihkan 4.12 GB ruang penyimpanan SSD!");
      }, 600);
    }

    function scheduleNvmeTrim() {
      toast("Menjalankan TRIM SSD pada /dev/nvme0n1...");
      setTimeout(() => {
        toast("TRIM selesai: 432.4 GB blok kosong telah dibebaskan!");
      }, 500);
    }

    function createBtrfsSnapshotPoint() {
      const snapName = "snap-root-" + new Date().toISOString().slice(0,10);
      toast("Membuat snapshot Btrfs CoW: '" + snapName + "'...");
      setTimeout(() => {
        toast("Snapshot Btrfs '" + snapName + "' berhasil dibuat dalam 12 ms!");
      }, 400);
    }

    function triggerOtaCheckFromSettings() {
      const btn = document.getElementById('btn-check-ota');
      const status = document.getElementById('ota-status-label');
      const progressContainer = document.getElementById('ota-progress-bar-container');
      const progressFill = document.getElementById('ota-progress-fill');
      const progressPct = document.getElementById('ota-progress-pct');
      const progressTask = document.getElementById('ota-progress-task');

      if (!btn) return;
      btn.disabled = true;
      btn.textContent = "Menghubungi DaXCloud...";
      if (progressContainer) progressContainer.style.display = 'block';

      let pct = 0;
      const interval = setInterval(() => {
        pct += 15;
        if (pct > 100) pct = 100;
        if (progressFill) progressFill.style.width = pct + "%";
        if (progressPct) progressPct.textContent = pct + "%";

        if (pct === 30 && progressTask) progressTask.textContent = "Mengunduh paket delta (48.4 MB)...";
        if (pct === 75 && progressTask) progressTask.textContent = "Memverifikasi kriptografi SHA3-512...";
        if (pct === 90 && progressTask) progressTask.textContent = "Staging biner ke Slot B (/dev/nvme0n1p3)...";

        if (pct >= 100) {
          clearInterval(interval);
          btn.disabled = false;
          btn.textContent = "Pembaruan Siap";
          if (progressTask) progressTask.textContent = "Pembaruan berhasil distaging ke Slot B!";
          if (status) status.innerHTML = "<span style='color: #30D158;'>Pembaruan Siap Dipasang!</span> Booting ke Slot B saat restart.";
          toast("OTA Update siap! GRUB 2.12 akan booting ke Slot B dengan aman.");
        }
      }, 180);
    }
"""

def main():
    print("[1/3] Reading index.html...")
    content = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Replace nav items
    nav_start = '<div class="settings-nav-item active" id="snav-displays"'
    nav_end = '<!-- Content Panes -->'
    if nav_start in content and nav_end in content:
        start_idx = content.find(nav_start)
        end_idx = content.find(nav_end)
        content = content[:start_idx] + NEW_NAV_ITEMS + "\n        </div>\n\n        " + content[end_idx:]
        print("[2/3] Updated settings navigation items with 5 powerful categories!")

    # 2. Add new subpanes before the end of settings-content-pane
    # Locate spane-about closing tag
    about_anchor = 'id="spane-about"'
    if about_anchor in content:
        # Find the closing </div> of spane-about
        about_idx = content.find(about_anchor)
        # Find closing div of this subpane
        # It's followed by </div>\n        </div>\n      </div>\n    </div>\n  </div>
        close_subpane_marker = '</div>\n        </div>\n      </div>\n    </div>\n  </div>'
        if close_subpane_marker in content[about_idx:]:
            insert_pos = content.find(close_subpane_marker, about_idx)
            content = content[:insert_pos] + "</div>\n\n" + NEW_SUBPANES + "\n" + content[insert_pos:]
            print("[3/3] Injected 5 complete & powerful settings subpanes!")

    # 3. Add JS controllers before </script>
    if "function restartSystemdService" not in content:
        script_close = "</script>"
        last_script = content.rfind(script_close)
        if last_script != -1:
            content = content[:last_script] + JS_CONTROLLERS + "\n  " + content[last_script:]
            print("[4/4] Injected JavaScript controllers for systemd, performance, storage, and OTA!")

    INDEX_HTML.write_text(content, encoding="utf-8")
    print(f"[PASS] Successfully updated {INDEX_HTML} ({len(content)} bytes)!")

if __name__ == "__main__":
    main()
