#!/usr/bin/env bash
# ==============================================================================
# DAXOS Boot Autostart Application Manager
# Binary / Tool: daxos-autostart-manager.sh
# Supports CLI manipulation & boot execution of startup applications
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONFIG_FILE="${WORKSPACE_ROOT}/boot/autostart.toml"
if [[ -f "/etc/daxos/autostart.toml" ]]; then
  CONFIG_FILE="/etc/daxos/autostart.toml"
fi

show_help() {
  cat << 'EOF'
Pengelola Aplikasi Mulai Otomatis (DAXOS Boot Autostart Manager)

Penggunaan:
  daxos-autostart-manager.sh [OPSI]

Opsi:
  -s, --status              Tampilkan status master dan daftar aplikasi auto-start
  -e, --enable <app>        Aktifkan aplikasi tertentu untuk mulai otomatis saat boot
  -d, --disable <app>       Nonaktifkan aplikasi dari mulai otomatis
  --master-on               Aktifkan sakelar master auto-start
  --master-off              Matikan sakelar master auto-start (Clean Boot Mode)
  -p, --preset <nama>       Terapkan preset: none | recommended | dev | full
  -x, --exec                Jalankan aplikasi yang diaktifkan secara berurutan (Boot Exec)
  -j, --json                Keluarkan data status dalam format JSON
  -h, --help                Tampilkan bantuan ini

Aplikasi Terdaftar:
  finder, duraserv, terminal, sysmon, dxdef, daxbro, dcodx_ide, daxword, daxsheet, camera
EOF
}

get_master_status() {
  if grep -q "master_enabled = false" "$CONFIG_FILE" 2>/dev/null; then
    echo "false"
  else
    echo "true"
  fi
}

