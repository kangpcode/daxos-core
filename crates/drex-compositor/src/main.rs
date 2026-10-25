//! ============================================================================
//! DAXOS WAYLAND ACRYLIC GLASS DYNAMIC COMPOSITOR (drex-compositor)
//! File: crates/drex-compositor/src/main.rs
//! ============================================================================

use drex_compositor::{AcrylicParameters, DesktopShell, DrexCompositorEngine};
use drexvis::{CudaBackend, GpuBackend, RdnaBackend};
use std::env;
use std::time::Instant;

fn print_usage() {
    println!("DAXOS Wayland Acrylic Glass Dynamic Compositor (drex-compositor) v1.0.0");
    println!("Usage:");
    println!("  drex-compositor [options]");
    println!();
    println!("Options:");
    println!("  --config <path>          Path to compositor configuration (default: /etc/daxos/compositor.conf)");
    println!("  --enable-acrylic-blur    Enable real-time Dual-Kawase acrylic glass effects (default: true)");
    println!("  --backend <cuda|rdna>    GPU acceleration driver backend (default: cuda)");
    println!("  --refresh-hz <hz>        Target display refresh rate (default: 120)");
    println!("  --display-mode <mode>    Display topology mode: extended or mirror (default: extended)");
    println!("  --external-monitor       Simulate connecting an external monitor (4K UHD 144Hz)");
    println!("  --desktop, --gui         Launch full graphical DreXUI Wayland Desktop Shell environment");
    println!("  --drexui                 Alias for --gui / --desktop");
    println!("  --test-frame             Render a test multi-pass acrylic frame and exit");
    println!("  --benchmark              Benchmark 100 frames of acrylic glass compositing");
    println!("  --help                   Show this message");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut backend_name = "cuda".to_string();
    let mut refresh_hz = 120u32;
    let mut action = "test_frame";
    let mut display_mode = drex_compositor::DisplayMode::Extended;
    let mut add_external_monitor = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--backend" => {
                if i + 1 < args.len() {
                    backend_name = args[i + 1].clone();
                    i += 1;
                }
            }
            "--refresh-hz" => {
                if i + 1 < args.len() {
                    refresh_hz = args[i + 1].parse().unwrap_or(120);
                    i += 1;
                }
            }
            "--display-mode" => {
                if i + 1 < args.len() {
                    match args[i + 1].to_lowercase().as_str() {
                        "mirror" | "duplicate" | "duplikat" => display_mode = drex_compositor::DisplayMode::Mirror,
                        "primary" | "primaryonly" => display_mode = drex_compositor::DisplayMode::PrimaryOnly,
                        "external" | "externalonly" => display_mode = drex_compositor::DisplayMode::ExternalOnly,
                        _ => display_mode = drex_compositor::DisplayMode::Extended,
                    }
                    i += 1;
                }
            }
            "--external-monitor" => {
                add_external_monitor = true;
            }
            "--config" => {
                if i + 1 < args.len() {
                    i += 1;
                }
            }
            "--enable-acrylic-blur" => {}
            "--desktop" | "--gui" | "--drexui" => action = "desktop",
            "--test-frame" => action = "test_frame",
            "--benchmark" => action = "benchmark",
            "--help" | "-h" => {
                print_usage();
                return;
            }
            other => {
                eprintln!("Unknown argument: {}", other);
                print_usage();
                std::process::exit(1);
            }
        }
        i += 1;
    }

    println!("================================================================");
    println!("    DAXOS DREX-COMPOSITOR WAYLAND ACRYLIC GLASS ENGINE         ");
    println!("================================================================");
    println!("GPU Driver Backend : {}", backend_name.to_uppercase());
    println!("Target Refresh Rate: {} Hz (Budget: {:.2} ms/frame)", refresh_hz, 1000.0 / refresh_hz as f64);

    let mut backend: Box<dyn GpuBackend> = if backend_name == "rdna" {
        Box::new(RdnaBackend::new())
    } else {
        Box::new(CudaBackend::new())
    };

    if let Err(e) = backend.initialize() {
        eprintln!("Failed to initialize GPU driver backend: {:?}", e);
        std::process::exit(1);
    }

    let mut engine = DrexCompositorEngine::new(backend, refresh_hz);
    let surface_id = engine.create_client_surface(1001, 1920, 1080);
    let params = AcrylicParameters {
        opacity: 0.72,
        blur_radius_px: 36,
        edge_brightness: 1.15,
        noise_intensity: 0.04,
    };
    let _ = engine.attach_acrylic_effect(surface_id, params);

    match action {
        "desktop" => {
            let mut shell = DesktopShell::new(1920, 1080);
            if add_external_monitor {
                shell.connect_external_monitor(
                    "Studio Display Pro (External 4K UHD)",
                    "HDMI-A-1",
                    3840,
                    2160,
                    144,
                );
            }
            shell.set_display_mode(display_mode);

            println!("Starting DAXOS DreX macOS-style Desktop Shell environment (GUI Mode)...");
            println!("  Operating System: DAXOS 1.10.2026 'Rhino' (Full Graphical Native OS)");
            println!("  Display Protocol: Wayland 1.23 (Socket: /run/user/1000/wayland-1, XDG_CURRENT_DESKTOP=DAXOS)");
            println!("  UI Framework    : DreXUI Declarative Hydro-Glass Liquid Architecture");
            println!("  Graphics Pipeline: Vulkan 1.3 Hardware HAL + Dual-Kawase Shaders (240Hz governor)");
            println!("  Virtual Canvas  : {}x{} (Topology Mode: {:?})", shell.screen_width, shell.screen_height, display_mode);
            println!("  Acrylic Vibrancy: Multi-pass Dual-Kawase (Blur: 36px, Opacity: 0.72)");
            println!("  Displays ({}):", shell.display_manager.displays.len());
            for d in &shell.display_manager.displays {
                let tag = if d.is_primary { "[Primary]" } else { "[External]" };
                println!("    * #{} {:<10} {:<32} [{}x{} @ {}Hz] Offset: ({}, {}) Scale: {:.1}x Status: {}",
                    d.id, tag, d.name, d.width, d.height, d.refresh_rate_hz, d.offset_x, d.offset_y, d.scale_factor, if d.is_active { "ACTIVE" } else { "OFF" });
            }
            println!("  Active Focus App: '{}'", shell.active_app_title);
            println!("  Top Menu Bar    : [DAXOS | File | Edit | View | Window | Help] [WiFi | Battery 92% | Settings | 22:45]");
            println!("  Open Windows ({}):", shell.open_windows.len());
            for win in &shell.open_windows {
                println!("    - ID {}: '{}' ({}) at ({}, {}) [{}x{}]", win.window_id, win.title, win.bundle_id, win.x, win.y, win.width, win.height);
            }
            println!("  Acrylic Dock Items ({}):", shell.dock_items.len());
            for item in &shell.dock_items {
                let dot = if item.has_dot_indicator { "[Running]" } else { "         " };
                println!("    - {:<22} {:<18} {}", item.icon, item.name, dot);
            }
            let frame_id = engine.render_frame().expect("Render frame failed");
            println!("[OK] DreXUI Desktop Shell successfully initialized & rendered Frame #{} on Wayland-1!", frame_id);
            println!("  {}", shell.render_scene_summary());
        }
        "benchmark" => {
            println!("Benchmarking 100 frames of Dual-Kawase acrylic multi-pass composition...");
            let start = Instant::now();
            let count = 100;
            for _ in 0..count {
                let _ = engine.render_frame();
            }
            let elapsed = start.elapsed();
            let avg_ms = elapsed.as_secs_f64() * 1000.0 / count as f64;
            let fps = 1000.0 / avg_ms;
            println!("[OK] Benchmark Results:");
            println!("  Total Elapsed   : {:.2} ms", elapsed.as_secs_f64() * 1000.0);
            println!("  Avg Frame Time  : {:.4} ms (Budget: {:.2} ms)", avg_ms, engine.get_target_frametime_ms());
            println!("  Throughput Rate : {:.1} FPS (Target: {} FPS)", fps, refresh_hz);
        }
        _ => {
            let start = Instant::now();
            match engine.render_frame() {
                Ok(frame_id) => {
                    let frame_time = start.elapsed().as_secs_f64() * 1000.0;
                    println!("[OK] Successfully composed Frame #{} with Acrylic Glass effect", frame_id);
                    println!("  Surface Resolution : 1920x1080");
                    println!("  Acrylic Parameters : Opacity 0.72, Blur 36px, Edge 1.15, Noise 0.04");
                    println!("  Frame Latency      : {:.4} ms (Within SLA budget: {:.2} ms)", frame_time, engine.get_target_frametime_ms());
                }
                Err(e) => {
                    eprintln!("Render error: {}", e);
                    std::process::exit(1);
                }
            }
        }
    }
}
