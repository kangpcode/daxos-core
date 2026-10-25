//! ============================================================================
//! DAXOS SHELL EXECUTABLE (daxsh)
//! Binary: daxsh
//! ============================================================================

use std::env;
use std::io::{self, BufRead, Write};
use std::process;
use daxsh::DaxShell;

const WELCOME_BANNER: &str = "\x1b[1;36m
  ╔═══════════════════════════════════════════════════════════════╗
  ║    DAXOS SHELL (daxsh v1.2) — Powered by Acrylic Flow Engine  ║
  ║    Ketik \x1b[1;33m'fetch'\x1b[1;36m untuk info sistem, \x1b[1;33m'help'\x1b[1;36m untuk bantuan, \x1b[1;33m'exit'\x1b[1;36m untuk keluar║
  ╚═══════════════════════════════════════════════════════════════╝\x1b[0m";

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut shell = DaxShell::new();

    // Mode eksekusi satu baris (-c "perintah")
    if args.len() >= 3 && args[1] == "-c" {
        let cmd_str = args[2..].join(" ");
        match shell.execute(&cmd_str) {
            Ok(Some(out)) => println!("{}", out),
            Ok(None) => {}
            Err(e) => {
                eprintln!("\x1b[1;31m[ERROR]\x1b[0m {}", e);
                process::exit(1);
            }
        }
        return;
    }

    // Mode interaktif REPL
    println!("{}", WELCOME_BANNER);

    let stdin = io::stdin();
    let mut stdout = io::stdout();

    while shell.running {
        print!("{}", shell.prompt());
        let _ = stdout.flush();

        let mut line = String::new();
        match stdin.lock().read_line(&mut line) {
            Ok(0) => {
                // EOF (Ctrl+D)
                println!("\nSampai jumpa dari DAXOS!");
                break;
            }
            Ok(_) => {
                let trimmed = line.trim();
                if trimmed.is_empty() {
                    continue;
                }
                match shell.execute(trimmed) {
                    Ok(Some(out)) => println!("{}", out),
                    Ok(None) => {}
                    Err(e) => eprintln!("\x1b[1;31m{}\x1b[0m", e),
                }
            }
            Err(e) => {
                eprintln!("Error membaca input: {}", e);
                break;
            }
        }
    }
}
