// ============================================================================
// SURFLANG BRANDING & SHOWCASE INTERACTION ENGINE
// File: web-surflang/app.js
// Purpose: Interactive Multi-Monitor Visualizer, Playground Compiler & Live UI
// Architect: Dhafa Nazula Permadi (@kangpcode)
// Strictly ZERO Emojis
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
  initMultiMonitorSimulator();
  initPlayground();
  initCopyButton();
});

// ----------------------------------------------------------------------------
// 1. PRESET SURFLANG EXAMPLES
// ----------------------------------------------------------------------------
const SURFLANG_EXAMPLES = {
  calculator: `module daxos.calculator;
import surf.ui;

component CalculatorApp: Component {
    @State var displayValue: String = "42";
    @State var currentOperation: String = "";
    @State var storedOperand: Float = 0.0;
    @State var isEnteringSecondOperand: Bool = false;
    @State var acrylicBlurRadius: Int32 = 36;

    func render() -> ViewNode {
        return Window(title: "Calculator — DreXUI") {
            VStack(spacing: 12) {
                Text(self.displayValue)
                    .font(.system(size: 32, weight: .bold))
                    .frame(maxWidth: .infinity, alignment: .trailing);
                
                Grid(columns: 4, spacing: 8) {
                    Button("C")   { self.clear(); }
                    Button("+/-") { self.toggleSign(); }
                    Button("%")   { self.applyPercent(); }
                    Button("/")   { self.setOp("/"); }
                    
                    Button("7")   { self.appendDigit("7"); }
                    Button("8")   { self.appendDigit("8"); }
                    Button("9")   { self.appendDigit("9"); }
                    Button("*")   { self.setOp("*"); }
                    
                    Button("4")   { self.appendDigit("4"); }
                    Button("5")   { self.appendDigit("5"); }
                    Button("6")   { self.appendDigit("6"); }
                    Button("-")   { self.setOp("-"); }
                    
                    Button("1")   { self.appendDigit("1"); }
                    Button("2")   { self.appendDigit("2"); }
                    Button("3")   { self.appendDigit("3"); }
                    Button("+")   { self.setOp("+"); }
                    
                    Button("0")   { self.appendDigit("0"); }
                    Button("00")  { self.appendDigit("00"); }
                    Button(".")   { self.appendDecimal(); }
                    Button("=")   { self.evaluate(); }
                }
            }
            .padding(16)
            .glassEffect(blurRadius: self.acrylicBlurRadius, opacity: 0.72)
        };
    }
}`,

  multimonitor: `module daxos.display.canvas;
import surf.display;
import surf.ui;

component MultiMonitorDisplayPanel: Component {
    @State var topology: DisplayMode = .extended;
    @State var primaryScreen: DisplayOutput = DisplayOutput(id: 1, name: "eDP-1", width: 1920, height: 1080);
    @State var externalScreen: DisplayOutput = DisplayOutput(id: 2, name: "HDMI-A-1", width: 3840, height: 2160);
    @State var refreshRateHz: Int32 = 144;

    func switchMode(target: DisplayMode) {
        self.topology = target;
        // Mengirim instruksi atomic wayland ke DreX Compositor
        DisplayManager.setTopology(mode: target);
    }

    func render() -> ViewNode {
        return Window(title: "Multi-Display Topology") {
            VStack(spacing: 16) {
                Text("Monitor Setup: eDP-1 + HDMI-A-1 4K").font(.headline);
                HStack(spacing: 12) {
                    Button(self.topology == .extended ? "[AKTIF] Extended" : "Perluas Tampilan") {
                        self.switchMode(.extended);
                    }
                    Button(self.topology == .mirror ? "[AKTIF] Mirror" : "Duplikat Tampilan") {
                        self.switchMode(.mirror);
                    }
                }
            }
            .glassEffect(blurRadius: 36, opacity: 0.8)
        };
    }
}`,

  preferences: `module daxos.preferences;
import surf.ui;
import surf.core;

component SystemSettingsPanel: Component {
    @State var acrylicOpacity: Float = 0.72;
    @State var blurRadiusPx: Int32 = 36;
    @State var spatialAudioEnabled: Bool = true;
    @State var updateChannel: String = "stable";

    func render() -> ViewNode {
        return Window(title: "System Preferences") {
            VStack(spacing: 14) {
                Text("DreXUI Acrylic Vibrancy Control").font(.headline);
                Slider(value: $self.acrylicOpacity, in: 0.2...1.0, label: "Opasitas Akrilik");
                Slider(value: $self.blurRadiusPx, in: 8...64, label: "Radius Blur (px)");
                Toggle("Spatial Audio HRTF 3D DSP", isOn: $self.spatialAudioEnabled);
            }
            .padding(18)
            .glassEffect(blurRadius: self.blurRadiusPx, opacity: self.acrylicOpacity)
        };
    }
}`,

  audio: `module daxos.audio.dsp;
import surf.audio;
import surf.ui;

component ParametricEqualizer: Component {
    @State var masterGainDb: Float = 0.0;
    @State var preset: String = "Acoustic Clarity";
    @State var bands: [Float] = [0.0, 1.5, 2.0, 0.0, -1.0, 0.5, 1.8, 3.0, 2.5, 1.0];

    func applyPreset(name: String) {
        self.preset = name;
        PipeWireDSP.set10BandGains(self.bands);
    }

    func render() -> ViewNode {
        return Window(title: "10-Band Parametric Equalizer") {
            VStack(spacing: 10) {
                Text("Preset: " + self.preset).font(.subheadline);
                HStack(spacing: 6) {
                    ForEach(self.bands) { gain in
                        Gauge(value: gain, in: -12.0...12.0);
                    }
                }
            }
            .glassEffect(blurRadius: 32, opacity: 0.75)
        };
    }
}`,

  sandbox: `module daxos.security.vault;
import surf.security;
import surf.ui;

component LandlockSecureVault: Component {
    @State var isEnforced: Bool = true;
    @State var allowedPaths: [String] = ["/home/daxuser/Documents", "/tmp"];
    @State var tpm2KeyPresent: Bool = true;

    func enforcePolicy() {
        LandlockSandbox.enforceAbiV5(paths: self.allowedPaths);
        self.isEnforced = true;
    }

    func render() -> ViewNode {
        return Window(title: "Landlock Security Guard") {
            VStack(spacing: 12) {
                Badge("LANDLOCK LSM ABI v5: ENFORCED", color: .green);
                Text("Isolation status: Zero root privileges, Strict Seccomp BPF");
            }
            .glassEffect(blurRadius: 36, opacity: 0.8)
        };
    }
}`
};

