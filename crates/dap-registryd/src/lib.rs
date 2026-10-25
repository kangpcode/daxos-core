//! ============================================================================
//! DAXOS REGISTRY DAEMON (dap-registryd)
//! File: crates/dap-registryd/src/lib.rs
//! Purpose: Central SQLite WAL State & IPC Service for OS Subsystems
//! ============================================================================

use rusqlite::{params, Connection};
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};

pub const SCHEMA_SQL: &str = include_str!("../../../schema/daxos_registry.sql");

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "action", content = "payload")]
pub enum RegistryRequest {
    GetConfig { key: String },
    SetConfig { key: String, value: String },
    GetActiveBootSlot,
    SetActiveBootSlot { slot_id: String },
    UpdateGlassProfile {
        user_id: String,
        opacity: f64,
        blur_radius: i64,
        edge_brightness: f64,
        noise_intensity: f64,
    },
    RecordDriverRecovery {
        driver_id: String,
        exit_signal: i32,
        duration_ms: i64,
        status: String,
    },
    QueryLatestOtaRelease { channel: String, arch: String },
    CheckSandboxPermission {
        bundle_id: String,
        permission_code: String,
    },
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(tag = "status", content = "data")]
pub enum RegistryResponse {
    Success(serde_json::Value),
    Error(String),
}

pub struct RegistryService {
    conn: Arc<Mutex<Connection>>,
}

impl RegistryService {
    pub fn new_in_memory() -> Result<Self, rusqlite::Error> {
        let conn = Connection::open_in_memory()?;
        conn.execute_batch("PRAGMA foreign_keys = ON;")?;
        conn.execute_batch(SCHEMA_SQL)?;
        Ok(Self {
            conn: Arc::new(Mutex::new(conn)),
        })
    }

    pub fn new_from_path(db_path: &str) -> Result<Self, rusqlite::Error> {
        let conn = Connection::open(db_path)?;
        conn.execute_batch("PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;")?;
        
        // Cek jika tabel kosong, bootstrap dengan SCHEMA_SQL
        let count: i64 = conn
            .query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='system_nodes';",
                [],
                |row| row.get(0),
            )
            .unwrap_or(0);

        if count == 0 {
            conn.execute_batch(SCHEMA_SQL)?;
        }

