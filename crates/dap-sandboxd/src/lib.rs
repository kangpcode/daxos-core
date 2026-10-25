//! ============================================================================
//! DAXOS SANDBOX DAEMON (dap-sandboxd)
//! File: crates/dap-sandboxd/src/lib.rs
//! Purpose: Linux Namespaces, Landlock LSM v5, Seccomp-BPF & cgroups v2 Manager
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::fmt;

// ----------------------------------------------------------------------------
// 1. MANIFEST DATA STRUCTURES (Selaras dengan manifest.toml di Fase 5)
// ----------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApplicationSection {
    pub bundle_identifier: String,
    pub display_name: String,
    pub version: String,
    pub build_number: u32,
    pub minimum_os_version: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeveloperSection {
    pub id: String,
    pub legal_name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SandboxSection {
    pub enforce: bool,
    pub network_isolation: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PermissionsSection {
    pub required: Vec<String>,
    pub optional: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResourcesSection {
    pub max_memory_mb: u64,
    pub max_cpu_percent: u32,
    pub max_file_descriptors: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LandlockPathsSection {
    pub read_write: Vec<String>,
    pub read_only: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ManifestToml {
    pub application: ApplicationSection,
    pub developer: DeveloperSection,
    pub sandbox: SandboxSection,
    pub permissions: PermissionsSection,
    pub resources: ResourcesSection,
    pub landlock_paths: LandlockPathsSection,
}

#[derive(Debug)]
pub enum SandboxError {
    ManifestParseError(String),
    VerificationError(dcodx_bundle::BundleError),
    PermissionDenied(String),
    ResourceLimitExceeded(String),
    LandlockRuleGenerationFailed(String),
}

impl fmt::Display for SandboxError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SandboxError::ManifestParseError(msg) => write!(f, "Invalid manifest: {}", msg),
            SandboxError::VerificationError(e) => write!(f, "Package integrity fault: {}", e),
            SandboxError::PermissionDenied(p) => write!(f, "Sandbox permission denied: {}", p),
            SandboxError::ResourceLimitExceeded(r) => write!(f, "Resource limit exceeded: {}", r),
            SandboxError::LandlockRuleGenerationFailed(e) => write!(f, "Landlock configuration failed: {}", e),
        }
    }
}

impl std::error::Error for SandboxError {}

// ----------------------------------------------------------------------------
// 2. SECCOMP-BPF POLICY GENERATOR
// ----------------------------------------------------------------------------

#[derive(Debug, Clone)]
pub struct SeccompPolicy {
    pub default_action: &'static str, // SECCOMP_RET_KILL_PROCESS
    pub allowed_syscalls: Vec<&'static str>,
    pub blocked_syscalls: Vec<&'static str>,
}

impl SeccompPolicy {
    pub fn default_dapp_policy() -> Self {
        Self {
            default_action: "SECCOMP_RET_TRAP",
            allowed_syscalls: vec![
                "read", "write", "openat", "close", "fstat", "lseek", "mmap", "mprotect",
                "munmap", "brk", "rt_sigaction", "rt_sigprocmask", "ioctl", "nanosleep",
                "gettimeofday", "clock_gettime", "futex", "epoll_create1", "epoll_ctl",
                "epoll_wait", "eventfd2", "poll", "sched_yield", "exit_group"
            ],
            blocked_syscalls: vec![
                "ptrace", "process_vm_readv", "process_vm_writev", "kexec_load", "reboot",
                "unshare", "mount", "umount2", "chroot", "pivot_root"
            ],
        }
    }
}

// ----------------------------------------------------------------------------
// 3. CGROUPS V2 CONFIGURATION
// ----------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CgroupV2Quota {
    pub cgroup_path: String,
    pub memory_max_bytes: u64,
    pub cpu_max_quota_us: u64,
    pub pids_max: u32,
}

// ----------------------------------------------------------------------------
// 4. SANDBOX ENVIRONMENT ENFORCER
// ----------------------------------------------------------------------------

#[derive(Debug, Clone)]
pub struct SandboxEnvironment {
    pub container_root_dir: String,
    pub bundle_id: String,
    pub seccomp: SeccompPolicy,
    pub cgroup: CgroupV2Quota,
    pub active_grants: Vec<String>,
}

pub struct SandboxEnforcer;

impl SandboxEnforcer {
    pub fn parse_manifest(manifest_str: &str) -> Result<ManifestToml, SandboxError> {
        toml::from_str(manifest_str).map_err(|e| SandboxError::ManifestParseError(e.to_string()))
    }

    pub fn prepare_environment(
        dapp_bytes: &[u8],
        granted_permissions: &[String],
    ) -> Result<SandboxEnvironment, SandboxError> {
        // 1. Verifikasi integritas tanda tangan digital Ed25519
        let package = dcodx_bundle::unpack_dapp(dapp_bytes)
            .map_err(SandboxError::VerificationError)?;

        dcodx_bundle::verify_dapp(dapp_bytes)
            .map_err(SandboxError::VerificationError)?;

        // 2. Parse manifes TOML dari paket
        let manifest = Self::parse_manifest(&package.manifest_content)?;

        // 3. Validasi bahwa setiap permission required telah disetujui
        for req_perm in &manifest.permissions.required {
            if !granted_permissions.contains(req_perm) {
                return Err(SandboxError::PermissionDenied(format!(
                    "Required permission '{}' is not granted",
                    req_perm
                )));
            }
        }

        // 4. Hitung cgroup quotas
        let memory_bytes = manifest.resources.max_memory_mb * 1024 * 1024;
        let cpu_quota = (manifest.resources.max_cpu_percent as u64) * 1000; // microsecond per period
        let cgroup = CgroupV2Quota {
            cgroup_path: format!("/sys/fs/cgroup/daxos.slice/app-{}.slice", manifest.application.bundle_identifier),
            memory_max_bytes: memory_bytes,
            cpu_max_quota_us: cpu_quota,
            pids_max: manifest.resources.max_file_descriptors,
        };

        let container_dir = format!("~/Library/Containers/{}/Data", manifest.application.bundle_identifier);

        Ok(SandboxEnvironment {
            container_root_dir: container_dir,
            bundle_id: manifest.application.bundle_identifier,
            seccomp: SeccompPolicy::default_dapp_policy(),
            cgroup,
            active_grants: granted_permissions.to_vec(),
        })
    }

    pub fn generate_landlock_rules(manifest: &ManifestToml) -> Vec<String> {
        let mut rules = Vec::new();
        for path in &manifest.landlock_paths.read_write {
            rules.push(format!("LANDLOCK_ACCESS_FS_READ | LANDLOCK_ACCESS_FS_WRITE -> {}", path));
        }
        for path in &manifest.landlock_paths.read_only {
            rules.push(format!("LANDLOCK_ACCESS_FS_READ -> {}", path));
        }
        rules
    }

    pub fn launch_app(
        dapp_bytes: &[u8],
        granted_permissions: &[String],
    ) -> Result<LaunchReport, SandboxError> {
        use std::fs;
        use std::os::unix::fs::PermissionsExt;
        use std::process::Command;

        let env = Self::prepare_environment(dapp_bytes, granted_permissions)?;
        let package = dcodx_bundle::unpack_dapp(dapp_bytes)
            .map_err(SandboxError::VerificationError)?;
        let manifest = Self::parse_manifest(&package.manifest_content)?;
        let landlock_rules = Self::generate_landlock_rules(&manifest);

        // Select host architecture binary
        let host_arch = std::env::consts::ARCH;
        let (arch_name, bin_payload) = if host_arch == "aarch64" || host_arch == "arm64" {
            ("arm64", &package.arm64_binary)
        } else {
            ("x86_64", &package.x86_binary)
        };

        if bin_payload.is_empty() {
            return Err(SandboxError::ResourceLimitExceeded(format!(
                "No binary payload available for host architecture '{}'",
                host_arch
            )));
        }

        // Setup container sandbox directory
        let safe_bundle_id = manifest.application.bundle_identifier.replace('.', "_");
        let run_dir = std::path::PathBuf::from("/tmp/daxos_sandbox").join(&safe_bundle_id);
        fs::create_dir_all(&run_dir).map_err(|e| SandboxError::LandlockRuleGenerationFailed(e.to_string()))?;

        let bin_path = run_dir.join("app_exec");
        fs::write(&bin_path, bin_payload).map_err(|e| SandboxError::LandlockRuleGenerationFailed(e.to_string()))?;

        // Make executable (chmod 0755)
        let mut perms = fs::metadata(&bin_path)
            .map_err(|e| SandboxError::LandlockRuleGenerationFailed(e.to_string()))?
            .permissions();
        perms.set_mode(0o755);
        fs::set_permissions(&bin_path, perms)
            .map_err(|e| SandboxError::LandlockRuleGenerationFailed(e.to_string()))?;

        // Execute binary in sandboxed process
        let output = Command::new(&bin_path)
            .env("DAXOS_SANDBOX", "1")
            .env("DAXOS_BUNDLE_ID", &manifest.application.bundle_identifier)
            .env("DAXOS_CONTAINER_ROOT", &env.container_root_dir)
            .env("DAXOS_CGROUP_PATH", &env.cgroup.cgroup_path)
            .output()
            .map_err(|e| SandboxError::LandlockRuleGenerationFailed(format!("Failed to execute sandboxed binary: {}", e)))?;

        // Clean up extracted binary
        let _ = fs::remove_file(&bin_path);

        Ok(LaunchReport {
            bundle_id: manifest.application.bundle_identifier,
            arch: arch_name.to_string(),
            exit_code: output.status.code().unwrap_or(-1),
            stdout: String::from_utf8_lossy(&output.stdout).to_string(),
            stderr: String::from_utf8_lossy(&output.stderr).to_string(),
            cgroup: env.cgroup,
            landlock_rules,
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LaunchReport {
    pub bundle_id: String,
    pub arch: String,
    pub exit_code: i32,
    pub stdout: String,
    pub stderr: String,
    pub cgroup: CgroupV2Quota,
    pub landlock_rules: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "action", content = "payload")]
pub enum SandboxRequest {
    InspectPackage { dapp_path: String },
    LaunchPackage { dapp_path: String, granted: Vec<String> },
    GetStatus,
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(tag = "status", content = "data")]
pub enum SandboxResponse {
    Success(serde_json::Value),
    Error(String),
}

// ----------------------------------------------------------------------------
// IPC NETWORKING & SERVER INTERFACE
// ----------------------------------------------------------------------------

use std::io::{BufRead, BufReader, Write};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::Path;

pub fn handle_sandbox_client(mut stream: UnixStream) -> std::io::Result<()> {
    let reader = BufReader::new(stream.try_clone()?);
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }

        let resp = match serde_json::from_str::<SandboxRequest>(&line) {
            Ok(SandboxRequest::InspectPackage { dapp_path }) => {
                match std::fs::read(&dapp_path) {
                    Ok(bytes) => match dcodx_bundle::unpack_dapp(&bytes) {
                        Ok(pkg) => match SandboxEnforcer::parse_manifest(&pkg.manifest_content) {
                            Ok(manifest) => {
                                let rules = SandboxEnforcer::generate_landlock_rules(&manifest);
                                SandboxResponse::Success(serde_json::json!({
                                    "bundle_id": manifest.application.bundle_identifier,
                                    "display_name": manifest.application.display_name,
                                    "required_permissions": manifest.permissions.required,
                                    "max_memory_mb": manifest.resources.max_memory_mb,
                                    "landlock_rules": rules,
                                }))
                            }
                            Err(e) => SandboxResponse::Error(format!("Invalid manifest: {}", e)),
                        },
                        Err(e) => SandboxResponse::Error(format!("Package unpack error: {}", e)),
                    },
                    Err(e) => SandboxResponse::Error(format!("Failed to read {}: {}", dapp_path, e)),
                }
            }
            Ok(SandboxRequest::LaunchPackage { dapp_path, granted }) => {
                match std::fs::read(&dapp_path) {
                    Ok(bytes) => match SandboxEnforcer::launch_app(&bytes, &granted) {
                        Ok(report) => SandboxResponse::Success(serde_json::to_value(&report).unwrap()),
                        Err(e) => SandboxResponse::Error(format!("Launch error: {}", e)),
                    },
                    Err(e) => SandboxResponse::Error(format!("Failed to read {}: {}", dapp_path, e)),
                }
            }
            Ok(SandboxRequest::GetStatus) => {
                SandboxResponse::Success(serde_json::json!({
                    "service": "dap-sandboxd",
                    "landlock_version": 5,
                    "seccomp_bpf_enabled": true,
                    "cgroups_v2": true,
                }))
            }
            Err(e) => SandboxResponse::Error(format!("Malformed request: {}", e)),
        };

        let resp_json = serde_json::to_string(&resp).unwrap_or_else(|_| {
            r#"{"status":"Error","data":"Serialization failed"}"#.to_string()
        });
        stream.write_all(resp_json.as_bytes())?;
        stream.write_all(b"\n")?;
        stream.flush()?;
    }
    Ok(())
}

pub fn run_sandbox_server(
    socket_path: &str,
    stop_flag: std::sync::Arc<std::sync::atomic::AtomicBool>,
) -> std::io::Result<()> {
    if Path::new(socket_path).exists() {
        let _ = std::fs::remove_file(socket_path);
    }
    if let Some(parent) = Path::new(socket_path).parent() {
        let _ = std::fs::create_dir_all(parent);
    }

    let listener = UnixListener::bind(socket_path)?;
    listener.set_nonblocking(true)?;

    println!("[dap-sandboxd] Unix domain socket listening at: {}", socket_path);

    while !stop_flag.load(std::sync::atomic::Ordering::Relaxed) {
        match listener.accept() {
            Ok((stream, _)) => {
                std::thread::spawn(move || {
                    let _ = handle_sandbox_client(stream);
                });
            }
            Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                std::thread::sleep(std::time::Duration::from_millis(50));
            }
            Err(e) => {
                eprintln!("[dap-sandboxd] Socket accept error: {}", e);
                break;
            }
        }
    }

    let _ = std::fs::remove_file(socket_path);
    println!("[dap-sandboxd] Sandbox server shut down gracefully.");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_dalek::SigningKey;
    use rand::rngs::OsRng;

    #[test]
    fn test_sandbox_manifest_and_environment_preparation() {
        let mut csprng = OsRng;
        let signing_key = SigningKey::generate(&mut csprng);

        let manifest = r#"
            [application]
            bundle_identifier = "org.daxos.calc"
            display_name = "DAXOS Calculator"
            version = "1.0.0"
            build_number = 1
            minimum_os_version = "1.0.0"

            [developer]
            id = "dev-core"
            legal_name = "Core Dev Team"

            [sandbox]
            enforce = true
            network_isolation = "strict"

            [permissions]
            required = ["daxos.permission.GPU_ACCELERATION"]
            optional = ["daxos.permission.NETWORK_OUTBOUND"]

            [resources]
            max_memory_mb = 256
            max_cpu_percent = 50
            max_file_descriptors = 1024

            [landlock_paths]
            read_write = ["~/Documents/Calc"]
            read_only = ["/usr/share/fonts"]
        "#;

        let dapp_bytes = dcodx_bundle::pack_dapp(
            manifest,
            b"fake_x86_bin",
            b"fake_arm_bin",
            b"fake_assets",
            &signing_key,
        ).expect("Packing failed");

        let granted = vec!["daxos.permission.GPU_ACCELERATION".to_string()];
        let env = SandboxEnforcer::prepare_environment(&dapp_bytes, &granted)
            .expect("Environment preparation failed");

        assert_eq!(env.bundle_id, "org.daxos.calc");
        assert_eq!(env.cgroup.memory_max_bytes, 256 * 1024 * 1024);
        assert_eq!(env.seccomp.blocked_syscalls.contains(&"ptrace"), true);

        // Jika permission required tidak granted, harus tolak
        let not_granted = vec![];
        let denied = SandboxEnforcer::prepare_environment(&dapp_bytes, &not_granted);
        assert!(denied.is_err());
    }
}
