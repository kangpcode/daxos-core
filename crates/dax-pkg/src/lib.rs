//! ============================================================================
//! DAXOS NATIVE PACKAGE MANAGER (dax)
//! File: crates/dax-pkg/src/lib.rs
//! Purpose: Full-featured package management for .dapp packages — setara apt/pacman
//!          Features: install, remove, upgrade, search, info, list, audit, pin, repo
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::fmt;

// ─────────────────────────────────────────────────────────────────────────────
// 1. DATA STRUCTURES
// ─────────────────────────────────────────────────────────────────────────────

/// Status instalasi paket
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum PackageStatus {
    Installed,
    Available,
    Upgradeable,
    Held,
    Broken,
    Removed,
}

impl fmt::Display for PackageStatus {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            PackageStatus::Installed    => "installed",
            PackageStatus::Available    => "available",
            PackageStatus::Upgradeable  => "upgradeable",
            PackageStatus::Held         => "held",
            PackageStatus::Broken       => "broken",
            PackageStatus::Removed      => "removed",
        };
        write!(f, "{}", s)
    }
}

/// Tipe dari sebuah paket
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum PackageKind {
    /// Aplikasi GUI dengan bundle .dapp
    Application,
    /// Library shared (dylib / rlib)
    Library,
    /// Command-line tool
    Tool,
    /// Sistem framework (DreXUI, DreXVIS, dll.)
    SystemFramework,
    /// Font, icon themes, dsb.
    Asset,
    /// Firmware perangkat keras
    Firmware,
}

impl fmt::Display for PackageKind {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            PackageKind::Application     => "app",
            PackageKind::Library         => "lib",
            PackageKind::Tool            => "tool",
            PackageKind::SystemFramework => "framework",
            PackageKind::Asset           => "asset",
            PackageKind::Firmware        => "firmware",
        };
        write!(f, "{}", s)
    }
}

/// Metadata paket lengkap
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PackageMetadata {
    pub id: String,
    pub name: String,
    pub version: String,
    pub kind: PackageKind,
    pub description: String,
    pub long_description: String,
    pub author: String,
    pub developer_id: String,
    pub homepage: String,
    pub license: String,
    pub categories: Vec<String>,
    pub tags: Vec<String>,
    pub dependencies: Vec<PackageDep>,
    pub conflicts: Vec<String>,
    pub replaces: Vec<String>,
    pub provides: Vec<String>,
    pub min_os_version: String,
    pub architectures: Vec<String>,
    pub installed_size_bytes: u64,
    pub download_size_bytes: u64,
    pub sha3_512: String,
    pub signature_ed25519: String,
    pub repo_url: String,
    pub download_url: String,
    pub install_date: Option<String>,
    pub status: PackageStatus,
    pub is_system: bool,
    pub is_pinned: bool,
    pub install_reason: InstallReason,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PackageDep {
    pub id: String,
    pub min_version: Option<String>,
    pub optional: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum InstallReason {
    /// Diinstall secara eksplisit oleh pengguna
    Manual,
    /// Diinstall sebagai dependensi otomatis
    Auto,
    /// Bagian dari OS base
    System,
}

/// Entry dalam database lokal paket terinstall
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InstalledEntry {
    pub metadata: PackageMetadata,
    pub install_root: String,
    pub files: Vec<String>,
    pub config_files: Vec<String>,
}

// ─────────────────────────────────────────────────────────────────────────────
// 2. REPOSITORY
// ─────────────────────────────────────────────────────────────────────────────

/// Konfigurasi satu repositori paket
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RepoConfig {
    pub name: String,
    pub url: String,
    pub enabled: bool,
    pub priority: i32,
    pub gpg_fingerprint: Option<String>,
    pub channel: RepoChannel,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RepoChannel {
    Stable,
    Beta,
    Nightly,
    Canary,
    ThirdParty(String),
}

impl fmt::Display for RepoChannel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RepoChannel::Stable         => write!(f, "stable"),
            RepoChannel::Beta           => write!(f, "beta"),
            RepoChannel::Nightly        => write!(f, "nightly"),
            RepoChannel::Canary         => write!(f, "canary"),
            RepoChannel::ThirdParty(n)  => write!(f, "third-party:{}", n),
        }
    }
}

/// Index paket dari satu repository
#[derive(Debug, Serialize, Deserialize)]
pub struct RepoIndex {
    pub repo: RepoConfig,
    pub packages: Vec<PackageMetadata>,
    pub generated_at: String,
    pub total_count: usize,
}

// ─────────────────────────────────────────────────────────────────────────────
// 3. PACKAGE DATABASE (Local SQLite)
// ─────────────────────────────────────────────────────────────────────────────

pub struct PackageDb {
    conn: rusqlite::Connection,
}

