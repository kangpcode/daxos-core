//! ============================================================================
//! DAXOS REGISTRY DAEMON CLI / MAIN SERVICE (dap-registryd)
//! File: crates/dap-registryd/src/main.rs
//! ============================================================================

use dap_registryd::{run_socket_server, RegistryService};
use std::env;
use std::sync::atomic::AtomicBool;
use std::sync::Arc;

fn print_usage() {
    println!("DAXOS Central System Registry Daemon (dap-registryd) v1.0.0");
    println!("Usage:");
    println!("  dap-registryd [options]");
    println!();
    println!("Options:");
    println!("  --db-path <path>       Path to registry SQLite database (default: /var/lib/daxos/registry.db)");
    println!("  --socket <path>        Path to Unix domain socket (default: /run/daxos/registry.sock)");
    println!("  --status               Print registry status & statistics then exit");
    println!("  --init-db              Initialize schema and exit");
    println!("  --help                 Show this help message");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut db_path = "/var/lib/daxos/registry.db".to_string();
    let mut socket_path = "/run/daxos/registry.sock".to_string();
    let mut status_only = false;
    let mut init_only = false;

    // Use fallback directories if running as unprivileged user
    if !std::path::Path::new("/var/lib/daxos").exists() {
        db_path = "/tmp/daxos_registry.db".to_string();
    }
    if !std::path::Path::new("/run/daxos").exists() {
        socket_path = "/tmp/daxos_registry.sock".to_string();
    }

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--db-path" => {
                if i + 1 < args.len() {
                    db_path = args[i + 1].clone();
                    i += 1;
                }
            }
            "--socket" => {
                if i + 1 < args.len() {
                    socket_path = args[i + 1].clone();
                    i += 1;
                }
            }
            "--status" => {
                status_only = true;
            }
            "--init-db" => {
                init_only = true;
            }
            "--help" | "-h" => {
                print_usage();
                return;
            }
            unknown => {
                eprintln!("Unknown argument: {}", unknown);
                print_usage();
                std::process::exit(1);
            }
        }
        i += 1;
    }

    println!("================================================================");
    println!("    DAXOS REGISTRY DAEMON (dap-registryd)                       ");
    println!("================================================================");
    println!("Database Path : {}", db_path);
    println!("Socket Path   : {}", socket_path);

    let service = match RegistryService::new_from_path(&db_path) {
        Ok(s) => Arc::new(s),
        Err(e) => {
            eprintln!("Failed to initialize SQLite registry: {}", e);
            std::process::exit(1);
        }
    };

    if init_only {
        println!("[OK] Registry database schema initialized successfully.");
        return;
    }

    if status_only {
        match service.get_statistics() {
            Ok(stats) => {
                println!("=== REGISTRY STATUS ===");
                println!("Active Boot Slot  : {}", stats["active_boot_slot"]);
                println!("System Nodes      : {}", stats["nodes_count"]);
                println!("Bootloader Slots  : {}", stats["boot_slots_count"]);
                println!("Drivers Registered: {}", stats["drivers_count"]);
                println!("Applications      : {}", stats["applications_count"]);
            }
            Err(e) => {
                eprintln!("Error querying registry: {}", e);
                std::process::exit(1);
            }
        }
        return;
    }

    let stop_flag = Arc::new(AtomicBool::new(false));
    let stop_signal = Arc::clone(&stop_flag);

    // Run socket server in foreground or thread
    let s_path = socket_path.clone();
    let service_clone = Arc::clone(&service);

    let handle = std::thread::spawn(move || {
        if let Err(e) = run_socket_server(service_clone, &s_path, stop_signal) {
            eprintln!("Server error: {}", e);
        }
    });

    println!("Registry service is running. Press Ctrl+C to terminate.");
    let _ = handle.join();
}
