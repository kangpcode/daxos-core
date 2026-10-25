//! ============================================================================
//! DAXOS PRODUCTION STORAGE & PARTITION MANAGER (dax-disks)
//! File: crates/dax-disks/src/lib.rs
//! Purpose: Real Linux sysfs/procfs block device, partition, and mount analyzer
//! Strictly ZERO EMOJIS - Production Grade
//! ============================================================================

use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BlockDevice {
    pub name: String,
    pub major: u32,
    pub minor: u32,
    pub blocks: u64,
    pub size_bytes: u64,
    pub is_rotational: bool,
    pub is_partition: bool,
    pub model: String,
    pub mount_point: Option<String>,
    pub fs_type: Option<String>,
    pub used_bytes: Option<u64>,
    pub avail_bytes: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MountEntry {
    pub device: String,
    pub mount_point: String,
    pub fs_type: String,
    pub options: String,
}

pub struct DiskScanner;

impl DiskScanner {
    /// Read all active mount points from /proc/mounts
    pub fn get_mounts() -> Vec<MountEntry> {
        let mut mounts = Vec::new();
        if let Ok(content) = fs::read_to_string("/proc/mounts") {
            for line in content.lines() {
                let parts: Vec<&str> = line.split_whitespace().collect();
                if parts.len() >= 4 {
                    mounts.push(MountEntry {
                        device: parts[0].to_string(),
                        mount_point: parts[1].to_string(),
                        fs_type: parts[2].to_string(),
                        options: parts[3].to_string(),
                    });
                }
            }
        }
        mounts
    }

    /// Read all block devices from /proc/partitions and /sys/block
    pub fn get_block_devices() -> Vec<BlockDevice> {
        let mut devices = Vec::new();
        let mounts = Self::get_mounts();

        if let Ok(content) = fs::read_to_string("/proc/partitions") {
            for line in content.lines().skip(2) {
                let parts: Vec<&str> = line.split_whitespace().collect();
                if parts.len() >= 4 {
                    let major: u32 = parts[0].parse().unwrap_or(0);
                    let minor: u32 = parts[1].parse().unwrap_or(0);
                    let blocks: u64 = parts[2].parse().unwrap_or(0);
                    let name = parts[3].to_string();

                    // 1 block in /proc/partitions is usually 1024 bytes (1 KiB)
                    let size_bytes = blocks * 1024;

                    // Determine base device (e.g. nvme0n1 for nvme0n1p1, sda for sda1)
                    let base_dev = if name.starts_with("nvme") {
                        if let Some(idx) = name.find('p') {
                            name[..idx].to_string()
                        } else {
                            name.clone()
                        }
                    } else {
                        name.trim_end_matches(char::is_numeric).to_string()
                    };

                    let is_rotational = Self::check_rotational(&base_dev);
                    let is_partition = name != base_dev;
                    let model = Self::read_model(&base_dev);

                    // Check if this device is mounted
                    let dev_path = format!("/dev/{}", name);
                    let mount_info = mounts.iter().find(|m| m.device == dev_path);
                    let mount_point = mount_info.map(|m| m.mount_point.clone());
                    let fs_type = mount_info.map(|m| m.fs_type.clone());

                    let (used_bytes, avail_bytes) = if let Some(ref mp) = mount_point {
                        Self::get_statvfs_usage(mp)
                    } else {
                        (None, None)
                    };

                    devices.push(BlockDevice {
                        name,
                        major,
                        minor,
                        blocks,
                        size_bytes,
                        is_rotational,
                        is_partition,
                        model,
                        mount_point,
                        fs_type,
                        used_bytes,
                        avail_bytes,
                    });
                }
            }
        }

        devices
    }

    fn check_rotational(base_dev: &str) -> bool {
        let path = format!("/sys/block/{}/queue/rotational", base_dev);
        if let Ok(val) = fs::read_to_string(path) {
            val.trim() == "1"
        } else {
            false
        }
    }

    fn read_model(base_dev: &str) -> String {
        let path = format!("/sys/block/{}/device/model", base_dev);
        if let Ok(val) = fs::read_to_string(path) {
            val.trim().to_string()
        } else {
            if base_dev.starts_with("nvme") {
                "NVMe Solid State Drive".to_string()
            } else if base_dev.starts_with("loop") {
                "Loopback Device".to_string()
            } else {
                "Generic Block Storage".to_string()
            }
        }
    }

    /// Read usage via statvfs libc call safely
    pub fn get_statvfs_usage(path: &str) -> (Option<u64>, Option<u64>) {
        use std::ffi::CString;
        use std::mem::MaybeUninit;

        let c_path = match CString::new(path) {
            Ok(c) => c,
            Err(_) => return (None, None),
        };

        unsafe {
            let mut stat = MaybeUninit::<libc::statvfs>::uninit();
            if libc::statvfs(c_path.as_ptr(), stat.as_mut_ptr()) == 0 {
                let stat = stat.assume_init();
                let bsize = stat.f_frsize;
                let total = stat.f_blocks * bsize;
                let avail = stat.f_bavail * bsize;
                let used = total.saturating_sub(stat.f_bfree * bsize);
                (Some(used), Some(avail))
            } else {
                (None, None)
            }
        }
    }

    pub fn format_bytes(bytes: u64) -> String {
        const KB: u64 = 1024;
        const MB: u64 = KB * 1024;
        const GB: u64 = MB * 1024;
        const TB: u64 = GB * 1024;

        if bytes >= TB {
            format!("{:.2} TB", bytes as f64 / TB as f64)
        } else if bytes >= GB {
            format!("{:.2} GB", bytes as f64 / GB as f64)
        } else if bytes >= MB {
            format!("{:.2} MB", bytes as f64 / MB as f64)
        } else if bytes >= KB {
            format!("{:.2} KB", bytes as f64 / KB as f64)
        } else {
            format!("{} B", bytes)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_bytes() {
        assert_eq!(DiskScanner::format_bytes(500), "500 B");
        assert_eq!(DiskScanner::format_bytes(1024), "1.00 KB");
        assert_eq!(DiskScanner::format_bytes(1024 * 1024 * 512), "512.00 MB");
        assert_eq!(DiskScanner::format_bytes(1024 * 1024 * 1024 * 4), "4.00 GB");
    }

    #[test]
    fn test_mount_reading_from_proc() {
        let mounts = DiskScanner::get_mounts();
        assert!(!mounts.is_empty(), "Must read at least one mount from /proc/mounts");
        assert!(mounts.iter().any(|m| m.mount_point == "/"));
    }

    #[test]
    fn test_block_devices_reading() {
        let devs = DiskScanner::get_block_devices();
        assert!(!devs.is_empty(), "Must read devices from /proc/partitions");
    }
}
