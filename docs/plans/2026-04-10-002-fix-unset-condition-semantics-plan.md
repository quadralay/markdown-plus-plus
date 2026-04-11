---
title: "fix: Revise Unset condition semantics to pass-through instead of truthiness"
type: fix
status: completed
date: 2026-04-10
---

# fix: Revise Unset condition semantics to pass-through instead of truthiness

## Overview

The specification incorrectly applied truthiness/falsy logic to undefined (Unset) conditions, treating Unset as equivalent to Visible in boolean evaluation. Markdown++ does not evaluate undefined conditions — it passes through undefined conditional content and allows the implementation to resolve it downstream. This plan addresses all six locations identified in issue #72 plus the condition set definition, ensuring consistent pass-through semantics throughout the normative specification.

## Problem Frame

The spec defined Unset as a third state that behaved like Visible in all boolean contexts. This would force a processor to silently include content guarded by undefined conditions, masking authoring errors. The correct behavior is pass-through: when a condition name is not defined in the condition set, the processor does not evaluate the expression and preserves the entire condition block (opening tag, content, closing tag) as-is in the output.

## Requirements Trace

- R1. The Unset state definition MUST describe pass-through behavior instead of "included in output"
- R2. The AND/OR/NOT operator tables MUST NOT treat Unset as equivalent to Visible
- R3. A clear statement MUST be added: when a condition expression references an undefined name, the condition block passes through without evaluation
- R4. All six locations from issue #72 MUST be updated consistently
- R5. The `spec/specification.md` condition set definition MUST be updated
- R6. Version bump MUST be included

## Scope Boundaries

- Visible/Hidden semantics are unchanged
- AND/OR/NOT operator syntax is unchanged
- MDPP diagnostic codes for undefined conditions are a separate concern (out of scope)
- Historical brainstorm/plan documents are not updated — they reflect what was believed at the time

## Context & Research

### Relevant Code and Patterns

The fix touches three normative files and two version metadata files:

- `spec/specification.md` — Terminology (line 124), tri-state model table (line 558), expression operators table (lines 568-570)
- `spec/processing-model.md` — Definitions (line 24, 32), tri-state model (line 175), expression operators table (lines 186-187), NOT description (line 191)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` — Tri-state model summary

The existing pattern across both spec documents is consistent: each location that described Unset behavior used "included in output" or "Visible or Unset" phrasing that needed replacement with pass-through language.

### Institutional Learnings

No prior solutions in `docs/solutions/` address this topic.

## Key Technical Decisions

- **Pass-through preserves tags**: The Unset behavior preserves the opening tag, content, AND closing tag as-is. This is critical — it means downstream tools can detect and handle unresolved conditions rather than receiving unmarked content.
- **Any Unset operand triggers pass-through for the entire block**: In compound expressions (AND/OR), if any operand is Unset, the entire block passes through. This avoids partial evaluation of expressions with undefined terms.
- **NOT with Unset also passes through**: `!name` where `name` is Unset does not invert to true — it passes through. This prevents a NOT-undefined condition from silently including content.
- **Condition set definition revised**: The condition set definition was changed from "each assigned one of three states" to "each assigned a state of Visible or Hidden" with Unset described as the absence of definition, not an assigned state.

## Open Questions

### Resolved During Planning

- **Should historical brainstorm/plan documents be updated?** No — they reflect what was believed at the time and are not normative. The spec files are the source of truth.
- **Should the SKILL.md be updated?** Yes — it summarizes the tri-state model for AI-assisted authoring and must reflect the correct semantics.

### Deferred to Implementation

- None — all changes are straightforward text corrections with no runtime unknowns.

## Implementation Units

- [x] **Unit 1: Update condition set definition in specification.md**

**Goal:** Revise the terminology definition so Unset is the absence of assignment, not an assigned state.

**Requirements:** R5

**Dependencies:** None

**Files:**
- Modify: `spec/specification.md` (line 124, terminology section)

**Approach:**
- Change "each assigned one of three states: Visible, Hidden, or Unset" to "each assigned a state of Visible or Hidden. A condition name not present in the set is Unset (undefined)."

**Verification:**
- The condition set definition clearly distinguishes between assigned states (Visible/Hidden) and the absence of assignment (Unset)

- [x] **Unit 2: Update tri-state model and operators in specification.md**

**Goal:** Revise the Unset row in the tri-state table and all three operator rows to describe pass-through instead of inclusion/truthiness.

**Requirements:** R1, R2, R3

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/specification.md` (lines 558, 568-570)

