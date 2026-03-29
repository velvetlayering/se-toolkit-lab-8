"""Telegram bot entry point with --test mode."""

from __future__ import annotations

import argparse


def handle_start() -> str:
    """Return a welcome message for /start."""

    return "Welcome to Nanobot!"


def handle_help() -> str:
    """Return available commands."""

    commands = [
        "/start - show welcome message",
        "/help - list commands",
        "/health - placeholder for backend health",
        "/labs - placeholder for labs list",
        "/scores - placeholder for scores",
    ]
    return "Available commands:\n" + "\n".join(commands)


def handle_health() -> str:
    """Placeholder health handler."""

    return "Health check not implemented yet"


def handle_labs() -> str:
    """Placeholder labs handler."""

    return "Labs list not implemented yet"


def handle_scores() -> str:
    """Placeholder scores handler."""

    return "Scores not implemented yet"


def run_test(command: str) -> str:
    """Run the given command string in test mode."""

    normalized = command.strip()
    if normalized == "/start":
        return handle_start()
    if normalized == "/help":
        return handle_help()
    if normalized == "/health":
        return handle_health()
    if normalized == "/labs":
        return handle_labs()
    if normalized == "/scores":
        return handle_scores()
    return "Unknown command"


def main() -> None:
    parser = argparse.ArgumentParser(description="Telegram bot entry point")
    parser.add_argument("command", nargs="?", help="Command to run in --test mode")
    parser.add_argument(
        "--test",
        dest="test",
        action="store_true",
        help="Run a handler without Telegram",
    )
    args = parser.parse_args()

    if args.test:
        if not args.command:
            parser.error("--test requires a command string")
        print(run_test(args.command))
        return

    raise SystemExit("Telegram integration not implemented yet")


if __name__ == "__main__":
    main()
