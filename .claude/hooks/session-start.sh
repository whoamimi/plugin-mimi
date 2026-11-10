#!/bin/bash
# Claude Code cloud sessions: install the tools scripts/check.sh uses and
# enable this repository's git hooks. Safe to run repeatedly.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

git config core.hooksPath .githooks

python3 -c "import yaml" 2>/dev/null || pip install -q pyyaml
command -v ruff >/dev/null 2>&1 || pip install -q ruff==0.16.8

missing=()
command -v shellcheck >/dev/null 2>&1 || missing+=(shellcheck)
command -v tree >/dev/null 2>&1 || missing+=(tree)
if [ "${#missing[@]}" -gt 0 ]; then
  apt-get update -qq && apt-get install -y -qq "${missing[@]}" >/dev/null
fi

# The version-bump check compares with origin/main; tags feed post-merge.
git fetch -q origin main --tags || echo "session-start: could not fetch origin/main" >&2

echo "session-start: git hooks enabled; check tools ready"
