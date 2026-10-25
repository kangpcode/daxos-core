#!/bin/bash
# ==============================================================================
# DAXOS END-TO-END INTEGRATION & VERIFICATION SUITE
# File: scripts/run_e2e_verification.sh
# Purpose: Comprehensive validation of all DAXOS sub-ecosystems (kernel configs,
#          drivers, compiler, packaging, registry, sandbox, OTA, and bootloader)
# ==============================================================================

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${WORKSPACE_ROOT}"

echo "=================================================================="
echo "    DAXOS OPERATING SYSTEM - END-TO-END VERIFICATION HARNESS      "
echo "=================================================================="

# STEP 1: Cargo Workspace Compilation, Unit Testing & Fuzzing
echo -e "\n[STEP 1/10] Running Cargo Workspace Tests, Daemon IPC & Fuzzing Suite..."
cargo test --workspace
cargo test -p dcodx-bundle --test test_dapp_header_fuzz
cargo test -p dcodx-cli --test test_daemon_services
echo "[PASS] All workspace unit tests, fuzzer tests, and daemon IPC tests passed with 0 errors!"

# STEP 2: SQLite Registry Schema DDL & Triggers
echo -e "\n[STEP 2/10] Validating SQLite Registry Schema & Triggers..."
TEST_DB="/tmp/daxos_e2e_registry.db"
rm -f "${TEST_DB}"
sqlite3 "${TEST_DB}" < schema/daxos_registry.sql
NODE_COUNT=$(sqlite3 "${TEST_DB}" "SELECT COUNT(*) FROM system_nodes;")
SLOT_COUNT=$(sqlite3 "${TEST_DB}" "SELECT COUNT(*) FROM bootloader_slots;")
DRIVER_COUNT=$(sqlite3 "${TEST_DB}" "SELECT COUNT(*) FROM drivers;")

if [ "${NODE_COUNT}" -ge 1 ] && [ "${SLOT_COUNT}" -ge 2 ] && [ "${DRIVER_COUNT}" -ge 2 ]; then
    echo "[PASS] Database schema initialized successfully: ${NODE_COUNT} node, ${SLOT_COUNT} boot slots, ${DRIVER_COUNT} drivers."
else
    echo "[FAIL] Database initialization error"
    exit 1
fi
rm -f "${TEST_DB}"

# STEP 3: Wayland Acrylic Protocol Validation & C++ Plugin Compilation
echo -e "\n[STEP 3/10] Validating Wayland Protocol XML & C++ Plugin..."
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('protocols/daxos-acrylic-blur-v1.xml')
root = tree.getroot()
assert root.tag == 'protocol'
assert root.attrib.get('name') == 'daxos_acrylic_blur_v1'
"
g++ -std=c++20 -I include -c src/compositor/daxos_acrylic_hyprland_plugin.cpp -o /tmp/daxos_plugin_test.o
gcc -I include -c src/compositor/daxos-acrylic-blur-protocol.c -o /tmp/daxos_protocol_test.o
rm -f /tmp/daxos_plugin_test.o /tmp/daxos_protocol_test.o
echo "[PASS] Wayland protocol daxos-acrylic-blur-v1 and C++ Hyprland plugin compiled cleanly!"

# STEP 4: DCODX Compiler on Surflang Sources & LLVM IR Generation
echo -e "\n[STEP 4/10] Compiling Surflang Components & Emitting LLVM IR..."
cargo run -p dcodx-cli -- build src/ui/PreferencesPanel.surf
cargo run -p dcodx-cli -- build examples/calculator/src/main.surf
cargo run -p dcodx-cli -- build examples/preferences/src/main.surf
cargo run -p dcodx-cli -- build examples/camera/src/main.surf
cargo run -p dcodx-cli -- build examples/terminal/src/main.surf
cargo run -p dcodx-cli -- build examples/files/src/main.surf
cargo run -p dcodx-cli -- build examples/installer/src/main.surf
cargo run -p dcodx-cli -- build examples/store/src/main.surf
cargo run -p dcodx-cli -- build examples/dcodx-ide/src/main.surf
cargo run -p dcodx-cli -- build examples/daxbro/src/main.surf
cargo run -p dcodx-cli -- build examples/dxdef/src/main.surf
cargo run -p dcodx-cli -- build examples/editor/src/main.surf
cargo run -p dcodx-cli -- build examples/sysmon/src/main.surf
cargo run -p dcodx-cli -- build examples/disks/src/main.surf
cargo run -p dcodx-cli -- build examples/media/src/main.surf
cargo run -p dcodx-cli -- build examples/daxdrop/src/main.surf
cargo run -p dcodx-cli -- build examples/duraserv/src/main.surf
test -f src/ui/PreferencesPanel.surf.ll
test -f examples/calculator/src/main.surf.ll
test -f examples/preferences/src/main.surf.ll
test -f examples/camera/src/main.surf.ll
test -f examples/terminal/src/main.surf.ll
test -f examples/files/src/main.surf.ll
test -f examples/installer/src/main.surf.ll
test -f examples/store/src/main.surf.ll
test -f examples/dcodx-ide/src/main.surf.ll
test -f examples/daxbro/src/main.surf.ll
test -f examples/dxdef/src/main.surf.ll
test -f examples/editor/src/main.surf.ll
test -f examples/sysmon/src/main.surf.ll
test -f examples/disks/src/main.surf.ll
test -f examples/media/src/main.surf.ll
test -f examples/daxdrop/src/main.surf.ll
test -f examples/duraserv/src/main.surf.ll
echo "[PASS] All 16 Surflang components compiled cleanly into DreX-HIR and LLVM IR!"

