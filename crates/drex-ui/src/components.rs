//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: DECLARATIVE COMPONENTS
//! File: crates/drex-ui/src/components.rs
//! Purpose: Built-in component primitives matching SwiftUI and ArkUI standards
//! ============================================================================

use crate::node::{UiNode, UiNodeType};
use crate::types::{Color, Typography};

#[allow(non_snake_case)]
pub fn Text(content: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Text {
        content: content.into(),
        typo: Typography::Body,
    })
}

#[allow(non_snake_case)]
pub fn LargeTitle(content: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Text {
        content: content.into(),
        typo: Typography::LargeTitle,
    })
}

#[allow(non_snake_case)]
pub fn Title(content: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Text {
        content: content.into(),
        typo: Typography::Title,
    })
}

#[allow(non_snake_case)]
pub fn Headline(content: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Text {
        content: content.into(),
        typo: Typography::Headline,
    })
}

#[allow(non_snake_case)]
pub fn Subheadline(content: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Text {
        content: content.into(),
        typo: Typography::Subheadline,
    })
}

#[allow(non_snake_case)]
pub fn Caption(content: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Text {
        content: content.into(),
        typo: Typography::Caption,
    })
}

#[allow(non_snake_case)]
pub fn TextField(
    placeholder: impl Into<String>,
    text: impl Into<String>,
    on_change_id: Option<impl Into<String>>,
) -> UiNode {
    UiNode::new(UiNodeType::TextField {
        placeholder: placeholder.into(),
        text: text.into(),
        on_change_id: on_change_id.map(|s| s.into()),
    })
    .padding(10.0)
    .corner_radius(8.0)
    .background(Color::rgba(0.08, 0.12, 0.20, 0.6))
    .border(1.0, Color::ACRYLIC_BORDER)
}

#[allow(non_snake_case)]
pub fn SecureField(
    placeholder: impl Into<String>,
    text: impl Into<String>,
    on_change_id: Option<impl Into<String>>,
) -> UiNode {
    UiNode::new(UiNodeType::SecureField {
        placeholder: placeholder.into(),
        text: text.into(),
        on_change_id: on_change_id.map(|s| s.into()),
    })
    .padding(10.0)
    .corner_radius(8.0)
    .background(Color::rgba(0.08, 0.12, 0.20, 0.6))
    .border(1.0, Color::ACRYLIC_BORDER)
}

#[allow(non_snake_case)]
pub fn Button(label: impl Into<String>, action_id: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Button {
        label: label.into(),
        action_id: action_id.into(),
    })
    .padding_symmetric(8.0, 16.0)
    .corner_radius(8.0)
    .background(Color::BLUE)
    .foreground_color(Color::WHITE)
}

#[allow(non_snake_case)]
pub fn Toggle(
    label: impl Into<String>,
    is_on: bool,
    action_id: Option<impl Into<String>>,
) -> UiNode {
    UiNode::new(UiNodeType::Toggle {
        label: label.into(),
        is_on,
        action_id: action_id.map(|s| s.into()),
    })
}

#[allow(non_snake_case)]
pub fn Slider(
    value: f32,
    min: f32,
    max: f32,
    action_id: Option<impl Into<String>>,
) -> UiNode {
    UiNode::new(UiNodeType::Slider {
        value,
        min,
        max,
        action_id: action_id.map(|s| s.into()),
    })
}

#[allow(non_snake_case)]
pub fn Picker(
    title: impl Into<String>,
    selected_index: usize,
    options: Vec<String>,
    action_id: Option<impl Into<String>>,
) -> UiNode {
    UiNode::new(UiNodeType::Picker {
        title: title.into(),
        selected_index,
        options,
        action_id: action_id.map(|s| s.into()),
    })
}

#[allow(non_snake_case)]
pub fn ProgressView(progress: Option<f32>, label: Option<impl Into<String>>) -> UiNode {
    UiNode::new(UiNodeType::ProgressView {
        progress,
        label: label.map(|s| s.into()),
    })
}

