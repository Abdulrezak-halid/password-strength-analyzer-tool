"""Utility helpers for password strength analysis."""

from __future__ import annotations

import math
import re
import string
from typing import Iterable


KEYBOARD_PATTERNS = (
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "1qaz",
    "12345",
)



def has_lowercase(password: str) -> bool:
    """Return True if password contains at least one lowercase character."""
    return any(char.islower() for char in password)



def has_uppercase(password: str) -> bool:
    """Return True if password contains at least one uppercase character."""
    return any(char.isupper() for char in password)



def has_digit(password: str) -> bool:
    """Return True if password contains at least one digit."""
    return any(char.isdigit() for char in password)



def has_symbol(password: str) -> bool:
    """Return True if password contains at least one symbol/punctuation."""
    return any(char in string.punctuation for char in password)



def has_repeated_characters(password: str, repeat_threshold: int = 3) -> bool:
    """Detect repeated characters such as 'aaaa' or '1111'.

    Args:
        password: Password to inspect.
        repeat_threshold: Minimum consecutive identical characters to flag.
    """
    pattern = rf"(.)\\1{{{repeat_threshold - 1},}}"
    return bool(re.search(pattern, password))



def _has_sequence_in_reference(password: str, reference: str, window_size: int = 4) -> bool:
    """Return True if password contains a sequential slice from a reference string."""
    if window_size < 3:
        window_size = 3

    normalized = password.lower()

    for index in range(len(reference) - window_size + 1):
        chunk = reference[index : index + window_size]
        if chunk in normalized or chunk[::-1] in normalized:
            return True
    return False



def has_sequential_pattern(password: str) -> bool:
    """Detect sequential alphabetic or numeric patterns like '1234' or 'abcd'."""
    numeric = _has_sequence_in_reference(password, string.digits)
    alphabetic = _has_sequence_in_reference(password, string.ascii_lowercase)
    return numeric or alphabetic



def has_keyboard_pattern(password: str, patterns: Iterable[str] = KEYBOARD_PATTERNS) -> bool:
    """Detect keyboard-walk patterns such as 'qwerty' and 'asdf'."""
    lowered = password.lower()
    return any(pattern in lowered for pattern in patterns)



def calculate_entropy(password: str) -> float:
    """Estimate password entropy in bits using character set size and length.

    This is a simplified estimate: entropy ~= L * log2(R), where
    L is the password length and R is the estimated character pool.
    """
    if not password:
        return 0.0

    pool_size = 0
    if has_lowercase(password):
        pool_size += 26
    if has_uppercase(password):
        pool_size += 26
    if has_digit(password):
        pool_size += 10
    if has_symbol(password):
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0.0

    return len(password) * math.log2(pool_size)



def contains_username_or_email(password: str, username: str | None) -> bool:
    """Return True if password includes the username or email local-part."""
    if not username:
        return False

    normalized_password = password.lower()
    normalized_username = username.strip().lower()

    if not normalized_username:
        return False

    email_local_part = normalized_username.split("@", maxsplit=1)[0]

    return (
        normalized_username in normalized_password
        or email_local_part in normalized_password
    )



def yes_no(value: bool) -> str:
    """Convert a boolean to a user-facing Yes/No value."""
    return "Yes" if value else "No"
