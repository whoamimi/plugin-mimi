---
description: Rebuild the cyber category and tag indexes (security, AI, attack) from the mimi-cyber YAML catalogs
---

Rebuild the six index files of the mimi-cyber skill from its YAML catalogs.

1. Run:

   ```bash
   python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/mimi-cyber/resources/scripts/update_catalog.py"
   ```

   It reads `resources/scripts/actors.yml`, `checks.yml`, `strategy.yml` and `attacks.yml`, and rewrites `security_categories.md`, `security_tags.md`, `ai_categories.md`, `ai_tags.md`, `attack_categories.md` and `attack_tags.md` as sorted bullet lists of unique labels.

2. If it prints any `problem:` lines, fix them in the YAML (wrong label format, a strategy missing from `strategy.yml`, an attack missing from `attacks.yml`, an invalid `domain` or `severity`) and run it again until it prints none.

3. Report in 2–3 lines: how many labels each index now has, which files changed, and any new categories or tags that look like near-duplicates of existing ones (for example `PROMPT_INJECTION` and `PROMPT_INJECTIONS`), so the user can merge them.

Never edit the index files by hand; change the YAML and re-run.
