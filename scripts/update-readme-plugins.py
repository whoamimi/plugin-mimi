#!/usr/bin/env python3
"""Regenerate the plugin table in README.md between the plugins markers.

usage: python3 scripts/update-readme-plugins.py [--check]

One row per marketplace plugin: name, a live version badge (shields.io reads
the version from plugin.json on main, so it updates on every merge with no
README edit), its skills, and the install command. With --check, nothing is
written and the exit code is 1 if the table is out of date. Stdlib only.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
START, END = "<!-- plugins:start -->", "<!-- plugins:end -->"


def badge(repo_path, name):
    raw = f"https://raw.githubusercontent.com/{repo_path}/main/plugins/{name}/.claude-plugin/plugin.json"
    url = (f"https://img.shields.io/badge/dynamic/json?url={quote(raw, safe='')}"
           f"&query={quote('$.version', safe='')}&label=version&color=blue")
    return f"![{name} version]({url})"


def table():
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    rows = ["| Plugin | Version | Skills | Install |", "|---|---|---|---|"]
    for entry in marketplace["plugins"]:
        plugin_dir = (ROOT / entry["source"]).resolve()
        manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
        name = manifest["name"]
        repo = manifest.get("repository", "")
        match = re.match(r"https://github\.com/([^/]+/[^/]+?)(?:\.git)?/?$", repo)
        version = badge(match.group(1), name) if match else f"`{manifest.get('version', '?')}`"
        skills = sorted(p.parent.name for p in (plugin_dir / "skills").glob("*/SKILL.md"))
        title = manifest.get("displayName", name)
        home = manifest.get("homepage")
        label = f"[{title}]({home})" if home else title
        rows.append(f"| {label} | {version} | {', '.join(f'`{s}`' for s in skills)} "
                    f"| `claude plugin install {entry['name']}@{marketplace['name']}` |")
    return "\n".join(rows) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if the table is out of date")
    a = ap.parse_args()
    text = README.read_text()
    if START not in text or END not in text:
        sys.exit(f"README.md is missing the {START} / {END} markers")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    updated = f"{before}{START}\n{table()}{END}{after}"
    if updated == text:
        return 0
    if a.check:
        print("README plugin table is out of date; run scripts/update-readme-plugins.py")
        return 1
    README.write_text(updated)
    print("README plugin table updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
