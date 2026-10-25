//! ============================================================================
//! DAXOS DreXSDK: DREXAPP LIFECYCLE & DECLARATIVE RUNTIME BUILDER
//! File: crates/drex-sdk/src/app.rs
//! Purpose: Top-level application builder with built-in anti-crash protection
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS
//! ============================================================================

use crate::anticrash::CrashShield;
use drex_ui::node::UiNode;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppMetadata {
    pub bundle_id: String,
    pub title: String,
    pub version: String,
    pub window_width: u32,
    pub window_height: u32,
    pub acrylic_blur_radius: f32,
}

pub struct DreXApp {
    metadata: AppMetadata,
    shield: CrashShield,
    root_node: Option<UiNode>,
}

impl DreXApp {
    pub fn new(bundle_id: impl Into<String>, title: impl Into<String>) -> Self {
        let b_id = bundle_id.into();
        let t_str = title.into();
        let shield = CrashShield::new(&b_id);

        Self {
            metadata: AppMetadata {
                bundle_id: b_id,
                title: t_str,
                version: "1.10.2026".to_string(),
                window_width: 840,
                window_height: 560,
                acrylic_blur_radius: 36.0,
            },
            shield,
            root_node: None,
        }
    }

    pub fn window_size(mut self, width: u32, height: u32) -> Self {
        self.metadata.window_width = width;
        self.metadata.window_height = height;
        self
    }

    pub fn acrylic_blur(mut self, radius: f32) -> Self {
        self.metadata.acrylic_blur_radius = radius;
        self
    }

    pub fn root_view(mut self, node: UiNode) -> Self {
        self.root_node = Some(node);
        self
    }

    pub fn run_protected<F, R>(&self, action: F) -> Result<R, crate::anticrash::CrashReport>
    where
        F: FnOnce() -> R,
    {
        self.shield.execute(action)
    }

    pub fn metadata(&self) -> &AppMetadata {
        &self.metadata
    }

    pub fn has_root_view(&self) -> bool {
        self.root_node.is_some()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use drex_ui::components::Text;

    #[test]
    fn test_drex_app_initialization() {
        let app = DreXApp::new("org.daxos.test", "Test App")
            .window_size(1024, 768)
            .root_view(Text("Hello DreXSDK"));

        assert_eq!(app.metadata().window_width, 1024);
        assert_eq!(app.metadata().window_height, 768);
        assert!(app.has_root_view());

        let res = app.run_protected(|| 42);
        assert_eq!(res.unwrap(), 42);
    }
}
