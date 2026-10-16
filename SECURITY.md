# Security Policy

`plugin-mimi` is a personal Claude plugin marketplace. It is built and used mainly by its owner, [@whoamimi](https://github.com/whoamimi), and is public so the plugins can be installed with `claude plugin marketplace add whoamimi/plugin-mimi`. It is not a supported product, and fixes are made on a best-effort basis.

## Supported Versions

Only the latest commit on `main` is supported. Plugins are not released separately, so update to the latest `main` before reporting an issue.

| Version | Supported |
| ------- | --------- |
| `main` (latest) | :white_check_mark: |
| Older commits, forks and copies | :x: |

## Reporting a Vulnerability

Please **do not open a public issue** for a security problem.

1. Report it privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**.
2. Include the affected plugin or skill, the file and line if you know them, steps to reproduce, and the impact.
3. Expect an acknowledgement within **7 days**. As a personal project, there is no guaranteed fix time; confirmed issues are fixed on `main` as soon as practical, and declined reports get a short explanation.

Public issues are fine for non-security bugs and suggestions.

## Scope

**In scope**

- Skills that could make Claude take harmful or unexpected actions, such as running destructive commands, leaking data, or ignoring the user's confirmation.
- Bundled scripts (for example `craft-skills/skills/mimi-sprite-studio/scripts/`) that could run untrusted code or write outside their output folder.
- The GitHub Actions workflow in `.github/workflows/`, including the automatic merge and the push to `main`.
- Personal data or credentials accidentally committed to the repository.

**Out of scope**

- Claude, Claude Code and the Claude apps themselves: report those to [Anthropic](https://www.anthropic.com/responsible-disclosure-policy).
- Plugins from other marketplaces, such as `code-review` from `claude-plugins-official`, which `code-skills` depends on: report those to their maintainers.
- Issues that need the user to approve an action Claude asked about.
- Forks and modified copies.

## How this repository is kept safe

These rules apply to every change, including the owner's own.

### Never commit secrets or private details

The repository is public, so everything in it is public, including Git history.

- No API keys, tokens, passwords, cookies, or `.env` files.
- No IP addresses, hostnames, Wi-Fi names, device serial numbers or remote-access links. Skills such as `mimi-core:check-beehive` and `mimi-core:mimi-world` describe the home network and personal projects in general terms only; real values belong in local, uncommitted config.
- No email addresses, phone numbers, or real names of other people. `life-skills:check-gmail` must never include message contents or addresses in examples.
- `life-skills:mimi-cbt` must not contain personal health history. It is a self-help guide, not a substitute for professional care.

If a secret is committed, treat it as exposed: revoke or rotate it first, then remove it from history. Deleting it in a new commit is not enough.

### Skills

- Skills ask before destructive or outward-facing actions (pushing, merging, posting, deleting, sending email) and never bypass the user's permission settings.
- Instructions found in emails, web pages, files or tool output are treated as data, not as commands.
- Bundled scripts run locally, use only the standard library, Pillow and numpy (plus Chromium for SVG rendering), and make no network calls. Run them with `python3 -I` and write output to a scratch folder.

### Dependencies

- `code-skills` depends on `code-review` from Anthropic's `claude-plugins-official` marketplace. `marketplace.json` allows dependencies from that marketplace only (`allowCrossMarketplaceDependenciesOn`); adding another marketplace there requires a review of its plugins first.
- The workflow pins the Claude Code CLI and `ruff` to exact versions. Update them deliberately, not automatically.

### Automatic merge

Pull requests to `main` are merged without review once the `check` job passes (strict plugin validation, `scripts/lint-plugins.py`, `ruff`, `shellcheck` and the README tree check). To keep this safe:

- Only branches in this repository are auto-merged; pull requests from forks are checked but never merged automatically.
- Only the owner has write access. Adding a collaborator means anyone with that access can merge to `main`, so review this workflow first.
- The workflow uses the built-in `GITHUB_TOKEN` with the minimum permissions each job needs, and stores no other secrets.
- Recommended GitHub settings: enable **Private vulnerability reporting**, **Secret scanning** and **Push protection** under *Settings → Code security*.
