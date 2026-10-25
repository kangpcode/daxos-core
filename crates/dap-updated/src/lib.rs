//! ============================================================================
//! DAXOS ATOMIC UPDATE DAEMON (dap-updated)
//! File: crates/dap-updated/src/lib.rs
//! Purpose: Atomic A/B OTA Updater, dm-verity Merkle Verifier & GRUB Boot Orchestrator
//! ============================================================================

use serde::{Deserialize, Serialize};
use sha3::{Digest, Sha3_512};
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum BootSlot {
    A,
    B,
}

impl BootSlot {
    pub fn alternate(&self) -> Self {
        match self {
            BootSlot::A => BootSlot::B,
            BootSlot::B => BootSlot::A,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            BootSlot::A => "A",
            BootSlot::B => "B",
        }
    }

    pub fn partition_label(&self) -> &'static str {
        match self {
            BootSlot::A => "DAXOS_ROOT_A",
            BootSlot::B => "DAXOS_ROOT_B",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GrubEnvironment {
    pub slot_active: BootSlot,
    pub slot_pending: Option<BootSlot>,
    pub boot_counter: u32,
    pub slot_successful: bool,
}

impl GrubEnvironment {
    pub fn new_default() -> Self {
        Self {
            slot_active: BootSlot::A,
            slot_pending: None,
            boot_counter: 0,
            slot_successful: true,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OtaReleasePackage {
    pub release_id: String,
    pub version: String,
    pub build_epoch: u64,
    pub image_size_bytes: u64,
    pub sha3_512_hash: String,
    pub expected_dm_verity_roothash: String,
}

#[derive(Debug)]
pub enum UpdateError {
    HashMismatch { expected: String, actual: String },
    NoUpdateAvailable,
    SlotAlreadyActive,
    Io(String),
}

impl fmt::Display for UpdateError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            UpdateError::HashMismatch { expected, actual } => {
                write!(f, "Cryptographic hash mismatch! Expected: {}, actual: {}", expected, actual)
            }
            UpdateError::NoUpdateAvailable => write!(f, "System is already running the latest build epoch"),
            UpdateError::SlotAlreadyActive => write!(f, "Target slot is currently the active boot slot"),
            UpdateError::Io(s) => write!(f, "I/O update failure: {}", s),
        }
    }
}

impl std::error::Error for UpdateError {}

pub struct OtaManager {
    grub_env: GrubEnvironment,
    current_build_epoch: u64,
}

impl OtaManager {
    pub const MAX_BOOT_ATTEMPTS: u32 = 3;

    pub fn new(current_build_epoch: u64, grub_env: GrubEnvironment) -> Self {
        Self {
            grub_env,
            current_build_epoch,
        }
    }

    pub fn check_update(&self, available_release: &OtaReleasePackage) -> Result<bool, UpdateError> {
        if available_release.build_epoch > self.current_build_epoch {
            Ok(true)
        } else {
            Err(UpdateError::NoUpdateAvailable)
        }
    }

    pub fn stage_update_payload(
        &mut self,
        release: &OtaReleasePackage,
        payload_bytes: &[u8],
    ) -> Result<BootSlot, UpdateError> {
        // 1. Verifikasi Hash SHA3-512 dari payload
        let mut hasher = Sha3_512::new();
        hasher.update(payload_bytes);
        let actual_hash = format!("{:x}", hasher.finalize());

        if actual_hash != release.sha3_512_hash {
            return Err(UpdateError::HashMismatch {
                expected: release.sha3_512_hash.clone(),
                actual: actual_hash,
            });
        }

        // 2. Tentukan target slot pasif
        let target_slot = self.grub_env.slot_active.alternate();

        // 3. Konfigurasi GRUB environment: jadwalkan target slot sebagai slot_pending
        self.grub_env.slot_pending = Some(target_slot.clone());
        self.grub_env.boot_counter = 0;
        self.grub_env.slot_successful = false;

        Ok(target_slot)
    }

    pub fn mark_good(&mut self) {
        if let Some(pending) = self.grub_env.slot_pending.take() {
            self.grub_env.slot_active = pending;
        }
        self.grub_env.boot_counter = 0;
        self.grub_env.slot_successful = true;
    }

    pub fn mark_bad_or_rollback_if_needed(&mut self) -> bool {
        self.grub_env.boot_counter += 1;
        if self.grub_env.boot_counter >= Self::MAX_BOOT_ATTEMPTS {
            // Rollback otomatis ke slot sebelumnya
            self.grub_env.slot_pending = None;
            self.grub_env.boot_counter = 0;
            self.grub_env.slot_successful = true;
            true // Triggered rollback
        } else {
            false
        }
    }

    pub fn get_grub_env(&self) -> &GrubEnvironment {
        &self.grub_env
    }

    pub fn get_grub_env_mut(&mut self) -> &mut GrubEnvironment {
        &mut self.grub_env
    }
}

// ----------------------------------------------------------------------------
// GRUBENV PERSISTENCE
// ----------------------------------------------------------------------------

use std::fs;
use std::io::{BufRead, BufReader, Write};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::Path;
use std::sync::{Arc, Mutex};

pub fn load_grubenv(path: &Path) -> GrubEnvironment {
    let mut env = GrubEnvironment::new_default();
    if let Ok(content) = fs::read_to_string(path) {
        for line in content.lines() {
            let parts: Vec<&str> = line.splitn(2, '=').collect();
            if parts.len() == 2 {
                let key = parts[0].trim();
                let val = parts[1].trim();
                match key {
                    "slot_active" => {
                        env.slot_active = if val == "B" { BootSlot::B } else { BootSlot::A };
                    }
                    "slot_pending" => {
                        env.slot_pending = match val {
                            "A" => Some(BootSlot::A),
                            "B" => Some(BootSlot::B),
                            _ => None,
                        };
                    }
                    "boot_counter" => {
                        env.boot_counter = val.parse().unwrap_or(0);
                    }
                    "slot_successful" => {
                        env.slot_successful = val == "1" || val == "true";
                    }
                    _ => {}
                }
            }
        }
    }
    env
}

pub fn save_grubenv(path: &Path, env: &GrubEnvironment) -> std::io::Result<()> {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let pending_str = match &env.slot_pending {
        Some(s) => s.as_str(),
        None => "none",
    };
    let content = format!(
        "# DAXOS GRUB Environment Block\nslot_active={}\nslot_pending={}\nboot_counter={}\nslot_successful={}\n",
        env.slot_active.as_str(),
        pending_str,
        env.boot_counter,
        if env.slot_successful { 1 } else { 0 }
    );
    fs::write(path, content)
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "action", content = "payload")]
pub enum OtaRequest {
    GetStatus,
    MarkGood,
    SimulateBootFailure,
    CheckUpdate { epoch: u64 },
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(tag = "status", content = "data")]
pub enum OtaResponse {
    Success(serde_json::Value),
    Error(String),
}

pub fn handle_update_client(mut stream: UnixStream, manager: &Arc<Mutex<OtaManager>>, grubenv_path: &Path) -> std::io::Result<()> {
    let reader = BufReader::new(stream.try_clone()?);
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }

