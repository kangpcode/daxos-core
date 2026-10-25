-- ============================================================================
-- DAXOS REGISTRY DATABASE DDL (SQLite 3.37+ WAL MODE COMPATIBLE)
-- File: /var/lib/daxos/registry.db
-- Purpose: Central System Registry, Hardware, Security, OTA & DapStore Schema
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- DOMAIN 1: STATUS OPERASIONAL SISTEM & KONFIGURASI INTI
-- ----------------------------------------------------------------------------

CREATE TABLE system_nodes (
    node_id TEXT PRIMARY KEY,
    hostname TEXT NOT NULL,
    architecture TEXT NOT NULL CHECK(architecture IN ('x86_64', 'arm64')),
    kernel_release TEXT NOT NULL,
    tpm_version TEXT NOT NULL DEFAULT '2.0',
    secure_boot_enabled INTEGER NOT NULL CHECK(secure_boot_enabled IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE system_configurations (
    config_key TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    config_value TEXT NOT NULL,
    data_type TEXT NOT NULL CHECK(data_type IN ('string', 'integer', 'float', 'boolean', 'json')),
    is_readonly INTEGER NOT NULL DEFAULT 0 CHECK(is_readonly IN (0, 1)),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (node_id) REFERENCES system_nodes(node_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_sys_config_node ON system_configurations(node_id);

-- ----------------------------------------------------------------------------
-- DOMAIN 2: SKEMA PARTISI BOOTLOADER GRUB (SLOT A/B)
-- ----------------------------------------------------------------------------

CREATE TABLE bootloader_slots (
    slot_id TEXT PRIMARY KEY CHECK(slot_id IN ('A', 'B')),
    node_id TEXT NOT NULL,
    partition_label TEXT NOT NULL UNIQUE,
    dm_verity_roothash TEXT NOT NULL,
    boot_counter INTEGER NOT NULL DEFAULT 0 CHECK(boot_counter >= 0 AND boot_counter <= 3),
    is_active INTEGER NOT NULL DEFAULT 0 CHECK(is_active IN (0, 1)),
    is_successful INTEGER NOT NULL DEFAULT 0 CHECK(is_successful IN (0, 1)),
    last_boot_timestamp TEXT,
    FOREIGN KEY (node_id) REFERENCES system_nodes(node_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_boot_slots_node ON bootloader_slots(node_id);

-- Trigger: Hanya satu slot yang boleh aktif (is_active = 1) per node
CREATE TRIGGER trg_single_active_slot_before_insert
BEFORE INSERT ON bootloader_slots
FOR EACH ROW
WHEN NEW.is_active = 1
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM bootloader_slots WHERE node_id = NEW.node_id AND is_active = 1) >= 1
        THEN RAISE(ABORT, 'Integritas Gagal: Hanya satu slot bootloader yang diizinkan aktif per perangkat.')
    END;
END;

CREATE TRIGGER trg_single_active_slot_before_update
BEFORE UPDATE OF is_active ON bootloader_slots
FOR EACH ROW
WHEN NEW.is_active = 1
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM bootloader_slots WHERE node_id = NEW.node_id AND is_active = 1 AND slot_id != NEW.slot_id) >= 1
        THEN RAISE(ABORT, 'Integritas Gagal: Hanya satu slot bootloader yang diizinkan aktif per perangkat.')
    END;
END;

-- ----------------------------------------------------------------------------
-- DOMAIN 3: MANAJEMEN OTA (OVER-THE-AIR ATOMIC UPDATES)
-- ----------------------------------------------------------------------------

CREATE TABLE ota_channels (
    channel_id TEXT PRIMARY KEY CHECK(channel_id IN ('stable', 'beta', 'nightly', 'canary')),
    description TEXT NOT NULL,
    check_interval_seconds INTEGER NOT NULL DEFAULT 3600 CHECK(check_interval_seconds >= 60)
);

CREATE TABLE ota_releases (
    release_id TEXT PRIMARY KEY,
    channel_id TEXT NOT NULL,
    version_semver TEXT NOT NULL UNIQUE,
    build_epoch INTEGER NOT NULL CHECK(build_epoch > 0),
    target_architecture TEXT NOT NULL CHECK(target_architecture IN ('x86_64', 'arm64')),
    image_type TEXT NOT NULL CHECK(image_type IN ('full', 'delta')),
    image_size_bytes INTEGER NOT NULL CHECK(image_size_bytes > 0),
    sha3_512_hash TEXT NOT NULL,
    ed25519_signature TEXT NOT NULL,
    changelog_json TEXT NOT NULL,
    published_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (channel_id) REFERENCES ota_channels(channel_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_ota_releases_chan_ver ON ota_releases(channel_id, build_epoch DESC);

CREATE TABLE ota_update_jobs (
    job_id TEXT PRIMARY KEY,
    release_id TEXT NOT NULL,
    target_slot TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending', 'downloading', 'verifying', 'staged', 'applied', 'failed', 'rolled_back')),
    download_progress_percent REAL NOT NULL DEFAULT 0.0 CHECK(download_progress_percent >= 0.0 AND download_progress_percent <= 100.0),
    bytes_downloaded INTEGER NOT NULL DEFAULT 0 CHECK(bytes_downloaded >= 0),
    error_message TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    completed_at TEXT,
    FOREIGN KEY (release_id) REFERENCES ota_releases(release_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (target_slot) REFERENCES bootloader_slots(slot_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_ota_jobs_status ON ota_update_jobs(status);

CREATE TABLE ota_rollback_logs (
    log_id TEXT PRIMARY KEY,
    job_id TEXT,
    failed_slot TEXT NOT NULL,
    fallback_slot TEXT NOT NULL,
    failure_reason TEXT NOT NULL,
    boot_attempts INTEGER NOT NULL CHECK(boot_attempts > 0),
    occurred_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (job_id) REFERENCES ota_update_jobs(job_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (failed_slot) REFERENCES bootloader_slots(slot_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (fallback_slot) REFERENCES bootloader_slots(slot_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_ota_rollback_occurred ON ota_rollback_logs(occurred_at DESC);

-- ----------------------------------------------------------------------------
-- DOMAIN 4: DEVELOPER & PUBLIKASI DAPSTORE
-- ----------------------------------------------------------------------------

CREATE TABLE developers (
    developer_id TEXT PRIMARY KEY,
    legal_name TEXT NOT NULL,
    contact_email TEXT NOT NULL UNIQUE,
    ed25519_public_key TEXT NOT NULL UNIQUE,
    reputation_score REAL NOT NULL DEFAULT 100.0 CHECK(reputation_score >= 0.0 AND reputation_score <= 100.0),
    is_revoked INTEGER NOT NULL DEFAULT 0 CHECK(is_revoked IN (0, 1)),
    registered_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE developer_certificates (
    certificate_id TEXT PRIMARY KEY,
    developer_id TEXT NOT NULL,
    fingerprint_sha256 TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK(status IN ('active', 'revoked', 'expired')),
    issued_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    FOREIGN KEY (developer_id) REFERENCES developers(developer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_dev_certs_dev ON developer_certificates(developer_id, status);

CREATE TABLE applications (
    app_id TEXT PRIMARY KEY,
    developer_id TEXT NOT NULL,
    bundle_identifier TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('productivity', 'developer', 'graphics', 'games', 'system', 'utilities')),
    is_sandboxed INTEGER NOT NULL DEFAULT 1 CHECK(is_sandboxed IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (developer_id) REFERENCES developers(developer_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_apps_bundle ON applications(bundle_identifier);

CREATE TABLE application_versions (
    version_id TEXT PRIMARY KEY,
    app_id TEXT NOT NULL,
    version_number TEXT NOT NULL,
    build_number INTEGER NOT NULL CHECK(build_number > 0),
    min_daxos_version TEXT NOT NULL,
    package_sha3_512 TEXT NOT NULL,
    signature_ed25519 TEXT NOT NULL,
    download_count INTEGER NOT NULL DEFAULT 0 CHECK(download_count >= 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
    released_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE(app_id, version_number),
    FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_app_ver_active ON application_versions(app_id, is_active);

CREATE TABLE application_reviews (
    review_id TEXT PRIMARY KEY,
    app_id TEXT NOT NULL,
    user_identifier TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    review_text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE(app_id, user_identifier),
    FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_reviews_app ON application_reviews(app_id);

-- ----------------------------------------------------------------------------
-- DOMAIN 5: PEMETAAN IZIN SANDBOX .DAPP & AUDIT KEAMANAN
-- ----------------------------------------------------------------------------

CREATE TABLE sandbox_permissions (
    permission_id TEXT PRIMARY KEY,
    permission_code TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK(category IN ('hardware', 'network', 'filesystem', 'ipc', 'display')),
    risk_level TEXT NOT NULL CHECK(risk_level IN ('low', 'medium', 'high', 'critical')),
    description TEXT NOT NULL
);

CREATE TABLE sandbox_grants (
    grant_id TEXT PRIMARY KEY,
    app_id TEXT NOT NULL,
    permission_id TEXT NOT NULL,
    grant_status TEXT NOT NULL CHECK(grant_status IN ('granted', 'denied', 'prompt_on_use')),
    granted_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    expires_at TEXT,
    UNIQUE(app_id, permission_id),
    FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES sandbox_permissions(permission_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_sandbox_grants_lookup ON sandbox_grants(app_id, grant_status);

CREATE TABLE sandbox_audit_logs (
    audit_id TEXT PRIMARY KEY,
    app_id TEXT NOT NULL,
    permission_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('access_allowed', 'access_denied', 'violation_trapped')),
    resource_target TEXT NOT NULL,
    logged_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES sandbox_permissions(permission_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_sandbox_audit_app_action ON sandbox_audit_logs(app_id, action, logged_at DESC);

-- ----------------------------------------------------------------------------
-- DOMAIN 6: PROFIL VISUAL GLASS PER USER
-- ----------------------------------------------------------------------------

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE visual_glass_profiles (
    profile_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    profile_name TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 0 CHECK(is_active IN (0, 1)),
    opacity REAL NOT NULL CHECK(opacity >= 0.05 AND opacity <= 1.00),
    blur_radius_px INTEGER NOT NULL CHECK(blur_radius_px >= 0 AND blur_radius_px <= 128),
    edge_brightness REAL NOT NULL CHECK(edge_brightness >= 0.00 AND edge_brightness <= 2.00),
    noise_intensity REAL NOT NULL CHECK(noise_intensity >= 0.00 AND noise_intensity <= 1.00),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE(user_id, profile_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_glass_user_active ON visual_glass_profiles(user_id, is_active);

-- Trigger: Hanya satu profil visual glass yang boleh aktif per user
CREATE TRIGGER trg_single_active_glass_profile_update
BEFORE UPDATE OF is_active ON visual_glass_profiles
FOR EACH ROW
WHEN NEW.is_active = 1
BEGIN
    UPDATE visual_glass_profiles
    SET is_active = 0
    WHERE user_id = NEW.user_id AND profile_id != NEW.profile_id;
END;

-- ----------------------------------------------------------------------------
-- DOMAIN 7: PROFIL AUDIO HARDWARE & PRESET
-- ----------------------------------------------------------------------------

CREATE TABLE audio_devices (
    device_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    device_name TEXT NOT NULL,
    alsa_card_index INTEGER NOT NULL,
    sample_rate_hz INTEGER NOT NULL DEFAULT 48000 CHECK(sample_rate_hz IN (44100, 48000, 96000, 192000)),
    buffer_size_frames INTEGER NOT NULL DEFAULT 64 CHECK(buffer_size_frames IN (32, 64, 128, 256, 512)),
    is_default INTEGER NOT NULL DEFAULT 0 CHECK(is_default IN (0, 1)),
    FOREIGN KEY (node_id) REFERENCES system_nodes(node_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE audio_eq_presets (
    preset_id TEXT PRIMARY KEY,
    preset_name TEXT NOT NULL UNIQUE,
    preamp_gain_db REAL NOT NULL DEFAULT 0.0 CHECK(preamp_gain_db >= -24.0 AND preamp_gain_db <= 12.0),
    bands_json TEXT NOT NULL
);

CREATE TABLE audio_user_profiles (
    profile_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    preset_id TEXT NOT NULL,
    master_gain_db REAL NOT NULL DEFAULT 0.0 CHECK(master_gain_db >= -96.0 AND master_gain_db <= 6.0),
    spatial_audio_enabled INTEGER NOT NULL DEFAULT 0 CHECK(spatial_audio_enabled IN (0, 1)),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE(user_id, device_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (device_id) REFERENCES audio_devices(device_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (preset_id) REFERENCES audio_eq_presets(preset_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_audio_user_profile ON audio_user_profiles(user_id, device_id);

-- ----------------------------------------------------------------------------
-- DOMAIN 8: STATUS & RIWAYAT PEMULIHAN DREX-DRIVER
-- ----------------------------------------------------------------------------

CREATE TABLE drivers (
    driver_id TEXT PRIMARY KEY,
    driver_name TEXT NOT NULL UNIQUE,
    driver_type TEXT NOT NULL CHECK(driver_type IN ('gpu', 'audio', 'network', 'input')),
    binary_path TEXT NOT NULL,
    max_restart_retries INTEGER NOT NULL DEFAULT 3 CHECK(max_restart_retries > 0),
    restart_cooldown_seconds INTEGER NOT NULL DEFAULT 30 CHECK(restart_cooldown_seconds > 0)
);

CREATE TABLE driver_status (
    driver_id TEXT PRIMARY KEY,
    current_state TEXT NOT NULL CHECK(current_state IN ('active', 'degraded', 'quarantined', 'stopped')),
    current_pid INTEGER,
    crash_count_window INTEGER NOT NULL DEFAULT 0 CHECK(crash_count_window >= 0),
    last_crash_timestamp TEXT,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE driver_recovery_logs (
    log_id TEXT PRIMARY KEY,
    driver_id TEXT NOT NULL,
    exit_signal INTEGER NOT NULL,
    recovery_duration_ms INTEGER NOT NULL CHECK(recovery_duration_ms >= 0),
    recovery_status TEXT NOT NULL CHECK(recovery_status IN ('recovered', 'quarantined', 'fallback_invoked')),
    fallback_driver_id TEXT,
    incident_timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (fallback_driver_id) REFERENCES drivers(driver_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE INDEX idx_driver_rec_time ON driver_recovery_logs(driver_id, incident_timestamp DESC);

-- ============================================================================
-- SEED DATA MINIMAL KONKRET
-- ============================================================================

INSERT INTO system_nodes (node_id, hostname, architecture, kernel_release, tpm_version, secure_boot_enabled)
VALUES ('node-local-01', 'daxos-station', 'x86_64', '6.12.4-daxos-hybrid', '2.0', 1);

INSERT INTO system_configurations (config_key, node_id, config_value, data_type, is_readonly)
VALUES 
    ('kernel.hybrid_scheduler.timeslice_us', 'node-local-01', '750', 'integer', 1),
    ('compositor.target_framerate', 'node-local-01', '120', 'integer', 0),
    ('drex_boost.governor_enabled', 'node-local-01', 'true', 'boolean', 0);

INSERT INTO bootloader_slots (slot_id, node_id, partition_label, dm_verity_roothash, boot_counter, is_active, is_successful, last_boot_timestamp)
VALUES 
    ('A', 'node-local-01', 'DAXOS_ROOT_A', 'b3f5c719e83610928a41753cfa9e39b207a618d3b854ec7a6f2098d89a42be7c', 0, 1, 1, '2026-10-15T06:00:00.000Z'),
    ('B', 'node-local-01', 'DAXOS_ROOT_B', 'e1c8491035acdb8271fe5923ba61c2847d0e1948ba265a7f9c31405e6b72a9df', 0, 0, 1, '2026-10-10T12:00:00.000Z');

INSERT INTO ota_channels (channel_id, description, check_interval_seconds)
VALUES 
    ('stable', 'Kanal rilis teruji penuh untuk produktivitas enterprise.', 86400),
    ('beta', 'Kanal pratinjau fitur baru dengan validasi regression testing.', 21600),
    ('nightly', 'Kanal pengembangan otomatis build harian.', 3600),
    ('canary', 'Kanal bleeding-edge kompilasi commit langsung.', 1800);

INSERT INTO ota_releases (release_id, channel_id, version_semver, build_epoch, target_architecture, image_type, image_size_bytes, sha3_512_hash, ed25519_signature, changelog_json)
VALUES (
    'rel-daxos-1.2.0',
    'stable',
    '1.2.0',
    1776200000,
    'x86_64',
    'delta',
    419430400,
    'a7f8e3b29c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b',
    'ed25519_sig_f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1',
    '{"features":["DreXVIS RDNA4 RayTracing Support","Acrylic Blur 240Hz Optimization"],"fixes":["Fix audio buffer underrun in PipeWire ALSA Direct"]}'
);

INSERT INTO developers (developer_id, legal_name, contact_email, ed25519_public_key, reputation_score)
VALUES ('dev-daxos-core', 'DAXOS Core Engineering Group', 'security@daxos.org', 'ed25519_pub_4f8a92bc130987adaabbccddeeff00112233445566778899aabbccddeeff0011', 100.0);

INSERT INTO developer_certificates (certificate_id, developer_id, fingerprint_sha256, status, issued_at, expires_at)
VALUES ('cert-dev-core-01', 'dev-daxos-core', 'sha256_fp_998877aabbccddeeff00112233445566778899aabbccddeeff001122334455', 'active', '2026-01-01T00:00:00.000Z', '2028-01-01T00:00:00.000Z');

INSERT INTO applications (app_id, developer_id, bundle_identifier, display_name, category, is_sandboxed)
VALUES ('app-core-terminal', 'dev-daxos-core', 'org.daxos.terminal', 'DAXOS Accelerated Terminal', 'developer', 1);

INSERT INTO application_versions (version_id, app_id, version_number, build_number, min_daxos_version, package_sha3_512, signature_ed25519, download_count, is_active)
VALUES (
    'ver-term-1.0.4',
    'app-core-terminal',
    '1.0.4',
    104,
    '1.0.0',
    'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5',
    'ed25519_sig_term_01a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7',
    4520,
    1
);

INSERT INTO sandbox_permissions (permission_id, permission_code, category, risk_level, description)
VALUES 
    ('perm-gpu', 'daxos.permission.GPU_ACCELERATION', 'hardware', 'medium', 'Akses ke pipeline 3D DreXVIS dan hardware surface buffer.'),
    ('perm-net', 'daxos.permission.NETWORK_OUTBOUND', 'network', 'high', 'Mengizinkan koneksi soket TCP/UDP ke jaringan publik.'),
    ('perm-mic', 'daxos.permission.AUDIO_CAPTURE', 'hardware', 'high', 'Mengizinkan perekaman audio dari mikrofon perangkat.'),
    ('perm-fs-docs', 'daxos.permission.FILESYSTEM_DOCUMENTS_READWRITE', 'filesystem', 'medium', 'Akses read/write ke direktori dokumen pengguna via portal.');

INSERT INTO sandbox_grants (grant_id, app_id, permission_id, grant_status)
VALUES 
    ('grant-term-gpu', 'app-core-terminal', 'perm-gpu', 'granted'),
    ('grant-term-net', 'app-core-terminal', 'perm-net', 'granted'),
    ('grant-term-mic', 'app-core-terminal', 'perm-mic', 'denied');

INSERT INTO audio_eq_presets (preset_id, preset_name, preamp_gain_db, bands_json)
VALUES 
    ('eq-flat', 'Flat Baseline', 0.0, '{"32Hz":0.0,"64Hz":0.0,"125Hz":0.0,"250Hz":0.0,"500Hz":0.0,"1kHz":0.0,"2kHz":0.0,"4kHz":0.0,"8kHz":0.0,"16kHz":0.0}'),
    ('eq-bass', 'Bass & Low-End Boost', -2.0, '{"32Hz":5.5,"64Hz":4.0,"125Hz":2.5,"250Hz":1.0,"500Hz":0.0,"1kHz":0.0,"2kHz":0.5,"4kHz":1.0,"8kHz":2.0,"16kHz":2.5}'),
    ('eq-glass', 'DreX Cinematic Glass', -1.5, '{"32Hz":2.0,"64Hz":3.0,"125Hz":1.0,"250Hz":-1.0,"500Hz":-0.5,"1kHz":1.5,"2kHz":2.5,"4kHz":3.0,"8kHz":4.0,"16kHz":4.5}');

INSERT INTO users (user_id, username, display_name)
VALUES ('user-master-01', 'daxosuser', 'DAXOS Master Operator');

INSERT INTO visual_glass_profiles (profile_id, user_id, profile_name, is_active, opacity, blur_radius_px, edge_brightness, noise_intensity)
VALUES 
    ('glass-prof-default', 'user-master-01', 'Default Acrylic Frosted', 1, 0.72, 36, 1.15, 0.04),
    ('glass-prof-vibrant', 'user-master-01', 'Vibrant Deep Glass', 0, 0.55, 48, 1.40, 0.06);

INSERT INTO audio_devices (device_id, node_id, device_name, alsa_card_index, sample_rate_hz, buffer_size_frames, is_default)
VALUES ('dev-audio-hw0', 'node-local-01', 'Realtek ALC1220 High Definition Audio', 0, 48000, 64, 1);

INSERT INTO audio_user_profiles (profile_id, user_id, device_id, preset_id, master_gain_db, spatial_audio_enabled)
VALUES ('aud-prof-default', 'user-master-01', 'dev-audio-hw0', 'eq-glass', 0.0, 1);

INSERT INTO drivers (driver_id, driver_name, driver_type, binary_path, max_restart_retries, restart_cooldown_seconds)
VALUES 
    ('drv-gpu-drexvis', 'drexvis-nvidia-bridge', 'gpu', '/usr/lib/daxos/drivers/drex-gpu-worker', 3, 30),
    ('drv-audio-pipewire', 'pipewire-dsp-worker', 'audio', '/usr/lib/daxos/drivers/drex-audio-worker', 3, 30);

INSERT INTO driver_status (driver_id, current_state, current_pid, crash_count_window, last_crash_timestamp)
VALUES 
    ('drv-gpu-drexvis', 'active', 1042, 0, NULL),
    ('drv-audio-pipewire', 'active', 1045, 0, NULL);
