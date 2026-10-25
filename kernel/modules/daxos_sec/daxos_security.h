/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * DAXOS DXU HYBRID KERNEL - SECURITY & INTEGRITY INTERNAL HEADER
 * File: kernel/modules/daxos_sec/daxos_security.h
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _DAXOS_SECURITY_INTERNAL_H
#define _DAXOS_SECURITY_INTERNAL_H

#include <linux/types.h>
#include <linux/spinlock.h>
#include <linux/miscdevice.h>
#include <linux/kobject.h>
#include <linux/sysfs.h>
#include "../../include/uapi/daxos/security.h"

#define DAXOS_MAX_TAMPER_LOGS 32

struct daxos_sec_core {
	struct miscdevice misc;
	struct kobject *kobj;
	spinlock_t lock;

	struct daxos_integrity_status status;
	struct daxos_tamper_event tamper_logs[DAXOS_MAX_TAMPER_LOGS];
	int tamper_log_count;
};

#endif /* _DAXOS_SECURITY_INTERNAL_H */
