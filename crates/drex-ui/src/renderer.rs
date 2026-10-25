//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: RENDERER & LAYOUT ENGINE
//! File: crates/drex-ui/src/renderer.rs
//! Purpose: Headless layout solver, Wayland render list, and HTML/CSS generator
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS - Production Grade
//! ============================================================================

use crate::glyphs::VectorGlyphRegistry;
use crate::node::{UiNode, UiNodeType};
use crate::types::Rect;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LayoutBox {
    pub node_id: String,
    pub bounds: Rect,
    pub children: Vec<LayoutBox>,
}

pub struct LayoutEngine;

impl LayoutEngine {
    /// Estimate intrinsic dimensions (width, height) of a node to avoid layout squishing & overlap
    pub fn estimate_node_size(node: &UiNode, parent_w: f32) -> (f32, f32) {
        let width = if let Some(w) = node.style.width {
            w
        } else {
            match &node.node_type {
                UiNodeType::Text { content, .. } => (content.len() as f32 * 7.5 + 8.0).min(parent_w),
                UiNodeType::Button { label, .. } => (label.len() as f32 * 8.0 + 32.0).max(64.0).min(parent_w),
                UiNodeType::Badge { text, .. } => text.len() as f32 * 7.0 + 20.0,
                UiNodeType::Avatar { size, .. } => *size,
                UiNodeType::Image { width, .. } => *width,
                UiNodeType::Divider | UiNodeType::Spacer => parent_w,
                _ => parent_w,
            }
        };

        let height = if let Some(h) = node.style.height {
            h
        } else {
            match &node.node_type {
                UiNodeType::Text { content, typo } => {
                    let fs = typo.font_size();
                    let line_count = content.lines().count().max(1) as f32;
                    line_count * (fs * 1.45)
                }
                UiNodeType::Button { .. } => 38.0,
                UiNodeType::TextField { .. } | UiNodeType::SecureField { .. } => 42.0,
                UiNodeType::Toggle { .. } => 34.0,
                UiNodeType::Slider { .. } => 48.0,
                UiNodeType::Picker { .. } => 38.0,
                UiNodeType::ProgressView { .. } => 40.0,
                UiNodeType::Gauge { .. } => 60.0,
                UiNodeType::Badge { .. } => 24.0,
                UiNodeType::Avatar { size, .. } => *size,
                UiNodeType::Image { height, .. } => *height,
                UiNodeType::Divider => 13.0,
                UiNodeType::Spacer => 12.0,
                UiNodeType::BreadcrumbBar { .. } => 34.0,
                UiNodeType::Toolbar { .. } => 48.0,
                UiNodeType::CodeEditor { code, .. } => {
                    let lines = code.lines().count().max(3) as f32;
                    lines * 20.0 + 32.0
                }
                UiNodeType::CanvasSurface { height, .. } => *height,
                UiNodeType::Card { title } => {
                    let title_h = if title.is_some() { 28.0 } else { 0.0 };
                    let mut child_h = 0.0;
                    for c in &node.children {
                        child_h += Self::estimate_node_size(c, width - 32.0).1 + 10.0;
                    }
                    title_h + child_h + 32.0
                }
                UiNodeType::Window { .. } => {
                    let mut child_h = 0.0;
                    for c in &node.children {
                        child_h += Self::estimate_node_size(c, width - 32.0).1;
                    }
                    42.0 + child_h + 32.0
                }
                UiNodeType::VStack { spacing, .. } => {
                    let mut total_h = node.style.padding.top + node.style.padding.bottom;
                    for (i, c) in node.children.iter().enumerate() {
                        total_h += Self::estimate_node_size(c, width).1;
                        if i + 1 < node.children.len() {
                            total_h += spacing;
                        }
                    }
                    total_h.max(24.0)
                }
                UiNodeType::HStack { .. } => {
                    let mut max_h: f32 = 24.0;
                    for c in &node.children {
                        let h = Self::estimate_node_size(c, width / node.children.len().max(1) as f32).1;
                        if h > max_h {
                            max_h = h;
                        }
                    }
                    max_h + node.style.padding.top + node.style.padding.bottom
                }
                UiNodeType::Grid { columns, spacing } | UiNodeType::LazyVGrid { columns, spacing } => {
                    let cols = (*columns).max(1);
                    let rows = (node.children.len() + cols - 1) / cols;
                    let row_h = 70.0;
                    rows as f32 * row_h + (rows.saturating_sub(1) as f32 * spacing)
                }
                UiNodeType::SplitView { .. } => 400.0,
                _ => 32.0,
            }
        };

        (width, height)
    }