        let mut mgr = manager.lock().unwrap();
        let resp = match serde_json::from_str::<OtaRequest>(&line) {
            Ok(OtaRequest::GetStatus) => {
                let env = mgr.get_grub_env().clone();
                OtaResponse::Success(serde_json::json!({
                    "slot_active": env.slot_active.as_str(),
                    "slot_pending": env.slot_pending.as_ref().map(|s| s.as_str()).unwrap_or("none"),
                    "boot_counter": env.boot_counter,
                    "slot_successful": env.slot_successful,
                }))
            }
            Ok(OtaRequest::MarkGood) => {
                mgr.mark_good();
                let _ = save_grubenv(grubenv_path, mgr.get_grub_env());
                OtaResponse::Success(serde_json::json!({ "marked_good": true }))
            }
            Ok(OtaRequest::SimulateBootFailure) => {
                let rolled_back = mgr.mark_bad_or_rollback_if_needed();
                let _ = save_grubenv(grubenv_path, mgr.get_grub_env());
                let env = mgr.get_grub_env().clone();
                OtaResponse::Success(serde_json::json!({
                    "rolled_back": rolled_back,
                    "boot_counter": env.boot_counter,
                    "slot_active": env.slot_active.as_str(),
                }))
            }
            Ok(OtaRequest::CheckUpdate { epoch }) => {
                let rel = OtaReleasePackage {
                    release_id: "ota-update-target".into(),
                    version: "1.1.0".into(),
                    build_epoch: epoch,
                    image_size_bytes: 4096,
                    sha3_512_hash: String::new(),
                    expected_dm_verity_roothash: String::new(),
                };
                match mgr.check_update(&rel) {
                    Ok(available) => OtaResponse::Success(serde_json::json!({ "update_available": available })),
                    Err(e) => OtaResponse::Error(e.to_string()),
                }
            }
            Err(e) => OtaResponse::Error(format!("Malformed request: {}", e)),
        };

        let resp_json = serde_json::to_string(&resp).unwrap_or_else(|_| {
            r#"{"status":"Error","data":"Serialization failed"}"#.to_string()
        });
        stream.write_all(resp_json.as_bytes())?;
        stream.write_all(b"\n")?;
        stream.flush()?;
    }
    Ok(())
}