// ----------------------------------------------------------------------------
// 2. MULTI-MONITOR DISPLAY SIMULATOR
// ----------------------------------------------------------------------------
function initMultiMonitorSimulator() {
  const btnExtended = document.getElementById('btn-mode-extended');
  const btnMirror = document.getElementById('btn-mode-mirror');
  const canvasBoundsLabel = document.getElementById('canvas-bounds-label');
  const extSpecs = document.getElementById('ext-specs');
  const cardExtended = document.getElementById('detail-extended');
  const cardMirror = document.getElementById('detail-mirror');
  const simCard = document.querySelector('.display-simulator-card');
  const monitorExternal = document.getElementById('monitor-external');

  if (!btnExtended || !btnMirror) return;

  function setMode(mode) {
    if (mode === 'extended') {
      btnExtended.classList.add('active');
      btnMirror.classList.remove('active');
      cardExtended.classList.add('active-card');
      cardMirror.classList.remove('active-card');
      simCard.classList.remove('mirror-active');
      canvasBoundsLabel.textContent = 'Virtual Canvas: 5760 x 2160 px (Topology: Extended)';
      extSpecs.textContent = '3840 \u00d7 2160 @ 144Hz \u2022 Offset (1920, 0)';
      
      // Kembalikan tampilan jendela monitor eksternal
      const existingClone = monitorExternal.querySelector('.duplicate-clone-box');
      if (existingClone) existingClone.remove();
      const extWin = monitorExternal.querySelector('.win-external');
      if (extWin) extWin.style.display = 'block';
    } else {
      btnMirror.classList.add('active');
      btnExtended.classList.remove('active');
      cardMirror.classList.add('active-card');
      cardExtended.classList.remove('active-card');
      simCard.classList.add('mirror-active');
      canvasBoundsLabel.textContent = 'Virtual Canvas: 1920 x 1080 px (Topology: Mirror Cloned)';
      extSpecs.textContent = '3840 \u00d7 2160 (Cloned from eDP-1) \u2022 Offset (0, 0)';

      // Tampilkan indikator kloning duplikat pada layar eksternal
      const extContent = monitorExternal.querySelector('.screen-content');
      const extWin = monitorExternal.querySelector('.win-external');
      if (extWin) extWin.style.display = 'none';

      let cloneBox = monitorExternal.querySelector('.duplicate-clone-box');
      if (!cloneBox && extContent) {
        cloneBox = document.createElement('div');
        cloneBox.className = 'duplicate-clone-box';
        cloneBox.innerHTML = '<strong>[MIRROR CLONE]</strong><br>Swapchain Duplikasi Terpasang Langsung ke eDP-1';
        extContent.appendChild(cloneBox);
      }
    }
  }

  btnExtended.addEventListener('click', () => setMode('extended'));
  btnMirror.addEventListener('click', () => setMode('mirror'));
  setMode('extended');
}

