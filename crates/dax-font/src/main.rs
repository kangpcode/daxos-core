//! DAXOS Font Manager CLI (`dfont`)

use dax_font::*;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let command = args.get(1).map(|s| s.as_str()).unwrap_or("list");

    match command {
        "version" | "--version" | "-v" => {
            println!("DAXOS Font Manager & Typography Engine v1.10.2026 'Rhino'");
            println!("  FreeType 2.13.2 / HarfBuzz 8.3 / DreXUI Sub-pixel LCD Pipeline");
            println!("  Path Direktori Font: /usr/share/fonts, ~/.local/share/fonts");
        }
        "list" => {
            println!("==> Daftar Font Terpasang di DAXOS (Sistem & Pengguna):");
            println!("{:<22} {:<18} {:<10} {:<14} {:<8}", "NAMA KELUARGA FONT", "KATEGORI", "BOBOT", "FORMAT", "GLYPHS");
            println!("{}", "─".repeat(76));
            for f in get_system_font_catalog() {
                println!(
                    "{:<22} {:<18} {:<10} {:<14} {:<8}",
                    f.name,
                    f.category.as_str(),
                    format!("{} varian", f.weights.len()),
                    f.format,
                    f.glyph_count
                );
            }
        }
        "info" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or("Inter Display");
            let catalog = get_system_font_catalog();
            if let Some(f) = catalog.iter().find(|font| font.name.eq_ignore_ascii_case(target)) {
                println!("==> Informasi Rinci Font: {}", f.name);
                println!("  • Kategori         : {}", f.category.as_str());
                println!("  • Perancang/Desain : {}", f.designer);
                println!("  • Lisensi          : {}", f.license);
                println!("  • Versi Berkas     : {}", f.version);
                println!("  • Format Kontainer : {}", f.format);
                println!("  • Total Glif Karakter: {} glyphs", f.glyph_count);
                println!("  • Fitur OpenType   : {}", f.opentype_features.join(", "));
                println!("  • Contoh Pangram   : \"{}\"", f.sample_pangram);
                println!("\n  Daftar Varian & Bobot:");
                for w in &f.weights {
                    println!("    - {:<10} (W{}) | PostScript: {:<22} | Path: {}", w.weight_name, w.weight_value, w.postscript_name, w.file_path);
                }
            } else {
                eprintln!("Font '{}' tidak ditemukan di pustaka DAXOS.", target);
            }
        }
        "preview" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or("Inter Display");
            let custom_text = args.get(3).map(|s| s.as_str()).unwrap_or("The quick brown fox jumps over the lazy dog 1234567890");
            println!("==> Air Terjun Ukuran Font (Waterfall Preview) - {}", target);
            let sizes = [10, 12, 14, 18, 24, 32, 48];
            for size in sizes {
                println!("[{:>2}pt] {}", size, custom_text);
            }
        }
        "glyphs" => {
            let target = args.get(2).map(|s| s.as_str()).unwrap_or("Inter Display");
            println!("==> Pemeriksa Peta Karakter Unicode (Character Map) - {}", target);
            println!("{:<6} {:<8} {:<32} {:<18}", "GLIF", "HEX", "NAMA KARAKTER", "KATEGORI");
            println!("{}", "─".repeat(68));
            for g in get_sample_unicode_glyphs() {
                println!("{:<6} {:<8} {:<32} {:<18}", g.character, g.unicode_hex, g.name, g.category);
            }
        }
        "config" => {
            let cfg = TypographyRenderConfig::default();
            println!("==> Konfigurasi Perenderan Tipografi DAXOS (FreeType & Wayland):");
            println!("  • Antialiasing     : {}", cfg.antialiasing);
            println!("  • Level Hinting    : {}", cfg.hinting_level);
            println!("  • Subpixel Order   : {}", cfg.subpixel_order);
            println!("  • LCD Filter       : {}", cfg.lcd_filter);
            println!("  • Layar Monitor DPI: {} DPI", cfg.font_dpi);
            println!("  • Koreksi Gamma    : {:.1}", cfg.gamma);
        }
        "install" => {
            let path = args.get(2).map(|s| s.as_str()).unwrap_or("/tmp/SampleFont.otf");
            match install_font(path) {
                Ok(msg) => println!("[SUKSES] {}", msg),
                Err(err) => eprintln!("[GAGAL] {}", err),
            }
        }
        _ => {
            println!("Perintah 'dfont' tidak dikenal: {}", command);
            println!("Penggunaan: dfont [list | info <nama> | preview <nama> [teks] | glyphs <nama> | config | install <berkas> | version]");
        }
    }
}
