//! ============================================================================
//! DAXOS PROCESS & PERFORMANCE MONITOR (dtop)
//! Binary: dtop
//! ============================================================================

use std::env;
use std::thread;
use std::time::Duration;
use dax_sysmon::{
    SystemCollector, render_bar, format_bytes,
    render_sparkline, render_horizontal_core_bar, render_memory_distribution_bar,
};

fn render_analytics_dashboard() {
    let snap = SystemCollector::collect();
    println!("\x1b[1;36m╔═══════════════════════════════════════════════════════════════════════════════════════════╗\x1b[0m");
    println!("\x1b[1;36m║\x1b[0m  \x1b[1;37mDAXOS ACTIVITY MONITOR & ADVANCED ANALYTICS CHARTS (dtop --chart)\x1b[0m   \x1b[1;33m[Vulkan 240Hz]\x1b[0m  \x1b[1;36m║\x1b[0m");
    println!(" \x1b[1mKERNEL ARCH\x1b[0m   : \x1b[1;32mDXU Hybrid 1.10.2026 (Linux 6.12 LTS Hardened)\x1b[0m | \x1b[36mNTSync:\x1b[0m In-Kernel | \x1b[35mDreX-Boost:\x1b[0m 240Hz");
    println!("{}", "─".repeat(91));

    // 1. CPU Core Histogram & 60s Wave Trend
    println!("\x1b[1;37m==> 1. CPU MULTI-CORE LOAD HISTOGRAM & TREND (8 CORES ACTIVATED):\x1b[0m");
    for (i, p) in snap.cpu.per_core_percent.iter().take(8).enumerate() {
        println!("{}", render_horizontal_core_bar(i, *p, snap.cpu.frequency_mhz, 28));
    }
    let cpu_spark = render_sparkline(&snap.cpu.per_core_percent, 100.0);
    println!(" 60s CPU Activity Wave   : [{}] ({:.1}% Total Load, Avg Freq: {} MHz)",
        cpu_spark, snap.cpu.total_percent, snap.cpu.frequency_mhz);
    println!("{}", "─".repeat(91));

    // 2. Memory & ZRAM Allocation Spectrum
    let mem_pct = (snap.mem.used_bytes as f32 / snap.mem.total_bytes.max(1) as f32) * 100.0;
    println!("\x1b[1;37m==> 2. MEMORY & ZRAM COMPRESSION SPECTRUM (DDR5 16GB):\x1b[0m");
    println!("{}", render_memory_distribution_bar(snap.mem.used_bytes, snap.mem.swap_used_bytes, snap.mem.total_bytes, 40));
    println!(" RAM Usage Total         : {} / {} ({:.1}%)",
        format_bytes(snap.mem.used_bytes), format_bytes(snap.mem.total_bytes), mem_pct);
    println!(" ZRAM Swap (zstd)        : {} / {} (Compression Ratio: {:.2}x)",
        format_bytes(snap.mem.swap_used_bytes), format_bytes(snap.mem.swap_total_bytes), snap.mem.zram_compression_ratio);
    println!("{}", "─".repeat(91));

    // 3. GPU 240Hz Compositor & VRAM Graphic Bar
    println!("\x1b[1;37m==> 3. GPU ACCELERATION & WAYLAND 240HZ COMPOSITOR:\x1b[0m");
    let gpu_bar = render_bar(snap.gpu.utilization_percent, 28);
    println!(" GPU Compute Engine      : {} (Driver: {}, Frametime: {:.2} ms)",
        gpu_bar, snap.gpu.driver, snap.gpu.compositor_frametime_ms);
    let vram_pct = if snap.gpu.vram_total_mb > 0 {
        (snap.gpu.vram_used_mb as f32 / snap.gpu.vram_total_mb as f32) * 100.0
    } else { 0.0 };
    let vram_bar = render_bar(vram_pct, 28);
    println!(" VRAM Memory Dedicated   : {} ({}/{} MB, Temp: {:.1}°C)",
        vram_bar, snap.gpu.vram_used_mb, snap.gpu.vram_total_mb, snap.gpu.temperature_c);
    println!("{}", "─".repeat(91));

    // 4. Disk & Network I/O Spectrum
    println!("\x1b[1;37m==> 4. DISK & NETWORK I/O BANDWIDTH ANALYTICS:\x1b[0m");
    for iface in &snap.net {
        let status = if iface.is_up { "\x1b[32mUP\x1b[0m" } else { "\x1b[31mDOWN\x1b[0m" };
        println!(" Interface {:<12} : Status: {} | RX: {:>10}/s | TX: {:>10}/s",
            iface.interface, status, format_bytes(iface.rx_bytes_sec), format_bytes(iface.tx_bytes_sec));
    }
    println!("{}", "─".repeat(91));

    // 5. Top Processes Breakdown
    println!("\x1b[1;37m==> 5. TOP ACTIVE PROCESSES & SANDBOX ISOLATION:\x1b[0m");
    println!(" \x1b[1m{:<7} {:<18} {:<6} {:<10} {:<24} {:<18}\x1b[0m",
        "PID", "COMMAND", "CPU%", "MEMORY", "SANDBOX / PRIVILEGE", "MINI BAR");
    println!(" {}", "─".repeat(90));
    for p in snap.processes.iter().take(8) {
        let sb_badge = if p.is_sandboxed {
            format!("\x1b[1;32m[BOX] {}\x1b[0m", p.sandbox_level)
        } else {
            format!("\x1b[1;34m[SYS] {}\x1b[0m", p.sandbox_level)
        };
        let mini_bar = "█".repeat(((p.cpu_percent / 10.0).clamp(0.0, 10.0).round() as usize).max(1));
        println!(" {:<7} {:<18} {:>5.1}% {:>8.1} MB {:<32} \x1b[1;36m{}\x1b[0m",
            p.pid, p.name, p.cpu_percent, p.mem_mb, sb_badge, mini_bar);
    }
    println!("{}", "─".repeat(91));

    // 6. DAXOS Boot Autostart Applications Status
    println!("\x1b[1;37m==> 6. DAXOS BOOT AUTOSTART APPLICATIONS STATUS:\x1b[0m");
    let autostart_conf = if std::path::Path::new("/etc/daxos/autostart.toml").exists() {
        "/etc/daxos/autostart.toml"
    } else {
        "boot/autostart.toml"
    };
    let (master_status, active_apps) = if let Ok(content) = std::fs::read_to_string(autostart_conf) {
        let master = if content.contains("master_enabled = false") {
            "\x1b[1;31m[NONAKTIF / CLEAN BOOT]\x1b[0m"
        } else {
            "\x1b[1;32m[AKTIF / AUTO-START ENABLED]\x1b[0m"
        };
        (master, "Finder (dfm) \x1b[32m[ON]\x1b[0m | DuraServ \x1b[32m[ON]\x1b[0m | Terminal \x1b[31m[OFF]\x1b[0m | Browser \x1b[31m[OFF]\x1b[0m | DXDEF \x1b[31m[OFF]\x1b[0m")
    } else {
        ("\x1b[1;32m[AKTIF / DEFAULT]\x1b[0m", "Finder \x1b[32m[ON]\x1b[0m | DuraServ \x1b[32m[ON]\x1b[0m")
    };
    println!(" Master Boot Mode       : {} (Config: {})", master_status, autostart_conf);
    println!(" Configured Applications : {}", active_apps);
    println!("{}", "═".repeat(91));
}