// ----------------------------------------------------------------------------
// 3. PLAYGROUND, COMPILER & LIVE UI ENGINE
// ----------------------------------------------------------------------------
let currentCalcState = {
  display: '42',
  prevVal: 0,
  op: null,
  clearOnNext: false
};

function initPlayground() {
  const codeTextarea = document.getElementById('code-input');
  const exampleSelect = document.getElementById('example-select');
  const btnCompile = document.getElementById('btn-compile');
  const btnReset = document.getElementById('btn-reset-code');
  const editorStatus = document.getElementById('editor-status');
  const lineColDisplay = document.getElementById('editor-line-col');

  if (!codeTextarea || !exampleSelect) return;

  // Load default example
  codeTextarea.value = SURFLANG_EXAMPLES.calculator;

  exampleSelect.addEventListener('change', (e) => {
    const val = e.target.value;
    if (SURFLANG_EXAMPLES[val]) {
      codeTextarea.value = SURFLANG_EXAMPLES[val];
      triggerCompilation();
    }
  });

  btnReset.addEventListener('click', () => {
    const val = exampleSelect.value;
    codeTextarea.value = SURFLANG_EXAMPLES[val] || SURFLANG_EXAMPLES.calculator;
    triggerCompilation();
  });

  codeTextarea.addEventListener('input', () => {
    editorStatus.textContent = 'Status: Dimodifikasi (Belum Dikompilasi)';
    editorStatus.className = 'status-compiling';
  });

  codeTextarea.addEventListener('keyup', updateCursorPosition);
  codeTextarea.addEventListener('click', updateCursorPosition);

  function updateCursorPosition() {
    const pos = codeTextarea.selectionStart;
    const text = codeTextarea.value.substring(0, pos);
    const lines = text.split('\n');
    const lineNum = lines.length;
    const colNum = lines[lines.length - 1].length + 1;
    if (lineColDisplay) {
      lineColDisplay.textContent = `Baris: ${lineNum} \u2022 Kolom: ${colNum}`;
    }
  }

  btnCompile.addEventListener('click', triggerCompilation);

  // Tab switching logic
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add('active');
    });
  });

  // Initial compilation
  triggerCompilation();
}

