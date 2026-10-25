//! ============================================================================
//! DAXOS SCIENTIFIC & PROGRAMMER CALCULATOR ENGINE (dax-calc)
//! File: crates/dax-calc/src/lib.rs
//! Purpose: High-precision math evaluator, programmer bitwise engine, and unit converter
//! ============================================================================

use std::f64::consts::{PI, E};

/// Evaluasi ekspresi matematika standar & saintifik
pub struct MathEvaluator;

impl MathEvaluator {
    pub fn eval(expr: &str) -> Result<f64, String> {
        let clean = expr.trim()
            .replace("pi", &PI.to_string())
            .replace("PI", &PI.to_string())
            .replace(" e ", &format!(" {} ", E));

        let tokens = Self::tokenize(&clean)?;
        let mut pos = 0;
        let res = Self::parse_expression(&tokens, &mut pos)?;
        if pos < tokens.len() {
            return Err(format!("Karakter tidak terduga setelah ekspresi: {:?}", &tokens[pos..]));
        }
        Ok(res)
    }

    fn tokenize(s: &str) -> Result<Vec<String>, String> {
        let mut tokens = Vec::new();
        let mut chars = s.chars().peekable();

        while let Some(&c) = chars.peek() {
            if c.is_whitespace() {
                chars.next();
                continue;
            }

            if c.is_ascii_digit() || c == '.' {
                let mut num = String::new();
                while let Some(&d) = chars.peek() {
                    if d.is_ascii_digit() || d == '.' {
                        num.push(d);
                        chars.next();
                    } else {
                        break;
                    }
                }
                tokens.push(num);
            } else if c.is_alphabetic() {
                let mut ident = String::new();
                while let Some(&d) = chars.peek() {
                    if d.is_alphanumeric() {
                        ident.push(d);
                        chars.next();
                    } else {
                        break;
                    }
                }
                tokens.push(ident);
            } else if "+-*/%^()".contains(c) {
                tokens.push(c.to_string());
                chars.next();
            } else {
                return Err(format!("Karakter tidak valid dalam kalkulator: '{}'", c));
            }
        }
        Ok(tokens)
    }

    fn parse_expression(tokens: &[String], pos: &mut usize) -> Result<f64, String> {
        let mut val = Self::parse_term(tokens, pos)?;

        while *pos < tokens.len() {
            let op = &tokens[*pos];
            if op == "+" {
                *pos += 1;
                val += Self::parse_term(tokens, pos)?;
            } else if op == "-" {
                *pos += 1;
                val -= Self::parse_term(tokens, pos)?;
            } else {
                break;
            }
        }
        Ok(val)
    }

    fn parse_term(tokens: &[String], pos: &mut usize) -> Result<f64, String> {
        let mut val = Self::parse_factor(tokens, pos)?;

        while *pos < tokens.len() {
            let op = &tokens[*pos];
            if op == "*" {
                *pos += 1;
                val *= Self::parse_factor(tokens, pos)?;
            } else if op == "/" {
                *pos += 1;
                let divisor = Self::parse_factor(tokens, pos)?;
                if divisor == 0.0 {
                    return Err("Error: Pembagian dengan angka nol!".to_string());
                }
                val /= divisor;
            } else if op == "%" {
                *pos += 1;
                val %= Self::parse_factor(tokens, pos)?;
            } else if op == "^" {
                *pos += 1;
                val = val.powf(Self::parse_factor(tokens, pos)?);
            } else {
                break;
            }
        }
        Ok(val)
    }

    fn parse_factor(tokens: &[String], pos: &mut usize) -> Result<f64, String> {
        if *pos >= tokens.len() {
            return Err("Ekspresi tidak lengkap".to_string());
        }

        let token = &tokens[*pos];

        if token == "-" {
            *pos += 1;
            return Ok(-Self::parse_factor(tokens, pos)?);
        }

        if token == "+" {
            *pos += 1;
            return Self::parse_factor(tokens, pos);
        }

        if token == "(" {
            *pos += 1;
            let val = Self::parse_expression(tokens, pos)?;
            if *pos >= tokens.len() || tokens[*pos] != ")" {
                return Err("Kurung tutup ')' tidak ditemukan".to_string());
            }
            *pos += 1;
            return Ok(val);
        }

        // Fungsi saintifik
        match token.to_lowercase().as_str() {
            "sin" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                return Ok(arg.sin());
            }
            "cos" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                return Ok(arg.cos());
            }
            "tan" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                return Ok(arg.tan());
            }
            "sqrt" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                if arg < 0.0 {
                    return Err("Error: Akar bilangan negatif tidak terdefinisi pada real numbers".to_string());
                }
                return Ok(arg.sqrt());
            }
            "ln" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                return Ok(arg.ln());
            }
            "log" | "log10" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                return Ok(arg.log10());
            }
            "abs" => {
                *pos += 1;
                let arg = Self::parse_factor(tokens, pos)?;
                return Ok(arg.abs());
            }
            _ => {}
        }

        // Angka literal
        if let Ok(num) = token.parse::<f64>() {
            *pos += 1;
            Ok(num)
        } else {
            Err(format!("Token tidak dikenali: '{}'", token))
        }
    }
}

