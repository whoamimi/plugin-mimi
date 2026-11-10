# Changelog

Each plugin is versioned on its own with [semantic versioning](https://semver.org): **major** for removed, renamed or moved skills, **minor** for new skills or features, **patch** for fixes and wording. Every released version is tagged `<plugin>--v<version>`.

## code-skills

### 2.1.0
- Added `python-like-mimi`, `react-like-mimi` and `react-native-like-mimi` coding style skills.
- Updated `backup-project`.

### 2.0.0
- **Breaking:** removed `mimi-pr-review` and `hipaa-readiness-audit`, and with them the dependency on Anthropic's `code-review` plugin.
- Added `git-repository-setup`: main branch, repository files, committed hooks, CI workflow templates, branch protection ruleset and release versioning.
- Moved `write-readme` and `mimi-cyber` (with the `update-meta-catalog` and `display-cyber` commands, now `/code-skills:…`) here from `mimi-core`.
- Added display name, homepage, repository and keywords.

### 1.1.0
- Added `hipaa-readiness-audit`, `depth-breakdown`, `get-started` and `backup-project`.

### 1.0.0
- `mimi-pr-review`, with Anthropic's `code-review` plugin as a dependency.

## craft-skills

### 2.0.1
- Reformatted the plugin manifest.

### 2.0.0
- **Breaking:** renamed `create-project-assets` to `create-brand-assets`, which now uses `mimi-sprite-studio` as its default design generator.
- `mimi-sprite-studio`: `render_svg.py` gained `--height` for non-square art such as banners.
- Added `get-astro-today` and `run-tarot-reading`.
- Rewrote descriptions with triggers and example requests.
- Added display name, homepage and repository metadata.

### 1.0.0
- `mimi-sprite-studio`.

## life-skills

### 2.0.0
- **Breaking:** renamed `daily-decision-maker` to `make-decisions`.
- **Breaking:** removed `mimi-cbt`.

### 1.1.0
- Added `daily-decision-maker`.
- Rewrote descriptions with triggers and example requests; `mimi-cbt` reframed as CBT-informed self-help.
- Added display name, homepage, repository and keywords.

### 1.0.0
- `check-gmail` and `mimi-cbt`.

## mimi-core

### 2.0.0
- **Breaking:** moved `write-readme` and `mimi-cyber` (with its commands) to `code-skills`.
- Added `audit-mimis-imac`.
- Rewrote descriptions with triggers and example requests.
- Added display name, homepage, repository and keywords.

### 1.0.0
- `check-beehive`, `mimi-world` and `write-readme`.

## soft-skills

### 2.0.0
- **Breaking:** replaced `mimi-define-word`, `mimi-english-tutor`, `mimi-paraphrase` and `mimi-paraphrase-advance` with `mimi-edit`, `mimi-rephrase` and `mimi-tutor`.
- Added `mimi-notes-summary`.
- Rewrote descriptions with triggers and example requests.
- Added display name, homepage, repository and keywords.

### 1.0.0
- `mimi-define-word`, `mimi-english-tutor`, `mimi-paraphrase` and `mimi-paraphrase-advance`.
