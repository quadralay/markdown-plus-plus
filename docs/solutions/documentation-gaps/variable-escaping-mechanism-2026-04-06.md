---
date: 2026-04-06
status: active
issue: 16
---

# Variable escaping mechanism

## Problem

The whitepaper and syntax reference mentioned `\$` as the escape for preventing variable interpretation, but the documentation was minimal — a single table row and a brief example. The escaping mechanism was not formally specified, and the processing order (escape resolution before variable substitution) was not documented. Additionally, inline code spans as a second escaping mechanism were not mentioned.

## Decision

Two escaping mechanisms are supported:

1. **Backslash escaping** (`\$name;`) — the `\$` sequence is recognized and handled in Phase 1, *before* variable substitution runs. The backslash is consumed and the `$` becomes a literal character.

2. **Inline code spans** (`` `$name;` ``) — code spans are excluded from variable scanning entirely. This already works in parsers that respect CommonMark code span boundaries.

## Changes made

- **syntax-reference.md**: Added dedicated "Escaping Variables" subsection under Variables with both mechanisms, processing order note, and usage guidance table.
- **whitepaper.md**: Expanded inline token description to mention both escaping mechanisms.
- **examples/styles-and-variables.md**: Replaced single-line escape example with subsection showing both mechanisms.
- **best-practices.md**: Added "Escaping variables" guidance in the Variables section.
- **SKILL.md**: Updated escape rule to mention both mechanisms.
- **validate-mdpp.py**: Updated variable regex patterns to use negative lookbehind (`(?<!\\)`) so escaped variables are not flagged as invalid.

## Why this matters

- Without formal specification, parser implementations may handle escaping inconsistently
- The processing order (escape resolution before variable substitution) is critical for correct behavior
- Authors need clear guidance on when to use each mechanism
