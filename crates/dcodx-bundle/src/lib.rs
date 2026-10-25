//! ============================================================================
//! DAXOS DCODX BUNDLE TOOLCHAIN
//! File: crates/dcodx-bundle/src/lib.rs
//! Format: .dapp Universal Fat Binary Container with Ed25519 Cryptographic Proof
//! ============================================================================

use ed25519_dalek::{Signature, Signer, SigningKey, Verifier, VerifyingKey};
use sha3::{Digest, Sha3_512};
use std::fmt;
use std::io::{self, Cursor, Read, Write};

pub const DAPP_MAGIC_NUMBER: u32 = 0x44415058; // "DAPX" in ASCII Big-Endian
pub const DAPP_CONTAINER_VERSION: u16 = 0x0001;

pub const DBPP_MAGIC_NUMBER: u32 = 0x44425050; // "DBPP" in ASCII Big-Endian (DAXOS Blueprint Project Package)
pub const DBPP_CONTAINER_VERSION: u16 = 0x0001;

pub const DAPP_ARCH_X86_64: u32 = 0x00000001;
pub const DAPP_ARCH_ARM64: u32 = 0x00000002;

pub const DAPP_FLAG_SANDBOX_ENFORCED: u16 = 1 << 0;
pub const DAPP_FLAG_PAYLOAD_COMPRESSED: u16 = 1 << 1;
pub const DAPP_FLAG_HARDENED_RUNTIME: u16 = 1 << 2;

pub const HEADER_SIZE: usize = 64;
pub const ARCH_ENTRY_SIZE: usize = 96;
pub const DBPP_HEADER_SIZE: usize = 160;

#[derive(Debug)]
pub enum BundleError {
    InvalidMagic(u32),
    UnsupportedVersion(u16),
    BufferTooSmall { required: usize, actual: usize },
    DigestMismatch { expected: Vec<u8>, computed: Vec<u8> },
    SignatureVerificationFailed,
    Io(io::Error),
    CorruptedPackage(String),
}

impl fmt::Display for BundleError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            BundleError::InvalidMagic(m) => write!(f, "Invalid magic number: 0x{:08X}", m),
            BundleError::UnsupportedVersion(v) => write!(f, "Unsupported container version: {}", v),
            BundleError::BufferTooSmall { required, actual } => {
                write!(f, "Buffer too small: required {}, actual {}", required, actual)
            }
            BundleError::DigestMismatch { expected, computed } => {
                write!(f, "SHA3-512 digest mismatch: expected {:?}, computed {:?}", expected, computed)
            }
            BundleError::SignatureVerificationFailed => write!(f, "Ed25519 signature verification failed"),
            BundleError::Io(e) => write!(f, "I/O error: {}", e),
            BundleError::CorruptedPackage(s) => write!(f, "Corrupted package: {}", s),
        }
    }
}

impl std::error::Error for BundleError {}

