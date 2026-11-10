---
description: Display the mimi-cyber category and tag indexes for security, AI governance and attacks
---

Show the user the mimi-cyber catalog indexes.

1. Read these files from `${CLAUDE_PLUGIN_ROOT}/skills/mimi-cyber/`:
   - `security_categories.md`, `security_tags.md`
   - `ai_categories.md`, `ai_tags.md`
   - `attack_categories.md`, `attack_tags.md`

2. If any is missing, or the user's YAML was changed after the indexes were built, run the update first:

   ```bash
   python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/mimi-cyber/resources/scripts/update_catalog.py" --check
   ```

   If it reports anything out of date, follow the update-meta-catalog command, then continue.

3. Display one table with a row per domain:

   | Domain | Categories | Tags |
   |---|---|---|
   | Security | ... | ... |
   | AI governance and security | ... | ... |
   | Attacks | ... | ... |

   List labels comma-separated in each cell, and end with one line giving the totals (number of categories and tags per domain).

4. If the user names a category or tag, also list the records that use it: the `audit_label` entries in `resources/scripts/checks.yml` and the `label` entries in `resources/scripts/actors.yml`.
