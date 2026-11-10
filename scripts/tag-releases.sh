#!/usr/bin/env bash
# Tag each plugin's current version as <plugin>--v<version> on HEAD.
# This is the release-tag convention Claude Code resolves plugin dependency
# version ranges against. Existing tags are never moved; --push publishes
# every current release tag, so a run whose push failed can simply be repeated.
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

release_tags=()
new_tags=()
for manifest in plugins/*/.claude-plugin/plugin.json; do
  read -r name version < <(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["name"], d["version"])' "$manifest")
  tag="${name}--v${version}"
  release_tags+=("${tag}")
  if git rev-parse --quiet --verify "refs/tags/${tag}" >/dev/null; then
    echo "exists  ${tag}"
    continue
  fi
  git tag -a "${tag}" -m "${name} ${version}"
  new_tags+=("${tag}")
  echo "created ${tag}"
done

if [ "${push}" = true ]; then
  # Tags already on the remote at the same commit are left as they are; a tag
  # that points elsewhere on the remote makes the push fail rather than move it.
  git push origin "${release_tags[@]}"
elif [ "${#new_tags[@]}" -eq 0 ]; then
  echo "No new release tags."
else
  echo "Push with: $0 --push"
fi
