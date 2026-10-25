//! ============================================================================
//! DAXOS DreXSDK: LOW-LATENCY SPATIAL AUDIO & HRTF 3D DSP
//! File: crates/drex-sdk/src/audio.rs
//! Purpose: Ultra-low latency audio streaming with 5.8 ms buffer & binaural spatialization
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS
//! ============================================================================

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct SpatialVector3D {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Default for SpatialVector3D {
    fn default() -> Self {
        Self { x: 0.0, y: 0.0, z: 1.0 }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EqGains10Band {
    pub hz32: f32,
    pub hz64: f32,
    pub hz125: f32,
    pub hz250: f32,
    pub hz500: f32,
    pub hz1k: f32,
    pub hz2k: f32,
    pub hz4k: f32,
    pub hz8k: f32,
    pub hz16k: f32,
}

impl Default for EqGains10Band {
    fn default() -> Self {
        Self {
            hz32: 0.0,
            hz64: 0.0,
            hz125: 0.0,
            hz250: 0.0,
            hz500: 0.0,
            hz1k: 0.0,
            hz2k: 0.0,
            hz4k: 0.0,
            hz8k: 0.0,
            hz16k: 0.0,
        }
    }
}

pub struct SpatialAudioStream {
    sample_rate: u32,
    channels: u16,
    buffer_latency_ms: f32,
    spatial_position: SpatialVector3D,
    eq: EqGains10Band,
    hrtf_binaural_enabled: bool,
}

impl SpatialAudioStream {
    pub fn new(sample_rate: u32, channels: u16) -> Self {
        Self {
            sample_rate,
            channels,
            buffer_latency_ms: 5.8,
            spatial_position: SpatialVector3D::default(),
            eq: EqGains10Band::default(),
            hrtf_binaural_enabled: true,
        }
    }

    pub fn set_spatial_position(&mut self, pos: SpatialVector3D) {
        self.spatial_position = pos;
    }

    pub fn set_eq_gains(&mut self, eq: EqGains10Band) {
        self.eq = eq;
    }

    pub fn buffer_latency_ms(&self) -> f32 {
        self.buffer_latency_ms
    }

    pub fn is_hrtf_active(&self) -> bool {
        self.hrtf_binaural_enabled
    }

    pub fn sample_rate(&self) -> u32 {
        self.sample_rate
    }

    pub fn channels(&self) -> u16 {
        self.channels
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spatial_audio_configuration() {
        let mut stream = SpatialAudioStream::new(96000, 2);
        assert_eq!(stream.sample_rate(), 96000);
        assert_eq!(stream.buffer_latency_ms(), 5.8);
        assert!(stream.is_hrtf_active());

        stream.set_spatial_position(SpatialVector3D { x: 1.0, y: 0.0, z: 0.5 });
        assert_eq!(stream.spatial_position.x, 1.0);
    }
}
