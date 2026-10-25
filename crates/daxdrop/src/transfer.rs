//! ============================================================================
//! DAXDROP CRYPTOGRAPHIC FILE TRANSFER PIPELINE
//! File: crates/daxdrop/src/transfer.rs
//! Purpose: Encrypted streaming transfer over TLS 1.3 / ChaCha20-Poly1305
//! ============================================================================

use serde::{Deserialize, Serialize};
use sha3::{Digest, Sha3_512};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TransferManifest {
    pub transfer_id: String,
    pub filename: String,
    pub file_size_bytes: u64,
    pub sha3_hash: String,
    pub sender_name: String,
    pub receiver_name: String,
    pub chunk_count: u32,
}

pub struct TransferManager;

impl TransferManager {
    pub fn prepare_manifest(
        filename: &str,
        content: &[u8],
        sender: &str,
        receiver: &str,
    ) -> TransferManifest {
        let mut hasher = Sha3_512::new();
        hasher.update(content);
        let result = hasher.finalize();
        let hash_hex = format!("{:x}", result);

        let chunk_size = 64 * 1024; // 64 KB chunks
        let chunk_count = ((content.len() as f64) / (chunk_size as f64)).ceil() as u32;

        TransferManifest {
            transfer_id: format!("transfer-{}", &hash_hex[..8]),
            filename: filename.to_string(),
            file_size_bytes: content.len() as u64,
            sha3_hash: hash_hex,
            sender_name: sender.to_string(),
            receiver_name: receiver.to_string(),
            chunk_count: std::cmp::max(1, chunk_count),
        }
    }

    pub fn verify_integrity(manifest: &TransferManifest, received_bytes: &[u8]) -> bool {
        let mut hasher = Sha3_512::new();
        hasher.update(received_bytes);
        let result = hasher.finalize();
        let hash_hex = format!("{:x}", result);
        manifest.sha3_hash == hash_hex && manifest.file_size_bytes == received_bytes.len() as u64
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_transfer_manifest_and_verification() {
        let sample_data = b"DAXOS Kernel 6.6.21-rhino Production Image File";
        let manifest = TransferManager::prepare_manifest("kernel.bin", sample_data, "laptop", "phone");

        assert_eq!(manifest.filename, "kernel.bin");
        assert_eq!(manifest.file_size_bytes, sample_data.len() as u64);
        assert!(!manifest.sha3_hash.is_empty());

        let ok = TransferManager::verify_integrity(&manifest, sample_data);
        assert!(ok);

        let corrupted = b"Corrupted Data";
        let bad = TransferManager::verify_integrity(&manifest, corrupted);
        assert!(!bad);
    }
}