        Ok(Self {
            conn: Arc::new(Mutex::new(conn)),
        })
    }

    pub fn handle_request(&self, request: RegistryRequest) -> RegistryResponse {
        let conn = self.conn.lock().unwrap();

        match request {
            RegistryRequest::GetConfig { key } => {
                let res: Result<String, _> = conn.query_row(
                    "SELECT config_value FROM system_configurations WHERE config_key = ?1",
                    params![key],
                    |row| row.get(0),
                );
                match res {
                    Ok(val) => RegistryResponse::Success(serde_json::json!({ "value": val })),
                    Err(e) => RegistryResponse::Error(format!("Config not found: {}", e)),
                }
            }
            RegistryRequest::SetConfig { key, value } => {
                let res = conn.execute(
                    "UPDATE system_configurations SET config_value = ?1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE config_key = ?2",
                    params![value, key],
                );
                match res {
                    Ok(rows) if rows > 0 => RegistryResponse::Success(serde_json::json!({ "updated": true })),
                    Ok(_) => RegistryResponse::Error(format!("Config key '{}' not found", key)),
                    Err(e) => RegistryResponse::Error(e.to_string()),
                }
            }
            RegistryRequest::GetActiveBootSlot => {
                let res: Result<(String, String, i64), _> = conn.query_row(
                    "SELECT slot_id, partition_label, boot_counter FROM bootloader_slots WHERE is_active = 1 LIMIT 1",
                    [],
                    |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?)),
                );
                match res {
                    Ok((slot, part, counter)) => RegistryResponse::Success(serde_json::json!({
                        "slot_id": slot,
                        "partition_label": part,
                        "boot_counter": counter,
                    })),
                    Err(e) => RegistryResponse::Error(format!("Active slot not found: {}", e)),
                }
            }
            RegistryRequest::SetActiveBootSlot { slot_id } => {
                let tx_res = conn.execute_batch(&format!(
                    "UPDATE bootloader_slots SET is_active = 0 WHERE slot_id != '{0}';
                     UPDATE bootloader_slots SET is_active = 1, last_boot_timestamp = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE slot_id = '{0}';",
                    slot_id
                ));
                match tx_res {
                    Ok(_) => RegistryResponse::Success(serde_json::json!({ "active_slot": slot_id })),
                    Err(e) => RegistryResponse::Error(e.to_string()),
                }
            }
            RegistryRequest::UpdateGlassProfile { user_id, opacity, blur_radius, edge_brightness, noise_intensity } => {
                let res = conn.execute(
                    "UPDATE visual_glass_profiles 
                     SET opacity = ?1, blur_radius_px = ?2, edge_brightness = ?3, noise_intensity = ?4, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                     WHERE user_id = ?5 AND is_active = 1",
                    params![opacity, blur_radius, edge_brightness, noise_intensity, user_id],
                );
                match res {
                    Ok(rows) if rows > 0 => RegistryResponse::Success(serde_json::json!({ "synced": true })),
                    Ok(_) => RegistryResponse::Error("Active profile not found for user".to_string()),
                    Err(e) => RegistryResponse::Error(e.to_string()),
                }
            }
            RegistryRequest::RecordDriverRecovery { driver_id, exit_signal, duration_ms, status } => {
                let log_id = format!("rec-{}", std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_millis());
                let res = conn.execute(
                    "INSERT INTO driver_recovery_logs (log_id, driver_id, exit_signal, recovery_duration_ms, recovery_status)
                     VALUES (?1, ?2, ?3, ?4, ?5)",
                    params![log_id, driver_id, exit_signal, duration_ms, status],
                );
                match res {
                    Ok(_) => RegistryResponse::Success(serde_json::json!({ "logged_id": log_id })),
                    Err(e) => RegistryResponse::Error(e.to_string()),
                }
            }
            RegistryRequest::QueryLatestOtaRelease { channel, arch } => {
                let res: Result<(String, String, i64, i64), _> = conn.query_row(
                    "SELECT r.release_id, r.version_semver, r.build_epoch, r.image_size_bytes
                     FROM ota_releases r
                     JOIN ota_channels c ON r.channel_id = c.channel_id
                     WHERE c.channel_id = ?1 AND r.target_architecture = ?2
                     ORDER BY r.build_epoch DESC LIMIT 1",
                    params![channel, arch],
                    |row| Ok((row.get(0)?, row.get(1)?, row.get(2)?, row.get(3)?)),
                );
                match res {
                    Ok((rel_id, ver, epoch, size)) => RegistryResponse::Success(serde_json::json!({
                        "release_id": rel_id,
                        "version": ver,
                        "build_epoch": epoch,
                        "size_bytes": size,
                    })),
                    Err(e) => RegistryResponse::Error(format!("No release found: {}", e)),
                }
            }
            RegistryRequest::CheckSandboxPermission { bundle_id, permission_code } => {
                let res: Result<String, _> = conn.query_row(
                    "SELECT g.grant_status
                     FROM applications a
                     JOIN sandbox_grants g ON a.app_id = g.app_id
                     JOIN sandbox_permissions p ON g.permission_id = p.permission_id
                     WHERE a.bundle_identifier = ?1 AND p.permission_code = ?2",
                    params![bundle_id, permission_code],
                    |row| row.get(0),
                );
                match res {
                    Ok(status) => RegistryResponse::Success(serde_json::json!({ "grant_status": status })),
                    Err(_) => RegistryResponse::Success(serde_json::json!({ "grant_status": "denied" })),
                }
            }
        }
    }

    pub fn get_statistics(&self) -> Result<serde_json::Value, rusqlite::Error> {
        let conn = self.conn.lock().unwrap();
        let nodes: i64 = conn.query_row("SELECT COUNT(*) FROM system_nodes", [], |r| r.get(0))?;
        let slots: i64 = conn.query_row("SELECT COUNT(*) FROM bootloader_slots", [], |r| r.get(0))?;
        let drivers: i64 = conn.query_row("SELECT COUNT(*) FROM drivers", [], |r| r.get(0))?;
        let apps: i64 = conn.query_row("SELECT COUNT(*) FROM applications", [], |r| r.get(0))?;
        let active_slot: String = conn.query_row(
            "SELECT slot_id FROM bootloader_slots WHERE is_active = 1 LIMIT 1",
            [],
            |r| r.get(0),
        ).unwrap_or_else(|_| "Unknown".to_string());

        Ok(serde_json::json!({
            "nodes_count": nodes,
            "boot_slots_count": slots,
            "drivers_count": drivers,
            "applications_count": apps,
            "active_boot_slot": active_slot,
        }))
    }
}

// ----------------------------------------------------------------------------
// IPC NETWORKING & CLIENT INTERFACE
// ----------------------------------------------------------------------------

use std::io::{BufRead, BufReader, Write};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::Path;

pub struct RegistryClient {
    pub socket_path: String,
}

impl RegistryClient {
    pub fn new(socket_path: impl Into<String>) -> Self {
        Self { socket_path: socket_path.into() }
    }

    pub fn send(&self, req: &RegistryRequest) -> Result<RegistryResponse, String> {
        let mut stream = UnixStream::connect(&self.socket_path)
            .map_err(|e| format!("Failed to connect to registry socket at {}: {}", self.socket_path, e))?;
        let json_line = serde_json::to_string(req)
            .map_err(|e| format!("Failed to serialize request: {}", e))?;
        stream.write_all(json_line.as_bytes())
            .map_err(|e| format!("Failed to write request: {}", e))?;
        stream.write_all(b"\n")
            .map_err(|e| format!("Failed to write newline: {}", e))?;
        stream.flush()
            .map_err(|e| format!("Failed to flush stream: {}", e))?;

        let mut reader = BufReader::new(stream);
        let mut resp_line = String::new();
        reader.read_line(&mut resp_line)
            .map_err(|e| format!("Failed to read response: {}", e))?;

        serde_json::from_str(&resp_line)
            .map_err(|e| format!("Failed to parse response JSON: {}", e))
    }
}