impl PackageDb {
    pub fn open(path: &str) -> Result<Self, PkgError> {
        let db_path = if std::path::Path::new("/var/lib/daxos/pkg").exists() {
            format!("/var/lib/daxos/pkg/{}", path)
        } else {
            format!("/tmp/daxos_pkg_{}", path)
        };

        let conn = rusqlite::Connection::open(&db_path)
            .map_err(|e| PkgError::DbError(e.to_string()))?;

        let db = Self { conn };
        db.initialize_schema()?;
        Ok(db)
    }

    fn initialize_schema(&self) -> Result<(), PkgError> {
        self.conn.execute_batch(r#"
        CREATE TABLE IF NOT EXISTS packages (
            id              TEXT PRIMARY KEY,
            name            TEXT NOT NULL,
            version         TEXT NOT NULL,
            kind            TEXT NOT NULL DEFAULT 'app',
            description     TEXT NOT NULL DEFAULT '',
            long_description TEXT NOT NULL DEFAULT '',
            author          TEXT NOT NULL DEFAULT '',
            developer_id    TEXT NOT NULL DEFAULT '',
            license         TEXT NOT NULL DEFAULT 'Proprietary',
            categories      TEXT NOT NULL DEFAULT '[]',
            tags            TEXT NOT NULL DEFAULT '[]',
            dependencies    TEXT NOT NULL DEFAULT '[]',
            conflicts       TEXT NOT NULL DEFAULT '[]',
            architectures   TEXT NOT NULL DEFAULT '["x86_64","arm64"]',
            installed_size_bytes INTEGER NOT NULL DEFAULT 0,
            sha3_512        TEXT NOT NULL DEFAULT '',
            signature_ed25519 TEXT NOT NULL DEFAULT '',
            install_root    TEXT NOT NULL DEFAULT '/var/lib/daxos/apps',
            install_date    TEXT,
            install_reason  TEXT NOT NULL DEFAULT 'manual',
            status          TEXT NOT NULL DEFAULT 'installed',
            is_system       INTEGER NOT NULL DEFAULT 0,
            is_pinned       INTEGER NOT NULL DEFAULT 0,
            files_json      TEXT NOT NULL DEFAULT '[]',
            config_files_json TEXT NOT NULL DEFAULT '[]',
            metadata_json   TEXT NOT NULL DEFAULT '{}'
        ) STRICT;

        CREATE TABLE IF NOT EXISTS repos (
            name            TEXT PRIMARY KEY,
            url             TEXT NOT NULL,
            enabled         INTEGER NOT NULL DEFAULT 1,
            priority        INTEGER NOT NULL DEFAULT 50,
            channel         TEXT NOT NULL DEFAULT 'stable',
            gpg_fingerprint TEXT,
            last_updated    TEXT,
            package_count   INTEGER NOT NULL DEFAULT 0
        ) STRICT;

        CREATE TABLE IF NOT EXISTS repo_packages (
            repo_name   TEXT NOT NULL REFERENCES repos(name) ON DELETE CASCADE,
            package_id  TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            PRIMARY KEY (repo_name, package_id)
        ) STRICT;

        CREATE TABLE IF NOT EXISTS hold_list (
            package_id TEXT PRIMARY KEY
        ) STRICT;

        CREATE TABLE IF NOT EXISTS pkg_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            action      TEXT NOT NULL,
            package_id  TEXT NOT NULL,
            from_version TEXT,
            to_version  TEXT,
            timestamp   TEXT NOT NULL DEFAULT (datetime('now')),
            success     INTEGER NOT NULL DEFAULT 1,
            error_msg   TEXT
        ) STRICT;

        CREATE INDEX IF NOT EXISTS idx_packages_name ON packages(name);
        CREATE INDEX IF NOT EXISTS idx_packages_status ON packages(status);
        CREATE INDEX IF NOT EXISTS idx_packages_kind ON packages(kind);
        CREATE INDEX IF NOT EXISTS idx_repo_packages_repo ON repo_packages(repo_name);
        "#).map_err(|e| PkgError::DbError(e.to_string()))?;

        // Seed default repos
        let _ = self.conn.execute(
            "INSERT OR IGNORE INTO repos (name, url, enabled, priority, channel, package_count) 
             VALUES (?1, ?2, 1, 100, 'stable', 0)",
            rusqlite::params![
                "daxos-official",
                "https://dapstore.daxos.org/repo/stable"
            ]
        );
        let _ = self.conn.execute(
            "INSERT OR IGNORE INTO repos (name, url, enabled, priority, channel, package_count) 
             VALUES (?1, ?2, 1, 50, 'beta', 0)",
            rusqlite::params![
                "daxos-beta",
                "https://dapstore.daxos.org/repo/beta"
            ]
        );

        // Seed built-in system packages
        self.seed_system_packages()?;
        Ok(())
    }