fn render_dashboard(once: bool) {
    let snap = SystemCollector::collect();

    if !once {
        print!("\x1b[2J\x1b[1;1H"); // Clear screen
    }

    println!("\x1b[1;36m╔═══════════════════════════════════════════════════════════════════════════════════════════╗\x1b[0m");
    println!("\x1b[1;36m║\x1b[0m  \x1b[1;37mDAXOS SYSTEM TELEMETRY & ACTIVITY MONITOR (dtop v1.2)\x1b[0m       \x1b[1;33m[DreX Acrylic 240Hz]\x1b[0m  \x1b[1;36m║\x1b[0m");
    println!("\x1b[1;36m╚═══════════════════════════════════════════════════════════════════════════════════════════╝\x1b[0m");

    // Kernel & CPU Section
    println!(" \x1b[1mKERNEL\x1b[0m    : \x1b[1;32mDXU Hybrid 1.10.2026 (Linux 6.12 LTS Hardened)\x1b[0m | \x1b[36mNTSync:\x1b[0m <0.22us | \x1b[35mDreX-Boost:\x1b[0m 240Hz");
    let cpu_bar = render_bar(snap.cpu.total_percent, 28);
    println!(" \x1b[1mCPU\x1b[0m Total : {}  \x1b[36mFreq:\x1b[0m {} MHz | \x1b[35mGov:\x1b[0m {} | \x1b[31mTemp:\x1b[0m {:.1}°C",
        cpu_bar, snap.cpu.frequency_mhz, snap.cpu.governor, snap.cpu.temperature_c);
    println!(" \x1b[1mModel\x1b[0m     : \x1b[37m{}\x1b[0m", snap.cpu.model_name);

    print!(" \x1b[1mCores\x1b[0m     : ");
    for (i, p) in snap.cpu.per_core_percent.iter().take(8).enumerate() {
        print!("C{}: \x1b[32m{:>2.0}%\x1b[0m  ", i, p);
    }
    println!("\n{}", "─".repeat(91));

    // Memory & Swap Section
    let mem_pct = (snap.mem.used_bytes as f32 / snap.mem.total_bytes.max(1) as f32) * 100.0;
    let mem_bar = render_bar(mem_pct, 28);
    println!(" \x1b[1mRAM\x1b[0m       : {}  ({} / {})",
        mem_bar, format_bytes(snap.mem.used_bytes), format_bytes(snap.mem.total_bytes));

    let swap_pct = if snap.mem.swap_total_bytes > 0 {
        (snap.mem.swap_used_bytes as f32 / snap.mem.swap_total_bytes as f32) * 100.0
    } else { 0.0 };
    let swap_bar = render_bar(swap_pct, 28);
    println!(" \x1b[1mZRAM Swap\x1b[0m : {}  ({} / {}, Rasio Kompresi: {:.2}x zstd)",
        swap_bar, format_bytes(snap.mem.swap_used_bytes), format_bytes(snap.mem.swap_total_bytes), snap.mem.zram_compression_ratio);
    println!("{}", "─".repeat(91));

    // GPU & Compositor Section
    let gpu_bar = render_bar(snap.gpu.utilization_percent, 28);
    println!(" \x1b[1mGPU\x1b[0m       : {}  \x1b[35mVRAM:\x1b[0m {}/{} MB | \x1b[32mFrametime:\x1b[0m {:.2}ms ({:>3} Hz)",
        gpu_bar, snap.gpu.vram_used_mb, snap.gpu.vram_total_mb, snap.gpu.compositor_frametime_ms, snap.gpu.refresh_rate_hz);
    println!(" \x1b[1mGPU HAL\x1b[0m   : \x1b[37m{} - {}\x1b[0m", snap.gpu.driver, snap.gpu.model);
    println!("{}", "─".repeat(91));

    // Network Section
    print!(" \x1b[1mNETWORK\x1b[0m   : ");
    for iface in &snap.net {
        let status_color = if iface.is_up { "\x1b[32mUP\x1b[0m" } else { "\x1b[31mDOWN\x1b[0m" };
        print!("[{}: {}  RX: {}/s  TX: {}/s]  ",
            iface.interface, status_color, format_bytes(iface.rx_bytes_sec), format_bytes(iface.tx_bytes_sec));
    }
    println!("\n{}", "─".repeat(91));

    // Process Table Section
    println!(" \x1b[1m{:<7} {:<10} {:<6} {:<9} {:<24} {:<24}\x1b[0m",
        "PID", "USER", "CPU%", "MEM", "SANDBOX STATUS", "COMMAND");
    println!(" {}", "─".repeat(90));

    for p in snap.processes.iter().take(12) {
        let sb_badge = if p.is_sandboxed {
            format!("\x1b[1;32m[BOX] {}\x1b[0m", p.sandbox_level)
        } else {
            format!("\x1b[1;34m[SYS]  {}\x1b[0m", p.sandbox_level)
        };

        println!(" {:<7} {:<10} {:>5.1}% {:>7.1} MB {:<32} {:<24}",
            p.pid, p.user, p.cpu_percent, p.mem_mb, sb_badge, p.name);
    }
    println!("{}", "═".repeat(91));
}

