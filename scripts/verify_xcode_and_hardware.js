const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--use-gl=angle', '--use-angle=swiftshader']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  const consoleLogs = [];
  page.on('console', msg => consoleLogs.push({ type: msg.type(), text: msg.text() }));
  page.on('pageerror', err => consoleLogs.push({ type: 'error', text: err.toString() }));

  console.log('1. Loading desktop_preview at http://localhost:8089/index.html...');
  await page.goto('http://localhost:8089/index.html', { waitUntil: 'networkidle2' });

  // Wait 1.5 seconds for boot splash to complete or unlock
  await new Promise(r => setTimeout(r, 1600));

  // Take screenshot of desktop after boot
  const artifactDir = '/home/kangpcode/.gemini/antigravity-ide/brain/5621e49e-fa3a-4d42-878a-57046412188d';
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_daxos_boot_unlocked.png') });
  console.log('Saved screenshot_daxos_boot_unlocked.png');

  // Open DCODX Studio IDE (Xcode Layout)
  console.log('2. Opening DCODX Studio IDE (Xcode Layout)...');
  await page.evaluate(() => {
    // If lock screen is open, unlock it
    if (typeof unlockDesktop === 'function') unlockDesktop();
    openApp('win-ide', 'DCODX Studio');
    if (typeof xcodeChangeProject === 'function') {
      xcodeChangeProject('xcode26');
    }
  });

  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_dcodx_xcode26_swiftui.png') });
  console.log('Saved screenshot_dcodx_xcode26_swiftui.png');

  // Switch to Travel SwiftUI project
  console.log('3. Switching scheme to Travel project (3D Globe + Golden Gate Bridge)...');
  await page.evaluate(() => {
    if (typeof xcodeChangeProject === 'function') {
      xcodeChangeProject('travel');
    }
  });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_dcodx_xcode_travel.png') });
  console.log('Saved screenshot_dcodx_xcode_travel.png');

  // Switch to Calculator DreXUI project
  console.log('4. Switching scheme to Calculator project...');
  await page.evaluate(() => {
    if (typeof xcodeChangeProject === 'function') {
      xcodeChangeProject('calculator');
    }
  });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_dcodx_xcode_calculator.png') });
  console.log('Saved screenshot_dcodx_xcode_calculator.png');

  // Switch to AI Assistant tab in Left Pane
  console.log('5. Switching to AI Assistant tab (Image 1 style)...');
  await page.evaluate(() => {
    if (typeof xcodeSetNavTab === 'function') {
      xcodeSetNavTab('ai');
    }
  });
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_dcodx_xcode_ai_assistant.png') });
  console.log('Saved screenshot_dcodx_xcode_ai_assistant.png');

  // Open Activity Monitor & Driver Settings to verify real hardware telemetry
  console.log('6. Opening Activity Monitor and Driver Settings (Real Hardware Telemetry)...');
  await page.evaluate(() => {
    closeWindow('win-ide');
    openApp('win-activity-monitor', 'Activity Monitor');
    openApp('win-driver-settings', 'Driver Settings');
    openApp('win-about', 'About DAXOS');
  });
  await new Promise(r => setTimeout(r, 600));
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_hardware_telemetry_real.png') });
  console.log('Saved screenshot_hardware_telemetry_real.png');

  console.log('Console Logs count:', consoleLogs.length);
  const errors = consoleLogs.filter(l => l.type === 'error');
  if (errors.length > 0) {
    console.error('Browser Errors found:', errors);
  } else {
    console.log('ZERO BROWSER ERRORS! All quality gates passed cleanly.');
  }

  await browser.close();
})();
