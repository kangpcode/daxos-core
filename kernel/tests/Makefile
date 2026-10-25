# SPDX-License-Identifier: GPL-2.0-only
# DAXOS Kernel Test Suite Makefile

CC ?= gcc
CFLAGS ?= -O2 -Wall -Wextra -pthread -I../include/uapi

TARGETS := test_ntsync test_sched_boost test_kernel_integrity

.PHONY: all clean test

all: $(TARGETS)

test_ntsync: test_ntsync.c
	$(CC) $(CFLAGS) -o $@ $<

test_sched_boost: test_sched_boost.c
	$(CC) $(CFLAGS) -o $@ $<

test_kernel_integrity: test_kernel_integrity.c
	$(CC) $(CFLAGS) -o $@ $<

test: all
	@echo "=== Running DAXOS Kernel Subsystem Verification Harness ==="
	@./test_ntsync
	@./test_sched_boost
	@./test_kernel_integrity
	@echo "[OK] All DAXOS kernel test suites passed successfully!"

clean:
	rm -f $(TARGETS) *.o