    /// Compute a recursive layout tree given a bounding constraint without overlapping
    pub fn compute_layout(node: &UiNode, parent_rect: Rect) -> LayoutBox {
        let (est_w, est_h) = Self::estimate_node_size(node, parent_rect.size.width);
        let width = node.style.width.unwrap_or_else(|| {
            if parent_rect.size.width > 0.0 {
                parent_rect.size.width
            } else {
                est_w
            }
        });
        let height = node.style.height.unwrap_or_else(|| {
            if parent_rect.size.height > 0.0 {
                parent_rect.size.height
            } else {
                est_h
            }
        });
        let my_bounds = Rect::new(parent_rect.origin.x, parent_rect.origin.y, width, height);

        let mut child_boxes = Vec::new();
        match &node.node_type {
            UiNodeType::VStack { spacing, .. } => {
                let mut current_y = my_bounds.origin.y + node.style.padding.top;
                let available_w = (my_bounds.size.width - node.style.padding.leading - node.style.padding.trailing).max(0.0);

                for child in &node.children {
                    let (_, child_est_h) = Self::estimate_node_size(child, available_w);
                    let child_h = child.style.height.unwrap_or(child_est_h);
                    let child_rect = Rect::new(
                        my_bounds.origin.x + node.style.padding.leading,
                        current_y,
                        child.style.width.unwrap_or(available_w),
                        child_h,
                    );
                    let cbox = Self::compute_layout(child, child_rect);
                    current_y += child_h + spacing;
                    child_boxes.push(cbox);
                }
            }
            UiNodeType::HStack { spacing, .. } => {
                let mut current_x = my_bounds.origin.x + node.style.padding.leading;
                let available_h = (my_bounds.size.height - node.style.padding.top - node.style.padding.bottom).max(0.0);
                let available_w = (my_bounds.size.width - node.style.padding.leading - node.style.padding.trailing).max(0.0);
                let child_count = node.children.len().max(1);
                let fallback_w = ((available_w - (child_count.saturating_sub(1) as f32 * spacing)) / child_count as f32).max(20.0);

                for child in &node.children {
                    let (child_est_w, _) = Self::estimate_node_size(child, available_w);
                    let child_w = child.style.width.unwrap_or(if child_est_w < fallback_w { child_est_w } else { fallback_w });
                    let child_rect = Rect::new(
                        current_x,
                        my_bounds.origin.y + node.style.padding.top,
                        child_w,
                        child.style.height.unwrap_or(available_h),
                    );
                    let cbox = Self::compute_layout(child, child_rect);
                    current_x += child_w + spacing;
                    child_boxes.push(cbox);
                }
            }
            UiNodeType::Grid { columns, spacing } | UiNodeType::LazyVGrid { columns, spacing } => {
                let cols = (*columns).max(1);
                let col_spacing_total = (cols.saturating_sub(1) as f32) * spacing;
                let col_w = ((my_bounds.size.width - node.style.padding.leading - node.style.padding.trailing - col_spacing_total) / cols as f32).max(10.0);
                let row_h = 64.0;

                for (idx, child) in node.children.iter().enumerate() {
                    let col = idx % cols;
                    let row = idx / cols;
                    let cell_x = my_bounds.origin.x + node.style.padding.leading + col as f32 * (col_w + spacing);
                    let cell_y = my_bounds.origin.y + node.style.padding.top + row as f32 * (row_h + spacing);
                    let child_rect = Rect::new(
                        cell_x,
                        cell_y,
                        child.style.width.unwrap_or(col_w),
                        child.style.height.unwrap_or(row_h),
                    );
                    child_boxes.push(Self::compute_layout(child, child_rect));
                }
            }
            UiNodeType::SplitView { orientation_horizontal, divider_position } => {
                let primary_pct = if *divider_position <= 1.0 { *divider_position } else { *divider_position / 100.0 };
                if *orientation_horizontal {
                    let primary_w = (my_bounds.size.width * primary_pct).max(120.0);
                    let secondary_w = (my_bounds.size.width - primary_w).max(120.0);
                    if let Some(primary) = node.children.first() {
                        let r = Rect::new(my_bounds.origin.x, my_bounds.origin.y, primary_w, my_bounds.size.height);
                        child_boxes.push(Self::compute_layout(primary, r));
                    }
                    if let Some(secondary) = node.children.get(1) {
                        let r = Rect::new(my_bounds.origin.x + primary_w, my_bounds.origin.y, secondary_w, my_bounds.size.height);
                        child_boxes.push(Self::compute_layout(secondary, r));
                    }
                } else {
                    let primary_h = my_bounds.size.height * primary_pct;
                    let secondary_h = my_bounds.size.height - primary_h;
                    if let Some(primary) = node.children.first() {
                        let r = Rect::new(my_bounds.origin.x, my_bounds.origin.y, my_bounds.size.width, primary_h);
                        child_boxes.push(Self::compute_layout(primary, r));
                    }
                    if let Some(secondary) = node.children.get(1) {
                        let r = Rect::new(my_bounds.origin.x, my_bounds.origin.y + primary_h, my_bounds.size.width, secondary_h);
                        child_boxes.push(Self::compute_layout(secondary, r));
                    }
                }
            }
            UiNodeType::Window { .. } => {
                let titlebar_h = 38.0;
                let content_rect = Rect::new(
                    my_bounds.origin.x + node.style.padding.leading,
                    my_bounds.origin.y + titlebar_h + node.style.padding.top,
                    my_bounds.size.width - node.style.padding.leading - node.style.padding.trailing,
                    (my_bounds.size.height - titlebar_h - node.style.padding.top - node.style.padding.bottom).max(0.0),
                );
                for child in &node.children {
                    child_boxes.push(Self::compute_layout(child, content_rect));
                }
            }
            UiNodeType::Card { title } => {
                let title_h = if title.is_some() { 28.0 } else { 0.0 };
                let content_rect = Rect::new(
                    my_bounds.origin.x + node.style.padding.leading,
                    my_bounds.origin.y + title_h + node.style.padding.top,
                    my_bounds.size.width - node.style.padding.leading - node.style.padding.trailing,
                    (my_bounds.size.height - title_h - node.style.padding.top - node.style.padding.bottom).max(0.0),
                );
                for child in &node.children {
                    child_boxes.push(Self::compute_layout(child, content_rect));
                }
            }
            _ => {
                for child in &node.children {
                    child_boxes.push(Self::compute_layout(child, my_bounds));
                }
            }
        }

        LayoutBox {
            node_id: node.node_id.clone(),
            bounds: my_bounds,
            children: child_boxes,
        }
    }

