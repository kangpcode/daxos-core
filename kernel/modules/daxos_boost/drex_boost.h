/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * DAXOS DXU HYBRID KERNEL - DREX-BOOST INTERNAL HEADER
 * File: kernel/modules/daxos_boost/drex_boost.h
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _DAXOS_DREX_BOOST_INTERNAL_H
#define _DAXOS_DREX_BOOST_INTERNAL_H

#include <linux/types.h>
#include <linux/spinlock.h>
#include <linux/timer.h>
#include <linux/miscdevice.h>
#include <linux/proc_fs.h>
#include "../../include/uapi/daxos/boost.h"

#define DREX_MAX_BOOST_TASKS 64

struct drex_boosted_task {
	pid_t pid;
	__u32 task_type;
	__u32 target_fps;
	__u32 latency_budget_us;
	__u64 registered_jiffies;
	__u64 frames_rendered;
};

struct drex_boost_core {
	struct miscdevice misc;
	struct proc_dir_entry *proc_entry;
	struct proc_dir_entry *proc_dir;
	spinlock_t lock;
	struct timer_list decay_timer;

	struct drex_boosted_task tasks[DREX_MAX_BOOST_TASKS];
	int task_count;

	/* Telemetry */
	struct drex_boost_telemetry telemetry;
	__u64 last_input_jiffies;
};

#endif /* _DAXOS_DREX_BOOST_INTERNAL_H */
