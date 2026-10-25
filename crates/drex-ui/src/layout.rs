//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: DECLARATIVE LAYOUT CONTAINERS
//! File: crates/drex-ui/src/layout.rs
//! Purpose: Structural containers equivalent to SwiftUI & ArkUI
//! ============================================================================

use crate::node::{UiNode, UiNodeType};
use crate::types::Alignment;

#[allow(non_snake_case)]
pub fn VStack(spacing: f32, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::VStack {
        spacing,
        alignment: Alignment::Leading,
    })
    .with_children(children)
}

#[allow(non_snake_case)]
pub fn HStack(spacing: f32, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::HStack {
        spacing,
        alignment: Alignment::Center,
    })
    .with_children(children)
}

#[allow(non_snake_case)]
pub fn ZStack(children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::ZStack {
        alignment: Alignment::Center,
    })
    .with_children(children)
}

#[allow(non_snake_case)]
pub fn Grid(columns: usize, spacing: f32, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::Grid { columns, spacing }).with_children(children)
}

#[allow(non_snake_case)]
pub fn LazyVGrid(columns: usize, spacing: f32, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::LazyVGrid { columns, spacing }).with_children(children)
}

#[allow(non_snake_case)]
pub fn LazyHGrid(rows: usize, spacing: f32, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::LazyHGrid { rows, spacing }).with_children(children)
}

#[allow(non_snake_case)]
pub fn ScrollView(horizontal: bool, vertical: bool, child: UiNode) -> UiNode {
    UiNode::new(UiNodeType::ScrollView { horizontal, vertical }).with_child(child)
}

#[allow(non_snake_case)]
pub fn List(children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::List { selectable: true }).with_children(children)
}

#[allow(non_snake_case)]
pub fn ListItem(child: UiNode, selected: bool) -> UiNode {
    UiNode::new(UiNodeType::ListItem { selected }).with_child(child)
}

#[allow(non_snake_case)]
pub fn Section(header: Option<&str>, footer: Option<&str>, children: Vec<UiNode>) -> UiNode {
    UiNode::new(UiNodeType::Section {
        header: header.map(|s| s.to_string()),
        footer: footer.map(|s| s.to_string()),
    })
    .with_children(children)
}

#[allow(non_snake_case)]
pub fn ForEach<T, F>(items: &[T], builder: F) -> Vec<UiNode>
where
    F: Fn(&T) -> UiNode,
{
    items.iter().map(builder).collect()
}

#[allow(non_snake_case)]
pub fn Spacer() -> UiNode {
    UiNode::new(UiNodeType::Spacer)
}

#[allow(non_snake_case)]
pub fn Divider() -> UiNode {
    UiNode::new(UiNodeType::Divider)
}

#[allow(non_snake_case)]
pub fn Center(child: UiNode) -> UiNode {
    ZStack(vec![child])
}

#[allow(non_snake_case)]
pub fn Container(child: UiNode) -> UiNode {
    UiNode::new(UiNodeType::ZStack {
        alignment: Alignment::Center,
    })
    .with_child(child)
}

#[allow(non_snake_case)]
pub fn WindowChrome(title: &str, traffic_lights: bool, child: UiNode) -> UiNode {
    UiNode::new(UiNodeType::Window {
        title: title.to_string(),
        traffic_lights,
    })
    .with_child(child)
}