/// Mode kalkulator programmer (basis bilangan & bitwise)
pub struct ProgrammerCalc;

#[derive(Debug, PartialEq, Eq)]
pub struct BaseValues {
    pub dec: i64,
    pub hex: String,
    pub oct: String,
    pub bin: String,
}

impl ProgrammerCalc {
    pub fn convert(val: i64) -> BaseValues {
        BaseValues {
            dec: val,
            hex: format!("0x{:X}", val),
            oct: format!("0o{:o}", val),
            bin: format!("0b{:016b}", val),
        }
    }

    pub fn bitwise_and(a: i64, b: i64) -> i64 { a & b }
    pub fn bitwise_or(a: i64, b: i64) -> i64 { a | b }
    pub fn bitwise_xor(a: i64, b: i64) -> i64 { a ^ b }
    pub fn bitwise_not(a: i64) -> i64 { !a }
    pub fn shift_left(a: i64, n: u32) -> i64 { a << n }
    pub fn shift_right(a: i64, n: u32) -> i64 { a >> n }
}

/// Konverter satuan terpadu (suhu, panjang, data)
pub struct UnitConverter;

impl UnitConverter {
    pub fn convert(val: f64, from: &str, to: &str) -> Result<f64, String> {
        let f = from.to_lowercase();
        let t = to.to_lowercase();

        // Suhu
        if f == "c" && t == "f" { return Ok((val * 9.0 / 5.0) + 32.0); }
        if f == "f" && t == "c" { return Ok((val - 32.0) * 5.0 / 9.0); }
        if f == "c" && t == "k" { return Ok(val + 273.15); }
        if f == "k" && t == "c" { return Ok(val - 273.15); }

        // Data
        if f == "gb" && t == "mb" { return Ok(val * 1024.0); }
        if f == "mb" && t == "gb" { return Ok(val / 1024.0); }
        if f == "tb" && t == "gb" { return Ok(val * 1024.0); }
        if f == "kb" && t == "mb" { return Ok(val / 1024.0); }

        // Jarak
        if f == "km" && t == "miles" { return Ok(val * 0.621371); }
        if f == "miles" && t == "km" { return Ok(val / 0.621371); }
        if f == "m" && t == "ft" { return Ok(val * 3.28084); }
        if f == "ft" && t == "m" { return Ok(val / 3.28084); }

        Err(format!("Konversi dari '{}' ke '{}' belum didukung", from, to))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_arithmetic() {
        assert_eq!(MathEvaluator::eval("2 + 3 * 4").unwrap(), 14.0);
        assert_eq!(MathEvaluator::eval("(2 + 3) * 4").unwrap(), 20.0);
        assert_eq!(MathEvaluator::eval("10 / 2 - 3").unwrap(), 2.0);
    }

    #[test]
    fn test_scientific_math() {
        assert_eq!(MathEvaluator::eval("sqrt(16)").unwrap(), 4.0);
        assert_eq!(MathEvaluator::eval("2 ^ 3").unwrap(), 8.0);
        assert!((MathEvaluator::eval("sin(0)").unwrap() - 0.0).abs() < 1e-6);
        assert!((MathEvaluator::eval("cos(0)").unwrap() - 1.0).abs() < 1e-6);
    }

    #[test]
    fn test_programmer_bases() {
        let b = ProgrammerCalc::convert(255);
        assert_eq!(b.dec, 255);
        assert_eq!(b.hex, "0xFF");
        assert_eq!(b.oct, "0o377");
        assert!(b.bin.contains("11111111"));
    }

    #[test]
    fn test_unit_converter() {
        let f = UnitConverter::convert(100.0, "c", "f").unwrap();
        assert_eq!(f, 212.0);

        let mb = UnitConverter::convert(2.0, "gb", "mb").unwrap();
        assert_eq!(mb, 2048.0);
    }
}
