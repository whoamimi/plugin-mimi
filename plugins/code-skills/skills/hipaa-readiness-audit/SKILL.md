---
name: hipaa-readiness-audit
description: Audits a codebase that calls the Claude API for HIPAA readiness gaps — features the API blocks for HIPAA-enabled organizations, features accepted but not covered, PHI in places the BAA does not protect, and unsupported platforms or models — then reports findings by severity with fixes. Use when the user handles protected health information with Claude, has signed or plans to sign Anthropic's BAA, or asks whether their Claude integration is HIPAA-ready. Examples include "audit this repo for HIPAA readiness", "is my Claude integration HIPAA compliant?", "check my API calls before we enable HIPAA" and "why does the API return a HIPAA 400 error?".
---

# HIPAA Readiness Audit

Audit how a codebase uses the Claude API against Anthropic's HIPAA readiness rules, then report gaps with concrete fixes. This is a technical aid, not legal advice: the user's signed BAA and Anthropic's HIPAA Implementation Guide are the source of truth.

Source page: <https://platform.claude.com/docs/en/manage-claude/api-and-data-retention>. Feature eligibility changes over time, so fetch that page at the start of every audit and compare it with [references/feature-eligibility.md](references/feature-eligibility.md). If they differ, trust the live page, tell the user what changed, and offer to update the reference file.

Never send real PHI to any tool, search or external service during the audit. Report the location of suspected PHI, never its value.

## Steps

1. **Confirm scope**: ask which repository or directories to audit, if not obvious, and whether the organization already has HIPAA readiness enabled. Note that enablement is permanent and organization-wide.
2. **Run the scanner** (stdlib only):

   ```bash
   python3 scripts/scan_hipaa.py <repo-path> --json findings.json
   ```

   It flags API features, endpoints, platforms and models by pattern. Treat every hit as a lead to verify, not a confirmed finding.
3. **Verify each hit** by reading the surrounding code. Drop false positives (comments, tests of non-HIPAA paths, unrelated `files` variables) and say why.
4. **Work through the checklist** below, including the manual checks the scanner cannot do.
5. **Report** most severe first, using this format for each finding:
   - **[Severity] file:line** — the problem, which rule it breaks, and a concrete fix.

   Severities:
   - **Blocker**: the API returns `400` for HIPAA organizations (a "No" feature in the reference table).
   - **Gap**: accepted by the API but outside HIPAA coverage, or PHI in an unprotected field.
   - **Check**: needs a human or account-level confirmation that code cannot show.

   End with a short summary table of counts per severity, and say plainly when nothing was found.
6. **Fix on request**: apply only fixes the user approves, then re-run the scanner.

## Checklist

### 1. Organization and platform

- BAA signed and HIPAA readiness enabled for the organization (Check).
- HIPAA and non-HIPAA workloads use separate organizations and API keys (Check).
- Calls go to `api.anthropic.com` or Claude in Microsoft Foundry with the Azure HIPAA configuration. Flag Claude Platform on AWS, Amazon Bedrock, Google Cloud, Console or playground usage, and Claude Code processing PHI (Gap).

### 2. Blocked features

Every feature marked "No" for HIPAA in the reference table is a Blocker, unless its row says the API accepts it. Common ones: code execution, programmatic tool calling, batch processing, Files API, MCP connector and tunnels, Agent Skills, Managed Agents, message threads, advisor tool, tool search, web fetch, context editing, threshold compaction, cache diagnostics, user profiles with PHI, and dynamic filtering on web search or fetch.

### 3. Accepted but not covered

- Browser use tool: not blocked, but outside HIPAA readiness (Gap).
- Beta features or `anthropic-beta` headers not listed as eligible (Gap).
- Third-party tools, connectors or webhooks that receive message content (Gap).

### 4. PHI placement

- JSON schemas for structured outputs and `strict: true` tools must contain no PHI in property names, `enum`, `const` or `pattern` values (Gap).
- PDFs and images go inline in message content, not through the Files API (Blocker if Files API).
- No PHI in file names, request metadata, `metadata.user_id`, workspace names, user profiles, billing data or support tickets (Gap).

### 5. Logging and telemetry

- Application logs, error trackers (Sentry and similar), caches and analytics must not record prompts or responses unless that store is itself HIPAA-covered (Gap).
- OpenTelemetry export: HIPAA organizations may export metadata only; confirm the destination's own controls (Check).

### 6. Error handling

- Code handles `400 invalid_request_error` whose message mentions HIPAA by surfacing the listed features, not by retrying the same payload (Gap).

### 7. Models

- Covered Models (Claude Fable 5, Fable 5.1, Mythos 5, Mythos 5.1) require 30-day retention; flag them so the user can confirm this is acceptable under their BAA (Check).

## Rules

- Never commit, push or open pull requests unless the user asks.
- Do not mark anything compliant; say "no issues found for this check" instead.
- Keep PHI values out of the report, logs and commit messages.
