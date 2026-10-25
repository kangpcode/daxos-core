//! ============================================================================
//! DAXOS PRODUCTION AUDIO CONTROLLER CLI (daudio)
//! File: crates/dax-audiod/src/main.rs
//! Purpose: Production CLI tool for audio hardware, spatial audio, and DSP mixer
//! ============================================================================

use dax_audiod::AudioSubsystem;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let subcmd = args.get(1).map(|s| s.as_str()).unwrap_or("status");

    match subcmd {
        "status" => {
            let status = AudioSubsystem::get_status();
            println!("================================================================================");
            println!("  DAXOS HIGH-FIDELITY AUDIO & SPATIAL DSP SUBSYSTEM (daudio)");
            println!("  ALSA / PipeWire Pro-Audio Real-Time Pipeline (SCHED_RR Priority 88)");
            println!("================================================================================");
            let mute_str = if status.is_muted { "\x1b[31m[MUTED]\x1b[0m" } else { "\x1b[32m[ACTIVE]\x1b[0m" };
            println!("Master Volume      : {}% {}", status.volume_percent, mute_str);
            println!("Default Output     : {}", status.default_card.as_deref().unwrap_or("Unknown"));

            println!("\n\x1b[1;36m[SPATIAL AUDIO 3D HRTF]\x1b[0m");
            println!("  • Status         : {}", if status.spatial_config.enabled { "\x1b[32mAKTIF (3D Binaural Virtualization)\x1b[0m" } else { "\x1b[33mNONAKTIF\x1b[0m" });
            println!("  • HRTF Profil    : {}", status.spatial_config.hrtf_profile);
            println!("  • Crossfeed DSP  : {:.0}% Headphone acoustic blending", status.spatial_config.crossfeed_amount * 100.0);
            println!("  • Virtual Setup  : {} Channels (7.1 Surround Virtual Soundstage)", status.spatial_config.virtual_speakers);

            println!("\n\x1b[1;35m[10-BAND PARAMETRIC EQUALIZER]\x1b[0m");
            println!("  • Preset Aktif   : \x1b[1m{}\x1b[0m", status.eq_config.preset_name);
            print!("  • Gain Curve     : ");
            let freqs = ["31", "62", "125", "250", "500", "1k", "2k", "4k", "8k", "16k"];
            for (i, f) in freqs.iter().enumerate() {
                let g = status.eq_config.gains_db[i];
                let sign = if g >= 0.0 { "+" } else { "" };
                print!("{}:{}{:.1}dB ", f, sign, g);
            }
            println!();

            println!("\n\x1b[1;33m[HI-RES DAC ENGINE & LATENCY]\x1b[0m");
            println!("  • Bit-Perfect    : {}", if status.dac_config.bit_perfect { "\x1b[32mAKTIF (Direct Hardware Stream)\x1b[0m" } else { "Resampled" });
            println!("  • Audio Format   : {} Hz / {}-bit (Lossless Studio Master)", status.dac_config.sample_rate_hz, status.dac_config.bit_depth);
            println!("  • DSD Stream     : {}", status.dac_config.dsd_mode);
            println!("  • Buffer Latensi : {:.2} ms (Quantum: {} samples @ {} Hz)", status.latency_config.latency_ms, status.latency_config.quantum_samples, status.latency_config.sample_rate_hz);

            println!("\nDetected Sound Cards ({}):", status.cards.len());
            for c in &status.cards {
                println!("  Card #{}: [{}] {} ({})", c.index, c.id, c.name, c.long_name);
            }
            println!("\nPCM Streams ({}):", status.pcm_streams.len());
            for p in &status.pcm_streams {
                let mut caps = Vec::new();
                if p.is_playback { caps.push("Playback"); }
                if p.is_capture { caps.push("Capture"); }
                println!("  pcmC{}D{}: {} [{}]", p.card_index, p.device_index, p.name, caps.join(", "));
            }
            println!("--------------------------------------------------------------------------------");
        }
        "spatial" => {
            let opt = args.get(2).map(|s| s.as_str()).unwrap_or("status");
            match opt {
                "on" | "enable" | "1" => {
                    AudioSubsystem::set_spatial_enabled(true).expect("Failed to enable spatial audio");
                    println!("\x1b[1;32m[OK]\x1b[0m Spatial Audio 3D Binaural HRTF diaktifkan.");
                }
                "off" | "disable" | "0" => {
                    AudioSubsystem::set_spatial_enabled(false).expect("Failed to disable spatial audio");
                    println!("\x1b[1;33m[OK]\x1b[0m Spatial Audio 3D dinonaktifkan (Mode Stereo Standar).");
                }
                "profile" => {
                    let profile_name = args.get(3).map(|s| s.as_str()).unwrap_or("Binaural Studio HRTF");
                    AudioSubsystem::set_spatial_profile(profile_name).expect("Failed to set spatial profile");
                    println!("\x1b[1;32m[OK]\x1b[0m Profil Spatial Audio diatur ke: '{}'", profile_name);
                }
                _ => {
                    let cfg = AudioSubsystem::get_spatial_config();
                    println!("Spatial Audio 3D Status: {}", if cfg.enabled { "AKTIF" } else { "NONAKTIF" });
                    println!("Profil HRTF           : {}", cfg.hrtf_profile);
                    println!("Crossfeed             : {:.0}%", cfg.crossfeed_amount * 100.0);
                }
            }
        }
        "eq" => {
            let preset = args.get(2).map(|s| s.as_str()).unwrap_or("status");
            match preset {
                "status" => {
                    let eq = AudioSubsystem::get_eq_config();
                    println!("10-Band Equalizer Preset: {}", eq.preset_name);
                    for (i, g) in eq.gains_db.iter().enumerate() {
                        let sign = if *g >= 0.0 { "+" } else { "" };
                        println!("  Band {}: {}{:.1} dB", i + 1, sign, g);
                    }
                }
                "list" => {
                    println!("Tersedia Preset Equalizer Studio:");
                    println!("  • acoustic  : Acoustic Clarity (Default High-Definition)");
                    println!("  • bass      : Bass Boost Extreme (+7dB sub-bass)");
                    println!("  • spatial   : Spatial 3D Immersion (Wide Soundstage)");
                    println!("  • flat      : Studio Monitor Flat (0.0 dB reference)");
                    println!("  • vocal     : Vocal Air & Presence (Enhanced mids/treble)");
                    println!("  • atmos     : Cinema Dolby Atmos 7.1 Emulation");
                }
                other => {
                    AudioSubsystem::set_eq_preset(other).expect("Failed to set EQ preset");
                    println!("\x1b[1;32m[OK]\x1b[0m Equalizer preset diubah ke: '{}'", other);
                }
            }
        }
        "dac" => {
            let opt = args.get(2).map(|s| s.as_str()).unwrap_or("status");
            match opt {
                "bit-perfect" | "bp" => {
                    AudioSubsystem::set_dac_bit_perfect(true).expect("Failed to set DAC bit-perfect");
                    println!("\x1b[1;32m[OK]\x1b[0m DAC Stream: Bit-Perfect Direct Hardware Mode AKTIF.");
                }
                "oversample" => {
                    AudioSubsystem::set_dac_bit_perfect(false).expect("Failed to set DAC oversample");
                    println!("\x1b[1;33m[OK]\x1b[0m DAC Stream: DSP Oversampling Mode AKTIF.");
                }
                _ => {
                    let dac = AudioSubsystem::get_dac_config();
                    println!("DAC Hi-Res Status:");
                    println!("  Mode Bit-Perfect : {}", dac.bit_perfect);
                    println!("  Sample Rate      : {} Hz / {}-bit", dac.sample_rate_hz, dac.bit_depth);
                    println!("  DSD Stream       : {}", dac.dsd_mode);
                    println!("  Master Jitter    : {:.2} ps RMS", dac.master_clock_jitter_ps);
                }
            }
        }
        "latency" => {
            if let Some(quantum_str) = args.get(2) {
                if let Ok(quantum) = quantum_str.parse::<u32>() {
                    AudioSubsystem::set_quantum_samples(quantum).expect("Failed to set quantum");
                    let cfg = AudioSubsystem::get_latency_config();
                    println!("\x1b[1;32m[OK]\x1b[0m PipeWire Quantum diatur ke: {} samples (Buffer Latensi: {:.2} ms)", cfg.quantum_samples, cfg.latency_ms);
                } else {
                    eprintln!("[ERROR] Quantum must be 64, 128, 256, 512, or 1024");
                }
            } else {
                let cfg = AudioSubsystem::get_latency_config();
                println!("PipeWire Latency Configuration:");
                println!("  Quantum Buffer   : {} samples", cfg.quantum_samples);
                println!("  Latensi Hardware : {:.2} ms", cfg.latency_ms);
                println!("  Prioritas Realtime: SCHED_RR priority {}", cfg.realtime_priority);
                println!("  Lock Memory      : {}", cfg.memory_locked);
            }
        }
        "cards" => {
            let cards = AudioSubsystem::get_sound_cards();
            println!("Hardware Sound Cards:");
            for c in cards {
                println!("  #{} [{}] {}", c.index, c.id, c.name);
            }
        }
        "pcm" => {
            let streams = AudioSubsystem::get_pcm_streams();
            println!("PCM Streams:");
            for s in streams {
                println!("  Card {} Dev {}: {}", s.card_index, s.device_index, s.name);
            }
        }
        "set-vol" => {
            if let Some(vol_str) = args.get(2) {
                if let Ok(vol) = vol_str.parse::<u32>() {
                    AudioSubsystem::set_volume(vol).expect("Failed to set volume");
                    println!("[OK] Master volume set to {}%", vol.min(100));
                } else {
                    eprintln!("[ERROR] Volume must be an integer between 0 and 100");
                    std::process::exit(1);
                }
            } else {
                eprintln!("Usage: daudio set-vol <0-100>");
                std::process::exit(1);
            }
        }
        "mute" => {
            AudioSubsystem::set_mute(true).expect("Failed to mute");
            println!("[OK] Master audio MUTED");
        }
        "unmute" => {
            AudioSubsystem::set_mute(false).expect("Failed to unmute");
            println!("[OK] Master audio UNMUTED");
        }
        "json" => {
            let status = AudioSubsystem::get_status();
            let json = serde_json::to_string_pretty(&status).unwrap();
            println!("{}", json);
        }
        _ => {
            println!("DAXOS Audio Controller & Spatial DSP (daudio)");
            println!("Usage: daudio [status | spatial <on|off|profile> | eq <preset|list> | dac <bit-perfect|oversample> | latency <samples> | cards | pcm | set-vol <0-100> | mute | unmute | json]");
        }
    }
}
