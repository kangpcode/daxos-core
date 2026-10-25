#!/usr/bin/env bash
# ==============================================================================
# DAXOS Desktop Wallpaper Manager (CLI & Wayland)
# Tool: daxos-wallpaper-manager.sh
# Purpose: Control desktop wallpaper from terminal and system scripts
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONFIG_FILE="${WORKSPACE_ROOT}/boot/wallpaper.conf"
if [[ -f "/etc/daxos/wallpaper.conf" ]]; then
  CONFIG_FILE="/etc/daxos/wallpaper.conf"
fi

show_help() {
  cat << 'EOF'
Pengelola Wallpaper Desktop DAXOS (DreXUI Wallpaper Manager)

Penggunaan:
  daxos-wallpaper-manager.sh [OPSI]

Opsi:
  -l, --list             Tampilkan semua tema wallpaper yang tersedia
  -c, --current          Tampilkan wallpaper yang sedang aktif
  -s, --set <tema|path>  Terapkan wallpaper (nama tema atau path berkas gambar lokal)
  -r, --random           Pilih dan terapkan tema wallpaper secara acak
  -h, --help             Tampilkan bantuan ini

Tema Tersedia:
  acrylic, obsidian, cyberpunk, emerald, nebula, sunrise, glacier, tokyo, gold
EOF
}

cmd_list() {
  echo -e "\e[1;36m╔═══════════════════════════════════════════════════════════════════════════╗\e[0m"
  echo -e "\e[1;36m║\e[0m  \e[1;37mDAXOS DESKTOP WALLPAPER THEME GALLERY (DreXUI 240Hz)\e[0m                     \e[1;36m║\e[0m"
  echo -e "\e[1;36m╚═══════════════════════════════════════════════════════════════════════════╝\e[0m"
  local cur
  cur="$(grep -E '^theme = ' "$CONFIG_FILE" | head -n1 | cut -d'"' -f2 || echo "acrylic")"
  echo -e " Wallpaper Aktif: \e[1;32m${cur}\e[0m (File: ${CONFIG_FILE})\n"
  printf "  %-12s %-28s %-30s\n" "KODE TEMA" "NAMA TEMA" "KARAKTER VISUAL"
  echo "───────────────────────────────────────────────────────────────────────────"
  printf "  %-12s %-28s %-30s\n" "acrylic" "Liquid Acrylic (Default)" "Vibrant Aurora & 240Hz"
  printf "  %-12s %-28s %-30s\n" "obsidian" "Obsidian AMOLED" "Deep Void & Hemat Daya"
  printf "  %-12s %-28s %-30s\n" "cyberpunk" "Cyberpunk Sunset" "Crimson Glow & Gaming"
  printf "  %-12s %-28s %-30s\n" "emerald" "Emerald Matrix" "Forest Cyan & Coding"
  printf "  %-12s %-28s %-30s\n" "nebula" "Deep Space Nebula" "Cosmic Violet & Sci-Fi"
  printf "  %-12s %-28s %-30s\n" "sunrise" "Pacific Sunrise" "Warm Amber & Fajar Pasifik"
  printf "  %-12s %-28s %-30s\n" "glacier" "Nordic Glacier Frost" "Crisp Ice & Sejuk Minimalis"
  printf "  %-12s %-28s %-30s\n" "tokyo" "Tokyo Midnight Rain" "Neon Asphalt & Urban Night"
  printf "  %-12s %-28s %-30s\n" "gold" "Rhino Platinum Gold" "Edisi Spesial DAXOS & Mewah"
  echo "═══════════════════════════════════════════════════════════════════════════"
}

cmd_current() {
  local cur
  cur="$(grep -E '^theme = ' "$CONFIG_FILE" | head -n1 | cut -d'"' -f2 || echo "acrylic")"
  echo "Wallpaper Aktif: ${cur}"
}

cmd_set() {
  local target="$1"
  sed -i "s/^theme = .*/theme = \"${target}\"/" "$CONFIG_FILE"
  echo -e "\e[1;32m[OK]\e[0m Wallpaper desktop berhasil diubah ke: \e[1m${target}\e[0m"
}

cmd_random() {
  local themes=("acrylic" "obsidian" "cyberpunk" "emerald" "nebula" "sunrise" "glacier" "tokyo" "gold")
  local selected="${themes[$RANDOM % ${#themes[@]}]}"
  cmd_set "$selected"
}

case "${1:-}" in
  -l|--list|"")
    cmd_list
    ;;
  -c|--current)
    cmd_current
    ;;
  -s|--set)
    cmd_set "${2:?Tentukan nama tema atau path berkas}"
    ;;
  -r|--random)
    cmd_random
    ;;
  -h|--help)
    show_help
    ;;
  *)
    echo "Opsi tidak dikenal: $1"
    show_help
    exit 1
    ;;
esac
