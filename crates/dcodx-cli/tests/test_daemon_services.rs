//! ============================================================================
//! DAXOS INTEGRATION TEST: DAEMON SERVICES & IPC ECOSYSTEM
//! File: crates/dcodx-cli/tests/test_daemon_services.rs
//! Purpose: End-to-end integration tests for all 5 DAXOS daemons
//! ============================================================================

use dap_registryd::{run_socket_server, RegistryClient, RegistryRequest, RegistryResponse, RegistryService};
use dap_sandboxd::{run_sandbox_server, SandboxRequest, SandboxResponse};
use dap_updated::{run_update_server, GrubEnvironment, OtaManager, OtaRequest, OtaResponse};
use drex_boostd::{run_boost_server, BoostRequest, BoostResponse, DrexBoostGovernor};
use drex_compositor::{AcrylicParameters, DrexCompositorEngine};
use drexvis::{CudaBackend, GpuBackend};

use std::io::{BufRead, BufReader, Write};
use std::os::unix::net::UnixStream;
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Duration;

#[test]
fn test_registry_daemon_ipc() {
    let service = Arc::new(RegistryService::new_in_memory().expect("In-memory DB init failed"));
    let sock = "/tmp/test_integ_reg.sock";
    let stop = Arc::new(AtomicBool::new(false));

    let s_clone = Arc::clone(&service);
    let st_clone = Arc::clone(&stop);
    let s_path = sock.to_string();

    let handle = std::thread::spawn(move || {
        let _ = run_socket_server(s_clone, &s_path, st_clone);
    });
    std::thread::sleep(Duration::from_millis(50));

    let client = RegistryClient::new(sock);

    // Test 1: GetConfig
    let resp = client.send(&RegistryRequest::GetConfig {
        key: "compositor.target_framerate".to_string(),
    }).expect("GetConfig failed");
    match resp {
        RegistryResponse::Success(v) => assert_eq!(v["value"], "120"),
        other => panic!("Unexpected: {:?}", other),
    }

    // Test 2: GetActiveBootSlot
    let resp = client.send(&RegistryRequest::GetActiveBootSlot).expect("GetActiveBootSlot failed");
    match resp {
        RegistryResponse::Success(v) => assert_eq!(v["slot_id"], "A"),
        other => panic!("Unexpected: {:?}", other),
    }

    stop.store(true, Ordering::Relaxed);
    let _ = handle.join();
}

#[test]
fn test_sandbox_daemon_ipc() {
    let sock = "/tmp/test_integ_sandbox.sock";
    let stop = Arc::new(AtomicBool::new(false));
    let st_clone = Arc::clone(&stop);
    let s_path = sock.to_string();

    let handle = std::thread::spawn(move || {
        let _ = run_sandbox_server(&s_path, st_clone);
    });
    std::thread::sleep(Duration::from_millis(50));

    let mut stream = UnixStream::connect(sock).expect("Failed to connect to sandbox socket");

    // Send GetStatus
    let req = serde_json::to_string(&SandboxRequest::GetStatus).unwrap() + "\n";
    stream.write_all(req.as_bytes()).unwrap();
    stream.flush().unwrap();

    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).unwrap();

    let resp: SandboxResponse = serde_json::from_str(&line).unwrap();
    match resp {
        SandboxResponse::Success(v) => {
            assert_eq!(v["service"], "dap-sandboxd");
            assert_eq!(v["landlock_version"], 5);
        }
        other => panic!("Unexpected: {:?}", other),
    }

    stop.store(true, Ordering::Relaxed);
    let _ = handle.join();
}

#[test]
fn test_updated_daemon_ipc() {
    let sock = "/tmp/test_integ_update.sock";
    let grubenv = Path::new("/tmp/test_integ_grubenv");
    let env = GrubEnvironment::new_default();
    let mgr = Arc::new(Mutex::new(OtaManager::new(1776200000, env)));
    let stop = Arc::new(AtomicBool::new(false));

    let m_clone = Arc::clone(&mgr);
    let st_clone = Arc::clone(&stop);
    let s_path = sock.to_string();

    let handle = std::thread::spawn(move || {
        let _ = run_update_server(m_clone, &s_path, grubenv, st_clone);
    });
    std::thread::sleep(Duration::from_millis(50));

    let mut stream = UnixStream::connect(sock).expect("Failed to connect to update socket");

    // Send GetStatus
    let req = serde_json::to_string(&OtaRequest::GetStatus).unwrap() + "\n";
    stream.write_all(req.as_bytes()).unwrap();
    stream.flush().unwrap();

    let mut reader = BufReader::new(stream.try_clone().unwrap());
    let mut line = String::new();
    reader.read_line(&mut line).unwrap();

    let resp: OtaResponse = serde_json::from_str(&line).unwrap();
    match resp {
        OtaResponse::Success(v) => {
            assert_eq!(v["slot_active"], "A");
            assert_eq!(v["boot_counter"], 0);
        }
        other => panic!("Unexpected: {:?}", other),
    }

    // Send SimulateBootFailure
    let req = serde_json::to_string(&OtaRequest::SimulateBootFailure).unwrap() + "\n";
    stream.write_all(req.as_bytes()).unwrap();
    stream.flush().unwrap();

    line.clear();
    reader.read_line(&mut line).unwrap();
    let resp: OtaResponse = serde_json::from_str(&line).unwrap();
    match resp {
        OtaResponse::Success(v) => assert_eq!(v["boot_counter"], 1),
        other => panic!("Unexpected: {:?}", other),
    }

    stop.store(true, Ordering::Relaxed);
    let _ = handle.join();
    let _ = std::fs::remove_file(grubenv);
}

#[test]
fn test_boost_daemon_ipc() {
    let sock = "/tmp/test_integ_boost.sock";
    let gov = Arc::new(Mutex::new(DrexBoostGovernor::new()));
    let stop = Arc::new(AtomicBool::new(false));

    let g_clone = Arc::clone(&gov);
    let st_clone = Arc::clone(&stop);
    let s_path = sock.to_string();

    let handle = std::thread::spawn(move || {
        let _ = run_boost_server(g_clone, &s_path, st_clone);
    });
    std::thread::sleep(Duration::from_millis(50));

    let mut stream = UnixStream::connect(sock).expect("Failed to connect to boost socket");

    // Send InputEvent
    let req = serde_json::to_string(&BoostRequest::InputEvent).unwrap() + "\n";
    stream.write_all(req.as_bytes()).unwrap();
    stream.flush().unwrap();

    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).unwrap();

    let resp: BoostResponse = serde_json::from_str(&line).unwrap();
    match resp {
        BoostResponse::Success(v) => {
            assert_eq!(v["state"], "InteractiveBoost");
            assert_eq!(v["clock_offset_mhz"], 60);
        }
        other => panic!("Unexpected: {:?}", other),
    }

    stop.store(true, Ordering::Relaxed);
    let _ = handle.join();
}

#[test]
fn test_compositor_acrylic_glass_engine() {
    let mut backend = Box::new(CudaBackend::new());
    backend.initialize().unwrap();

    let mut engine = DrexCompositorEngine::new(backend, 120);
    let surf = engine.create_client_surface(999, 2560, 1440);
    let params = AcrylicParameters {
        opacity: 0.80,
        blur_radius_px: 40,
        edge_brightness: 1.25,
        noise_intensity: 0.03,
    };
    engine.attach_acrylic_effect(surf, params).unwrap();

    let f1 = engine.render_frame().unwrap();
    let f2 = engine.render_frame().unwrap();
    assert_eq!(f1, 1);
    assert_eq!(f2, 2);
}
