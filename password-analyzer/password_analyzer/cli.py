"""CLI orchestration for the Password Strength Analyzer."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_password, load_common_passwords
from .tui import run_interactive
from .utils import yes_no



def get_common_passwords_path() -> Path:
    """Return the common-passwords file path with fallback support."""
    root = Path(__file__).resolve().parent.parent
    preferred = root / "data" / "common_passwords.txt"
    legacy = root / "common_passwords.txt"

    if preferred.exists():
        return preferred
    return legacy



def render_report(result) -> str:
    """Format analysis results for CLI display."""
    lines = [
        "Password Strength Analysis Report",
        "=" * 35,
        f"Password: {result.password}",
        "",
        f"Length: {result.length}",
        f"Uppercase: {yes_no(result.has_uppercase)}",
        f"Lowercase: {yes_no(result.has_lowercase)}",
        f"Digits: {yes_no(result.has_digits)}",
        f"Symbols: {yes_no(result.has_symbols)}",
        f"Common Password: {yes_no(result.common_password)}",
        f"Pattern Detected: {yes_no(result.pattern_detected)}",
        f"  - Repeated Characters: {yes_no(result.repeated_pattern)}",
        f"  - Sequential Pattern: {yes_no(result.sequential_pattern)}",
        f"  - Keyboard Pattern: {yes_no(result.keyboard_pattern)}",
        f"Contains Username/Email: {yes_no(result.contains_username)}",
        f"Estimated Entropy: {result.entropy_bits:.2f} bits",
        "",
        f"Score: {result.score}/10",
        f"Strength: {result.strength}",
    ]

    if result.notes:
        lines.append("")
        lines.append("Recommendations:")
        for note in result.notes:
            lines.append(f"- {note}")

    return "\n".join(lines)



def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser with command and interactive modes."""
    parser = argparse.ArgumentParser(
        prog="password-analyzer",
        description="Analyze password strength using practical security checks.",
    )

    parser.add_argument(
        "--password",
        required=False,
        help="Backward-compatible direct password analysis mode.",
    )
    parser.add_argument(
        "--username",
        required=False,
        default=None,
        help="Optional username/email used for additional checks.",
    )

    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser(
        "check",
        help="Analyze a single password from the command line.",
    )
    check_parser.add_argument("--password", required=True, help="Password to analyze.")
    check_parser.add_argument(
        "--username",
        required=False,
        default=None,
        help="Optional username/email used for additional checks.",
    )

    subparsers.add_parser(
        "interactive",
        help="Launch interactive terminal mode for repeated analysis.",
    )

    return parser



def run_cli(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """Execute requested CLI action and return process exit code."""
    common_passwords = load_common_passwords(get_common_passwords_path())

    if args.command == "interactive":
        run_interactive(common_passwords)
        return 0

    if args.command == "check":
        password = args.password
        username = args.username
    elif args.password is not None:
        # Backward-compatible path: python main.py --password "..."
        password = args.password
        username = args.username
    else:
        parser.print_help()
        return 2

    if password is None or not password.strip():
        parser.error("password cannot be empty.")

    result = analyze_password(
        password=password,
        common_passwords=common_passwords,
        username=username,
    )
    print(render_report(result))
    return 0
