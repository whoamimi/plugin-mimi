#!/usr/bin/env bash
# Regenerate the directory tree in README.md between the tree markers.
# Usage: scripts/update-readme-tree.sh [--check]   (requires the `tree` CLI)
# --check writes nothing and exits 1 if the tree is out of date.
set -euo pipefail

cd "$(dirname "$0")/.."

check=false
[ "${1:-}" = "--check" ] && check=true

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
  LC_ALL=C tree -a -d -L 3 --gitignore --noreport --charset=utf-8 -I '.git|.*'
  echo '```'
} > "$tree_file"

awk -v start="$start" -v end="$end" -v tree_file="$tree_file" '
  $0 == start { print; while ((getline line < tree_file) > 0) print line; skip = 1; next }
  $0 == end   { skip = 0 }
  !skip
' README.md > README.md.tmp

if [ "${check}" = true ]; then
  if cmp -s README.md README.md.tmp; then
    rm -f README.md.tmp
    exit 0
  fi
  rm -f README.md.tmp
  echo "README directory tree is out of date; run scripts/update-readme-tree.sh" >&2
  exit 1
fi
mv README.md.tmp README.md
