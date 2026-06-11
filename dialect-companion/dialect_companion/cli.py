"""Command-line interface: interactive chat REPL and one-shot translation."""

import argparse
import os
import sys

import anthropic

from .companion import Companion
from .dialects import DEFAULT_DIALECT, DIALECTS, get_dialect

BANNER = """\
╭──────────────────────────────────────────────╮
│  Dialect Companion — {name}
│  Type in dialect, Arabizi, French or English.
│  Commands: /translate on|off  /dialects  /quit
╰──────────────────────────────────────────────╯
"""


def run_chat(args: argparse.Namespace) -> None:
    dialect = get_dialect(args.dialect)
    companion = Companion(dialect, show_translations=not args.no_translations)
    print(BANNER.format(name=dialect.name))
    print("صحّيت! وشراك؟ (sahit! wechrak?)\n")

    while True:
        try:
            user_text = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nبقاو على خير! (beslama!)")
            return
        if not user_text:
            continue
        if user_text in ("/quit", "/exit", "/q"):
            print("بقاو على خير! (beslama!)")
            return
        if user_text == "/dialects":
            for d in DIALECTS.values():
                print(f"  {d.key:12} {d.name}")
            continue
        if user_text.startswith("/translate"):
            arg = user_text.removeprefix("/translate").strip()
            if arg in ("on", "off"):
                companion.show_translations = arg == "on"
                print(f"[translations {arg}]")
            else:
                print("usage: /translate on|off")
            continue

        print()
        try:
            for chunk in companion.chat(user_text):
                print(chunk, end="", flush=True)
        except anthropic.APIConnectionError:
            print("[connection error — check your network and try again]")
        except anthropic.RateLimitError:
            print("[rate limited — wait a moment and try again]")
        except anthropic.APIStatusError as e:
            print(f"[API error {e.status_code}: {e.message}]")
        print("\n")


def run_translate(args: argparse.Namespace) -> None:
    dialect = get_dialect(args.dialect)
    companion = Companion(dialect)
    text = args.text or sys.stdin.read().strip()
    if not text:
        raise SystemExit("Nothing to translate: pass text as an argument or pipe it on stdin.")

    result = companion.translate(text)
    print(f"Input ({dialect.name}):")
    print(f"  {result.detected_input}\n")
    print(f"MSA: {result.standard_arabic}")
    print(f"EN:  {result.english}")
    print(f"FR:  {result.french}")
    if result.notes:
        print(f"\nNotes: {result.notes}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dialect-companion",
        description="AI companion that chats in Arabic dialects and translates to English/French.",
    )
    parser.add_argument(
        "--dialect",
        default=DEFAULT_DIALECT,
        help=f"Dialect to use (default: {DEFAULT_DIALECT}). See /dialects in chat.",
    )
    sub = parser.add_subparsers(dest="command")

    chat_parser = sub.add_parser("chat", help="Interactive chat (default)")
    chat_parser.add_argument(
        "--no-translations",
        action="store_true",
        help="Don't append EN/FR translations after each exchange",
    )

    translate_parser = sub.add_parser("translate", help="Translate dialect text to MSA/English/French")
    translate_parser.add_argument("text", nargs="?", help="Text to translate (or pipe via stdin)")

    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        raise SystemExit("Set ANTHROPIC_API_KEY (or ANTHROPIC_AUTH_TOKEN) before running.")

    if args.command == "translate":
        run_translate(args)
    else:
        if args.command is None:
            args.no_translations = False
        run_chat(args)


if __name__ == "__main__":
    main()
