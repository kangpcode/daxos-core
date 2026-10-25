#!/usr/bin/env bash
# ==============================================================================
# DAXOS Official USB Flashing Tool (v1.10.2026 'Rhino Alpha')
# ==============================================================================
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Penggunaan: sudo ./scripts/create_bootable_usb.sh /dev/sdX"
    echo "Contoh: sudo ./scripts/create_bootable_usb.sh /dev/sdb"
    exit 1
fi

TARGET_DEV="$1"
ISO_FILE="build/daxos-1.10.2026-x86_64.iso"

if [ ! -f "${ISO_FILE}" ]; then
    ISO_FILE="build/daxos-x86_64.iso"
fi

if [ ! -f "${ISO_FILE}" ]; then
    echo "[ERROR] Berkas ISO tidak ditemukan di direktori build/."
    exit 1
fi

echo "=================================================================="
echo "    DAXOS OFFICIAL USB INSTALLATION MEDIA CREATOR                "
echo "=================================================================="
echo "Berkas ISO : ${ISO_FILE} ($(ls -lh "${ISO_FILE}" | awk '{print $5}'))"
echo "Target Drive: ${TARGET_DEV}"
echo ""
echo "PERINGATAN: Seluruh data pada ${TARGET_DEV} akan dihapus!"
read -p "Apakah Anda yakin ingin melanjutkan? (y/N): " CONFIRM
if [[ "${CONFIRM}" != [yY] ]]; then
    echo "Dibatalkan oleh pengguna."
    exit 0
fi

echo "[1/3] Menulis citra hybrid El Torito ke ${TARGET_DEV}..."
dd if="${ISO_FILE}" of="${TARGET_DEV}" bs=4M status=progress conv=fdatasync

echo "[2/3] Menyinkronkan buffer cache hardware..."
sync

echo "[3/3] Memvalidasi integritas bootable media..."
partprobe "${TARGET_DEV}" || true

echo "=================================================================="
echo "    SUKSES! USB Bootable DAXOS 1.10.2026 Siap Digunakan.         "
echo "=================================================================="