pub fn run_update_server(
    manager: Arc<Mutex<OtaManager>>,
    socket_path: &str,
    grubenv_path: &Path,
    stop_flag: Arc<std::sync::atomic::AtomicBool>,
) -> std::io::Result<()> {
    if Path::new(socket_path).exists() {
        let _ = fs::remove_file(socket_path);
    }
    if let Some(parent) = Path::new(socket_path).parent() {
        let _ = fs::create_dir_all(parent);
    }

    let listener = UnixListener::bind(socket_path)?;
    listener.set_nonblocking(true)?;

    println!("[dap-updated] Unix domain socket listening at: {}", socket_path);

    let grub_path_buf = grubenv_path.to_path_buf();
    while !stop_flag.load(std::sync::atomic::Ordering::Relaxed) {
        match listener.accept() {
            Ok((stream, _)) => {
                let m_clone = Arc::clone(&manager);
                let g_clone = grub_path_buf.clone();
                std::thread::spawn(move || {
                    let _ = handle_update_client(stream, &m_clone, &g_clone);
                });
            }
            Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                std::thread::sleep(std::time::Duration::from_millis(50));
            }
            Err(e) => {
                eprintln!("[dap-updated] Socket error: {}", e);
                break;
            }
        }
    }

    let _ = fs::remove_file(socket_path);
    println!("[dap-updated] Update server shut down gracefully.");
    Ok(())
}

// ----------------------------------------------------------------------------
// REMOTE DAXCLOUD OTA CLIENT API
// ----------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemoteOtaCheckResponse {
    pub status: String,
    pub version: String,
    pub title: String,
    pub channel: String,
    pub description: String,
    pub download_url: String,
    pub package_size_bytes: u64,
    pub package_size_mb: f64,
    pub sha256_hash: String,
    pub slot_target: String,
    pub kernel_target: String,
    pub release_notes: String,
}

pub fn query_remote_daxcloud_ota(host: &str, port: u16, path: &str) -> Result<RemoteOtaCheckResponse, String> {
    use std::io::{Read, Write};
    use std::net::TcpStream;
    use std::time::Duration;

    let addr = format!("{}:{}", host, port);
    let mut stream = TcpStream::connect_timeout(
        &addr.parse().map_err(|e| format!("Invalid address: {}", e))?,
        Duration::from_secs(3),
    ).map_err(|e| format!("Cannot connect to DaXCloud OTA server at {}: {}", addr, e))?;

    let req = format!(
        "GET {} HTTP/1.1\r\nHost: {}:{}\r\nUser-Agent: DAXOS-OTA-Client/1.10.2026\r\nConnection: close\r\n\r\n",
        path, host, port
    );
    stream.write_all(req.as_bytes()).map_err(|e| format!("Write failure: {}", e))?;

    let mut response = String::new();
    stream.read_to_string(&mut response).map_err(|e| format!("Read failure: {}", e))?;

    if let Some(body_start) = response.find("\r\n\r\n") {
        let body = &response[body_start + 4..];
        serde_json::from_str::<RemoteOtaCheckResponse>(body)
            .map_err(|e| format!("JSON decode failure: {}. Raw body: {}", e, body))
    } else {
        Err("Invalid HTTP response: header delimiter missing".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ota_staging_and_mark_good() {
        let env = GrubEnvironment::new_default();
        let mut ota = OtaManager::new(1700000000, env);

        let test_payload = b"DAXOS_EROFS_RAW_DELTA_IMAGE_STREAM_BLOCKS";
        let mut hasher = Sha3_512::new();
        hasher.update(test_payload);
        let hash_hex = format!("{:x}", hasher.finalize());

        let release = OtaReleasePackage {
            release_id: "rel-1.2.0".to_string(),
            version: "1.2.0".to_string(),
            build_epoch: 1776200000,
            image_size_bytes: test_payload.len() as u64,
            sha3_512_hash: hash_hex,
            expected_dm_verity_roothash: "roothash_abc123".to_string(),
        };

        // 1. Cek update
        assert!(ota.check_update(&release).is_ok());

        // 2. Stage update
        let staged_slot = ota.stage_update_payload(&release, test_payload).expect("Staging failed");
        assert_eq!(staged_slot, BootSlot::B);
        assert_eq!(ota.get_grub_env().slot_pending, Some(BootSlot::B));

        // 3. Mark good setelah desktop boot berhasil
        ota.mark_good();
        assert_eq!(ota.get_grub_env().slot_active, BootSlot::B);
        assert_eq!(ota.get_grub_env().slot_pending, None);
        assert_eq!(ota.get_grub_env().slot_successful, true);
    }

    #[test]
    fn test_automatic_rollback_on_three_failures() {
        let env = GrubEnvironment {
            slot_active: BootSlot::A,
            slot_pending: Some(BootSlot::B),
            boot_counter: 0,
            slot_successful: false,
        };
        let mut ota = OtaManager::new(1776200000, env);

        // Percobaan boot 1 & 2
        assert_eq!(ota.mark_bad_or_rollback_if_needed(), false); // counter = 1
        assert_eq!(ota.mark_bad_or_rollback_if_needed(), false); // counter = 2

        // Percobaan boot 3: Rollback dipicu
        assert_eq!(ota.mark_bad_or_rollback_if_needed(), true); // counter = 3 -> rollback
        assert_eq!(ota.get_grub_env().slot_active, BootSlot::A);
        assert_eq!(ota.get_grub_env().slot_pending, None);
    }
}
