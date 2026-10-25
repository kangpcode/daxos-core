//! ============================================================================
//! DAXDROP VISION AIR-GESTURE RECOGNITION ENGINE
//! File: crates/daxdrop/src/gesture.rs
//! Purpose: Real-time hand tracking and mid-air fist clench ("kepal tangan")
//!          detection for seamless gesture-based file grab and transfer
//! ============================================================================

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum HandPose {
    NoHand,
    OpenPalm,
    FistClench, // "Kepal Tangan" - Grabs file/content from screen
    AirDrag,    // Moving clenched hand towards target screen/peer
    AirRelease, // Opening fist - Drops/transmits file to target peer
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct GestureDetectionFrame {
    pub timestamp_ms: u64,
    pub pose: HandPose,
    pub confidence: f32,
    pub hand_x: f32, // Normalized 0.0 - 1.0
    pub hand_y: f32, // Normalized 0.0 - 1.0
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum GestureState {
    Idle,
    TrackingHand,
    FileGrabbed { file_path: String },
    Transmitting { target_peer: String },
}

pub struct AirGestureEngine {
    state: GestureState,
    min_confidence: f32,
    history: Vec<GestureDetectionFrame>,
}

impl AirGestureEngine {
    pub fn new(min_confidence: f32) -> Self {
        Self {
            state: GestureState::Idle,
            min_confidence,
            history: Vec::with_capacity(32),
        }
    }

    pub fn current_state(&self) -> &GestureState {
        &self.state
    }

    pub fn process_frame(&mut self, frame: GestureDetectionFrame) -> Option<String> {
        if frame.confidence < self.min_confidence {
            return None;
        }

        self.history.push(frame.clone());
        if self.history.len() > 32 {
            self.history.remove(0);
        }

        match (&self.state, frame.pose) {
            (GestureState::Idle, HandPose::OpenPalm) => {
                self.state = GestureState::TrackingHand;
                Some("[GESTURE] Open palm detected. Ready for air-grab.".to_string())
            }
            (GestureState::TrackingHand, HandPose::FistClench) => {
                self.state = GestureState::FileGrabbed {
                    file_path: "selected_item".to_string(),
                };
                Some("[GESTURE: KEPAL TANGAN] Fist clench detected! Content grabbed into DaXDrop air-buffer.".to_string())
            }
            (GestureState::FileGrabbed { file_path }, HandPose::AirRelease) => {
                let msg = format!("[GESTURE: LEPAS TANGAN] Air release detected! Dropping '{}' to nearest DAXOS peer.", file_path);
                self.state = GestureState::Idle;
                Some(msg)
            }
            (GestureState::TrackingHand, HandPose::NoHand) => {
                self.state = GestureState::Idle;
                None
            }
            _ => None,
        }
    }

    pub fn set_grabbed_file(&mut self, path: impl Into<String>) {
        self.state = GestureState::FileGrabbed {
            file_path: path.into(),
        };
    }
}

// ----------------------------------------------------------------------------
// REAL V4L2 HARDWARE CAMERA PROBER & OPTICAL FRAME ANALYZER
// ----------------------------------------------------------------------------

use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PhysicalCameraInfo {
    pub device_node: String,
    pub card_name: String,
    pub sysfs_path: String,
    pub is_available: bool,
}

pub fn probe_physical_cameras() -> Vec<PhysicalCameraInfo> {
    let mut cameras = Vec::new();
    let v4l_path = Path::new("/sys/class/video4linux");

    if let Ok(entries) = fs::read_dir(v4l_path) {
        for entry in entries.flatten() {
            let file_name = entry.file_name().to_string_lossy().to_string();
            if file_name.starts_with("video") {
                let node_path = format!("/dev/{}", file_name);
                let name_file = entry.path().join("name");
                let card_name = fs::read_to_string(&name_file)
                    .unwrap_or_else(|_| "Unknown V4L2 Camera".to_string())
                    .trim()
                    .to_string();

                let is_available = Path::new(&node_path).exists();
                cameras.push(PhysicalCameraInfo {
                    device_node: node_path,
                    card_name,
                    sysfs_path: entry.path().to_string_lossy().to_string(),
                    is_available,
                });
            }
        }
    }

    cameras
}

pub struct OpticalContourAnalyzer;

impl OpticalContourAnalyzer {
    /// Menganalisis frame buffer citra nyata (RGB/RGBA) untuk mendeteksi pose tangan
    /// berbasis sebaran densitas piksel dan rasio kekompakan kontur (bounding box compactness)
    pub fn analyze_frame_buffer(width: u32, height: u32, rgba_pixels: &[u8]) -> GestureDetectionFrame {
        if rgba_pixels.len() < (width * height * 4) as usize {
            return GestureDetectionFrame {
                timestamp_ms: 0,
                pose: HandPose::NoHand,
                confidence: 0.0,
                hand_x: 0.0,
                hand_y: 0.0,
            };
        }

        let mut skin_pixels = 0usize;
        let mut sum_x = 0u64;
        let mut sum_y = 0u64;
        let mut min_x = width;
        let mut max_x = 0u32;
        let mut min_y = height;
        let mut max_y = 0u32;

        // Sampling 1 dari 4 piksel untuk kecepatan real-time 60fps
        for y in (0..height).step_by(2) {
            for x in (0..width).step_by(2) {
                let idx = ((y * width + x) * 4) as usize;
                let r = rgba_pixels[idx] as f32;
                let g = rgba_pixels[idx + 1] as f32;
                let b = rgba_pixels[idx + 2] as f32;

                // Thresholding deteksi rona kulit/tangan dalam ruang RGB terkalibrasi
                if r > 95.0 && g > 40.0 && b > 20.0 && (r - g).abs() > 15.0 && r > g && r > b {
                    skin_pixels += 1;
                    sum_x += x as u64;
                    sum_y += y as u64;
                    if x < min_x { min_x = x; }
                    if x > max_x { max_x = x; }
                    if y < min_y { min_y = y; }
                    if y > max_y { max_y = y; }
                }
            }
        }

        if skin_pixels < 100 || min_x >= max_x || min_y >= max_y {
            return GestureDetectionFrame {
                timestamp_ms: 0,
                pose: HandPose::NoHand,
                confidence: 0.1,
                hand_x: 0.5,
                hand_y: 0.5,
            };
        }

        let hand_x = (sum_x as f32 / skin_pixels as f32) / width as f32;
        let hand_y = (sum_y as f32 / skin_pixels as f32) / height as f32;

        let bbox_w = (max_x - min_x) as f32;
        let bbox_h = (max_y - min_y) as f32;
        let bbox_area = bbox_w * bbox_h;
        let density = (skin_pixels as f32 * 4.0) / bbox_area.max(1.0);
        let aspect_ratio = bbox_h / bbox_w.max(1.0);

        // Jika tangan terkepal (Fist Clench / Kepal Tangan):
        let (pose, confidence) = if density > 0.60 && (0.85..=1.25).contains(&aspect_ratio) {
            (HandPose::FistClench, 0.94)
        } else if aspect_ratio > 1.30 {
            // Jari-jari terbuka ke atas (Open Palm)
            (HandPose::OpenPalm, 0.91)
        } else {
            (HandPose::AirDrag, 0.82)
        };

        GestureDetectionFrame {
            timestamp_ms: 0,
            pose,
            confidence,
            hand_x,
            hand_y,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_air_grab_state_machine() {
        let mut engine = AirGestureEngine::new(0.75);
        assert_eq!(*engine.current_state(), GestureState::Idle);

        // Step 1: Open palm
        let evt1 = engine.process_frame(GestureDetectionFrame {
            timestamp_ms: 100,
            pose: HandPose::OpenPalm,
            confidence: 0.92,
            hand_x: 0.5,
            hand_y: 0.5,
        });
        assert!(evt1.is_some());
        assert_eq!(*engine.current_state(), GestureState::TrackingHand);

        // Step 2: Fist clench ("Kepal Tangan")
        let evt2 = engine.process_frame(GestureDetectionFrame {
            timestamp_ms: 250,
            pose: HandPose::FistClench,
            confidence: 0.88,
            hand_x: 0.52,
            hand_y: 0.48,
        });
        assert!(evt2.is_some());
        assert!(evt2.unwrap().contains("KEPAL TANGAN"));

        // Step 3: Air release ("Lepas Tangan")
        let evt3 = engine.process_frame(GestureDetectionFrame {
            timestamp_ms: 600,
            pose: HandPose::AirRelease,
            confidence: 0.85,
            hand_x: 0.70,
            hand_y: 0.35,
        });
        assert!(evt3.is_some());
        assert!(evt3.unwrap().contains("LEPAS TANGAN"));
        assert_eq!(*engine.current_state(), GestureState::Idle);
    }

    #[test]
    fn test_probe_physical_cameras() {
        let cameras = probe_physical_cameras();
        // Memastikan parser V4L2 sysfs tidak pernah panic
        println!("Probed {} physical V4L2 camera devices", cameras.len());
    }

    #[test]
    fn test_optical_frame_analyzer() {
        let w = 64u32;
        let h = 64u32;
        let mut pixels = vec![0u8; (w * h * 4) as usize];

        // Buat pola tangan buatan di tengah (kulit RGB: 200, 120, 80)
        for y in 20..44 {
            for x in 20..44 {
                let idx = ((y * w + x) * 4) as usize;
                pixels[idx] = 200;
                pixels[idx + 1] = 120;
                pixels[idx + 2] = 80;
                pixels[idx + 3] = 255;
            }
        }

        let res = OpticalContourAnalyzer::analyze_frame_buffer(w, h, &pixels);
        assert_ne!(res.pose, HandPose::NoHand);
        assert!(res.confidence > 0.80);
    }
}
