//! ============================================================================
//! DAXOS CALCULATOR CLI & APP (dcalc)
//! Binary: dcalc
//! ============================================================================

use std::env;
use std::io::{self, BufRead, Write};
use dax_calc::{MathEvaluator, ProgrammerCalc, UnitConverter};

const BANNER: &str = "\x1b[1;36m
  ╔═════════════════════════════════════════════════════════╗
  ║    DAXOS SCIENTIFIC & PROGRAMMER CALCULATOR (dcalc)     ║
  ║    Precision Arithmetic Engine — DreX Native App        ║
  ╚═════════════════════════════════════════════════════════╝\x1b[0m";

fn print_usage() {
    println!("{}", BANNER);
    println!("\x1b[1mPENGGUNAAN:\x1b[0m");
    println!("  dcalc \"<ekspresi>\"             Evaluasi ekspresi matematika");
    println!("  dcalc base <angka>             Konversi basis bilangan (HEX, DEC, OCT, BIN)");
    println!("  dcalc conv <nilai> <dari> <ke> Konversi satuan (suhu, data, jarak)");
    println!("  dcalc                          Buka mode kalkulator interaktif REPL\n");
    println!("\x1b[1mCONTOH:\x1b[0m");
    println!("  dcalc \"sqrt(144) + 2^4 - sin(0)\"");
    println!("  dcalc base 65535");
    println!("  dcalc conv 100 c f");
    println!("  dcalc conv 16 gb mb\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() > 1 {
        match args[1].as_str() {
            "help" | "-h" | "--help" => {
                print_usage();
                return;
            }
            "base" | "prog" => {
                if args.len() < 3 {
                    eprintln!("Masukkan angka desimal untuk dikonversi.");
                    return;
                }
                if let Ok(num) = args[2].parse::<i64>() {
                    let b = ProgrammerCalc::convert(num);
                    println!("\x1b[1;36m==>\x1b[0m Konversi Basis untuk \x1b[1m{}\x1b[0m:", num);
                    println!("  • \x1b[1mDEC\x1b[0m : \x1b[32m{}\x1b[0m", b.dec);
                    println!("  • \x1b[1mHEX\x1b[0m : \x1b[33m{}\x1b[0m", b.hex);
                    println!("  • \x1b[1mOCT\x1b[0m : \x1b[35m{}\x1b[0m", b.oct);
                    println!("  • \x1b[1mBIN\x1b[0m : \x1b[36m{}\x1b[0m", b.bin);
                } else {
                    eprintln!("Bukan angka bulat yang valid: {}", args[2]);
                }
                return;
            }
            "conv" => {
                if args.len() < 5 {
                    eprintln!("Gunakan: dcalc conv <nilai> <dari> <ke>. Contoh: dcalc conv 100 c f");
                    return;
                }
                if let Ok(val) = args[2].parse::<f64>() {
                    match UnitConverter::convert(val, &args[3], &args[4]) {
                        Ok(res) => println!("\x1b[1;32m[HASIL]\x1b[0m {} {} = \x1b[1;36m{:.4}\x1b[0m {}", val, args[3].to_uppercase(), res, args[4].to_uppercase()),
                        Err(e) => eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e),
                    }
                } else {
                    eprintln!("Nilai angka tidak valid: {}", args[2]);
                }
                return;
            }
            _expr => {
                // Evaluasi ekspresi langsung
                let full_expr = args[1..].join(" ");
                match MathEvaluator::eval(&full_expr) {
                    Ok(val) => {
                        println!("\x1b[1;36m==>\x1b[0m {} = \x1b[1;32m{}\x1b[0m", full_expr, val);
                    }
                    Err(e) => {
                        eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e);
                    }
                }
                return;
            }
        }
    }

    // Mode interaktif REPL
    println!("{}", BANNER);
    println!("Ketik ekspresi matematika, 'conv', atau 'exit' untuk keluar.\n");

    let stdin = io::stdin();
    let mut stdout = io::stdout();

    loop {
        print!("\x1b[1;35mdcalc>\x1b[0m ");
        let _ = stdout.flush();

        let mut line = String::new();
        if stdin.lock().read_line(&mut line).unwrap_or(0) == 0 {
            break;
        }

        let trimmed = line.trim();
        if trimmed.is_empty() { continue; }
        if trimmed == "exit" || trimmed == "quit" { break; }

        match MathEvaluator::eval(trimmed) {
            Ok(res) => println!("  \x1b[1;32m= {}\x1b[0m", res),
            Err(e) => eprintln!("  \x1b[1;31m{}\x1b[0m", e),
        }
    }
}