# STEP 5: Universal .dapp Packaging, Native ELF64 Binaries, Sandboxing & Scaffolding
echo -e "\n[STEP 5/10] Packaging Universal .dapp, Signing, Sandboxed Execution & Scaffolding..."
TMP_DAPPS_DIR="/tmp/daxos_e2e_dapps"
mkdir -p "${TMP_DAPPS_DIR}"

for app in calculator preferences camera terminal files installer store dcodx-ide daxbro dxdef editor sysmon disks media daxdrop duraserv; do
    DAPP_PKG="${TMP_DAPPS_DIR}/${app}.dapp"
    cargo run -p dcodx-cli -- pack "examples/${app}/manifest.toml" -o "${DAPP_PKG}"
    cargo run -p dcodx-cli -- verify "${DAPP_PKG}"
    cargo run -p dcodx-cli -- run "${DAPP_PKG}"
done
cargo run -p dap-sandboxd -- launch "${TMP_DAPPS_DIR}/calculator.dapp"
cargo run -p dap-sandboxd -- launch "${TMP_DAPPS_DIR}/camera.dapp"
cargo run -p dap-sandboxd -- launch "${TMP_DAPPS_DIR}/installer.dapp"
cargo run -p dap-sandboxd -- launch "${TMP_DAPPS_DIR}/editor.dapp"
cargo run -p dap-sandboxd -- launch "${TMP_DAPPS_DIR}/sysmon.dapp"
cargo run -p dap-sandboxd -- launch "${TMP_DAPPS_DIR}/media.dapp"

# Developer Workflow: Scaffolding new app via dcodx new
NEW_APP_DIR="/tmp/daxos_e2e_scaffold_app"
rm -rf "${NEW_APP_DIR}" "${NEW_APP_DIR}.dapp"
cargo run -p dcodx-cli -- new "${NEW_APP_DIR}"
cargo run -p dcodx-cli -- build "${NEW_APP_DIR}/src/main.surf"
cargo run -p dcodx-cli -- pack "${NEW_APP_DIR}/manifest.toml" -o "${NEW_APP_DIR}.dapp"
cargo run -p dcodx-cli -- verify "${NEW_APP_DIR}.dapp"
cargo run -p dcodx-cli -- run "${NEW_APP_DIR}.dapp"

# Production Blueprint Project Package (.dbpp) Toolchain Roundtrip
cargo run -p dcodx-cli -- pack-dbpp "${NEW_APP_DIR}" -o "/tmp/test_scaffold.dbpp"
cargo run -p dcodx-cli -- inspect-dbpp "/tmp/test_scaffold.dbpp"
cargo run -p dcodx-cli -- build-dbpp "/tmp/test_scaffold.dbpp" -o "/tmp/test_scaffold_built.dapp"
cargo run -p dcodx-cli -- verify "/tmp/test_scaffold_built.dapp"
cargo run -p dcodx-cli -- unpack-dbpp "/tmp/test_scaffold.dbpp" -d "/tmp/test_scaffold_unpacked"
test -f "/tmp/test_scaffold_unpacked/Project.toml"
test -f "/tmp/test_scaffold_unpacked/src/main.surf"
rm -rf "${NEW_APP_DIR}" "${NEW_APP_DIR}.dapp" "${TMP_DAPPS_DIR}" "/tmp/test_scaffold.dbpp" "/tmp/test_scaffold_built.dapp" "/tmp/test_scaffold_unpacked"

