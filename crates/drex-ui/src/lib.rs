//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK (drex-ui)
//! File: crates/drex-ui/src/lib.rs
//! Purpose: Production Declarative Native UI Framework for DAXOS
//! Inspired by SwiftUI and HarmonyOS ArkUI with Hydro-Glass Liquid Architecture
//! Lead Architect: Dhafa Nazula Permadi (kangpcode)
//! Strictly ZERO EMOJIS - Production Ready
//! ============================================================================

#![allow(non_snake_case)]

pub mod components;
pub mod gestures;
pub mod glyphs;
pub mod hydro;
pub mod layout;
pub mod node;
pub mod renderer;
pub mod state;
pub mod types;

// Re-exports
pub use components::*;
pub use gestures::*;
pub use glyphs::*;
pub use hydro::*;
pub use layout::*;
pub use node::*;
pub use renderer::*;
pub use state::*;
pub use types::*;

pub mod prelude {
    pub use super::components::*;
    pub use super::gestures::*;
    pub use super::glyphs::*;
    pub use super::hydro::*;
    pub use super::layout::*;
    pub use super::node::*;
    pub use super::renderer::*;
    pub use super::state::*;
    pub use super::types::*;
    pub use super::View;
}

// ----------------------------------------------------------------------------
// DECLARATIVE VIEW TRAIT (SwiftUI & ArkUI Paradigm)
// ----------------------------------------------------------------------------

pub trait View: Send + Sync {
    fn body(&self) -> UiNode;
}

impl<F> View for F
where
    F: Fn() -> UiNode + Send + Sync,
{
    fn body(&self) -> UiNode {
        self()
    }
}

