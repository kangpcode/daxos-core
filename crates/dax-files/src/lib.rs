//! ============================================================================
//! DAXOS FILE MANAGER CORE ENGINE (dfm / dax-files)
//! File: crates/dax-files/src/lib.rs
//! Purpose: Real file operations, tree traversal, metadata, checksums, and search
//! ============================================================================

use serde::{Deserialize, Serialize};
use sha3::{Digest, Sha3_512};
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::path::Path;
use std::time::SystemTime;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileEntry {
    pub name: String,
    pub path: String,
    pub is_dir: bool,
    pub is_symlink: bool,
    pub size_bytes: u64,
    pub modified_str: String,
    pub permissions_str: String,
    pub icon: &'static str,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeepFileInfo {
    pub path: String,
    pub name: String,
    pub is_dir: bool,
    pub size_bytes: u64,
    pub size_formatted: String,
    pub permissions_octal: String,
    pub modified_str: String,
    pub sha3_512_hash: Option<String>,
    pub mime_hint: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrashEntry {
    pub id: String,
    pub original_name: String,
    pub original_path: String,
    pub deletion_date: String,
    pub size_bytes: u64,
    pub size_formatted: String,
}

pub struct FileManager;

impl FileManager {
    /// Baca direktori dan kembalikan daftar berkas dengan detail
    pub fn list_dir(dir_path: &Path, show_hidden: bool) -> Result<Vec<FileEntry>, String> {
        let mut entries = Vec::new();
        let read_dir = fs::read_dir(dir_path)
            .map_err(|e| format!("Gagal membaca direktori '{}': {}", dir_path.display(), e))?;

        for entry in read_dir.flatten() {
            let name = entry.file_name().to_string_lossy().to_string();
            if !show_hidden && name.starts_with('.') {
                continue;
            }

            let path = entry.path();
            let metadata = entry.metadata().ok();
            let is_dir = metadata.as_ref().map(|m| m.is_dir()).unwrap_or(false);
            let is_symlink = metadata.as_ref().map(|m| m.file_type().is_symlink()).unwrap_or(false);
            let size_bytes = metadata.as_ref().map(|m| m.len()).unwrap_or(0);

            let permissions_str = metadata.as_ref()
                .map(|m| format_mode(m.permissions().mode()))
                .unwrap_or_else(|| "---------".to_string());

            let modified_str = metadata.as_ref()
                .and_then(|m| m.modified().ok())
                .map(format_system_time)
                .unwrap_or_else(|| "-".to_string());

            let icon = if is_dir {
                "[DIR]"
            } else if is_symlink {
                "[LINK]"
            } else {
                file_icon(&name)
            };

            entries.push(FileEntry {
                name,
                path: path.to_string_lossy().to_string(),
                is_dir,
                is_symlink,
                size_bytes,
                modified_str,
                permissions_str,
                icon,
            });
        }

        // Urutkan: direktori lebih dulu, lalu nama secara alfabetis
        entries.sort_by(|a, b| {
            b.is_dir.cmp(&a.is_dir).then_with(|| a.name.to_lowercase().cmp(&b.name.to_lowercase()))
        });

        Ok(entries)
    }

    /// Tampilkan visualisasi pohon direktori rekursif
    pub fn get_tree(dir_path: &Path, max_depth: usize) -> Vec<String> {
        let mut lines = Vec::new();
        lines.push(format!("\x1b[1;36m{}\x1b[0m", dir_path.display()));
        Self::build_tree_recursive(dir_path, "", 0, max_depth, &mut lines);
        lines
    }

    fn build_tree_recursive(dir: &Path, prefix: &str, depth: usize, max_depth: usize, out: &mut Vec<String>) {
        if depth >= max_depth {
            return;
        }

        if let Ok(entries) = fs::read_dir(dir) {
            let mut list: Vec<_> = entries.flatten().collect();
            list.sort_by_key(|e| e.file_name());

            let count = list.len();
            for (i, entry) in list.iter().enumerate() {
                let name = entry.file_name().to_string_lossy().to_string();
                if name.starts_with('.') { continue; }

                let is_last = i + 1 == count;
                let branch = if is_last { "└── " } else { "├── " };
                let next_prefix = if is_last { "    " } else { "│   " };

                let is_dir = entry.file_type().map(|t| t.is_dir()).unwrap_or(false);
                let icon = if is_dir { "[DIR]" } else { file_icon(&name) };

                out.push(format!("{}{}{} {}", prefix, branch, icon, name));

                if is_dir {
                    let sub_prefix = format!("{}{}", prefix, next_prefix);
                    Self::build_tree_recursive(&entry.path(), &sub_prefix, depth + 1, max_depth, out);
                }
            }
        }
    }

    /// Ambil informasi detail berkas beserta hash SHA3-512
    pub fn get_info(path: &Path) -> Result<DeepFileInfo, String> {
        let metadata = fs::metadata(path)
            .map_err(|e| format!("Gagal membaca metadata '{}': {}", path.display(), e))?;

        let is_dir = metadata.is_dir();
        let size_bytes = metadata.len();
        let mode = metadata.permissions().mode();
        let octal_str = format!("{:04o}", mode & 0o7777);

        let modified_str = metadata.modified().ok()
            .map(format_system_time)
            .unwrap_or_else(|| "-".to_string());

        let name = path.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();

        let sha3_512_hash = if !is_dir && size_bytes <= 100 * 1024 * 1024 {
            // Hitung SHA3-512 hanya untuk berkas < 100MB
            fs::read(path).ok().map(|bytes| {
                let mut hasher = Sha3_512::new();
                hasher.update(&bytes);
                format!("{:x}", hasher.finalize())
            })
        } else {
            None
        };

        let mime_hint = detect_mime(&name, is_dir);

        Ok(DeepFileInfo {
            path: path.to_string_lossy().to_string(),
            name,
            is_dir,
            size_bytes,
            size_formatted: format_size(size_bytes),
            permissions_octal: octal_str,
            modified_str,
            sha3_512_hash,
            mime_hint,
        })
    }

    /// Cari berkas secara rekursif berdasarkan pola string
    pub fn find_files(dir_path: &Path, query: &str) -> Vec<String> {
        let mut results = Vec::new();
        let q = query.to_lowercase();
        Self::find_recursive(dir_path, &q, &mut results, 0, 10);
        results
    }

    fn find_recursive(dir: &Path, q: &str, out: &mut Vec<String>, depth: usize, max_depth: usize) {
        if depth > max_depth || out.len() >= 100 {
            return;
        }

        if let Ok(entries) = fs::read_dir(dir) {
            for entry in entries.flatten() {
                let name = entry.file_name().to_string_lossy().to_string();
                let path = entry.path();
                if name.to_lowercase().contains(q) {
                    out.push(path.to_string_lossy().to_string());
                }

                if let Ok(ft) = entry.file_type() {
                    if ft.is_dir() && !name.starts_with('.') {
                        Self::find_recursive(&path, q, out, depth + 1, max_depth);
                    }
                }
            }
        }
    }

    /// Hitung pemakaian disk direktori secara rekursif
    pub fn calc_disk_usage(path: &Path) -> (u64, usize) {
        let mut total_bytes = 0u64;
        let mut file_count = 0usize;

        if path.is_file() {
            if let Ok(meta) = fs::metadata(path) {
                return (meta.len(), 1);
            }
        }

        if let Ok(entries) = fs::read_dir(path) {
            for entry in entries.flatten() {
                let p = entry.path();
                if p.is_dir() {
                    let (sub_bytes, sub_files) = Self::calc_disk_usage(&p);
                    total_bytes += sub_bytes;
                    file_count += sub_files;
                } else if let Ok(m) = entry.metadata() {
                    total_bytes += m.len();
                    file_count += 1;
                }
            }
        }

        (total_bytes, file_count)
    }

    pub fn get_trash_base_dir() -> std::path::PathBuf {
        if let Ok(dir) = std::env::var("DAXOS_TRASH_DIR") {
            std::path::PathBuf::from(dir)
        } else if let Ok(home) = std::env::var("HOME") {
            std::path::PathBuf::from(home).join(".local/share/Trash")
        } else {
            std::path::PathBuf::from("/tmp/daxos_trash")
        }
    }

    /// Pindahkan berkas atau direktori ke Tempat Sampah (Recycle Bin)
    pub fn move_to_trash(target_path: &Path) -> Result<TrashEntry, String> {
        if !target_path.exists() {
            return Err(format!("Berkas atau direktori tidak ditemukan: '{}'", target_path.display()));
        }

        let abs_path = target_path.canonicalize()
            .map_err(|e| format!("Gagal menyelesaikan path absolut: {}", e))?;
        
        let file_name = abs_path.file_name()
            .map(|s| s.to_string_lossy().to_string())
            .unwrap_or_else(|| "unnamed".to_string());

        let (size_bytes, _) = Self::calc_disk_usage(&abs_path);
        let timestamp = chrono::Local::now().format("%Y%m%d_%H%M%S").to_string();
        let trash_id = format!("{}_{}", timestamp, file_name);

        let trash_base = Self::get_trash_base_dir();
        let files_dir = trash_base.join("files");
        let info_dir = trash_base.join("info");

        fs::create_dir_all(&files_dir).map_err(|e| format!("Gagal membuat direktori trash/files: {}", e))?;
        fs::create_dir_all(&info_dir).map_err(|e| format!("Gagal membuat direktori trash/info: {}", e))?;

        let dest_file = files_dir.join(&trash_id);
        fs::rename(&abs_path, &dest_file).or_else(|_| {
            if abs_path.is_dir() {
                Err(format!("Gagal memindahkan direktori ke trash"))
            } else {
                fs::copy(&abs_path, &dest_file)
                    .and_then(|_| fs::remove_file(&abs_path))
                    .map_err(|e| format!("Gagal menyalin ke trash: {}", e))
            }
        })?;

        let now_str = chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
        let info_content = format!(
            "[Trash Info]\nPath={}\nDeletionDate={}\nSize={}\nId={}\n",
            abs_path.display(),
            now_str,
            size_bytes,
            trash_id
        );

        let info_file = info_dir.join(format!("{}.trashinfo", trash_id));
        fs::write(&info_file, info_content)
            .map_err(|e| format!("Gagal menulis berkas metadata .trashinfo: {}", e))?;

        Ok(TrashEntry {
            id: trash_id,
            original_name: file_name,
            original_path: abs_path.to_string_lossy().to_string(),
            deletion_date: now_str,
            size_bytes,
            size_formatted: format_size(size_bytes),
        })
    }

    /// Daftar semua berkas yang ada di Tempat Sampah
    pub fn list_trash() -> Result<Vec<TrashEntry>, String> {
        let trash_base = Self::get_trash_base_dir();
        let info_dir = trash_base.join("info");
        if !info_dir.exists() {
            return Ok(Vec::new());
        }

        let mut entries = Vec::new();
        if let Ok(read_dir) = fs::read_dir(&info_dir) {
            for entry in read_dir.flatten() {
                let path = entry.path();
                if path.extension().and_then(|s| s.to_str()) == Some("trashinfo") {
                    if let Ok(content) = fs::read_to_string(&path) {
                        let mut orig_path = String::new();
                        let mut del_date = String::new();
                        let mut size_bytes = 0u64;
                        let mut id = path.file_stem().map(|s| s.to_string_lossy().to_string()).unwrap_or_default();

                        for line in content.lines() {
                            if let Some(v) = line.strip_prefix("Path=") {
                                orig_path = v.to_string();
                            } else if let Some(v) = line.strip_prefix("DeletionDate=") {
                                del_date = v.to_string();
                            } else if let Some(v) = line.strip_prefix("Size=") {
                                size_bytes = v.parse().unwrap_or(0);
                            } else if let Some(v) = line.strip_prefix("Id=") {
                                id = v.to_string();
                            }
                        }

                        let orig_name = Path::new(&orig_path)
                            .file_name()
                            .map(|s| s.to_string_lossy().to_string())
                            .unwrap_or_else(|| id.clone());

                        entries.push(TrashEntry {
                            id,
                            original_name: orig_name,
                            original_path: orig_path,
                            deletion_date: del_date,
                            size_bytes,
                            size_formatted: format_size(size_bytes),
                        });
                    }
                }
            }
        }

        entries.sort_by(|a, b| b.deletion_date.cmp(&a.deletion_date));
        Ok(entries)
    }

    /// Pulihkan berkas dari Tempat Sampah ke lokasi asalnya
    pub fn restore_from_trash(id_or_name: &str) -> Result<String, String> {
        let items = Self::list_trash()?;
        let target = items.into_iter().find(|it| it.id == id_or_name || it.original_name == id_or_name)
            .ok_or_else(|| format!("Item '{}' tidak ditemukan di Tempat Sampah", id_or_name))?;

        let trash_base = Self::get_trash_base_dir();
        let src_file = trash_base.join("files").join(&target.id);
        let dest_path = Path::new(&target.original_path);

        if let Some(parent) = dest_path.parent() {
            fs::create_dir_all(parent).ok();
        }

        fs::rename(&src_file, dest_path).or_else(|_| {
            fs::copy(&src_file, dest_path)
                .and_then(|_| fs::remove_file(&src_file))
                .map_err(|e| format!("Gagal memulihkan berkas: {}", e))
        })?;

        let info_file = trash_base.join("info").join(format!("{}.trashinfo", target.id));
        fs::remove_file(info_file).ok();

        Ok(target.original_path)
    }

    /// Kosongkan seluruh isi Tempat Sampah
    pub fn empty_trash() -> Result<usize, String> {
        let trash_base = Self::get_trash_base_dir();
        let files_dir = trash_base.join("files");
        let info_dir = trash_base.join("info");

        let mut count = 0;
        if files_dir.exists() {
            if let Ok(entries) = fs::read_dir(&files_dir) {
                for entry in entries.flatten() {
                    let p = entry.path();
                    if p.is_dir() {
                        fs::remove_dir_all(p).ok();
                    } else {
                        fs::remove_file(p).ok();
                    }
                    count += 1;
                }
            }
        }

        if info_dir.exists() {
            if let Ok(entries) = fs::read_dir(&info_dir) {
                for entry in entries.flatten() {
                    fs::remove_file(entry.path()).ok();
                }
            }
        }

        Ok(count)
    }
}

pub fn format_size(bytes: u64) -> String {
    if bytes < 1024 { return format!("{} B", bytes); }
    if bytes < 1024 * 1024 { return format!("{:.1} KB", bytes as f64 / 1024.0); }
    if bytes < 1024 * 1024 * 1024 { return format!("{:.1} MB", bytes as f64 / (1024.0 * 1024.0)); }
    format!("{:.2} GB", bytes as f64 / (1024.0 * 1024.0 * 1024.0))
}

fn format_mode(mode: u32) -> String {
    let r = |m, bit| if m & bit != 0 { 'r' } else { '-' };
    let w = |m, bit| if m & bit != 0 { 'w' } else { '-' };
    let x = |m, bit| if m & bit != 0 { 'x' } else { '-' };

    format!("{}{}{}{}{}{}{}{}{}",
        r(mode, 0o400), w(mode, 0o200), x(mode, 0o100),
        r(mode, 0o040), w(mode, 0o020), x(mode, 0o010),
        r(mode, 0o004), w(mode, 0o002), x(mode, 0o001),
    )
}

fn format_system_time(time: SystemTime) -> String {
    let datetime: chrono::DateTime<chrono::Local> = time.into();
    datetime.format("%Y-%m-%d %H:%M:%S").to_string()
}

fn file_icon(name: &str) -> &'static str {
    let ext = Path::new(name).extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();
    match ext.as_str() {
        "rs" | "surf" | "c" | "cpp" | "h" | "py" | "js" | "sh" => "[CFG]",
        "dapp" | "deb" | "rpm" | "tar" | "gz" | "zip" => "[PKG]",
        "png" | "jpg" | "jpeg" | "webp" | "svg" => "[IMG]",
        "mp3" | "wav" | "flac" | "ogg" => "[AUDIO]",
        "mp4" | "mkv" | "mov" | "webm" => "[VIDEO]",
        "json" | "toml" | "xml" | "yaml" | "yml" => "[DATA]",
        "md" | "txt" | "pdf" | "doc" => "[FILE]",
        _ => "[FILE]",
    }
}