is_app_enabled() {
  local app="$1"
  # Check if section [applications.<app>] has enabled = true
  awk -v target="[applications.${app}]" '
    $0 == target { in_sec=1; next }
    /^\[/ { in_sec=0 }
    in_sec && /^enabled = true/ { print "true"; exit }
    in_sec && /^enabled = false/ { print "false"; exit }
  ' "$CONFIG_FILE"
}

cmd_status() {
  local master
  master="$(get_master_status)"
  echo -e "\e[1;36m╔═══════════════════════════════════════════════════════════════════════════╗\e[0m"
  echo -e "\e[1;36m║\e[0m  \e[1;37mDAXOS STARTUP APPLICATIONS MANAGER (Boot Autostart)\e[0m                     \e[1;36m║\e[0m"
  echo -e "\e[1;36m╚═══════════════════════════════════════════════════════════════════════════╝\e[0m"
  
  if [[ "$master" == "true" ]]; then
    echo -e " \e[1mMaster Autostart:\e[0m \e[1;32m[AKTIF / ENABLED]\e[0m - Aplikasi terpilih akan dibuka saat booting"
  else
    echo -e " \e[1mMaster Autostart:\e[0m \e[1;31m[NONAKTIF / CLEAN BOOT]\e[0m - Boot murni tanpa aplikasi otomatis"
  fi
  echo -e " \e[1mFile Konfigurasi:\e[0m ${CONFIG_FILE}"
  echo "───────────────────────────────────────────────────────────────────────────"
  printf "  %-14s %-18s\n" "APLIKASI" "STATUS BOOT"
  echo "───────────────────────────────────────────────────────────────────────────"

  local apps=("finder" "duraserv" "terminal" "sysmon" "dxdef" "daxbro" "dcodx_ide" "daxword" "daxsheet" "camera")
  for app in "${apps[@]}"; do
    local en
    en="$(is_app_enabled "$app")"
    local status_badge
    if [[ "$master" == "false" ]]; then
      status_badge="\e[1;30mDIMATIKAN\e[0m"
    elif [[ "$en" == "true" ]]; then
      status_badge="\e[1;32mAKTIF\e[0m    "
    else
      status_badge="\e[1;31mOFF\e[0m      "
    fi
    printf "  %-14s %-18b %-8s\n" "$app" "$status_badge"
  done
  echo "═══════════════════════════════════════════════════════════════════════════"
}

cmd_set_app() {
  local app="$1"
  local val="$2"
  if ! grep -q "\[applications\.${app}\]" "$CONFIG_FILE"; then
    echo "Error: Aplikasi '${app}' tidak ditemukan dalam ${CONFIG_FILE}"
    exit 1
  fi

  # Update enabled flag within section [applications.<app>]
  python3 -c "
import sys, re
path = '${CONFIG_FILE}'
app = '${app}'
val = '${val}'
with open(path, 'r') as f:
    content = f.read()
pattern = r'(\[applications\.' + re.escape(app) + r'\][\s\S]*?enabled\s*=\s*)(true|false)'
content = re.sub(pattern, r'\g<1>' + val, content, count=1)
with open(path, 'w') as f:
    f.write(content)
"
  echo "Berhasil memperbarui ${app} -> enabled = ${val}"
}

cmd_set_master() {
  local val="$1"
  sed -i "s/master_enabled = .*/master_enabled = ${val}/" "$CONFIG_FILE"
  echo "Master Boot Autostart diperbarui -> ${val}"
}

cmd_preset() {
  local p="$1"
  case "$p" in
    none)
      cmd_set_master "false"
      for a in finder duraserv terminal sysmon dxdef daxbro dcodx_ide daxword daxsheet camera; do
        cmd_set_app "$a" "false" >/dev/null
      done
      echo "Preset 'none' diterapkan (Clean Boot - Seluruh auto-start dimatikan)"
      ;;
    recommended)
      cmd_set_master "true"
      for a in terminal sysmon dxdef daxbro dcodx_ide daxword daxsheet camera; do
        cmd_set_app "$a" "false" >/dev/null
      done
      cmd_set_app "finder" "true" >/dev/null
      cmd_set_app "duraserv" "true" >/dev/null
      echo "Preset 'recommended' diterapkan (Finder & DuraServ aktif)"
      ;;
    dev)
      cmd_set_master "true"
      for a in dxdef daxbro daxword daxsheet camera; do
        cmd_set_app "$a" "false" >/dev/null
      done
      cmd_set_app "finder" "true" >/dev/null
      cmd_set_app "duraserv" "true" >/dev/null
      cmd_set_app "terminal" "true" >/dev/null
      cmd_set_app "dcodx_ide" "true" >/dev/null
      echo "Preset 'dev' diterapkan (Finder, DuraServ, Terminal & IDE aktif)"
      ;;
    full)
      cmd_set_master "true"
      for a in finder duraserv terminal sysmon dxdef daxbro dcodx_ide daxword daxsheet camera; do
        cmd_set_app "$a" "true" >/dev/null
      done
      echo "Preset 'full' diterapkan (Semua aplikasi aktif)"
      ;;
    *)
      echo "Preset tidak dikenal: $p (Gunakan: none | recommended | dev | full)"
      exit 1
      ;;
  esac
}

cmd_exec() {
  local master
  master="$(get_master_status)"
  if [[ "$master" != "true" ]]; then
    echo "[DAXOS Boot] Master autostart dinonaktifkan. Menjalankan Clean Boot."
    exit 0
  fi

  echo "[DAXOS Boot] Memulai peluncuran aplikasi auto-start..."
  local apps=("finder" "duraserv" "terminal" "sysmon" "dxdef" "daxbro" "dcodx_ide" "daxword" "daxsheet" "camera")
  local launched=0
  for app in "${apps[@]}"; do
    local en
    en="$(is_app_enabled "$app")"
    if [[ "$en" == "true" ]]; then
      echo " -> [STARTUP] Meluncurkan aplikasi: ${app}"
      launched=$((launched + 1))
      sleep 0.1
    fi
  done
  echo "[DAXOS Boot] Selesai. ${launched} aplikasi telah diluncurkan ke desktop."
}

# CLI Argument Router
case "${1:-}" in
  -s|--status|"")
    cmd_status
    ;;
  -e|--enable)
    cmd_set_app "${2:?Tentukan nama aplikasi}" "true"
    ;;
  -d|--disable)
    cmd_set_app "${2:?Tentukan nama aplikasi}" "false"
    ;;
  --master-on)
    cmd_set_master "true"
    ;;
  --master-off)
    cmd_set_master "false"
    ;;
  -p|--preset)
    cmd_preset "${2:?Tentukan nama preset}"
    ;;
  -x|--exec)
    cmd_exec
    ;;
  -j|--json)
    master="$(get_master_status)"
    echo "{\"master_enabled\": ${master}, \"config_path\": \"${CONFIG_FILE}\"}"
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