function triggerCompilation() {
  const codeTextarea = document.getElementById('code-input');
  const editorStatus = document.getElementById('editor-status');
  const llvmOutput = document.getElementById('llvm-output');
  const previewTitle = document.getElementById('preview-title');
  const previewBody = document.getElementById('preview-body');
  const repStateVars = document.getElementById('rep-state-vars');
  const repMultiMon = document.getElementById('rep-multi-mon');

  if (!codeTextarea) return;

  const code = codeTextarea.value;
  editorStatus.textContent = 'Status: Mengompilasi...';
  editorStatus.className = 'status-compiling';

  // Extract module name & state vars client-side for instant responsive UI
  const modMatch = code.match(/module\s+([a-zA-Z0-9_.]+);/);
  const moduleName = modMatch ? modMatch[1] : 'daxos.custom';
  const stateMatches = [...code.matchAll(/@State\s+var\s+([a-zA-Z0-9_]+)/g)].map(m => m[1]);
  if (repStateVars) {
    repStateVars.textContent = stateMatches.length > 0 ? stateMatches.join(', ') : 'Tidak ada (Statik)';
  }

  const isMultiMon = code.includes('Display') || code.includes('display') || code.includes('extended') || code.includes('mirror');
  if (repMultiMon) {
    repMultiMon.textContent = isMultiMon ? 'Ya (Extended & Mirror Ready)' : 'Single Viewport';
  }

  if (previewTitle) {
    previewTitle.textContent = `${moduleName} \u2014 DreXUI`;
  }
  renderInteractiveComponent(code, previewBody);

  // Attempt backend API compilation; fallback to local simulation
  fetch('/api/compile', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source: code })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'SUCCESS') {
      editorStatus.textContent = 'Status: Sukses [0 Error, LLVM IR Terverifikasi]';
      editorStatus.className = 'status-ready';
      if (llvmOutput) {
        llvmOutput.innerHTML = `<code>; ModuleID = '${moduleName}.surf'\nsource_filename = "${moduleName}.surf"\ntarget datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"\ntarget triple = "x86_64-unknown-linux-gnu"\n\ndeclare void @drex_ui_emit_node(i8*, i32)\ndeclare void @drex_drop_glue(i8*)\ndeclare void @drex_wayland_present_frame(i64, i32)\n\ndefine dso_local void @render_view_init() #0 {\nentry:\n  %reg0 = alloca i8, align 8 ; GlassConfigPayload\n  ; emit UI component nodes (Total @State vars: ${stateMatches.length})\n  call void @drex_ui_emit_node(i8* null, i32 4)\n  call void @drex_drop_glue(i8* %reg0)\n  ret void\n}\n\nattributes #0 = { noinline nounwind optnone sspstrong uwtable }</code>`;
      }
    } else {
      editorStatus.textContent = 'Status: Peringatan Kompilasi';
      editorStatus.className = 'status-compiling';
    }
  })
  .catch(() => {
    // Client-side simulation fallback
    editorStatus.textContent = 'Status: Sukses [Client-Side DreX Simulation]';
    editorStatus.className = 'status-ready';
    if (llvmOutput) {
      llvmOutput.innerHTML = `<code>; ModuleID = '${moduleName}.surf'\nsource_filename = "${moduleName}.surf"\ntarget datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"\ntarget triple = "x86_64-unknown-linux-gnu"\n\ndeclare void @drex_ui_emit_node(i8*, i32)\ndeclare void @drex_drop_glue(i8*)\n\ndefine dso_local void @render_view_init() #0 {\nentry:\n  %reg0 = alloca i8, align 8 ; GlassConfigPayload\n  call void @drex_ui_emit_node(i8* null, i32 4)\n  call void @drex_drop_glue(i8* %reg0)\n  ret void\n}\n\nattributes #0 = { noinline nounwind optnone sspstrong uwtable }</code>`;
    }
  });
}