impl From<io::Error> for BundleError {
    fn from(e: io::Error) -> Self {
        BundleError::Io(e)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DappHeader {
    pub magic: u32,
    pub version: u16,
    pub flags: u16,
    pub total_package_size: u64,
    pub manifest_offset: u64,
    pub manifest_length: u64,
    pub signature_offset: u64,
    pub signature_length: u64,
    pub arch_entry_count: u32,
    pub reserved: [u8; 12],
}

impl DappHeader {
    pub fn write_to<W: Write>(&self, w: &mut W) -> io::Result<()> {
        w.write_all(&self.magic.to_be_bytes())?;
        w.write_all(&self.version.to_le_bytes())?;
        w.write_all(&self.flags.to_le_bytes())?;
        w.write_all(&self.total_package_size.to_le_bytes())?;
        w.write_all(&self.manifest_offset.to_le_bytes())?;
        w.write_all(&self.manifest_length.to_le_bytes())?;
        w.write_all(&self.signature_offset.to_le_bytes())?;
        w.write_all(&self.signature_length.to_le_bytes())?;
        w.write_all(&self.arch_entry_count.to_le_bytes())?;
        w.write_all(&self.reserved)?;
        Ok(())
    }

    pub fn read_from<R: Read>(r: &mut R) -> Result<Self, BundleError> {
        let mut buf = [0u8; HEADER_SIZE];
        r.read_exact(&mut buf)?;

        let magic = u32::from_be_bytes(buf[0..4].try_into().unwrap());
        if magic != DAPP_MAGIC_NUMBER {
            return Err(BundleError::InvalidMagic(magic));
        }

        let version = u16::from_le_bytes(buf[4..6].try_into().unwrap());
        if version != DAPP_CONTAINER_VERSION {
            return Err(BundleError::UnsupportedVersion(version));
        }

        let flags = u16::from_le_bytes(buf[6..8].try_into().unwrap());
        let total_package_size = u64::from_le_bytes(buf[8..16].try_into().unwrap());
        let manifest_offset = u64::from_le_bytes(buf[16..24].try_into().unwrap());
        let manifest_length = u64::from_le_bytes(buf[24..32].try_into().unwrap());
        let signature_offset = u64::from_le_bytes(buf[32..40].try_into().unwrap());
        let signature_length = u64::from_le_bytes(buf[40..48].try_into().unwrap());
        let arch_entry_count = u32::from_le_bytes(buf[48..52].try_into().unwrap());
        let mut reserved = [0u8; 12];
        reserved.copy_from_slice(&buf[52..64]);

        Ok(Self {
            magic,
            version,
            flags,
            total_package_size,
            manifest_offset,
            manifest_length,
            signature_offset,
            signature_length,
            arch_entry_count,
            reserved,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DappArchEntry {
    pub arch_id: u32,
    pub flags: u32,
    pub binary_offset: u64,
    pub binary_length: u64,
    pub binary_sha3_512: [u8; 64],
    pub entry_point_offset: u64,
}

impl DappArchEntry {
    pub fn write_to<W: Write>(&self, w: &mut W) -> io::Result<()> {
        w.write_all(&self.arch_id.to_le_bytes())?;
        w.write_all(&self.flags.to_le_bytes())?;
        w.write_all(&self.binary_offset.to_le_bytes())?;
        w.write_all(&self.binary_length.to_le_bytes())?;
        w.write_all(&self.binary_sha3_512)?;
        w.write_all(&self.entry_point_offset.to_le_bytes())?;
        Ok(())
    }

    pub fn read_from<R: Read>(r: &mut R) -> Result<Self, BundleError> {
        let mut buf = [0u8; ARCH_ENTRY_SIZE];
        r.read_exact(&mut buf)?;

        let arch_id = u32::from_le_bytes(buf[0..4].try_into().unwrap());
        let flags = u32::from_le_bytes(buf[4..8].try_into().unwrap());
        let binary_offset = u64::from_le_bytes(buf[8..16].try_into().unwrap());
        let binary_length = u64::from_le_bytes(buf[16..24].try_into().unwrap());
        let mut binary_sha3_512 = [0u8; 64];
        binary_sha3_512.copy_from_slice(&buf[24..88]);
        let entry_point_offset = u64::from_le_bytes(buf[88..96].try_into().unwrap());

        Ok(Self {
            arch_id,
            flags,
            binary_offset,
            binary_length,
            binary_sha3_512,
            entry_point_offset,
        })
    }
}

#[derive(Debug, Clone)]
pub struct DappPackage {
    pub header: DappHeader,
    pub arch_entries: Vec<DappArchEntry>,
    pub manifest_content: String,
    pub signature_bytes: Vec<u8>,
    pub developer_public_key: Vec<u8>,
    pub x86_binary: Vec<u8>,
    pub arm64_binary: Vec<u8>,
    pub assets_payload: Vec<u8>,
}

#[derive(Debug, Clone)]
pub struct VerificationReport {
    pub is_valid: bool,
    pub total_size_bytes: u64,
    pub arch_count: u32,
    pub manifest_bundle_id: String,
    pub developer_key_hex: String,
}

pub fn compute_sha3_512(data: &[u8]) -> [u8; 64] {
    let mut hasher = Sha3_512::new();
    hasher.update(data);
    let result = hasher.finalize();
    let mut out = [0u8; 64];
    out.copy_from_slice(&result);
    out
}

pub fn pack_dapp(
    manifest_toml: &str,
    x86_bin: &[u8],
    arm64_bin: &[u8],
    assets: &[u8],
    signing_key: &SigningKey,
) -> Result<Vec<u8>, BundleError> {
    let arch_count = 2u32;
    let header_and_table_size = HEADER_SIZE + (ARCH_ENTRY_SIZE * arch_count as usize);

    let manifest_bytes = manifest_toml.as_bytes();
    let manifest_offset = header_and_table_size as u64;
    let manifest_length = manifest_bytes.len() as u64;

    let x86_offset = manifest_offset + manifest_length;
    let x86_length = x86_bin.len() as u64;

    let arm64_offset = x86_offset + x86_length;
    let arm64_length = arm64_bin.len() as u64;

    let assets_offset = arm64_offset + arm64_length;
    let assets_length = assets.len() as u64;

    let signature_offset = assets_offset + assets_length;

    let x86_hash = compute_sha3_512(x86_bin);
    let arm64_hash = compute_sha3_512(arm64_bin);

    let x86_entry = DappArchEntry {
        arch_id: DAPP_ARCH_X86_64,
        flags: 0,
        binary_offset: x86_offset,
        binary_length: x86_length,
        binary_sha3_512: x86_hash,
        entry_point_offset: 0x1000,
    };

    let arm64_entry = DappArchEntry {
        arch_id: DAPP_ARCH_ARM64,
        flags: 0,
        binary_offset: arm64_offset,
        binary_length: arm64_length,
        binary_sha3_512: arm64_hash,
        entry_point_offset: 0x1000,
    };

    // Buffer awal sebelum signature
    let mut unsigned_buffer = Vec::new();
    let dummy_header = DappHeader {
        magic: DAPP_MAGIC_NUMBER,
        version: DAPP_CONTAINER_VERSION,
        flags: DAPP_FLAG_SANDBOX_ENFORCED | DAPP_FLAG_HARDENED_RUNTIME,
        total_package_size: 0, // diisi nanti
        manifest_offset,
        manifest_length,
        signature_offset,
        signature_length: 0, // diisi nanti
        arch_entry_count: arch_count,
        reserved: [0u8; 12],
    };

    dummy_header.write_to(&mut unsigned_buffer)?;
    x86_entry.write_to(&mut unsigned_buffer)?;
    arm64_entry.write_to(&mut unsigned_buffer)?;
    unsigned_buffer.write_all(manifest_bytes)?;
    unsigned_buffer.write_all(x86_bin)?;
    unsigned_buffer.write_all(arm64_bin)?;
    unsigned_buffer.write_all(assets)?;

    // Sign the whole package hash
    let package_digest = compute_sha3_512(&unsigned_buffer);
    let signature = signing_key.sign(&package_digest);
    let verifying_key = signing_key.verifying_key();

    let mut sig_block = Vec::new();
    sig_block.write_all(&1u16.to_le_bytes())?; // version
    sig_block.write_all(&1u16.to_le_bytes())?; // cert chain depth
    sig_block.write_all(verifying_key.as_bytes())?; // 32 bytes public key
    sig_block.write_all(&signature.to_bytes())?; // 64 bytes signature

    let signature_length = sig_block.len() as u64;
    let total_package_size = unsigned_buffer.len() as u64 + signature_length;

    // Tulis ulang header yang benar
    let final_header = DappHeader {
        total_package_size,
        signature_length,
        ..dummy_header
    };

    let mut final_buffer = Vec::with_capacity(total_package_size as usize);
    final_header.write_to(&mut final_buffer)?;
    x86_entry.write_to(&mut final_buffer)?;
    arm64_entry.write_to(&mut final_buffer)?;
    final_buffer.write_all(manifest_bytes)?;
    final_buffer.write_all(x86_bin)?;
    final_buffer.write_all(arm64_bin)?;
    final_buffer.write_all(assets)?;
    final_buffer.write_all(&sig_block)?;

    Ok(final_buffer)
}

pub fn unpack_dapp(dapp_bytes: &[u8]) -> Result<DappPackage, BundleError> {
    if dapp_bytes.len() < HEADER_SIZE {
        return Err(BundleError::BufferTooSmall {
            required: HEADER_SIZE,
            actual: dapp_bytes.len(),
        });
    }

    let mut cursor = Cursor::new(dapp_bytes);
    let header = DappHeader::read_from(&mut cursor)?;

    let mut arch_entries = Vec::with_capacity(header.arch_entry_count as usize);
    for _ in 0..header.arch_entry_count {
        arch_entries.push(DappArchEntry::read_from(&mut cursor)?);
    }

    // Extract manifest
    let m_start = header.manifest_offset as usize;
    let m_end = m_start + header.manifest_length as usize;
    if m_end > dapp_bytes.len() {
        return Err(BundleError::CorruptedPackage("Manifest bounds exceed package size".into()));
    }
    let manifest_content = String::from_utf8_lossy(&dapp_bytes[m_start..m_end]).to_string();

    // Extract binaries
    let mut x86_bin = Vec::new();
    let mut arm64_bin = Vec::new();

    for entry in &arch_entries {
        let b_start = entry.binary_offset as usize;
        let b_end = b_start + entry.binary_length as usize;
        if b_end > dapp_bytes.len() {
            return Err(BundleError::CorruptedPackage("Binary bounds exceed package size".into()));
        }
        let bin_slice = &dapp_bytes[b_start..b_end];

        let computed_hash = compute_sha3_512(bin_slice);
        if computed_hash != entry.binary_sha3_512 {
            return Err(BundleError::DigestMismatch {
                expected: entry.binary_sha3_512.to_vec(),
                computed: computed_hash.to_vec(),
            });
        }

        if entry.arch_id == DAPP_ARCH_X86_64 {
            x86_bin = bin_slice.to_vec();
        } else if entry.arch_id == DAPP_ARCH_ARM64 {
            arm64_bin = bin_slice.to_vec();
        }
    }

    // Extract signature block
    let s_start = header.signature_offset as usize;
    let s_end = s_start + header.signature_length as usize;
    if s_end > dapp_bytes.len() {
        return Err(BundleError::CorruptedPackage("Signature block exceeds package size".into()));
    }
    let sig_slice = &dapp_bytes[s_start..s_end];
    if sig_slice.len() < 100 {
        return Err(BundleError::CorruptedPackage("Signature block malformed".into()));
    }

    let dev_pubkey = sig_slice[4..36].to_vec();
    let sig_bytes = sig_slice[36..100].to_vec();

    // Extract assets
    let last_arch = arch_entries.last().unwrap();
    let assets_start = (last_arch.binary_offset + last_arch.binary_length) as usize;
    let assets_payload = dapp_bytes[assets_start..s_start].to_vec();

    Ok(DappPackage {
        header,
        arch_entries,
        manifest_content,
        signature_bytes: sig_bytes,
        developer_public_key: dev_pubkey,
        x86_binary: x86_bin,
        arm64_binary: arm64_bin,
        assets_payload,
    })
}

pub fn verify_dapp(dapp_bytes: &[u8]) -> Result<VerificationReport, BundleError> {
    let package = unpack_dapp(dapp_bytes)?;

    let pubkey_bytes: [u8; 32] = package
        .developer_public_key
        .as_slice()
        .try_into()
        .map_err(|_| BundleError::CorruptedPackage("Invalid public key size".into()))?;

    let verifying_key = VerifyingKey::from_bytes(&pubkey_bytes)
        .map_err(|_| BundleError::CorruptedPackage("Invalid ed25519 public key".into()))?;

    let sig_bytes: [u8; 64] = package
        .signature_bytes
        .as_slice()
        .try_into()
        .map_err(|_| BundleError::CorruptedPackage("Invalid signature size".into()))?;

    let signature = Signature::from_bytes(&sig_bytes);

    // Reconstruct the exact unsigned slice
    let s_start = package.header.signature_offset as usize;
    let mut unsigned_slice = dapp_bytes[..s_start].to_vec();

    // Mask out the total_package_size and signature_length in the header for digest check
    unsigned_slice[8..16].copy_from_slice(&0u64.to_le_bytes());
    unsigned_slice[40..48].copy_from_slice(&0u64.to_le_bytes());

    let computed_digest = compute_sha3_512(&unsigned_slice);

    verifying_key
        .verify(&computed_digest, &signature)
        .map_err(|_| BundleError::SignatureVerificationFailed)?;

    let dev_key_hex = hex_encode(&package.developer_public_key);

    Ok(VerificationReport {
        is_valid: true,
        total_size_bytes: package.header.total_package_size,
        arch_count: package.header.arch_entry_count,
        manifest_bundle_id: "org.daxos.app".to_string(),
        developer_key_hex: dev_key_hex,
    })
}

// ============================================================================
// DAXOS BLUEPRINT PROJECT PACKAGE (.dbpp) IMPLEMENTATION
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DbppHeader {
    pub magic: u32,
    pub version: u16,
    pub flags: u16,
    pub total_package_size: u64,
    pub project_toml_offset: u64,
    pub project_toml_length: u64,
    pub manifest_offset: u64,
    pub manifest_length: u64,
    pub source_offset: u64,
    pub source_length: u64,
    pub assets_offset: u64,
    pub assets_length: u64,
    pub shaders_offset: u64,
    pub shaders_length: u64,
    pub checksum_sha3_512: [u8; 64],
}

impl DbppHeader {
    pub fn write_to<W: Write>(&self, w: &mut W) -> io::Result<()> {
        w.write_all(&self.magic.to_be_bytes())?;
        w.write_all(&self.version.to_le_bytes())?;
        w.write_all(&self.flags.to_le_bytes())?;
        w.write_all(&self.total_package_size.to_le_bytes())?;
        w.write_all(&self.project_toml_offset.to_le_bytes())?;
        w.write_all(&self.project_toml_length.to_le_bytes())?;
        w.write_all(&self.manifest_offset.to_le_bytes())?;
        w.write_all(&self.manifest_length.to_le_bytes())?;
        w.write_all(&self.source_offset.to_le_bytes())?;
        w.write_all(&self.source_length.to_le_bytes())?;
        w.write_all(&self.assets_offset.to_le_bytes())?;
        w.write_all(&self.assets_length.to_le_bytes())?;
        w.write_all(&self.shaders_offset.to_le_bytes())?;
        w.write_all(&self.shaders_length.to_le_bytes())?;
        w.write_all(&self.checksum_sha3_512)?;
        Ok(())
    }

    pub fn read_from<R: Read>(r: &mut R) -> Result<Self, BundleError> {
        let mut buf = [0u8; DBPP_HEADER_SIZE];
        r.read_exact(&mut buf)?;

        let magic = u32::from_be_bytes(buf[0..4].try_into().unwrap());
        if magic != DBPP_MAGIC_NUMBER {
            return Err(BundleError::InvalidMagic(magic));
        }

        let version = u16::from_le_bytes(buf[4..6].try_into().unwrap());
        if version != DBPP_CONTAINER_VERSION {
            return Err(BundleError::UnsupportedVersion(version));
        }

        let flags = u16::from_le_bytes(buf[6..8].try_into().unwrap());
        let total_package_size = u64::from_le_bytes(buf[8..16].try_into().unwrap());
        let project_toml_offset = u64::from_le_bytes(buf[16..24].try_into().unwrap());
        let project_toml_length = u64::from_le_bytes(buf[24..32].try_into().unwrap());
        let manifest_offset = u64::from_le_bytes(buf[32..40].try_into().unwrap());
        let manifest_length = u64::from_le_bytes(buf[40..48].try_into().unwrap());
        let source_offset = u64::from_le_bytes(buf[48..56].try_into().unwrap());
        let source_length = u64::from_le_bytes(buf[56..64].try_into().unwrap());
        let assets_offset = u64::from_le_bytes(buf[64..72].try_into().unwrap());
        let assets_length = u64::from_le_bytes(buf[72..80].try_into().unwrap());
        let shaders_offset = u64::from_le_bytes(buf[80..88].try_into().unwrap());
        let shaders_length = u64::from_le_bytes(buf[88..96].try_into().unwrap());
        let mut checksum_sha3_512 = [0u8; 64];
        checksum_sha3_512.copy_from_slice(&buf[96..160]);

        Ok(Self {
            magic,
            version,
            flags,
            total_package_size,
            project_toml_offset,
            project_toml_length,
            manifest_offset,
            manifest_length,
            source_offset,
            source_length,
            assets_offset,
            assets_length,
            shaders_offset,
            shaders_length,
            checksum_sha3_512,
        })
    }
}

#[derive(Debug, Clone)]
pub struct DbppPackage {
    pub header: DbppHeader,
    pub project_toml: String,
    pub manifest_toml: String,
    pub source_surf: String,
    pub assets_payload: Vec<u8>,
    pub shaders_payload: Vec<u8>,
}

pub fn pack_dbpp(
    project_toml: &str,
    manifest_toml: &str,
    source_surf: &str,
    assets: &[u8],
    shaders: &[u8],
) -> Result<Vec<u8>, BundleError> {
    let p_bytes = project_toml.as_bytes();
    let m_bytes = manifest_toml.as_bytes();
    let s_bytes = source_surf.as_bytes();

    let project_toml_offset = DBPP_HEADER_SIZE as u64;
    let project_toml_length = p_bytes.len() as u64;

    let manifest_offset = project_toml_offset + project_toml_length;
    let manifest_length = m_bytes.len() as u64;

    let source_offset = manifest_offset + manifest_length;
    let source_length = s_bytes.len() as u64;

    let assets_offset = source_offset + source_length;
    let assets_length = assets.len() as u64;

    let shaders_offset = assets_offset + assets_length;
    let shaders_length = shaders.len() as u64;

    let total_package_size = shaders_offset + shaders_length;

    // Hitung hash dari seluruh isi payload
    let mut payload = Vec::new();
    payload.write_all(p_bytes)?;
    payload.write_all(m_bytes)?;
    payload.write_all(s_bytes)?;
    payload.write_all(assets)?;
    payload.write_all(shaders)?;

    let checksum_sha3_512 = compute_sha3_512(&payload);

    let header = DbppHeader {
        magic: DBPP_MAGIC_NUMBER,
        version: DBPP_CONTAINER_VERSION,
        flags: 0,
        total_package_size,
        project_toml_offset,
        project_toml_length,
        manifest_offset,
        manifest_length,
        source_offset,
        source_length,
        assets_offset,
        assets_length,
        shaders_offset,
        shaders_length,
        checksum_sha3_512,
    };

    let mut final_buf = Vec::with_capacity(total_package_size as usize);
    header.write_to(&mut final_buf)?;
    final_buf.write_all(&payload)?;

    Ok(final_buf)
}

pub fn unpack_dbpp(dbpp_bytes: &[u8]) -> Result<DbppPackage, BundleError> {
    if dbpp_bytes.len() < DBPP_HEADER_SIZE {
        return Err(BundleError::BufferTooSmall {
            required: DBPP_HEADER_SIZE,
            actual: dbpp_bytes.len(),
        });
    }

    let mut cursor = Cursor::new(dbpp_bytes);
    let header = DbppHeader::read_from(&mut cursor)?;

    let p_start = header.project_toml_offset as usize;
    let p_end = p_start + header.project_toml_length as usize;

    let m_start = header.manifest_offset as usize;
    let m_end = m_start + header.manifest_length as usize;

    let s_start = header.source_offset as usize;
    let s_end = s_start + header.source_length as usize;

    let a_start = header.assets_offset as usize;
    let a_end = a_start + header.assets_length as usize;

    let sh_start = header.shaders_offset as usize;
    let sh_end = sh_start + header.shaders_length as usize;

    if sh_end > dbpp_bytes.len() {
        return Err(BundleError::CorruptedPackage("DBPP bounds exceed buffer length".into()));
    }

    let payload = &dbpp_bytes[p_start..sh_end];
    let computed_hash = compute_sha3_512(payload);
    if computed_hash != header.checksum_sha3_512 {
        return Err(BundleError::DigestMismatch {
            expected: header.checksum_sha3_512.to_vec(),
            computed: computed_hash.to_vec(),
        });
    }

    let project_toml = String::from_utf8_lossy(&dbpp_bytes[p_start..p_end]).to_string();
    let manifest_toml = String::from_utf8_lossy(&dbpp_bytes[m_start..m_end]).to_string();
    let source_surf = String::from_utf8_lossy(&dbpp_bytes[s_start..s_end]).to_string();
    let assets_payload = dbpp_bytes[a_start..a_end].to_vec();
    let shaders_payload = dbpp_bytes[sh_start..sh_end].to_vec();

    Ok(DbppPackage {
        header,
        project_toml,
        manifest_toml,
        source_surf,
        assets_payload,
        shaders_payload,
    })
}

pub fn pack_dbpp_dir(project_dir: &std::path::Path) -> Result<Vec<u8>, BundleError> {
    let p_path = project_dir.join("Project.toml");
    let m_path = project_dir.join("manifest.toml");
    let s_path = project_dir.join("src/main.surf");

    let p_content = if p_path.exists() {
        std::fs::read_to_string(&p_path)?
    } else {
        format!("[project]\nname = \"{}\"\nversion = \"1.10.2026\"\n",
            project_dir.file_name().and_then(|n| n.to_str()).unwrap_or("app"))
    };

    let m_content = if m_path.exists() {
        std::fs::read_to_string(&m_path)?
    } else {
        format!("bundle_identifier = \"org.daxos.{}\"\ndisplay_name = \"{}\"\nversion = \"1.10.2026\"\n",
            project_dir.file_name().and_then(|n| n.to_str()).unwrap_or("app"),
            project_dir.file_name().and_then(|n| n.to_str()).unwrap_or("App"))
    };

    let s_content = if s_path.exists() {
        std::fs::read_to_string(&s_path)?
    } else {
        "module daxos.app; component Main: Component {}".to_string()
    };

    let assets = b"DBPP_ASSETS_ZSTD_RESOURCES_BLOCK";
    let shaders = b"DBPP_SHADERS_DREXVIS_SPIRV_BLOCK";

    pack_dbpp(&p_content, &m_content, &s_content, assets, shaders)
}

pub fn extract_dbpp_to_dir(dbpp_bytes: &[u8], target_dir: &std::path::Path) -> Result<(), BundleError> {
    let pkg = unpack_dbpp(dbpp_bytes)?;
    std::fs::create_dir_all(target_dir.join("src"))?;
    std::fs::create_dir_all(target_dir.join("assets"))?;
    std::fs::create_dir_all(target_dir.join("shaders"))?;

    std::fs::write(target_dir.join("Project.toml"), pkg.project_toml)?;
    std::fs::write(target_dir.join("manifest.toml"), pkg.manifest_toml)?;
    std::fs::write(target_dir.join("src/main.surf"), pkg.source_surf)?;
    std::fs::write(target_dir.join("assets/resources.bin"), pkg.assets_payload)?;
    std::fs::write(target_dir.join("shaders/drevis_shaders.bin"), pkg.shaders_payload)?;

    Ok(())
}

fn hex_encode(data: &[u8]) -> String {
    data.iter().map(|b| format!("{:02x}", b)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::rngs::OsRng;

    #[test]
    fn test_pack_unpack_and_verify() {
        let mut csprng = OsRng;
        let signing_key = SigningKey::generate(&mut csprng);

        let manifest = r#"
            [application]
            bundle_identifier = "org.daxos.calc"
            version = "1.0.0"
        "#;
        let x86_bin = b"\x7fELF_FAKE_X86_64_BINARY_DATA_0123456789";
        let arm64_bin = b"\x7fELF_FAKE_ARM64_BINARY_DATA_9876543210";
        let assets = b"ASSETS_ZSTD_MOCK_STREAM";

        let packed_bundle = pack_dapp(manifest, x86_bin, arm64_bin, assets, &signing_key)
            .expect("Packing .dapp failed");

        assert!(packed_bundle.len() > HEADER_SIZE + (ARCH_ENTRY_SIZE * 2));

        let unpacked = unpack_dapp(&packed_bundle).expect("Unpacking failed");
        assert_eq!(unpacked.header.magic, DAPP_MAGIC_NUMBER);
        assert_eq!(unpacked.header.version, DAPP_CONTAINER_VERSION);
        assert_eq!(unpacked.arch_entries.len(), 2);
        assert_eq!(unpacked.x86_binary, x86_bin);
        assert_eq!(unpacked.arm64_binary, arm64_bin);
        assert_eq!(unpacked.assets_payload, assets);

        let report = verify_dapp(&packed_bundle).expect("Verification failed");
        assert!(report.is_valid);
    }

    #[test]
    fn test_tamper_detection() {
        let mut csprng = OsRng;
        let signing_key = SigningKey::generate(&mut csprng);

        let manifest = "test_manifest";
        let x86_bin = b"valid_binary";
        let arm64_bin = b"valid_arm_binary";
        let assets = b"valid_assets";

        let mut packed = pack_dapp(manifest, x86_bin, arm64_bin, assets, &signing_key).unwrap();

        // Modifikasi 1 byte di dalam payload
        let tamper_idx = packed.len() - 150;
        packed[tamper_idx] ^= 0xFF;

        let verify_result = verify_dapp(&packed);
        assert!(verify_result.is_err(), "Tampered package must fail verification!");
    }

    #[test]
    fn test_dbpp_pack_and_unpack() {
        let p_toml = "[project]\nname = \"StudioTest\"\nversion = \"1.10.2026\"\n";
        let m_toml = "bundle_identifier = \"org.daxos.studiotest\"\n";
        let s_surf = "module daxos.test; component StudioApp: Component {}";
        let assets = b"ASSETS_TEST_DATA";
        let shaders = b"SHADERS_TEST_DATA";

        let dbpp_bytes = pack_dbpp(p_toml, m_toml, s_surf, assets, shaders)
            .expect("Failed to pack dbpp");
        assert!(dbpp_bytes.len() >= DBPP_HEADER_SIZE);

        let pkg = unpack_dbpp(&dbpp_bytes).expect("Failed to unpack dbpp");
        assert_eq!(pkg.header.magic, DBPP_MAGIC_NUMBER);
        assert_eq!(pkg.header.version, DBPP_CONTAINER_VERSION);
        assert_eq!(pkg.project_toml, p_toml);
        assert_eq!(pkg.manifest_toml, m_toml);
        assert_eq!(pkg.source_surf, s_surf);
        assert_eq!(pkg.assets_payload, assets);
        assert_eq!(pkg.shaders_payload, shaders);
    }
}
