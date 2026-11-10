"""Cozy Grove styling for Discord posts: palette, embed and card builders, senders.

Images are uploaded with each message and referenced as attachment://<name>,
so nothing needs to be hosted.
"""

import json
import os
from pathlib import Path

import httpx

API = "https://discord.com/api/v10"
ASSETS = Path(__file__).parent / "assets"

COZY = {
    "leaf": 0x82A884,
    "meadow": 0xA4C263,
    "moss": 0x688A7B,
    "path": 0xE8CFA6,
    "peach": 0xEEBA77,
    "bark": 0xC49A6C,
    "bloom": 0xEAE178,
    "ink": 0x5C7479,
}

STYLES = {
    "rules":   {"color": COZY["moss"],   "emoji": "🍄", "banner": "banner_rules.gif"},
    "welcome": {"color": COZY["meadow"], "emoji": "🌿", "banner": "banner_welcome.gif"},
    "news":    {"color": COZY["peach"],  "emoji": "🍊", "banner": "banner_news.gif"},
    "event":   {"color": COZY["bloom"],  "emoji": "🌼", "banner": "banner_event.gif"},
}

THUMB = "cat_idle.gif"
ICON = "icon_leaf.png"
DIVIDER = "divider.gif"
FOOTER = "🐾 tend the grove kindly"
NO_PINGS = {"parse": []}


# ─── Builders ──────────────────────────────────────────────────────
def cozy_embed(kind, title, body, author="Cozy Grove"):
    """Classic embed: coloured side bar, cat thumbnail, animated banner."""
    style = STYLES[kind]
    return {
        "color": style["color"],
        "author": {"name": author, "icon_url": f"attachment://{ICON}"},
        "title": f"{style['emoji']}  {title}"[:256],
        "description": body[:4096],
        "thumbnail": {"url": f"attachment://{THUMB}"},
        "image": {"url": f"attachment://{style['banner']}"},
        "footer": {"text": FOOTER, "icon_url": f"attachment://{ICON}"},
    }


def cozy_card(kind, title, sections, subtitle="Cozy Grove"):
    """Components V2 card: banner on top, title row with cat, divided sections.

    sections: list of (heading, text) tuples.
    """
    style = STYLES[kind]
    parts = [
        {"type": 12, "items": [{"media": {"url": f"attachment://{style['banner']}"}}]},
        {
            "type": 9,
            "components": [{"type": 10, "content": f"## {style['emoji']} {title}\n-# {subtitle}"}],
            "accessory": {"type": 11, "media": {"url": f"attachment://{THUMB}"}},
        },
    ]
    for i, (heading, text) in enumerate(sections):
        if i:
            parts.append({"type": 14, "divider": True, "spacing": 1})
        else:
            parts.append({"type": 12, "items": [{"media": {"url": f"attachment://{DIVIDER}"}}]})
        parts.append({"type": 10, "content": f"### {heading}\n{text}"[:4000]})
    parts.append({"type": 14, "divider": False, "spacing": 2})
    parts.append({"type": 10, "content": f"-# {FOOTER}"})
    return {"type": 17, "accent_color": style["color"], "components": parts}


# ─── Senders ───────────────────────────────────────────────────────
def _send(channel_id, payload, filenames, message_id=None):
    token = os.environ["DISCORD_BOT_TOKEN"]
    url = f"{API}/channels/{channel_id}/messages"
    method = "POST"
    if message_id:
        url += f"/{message_id}"
        method = "PATCH"
    # API v10 needs every attachment listed; on edit, this also replaces the old ones
    payload = {**payload, "attachments": [{"id": i, "filename": n} for i, n in enumerate(filenames)]}
    files = [
        (f"files[{i}]", (name, (ASSETS / name).read_bytes(), _mime(name)))
        for i, name in enumerate(filenames)
    ]
    response = httpx.request(
        method,
        url,
        headers={"Authorization": f"Bot {token}"},
        data={"payload_json": json.dumps(payload)},
        files=files,
        timeout=30,
    )
    if response.is_error:
        raise RuntimeError(f"Discord API {response.status_code}: {response.text}")
    return response.json()["id"]


def _mime(name):
    return "image/gif" if name.endswith(".gif") else "image/png"


def post_cozy(channel_id, kind, title, body, message_id=None):
    """Post (or edit, with message_id) a classic Cozy Grove embed. Returns the message ID."""
    payload = {"embeds": [cozy_embed(kind, title, body)], "allowed_mentions": NO_PINGS}
    return _send(channel_id, payload, [ICON, THUMB, STYLES[kind]["banner"]], message_id)


def post_cozy_card(channel_id, kind, title, sections, message_id=None):
    """Post (or edit) a Components V2 Cozy Grove card. Returns the message ID."""
    payload = {
        "flags": 1 << 15,  # IS_COMPONENTS_V2
        "components": [cozy_card(kind, title, sections)],
        "allowed_mentions": NO_PINGS,
    }
    return _send(channel_id, payload, [STYLES[kind]["banner"], THUMB, DIVIDER], message_id)
