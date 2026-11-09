# Claude API feature eligibility for HIPAA readiness

Snapshot of <https://platform.claude.com/docs/en/manage-claude/api-and-data-retention>, taken 2026-11-09. Always compare with the live page before an audit.

Under HIPAA readiness the API returns `400 invalid_request_error` for any "No" feature, unless the notes say it is accepted. Beta features are not covered unless listed as eligible.

| Feature | Signal in code | HIPAA | Notes |
|---|---|---|---|
| Messages API | `/v1/messages`, `messages.create` | Yes | |
| Token counting | `/v1/messages/count_tokens` | Yes | |
| 1M context window | | Yes | |
| Citations | `citations` | Yes | |
| Computer use tool | `computer` tool | Yes | Client-side |
| Bash tool | `bash` tool | Yes | Client-side |
| Text editor tool | `text_editor` tool | Yes | Client-side |
| Memory tool | `memory` tool | Yes | Client-side; your storage must be covered |
| Data residency | `inference_geo` | Yes | |
| Effort | `effort` | Yes | |
| Fast mode | `speed: "fast"` | Yes | |
| Thinking, adaptive thinking | `thinking` | Yes | |
| Mid-conversation system messages | `role: "system"` in messages | Yes | |
| PDF support | `document` blocks inline | Yes | Inline only, not via Files API |
| Prompt caching | `cache_control` | Yes | |
| Search results | `search_results` | Yes | |
| Structured outputs, strict tools | `output_format`, `strict: true` | Yes | No PHI in JSON schemas |
| Fine-grained tool streaming | | Yes | |
| Web search tool | `web_search` | Yes | Dynamic filtering is not eligible |
| Advisor tool | `advisor` | No | |
| Agent Skills | `/v1/skills`, `skills` | No | |
| Batch processing | `/v1/messages/batches` | No | |
| Browser use tool | `browser` toolset | No | Accepted by the API, but not covered |
| Cache diagnostics | `diagnostics` | No | |
| Code execution tool | `code_execution` | No | |
| Context editing | `context_management` | No | |
| Files API | `/v1/files`, `file_id` | No | |
| MCP connector | `mcp_servers` | No | |
| MCP tunnels | `/v1/tunnels` | No | |
| Message threads | `thread` | No | |
| Programmatic tool calling | `code_execution` with tool callers | No | |
| Threshold compaction | `context_management` | No | |
| Tool search tool | `tool_search` | No | |
| Web fetch tool | `web_fetch` | No | |
| Managed Agents | `/v1/agents`, `/v1/sessions`, `/v1/environments` | No | |
| User profiles | `/v1/user_profiles` | No | Usable, but never put PHI in profile data |
| OpenTelemetry export | `/v1/organizations/telemetry_destinations` | No | HIPAA organizations may export metadata |

## Platforms

- Covered: Claude API (`api.anthropic.com`); Claude in Microsoft Foundry with a BAA and the Azure HIPAA configuration.
- Not covered: Claude Console and playground, consumer plans, Claude Platform on AWS, Amazon Bedrock and Google Cloud (use the provider's own compliance docs), Claude Code, third-party integrations.

## Other rules

- Enablement is permanent and organization-wide; use a separate organization for non-HIPAA work.
- Flagged content or legal holds may be retained for up to 2 years regardless of arrangement.
- Covered Models (Fable 5, Fable 5.1, Mythos 5, Mythos 5.1) require 30-day retention.
