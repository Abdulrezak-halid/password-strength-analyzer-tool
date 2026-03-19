"""Interactive terminal UI for password analysis."""

from __future__ import annotations

from getpass import getpass

from .analyzer import analyze_password
from .utils import yes_no



def _render_report(result) -> str:
    """Format analysis results for interactive terminal mode."""
    lines = [
        "\nPassword Strength Analysis Report",
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
        lines.append("\nRecommendations:")
        for note in result.notes:
            lines.append(f"- {note}")

    return "\n".join(lines)



def run_interactive(common_passwords: set[str]) -> None:
    """Start an interactive session for repeated password checks."""
    print("Interactive Password Strength Analyzer")
    print("Type 'exit' to quit or press Ctrl+C.")

    while True:
        try:
            password = getpass("\nEnter password: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            return

        if password.lower() == "exit":
            print("Session ended.")
            return

        if not password:
            print("Password cannot be empty. Try again.")
            continue

        username = input("Username/email (optional): ").strip()
        if username.lower() == "exit":
            print("Session ended.")
            return

        result = analyze_password(
            password=password,
            common_passwords=common_passwords,
            username=username or None,
        )
        print(_render_report(result))
