// Automated screenshot capture of Camera Pro features and macOS Window Animations
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
  console.log('[capture] Starting headless Google Chrome for camera & animation captures...');
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
    const targetsRes = await fetch(`http://localhost:${PORT}/json/list`);
    const targets = await targetsRes.json();
    const pageTarget = targets.find(t => t.type === 'page');
    if (!pageTarget) throw new Error('No page target found');

    const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await client.connect();

    await client.send('Page.enable');
    await client.send('Runtime.enable');

    await client.send('Page.navigate', { url: TARGET_URL });
    await sleep(2500);

    // Skip boot splash and lock screen to clean desktop
    await client.evaluate(`
      document.getElementById('boot-splash').style.display = 'none';
      document.getElementById('lock-screen').style.display = 'none';
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
    `);

    // 1. Open Camera in "Presisi Asli 1:1 (True-Sight, Unmirrored)" mode with Pro Drawer open
    console.log('[capture] Capturing Camera in Presisi Asli 1:1 (True-Sight) with Pro Drawer...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-camera', 'Camera');
      isMirrored = false;
      applyCameraTransform();
      document.getElementById('cam-mirror-label').textContent = "PRESISI ASLI 1:1 (UNMIRRORED)";
      document.getElementById('cam-pro-drawer').style.display = 'grid';
      document.getElementById('cam-pro-btn').classList.add('active');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_camera_precision_unmirrored.png');

    // 2. Toggle to "Cermin Natural (Mirrored / Selfie)" mode
    console.log('[capture] Capturing Camera in Cermin Natural (Mirrored)...');
    await client.evaluate(`
      isMirrored = true;
      applyCameraTransform();
      document.getElementById('cam-mirror-label').textContent = "CERMIN NATURAL (MIRRORED)";
      document.getElementById('cam-mirror-btn').classList.add('active');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_camera_mirror_mode.png');

    // 3. Test Camera QuickLook Photo Review
    console.log('[capture] Capturing Camera QuickLook Photo Review Modal...');
    await client.evaluate(`
      triggerShutterAction();
      openPhotoReview();
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_camera_photo_review.png');
    await client.evaluate(`closePhotoReview();`);

    // 4. Test macOS Maximized Window state
    console.log('[capture] Capturing macOS Maximized Window state...');
    await client.evaluate(`
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
      openApp('win-camera', 'Camera');
      maximizeWindow('win-camera');
    `);
    await sleep(400);
    await client.captureScreenshot('screenshot_macos_window_maximized.png');
    await client.evaluate(`maximizeWindow('win-camera');`); // restore bounds

    // 5. Test macOS Control Center spring panel
    console.log('[capture] Capturing macOS Control Center Panel animation...');
    await client.evaluate(`
      document.getElementById('control-center').classList.add('open');
    `);
    await sleep(350);
    await client.captureScreenshot('screenshot_macos_control_center.png');
    await client.evaluate(`document.getElementById('control-center').classList.remove('open');`);

    client.close();
    console.log('[capture] Camera and animation captures finished successfully!');
  } finally {
    chromeProc.kill();
  }
}

main().catch(err => {
  console.error('[capture] Error:', err);
  process.exit(1);
});
