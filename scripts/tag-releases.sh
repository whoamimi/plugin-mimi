#!/usr/bin/env bash
# Tag each plugin's current version as <plugin>--v<version> on HEAD.
# This is the release-tag convention Claude Code resolves plugin dependency
# version ranges against. Existing tags are never moved.
# Usage: scripts/tag-releases.sh [--push]
set -euo pipefail

cd "$(dirname "$0")/.."

push=false
if [ "${1:-}" = "--push" ]; then
  push=true
elif [ -n "${1:-}" ]; then
  echo "usage: $0 [--push]" >&2
  exit 2
fi

new_tags=()
for manifest in plugins/*/.claude-plugin/plugin.json; do
  read -r name version < <(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["name"], d["version"])' "$manifest")
  tag="${name}--v${version}"
  if git rev-parse --quiet --verify "refs/tags/${tag}" >/dev/null; then
    echo "exists  ${tag}"
    continue
  fi
  git tag -a "${tag}" -m "${name} ${version}"
  new_tags+=("${tag}")
  echo "created ${tag}"
done

if [ "${#new_tags[@]}" -eq 0 ]; then
  echo "No new release tags."
elif [ "${push}" = true ]; then
  git push origin "${new_tags[@]}"
else
  echo "Push with: git push origin ${new_tags[*]}"
fi