function renderInteractiveComponent(code, container) {
  if (!container) return;

  if (code.includes('CalculatorApp') || code.includes('calculator')) {
    container.innerHTML = `
      <div class="calc-display" id="c-display">42</div>
      <div class="calc-grid">
        <button class="c-btn op-btn" data-act="c">C</button>
        <button class="c-btn op-btn" data-act="sign">+/-</button>
        <button class="c-btn op-btn" data-act="pct">%</button>
        <button class="c-btn op-btn" data-act="/">/</button>
        
        <button class="c-btn num-btn" data-num="7">7</button>
        <button class="c-btn num-btn" data-num="8">8</button>
        <button class="c-btn num-btn" data-num="9">9</button>
        <button class="c-btn op-btn" data-act="*">*</button>
        
        <button class="c-btn num-btn" data-num="4">4</button>
        <button class="c-btn num-btn" data-num="5">5</button>
        <button class="c-btn num-btn" data-num="6">6</button>
        <button class="c-btn op-btn" data-act="-">-</button>
        
        <button class="c-btn num-btn" data-num="1">1</button>
        <button class="c-btn num-btn" data-num="2">2</button>
        <button class="c-btn num-btn" data-num="3">3</button>
        <button class="c-btn op-btn" data-act="+">+</button>
        
        <button class="c-btn num-btn" data-num="0">0</button>
        <button class="c-btn num-btn" data-num="00">00</button>
        <button class="c-btn num-btn" data-act="dot">.</button>
        <button class="c-btn eq-btn" data-act="eq">=</button>
      </div>
    `;

    // Hook interactive calculator buttons
    currentCalcState = { display: '42', prevVal: 0, op: null, clearOnNext: false };
    const displayEl = container.querySelector('#c-display');

    container.querySelectorAll('.c-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const num = btn.getAttribute('data-num');
        const act = btn.getAttribute('data-act');

        if (num !== null) {
          if (currentCalcState.clearOnNext || currentCalcState.display === '0') {
            currentCalcState.display = num;
            currentCalcState.clearOnNext = false;
          } else {
            currentCalcState.display += num;
          }
        } else if (act === 'c') {
          currentCalcState.display = '0';
          currentCalcState.prevVal = 0;
          currentCalcState.op = null;
        } else if (act === 'sign') {
          const val = parseFloat(currentCalcState.display) || 0;
          currentCalcState.display = (-val).toString();
        } else if (act === 'pct') {
          const val = parseFloat(currentCalcState.display) || 0;
          currentCalcState.display = (val / 100).toString();
        } else if (act === 'dot') {
          if (!currentCalcState.display.includes('.')) {
            currentCalcState.display += '.';
          }
        } else if (['+', '-', '*', '/'].includes(act)) {
          currentCalcState.prevVal = parseFloat(currentCalcState.display) || 0;
          currentCalcState.op = act;
          currentCalcState.clearOnNext = true;
        } else if (act === 'eq') {
          if (currentCalcState.op) {
            const current = parseFloat(currentCalcState.display) || 0;
            let res = 0;
            if (currentCalcState.op === '+') res = currentCalcState.prevVal + current;
            if (currentCalcState.op === '-') res = currentCalcState.prevVal - current;
            if (currentCalcState.op === '*') res = currentCalcState.prevVal * current;
            if (currentCalcState.op === '/') res = current !== 0 ? currentCalcState.prevVal / current : 0;
            currentCalcState.display = Math.round(res * 10000) / 10000 + '';
            currentCalcState.op = null;
            currentCalcState.clearOnNext = true;
          }
        }

        if (displayEl) displayEl.textContent = currentCalcState.display;
      });
    });
  } else if (code.includes('MultiMonitor') || code.includes('DisplayMode')) {
    container.innerHTML = `
      <div style="text-align: center; padding: 20px;">
        <h4 style="color: var(--primary-cyan); font-family: var(--font-heading); margin-bottom: 8px;">Topologi Multi-Monitor Aktif</h4>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 16px;">Output: eDP-1 (1920x1080) + HDMI-A-1 (3840x2160 4K)</p>
        <div style="display: flex; gap: 8px; justify-content: center;">
          <button class="btn btn-sm btn-primary" style="font-size: 0.75rem;">Extended Mode</button>
          <button class="btn btn-sm btn-outline" style="font-size: 0.75rem;">Mirror Mode</button>
        </div>
      </div>
    `;
  } else if (code.includes('SystemSettings') || code.includes('acrylicOpacity')) {
    container.innerHTML = `
      <div style="padding: 16px; font-size: 0.85rem;">
        <div style="margin-bottom: 12px; font-weight: 600; color: var(--primary-cyan);">Pengaturan Tampilan & DSP</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span>Opasitas Akrilik:</span> <strong style="color: var(--accent-mint)">0.72</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span>Radius Blur:</span> <strong style="color: var(--primary-cyan)">36 px</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span>Spatial Audio PipeWire:</span> <strong style="color: var(--accent-mint)">AKTIF</strong>
        </div>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div style="padding: 20px; text-align: center; color: var(--accent-mint); font-family: var(--font-code); font-size: 0.85rem;">
        [OK] DreXUI Reactive Component Ready<br>
        Rendering 240Hz ProMotion Surface
      </div>
    `;
  }
}

// ----------------------------------------------------------------------------
// 4. CLIPBOARD COPY HELPER
// ----------------------------------------------------------------------------
function initCopyButton() {
  const copyBtn = document.getElementById('copy-install-btn');
  if (!copyBtn) return;

  copyBtn.addEventListener('click', () => {
    const textToCopy = 'curl -sSf https://surflang.daxos.org/install.sh | sh';
    navigator.clipboard.writeText(textToCopy).then(() => {
      copyBtn.textContent = 'Tersalin!';
      copyBtn.style.background = '#00F5A0';
      copyBtn.style.color = '#030612';
      setTimeout(() => {
        copyBtn.textContent = 'Salin';
        copyBtn.style.background = '';
        copyBtn.style.color = '';
      }, 2000);
    });
  });
}
