/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * DAXOS DXU HYBRID KERNEL - NTSYNC DRIVER INTERNAL HEADER
 * File: kernel/modules/daxos_ntsync/ntsync.h
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _DAXOS_NTSYNC_INTERNAL_H
#define _DAXOS_NTSYNC_INTERNAL_H

#include <linux/types.h>
#include <linux/spinlock.h>
#include <linux/wait.h>
#include <linux/kref.h>
#include "../../include/uapi/daxos/ntsync.h"

#define NTSYNC_MAX_OBJS 1024

struct ntsync_object {
	__u32 id;
	__u32 type; /* NTSYNC_TYPE_* */
	struct kref kref;
	spinlock_t lock;
	wait_queue_head_t waitq;

	union {
		struct {
			__u32 count;
			__u32 max;
		} sem;
		struct {
			pid_t owner_tid;
			__u32 recursion_count;
		} mutex;
		struct {
			bool manual_reset;
			bool signaled;
		} event;
	} u;
};

struct ntsync_device {
	struct miscdevice misc;
	spinlock_t table_lock;
	struct ntsync_object *objects[NTSYNC_MAX_OBJS];
	__u32 next_id;
};

#endif /* _DAXOS_NTSYNC_INTERNAL_H */
