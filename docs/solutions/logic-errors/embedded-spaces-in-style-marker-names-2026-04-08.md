---
title: Allow embedded spaces in style and marker names
date: 2026-04-08
category: logic-errors
module: markdown-plus-plus-spec
problem_type: logic_error
component: documentation
symptoms:
  - "Processor-defined compound style names (e.g., Blockquote Paragraph, Table Cell Head) rejected by unified naming rule"
  - "Legacy ePublisher projects with space-embedded style names could not be represented in valid Markdown++"
  - "Marker keys with embedded spaces (e.g., Index Entry) rejected as invalid names"
  - "Validator produced false-positive MDPP002 errors on legitimate style and marker names containing spaces"
root_cause: logic_error
resolution_type: documentation_update
severity: medium
tags:
  - naming-rule
  - embedded-spaces
  - style-names
  - marker-names
  - mdpp002
  - formal-grammar
  - validation
---

# Allow embedded spaces in style and marker names

## Problem

Issue #15 established a unified naming rule `[a-zA-Z_][a-zA-Z0-9_\-]*` for all Markdown++ named entities, forbidding spaces everywhere. This was an overreach — styles and markers need embedded spaces for processor-defined compound names like `Blockquote Paragraph`, `OList Item`, and `Table Cell Head`, and for legacy ePublisher compatibility.

## Symptoms

- Processor-generated compound style names (`Blockquote Paragraph`, `Table Cell Head`, `OList Item`) were invalid under the unified naming rule, creating an internal contradiction where the spec's own compound naming system produced names that violated the spec's own rule
- The `element-interactions.md` spec had to include a disclaimer that compound names "do not conform to `STANDARD_NAME_RE`" — an ad hoc workaround that undermined the grammar's authority
- Legacy ePublisher projects with space-embedded style names could not be represented in valid Markdown++
- Authors could not write `<!-- style:Code Block -->` or `<!-- marker:Index Entry="setup" -->` despite these being natural, real-world names
- The validator produced false-positive MDPP002 errors on legitimate style and marker names containing spaces

## What Didn't Work

The original approach from issue #15 defined only two identifier forms — a standard identifier (for variables, styles, conditions, and marker keys) and an alias name (adding digit-first for aliases). This treated all non-alias entities identically, failing to account for: (1) the spec's own compound naming system producing space-separated names, (2) processor-defined style names that naturally contain spaces, and (3) legacy tooling compatibility. The `element-interactions.md` document awkwardly noted compound names "fall outside the single-identifier naming rule," creating an internal inconsistency rather than fixing the grammar.

## Solution

Introduced a third identifier form — the **style/marker name** — creating a three-tier naming system across 6 files:

| Pattern | Regex | Used By | Spaces |
|---------|-------|---------|--------|
| **Standard identifier** | `[a-zA-Z_][a-zA-Z0-9_\-]*` | Variables, conditions | No |
| **Alias name** | `[a-zA-Z0-9_][a-zA-Z0-9_\-]*` | Aliases | No |
| **Style/marker name** | `[a-zA-Z_][a-zA-Z0-9_\- ]*` trimmed | Styles, markers | Yes, embedded |

Key changes:

- **`spec/formal-grammar.md`** — Added `style_name` production to EBNF and PEG grammars. Changed `style_cmd` and `marker_cmd` to use `style_name` instead of `identifier`.
- **`spec/specification.md`** — Section 4.2 naming rules expanded from two rows to three.
- **`spec/element-interactions.md`** — Compound naming section rewritten: the old disclaimer ("do not conform to `STANDARD_NAME_RE`... by design") replaced with "conform to the style/marker name pattern."
- **`syntax-reference.md`** — Naming Rules restructured into three subsections with expanded valid/invalid tables.
- **`validate-mdpp.py`** — Added `STYLE_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_ -]*$')`. Changed `validate_style_name()` and `validate_marker_key()` to use `STYLE_NAME_RE` with `.strip()` trimming.
- **`sample-invalid-names.md`** — Removed old false-positive case. Added positive cases (digit-first + space, punctuation + space) and negative cases validating `Code Block`, `Table Cell Head`, `Index Entry`, `Blockquote Paragraph`.

## Why This Works

Variables and conditions need strict names because spaces are operators (AND operator in conditions) or syntactically ambiguous (`$has space;`). But style names and marker keys appear in structured positions (after `style:`, after `marker:`, or as JSON keys in quotes) where embedded spaces are unambiguous — the `style:` prefix and the `="` suffix in markers clearly delimit name boundaries. The fix recognizes this distinction by giving styles and markers their own pattern that allows embedded spaces while enforcing the same first-character rule (letter or underscore) and prohibiting punctuation.

This also resolves the circular correction: pre-#15 styles used `.+` (accepting anything including spaces), #15 tightened all names to no-spaces, and #52 restores space support specifically for styles and markers via a properly constrained pattern.

## Prevention

1. **Test compound naming outputs against the naming grammar.** The compound naming system (`ContainerStyle + space + ElementStyle`) always produces space-embedded names. Any naming grammar change must be validated against compound naming examples in `element-interactions.md`.

2. **Distinguish entities by their syntactic context.** Before applying a uniform rule across entity types, analyze whether each type's parsing context supports the restriction. Variables (`$name;`) have no quoting, making spaces ambiguous. Styles (`style:Name`) and markers (`marker:Key="value"`) have structural delimiters that make spaces unambiguous.

3. **Check legacy compatibility when restricting naming.** Before tightening a naming rule, inventory the names that existing tools and projects actually use.

4. **Watch for spec-internal contradictions as a signal.** When one spec document has to explain why another document's rule "doesn't apply" to its outputs, that is a strong signal the rule is wrong — not that the output is a special case.

5. **Expand test cases proactively.** The test file now includes Cases 18-22 covering embedded spaces. New naming rule changes should add both positive and negative test cases for every entity type that might be affected.

## Related Issues

- [#52](https://github.com/quadralay/markdown-plus-plus/issues/52) — This issue: allow embedded spaces in style and marker names
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) — Direct predecessor: established the two-pattern naming system that #52 extends to three patterns
- [#27](https://github.com/quadralay/markdown-plus-plus/issues/27) — ePublisher adapter regex updates (downstream, may need updating for STYLE_NAME_RE)
- [#49](https://github.com/quadralay/markdown-plus-plus/issues/49) — Element interaction refinements (depends on embedded spaces being valid)
- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` — The #15 learning that established the two-pattern system; now partially stale (shows only two constants, needs refresh)
- `docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md` — States "two identifier productions" when the grammar now defines three; needs refresh
