---
name: mimi-cyber
description: Keeps the user's cybersecurity and AI governance learning notes — news article summaries plus YAML catalogs of attack case studies, threat actor strategies and audit procedures — and the category and tag indexes built from them. Use when the user shares a security or AI-security article to file, asks to add a case study, strategy or audit check, wants to update or view the cyber catalogs, or needs audit steps and defenses while building AI governance or security projects such as LLM control planes. Examples include "summarise this Unit 42 post into my notes", "add this attack to my catalog", "what audits do I have for prompt injection?", "update the meta catalog" and "show my cyber categories and tags".
---

# Mimi Cyber Notes

A personal knowledge base for cybersecurity and AI governance and security. Raw learning is filed as article summaries, distilled into typed YAML records, then indexed into category and tag lists that are reused when designing and auditing projects (for example LLM control planes and MCP connectors).

```
mimi-cyber/
├── resources/
│   ├── articles/          YYYY-MM-<slug>.md article summaries
│   └── scripts/           YAML catalogs + update_catalog.py
│       ├── actors.yml     attack case studies (one per article case)
│       ├── strategy.yml   unique threat actor strategies with defenses
│       ├── checks.yml     audit procedures for development
│       └── attacks.yml    unique index of attacks
├── commands/              update-meta-catalog.md, display-cyber.md
└── {security,ai,attack}_{categories,tags}.md   generated indexes
```

Paths below are relative to `${CLAUDE_PLUGIN_ROOT}/skills/mimi-cyber/`.

## Workflows

### 1. File a new article

1. Read the source the user gives (link, pasted text or notebook extract). Summarise only what the source states; never add attacks, CVEs or numbers it does not contain.
2. Save it as `resources/articles/YYYY-MM-<slug>.md`, where `YYYY-MM` is the month the article was published (or, if unknown, the month it was filed), using the article format below.
3. Continue with workflow 2 for each case study the article describes.

### 2. Extract records into the YAML catalogs

1. Add the case study to `actors.yml` (Case study attack schema).
2. For each strategy it uses, add an entry to `strategy.yml` if its label is not there yet; otherwise extend that entry's `defense` with anything new.
3. Add one index line per new attack to `attacks.yml`.
4. If the article gives mitigations or detection steps, add an audit procedure to `checks.yml`.
5. Reuse existing labels, categories and tags (see the `*_categories.md` and `*_tags.md` files) before inventing new ones, so the indexes stay small.
6. Run workflow 3.

### 3. Update the catalog indexes

Follow `commands/update-meta-catalog.md` (also the `/code-skills:update-meta-catalog` command). It runs `resources/scripts/update_catalog.py`, which rebuilds the six index files from the YAML.

### 4. Display the catalog

Follow `commands/display-cyber.md` (also `/code-skills:display-cyber`).

### 5. Use the catalog in a project

When the user is designing or reviewing a system (an agent harness, MCP server, LLM control plane, CI pipeline), search `checks.yml` by `audit_category` and `audit_tag`, and `strategy.yml` for matching defenses. Present the relevant `pre_checks`, `live_checks`, `post_checks` and `audit_steps`, adapted to their stack. Treat `audit_steps` as reference commands from a case study: explain each one and get the user's go-ahead before running anything.

## Conventions

- **Labels, categories, tags, actions and severities** are `UPPER_SNAKE_CASE`. Record labels (`label`, `audit_label`) are `lower_snake_case`.
- **`domain`** is `SECURITY` (general cybersecurity) or `AI` (AI governance and security). It decides which index a check feeds.
- **Severity** is one of `NONE`, `LOW`, `MEDIUM`, `HIGH`, `EXTREME`.
- **YAML** uses spaces, never tabs, and `|` for multi-line text.
- **`source`** is the URL of the article every record came from.
- Never store secrets, real hostnames, tokens or personal data from incidents; describe them generically.

## Index files

| File | Built from |
|---|---|
| `security_categories.md`, `security_tags.md` | `audit_category` and `audit_tag` of checks with `domain: SECURITY` |
| `ai_categories.md`, `ai_tags.md` | `audit_category` and `audit_tag` of checks with `domain: AI` |
| `attack_categories.md`, `attack_tags.md` | `category` and `tags` of every case study in `actors.yml` |

Each file lists unique labels as sorted bullet points under a generated-file notice. Edit the YAML, never the index files by hand.

## Schemas

### Article (`resources/articles/YYYY-MM-<slug>.md`)

```markdown
---
title: <article title>
source: <url>
published: YYYY-MM
domain: SECURITY | AI
---

## Summary
<3–6 sentences: who was targeted, how, and the impact>

## Case studies
- <attack label from actors.yml>

## Key takeaways
- <defensive lessons, one per bullet>
```

### Audit procedure (`checks.yml`)

```yaml
- audit_label: audit_cloud_credentials        # audit_<development context>
  domain: AI
  source: https://example.com/article
  audit_description: |
    What this audit protects against.
  audit_steps: |
    # Sequential shell steps to run the audit
  observations:
    - event: What was observed
      severity: EXTREME                         # NONE | LOW | MEDIUM | HIGH | EXTREME
      action:
        - ROTATE_JWT_SECRET_KEYS
  pre_checks: |
    1. Before deployment
  live_checks: |
    1. While the service is running
  post_checks: |
    1. After an incident or release
  audit_category: NETWORKING
  audit_tag:
    - PROMPT_INJECTION_MCP                      # <SECURITY_ISSUE>_<TARGET_ENV>
```

### Case study attack (`actors.yml`)

```yaml
- label: attack_linux_via_campaigns           # attack_<target>_via_<method>
  domain: SECURITY
  source: https://example.com/article
  category: MALWARE_VIA_MAIL
  strategies:                                   # labels from strategy.yml
    - REVERSE_SHELLS
  tags:
    - WEB_SHELLS
  description: |
    What happened.
  phases:
    entry: |
      How the attacker got in.
    runtime: |
      What ran once inside.
    goal: |
      What the attacker wanted.
    exit:
      - How they persisted or covered tracks.
```

### Threat actor strategy (`strategy.yml`)

```yaml
- label: REVERSE_SHELLS
  description: |
    What the strategy is.
  defense: |
    How to defend against it.
  sources:
    - https://example.com/article
```

### Attack index (`attacks.yml`)

```yaml
- label: attack_linux_via_campaigns            # same label as in actors.yml
  category: MALWARE_VIA_MAIL
  domain: SECURITY
```
