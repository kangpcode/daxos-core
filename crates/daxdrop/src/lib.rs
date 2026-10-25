//! ============================================================================
//! DAXDROP SUBSYSTEM: WIRELESS P2P FILE SHARING & VISION AIR-GESTURE TRANSFER
//! File: crates/daxdrop/src/lib.rs
//! Purpose: Real-time discovery, encrypted transfer, and HarmonyOS-style
//!          air-grab ("kepal tangan") gesture interaction
//! ============================================================================

pub mod discovery;
pub mod gesture;
pub mod transfer;

pub use discovery::{DevicePeer, DeviceType, DiscoveryManager};
pub use gesture::{probe_physical_cameras, AirGestureEngine, GestureDetectionFrame, GestureState, HandPose, OpticalContourAnalyzer, PhysicalCameraInfo};
pub use transfer::{TransferManager, TransferManifest};

pub struct DaXDropService {
    pub discovery: DiscoveryManager,
    pub gesture_engine: AirGestureEngine,
    pub is_active: bool,
}

impl DaXDropService {
    pub fn new(device_name: impl Into<String>) -> Self {
        Self {
            discovery: DiscoveryManager::new(device_name),
            gesture_engine: AirGestureEngine::new(0.80),
            is_active: true,
        }
    }

    pub fn status_report(&mut self) -> String {
        let peers = self.discovery.scan_nearby_peers();
        let mut out = String::new();
        out.push_str("================================================================================\n");
        out.push_str("  DAXOS DAXDROP SUBSYSTEM & AIR-GESTURE SHARING ENGINE\n");
        out.push_str("  Direct P2P Wireless, ChaCha20-Poly1305 Encryption, Vision Hand Tracking\n");
        out.push_str("================================================================================\n");
        out.push_str(&format!("Device Name    : {} [ONLINE]\n", self.discovery.local_name()));
        out.push_str("Protocol       : DaXDrop v1.2 (mDNS _daxdrop._tcp, Wi-Fi Direct)\n");
        out.push_str("Air Gestures   : Active (Vision Air-Grab 'Kepal Tangan' Enabled)\n");
        out.push_str("Encryption     : TLS 1.3 / ChaCha20-Poly1305 with SHA3-512 Verification\n\n");
        out.push_str("Discovered Nearby DAXOS Peers:\n");
        for peer in peers {
            out.push_str(&format!(
                "  - [{:?}] {} (IP: {}, RSSI: {} dBm, Trusted: {})\n",
                peer.device_type, peer.name, peer.ip_address, peer.signal_rssi, peer.is_trusted
            ));
        }
        out.push_str("--------------------------------------------------------------------------------\n");
        out
    }
}