**Approach:**
- Unset table row: Replace "included in output (document-default behavior)" with pass-through language
- Replace the "documents render completely by default" rationale with the MUST NOT evaluate statement
- NOT row: Add "If `name` is Unset, the block passes through"
- AND row: Remove "or Unset" from truthiness, add "If any operand is Unset, the block passes through"
- OR row: Same pattern as AND

**Verification:**
- No mention of Unset being "included" or treated as Visible in any operator description
- Each operator row explicitly states Unset triggers pass-through

- [x] **Unit 3: Update condition set definition in processing-model.md**

**Goal:** Align the processing model's condition set definition with the revised specification.md definition.

**Requirements:** R4, R5

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/processing-model.md` (line 24)

**Approach:**
- Mirror the same definition change as Unit 1

**Verification:**
- Both files use identical condition set definition language

- [x] **Unit 4: Update tri-state model and operators in processing-model.md**

**Goal:** Revise all Unset references in the processing model's condition evaluation section to use pass-through semantics.

**Requirements:** R1, R2, R3, R4

**Dependencies:** Unit 3

**Files:**
- Modify: `spec/processing-model.md` (lines 32, 175, 186-187, 191)

**Approach:**
- Condition state table (line 32): Replace "included in output (document-default behavior)" with pass-through
- Tri-state model prose (line 175): Same replacement
- Replace "documents render completely by default" rationale with MUST NOT evaluate statement
- NOT/AND/OR operator table rows (lines 186-187): Same pattern as Unit 2
- NOT prose (line 191): Remove "or Unset" from the false case, add pass-through sentence

**Verification:**
- All six issue locations updated consistently
- No remaining "Visible or Unset" phrasing in operator definitions

- [x] **Unit 5: Update SKILL.md tri-state summary**

**Goal:** Align the plugin skill's condition model summary with the corrected semantics.

**Requirements:** R1

**Dependencies:** Units 2, 4

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`

**Approach:**
- Replace "Unset conditions default to visible" with pass-through language

**Verification:**
- SKILL.md accurately summarizes the pass-through behavior

- [x] **Unit 6: Version bump**

**Goal:** Bump patch version to reflect the spec correction.

**Requirements:** R6

**Dependencies:** All other units

**Files:**
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Approach:**
- Patch bump from 1.1.11 to 1.1.12 using `scripts/bump-version.sh patch`

**Verification:**
- Both plugin.json and marketplace.json show version 1.1.12

## System-Wide Impact

- **API surface parity:** The SKILL.md (AI skill context) must match the normative spec. Both are updated.
- **Downstream processors:** Any processor implementing the old Unset-as-Visible behavior would need to change to pass-through. This is a spec correction, not a behavioral change for conformant processors — the old spec was wrong.
- **Existing documents:** Documents that relied on Unset-as-Visible behavior (undefined conditions silently including content) would now have that content passed through with tags intact instead. This surfaces previously hidden authoring errors.

## Risks & Dependencies

- **Risk: Historical documents reference old semantics.** Brainstorm and plan files from 2026-04-08 describe Unset as "always render their content." These are non-normative historical artifacts and do not need updating.
- **Classification:** Release blocker — spec correctness issue that must be resolved before the specification can be considered stable.

## Sources & References

- Related issue: #72
- Related commit: `87ed46e fix: revise Unset condition semantics to pass-through instead of truthiness`
- Related code: `spec/specification.md`, `spec/processing-model.md`