    fn seed_system_packages(&self) -> Result<(), PkgError> {
        let count: i64 = self.conn
            .query_row("SELECT COUNT(*) FROM packages WHERE is_system = 1", [], |r| r.get(0))
            .unwrap_or(0);
        if count > 0 { return Ok(()); }

        let system_pkgs = vec![
            ("org.daxos.kernel",       "dxu-hybrid",           "1.10.2026-daxos-hybrid",   "tool",      "DXU Hybrid Kernel",                              "Official DXU Hybrid Kernel architecture with DreX-Boost, NTSync, and dm-verity."),
            ("org.daxos.init",         "daxos-init",           "1.10.2026",               "tool",      "DAXOS Initialization System",                    "Systemd-based init system with DAXOS-specific unit targets."),
            ("org.daxos.compositor",   "drex-compositor",      "1.10.2026",               "framework", "DreX Wayland Compositor (Acrylic Glass)",         "Hyprland-based compositor with real-time glassmorphism blur and tiling."),
            ("org.daxos.registryd",    "dap-registryd",        "1.10.2026",               "tool",      "DAXOS Registry Daemon",                           "Centralized SQLite-backed registry for OS state, drivers, and configurations."),
            ("org.daxos.sandboxd",     "dap-sandboxd",         "1.10.2026",               "tool",      "DAXOS Application Sandbox Daemon",               "Enforces Landlock LSM, Seccomp-BPF, and cgroups v2 isolation for all .dapp packages."),
            ("org.daxos.updated",      "dap-updated",          "1.10.2026",               "tool",      "DAXOS Atomic A/B OTA Updater Daemon",             "Manages atomic OS updates using dual-slot A/B partition switching."),
            ("org.daxos.boostd",       "drex-boostd",          "1.10.2026",               "tool",      "DreX Dynamic Hardware Governor Daemon",           "PID-controlled CPU/GPU frequency governor for smooth 240Hz rendering."),
            ("org.daxos.drexvis",      "drexvis",              "1.10.2026",               "framework", "DreXVIS GPU Driver Abstraction Layer",            "Universal GPU driver framework supporting CUDA, RDNA, Intel Xe, and Vulkan."),
            ("org.daxos.drexui",       "drex-ui",              "1.10.2026",               "framework", "DreXUI Declarative Reactive UI Framework",        "Reactive component tree with @State/@Binding targeting 120–240Hz displays."),
            ("org.daxos.dcodx",        "dcodx",                "1.10.2026",               "tool",      "DCODX Surflang Compiler & Developer Toolchain",  "Full compiler pipeline from Surflang → DreX-HIR → LLVM IR → .dapp fat binary."),
            ("org.daxos.dax-pkg",      "dax",                  "1.10.2026",               "tool",      "DAXOS Package Manager",                           "Native package manager for installing, removing, and upgrading .dapp packages."),
            ("org.daxos.daxsh",        "daxsh",                "1.10.2026",               "tool",      "DAXOS Shell (daxsh)",                             "POSIX-compatible shell with DAXOS-native built-in commands."),
            ("org.daxos.sysmon",       "dax-sysmon",           "1.10.2026",               "tool",      "DAXOS System Monitor Daemon",                    "Real-time CPU, RAM, GPU, disk, and network performance metrics daemon."),
            ("org.daxos.netd",         "dax-netd",             "1.10.2026",               "tool",      "DAXOS Network Manager Daemon",                   "Wi-Fi/Ethernet/DNS management with WPA3 support and network isolation."),
            ("org.daxos.dap-compat",   "dax-run",              "1.10.2026",               "tool",      "DAXOS Universal App Runtime",                    "Binary translation layer for macOS Mach-O, Windows PE, and Debian .deb packages."),
        ];

        for (id, name, ver, kind, desc, long_desc) in &system_pkgs {
            let _ = self.conn.execute(
                "INSERT OR IGNORE INTO packages (id, name, version, kind, description, long_description, is_system, status, install_reason)
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, 1, 'installed', 'system')",
                rusqlite::params![id, name, ver, kind, desc, long_desc]
            );
        }

        // Seed common user apps
        let user_apps = vec![
            ("org.daxos.calculator",  "Calculator",  "2.1.0",   "app",  "DAXOS Calculator",          "Precision arithmetic calculator with expression chaining and unit conversion."),
            ("org.daxos.camera",      "Camera",      "1.5.0",   "app",  "DAXOS Camera",              "True-perspective 1:1 optical rendering camera with RAW DNG capture support."),
            ("org.daxos.terminal",    "Terminal",    "3.0.1",   "app",  "DAXOS Terminal",            "Modern terminal emulator with GPU-accelerated rendering, tabs, and split views."),
            ("org.daxos.files",       "Files",       "2.3.0",   "app",  "Files (Finder)",             "Full-featured file manager with tagging, smart folders, and DaXCloud sync."),
            ("org.daxos.preferences", "Settings",    "1.10.2026","app",  "System Settings",           "Unified system configuration: display, audio, network, privacy, and updates."),
            ("org.daxos.installer",   "Install DAXOS","1.10.2026","app", "DAXOS Installer",           "Interactive system installer with disk partitioning, account setup, and live preview."),
            ("org.daxos.dapstore",    "DapStore",    "1.10.2026","app",  "DapStore — App Store",      "Official DAXOS application store with curated apps, ratings, and instant download."),
            ("org.daxos.dcodx.ide",   "DCODX IDE",  "1.10.2026","app",  "DCODX Developer IDE",       "Multi-target IDE for Surflang, Rust, C++, Python with hot-reload and GPU profiler."),
            ("org.daxos.daxbro",      "DaXBro",     "1.10.2026","app",  "DaXBro Browser",            "Privacy-first WebKit/Blink browser with hardware-accelerated rendering."),
            ("org.daxos.dxdef",       "DXDEF",      "1.10.2026","app",  "DXDEF Security Center",     "Comprehensive security dashboard: firewall, malware scan, and privacy reports."),
        ];

