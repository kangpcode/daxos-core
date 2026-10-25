/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
/*
 * DAXOS DXU HYBRID KERNEL - SECURITY & INTEGRITY UAPI HEADER
 * File: kernel/include/uapi/daxos/security.h
 * Purpose: In-kernel dm-verity Merkle root integrity and tamper reporting
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _UAPI_DAXOS_SECURITY_H
#define _UAPI_DAXOS_SECURITY_H

#include <linux/types.h>
#include <linux/ioctl.h>

#define DAXOS_SEC_IOC_MAGIC 0x88

/* Integrity state flags */
#define DAXOS_INTEGRITY_OK              0x0001
#define DAXOS_INTEGRITY_ROOTFS_RO       0x0002
#define DAXOS_INTEGRITY_DMVERITY_LOCKED 0x0004
#define DAXOS_INTEGRITY_LANDLOCK_V5     0x0008
#define DAXOS_INTEGRITY_TPM2_SEALED     0x0010
#define DAXOS_INTEGRITY_TAMPER_ALERT    0x8000

/* Security status report */
struct daxos_integrity_status {
	__u32 integrity_flags;
	__u8  expected_root_hash[64]; /* SHA3-512 root hash (64 bytes) */
	__u8  current_root_hash[64];
	__u32 sandbox_violations_count;
	__u32 landlock_abi_version;
	__u32 active_sandboxed_cgroups;
	__u64 uptime_seconds;
};

/* Security tamper event logged to netlink ring buffer */
struct daxos_tamper_event {
	__u32 event_type;       /* 1 = Mount tamper, 2 = Seccomp breach, 3 = Landlock escape */
	__s32 violator_pid;
	__u32 violator_uid;
	char  process_comm[16];
	char  target_path[256];
	__u64 timestamp_ns;
};

/* IOCTL Commands */
#define DAXOS_SEC_IOC_GET_STATUS     _IOR(DAXOS_SEC_IOC_MAGIC, 0x01, struct daxos_integrity_status)
#define DAXOS_SEC_IOC_VERIFY_ROOTHASH _IOW(DAXOS_SEC_IOC_MAGIC, 0x02, __u8[64])
#define DAXOS_SEC_IOC_FLUSH_ALERTS   _IO(DAXOS_SEC_IOC_MAGIC,  0x03)

#endif /* _UAPI_DAXOS_SECURITY_H */
