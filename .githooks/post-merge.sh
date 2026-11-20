#!/usr/bin/env bash
# After pulling main, list plugin versions that have no release tag yet.
set -uo pipefail

cd "$(git rev-parse --show-toplevel)" || exit 0
[ "$(git branch --show-current)" = "main" ] || exit 0

missing=()
for manifest in plugins/*/.claude-plugin/plugin.json; do
  tag=$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["name"] + "--v" + d["version"])' "$manifest") || continue
  git rev-parse --quiet --verify "refs/tags/${tag}" >/dev/null || missing+=("$tag")
done

if [ "${#missing[@]}" -gt 0 ]; then
  echo "post-merge: untagged plugin versions: ${missing[*]}"
  echo "post-merge: fetch tags with 'git fetch --tags', then tag with 'scripts/tag-releases.sh --push'"
fi
