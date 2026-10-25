//! ============================================================================
//! DAXOS UNIVERSAL RUNTIME CLI (dax-run)
//! File: crates/dap-compat/src/main.rs
//! Purpose: CLI Dispatcher to launch Windows, macOS, Debian/Ubuntu & DAXOS apps
//! Lead Architect: Dhafa Nazula Permadi (kangpcode)
//! ============================================================================

use dap_compat::{inspect_binary_file, UniversalRunner};
use std::env;
use std::path::Path;

fn print_usage() {
    println!("DAXOS Universal Application Runner (dax-run) v1.10.2026 'Rhino'");
    println!("Lead Architect: Dhafa Nazula Permadi (@kangpcode)");
    println!();
    println!("Usage:");
    println!("  dax-run <path_to_binary> [args...]");
    println!("  dax-run --game <path_to_game_exe> [args...]");
    println!("  dax-run --inspect <path_to_binary>");
    println!("  dax-run --list-runtimes");
    println!("  dax-run --help");
    println!();
    println!("Supported Target Environments:");
    println!("  - Windows PE (.exe, .msi, PE32+) via DaxWinBridge (Wine / DXVK)");
    println!("  - Windows Games (Direct3D 9-12) via DaxProtonBridge (Vulkan DXVK 2.3 / Esync / Fsync)");
    println!("  - Apple macOS (.app, Mach-O universal) via DaxMacBridge (Darling / Cocoa)");
    println!("  - Debian / Ubuntu (.deb, ELF Linux) via DaxDebBridge (Bubblewrap / glibc)");
    println!("  - ARM64 Universal SoC (Qualcomm Snapdragon / MediaTek Dimensity) via DaxArmBridge");
    println!("  - DAXOS Native (.dapp fat binary) via DreX Landlock v5 Sandbox");
}

fn print_runtimes() {
    println!("=== DAXOS UNIVERSAL RUNTIME SUBSYSTEM STATUS ===");
    println!("OS Kernel          : Linux 6.6.21-daxos-hardened x86_64 / ARM64");
    println!("Display Compositor : DreX Wayland Acrylic (60Hz / 120Hz Universal)");
    println!("Processors Support : AMD Ryzen (Zen 1-5), Intel Core Ultra (All Gens),");
    println!("                     Qualcomm Snapdragon X Elite, MediaTek Dimensity 9000+, SPARC64");
    println!();
    println!("Runtimes Active:");
    println!("  [READY] DaxWinBridge    : Windows PE32+ Subsystem (DirectX -> Vulkan DXVK)");
    println!("  [READY] DaxProtonBridge : High-Performance Gaming Subsystem (Esync/Fsync, DXVK 2.3, VKD3D)");
    println!("  [READY] DaxMacBridge    : macOS Mach-O Subsystem (Cocoa -> DreXUI Bridge)");
    println!("  [READY] DaxDebBridge    : Debian / Ubuntu Multiarch Subsystem (.deb / glibc)");
    println!("  [READY] DaxArmBridge    : Snapdragon X Elite & MediaTek ARM64 JIT Bridge");
    println!("  [READY] DaxNativeCore   : Universal Signed .dapp Fat Binary Engine");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        return;
    }

    match args[1].as_str() {
        "--help" | "-h" => print_usage(),
        "--list-runtimes" => print_runtimes(),
        "--game" => {
            if args.len() < 3 {
                eprintln!("Error: Please provide a game binary path to execute.");
                std::process::exit(1);
            }
            let file_path = Path::new(&args[2]);
            let pass_args = if args.len() > 3 { &args[3..] } else { &[] };
            match UniversalRunner::run_game(file_path, pass_args) {
                Ok(msg) => {
                    println!("[OK] {}", msg);
                }
                Err(e) => {
                    eprintln!("Gaming execution error: {}", e);
                    std::process::exit(1);
                }
            }
        }
        "--inspect" => {
            if args.len() < 3 {
                eprintln!("Error: Please provide a file to inspect.");
                std::process::exit(1);
            }
            let file_path = Path::new(&args[2]);
            match inspect_binary_file(file_path) {
                Ok(info) => {
                    println!("=== BINARY COMPATIBILITY INSPECTION ===");
                    println!("File Path      : {}", info.file_path);
                    println!("Platform       : {}", info.platform);
                    println!("Architecture   : {}", info.architecture);
                    println!("Executable     : {}", info.is_executable);
                    println!("Sandboxed      : {}", info.requires_sandbox);
                    println!("Subsystem      : {}", info.runtime_subsystem);
                    println!("Details        : {}", info.details);
                }
                Err(e) => {
                    eprintln!("Inspection failed: {}", e);
                    std::process::exit(1);
                }
            }
        }
        target_path => {
            let file_path = Path::new(target_path);
            let pass_args = if args.len() > 2 { &args[2..] } else { &[] };

            match UniversalRunner::run(file_path, pass_args) {
                Ok(msg) => {
                    println!("[OK] {}", msg);
                }
                Err(e) => {
                    eprintln!("Execution error: {}", e);
                    std::process::exit(1);
                }
            }
        }
    }
}
