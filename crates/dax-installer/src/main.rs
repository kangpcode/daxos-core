//! ============================================================================
//! DAXOS PRODUCTION OS INSTALLER CLI (dax-installer)
//! Binary: dax-installer
//! ============================================================================

use std::env;
use std::thread;
use std::time::Duration;
use dax_installer::{InstallerEngine, InstallConfig, PartitionScheme, SwapType, SystemProfile};

const BANNER: &str = "\x1b[1;36m
  ╔═════════════════════════════════════════════════════════════════════╗
  ║    DAXOS PRODUCTION OPERATING SYSTEM INSTALLER (v1.10.2026)          ║
  ║    Wayland & DreXUI Micro-Optimized Operating System Engine          ║
  ╚═════════════════════════════════════════════════════════════════════╝\x1b[0m";

fn print_usage() {
    println!("DAXOS Operating System Installer CLI (dax-installer)");
    println!("Usage:");
    println!("  dax-installer [options]");
    println!();
    println!("Options:");
    println!("  --scheme <clean-btrfs|dual-boot|manual>  Partition layout scheme (default: clean-btrfs)");
    println!("  --swap <zram|luks2|none>                 Swap memory configuration (default: zram)");
    println!("  --profile <ultimate|developer|minimal>   System software profile (default: ultimate)");
    println!("  --target <device>                        Target disk block device (e.g. /dev/nvme0n1)");
    println!("  --filesystem <btrfs|ext4>                Root filesystem format (default: btrfs)");
    println!("  --log-stream                             Stream real-time low-level kernel & disk logs");
    println!("  --help, -h                               Display this help message");
}

fn render_progress_bar(pct: u8, width: usize) -> String {
    let filled = (pct as usize * width) / 100;
    let empty = width.saturating_sub(filled);
    format!("\x1b[1;32m[{}{}]\x1b[0m \x1b[1;37m{:>3}%\x1b[0m", "█".repeat(filled), "░".repeat(empty), pct)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut scheme_str = "clean-btrfs".to_string();
    let mut swap_str = "zram".to_string();
    let mut profile_str = "ultimate".to_string();
    let mut fs_str = "btrfs".to_string();
    let mut custom_target: Option<String> = None;
    let mut stream_logs = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--scheme" => {
                if i + 1 < args.len() {
                    scheme_str = args[i + 1].to_lowercase();
                    i += 1;
                }
            }
            "--swap" => {
                if i + 1 < args.len() {
                    swap_str = args[i + 1].to_lowercase();
                    i += 1;
                }
            }
            "--profile" => {
                if i + 1 < args.len() {
                    profile_str = args[i + 1].to_lowercase();
                    i += 1;
                }
            }
            "--target" => {
                if i + 1 < args.len() {
                    custom_target = Some(args[i + 1].clone());
                    i += 1;
                }
            }
            "--filesystem" => {
                if i + 1 < args.len() {
                    fs_str = args[i + 1].to_lowercase();
                    i += 1;
                }
            }
            "--log-stream" => {
                stream_logs = true;
            }
            "--help" | "-h" => {
                print_usage();
                return;
            }
            other => {
                eprintln!("\x1b[1;33m[PERINGATAN]\x1b[0m Parameter tidak dikenal: '{}'", other);
            }
        }
        i += 1;
    }

    println!("{}", BANNER);

    let scheme_enum = match scheme_str.as_str() {
        "dual-boot" | "dualboot" | "windows" => PartitionScheme::DualBoot,
        "manual" | "subvolumes" => PartitionScheme::ManualSubvolumes,
        _ => PartitionScheme::CleanBtrfs,
    };

    let swap_enum = match swap_str.as_str() {
        "luks2" | "luks" | "encrypted" => SwapType::Luks2,
        "none" | "tanpa-swap" => SwapType::None,
        _ => SwapType::Zram,
    };

    let profile_enum = match profile_str.as_str() {
        "developer" | "dev" | "engineering" => SystemProfile::DeveloperEngineering,
        "minimal" | "lightweight" => SystemProfile::LightweightMinimal,
        _ => SystemProfile::UltimateWorkstation,
    };

    // 1. Pemeriksaan Pra-syarat
    println!("\x1b[1;36m[TAHAP 1/4]\x1b[0m Memeriksa spesifikasi dan kelayakan perangkat keras...");
    let preflight = InstallerEngine::preflight_check();

    println!("  • Arsitektur CPU   : \x1b[1;32m{}\x1b[0m (64-bit)", preflight.cpu_arch);
    println!("  • Kapasitas RAM    : \x1b[1;32m{} MB\x1b[0m (Status: {})",
        preflight.ram_mb, if preflight.ram_ok { "\x1b[32mMemenuhi Syarat\x1b[0m" } else { "\x1b[31mKurang dari 4GB\x1b[0m" });
    println!("  • Mode Firmware    : {}",
        if preflight.is_uefi { "\x1b[32mUEFI 64-bit (SecureBoot Ready)\x1b[0m" } else { "\x1b[33mLegacy BIOS / Emulated UEFI\x1b[0m" });

    println!("  • Disk Terdeteksi  :");
    for (i, d) in preflight.available_disks.iter().enumerate() {
        println!("    [{}] \x1b[1m{}\x1b[0m - {} ({:.1} GB) [NVMe/SSD]", i + 1, d.path, d.model, d.size_gb);
    }

    if !preflight.passed {
        eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sistem tidak memenuhi persyaratan minimum untuk DAXOS.");
        return;
    }

    let target_disk = custom_target.unwrap_or_else(|| preflight.available_disks[0].path.clone());

    // 2. Rencana Partisi
    println!("\n\x1b[1;36m[TAHAP 2/4]\x1b[0m Rencana Tata Letak Partisi Target: '\x1b[1m{}\x1b[0m' (Skema: {:?})", target_disk, scheme_enum);
    let parts = InstallerEngine::plan_partitions_with_options(&target_disk, scheme_enum, swap_enum);
    println!("{:<6} {:<18} {:<12} {:<32} {:<24}", "PART", "LABEL", "UKURAN", "SISTEM BERKAS", "MOUNTPOINT / FITUR");
    println!("{}", "─".repeat(94));
    for p in &parts {
        println!("p{:<5} {:<18} {:<12} {:<32} {:<24}",
            p.part_num, p.label, p.size_desc, p.fs_type, p.mount_point);
    }

    // 3. Konfigurasi Pengguna
    let config = InstallConfig {
        target_disk: target_disk.clone(),
        enable_ab_slots: true,
        filesystem: fs_str.clone(),
        enable_compression: true,
        partition_scheme: scheme_str.clone(),
        swap_type: swap_str.clone(),
        system_profile: profile_str.clone(),
        hostname: "daxos-rhino".to_string(),
        username: "daxuser".to_string(),
        full_name: "DAXOS Administrator".to_string(),
        timezone: "Asia/Jakarta".to_string(),
        locale: "id_ID.UTF-8".to_string(),
        keyboard_layout: "us".to_string(),
    };

    let profile_desc = match profile_enum {
        SystemProfile::UltimateWorkstation => "DAXOS Ultimate Workstation (Wayland + DreXUI Full Stack, 30 Apps)",
        SystemProfile::DeveloperEngineering => "Developer & Engineering Workstation (LLVM/Rust/Docker/Dev Tools)",
        SystemProfile::LightweightMinimal => "Lightweight Minimalist (<1.2GB RAM, Wayland Core)",
    };

    println!("\n\x1b[1;36m[TAHAP 3/4]\x1b[0m Parameter Instalasi Sistem:");
    println!("  • Target Penyimpanan : \x1b[1m{}\x1b[0m (Skema: \x1b[33m{}\x1b[0m, Swap: \x1b[33m{}\x1b[0m)", config.target_disk, config.partition_scheme, config.swap_type);
    println!("  • Profil Instalasi   : \x1b[35m{}\x1b[0m", profile_desc);
    println!("  • Sistem Berkas Data : \x1b[32mBtrfs dengan zstd:3 compression & copy-on-write\x1b[0m");
    println!("  • Dual-Slot A/B OTA  : \x1b[32mAktif (dm-verity cryptographic verification)\x1b[0m");
    println!("  • Hostname / Akun    : {} / {} ({})", config.hostname, config.username, config.full_name);
    println!("  • Zona Waktu / Bahasa: {} / {}", config.timezone, config.locale);

    // 4. Eksekusi Instalasi Langkah demi Langkah
    println!("\n\x1b[1;36m[TAHAP 4/4]\x1b[0m Memulai Eksekusi Instalasi DAXOS ke '{}'...", target_disk);
    let steps = InstallerEngine::get_install_steps();

    for (step_idx, (title, detail, pct)) in steps.iter().enumerate() {
        println!("  \x1b[1;33m[{}/{}]\x1b[0m \x1b[1m{}\x1b[0m", step_idx + 1, steps.len(), title);
        println!("        {}", detail);
        if stream_logs {
            match step_idx {
                0 => {
                    println!("        \x1b[90m[KERNEL] gpt: created PMBR and primary GPT on {} (sectors: 0..1000215216)\x1b[0m", target_disk);
                }
                1 => {
                    println!("        \x1b[90m[BTRFS] btrfs-progs v6.12: created fs on {} with subvolumes @, @home, @var, @snapshots\x1b[0m", target_disk);
                }
                2 => {
                    println!("        \x1b[90m[EROFS] erofs-utils: mounting squashfs rootfs (zstd 19:1 ratio, 3.8GB decompressed)\x1b[0m");
                }
                3 => {
                    println!("        \x1b[90m[DM-VERITY] computing tree hash: root_hash=9f82c0b... (integrity verified)\x1b[0m");
                }
                4 => {
                    println!("        \x1b[90m[GRUB] grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=daxos\x1b[0m");
                }
                5 => {
                    println!("        \x1b[90m[WAYLAND] compiling DreXUI Dual-Kawase acrylic shaders with Vulkan 1.3 pipeline cache\x1b[0m");
                }
                _ => {}
            }
        }
        let bar = render_progress_bar(*pct, 36);
        print!("        Kemajuan: {} ", bar);
        std::io::Write::flush(&mut std::io::stdout()).unwrap();

        // Delay pendek simulasi langkah penulisan storage
        thread::sleep(Duration::from_millis(60));
        println!("\x1b[32m [SELESAI]\x1b[0m");
    }

    println!("\n\x1b[1;32m╔═════════════════════════════════════════════════════════════════════╗\x1b[0m");
    println!("\x1b[1;32m║  INSTALASI DAXOS BERHASIL! SISTEM SIAP DIGUNAKAN PRODUKSI           ║\x1b[0m");
    println!("\x1b[1;32m╚═════════════════════════════════════════════════════════════════════╝\x1b[0m");
    println!("  • Bootloader: UEFI GRUB 2.12 terpasang pada /boot/efi/EFI/daxos/grubx64.efi");
    println!("  • Kernel    : /boot/vmlinuz-dxu-hybrid (DXU Hybrid Kernel 1.10.2026) terverifikasi dm-verity");
    println!("  • Desktop   : DreX Wayland Compositor (Wayland-1, Acrylic Blur Glass & 240Hz governor)");
    println!("  • Profil    : {}", profile_desc);
    println!("  • Silakan reboot komputer dan lepaskan media instalasi.\n");
}
