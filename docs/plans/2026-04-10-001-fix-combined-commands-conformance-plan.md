---
title: "fix: Promote combined commands from OPTIONAL to REQUIRED conformance"
type: fix
status: completed
date: 2026-04-10
---

# fix: Promote combined commands from OPTIONAL to REQUIRED conformance

## Overview

Combined commands (semicolon-separated directives in a single HTML comment) are classified as OPTIONAL in the processing model, but they are structurally necessary for the format and used throughout the spec's own normative examples. This plan promotes them to REQUIRED and relaxes the evaluation order from MUST to RECOMMENDED per maintainer feedback.

## Problem Frame

The attachment rule means only the comment immediately before an element attaches to it. Stacking two separate comments orphans the top one. Without combined commands, there is no way to apply both a style and an alias (or style + marker, or any multi-directive combination) to the same element. The spec itself uses combined commands throughout its normative examples — the heading pattern `<!-- style:Heading2 ; #200010 -->` appears dozens of times. A processor that omits combined commands would be "conformant" but unable to handle the spec's own recommended patterns.

Maintainer feedback (PR #74): the evaluation order listed in the spec is a recommendation for readability, not a conformance requirement. Processors may evaluate segments in any order.

## Requirements Trace

- R1. `processing-model.md` moves combined commands from the optional features list to the required features list
- R2. `specification.md` section 16.5 no longer says "classified as an OPTIONAL feature"
- R3. The conformance statement in `processing-model.md` reflects the change
- R4. Evaluation order is RECOMMENDED, not MUST (maintainer feedback)

## Scope Boundaries

- No changes to combined command syntax or semantics
- No new combined command features
- No changes to the evaluation order table itself — only the normative language around it

## Context & Research

### Relevant Code and Patterns

- `spec/processing-model.md` — Required Features list (line ~525), Optional Features list (line ~538), Combined Command Evaluation Order section (line ~391)
- `spec/specification.md` — Section 16.5 Conformance Note (line ~1033)
- Existing pattern: required features are numbered items under `### Required Features`, optional under `### Optional Features`

## Key Technical Decisions

- **Promote to Required, not remove from Optional**: Combined commands move to item 12 in the Required Features list. The Optional Features list renumbers accordingly. (see R1, R3)
- **Relax evaluation order to RECOMMENDED**: Per maintainer feedback, the evaluation order is a readability recommendation, not a conformance mandate. Uses SHOULD/RECOMMENDED/MAY language per RFC 2119 conventions. (see R4)

## Implementation Units

- [x] **Unit 1: Promote combined commands in processing-model.md**

  **Goal:** Move combined commands from Optional to Required features list; relax evaluation order language.

  **Requirements:** R1, R3, R4

  **Dependencies:** None

  **Files:**
  - Modify: `spec/processing-model.md`

  **Approach:**
  - Add item 12 to Required Features: "Combined commands — Semicolon-separated commands in a single comment tag. The evaluation order listed in Combined Command Evaluation Order is RECOMMENDED for readability but not required; processors MAY evaluate segments in any order."
  - Remove combined commands from Optional Features; renumber remaining items
  - Change evaluation order section from "MUST evaluate" to "SHOULD evaluate... Processors MAY evaluate segments in any order"

  **Patterns to follow:**
  - Existing numbered items in Required Features list
  - RFC 2119 keyword conventions used throughout the spec

  **Verification:**
  - Combined commands appear in Required Features as item 12
  - Optional Features no longer mentions combined commands
  - Evaluation order section uses SHOULD/MAY language

- [x] **Unit 2: Update specification.md section 16.5**

  **Goal:** Update the conformance note to reflect REQUIRED status and RECOMMENDED evaluation order.

  **Requirements:** R2, R4

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `spec/specification.md`

  **Approach:**
  - Change "classified as an OPTIONAL feature" to "classified as a REQUIRED feature"
  - Change link target from `#optional-features` to `#required-features`
  - Change "MUST evaluate them in the order specified above" to RECOMMENDED language

  **Verification:**
  - Section 16.5 says REQUIRED with correct link to `processing-model.md#required-features`
  - Evaluation order is RECOMMENDED, not MUST

## Risks & Dependencies

- Low risk — this is a documentation/specification change only with no code impact
- The version bump (1.1.9 → 1.1.10) is already included in the branch

## Sources & References

- Related issue: quadralay/markdown-plus-plus#68
- Related PR: quadralay/markdown-plus-plus#74
- Maintainer feedback on evaluation order: PR #74 comment thread
