#!/usr/bin/env bash
# Run the repository's checks: the same ones the PR workflow runs.
# Usage: scripts/check.sh [--full] [--base REF]
#   default  fast checks (lint, catalog indexes, README), well under a second
#   --full   also strict plugin validation, ruff and shellcheck
#   --base   also require a version bump for every plugin changed since REF
# Output is shown only for failing checks. Locally, a check whose tool is not
# installed is skipped with a note; in CI (CI=true) a missing tool fails.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

full=false
base=""
while [ $# -gt 0 ]; do
  case "$1" in
    --full) full=true; shift ;;
    --base) base="${2:?--base needs a git ref}"; shift 2 ;;
    *) echo "usage: $0 [--full] [--base REF]" >&2; exit 2 ;;
  esac
done

failed=0
log=$(mktemp)
trap 'rm -f "$log"' EXIT

run() {
  local name="$1"
  shift
  if "$@" >"$log" 2>&1; then
    echo "ok    ${name}"
  else
    echo "FAIL  ${name}"
    sed 's/^/      /' "$log"
    failed=1
  fi
}

has() {
  if command -v "$1" >/dev/null 2>&1; then
    return 0
  fi
  if [ "${CI:-}" = "true" ]; then
    echo "FAIL  $2 ($1 is not installed)"
    failed=1
  else
    echo "skip  $2 ($1 is not installed)"
  fi
  return 1
}

lint_args=()
[ -n "$base" ] && lint_args=(--base "$base")
run "skill and manifest lint" python3 scripts/lint-plugins.py "${lint_args[@]}"

if python3 -c "import yaml" 2>/dev/null; then
  run "mimi-cyber catalog indexes" python3 plugins/code-skills/skills/mimi-cyber/resources/scripts/update_catalog.py --check
elif [ "${CI:-}" = "true" ]; then
  echo "FAIL  mimi-cyber catalog indexes (PyYAML is not installed)"; failed=1
else
  echo "skip  mimi-cyber catalog indexes (PyYAML is not installed)"
fi

run "README plugin table" python3 scripts/update-readme-plugins.py --check
if has tree "README directory tree"; then
  run "README directory tree" scripts/update-readme-tree.sh --check
fi

if [ "$full" = true ]; then
  if has claude "strict plugin validation"; then
    validate_all() {
      claude plugin validate --strict . || return 1
      local p
      for p in plugins/*/; do claude plugin validate --strict "$p" || return 1; done
    }
    run "strict plugin validation" validate_all
  fi
  if has ruff "ruff"; then
    run "ruff" ruff check --select E9,F --no-cache .
  fi
  if has shellcheck "shellcheck"; then
    run "shellcheck" shellcheck scripts/*.sh .githooks/* .claude/hooks/*.sh \
      plugins/code-skills/skills/git-repository-setup/templates/pre-commit \
      plugins/code-skills/skills/git-repository-setup/templates/commit-msg
  fi
fi

if [ "$failed" -ne 0 ]; then
  echo "Checks failed."
  exit 1
fi
echo "All checks passed."
