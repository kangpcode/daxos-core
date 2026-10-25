/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
/*
 * DAXOS DXU HYBRID KERNEL - DAPP BINARY FORMAT UAPI HEADER
 * File: kernel/include/uapi/daxos/dapp_binfmt.h
 * Purpose: Native in-kernel execution handler for .dapp Universal Fat Bundles
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _UAPI_DAXOS_DAPP_BINFMT_H
#define _UAPI_DAXOS_DAPP_BINFMT_H

#include <linux/types.h>

#define DAPP_MAGIC           0x44415050 /* ASCII "DAPP" */
#define DAPP_FORMAT_VERSION  1

#define DAPP_ARCH_X86_64     0x01
#define DAPP_ARCH_ARM64      0x02
#define DAPP_ARCH_RISCV64    0x03

#define DAPP_FLAG_SANDBOXED  0x0001
#define DAPP_FLAG_SIGNED     0x0002
#define DAPP_FLAG_COMPRESSED 0x0004

/* Per-architecture binary descriptor entry */
struct dapp_arch_entry_v1 {
	__u32 arch_id;          /* DAPP_ARCH_* */
	__u32 flags;
	__u64 binary_offset;    /* Byte offset from file start */
	__u64 binary_size;      /* Binary length in bytes */
	__u64 entry_point;      /* Virtual entry point offset */
	__u8  sha3_512[64];     /* Cryptographic binary digest */
};

/* File header (64-byte aligned) */
struct dapp_header_v1 {
	__u32 magic;            /* 0x44415050 */
	__u16 version;          /* 1 */
	__u16 header_size;      /* sizeof(struct dapp_header_v1) */
	__u32 arch_count;       /* Number of bundled architectures */
	__u32 flags;            /* DAPP_FLAG_* */
	__u64 manifest_offset;  /* Offset to embedded Landlock TOML manifest */
	__u64 manifest_size;
	__u64 signature_offset; /* Offset to Ed25519 signature proof */
	__u64 signature_size;
	__u8  developer_id[32]; /* Developer public key identity */
	__u8  reserved[64];     /* Reserved for future expansion */
};

#endif /* _UAPI_DAXOS_DAPP_BINFMT_H */