        for (id, name, ver, kind, desc, long_desc) in &user_apps {
            let _ = self.conn.execute(
                "INSERT OR IGNORE INTO packages (id, name, version, kind, description, long_description, is_system, status, install_reason)
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, 0, 'installed', 'manual')",
                rusqlite::params![id, name, ver, kind, desc, long_desc]
            );
        }
        Ok(())
    }

    /// List semua paket yang terinstall
    pub fn list_installed(&self, filter: Option<PackageStatus>) -> Result<Vec<InstalledSummary>, PkgError> {
        let query = match filter {
            Some(status) => format!(
                "SELECT id, name, version, kind, description, status, is_system, is_pinned, install_date, install_reason 
                 FROM packages WHERE status = '{}' ORDER BY is_system DESC, name",
                status
            ),
            None => "SELECT id, name, version, kind, description, status, is_system, is_pinned, install_date, install_reason 
                     FROM packages ORDER BY is_system DESC, name".to_string(),
        };

        let mut stmt = self.conn.prepare(&query)
            .map_err(|e| PkgError::DbError(e.to_string()))?;

        let rows = stmt.query_map([], |row| {
            Ok(InstalledSummary {
                id:             row.get(0)?,
                name:           row.get(1)?,
                version:        row.get(2)?,
                kind:           row.get::<_, String>(3)?,
                description:    row.get(4)?,
                status:         row.get::<_, String>(5)?,
                is_system:      row.get::<_, bool>(6)?,
                is_pinned:      row.get::<_, bool>(7)?,
                install_date:   row.get(8)?,
                install_reason: row.get(9)?,
            })
        }).map_err(|e| PkgError::DbError(e.to_string()))?;

        let mut results = Vec::new();
        for row in rows {
            results.push(row.map_err(|e| PkgError::DbError(e.to_string()))?);
        }
        Ok(results)
    }

    /// Cari paket berdasarkan query (name / description)
    pub fn search(&self, query: &str) -> Result<Vec<InstalledSummary>, PkgError> {
        let pattern = format!("%{}%", query.to_lowercase());
        let mut stmt = self.conn.prepare(
            "SELECT id, name, version, kind, description, status, is_system, is_pinned, install_date, install_reason 
             FROM packages 
             WHERE LOWER(name) LIKE ?1 OR LOWER(description) LIKE ?1 OR LOWER(id) LIKE ?1
             ORDER BY is_system DESC, name"
        ).map_err(|e| PkgError::DbError(e.to_string()))?;

        let rows = stmt.query_map(rusqlite::params![pattern], |row| {
            Ok(InstalledSummary {
                id:             row.get(0)?,
                name:           row.get(1)?,
                version:        row.get(2)?,
                kind:           row.get::<_, String>(3)?,
                description:    row.get(4)?,
                status:         row.get::<_, String>(5)?,
                is_system:      row.get::<_, bool>(6)?,
                is_pinned:      row.get::<_, bool>(7)?,
                install_date:   row.get(8)?,
                install_reason: row.get(9)?,
            })
        }).map_err(|e| PkgError::DbError(e.to_string()))?;

        let mut results = Vec::new();
        for row in rows {
            results.push(row.map_err(|e| PkgError::DbError(e.to_string()))?);
        }
        Ok(results)
    }

    /// Ambil info detail satu paket
    pub fn get_info(&self, id_or_name: &str) -> Result<Option<PackageInfo>, PkgError> {
        let mut stmt = self.conn.prepare(
            "SELECT id, name, version, kind, description, long_description, author, developer_id, 
                    license, categories, dependencies, architectures, installed_size_bytes, 
                    sha3_512, install_date, install_reason, status, is_system, is_pinned, install_root
             FROM packages 
             WHERE id = ?1 OR LOWER(name) = LOWER(?1)
             LIMIT 1"
        ).map_err(|e| PkgError::DbError(e.to_string()))?;

        let result = stmt.query_row(rusqlite::params![id_or_name], |row| {
            Ok(PackageInfo {
                id:             row.get(0)?,
                name:           row.get(1)?,
                version:        row.get(2)?,
                kind:           row.get::<_, String>(3)?,
                description:    row.get(4)?,
                long_description: row.get(5)?,
                author:         row.get::<_, Option<String>>(6)?.unwrap_or_default(),
                developer_id:   row.get::<_, Option<String>>(7)?.unwrap_or_default(),
                license:        row.get::<_, Option<String>>(8)?.unwrap_or_else(|| "Proprietary".to_string()),
                categories:     row.get::<_, Option<String>>(9)?.unwrap_or_else(|| "[]".to_string()),
                dependencies:   row.get::<_, Option<String>>(10)?.unwrap_or_else(|| "[]".to_string()),
                architectures:  row.get::<_, Option<String>>(11)?.unwrap_or_default(),
                installed_size_bytes: row.get::<_, Option<i64>>(12)?.unwrap_or(0) as u64,
                sha3_512:       row.get::<_, Option<String>>(13)?.unwrap_or_default(),
                install_date:   row.get(14)?,
                install_reason: row.get::<_, Option<String>>(15)?.unwrap_or_else(|| "manual".to_string()),
                status:         row.get::<_, Option<String>>(16)?.unwrap_or_else(|| "installed".to_string()),
                is_system:      row.get::<_, bool>(17)?,
                is_pinned:      row.get::<_, bool>(18)?,
                install_root:   row.get::<_, Option<String>>(19)?.unwrap_or_else(|| "/var/lib/daxos/apps".to_string()),
            })
        });

        match result {
            Ok(info) => Ok(Some(info)),
            Err(rusqlite::Error::QueryReturnedNoRows) => Ok(None),
            Err(e) => Err(PkgError::DbError(e.to_string())),
        }
    }

    /// Simulasi install paket (dalam mode aktual akan extract .dapp dan register)
    pub fn install_package(&mut self, meta: &PackageMetadata, reason: InstallReason) -> Result<InstallResult, PkgError> {
        // Cek konflik
        if let Some(conflict) = meta.conflicts.iter().find(|c| {
            self.conn.query_row(
                "SELECT COUNT(*) FROM packages WHERE id = ?1 AND status = 'installed'",
                rusqlite::params![c],
                |r| r.get::<_, i64>(0)
            ).unwrap_or(0) > 0
        }) {
            return Err(PkgError::ConflictError(format!(
                "Paket '{}' berkonflik dengan '{}' yang sudah terinstall", meta.name, conflict
            )));
        }

        // Cek apakah paket di-hold
        let is_held: i64 = self.conn
            .query_row("SELECT COUNT(*) FROM hold_list WHERE package_id = ?1",
                rusqlite::params![meta.id], |r| r.get(0))
            .unwrap_or(0);
        if is_held > 0 {
            return Err(PkgError::HeldError(format!("Paket '{}' sedang di-hold. Gunakan: dax unhold {}", meta.id, meta.id)));
        }

        let reason_str = match reason {
            InstallReason::Manual => "manual",
            InstallReason::Auto   => "auto",
            InstallReason::System => "system",
        };

        let install_date = chrono::Local::now().to_rfc3339();
        let existing: i64 = self.conn
            .query_row("SELECT COUNT(*) FROM packages WHERE id = ?1", rusqlite::params![meta.id], |r| r.get(0))
            .unwrap_or(0);

        if existing > 0 {
            // Update
            self.conn.execute(
                "UPDATE packages SET version = ?1, status = 'installed', install_date = ?2, install_reason = ?3 WHERE id = ?4",
                rusqlite::params![meta.version, install_date, reason_str, meta.id]
            ).map_err(|e| PkgError::DbError(e.to_string()))?;
        } else {
            self.conn.execute(
                "INSERT INTO packages (id, name, version, kind, description, long_description, author, developer_id,
                                       license, installed_size_bytes, sha3_512, status, install_date, install_reason, is_system)
                 VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, 'installed', ?12, ?13, 0)",
                rusqlite::params![
                    meta.id, meta.name, meta.version,
                    meta.kind.to_string(), meta.description, meta.long_description,
                    meta.author, meta.developer_id, meta.license,
                    meta.installed_size_bytes as i64, meta.sha3_512,
                    install_date, reason_str
                ]
            ).map_err(|e| PkgError::DbError(e.to_string()))?;
        }

        // Log history
        let _ = self.conn.execute(
            "INSERT INTO pkg_history (action, package_id, to_version) VALUES ('install', ?1, ?2)",
            rusqlite::params![meta.id, meta.version]
        );

        Ok(InstallResult {
            package_id: meta.id.clone(),
            name: meta.name.clone(),
            version: meta.version.clone(),
            installed_size_bytes: meta.installed_size_bytes,
            deps_installed: 0,
        })
    }

    /// Remove paket
    pub fn remove_package(&mut self, id_or_name: &str, purge: bool) -> Result<RemoveResult, PkgError> {
        // Cek system protection
        let is_system: i64 = self.conn
            .query_row("SELECT COUNT(*) FROM packages WHERE (id = ?1 OR LOWER(name) = LOWER(?1)) AND is_system = 1",
                rusqlite::params![id_or_name], |r| r.get(0))
            .unwrap_or(0);
        if is_system > 0 {
            return Err(PkgError::SystemProtected(format!(
                "Paket '{}' adalah komponen sistem DAXOS dan tidak bisa dihapus", id_or_name
            )));
        }

        let info = self.get_info(id_or_name)?
            .ok_or_else(|| PkgError::NotFound(id_or_name.to_string()))?;

        // Cek apakah paket di-hold
        let is_held: i64 = self.conn
            .query_row("SELECT COUNT(*) FROM hold_list WHERE package_id = ?1",
                rusqlite::params![info.id], |r| r.get(0))
            .unwrap_or(0);
        if is_held > 0 {
            return Err(PkgError::HeldError(format!("Paket '{}' sedang di-hold", info.id)));
        }

        let new_status = if purge { "purged" } else { "removed" };
        self.conn.execute(
            "UPDATE packages SET status = ?1 WHERE id = ?2",
            rusqlite::params![new_status, info.id]
        ).map_err(|e| PkgError::DbError(e.to_string()))?;

        let _ = self.conn.execute(
            "INSERT INTO pkg_history (action, package_id, from_version) VALUES (?1, ?2, ?3)",
            rusqlite::params![new_status, info.id, info.version]
        );

        Ok(RemoveResult {
            package_id: info.id,
            name: info.name,
            purged: purge,
            freed_bytes: info.installed_size_bytes,
        })
    }

    /// Hold paket (cegah upgrade)
    pub fn hold_package(&mut self, id_or_name: &str) -> Result<(), PkgError> {
        let info = self.get_info(id_or_name)?
            .ok_or_else(|| PkgError::NotFound(id_or_name.to_string()))?;
        self.conn.execute("INSERT OR IGNORE INTO hold_list (package_id) VALUES (?1)",
            rusqlite::params![info.id])
            .map_err(|e| PkgError::DbError(e.to_string()))?;
        self.conn.execute("UPDATE packages SET is_pinned = 1 WHERE id = ?1",
            rusqlite::params![info.id])
            .map_err(|e| PkgError::DbError(e.to_string()))?;
        Ok(())
    }

    /// Unhold paket
    pub fn unhold_package(&mut self, id_or_name: &str) -> Result<(), PkgError> {
        let info = self.get_info(id_or_name)?
            .ok_or_else(|| PkgError::NotFound(id_or_name.to_string()))?;
        self.conn.execute("DELETE FROM hold_list WHERE package_id = ?1",
            rusqlite::params![info.id])
            .map_err(|e| PkgError::DbError(e.to_string()))?;
        self.conn.execute("UPDATE packages SET is_pinned = 0 WHERE id = ?1",
            rusqlite::params![info.id])
            .map_err(|e| PkgError::DbError(e.to_string()))?;
        Ok(())
    }

    /// Statistik database paket
    pub fn statistics(&self) -> PkgStats {
        let total: i64 = self.conn.query_row("SELECT COUNT(*) FROM packages", [], |r| r.get(0)).unwrap_or(0);
        let installed: i64 = self.conn.query_row("SELECT COUNT(*) FROM packages WHERE status = 'installed'", [], |r| r.get(0)).unwrap_or(0);
        let system_pkgs: i64 = self.conn.query_row("SELECT COUNT(*) FROM packages WHERE is_system = 1", [], |r| r.get(0)).unwrap_or(0);
        let user_pkgs: i64 = self.conn.query_row("SELECT COUNT(*) FROM packages WHERE is_system = 0 AND status = 'installed'", [], |r| r.get(0)).unwrap_or(0);
        let held: i64 = self.conn.query_row("SELECT COUNT(*) FROM hold_list", [], |r| r.get(0)).unwrap_or(0);
        let total_size: i64 = self.conn.query_row("SELECT COALESCE(SUM(installed_size_bytes), 0) FROM packages WHERE status = 'installed'", [], |r| r.get(0)).unwrap_or(0);
        let repos: i64 = self.conn.query_row("SELECT COUNT(*) FROM repos WHERE enabled = 1", [], |r| r.get(0)).unwrap_or(0);

        PkgStats { total, installed, system_pkgs, user_pkgs, held, total_size_bytes: total_size as u64, active_repos: repos }
    }

    /// List repos yang terdaftar
    pub fn list_repos(&self) -> Vec<RepoSummary> {
        let mut stmt = match self.conn.prepare(
            "SELECT name, url, enabled, priority, channel, last_updated, package_count FROM repos ORDER BY priority DESC"
        ) {
            Ok(s) => s,
            Err(_) => return vec![],
        };

        let rows = stmt.query_map([], |row| {
            Ok(RepoSummary {
                name:          row.get(0)?,
                url:           row.get(1)?,
                enabled:       row.get(2)?,
                priority:      row.get(3)?,
                channel:       row.get(4)?,
                last_updated:  row.get(5)?,
                package_count: row.get(6)?,
            })
        });

        rows.map(|iter| iter.filter_map(|r| r.ok()).collect())
            .unwrap_or_default()
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// 4. VIEW TYPES
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug)]
pub struct InstalledSummary {
    pub id:             String,
    pub name:           String,
    pub version:        String,
    pub kind:           String,
    pub description:    String,
    pub status:         String,
    pub is_system:      bool,
    pub is_pinned:      bool,
    pub install_date:   Option<String>,
    pub install_reason: String,
}

