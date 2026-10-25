# SPDX-License-Identifier: GPL-2.0-only
# ==============================================================================
# DAXOS DXU HYBRID KERNEL - TOP-LEVEL MODULES BUILD SYSTEM
# File: kernel/modules/Makefile
# ==============================================================================

MODULE_DIRS := daxos_ntsync daxos_boost daxos_sec

.PHONY: all modules clean install help

all: modules

modules:
	@echo "=== Building DAXOS Kernel Modules ==="
	@for dir in $(MODULE_DIRS); do \
		echo "-> Building $$dir..."; \
		$(MAKE) -C $$dir || exit 1; \
	done
	@echo "[OK] All DAXOS kernel modules built successfully."

clean:
	@for dir in $(MODULE_DIRS); do \
		$(MAKE) -C $$dir clean || true; \
	done
	@rm -f *.o *.ko *.mod* Module.symvers modules.order

install:
	@echo "=== Installing DAXOS Kernel Modules to /lib/modules/$$(uname -r)/extra/daxos ==="
	@sudo mkdir -p /lib/modules/$$(uname -r)/extra/daxos
	@for dir in $(MODULE_DIRS); do \
		if [ -f $$dir/*.ko ]; then \
			sudo cp $$dir/*.ko /lib/modules/$$(uname -r)/extra/daxos/; \
		fi \
	done
	@sudo depmod -a
	@echo "[OK] DAXOS Kernel Modules installed."

help:
	@echo "DAXOS Kernel Modules Build Targets:"
	@echo "  make modules - Build all in-tree/out-of-tree DAXOS kernel modules"
	@echo "  make clean   - Clean intermediate artifacts"
	@echo "  make install - Install .ko modules to system driver tree"
