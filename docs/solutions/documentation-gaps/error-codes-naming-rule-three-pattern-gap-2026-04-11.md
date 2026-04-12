---
title: "error-codes.md naming rule section missing style/marker name pattern"
date: 2026-04-11
category: documentation-gaps
module: error-codes
problem_type: documentation_gap
component: documentation
symptoms:
  - "error-codes.md naming rule section described only two patterns (standard identifier, alias), omitting the style/marker name pattern that permits embedded spaces"
  - "MDPP002 listed a single regex (`^[a-zA-Z_][a-zA-Z0-9_\\-]*$`) for all entity types, which rejects valid directives like `<!--style:Code Block-->`"
  - "error-codes.md naming rules conflicted with the three-pattern table in specification.md §4.2 (lines 162-164)"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - naming-rules
  - error-codes
  - specification-alignment
  - mdpp002
  - style-names
  - marker-names
  - three-pattern
---

# error-codes.md naming rule section missing style/marker name pattern

## Problem

`error-codes.md`'s naming rule section documented only one or two of the three naming patterns defined in `specification.md` §4.2, and MDPP002 applied a single regex to all entity types — causing it to incorrectly reject valid style names and marker keys that contain embedded spaces (e.g., `<!--style:Code Block-->`).

## Symptoms

- A validator following `error-codes.md` would apply the standard identifier regex (`^[a-zA-Z_][a-zA-Z0-9_\-]*$`) to style names and marker keys, generating false-positive MDPP002 errors on valid directives like `<!--style:Code Block-->` and `<!--markers:{"Table Cell Head": "value"}-->`.
- MDPP002's description ("Name with illegal characters in any named entity") implied a single universal naming rule, giving implementors no signal that style names and marker keys follow a different, more permissive pattern.
- MDPP007 step 4 used the ambiguous phrase "naming rule regex" without specifying which of the three patterns applied.
- MDPP003's cross-reference said "the naming rule" (singular), obscuring that marker keys use the style/marker rule, not the standard identifier rule.
- The naming rule subsections were titled "Alias Exception" and "Style/Marker Name Exception" — diverging from the intro table names and suggesting these were edge cases rather than first-class patterns.

## What Didn't Work

The original `error-codes.md` naming rule section (pre-fix lines 29-47) listed the standard identifier pattern and an "Alias Exception" subsection but had no style/marker name subsection at all. The prior MDPP002 entry listed "variable names, condition names, style names, and marker key names" as things it validated, yet gave only the standard identifier regex — which forbids spaces — as the actual validation rule. Applying one regex uniformly to all entity types was the root failure: correct for variables and conditions, but wrong for styles and marker keys.

## Solution

**Before — single-regex MDPP002, two subsections, misleading headings:**

The naming rule section had two subsections: "Standard Identifier" and "Alias Exception." There was no style/marker name subsection. MDPP002 read:

> "A named entity (variable, condition name, style, marker key, or alias) contains one or more characters that violate the naming rule."

with one implicit regex (`^[a-zA-Z_][a-zA-Z0-9_\-]*$`) applying to all entity types.

---

**After — three-pattern table, per-entity MDPP002, precise cross-references:**

The naming rule section now leads with an intro table covering all three patterns:

| Form | Regex | Used By | Spaces |
|------|-------|---------|--------|
| **Standard identifier** | `^[a-zA-Z_][a-zA-Z0-9_\-]*$` | Variables, conditions | No |
| **Alias name** | `^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$` | Aliases (digit-first permitted) | No |
| **Style/marker name** | `^[a-zA-Z_][a-zA-Z0-9_ \-]*$` (trimmed) | Styles, marker keys | Yes, embedded |

Three subsections follow — "Standard Identifier," "Alias Name," and "Style/Marker Name" — with trigger examples and NOTEs for each.

MDPP002 description changed to:

> "A named entity (variable, condition name, style, marker key, or alias) contains characters that violate the naming rule **for its entity type**."

MDPP007 step 4 now says "standard identifier regex (`^[a-zA-Z_][a-zA-Z0-9_\-]*$`)" explicitly. MDPP003 cross-ref now says "style/marker name rule" rather than "the naming rule."

Table header "Used by" was also fixed to "Used By" for capitalization consistency with the spec.

## Why This Works

The root cause was documentation drift: `error-codes.md` was created (issue #14) while the two-pattern naming system was in place (issue #15), and it was never updated when the third pattern (style/marker name) was introduced by issue #52. The spec §4.2 three-pattern table is the normative source; `error-codes.md` is the validator reference derived from it. Making `error-codes.md` structurally parallel to the spec table — same three rows, same terminology — closes the gap and gives implementors unambiguous per-entity-type rules.

The advisory spec-internal contradiction between §13.2 prose (marker keys use standard identifier) and §13.4 error table (marker keys use style/marker name) was noted but is out of scope for this fix; it predates the PR and needs a dedicated spec correction.

## Prevention

- **Keep the naming rule table in `error-codes.md` structurally parallel to `specification.md` §4.2.** Both files now use the same three-row, four-column table format. When the spec table changes, the mismatch will be immediately visible on comparison.
- **Cross-reference the spec section number explicitly.** Noting "See specification.md §4.2 Naming Rules for the normative definition" in the `error-codes.md` naming rule intro creates a discoverable audit trail that prompts editors to open the spec before modifying the table.
- **Validate `error-codes.md` against the spec as part of PR review for naming-related changes.** Any PR touching §4.2 in `specification.md` should include a corresponding check of the naming rule table in `error-codes.md`, and vice versa. The two files are now structurally coupled.
- **Use per-entity-type names ("standard identifier rule," "alias rule," "style/marker rule") in error descriptions** rather than inlining regex strings. This reduces divergence surface: if a regex changes, only the naming rule table row and its subsection need updating, not every error entry that references it.
- **Track open spec contradictions as dedicated issues.** The §13.2 vs §13.4 conflict on marker key naming is a pre-existing spec-internal inconsistency that could cause implementation divergence. Opening an issue at the time of discovery prevents it from being lost in PR advisory notes.

## Related Issues

- [#65](https://github.com/quadralay/markdown-plus-plus/issues/65) — This fix (three-pattern gap in `error-codes.md`)
- [#52](https://github.com/quadralay/markdown-plus-plus/issues/52) — Introduced the third naming pattern (style/marker name with embedded spaces)
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) — Original unified naming rule creation (two-pattern system)
- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) — Creation of the standalone `error-codes.md` reference

**Related solution docs:**
- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` — Documents the original unified-rule creation (#15); solution narrative predates the three-pattern state
- `docs/solutions/logic-errors/embedded-spaces-in-style-marker-names-2026-04-08.md` — Documents the three-pattern extension (#52); the problem that created the gap this fix closes
- `docs/solutions/documentation-gaps/error-code-reference-2026-04-08.md` — Documents the creation of `error-codes.md` (#14); its MDPP002 naming rule description (single-regex) is now superseded by the three-pattern table
