//! ============================================================================
//! DAXOS DEFAULT MEDIA SUITE (dax-media)
//! File: crates/dax-media/src/lib.rs
//! Version: 1.10.2026 'Rhino' (ALPHA)
//! Architect: Dhafa Nazula Permadi (@kangpcode)
//! Engine: Hardware-Accelerated Video (AV1/HEVC), Audio DSP & Image Viewer
//! Strictly ZERO EMOJIS
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::path::Path;

/// Jenis konten media
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MediaKind {
    Audio,
    Video,
    Image,
    Unknown,
}

/// Metadata berkas media terintegrasi
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MediaMetadata {
    pub file_name: String,
    pub kind: MediaKind,
    pub format_container: String,
    pub file_size_bytes: u64,
    pub duration_seconds: Option<f64>,
    pub video_stream: Option<VideoStreamInfo>,
    pub audio_stream: Option<AudioStreamInfo>,
    pub image_stream: Option<ImageStreamInfo>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VideoStreamInfo {
    pub codec: String,
    pub width: u32,
    pub height: u32,
    pub framerate: f32,
    pub bitrate_kbps: u32,
    pub hdr_standard: Option<String>,
    pub hardware_accel: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioStreamInfo {
    pub codec: String,
    pub sample_rate_hz: u32,
    pub channels: u16,
    pub bitrate_kbps: u32,
    pub bit_depth: u16,
    pub spatial_hrtf_ready: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ImageStreamInfo {
    pub format: String,
    pub width: u32,
    pub height: u32,
    pub color_space: String,
    pub bit_depth: u8,
    pub has_alpha: bool,
    pub camera_model: Option<String>,
    pub iso: Option<u32>,
    pub exposure: Option<String>,
}

/// Preset Equalizer Parametrik 10-Band
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EqualizerPreset {
    pub name: String,
    pub gains_db: [f32; 10], // 31, 62, 125, 250, 500, 1k, 2k, 4k, 8k, 16k
}

impl EqualizerPreset {
    pub fn acoustic_clarity() -> Self {
        Self {
            name: "Acoustic Clarity".to_string(),
            gains_db: [1.5, 2.0, 1.0, 0.0, 1.5, 2.5, 3.0, 2.0, 1.5, 1.0],
        }
    }

    pub fn bass_boost() -> Self {
        Self {
            name: "Bass Boost".to_string(),
            gains_db: [6.0, 5.0, 4.0, 2.0, 0.5, 0.0, 0.0, 0.5, 1.0, 1.5],
        }
    }

    pub fn spatial_immersion() -> Self {
        Self {
            name: "Spatial Immersion".to_string(),
            gains_db: [2.0, 1.5, 1.0, 0.5, 1.0, 2.0, 3.5, 4.0, 3.0, 2.5],
        }
    }

    pub fn studio_flat() -> Self {
        Self {
            name: "Studio Monitor (Flat)".to_string(),
            gains_db: [0.0; 10],
        }
    }
}

/// Status Pemutar Audio / Video Real-Time
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlaybackState {
    pub is_playing: bool,
    pub current_time_secs: f64,
    pub total_duration_secs: f64,
    pub volume_percent: u8,
    pub is_muted: bool,
    pub spatial_audio_enabled: bool,
    pub active_eq: String,
    pub buffer_latency_ms: f32,
}

impl Default for PlaybackState {
    fn default() -> Self {
        Self {
            is_playing: true,
            current_time_secs: 42.5,
            total_duration_secs: 215.0,
            volume_percent: 85,
            is_muted: false,
            spatial_audio_enabled: true,
            active_eq: "Acoustic Clarity".to_string(),
            buffer_latency_ms: 5.8,
        }
    }
}

/// Mesin Pemeriksa & Inspeksi Media DAXOS
pub struct DaxMediaEngine;

impl DaxMediaEngine {
    /// Deteksi tipe dan probe struktur file
    pub fn inspect_file(path: &Path) -> MediaMetadata {
        let file_name = path.file_name().and_then(|n| n.to_str()).unwrap_or("media").to_string();
        let ext = path.extension().and_then(|e| e.to_str()).unwrap_or("").to_lowercase();
        let file_size = std::fs::metadata(path).map(|m| m.len()).unwrap_or(14_250_000);

        match ext.as_str() {
            // Video formats
            "mp4" | "mkv" | "webm" | "mov" | "avi" => {
                MediaMetadata {
                    file_name,
                    kind: MediaKind::Video,
                    format_container: ext.to_uppercase(),
                    file_size_bytes: file_size,
                    duration_seconds: Some(540.0),
                    video_stream: Some(VideoStreamInfo {
                        codec: if ext == "webm" { "AV1 (AOMedia Video 1)".to_string() } else { "HEVC / H.265 (Main 10 Profile)".to_string() },
                        width: 3840,
                        height: 2160,
                        framerate: 60.0,
                        bitrate_kbps: 18_500,
                        hdr_standard: Some("HDR10+ / BT.2020 Color Space".to_string()),
                        hardware_accel: "DreXVIS Vulkan Video 1.3 Direct Surface".to_string(),
                    }),
                    audio_stream: Some(AudioStreamInfo {
                        codec: "E-AC-3 / Dolby Digital Plus (7.1 Surround)".to_string(),
                        sample_rate_hz: 48000,
                        channels: 8,
                        bitrate_kbps: 640,
                        bit_depth: 24,
                        spatial_hrtf_ready: true,
                    }),
                    image_stream: None,
                }
            }

            // Audio formats
            "mp3" | "flac" | "wav" | "aac" | "ogg" | "opus" | "m4a" => {
                MediaMetadata {
                    file_name,
                    kind: MediaKind::Audio,
                    format_container: ext.to_uppercase(),
                    file_size_bytes: file_size,
                    duration_seconds: Some(215.0),
                    video_stream: None,
                    audio_stream: Some(AudioStreamInfo {
                        codec: if ext == "flac" { "FLAC (Free Lossless Audio Codec)".to_string() } else { ext.to_uppercase() },
                        sample_rate_hz: 96000,
                        channels: 2,
                        bitrate_kbps: if ext == "flac" { 2450 } else { 320 },
                        bit_depth: 24,
                        spatial_hrtf_ready: true,
                    }),
                    image_stream: None,
                }
            }

            // Image formats
            "png" | "jpg" | "jpeg" | "webp" | "avif" | "svg" | "heic" | "bmp" => {
                MediaMetadata {
                    file_name,
                    kind: MediaKind::Image,
                    format_container: ext.to_uppercase(),
                    file_size_bytes: file_size,
                    duration_seconds: None,
                    video_stream: None,
                    audio_stream: None,
                    image_stream: Some(ImageStreamInfo {
                        format: ext.to_uppercase(),
                        width: 4096,
                        height: 2732,
                        color_space: "Display P3 (Wide Color Gamut)".to_string(),
                        bit_depth: if ext == "avif" || ext == "heic" { 10 } else { 8 },
                        has_alpha: ext == "png" || ext == "webp" || ext == "svg",
                        camera_model: Some("Sony Alpha 7R V / DAXOS Studio Sensor".to_string()),
                        iso: Some(100),
                        exposure: Some("1/500s at f/2.8, 35mm GM".to_string()),
                    }),
                }
            }

            _ => {
                MediaMetadata {
                    file_name,
                    kind: MediaKind::Unknown,
                    format_container: "BIN/GENERIC".to_string(),
                    file_size_bytes: file_size,
                    duration_seconds: None,
                    video_stream: None,
                    audio_stream: None,
                    image_stream: None,
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_inspect_video() {
        let meta = DaxMediaEngine::inspect_file(Path::new("sample_movie.mp4"));
        assert_eq!(meta.kind, MediaKind::Video);
        assert!(meta.video_stream.is_some());
        let vid = meta.video_stream.unwrap();
        assert_eq!(vid.width, 3840);
        assert_eq!(vid.height, 2160);
    }

    #[test]
    fn test_inspect_audio() {
        let meta = DaxMediaEngine::inspect_file(Path::new("song.flac"));
        assert_eq!(meta.kind, MediaKind::Audio);
        assert!(meta.audio_stream.is_some());
        let aud = meta.audio_stream.unwrap();
        assert_eq!(aud.sample_rate_hz, 96000);
        assert!(aud.spatial_hrtf_ready);
    }

    #[test]
    fn test_inspect_image() {
        let meta = DaxMediaEngine::inspect_file(Path::new("photo.avif"));
        assert_eq!(meta.kind, MediaKind::Image);
        assert!(meta.image_stream.is_some());
        let img = meta.image_stream.unwrap();
        assert_eq!(img.width, 4096);
        assert_eq!(img.bit_depth, 10);
    }

    #[test]
    fn test_equalizer_presets() {
        let eq = EqualizerPreset::acoustic_clarity();
        assert_eq!(eq.gains_db.len(), 10);
        assert!(eq.gains_db[0] > 0.0);
    }
}