#[allow(non_snake_case)]
pub fn Gauge(value: f32, min: f32, max: f32, label: impl Into<String>) -> UiNode {
    UiNode::new(UiNodeType::Gauge {
        value,
        min,
        max,
        label: label.into(),
    })
}

#[allow(non_snake_case)]
pub fn Badge(text: impl Into<String>, color: Color) -> UiNode {
    UiNode::new(UiNodeType::Badge {
        text: text.into(),
        color,
    })
    .padding_symmetric(3.0, 8.0)
    .corner_radius(12.0)
}

#[allow(non_snake_case)]
pub fn Avatar(glyph_id: impl Into<String>, size: f32) -> UiNode {
    UiNode::new(UiNodeType::Avatar {
        glyph_id: glyph_id.into(),
        size,
    })
}

#[allow(non_snake_case)]
pub fn Icon(glyph_id: impl Into<String>, size: f32) -> UiNode {
    UiNode::new(UiNodeType::Image {
        glyph_id: glyph_id.into(),
        width: size,
        height: size,
    })
}

#[allow(non_snake_case)]
pub fn Card(title: Option<impl Into<String>>, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::Card {
        title: title.map(|t| t.into()),
    })
    .with_children(children)
    .glass_acrylic(36.0)
    .corner_radius(16.0)
    .padding(16.0)
}

#[allow(non_snake_case)]
pub fn Window(title: impl Into<String>, body: UiNode) -> UiNode {
    UiNode::new(UiNodeType::Window {
        title: title.into(),
        traffic_lights: true,
    })
    .with_child(body)
    .glass_acrylic(48.0)
    .corner_radius(20.0)
}

#[allow(non_snake_case)]
pub fn ModalSheet(is_presented: bool, title: impl Into<String>, content: UiNode) -> UiNode {
    UiNode::new(UiNodeType::ModalSheet {
        is_presented,
        title: title.into(),
    })
    .with_child(content)
}

#[allow(non_snake_case)]
pub fn NavigationStack(current_title: impl Into<String>, root_view: UiNode) -> UiNode {
    UiNode::new(UiNodeType::NavigationStack {
        current_title: current_title.into(),
    })
    .with_child(root_view)
}

#[allow(non_snake_case)]
pub fn Toolbar(title: impl Into<String>, items: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::Toolbar {
        title: title.into(),
    })
    .with_children(items)
}

#[allow(non_snake_case)]
pub fn SplitView(
    orientation_horizontal: bool,
    divider_position: f32,
    primary: UiNode,
    secondary: UiNode,
) -> UiNode {
    UiNode::new(UiNodeType::SplitView {
        orientation_horizontal,
        divider_position,
    })
    .with_children(vec![primary, secondary])
}

#[allow(non_snake_case)]
pub fn CodeEditor(
    code: impl Into<String>,
    language: impl Into<String>,
    show_line_numbers: bool,
) -> UiNode {
    UiNode::new(UiNodeType::CodeEditor {
        code: code.into(),
        language: language.into(),
        show_line_numbers,
    })
    .background(Color::hex("#0D1117"))
    .corner_radius(8.0)
    .border(1.0, Color::ACRYLIC_BORDER)
}

#[allow(non_snake_case)]
pub fn CanvasSurface(width: f32, height: f32, target_fps: u32) -> UiNode {
    UiNode::new(UiNodeType::CanvasSurface {
        width,
        height,
        target_fps,
    })
    .corner_radius(12.0)
    .background(Color::rgba(0.04, 0.06, 0.10, 0.9))
}

#[allow(non_snake_case)]
pub fn InspectorPane(title: impl Into<String>, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::InspectorPane {
        title: title.into(),
    })
    .with_children(children)
    .padding(12.0)
    .background(Color::rgba(0.08, 0.10, 0.16, 0.8))
    .border(1.0, Color::ACRYLIC_BORDER)
}

#[allow(non_snake_case)]
pub fn BreadcrumbBar(segments: Vec<String>) -> UiNode {
    UiNode::new(UiNodeType::BreadcrumbBar { segments })
        .padding_symmetric(6.0, 12.0)
        .background(Color::rgba(0.05, 0.07, 0.12, 0.7))
}