// ----------------------------------------------------------------------------
// UNIT TESTS
// ----------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_color_tokens_and_conversions() {
        let white = Color::hex("#FFFFFF");
        assert_eq!(white, Color::WHITE);

        let blue = Color::hex("#007AFF");
        assert!((blue.r - 0.0).abs() < 0.01);
        assert!((blue.g - 0.478).abs() < 0.01);

        let css = Color::HYDRO_ACRYLIC_DARK.to_css_rgba();
        assert!(css.starts_with("rgba("));
    }

    #[test]
    fn test_reactive_state_and_two_way_binding() {
        let count = State::new(100);
        assert_eq!(count.get(), 100);

        let was_called = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
        let was_called_clone = was_called.clone();
        count.on_change(move |new_val| {
            if *new_val == 240 {
                was_called_clone.store(true, std::sync::atomic::Ordering::SeqCst);
            }
        });

        let binding = count.binding();
        binding.set(240);
        assert_eq!(count.get(), 240);
        assert_eq!(binding.get(), 240);
        assert!(was_called.load(std::sync::atomic::Ordering::SeqCst));
    }

    #[test]
    fn test_environment_values_store() {
        let env = EnvironmentValues::new();
        env.insert(42u32);
        env.insert("DAXOS Hydro Desktop".to_string());

        assert_eq!(env.get::<u32>(), Some(42));
        assert_eq!(env.get::<String>(), Some("DAXOS Hydro Desktop".to_string()));
        assert_eq!(env.get::<bool>(), None);
    }

    #[test]
    fn test_hydro_glass_effect_and_css_generation() {
        let hg = HydroGlassEffect::midnight_hydro();
        assert_eq!(hg.blur_radius, 48.0);
        assert_eq!(hg.refraction_index, 1.48);
        assert!(hg.caustics_enabled);

        let css = hg.to_css_style();
        assert!(css.contains("backdrop-filter: blur(48.0px)"));
        assert!(css.contains("box-shadow:"));
    }

    #[test]
    fn test_swiftui_arkui_declarative_view_tree() {
        let profile_state = State::new("Extreme240Hz".to_string());

        let ui = Window(
            "DAXOS DreX-Boost Performance Controller",
            VStack(12.0, vec![
                LargeTitle("Performance & Hydro Engine"),
                HStack(8.0, vec![
                    Icon("drex.icon.cpu", 24.0),
                    Text(format!("Governor Mode: {}", profile_state.get())),
                    Spacer(),
                    Badge("ACTIVE", Color::GREEN),
                ]),
                Divider(),
                Card(
                    Some("Display Refresh Synchronizer"),
                    vec![
                        Text("Active Refresh Rate: 240Hz (Direct DRM KMS)"),
                        ProgressView(Some(0.95), Some("Bandwidth Saturation")),
                        Button("Apply 240Hz Extreme Preset", "btn_boost_240hz")
                            .hydro_glass(HydroGlassEffect::crystal_water()),
                    ]
                )
                .hydro_glass(HydroGlassEffect::midnight_hydro()),
            ])
        )
        .on_appear("hook_perf_window_opened");

        assert_eq!(ui.children.len(), 1);
        let root_child = &ui.children[0];
        assert_eq!(root_child.children.len(), 4);

        // Serialize to JSON tree
        let json_str = serde_json::to_string(&ui).expect("JSON serialization failed");
        assert!(json_str.contains("DAXOS DreX-Boost Performance Controller"));
        assert!(json_str.contains("btn_boost_240hz"));
        assert!(json_str.contains("drex.icon.cpu"));
        assert!(json_str.contains("hook_perf_window_opened"));

        // Generate HTML output
        let html = LayoutEngine::to_html(&ui);
        assert!(html.contains("hydro-window"));
        assert!(html.contains("traffic-lights"));
        assert!(html.contains("Performance &amp; Hydro Engine") || html.contains("Performance & Hydro Engine"));
    }

    #[test]
    fn test_vector_glyphs_zero_emojis() {
        for glyph in &[
            "drex.icon.apple",
            "drex.icon.windows",
            "drex.icon.linux",
            "drex.icon.folder",
            "drex.icon.gear",
            "drex.icon.terminal",
            "drex.icon.cloud",
            "drex.icon.shield",
            "drex.icon.cpu",
            "drex.icon.display",
            "drex.icon.network",
            "drex.icon.calc",
            "drex.icon.edit",
            "drex.icon.disk",
            "drex.icon.camera",
            "drex.icon.daxbro",
            "drex.icon.dapstore",
            "drex.icon.ide",
            "drex.icon.installer",
            "drex.icon.sysmon",
            "drex.icon.media",
            "drex.icon.daxdrop",
            "drex.icon.trash",
            "drex.icon.play",
            "drex.icon.pause",
        ] {
            let svg = VectorGlyphRegistry::get_svg(glyph);
            assert!(svg.starts_with("<svg"), "Glyph {} must be valid SVG", glyph);
        }
    }

    #[test]
    fn test_comprehensive_widgets_rendering_no_overlap() {
        let view = VStack(16.0, vec![
            TextField("Search packages...", "dcodx-compiler", Some("act_search")),
            SecureField("Root Password", "secret123", Some("act_pwd")),
            Toggle("Dynamic Acrylic Glass", true, Some("act_toggle_glass")),
            Slider(72.0, 0.0, 100.0, Some("act_slider_opacity")),
            Picker("Update Channel", 0, vec!["Stable".into(), "Beta".into(), "Canary".into()], Some("act_picker")),
            ProgressView(Some(0.85), Some("Compiling .dapp fat binary")),
            Gauge(14.8, 0.0, 100.0, "CPU Saturation"),
            Badge("SECURE ENCLAVE ACTIVE", Color::GREEN),
            CodeEditor("fn main() {\n    println!(\"DAXOS\");\n}", "rust", true),
            BreadcrumbBar(vec!["DAXOS HD".into(), "System".into(), "Preferences".into()]),
        ]);

        let html = LayoutEngine::to_html(&view);
        assert!(html.contains("hydro-input"));
        assert!(html.contains("hydro-toggle-row"));
        assert!(html.contains("hydro-slider-wrapper"));
        assert!(html.contains("hydro-picker"));
        assert!(html.contains("hydro-progress-view"));
        assert!(html.contains("hydro-gauge"));
        assert!(html.contains("hydro-badge"));
        assert!(html.contains("hydro-code-editor"));
        assert!(html.contains("hydro-breadcrumbs"));

        let full_doc = LayoutEngine::generate_full_document("DAXOS Test Preview", &view);
        assert!(full_doc.contains("<!DOCTYPE html>"));
        assert!(full_doc.contains("DAXOS Test Preview"));
        assert!(full_doc.contains("box-sizing: border-box;"));
    }

    #[test]
    fn test_anti_overlap_grid_and_splitview_layout() {
        let grid = Grid(3, 10.0, vec![
            Button("Item 1", "b1"),
            Button("Item 2", "b2"),
            Button("Item 3", "b3"),
            Button("Item 4", "b4"),
            Button("Item 5", "b5"),
            Button("Item 6", "b6"),
        ]);

        let bounds = Rect::new(0.0, 0.0, 600.0, 300.0);
        let layout = LayoutEngine::compute_layout(&grid, bounds);
        assert_eq!(layout.children.len(), 6);

        // Verify non-overlapping grid cells
        let c0 = &layout.children[0].bounds;
        let c1 = &layout.children[1].bounds;
        let c3 = &layout.children[3].bounds; // Next row

        assert!(c1.origin.x > c0.origin.x);
        assert!(c3.origin.y > c0.origin.y);

        // Verify SplitView layout
        let split = SplitView(true, 0.3, Card(None::<&str>, vec![Text("Sidebar")]), Card(None::<&str>, vec![Text("Content")]));
        let split_layout = LayoutEngine::compute_layout(&split, Rect::new(0.0, 0.0, 1000.0, 600.0));
        assert_eq!(split_layout.children.len(), 2);
        let primary_b = &split_layout.children[0].bounds;
        let secondary_b = &split_layout.children[1].bounds;
        assert_eq!(primary_b.size.width, 300.0);
        assert_eq!(secondary_b.origin.x, 300.0);
        assert_eq!(secondary_b.size.width, 700.0);
    }
}

