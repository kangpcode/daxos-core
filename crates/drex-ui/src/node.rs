//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: NODE GRAPH & MODIFIERS
//! File: crates/drex-ui/src/node.rs
//! Purpose: Core tree node representation and fluent modifier chain
//! ============================================================================

use crate::gestures::GestureAction;
use crate::hydro::{HydroGlassEffect, HydroMotionCurve, HydroRipple};
use crate::types::{Alignment, Color, CornerRadii, DropShadow, EdgeInsets, Typography};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UiStyle {
    pub padding: EdgeInsets,
    pub background: Option<Color>,
    pub foreground: Option<Color>,
    pub corner_radii: CornerRadii,
    pub border_width: f32,
    pub border_color: Option<Color>,
    pub acrylic_blur: Option<f32>,
    pub hydro_glass: Option<HydroGlassEffect>,
    pub shadow: Option<DropShadow>,
    pub width: Option<f32>,
    pub height: Option<f32>,
    pub min_width: Option<f32>,
    pub max_width: Option<f32>,
    pub min_height: Option<f32>,
    pub max_height: Option<f32>,
    pub opacity: f32,
    pub animation: Option<HydroMotionCurve>,
}

impl Default for UiStyle {
    fn default() -> Self {
        Self {
            padding: EdgeInsets::ZERO,
            background: None,
            foreground: None,
            corner_radii: CornerRadii::all(0.0),
            border_width: 0.0,
            border_color: None,
            acrylic_blur: None,
            hydro_glass: None,
            shadow: None,
            width: None,
            height: None,
            min_width: None,
            max_width: None,
            min_height: None,
            max_height: None,
            opacity: 1.0,
            animation: None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum UiNodeType {
    Text { content: String, typo: Typography },
    TextField { placeholder: String, text: String, on_change_id: Option<String> },
    SecureField { placeholder: String, text: String, on_change_id: Option<String> },
    Button { label: String, action_id: String },
    VStack { spacing: f32, alignment: Alignment },
    HStack { spacing: f32, alignment: Alignment },
    ZStack { alignment: Alignment },
    Grid { columns: usize, spacing: f32 },
    LazyVGrid { columns: usize, spacing: f32 },
    LazyHGrid { rows: usize, spacing: f32 },
    ScrollView { horizontal: bool, vertical: bool },
    List { selectable: bool },
    ListItem { selected: bool },
    Section { header: Option<String>, footer: Option<String> },
    Image { glyph_id: String, width: f32, height: f32 },
    Spacer,
    Divider,
    Card { title: Option<String> },
    Toggle { label: String, is_on: bool, action_id: Option<String> },
    Slider { value: f32, min: f32, max: f32, action_id: Option<String> },
    Picker { title: String, selected_index: usize, options: Vec<String>, action_id: Option<String> },
    ProgressView { progress: Option<f32>, label: Option<String> },
    Gauge { value: f32, min: f32, max: f32, label: String },
    Badge { text: String, color: Color },
    Avatar { glyph_id: String, size: f32 },
    Canvas { draw_commands_count: usize },
    Window { title: String, traffic_lights: bool },
    ModalSheet { is_presented: bool, title: String },
    NavigationStack { current_title: String },
    Toolbar { title: String },
    SplitView { orientation_horizontal: bool, divider_position: f32 },
    CodeEditor { code: String, language: String, show_line_numbers: bool },
    CanvasSurface { width: f32, height: f32, target_fps: u32 },
    InspectorPane { title: String },
    BreadcrumbBar { segments: Vec<String> },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UiNode {
    pub node_id: String,
    pub node_type: UiNodeType,
    pub style: UiStyle,
    pub gestures: Vec<GestureAction>,
    pub on_appear_hook: Option<String>,
    pub on_disappear_hook: Option<String>,
    pub active_ripple: Option<HydroRipple>,
    pub children: Vec<UiNode>,
}

impl UiNode {
    pub fn new(node_type: UiNodeType) -> Self {
        Self {
            node_id: format!("node_{:08x}", rand_u32()),
            node_type,
            style: UiStyle::default(),
            gestures: Vec::new(),
            on_appear_hook: None,
            on_disappear_hook: None,
            active_ripple: None,
            children: Vec::new(),
        }
    }

    pub fn id(mut self, custom_id: impl Into<String>) -> Self {
        self.node_id = custom_id.into();
        self
    }

    pub fn with_child(mut self, child: UiNode) -> Self {
        self.children.push(child);
        self
    }

    pub fn with_children(mut self, children: Vec<UiNode>) -> Self {
        self.children.extend(children);
        self
    }

    pub fn padding(mut self, p: f32) -> Self {
        self.style.padding = EdgeInsets::all(p);
        self
    }

    pub fn padding_insets(mut self, insets: EdgeInsets) -> Self {
        self.style.padding = insets;
        self
    }

    pub fn padding_symmetric(mut self, vertical: f32, horizontal: f32) -> Self {
        self.style.padding = EdgeInsets::symmetric(vertical, horizontal);
        self
    }

    pub fn background(mut self, color: Color) -> Self {
        self.style.background = Some(color);
        self
    }

    pub fn foreground_color(mut self, color: Color) -> Self {
        self.style.foreground = Some(color);
        self
    }

    pub fn corner_radius(mut self, radius: f32) -> Self {
        self.style.corner_radii = CornerRadii::all(radius);
        self
    }

    pub fn border(mut self, width: f32, color: Color) -> Self {
        self.style.border_width = width;
        self.style.border_color = Some(color);
        self
    }

    pub fn shadow(mut self, color: Color, radius: f32, x: f32, y: f32) -> Self {
        self.style.shadow = Some(DropShadow {
            color,
            radius,
            offset_x: x,
            offset_y: y,
        });
        self
    }

    pub fn opacity(mut self, alpha: f32) -> Self {
        self.style.opacity = alpha;
        self
    }

    pub fn frame(mut self, w: Option<f32>, h: Option<f32>) -> Self {
        self.style.width = w;
        self.style.height = h;
        self
    }

    pub fn frame_min_max(
        mut self,
        min_w: Option<f32>,
        max_w: Option<f32>,
        min_h: Option<f32>,
        max_h: Option<f32>,
    ) -> Self {
        self.style.min_width = min_w;
        self.style.max_width = max_w;
        self.style.min_height = min_h;
        self.style.max_height = max_h;
        self
    }

    /// Acrylic Frosted Glass (Fluent / macOS Style)
    pub fn glass_acrylic(mut self, blur_radius: f32) -> Self {
        self.style.acrylic_blur = Some(blur_radius);
        self.style.background = Some(Color::ACRYLIC_BACKGROUND);
        self.style.border_color = Some(Color::ACRYLIC_BORDER);
        self.style.border_width = 1.0;
        self
    }

    /// Hydro-Glass Liquid Refractive Architecture (DAXOS Next-Gen Signature)
    pub fn hydro_glass(mut self, effect: HydroGlassEffect) -> Self {
        self.style.hydro_glass = Some(effect.clone());
        self.style.background = Some(effect.frosted_tint);
        self.style.border_color = Some(Color::rgba(1.0, 1.0, 1.0, effect.specular_intensity * 0.5));
        self.style.border_width = 1.0;
        self.style.acrylic_blur = Some(effect.blur_radius);
        self
    }

    pub fn animation(mut self, curve: HydroMotionCurve) -> Self {
        self.style.animation = Some(curve);
        self
    }

    pub fn on_tap_gesture(mut self, handler_id: impl Into<String>) -> Self {
        self.gestures.push(GestureAction::tap(handler_id));
        self
    }

    pub fn on_hover(mut self, handler_id: impl Into<String>) -> Self {
        self.gestures.push(GestureAction::hover(handler_id));
        self
    }

    pub fn on_appear(mut self, hook_id: impl Into<String>) -> Self {
        self.on_appear_hook = Some(hook_id.into());
        self
    }

    pub fn on_disappear(mut self, hook_id: impl Into<String>) -> Self {
        self.on_disappear_hook = Some(hook_id.into());
        self
    }
}

static SEED: std::sync::atomic::AtomicU32 = std::sync::atomic::AtomicU32::new(0x240A_D901);
fn rand_u32() -> u32 {
    let mut val = SEED.fetch_add(0x45D9F3B, std::sync::atomic::Ordering::Relaxed);
    val ^= val << 13;
    val ^= val >> 17;
    val ^= val << 5;
    val
}
