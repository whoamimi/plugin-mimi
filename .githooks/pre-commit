#!/usr/bin/env bash
# Regenerate generated files and stage them, block secrets and large files,
# then run the fast checks. Enable once per clone: git config core.hooksPath .githooks
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

regenerated=()

# mimi-cyber indexes, when its YAML catalogs are staged.
catalog=plugins/code-skills/skills/mimi-cyber
if git diff --cached --name-only | grep -q "^${catalog}/resources/scripts/.*\.yml$"; then
  if python3 -c "import yaml" 2>/dev/null; then
    python3 "${catalog}/resources/scripts/update_catalog.py" >/dev/null
    regenerated+=("${catalog}"/*_categories.md "${catalog}"/*_tags.md)
  else
    echo "pre-commit: PyYAML missing; mimi-cyber indexes not regenerated" >&2
  fi
fi

# README plugin table and directory tree.
python3 scripts/update-readme-plugins.py >/dev/null
if command -v tree >/dev/null 2>&1; then
  scripts/update-readme-tree.sh
else
  echo "pre-commit: tree CLI missing; README directory tree not regenerated" >&2
fi
regenerated+=(README.md)

# Stage regenerated files that changed.
for f in "${regenerated[@]}"; do
  if ! git diff --quiet -- "$f"; then
    git add -- "$f"
    echo "pre-commit: regenerated and staged $f"
  fi
done

# Secret and large-file checks, then scripts/check.sh (fast checks).
exec plugins/code-skills/skills/git-repository-setup/templates/pre-commit
