//! ============================================================================
//! DAXOS DREX-BOOST HARDWARE GOVERNOR (drex-boostd)
//! File: crates/drex-boostd/src/lib.rs
//! Purpose: Adaptive P-State & Thermal Frequency Regulator
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::time::Instant;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum GovernorState {
    Idle,
    InteractiveBoost,
    SustainedLoad,
    ThermalProtection,
    EmergencyRollback,
}

pub struct PidController {
    pub kp: f64,
    pub ki: f64,
    pub kd: f64,
    target: f64,
    integral: f64,
    last_error: f64,
}

impl PidController {
    pub fn new(kp: f64, ki: f64, kd: f64, target: f64) -> Self {
        Self {
            kp,
            ki,
            kd,
            target,
            integral: 0.0,
            last_error: 0.0,
        }
    }

    pub fn compute(&mut self, current: f64, dt_seconds: f64) -> f64 {
        let error = self.target - current;
        self.integral += error * dt_seconds;
        let derivative = if dt_seconds > 0.0 {
            (error - self.last_error) / dt_seconds
        } else {
            0.0
        };
        self.last_error = error;

        self.kp * error + self.ki * self.integral + self.kd * derivative
    }

    pub fn reset(&mut self) {
        self.integral = 0.0;
        self.last_error = 0.0;
    }
}

pub struct DrexBoostGovernor {
    pub state: GovernorState,
    pub target_temp_c: f64,
    pub thermal_throttle_limit_c: f64,
    pub emergency_cutoff_c: f64,
    pub max_clock_offset_mhz: i32,
    pub current_clock_offset_mhz: i32,
    pub last_input_event: Instant,
    pub pid: PidController,
}

impl DrexBoostGovernor {
    pub const INTERACTIVE_TIMEOUT_MS: u128 = 150;

    pub fn new() -> Self {
        Self {
            state: GovernorState::Idle,
            target_temp_c: 75.0,
            thermal_throttle_limit_c: 82.0,
            emergency_cutoff_c: 90.0,
            max_clock_offset_mhz: 120,
            current_clock_offset_mhz: 0,
            last_input_event: Instant::now(),
            pid: PidController::new(2.4, 0.05, 0.8, 75.0),
        }
    }

    pub fn on_input_event(&mut self) {
        self.last_input_event = Instant::now();
        if self.state == GovernorState::Idle {
            self.state = GovernorState::InteractiveBoost;
            self.current_clock_offset_mhz = 60; // Fast interactive jump
        }
    }

    pub fn update(
        &mut self,
        current_temp_c: f64,
        frame_time_ms: f64,
        dt_seconds: f64,
    ) -> i32 {
        // 1. Cek batas darurat
        if current_temp_c >= self.emergency_cutoff_c {
            self.state = GovernorState::EmergencyRollback;
            self.current_clock_offset_mhz = 0;
            self.pid.reset();
            return 0;
        }

        // 2. Cek perlindungan termal
        if current_temp_c >= self.thermal_throttle_limit_c {
            self.state = GovernorState::ThermalProtection;
            self.current_clock_offset_mhz = (self.current_clock_offset_mhz - 25).max(0);
            return self.current_clock_offset_mhz;
        }

        // 3. Evaluasi idle timeout
        let idle_elapsed = self.last_input_event.elapsed().as_millis();
        if idle_elapsed > Self::INTERACTIVE_TIMEOUT_MS && frame_time_ms <= 8.33 {
            self.state = GovernorState::Idle;
            self.current_clock_offset_mhz = 0;
            self.pid.reset();
            return 0;
        }

        // 4. Deteksi beban berat (frame drop > 8.33 ms pada 120Hz)
        if frame_time_ms > 8.33 {
            self.state = GovernorState::SustainedLoad;
            let adjustment = self.pid.compute(current_temp_c, dt_seconds);
            let candidate = self.current_clock_offset_mhz as f64 + adjustment.clamp(-15.0, 15.0);
            self.current_clock_offset_mhz = candidate.clamp(0.0, self.max_clock_offset_mhz as f64) as i32;
        } else if self.state == GovernorState::InteractiveBoost {
            self.current_clock_offset_mhz = 60;
        }

        self.current_clock_offset_mhz
    }
}

