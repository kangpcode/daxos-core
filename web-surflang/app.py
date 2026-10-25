#!/usr/bin/env python3
"""
============================================================================
DAXOS SURFLANG BRANDING & WEB PLAYGROUND SERVER
File: web-surflang/app.py
Purpose: Serve Surflang branding site, playground API & compilation pipeline
Architect: Dhafa Nazula Permadi (@kangpcode)
Strictly ZERO Emojis
============================================================================
"""

import os
import subprocess
import json
from flask import Flask, send_from_directory, request, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    target = os.path.join(BASE_DIR, path)
    if os.path.exists(target) and os.path.isfile(target):
        return send_from_directory(BASE_DIR, path)
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/packages', methods=['GET'])
def api_packages():
    """Return standard ecosystem packages catalog."""
    packages = [
        {
            "name": "surf.core",
            "version": "1.10.2026",
            "category": "Systems & Runtime",
            "description": "Core affine memory management, RAII drop glue, and low-level system bindings",
            "modules": ["surf.core.memory", "surf.core.types", "surf.core.panic"]
        },
        {
            "name": "surf.ui",
            "version": "1.10.2026",
            "category": "User Interface",
            "description": "DreXUI declarative component system with Hydro-Glass liquid acrylic shaders and 240Hz ProMotion",
            "modules": ["surf.ui.views", "surf.ui.modifiers", "surf.ui.layout", "surf.ui.state"]
        },
        {
            "name": "surf.display",
            "version": "1.10.2026",
            "category": "Display & Graphics",
            "description": "First-class Multi-Monitor management, Extended Desktop topology, Screen Duplication (Mirror), and Display Hotplug",
            "modules": ["surf.display.manager", "surf.display.topology", "surf.display.canvas"]
        },
        {
            "name": "surf.async",
            "version": "1.10.2026",
            "category": "Concurrency",
            "description": "High-throughput asynchronous runtime with epoll, io_uring, and zero-allocation channels",
            "modules": ["surf.async.task", "surf.async.channel", "surf.async.timer"]
        },
        {
            "name": "surf.security",
            "version": "1.10.2026",
            "category": "Security & Sandbox",
            "description": "Landlock LSM ABI v5 kernel sandboxing, dm-verity cryptographic proofs, and TPM2 hardware vault",
            "modules": ["surf.security.sandbox", "surf.security.vault", "surf.security.crypto"]
        },
        {
            "name": "surf.audio",
            "version": "1.10.2026",
            "category": "Audio & Multimedia",
            "description": "PipeWire low-latency audio DSP, 10-band parametric equalizers, and 3D HRTF spatial audio",
            "modules": ["surf.audio.pipewire", "surf.audio.dsp", "surf.audio.spatial"]
        },
        {
            "name": "surf.vision",
            "version": "1.10.2026",
            "category": "Sensors & AI",
            "description": "Optical V4L2 physical camera sensors, skin-contour compactness, and Air-Grab gestures (DaXDrop)",
            "modules": ["surf.vision.camera", "surf.vision.gesture"]
        },
        {
            "name": "surf.net",
            "version": "1.10.2026",
            "category": "Networking",
            "description": "Zero-copy TCP/UDP networking, HTTP/3 QUIC, TLS 1.3 / Kyber hybrid post-quantum encryption, and Wi-Fi Direct",
            "modules": ["surf.net.socket", "surf.net.http", "surf.net.p2p"]
        },
        {
            "name": "surf.systemd",
            "version": "1.10.2026",
            "category": "Operating System",
            "description": "Systemd D-Bus supervisor, cgroups v2 resource slices, socket activation listeners, and journald telemetry",
            "modules": ["surf.systemd.service", "surf.systemd.slice", "surf.systemd.socket", "surf.systemd.journal"]
        },
        {
            "name": "surf.storage",
            "version": "1.10.2026",
            "category": "Filesystem & Block",
            "description": "Btrfs CoW snapshot management, subvolume encryption with fscrypt, and NVMe SSD TRIM scheduler",
            "modules": ["surf.storage.btrfs", "surf.storage.nvme", "surf.storage.crypto"]
        }
    ]
    return jsonify({"status": "SUCCESS", "packages": packages})

@app.route('/api/compile', methods=['POST'])
def api_compile():
    """Compile Surflang source code into LLVM IR and analysis report."""
    data = request.get_json(force=True, silent=True) or {}
    source = data.get('source', '')
    if not source.strip():
        return jsonify({"status": "ERROR", "message": "Source code cannot be empty"}), 400

    temp_surf = '/tmp/surflang_web_temp.surf'
    try:
        with open(temp_surf, 'w', encoding='utf-8') as f:
            f.write(source)

        cmd = ['cargo', 'run', '-q', '-p', 'dcodx-cli', '--', 'analyze', temp_surf]
        res = subprocess.run(cmd, cwd=WORKSPACE_ROOT, capture_output=True, text=True, timeout=10)
        
        output_txt = res.stdout.strip()
        is_success = (res.returncode == 0)

        return jsonify({
            "status": "SUCCESS" if is_success else "ERROR",
            "report_output": output_txt,
            "error_output": res.stderr.strip() if not is_success else None,
            "multi_monitor_ready": "Multi-Monitor Ready  : YES" in output_txt
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500
    finally:
        if os.path.exists(temp_surf):
            try:
                os.remove(temp_surf)
            except OSError:
                pass

@app.route('/api/displays', methods=['GET'])
def api_displays():
    """Return active display topology information."""
    return jsonify({
        "status": "SUCCESS",
        "topology_modes": ["extended", "mirror", "primary_only", "external_only"],
        "virtual_canvas": {
            "extended": {"width": 5760, "height": 2160},
            "mirror": {"width": 1920, "height": 1080}
        },
        "displays": [
            {
                "id": 1,
                "name": "eDP-1 (Internal Retina)",
                "connector": "eDP-1",
                "is_primary": True,
                "width": 1920,
                "height": 1080,
                "refresh_hz": 120,
                "scale": 1.0,
                "status": "ACTIVE"
            },
            {
                "id": 2,
                "name": "Studio Display Pro (External 4K UHD)",
                "connector": "HDMI-A-1",
                "is_primary": False,
                "width": 3840,
                "height": 2160,
                "refresh_hz": 144,
                "scale": 1.0,
                "status": "ACTIVE"
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5055))
    print(f"[OK] Surflang Branding & Playground Server running on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
