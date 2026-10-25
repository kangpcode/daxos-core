#!/bin/bash
# ==============================================================================
# DAXOS MARK-GOOD NOTIFICATION UTILITY
# File: boot/scripts/daxos-mark-good.sh
# Purpose: Marks active boot slot as healthy upon successful compositor startup
# ==============================================================================

set -euo pipefail

METADATA_ENV="/boot/efi/EFI/daxos/grubenv"

if [ ! -f "${METADATA_ENV}" ]; then
    echo "[dap-updated] Creating default metadata environment at ${METADATA_ENV}..."
    mkdir -p "$(dirname "${METADATA_ENV}")"
    grub-editenv "${METADATA_ENV}" create
    grub-editenv "${METADATA_ENV}" set slot_active=A slot_pending=none boot_counter=0 slot_successful=1
fi

CURRENT_SLOT=$(grub-editenv "${METADATA_ENV}" list | grep 'slot_pending' | cut -d'=' -f2 || echo "none")

if [ "${CURRENT_SLOT}" != "none" ] && [ -n "${CURRENT_SLOT}" ]; then
    echo "[dap-updated] New slot ${CURRENT_SLOT} has successfully booted and presented UI."
    echo "[dap-updated] Marking slot ${CURRENT_SLOT} as active and setting boot_counter=0..."
    grub-editenv "${METADATA_ENV}" set slot_active="${CURRENT_SLOT}"
    grub-editenv "${METADATA_ENV}" set slot_pending="none"
    grub-editenv "${METADATA_ENV}" set boot_counter=0
    grub-editenv "${METADATA_ENV}" set slot_successful=1
    echo "[dap-updated] Mark-good completed successfully."
else
    # Regular successful boot on existing slot
    grub-editenv "${METADATA_ENV}" set boot_counter=0
    echo "[dap-updated] Boot counter reset to 0 for slot."
fi
