---
name: git-repository-setup
description: Sets up a project's git repository with best practices — a main default branch, .gitignore and .gitattributes, committed git hooks (secret and large-file checks, conventional commit messages), GitHub Actions CI, branch protection on main, and semantic-version release tags with a changelog — inspecting what already exists and asking before any change to GitHub. Use when the user wants to set up, harden or tidy a git repository, add hooks or CI, protect main, or start versioning releases. Examples include "set up git properly for this project", "add pre-commit hooks", "create a CI workflow", "protect my main branch", "rename master to main" and "how should I tag releases?".
---

# Git Repository Setup

Turn a project folder into a well-configured repository, one step at a time. Templates are in `${CLAUDE_PLUGIN_ROOT}/skills/git-repository-setup/templates/`.

Related skills in this plugin: `get-started` scaffolds a new local project, and `backup-project` checks GitHub access and makes the first push. Use `backup-project` when the repository has no GitHub remote yet.

## Rules

- **Inspect before changing.** Never overwrite an existing file; show the difference and merge.
- **Local changes** (files, hooks, git config inside the repo): explain each one, then make it.
- **Anything outside the folder** (pushing, renaming the remote default branch, repository settings, branch protection, global git config): show the exact command and run it only after the user says yes.
- Never commit secrets. If the checks below find any, stop and help the user remove and rotate them first.

## Steps

Copy this checklist into your reply and tick items off as you go:

```
- [ ] 1. Inspect the repository
- [ ] 2. main as the default branch
- [ ] 3. Repository files
- [ ] 4. Git hooks
- [ ] 5. CI workflow
- [ ] 6. Protect main on GitHub
- [ ] 7. Versioning and releases
- [ ] 8. Verify
```

### 1. Inspect the repository

```bash
git rev-parse --is-inside-work-tree 2>/dev/null || echo "not a repository"
git branch --show-current; git remote -v; git config --get core.hooksPath
ls -a; ls .github/workflows .githooks 2>/dev/null
gh repo view --json defaultBranchRef,visibility 2>/dev/null
```

Report what exists and ask which language or stack the project uses (for the `.gitignore` and CI templates). Skip steps that are already done well.

### 2. main as the default branch

- **No repository yet:** `git init -b main`.
- **Local branch is `master`:** `git branch -m master main`.
- **Remote default is `master`** (ask first): `git push -u origin main`, then `gh repo edit --default-branch main`, then, once nothing depends on it, `git push origin --delete master`.
- **New repositories everywhere** (global config; ask first): `git config --global init.defaultBranch main`.

### 3. Repository files

| File | How |
|---|---|
| `.gitignore` | Start from GitHub's template for the stack: `gh api /gitignore/templates/Python --jq .source` (or `Node`, `Go`, `C++`). Add `.env`, editor folders and OS files such as `.DS_Store`. |
| `.gitattributes` | Copy `templates/gitattributes` to `.gitattributes`: consistent LF line endings and binary handling. |
| `README.md` | If missing, write one (the `write-readme` skill in this plugin has a template). |
| `LICENSE` | Ask which licence the user wants; never choose for them. `gh api /licenses/mit --jq .body` fetches the text. |
| `SECURITY.md` | For public repositories: how to report a vulnerability privately. |
| `.github/pull_request_template.md` | Copy `templates/pull_request_template.md`. |
| `.github/dependabot.yml` | Copy `templates/dependabot.yml` and keep the ecosystems the project uses. |

Before the first commit, check nothing sensitive or huge is staged: `git status --short` and `git diff --cached --stat`.

### 4. Git hooks

Keep hooks in the repository so every clone gets them:

```bash
mkdir -p .githooks
cp "${CLAUDE_PLUGIN_ROOT}/skills/git-repository-setup/templates/pre-commit" .githooks/pre-commit
cp "${CLAUDE_PLUGIN_ROOT}/skills/git-repository-setup/templates/commit-msg" .githooks/commit-msg
chmod +x .githooks/*
git config core.hooksPath .githooks
```

- `pre-commit` blocks staged files that look like secrets (private keys, `.env`, common token formats) and files over 5 MB, then runs the project's fast checks if a `scripts/check.sh` exists.
- `commit-msg` enforces [Conventional Commits](https://www.conventionalcommits.org) (`feat:`, `fix:`, `docs:` and so on), which makes changelogs and version bumps easy to derive.
- Tell the user that each clone must run `git config core.hooksPath .githooks` once, and add that line to the README's setup section. For Python projects, the [pre-commit](https://pre-commit.com) framework is a good alternative.

### 5. CI workflow

Copy the closest template to `.github/workflows/ci.yml`: `templates/ci-python.yml` or `templates/ci-node.yml`. Adapt the install, lint and test commands to the project, and run them locally first so the first CI run passes. The templates follow GitHub Actions good practice: they run on pull requests and pushes to `main`, use least-privilege `permissions: contents: read`, cancel superseded runs with `concurrency`, and set a job timeout.

### 6. Protect main on GitHub

Ask before running; this changes repository settings. Show the user `templates/ruleset-main.json`, which requires pull requests and the CI check, blocks force pushes and deletion of `main`, and requires a linear history. Then create it as a ruleset:

```bash
gh api repos/{owner}/{repo}/rulesets --method POST --input "${CLAUDE_PLUGIN_ROOT}/skills/git-repository-setup/templates/ruleset-main.json"
```

Set `required_status_checks` in the file to the CI job's name (`test` in the templates). Also suggest, under **Settings → Code security**, enabling secret scanning and push protection, and under **Settings → General**, "Automatically delete head branches".

Branch naming: short-lived branches off `main`, named `feat/<topic>`, `fix/<topic>` or `docs/<topic>`, merged by pull request and then deleted.

### 7. Versioning and releases

- Use [semantic versioning](https://semver.org): **major** for breaking changes, **minor** for new features, **patch** for fixes.
- Keep a `CHANGELOG.md` with one section per version, newest first.
- Tag each release on `main` with an annotated tag, never moving an existing one: `git tag -a v1.2.0 -m "v1.2.0"`, then (ask first) `git push origin v1.2.0` and `gh release create v1.2.0 --notes-from-tag` or `--generate-notes`.
- In a repository that holds several packages or Claude plugins, prefix tags with the package name, such as `my-plugin--v1.2.0`.

### 8. Verify

```bash
git config core.hooksPath                         # .githooks
msg=$(mktemp); printf 'not a conventional message\n' > "$msg"; .githooks/commit-msg "$msg"  # should fail
git log --oneline -1; git status --short
```

Finish with a short table: each step as done, skipped (already fine) or left for the user, with the reason.
