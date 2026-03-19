"""Core password analysis and scoring logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .utils import (
    calculate_entropy,
    contains_username_or_email,
    has_digit,
    has_keyboard_pattern,
    has_lowercase,
    has_repeated_characters,
    has_sequential_pattern,
    has_symbol,
    has_uppercase,
)


@dataclass(frozen=True)
class PasswordAnalysis:
    """Structured result of password strength analysis."""

    password: str
    length: int
    has_uppercase: bool
    has_lowercase: bool
    has_digits: bool
    has_symbols: bool
    common_password: bool
    pattern_detected: bool
    repeated_pattern: bool
    sequential_pattern: bool
    keyboard_pattern: bool
    contains_username: bool
    entropy_bits: float
    score: int
    strength: str
    notes: list[str]



def load_common_passwords(file_path: str | Path) -> set[str]:
    """Load common passwords from a text file, one password per line."""
    path = Path(file_path)

    if not path.exists():
        return set()

    with path.open("r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        }



def score_length(length: int) -> tuple[int, str]:
    """Return score contribution and length category description."""
    if length < 6:
        return 0, "very weak"
    if 6 <= length < 8:
        return 1, "weak"
    if 8 <= length < 12:
        return 2, "medium"
    return 4, "strong"



def classify_strength(score: int, common_password: bool) -> str:
    """Map score to final strength class."""
    if common_password:
        return "Weak"
    if score <= 4:
        return "Weak"
    if 5 <= score <= 7:
        return "Medium"
    return "Strong"



def analyze_password(
    password: str,
    common_passwords: set[str],
    username: str | None = None,
) -> PasswordAnalysis:
    """Analyze password quality and return a detailed report object."""
    length = len(password)

    lower = has_lowercase(password)
    upper = has_uppercase(password)
    digits = has_digit(password)
    symbols = has_symbol(password)

    repeated = has_repeated_characters(password)
    sequential = has_sequential_pattern(password)
    keyboard = has_keyboard_pattern(password)
    pattern_detected = repeated or sequential or keyboard

    common_password = password.lower() in common_passwords
    user_included = contains_username_or_email(password, username)
    entropy_bits = calculate_entropy(password)

    length_points, length_quality = score_length(length)
    diversity_points = sum([lower, upper, digits, symbols])

    # Pattern/composition bonus: starts at 2, reduced by risky patterns.
    pattern_points = 2
    notes: list[str] = []

    if common_password:
        pattern_points = 0
        notes.append("Password appears in common_passwords.txt and is high-risk.")

    if pattern_detected:
        if pattern_points > 0:
            pattern_points -= 1
        notes.append("Detected weak pattern (repeated, sequential, or keyboard walk).")

    if user_included:
        if pattern_points > 0:
            pattern_points -= 1
        notes.append("Password contains the provided username/email local-part.")

    if length < 8:
        notes.append("Use at least 8 characters; 12+ is recommended.")
    if diversity_points < 3:
        notes.append("Increase character diversity (upper/lower/digit/symbol).")
    if entropy_bits < 40:
        notes.append("Estimated entropy is low; increase complexity and length.")

    total_score = max(0, min(10, length_points + diversity_points + pattern_points))
    strength = classify_strength(total_score, common_password)

    notes.insert(0, f"Length category: {length_quality}.")

    return PasswordAnalysis(
        password=password,
        length=length,
        has_uppercase=upper,
        has_lowercase=lower,
        has_digits=digits,
        has_symbols=symbols,
        common_password=common_password,
        pattern_detected=pattern_detected,
        repeated_pattern=repeated,
        sequential_pattern=sequential,
        keyboard_pattern=keyboard,
        contains_username=user_included,
        entropy_bits=entropy_bits,
        score=total_score,
        strength=strength,
        notes=notes,
    )