echo "[PASS] Universal .dapp fat binary packing, .dbpp blueprint packages, Ed25519 verification, sandboxing, and scaffolding verified!"

# STEP 6: In-Kernel Subsystems, Modules Compilation & Driver Chaos Fault Injection
echo -e "\n[STEP 6/10] Building DAXOS Kernel Modules & Running In-Kernel Test Harness..."
./scripts/build_kernel.sh
make -C kernel/tests test
echo "[PASS] In-kernel NTSync driver, DreX-Boost governor, and security supervisor verified!"

echo -e "\n[STEP 6.2/10] Executing Driver Chaos Fault Injection..."
./tests/chaos/test_driver_fault_injection.sh
echo "[PASS] Driver recovery within <= 45ms SLA verified!"

# STEP 7: Power-Loss Resiliency & GRUB A/B Rollback Recovery
echo -e "\n[STEP 7/10] Executing Power-Loss Resiliency & Rollback Recovery..."
./tests/power_loss/test_ota_power_loss_recovery.sh
cargo run -p dcodx-cli -- ota simulate-rollback
echo "[PASS] Power-loss recovery and GRUB 2.12 A/B rollback verified!"

# STEP 8: Systemd Daemon Services & System Doctor Check
echo -e "\n[STEP 8/10] Validating Systemd Daemon Services, Remote OTA Sync & Cross-Platform Runner..."
test -f boot/systemd/dap-registryd.service
test -f boot/systemd/dap-sandboxd.service
test -f boot/systemd/dap-updated.service
test -f boot/systemd/drex-boostd.service
test -f boot/systemd/drex-compositor.service
test -f boot/systemd/dax-sysmon.service
test -f boot/systemd/dax-netd.service
test -f boot/systemd/dax-sec.service
test -f boot/systemd/dax-audiod.service
test -f boot/systemd/dax-disks.service
test -f boot/systemd/daxdrop.service
test -f boot/systemd/dap-compat.service
test -f boot/systemd/dax-pkgd.service
test -f boot/systemd/dax-powerd.service
test -f boot/systemd/dax-bluetoothd.service
test -f boot/systemd/dap-registryd.socket
test -f boot/systemd/dap-sandboxd.socket
test -f boot/systemd/daxos.slice
test -f boot/systemd/daxos-system.slice
test -f boot/systemd/daxos-apps.slice
test -f boot/systemd/daxos-drivers.slice
test -f boot/systemd/50-daxos.preset
test -f boot/systemd/journald-daxos.conf
test -f boot/systemd/daxos.target

# Validate standalone daemon executables
cargo run -p dap-registryd -- --status
cargo run -p dap-sandboxd -- --status
cargo run -p dap-updated -- --status

# Launch temporary DaXCloud OTA service on port 5051 for remote sync validation
PORT=5051 python3 web-daxcloud/app.py >/dev/null 2>&1 &
DAXCLOUD_PID=$!
sleep 1.5

cargo run -p dap-updated -- --check-remote
cargo run -p dap-updated -- --sync-ota
kill "${DAXCLOUD_PID}" 2>/dev/null || true

cargo run -p drex-boostd -- --simulate
cargo run -p drex-compositor -- --benchmark
cargo run -p dap-compat --bin dax-run -- --list-runtimes
cargo run -p dcodx-cli -- doctor
echo "[PASS] All daemon services, remote DaXCloud OTA sync, and universal runtime subsystems ready!"

# STEP 9: macOS Desktop Shell, Bootable ISO & VM Execution Engine
echo -e "\n[STEP 9/10] Validating Desktop Shell, Bootable Hybrid ISO & VM Execution Engine..."
cargo run -p drex-compositor -- --desktop
cargo run -p dcodx-cli -- desktop

# Build & Validate Bootable Hybrid ISO
./scripts/build_iso.sh
test -f build/daxos-x86_64.iso
file build/daxos-x86_64.iso | grep -q "ISO 9660"
# Verify volume ID DAXOS_1_10_2026
python3 -c "
import pycdlib
iso = pycdlib.PyCdlib()
iso.open('build/daxos-x86_64.iso')
assert b'DAXOS_1_10_2026' in iso.pvd.volume_identifier
iso.close()
print('[PASS] ISO Volume ID matches DAXOS_1_10_2026')
"
echo "[PASS] Hybrid El Torito bootable ISO verified: build/daxos-x86_64.iso ($(ls -lh build/daxos-x86_64.iso | awk '{print $5}'))"