fn detect_mime(name: &str, is_dir: bool) -> String {
    if is_dir { return "inode/directory".to_string(); }
    let ext = Path::new(name).extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();
    match ext.as_str() {
        "rs" => "text/x-rust".to_string(),
        "surf" => "text/x-surflang".to_string(),
        "c" | "cpp" => "text/x-c".to_string(),
        "py" => "text/x-python".to_string(),
        "json" => "application/json".to_string(),
        "toml" => "application/toml".to_string(),
        "dapp" => "application/x-daxos-dapp".to_string(),
        "png" => "image/png".to_string(),
        "jpg" | "jpeg" => "image/jpeg".to_string(),
        "md" => "text/markdown".to_string(),
        _ => "application/octet-stream".to_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_list_dir() {
        let entries = FileManager::list_dir(Path::new("."), false).unwrap();
        assert!(!entries.is_empty());
        assert!(entries.iter().any(|e| e.name == "Cargo.toml"));
    }

    #[test]
    fn test_file_info_and_hash() {
        let info = FileManager::get_info(Path::new("Cargo.toml")).unwrap();
        assert_eq!(info.name, "Cargo.toml");
        assert!(info.sha3_512_hash.is_some());
        assert!(!info.is_dir);
    }

    #[test]
    fn test_find_files() {
        let found = FileManager::find_files(Path::new("."), "Cargo.toml");
        assert!(!found.is_empty());
    }

    #[test]
    fn test_calc_disk_usage() {
        let (bytes, count) = FileManager::calc_disk_usage(Path::new("Cargo.toml"));
        assert!(bytes > 0);
        assert_eq!(count, 1);
    }

    #[test]
    fn test_trash_lifecycle() {
        let test_dir = tempfile_dir();
        let test_file = test_dir.join("test_trash_sample.txt");
        fs::write(&test_file, "Trash Test Payload DAXOS 2026").unwrap();
        assert!(test_file.exists());

        // Set custom trash dir for test isolation
        let trash_sandbox = test_dir.join("trash_vault");
        std::env::set_var("DAXOS_TRASH_DIR", &trash_sandbox);

        // 1. Move to trash
        let entry = FileManager::move_to_trash(&test_file).unwrap();
        assert_eq!(entry.original_name, "test_trash_sample.txt");
        assert!(!test_file.exists());

        // 2. List trash
        let items = FileManager::list_trash().unwrap();
        assert!(!items.is_empty());
        assert!(items.iter().any(|i| i.original_name == "test_trash_sample.txt"));

        // 3. Restore from trash
        let restored_path = FileManager::restore_from_trash(&entry.id).unwrap();
        assert_eq!(restored_path, test_file.to_string_lossy().to_string());
        assert!(test_file.exists());

        // 4. Move to trash again and empty trash
        FileManager::move_to_trash(&test_file).unwrap();
        let count = FileManager::empty_trash().unwrap();
        assert!(count >= 1);
        let items_after = FileManager::list_trash().unwrap();
        assert!(items_after.is_empty());

        // Clean up
        fs::remove_dir_all(&test_dir).ok();
        std::env::remove_var("DAXOS_TRASH_DIR");
    }

    fn tempfile_dir() -> std::path::PathBuf {
        let dir = std::env::temp_dir().join(format!("daxos_test_{}", std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
        fs::create_dir_all(&dir).unwrap();
        dir
    }
}
