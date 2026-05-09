---
title: Condition Block Nesting Incorrectly Documented as Supported
date: 2026-04-11
last_refreshed: 2026-05-09
category: documentation-gaps
module: markdown-plus-plus
problem_type: documentation_gap
component: documentation
symptoms:
  - spec/specification.md stated "Condition blocks MAY be nested within a single file" with a full Nesting subsection and example
  - spec/processing-model.md had a "Nested Conditions" subsection documenting evaluation order for nested blocks
  - spec/formal-grammar.md stated "Condition blocks may nest but MUST NOT overlap"
  - plugin references (syntax-reference.md) showed nested condition syntax as valid examples
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
related_components:
  - tooling
tags:
  - condition-blocks
  - nesting
  - spec-correction
  - logical-expressions
  - markdown-plus-plus
---

# Condition Block Nesting Incorrectly Documented as Supported

## Problem

The Markdown++ specification incorrectly documented that condition blocks could be nested within a single file across four locations. Condition block nesting is not and has never been a supported Markdown++ feature — the documentation was factually wrong and constituted a release-blocking spec error.

## Symptoms

- `spec/specification.md` line 578: "Condition blocks MAY be nested within a single file."
- `spec/specification.md` lines 578–591: Full "Nesting" subsection with example of nested `<!--condition:-->` blocks
- `spec/processing-model.md` lines 193–208: "Nested Conditions" subsection with evaluation order and example
- `spec/formal-grammar.md` line 327: "Condition blocks may nest but MUST NOT overlap."
- `plugins/.../references/syntax-reference.md`: Nested-condition example presented as valid syntax, plus an orphaned paragraph 19 lines below the new prohibition that still described nested block evaluation behavior
- `validate-mdpp.py` silently accepted nested conditions without raising an error (validator enforcement gap — resolved 2026-05-09; see Resolution Update below)

## What Didn't Work

This was a straightforward documentation-correction fix with no failed approaches. The challenge was ensuring full sweep coverage across all four primary spec locations plus secondary plugin reference files. An orphaned contradictory paragraph was missed in the initial pass and caught during code review.

## Solution

Replaced all permissive nesting language with explicit prohibition language and cross-references to logical expressions.

**Before (removed from spec):**
```markdown
Condition blocks MAY be nested within a single file.

<!--condition:web-->
  <!--condition:advanced-->
  Advanced web content.
  <!--/condition-->
<!--/condition-->
```

**After (correct):**
```markdown
Condition blocks MUST NOT nest or overlap. Use logical expressions for
multi-condition logic instead.

<!--condition:web advanced-->
Advanced web content.
<!--/condition-->
```

**Files changed:**

| File | Change |
|------|--------|
| `spec/specification.md` | Replaced lines 576–591 "Nesting" subsection with prohibition + logical-expression cross-reference |
| `spec/processing-model.md` | Replaced lines 193–208 "Nested Conditions" subsection with prohibition language |
| `spec/formal-grammar.md` | Changed line 327 from "may nest but MUST NOT overlap" to "MUST NOT nest or overlap" |
| `references/syntax-reference.md` | Replaced nested example with three flat examples (AND/OR/NOT); removed orphaned contradictory paragraph |
| `references/best-practices.md` | Added note that nesting is not supported |
| `references/error-codes.md` | Updated MDPP001 to state conditions "MUST NOT be nested" |
| `tests/sample-full.md` | Replaced nested condition example with logical AND equivalent |

**Logical expressions cover all nesting use cases:**

| Use case | Syntax |
|----------|--------|
| AND (all must be true) | `<!--condition:web advanced-->` (space-separated) |
| OR (any must be true) | `<!--condition:web,mobile-->` (comma-separated) |
| NOT (must be false) | `<!--condition:!draft-->` (! prefix) |
| Combined | `<!--condition:!draft advanced-->` |

## Why This Works

**Root cause:** Nesting was likely included in early spec drafts when the feature set was still being designed but was intentionally excluded from the final design in favor of logical operators. The logical operator syntax — AND (spaces), OR (commas), NOT (!) — provides complete coverage for all multi-condition scenarios that nesting would have handled, while maintaining simpler parser semantics and clearer document structure. The stale nesting documentation was never updated when the design decision was finalized.

**Why the fix works:** Prohibition language ("MUST NOT") gives implementors and validators an unambiguous normative constraint. Pairing each prohibition with a cross-reference to logical expressions ensures readers have an immediate alternative rather than a dead end.

## Prevention

**Cross-location sweep methodology:** When changing a feature's support status, always run `grep -r "nest" spec/ plugins/` (or the relevant keyword) to find all locations. Spec files and plugin references can drift independently — systematic grep is the only reliable way to catch all occurrences.

**Orphaned-text risk:** After any specification correction, grep for the old permissive claim alongside the new prohibition to catch contradicting text that survived the sweep. In this case, a paragraph in `syntax-reference.md` stating "If the outer condition is Unset, the entire outer block (including nested condition blocks and their tags) passes through without evaluation" appeared 19 lines below the new prohibition — a direct self-contradiction caught only during code review.

**Validator enforcement gap (resolved):** The `validate-mdpp.py` stack algorithm now checks nesting depth at the push site. After each `<!--condition:-->` push, it tests `len(condition_stack) > 1` and raises MDPP001 referencing the outer block's line and expression (`plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py:287-297`). The earlier prescription (a/b alternative — separate MDPP010 vs. extending MDPP001) was decided in favor of (a): nesting detection is folded into MDPP001 with a dedicated message and suggestion to use a logical expression instead.

**Error code documentation accuracy (resolved):** `error-codes.md` MDPP001 wording and validator behavior now agree — both treat nested condition blocks as MDPP001 violations.

**Test cases to add:**
- Valid: Flat AND expression `<!--condition:web advanced-->` (depth 1)
- Valid: Flat OR expression `<!--condition:web,mobile-->` (depth 1)
- Valid: Flat NOT expression `<!--condition:!draft-->` (depth 1)
- Invalid: Nested block `<!--condition:web-->...<!--condition:advanced-->` (depth 2) → should raise MDPP001

## Related Issues

- GitHub issue #71 — Remove nested condition support from spec (this fix)
- `docs/solutions/documentation-gaps/combined-commands-conformance-classification-2026-04-10.md` — Precedent for cross-file RFC 2119 specification corrections; recommended the grep-sweep approach used here
- `docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md` — Documents the condition expression grammar (AND/OR/NOT operator precedence); may still reference the old grammar production permitting nesting
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` — Documents condition evaluation model (Condition State Model: Visible/Hidden/Unset)

## Resolution Update — 2026-05-09

The two open items flagged in the Prevention section are now closed:

- **Validator enforcement** lives at `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py:287-297`. After the push that opens a condition block, the validator inspects `condition_stack`; depth > 1 raises MDPP001 with the outer block's line and expression in the message, and a suggestion to fold the conditions into a single logical expression.
- **Error-code wording and validator behavior** are aligned: `references/error-codes.md` MDPP001 says conditions "MUST NOT be nested," and the validator now enforces that exact rule under MDPP001 (the alternative MDPP010 path was not taken).

Spec files (`spec/specification.md:545,607-609`, `spec/processing-model.md:223-225`, `spec/formal-grammar.md:327`) consistently use the "MUST NOT nest or overlap" phrasing.
