//! ============================================================================
//! DAXOS DAPP CONTAINER HEADER & PARSER FUZZER
//! File: crates/dcodx-bundle/tests/test_dapp_header_fuzz.rs
//! Purpose: Validates robustness against malformed, corrupted, and hostile payloads
//! ============================================================================

use dcodx_bundle::{unpack_dapp, verify_dapp, BundleError, DAPP_MAGIC_NUMBER, HEADER_SIZE};

#[test]
fn test_fuzz_corrupted_magic_numbers() {
    let mut bad_header = [0u8; 256];
    // Write corrupted magic
    bad_header[0..4].copy_from_slice(&0xDEADBEEFu32.to_be_bytes());

    let res = unpack_dapp(&bad_header);
    assert!(res.is_err());
    match res.unwrap_err() {
        BundleError::InvalidMagic(m) => assert_eq!(m, 0xDEADBEEF),
        other => panic!("Expected InvalidMagic, got: {:?}", other),
    }
}

#[test]
fn test_fuzz_truncated_header_buffers() {
    for size in 0..HEADER_SIZE {
        let truncated = vec![0x44; size];
        let res = unpack_dapp(&truncated);
        assert!(res.is_err(), "Truncated buffer of size {} must fail gracefully", size);
    }
}

#[test]
fn test_fuzz_out_of_bounds_offsets() {
    let mut header = [0u8; 1024];
    // Valid magic
    header[0..4].copy_from_slice(&DAPP_MAGIC_NUMBER.to_be_bytes());
    // Version 1
    header[4..6].copy_from_slice(&1u16.to_le_bytes());
    // Out-of-bounds total size: claim 100MB but buffer is 1KB
    header[8..16].copy_from_slice(&100_000_000u64.to_le_bytes());
    // Out-of-bounds offsets
    header[16..24].copy_from_slice(&99_000_000u64.to_le_bytes()); // manifest_offset
    header[24..32].copy_from_slice(&10_000u64.to_le_bytes());     // manifest_length
    header[32..40].copy_from_slice(&99_500_000u64.to_le_bytes()); // signature_offset
    header[40..48].copy_from_slice(&64u64.to_le_bytes());         // signature_length
    header[48..52].copy_from_slice(&2u32.to_le_bytes());          // arch_entry_count

    let res = unpack_dapp(&header);
    assert!(res.is_err());
    let verify_res = verify_dapp(&header);
    assert!(verify_res.is_err());
}

#[test]
fn test_fuzz_pseudo_random_header_mutations() {
    // Generate 500 pseudo-random byte permutations to test parser resilience
    let mut lfsr: u32 = 0xACE1;
    for iteration in 0..500 {
        let mut buffer = vec![0u8; 128 + (iteration % 256)];
        for byte in buffer.iter_mut() {
            let bit = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5)) & 1;
            lfsr = (lfsr >> 1) | (bit << 15);
            *byte = (lfsr & 0xFF) as u8;
        }

        // Neither unpack nor verify must panic under any condition
        let _ = unpack_dapp(&buffer);
        let _ = verify_dapp(&buffer);
    }
}
