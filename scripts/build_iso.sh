#!/bin/bash
# ==============================================================================
# DAXOS ISO BUILDER SHELL WRAPPER
# File: scripts/build_iso.sh
# ==============================================================================

set -euo pipefail
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${WORKSPACE_ROOT}"

chmod +x scripts/build_iso.py
python3 scripts/build_iso.py "$@"