pub fn handle_client_stream(mut stream: UnixStream, service: &RegistryService) -> std::io::Result<()> {
    let reader = BufReader::new(stream.try_clone()?);
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        let resp = match serde_json::from_str::<RegistryRequest>(&line) {
            Ok(req) => service.handle_request(req),
            Err(e) => RegistryResponse::Error(format!("Malformed request: {}", e)),
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

pub fn run_socket_server(
    service: Arc<RegistryService>,
    socket_path: &str,
    stop_flag: Arc<std::sync::atomic::AtomicBool>,
) -> std::io::Result<()> {
    if Path::new(socket_path).exists() {
        let _ = std::fs::remove_file(socket_path);
    }
    if let Some(parent) = Path::new(socket_path).parent() {
        let _ = std::fs::create_dir_all(parent);
    }

    let listener = UnixListener::bind(socket_path)?;
    listener.set_nonblocking(true)?;

    println!("[dap-registryd] Unix domain socket listening at: {}", socket_path);

    while !stop_flag.load(std::sync::atomic::Ordering::Relaxed) {
        match listener.accept() {
            Ok((stream, _)) => {
                let s_clone = Arc::clone(&service);
                std::thread::spawn(move || {
                    let _ = handle_client_stream(stream, &s_clone);
                });
            }
            Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                std::thread::sleep(std::time::Duration::from_millis(50));
            }
            Err(e) => {
                eprintln!("[dap-registryd] Socket accept error: {}", e);
                break;
            }
        }
    }

    let _ = std::fs::remove_file(socket_path);
    println!("[dap-registryd] Socket server shut down gracefully.");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_registry_initialization_and_queries() {
        let service = RegistryService::new_in_memory().expect("In-memory DB init failed");

        // 1. Test GetConfig
        let req = RegistryRequest::GetConfig {
            key: "compositor.target_framerate".to_string(),
        };
        let resp = service.handle_request(req);
        match resp {
            RegistryResponse::Success(val) => {
                assert_eq!(val["value"], "120");
            }
            other => panic!("Expected success, got: {:?}", other),
        }

        // 2. Test GetActiveBootSlot
        let req_slot = RegistryRequest::GetActiveBootSlot;
        let resp_slot = service.handle_request(req_slot);
        match resp_slot {
            RegistryResponse::Success(val) => {
                assert_eq!(val["slot_id"], "A");
                assert_eq!(val["partition_label"], "DAXOS_ROOT_A");
            }
            other => panic!("Expected success, got: {:?}", other),
        }

        // 3. Test UpdateGlassProfile
        let req_glass = RegistryRequest::UpdateGlassProfile {
            user_id: "user-master-01".to_string(),
            opacity: 0.85,
            blur_radius: 42,
            edge_brightness: 1.3,
            noise_intensity: 0.05,
        };
        let resp_glass = service.handle_request(req_glass);
        assert_eq!(resp_glass, RegistryResponse::Success(serde_json::json!({ "synced": true })));

        // 4. Test CheckSandboxPermission
        let req_perm = RegistryRequest::CheckSandboxPermission {
            bundle_id: "org.daxos.terminal".to_string(),
            permission_code: "daxos.permission.GPU_ACCELERATION".to_string(),
        };
        let resp_perm = service.handle_request(req_perm);
        match resp_perm {
            RegistryResponse::Success(val) => {
                assert_eq!(val["grant_status"], "granted");
            }
            other => panic!("Expected success, got: {:?}", other),
        }

        // 5. Test Statistics
        let stats = service.get_statistics().expect("Failed to get stats");
        assert_eq!(stats["active_boot_slot"], "A");
    }

    #[test]
    fn test_registry_socket_server_client() {
        let service = Arc::new(RegistryService::new_in_memory().expect("In-memory DB init failed"));
        let socket_path = "/tmp/test_daxos_reg_sock.sock";
        let stop_flag = Arc::new(std::sync::atomic::AtomicBool::new(false));

        let stop_clone = Arc::clone(&stop_flag);
        let s_clone = Arc::clone(&service);
        let s_path = socket_path.to_string();

        let server_thread = std::thread::spawn(move || {
            let _ = run_socket_server(s_clone, &s_path, stop_clone);
        });

        // Give server time to bind
        std::thread::sleep(std::time::Duration::from_millis(50));

        let client = RegistryClient::new(socket_path);
        let req = RegistryRequest::GetConfig {
            key: "compositor.target_framerate".to_string(),
        };
        let resp = client.send(&req).expect("IPC send failed");
        match resp {
            RegistryResponse::Success(v) => assert_eq!(v["value"], "120"),
            other => panic!("Expected success from IPC, got: {:?}", other),
        }

        stop_flag.store(true, std::sync::atomic::Ordering::Relaxed);
        let _ = server_thread.join();
    }
}
