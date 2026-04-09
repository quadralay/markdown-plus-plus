---
title: Unified naming rule for Markdown++ named entities
date: 2026-04-06
category: logic-errors
module: markdown-plus-plus-spec
problem_type: logic_error
component: tooling
symptoms:
  - "Variables used [\\w]+ regex — excluded hyphens, allowed digit-first names"
  - "Conditions used [\\w ,!] — excluded hyphens from valid names"
  - "Styles used .+ — accepted any characters including spaces"
  - "Capture regexes used [^->]+? character class, silently truncating hyphenated names at the first hyphen"
  - "Validator only checked variable and condition names; styles, aliases, and marker keys had no name validation"
root_cause: logic_error
resolution_type: code_fix
severity: medium
tags:
  - naming-rule
  - regex
  - mdpp002
  - validation
  - syntax-reference
  - unified-grammar
---

# Unified naming rule for Markdown++ named entities

## Problem

The Markdown++ specification and validator defined naming rules independently per extension type (variables, conditions, styles, aliases, markers), leading to inconsistent constraints and gaps in validation coverage. Capture regexes used `[^->]+?` as a character class (excluding both `-` and `>`) rather than the intended "not `>`", silently truncating hyphenated names like `print-only` to `print`.

## Symptoms

- Variables used `[\w]+` — excluded hyphens, permitted digit-first names
- Conditions used `[\w ,!]` — excluded hyphens
- Styles used `.+` — accepted anything including spaces and special characters
- Aliases used `#.+` — accepted anything after `#`
- Validator only checked variable and condition names; styles, aliases, and marker keys had no name validation at all
- Style, condition, and include capture regexes used `[^->]+?`, which is a character class excluding both `-` and `>` — so a name like `print-only` was silently truncated to `print`
- Alias capture regex `[a-zA-Z0-9_-]+?` greedily consumed trailing `--` from `-->` closings

## What Didn't Work

- **Misread character class syntax.** The initial implementation missed that `[^->]+?` is a negated character class matching any character that is neither `-` nor `>`. This meant the fix had to change the character class itself (to `[^>]+?`), not just its placement. The same bug existed in the style, condition, and include patterns.
- **Alias regex too restrictive.** The alias regex `[a-zA-Z0-9_-]+?` was too restrictive in a silent way: aliases with disallowed characters (e.g., dots) would simply not match the pattern at all, so the validator would skip them entirely rather than report them as invalid. Widening the capture to `[^\s;>]+?` was required so that violating values could be captured and reported.

## Solution

### Spec (`syntax-reference.md`)

Added a shared `## Naming Rules` section (placed after Attachment Rules) with a single authoritative regex:

- **Standard names:** `[a-zA-Z_][a-zA-Z0-9_\-]*` — letter or underscore first, then letters/digits/hyphens/underscores (variables, conditions)
- **Alias exception:** `[a-zA-Z0-9_][a-zA-Z0-9_\-]*` — digit-first permitted for numeric identifiers like `#04499224`
- **Style/marker names:** `[a-zA-Z_][a-zA-Z0-9_\- ]*` trimmed — embedded spaces allowed for compound names like `Blockquote Paragraph` (added by #52)

Each extension section (Variables, Styles, Aliases, Conditions, Markers) was updated to cross-reference the shared rule rather than define its own. MDPP002 description was updated from "Invalid variable name" to "Invalid name (variable, style, alias, or marker key)".

### Validator (`validate-mdpp.py`)

Before (per-type, ad hoc):
```python
# Only variable names validated; no coverage for styles, aliases, markers
style_match = re.match(r'<!--\s*style\s+([^->]+?)\s*-->', line)  # truncates at hyphens
```

After (unified, later extended by #52 to three patterns):
```python
STANDARD_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_\-]*$')
ALIAS_NAME_RE    = re.compile(r'^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$')
STYLE_NAME_RE    = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_ -]*$')  # added by #52

def validate_style_name(name, line_num, errors):
    if not STYLE_NAME_RE.match(name.strip()):  # uses STYLE_NAME_RE, not STANDARD_NAME_RE
        errors.append((line_num, 'MDPP002', f'Invalid style name: {name!r}'))

def validate_alias_name(name, line_num, errors):
    if not ALIAS_NAME_RE.match(name):
        errors.append((line_num, 'MDPP002', f'Invalid alias name: {name!r}'))

def validate_marker_key(key, line_num, errors):
    if not STYLE_NAME_RE.match(key.strip()):  # uses STYLE_NAME_RE, not STANDARD_NAME_RE
        errors.append((line_num, 'MDPP002', f'Invalid marker key: {key!r}'))

# Fixed capture regex — [^>]+? instead of [^->]+?
style_match = re.match(r'<!--\s*style\s+([^>]+?)\s*-->', line)
# Widened alias capture to catch violations
alias_match = re.match(r'<!--\s*#([^\s;>]+?)\s*(?:;|-->)', line)
```

### Test file (`sample-invalid-names.md`)

8 positive test cases covering each name type with violations (all trigger MDPP002); 9 negative cases covering valid edge cases including hyphens, underscores, and digit-first aliases (none trigger MDPP002).

## Why This Works

The root cause was distributed, independently maintained naming constraints with no single source of truth. Each extension section defined (or omitted) its own rule, making consistency drift inevitable. The `[^->]+?` capture regex bug was a misread of character class syntax — because `-` and `>` were both excluded, hyphenated names were truncated at the first `-`, and the truncated value could pass validation even when the full name would not.

Unifying the grammar in one spec section, compiling shared regex constants in the validator, and fixing the character class from `[^->]` to `[^>]` eliminates all three failure modes simultaneously.

## Prevention

1. **Single source of truth for naming grammar.** The `## Naming Rules` section in the spec is now authoritative. Any future extension type must reference it rather than define its own pattern. Code review should flag any new per-type name regex as a policy violation.

2. **Shared compiled constants in the validator.** `STANDARD_NAME_RE`, `ALIAS_NAME_RE`, and `STYLE_NAME_RE` are defined once at module level. Adding a new extension type means calling an existing `validate_*_name()` helper, not writing a new regex.

3. **Capture regex review checklist.** When writing `[^...]` character classes in capture groups, verify that each excluded character is intentional. In particular, `-` inside `[^...]` should almost never appear in a name-capture regex — it indicates the regex is doing double duty (capturing and boundary-detecting) and should be split.

4. **Widen capture before narrowing validation.** The alias fix demonstrates the pattern: capture liberally (`[^\s;>]+?`) so violations land in the validator's hands, then apply the strict name regex to report them. A capture regex that is too strict causes silent pass-through of invalid input.

5. **Test file as regression guard.** `sample-invalid-names.md` with its explicit positive/negative split should be run against the validator after any naming rule change. The expected output (8 MDPP002 on positives, 0 on negatives) provides a concrete regression baseline.

## Related Issues

- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) — This issue: enforce unified naming rule
- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) — Error code reference (MDPP002 scope expanded by this work)
- [#11](https://github.com/quadralay/markdown-plus-plus/issues/11) — Formal grammar (defines `identifier` production backed by this rule)
- [#27](https://github.com/quadralay/markdown-plus-plus/issues/27) — ePublisher adapter regex updates (downstream, separate repo)
- [#52](https://github.com/quadralay/markdown-plus-plus/issues/52) — Extended the two-pattern system to three patterns, adding `STYLE_NAME_RE` for styles and markers with embedded spaces
- `docs/solutions/logic-errors/embedded-spaces-in-style-marker-names-2026-04-08.md` — Follow-up learning documenting the #52 correction