#[derive(Debug)]
pub struct PackageInfo {
    pub id:             String,
    pub name:           String,
    pub version:        String,
    pub kind:           String,
    pub description:    String,
    pub long_description: String,
    pub author:         String,
    pub developer_id:   String,
    pub license:        String,
    pub categories:     String,
    pub dependencies:   String,
    pub architectures:  String,
    pub installed_size_bytes: u64,
    pub sha3_512:       String,
    pub install_date:   Option<String>,
    pub install_reason: String,
    pub status:         String,
    pub is_system:      bool,
    pub is_pinned:      bool,
    pub install_root:   String,
}

#[derive(Debug)]
pub struct InstallResult {
    pub package_id: String,
    pub name:       String,
    pub version:    String,
    pub installed_size_bytes: u64,
    pub deps_installed: u32,
}

#[derive(Debug)]
pub struct RemoveResult {
    pub package_id: String,
    pub name:       String,
    pub purged:     bool,
    pub freed_bytes: u64,
}

#[derive(Debug)]
pub struct PkgStats {
    pub total:          i64,
    pub installed:      i64,
    pub system_pkgs:    i64,
    pub user_pkgs:      i64,
    pub held:           i64,
    pub total_size_bytes: u64,
    pub active_repos:   i64,
}

#[derive(Debug)]
pub struct RepoSummary {
    pub name:          String,
    pub url:           String,
    pub enabled:       bool,
    pub priority:      i64,
    pub channel:       String,
    pub last_updated:  Option<String>,
    pub package_count: i64,
}

