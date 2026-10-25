//! DAXOS Font Manager Subsystem & Typography Rendering Engine
//!
//! Provides enterprise-grade font management, font discovery, character mapping,
//! subpixel antialiasing tuning, and font installation for DAXOS.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum FontCategory {
    System,
    SansSerif,
    Serif,
    Monospace,
    Display,
    User,
}

impl FontCategory {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::System => "Sistem DAXOS",
            Self::SansSerif => "Sans-Serif",
            Self::Serif => "Serif",
            Self::Monospace => "Monospace / Kode",
            Self::Display => "Tampilan / Judul",
            Self::User => "Font Pengguna",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FontWeightItem {
    pub weight_name: String,
    pub weight_value: u32,
    pub italic: bool,
    pub postscript_name: String,
    pub file_path: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FontFamily {
    pub name: String,
    pub category: FontCategory,
    pub designer: String,
    pub license: String,
    pub version: String,
    pub format: String,
    pub glyph_count: u32,
    pub opentype_features: Vec<String>,
    pub weights: Vec<FontWeightItem>,
    pub sample_pangram: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GlyphInfo {
    pub character: char,
    pub unicode_hex: String,
    pub name: String,
    pub category: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TypographyRenderConfig {
    pub antialiasing: String,
    pub hinting_level: String,
    pub subpixel_order: String,
    pub lcd_filter: String,
    pub gamma: f32,
    pub font_dpi: u32,
}

impl Default for TypographyRenderConfig {
    fn default() -> Self {
        Self {
            antialiasing: "Subpixel LCD (RGB)".to_string(),
            hinting_level: "Slight".to_string(),
            subpixel_order: "RGB (Horizontal)".to_string(),
            lcd_filter: "Light (FreeType v2.13)".to_string(),
            gamma: 1.0,
            font_dpi: 96,
        }
    }
}

/// Returns the registry of built-in and user fonts in DAXOS
pub fn get_system_font_catalog() -> Vec<FontFamily> {
    vec![
        FontFamily {
            name: "Inter Display".to_string(),
            category: FontCategory::SansSerif,
            designer: "Rasmus Andersson".to_string(),
            license: "SIL Open Font License 1.1".to_string(),
            version: "v4.001".to_string(),
            format: "OpenType CFF (.otf)".to_string(),
            glyph_count: 2548,
            opentype_features: vec![
                "calt (Contextual Alternates)".to_string(),
                "dlig (Discretionary Ligatures)".to_string(),
                "tnum (Tabular Figures)".to_string(),
                "cv01 (Alternative 1)".to_string(),
                "ss01 (Open Digits)".to_string(),
            ],
            weights: vec![
                FontWeightItem {
                    weight_name: "Thin".to_string(),
                    weight_value: 100,
                    italic: false,
                    postscript_name: "Inter-Thin".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-Thin.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Light".to_string(),
                    weight_value: 300,
                    italic: false,
                    postscript_name: "Inter-Light".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-Light.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Regular".to_string(),
                    weight_value: 400,
                    italic: false,
                    postscript_name: "Inter-Regular".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-Regular.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Medium".to_string(),
                    weight_value: 500,
                    italic: false,
                    postscript_name: "Inter-Medium".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-Medium.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "SemiBold".to_string(),
                    weight_value: 600,
                    italic: false,
                    postscript_name: "Inter-SemiBold".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Bold".to_string(),
                    weight_value: 700,
                    italic: false,
                    postscript_name: "Inter-Bold".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-Bold.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Black".to_string(),
                    weight_value: 900,
                    italic: false,
                    postscript_name: "Inter-Black".to_string(),
                    file_path: "/usr/share/fonts/opentype/inter/Inter-Black.otf".to_string(),
                },
            ],
            sample_pangram: "The quick brown fox jumps over the lazy dog 1234567890".to_string(),
        },
        FontFamily {
            name: "JetBrains Mono".to_string(),
            category: FontCategory::Monospace,
            designer: "JetBrains & Philipp Nurullin".to_string(),
            license: "Apache License 2.0".to_string(),
            version: "v2.304".to_string(),
            format: "TrueType (.ttf)".to_string(),
            glyph_count: 1480,
            opentype_features: vec![
                "calt (Programming Ligatures ->, !=, ===, <=)".to_string(),
                "zero (Slashed Zero)".to_string(),
                "cv01 (Alternative f)".to_string(),
            ],
            weights: vec![
                FontWeightItem {
                    weight_name: "Regular".to_string(),
                    weight_value: 400,
                    italic: false,
                    postscript_name: "JetBrainsMono-Regular".to_string(),
                    file_path: "/usr/share/fonts/truetype/jetbrains/JetBrainsMono-Regular.ttf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Medium".to_string(),
                    weight_value: 500,
                    italic: false,
                    postscript_name: "JetBrainsMono-Medium".to_string(),
                    file_path: "/usr/share/fonts/truetype/jetbrains/JetBrainsMono-Medium.ttf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Bold".to_string(),
                    weight_value: 700,
                    italic: false,
                    postscript_name: "JetBrainsMono-Bold".to_string(),
                    file_path: "/usr/share/fonts/truetype/jetbrains/JetBrainsMono-Bold.ttf".to_string(),
                },
                FontWeightItem {
                    weight_name: "ExtraBold".to_string(),
                    weight_value: 800,
                    italic: false,
                    postscript_name: "JetBrainsMono-ExtraBold".to_string(),
                    file_path: "/usr/share/fonts/truetype/jetbrains/JetBrainsMono-ExtraBold.ttf".to_string(),
                },
            ],
            sample_pangram: "fn main() -> Result<(), Box<dyn Error>> { daxos_boost(240); }".to_string(),
        },
        FontFamily {
            name: "Fira Code".to_string(),
            category: FontCategory::Monospace,
            designer: "Nikita Prokopov".to_string(),
            license: "SIL Open Font License 1.1".to_string(),
            version: "v6.200".to_string(),
            format: "OpenType CFF (.otf)".to_string(),
            glyph_count: 1220,
            opentype_features: vec![
                "calt (Rich Ligatures)".to_string(),
                "zero (Dotted Zero)".to_string(),
            ],
            weights: vec![
                FontWeightItem {
                    weight_name: "Regular".to_string(),
                    weight_value: 400,
                    italic: false,
                    postscript_name: "FiraCode-Regular".to_string(),
                    file_path: "/usr/share/fonts/opentype/fira/FiraCode-Regular.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Bold".to_string(),
                    weight_value: 700,
                    italic: false,
                    postscript_name: "FiraCode-Bold".to_string(),
                    file_path: "/usr/share/fonts/opentype/fira/FiraCode-Bold.otf".to_string(),
                },
            ],
            sample_pangram: "const SLA: f32 = 0.045; // SLA Recovery <= 45ms".to_string(),
        },
        FontFamily {
            name: "Playfair Display".to_string(),
            category: FontCategory::Serif,
            designer: "Claus Eggers Sorensen".to_string(),
            license: "SIL Open Font License 1.1".to_string(),
            version: "v2.102".to_string(),
            format: "OpenType CFF (.otf)".to_string(),
            glyph_count: 1180,
            opentype_features: vec![
                "kern (Optical Kerning)".to_string(),
                "liga (Standard Ligatures)".to_string(),
            ],
            weights: vec![
                FontWeightItem {
                    weight_name: "Regular".to_string(),
                    weight_value: 400,
                    italic: false,
                    postscript_name: "PlayfairDisplay-Regular".to_string(),
                    file_path: "/usr/share/fonts/opentype/playfair/PlayfairDisplay-Regular.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Bold".to_string(),
                    weight_value: 700,
                    italic: false,
                    postscript_name: "PlayfairDisplay-Bold".to_string(),
                    file_path: "/usr/share/fonts/opentype/playfair/PlayfairDisplay-Bold.otf".to_string(),
                },
                FontWeightItem {
                    weight_name: "Black".to_string(),
                    weight_value: 900,
                    italic: false,
                    postscript_name: "PlayfairDisplay-Black".to_string(),
                    file_path: "/usr/share/fonts/opentype/playfair/PlayfairDisplay-Black.otf".to_string(),
                },
            ],
            sample_pangram: "Kemegahan Arsitektur Modern DAXOS Hybrid Operating System".to_string(),
        },
        FontFamily {
            name: "Outfit".to_string(),
            category: FontCategory::Display,
            designer: "Outfit International & Rodrigo Fuenzalida".to_string(),
            license: "SIL Open Font License 1.1".to_string(),
            version: "v1.200".to_string(),
            format: "TrueType (.ttf)".to_string(),
            glyph_count: 1350,
            opentype_features: vec![
                "ss01 (Geometric Stylistic Set)".to_string(),
                "tnum (Tabular Figures)".to_string(),
            ],
            weights: vec![
                FontWeightItem {
                    weight_name: "Regular".to_string(),
                    weight_value: 400,
                    italic: false,
                    postscript_name: "Outfit-Regular".to_string(),
                    file_path: "/usr/share/fonts/truetype/outfit/Outfit-Regular.ttf".to_string(),
                },
                FontWeightItem {
                    weight_name: "SemiBold".to_string(),
                    weight_value: 600,
                    italic: false,
                    postscript_name: "Outfit-SemiBold".to_string(),
                    file_path: "/usr/share/fonts/truetype/outfit/Outfit-SemiBold.ttf".to_string(),
                },
                FontWeightItem {
                    weight_name: "ExtraBold".to_string(),
                    weight_value: 800,
                    italic: false,
                    postscript_name: "Outfit-ExtraBold".to_string(),
                    file_path: "/usr/share/fonts/truetype/outfit/Outfit-ExtraBold.ttf".to_string(),
                },
            ],
            sample_pangram: "DAXOS 1.10.2026 Rhino: Fast, Fluid, and Futuristic".to_string(),
        },
    ]
}

/// Returns sample Unicode glyphs for inspector
pub fn get_sample_unicode_glyphs() -> Vec<GlyphInfo> {
    vec![
        GlyphInfo { character: 'A', unicode_hex: "U+0041".to_string(), name: "Latin Capital Letter A".to_string(), category: "Uppercase Letter".to_string() },
        GlyphInfo { character: 'B', unicode_hex: "U+0042".to_string(), name: "Latin Capital Letter B".to_string(), category: "Uppercase Letter".to_string() },
        GlyphInfo { character: 'C', unicode_hex: "U+0043".to_string(), name: "Latin Capital Letter C".to_string(), category: "Uppercase Letter".to_string() },
        GlyphInfo { character: 'a', unicode_hex: "U+0061".to_string(), name: "Latin Small Letter A".to_string(), category: "Lowercase Letter".to_string() },
        GlyphInfo { character: 'b', unicode_hex: "U+0062".to_string(), name: "Latin Small Letter B".to_string(), category: "Lowercase Letter".to_string() },
        GlyphInfo { character: 'c', unicode_hex: "U+0063".to_string(), name: "Latin Small Letter C".to_string(), category: "Lowercase Letter".to_string() },
        GlyphInfo { character: '0', unicode_hex: "U+0030".to_string(), name: "Digit Zero".to_string(), category: "Decimal Digit".to_string() },
        GlyphInfo { character: '1', unicode_hex: "U+0031".to_string(), name: "Digit One".to_string(), category: "Decimal Digit".to_string() },
        GlyphInfo { character: '2', unicode_hex: "U+0032".to_string(), name: "Digit Two".to_string(), category: "Decimal Digit".to_string() },
        GlyphInfo { character: '∑', unicode_hex: "U+2211".to_string(), name: "N-Ary Summation".to_string(), category: "Math Symbol".to_string() },
        GlyphInfo { character: '√', unicode_hex: "U+221A".to_string(), name: "Square Root".to_string(), category: "Math Symbol".to_string() },
        GlyphInfo { character: '∫', unicode_hex: "U+222B".to_string(), name: "Integral".to_string(), category: "Math Symbol".to_string() },
        GlyphInfo { character: '→', unicode_hex: "U+2192".to_string(), name: "Rightwards Arrow".to_string(), category: "Arrow".to_string() },
        GlyphInfo { character: '⇒', unicode_hex: "U+21D2".to_string(), name: "Rightwards Double Arrow".to_string(), category: "Arrow".to_string() },
        GlyphInfo { character: '⌘', unicode_hex: "U+2318".to_string(), name: "Place of Interest Sign (Command)".to_string(), category: "Symbol".to_string() },
        GlyphInfo { character: '⌥', unicode_hex: "U+2325".to_string(), name: "Option Key".to_string(), category: "Symbol".to_string() },
        GlyphInfo { character: '⇧', unicode_hex: "U+21E7".to_string(), name: "Upwards White Arrow (Shift)".to_string(), category: "Symbol".to_string() },
        GlyphInfo { character: '⏎', unicode_hex: "U+23CE".to_string(), name: "Return Symbol".to_string(), category: "Symbol".to_string() },
    ]
}

/// Simulate installing a font package into DAXOS system fonts directory
pub fn install_font(path: &str) -> Result<String, String> {
    if !path.ends_with(".ttf") && !path.ends_with(".otf") && !path.ends_with(".woff2") {
        return Err("Format tidak didukung. Harap gunakan berkas .ttf, .otf, atau .woff2".to_string());
    }
    let font_name = std::path::Path::new(path)
        .file_stem()
        .and_then(|s| s.to_str())
        .unwrap_or("CustomFont");

    Ok(format!(
        "Berhasil memasang font '{}' ke /usr/share/fonts/opentype/user/. Cache font fc-cache diperbarui.",
        font_name
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_system_font_catalog() {
        let catalog = get_system_font_catalog();
        assert!(catalog.len() >= 5);
        let inter = catalog.iter().find(|f| f.name == "Inter Display");
        assert!(inter.is_some());
        assert_eq!(inter.unwrap().category, FontCategory::SansSerif);
        assert!(inter.unwrap().weights.len() >= 4);
    }

    #[test]
    fn test_unicode_glyphs() {
        let glyphs = get_sample_unicode_glyphs();
        assert!(!glyphs.is_empty());
        let sum_sym = glyphs.iter().find(|g| g.character == '∑');
        assert!(sum_sym.is_some());
        assert_eq!(sum_sym.unwrap().unicode_hex, "U+2211");
    }

    #[test]
    fn test_font_installation() {
        let res_ok = install_font("/home/user/Downloads/GeistMono-Regular.otf");
        assert!(res_ok.is_ok());
        let res_err = install_font("/home/user/Downloads/sample.txt");
        assert!(res_err.is_err());
    }
}
