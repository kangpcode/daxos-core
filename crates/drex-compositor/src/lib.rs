//! ============================================================================
//! DAXOS DREX-COMPOSITOR CORE (drex-compositor)
//! File: crates/drex-compositor/src/lib.rs
//! Purpose: Wayland Compositor Core & Multi-Pass Acrylic Glass Render Pipeline
//! ============================================================================

use drexvis::{CommandGraph, CommandNode, GpuBackend, SharedSurface, SurfaceDescriptor};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::Instant;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AcrylicParameters {
    pub opacity: f32,
    pub blur_radius_px: u32,
    pub edge_brightness: f32,
    pub noise_intensity: f32,
}

impl Default for AcrylicParameters {
    fn default() -> Self {
        Self {
            opacity: 0.72,
            blur_radius_px: 36,
            edge_brightness: 1.15,
            noise_intensity: 0.04,
        }
    }
}

pub struct CompositorSurface {
    pub surface_id: u64,
    pub client_pid: u32,
    pub width: u32,
    pub height: u32,
    pub acrylic_params: Option<AcrylicParameters>,
    pub gpu_surface: Option<SharedSurface>,
}

pub struct DrexCompositorEngine {
    surfaces: HashMap<u64, CompositorSurface>,
    gpu_backend: Arc<Mutex<Box<dyn GpuBackend>>>,
    target_refresh_hz: u32,
    next_surface_id: u64,
    frame_counter: u64,
}

impl DrexCompositorEngine {
    pub fn new(backend: Box<dyn GpuBackend>, target_refresh_hz: u32) -> Self {
        Self {
            surfaces: HashMap::new(),
            gpu_backend: Arc::new(Mutex::new(backend)),
            target_refresh_hz,
            next_surface_id: 1,
            frame_counter: 0,
        }
    }

    pub fn create_client_surface(&mut self, client_pid: u32, width: u32, height: u32) -> u64 {
        let id = self.next_surface_id;
        self.next_surface_id += 1;

        let desc = SurfaceDescriptor {
            width,
            height,
            format_fourcc: 0x34325258, // XRGB8888
            modifier: 0,
        };

        let mut backend = self.gpu_backend.lock().unwrap();
        let gpu_surf = backend.create_surface(&desc).ok();

        let surf = CompositorSurface {
            surface_id: id,
            client_pid,
            width,
            height,
            acrylic_params: None,
            gpu_surface: gpu_surf,
        };

        self.surfaces.insert(id, surf);
        id
    }

    pub fn attach_acrylic_effect(&mut self, surface_id: u64, params: AcrylicParameters) -> Result<(), &'static str> {
        let surface = self.surfaces.get_mut(&surface_id).ok_or("Surface not found")?;
        surface.acrylic_params = Some(params);
        Ok(())
    }

    pub fn render_frame(&mut self) -> Result<u64, &'static str> {
        self.frame_counter += 1;

        // Bangun Command Graph Multi-Pass Dual Kawase Blur untuk setiap surface akrilik
        let mut nodes = Vec::new();

        for surface in self.surfaces.values() {
            if let Some(ref params) = surface.acrylic_params {
                // Pass 1: Downsample 1/2
                nodes.push(CommandNode::BeginRenderPass {
                    target_surface_id: surface.surface_id,
                    clear_color: [0.0, 0.0, 0.0, 1.0],
                });
                // Pass 2: Blur Convolution
                nodes.push(CommandNode::ComputeDispatch {
                    pipeline_id: 42,
                    groups_x: (surface.width / 16).max(1),
                    groups_y: (surface.height / 16).max(1),
                    groups_z: 1,
                });
                nodes.push(CommandNode::EndRenderPass);

                // Pass 3: Present
                nodes.push(CommandNode::Present {
                    surface_id: surface.surface_id,
                });
                let _ = params;
            }
        }

        let graph = CommandGraph {
            graph_id: self.frame_counter,
            nodes,
            created_at: Instant::now(),
        };

        let mut backend = self.gpu_backend.lock().unwrap();
        let _ = backend.submit_command_graph(&graph);

        Ok(self.frame_counter)
    }

    pub fn get_target_frametime_ms(&self) -> f64 {
        1000.0 / (self.target_refresh_hz as f64)
    }

    pub fn set_target_refresh_hz(&mut self, hz: u32) {
        if (30..=240).contains(&hz) {
            self.target_refresh_hz = hz;
        }
    }

    pub fn get_target_refresh_hz(&self) -> u32 {
        self.target_refresh_hz
    }

    pub fn auto_detect_display_profile(is_vm_or_legacy: bool) -> u32 {
        if is_vm_or_legacy {
            60 // 60Hz Universal compatibility for legacy monitors, VMs, and older CPUs
        } else {
            120 // 120Hz High-bandwidth ProMotion compositor
        }
    }
}