// ─────────────────────────────────────────────────────────────────────────────
// 5. ERRORS
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug)]
pub enum PkgError {
    DbError(String),
    NotFound(String),
    AlreadyInstalled(String),
    DependencyError(String),
    ConflictError(String),
    HeldError(String),
    SystemProtected(String),
    VerificationError(String),
    NetworkError(String),
    IoError(String),
}

impl fmt::Display for PkgError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PkgError::DbError(s)         => write!(f, "Database error: {}", s),
            PkgError::NotFound(s)        => write!(f, "Package not found: '{}'", s),
            PkgError::AlreadyInstalled(s)=> write!(f, "Package already installed: '{}'", s),
            PkgError::DependencyError(s) => write!(f, "Dependency resolution failed: {}", s),
            PkgError::ConflictError(s)   => write!(f, "Package conflict: {}", s),
            PkgError::HeldError(s)       => write!(f, "Hold violation: {}", s),
            PkgError::SystemProtected(s) => write!(f, "System protection: {}", s),
            PkgError::VerificationError(s)=> write!(f, "Verification failed: {}", s),
            PkgError::NetworkError(s)    => write!(f, "Network error: {}", s),
            PkgError::IoError(s)         => write!(f, "I/O error: {}", s),
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// 6. HELPER UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

