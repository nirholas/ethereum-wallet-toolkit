#!/bin/bash
# Run the eth_toolkit.py CLI test suite.
set -euo pipefail
cd "$(dirname "$0")"
python3 test_cli.py
