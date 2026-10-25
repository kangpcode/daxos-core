/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
/*
 * DAXOS DXU HYBRID KERNEL - NTSYNC UAPI HEADER
 * File: kernel/include/uapi/daxos/ntsync.h
 * Purpose: Windows NT fast synchronization object emulation via /dev/ntsync
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _UAPI_DAXOS_NTSYNC_H
#define _UAPI_DAXOS_NTSYNC_H

#include <linux/types.h>
#include <linux/ioctl.h>

#define NTSYNC_IOC_MAGIC 0x86

/* Object types */
#define NTSYNC_TYPE_SEM       1
#define NTSYNC_TYPE_MUTEX     2
#define NTSYNC_TYPE_EVENT     3

/* Event flags */
#define NTSYNC_EVENT_MANUAL_RESET   0x0001
#define NTSYNC_EVENT_INITIAL_STATE  0x0002

/* Wait flags */
#define NTSYNC_WAIT_ALERTABLE       0x0001
#define NTSYNC_WAIT_TIMEOUT_REL     0x0002

/* Semaphore creation arguments */
struct ntsync_sem_args {
	__u32 count;
	__u32 max;
	__u32 flags;
	__u32 sem_id;
};

/* Mutex creation arguments */
struct ntsync_mutex_args {
	__u32 initial_owner;
	__u32 flags;
	__u32 mutex_id;
	__u32 reserved;
};

/* Event creation arguments */
struct ntsync_event_args {
	__u32 manual_reset;
	__u32 initial_state;
	__u32 flags;
	__u32 event_id;
};

/* Wait operation arguments */
struct ntsync_wait_args {
	__u64 timeout_ns;
	__u32 count;
	__u32 flags;
	__u32 *objs;
	__u32 signaled_index;
	__u32 result_status;
};

/* Signal operation arguments */
struct ntsync_signal_args {
	__u32 obj_id;
	__u32 release_count;
	__u32 previous_count;
	__u32 flags;
};

/* IOCTL Commands */
#define NTSYNC_IOC_CREATE_SEM     _IOWR(NTSYNC_IOC_MAGIC, 0x01, struct ntsync_sem_args)
#define NTSYNC_IOC_CREATE_MUTEX   _IOWR(NTSYNC_IOC_MAGIC, 0x02, struct ntsync_mutex_args)
#define NTSYNC_IOC_CREATE_EVENT   _IOWR(NTSYNC_IOC_MAGIC, 0x03, struct ntsync_event_args)
#define NTSYNC_IOC_WAIT_ANY       _IOWR(NTSYNC_IOC_MAGIC, 0x04, struct ntsync_wait_args)
#define NTSYNC_IOC_WAIT_ALL       _IOWR(NTSYNC_IOC_MAGIC, 0x05, struct ntsync_wait_args)
#define NTSYNC_IOC_SIGNAL         _IOWR(NTSYNC_IOC_MAGIC, 0x06, struct ntsync_signal_args)
#define NTSYNC_IOC_RESET_EVENT    _IOWR(NTSYNC_IOC_MAGIC, 0x07, __u32)

#endif /* _UAPI_DAXOS_NTSYNC_H */
