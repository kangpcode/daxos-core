//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: HYDRO-GLASS ARCHITECTURE
//! File: crates/drex-ui/src/hydro.rs
//! Purpose: Liquid refraction, specular lighting, caustics, and fluid physics
//! ============================================================================

use crate::types::{Color, Point};
use serde::{Deserialize, Serialize};

/// Hydro-Glass Optical & Fluid Properties
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HydroGlassEffect {
    /// Dual-Kawase multi-pass blur radius (px)
    pub blur_radius: f32,
    /// Refraction index (1.33 = water, 1.49 = acrylic, 1.52 = crown glass)
    pub refraction_index: f32,
    /// Surface tension droplet curvature (0.0 flat to 1.0 full organic droplet)
    pub surface_tension: f32,
    /// Specular highlight reflection intensity (0.0 to 1.0)
    pub specular_intensity: f32,
    /// Light source incidence angle in degrees (0 to 360)
    pub specular_angle_deg: f32,
    /// Deep fluid tinted backdrop color
    pub frosted_tint: Color,
    /// Subsurface fluid caustics simulation
    pub caustics_enabled: bool,
    /// Hydrodynamic fluid viscosity dampening (0.0 ultra-fluid to 1.0 viscous)
    pub fluid_viscosity: f32,
}

impl Default for HydroGlassEffect {
    fn default() -> Self {
        Self {
            blur_radius: 40.0,
            refraction_index: 1.44,
            surface_tension: 0.85,
            specular_intensity: 0.35,
            specular_angle_deg: 135.0,
            frosted_tint: Color::HYDRO_ACRYLIC_DARK,
            caustics_enabled: true,
            fluid_viscosity: 0.15,
        }
    }
}

impl HydroGlassEffect {
    /// Ultra-deep midnight hydro glass preset
    pub fn midnight_hydro() -> Self {
        Self {
            blur_radius: 48.0,
            refraction_index: 1.48,
            surface_tension: 0.90,
            specular_intensity: 0.40,
            specular_angle_deg: 135.0,
            frosted_tint: Color::rgba(0.035, 0.055, 0.098, 0.75),
            caustics_enabled: true,
            fluid_viscosity: 0.12,
        }
    }

    /// Crystal-clear water glass preset
    pub fn crystal_water() -> Self {
        Self {
            blur_radius: 32.0,
            refraction_index: 1.33,
            surface_tension: 0.95,
            specular_intensity: 0.50,
            specular_angle_deg: 120.0,
            frosted_tint: Color::rgba(0.1, 0.2, 0.35, 0.45),
            caustics_enabled: true,
            fluid_viscosity: 0.08,
        }
    }

    /// Generate CSS representation for Web previews & Wayland hybrid rendering
    pub fn to_css_style(&self) -> String {
        let angle_rad = self.specular_angle_deg.to_radians();
        let spec_x = (angle_rad.cos() * 1.5).round();
        let spec_y = (angle_rad.sin() * 1.5).round();
        
        let _border_gradient = format!(
            "linear-gradient({:.0}deg, rgba(255, 255, 255, {:.2}) 0%, rgba(255, 255, 255, 0.03) 60%, rgba(56, 189, 248, {:.2}) 100%)",
            self.specular_angle_deg,
            self.specular_intensity,
            self.specular_intensity * 0.6
        );

        let shadow = if self.caustics_enabled {
            format!(
                "0 20px 50px rgba(0, 0, 0, 0.45), 0 0 30px rgba(56, 189, 248, 0.12), inset {}px {}px 1.5px rgba(255, 255, 255, {:.2})",
                spec_x, spec_y, self.specular_intensity * 1.2
            )
        } else {
            "0 16px 40px rgba(0, 0, 0, 0.4)".to_string()
        };

        format!(
            "background: {}; backdrop-filter: blur({:.1}px) saturate(190%) contrast(108%); -webkit-backdrop-filter: blur({:.1}px) saturate(190%); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: {};",
            self.frosted_tint.to_css_rgba(),
            self.blur_radius,
            self.blur_radius,
            shadow
        )
    }
}

/// Dynamic liquid wave ripple effect
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HydroRipple {
    pub center: Point,
    pub current_radius: f32,
    pub max_radius: f32,
    pub amplitude: f32,
    pub wavelength: f32,
    pub decay_rate: f32,
}

impl HydroRipple {
    pub fn new(center: Point, max_radius: f32) -> Self {
        Self {
            center,
            current_radius: 0.0,
            max_radius,
            amplitude: 1.0,
            wavelength: 24.0,
            decay_rate: 0.05,
        }
    }

    /// Advance simulation by dt seconds
    pub fn step(&mut self, dt: f32, wave_speed_px_per_sec: f32) -> bool {
        self.current_radius += wave_speed_px_per_sec * dt;
        self.amplitude *= (-self.decay_rate * dt * 60.0).exp();
        self.current_radius < self.max_radius && self.amplitude > 0.01
    }
}

/// Physics-based Fluid Motion & Animation Curves
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum HydroMotionCurve {
    /// Organic damped spring (stiffness, damping, mass)
    Spring { stiffness: f32, damping: f32, mass: f32 },
    /// Liquid ripple wave curve
    Wave { frequency: f32, decay: f32, ripple_radius: f32 },
    /// Viscous fluid acceleration
    FluidViscous { viscosity: f32, acceleration: f32 },
    /// Classic smooth hydro cubic-bezier
    SmoothHydro,
}

impl HydroMotionCurve {
    pub const DEFAULT_SPRING: Self = Self::Spring {
        stiffness: 180.0,
        damping: 18.0,
        mass: 1.0,
    };

    pub const HIGH_REFRESH_240HZ: Self = Self::Spring {
        stiffness: 320.0,
        damping: 24.0,
        mass: 0.75,
    };
}
