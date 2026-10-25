//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: GESTURES & INTERACTIONS
//! File: crates/drex-ui/src/gestures.rs
//! Purpose: Declarative touch, mouse, and gesture handlers like SwiftUI & ArkUI
//! ============================================================================

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum GestureType {
    Tap { count: u32 },
    LongPress { minimum_duration_ms: u64 },
    Drag { minimum_distance: f32 },
    Hover,
    Pinch,
    AirGrab { confidence: f32 }, // HarmonyOS-style mid-air fist clench for DaXDrop
    AirRelease,                  // Mid-air hand release to drop/send
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GestureAction {
    pub gesture_type: GestureType,
    pub handler_id: String,
}

impl GestureAction {
    pub fn tap(handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::Tap { count: 1 },
            handler_id: handler_id.into(),
        }
    }

    pub fn double_tap(handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::Tap { count: 2 },
            handler_id: handler_id.into(),
        }
    }

    pub fn long_press(minimum_duration_ms: u64, handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::LongPress { minimum_duration_ms },
            handler_id: handler_id.into(),
        }
    }

    pub fn drag(handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::Drag { minimum_distance: 4.0 },
            handler_id: handler_id.into(),
        }
    }

    pub fn hover(handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::Hover,
            handler_id: handler_id.into(),
        }
    }

    pub fn air_grab(confidence: f32, handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::AirGrab { confidence },
            handler_id: handler_id.into(),
        }
    }

    pub fn air_release(handler_id: impl Into<String>) -> Self {
        Self {
            gesture_type: GestureType::AirRelease,
            handler_id: handler_id.into(),
        }
    }
}