// ----------------------------------------------------------------------------
// IPC NETWORKING & SERVER INTERFACE
// ----------------------------------------------------------------------------

use std::io::{BufRead, BufReader, Write};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::Path;
use std::sync::{Arc, Mutex};

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "action", content = "payload")]
pub enum BoostRequest {
    InputEvent,
    UpdateMetrics { temp_c: f64, frame_time_ms: f64, dt_seconds: f64 },
    GetStatus,
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(tag = "status", content = "data")]
pub enum BoostResponse {
    Success(serde_json::Value),
    Error(String),
}

pub fn handle_boost_client(mut stream: UnixStream, governor: &Arc<Mutex<DrexBoostGovernor>>) -> std::io::Result<()> {
    let reader = BufReader::new(stream.try_clone()?);
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }

        let mut gov = governor.lock().unwrap();
        let resp = match serde_json::from_str::<BoostRequest>(&line) {
            Ok(BoostRequest::InputEvent) => {
                gov.on_input_event();
                BoostResponse::Success(serde_json::json!({
                    "state": format!("{:?}", gov.state),
                    "clock_offset_mhz": gov.current_clock_offset_mhz,
                }))
            }
            Ok(BoostRequest::UpdateMetrics { temp_c, frame_time_ms, dt_seconds }) => {
                let offset = gov.update(temp_c, frame_time_ms, dt_seconds);
                BoostResponse::Success(serde_json::json!({
                    "state": format!("{:?}", gov.state),
                    "clock_offset_mhz": offset,
                }))
            }
            Ok(BoostRequest::GetStatus) => {
                BoostResponse::Success(serde_json::json!({
                    "state": format!("{:?}", gov.state),
                    "current_clock_offset_mhz": gov.current_clock_offset_mhz,
                    "target_temp_c": gov.target_temp_c,
                    "thermal_throttle_limit_c": gov.thermal_throttle_limit_c,
                    "emergency_cutoff_c": gov.emergency_cutoff_c,
                    "max_clock_offset_mhz": gov.max_clock_offset_mhz,
                }))
            }
            Err(e) => BoostResponse::Error(format!("Malformed request: {}", e)),
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

pub fn run_boost_server(
    governor: Arc<Mutex<DrexBoostGovernor>>,
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

    println!("[drex-boostd] Unix domain socket listening at: {}", socket_path);

    while !stop_flag.load(std::sync::atomic::Ordering::Relaxed) {
        match listener.accept() {
            Ok((stream, _)) => {
                let g_clone = Arc::clone(&governor);
                std::thread::spawn(move || {
                    let _ = handle_boost_client(stream, &g_clone);
                });
            }
            Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                std::thread::sleep(std::time::Duration::from_millis(50));
            }
            Err(e) => {
                eprintln!("[drex-boostd] Socket error: {}", e);
                break;
            }
        }
    }

    let _ = std::fs::remove_file(socket_path);
    println!("[drex-boostd] Governor server shut down gracefully.");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_governor_interactive_boost_and_emergency_rollback() {
        let mut gov = DrexBoostGovernor::new();
        assert_eq!(gov.state, GovernorState::Idle);

        // Input event memicu boost
        gov.on_input_event();
        assert_eq!(gov.state, GovernorState::InteractiveBoost);
        assert_eq!(gov.current_clock_offset_mhz, 60);

        // Suhu normal, frame drop -> SustainedLoad
        let offset = gov.update(65.0, 12.0, 0.1);
        assert_eq!(gov.state, GovernorState::SustainedLoad);
        assert!(offset > 0);

        // Peningkatan suhu menyentuh cutoff darurat 90°C
        let emergency_offset = gov.update(92.0, 12.0, 0.1);
        assert_eq!(gov.state, GovernorState::EmergencyRollback);
        assert_eq!(emergency_offset, 0);
        assert_eq!(gov.current_clock_offset_mhz, 0);
    }
}
