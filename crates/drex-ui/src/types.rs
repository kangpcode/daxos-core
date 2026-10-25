//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: TYPES & GEOMETRY
//! File: crates/drex-ui/src/types.rs
//! Purpose: Color, geometry, typography, gradients, shadows, and design tokens
//! ============================================================================

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Color {
    pub r: f32,
    pub g: f32,
    pub b: f32,
    pub a: f32,
}

impl Color {
    pub const fn rgba(r: f32, g: f32, b: f32, a: f32) -> Self {
        Self { r, g, b, a }
    }

    pub const fn rgb(r: f32, g: f32, b: f32) -> Self {
        Self { r, g, b, a: 1.0 }
    }

    pub fn hex(hex_str: &str) -> Self {
        let clean = hex_str.trim_start_matches('#');
        if clean.len() == 6 {
            let r = u8::from_str_radix(&clean[0..2], 16).unwrap_or(0) as f32 / 255.0;
            let g = u8::from_str_radix(&clean[2..4], 16).unwrap_or(0) as f32 / 255.0;
            let b = u8::from_str_radix(&clean[4..6], 16).unwrap_or(0) as f32 / 255.0;
            Self::rgba(r, g, b, 1.0)
        } else if clean.len() == 8 {
            let r = u8::from_str_radix(&clean[0..2], 16).unwrap_or(0) as f32 / 255.0;
            let g = u8::from_str_radix(&clean[2..4], 16).unwrap_or(0) as f32 / 255.0;
            let b = u8::from_str_radix(&clean[4..6], 16).unwrap_or(0) as f32 / 255.0;
            let a = u8::from_str_radix(&clean[6..8], 16).unwrap_or(255) as f32 / 255.0;
            Self::rgba(r, g, b, a)
        } else {
            Self::rgba(1.0, 1.0, 1.0, 1.0)
        }
    }

    pub fn to_hex(&self) -> String {
        format!(
            "#{:02X}{:02X}{:02X}{:02X}",
            (self.r * 255.0).round() as u8,
            (self.g * 255.0).round() as u8,
            (self.b * 255.0).round() as u8,
            (self.a * 255.0).round() as u8
        )
    }

    pub fn to_css_rgba(&self) -> String {
        format!("rgba({}, {}, {}, {:.3})",
            (self.r * 255.0).round() as u8,
            (self.g * 255.0).round() as u8,
            (self.b * 255.0).round() as u8,
            self.a
        )
    }

    pub const CLEAR: Self = Self::rgba(0.0, 0.0, 0.0, 0.0);
    pub const WHITE: Self = Self::rgba(1.0, 1.0, 1.0, 1.0);
    pub const BLACK: Self = Self::rgba(0.0, 0.0, 0.0, 1.0);
    pub const BLUE: Self = Self::rgba(0.0, 0.478, 1.0, 1.0);
    pub const CYAN: Self = Self::rgba(0.188, 0.820, 0.929, 1.0);
    pub const TEAL: Self = Self::rgba(0.188, 0.820, 0.929, 1.0);
    pub const GREEN: Self = Self::rgba(0.196, 0.843, 0.294, 1.0);
    pub const RED: Self = Self::rgba(1.0, 0.231, 0.188, 1.0);
    pub const ORANGE: Self = Self::rgba(1.0, 0.584, 0.0, 1.0);
    pub const PURPLE: Self = Self::rgba(0.686, 0.322, 0.871, 1.0);