pub fn format_size(bytes: u64) -> String {
    if bytes < 1024 { return format!("{} B", bytes); }
    if bytes < 1024 * 1024 { return format!("{:.1} KB", bytes as f64 / 1024.0); }
    if bytes < 1024 * 1024 * 1024 { return format!("{:.1} MB", bytes as f64 / (1024.0 * 1024.0)); }
    format!("{:.2} GB", bytes as f64 / (1024.0 * 1024.0 * 1024.0))
}

pub fn kind_icon(kind: &str) -> &'static str {
    match kind {
        "app"       => "[APP]",
        "lib"       => "[LIB]",
        "tool"      => "[TOOL]",
        "framework" => "[FRWK]",
        "asset"     => "[ASSET]",
        "firmware"  => "[FIRM]",
        _           => "[OTHER]",
    }
}

pub fn status_indicator(status: &str, is_pinned: bool, is_system: bool) -> String {
    let mut flags = String::new();
    if is_system { flags.push_str("[SYS]"); }
    if is_pinned { flags.push_str("[HELD]"); }
    let state = match status {
        "installed"  => "[OK]",
        "removed"    => "[RM]",
        "purged"     => "[PURGED]",
        _            => "[--]",
    };
    if flags.is_empty() { state.to_string() } else { format!("{} {}", state, flags) }
}

