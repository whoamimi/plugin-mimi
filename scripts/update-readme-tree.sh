#!/usr/bin/env bash
# Regenerate the directory tree in README.md between the tree markers.
# Usage: scripts/update-readme-tree.sh   (requires the `tree` CLI)
set -euo pipefail

cd "$(dirname "$0")/.."

start='<!-- tree:start -->'
end='<!-- tree:end -->'

if ! grep -qF "$start" README.md || ! grep -qF "$end" README.md; then
  echo "README.md is missing the '$start' / '$end' markers" >&2
  exit 1
fi

tree_file=$(mktemp)
trap 'rm -f "$tree_file"' EXIT
{
  echo '```text'
  LC_ALL=C tree -a --noreport --charset=utf-8 -I '.git'
  echo '```'
} > "$tree_file"

awk -v start="$start" -v end="$end" -v tree_file="$tree_file" '
  $0 == start { print; while ((getline line < tree_file) > 0) print line; skip = 1; next }
  $0 == end   { skip = 0 }
  !skip
' README.md > README.md.tmp
mv README.md.tmp README.md