    // Semantic DreXUI Hydro-Glass Tokens
    pub const HYDRO_ACRYLIC_DARK: Self = Self::rgba(0.047, 0.071, 0.125, 0.68);
    pub const HYDRO_ACRYLIC_LIGHT: Self = Self::rgba(1.0, 1.0, 1.0, 0.15);
    pub const HYDRO_SPECULAR_EDGE: Self = Self::rgba(1.0, 1.0, 1.0, 0.24);
    pub const HYDRO_CAUSTIC_GLOW: Self = Self::rgba(0.2, 0.6, 1.0, 0.35);
    pub const ACRYLIC_BACKGROUND: Self = Self::rgba(0.078, 0.098, 0.141, 0.72);
    pub const ACRYLIC_BORDER: Self = Self::rgba(1.0, 1.0, 1.0, 0.12);
    pub const TEXT_PRIMARY: Self = Self::rgba(0.96, 0.97, 0.98, 1.0);
    pub const TEXT_SECONDARY: Self = Self::rgba(0.65, 0.68, 0.75, 1.0);
    pub const TEXT_TERTIARY: Self = Self::rgba(0.45, 0.48, 0.55, 1.0);
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Point {
    pub x: f32,
    pub y: f32,
}

impl Point {
    pub const ZERO: Self = Self { x: 0.0, y: 0.0 };
    pub const fn new(x: f32, y: f32) -> Self {
        Self { x, y }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Size {
    pub width: f32,
    pub height: f32,
}

impl Size {
    pub const ZERO: Self = Self { width: 0.0, height: 0.0 };
    pub const fn new(width: f32, height: f32) -> Self {
        Self { width, height }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Rect {
    pub origin: Point,
    pub size: Size,
}

impl Rect {
    pub const ZERO: Self = Self { origin: Point::ZERO, size: Size::ZERO };
    pub const fn new(x: f32, y: f32, width: f32, height: f32) -> Self {
        Self {
            origin: Point::new(x, y),
            size: Size::new(width, height),
        }
    }

    pub fn contains(&self, p: Point) -> bool {
        p.x >= self.origin.x && p.x <= self.origin.x + self.size.width &&
        p.y >= self.origin.y && p.y <= self.origin.y + self.size.height
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct EdgeInsets {
    pub top: f32,
    pub leading: f32,
    pub bottom: f32,
    pub trailing: f32,
}

impl EdgeInsets {
    pub const ZERO: Self = Self { top: 0.0, leading: 0.0, bottom: 0.0, trailing: 0.0 };
    pub const fn all(val: f32) -> Self {
        Self { top: val, leading: val, bottom: val, trailing: val }
    }
    pub const fn symmetric(vertical: f32, horizontal: f32) -> Self {
        Self { top: vertical, leading: horizontal, bottom: vertical, trailing: horizontal }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct CornerRadii {
    pub top_leading: f32,
    pub top_trailing: f32,
    pub bottom_leading: f32,
    pub bottom_trailing: f32,
}

impl CornerRadii {
    pub const fn all(r: f32) -> Self {
        Self { top_leading: r, top_trailing: r, bottom_leading: r, bottom_trailing: r }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Typography {
    LargeTitle,
    Title,
    Headline,
    Subheadline,
    Body,
    Callout,
    Footnote,
    Caption,
}

impl Typography {
    pub fn font_size(&self) -> f32 {
        match self {
            Self::LargeTitle => 34.0,
            Self::Title => 24.0,
            Self::Headline => 18.0,
            Self::Subheadline => 15.0,
            Self::Body => 14.0,
            Self::Callout => 13.0,
            Self::Footnote => 12.0,
            Self::Caption => 11.0,
        }
    }

    pub fn font_weight(&self) -> u16 {
        match self {
            Self::LargeTitle => 700,
            Self::Title => 700,
            Self::Headline => 600,
            Self::Subheadline => 500,
            Self::Body => 400,
            Self::Callout => 400,
            Self::Footnote => 400,
            Self::Caption => 400,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Alignment {
    TopLeading,
    Top,
    TopTrailing,
    Leading,
    Center,
    Trailing,
    BottomLeading,
    Bottom,
    BottomTrailing,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LinearGradient {
    pub start_point: Point,
    pub end_point: Point,
    pub stops: Vec<(f32, Color)>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct RadialGradient {
    pub center: Point,
    pub start_radius: f32,
    pub end_radius: f32,
    pub stops: Vec<(f32, Color)>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DropShadow {
    pub color: Color,
    pub radius: f32,
    pub offset_x: f32,
    pub offset_y: f32,
}
