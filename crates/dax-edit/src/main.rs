//! ============================================================================
//! DAXOS NOTEPAD++ & SCRATCHPAD VISUAL EDITOR (dedit)
//! File: crates/dax-edit/src/main.rs
//! Version: 1.10.2026 'Rhino' (ALPHA)
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS
//! ============================================================================

use std::env;
use std::fs;
use std::path::Path;
use std::process;
use dax_edit::TextBuffer;

const BANNER: &str = "\x1b[1;36m
  ╔═════════════════════════════════════════════════════════╗
  ║    DAXOS dEdit (NOTEPAD++ & SCRATCHPAD SUITE) v1.3       ║
  ║    Lightweight Text Processor, Code Scratchpad & Hex    ║
  ╚═════════════════════════════════════════════════════════╝\x1b[0m";

fn print_usage() {
    println!("{}", BANNER);
    println!("\x1b[1mPENGGUNAAN:\x1b[0m");
    println!("  dedit <berkas>                             Buka atau buat berkas dalam editor");
    println!("  dedit view <berkas>                        Lihat isi berkas dengan nomor baris");
    println!("  dedit count <berkas>                       Hitung statistik baris, kata, dan karakter");
    println!("  dedit search <berkas> <kueri>              Cari teks dalam berkas dengan baris & kolom");
    println!("  dedit replace <berkas> <cari> <ganti>      Global Search & Replace teks");
    println!("  dedit sort <berkas>                        Urutkan baris berkas secara alfabetis");
    println!("  dedit hex <berkas>                         Lihat dump heksadesimal & ASCII (Hex Editor)");
    println!("  dedit json <berkas>                        Validasi sintaksis & format rapi JSON");
    println!("  dedit strip <berkas>                       Bersihkan spasi akhir & normalisasi baris");
    println!("  dedit append <berkas> \"<teks>\"             Tambahkan baris teks ke akhir berkas");
    println!("  dedit help                                 Tampilkan bantuan ini\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        return;
    }

    let first = args[1].as_str();

    match first {
        "help" | "-h" | "--help" => {
            print_usage();
        }

        "view" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas yang ingin dilihat.");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            match TextBuffer::from_file(path) {
                Ok(buf) => print!("{}", buf.render_preview(100)),
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "count" | "stats" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas yang ingin dihitung.");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            match TextBuffer::from_file(path) {
                Ok(buf) => {
                    let s = buf.stats();
                    println!("\x1b[1;36m==>\x1b[0m Statistik Berkas: '\x1b[1m{}\x1b[0m'", path.display());
                    println!("  • \x1b[1mJumlah Baris\x1b[0m    : \x1b[32m{}\x1b[0m", s.line_count);
                    println!("  • \x1b[1mJumlah Kata\x1b[0m     : \x1b[33m{}\x1b[0m", s.word_count);
                    println!("  • \x1b[1mJumlah Karakter\x1b[0m : \x1b[36m{}\x1b[0m", s.char_count);
                    println!("  • \x1b[1mUkuran Bytes\x1b[0m    : \x1b[37m{} B\x1b[0m", s.byte_count);
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "search" | "find" => {
            if args.len() < 4 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dedit search <berkas> <kueri>");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            let q = &args[3];
            match TextBuffer::from_file(path) {
                Ok(buf) => {
                    let matches = buf.search(q);
                    println!("\x1b[1;36m==>\x1b[0m Ditemukan {} kecocokan untuk '\x1b[1m{}\x1b[0m' dalam '{}':",
                        matches.len(), q, path.display());
                    for (line, col) in matches {
                        println!("  • Baris {:>4}, Kolom {:>3} : {}", line, col, buf.lines[line - 1]);
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "replace" => {
            if args.len() < 5 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dedit replace <berkas> <cari> <ganti>");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            let target = &args[3];
            let replacement = &args[4];
            match fs::read_to_string(path) {
                Ok(content) => {
                    let count = content.matches(target).count();
                    let updated = content.replace(target, replacement);
                    if let Ok(()) = fs::write(path, updated) {
                        println!("\x1b[1;32m[SUKSES]\x1b[0m Mengganti {} kemunculan '{}' menjadi '{}' dalam '{}'.",
                            count, target, replacement, path.display());
                    } else {
                        eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gagal menulis perubahan ke {}", path.display());
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "sort" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas yang ingin diurutkan.");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            match fs::read_to_string(path) {
                Ok(content) => {
                    let mut lines: Vec<&str> = content.lines().collect();
                    lines.sort();
                    let sorted_text = lines.join("\n") + "\n";
                    if let Ok(()) = fs::write(path, sorted_text) {
                        println!("\x1b[1;32m[SUKSES]\x1b[0m Berkas '{}' berhasil diurutkan secara alfabetis ({} baris).",
                            path.display(), lines.len());
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "hex" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas yang ingin diinspeksi dalam format hex.");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            match fs::read(path) {
                Ok(bytes) => {
                    println!("\x1b[1;36m==>\x1b[0m Hex Viewer Notepad++: '{}' (Total {} bytes):", path.display(), bytes.len());
                    println!("{:<10} {:<48} {:<16}", "OFFSET", "HEX DUMP (16 BYTES)", "ASCII");
                    println!("{}", "─".repeat(76));

                    let limit = bytes.len().min(128); // preview first 128 bytes
                    for chunk_idx in (0..limit).step_by(16) {
                        let end = (chunk_idx + 16).min(limit);
                        let slice = &bytes[chunk_idx..end];
                        let mut hex_str = String::new();
                        let mut ascii_str = String::new();

                        for b in slice {
                            hex_str.push_str(&format!("{:02x} ", b));
                            if b.is_ascii_graphic() || *b == b' ' {
                                ascii_str.push(*b as char);
                            } else {
                                ascii_str.push('.');
                            }
                        }

                        println!("{:08x}   {:<48} |{}|", chunk_idx, hex_str, ascii_str);
                    }
                    if bytes.len() > 128 {
                        println!("... [{} bytes lainnya tidak ditampilkan]", bytes.len() - 128);
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "json" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas JSON.");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            match fs::read_to_string(path) {
                Ok(content) => {
                    match serde_json::from_str::<serde_json::Value>(&content) {
                        Ok(v) => {
                            let formatted = serde_json::to_string_pretty(&v).unwrap_or(content);
                            let _ = fs::write(path, &formatted);
                            println!("\x1b[1;32m[SUKSES]\x1b[0m Sintaksis JSON valid & diformat rapi (Notepad++ JSTool mode).");
                        }
                        Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m JSON tidak valid: {}", e),
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "strip" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas yang ingin dibersihkan.");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            match fs::read_to_string(path) {
                Ok(content) => {
                    let stripped: Vec<&str> = content.lines().map(|l| l.trim_end()).collect();
                    let res = stripped.join("\n") + "\n";
                    if let Ok(()) = fs::write(path, res) {
                        println!("\x1b[1;32m[SUKSES]\x1b[0m Spasi akhir dibersihkan & normalisasi line ending berhasil pada '{}'.", path.display());
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "append" => {
            if args.len() < 4 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dedit append <berkas> \"<teks>\"");
                process::exit(1);
            }
            let path = Path::new(&args[2]);
            let text = &args[3];
            let mut buf = TextBuffer::from_file(path).unwrap_or_else(|_| TextBuffer::new());
            let len = buf.lines.len();
            buf.insert_line(len, text.to_string());
            match buf.save_as(path) {
                Ok(()) => println!("\x1b[1;32m[SUKSES]\x1b[0m Berhasil menambahkan baris ke '{}'.", path.display()),
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        file_path => {
            let path = Path::new(file_path);
            let buf = TextBuffer::from_file(path).unwrap_or_else(|_| {
                println!("\x1b[1;33m[INFO]\x1b[0m Berkas baru: '{}'. Membuat berkas kosong...", path.display());
                TextBuffer::new()
            });

            println!("{}", BANNER);
            println!("\x1b[1;36m==>\x1b[0m Membuka '{}' dalam mode dEdit Visual Scratchpad:", path.display());
            print!("{}", buf.render_preview(25));
            println!("\x1b[1;32m[OK]\x1b[0m Berkas dimuat ke RAM. Gunakan perintah 'dedit view', 'dedit search', atau 'dedit replace'.");
        }
    }
}
