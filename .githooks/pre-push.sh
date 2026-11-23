#!/usr/bin/env bash
# Run the full checks, including the version-bump rule, before anything leaves
# this machine. Skip once with: git push --no-verify
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

base=origin/main
if ! git rev-parse --quiet --verify "$base" >/dev/null; then
  echo "pre-push: $base not found locally; run 'git fetch origin main' for the version-bump check" >&2
  exec scripts/check.sh --full
fi
exec scripts/check.sh --full --base "$base"
