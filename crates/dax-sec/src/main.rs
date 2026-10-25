//! ============================================================================
//! DAXOS SECURITY & DEFENDER CLI (dxdef-cli)
//! Binary: dxdef-cli
//! ============================================================================

use std::env;
use std::path::Path;
use std::process;
use dax_sec::{SecurityAuditor, FirewallManager};

const BANNER: &str = "\x1b[1;36m
  ╔═════════════════════════════════════════════════════════╗
  ║    DXDEF SECURITY CENTER & FIREWALL (dxdef-cli v1.2)    ║
  ║    Hardware Root-of-Trust & Sandboxing Infrastructure   ║
  ╚═════════════════════════════════════════════════════════╝\x1b[0m";

fn print_usage() {
    println!("{}", BANNER);
    println!("\x1b[1mPENGGUNAAN:\x1b[0m");
    println!("  dxdef-cli <perintah> [argumen...]\n");
    println!("\x1b[1mPERINTAH:\x1b[0m");
    println!("  \x1b[32mstatus\x1b[0m                        Audit status keamanan sistem & kernel");
    println!("  \x1b[33mscan\x1b[0m   <berkas>               Pindai integritas biner, SUID risk, & SHA3-512");
    println!("  \x1b[36mfirewall\x1b[0m allow <port> [proto] Izinkan lalu lintas port masuk (TCP/UDP)");
    println!("  \x1b[31mfirewall\x1b[0m deny  <port> [proto] Blokir lalu lintas port (TCP/UDP)");
    println!("  \x1b[34mfirewall\x1b[0m status               Tampilkan status firewall");
    println!("  \x1b[37mhelp\x1b[0m                          Tampilkan bantuan ini\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        return;
    }

    let cmd = args[1].as_str();

    match cmd {
        "status" | "report" => {
            let r = SecurityAuditor::audit_system();
            println!("{}", BANNER);
            println!("\x1b[1mSTATUS KEAMANAN SISTEM OPERASI DAXOS:\x1b[0m");
            println!("  • Kernel Lockdown Mode   : \x1b[32m{}\x1b[0m", r.kernel_lockdown);
            println!("  • Landlock LSM Sandbox   : {}", if r.landlock_available { "\x1b[32mAktif (Enforced ABI v5)\x1b[0m" } else { "\x1b[31mNonaktif\x1b[0m" });
            println!("  • Seccomp-BPF Filtering  : {}", if r.seccomp_available { "\x1b[32mAktif (Strict Syscall Filter)\x1b[0m" } else { "\x1b[31mNonaktif\x1b[0m" });
            println!("  • dm-verity Rootfs Trust : {}", if r.dm_verity_active { "\x1b[32mTerverifikasi Kriptografis\x1b[0m" } else { "\x1b[33mDevelopment Mode (Writable)\x1b[0m" });
            println!("  • Modul TPM 2.0 Hardware : {}", if r.tpm2_present { "\x1b[32mTerdeteksi & Siap Enkripsi\x1b[0m" } else { "\x1b[33mEmulasi Software Keystore\x1b[0m" });
            println!("  • In-Kernel Root-of-Trust: {}", if r.daxos_integrity_active { "\x1b[32mTerverifikasi (daxos_sec.ko Ring-0 Enforcing)\x1b[0m" } else { "\x1b[33mStandby\x1b[0m" });
            println!("  • In-Kernel NTSync Driver: {}", if r.ntsync_driver_active { "\x1b[32mAktif (/dev/ntsync < 0.22 us)\x1b[0m" } else { "\x1b[33mStandby\x1b[0m" });
            println!("  • In-Kernel DreX-Boost   : {}", if r.drex_boost_active { "\x1b[32mAktif (/dev/daxos_boost 240Hz clamp)\x1b[0m" } else { "\x1b[33mStandby\x1b[0m" });
            println!("  • Status Firewall DXDEF  : {}", if r.firewall_active { "\x1b[32mAktif & Memfilter Port\x1b[0m" } else { "\x1b[32mStandard BBRv3 Protection\x1b[0m" });
            println!("  • Perlindungan Privasi   : \x1b[32mKamera Terkunci (Hardware Guard), Mikrofon Terpantau\x1b[0m");
            println!("\n\x1b[1;32m[DXDEF STATUS: SECURE]\x1b[0m Sistem terlindungi secara menyeluruh.");
        }

        "scan" | "audit" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas biner yang ingin diaudit.");
                process::exit(1);
            }
            let target = Path::new(&args[2]);
            println!("\x1b[1;36m==>\x1b[0m Memindai biner: '\x1b[1m{}\x1b[0m'...", target.display());
            match SecurityAuditor::audit_binary(target) {
                Ok(res) => {
                    println!("  • Format Berkas      : {}", if res.is_dapp { "DAXOS Universal .dapp" } else if res.is_elf { "ELF64 Native Linux" } else { "Berkas Data/Naskah" });
                    println!("  • Ukuran Biner       : {} bytes", res.size_bytes);
                    println!("  • SHA3-512 Hash      : \x1b[32m{}\x1b[0m", res.sha3_512);
                    println!("  • Risiko SUID Root   : {}", if res.is_suid_root { "\x1b[31mYA (BAHAYA TINGGI)\x1b[0m" } else { "\x1b[32mAman (No SUID)\x1b[0m" });

                    if !res.dangerous_syscall_indicators.is_empty() {
                        println!("  • Indikator Panggilan:");
                        for ind in &res.dangerous_syscall_indicators {
                            println!("    - \x1b[33m{}\x1b[0m", ind);
                        }
                    } else {
                        println!("  • Panggilan Sistem   : \x1b[32mBersih dari exploit hooks\x1b[0m");
                    }

                    if res.passed {
                        println!("\n\x1b[1;32m[VERIFIKASI BERHASIL]\x1b[0m Berkas memenuhi standar keamanan DAXOS.");
                    } else {
                        println!("\n\x1b[1;31m[PERINGATAN KEAMANAN]\x1b[0m Berkas memiliki anomali hak akses.");
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "firewall" => {
            let sub = if args.len() > 2 { args[2].as_str() } else { "status" };
            match sub {
                "status" => {
                    let r = SecurityAuditor::audit_system();
                    println!("\x1b[1;36m==>\x1b[0m Status Firewall DAXOS: {}",
                        if r.firewall_active { "\x1b[32mAktif\x1b[0m" } else { "\x1b[33mSiap Dikonfigurasi\x1b[0m" });
                }
                "allow" => {
                    if args.len() < 4 {
                        eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dxdef-cli firewall allow <port> [tcp|udp]");
                        process::exit(1);
                    }
                    let port: u16 = args[3].parse().unwrap_or(80);
                    let proto = args.get(4).map(|s| s.as_str()).unwrap_or("tcp");
                    match FirewallManager::allow_port(port, proto) {
                        Ok(msg) => println!("\x1b[1;32m[SUKSES]\x1b[0m {}", msg),
                        Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
                    }
                }
                "deny" => {
                    if args.len() < 4 {
                        eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dxdef-cli firewall deny <port> [tcp|udp]");
                        process::exit(1);
                    }
                    let port: u16 = args[3].parse().unwrap_or(80);
                    let proto = args.get(4).map(|s| s.as_str()).unwrap_or("tcp");
                    match FirewallManager::deny_port(port, proto) {
                        Ok(msg) => println!("\x1b[1;32m[SUKSES]\x1b[0m {}", msg),
                        Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
                    }
                }
                _ => eprintln!("Subperintah firewall tidak dikenal. Pilihan: status, allow, deny"),
            }
        }

        "help" | "-h" | "--help" => {
            print_usage();
        }

        unknown => {
            eprintln!("\x1b[1;31m[ERROR]\x1b[0m Perintah tidak dikenal: '{}'. Gunakan 'dxdef-cli help'.", unknown);
            process::exit(1);
        }
    }
}
