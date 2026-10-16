#!/usr/bin/env python3
"""Lint the marketplace, plugin manifests and skills against Anthropic's
plugin and skill authoring guidance.

Sources:
  https://code.claude.com/docs/en/plugins-reference
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Usage: python3 scripts/lint-plugins.py   (from anywhere; stdlib only)
Exits 1 when any error is found. Warnings are printed but do not fail.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Limits from the skill authoring best practices.
NAME_MAX = 64
DESCRIPTION_MAX = 1024
BODY_MAX_LINES = 500
REFERENCE_TOC_LINES = 100
RESERVED_WORDS = ("anthropic", "claude")

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
XML_TAG = re.compile(r"<\/?[A-Za-z][^>]*>")
FIRST_OR_SECOND_PERSON = re.compile(r"^\s*(I|I'm|I can|I will|You|You can|We)\b")
FENCED_BLOCK = re.compile(r"^```.*?^```", re.S | re.M)
MD_LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
JUNK_FILES = (".DS_Store", "Thumbs.db")

errors, warnings = [], []


def rel(path):
    return path.relative_to(ROOT).as_posix()


def error(path, msg):
    errors.append(f"{rel(path)}: {msg}")


def warn(path, msg):
    warnings.append(f"{rel(path)}: {msg}")


def load_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        error(path, f"invalid JSON ({exc})")
        return None


def parse_frontmatter(path):
    """Return (fields, body_lines) for a SKILL.md, or (None, None) if it has no frontmatter."""
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, None
    fields, key = {}, None
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            fields[key] = "" if value in (">", "|", ">-", "|-") else value.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, lines[end + 1:]


def check_local_links(path, text, allow_md_links):
    text = FENCED_BLOCK.sub("", text)  # templates and examples inside code fences are not real links
    for target in MD_LINK.findall(text):
        if re.match(r"^[a-z]+:", target):
            continue
        if "\\" in target:
            error(path, f"link uses a Windows-style path: {target}")
            continue
        if not (path.parent / target).exists():
            warn(path, f"link target not found (fine if it is template text): {target}")
        elif not allow_md_links and target.endswith(".md"):
            warn(path, f"nested reference to {target}; keep references one level deep from SKILL.md")


def check_skill(skill_md):
    fields, body = parse_frontmatter(skill_md)
    if fields is None:
        error(skill_md, "missing YAML frontmatter")
        return
    folder = skill_md.parent.name
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        error(skill_md, "frontmatter is missing 'name'")
    else:
        if len(name) > NAME_MAX:
            error(skill_md, f"name is longer than {NAME_MAX} characters")
        if not KEBAB.match(name):
            error(skill_md, f"name '{name}' must be lowercase letters, numbers and hyphens")
        if any(word in name.lower() for word in RESERVED_WORDS):
            error(skill_md, f"name '{name}' contains a reserved word {RESERVED_WORDS}")
        if name != folder:
            error(skill_md, f"name '{name}' does not match its folder '{folder}'")

    if not description:
        error(skill_md, "frontmatter is missing 'description'")
    else:
        if len(description) > DESCRIPTION_MAX:
            error(skill_md, f"description is {len(description)} characters (max {DESCRIPTION_MAX})")
        if XML_TAG.search(description):
            error(skill_md, "description contains an XML tag")
        if FIRST_OR_SECOND_PERSON.match(description):
            warn(skill_md, "description should be written in the third person")
        if not re.search(r"\buse (when|for|this|whenever)\b", description, re.I):
            warn(skill_md, "description should say when to use the skill ('Use when ...')")

    if len(body) > BODY_MAX_LINES:
        error(skill_md, f"body is {len(body)} lines (keep it under {BODY_MAX_LINES})")
    check_local_links(skill_md, "\n".join(body), allow_md_links=True)

    for ref in skill_md.parent.rglob("*.md"):
        if ref == skill_md:
            continue
        text = ref.read_text()
        check_local_links(ref, text, allow_md_links=False)
        if len(text.splitlines()) > REFERENCE_TOC_LINES and "## Contents" not in text:
            warn(ref, f"reference is over {REFERENCE_TOC_LINES} lines; add a '## Contents' section")


def check_plugin(plugin_dir, entry):
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.exists():
        error(plugin_dir, "missing .claude-plugin/plugin.json")
        return
    manifest = load_json(manifest_path)
    if manifest is None:
        return

    name = manifest.get("name", "")
    if not KEBAB.match(name):
        error(manifest_path, f"plugin name '{name}' must be kebab-case")
    if name != entry.get("name"):
        error(manifest_path, f"name '{name}' differs from its marketplace entry '{entry.get('name')}'")
    if name != plugin_dir.name:
        warn(manifest_path, f"name '{name}' differs from its folder '{plugin_dir.name}'")
    for field in ("version", "description", "author"):
        if not manifest.get(field):
            error(manifest_path, f"missing '{field}'")
    if entry.get("version") and manifest.get("version") != entry.get("version"):
        error(manifest_path, f"version {manifest.get('version')} differs from marketplace entry {entry.get('version')}")
    icon = manifest.get("icon")
    if icon and not (plugin_dir / icon).is_file():
        error(manifest_path, f"icon not found: {icon}")

    if (plugin_dir / "CLAUDE.md").exists():
        error(plugin_dir / "CLAUDE.md", "a plugin-root CLAUDE.md is not loaded; move its instructions into a skill")
    for stray in plugin_dir.rglob("SKILL.md"):
        if stray.parent.parent.name != "skills":
            error(stray, "SKILL.md must live at skills/<skill-name>/SKILL.md")

    skills = sorted((plugin_dir / "skills").glob("*/SKILL.md"))
    if not skills and not manifest.get("dependencies"):
        warn(plugin_dir, "plugin has no skills and no dependencies")
    for skill_md in skills:
        check_skill(skill_md)


def main():
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = load_json(marketplace_path)
    if marketplace is None:
        return finish()

    listed = set()
    for entry in marketplace.get("plugins", []):
        source = entry.get("source")
        if not isinstance(source, str):
            continue
        plugin_dir = (ROOT / source).resolve()
        listed.add(plugin_dir)
        if not plugin_dir.is_dir():
            error(marketplace_path, f"source for '{entry.get('name')}' not found: {source}")
            continue
        check_plugin(plugin_dir, entry)

    for plugin_dir in sorted((ROOT / "plugins").iterdir()):
        if plugin_dir.is_dir() and plugin_dir.resolve() not in listed:
            error(plugin_dir, "plugin is not listed in marketplace.json")

    for junk in ROOT.rglob("*"):
        if ".git" in junk.parts:
            continue
        if junk.name in JUNK_FILES or junk.name == "__pycache__":
            error(junk, "remove generated or OS junk file")

    return finish()


def finish():
    for line in warnings:
        print(f"warning: {line}")
    for line in errors:
        print(f"error: {line}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
