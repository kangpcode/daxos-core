// SPDX-License-Identifier: GPL-2.0-only
//! ============================================================================
//! DAXOS DXU HYBRID KERNEL - SAFE RUST IN-TREE CORE MODULE
//! File: kernel/rust/daxos_core.rs
//! Kernel Baseline: Linux 6.12+ LTS (CONFIG_RUST=y)
//! Purpose: Memory-safe Ring-0 primitives, zero-copy IPC ring buffer, and
//!          affine resource handling for user-space driver supervisor.
//! Copyright (C) 2026 DAXOS Operating System Core Team.
//! ============================================================================

#![cfg_attr(not(test), no_std)]

#[cfg(not(test))]
extern crate alloc;

#[cfg(not(test))]
use core::sync::atomic::{AtomicU32, AtomicU64, Ordering};
#[cfg(test)]
use std::sync::atomic::{AtomicU32, AtomicU64, Ordering};

pub const DAXOS_RING_BUFFER_MAGIC: u32 = 0x44415852; // "DAXR"
pub const DAXOS_RING_BUFFER_CAPACITY: usize = 4096;

/// Ring buffer header shared between kernel ring 0 and DreX-Driver ring 3.
#[repr(C, align(64))]
pub struct RingBufferHeader {
    pub magic: u32,
    pub version: u16,
    pub flags: u16,
    pub head: AtomicU32,
    pub tail: AtomicU32,
    pub total_messages: AtomicU64,
    pub dropped_messages: AtomicU64,
    pub capacity: u32,
    _reserved: [u8; 32],
}

impl RingBufferHeader {
    pub const fn new() -> Self {
        Self {
            magic: DAXOS_RING_BUFFER_MAGIC,
            version: 1,
            flags: 0,
            head: AtomicU32::new(0),
            tail: AtomicU32::new(0),
            total_messages: AtomicU64::new(0),
            dropped_messages: AtomicU64::new(0),
            capacity: DAXOS_RING_BUFFER_CAPACITY as u32,
            _reserved: [0u8; 32],
        }
    }

    #[inline(always)]
    pub fn is_valid(&self) -> bool {
        self.magic == DAXOS_RING_BUFFER_MAGIC && self.version == 1
    }
}

/// Zero-copy affine memory message packet
#[repr(C, align(32))]
#[derive(Clone, Copy)]
pub struct DaxosKernelPacket {
    pub sequence: u64,
    pub timestamp_ns: u64,
    pub channel_id: u32,
    pub payload_size: u32,
    pub payload_hash: [u8; 32],
}

impl DaxosKernelPacket {
    pub const fn empty() -> Self {
        Self {
            sequence: 0,
            timestamp_ns: 0,
            channel_id: 0,
            payload_size: 0,
            payload_hash: [0u8; 32],
        }
    }
}

/// Safe zero-copy ring-buffer in kernel memory
pub struct ZeroCopyRingBuffer {
    pub header: RingBufferHeader,
    pub packets: [DaxosKernelPacket; DAXOS_RING_BUFFER_CAPACITY],
}

impl ZeroCopyRingBuffer {
    pub const fn new() -> Self {
        Self {
            header: RingBufferHeader::new(),
            packets: [DaxosKernelPacket::empty(); DAXOS_RING_BUFFER_CAPACITY],
        }
    }

    /// Push packet from kernel to user-space supervisor without memory copying
    pub fn push(&mut self, packet: DaxosKernelPacket) -> Result<u64, &'static str> {
        let head = self.header.head.load(Ordering::Acquire) as usize;
        let tail = self.header.tail.load(Ordering::Acquire) as usize;

        let next_head = (head + 1) % DAXOS_RING_BUFFER_CAPACITY;
        if next_head == tail {
            self.header.dropped_messages.fetch_add(1, Ordering::Relaxed);
            return Err("Ring buffer overflow: driver supervisor congested");
        }

        self.packets[head] = packet;
        self.header.head.store(next_head as u32, Ordering::Release);
        let seq = self.header.total_messages.fetch_add(1, Ordering::Relaxed);
        Ok(seq)
    }

    /// Pop packet by driver supervisor
    pub fn pop(&mut self) -> Option<DaxosKernelPacket> {
        let head = self.header.head.load(Ordering::Acquire) as usize;
        let tail = self.header.tail.load(Ordering::Acquire) as usize;

        if head == tail {
            return None; // Buffer is empty
        }

        let packet = self.packets[tail];
        let next_tail = (tail + 1) % DAXOS_RING_BUFFER_CAPACITY;
        self.header.tail.store(next_tail as u32, Ordering::Release);
        Some(packet)
    }

    pub fn is_empty(&self) -> bool {
        self.header.head.load(Ordering::Acquire) == self.header.tail.load(Ordering::Acquire)
    }
}

// ----------------------------------------------------------------------------
// Linux 6.12 In-Kernel Rust Module Definition
// ----------------------------------------------------------------------------
#[cfg(feature = "kernel_module")]
mod linux_module {
    use kernel::prelude::*;

    module! {
        type: DaxosCoreModule,
        name: "daxos_core",
        author: "DAXOS Kernel Engineering Group <kernel-core@daxos.org>",
        description: "DAXOS DXU Hybrid Safe Rust In-Tree Core Module",
        license: "GPL",
    }

    struct DaxosCoreModule;

    impl kernel::Module for DaxosCoreModule {
        fn init(_name: &'static CStr, _module: &'static ThisModule) -> Result<Self> {
            pr_info!("daxos_core: Rust in-tree hybrid core module loaded successfully\n");
            Ok(DaxosCoreModule)
        }
    }

    impl Drop for DaxosCoreModule {
        fn drop(&mut self) {
            pr_info!("daxos_core: Rust hybrid core module unloaded\n");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ring_buffer_fifo() {
        let mut rb = ZeroCopyRingBuffer::new();
        assert!(rb.is_empty());
        assert!(rb.header.is_valid());

        let mut pkt = DaxosKernelPacket::empty();
        pkt.sequence = 1001;
        pkt.channel_id = 7;
        pkt.payload_size = 256;

        let res = rb.push(pkt);
        assert!(res.is_ok());
        assert!(!rb.is_empty());

        let popped = rb.pop().expect("Should pop packet");
        assert_eq!(popped.sequence, 1001);
        assert_eq!(popped.channel_id, 7);
        assert_eq!(popped.payload_size, 256);
        assert!(rb.is_empty());
    }
}
