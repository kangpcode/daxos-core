/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
/*
 * DAXOS DXU HYBRID KERNEL - DREX-BOOST SCHEDULER UAPI HEADER
 * File: kernel/include/uapi/daxos/boost.h
 * Purpose: Interactive UI & audio thread priority clamping via /dev/daxos_boost
 * Copyright (C) 2026 DAXOS Operating System Core Team.
 */

#ifndef _UAPI_DAXOS_BOOST_H
#define _UAPI_DAXOS_BOOST_H

#include <linux/types.h>
#include <linux/ioctl.h>

#define DREX_BOOST_IOC_MAGIC 0x87

/* Priority Flags for sched_setattr */
#define SCHED_FLAG_DREX_UI_BOOST    0x80
#define SCHED_FLAG_DREX_AUDIO_BOOST 0x100

/* Governor State Constants */
#define DREX_GOV_STATE_IDLE               0
#define DREX_GOV_STATE_INTERACTIVE_BOOST  1
#define DREX_GOV_STATE_SUSTAINED_LOAD     2
#define DREX_GOV_STATE_THERMAL_PROTECT    3
#define DREX_GOV_STATE_EMERGENCY_ROLLBACK 4

/* Registration request */
struct drex_boost_register_args {
	__s32 target_pid;         /* Task PID to boost (0 = current task) */
	__u32 task_type;          /* 1 = Compositor UI, 2 = Audio DSP, 3 = Game Render */
	__u32 target_fps;         /* 60, 120, 144, 240 */
	__u32 latency_budget_us;  /* Allowed latency budget in microseconds (e.g. 4166 for 240Hz) */
};

/* Governor telemetry struct */
struct drex_boost_telemetry {
	__u32 governor_state;
	__s32 clock_offset_mhz;
	__u32 target_fps;
	__u32 jitter_p99_us;
	__u64 total_boosted_frames;
	__u64 frame_drops_prevented;
	__u32 thermal_headroom_c;
	__u32 active_boosted_tasks;
};

/* IOCTL Commands */
#define DREX_BOOST_IOC_REGISTER_PID    _IOW(DREX_BOOST_IOC_MAGIC, 0x01, struct drex_boost_register_args)
#define DREX_BOOST_IOC_UNREGISTER_PID  _IOW(DREX_BOOST_IOC_MAGIC, 0x02, __s32)
#define DREX_BOOST_IOC_SET_TARGET_FPS  _IOW(DREX_BOOST_IOC_MAGIC, 0x03, __u32)
#define DREX_BOOST_IOC_GET_TELEMETRY   _IOR(DREX_BOOST_IOC_MAGIC, 0x04, struct drex_boost_telemetry)
#define DREX_BOOST_IOC_NOTIFY_INPUT    _IO(DREX_BOOST_IOC_MAGIC,  0x05)

#endif /* _UAPI_DAXOS_BOOST_H */
