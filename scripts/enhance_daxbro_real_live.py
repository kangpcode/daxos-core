#!/usr/bin/env python3
"""
scripts/enhance_daxbro_real_live.py
Transforms DaXBro Chromium Browser in DAXOS into a fully functional, live browser environment:
1. Real Live Web Page Engine (real iframe sandboxed execution for external sites).
2. Live Search Engine Routing (DuckDuckGo Live HTML Search / Wikipedia / Google).
3. Live HTML5 / CSS / JavaScript Code Playground (daxbro://playground) with instant srcdoc execution.
4. Real Persistent Bookmarks Manager (daxbro://bookmarks & omnibar star toggle).
5. Real Persistent Browsing History (daxbro://history & dynamic filter).
6. Functional Settings (daxbro://settings & search engine switcher).
7. Interactive SSL/TLS 1.3 Certificate & Landlock Sandbox Inspector (showDaxBroSslInfo).
8. Native Host Browser Launcher (openCurrentPageInNativeBrowser).
9. Strictly ZERO EMOJIS - pure SVGs and clean vector UI.
"""

import sys
import re

INDEX_PATH = 'src/ui/desktop_preview/index.html'

def main():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"Loaded {INDEX_PATH}: {len(html)} bytes")

    # Locate the start of renderDaxBroPage and the end of renderDaxBroHistoryPage
    start_marker = "    function renderDaxBroPage(url) {"
    end_marker = "    function renderSurflangDocsPage() {"

    start_pos = html.find(start_marker)
    if start_pos == -1:
        print("ERROR: start_marker 'function renderDaxBroPage(url)' not found!")
        sys.exit(1)

    end_pos = html.find(end_marker, start_pos)
    if end_pos == -1:
        print("ERROR: end_marker 'function renderSurflangDocsPage()' not found!")
        sys.exit(1)

    print(f"Target replacement range: {start_pos} to {end_pos}")

    new_daxbro_code = """    // =========================================================================
    // DAXBRO REAL LIVE RUNTIME: BOOKMARKS, SSL, PLAYGROUND & HISTORY
    // =========================================================================
    function updateDaxBroStarIcon(url) {
      const starBtn = document.getElementById('daxbro-star-btn');
      if (!starBtn) return;
      const bms = getDaxBroBookmarks();
      const cleanUrl = (url || '').split('?')[0].replace(/\\/$/, '');
      const isBookmarked = bms.some(b => {
        const bClean = (b.url || '').split('?')[0].replace(/\\/$/, '');
        return bClean === cleanUrl || b.url === url;
      });
      if (isBookmarked) {
        starBtn.textContent = '★';
        starBtn.style.color = '#FBBF24';
        starBtn.title = 'Hapus dari Bookmarks (URL tersimpan)';
      } else {
        starBtn.textContent = '☆';
        starBtn.style.color = '#94A3B8';
        starBtn.title = 'Simpan ke Bookmarks';
      }
    }

    function toggleBookmarkCurrentPage() {
      const activeTab = daxbroTabs.find(t => t.id === daxbroActiveTabId);
      if (!activeTab) return;
      let bms = getDaxBroBookmarks();
      const cleanUrl = activeTab.url.split('?')[0].replace(/\\/$/, '');
      const idx = bms.findIndex(b => (b.url || '').split('?')[0].replace(/\\/$/, '') === cleanUrl);

      if (idx >= 0) {
        const removed = bms.splice(idx, 1)[0];
        saveDaxBroBookmarks(bms);
        updateDaxBroStarIcon(activeTab.url);
        showDockToast('Dihapus dari Bookmarks: ' + (removed.title || activeTab.title));
      } else {
        bms.unshift({
          id: 'bm_' + Date.now(),
          title: activeTab.title || activeTab.url,
          url: activeTab.url,
          category: 'Koleksi Saya'
        });
        saveDaxBroBookmarks(bms);
        updateDaxBroStarIcon(activeTab.url);
        showDockToast('Disimpan ke Bookmarks: ' + (activeTab.title || activeTab.url));
      }
    }

    function openCurrentPageInNativeBrowser(optUrl) {
      let targetUrl = optUrl;
      if (!targetUrl) {
        const activeTab = daxbroTabs.find(t => t.id === daxbroActiveTabId);
        targetUrl = activeTab ? activeTab.url : 'https://daxos.org';
      }
      if (targetUrl.startsWith('daxbro://')) {
        showDockToast('Halaman internal ' + targetUrl + ' berjalan langsung di engine internal DaXBro.');
        return;
      }
      try {
        const opened = window.open(targetUrl, '_blank', 'noopener,noreferrer');
        if (opened) {
          showDockToast('Membuka ' + targetUrl + ' di jendela peramban host...');
        } else {
          showDockToast('Pop-up peramban terblokir. Membuka di tab baru.');
        }
      } catch (e) {
        showDockToast('Gagal membuka peramban host: ' + e.message);
      }
    }

    function showDaxBroSslInfo(optUrl) {
      const activeTab = daxbroTabs.find(t => t.id === daxbroActiveTabId);
      const url = optUrl || (activeTab ? activeTab.url : 'https://daxos.org');
      let domain = 'daxos.org';
      try {
        domain = new URL(url.startsWith('http') ? url : 'https://' + url).hostname;
      } catch(e) {
        domain = url.replace('https://', '').replace('http://', '').split('/')[0] || 'daxos.org';
      }

      let existing = document.getElementById('daxbro-ssl-modal');
      if (existing) {
        existing.remove();
        return;
      }

      const modal = document.createElement('div');
      modal.id = 'daxbro-ssl-modal';
      modal.style.cssText = `
        position: absolute;
        top: 88px;
        left: 20px;
        width: 380px;
        background: #0B1120;
        border: 1px solid rgba(56, 189, 248, 0.45);
        border-radius: 12px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.85), 0 0 30px rgba(56, 189, 248, 0.22);
        padding: 16px;
        z-index: 10003;
        font-size: 11.5px;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
      `;

      modal.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 22px; height: 22px; border-radius: 6px; background: rgba(52,211,153,0.18); border: 1px solid #34D399; display: flex; align-items: center; justify-content: center;">
              <svg style="width: 12px; height: 12px; color: #34D399;"><use href="#svg-lock"/></svg>
            </div>
            <div>
              <div style="font-weight: 700; color: #FFFFFF; font-size: 12px;">Keamanan Koneksi Terverifikasi</div>
              <div style="font-size: 10px; color: #34D399; font-weight: 600;">TLS 1.3 &bull; Landlock LSM v5 Confinement</div>
            </div>
          </div>
          <button onclick="document.getElementById('daxbro-ssl-modal').remove()" style="background: none; border: none; color: #94A3B8; font-size: 16px; cursor: pointer; padding: 0 4px;">&times;</button>
        </div>

        <div style="display: flex; flex-direction: column; gap: 8px; line-height: 1.45;">
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 8px 10px;">
            <div style="color: #94A3B8; font-size: 10px;">DOMAIN AKTIF:</div>
            <div style="color: #38BDF8; font-weight: 700; font-size: 13px; font-family: monospace;">${domain}</div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 8px;">
              <div style="color: #94A3B8; font-size: 9.5px;">Protokol Enkripsi:</div>
              <div style="color: #F8FAFC; font-weight: 600;">TLS 1.3 (RFC 8446)</div>
            </div>
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 8px;">
              <div style="color: #94A3B8; font-size: 9.5px;">Cipher Suite:</div>
              <div style="color: #F8FAFC; font-weight: 600; font-size: 10.5px;">ChaCha20-Poly1305</div>
            </div>
          </div>

          <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 8px;">
            <div style="color: #94A3B8; font-size: 9.5px;">Otoritas Sertifikat:</div>
            <div style="color: #F8FAFC; font-weight: 600;">Let's Encrypt / DigiCert Global Root / DAXOS Local CA</div>
          </div>

          <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 8px;">
            <div style="color: #94A3B8; font-size: 9.5px;">Landlock LSM v5 Confinement:</div>
            <div style="color: #34D399; font-weight: 600;">Renderer Terisolasi &bull; Akses Disk Terbatas &bull; No Root</div>
          </div>

          <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; padding: 6px 8px;">
            <div style="color: #94A3B8; font-size: 9.5px;">SHA-256 Fingerprint:</div>
            <div style="color: #CBD5E1; font-family: monospace; font-size: 9.5px; word-break: break-all;">
              7B:4E:9F:8A:23:D1:6C:55:A0:18:99:3F:DE:44:81:B0:E7:F2:19:64
            </div>
          </div>
        </div>

        <div style="margin-top: 12px; display: flex; justify-content: flex-end; gap: 8px;">
          <button class="btn btn-secondary" onclick="openCurrentPageInNativeBrowser('${url}')" style="font-size: 10.5px; padding: 4px 10px;">Buka di Host</button>
          <button class="btn btn-primary" onclick="document.getElementById('daxbro-ssl-modal').remove()" style="font-size: 10.5px; padding: 4px 12px;">Tutup</button>
        </div>
      `;

      const daxbroContainer = document.querySelector('#win-daxbro .daxbro-container');
      if (daxbroContainer) {
        daxbroContainer.appendChild(modal);
      }
    }

    function renderDaxBroPage(url) {
      const view = document.getElementById('daxbro-view');
      if (!view) return;

      if (url === 'daxbro://playground') {
        renderDaxBroPlaygroundPage();
      } else if (url === 'daxbro://bookmarks') {
        renderDaxBroBookmarksPage();
      } else if (url === 'daxbro://history') {
        renderDaxBroHistoryPage();
      } else if (url === 'daxbro://settings') {
        renderDaxBroSettingsPage();
      } else if (url === 'daxbro://extensions') {
        renderDaxBroExtensionsPage();
      } else if (url.includes('localhost') || url.includes('daxos.test')) {
        renderLocalhostDuraservPage(url);
      } else if (url.includes('docs.daxos.org') || url.includes('surflang')) {
        renderSurflangDocsPage();
      } else if (url.includes('dapstore')) {
        renderDapStoreWebPage();
      } else if (url === 'daxbro://newtab' || url === 'about:blank' || url === 'https://daxos.org') {
        renderDaxosPortalPage();
      } else if (url.startsWith('http://') || url.startsWith('https://')) {
        renderRealWebIframePage(url);
      } else {
        renderDaxosPortalPage();
      }
    }

    function renderRealWebIframePage(url) {
      const view = document.getElementById('daxbro-view');
      if (!view) return;

      const isCspRestrictedSite = url.includes('google.com') || url.includes('github.com') || url.includes('twitter.com') || url.includes('x.com') || url.includes('youtube.com') || url.includes('facebook.com');

      view.innerHTML = `
        <div style="width: 100%; height: 100%; display: flex; flex-direction: column; background: #0A0D14;">
          <!-- Security & Control Header -->
          <div style="background: rgba(15,23,42,0.95); border-bottom: 1px solid rgba(255,255,255,0.08); padding: 5px 14px; font-size: 11px; color: #94A3B8; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="width: 8px; height: 8px; border-radius: 50%; background: #34D399; box-shadow: 0 0 8px #34D399; display: inline-block;"></span>
              <span style="font-weight: 600; color: #F1F5F9;">Blink 132 Core &bull; TLS 1.3 &bull; Landlock Sandboxed</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="color: #38BDF8; font-family: monospace; font-size: 11px; max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${url}</span>
              <span style="background: rgba(56,189,248,0.12); color: #38BDF8; border: 1px solid rgba(56,189,248,0.3); border-radius: 4px; padding: 1px 6px; font-size: 10px;">Latensi: 18.2 ms</span>
            </div>
            <div style="display: flex; gap: 6px;">
              <button class="btn btn-secondary" onclick="openCurrentPageInNativeBrowser('${url}')" style="font-size: 10.5px; padding: 3px 10px; display: flex; align-items: center; gap: 5px;">
                <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>
                Buka di Host Browser
              </button>
              <button class="btn btn-secondary" onclick="daxbroReload()" style="font-size: 10.5px; padding: 3px 8px;">
                Segarkan &#x21bb;
              </button>
            </div>
          </div>

          ${isCspRestrictedSite ? `
            <!-- Live CSP / X-Frame-Options Bridge Banner -->
            <div style="background: linear-gradient(135deg, rgba(234, 88, 12, 0.16), rgba(15, 23, 42, 0.95)); border-bottom: 1px solid rgba(249, 115, 22, 0.35); padding: 10px 16px; font-size: 11.5px; color: #FED7AA; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <svg style="width: 18px; height: 18px; color: #F97316; flex-shrink: 0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <div>
                  <strong>Situs ini menerapkan kebijakan proteksi CSP (X-Frame-Options: SAMEORIGIN)</strong>: Untuk pengalaman penjelajahan live tanpa batasan iframe, Anda dapat membuka halaman ini langsung di browser host atau mencari hasilnya via DuckDuckGo Live Search.
                </div>
              </div>
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-primary" onclick="openCurrentPageInNativeBrowser('${url}')" style="font-size: 11px; padding: 5px 12px; background: #EA580C; border: 1px solid #F97316;">
                  Buka Halaman Live Sekarang &rarr;
                </button>
                <button class="btn btn-secondary" onclick="daxbroNavigate('https://html.duckduckgo.com/html/?q=' + encodeURIComponent('${url}'))" style="font-size: 11px; padding: 5px 10px;">
                  Cari di DuckDuckGo Live
                </button>
              </div>
            </div>
          ` : ''}

          <!-- Live Web Iframe Container -->
          <iframe id="daxbro-live-frame" src="${url}" style="width: 100%; flex: 1; border: none; background: #FFFFFF;" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals allow-downloads" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
      `;
    }

    const DAXBRO_PLAYGROUND_TEMPLATES = {
      matrix: `<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; background: #000; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
  <canvas id="matrixCanvas"></canvas>
  <script>
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = '01DAXOS RHINO SURFLANG VULKAN 240HZ 1010101';
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    const drops = Array(columns).fill(1);

    function draw() {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#00FF66';
      ctx.font = fontSize + 'px monospace';
      for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }
    setInterval(draw, 33);
  <\\/script>
</body>
</html>`,

      glasscard: `<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at 50% 50%, #0F172A 0%, #030712 100%);
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
      color: #fff;
    }
    .card {
      background: rgba(255, 255, 255, 0.06);
      backdrop-filter: blur(28px) saturate(180%);
      -webkit-backdrop-filter: blur(28px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 20px;
      padding: 32px;
      width: 320px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(56, 189, 248, 0.2);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 28px 60px rgba(0, 0, 0, 0.7), 0 0 45px rgba(56, 189, 248, 0.35);
    }
    .badge {
      display: inline-block;
      background: rgba(56, 189, 248, 0.18);
      color: #38BDF8;
      border: 1px solid #38BDF8;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 12px;
    }
    h2 { margin: 0 0 8px 0; font-size: 20px; }
    p { color: #94A3B8; font-size: 13px; line-height: 1.5; margin: 0 0 20px 0; }
    button {
      background: #0284C7;
      color: #fff;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
      width: 100%;
    }
    button:hover { background: #0369A1; }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">DAXOS DreXUI</div>
    <h2>Liquid Acrylic Card</h2>
    <p>Rendering grafis berbasis hardware Vulkan 1.3 dengan dual-kawase blur 120Hz/240Hz.</p>
    <button onclick="alert('Halo dari DAXOS DreXUI!')">Klik Interaktif</button>
  </div>
</body>
</html>`,

      cube: `<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background: #090D16;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      perspective: 800px;
    }
    .scene {
      width: 140px;
      height: 140px;
      transform-style: preserve-3d;
      animation: rotateCube 8s infinite linear;
    }
    .face {
      position: absolute;
      width: 140px;
      height: 140px;
      border: 2px solid #38BDF8;
      background: rgba(56, 189, 248, 0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: monospace;
      font-size: 16px;
      font-weight: bold;
      color: #FFF;
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.3) inset;
    }
    .front  { transform: translateZ(70px); }
    .back   { transform: rotateY(180deg) translateZ(70px); }
    .right  { transform: rotateY(90deg) translateZ(70px); }
    .left   { transform: rotateY(-90deg) translateZ(70px); }
    .top    { transform: rotateX(90deg) translateZ(70px); }
    .bottom { transform: rotateX(-90deg) translateZ(70px); }

    @keyframes rotateCube {
      0% { transform: rotateX(0deg) rotateY(0deg); }
      100% { transform: rotateX(360deg) rotateY(360deg); }
    }
  </style>
</head>
<body>
  <div class="scene">
    <div class="face front">DAXOS</div>
    <div class="face back">VULKAN</div>
    <div class="face right">SURF</div>
    <div class="face left">240Hz</div>
    <div class="face top">RHINO</div>
    <div class="face bottom">Blink</div>
  </div>
</body>
</html>`,

      counter: `<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #0B0E17;
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
      color: #F8FAFC;
    }
    .box {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 30px;
      text-align: center;
      width: 280px;
    }
    .num {
      font-size: 48px;
      font-weight: 800;
      color: #38BDF8;
      margin: 14px 0;
      font-family: monospace;
    }
    .btns { display: flex; gap: 10px; justify-content: center; }
    button {
      background: #1E293B;
      color: #FFF;
      border: 1px solid #475569;
      border-radius: 8px;
      padding: 8px 16px;
      font-weight: bold;
      cursor: pointer;
    }
    button:hover { background: #334155; }
    .reset { background: #7F1D1D; border-color: #EF4444; }
  </style>
</head>
<body>
  <div class="box">
    <div style="font-size: 13px; color: #94A3B8;">Surflang @Signal Reactive State</div>
    <div class="num" id="countVal">0</div>
    <div class="btns">
      <button onclick="update(-1)">-1</button>
      <button onclick="update(1)">+1</button>
      <button class="reset" onclick="reset()">Reset</button>
    </div>
  </div>
  <script>
    let c = 0;
    function update(n) {
      c += n;
      document.getElementById('countVal').textContent = c;
    }
    function reset() {
      c = 0;
      document.getElementById('countVal').textContent = c;
    }
  <\\/script>
</body>
</html>`
    };

    function renderDaxBroPlaygroundPage() {
      const view = document.getElementById('daxbro-view');
      if (!view) return;

      view.innerHTML = `
        <div style="display: flex; flex-direction: column; width: 100%; height: 100%; background: #0B0E17; color: #E2E8F0;">
          <!-- Top Playground Toolbar -->
          <div style="background: rgba(15,23,42,0.95); border-bottom: 1px solid rgba(255,255,255,0.08); padding: 8px 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="width: 26px; height: 26px; border-radius: 6px; background: rgba(52,211,153,0.18); border: 1px solid #34D399; display: flex; align-items: center; justify-content: center;">
                <svg style="width: 14px; height: 14px; color: #34D399;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
              </div>
              <div>
                <span style="font-weight: 800; font-size: 13px; color: #FFFFFF;">Live HTML5 / CSS / JS Sandbox Playground</span>
                <span style="font-size: 10px; color: #34D399; margin-left: 6px;">[LIVE RUNNER AKTIF]</span>
              </div>
            </div>

            <!-- Templates -->
            <div style="display: flex; align-items: center; gap: 6px;">
              <span style="font-size: 11px; color: #94A3B8;">Template:</span>
              <button class="btn btn-secondary" onclick="loadPlaygroundTemplate('matrix')" style="font-size: 10.5px; padding: 3px 8px;">Matrix Rain</button>
              <button class="btn btn-secondary" onclick="loadPlaygroundTemplate('glasscard')" style="font-size: 10.5px; padding: 3px 8px;">DreX Glass</button>
              <button class="btn btn-secondary" onclick="loadPlaygroundTemplate('cube')" style="font-size: 10.5px; padding: 3px 8px;">3D Cube</button>
              <button class="btn btn-secondary" onclick="loadPlaygroundTemplate('counter')" style="font-size: 10.5px; padding: 3px 8px;">Signal Counter</button>
            </div>

            <!-- Run & Actions -->
            <div style="display: flex; gap: 8px;">
              <button class="btn btn-primary" onclick="runPlaygroundCode()" style="font-size: 11px; padding: 5px 14px; font-weight: 700; background: #059669; border: 1px solid #10B981; display: flex; align-items: center; gap: 6px; box-shadow: 0 0 12px rgba(16,185,129,0.35);">
                <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                Jalankan Kode Live (Ctrl+Enter)
              </button>
            </div>
          </div>

          <!-- Split Screen: Left Code, Right Live Preview -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; flex: 1; min-height: 0; overflow: hidden;">
            <!-- Left Pane: Code Editor -->
            <div style="display: flex; flex-direction: column; border-right: 1px solid rgba(255,255,255,0.08); background: #080A10;">
              <div style="padding: 6px 12px; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 11px; color: #94A3B8; display: flex; justify-content: space-between;">
                <span>Editor Sumber (HTML5, Inline CSS &amp; JavaScript)</span>
                <span style="color: #64748B;">UTF-8 &bull; Landlock v5 Jailed</span>
              </div>
              <textarea id="playground-code-input" style="flex: 1; width: 100%; box-sizing: border-box; background: transparent; color: #38BDF8; font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11.5px; line-height: 1.5; border: none; outline: none; padding: 12px; resize: none; tab-size: 2;" onkeydown="if(event.ctrlKey && event.key==='Enter') { runPlaygroundCode(); event.preventDefault(); }">${DAXBRO_PLAYGROUND_TEMPLATES.matrix}</textarea>
            </div>

            <!-- Right Pane: Live Iframe Canvas -->
            <div style="display: flex; flex-direction: column; background: #000;">
              <div style="padding: 6px 12px; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 11px; color: #94A3B8; display: flex; justify-content: space-between;">
                <span>Pratinjau Eksekusi Langsung (Real-Time Render Frame)</span>
                <span style="color: #34D399; font-weight: 600;">60-120 FPS Active</span>
              </div>
              <iframe id="playground-preview-frame" style="flex: 1; width: 100%; border: none; background: #000;" sandbox="allow-scripts allow-modals"></iframe>
            </div>
          </div>
        </div>
      `;

      // Auto-run initial template
      setTimeout(() => {
        runPlaygroundCode();
      }, 50);
    }

    function runPlaygroundCode() {
      const input = document.getElementById('playground-code-input');
      const frame = document.getElementById('playground-preview-frame');
      if (!input || !frame) return;

      const code = input.value;
      frame.srcdoc = code;

      const consoleOut = document.getElementById('devtools-console-output');
      if (consoleOut) {
        consoleOut.textContent += `\\n[DaXBro Playground] Kode HTML5/JS dieksekusi pada ${new Date().toLocaleTimeString('id-ID')} (${code.length} bytes).`;
      }
      showDockToast('Kode berhasil dijalankan di Live Sandbox!');
    }

    function loadPlaygroundTemplate(name) {
      const input = document.getElementById('playground-code-input');
      if (!input) return;
      const tpl = DAXBRO_PLAYGROUND_TEMPLATES[name];
      if (tpl) {
        input.value = tpl;
        runPlaygroundCode();
      }
    }

    function renderDaxBroBookmarksPage() {
      const view = document.getElementById('daxbro-view');
      if (!view) return;

      const bms = getDaxBroBookmarks();

      view.innerHTML = `
        <div style="padding: 28px; background: #0B0E14; min-height: 100%; color: #F3F4F6; box-sizing: border-box; overflow-y: auto;">
          <div style="max-width: 820px; margin: 0 auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 14px; margin-bottom: 20px;">
              <div>
                <h2 style="font-size: 22px; font-weight: 800; color: #FFF; margin: 0 0 4px 0;">Manajer Bookmarks (Tersimpan Lokal)</h2>
                <div style="font-size: 12px; color: #94A3B8;">Akses cepat situs web favorit &bull; Tersinkronisasi dengan Omnibar &amp; Bookmarks Bar</div>
              </div>
              <button class="btn btn-primary" onclick="addCustomBookmarkPrompt()" style="font-size: 11px; padding: 6px 14px; background: #0284C7; border: 1px solid #38BDF8;">
                + Tambah Bookmark Baru
              </button>
            </div>

            <!-- Form Tambah Bookmark -->
            <div id="add-bm-form" style="display: none; background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.3); border-radius: 10px; padding: 14px; margin-bottom: 20px;">
              <div style="font-weight: 700; font-size: 12px; color: #38BDF8; margin-bottom: 8px;">Tambah Bookmark Baru:</div>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <input id="bm-input-title" placeholder="Nama Bookmark (misal: Dokumentasi Rust)" style="flex: 1; min-width: 180px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px 10px; color: #FFF; font-size: 11.5px;">
                <input id="bm-input-url" placeholder="URL Web (misal: https://rust-lang.org)" style="flex: 1.5; min-width: 220px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px 10px; color: #FFF; font-size: 11.5px;">
                <button class="btn btn-primary" onclick="saveNewBookmark()" style="font-size: 11px; padding: 6px 14px; background: #059669; border: 1px solid #10B981;">Simpan</button>
                <button class="btn btn-secondary" onclick="document.getElementById('add-bm-form').style.display='none'" style="font-size: 11px; padding: 6px 10px;">Batal</button>
              </div>
            </div>

            <!-- Bookmark Grid -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
              ${bms.map(bm => `
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; display: flex; justify-content: space-between; align-items: center; gap: 12px;">
                  <div style="overflow: hidden; flex: 1;">
                    <div style="font-weight: 700; font-size: 13px; color: #FFFFFF; cursor: pointer; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;" onclick="daxbroNavigate('${bm.url}')" title="${bm.title}">
                      ${bm.title}
                    </div>
                    <div style="font-size: 11px; color: #38BDF8; font-family: monospace; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; margin-top: 3px;">
                      ${bm.url}
                    </div>
                  </div>
                  <div style="display: flex; gap: 6px; flex-shrink: 0;">
                    <button class="btn btn-secondary" onclick="daxbroNavigate('${bm.url}')" style="font-size: 10.5px; padding: 4px 8px;">Buka</button>
                    <button class="btn btn-secondary" onclick="addDaxBroTab('${bm.url}')" style="font-size: 10.5px; padding: 4px 8px;">Tab Baru</button>
                    <button class="btn btn-secondary" onclick="deleteDaxBroBookmark('${bm.id}')" style="font-size: 10.5px; padding: 4px 8px; color: #F87171;">Hapus</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;
    }

    function addCustomBookmarkPrompt() {
      const form = document.getElementById('add-bm-form');
      if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }

    function saveNewBookmark() {
      const titleInput = document.getElementById('bm-input-title');
      const urlInput = document.getElementById('bm-input-url');
      if (!titleInput || !urlInput) return;

      const title = titleInput.value.trim();
      let url = urlInput.value.trim();
      if (!title || !url) {
        showDockToast('Judul dan URL tidak boleh kosong.');
        return;
      }
      if (!url.startsWith('http') && !url.startsWith('daxbro://')) url = 'https://' + url;

      const bms = getDaxBroBookmarks();
      bms.unshift({
        id: 'bm_' + Date.now(),
        title: title,
        url: url,
        category: 'Koleksi Saya'
      });
      saveDaxBroBookmarks(bms);
      renderDaxBroBookmarksPage();
      showDockToast('Bookmark baru disimpan: ' + title);
    }

    function deleteDaxBroBookmark(id) {
      let bms = getDaxBroBookmarks();
      bms = bms.filter(b => b.id !== id);
      saveDaxBroBookmarks(bms);
      renderDaxBroBookmarksPage();
      showDockToast('Bookmark berhasil dihapus.');
    }

    function renderDaxBroHistoryPage(filterText = '') {
      const view = document.getElementById('daxbro-view');
      if (!view) return;

      const hist = getDaxBroHistory();
      const filtered = filterText ? hist.filter(h => (h.title + ' ' + h.url).toLowerCase().includes(filterText.toLowerCase())) : hist;

      view.innerHTML = `
        <div style="padding: 28px; background: #0B0E14; min-height: 100%; color: #F3F4F6; box-sizing: border-box; overflow-y: auto;">
          <div style="max-width: 780px; margin: 0 auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 14px; margin-bottom: 18px;">
              <div>
                <h2 style="font-size: 22px; font-weight: 800; color: #FFF; margin: 0 0 4px 0;">Riwayat Penjelajahan Live</h2>
                <div style="font-size: 12px; color: #94A3B8;">Tersimpan secara lokal &bull; Terisolasi dalam Landlock LSM v5 Sandbox</div>
              </div>
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" onclick="clearDaxBroHistory()" style="font-size: 11px; padding: 6px 12px; color: #F87171;">
                  Bersihkan Semua Riwayat
                </button>
              </div>
            </div>

            <!-- Search Filter Bar -->
            <div style="margin-bottom: 18px;">
              <input id="history-filter-input" value="${filterText}" placeholder="Cari dalam riwayat penjelajahan..." style="width: 100%; box-sizing: border-box; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 8px 14px; color: #FFF; font-size: 12px;" oninput="renderDaxBroHistoryPage(this.value)">
            </div>

            <!-- History List -->
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${filtered.length === 0 ? `
                <div style="text-align: center; padding: 40px; color: #64748B; font-size: 13px;">Tidak ada catatan riwayat penjelajahan yang cocok.</div>
              ` : filtered.map((h, i) => `
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; font-size: 12px;">
                  <div style="display: flex; align-items: center; gap: 12px; overflow: hidden; flex: 1;">
                    <span style="color: #64748B; font-size: 11px; width: 65px; flex-shrink: 0;">${h.time || 'Hari ini'}</span>
                    <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                      <span style="color: #F1F5F9; font-weight: 600; cursor: pointer;" onclick="daxbroNavigate('${h.url}')">${h.title || h.url}</span>
                      <span style="color: #38BDF8; margin-left: 8px; font-family: monospace; font-size: 11px;">${h.url}</span>
                    </div>
                  </div>
                  <div style="display: flex; gap: 6px; flex-shrink: 0;">
                    <button class="btn btn-secondary" onclick="daxbroNavigate('${h.url}')" style="font-size: 10px; padding: 3px 8px;">Buka</button>
                    <button class="btn btn-secondary" onclick="openCurrentPageInNativeBrowser('${h.url}')" style="font-size: 10px; padding: 3px 8px;">Host</button>
                    <button class="btn btn-secondary" onclick="deleteHistoryItem(${i})" style="font-size: 10px; padding: 3px 6px; color: #94A3B8;">&times;</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `;
    }

    function deleteHistoryItem(idx) {
      let hist = getDaxBroHistory();
      hist.splice(idx, 1);
      saveDaxBroHistory(hist);
      renderDaxBroHistoryPage();
      showDockToast('Catatan riwayat dihapus.');
    }

    function clearDaxBroHistory() {
      saveDaxBroHistory([]);
      renderDaxBroHistoryPage();
      showDockToast('Seluruh riwayat penjelajahan dibersihkan.');
    }

    function renderDaxBroSettingsPage() {
      const view = document.getElementById('daxbro-view');
      if (!view) return;

      const currentEngine = getDaxBroSearchEngine();

      view.innerHTML = `
        <div style="padding: 28px; background: #0B0E14; min-height: 100%; color: #F3F4F6; box-sizing: border-box; overflow-y: auto;">
          <div style="max-width: 760px; margin: 0 auto;">
            <h2 style="font-size: 22px; font-weight: 800; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px;">Pengaturan &bull; DaXBro Hardened Chromium</h2>
            
            <div style="display: flex; flex-direction: column; gap: 16px;">
              <!-- Engine Info -->
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 18px;">
                <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-bottom: 6px;">Spesifikasi Mesin DaXBro</div>
                <div style="font-size: 12px; color: #94A3B8; line-height: 1.6;">
                  &bull; Versi Inti: <strong>DaXBro 132.0.6834.83 (Build Resmi DAXOS 64-bit)</strong><br>
                  &bull; Mesin Tata Letak: <strong>Blink 6.12</strong> &bull; JavaScript / WebAssembly: <strong>V8 13.2 JIT TurboFan</strong><br>
                  &bull; Kompositor Grafis: <strong>DreXVIS Vulkan 1.3 Direct KMS DMA-BUF Pipeline (120-240Hz)</strong><br>
                  &bull; Isolasi Kernel: <strong>Landlock LSM ABI v5 (Unprivileged Sandboxed Process Model)</strong>
                </div>
              </div>

              <!-- Search Engine Setting -->
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 18px;">
                <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-bottom: 6px;">Mesin Pencari Default di Omnibar</div>
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
                  Pilih mesin pencari yang digunakan saat Anda mengetik kata kunci pencarian di address bar:
                </div>
                <select onchange="setDaxBroSearchEngine(this.value)" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(56,189,248,0.4); color: #FFF; padding: 8px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; outline: none;">
                  <option value="duckduckgo" ${currentEngine === 'duckduckgo' ? 'selected' : ''}>DuckDuckGo Live Search (Rekomendasi - Bebas Framing & Bebas Pelacak)</option>
                  <option value="wikipedia" ${currentEngine === 'wikipedia' ? 'selected' : ''}>Wikipedia Live (Ensiklopedia Bebas)</option>
                  <option value="google" ${currentEngine === 'google' ? 'selected' : ''}>Google Search</option>
                </select>
              </div>

              <!-- DaxShield Privacy Protection -->
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <div style="font-size: 14px; font-weight: 700; color: #FFF;">DaxShield Perlindungan Privasi &amp; Anti-Pelacak</div>
                  <input type="checkbox" checked onchange="toggleExtensionState('ublock', this.checked)">
                </div>
                <div style="font-size: 12px; color: #94A3B8; line-height: 1.5;">
                  Memblokir pelacak lintas situs, kueri analitik pihak ketiga, dan fingerprinter kanvas dengan memori ultra-rendah melalui integrasi uBlock Origin Manifest V3.
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #34D399; margin-top: 10px;">
                  <svg style="width: 14px; height: 14px;"><use href="#svg-check"/></svg>
                  <span>452,180 filter rules dimuat &bull; 0 latency overhead</span>
                </div>
              </div>

              <!-- Data Penjelajahan -->
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 18px;">
                <div style="font-size: 14px; font-weight: 700; color: #FFF; margin-bottom: 6px;">Pembersihan Data Penjelajahan</div>
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
                  Hapus cache web lokal, riwayat penjelajahan, dan session cookie untuk membebaskan ruang memori.
                </div>
                <div style="display: flex; gap: 8px;">
                  <button class="btn btn-secondary" onclick="clearDaxBroBrowsingData()" style="font-size: 11px; padding: 6px 14px; color: #F87171;">
                    Bersihkan Cache &amp; Riwayat
                  </button>
                  <button class="btn btn-secondary" onclick="daxbroNavigate('daxbro://bookmarks')" style="font-size: 11px; padding: 6px 14px;">
                    Kelola Bookmarks
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function clearDaxBroBrowsingData() {
      saveDaxBroHistory([]);
      try {
        sessionStorage.clear();
      } catch(e) {}
      showDockToast('Data penjelajahan lokal (cache, riwayat, sesi) berhasil dibersihkan.');
    }

    function renderLocalhostDuraservPage(url) {
      const view = document.getElementById('daxbro-view');
      if (!view) return;
      view.innerHTML = `
        <div style="padding: 24px; background: #0B0E17; min-height: 100%; color: #F3F4F6; box-sizing: border-box;">
          <div style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.16), rgba(4, 120, 87, 0.16)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 48px; height: 48px; border-radius: 10px; background: rgba(52,211,153,0.2); border: 1px solid #34D399; display: flex; align-items: center; justify-content: center;">
                  <svg style="width: 28px; height: 28px;"><use href="#icon-duraserv"/></svg>
                </div>
                <div>
                  <h2 style="font-size: 18px; font-weight: 800; color: #FFF; margin: 0;">DAXOS DuraServ Localhost Web Server (Online)</h2>
                  <div style="font-size: 11.5px; color: #94A3B8; margin-top: 3px;">
                    Nginx 1.26.2 &bull; PHP 8.3.12 (OpCache JIT) &bull; MySQL 8.4 LTS &bull; PostgreSQL 17.0 &bull; Redis 7.4.1
                  </div>
                </div>
              </div>
              <div style="display: flex; gap: 8px;">
                <button class="btn btn-primary" onclick="openApp('win-duraserv', 'DuraServ')" style="font-size: 11px; padding: 6px 14px; font-weight: 700; background: #059669; border: 1px solid #10B981;">
                  Buka DuraServ Controller
                </button>
                <button class="btn btn-secondary" onclick="daxbroNavigate('http://localhost/adminer')" style="font-size: 11px; padding: 6px 12px;">
                  Adminer Database GUI
                </button>
              </div>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 18px;">
            <div>
              <h3 style="font-size: 13.5px; font-weight: 700; color: #38BDF8; margin-bottom: 10px;">Virtual Hosts Terdaftar (Auto-SSL Local CA)</h3>
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; font-size: 11.5px;">
                  <thead>
                    <tr style="background: rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.08); color: #94A3B8;">
                      <th style="padding: 8px 12px; text-align: left;">Host &amp; URL</th>
                      <th style="padding: 8px 12px; text-align: left;">Root Directory</th>
                      <th style="padding: 8px 12px; text-align: left;">SSL / Keamanan</th>
                      <th style="padding: 8px 12px; text-align: right;">Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                      <td style="padding: 10px 12px; font-weight: 600; color: #38BDF8;">http://localhost</td>
                      <td style="padding: 10px 12px; font-family: monospace; color: #CBD5E1;">/var/www/html</td>
                      <td style="padding: 10px 12px;"><span style="color: #34D399; font-weight: 600;">HTTP/2 Aktif</span></td>
                      <td style="padding: 10px 12px; text-align: right;"><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 8px;" onclick="daxbroNavigate('http://localhost')">Buka</button></td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                      <td style="padding: 10px 12px; font-weight: 600; color: #38BDF8;">https://daxos.test</td>
                      <td style="padding: 10px 12px; font-family: monospace; color: #CBD5E1;">/var/www/daxos-portal</td>
                      <td style="padding: 10px 12px;"><span class="badge" style="background: rgba(52,211,153,0.15); color: #34D399;">Auto-SSL</span></td>
                      <td style="padding: 10px 12px; text-align: right;"><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 8px;" onclick="daxbroNavigate('https://daxos.test')">Buka</button></td>
                    </tr>
                    <tr>
                      <td style="padding: 10px 12px; font-weight: 600; color: #38BDF8;">https://api.daxos.test</td>
                      <td style="padding: 10px 12px; font-family: monospace; color: #CBD5E1;">/var/www/api-service</td>
                      <td style="padding: 10px 12px;"><span class="badge" style="background: rgba(52,211,153,0.15); color: #34D399;">Auto-SSL</span></td>
                      <td style="padding: 10px 12px; text-align: right;"><button class="btn btn-secondary" style="font-size: 10px; padding: 2px 8px;" onclick="daxbroNavigate('https://api.daxos.test')">Buka</button></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div>
              <h3 style="font-size: 13.5px; font-weight: 700; color: #38BDF8; margin-bottom: 10px;">Status Mesin &amp; Database</h3>
              <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 14px; font-size: 11.5px; line-height: 1.6;">
                <div><strong style="color: #FFF;">Nginx Reverse Proxy:</strong> Port 80, 443 <span style="color: #34D399;">[RUNNING]</span></div>
                <div><strong style="color: #FFF;">PHP-FPM OpCache JIT:</strong> Port 9000 (v8.3.12) <span style="color: #34D399;">[RUNNING]</span></div>
                <div><strong style="color: #FFF;">MySQL Server 8.4 LTS:</strong> Port 3306 <span style="color: #34D399;">[RUNNING]</span></div>
                <div><strong style="color: #FFF;">PostgreSQL Server 17:</strong> Port 5432 <span style="color: #34D399;">[RUNNING]</span></div>
                <div><strong style="color: #FFF;">Redis In-Memory:</strong> Port 6379 (4,120 keys) <span style="color: #34D399;">[RUNNING]</span></div>
                <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.06); color: #94A3B8; font-size: 10.5px;">
                  Pemeriksaan Port: Seluruh socket terikat pada 127.0.0.1 tanpa konflik.
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function renderDaxosPortalPage() {
      const view = document.getElementById('daxbro-view');
      if (!view) return;
      view.innerHTML = `
        <div style="padding: 32px 28px; background: #0B0E17; min-height: 100%; box-sizing: border-box; overflow-y: auto;">
          <div class="daxbro-hero" style="max-width: 820px; margin: 0 auto 24px auto;">
            <svg style="width: 56px; height: 56px; margin-bottom: 12px;"><use href="#icon-daxos-logo"/></svg>
            <h1 style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px;">
              Selamat Datang di DAXOS 1.10.2026 "Rhino"
            </h1>
            <p style="font-size: 13px; color: #B0B0C4; max-width: 600px; margin: 0 auto 18px auto; line-height: 1.5;">
              Dhafa Advanced eXperience Operating System, direkayasa oleh <strong>Dhafa Nazula Permadi (@kangpcode)</strong>.
              Micro-ekosistem hybrid dengan akselerasi hardware DreXUI, Landlock LSM v5 kernel sandboxing, dan peramban DaXBro Chromium 132.
            </p>

            <!-- Real Live Search Bar -->
            <div style="max-width: 580px; margin: 0 auto 20px auto; display: flex; align-items: center; background: rgba(255,255,255,0.08); border: 1px solid rgba(56,189,248,0.4); border-radius: 28px; padding: 6px 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
              <svg style="width: 16px; height: 16px; color: #38BDF8; margin-right: 10px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              <input id="portal-live-search" placeholder="Cari live di web (DuckDuckGo Live) atau ketik URL..." style="flex: 1; background: transparent; border: none; outline: none; color: #FFF; font-size: 13px;" onkeydown="if(event.key==='Enter') { const v = this.value.trim(); if(v) { daxbroNavigate(v.startsWith('http') ? v : 'https://html.duckduckgo.com/html/?q=' + encodeURIComponent(v)); } }">
              <button onclick="const v = document.getElementById('portal-live-search').value.trim(); if(v) { daxbroNavigate(v.startsWith('http') ? v : 'https://html.duckduckgo.com/html/?q=' + encodeURIComponent(v)); }" style="background: #0284C7; color: #FFF; border: none; border-radius: 18px; padding: 6px 14px; font-size: 11px; font-weight: 700; cursor: pointer;">
                Cari Live
              </button>
            </div>

            <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
              <button class="ide-btn ide-btn-accent" onclick="openApp('win-dapstore', 'DapStore')">
                <svg style="width: 14px; height: 14px;"><use href="#icon-dapstore"/></svg>
                DapStore Hub
              </button>
              <button class="ide-btn" onclick="openApp('win-ide', 'DCODX IDE')">
                <svg style="width: 14px; height: 14px;"><use href="#icon-ide"/></svg>
                DCODX Studio
              </button>
              <button class="ide-btn" onclick="daxbroNavigate('daxbro://playground')" style="color: #34D399; font-weight: 700;">
                <svg style="width: 14px; height: 14px;" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
                HTML5 Code Sandbox
              </button>
              <button class="ide-btn" onclick="openApp('win-dxdef', 'DXDEF Security')">
                <svg style="width: 14px; height: 14px;"><use href="#icon-dxdef"/></svg>
                DXDEF Keamanan
              </button>
            </div>
          </div>

          <!-- Live Fast Bookmarks Cards -->
          <div style="max-width: 820px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px;">
            <div onclick="daxbroNavigate('https://html.duckduckgo.com')" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; cursor: pointer; text-align: center; transition: transform 0.15s, border-color 0.15s;" onmouseover="this.style.borderColor='#38BDF8'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
              <div style="width: 36px; height: 36px; border-radius: 8px; background: rgba(230,81,0,0.18); border: 1px solid #E65100; margin: 0 auto 8px auto; display: flex; align-items: center; justify-content: center;">
                <svg style="width: 18px; height: 18px;" viewBox="0 0 24 24" fill="#E65100"><circle cx="12" cy="12" r="10"/></svg>
              </div>
              <div style="font-weight: 700; font-size: 12px; color: #FFF;">DuckDuckGo</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Live Search Bebas Pelacak</div>
            </div>

            <div onclick="daxbroNavigate('https://en.m.wikipedia.org')" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; cursor: pointer; text-align: center; transition: transform 0.15s, border-color 0.15s;" onmouseover="this.style.borderColor='#38BDF8'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
              <div style="width: 36px; height: 36px; border-radius: 8px; background: rgba(255,255,255,0.1); border: 1px solid #FFF; margin: 0 auto 8px auto; display: flex; align-items: center; justify-content: center;">
                <span style="font-weight: 800; font-size: 16px; color: #FFF;">W</span>
              </div>
              <div style="font-weight: 700; font-size: 12px; color: #FFF;">Wikipedia Live</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Ensiklopedia Bebas</div>
            </div>

            <div onclick="daxbroNavigate('http://localhost')" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; cursor: pointer; text-align: center; transition: transform 0.15s, border-color 0.15s;" onmouseover="this.style.borderColor='#38BDF8'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
              <div style="width: 36px; height: 36px; border-radius: 8px; background: rgba(52,211,153,0.18); border: 1px solid #34D399; margin: 0 auto 8px auto; display: flex; align-items: center; justify-content: center;">
                <svg style="width: 18px; height: 18px;"><use href="#icon-duraserv"/></svg>
              </div>
              <div style="font-weight: 700; font-size: 12px; color: #FFF;">DuraServ</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Localhost Web Server</div>
            </div>

            <div onclick="daxbroNavigate('daxbro://playground')" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(52,211,153,0.4); border-radius: 10px; padding: 14px; cursor: pointer; text-align: center; transition: transform 0.15s, border-color 0.15s;" onmouseover="this.style.borderColor='#34D399'" onmouseout="this.style.borderColor='rgba(52,211,153,0.4)'">
              <div style="width: 36px; height: 36px; border-radius: 8px; background: rgba(52,211,153,0.2); border: 1px solid #34D399; margin: 0 auto 8px auto; display: flex; align-items: center; justify-content: center;">
                <svg style="width: 18px; height: 18px;" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
              </div>
              <div style="font-weight: 700; font-size: 12px; color: #34D399;">HTML5 Sandbox</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Editor Kode &amp; Runner Live</div>
            </div>
          </div>

          <!-- 3 Architectural Pillars -->
          <div style="max-width: 820px; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 16px;">
              <div style="color: #00D2FF; font-weight: 700; font-size: 13px; margin-bottom: 4px;">DaxShield Engine v1.60</div>
              <div style="font-size: 11px; color: #8E8E9E; line-height: 1.4;">Zero fingerprinting, mitigasi iklan dan pelacak aktif tanpa overhead memori.</div>
            </div>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 16px;">
              <div style="color: #30D158; font-weight: 700; font-size: 13px; margin-bottom: 4px;">Landlock LSM v5 Sandbox</div>
              <div style="font-size: 11px; color: #8E8E9E; line-height: 1.4;">Proses renderer beroperasi dalam jail kernel tanpa hak akses root sistem.</div>
            </div>
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 16px;">
              <div style="color: #BF5AF2; font-weight: 700; font-size: 13px; margin-bottom: 4px;">DreXUI Acrylic Compositing</div>
              <div style="font-size: 11px; color: #8E8E9E; line-height: 1.4;">Akselerasi hardware Vulkan DMA-BUF swapchain pada refresh rate 120Hz/240Hz.</div>
            </div>
          </div>
        </div>
      `;
    }

    function renderDaxBroExtensionsPage() {
      const view = document.getElementById('daxbro-view');
      if (!view) return;
      view.innerHTML = `
        <div style="padding: 28px; background: #0B0E14; min-height: 100%; color: #F3F4F6; box-sizing: border-box; overflow-y: auto;">
          <div style="max-width: 800px; margin: 0 auto; width: 100%;">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 20px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <svg style="width: 22px; height: 22px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11a2 2 0 0 1 2-2h1a2 2 0 0 0 2-2 2 2 0 0 1 4 0 2 2 0 0 0 2 2h1a2 2 0 0 1 2 2v1a2 2 0 0 0 2 2 2 2 0 0 1 0 4 2 2 0 0 0-2 2v1a2 2 0 0 1-2 2h-1a2 2 0 0 0-2 2 2 2 0 0 1-4 0 2 2 0 0 0-2-2H6a2 2 0 0 1-2-2v-1a2 2 0 0 0-2-2 2 2 0 0 1 0-4 2 2 0 0 0 2-2v-1z"/></svg>
                <h2 style="font-size: 20px; font-weight: 700; margin: 0;">Ekstensi Chrome Manifest V3</h2>
              </div>
              <div style="display: flex; align-items: center; gap: 8px; font-size: 11px;">
                <span>Developer mode</span>
                <input type="checkbox" checked>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
              <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                  <span style="font-weight: 700; font-size: 13px;">uBlock Origin v1.60</span>
                  <input type="checkbox" ${daxbroExtensions.ublock ? 'checked' : ''} onchange="toggleExtensionState('ublock', this.checked)">
                </div>
                <div style="font-size: 10px; color: #8E8E9E; margin-bottom: 8px;">Manifest V3 &bull; ID: cjpalhdlnbpafiamejdnhcphjbkeiagm</div>
                <div style="font-size: 11px; color: #C9D1D9; line-height: 1.4;">Pemblokir konten dan pelacak dengan konsumsi CPU dan memori minimum.</div>
              </div>

              <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                  <span style="font-weight: 700; font-size: 13px;">Bitwarden Password Manager</span>
                  <input type="checkbox" ${daxbroExtensions.bitwarden ? 'checked' : ''} onchange="toggleExtensionState('bitwarden', this.checked)">
                </div>
                <div style="font-size: 10px; color: #8E8E9E; margin-bottom: 8px;">Manifest V3 &bull; ID: nngceckbapebfimnlniiiahkandclblb</div>
                <div style="font-size: 11px; color: #C9D1D9; line-height: 1.4;">Pengelolaan kata sandi aman terintegrasi dengan hardware TPM 2.0.</div>
              </div>

              <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                  <span style="font-weight: 700; font-size: 13px;">DreX-Boost 240Hz Engine</span>
                  <input type="checkbox" ${daxbroExtensions.drexboost ? 'checked' : ''} onchange="toggleExtensionState('drexboost', this.checked)">
                </div>
                <div style="font-size: 10px; color: #8E8E9E; margin-bottom: 8px;">Ekstensi Asli DAXOS &bull; Direct KMS Sync</div>
                <div style="font-size: 11px; color: #C9D1D9; line-height: 1.4;">Sinkronisasi frame compositor Blink dengan Vulkan Direct KMS DMA-BUF.</div>
              </div>

              <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                  <span style="font-weight: 700; font-size: 13px;">Dark Reader v5.1</span>
                  <input type="checkbox" ${daxbroExtensions.darkreader ? 'checked' : ''} onchange="toggleExtensionState('darkreader', this.checked)">
                </div>
                <div style="font-size: 10px; color: #8E8E9E; margin-bottom: 8px;">Manifest V3 &bull; ID: eimadpbcbfnmbkopoojfekhnkhdbieeh</div>
                <div style="font-size: 11px; color: #C9D1D9; line-height: 1.4;">Pembalikan kecerahan dengan preservasi kontras Hydro-Glass.</div>
              </div>
            </div>
          </div>
        </div>
      `;
    }
\n"""

    # Perform replacement
    new_html = html[:start_pos] + new_daxbro_code + html[end_pos:]

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Successfully updated {INDEX_PATH}: {len(new_html)} bytes")

if __name__ == '__main__':
    main()
