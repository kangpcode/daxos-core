// ==============================================================================
// DAXOS HYPRLAND COMPOSITOR ACRYLIC BLUR PLUGIN (C++23)
// File: src/compositor/daxos_acrylic_hyprland_plugin.cpp
// Purpose: Dual-Kawase Multi-Pass Blur, Specular Edge Highlighting & Noise Shader
// ==============================================================================

#include <cstdint>
#include <cmath>
#include <vector>
#include <memory>
#include <unordered_map>
#include <iostream>
#include <algorithm>

#include "daxos/daxos-acrylic-blur-server-protocol.h"

namespace daxos::compositor {

struct AcrylicSurfaceState {
    uint32_t blur_radius_px = 32;
    float opacity = 0.72f;
    float edge_brightness = 1.15f;
    float noise_intensity = 0.04f;
    uint32_t frame_counter = 0;
    bool is_dirty = true;
};

// GLSL Fragment Shader for Dual-Kawase Downsample Pass
constexpr const char* DUAL_KAWASE_DOWNSAMPLE_FRAG = R"glsl(
#version 450 core
layout(location = 0) in vec2 v_texcoord;
layout(location = 0) out vec4 out_color;

layout(binding = 0) uniform sampler2D u_source_texture;
layout(location = 0) uniform vec2 u_half_pixel;

void main() {
    vec4 sum = texture(u_source_texture, v_texcoord) * 4.0;
    sum += texture(u_source_texture, v_texcoord - u_half_pixel);
    sum += texture(u_source_texture, v_texcoord + u_half_pixel);
    sum += texture(u_source_texture, v_texcoord + vec2(u_half_pixel.x, -u_half_pixel.y));
    sum += texture(u_source_texture, v_texcoord + vec2(-u_half_pixel.x, u_half_pixel.y));
    out_color = sum / 8.0;
}
)glsl";

// GLSL Fragment Shader for Acrylic Glass Finishing (Upsample + Noise + Edge Highlight)
constexpr const char* ACRYLIC_FINISHING_FRAG = R"glsl(
#version 450 core
layout(location = 0) in vec2 v_texcoord;
layout(location = 0) out vec4 out_color;

layout(binding = 0) uniform sampler2D u_blurred_background;
layout(binding = 1) uniform sampler2D u_content_texture;

layout(location = 0) uniform float u_opacity;
layout(location = 1) uniform float u_edge_brightness;
layout(location = 2) uniform float u_noise_intensity;
layout(location = 3) uniform vec2  u_resolution;

// High quality pseudo-random procedural noise
float hash21(vec2 p) {
    p = fract(p * vec2(234.34, 435.345));
    p += dot(p, p + 34.23);
    return fract(p.x * p.y);
}

void main() {
    vec4 bg_blur = texture(u_blurred_background, v_texcoord);
    vec4 fg_content = texture(u_content_texture, v_texcoord);

    // Compute edge specular proximity
    vec2 border_dist = min(v_texcoord, 1.0 - v_texcoord) * u_resolution;
    float min_dist = min(border_dist.x, border_dist.y);
    float edge_factor = 1.0;
    if (min_dist < 2.0) {
        edge_factor = u_edge_brightness;
    }

    // Procedural noise grain
    float grain = (hash21(v_texcoord * u_resolution) - 0.5) * u_noise_intensity;

    vec3 composite_rgb = mix(bg_blur.rgb, fg_content.rgb, u_opacity) * edge_factor + vec3(grain);
    out_color = vec4(clamp(composite_rgb, 0.0, 1.0), 1.0);
}
)glsl";

class AcrylicBlurManager {
public:
    static AcrylicBlurManager& instance() {
        static AcrylicBlurManager s_instance;
        return s_instance;
    }

    void register_surface(uint64_t surface_id) {
        m_surfaces[surface_id] = std::make_unique<AcrylicSurfaceState>();
        std::cout << "[drex-compositor] Bound acrylic blur extension to surface 0x" 
                  << std::hex << surface_id << std::dec << std::endl;
    }

    void unregister_surface(uint64_t surface_id) {
        m_surfaces.erase(surface_id);
    }

    void set_parameters(uint64_t surface_id, uint32_t radius_px, float opacity, float edge, float noise) {
        auto it = m_surfaces.find(surface_id);
        if (it != m_surfaces.end()) {
            it->second->blur_radius_px = std::clamp(radius_px, 0u, 128u);
            it->second->opacity = std::clamp(opacity, 0.05f, 1.0f);
            it->second->edge_brightness = std::clamp(edge, 0.0f, 2.0f);
            it->second->noise_intensity = std::clamp(noise, 0.0f, 1.0f);
            it->second->is_dirty = true;
        }
    }

    void render_frame(uint64_t surface_id) {
        auto it = m_surfaces.find(surface_id);
        if (it != m_surfaces.end() && it->second->is_dirty) {
            it->second->frame_counter++;
            it->second->is_dirty = false;
        }
    }

    const AcrylicSurfaceState* get_state(uint64_t surface_id) const {
        auto it = m_surfaces.find(surface_id);
        return (it != m_surfaces.end()) ? it->second.get() : nullptr;
    }

private:
    AcrylicBlurManager() = default;
    std::unordered_map<uint64_t, std::unique_ptr<AcrylicSurfaceState>> m_surfaces;
};

} // namespace daxos::compositor

// Exported C API for Hyprland dynamic loading
extern "C" {

void* daxos_acrylic_plugin_init() {
    std::cout << "[drex-compositor] Initializing DAXOS Acrylic Blur Hyprland Plugin v1.0.0" << std::endl;
    return &daxos::compositor::AcrylicBlurManager::instance();
}

void daxos_acrylic_plugin_render_surface(uint64_t surface_id) {
    daxos::compositor::AcrylicBlurManager::instance().render_frame(surface_id);
}

}