// ─────────────────────────────────────────────────────────────────────────────
// 7. TESTS
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    fn open_test_db() -> PackageDb {
        std::env::set_var("HOME", "/tmp");
        PackageDb::open("test_pkg.db").expect("DB should open")
    }

    #[test]
    fn test_db_initializes_with_system_packages() {
        let db = open_test_db();
        let stats = db.statistics();
        assert!(stats.system_pkgs >= 10, "Should have at least 10 system packages seeded, got {}", stats.system_pkgs);
        assert!(stats.installed >= 15, "Should have at least 15 packages installed");
    }

    #[test]
    fn test_list_and_search() {
        let db = open_test_db();
        let all = db.list_installed(None).expect("list_installed failed");
        assert!(!all.is_empty(), "Package list should not be empty");

        let found = db.search("compositor").expect("search failed");
        assert!(!found.is_empty(), "Should find compositor package");

        let found2 = db.search("calculator").expect("search failed");
        assert!(!found2.is_empty(), "Should find Calculator");
    }

    #[test]
    fn test_package_info() {
        let db = open_test_db();
        let info = db.get_info("org.daxos.kernel").expect("get_info failed");
        assert!(info.is_some(), "Kernel package should exist");
        let pkg = info.unwrap();
        assert_eq!(pkg.is_system, true);
        assert!(pkg.version.contains("daxos") || pkg.version.contains("hybrid"));
    }

    #[test]
    fn test_install_and_remove_user_package() {
        let mut db = open_test_db();

        let meta = PackageMetadata {
            id: "org.test.hello-world".to_string(),
            name: "Hello World Test".to_string(),
            version: "1.0.0".to_string(),
            kind: PackageKind::Application,
            description: "Test app for dax unit tests".to_string(),
            long_description: "A test application used in automated testing.".to_string(),
            author: "DAXOS Test Suite".to_string(),
            developer_id: "test.daxos.org".to_string(),
            homepage: "https://daxos.org".to_string(),
            license: "MIT".to_string(),
            categories: vec!["Test".to_string()],
            tags: vec!["test".to_string()],
            dependencies: vec![],
            conflicts: vec![],
            replaces: vec![],
            provides: vec![],
            min_os_version: "1.0.0".to_string(),
            architectures: vec!["x86_64".to_string(), "arm64".to_string()],
            installed_size_bytes: 1024 * 512,
            download_size_bytes: 1024 * 256,
            sha3_512: "abc123".to_string(),
            signature_ed25519: "sig123".to_string(),
            repo_url: "https://dapstore.daxos.org".to_string(),
            download_url: "https://dapstore.daxos.org/dl/hello-world.dapp".to_string(),
            install_date: None,
            status: PackageStatus::Available,
            is_system: false,
            is_pinned: false,
            install_reason: InstallReason::Manual,
        };

        let result = db.install_package(&meta, InstallReason::Manual);
        assert!(result.is_ok(), "Install should succeed: {:?}", result);

        let info = db.get_info("org.test.hello-world").expect("get_info failed");
        assert!(info.is_some(), "Package should exist after install");
        assert_eq!(info.unwrap().status, "installed");

        let rm = db.remove_package("org.test.hello-world", false);
        assert!(rm.is_ok(), "Remove should succeed: {:?}", rm);
    }

    #[test]
    fn test_system_package_cannot_be_removed() {
        let mut db = open_test_db();
        let result = db.remove_package("org.daxos.kernel", false);
        assert!(result.is_err(), "System package should be protected from removal");
        match result {
            Err(PkgError::SystemProtected(_)) => {}
            Err(e) => panic!("Expected SystemProtected, got {:?}", e),
            Ok(_) => panic!("Should have failed"),
        }
    }

    #[test]
    fn test_hold_prevents_removal() {
        let mut db = open_test_db();

        // Install test app
        let meta = PackageMetadata {
            id: "org.test.holdtest".to_string(),
            name: "Hold Test App".to_string(),
            version: "1.0.0".to_string(),
            kind: PackageKind::Application,
            description: "Test hold functionality".to_string(),
            long_description: String::new(),
            author: String::new(), developer_id: String::new(), homepage: String::new(),
            license: "MIT".to_string(), categories: vec![], tags: vec![],
            dependencies: vec![], conflicts: vec![], replaces: vec![], provides: vec![],
            min_os_version: "1.0.0".to_string(), architectures: vec![],
            installed_size_bytes: 0, download_size_bytes: 0,
            sha3_512: String::new(), signature_ed25519: String::new(),
            repo_url: String::new(), download_url: String::new(), install_date: None,
            status: PackageStatus::Available, is_system: false, is_pinned: false,
            install_reason: InstallReason::Manual,
        };
        let _ = db.install_package(&meta, InstallReason::Manual);

        db.hold_package("org.test.holdtest").expect("hold failed");
        let result = db.remove_package("org.test.holdtest", false);
        assert!(matches!(result, Err(PkgError::HeldError(_))));

        db.unhold_package("org.test.holdtest").expect("unhold failed");
        let result = db.remove_package("org.test.holdtest", false);
        assert!(result.is_ok(), "Should remove after unhold");
    }

    #[test]
    fn test_format_size() {
        assert_eq!(format_size(512), "512 B");
        assert_eq!(format_size(1536), "1.5 KB");
        assert_eq!(format_size(5 * 1024 * 1024), "5.0 MB");
    }
}
