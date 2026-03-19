"""CLI entry point for the Password Strength Analyzer tool."""

from __future__ import annotations

import sys

from password_analyzer.cli import build_parser, run_cli


def main() -> None:
    """CLI bootstrap function."""
    parser = build_parser()
    args = parser.parse_args()
    exit_code = run_cli(args, parser)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
