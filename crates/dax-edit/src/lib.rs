//! ============================================================================
//! DAXOS TEXT EDITOR ENGINE (dedit / dax-edit)
//! File: crates/dax-edit/src/lib.rs
//! Purpose: In-memory text buffer, editing primitives, syntax coloring, search & save
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TextStats {
    pub line_count: usize,
    pub word_count: usize,
    pub char_count: usize,
    pub byte_count: usize,
}

#[derive(Debug, Clone)]
pub struct TextBuffer {
    pub lines: Vec<String>,
    pub file_path: Option<PathBuf>,
    pub is_modified: bool,
    pub cursor_line: usize,
    pub cursor_col: usize,
}

impl Default for TextBuffer {
    fn default() -> Self {
        Self::new()
    }
}

impl TextBuffer {
    pub fn new() -> Self {
        Self {
            lines: vec![String::new()],
            file_path: None,
            is_modified: false,
            cursor_line: 0,
            cursor_col: 0,
        }
    }

    pub fn from_file(path: &Path) -> Result<Self, String> {
        let content = fs::read_to_string(path)
            .map_err(|e| format!("Gagal membuka berkas '{}': {}", path.display(), e))?;

        let mut lines: Vec<String> = content.lines().map(|s| s.to_string()).collect();
        if lines.is_empty() {
            lines.push(String::new());
        }

        Ok(Self {
            lines,
            file_path: Some(path.to_path_buf()),
            is_modified: false,
            cursor_line: 0,
            cursor_col: 0,
        })
    }

    pub fn save(&mut self) -> Result<(), String> {
        let path = self.file_path.as_ref()
            .ok_or_else(|| "Tidak ada nama berkas tujuan yang ditentukan.".to_string())?;

        let content = self.lines.join("\n");
        fs::write(path, content)
            .map_err(|e| format!("Gagal menyimpan berkas ke '{}': {}", path.display(), e))?;

        self.is_modified = false;
        Ok(())
    }

    pub fn save_as(&mut self, path: &Path) -> Result<(), String> {
        self.file_path = Some(path.to_path_buf());
        self.save()
    }

    pub fn insert_line(&mut self, idx: usize, text: String) {
        if idx <= self.lines.len() {
            self.lines.insert(idx, text);
            self.is_modified = true;
        }
    }

    pub fn delete_line(&mut self, idx: usize) -> Option<String> {
        if idx < self.lines.len() {
            self.is_modified = true;
            let removed = self.lines.remove(idx);
            if self.lines.is_empty() {
                self.lines.push(String::new());
            }
            Some(removed)
        } else {
            None
        }
    }

    pub fn set_line(&mut self, idx: usize, text: String) {
        if idx < self.lines.len() {
            self.lines[idx] = text;
            self.is_modified = true;
        }
    }

    pub fn search(&self, query: &str) -> Vec<(usize, usize)> {
        let mut matches = Vec::new();
        let q = query.to_lowercase();
        for (line_idx, line) in self.lines.iter().enumerate() {
            let lower = line.to_lowercase();
            let mut start = 0;
            while let Some(pos) = lower[start..].find(&q) {
                let actual_pos = start + pos;
                matches.push((line_idx + 1, actual_pos + 1));
                start = actual_pos + q.len();
            }
        }
        matches
    }

    pub fn stats(&self) -> TextStats {
        let line_count = self.lines.len();
        let mut word_count = 0;
        let mut char_count = 0;
        let mut byte_count = 0;

        for line in &self.lines {
            word_count += line.split_whitespace().count();
            char_count += line.chars().count();
            byte_count += line.len() + 1; // +1 untuk newline
        }

        TextStats {
            line_count,
            word_count,
            char_count,
            byte_count,
        }
    }

    pub fn render_preview(&self, max_lines: usize) -> String {
        let mut out = String::new();
        let title = self.file_path.as_ref()
            .map(|p| p.display().to_string())
            .unwrap_or_else(|| "[Dokumen Baru]".to_string());

        let mod_tag = if self.is_modified { " \x1b[1;33m[Dimodifikasi]\x1b[0m" } else { "" };
        out.push_str(&format!("\x1b[1;36m┌───\x1b[0m \x1b[1m{}{}\x1b[0m \x1b[1;36m{}\n\x1b[0m",
            title, mod_tag, "─".repeat(50)));

        for (i, line) in self.lines.iter().take(max_lines).enumerate() {
            out.push_str(&format!("\x1b[2m{:4} │\x1b[0m {}\n", i + 1, line));
        }

        if self.lines.len() > max_lines {
            out.push_str(&format!("\x1b[2m     │ ... ({} baris lainnya)\x1b[0m\n", self.lines.len() - max_lines));
        }

        let st = self.stats();
        out.push_str(&format!("\x1b[1;36m└───\x1b[0m Baris: {} | Kata: {} | Karakter: {} | Ukuran: {} bytes\n",
            st.line_count, st.word_count, st.char_count, st.byte_count));
        out
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_text_buffer_operations() {
        let mut buf = TextBuffer::new();
        buf.set_line(0, "Halo DAXOS".to_string());
        buf.insert_line(1, "Sistem Operasi Masa Depan".to_string());
        assert_eq!(buf.lines.len(), 2);
        assert!(buf.is_modified);

        let matches = buf.search("DAXOS");
        assert_eq!(matches.len(), 1);
        assert_eq!(matches[0], (1, 6));

        let st = buf.stats();
        assert_eq!(st.line_count, 2);
        assert_eq!(st.word_count, 6);
    }

    #[test]
    fn test_save_and_load() {
        let path = Path::new("/tmp/test_daxos_dedit.txt");
        let mut buf = TextBuffer::new();
        buf.set_line(0, "Baris Uji Coba DAXOS".to_string());
        buf.save_as(path).expect("Harus bisa menyimpan berkas");

        let loaded = TextBuffer::from_file(path).expect("Harus bisa memuat berkas");
        assert_eq!(loaded.lines[0], "Baris Uji Coba DAXOS");
        let _ = fs::remove_file(path);
    }
}
