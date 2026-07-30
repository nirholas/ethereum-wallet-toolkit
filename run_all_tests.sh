#!/bin/bash
# Test script for all MCP servers.
set -uo pipefail
cd "$(dirname "$0")"

SERVERS=(
  ethereum-wallet-mcp
  signing-mcp-server
  keystore-mcp-server
  transaction-mcp-server
  validation-mcp-server
)

echo "======================================"
echo "Running all MCP server tests"
echo "======================================"

# Install every server into the active environment.
for server in "${SERVERS[@]}"; do
  python3 -m pip install -e "$server" > /dev/null 2>&1
done

status=0
index=1
for server in "${SERVERS[@]}"; do
  echo ""
  echo "=== $index. $(echo "$server" | tr '[:lower:]' '[:upper:]') TESTS ==="
  python3 -m pytest "$server/tests/" --tb=short || status=1
  index=$((index + 1))
done

echo ""
echo "======================================"
if [ "$status" -eq 0 ]; then
  echo "All test suites passed"
else
  echo "At least one test suite FAILED"
fi
echo "======================================"
exit "$status"
