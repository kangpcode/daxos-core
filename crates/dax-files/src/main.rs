//! ============================================================================
//! DAXOS FILE MANAGER CLI (dfm)
//! Binary: dfm
//! ============================================================================

use std::env;
use std::fs;
use std::path::Path;
use std::process;
use dax_files::{FileManager, format_size};

const BANNER: &str = "\x1b[1;36m
  ╔═════════════════════════════════════════════════════════╗
  ║    DAXOS FILE MANAGER & EXPLORER (dfm v1.2)             ║
  ║    High-Speed Unified Virtual File System Navigator     ║
  ╚═════════════════════════════════════════════════════════╝\x1b[0m";

fn print_usage() {
    println!("{}", BANNER);
    println!("\x1b[1mPENGGUNAAN:\x1b[0m");
    println!("  dfm <perintah> [opsi...] [argumen...]\n");
    println!("\x1b[1mPERINTAH:\x1b[0m");
    println!("  \x1b[32mls\x1b[0m    [path] [-a]         Daftar isi direktori dengan ikon, ukuran, & perizinan");
    println!("  \x1b[34mtree\x1b[0m  [path] [--depth N]  Visualisasi struktur direktori hierarkis bercabang");
    println!("  \x1b[36minfo\x1b[0m  <path>              Detail metadata, perizinan oktal, & hash SHA3-512");
    println!("  \x1b[33mfind\x1b[0m  <kueri> [path]      Pencarian berkas cepat secara rekursif");
    println!("  \x1b[35mdu\x1b[0m    [path]              Hitung total penggunaan penyimpanan direktori");
    println!("  \x1b[37mcat\x1b[0m   <file> [--lines N]  Tampilkan isi berkas teks dengan nomor baris");
    println!("  \x1b[32mcp\x1b[0m    <src> <dst>         Salin berkas atau direktori");
    println!("  \x1b[33mmv\x1b[0m    <src> <dst>         Pindahkan atau ubah nama berkas");
    println!("  \x1b[31mrm\x1b[0m    <path>              Hapus berkas atau direktori");
    println!("  \x1b[36mmkdir\x1b[0m <path>              Buat direktori baru");
    println!("  \x1b[35mtrash\x1b[0m <path>              Pindahkan ke Tempat Sampah (Recycle Bin)");
    println!("  \x1b[35mlist-trash\x1b[0m                 Daftar berkas di Tempat Sampah");
    println!("  \x1b[32mrestore\x1b[0m    <nama/id>       Pulihkan berkas dari Tempat Sampah ke asal");
    println!("  \x1b[31mempty-trash\x1b[0m               Kosongkan seluruh Tempat Sampah");
    println!("  \x1b[37mhelp\x1b[0m                      Tampilkan bantuan ini\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        // Default: list direktori saat ini
        list_directory(".");
        return;
    }

    let cmd = args[1].as_str();

    match cmd {
        "ls" | "list" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or(".");
            let show_hidden = args.iter().any(|a| a == "-a" || a == "--all");
            list_directory_custom(target, show_hidden);
        }

        "tree" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or(".");
            let depth = 3;
            println!("\x1b[1;36m==>\x1b[0m Pohon Direktori untuk '{}':", target);
            for line in FileManager::get_tree(Path::new(target), depth) {
                println!("{}", line);
            }
        }

        "info" | "stat" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan path berkas atau direktori.");
                process::exit(1);
            }
            let target = &args[2];
            match FileManager::get_info(Path::new(target)) {
                Ok(info) => {
                    println!("\x1b[1;36m==>\x1b[0m Informasi Metadata: '\x1b[1m{}\x1b[0m'", info.name);
                    println!("  • \x1b[1mPath Lengkap\x1b[0m       : {}", info.path);
                    println!("  • \x1b[1mTipe Berkas\x1b[0m        : {}", if info.is_dir { "Direktori" } else { "Berkas Reguler" });
                    println!("  • \x1b[1mUkuran\x1b[0m             : {} ({} bytes)", info.size_formatted, info.size_bytes);
                    println!("  • \x1b[1mPerizinan Oktal\x1b[0m    : 0o{}", info.permissions_octal);
                    println!("  • \x1b[1mTerakhir Diubah\x1b[0m    : {}", info.modified_str);
                    println!("  • \x1b[1mMIME Type\x1b[0m          : {}", info.mime_hint);
                    if let Some(hash) = info.sha3_512_hash {
                        println!("  • \x1b[1mSHA3-512 Checksum\x1b[0m  : \x1b[32m{}\x1b[0m", hash);
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "find" | "search" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Masukkan nama atau kueri pencarian.");
                process::exit(1);
            }
            let q = &args[2];
            let target = args.get(3).map(|s| s.as_str()).unwrap_or(".");
            println!("\x1b[1;36m==>\x1b[0m Mencari '\x1b[1m{}\x1b[0m' di dalam '{}':", q, target);
            let results = FileManager::find_files(Path::new(target), q);
            if results.is_empty() {
                println!("  Tidak ada berkas yang cocok ditemukan.");
            } else {
                for r in results {
                    println!("  • {}", r);
                }
            }
        }

        "du" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or(".");
            println!("\x1b[1;36m==>\x1b[0m Menganalisis pemakaian disk '{}'...", target);
            let (bytes, count) = FileManager::calc_disk_usage(Path::new(target));
            println!("  Total Ukuran : \x1b[1;32m{}\x1b[0m ({} bytes)", format_size(bytes), bytes);
            println!("  Total Item   : \x1b[1m{}\x1b[0m berkas/subdirektori", count);
        }

        "cat" | "view" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas yang ingin ditampilkan.");
                process::exit(1);
            }
            let target = &args[2];
            match fs::read_to_string(target) {
                Ok(content) => {
                    println!("\x1b[1;36m==>\x1b[0m Menampilkan isi berkas: \x1b[1m{}\x1b[0m", target);
                    for (i, line) in content.lines().take(50).enumerate() {
                        println!("\x1b[2m{:4} │\x1b[0m {}", i + 1, line);
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gagal membaca '{}': {}", target, e),
            }
        }

        "mkdir" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan nama direktori baru.");
                process::exit(1);
            }
            let dir = &args[2];
            match fs::create_dir_all(dir) {
                Ok(_) => println!("\x1b[1;32m[SUKSES]\x1b[0m Direktori '{}' berhasil dibuat.", dir),
                Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
            }
        }

        "rm" | "del" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas atau direktori yang ingin dihapus.");
                process::exit(1);
            }
            let target = Path::new(&args[2]);
            let res = if target.is_dir() {
                fs::remove_dir_all(target)
            } else {
                fs::remove_file(target)
            };
            match res {
                Ok(_) => println!("\x1b[1;32m[SUKSES]\x1b[0m Berhasil menghapus '{}'.", target.display()),
                Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
            }
        }

        "cp" => {
            if args.len() < 4 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dfm cp <sumber> <tujuan>");
                process::exit(1);
            }
            match fs::copy(&args[2], &args[3]) {
                Ok(bytes) => println!("\x1b[1;32m[SUKSES]\x1b[0m Berhasil menyalin ke '{}' ({}).", args[3], format_size(bytes)),
                Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
            }
        }

        "mv" => {
            if args.len() < 4 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Gunakan: dfm mv <sumber> <tujuan>");
                process::exit(1);
            }
            match fs::rename(&args[2], &args[3]) {
                Ok(_) => println!("\x1b[1;32m[SUKSES]\x1b[0m Berhasil memindahkan '{}' ke '{}'.", args[2], args[3]),
                Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
            }
        }

        "trash" | "recycle" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan berkas atau direktori yang ingin dibuang ke Tempat Sampah.");
                process::exit(1);
            }
            let target = &args[2];
            match FileManager::move_to_trash(Path::new(target)) {
                Ok(item) => {
                    println!("\x1b[1;32m[SUKSES]\x1b[0m Berkas '{}' dipindahkan ke Tempat Sampah DAXOS.", item.original_name);
                    println!("  • ID Sampah : {}", item.id);
                    println!("  • Asal      : {}", item.original_path);
                    println!("  • Ukuran    : {}", item.size_formatted);
                    println!("  • Waktu     : {}", item.deletion_date);
                }
                Err(e) => {
                    eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e);
                    process::exit(1);
                }
            }
        }

        "list-trash" | "trash-list" => {
            match FileManager::list_trash() {
                Ok(items) => {
                    println!("\x1b[1;36m==>\x1b[0m Isi Tempat Sampah DAXOS (Total: {} item):", items.len());
                    if items.is_empty() {
                        println!("  Tempat Sampah bersih (tidak ada item).");
                    } else {
                        println!("{:<32} {:<10} {:<20} {:<30}", "ID SAMPAH", "UKURAN", "TANGGAL DIHAPUS", "LOKASI ASLI");
                        println!("{}", "─".repeat(95));
                        for it in items {
                            println!("{:<32} {:<10} {:<20} {}", it.id, it.size_formatted, it.deletion_date, it.original_path);
                        }
                    }
                }
                Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
            }
        }

        "restore" | "restore-trash" => {
            if args.len() < 3 {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m Sebutkan ID atau nama berkas yang ingin dipulihkan.");
                process::exit(1);
            }
            let target = &args[2];
            match FileManager::restore_from_trash(target) {
                Ok(path) => println!("\x1b[1;32m[SUKSES]\x1b[0m Berkas berhasil dipulihkan ke: '{}'", path),
                Err(e) => {
                    eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e);
                    process::exit(1);
                }
            }
        }

        "empty-trash" => {
            match FileManager::empty_trash() {
                Ok(count) => println!("\x1b[1;32m[SUKSES]\x1b[0m Tempat Sampah dikosongkan. Sebanyak {} item dihapus permanen.", count),
                Err(e) => eprintln!("\x1b[1;31m[GAGAL]\x1b[0m {}", e),
            }
        }

        "help" | "-h" | "--help" => {
            print_usage();
        }

        unknown => {
            eprintln!("\x1b[1;31m[ERROR]\x1b[0m Perintah tidak dikenal: '{}'. Gunakan 'dfm help'.", unknown);
            process::exit(1);
        }
    }
}

fn list_directory(target: &str) {
    list_directory_custom(target, false);
}

fn list_directory_custom(target: &str, show_hidden: bool) {
    match FileManager::list_dir(Path::new(target), show_hidden) {
        Ok(entries) => {
            println!("\x1b[1;36m==>\x1b[0m Direktori: \x1b[1m{}\x1b[0m (Total: {} item)", target, entries.len());
            println!("{:<4} {:<12} {:<10} {:<20} {:<30}", "TIPE", "PERIZINAN", "UKURAN", "DIUBAH", "NAMA");
            println!("{}", "─".repeat(84));
            for e in entries {
                let size_str = if e.is_dir { "-".to_string() } else { format_size(e.size_bytes) };
                let name_color = if e.is_dir { "\x1b[1;34m" } else { "\x1b[0m" };
                println!("{:<4} {:<12} {:>9}  {:<20} {}{}\x1b[0m",
                    e.icon, e.permissions_str, size_str, e.modified_str, name_color, e.name);
            }
        }
        Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
    }
}