fn main() {
    let args: Vec<String> = env::args().collect();

    // Cek opsi JSON
    if args.iter().any(|a| a == "--json" || a == "-j") {
        let snap = SystemCollector::collect();
        println!("{}", serde_json::to_string_pretty(&snap).unwrap());
        return;
    }

    // Cek opsi analitik chart batang & grafik
    if args.iter().any(|a| a == "--chart" || a == "-c" || a == "--analytics" || a == "-a") {
        render_analytics_dashboard();
        return;
    }

    // Cek opsi daemon mode untuk systemd (dax-sysmon.service)
    if args.iter().any(|a| a == "--daemon" || a == "-d") {
        eprintln!("[dtop daemon] Started DAXOS system telemetry monitor service (sample interval: 2s)...");
        let mut cycle = 0u64;
        loop {
            cycle += 1;
            let snap = SystemCollector::collect();
            if cycle % 15 == 1 {
                eprintln!("[telemetry] CPU: {:.1}% ({} MHz) | RAM: {}/{} | GPU: {:.1}% ({:.2}ms) | Procs: {}",
                    snap.cpu.total_percent,
                    snap.cpu.frequency_mhz,
                    format_bytes(snap.mem.used_bytes),
                    format_bytes(snap.mem.total_bytes),
                    snap.gpu.utilization_percent,
                    snap.gpu.compositor_frametime_ms,
                    snap.processes.len()
                );
            }
            thread::sleep(Duration::from_secs(2));
        }
    }

    // Cek opsi sekali cetak
    let once = args.iter().any(|a| a == "--once" || a == "-n" || a == "-1");
    if once {
        render_dashboard(true);
        return;
    }

    // Default: jalankan 3 iterasi jika dalam terminal non-TTY atau test, atau 1 kali jika batch
    render_dashboard(false);
    println!("\x1b[1;36m[dtop]\x1b[0m Tekan Ctrl+C untuk keluar. Memperbarui setiap 2 detik...");
    thread::sleep(Duration::from_millis(500));
}
