#!/usr/bin/env python3
"""Scan a codebase for Claude API usage that matters for HIPAA readiness.

Pattern-based and deliberately noisy: every hit is a lead to verify by
reading the code, not a confirmed finding. Findings record only file, line
and rule, never source text, so suspected PHI is not copied. Stdlib only.

Usage:
  python3 scan_hipaa.py <path> [--json findings.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist",
    "build", ".next", ".ruff_cache", ".pytest_cache", ".mypy_cache", "coverage",
}
SCAN_SUFFIXES = {
    ".py", ".ipynb", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go",
    ".java", ".kt", ".rb", ".php", ".cs", ".rs", ".sh", ".json", ".yaml",
    ".yml", ".toml", ".env", ".tf",
}
MAX_BYTES = 2_000_000

# (severity, id, description, regex)
RULES = [
    # Blockers: the API returns 400 for HIPAA-enabled organizations.
    ("Blocker", "code-execution", "Code execution / programmatic tool calling", r"code_execution"),
    ("Blocker", "batch", "Message Batches API", r"/v1/messages/batches|messages\.batches"),
    ("Blocker", "files-api", "Files API", r"/v1/files|\.files\.(upload|create|list|retrieve|delete)|[\"']file_id[\"']|\bfile_id\s*="),
    ("Blocker", "mcp-connector", "MCP connector", r"mcp_servers"),
    ("Blocker", "mcp-tunnels", "MCP tunnels", r"/v1/tunnels"),
    ("Blocker", "agent-skills", "Agent Skills", r"/v1/skills|\.skills\.(create|list|retrieve)|[\"']skills[\"']\s*:"),
    ("Blocker", "managed-agents", "Managed Agents", r"/v1/(agents|sessions|environments)\b|\.beta\.(agents|sessions|environments)\."),
    ("Blocker", "message-threads", "Message threads", r"[\"']thread[\"']\s*:|\bthread\s*=\s*\{"),
    ("Blocker", "advisor", "Advisor tool", r"[\"']advisor[\"']|advisor_20\d+"),
    ("Blocker", "tool-search", "Tool search tool", r"tool_search"),
    ("Blocker", "web-fetch", "Web fetch tool", r"web_fetch"),
    ("Blocker", "context-management", "Context editing / threshold compaction", r"context_management"),
    ("Blocker", "cache-diagnostics", "Cache diagnostics", r"[\"']diagnostics[\"']\s*:"),
    ("Blocker", "user-profiles", "User profiles API (no PHI allowed)", r"/v1/user_profiles|user_profiles\."),
    # Gaps: accepted by the API or not blocked, but outside HIPAA coverage.
    ("Gap", "browser-tool", "Browser use tool (accepted, not covered)", r"browser_20\d+|[\"']type[\"']\s*:\s*[\"']browser"),
    ("Gap", "beta-header", "Beta feature header (check eligibility)", r"anthropic-beta|betas\s*=|\.beta\."),
    ("Gap", "dynamic-filtering", "Dynamic filtering on web search/fetch", r"dynamic_filter"),
    ("Gap", "structured-schema", "JSON schema for structured outputs / strict tools (no PHI in schema)", r"output_format|output_config|[\"']strict[\"']\s*:\s*true|strict\s*=\s*True"),
    ("Gap", "metadata", "Request metadata (no PHI in metadata.user_id)", r"[\"']user_id[\"']\s*:|metadata\s*=\s*\{"),
    ("Gap", "platform-bedrock", "Amazon Bedrock (provider handles compliance)", r"AnthropicBedrock|bedrock-runtime|anthropic\.claude"),
    ("Gap", "platform-vertex", "Google Cloud (provider handles compliance)", r"AnthropicVertex|aiplatform\.googleapis|vertex_?ai"),
    ("Gap", "platform-aws", "Claude Platform on AWS (HIPAA not available)", r"Claude Platform on AWS|claude-platform-aws"),
    ("Gap", "prompt-logging", "Possible logging of prompts or responses", r"(log(ger)?|print|console\.log|sentry)\S*\(.*\b(messages|prompt|response|completion|content)\b"),
    # Checks: need a human or account-level confirmation.
    ("Check", "covered-model", "Covered Model (30-day retention)", r"claude-(fable|mythos)-5"),
    ("Check", "otel", "OpenTelemetry export (metadata only)", r"telemetry_destinations|opentelemetry"),
    ("Check", "hipaa-error", "HIPAA error handling present", r"HIPAA-regulated|hipaa"),
]
COMPILED = [(sev, rid, desc, re.compile(pat, re.I)) for sev, rid, desc, pat in RULES]
ORDER = {"Blocker": 0, "Gap": 1, "Check": 2}


def iter_files(root):
    for path in root.rglob("*"):
        # Only directories beneath the audit root are excluded, so an ancestor
        # such as /workspace/build cannot suppress the whole scan.
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and (path.suffix.lower() in SCAN_SUFFIXES or path.name.startswith(".env")):
            try:
                if path.stat().st_size <= MAX_BYTES:
                    yield path
            except OSError:
                continue


def scan(root):
    findings = []
    for path in iter_files(root):
        try:
            lines = path.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            for sev, rid, desc, regex in COMPILED:
                if regex.search(line):
                    findings.append({
                        "severity": sev,
                        "rule": rid,
                        "description": desc,
                        "file": path.relative_to(root).as_posix(),
                        "line": lineno,
                        # No source text is copied: matched lines may hold PHI.
                    })
    findings.sort(key=lambda f: (ORDER[f["severity"]], f["rule"], f["file"], f["line"]))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", type=Path, help="write findings to this JSON file")
    args = parser.parse_args()
    root = args.path.resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    findings = scan(root)
    for f in findings:
        print(f"[{f['severity']}] {f['file']}:{f['line']} {f['rule']} - {f['description']}")
    counts = {sev: sum(f["severity"] == sev for f in findings) for sev in ORDER}
    print("Summary: " + ", ".join(f"{sev} {n}" for sev, n in counts.items()))
    if args.json:
        args.json.write_text(json.dumps({"root": str(root), "counts": counts, "findings": findings}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
