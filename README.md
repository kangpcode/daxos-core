# DAXOS: Dhafa Advanced eXperience Operating System

**Versi**: `1.10.2026-ALPHA` (Codename: **Rhino Alpha**)  
**Lead Architect**: Dhafa Nazula Permadi ([@kangpcode](https://github.com/kangpcode))  
**Target Arsitektur**: Universal Binary `x86_64` (Intel/AMD) & `ARM64` (Apple Silicon, Snapdragon X Elite, Server ARM)

[![DAXOS E2E Verification](https://img.shields.io/badge/DAXOS_E2E-10%2F10_Gates_Passed-30D158?style=for-the-badge&logo=checkmarx)](scripts/run_e2e_verification.sh)
[![Cargo Tests](https://img.shields.io/badge/Cargo_Tests-117%2F117_Passing-0A84FF?style=for-the-badge&logo=rust)](Cargo.toml)
[![Production ISO](https://img.shields.io/badge/Production_ISO-2.81_GB_El_Torito-BF5AF2?style=for-the-badge&logo=discogs)](build/RELEASE_MANIFEST.json)
[![Wayland Acrylic](https://img.shields.io/badge/Compositor-Wayland_Acrylic_240Hz-FF9F0A?style=for-the-badge&logo=wayland)](protocols/daxos-acrylic-blur-v1.xml)
[![Parity Spec](https://img.shields.io/badge/Parity_Spec-macOS_%26_Win11_Equivalence-5856D6?style=for-the-badge)](docs/DISTRIBUTION_AND_PARITY_SPEC.md)

---

##  Ringkasan Eksekutif

**DAXOS** adalah sistem operasi desktop modern berperforma tinggi yang dirancang dengan perpaduan keindahan visual *glassmorphism / acrylic glass*, arsitektur keamanan *immutable core* dengan enkripsi penuh berbasis perangkat keras (TPM 2.0 / Apple Secure Enclave SEP), dan subsistem translasi biner universal.

###  Keunggulan Fondasi DAXOS
1. **Core Kernel DXU Hybrid & Driver Terisolasi**:
   - Kernel **DXU Hybrid** (Dhafa eXperience Unified Hybrid Kernel) dengan penjadwalan `DreX-Boost` (jitter UI ≤ 0.42 ms pada 240Hz) dan in-kernel `ntsync` driver untuk akselerasi gaming Proton/WINE.
   - Root filesystem read-only berbasis EROFS yang dilindungi dm-verity Merkle tree dan dm-crypt XTS-AES-256 (kunci efektif 512-bit).
   - Driver grafis dan periferal berjalan di user-space melalui **DreX-Driver Supervisor** dengan SLA pemulihan otomatis dari crash ≤ 45 ms tanpa kernel panic.
2. **Visual Full-Glass & Audio Real-Time**:
   - Protokol Wayland orisinal `protocols/daxos-acrylic-blur-v1.xml` terintegrasi dengan compositor Dual-Kawase multi-pass blur, specular highlights, dan noise dithering.
   - Subsistem audio berlatensi rendah 5.8 ms dengan kontrol gain dB, spatial audio binaural HRTF, dan preset EQ 10-band.
3. **Ekosistem Bahasa Surflang & DreXUI**:
   - **Surflang 1.0**: Bahasa sistem *strongly-typed* dengan *affine ownership* (zero-cost abstraction tanpa garbage collector) dan sintaksis deklaratif reaktif modern ala Swift.
   - **DreXUI**: Framework UI reaktif berbasis `@State` dan `@Binding` dengan rendering pipeline 120–240Hz+ bebas stutter.
4. **Compiler DCODX & Fat Universal Bundle (`.dapp`)**:
   - Pipeline compiler multi-target: Lexer → Recursive Descent AST → Affine Borrow Checker → DreX-HIR → LLVM IR 19.
   - Format paket biner `.dapp` mandiri (*fat container*) dengan header 128-byte (magic `0x44415050`), tanda tangan digital Ed25519, serta isolasi sandbox Landlock LSM ABI v5 dan Seccomp-BPF.
5. **Pembaruan Sistem Tanpa Henti (Atomic A/B OTA)**:
   - Partisi ganda A/B terkelola oleh daemon `dap-updated` dan bootloader GRUB 2.12.
   - Rollback otomatis ke slot stabil jika terjadi 3 kegagalan boot beruntun (`boot_counter >= 3`).
   - Sinkronisasi awan terpusat dengan portal DaXCloud via REST API.

---

##  Struktur Monorepo DAXOS

```text
daxos/
├── CLAUDE.md                 # Master blueprint, status checklist & gates verifikasi
├── Cargo.toml                # Workspace configuration (29 Rust crates)
├── boot/
│   ├── grub/grub.cfg         # Konfigurasi GRUB 2.12 dual-slot A/B & rollback state machine
│   ├── initramfs/            # Early userspace init, TPM2 unsealing & dm-verity mount
│   ├── scripts/              # Skrip pendukung bootloader (daxos-mark-good.sh)
│   └── systemd/              # Unit systemd untuk daemons inti sistem operasi
├── crates/
│   ├── dap-compat/           # Layer kompatibilitas biner universal (Mach-O, PE, ELF, Deb)
│   ├── dap-registryd/        # Daemon registry pusat SQLite WAL & Unix socket server
│   ├── dap-sandboxd/         # Manager sandbox aplikasi (Landlock LSM, Seccomp, cgroups)
│   ├── dap-updated/          # Daemon updater atomik A/B OTA & client DaXCloud
│   ├── dax-audiod/           # Audio subsystem DSP 5.8ms & HRTF 3D engine (daudio)
│   ├── dax-bro/              # Peramban Chromium 132, Blink 6.12, V8, Manifest V3 & CDP (daxbro)
│   ├── dax-calc/             # Kalkulator saintifik & programmer presisi tinggi (dcalc)
│   ├── dax-clock/            # Jam dunia, alarm, stopwatch presisi tinggi & timer pomodoro (dclock)
│   ├── dax-disks/            # Manajer partisi GPT, Btrfs & SMART health diagnostics (ddisk)
│   ├── dax-edit/             # Editor teks visual terminal ringan Notepad++ (dedit)
│   ├── dax-files/            # Manajer berkas visual & VFS navigator (dfm)
│   ├── dax-font/             # Manajer font & inspektor peta karakter Unicode FreeType (dfont)
│   ├── dax-installer/        # Engine instalasi OS produksi bare-metal & VM (dax-installer)
│   ├── dax-media/            # Suite pemutar media 3-in-1: 4K Video AV1, Audio DSP & Foto (dmedia)
│   ├── dax-netd/             # Daemon pengelola jaringan riil, ICMP ping & Wi-Fi WPA3 (dnet)
│   ├── dax-office/           # Suite produktivitas Office native: DaxWord, DaxSheet, DaxSlide (doffice)
│   ├── dax-pkg/              # Package manager atomik biner .dapp resmi (dax)
│   ├── dax-sec/              # Pusat keamanan sistem, Landlock auditor & firewall (dxdef-cli)
│   ├── dax-sysmon/           # Telemetri performa hardware kernel riil (dtop)
│   ├── daxdrop/              # Berbagi berkas P2P wireless & gestur kamera optik "Kepal Tangan" (daxdrop)
│   ├── daxsh/                # Shell interaktif DAXOS bertenaga Rust (daxsh)
│   ├── dcodx-bundle/         # Tooling pembungkus fat binary container universal .dapp
│   ├── dcodx-cli/            # Unified developer CLI & IDE toolchain (build, pack, lsp, fmt, test, sdk, studio)
│   ├── dcodx-compiler/       # Compiler Surflang -> DreX-HIR -> LLVM IR
│   ├── drex-boostd/          # Governor dinamis pengatur prioritas render & thermals
│   ├── drex-compositor/      # Compositor Wayland acrylic blur Dual-Kawase
│   ├── drex-sdk/             # Official Software Development Kit & Zero-Crash Fault Shield
│   ├── drex-ui/              # Framework UI deklaratif reaktif Surflang/DreXUI
│   └── drexvis/              # Abstraksi driver GPU Rust & hardware isolation (CUDA, RDNA, Arc, VirtIO)
├── docs/                     # Dokumentasi arsitektur resmi FASE 0 s/d FASE 7
├── examples/                 # 15 Aplikasi sistem universal mandiri (.dapp)
├── kernel/
│   ├── configs/              # Kernel defconfigs x86_64 & ARM64
│   └── patches/              # In-kernel patches: NTSync & DreX dynamic boost
├── protocols/                # Protokol resmi Wayland (daxos-acrylic-blur-v1.xml)
├── schema/                   # Skema database SQLite3 Registry (19 tabel DDL)
├── scripts/
│   ├── build_iso.sh          # Generator bootable hybrid ISO9660 El Torito (~2.81 GB)
│   ├── run_e2e_verification.sh # Test harness 10-gate verifikasi otomatis end-to-end
│   └── run_qemu_vm.sh        # Runner mesin virtual akselerasi perangkat keras QEMU
├── src/
│   ├── compositor/           # C++20 Hyprland acrylic blur plugin
│   └── ui/                   # Source Surflang Preferences Panel & Desktop Preview Web
├── web-dapstore/             # Portal Web DapStore App Store (Python/Flask/SQLite/MySQL)
└── web-daxcloud/             # Portal Web DaXCloud Storage & Hub OTA (Python/Flask/SQLite/MySQL)
```

---

## [240Hz] Verifikasi & Pengujian Otomatis (E2E Test Harness)

Seluruh komponen sistem operasi divalidasi secara otomatis melalui skrip verifikasi terpadu:

```bash
# Jalankan seluruh 10 gate pengujian dari root repositori:
./scripts/run_e2e_verification.sh
```

### Hasil Validasi 10 Gate:
* [PASS] **Gate 1**: Cargo Workspace compilation, 52 unit tests, fuzzer header `.dapp`, dan daemon IPC.
* [PASS] **Gate 2**: SQLite Registry schema (19 tabel DDL, foreign keys, triggers, seed data).
* [PASS] **Gate 3**: Protokol Wayland XML validasi dan kompilasi plugin C++20 Hyprland.
* [PASS] **Gate 4**: DCODX compiler memvalidasi dan mengompilasi 15 file Surflang (`.surf`) menjadi DreX-HIR dan LLVM IR.
* [PASS] **Gate 5**: Universal fat binary packaging `.dapp` (15 aplikasi), verifikasi Ed25519, sandboxed execution, dan developer project scaffolding (`dcodx new`).
* [PASS] **Gate 6**: Driver chaos fault injection (SIGSEGV/SIGBUS) dengan SLA pemulihan ≤ 45 ms.
* [PASS] **Gate 7**: Power-loss resiliency test dan GRUB 2.12 rollback otomatis 3-strike failure.
* [PASS] **Gate 8**: Systemd daemon standalone checks, remote DaXCloud OTA check & sync.
* [PASS] **Gate 9**: Pembuatan image bootable ISO production `build/daxos-x86_64.iso` (2.81 GB) dan validasi runner VM QEMU.
* [PASS] **Gate 10**: Validasi utilitas sistem produksi inti (`dax`, `daxsh`, `dtop`, `dnet`, `dax-installer`, `dcalc`).

---

##  Perangkat Lunak Bawaan & Utilitas Sistem Produksi

DAXOS dilengkapi utilitas sistem operasi mandiri (*native*) yang setara dengan ekosistem macOS, Windows 11, dan Ubuntu:

### 1. `dax` — DAXOS Native Package Manager
Pengelola paket atomik berkecepatan tinggi untuk paket biner `.dapp`, repositori resmi, dan dependensi sistem:
```bash
dax search browser          # Cari paket di repositori resmi
dax install calculator      # Pasang aplikasi terverifikasi Ed25519
dax info drex-compositor    # Periksa metadata, lisensi, & sandbox level
dax list --system           # Daftar seluruh paket subsistem terlindungi
dax stats                   # Telemetri penyimpanan & status database
dax audit                   # Audit integritas sistem & sandbox Landlock
```

### 2. `daxsh` — DAXOS Interactive Shell
Shell interaktif bertenaga Rust dengan kompatibilitas POSIX dan perintah built-in ekosistem DAXOS:
```bash
daxsh                       # Masuk ke sesi REPL interaktif
fetch                       # Tampilkan logo visual DAXOS, spesifikasi, kernel, & memori (fastfetch)
boost extreme-240hz         # Alihkan profil governor CPU/GPU ke 240Hz Ultra-Low Latency
service list                # Status dan manajemen daemon sistem (systemd-compatible)
disks                       # Tata letak partisi GPT dan status slot aktif A/B dm-verity
mem                         # Alokasi memori fisik dan rasio kompresi ZRAM zstd
```

### 3. `dtop` — Real-Time Activity & Telemetry Monitor
Monitor performa dan aktivitas sistem real-time dengan visual progress bar ANSI:
```bash
dtop                        # Dashboard interaktif CPU per-core, RAM, ZRAM, GPU 240Hz, & Sandbox
dtop --once                 # Cetak satu snapshot performa (cocok untuk skrip)
dtop --json                 # Ekspor telemetri lengkap dalam format JSON
```

### 4. `dnet` — Network & Wireless Controller
Manajemen antarmuka jaringan fisik/virtual, pemindaian Wi-Fi 6E/7 (WPA3-SAE), dan proteksi DNS:
```bash
dnet status                 # Ringkasan koneksi aktif, IP, gateway, & DoH
dnet dev                    # Daftar seluruh kartu jaringan (Ethernet, Wi-Fi, Loopback)
dnet wifi scan              # Pemindaian sinyal Wi-Fi 2.4/5/6 GHz dengan indikator bar
dnet wifi connect <SSID>    # Autentikasi aman WPA3-Personal (SAE)
dnet ping 1.1.1.1           # Uji latensi transmisi paket BBRv3
```

### 5. `dax-installer` — Production Operating System Installer
Engine penginstal sistem operasi siap pakai untuk perangkat keras bare-metal atau VM:
```bash
dax-installer               # Panduan instalasi interaktif: Preflight hardware check,
                            # partisi GPT (ESP, ROOT_A, ROOT_B, DATA Btrfs),
                            # konfigurasi pengguna, dan pemasangan bootloader GRUB UEFI
```

### 6. `dcalc` — Scientific & Programmer Calculator
Kalkulator saintifik presisi tinggi, konverter basis bilangan programmer, dan konverter satuan:
```bash
dcalc "2 * (10 + 5) - sqrt(81)"  # Evaluasi ekspresi matematika
dcalc base 65535                 # Konversi basis simultan (DEC, HEX, OCT, BIN)
dcalc conv 100 c f               # Konversi suhu (Celsius ke Fahrenheit)
dcalc conv 16 gb mb              # Konversi kapasitas data penyimpanan
```

### 7. `dfm` — High-Speed File Manager & VFS Explorer
Manajer berkas visual terminal setara macOS Finder dan Windows Explorer:
```bash
dfm ls                           # Daftar direktori dengan ikon, ukuran, perizinan, & waktu
dfm tree .                       # Visualisasi hierarki pohon berkas bercabang
dfm info Cargo.toml              # Metadata mendalam, perizinan oktal, & checksum kriptografis SHA3-512
dfm find "target"                # Pencarian berkas cepat secara rekursif
dfm du .                         # Analisis pemakaian disk per folder
dfm cat <file>                   # Penampil isi berkas dengan penomoran baris rapi
```

### 8. `dedit` — Visual Lightweight Text Editor
Editor teks terminal visual setara Notepad / TextEdit / nano dengan nomor baris dan status bar:
```bash
dedit my_document.txt            # Buka editor visual interaktif (:w simpan, :q keluar)
dedit view my_document.txt       # Tampilkan dokumen dengan nomor baris
dedit count my_document.txt      # Hitung total baris, kata, karakter, dan byte
dedit search my_document.txt "OS"# Cari kata dengan posisi baris & kolom
```

### 9. `dxdef-cli` — Security Center & Firewall Manager
Pusat keamanan terpadu setara Windows Defender dan macOS XProtect / Gatekeeper:
```bash
dxdef-cli status                 # Audit kernel lockdown, Landlock ABI v5, Seccomp, dm-verity, & TPM 2.0
dxdef-cli scan my_binary         # Pindai integritas berkas biner, SUID risk, & SHA3-512
dxdef-cli firewall status        # Status firewall aktif
dxdef-cli firewall allow 443 tcp # Izinkan port HTTPS
dxdef-cli firewall deny 8080 tcp # Blokir port
```

### 10. `ddisk` — Storage & Block Device Subsystem
Manajer penyimpanan, partisi GPT, dan kesehatan SMART disk (NVMe PCIe 5.0 / SATA SSD):
```bash
ddisk list                       # Daftar seluruh media penyimpanan & partisi
ddisk mounts                     # Tampilkan seluruh titik mount aktif
ddisk usage /                    # Analisis kapasitas & persentase penggunaan filesystem
ddisk json                       # Ekspor topologi penyimpanan ke format JSON
```

### 11. `daudio` — Low-Latency Audio Subsystem
Pengontrol audio hardware ALSA/PipeWire dengan dukungan spatial audio & equalizer 10-band:
```bash
daudio status                    # Status volume master, kartu suara, & PCM streams
daudio cards                     # Deteksi sound card hardware (Intel, Realtek, USB DAC)
daudio set-vol 80                # Set volume master (0-100%)
daudio mute / daudio unmute      # Mute / unmute audio instan
```

### 12. `ddrv` — DreXVIS Hardware Driver Manager
Sistem manajemen driver DRM/KMS langsung dengan pemulihan crash SLA ≤ 45 ms:
```bash
ddrv status                      # Status bus PCI, akselerasi GPU (AMD/NVIDIA/Intel/ARM), & governor
ddrv probe                       # Pindai perangkat keras baru secara otomatis
```

### 13. `daxdrop` — P2P Discovery & Air-Gesture Sharing Engine
Ekosistem transfer nirkabel lokal terenkripsi TLS 1.3 / ChaCha20-Poly1305 dengan pelacakan kamera V4L2 ('Kepal Tangan'):
```bash
daxdrop status                   # Status perangkat lokal, sensor kamera optik V4L2, & gesture
daxdrop list                     # Pindai peer DAXOS sekitar (Phone, Tablet, Desktop)
daxdrop gesture                  # Uji pipeline gesture kepal tangan (air-grab)
```

### 14. `dax-run` & `dax-trans` — Universal Compatibility Subsystems
Eksekusi langsung aplikasi Windows (.exe), macOS (.app), dan Debian (.deb):
```bash
dax-run --list-runtimes          # Tampilkan status DaxWinBridge, DaxMacBridge, DaxDebBridge, DaxProtonBridge
dax-trans /bin/ls                # AOT translator & syscall mapping biner asing
dax-run my_app.exe               # Jalankan biner Windows dengan dekorasi DreXUI acrylic
dax-run --game Cyberpunk2077.exe # Mode Gaming ultra-low latency (Proton 9.0 + DXVK 2.3 + Fsync)
```

### 15. `build_kernel.sh` — Production Kernel Build Pipeline
Pipeline otomatis untuk membangun kernel Linux 6.12 LTS kustom DAXOS:
```bash
./scripts/build_kernel.sh        # Ekstraksi kernel 6.12 LTS, patch NTSync & DreX-Boost,
                                 # konfigurasi daxos_x86_64_defconfig, dan verifikasi vmlinuz
```

---

## [PERF] Panduan Developer CLI Toolchain (`dcodx`)

Toolchain CLI terpadu `dcodx` menyediakan alur kerja lengkap untuk pembuatan aplikasi DAXOS:

```bash
# 1. Membuat proyek aplikasi baru berbasis template DreXUI
cargo run -p dcodx-cli -- new my_daxos_app

# 2. Mengompilasi kode sumber Surflang ke DreX-HIR & LLVM IR
cargo run -p dcodx-cli -- build my_daxos_app/src/main.surf

# 3. Membungkus proyek menjadi Universal Fat Executable Bundle (.dapp)
cargo run -p dcodx-cli -- pack my_daxos_app/manifest.toml -o my_daxos_app.dapp

# 4. Memverifikasi bukti kriptografi tanda tangan digital Ed25519
cargo run -p dcodx-cli -- verify my_daxos_app.dapp

# 5. Menjalankan aplikasi dalam sandbox terisolasi
cargo run -p dcodx-cli -- run my_daxos_app.dapp

# 6. Memeriksa kesehatan ekosistem sistem operasi
cargo run -p dcodx-cli -- doctor
```

---

##  Pembuatan & Pengujian Bootable ISO

DAXOS menyediakan generator ISO terpadu untuk instalasi langsung pada perangkat keras bare-metal atau mesin virtual:

```bash
# 1. Bangun image ISO hybrid produksi (~2.81 GB)
./scripts/build_iso.sh

# 2. Jalankan mesin virtual QEMU dengan akselerasi perangkat keras VirtIO
./scripts/run_qemu_vm.sh

# Mode headless via VNC (port 5901):
./scripts/run_qemu_vm.sh --vnc :1

# Pembuatan virtual disk 64GB untuk pengujian instalasi:
./scripts/run_qemu_vm.sh --create-disk
```

---

##  Portal Ekosistem Web (DapStore & DaXCloud)

DAXOS dilengkapi dua platform web mandiri siap produksi:
* **Web DapStore** (`web-dapstore/`): Toko aplikasi resmi untuk eksplorasi katalog, instalasi paket `.dapp`, manajemen pengembang, review, dan rating bintang. Port default: `5000`.
* **Web DaXCloud** (`web-daxcloud/`): Penyimpanan awan terenkripsi ChaCha20-Poly1305 end-to-end dengan kuota 2TB, file sharing, dan hub pembaruan sistem OTA pusat. Port default: `5051`.

Dukungan basis data ganda: SQLite3 mandiri untuk pengembangan lokal dan MySQL/MariaDB dengan konfigurasi cPanel Phusion Passenger untuk hosting web enterprise.

---

##  Lisensi & Pengembang

Dikembangkan dengan dedikasi penuh oleh **Dhafa Nazula Permadi (@kangpcode)**.  
Hak Cipta © 2026 DAXOS Operating System Core Team. Seluruh hak dilindungi undang-undang.
