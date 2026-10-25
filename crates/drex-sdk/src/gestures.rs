//! ============================================================================
//! DAXOS DreXSDK: AIR-GESTURE & OPTICAL TRACKING EVENT RECEIVER
//! File: crates/drex-sdk/src/gestures.rs
//! Purpose: Real-time hand pose classification (Open Palm, Fist Clench, Release)
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS
//! ============================================================================

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum HandPose {
    None,
    OpenPalm,
    FistClench,  // Gestur "Kepal Tangan" for air-grab
    FistRelease, // Gestur "Lepas Tangan" for air-drop
    AirSwipeLeft,
    AirSwipeRight,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GestureEvent {
    pub pose: HandPose,
    pub confidence: f32,
    pub normalized_x: f32,
    pub normalized_y: f32,
    pub timestamp_ms: u64,
}

pub struct AirGestureReceiver {
    sensor_device: String,
    last_pose: HandPose,
}

impl AirGestureReceiver {
    pub fn new(sensor_device: impl Into<String>) -> Self {
        Self {
            sensor_device: sensor_device.into(),
            last_pose: HandPose::None,
        }
    }

    pub fn process_frame_landmarks(&mut self, landmarks_count: usize, fist_detected: bool) -> GestureEvent {
        let pose = if fist_detected {
            HandPose::FistClench
        } else if self.last_pose == HandPose::FistClench && !fist_detected {
            HandPose::FistRelease
        } else if !fist_detected && landmarks_count > 15 {
            HandPose::OpenPalm
        } else {
            HandPose::None
        };

        self.last_pose = pose;

        GestureEvent {
            pose,
            confidence: 0.98,
            normalized_x: 0.5,
            normalized_y: 0.5,
            timestamp_ms: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap_or_default()
                .as_millis() as u64,
        }
    }

    pub fn sensor_device(&self) -> &str {
        &self.sensor_device
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_air_gesture_state_transition() {
        let mut receiver = AirGestureReceiver::new("/dev/video0");
        let ev1 = receiver.process_frame_landmarks(21, false);
        assert_eq!(ev1.pose, HandPose::OpenPalm);

        let ev2 = receiver.process_frame_landmarks(21, true);
        assert_eq!(ev2.pose, HandPose::FistClench);

        let ev3 = receiver.process_frame_landmarks(21, false);
        assert_eq!(ev3.pose, HandPose::FistRelease);
    }
}
