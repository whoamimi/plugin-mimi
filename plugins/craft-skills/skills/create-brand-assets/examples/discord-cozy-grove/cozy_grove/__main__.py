"""Post a Cozy Grove message from the command line.

Examples:
    uv run python -m cozy_grove rules --channel 222 --body-file channels/rules.md
    uv run python -m cozy_grove news --channel 333 --title "Update" --body "New channels are open!"
    uv run python -m cozy_grove welcome --channel 444 --card
    uv run python -m cozy_grove rules --channel 222 --body-file channels/rules.md --edit 1234567890
"""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from .style import STYLES, post_cozy, post_cozy_card

DEFAULT_TITLES = {"rules": "Grove Rules", "welcome": "Welcome to the Grove",
                  "news": "Grove News", "event": "Grove Event"}
SAMPLE_BODY = (
    "🌿 **Be kind.** No harassment, hate or personal attacks.\n"
    "🍊 **No spam.** Ask a keeper before promoting anything.\n"
    "🍄 **Stay on the path.** Keep topics in their channels.\n"
    "🌼 **Keep it cozy.** No NSFW content.\n\n"
    "> 🐾 Keepers have the final say."
)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(prog="cozy_grove", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=sorted(STYLES))
    parser.add_argument("--channel", required=True, help="Channel (or thread) ID to post in")
    parser.add_argument("--title", help="Post title (defaults per kind)")
    body = parser.add_mutually_exclusive_group()
    body.add_argument("--body", help="Post text (Markdown)")
    body.add_argument("--body-file", type=Path, help="Read the post text from a Markdown file")
    parser.add_argument("--card", action="store_true", help="Use the Components V2 card layout")
    parser.add_argument("--edit", metavar="MESSAGE_ID", help="Edit this message instead of posting")
    args = parser.parse_args()

    title = args.title or DEFAULT_TITLES[args.kind]
    text = args.body_file.read_text(encoding="utf-8") if args.body_file else (args.body or SAMPLE_BODY)

    if args.card:
        sections = [(title, text)]
        message_id = post_cozy_card(args.channel, args.kind, title, sections, args.edit)
    else:
        message_id = post_cozy(args.channel, args.kind, title, text, args.edit)
    print(f"{'Edited' if args.edit else 'Posted'} message {message_id}")


if __name__ == "__main__":
    main()
