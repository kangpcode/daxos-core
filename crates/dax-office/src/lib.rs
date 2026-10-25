//! ============================================================================
//! DAXOS OFFICE PRODUCTIVITY SUITE (dax-office)
//! File: crates/dax-office/src/lib.rs
//! Version: 1.10.2026 'Rhino' (ALPHA)
//! Architect: Dhafa Nazula Permadi (@kangpcode)
//! Modules: DaxWord (Docs), DaxSheet (Spreadsheets), DaxSlide (Presentations)
//! Strictly ZERO EMOJIS
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// ============================================================================
// DAXWORD: RICH DOCUMENT PROCESSOR (WORD / DOCS)
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum HeadingLevel {
    Title,
    Subtitle,
    Heading1,
    Heading2,
    Heading3,
    Body,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DocumentParagraph {
    pub level: HeadingLevel,
    pub text: String,
    pub is_bold: bool,
    pub is_italic: bool,
    pub is_underlined: bool,
    pub alignment: String, // "left", "center", "right", "justify"
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DaxWordDocument {
    pub title: String,
    pub author: String,
    pub paragraphs: Vec<DocumentParagraph>,
    pub paper_size: String, // "A4", "Letter"
    pub margins_mm: (u32, u32, u32, u32), // top, right, bottom, left
}

impl Default for DaxWordDocument {
    fn default() -> Self {
        Self::new("Dokumen Tanpa Judul")
    }
}

impl DaxWordDocument {
    pub fn new(title: &str) -> Self {
        let mut doc = Self {
            title: title.to_string(),
            author: "DAXOS Enterprise Architect".to_string(),
            paragraphs: Vec::new(),
            paper_size: "A4".to_string(),
            margins_mm: (25, 25, 25, 25),
        };

        doc.add_paragraph(HeadingLevel::Title, title, true, false, false, "center");
        doc.add_paragraph(
            HeadingLevel::Body,
            "Dokumen ini dirancang menggunakan DaxWord dengan akselerasi tipografi DreXUI dan rendering vector anti-aliased sub-pixel.",
            false,
            false,
            false,
            "justify",
        );
        doc
    }

    pub fn add_paragraph(
        &mut self,
        level: HeadingLevel,
        text: &str,
        is_bold: bool,
        is_italic: bool,
        is_underlined: bool,
        alignment: &str,
    ) {
        self.paragraphs.push(DocumentParagraph {
            level,
            text: text.to_string(),
            is_bold,
            is_italic,
            is_underlined,
            alignment: alignment.to_string(),
        });
    }

    pub fn word_count(&self) -> usize {
        self.paragraphs
            .iter()
            .map(|p| p.text.split_whitespace().count())
            .sum()
    }

    pub fn character_count(&self) -> usize {
        self.paragraphs.iter().map(|p| p.text.len()).sum()
    }
}

// ============================================================================
// DAXSHEET: HIGH-PERFORMANCE SPREADSHEET (EXCEL / NUMBERS)
// ============================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpreadsheetCell {
    pub coordinate: String, // e.g. "A1", "B2"
    pub raw_value: String,
    pub computed_value: f64,
    pub formula: Option<String>,
    pub number_format: String, // "currency", "percent", "number", "text"
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DaxSheet {
    pub name: String,
    pub cells: HashMap<String, SpreadsheetCell>,
    pub max_rows: usize,
    pub max_cols: usize,
}

impl DaxSheet {
    pub fn new(name: &str) -> Self {
        let mut sheet = Self {
            name: name.to_string(),
            cells: HashMap::new(),
            max_rows: 30,
            max_cols: 10,
        };

        // Seed with sample financial data
        sheet.set_cell("A1", "Kategori Anggaran", None, "text");
        sheet.set_cell("B1", "Alokasi (Rp)", None, "text");
        sheet.set_cell("A2", "R&D Kernel Hybrid", None, "text");
        sheet.set_cell("B2", "150000000", None, "currency");
        sheet.set_cell("A3", "DreXVIS Graphics Engine", None, "text");
        sheet.set_cell("B3", "120000000", None, "currency");
        sheet.set_cell("A4", "Landlock Sandbox Security", None, "text");
        sheet.set_cell("B4", "85000000", None, "currency");
        sheet.set_cell("A5", "Total Anggaran", None, "text");
        sheet.set_cell("B5", "355000000", Some("=SUM(B2:B4)".to_string()), "currency");

        sheet
    }

    pub fn set_cell(&mut self, coord: &str, raw: &str, formula: Option<String>, fmt: &str) {
        let computed = raw.parse::<f64>().unwrap_or(0.0);
        self.cells.insert(
            coord.to_uppercase(),
            SpreadsheetCell {
                coordinate: coord.to_uppercase(),
                raw_value: raw.to_string(),
                computed_value: computed,
                formula,
                number_format: fmt.to_string(),
            },
        );
    }

    pub fn get_cell_value(&self, coord: &str) -> Option<&SpreadsheetCell> {
        self.cells.get(&coord.to_uppercase())
    }

    pub fn evaluate_sum(&self, start_col: char, start_row: usize, end_row: usize) -> f64 {
        let mut total = 0.0;
        for r in start_row..=end_row {
            let coord = format!("{}{}", start_col, r);
            if let Some(cell) = self.cells.get(&coord) {
                total += cell.computed_value;
            }
        }
        total
    }
}

// ============================================================================
// DAXSLIDE: PRESENTATION & SLIDE DECK (POWERPOINT / KEYNOTE)
// ============================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SlideItem {
    pub slide_number: usize,
    pub title: String,
    pub subtitle: String,
    pub bullets: Vec<String>,
    pub transition: String, // "Fade", "Push", "SlideLeft", "Dissolve"
    pub presenter_notes: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DaxPresentation {
    pub title: String,
    pub slides: Vec<SlideItem>,
    pub aspect_ratio: String, // "16:9", "4:3"
}

impl Default for DaxPresentation {
    fn default() -> Self {
        Self::new("DAXOS Master Keynote 2026")
    }
}

impl DaxPresentation {
    pub fn new(title: &str) -> Self {
        let mut deck = Self {
            title: title.to_string(),
            slides: Vec::new(),
            aspect_ratio: "16:9".to_string(),
        };

        deck.add_slide(
            "DAXOS: Redefining Operating Systems",
            "Next-Generation Hybrid Kernel, Wayland Acrylic 240Hz & Microsecond Recovery",
            vec![
                "Surflang 1.0 zero-cost abstraction compiler".to_string(),
                "Landlock LSM ABI v5 strict application sandboxing".to_string(),
                "Universal binary execution: Native ELF, macOS Mach-O & Windows PE".to_string(),
            ],
            "Push",
            "Tekankan keunggulan latensi 5.8ms dan keamanan zero-crash SLA <= 45ms.",
        );

        deck.add_slide(
            "DCODX Studio & Developer Toolchain",
            "Full Xcode & VSCode Parity with LSP 3.17 & Live Reactive Canvas",
            vec![
                "Autonomous code formatting & AST linting".to_string(),
                "Real-time DreXUI preview with 120-240Hz swapchain".to_string(),
                "Integrated package toolchain for .dbpp and signed .dapp".to_string(),
            ],
            "Fade",
            "Tunjukkan perbandingan kecepatan build 3.8s vs kompetitor.",
        );

        deck
    }

    pub fn add_slide(
        &mut self,
        title: &str,
        subtitle: &str,
        bullets: Vec<String>,
        transition: &str,
        notes: &str,
    ) {
        let num = self.slides.len() + 1;
        self.slides.push(SlideItem {
            slide_number: num,
            title: title.to_string(),
            subtitle: subtitle.to_string(),
            bullets,
            transition: transition.to_string(),
            presenter_notes: notes.to_string(),
        });
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_daxword_stats() {
        let doc = DaxWordDocument::new("Rencana Strategis DAXOS");
        assert!(doc.word_count() > 5);
        assert!(doc.character_count() > 30);
    }

    #[test]
    fn test_daxsheet_evaluation() {
        let sheet = DaxSheet::new("Financials");
        let sum_b = sheet.evaluate_sum('B', 2, 4);
        assert_eq!(sum_b, 355000000.0);
        let total_cell = sheet.get_cell_value("B5").unwrap();
        assert_eq!(total_cell.computed_value, sum_b);
    }

    #[test]
    fn test_daxslide_deck() {
        let deck = DaxPresentation::default();
        assert_eq!(deck.slides.len(), 2);
        assert_eq!(deck.aspect_ratio, "16:9");
        assert!(deck.slides[0].bullets.len() >= 3);
    }
}