# Validate QEMU VM Execution runner
./scripts/run_qemu_vm.sh --dry-run
echo "[PASS] QEMU VM hardware execution harness validated!"

# STEP 10: Production Core OS Applications & Utilities
echo -e "\n[STEP 10/10] Validating Native Core OS Utilities & Production Apps..."
test -f boot/systemd/dax-sysmon.service
test -f boot/systemd/dax-netd.service

cargo run -p dax-pkg -- stats
cargo run -p dax-pkg -- list --system
cargo run -p daxsh -- -c "fetch"
cargo run -p daxsh -- -c "service list"
cargo run -p daxsh -- -c "service slices"
cargo run -p daxsh -- -c "service status dap-registryd"
cargo run -p daxsh -- -c "disks"
cargo run -p dax-sysmon -- --once
cargo run -p dax-sysmon -- --chart
cargo run -p dax-netd -- status
cargo run -p dax-netd -- wifi scan
cargo run -p dax-netd -- dev
cargo run -p dax-netd -- trace 1.1.1.1
cargo run -p dax-netd -- subnet 10.0.0.0/16
cargo run -p dax-netd -- stats
cargo run -p dax-netd -- routes
cargo run -p dax-netd -- vpn
cargo run -p dax-installer
cargo run -p dax-calc -- "2 * (10 + 5) - sqrt(81)"
cargo run -p dax-calc -- base 65535
cargo run -p dax-calc -- conv 100 c f
cargo run -p dax-files -- ls
cargo run -p dax-files -- info Cargo.toml
cargo run -p dax-edit -- count Cargo.toml
cargo run -p dax-edit -- hex Cargo.toml
cargo run -p dax-sec -- status
cargo run -p dax-sec -- scan Cargo.toml
cargo run -p dax-sec -- firewall status
cargo run -p dax-disks -- list
cargo run -p dax-disks -- mounts
cargo run -p dax-disks -- usage /
cargo run -p dax-audiod -- status
cargo run -p dax-audiod -- cards
cargo run -p dax-audiod -- set-vol 80
cargo run -p drexvis --bin ddrv -- status
cargo run -p drexvis --bin ddrv -- probe
cargo run -p drexvis --bin ddrv -- health
cargo run -p drexvis --bin ddrv -- benchmark
cargo run -p daxdrop -- status
cargo run -p daxdrop -- cameras
cargo run -p daxdrop -- gesture
cargo run -p dap-compat --bin dax-run -- --list-runtimes
cargo run -p dap-compat --bin dax-trans -- /bin/ls
cargo run -p dcodx-cli -- lsp
cargo run -p dcodx-cli -- sdk
cargo run -p dcodx-cli -- studio
cargo run -p dcodx-cli -- test
cargo run -p dax-netd -- ping 1.1.1.1
cargo run -p daxsh -- -c "ping 1.1.1.1"
cargo run -p dax-bro -- version
cargo run -p dax-bro -- procs
cargo run -p dax-bro -- benchmark
cargo run -p dax-bro -- extensions list
cargo run -p dax-media -- info Cargo.toml
cargo run -p dax-media -- play sample.flac
cargo run -p dax-media -- view photo.avif
cargo run -p dax-media -- eq clarity
cargo run -p dax-media -- spatial on
cargo run -p dax-office -- version
cargo run -p dax-office -- word
cargo run -p dax-office -- sheet
cargo run -p dax-office -- slide
cargo run -p dax-office -- stats
cargo run -p dax-clock -- version
cargo run -p dax-clock -- world
cargo run -p dax-clock -- alarm
cargo run -p dax-clock -- stopwatch
cargo run -p dax-clock -- timer
cargo run -p dax-font -- version
cargo run -p dax-font -- list
cargo run -p dax-font -- info "Inter Display"
cargo run -p dax-font -- config
cargo run -p dax-font -- glyphs "Inter Display"
echo "[PASS] All production core OS utilities & developer toolchains (dcodx, dax, daxsh, dtop, dnet, ping, dax-installer, dcalc, dfm, dedit, dxdef-cli, ddisk, daudio, ddrv, daxdrop, dax-run, dax-trans, daxbro, dmedia, doffice, dclock, dfont) validated successfully!"

echo -e "\n=================================================================="
echo "    DAXOS VERIFICATION COMPLETE: ALL 10 GATES AND TESTS PASSED!  "
echo "=================================================================="

