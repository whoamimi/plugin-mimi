<p align="center">
  <img src="assets/logo.png" alt="Happiness Potion logo" width="200">
</p>

# Plug Mimi

Claude Plugin Skill to assist a female's life.

## Installation

```bash
claude plugin marketplace add whoamimi/plugin-mimi
claude plugin install <plugin-name>@plugin-mimi
```

`code-skills` depends on Anthropic's `code-review` plugin. Add Anthropic's marketplace once before installing it, so the dependency can be installed automatically:

```bash
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin install code-skills@plugin-mimi
```

## Directory Overview

<!-- tree:start -->
```text
.
├── .claude-plugin
│   └── marketplace.json
├── .github
│   └── workflows
│       └── pr-check-and-merge.yml
├── README.md
├── SECURITY.md
├── assets
│   └── logo.png
├── plugins
│   ├── code-skills
│   │   ├── .claude-plugin
│   │   │   └── plugin.json
│   │   ├── assets
│   │   │   └── icon.png
│   │   └── skills
│   │       └── mimi-pr-review
│   │           └── SKILL.md
│   ├── craft-skills
│   │   ├── .claude-plugin
│   │   │   └── plugin.json
│   │   ├── assets
│   │   │   └── icon.png
│   │   └── skills
│   │       └── mimi-sprite-studio
│   │           ├── SKILL.md
│   │           ├── references
│   │           │   ├── layered-animation.md
│   │           │   └── mascot-styles.md
│   │           └── scripts
│   │               ├── animate.py
│   │               ├── cutout.py
│   │               └── render_svg.py
│   ├── life-skills
│   │   ├── .claude-plugin
│   │   │   └── plugin.json
│   │   ├── assets
│   │   │   └── icon.png
│   │   └── skills
│   │       ├── check-gmail
│   │       │   └── SKILL.md
│   │       └── mimi-cbt
│   │           └── SKILL.md
│   ├── mimi-core
│   │   ├── .claude-plugin
│   │   │   └── plugin.json
│   │   ├── assets
│   │   │   └── icon.png
│   │   └── skills
│   │       ├── check-beehive
│   │       │   └── SKILL.md
│   │       ├── mimi-world
│   │       │   └── SKILL.md
│   │       └── write-readme
│   │           └── SKILL.md
│   └── soft-skills
│       ├── .claude-plugin
│       │   └── plugin.json
│       ├── assets
│       │   └── icon.png
│       └── skills
│           ├── mimi-edit
│           │   └── SKILL.md
│           ├── mimi-notes-summary
│           │   └── SKILL.md
│           ├── mimi-rephrase
│           │   └── SKILL.md
│           └── mimi-tutor
│               └── SKILL.md
└── scripts
    └── update-readme-tree.sh
```
<!-- tree:end -->
