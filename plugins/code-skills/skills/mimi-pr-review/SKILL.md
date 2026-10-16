---
name: mimi-pr-review
description: Prepare and review a GitHub pull request end to end — check the branch is ready, run Anthropic's multi-agent code review, then summarise and fix the findings. Use when the user asks to "review my PR", "check this branch before I merge", "is this PR ready", or wants a pre-merge review of their changes.
---

# PR Review

This skill relies on the `code-review` plugin from `claude-plugins-official`, which `code-skills` installs as a dependency. It provides the `/code-review:code-review` command.

## Prerequisites

- The repository has a GitHub remote, and the current branch has an open pull request.
- The GitHub CLI is installed and authenticated (`gh auth status`). If it is not, tell the user to run `gh auth login` and stop.

## Steps

1. **Check the branch is ready**
   - Run `git status` and `git log --oneline origin/<base>..HEAD`; report uncommitted changes or unpushed commits.
   - Run the repository's own fast checks (lint, format, type-check, unit tests) when they exist, and report failures before reviewing.
2. **Run the review** — invoke `/code-review:code-review`. It launches specialised review agents and keeps only high-confidence findings.
3. **Summarise** the findings for the user, most severe first:
   - **[Severity] file:line** — the problem, and a concrete fix.
   - Say plainly when the review found nothing.
4. **Fix on request** — apply only the fixes the user approves, re-run the checks from step 1, then commit with a clear message.

## Rules

- Never push, merge, or post comments on the pull request unless the user asks.
- Treat review findings as claims to verify against the code, not as orders; drop any you cannot reproduce and say why.
