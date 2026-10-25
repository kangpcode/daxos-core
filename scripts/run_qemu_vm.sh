#!/bin/bash
# ==============================================================================
# DAXOS QEMU VIRTUAL MACHINE RUNNER
# File: scripts/run_qemu_vm.sh
# Purpose: Launches DAXOS in a high-performance QEMU virtual machine instance
#          booting directly from build/daxos-x86_64.iso with VirtIO hardware
#          acceleration, UEFI/BIOS boot, and headless/VNC/GUI display modes.
# ==============================================================================

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${WORKSPACE_ROOT}"

ISO_IMAGE="build/daxos-x86_64.iso"
DISK_IMAGE="build/daxos_virtual_disk.qcow2"
DISK_SIZE="64G"
RAM="4096"
SMP="4"
DISPLAY_MODE="auto"
VNC_PORT=":1"
ENABLE_KVM=true
DRY_RUN=false

print_usage() {
    echo "DAXOS Virtual Machine Launcher (QEMU)"
    echo "Usage: ./scripts/run_qemu_vm.sh [options]"
    echo ""
    echo "Options:"
    echo "  --iso <path>            Path to bootable ISO (default: build/daxos-x86_64.iso)"
    echo "  --memory <MB>           RAM size in MB (default: 4096)"
    echo "  --smp <cores>           Number of virtual CPU cores (default: 4)"
    echo "  --display <mode>        Display output: gtk, sdl, cocoa, vnc, none (default: auto)"
    echo "  --vnc <display>         VNC display address (default: :1 -> port 5901)"
    echo "  --no-kvm                Disable KVM hardware acceleration (use TCG emulator)"
    echo "  --dry-run               Print QEMU command line without executing"
    echo "  --create-disk           Initialize 64GB QCOW2 virtual disk for installer testing"
    echo "  -h, --help              Show this help menu"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --iso)
            ISO_IMAGE="$2"
            shift 2
            ;;
        --memory)
            RAM="$2"
            shift 2
            ;;
        --smp)
            SMP="$2"
            shift 2
            ;;
        --display)
            DISPLAY_MODE="$2"
            shift 2
            ;;
        --vnc)
            DISPLAY_MODE="vnc"
            VNC_PORT="$2"
            shift 2
            ;;
        --no-kvm)
            ENABLE_KVM=false
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --create-disk)
            mkdir -p build
            qemu-img create -f qcow2 "${DISK_IMAGE}" "${DISK_SIZE}"
            echo "[OK] Created ${DISK_SIZE} virtual disk at ${DISK_IMAGE}"
            exit 0
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Ensure ISO exists
if [[ ! -f "${ISO_IMAGE}" ]]; then
    echo "[run_qemu_vm] ISO image not found at ${ISO_IMAGE}. Triggering automated build..."
    ./scripts/build_iso.sh
fi

# Locate QEMU binary
QEMU_BIN=""
for bin in qemu-system-x86_64 /usr/bin/qemu-system-x86_64 /usr/local/bin/qemu-system-x86_64; do
    if command -v "${bin}" &>/dev/null; then
        QEMU_BIN="${bin}"
        break
    fi
done

if [[ -z "${QEMU_BIN}" ]]; then
    echo "WARNING: qemu-system-x86_64 binary not found in PATH."
    echo "Displaying simulated execution arguments for reference:"
    QEMU_BIN="qemu-system-x86_64"
fi

# Build QEMU arguments
QEMU_ARGS=(
    "${QEMU_BIN}"
    "-name" "DAXOS-Virtual-Machine"
    "-m" "${RAM}"
    "-smp" "${SMP}"
    "-cpu" "host"
    "-boot" "d"
    "-cdrom" "${ISO_IMAGE}"
    "-net" "nic,model=virtio"
    "-net" "user"
    "-vga" "virtio"
)

# KVM Check
if [[ "${ENABLE_KVM}" == true ]] && [[ -e /dev/kvm ]] && [[ -r /dev/kvm ]] && [[ -w /dev/kvm ]]; then
    QEMU_ARGS+=("-enable-kvm")
else
    # Fallback to TCG max CPU
    QEMU_ARGS+=("-cpu" "max")
fi

# Display selection
if [[ "${DISPLAY_MODE}" == "auto" ]]; then
    if [[ -n "${DISPLAY:-}" ]]; then
        QEMU_ARGS+=("-display" "gtk,gl=on")
    else
        QEMU_ARGS+=("-display" "none" "-vnc" "${VNC_PORT}")
        echo "[run_qemu_vm] Headless environment detected. VNC server enabled on ${VNC_PORT} (port 5901)."
    fi
elif [[ "${DISPLAY_MODE}" == "vnc" ]]; then
    QEMU_ARGS+=("-display" "none" "-vnc" "${VNC_PORT}")
    echo "[run_qemu_vm] VNC display mode selected on ${VNC_PORT}."
else
    QEMU_ARGS+=("-display" "${DISPLAY_MODE}")
fi

# Target installation virtual disk (if present)
if [[ -f "${DISK_IMAGE}" ]]; then
    QEMU_ARGS+=("-drive" "file=${DISK_IMAGE},if=virtio,format=qcow2")
    echo "[run_qemu_vm] Attached VirtIO installation disk: ${DISK_IMAGE}"
fi

echo "=================================================================="
echo "    DAXOS 1.0 HARDWARE ACCELERATED VIRTUAL MACHINE RUNNER         "
echo "=================================================================="
echo "  ISO Path      : ${ISO_IMAGE}"
echo "  RAM Memory    : ${RAM} MB"
echo "  CPU Cores     : ${SMP}"
echo "  VGA Device    : VirtIO GPU (Wayland Acrylic Compositor Ready)"
echo "  Command Line  : ${QEMU_ARGS[*]}"
echo "=================================================================="

if [[ "${DRY_RUN}" == true ]]; then
    echo "Dry run completed. Command is ready to be launched."
    exit 0
fi

if ! command -v "${QEMU_BIN}" &>/dev/null; then
    echo "Notice: Install 'qemu-system-x86' to execute directly on host."
    exit 0
fi

exec "${QEMU_ARGS[@]}"
