#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${1:-openclaw-mcp-agentic-lab}"
VISIBILITY="${2:-public}"

git init
git add .
git commit -m "Initial OpenClaw MCP agentic AI lab"

gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=origin --push
