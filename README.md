# Password Strength Analyzer (CLI + Interactive Terminal UI)

A practical Python security tool for university-level Computer Network Security coursework. It analyzes passwords using real-world criteria, produces a numeric score, and supports both direct CLI checks and an interactive terminal workflow.

## Features

- CLI-based password analysis with `argparse`
- Interactive terminal mode for repeated checks in one session
- Easy-run scripts for quick input
- Length-based strength evaluation
- Character diversity analysis:
  - Lowercase
  - Uppercase
  - Digits
  - Symbols
- Common-password detection from wordlist file
- Pattern detection:
  - Repeated characters (`aaaa`, `1111`)
  - Sequential characters (`1234`, `abcd`)
  - Keyboard walks (`qwerty`, `asdf`)
- Optional advanced checks:
  - Estimated entropy (bits)
  - Username/email local-part detection
- Final score and classification (`Weak`, `Medium`, `Strong`)

## Installation

1. Install Python 3.10+.
2. Open terminal in project directory:

```bash
cd password-analyzer
```

No third-party dependencies are required.

## Usage

### 1) Backward-compatible direct mode

```bash
python main.py --password 'P@ss123'
python main.py --password 'admin123' --username 'admin'
```

### 2) Explicit command mode

```bash
python main.py check --password 'P@ss123'
python main.py check --password 'MyMail2026!' --username 'student@example.edu'
```

### 3) Interactive terminal UI

```bash
python main.py interactive
```

You can type multiple passwords in one session, and type `exit` to quit.

### 4) Easy input scripts

Quick one-line password check:

```bash
./scripts/quick_check.sh 'P@ss123'
./scripts/quick_check.sh 'admin123' 'admin'
```

Start interactive mode:

```bash
./scripts/interactive.sh
```

## Scoring Logic (0-10)

- Length: up to **4 points**
  - `< 6` -> 0 points (very weak)
  - `6-7` -> 1 point (weak)
  - `8-11` -> 2 points (medium)
  - `12+` -> 4 points (strong)
- Character diversity: up to **4 points**
  - +1 each for lowercase, uppercase, digits, symbols
- Pattern/composition safety: up to **2 points**
  - Starts at 2 points
  - Common password -> 0 points (high-risk override)
  - Weak patterns reduce safety points
  - Username/email in password can reduce safety points

Final classification:

- `0-4` -> Weak
- `5-7` -> Medium
- `8-10` -> Strong

## Example Outputs

### Example 1

Command:

```bash
python main.py check --password 'P@ss123'
```

Output:

```text
Password Strength Analysis Report
===================================
Password: P@ss123

Length: 7
Uppercase: Yes
Lowercase: Yes
Digits: Yes
Symbols: Yes
Common Password: No
Pattern Detected: No
  - Repeated Characters: No
  - Sequential Pattern: No
  - Keyboard Pattern: No
Contains Username/Email: No
Estimated Entropy: 45.88 bits

Score: 7/10
Strength: Medium

Recommendations:
- Length category: weak.
- Use at least 8 characters; 12+ is recommended.
```

## Error Handling

- Missing required arguments (handled by `argparse`)
- Empty password validation
- Invalid CLI flags and subcommands
- Safe interactive-session exits with `exit`, `Ctrl+C`, or `EOF`

## Educational Note

This is a defensive security education tool for password policy awareness and local analysis. It does not query external breach APIs.
