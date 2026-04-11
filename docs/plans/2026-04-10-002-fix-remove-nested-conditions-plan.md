---
title: "fix: Remove nested condition support from spec"
type: fix
status: completed
date: 2026-04-10
---

# fix: Remove nested condition support from spec

## Overview

Remove all references to condition block nesting from the Markdown++ specification and replace them with cross-references to logical expressions (AND/OR/NOT operators), which are the intended mechanism for multi-condition logic.

## Problem Frame

The spec claimed in multiple locations that condition blocks may be nested within a single file. This is incorrect — condition nesting is not a Markdown++ feature. Supporting nested conditions creates unnecessary complexity for both parsers and document maintainers. The logical expression syntax (`space` for AND, `,` for OR, `!` for NOT) already covers all practical multi-condition scenarios and is simpler to write, read, parse, and maintain.

Four locations in the spec asserted nesting support:

1. `spec/specification.md` — "Condition blocks MAY nest but MUST NOT overlap" and a full "Nesting" subsection with example
2. `spec/processing-model.md` — "Nested Conditions" subsection with example
3. `spec/formal-grammar.md` — "Condition blocks may nest but MUST NOT overlap"
4. Plugin reference files echoing the nesting capability

## Requirements Trace

- R1. The "Nesting" subsection in specification.md is replaced with a note that nesting is not supported, cross-referencing logical expressions
- R2. The "Nested Conditions" subsection in processing-model.md is replaced similarly
- R3. formal-grammar.md no longer says condition blocks may nest
- R4. A brief note explains that logical expressions (AND/OR/NOT) replace the need for nesting
- R5. No remaining text in the spec suggests condition nesting is supported
- R6. Plugin reference files (syntax-reference, best-practices, error-codes, sample-full) are updated consistently

## Scope Boundaries

- Out of scope: Changing condition expression syntax or operators
- Out of scope: Modifying cross-file condition span rules (MDPP012)
- Out of scope: Changes to the validation script logic

## Context & Research

### Relevant Code and Patterns

- `spec/specification.md` Section 11 — Conditions: expression operators, nesting subsection, block/inline usage
- `spec/processing-model.md` Section on condition evaluation: expression operators, nested conditions subsection
- `spec/formal-grammar.md` — Condition pairing structural constraint
- `plugins/.../references/syntax-reference.md` — Nesting Conditions subsection and common mistakes table
- `plugins/.../references/best-practices.md` — Conditions avoidance list
- `plugins/.../references/error-codes.md` — MDPP001 description
- `plugins/.../tests/sample-full.md` — Nested conditions test section

### Institutional Learnings

No prior solutions docs specifically address condition nesting. The design rationale is clear from the issue: logical expressions are strictly more maintainable than nesting for all practical use cases.

## Key Technical Decisions

- **Replace, don't just delete:** Each nesting reference is replaced with a normative "MUST NOT nest" statement plus a cross-reference to logical expressions, so the spec is explicit about the constraint rather than silent
- **Preserve section headers:** The "Nesting" subsection headers are kept (rather than deleted) to make the constraint discoverable — readers looking for nesting info will find the prohibition
- **Update plugin references consistently:** All plugin documentation that mentioned nesting is updated to match the spec

## Implementation Units

- [x] **Unit 1: Update spec/specification.md**

**Goal:** Remove nesting support claims and add prohibition with logical expression cross-reference

**Requirements:** R1, R4, R5

**Dependencies:** None

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- Line 544: Change "MAY nest but MUST NOT overlap" to "MUST NOT nest or overlap"
- Lines 576-591: Replace the Nesting subsection's multi-paragraph explanation and code example with a single normative paragraph stating "MUST NOT be nested" and cross-referencing Expression Operators

**Verification:**
- No text in specification.md suggests nesting is supported
- The Nesting subsection clearly prohibits nesting and points to logical expressions

- [x] **Unit 2: Update spec/processing-model.md**

**Goal:** Remove nested conditions subsection and replace with prohibition

**Requirements:** R2, R4, R5

**Dependencies:** None

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Lines 193-208: Replace the "Nested Conditions" subsection (including its multi-line code example and explanation) with a single normative paragraph under the heading "Nesting" that states "MUST NOT be nested" and cross-references Condition Expression Operators

**Verification:**
- No text in processing-model.md suggests nesting is supported
- The replacement text cross-references logical expressions

- [x] **Unit 3: Update spec/formal-grammar.md**

**Goal:** Fix condition pairing constraint to prohibit nesting

**Requirements:** R3, R5

**Dependencies:** None

**Files:**
- Modify: `spec/formal-grammar.md`

**Approach:**
- Line 327: Change "may nest but MUST NOT overlap" to "MUST NOT nest or overlap"

**Verification:**
- The condition pairing paragraph explicitly prohibits nesting

- [x] **Unit 4: Update plugin reference files**

**Goal:** Align all plugin documentation with the updated spec

**Requirements:** R5, R6

**Dependencies:** Units 1-3 (spec is source of truth)

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-full.md`

**Approach:**
- syntax-reference.md: Replace "Nesting Conditions" subsection with "Multi-Condition Logic" showing AND/OR/NOT examples; update common mistakes table to list nested conditions as an error
- best-practices.md: Change "Deeply nested conditions" avoidance to "Nesting condition blocks (not supported)"
- error-codes.md: Update MDPP001 description to say pairs "MUST NOT be nested"
- sample-full.md: Replace nested condition test case with logical expression equivalents

**Verification:**
- No plugin reference text suggests condition nesting is supported
- syntax-reference.md shows logical expressions as the multi-condition mechanism
- sample-full.md demonstrates AND logic instead of nesting

- [x] **Unit 5: Version bump**

**Goal:** Bump patch version for spec correction

**Requirements:** Repository convention

**Dependencies:** Units 1-4

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

**Approach:**
- Bump patch version from 1.1.11 to 1.1.12

**Verification:**
- Both version files show 1.1.12

## Risks & Dependencies

- **Low risk:** These are documentation-only changes with no runtime impact
- **Consistency check:** After all changes, a grep for "nest" in spec and plugin files should show only prohibition language or references to other types of nesting (tables, indentation)

## Sources & References

- Related issue: #71
- Design rationale: Logical expressions (`space` for AND, `,` for OR, `!` for NOT) cover all practical multi-condition scenarios
