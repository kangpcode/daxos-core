//! ============================================================================
//! DAXOS DREX-SDK: OFFICIAL APPLICATION & ANTI-CRASH RUNTIME SDK
//! File: crates/drex-sdk/src/lib.rs
//! Purpose: Production Software Development Kit for DAXOS Universal Applications
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS
//! ============================================================================

pub mod anticrash;
pub mod app;
pub mod audio;
pub mod gestures;
pub mod memory;
pub mod telemetry;
pub mod vault;

pub mod prelude {
    pub use crate::anticrash::{CrashReport, CrashShield, QuarantineState, WatchdogClient};
    pub use crate::app::{AppMetadata, DreXApp};
    pub use crate::audio::{EqGains10Band, SpatialAudioStream, SpatialVector3D};
    pub use crate::gestures::{AirGestureReceiver, GestureEvent, HandPose};
    pub use crate::memory::{AffineBuffer, ZeroCopyRingBuffer};
    pub use crate::telemetry::{HardwareTelemetry, TelemetrySnapshot};
    pub use crate::vault::{SecureToken, SecureVault, VaultEntry};
    pub use drex_ui::prelude::*;
}

pub use prelude::*;