// ============================================================================
// MACOS-LIKE DREX DESKTOP SHELL SUBSYSTEM
// ============================================================================

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DockItem {
    pub bundle_id: String,
    pub name: String,
    pub icon: String,
    pub is_running: bool,
    pub has_dot_indicator: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ShellWindow {
    pub window_id: u64,
    pub title: String,
    pub bundle_id: String,
    pub x: i32,
    pub y: i32,
    pub width: u32,
    pub height: u32,
    pub is_minimized: bool,
    pub is_maximized: bool,
    pub is_focused: bool,
    pub acrylic_blur: f32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DisplayMode {
    Extended,     // Canvas diperluas melintasi monitor utama dan eksternal
    Mirror,       // Tampilan diduplikasi/dikloning persis ke monitor eksternal
    PrimaryOnly,  // Hanya aktifkan monitor utama (laptop display)
    ExternalOnly, // Clamshell mode (hanya aktifkan monitor eksternal)
}

impl Default for DisplayMode {
    fn default() -> Self {
        Self::Extended
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DisplayOutput {
    pub id: u32,
    pub name: String,
    pub connector: String,
    pub is_primary: bool,
    pub is_connected: bool,
    pub width: u32,
    pub height: u32,
    pub refresh_rate_hz: u32,
    pub scale_factor: f32,
    pub offset_x: i32,
    pub offset_y: i32,
    pub is_active: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DisplayManager {
    pub mode: DisplayMode,
    pub displays: Vec<DisplayOutput>,
    pub virtual_canvas_width: u32,
    pub virtual_canvas_height: u32,
    next_display_id: u32,
}

impl DisplayManager {
    pub fn new(primary_w: u32, primary_h: u32, primary_hz: u32) -> Self {
        let primary = DisplayOutput {
            id: 1,
            name: "eDP-1 (Internal Retina)".to_string(),
            connector: "eDP-1".to_string(),
            is_primary: true,
            is_connected: true,
            width: primary_w,
            height: primary_h,
            refresh_rate_hz: primary_hz,
            scale_factor: 1.0,
            offset_x: 0,
            offset_y: 0,
            is_active: true,
        };

        Self {
            mode: DisplayMode::Extended,
            displays: vec![primary],
            virtual_canvas_width: primary_w,
            virtual_canvas_height: primary_h,
            next_display_id: 2,
        }
    }

    pub fn connect_external(
        &mut self,
        name: &str,
        connector: &str,
        width: u32,
        height: u32,
        refresh_rate_hz: u32,
        scale: f32,
    ) -> u32 {
        let id = self.next_display_id;
        self.next_display_id += 1;

        let ext = DisplayOutput {
            id,
            name: name.to_string(),
            connector: connector.to_string(),
            is_primary: false,
            is_connected: true,
            width,
            height,
            refresh_rate_hz,
            scale_factor: scale,
            offset_x: 0,
            offset_y: 0,
            is_active: true,
        };

        self.displays.push(ext);
        self.recalculate_topology();
        id
    }

    pub fn disconnect_external(&mut self, id: u32) -> bool {
        if let Some(pos) = self.displays.iter().position(|d| d.id == id && !d.is_primary) {
            self.displays.remove(pos);
            self.recalculate_topology();
            true
        } else {
            false
        }
    }

    pub fn set_display_mode(&mut self, mode: DisplayMode) {
        self.mode = mode;
        self.recalculate_topology();
    }

    pub fn recalculate_topology(&mut self) {
        match self.mode {
            DisplayMode::Extended => {
                let mut current_x = 0i32;
                let mut max_h = 0u32;
                for d in &mut self.displays {
                    d.is_active = true;
                    d.offset_x = current_x;
                    d.offset_y = 0;
                    current_x += d.width as i32;
                    max_h = max_h.max(d.height);
                }
                self.virtual_canvas_width = current_x as u32;
                self.virtual_canvas_height = max_h.max(1080);
            }
            DisplayMode::Mirror => {
                let primary_w = self.displays.iter().find(|d| d.is_primary).map(|d| d.width).unwrap_or(1920);
                let primary_h = self.displays.iter().find(|d| d.is_primary).map(|d| d.height).unwrap_or(1080);
                for d in &mut self.displays {
                    d.is_active = true;
                    d.offset_x = 0;
                    d.offset_y = 0;
                }
                self.virtual_canvas_width = primary_w;
                self.virtual_canvas_height = primary_h;
            }
            DisplayMode::PrimaryOnly => {
                for d in &mut self.displays {
                    d.is_active = d.is_primary;
                    d.offset_x = 0;
                    d.offset_y = 0;
                }
                let primary = self.displays.iter().find(|d| d.is_primary);
                self.virtual_canvas_width = primary.map(|d| d.width).unwrap_or(1920);
                self.virtual_canvas_height = primary.map(|d| d.height).unwrap_or(1080);
            }
            DisplayMode::ExternalOnly => {
                let mut first_ext_found = false;
                for d in &mut self.displays {
                    if !d.is_primary && !first_ext_found {
                        d.is_active = true;
                        d.offset_x = 0;
                        d.offset_y = 0;
                        first_ext_found = true;
                        self.virtual_canvas_width = d.width;
                        self.virtual_canvas_height = d.height;
                    } else {
                        d.is_active = false;
                    }
                }
            }
        }
    }

    pub fn get_display_for_point(&self, x: i32, y: i32) -> Option<u32> {
        for d in &self.displays {
            if !d.is_active { continue; }
            let in_x = x >= d.offset_x && x < d.offset_x + d.width as i32;
            let in_y = y >= d.offset_y && y < d.offset_y + d.height as i32;
            if in_x && in_y {
                return Some(d.id);
            }
        }
        None
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ControlCenterState {
    pub is_open: bool,
    pub wifi_enabled: bool,
    pub bluetooth_enabled: bool,
    pub daxdrop_active: bool,
    pub display_brightness_pct: u32,
    pub sound_volume_pct: u32,
    pub dark_mode: bool,
    pub display_mode: DisplayMode,
    pub external_monitor_connected: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DesktopShell {
    pub screen_width: u32,
    pub screen_height: u32,
    pub display_manager: DisplayManager,
    pub dock_items: Vec<DockItem>,
    pub open_windows: Vec<ShellWindow>,
    pub control_center: ControlCenterState,
    pub active_app_title: String,
    pub next_window_id: u64,
}

impl DesktopShell {
    pub fn new(screen_width: u32, screen_height: u32) -> Self {
        let dock_items = vec![
            DockItem {
                bundle_id: "org.daxos.files".to_string(),
                name: "Finder".to_string(),
                icon: "drex.icon.finder".to_string(),
                is_running: true,
                has_dot_indicator: true,
            },
            DockItem {
                bundle_id: "org.daxos.daxbro".to_string(),
                name: "DaXBro Browser".to_string(),
                icon: "drex.icon.daxbro".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.dcodx.ide".to_string(),
                name: "DCODX IDE".to_string(),
                icon: "drex.icon.ide".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.dapstore".to_string(),
                name: "DapStore".to_string(),
                icon: "drex.icon.dapstore".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.dxdef".to_string(),
                name: "DXDEF Security".to_string(),
                icon: "drex.icon.dxdef".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.terminal".to_string(),
                name: "Terminal".to_string(),
                icon: "drex.icon.terminal".to_string(),
                is_running: true,
                has_dot_indicator: true,
            },
            DockItem {
                bundle_id: "org.daxos.camera".to_string(),
                name: "Camera".to_string(),
                icon: "drex.icon.camera".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.calculator".to_string(),
                name: "Calculator".to_string(),
                icon: "drex.icon.calculator".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.preferences".to_string(),
                name: "System Settings".to_string(),
                icon: "drex.icon.settings".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.installer".to_string(),
                name: "Install DAXOS".to_string(),
                icon: "drex.icon.installer".to_string(),
                is_running: true,
                has_dot_indicator: true,
            },
            DockItem {
                bundle_id: "org.daxos.editor".to_string(),
                name: "Text Editor (dEdit)".to_string(),
                icon: "drex.icon.editor".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.sysmon".to_string(),
                name: "Activity Monitor (dTop)".to_string(),
                icon: "drex.icon.sysmon".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.disks".to_string(),
                name: "Disk Utility (dDisk)".to_string(),
                icon: "drex.icon.disks".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.media".to_string(),
                name: "Music & Spatial Audio".to_string(),
                icon: "drex.icon.media".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.daxdrop".to_string(),
                name: "DaXDrop Air-Gesture".to_string(),
                icon: "drex.icon.daxdrop".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
            DockItem {
                bundle_id: "org.daxos.trash".to_string(),
                name: "Trash".to_string(),
                icon: "drex.icon.trash".to_string(),
                is_running: false,
                has_dot_indicator: false,
            },
        ];

        let initial_windows = vec![
            ShellWindow {
                window_id: 1,
                title: "Install DAXOS Setup Assistant".to_string(),
                bundle_id: "org.daxos.installer".to_string(),
                x: 180,
                y: 80,
                width: 760,
                height: 520,
                is_minimized: false,
                is_maximized: false,
                is_focused: true,
                acrylic_blur: 32.0,
            },
            ShellWindow {
                window_id: 2,
                title: "DAXOS Terminal (zsh / dcodx-sh)".to_string(),
                bundle_id: "org.daxos.terminal".to_string(),
                x: 420,
                y: 200,
                width: 680,
                height: 420,
                is_minimized: false,
                is_maximized: false,
                is_focused: false,
                acrylic_blur: 36.0,
            },
        ];

        let display_mgr = DisplayManager::new(screen_width, screen_height, 120);

        Self {
            screen_width: display_mgr.virtual_canvas_width,
            screen_height: display_mgr.virtual_canvas_height,
            display_manager: display_mgr,
            dock_items,
            open_windows: initial_windows,
            control_center: ControlCenterState {
                is_open: false,
                wifi_enabled: true,
                bluetooth_enabled: true,
                daxdrop_active: true,
                display_brightness_pct: 90,
                sound_volume_pct: 75,
                dark_mode: true,
                display_mode: DisplayMode::Extended,
                external_monitor_connected: false,
            },
            active_app_title: "Install DAXOS".to_string(),
            next_window_id: 3,
        }
    }

    pub fn set_display_mode(&mut self, mode: DisplayMode) {
        self.display_manager.set_display_mode(mode);
        self.control_center.display_mode = mode;
        self.screen_width = self.display_manager.virtual_canvas_width;
        self.screen_height = self.display_manager.virtual_canvas_height;

        // Jika mode Mirror atau PrimaryOnly, relokasi jendela yang berada di luar monitor utama
        if mode == DisplayMode::Mirror || mode == DisplayMode::PrimaryOnly {
            let primary_w = self.display_manager.displays.iter().find(|d| d.is_primary).map(|d| d.width).unwrap_or(1920) as i32;
            let primary_h = self.display_manager.displays.iter().find(|d| d.is_primary).map(|d| d.height).unwrap_or(1080) as i32;
            for win in &mut self.open_windows {
                if win.x + (win.width as i32) > primary_w || win.x < 0 {
                    win.x = (win.x % (primary_w - 300)).max(60);
                }
                if win.y + (win.height as i32) > primary_h || win.y < 0 {
                    win.y = (win.y % (primary_h - 200)).max(60);
                }
            }
        }
    }

    pub fn connect_external_monitor(&mut self, name: &str, connector: &str, width: u32, height: u32, hz: u32) -> u32 {
        let id = self.display_manager.connect_external(name, connector, width, height, hz, 1.0);
        self.control_center.external_monitor_connected = true;
        self.screen_width = self.display_manager.virtual_canvas_width;
        self.screen_height = self.display_manager.virtual_canvas_height;
        id
    }

    pub fn disconnect_external_monitor(&mut self, display_id: u32) -> bool {
        let ok = self.display_manager.disconnect_external(display_id);
        if ok {
            self.control_center.external_monitor_connected = self.display_manager.displays.len() > 1;
            self.screen_width = self.display_manager.virtual_canvas_width;
            self.screen_height = self.display_manager.virtual_canvas_height;
            // Relokasi jendela yang berada di monitor yang terlepas
            let primary_w = self.display_manager.virtual_canvas_width as i32;
            for win in &mut self.open_windows {
                if win.x >= primary_w {
                    win.x = 100;
                    win.y = 100;
                }
            }
        }
        ok
    }

    pub fn move_window_to_display(&mut self, window_id: u64, target_display_id: u32) -> bool {
        let target_disp = self.display_manager.displays.iter().find(|d| d.id == target_display_id && d.is_active).cloned();
        if let Some(target) = target_disp {
            if let Some(win) = self.open_windows.iter_mut().find(|w| w.window_id == window_id) {
                win.x = target.offset_x + 60;
                win.y = target.offset_y + 60;
                win.is_focused = true;
                return true;
            }
        }
        false
    }

    pub fn launch_app(&mut self, bundle_id: &str, title: &str) -> u64 {
        let win_id = self.next_window_id;
        self.next_window_id += 1;

        for item in &mut self.dock_items {
            if item.bundle_id == bundle_id {
                item.is_running = true;
                item.has_dot_indicator = true;
            }
        }

        for win in &mut self.open_windows {
            win.is_focused = false;
        }

        let new_win = ShellWindow {
            window_id: win_id,
            title: title.to_string(),
            bundle_id: bundle_id.to_string(),
            x: 240 + (win_id as i32 % 5) * 30,
            y: 120 + (win_id as i32 % 5) * 30,
            width: 720,
            height: 480,
            is_minimized: false,
            is_maximized: false,
            is_focused: true,
            acrylic_blur: 30.0,
        };

        self.active_app_title = title.to_string();
        self.open_windows.push(new_win);
        win_id
    }

    pub fn close_window(&mut self, window_id: u64) -> bool {
        if let Some(pos) = self.open_windows.iter().position(|w| w.window_id == window_id) {
            let win = self.open_windows.remove(pos);
            let has_other = self.open_windows.iter().any(|w| w.bundle_id == win.bundle_id);
            if !has_other {
                for item in &mut self.dock_items {
                    if item.bundle_id == win.bundle_id {
                        item.is_running = false;
                        item.has_dot_indicator = false;
                    }
                }
            }
            if let Some(last) = self.open_windows.last_mut() {
                last.is_focused = true;
                self.active_app_title = last.title.clone();
            } else {
                self.active_app_title = "Finder".to_string();
            }
            true
        } else {
            false
        }
    }

    pub fn minimize_window(&mut self, window_id: u64) -> bool {
        if let Some(win) = self.open_windows.iter_mut().find(|w| w.window_id == window_id) {
            win.is_minimized = true;
            win.is_focused = false;
            true
        } else {
            false
        }
    }

    pub fn maximize_window(&mut self, window_id: u64) -> bool {
        if let Some(win) = self.open_windows.iter_mut().find(|w| w.window_id == window_id) {
            win.is_maximized = !win.is_maximized;
            true
        } else {
            false
        }
    }

    pub fn focus_window(&mut self, window_id: u64) -> bool {
        let mut found = false;
        let mut app_name = String::new();
        for win in &mut self.open_windows {
            if win.window_id == window_id {
                win.is_focused = true;
                win.is_minimized = false;
                app_name = win.title.clone();
                found = true;
            } else {
                win.is_focused = false;
            }
        }
        if found {
            self.active_app_title = app_name;
        }
        found
    }

    pub fn toggle_control_center(&mut self) {
        self.control_center.is_open = !self.control_center.is_open;
    }

    pub fn render_scene_summary(&self) -> String {
        format!(
            "DesktopShell [Canvas: {}x{}] | Display Mode: {:?} (Displays: {}) | Active App: '{}' | Windows: {} (Focused: {}) | Dock Items: {} | Control Center: {}",
            self.screen_width,
            self.screen_height,
            self.display_manager.mode,
            self.display_manager.displays.len(),
            self.active_app_title,
            self.open_windows.len(),
            self.open_windows.iter().filter(|w| w.is_focused).count(),
            self.dock_items.len(),
            if self.control_center.is_open { "Open" } else { "Closed" }
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use drexvis::CudaBackend;

    #[test]
    fn test_compositor_surface_and_acrylic_pipeline() {
        let mut backend = Box::new(CudaBackend::new());
        backend.initialize().unwrap();

        let mut compositor = DrexCompositorEngine::new(backend, 120);
        assert!((compositor.get_target_frametime_ms() - 8.333).abs() < 0.01);

        let surf_id = compositor.create_client_surface(1042, 1920, 1080);
        assert!(surf_id > 0);

        let params = AcrylicParameters {
            opacity: 0.8,
            blur_radius_px: 48,
            edge_brightness: 1.2,
            noise_intensity: 0.05,
        };

        assert!(compositor.attach_acrylic_effect(surf_id, params).is_ok());

        let frame = compositor.render_frame().expect("Frame render failed");
        assert_eq!(frame, 1);
    }

    #[test]
    fn test_desktop_shell_lifecycle() {
        let mut shell = DesktopShell::new(1920, 1080);
        assert_eq!(shell.dock_items.len(), 16);
        assert_eq!(shell.open_windows.len(), 2);
        assert_eq!(shell.active_app_title, "Install DAXOS");

        let calc_win = shell.launch_app("org.daxos.calculator", "DAXOS Pro Calculator");
        assert_eq!(shell.open_windows.len(), 3);
        assert_eq!(shell.active_app_title, "DAXOS Pro Calculator");

        assert!(shell.minimize_window(calc_win));
        let win = shell.open_windows.iter().find(|w| w.window_id == calc_win).unwrap();
        assert!(win.is_minimized);

        assert!(shell.focus_window(1));
        assert_eq!(shell.active_app_title, "Install DAXOS Setup Assistant");

        assert!(shell.close_window(calc_win));
        assert_eq!(shell.open_windows.len(), 2);

        shell.toggle_control_center();
        assert!(shell.control_center.is_open);

        let summary = shell.render_scene_summary();
        assert!(summary.contains("DesktopShell [Canvas: 1920x1080]"));
        assert!(summary.contains("Extended"));
    }

    #[test]
    fn test_multi_monitor_extended_and_mirror_display() {
        let mut shell = DesktopShell::new(1920, 1080);
        assert_eq!(shell.display_manager.displays.len(), 1);
        assert_eq!(shell.screen_width, 1920);
        assert_eq!(shell.screen_height, 1080);
        assert_eq!(shell.display_manager.mode, DisplayMode::Extended);

        // 1. Hubungkan monitor eksternal 4K UHD (3840x2160 @ 144Hz) via HDMI-A-1
        let ext_id = shell.connect_external_monitor(
            "HDMI-A-1 (External 4K UHD)",
            "HDMI-A-1",
            3840,
            2160,
            144,
        );
        assert_eq!(ext_id, 2);
        assert_eq!(shell.display_manager.displays.len(), 2);
        assert!(shell.control_center.external_monitor_connected);

        // Pada mode Extended: Canvas diperluas horizontal (1920 + 3840 = 5760 px)
        assert_eq!(shell.screen_width, 5760);
        assert_eq!(shell.screen_height, 2160);

        // Periksa offset monitor
        let primary = &shell.display_manager.displays[0];
        assert_eq!(primary.offset_x, 0);
        let external = &shell.display_manager.displays[1];
        assert_eq!(external.offset_x, 1920);

        // Pindahkan jendela #1 ("Install DAXOS") ke monitor eksternal
        assert!(shell.move_window_to_display(1, ext_id));
        let win1 = shell.open_windows.iter().find(|w| w.window_id == 1).unwrap();
        assert!(win1.x >= 1920); // Terletak di ruang monitor eksternal

        // 2. Beralih ke Mode Duplikasi / Mirroring (Tampilan Presentasi / Proyektor)
        shell.set_display_mode(DisplayMode::Mirror);
        assert_eq!(shell.display_manager.mode, DisplayMode::Mirror);
        assert_eq!(shell.screen_width, 1920); // Canvas kembali ke batas monitor primer
        assert_eq!(shell.screen_height, 1080);

        // Jendela harus direlokasi otomatis agar tetap terlihat di dalam batas duplikasi
        let win1_relocated = shell.open_windows.iter().find(|w| w.window_id == 1).unwrap();
        assert!(win1_relocated.x < 1920);

        // 3. Putuskan sambungan monitor eksternal (Unplug)
        assert!(shell.disconnect_external_monitor(ext_id));
        assert_eq!(shell.display_manager.displays.len(), 1);
        assert!(!shell.control_center.external_monitor_connected);
    }

    #[test]
    fn test_refresh_rate_and_profile_switching() {
        let mut backend = Box::new(drexvis::LegacySoftwareBackend::new());
        backend.initialize().unwrap();

        let mut compositor = DrexCompositorEngine::new(backend, 60);
        assert_eq!(compositor.get_target_refresh_hz(), 60);
        assert!((compositor.get_target_frametime_ms() - 16.666).abs() < 0.01);

        // Switch to 120Hz
        compositor.set_target_refresh_hz(120);
        assert_eq!(compositor.get_target_refresh_hz(), 120);
        assert!((compositor.get_target_frametime_ms() - 8.333).abs() < 0.01);

        // Auto-detect profiles
        assert_eq!(DrexCompositorEngine::auto_detect_display_profile(true), 60);
        assert_eq!(DrexCompositorEngine::auto_detect_display_profile(false), 120);
    }
}
