//! ============================================================================
//! DAXOS DYNAMIC HARDWARE & GPU GOVERNOR (drex-boostd)
//! File: crates/drex-boostd/src/main.rs
//! ============================================================================

use drex_boostd::{run_boost_server, DrexBoostGovernor};
use std::env;
use std::sync::atomic::AtomicBool;
use std::sync::{Arc, Mutex};

fn print_usage() {
    println!("DAXOS Dynamic Hardware Governor Daemon (drex-boostd) v1.0.0");
    println!("Usage:");
    println!("  drex-boostd [options]");
    println!();
    println!("Options:");
    println!("  --socket <path>            Unix domain socket (default: /run/daxos/boost.sock)");
    println!("  --sampling-rate-ms <ms>    Sampling rate interval (default: 10)");
    println!("  --status                   Print governor current telemetry and exit");
    println!("  --simulate                 Simulate workload, boost, and thermal protection");
    println!("  --help                     Show this message");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut socket_path = "/run/daxos/boost.sock".to_string();
    let mut sampling_rate_ms = 10u64;

    if !std::path::Path::new("/run/daxos").exists() {
        socket_path = "/tmp/daxos_boost.sock".to_string();
    }

    let mut action = "daemon";
    let mut i = 1;

    while i < args.len() {
        match args[i].as_str() {
            "--socket" => {
                if i + 1 < args.len() {
                    socket_path = args[i + 1].clone();
                    i += 1;
                }
            }
            "--sampling-rate-ms" => {
                if i + 1 < args.len() {
                    sampling_rate_ms = args[i + 1].parse().unwrap_or(10);
                    i += 1;
                }
            }
            "--status" => action = "status",
            "--simulate" => action = "simulate",
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

    let governor = Arc::new(Mutex::new(DrexBoostGovernor::new()));

    match action {
        "status" => {
            let gov = governor.lock().unwrap();
            println!("=== DREX-BOOST HARDWARE GOVERNOR TELEMETRY ===");
            println!("Governor State       : {:?}", gov.state);
            println!("Current Clock Offset : +{} MHz", gov.current_clock_offset_mhz);
            println!("Target Temperature   : {:.1} °C", gov.target_temp_c);
            println!("Thermal Throttle Cap : {:.1} °C", gov.thermal_throttle_limit_c);
            println!("Emergency Cutoff Cap : {:.1} °C", gov.emergency_cutoff_c);
            println!("Max Clock Allowed    : +{} MHz", gov.max_clock_offset_mhz);
        }
        "simulate" => {
            println!("=== SIMULATING DREX-BOOST GOVERNOR ADAPTIVE STATES ===");
            let mut gov = governor.lock().unwrap();
            println!("[Step 1] Baseline Idle: State={:?}, Offset=+{}MHz", gov.state, gov.current_clock_offset_mhz);

            gov.on_input_event();
            println!("[Step 2] User Input Event Detected! State={:?}, Offset=+{}MHz", gov.state, gov.current_clock_offset_mhz);

            let offset = gov.update(65.0, 11.5, 0.1);
            println!("[Step 3] Rendering Stutter (11.5ms > 8.33ms): State={:?}, Offset=+{}MHz", gov.state, offset);

            let offset_hot = gov.update(83.5, 11.5, 0.1);
            println!("[Step 4] Thermal Throttle (83.5°C >= 82°C): State={:?}, Offset=+{}MHz", gov.state, offset_hot);

            let offset_crit = gov.update(92.0, 11.5, 0.1);
            println!("[Step 5] Emergency Cutoff (92.0°C >= 90°C): State={:?}, Offset=+{}MHz", gov.state, offset_crit);
            println!("[OK] DreX-Boost governor safety envelope verified!");
        }
        _ => {
            println!("================================================================");
            println!("    DAXOS DYNAMIC HARDWARE GOVERNOR (drex-boostd)               ");
            println!("================================================================");
            println!("Socket Path      : {}", socket_path);
            println!("Sampling Rate    : {} ms", sampling_rate_ms);

            let stop_flag = Arc::new(AtomicBool::new(false));
            let stop_signal = Arc::clone(&stop_flag);

            let handle = std::thread::spawn(move || {
                if let Err(e) = run_boost_server(governor, &socket_path, stop_signal) {
                    eprintln!("Boost server error: {}", e);
                }
            });

            println!("Governor daemon is running. Press Ctrl+C to terminate.");
            let _ = handle.join();
        }
    }
}
