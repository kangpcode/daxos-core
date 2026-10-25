//! ============================================================================
//! DAXOS DreXSDK: AFFINE ZERO-COST MEMORY & LOCK-FREE RING BUFFER
//! File: crates/drex-sdk/src/memory.rs
//! Purpose: High-speed affine memory buffer & lock-free inter-thread ring buffer
//! Lead Architect: Dhafa Nazula Permadi (@kangpcode)
//! Strictly ZERO EMOJIS
//! ============================================================================

use std::sync::atomic::{AtomicUsize, Ordering};

/// Affine linear memory buffer ensuring single-consumer zero-copy transfer
pub struct AffineBuffer<T> {
    data: Vec<T>,
    consumed: bool,
}

impl<T> AffineBuffer<T> {
    pub fn new(capacity: usize) -> Self {
        Self {
            data: Vec::with_capacity(capacity),
            consumed: false,
        }
    }

    pub fn push(&mut self, item: T) -> Result<(), &'static str> {
        if self.consumed {
            return Err("AffineBuffer has already been consumed and invalidated");
        }
        self.data.push(item);
        Ok(())
    }

    /// Consume the buffer linearly. Once consumed, the buffer cannot be used again.
    pub fn consume_linearly(mut self) -> Vec<T> {
        self.consumed = true;
        std::mem::take(&mut self.data)
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }
}

/// Lock-free Single-Producer Single-Consumer (SPSC) Ring Buffer
/// Designed for 5.8 ms audio DSP buffers and 120Hz/240Hz frame telemetry
pub struct ZeroCopyRingBuffer<T: Copy + Default, const CAPACITY: usize> {
    buffer: [T; CAPACITY],
    head: AtomicUsize,
    tail: AtomicUsize,
}

impl<T: Copy + Default, const CAPACITY: usize> ZeroCopyRingBuffer<T, CAPACITY> {
    pub fn new() -> Self {
        Self {
            buffer: [T::default(); CAPACITY],
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        }
    }

    pub fn push(&mut self, item: T) -> bool {
        let head = self.head.load(Ordering::Relaxed);
        let tail = self.tail.load(Ordering::Acquire);

        let next_head = (head + 1) % CAPACITY;
        if next_head == tail {
            return false; // Buffer full
        }

        self.buffer[head] = item;
        self.head.store(next_head, Ordering::Release);
        true
    }

    pub fn pop(&mut self) -> Option<T> {
        let tail = self.tail.load(Ordering::Relaxed);
        let head = self.head.load(Ordering::Acquire);

        if tail == head {
            return None; // Buffer empty
        }

        let item = self.buffer[tail];
        self.tail.store((tail + 1) % CAPACITY, Ordering::Release);
        Some(item)
    }

    pub fn available(&self) -> usize {
        let head = self.head.load(Ordering::Relaxed);
        let tail = self.tail.load(Ordering::Relaxed);
        if head >= tail {
            head - tail
        } else {
            CAPACITY - (tail - head)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_affine_buffer_lifecycle() {
        let mut buf = AffineBuffer::new(4);
        assert!(buf.push(10).is_ok());
        assert!(buf.push(20).is_ok());
        assert_eq!(buf.len(), 2);

        let consumed = buf.consume_linearly();
        assert_eq!(consumed, vec![10, 20]);
    }

    #[test]
    fn test_zero_copy_ring_buffer() {
        let mut ring: ZeroCopyRingBuffer<f32, 8> = ZeroCopyRingBuffer::new();
        assert!(ring.push(0.5));
        assert!(ring.push(1.0));
        assert_eq!(ring.available(), 2);

        assert_eq!(ring.pop(), Some(0.5));
        assert_eq!(ring.pop(), Some(1.0));
        assert_eq!(ring.pop(), None);
    }
}
