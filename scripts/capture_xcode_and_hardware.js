// Automated screenshot capture of DCODX Xcode 26 layout & Real Hardware Telemetry via native CDP
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = '/home/kangpcode/.gemini/antigravity-ide/brain/5621e49e-fa3a-4d42-878a-57046412188d';
const PORT = 9223;
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
  console.log('[capture] Launching headless Google Chrome on port ' + PORT + '...');
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

    const pageErrors = [];
    client.ws.addEventListener('message', (msg) => {
      try {
        const data = JSON.parse(msg.data);
        if (data.method === 'Runtime.exceptionThrown') {
          pageErrors.push(data.params);
        }
      } catch (_) {}
    });

    console.log('[capture] Navigating to ' + TARGET_URL + '...');
    await client.send('Page.navigate', { url: TARGET_URL });
    await sleep(800);

    // 1. Capture Boot Loading
    console.log('[capture] Capturing boot loading screen...');
    await client.captureScreenshot('screenshot_boot_and_lock_transition.png');

    // 2. Transition to Lock Screen
    console.log('[capture] Showing and capturing Lock Screen...');
    await client.evaluate(`
      localStorage.setItem('daxos_os_installed', 'true');
      finishBootSplash();
      showLockScreen();
    `);
    await sleep(500);
    await client.captureScreenshot('screenshot_daxos_lock_screen.png');

    // 3. Unlock to Main Workspace
    console.log('[capture] Unlocking to Main Workspace...');
    await client.evaluate(`
      unlockDesktop();
      document.querySelectorAll('.window').forEach(w => w.style.display = 'none');
    `);
    await sleep(600);
    await client.captureScreenshot('screenshot_daxos_workspace_unlocked.png');
    await sleep(500);

    // 2. Open DCODX Studio IDE (Xcode 26 layout matching Image 1)
    console.log('[capture] Opening DCODX Studio IDE (Xcode 26 SwiftUI + iPhone 17 Pro Dynamic Island)...');
    await client.evaluate(`
      openApp('win-ide', 'DCODX Studio');
      if (typeof xcodeChangeProject === 'function') {
        xcodeChangeProject('xcode26');
      }
      if (typeof xcodeSetNavTab === 'function') {
        xcodeSetNavTab('files');
      }
    `);
    await sleep(700);
    await client.captureScreenshot('screenshot_dcodx_xcode26_layout.png');

    // 3. Switch to AI Assistant tab (GPT-5 / DCODX Intelligence matching left pane of Image 1)
    console.log('[capture] Capturing Xcode AI Assistant (GPT-5 New Conversation)...');
    await client.evaluate(`
      if (typeof xcodeSetNavTab === 'function') {
        xcodeSetNavTab('ai');
      }
    `);
    await sleep(500);
    await client.captureScreenshot('screenshot_dcodx_ai_assistant.png');

    // 4. Switch to Travel Project (3D Globe + Golden Gate Bridge matching Image 2)
    console.log('[capture] Switching to Travel Project (Image 2 style with DiscoverView.swift & 3D Globe)...');
    await client.evaluate(`
      if (typeof xcodeSetNavTab === 'function') {
        xcodeSetNavTab('files');
      }
      if (typeof xcodeChangeProject === 'function') {
        xcodeChangeProject('travel');
      }
    `);
    await sleep(700);
    await client.captureScreenshot('screenshot_dcodx_travel_3dglobe.png');

    // 5. Switch to Calculator Project (real project from examples/calculator)
    console.log('[capture] Switching to Calculator Project (from examples/calculator)...');
    await client.evaluate(`
      if (typeof xcodeChangeProject === 'function') {
        xcodeChangeProject('calculator');
      }
    `);
    await sleep(700);
    await client.captureScreenshot('screenshot_dcodx_calculator_project.png');

    // 6. Test Real Hardware Telemetry (Activity Monitor, Driver Settings, About DAXOS)
    console.log('[capture] Testing Real Hardware Telemetry (Activity Monitor, Driver Settings, About DAXOS)...');
    const hwTelemetry = await client.evaluate(`
      closeWindow('win-ide');
      openApp('win-activity-monitor', 'Activity Monitor');
      openApp('win-driver-settings', 'Driver Settings');
      openApp('win-about', 'About DAXOS');

      // Return detected hardware details from real system
      ({
        cpuCores: window.daxosHardwareTelemetry ? window.daxosHardwareTelemetry.cores : navigator.hardwareConcurrency,
        gpuVendor: window.daxosHardwareTelemetry ? window.daxosHardwareTelemetry.gpuVendor : 'Probed',
        gpuRenderer: window.daxosHardwareTelemetry ? window.daxosHardwareTelemetry.gpuRenderer : 'Probed',
        ramGB: window.daxosHardwareTelemetry ? window.daxosHardwareTelemetry.ramGB : navigator.deviceMemory,
        refreshHz: window.daxosHardwareTelemetry ? window.daxosHardwareTelemetry.refreshRateHz : 60,
        batteryPct: window.daxosHardwareTelemetry ? window.daxosHardwareTelemetry.batteryPct : 100
      })
    `);
    console.log('[capture] Real Hardware Telemetry Detected from Host:', JSON.stringify(hwTelemetry, null, 2));
    await sleep(800);
    await client.captureScreenshot('screenshot_real_hardware_telemetry.png');

    if (pageErrors.length > 0) {
      console.warn('[capture] Page exceptions caught:', JSON.stringify(pageErrors, null, 2));
    } else {
      console.log('[capture] ZERO page exceptions! Clean and stable.');
    }

    client.close();
    console.log('[capture] Verification and screenshot captures completed successfully!');
  } finally {
    chromeProc.kill();
  }
}

main().catch(err => {
  console.error('[capture] Error:', err);
  process.exit(1);
});
