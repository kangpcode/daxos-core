//! ============================================================================
//! DAXOS PRODUCTION STORAGE & PARTITION MANAGER CLI (ddisk)
//! File: crates/dax-disks/src/main.rs
//! Purpose: Production CLI tool for storage devices and partitions
//! ============================================================================

use dax_disks::DiskScanner;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let subcmd = args.get(1).map(|s| s.as_str()).unwrap_or("list");

    match subcmd {
        "list" | "ls" => {
            println!("================================================================================");
            println!("  DAXOS STORAGE & BLOCK DEVICE SUBSYSTEM (ddisk)");
            println!("  Hardware Rootfs, Partitions, and Mount Analyzers");
            println!("================================================================================");
            println!("{:<12} {:<8} {:<10} {:<18} {:<16} {:<14}",
                "DEVICE", "TYPE", "SIZE", "MEDIA", "MOUNTPOINT", "USED / AVAIL");
            println!("--------------------------------------------------------------------------------");

            let devs = DiskScanner::get_block_devices();
            for d in &devs {
                // Filter out small loop devices from display unless verbose
                if d.name.starts_with("loop") && d.size_bytes < 100 * 1024 * 1024 {
                    continue;
                }

                let media = if d.name.starts_with("nvme") {
                    "NVMe SSD"
                } else if !d.is_rotational {
                    "SATA SSD"
                } else {
                    "HDD (Rotational)"
                };

                let dev_type = if d.is_partition { "part" } else { "disk" };
                let mp = d.mount_point.as_deref().unwrap_or("-");

                let usage = if let (Some(used), Some(avail)) = (d.used_bytes, d.avail_bytes) {
                    format!("{} / {}", DiskScanner::format_bytes(used), DiskScanner::format_bytes(avail))
                } else {
                    "-".to_string()
                };

                println!("{:<12} {:<8} {:<10} {:<18} {:<16} {:<14}",
                    d.name,
                    dev_type,
                    DiskScanner::format_bytes(d.size_bytes),
                    media,
                    mp,
                    usage
                );
            }
            println!("--------------------------------------------------------------------------------");
        }
        "mounts" => {
            println!("=== ACTIVE MOUNT POINTS ===");
            let mounts = DiskScanner::get_mounts();
            for m in mounts {
                if m.device.starts_with('/') {
                    println!("{:<24} on {:<20} type {:<10} ({})",
                        m.device, m.mount_point, m.fs_type, m.options);
                }
            }
        }
        "usage" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or("/");
            let (used, avail) = DiskScanner::get_statvfs_usage(target);
            if let (Some(u), Some(a)) = (used, avail) {
                let total = u + a;
                let pct = if total > 0 { (u as f64 / total as f64) * 100.0 } else { 0.0 };
                println!("Filesystem Usage for '{}':", target);
                println!("  Total Size : {}", DiskScanner::format_bytes(total));
                println!("  Used Space : {} ({:.1}%)", DiskScanner::format_bytes(u), pct);
                println!("  Free Space : {}", DiskScanner::format_bytes(a));
            } else {
                eprintln!("[ERROR] Failed to query filesystem stats for '{}'", target);
                std::process::exit(1);
            }
        }
        "json" => {
            let devs = DiskScanner::get_block_devices();
            let json = serde_json::to_string_pretty(&devs).unwrap();
            println!("{}", json);
        }
        _ => {
            println!("DAXOS Storage Manager (ddisk)");
            println!("Usage: ddisk [list | mounts | usage <path> | json]");
        }
    }
}