    /// Export the UI Node to an authentic Hydro-Glass HTML/CSS DOM string
    pub fn to_html(node: &UiNode) -> String {
        let mut html = String::new();
        let mut style_parts = Vec::new();

        if let Some(ref hg) = node.style.hydro_glass {
            style_parts.push(hg.to_css_style());
        } else if let Some(blur) = node.style.acrylic_blur {
            style_parts.push(format!(
                "backdrop-filter: blur({:.1}px); -webkit-backdrop-filter: blur({:.1}px); background: rgba(15, 23, 42, 0.72); border: 1px solid rgba(255, 255, 255, 0.12);",
                blur, blur
            ));
        } else if let Some(ref bg) = node.style.background {
            style_parts.push(format!("background: {};", bg.to_css_rgba()));
        }

        if let Some(ref fg) = node.style.foreground {
            style_parts.push(format!("color: {};", fg.to_css_rgba()));
        }

        if node.style.padding.top > 0.0
            || node.style.padding.trailing > 0.0
            || node.style.padding.bottom > 0.0
            || node.style.padding.leading > 0.0
        {
            style_parts.push(format!(
                "padding: {:.1}px {:.1}px {:.1}px {:.1}px;",
                node.style.padding.top,
                node.style.padding.trailing,
                node.style.padding.bottom,
                node.style.padding.leading
            ));
        }

        if node.style.corner_radii.top_leading > 0.0 {
            style_parts.push(format!("border-radius: {:.1}px;", node.style.corner_radii.top_leading));
        }

        if node.style.border_width > 0.0 {
            let bcolor = node
                .style
                .border_color
                .as_ref()
                .map(|c| c.to_css_rgba())
                .unwrap_or_else(|| "rgba(255, 255, 255, 0.15)".to_string());
            style_parts.push(format!("border: {:.1}px solid {};", node.style.border_width, bcolor));
        }

        if let Some(w) = node.style.width {
            style_parts.push(format!("width: {:.1}px;", w));
        }
        if let Some(h) = node.style.height {
            style_parts.push(format!("height: {:.1}px;", h));
        }
        if let Some(min_w) = node.style.min_width {
            style_parts.push(format!("min-width: {:.1}px;", min_w));
        }
        if let Some(max_w) = node.style.max_width {
            style_parts.push(format!("max-width: {:.1}px;", max_w));
        }

        if let Some(ref s) = node.style.shadow {
            style_parts.push(format!(
                "box-shadow: {:.1}px {:.1}px {:.1}px {};",
                s.offset_x, s.offset_y, s.radius, s.color.to_css_rgba()
            ));
        }

        let inline_css = style_parts.join(" ");

        match &node.node_type {
            UiNodeType::Text { content, typo } => {
                let fs = typo.font_size();
                let fw = typo.font_weight();
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-text" style="font-size: {:.1}px; font-weight: {}; line-height: 1.45; letter-spacing: -0.01em; {}">{}</div>"#,
                    node.node_id, fs, fw, inline_css, content
                ));
            }
            UiNodeType::Button { label, action_id } => {
                html.push_str(&format!(
                    r#"<button id="{}" data-action="{}" class="hydro-btn" style="cursor: pointer; {}">{}</button>"#,
                    node.node_id, action_id, inline_css, label
                ));
            }
            UiNodeType::TextField { placeholder, text, on_change_id } => {
                let change_attr = on_change_id
                    .as_ref()
                    .map(|id| format!(r#" data-change="{}""#, id))
                    .unwrap_or_default();
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-input-wrapper" style="{}"><input type="text" class="hydro-input" placeholder="{}" value="{}"{} style="width: 100%; outline: none;" /></div>"#,
                    node.node_id, inline_css, placeholder, text, change_attr
                ));
            }
            UiNodeType::SecureField { placeholder, text, on_change_id } => {
                let change_attr = on_change_id
                    .as_ref()
                    .map(|id| format!(r#" data-change="{}""#, id))
                    .unwrap_or_default();
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-input-wrapper" style="{}"><input type="password" class="hydro-input" placeholder="{}" value="{}"{} style="width: 100%; outline: none;" /></div>"#,
                    node.node_id, inline_css, placeholder, text, change_attr
                ));
            }
            UiNodeType::Toggle { label, is_on, action_id } => {
                let checked_attr = if *is_on { "checked" } else { "" };
                let bg_color = if *is_on { "#007AFF" } else { "rgba(255, 255, 255, 0.15)" };
                let thumb_left = if *is_on { "22px" } else { "3px" };
                let act_attr = action_id
                    .as_ref()
                    .map(|a| format!(r#" data-action="{}""#, a))
                    .unwrap_or_default();

                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-toggle-row" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%; {}"><span class="hydro-label" style="font-size: 13px; font-weight: 500; color: #e2e8f0;">{}</span><label class="hydro-switch" style="position: relative; display: inline-block; width: 44px; height: 24px; flex-shrink: 0;"><input type="checkbox" {}{}{} style="opacity: 0; width: 0; height: 0;"><span class="hydro-switch-track" style="position: absolute; cursor: pointer; inset: 0; background: {}; border-radius: 24px; transition: .25s; border: 1px solid rgba(255,255,255,0.15);"><span class="hydro-switch-thumb" style="position: absolute; height: 16px; width: 16px; left: {}; bottom: 3px; background: #ffffff; border-radius: 50%; transition: .25s; box-shadow: 0 2px 4px rgba(0,0,0,0.35);"></span></span></label></div>"#,
                    node.node_id, inline_css, label, checked_attr, act_attr, "", bg_color, thumb_left
                ));
            }
            UiNodeType::Slider { value, min, max, action_id } => {
                let act_attr = action_id
                    .as_ref()
                    .map(|a| format!(r#" data-action="{}""#, a))
                    .unwrap_or_default();
                let pct = if max > min { ((value - min) / (max - min) * 100.0).clamp(0.0, 100.0) } else { 50.0 };

                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-slider-wrapper" style="display: flex; flex-direction: column; gap: 6px; width: 100%; {}"><div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8;"><span style="font-weight: 500;">Adjustment</span><span style="font-family: monospace; color: #38bdf8;">{:.2}</span></div><input type="range" class="hydro-range" min="{}" max="{}" value="{}" step="0.01"{} style="width: 100%; accent-color: #007AFF; cursor: pointer;" /><div style="display: flex; justify-content: space-between; font-size: 10px; color: #64748b;"><span>{:.1}</span><span>{:.0}%</span><span>{:.1}</span></div></div>"#,
                    node.node_id, inline_css, value, min, max, value, act_attr, min, pct, max
                ));
            }
            UiNodeType::Picker { title, selected_index, options, action_id } => {
                let act_attr = action_id
                    .as_ref()
                    .map(|a| format!(r#" data-action="{}""#, a))
                    .unwrap_or_default();
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-picker" style="display: flex; flex-direction: column; gap: 6px; width: 100%; {}"><span style="font-size: 12px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">{}</span><div class="hydro-segmented"{} style="display: flex; background: rgba(0,0,0,0.35); border-radius: 8px; padding: 3px; gap: 4px; border: 1px solid rgba(255,255,255,0.08);">"#,
                    node.node_id, inline_css, title, act_attr
                ));
                for (idx, opt) in options.iter().enumerate() {
                    let is_active = idx == *selected_index;
                    let active_style = if is_active {
                        "background: rgba(255,255,255,0.18); color: #ffffff; font-weight: 600; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"
                    } else {
                        "background: transparent; color: #94a3b8; font-weight: 500;"
                    };
                    html.push_str(&format!(
                        r#"<button class="segmented-item" data-index="{}" style="flex: 1; padding: 6px 10px; border-radius: 6px; border: none; font-size: 12px; cursor: pointer; transition: all 0.2s; {}">{}</button>"#,
                        idx, active_style, opt
                    ));
                }
                html.push_str("</div></div>");
            }
            UiNodeType::ProgressView { progress, label } => {
                let pct = progress.unwrap_or(0.5) * 100.0;
                let lbl = label.as_deref().unwrap_or("Progress");
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-progress-view" style="display: flex; flex-direction: column; gap: 6px; width: 100%; {}"><div style="display: flex; justify-content: space-between; font-size: 12px; color: #cbd5e1;"><span style="font-weight: 500;">{}</span><span style="font-family: monospace; color: #38bdf8;">{:.0}%</span></div><div class="hydro-progress-track" style="width: 100%; height: 8px; border-radius: 4px; background: rgba(255,255,255,0.1); overflow: hidden; position: relative;"><div class="hydro-progress-fill" style="width: {:.1}%; height: 100%; border-radius: 4px; background: linear-gradient(90deg, #007AFF, #00D2FF); box-shadow: 0 0 10px rgba(0,210,255,0.5); transition: width 0.3s ease;"></div></div></div>"#,
                    node.node_id, inline_css, lbl, pct, pct
                ));
            }
            UiNodeType::Gauge { value, min, max, label } => {
                let pct = if max > min { ((value - min) / (max - min) * 100.0).clamp(0.0, 100.0) } else { 50.0 };
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-gauge" style="display: flex; flex-direction: column; gap: 6px; width: 100%; padding: 12px; background: rgba(15,23,42,0.5); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); {}"><div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 12px; font-weight: 600; color: #94a3b8;">{}</span><span style="font-size: 14px; font-weight: 700; color: #38bdf8; font-family: monospace;">{:.1}</span></div><div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden;"><div style="width: {:.1}%; height: 100%; background: linear-gradient(90deg, #30D158, #00D2FF); border-radius: 3px;"></div></div></div>"#,
                    node.node_id, inline_css, label, value, pct
                ));
            }
            UiNodeType::Badge { text, color } => {
                html.push_str(&format!(
                    r#"<span id="{}" class="hydro-badge" style="display: inline-flex; align-items: center; justify-content: center; padding: 3px 9px; border-radius: 12px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; background: {}; color: #ffffff; box-shadow: 0 0 12px {}; {}">{}</span>"#,
                    node.node_id, color.to_css_rgba(), color.to_css_rgba(), inline_css, text
                ));
            }
            UiNodeType::Avatar { glyph_id, size } => {
                let svg = VectorGlyphRegistry::get_svg(glyph_id);
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-avatar" style="width: {:.1}px; height: {:.1}px; border-radius: 50%; overflow: hidden; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)); border: 1.5px solid rgba(255,255,255,0.2); box-shadow: 0 4px 12px rgba(0,0,0,0.25); {}"><div style="width: 60%; height: 60%; display: flex; align-items: center; justify-content: center; color: #ffffff;">{}</div></div>"#,
                    node.node_id, size, size, inline_css, svg
                ));
            }
            UiNodeType::Image { glyph_id, width, height } => {
                let svg = VectorGlyphRegistry::get_svg(glyph_id);
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-icon" style="width: {:.1}px; height: {:.1}px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; color: inherit; {}">{}</div>"#,
                    node.node_id, width, height, inline_css, svg
                ));
            }
            UiNodeType::VStack { spacing, .. } => {
                html.push_str(&format!(
                    r#"<div id="{}" style="display: flex; flex-direction: column; gap: {:.1}px; width: 100%; {}">"#,
                    node.node_id, spacing, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::HStack { spacing, .. } => {
                html.push_str(&format!(
                    r#"<div id="{}" style="display: flex; flex-direction: row; align-items: center; gap: {:.1}px; width: 100%; {}">"#,
                    node.node_id, spacing, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::ZStack { .. } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-zstack" style="position: relative; width: 100%; min-height: 100%; display: grid; align-items: center; justify-items: center; {}">"#,
                    node.node_id, inline_css
                ));
                for (z_idx, child) in node.children.iter().enumerate() {
                    html.push_str(&format!(r#"<div style="grid-area: 1/1; width: 100%; height: 100%; z-index: {};">"#, z_idx + 1));
                    html.push_str(&Self::to_html(child));
                    html.push_str("</div>");
                }
                html.push_str("</div>");
            }
            UiNodeType::Grid { columns, spacing } | UiNodeType::LazyVGrid { columns, spacing } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-grid" style="display: grid; grid-template-columns: repeat({}, minmax(0, 1fr)); gap: {:.1}px; width: 100%; {}">"#,
                    node.node_id, columns, spacing, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::LazyHGrid { rows, spacing } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-lazy-hgrid" style="display: grid; grid-template-rows: repeat({}, minmax(0, 1fr)); grid-auto-flow: column; gap: {:.1}px; width: 100%; overflow-x: auto; {}">"#,
                    node.node_id, rows, spacing, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::ScrollView { horizontal, vertical } => {
                let overflow_x = if *horizontal { "auto" } else { "hidden" };
                let overflow_y = if *vertical { "auto" } else { "hidden" };
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-scrollview" style="overflow-x: {}; overflow-y: {}; max-height: 100%; width: 100%; scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.2) transparent; {}">"#,
                    node.node_id, overflow_x, overflow_y, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::List { .. } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-list" style="display: flex; flex-direction: column; width: 100%; border-radius: 12px; background: rgba(15,23,42,0.4); border: 1px solid rgba(255,255,255,0.08); overflow: hidden; {}">"#,
                    node.node_id, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::ListItem { selected } => {
                let sel_style = if *selected {
                    "background: rgba(0, 122, 255, 0.2); border-left: 3px solid #007AFF;"
                } else {
                    "background: transparent;"
                };
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-list-item" style="display: flex; align-items: center; padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s ease; cursor: pointer; {} {}">"#,
                    node.node_id, sel_style, inline_css
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::Section { header, footer } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-section" style="display: flex; flex-direction: column; gap: 8px; width: 100%; margin-bottom: 16px; {}">"#,
                    node.node_id, inline_css
                ));
                if let Some(ref h) = header {
                    html.push_str(&format!(
                        r#"<div class="section-header" style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #94a3b8; padding-left: 4px;">{}</div>"#,
                        h
                    ));
                }
                html.push_str(r#"<div class="section-content" style="display: flex; flex-direction: column; gap: 6px;">"#);
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
                if let Some(ref f) = footer {
                    html.push_str(&format!(
                        r#"<div class="section-footer" style="font-size: 11px; color: #64748b; padding-left: 4px;">{}</div>"#,
                        f
                    ));
                }
                html.push_str("</div>");
            }
            UiNodeType::SplitView { orientation_horizontal, divider_position } => {
                let primary_pct = if *divider_position <= 1.0 { *divider_position * 100.0 } else { *divider_position };
                let flex_dir = if *orientation_horizontal { "row" } else { "column" };
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-splitview" style="display: flex; flex-direction: {}; width: 100%; height: 100%; min-height: 0; {}">"#,
                    node.node_id, flex_dir, inline_css
                ));
                if let Some(primary) = node.children.first() {
                    let border = if *orientation_horizontal { "border-right: 1px solid rgba(255,255,255,0.08);" } else { "border-bottom: 1px solid rgba(255,255,255,0.08);" };
                    html.push_str(&format!(
                        r#"<div class="hydro-split-pane primary" style="flex: 0 0 {:.1}%; max-width: {:.1}%; overflow: auto; {}">{}</div>"#,
                        primary_pct, primary_pct, border, Self::to_html(primary)
                    ));
                }
                if let Some(secondary) = node.children.get(1) {
                    html.push_str(&format!(
                        r#"<div class="hydro-split-pane secondary" style="flex: 1 1 0%; min-width: 0; overflow: auto;">{}</div>"#,
                        Self::to_html(secondary)
                    ));
                }
                html.push_str("</div>");
            }
            UiNodeType::CodeEditor { code, language: _, show_line_numbers } => {
                let lines_count = code.lines().count().max(1);
                let mut line_num_str = String::new();
                if *show_line_numbers {
                    for i in 1..=lines_count {
                        line_num_str.push_str(&format!("{}<br>", i));
                    }
                }
                let escaped_code = code.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;");
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-code-editor" style="display: flex; width: 100%; font-family: 'SF Mono', 'JetBrains Mono', 'Fira Code', Menlo, monospace; font-size: 13px; line-height: 1.6; background: #0b0f19; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.4); {}">"#,
                    node.node_id, inline_css
                ));
                if *show_line_numbers {
                    html.push_str(&format!(
                        r#"<div class="gutter" style="padding: 14px 10px; background: rgba(0,0,0,0.3); border-right: 1px solid rgba(255,255,255,0.06); color: #475569; user-select: none; text-align: right; font-size: 12px;">{}</div>"#,
                        line_num_str
                    ));
                }
                html.push_str(&format!(
                    r#"<pre style="margin: 0; padding: 14px 18px; color: #f1f5f9; overflow-x: auto; flex: 1; min-width: 0;"><code>{}</code></pre></div>"#,
                    escaped_code
                ));
            }
            UiNodeType::BreadcrumbBar { segments } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-breadcrumbs" style="display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 500; color: #94a3b8; {}">"#,
                    node.node_id, inline_css
                ));
                for (i, seg) in segments.iter().enumerate() {
                    if i > 0 {
                        html.push_str(r#"<span style="opacity: 0.35;">/</span>"#);
                    }
                    let is_last = i + 1 == segments.len();
                    let color = if is_last { "#ffffff" } else { "#94a3b8" };
                    html.push_str(&format!(r#"<span style="color: {};">{}</span>"#, color, seg));
                }
                html.push_str("</div>");
            }
            UiNodeType::Toolbar { title } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-toolbar" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%; padding: 10px 16px; background: rgba(255,255,255,0.04); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.08); {}"><div class="toolbar-title" style="font-size: 13px; font-weight: 700; color: #f8fafc; letter-spacing: -0.01em;">{}</div><div class="toolbar-items" style="display: flex; align-items: center; gap: 8px;">"#,
                    node.node_id, inline_css, title
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div></div>");
            }
            UiNodeType::InspectorPane { title } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-inspector" style="display: flex; flex-direction: column; gap: 12px; width: 100%; padding: 16px; background: rgba(15,23,42,0.85); backdrop-filter: blur(30px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; {}"><div class="inspector-header" style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #94a3b8; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.06);">{}</div>"#,
                    node.node_id, inline_css, title
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::ModalSheet { is_presented, title } => {
                let disp = if *is_presented { "flex" } else { "none" };
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-modal-overlay" style="position: fixed; inset: 0; background: rgba(0,0,0,0.65); backdrop-filter: blur(12px); display: {}; align-items: center; justify-content: center; z-index: 9999; {}"><div class="hydro-modal-dialog" style="min-width: 440px; max-width: 90%; max-height: 85vh; border-radius: 20px; background: rgba(15,23,42,0.9); border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 25px 60px rgba(0,0,0,0.7); overflow: hidden;"><div class="modal-header" style="padding: 16px 20px; font-size: 16px; font-weight: 700; color: #fff; border-bottom: 1px solid rgba(255,255,255,0.08);">{}</div><div class="modal-body" style="padding: 20px;">"#,
                    node.node_id, disp, inline_css, title
                ));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div></div></div>");
            }
            UiNodeType::CanvasSurface { width, height, target_fps } => {
                html.push_str(&format!(
                    r#"<div id="{}" class="hydro-canvas-surface" style="width: {:.1}px; height: {:.1}px; position: relative; border-radius: 12px; overflow: hidden; background: radial-gradient(circle at 50% 50%, rgba(30,41,59,0.8), rgba(15,23,42,0.95)); border: 1px solid rgba(255,255,255,0.1); {}"><div class="fps-badge" style="position: absolute; top: 8px; right: 8px; font-size: 10px; font-family: monospace; padding: 2px 6px; border-radius: 4px; background: rgba(0,0,0,0.6); color: #30D158;">{} FPS</div></div>"#,
                    node.node_id, width, height, inline_css, target_fps
                ));
            }
            UiNodeType::Card { title } => {
                html.push_str(&format!(r#"<div id="{}" class="hydro-card" style="{}">"#, node.node_id, inline_css));
                if let Some(ref t) = title {
                    html.push_str(&format!(
                        r#"<div class="card-title" style="font-weight: 600; font-size: 15px; margin-bottom: 12px; color: #f8fafc; letter-spacing: -0.01em;">{}</div>"#,
                        t
                    ));
                }
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
            UiNodeType::Window { title, traffic_lights } => {
                html.push_str(&format!(r#"<div id="{}" class="hydro-window" style="overflow: hidden; {}">"#, node.node_id, inline_css));
                html.push_str(r#"<div class="window-titlebar" style="display: flex; align-items: center; padding: 10px 14px; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.08); user-select: none;">"#);
                if *traffic_lights {
                    html.push_str(r#"<div class="traffic-lights" style="display: flex; gap: 6px; margin-right: 12px;"><span style="width:10px;height:10px;border-radius:50%;background:#ff5f56;display:inline-block;box-shadow:0 0 6px rgba(255,95,86,0.6);"></span><span style="width:10px;height:10px;border-radius:50%;background:#ffbd2e;display:inline-block;box-shadow:0 0 6px rgba(255,189,46,0.6);"></span><span style="width:10px;height:10px;border-radius:50%;background:#27c93f;display:inline-block;box-shadow:0 0 6px rgba(39,201,63,0.6);"></span></div>"#);
                }
                html.push_str(&format!(r#"<span class="window-title" style="font-size: 13px; font-weight: 500; color: #e2e8f0; letter-spacing: -0.01em;">{}</span></div>"#, title));
                html.push_str(r#"<div class="window-content" style="padding: 16px;">"#);
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div></div>");
            }
            UiNodeType::Divider => {
                html.push_str(r#"<div style="height: 1px; width: 100%; background: rgba(255, 255, 255, 0.08); margin: 6px 0; flex-shrink: 0;"></div>"#);
            }
            UiNodeType::Spacer => {
                html.push_str(r#"<div style="flex: 1; min-width: 8px; min-height: 8px;"></div>"#);
            }
            _ => {
                html.push_str(&format!(r#"<div id="{}" style="{}">"#, node.node_id, inline_css));
                for child in &node.children {
                    html.push_str(&Self::to_html(child));
                }
                html.push_str("</div>");
            }
        }

        html
    }

    /// Complete modern stylesheet providing the authentic Hydro-Glass design tokens and zero-overlap resets
    pub fn default_css() -> &'static str {
        r#"
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
:root {
    --hydro-font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Segoe UI", Roboto, sans-serif;
    --hydro-mono: "SF Mono", "JetBrains Mono", "Fira Code", Menlo, monospace;
    --hydro-glass-bg: rgba(15, 23, 42, 0.75);
    --hydro-glass-border: rgba(255, 255, 255, 0.12);
    --hydro-primary: #007AFF;
    --hydro-accent: #00D2FF;
    --hydro-success: #30D158;
    --hydro-warning: #FF9F0A;
    --hydro-danger: #FF453A;
}
body {
    font-family: var(--hydro-font);
    background: #090d16;
    color: #f1f5f9;
    -webkit-font-smoothing: antialiased;
    line-height: 1.5;
}
.hydro-window {
    background: var(--hydro-glass-bg);
    border: 1px solid var(--hydro-glass-border);
    border-radius: 18px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(48px);
    -webkit-backdrop-filter: blur(48px);
}
.hydro-card {
    background: rgba(22, 27, 46, 0.65);
    border: 1px solid var(--hydro-glass-border);
    border-radius: 16px;
    backdrop-filter: blur(36px);
    -webkit-backdrop-filter: blur(36px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.hydro-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    font-family: var(--hydro-font);
    font-size: 13px;
    font-weight: 600;
    padding: 8px 16px;
    min-height: 36px;
    white-space: nowrap;
    user-select: none;
    background: var(--hydro-primary);
    color: #ffffff;
    box-shadow: 0 2px 10px rgba(0, 122, 255, 0.3);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    outline: none;
}
.hydro-btn:hover {
    transform: translateY(-1.5px);
    filter: brightness(1.15);
    box-shadow: 0 6px 20px rgba(0, 122, 255, 0.45);
}
.hydro-btn:active {
    transform: translateY(0px) scale(0.97);
    filter: brightness(0.92);
}
.hydro-input {
    font-family: var(--hydro-font);
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--hydro-glass-border);
    border-radius: 8px;
    color: #f8fafc;
    padding: 10px 14px;
    font-size: 13px;
    transition: all 0.2s ease;
}
.hydro-input:focus {
    border-color: var(--hydro-primary);
    box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.3);
}
.hydro-badge {
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
}
"#
    }

    /// Generate a standalone HTML page embedding complete Hydro-Glass styling
    pub fn generate_full_document(title: &str, node: &UiNode) -> String {
        format!(
            r#"<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
    <style>
{}
    </style>
</head>
<body style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; background: radial-gradient(circle at 50% 20%, #1e293b, #090d16 80%);">
{}
</body>
</html>"#,
            title,
            Self::default_css(),
            Self::to_html(node)
        )
    }
}
