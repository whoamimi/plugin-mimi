#!/usr/bin/env python3
"""Lint the marketplace, plugin manifests and skills against Anthropic's
plugin and skill authoring guidance.

Sources:
  https://code.claude.com/docs/en/plugins-reference
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Usage: python3 scripts/lint-plugins.py [--base origin/main]   (stdlib only)
Exits 1 when any error is found. Warnings are printed but do not fail.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Limits from the skill authoring best practices.
NAME_MAX = 64
DESCRIPTION_MAX = 1024
BODY_MAX_LINES = 500
REFERENCE_TOC_LINES = 100
RESERVED_WORDS = ("anthropic", "claude")

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
XML_TAG = re.compile(r"<\/?[A-Za-z][^>]*>")
FIRST_OR_SECOND_PERSON = re.compile(r"^\s*(I|I'm|I can|I will|You|You can|We)\b")
FENCED_BLOCK = re.compile(r"^```.*?^```", re.S | re.M)
MD_LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
JUNK_FILES = (".DS_Store", "Thumbs.db")
JUNK_DIRS = ("__pycache__", ".ruff_cache", ".pytest_cache")

errors, warnings = [], []
BASE_REF = None


def rel(path):
    return path.relative_to(ROOT).as_posix()


def error(path, msg):
    errors.append(f"{rel(path)}: {msg}")


def warn(path, msg):
    warnings.append(f"{rel(path)}: {msg}")


def tracked_files():
    """Files tracked by git, so ignored local caches are not reported."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    return out.stdout.splitlines()


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


def raw_scalar_breaks_yaml(path):
    """A plain (unquoted) YAML value cannot contain ': ' or ' #'."""
    for line in path.read_text().splitlines()[1:]:
        if line.strip() == "---":
            return False
        match = re.match(r"^description:\s*(.*)$", line)
        if match:
            value = match.group(1)
            if value[:1] in ("'", '"', ">", "|"):
                return False
            return ": " in value or " #" in value
    return False


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
        if raw_scalar_breaks_yaml(skill_md):
            error(skill_md, "unquoted description contains ': ' or ' #', which breaks YAML; quote it or reword")
        if XML_TAG.search(description):
            error(skill_md, "description contains an XML tag")
        if FIRST_OR_SECOND_PERSON.match(description):
            warn(skill_md, "description should be written in the third person")
        if not re.search(r"\buse (when|for|this|whenever)\b", description, re.I):
            warn(skill_md, "description should say when to use the skill ('Use when ...')")
        if not re.search(r'"[^"]+"', description):
            warn(skill_md, 'description should quote one or more example requests, e.g. Examples include "..."')

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


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def check_version_bump(plugin_dir, manifest_path, version):
    """A plugin whose files changed since BASE_REF must raise its version.

    Users only receive an update when the version string changes, so a change
    without a bump never reaches anyone who installed the plugin.
    """
    rel = plugin_dir.relative_to(ROOT).as_posix()
    # Compare the working tree with the merge base, so both committed and
    # uncommitted changes count, but changes made on the base branch do not.
    base = git("merge-base", BASE_REF, "HEAD").stdout.strip() or BASE_REF
    if not git("diff", "--quiet", base, "--", rel).returncode:
        return  # no changes in this plugin
    old = git("show", f"{base}:{rel}/.claude-plugin/plugin.json")
    if old.returncode:
        return  # new plugin: nothing to compare against
    try:
        old_version = json.loads(old.stdout).get("version", "")
    except json.JSONDecodeError:
        return
    if not (SEMVER.match(version) and SEMVER.match(old_version)):
        return
    if tuple(map(int, version.split("."))) <= tuple(map(int, old_version.split("."))):
        error(manifest_path, f"plugin changed since {BASE_REF} but version is still {old_version}; "
                             "bump it (patch: fixes, minor: new skills, major: removed or renamed skills)")


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
    version = manifest.get("version", "")
    if version and not SEMVER.match(version):
        error(manifest_path, f"version '{version}' must be MAJOR.MINOR.PATCH")
    if "version" in entry:
        error(ROOT / ".claude-plugin" / "marketplace.json",
              f"entry '{entry.get('name')}' sets version; keep it only in plugin.json")
    if BASE_REF:
        check_version_bump(plugin_dir, manifest_path, version)
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
    global BASE_REF
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", metavar="REF",
                    help="git ref to compare against, e.g. origin/main; changed plugins must bump their version")
    BASE_REF = ap.parse_args().base
    if BASE_REF and git("rev-parse", "--verify", "--quiet", BASE_REF).returncode:
        error(ROOT, f"--base {BASE_REF} is not a known git ref (fetch it first)")
        return finish()
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

    for tracked in tracked_files():
        parts = Path(tracked).parts
        if parts[-1] in JUNK_FILES or any(part in JUNK_DIRS for part in parts):
            error(ROOT / tracked, "generated or OS junk file is committed; remove it and add it to .gitignore")

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
