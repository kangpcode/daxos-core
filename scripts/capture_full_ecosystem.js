// Automated Screenshot Capture via Chrome DevTools Protocol (CDP) & Node native WebSocket
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = '/home/kangpcode/.gemini/antigravity-ide/brain/5621e49e-fa3a-4d42-878a-57046412188d';
const PORT = 9222;
const TARGET_URL = 'http://localhost:8089/';

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.id = 0;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (msg) => {
        const data = JSON.parse(msg.data);
        if (data.id && this.callbacks.has(data.id)) {
          const { resolve, reject } = this.callbacks.get(data.id);
          this.callbacks.delete(data.id);
          if (data.error) reject(data.error);
          else resolve(data.result);
        }
      };
    });
  }

  async send(method, params = {}) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    return res.result?.value;
  }

  async captureScreenshot(filename) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    const buffer = Buffer.from(res.data, 'base64');
    const outPath = path.join(ARTIFACT_DIR, filename);
    fs.writeFileSync(outPath, buffer);
    console.log(`[Captured] ${filename} (${buffer.length} bytes)`);
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function main() {
  console.log('[capture] Starting headless Google Chrome with remote debugging on port 9222...');
  const chromeProc = spawn('google-chrome', [
    '--headless',
    '--remote-debugging-port=' + PORT,
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1440,900',
    'about:blank'
  ]);

  await sleep(1500);

  try {
    // Get list of targets
    const targetsRes = await fetch(`http://localhost:${PORT}/json/list`);
    const targets = await targetsRes.json();
    const pageTarget = targets.find(t => t.type === 'page');
    if (!pageTarget) throw new Error('No page target found');

    console.log('[capture] Connecting to CDP WebSocket:', pageTarget.webSocketDebuggerUrl);
    const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await client.connect();

    await client.send('Page.enable');
    await client.send('Runtime.enable');

    console.log('[capture] Navigating to:', TARGET_URL);
    await client.send('Page.navigate', { url: TARGET_URL });
    await sleep(2500);

    // 1. Capture Boot Splash Screen
    console.log('[capture] Capturing Boot Splash Screen...');
    await client.evaluate(`
      const splash = document.getElementById('boot-splash');
      if (splash) {
        splash.style.display = 'flex';
        splash.style.opacity = '1';
        document.getElementById('boot-progress-bar').style.width = '68%';
        document.getElementById('boot-log-text').textContent = '[    0.410940] DaxProton DirectX 12/11 -> Vulkan translation pipeline initialized';
      }
    `);
    await sleep(300);
    await client.captureScreenshot('screenshot_boot_splash.png');

    // 2. Capture Lock Screen
    console.log('[capture] Capturing Lock Screen...');
    await client.evaluate(`
      document.getElementById('boot-splash').style.display = 'none';
      const lock = document.getElementById('lock-screen');
      if (lock) {
        lock.style.display = 'flex';
        lock.style.opacity = '1';
        lock.style.transform = 'translateY(0)';
      }
      updateLockClock();
      updateLockCredentials();
    `);
    await sleep(300);
    await client.captureScreenshot('screenshot_lock_screen.png');

    // 3. Unlock to Clean Desktop Workspace (Zero leaked text, pristine wallpaper)
    console.log('[capture] Unlocking to Clean Desktop Workspace...');
    await client.evaluate(`
      document.getElementById('lock-screen').style.display = 'none';
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_desktop_clean.png');

    // 4. Open Setup Assistant at Step 3 (User Account Setup with Full Name, Username, Optional Password)
    console.log('[capture] Capturing Setup Assistant (User Account Creation)...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-installer', 'Install DAXOS');
      installerStep = 3;
      document.getElementById('inst-step-1').style.display = 'none';
      document.getElementById('inst-step-2').style.display = 'none';
      document.getElementById('inst-step-3').style.display = 'flex';
      document.getElementById('inst-step-4').style.display = 'none';
      document.getElementById('inst-step-5').style.display = 'none';
      document.getElementById('inst-step-6').style.display = 'none';
      document.getElementById('inst-back-btn').style.display = 'inline-block';
      document.getElementById('inst-next-btn').style.display = 'inline-block';
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_installer_account.png');

    // 5. Open Network & DNS Manager
    console.log('[capture] Capturing Network & DNS Manager...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-network-manager', 'Network & DNS Manager');
      selectNetTab('dns');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_network_manager.png');

    // 6. Open Application Manager (Remove Programs)
    console.log('[capture] Capturing Application Manager...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-app-manager', 'App Manager');
      selectAppFilter('all');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_app_manager.png');

    // 7. Open Gaming Hub
    console.log('[capture] Capturing DAXOS Gaming Hub...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-gaming-hub', 'Gaming Hub');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_gaming_hub.png');

    // 8. Open Terminal and execute daxfetch & dax-run
    console.log('[capture] Capturing Terminal with daxfetch & dax-run...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-terminal', 'Terminal');
      runTerminal('daxfetch');
      runTerminal('dax-run --game /games/cyberpunk2077.exe');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_terminal_daxfetch.png');

    client.close();
    console.log('[capture] All screenshots captured successfully!');
  } finally {
    chromeProc.kill();
  }
}

main().catch(err => {
  console.error('[capture] Error:', err);
  process.exit(1);
});
