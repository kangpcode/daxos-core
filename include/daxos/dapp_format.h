/**
 * ============================================================================
 * DAXOS OPERATING SYSTEM - DAPP FAT BINARY CONTAINER HEADER SPECIFICATION
 * File: include/daxos/dapp_format.h
 * Language: ANSI C99 / C++23 Standalone Header
 * ============================================================================
 */

#ifndef DAXOS_DAPP_FORMAT_H
#define DAXOS_DAPP_FORMAT_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#pragma pack(push, 1)

/** Magic Number: "DAPX" in ASCII Big-Endian (0x44415058) */
#define DAPP_MAGIC_NUMBER 0x44415058U

/** Versi Kontainer DAPP Saat Ini */
#define DAPP_CONTAINER_VERSION 0x0001U

/** Identifikasi Arsitektur CPU Target */
#define DAPP_ARCH_X86_64  0x00000001U
#define DAPP_ARCH_ARM64   0x00000002U

/** Flag Bitmask Kontainer */
#define DAPP_FLAG_SANDBOX_ENFORCED    (1U << 0)
#define DAPP_FLAG_PAYLOAD_COMPRESSED  (1U << 1)
#define DAPP_FLAG_HARDENED_RUNTIME    (1U << 2)

/**
 * Entri Arsitektur Biner di dalam Header FAT DAPP
 * Ukuran per entri: 96 byte
 */
typedef struct {
    uint32_t arch_id;              /**< DAPP_ARCH_X86_64 atau DAPP_ARCH_ARM64 */
    uint32_t flags;                /**< Ekstensi instruksi khusus (mis. AVX2, NEON) */
    uint64_t binary_offset;        /**< Byte offset dari awal file ke payload biner ELF */
    uint64_t binary_length;        /**< Panjang payload biner dalam byte */
    uint8_t  binary_sha3_512[64];  /**< SHA3-512 digest biner untuk verifikasi integritas */
    uint64_t entry_point_offset;   /**< Virtual memory offset simbol entry point */
} DappArchEntry;

/**
 * Header Utama File .dapp (Fat Executable Container)
 * Ukuran tetap: 64 byte dasar + (N * 96 byte entri arsitektur)
 */
typedef struct {
    uint32_t magic;                /**< Harus bernilai DAPP_MAGIC_NUMBER (0x44415058) */
    uint16_t version;              /**< Harus bernilai DAPP_CONTAINER_VERSION (0x0001) */
    uint16_t flags;                /**< Bitmask status keamanan & kompresi kontainer */
    uint64_t total_package_size;   /**< Total ukuran seluruh file .dapp dalam byte */
    uint64_t manifest_offset;      /**< Byte offset ke payload manifest.toml / manifest.dson */
    uint64_t manifest_length;      /**< Ukuran manifest dalam byte */
    uint64_t signature_offset;     /**< Byte offset ke blok tanda tangan Ed25519 & sertifikat */
    uint64_t signature_length;     /**< Panjang blok tanda tangan dan rantai sertifikat */
    uint32_t arch_entry_count;     /**< Jumlah arsitektur biner yang tersedia (default: 2) */
    uint8_t  reserved[12];         /**< Reserved padding untuk ekstensi ABI masa depan (isi nol) */
} DappHeader;

/**
 * Blok Tanda Tangan Kriptografis Ed25519 (.dapp signature block)
 */
typedef struct {
    uint16_t sig_version;          /**< Versi blok tanda tangan (0x0001) */
    uint16_t cert_chain_depth;     /**< Jumlah sertifikat dalam rantai (default: 3) */
    uint8_t  ed25519_signature[64];/**< Tanda tangan Ed25519 atas SHA3-512 paket */
    uint64_t certificate_chain_len;/**< Panjang byte blok sertifikat X.509 DER */
} DappSignatureBlock;

#pragma pack(pop)

#ifdef __cplusplus
}
#endif

#endif /* DAXOS_DAPP_FORMAT_H */
