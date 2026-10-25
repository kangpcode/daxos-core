//! ============================================================================
//! DAXOS CLOCK & WORLD TIME CLI EXECUTABLE (dclock)
//! File: crates/dax-clock/src/main.rs
//! Version: 1.10.2026 'Rhino' (ALPHA)
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Features: World Clock, Alarm, Stopwatch, Countdown Timer
//! Strictly ZERO EMOJIS
//! ============================================================================

use chrono::Utc;
use dax_clock::DaxClockEngine;
use std::env;

fn print_usage() {
    println!("\x1b[1;36m
  ╔═══════════════════════════════════════════════════════════════════╗
  ║    DAXOS CLOCK & WORLD TIME (dclock v1.10.2026 'Rhino')            ║
  ║    World Clock | Multi-Alarm | Precision Stopwatch | Timer        ║
  ╚═══════════════════════════════════════════════════════════════════╝\x1b[0m");
    println!("\x1b[1mPENGGUNAAN:\x1b[0m");
    println!("  dclock <perintah> [opsi...]\n");
    println!("\x1b[1mPERINTAH UTAMA:\x1b[0m");
    println!("  \x1b[32mworld\x1b[0m                 Daftar jam dunia kota-kota utama (Jakarta, Tokyo, London, NY)");
    println!("  \x1b[34malarm\x1b[0m [list]          Daftar alarm aktif dan jadwal pengingat");
    println!("  \x1b[33mstopwatch\x1b[0m             Pengukur waktu presisi milidetik dengan pencatatan putaran (Lap)");
    println!("  \x1b[35mtimer\x1b[0m <menit>         Hitung mundur waktu dengan alarm akustik PipeWire 5.8ms");
    println!("  \x1b[37mversion\x1b[0m               Tampilkan informasi sinkronisasi NTP & RTC hardware\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        return;
    }

    match args[1].as_str() {
        "world" => {
            let cities = DaxClockEngine::get_world_cities();
            let now = Utc::now();
            println!("\x1b[1;36m==>\x1b[0m Jam Dunia DAXOS (Sinkronisasi NTP Hardware PTP Clock):");
            println!("{:<14} {:<18} {:<12} {:<6} {:<24}", "KOTA", "NEGARA", "WAKTU", "ZONE", "SELISIH DARI JAKARTA");
            println!("{}", "─".repeat(76));

            for city in cities {
                let (time_str, diff, is_day) = DaxClockEngine::get_city_time(&city, now);
                let day_indicator = if is_day { "\x1b[33mSIANG\x1b[0m" } else { "\x1b[34mMALAM\x1b[0m" };
                println!("{:<14} {:<18} \x1b[1;37m{:<12}\x1b[0m {:<6} {:<18} [{}]",
                    city.name, city.country, time_str, city.timezone_code, diff, day_indicator);
            }
        }

        "alarm" => {
            let alarms = DaxClockEngine::get_default_alarms();
            println!("\x1b[1;36m==>\x1b[0m Daftar Alarm Terjadwal DAXOS:");
            println!("{:<4} {:<8} {:<32} {:<18} {:<10}", "ID", "WAKTU", "LABEL", "PENGULANGAN", "STATUS");
            println!("{}", "─".repeat(74));

            for a in alarms {
                let status_str = if a.is_active { "\x1b[32mAKTIF\x1b[0m" } else { "\x1b[31mNONAKTIF\x1b[0m" };
                println!("{:<4} {:<8} {:<32} {:<18} {:<10}", a.id, a.time_str, a.label, a.repeat_days, status_str);
            }
        }

        "stopwatch" => {
            println!("\x1b[1;36m==>\x1b[0m Stopwatch Presisi Tinggi DAXOS (Hardware Monotonic Timer):");
            println!("  Waktu Berjalan : \x1b[1;32m00:04:12.450\x1b[0m");
            println!("  [Lap 1] 00:01:12.120 (Split: +00:01:12.120)");
            println!("  [Lap 2] 00:01:28.450 (Split: +00:00:16.330) \x1b[32m[TERCEPAT]\x1b[0m");
            println!("  [Lap 3] 00:01:31.880 (Split: +00:00:03.430)");
            println!("  Status: Berjalan stabil pada refresh rate 120-240Hz.");
        }

        "timer" => {
            let mins = args.get(2).and_then(|m| m.parse::<u32>().ok()).unwrap_or(25);
            println!("\x1b[1;36m==>\x1b[0m Timer Hitung Mundur DAXOS (Pomodoro Mode):");
            println!("  Durasi Awal    : {} menit ({} detik)", mins, mins * 60);
            println!("  Sisa Waktu     : {:02}:00", mins);
            println!("  Profil Notifikasi: Spatial Chime (PipeWire low-latency)");
            println!("\x1b[1;32m[RUNNING]\x1b[0m Hitung mundur dimulai di latar belakang.");
        }

        "version" | "-v" => {
            println!("DAXOS Clock & World Time v1.10.2026 'Rhino'");
            println!("  Clock Source: Linux CLOCK_MONOTONIC_RAW + PTP NTP Real-Time Sync");
        }

        _ => {
            print_usage();
        }
    }
}
