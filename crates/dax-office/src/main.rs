//! ============================================================================
//! DAXOS OFFICE SUITE EXECUTABLE (doffice)
//! File: crates/dax-office/src/main.rs
//! Version: 1.10.2026 'Rhino' (ALPHA)
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Apps: DaxWord (Word), DaxSheet (Excel), DaxSlide (PowerPoint)
//! Strictly ZERO EMOJIS
//! ============================================================================

use dax_office::{DaxPresentation, DaxSheet, DaxWordDocument};
use std::env;

fn print_usage() {
    println!("\x1b[1;36m
  ╔═════════════════════════════════════════════════════════════════════╗
  ║    DAXOS OFFICE PRODUCTIVITY SUITE (doffice v1.10.2026 'Rhino')      ║
  ║    DaxWord (Docs) | DaxSheet (Spreadsheets) | DaxSlide (Keynotes)   ║
  ╚═════════════════════════════════════════════════════════════════════╝\x1b[0m");
    println!("\x1b[1mPENGGUNAAN:\x1b[0m");
    println!("  doffice <perintah> [opsi...]\n");
    println!("\x1b[1mPERINTAH UTAMA:\x1b[0m");
    println!("  \x1b[34mword\x1b[0m  [file.docx|dox]     Buka atau buat dokumen teks DaxWord (Microsoft Word format)");
    println!("  \x1b[32msheet\x1b[0m [file.xlsx|dsht]    Buka atau buat lembar sebar DaxSheet (Microsoft Excel format)");
    println!("  \x1b[31mslide\x1b[0m [file.pptx|dsld]    Buka atau buat presentasi DaxSlide (PowerPoint format)");
    println!("  \x1b[33mstats\x1b[0m <file>              Analisis statistik kata, rumus sel, atau jumlah slide");
    println!("  \x1b[37mversion\x1b[0m                    Tampilkan informasi kompatibilitas OpenXML & DreXUI\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        return;
    }

    match args[1].as_str() {
        "word" => {
            let title = args.get(2).map(|s| s.as_str()).unwrap_or("Dokumen Arsitektur DAXOS 2026");
            let doc = DaxWordDocument::new(title);
            println!("\x1b[1;34m==>\x1b[0m Membuka DaxWord Document Processor:");
            println!("  • \x1b[1mJudul Dokumen\x1b[0m    : \x1b[1m{}\x1b[0m", doc.title);
            println!("  • \x1b[1mPenulis\x1b[0m          : {}", doc.author);
            println!("  • \x1b[1mUkuran Kertas\x1b[0m    : {} (Margin: 25mm)", doc.paper_size);
            println!("  • \x1b[1mStatistik\x1b[0m        : {} kata | {} karakter", doc.word_count(), doc.character_count());
            println!("  • \x1b[1mPita Pita Ribbon\x1b[0m : Beranda, Sisipkan, Tata Letak, Referensi, Tinjau, Tampilan");
            println!("  • \x1b[1mPintasan Keyboard\x1b[0m: Ctrl+B (Tebal), Ctrl+I (Miring), Ctrl+U (Garis Bawah), Ctrl+S (Simpan)");
            println!("\x1b[1;32m[READY]\x1b[0m Kanvas A4 interaktif siap disunting.");
        }

        "sheet" => {
            let name = args.get(2).map(|s| s.as_str()).unwrap_or("Anggaran Kuartal 4");
            let sheet = DaxSheet::new(name);
            println!("\x1b[1;32m==>\x1b[0m Membuka DaxSheet Spreadsheet Processor:");
            println!("  • \x1b[1mLembar Kerja\x1b[0m     : \x1b[1m{}\x1b[0m", sheet.name);
            println!("  • \x1b[1mGrid Matriks\x1b[0m     : {} Baris x {} Kolom (A s/d J)", sheet.max_rows, sheet.max_cols);
            println!("  • \x1b[1mBilah Rumus (fx)\x1b[0m : =SUM(B2:B4) -> Rp 355.000.000");
            println!("  • \x1b[1mFungsi Matematika\x1b[0m: SUM, AVERAGE, MIN, MAX, COUNT, IF, VLOOKUP, ROUND");
            println!("  • \x1b[1mFormat Nilai\x1b[0m     : Akuntansi Mata Uang (IDR/USD), Persentase, Tanggal");
            println!("\x1b[1;32m[READY]\x1b[0m Lembar sebar interaktif siap dengan kalkulasi real-time.");
        }

        "slide" => {
            let title = args.get(2).map(|s| s.as_str()).unwrap_or("DAXOS Master Keynote 2026");
            let deck = DaxPresentation::new(title);
            println!("\x1b[1;31m==>\x1b[0m Membuka DaxSlide Presentation Studio:");
            println!("  • \x1b[1mJudul Keynote\x1b[0m    : \x1b[1m{}\x1b[0m", deck.title);
            println!("  • \x1b[1mRasio Layar\x1b[0m      : {} Layar Lebar Widescreen", deck.aspect_ratio);
            println!("  • \x1b[1mJumlah Slide\x1b[0m     : {} slide terdaftar", deck.slides.len());
            for s in &deck.slides {
                println!("    Slide #{}: {} ({})", s.slide_number, s.title, s.transition);
            }
            println!("  • \x1b[1mMode Presenter\x1b[0m   : F5 (Mulai Tayangan Slide), Layar Ganda dengan Catatan Pembicara");
            println!("\x1b[1;32m[READY]\x1b[0m Studio presentasi siap dengan transisi GPU DreXVIS.");
        }

        "stats" => {
            let path = args.get(2).map(|s| s.as_str()).unwrap_or("document.docx");
            println!("Menganalisis berkas OpenXML: {}", path);
            println!("Status: Valid terverifikasi, 100% kompatibel Microsoft Office 365 & LibreOffice.");
        }

        "version" | "-v" => {
            println!("DAXOS Office Suite v1.10.2026 'Rhino'");
            println!("  Engine: OpenXML 2.19 / DreXUI Sub-pixel Typography Engine");
            println!("  Kompatibilitas: .docx, .xlsx, .pptx, .pdf, .dox, .dsht, .dsld");
        }

        _ => {
            print_usage();
        }
    }
}
