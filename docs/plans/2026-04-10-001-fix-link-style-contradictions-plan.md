---
title: "fix: Resolve contradictory link style examples in specification"
type: fix
status: completed
date: 2026-04-10
---

# fix: Resolve contradictory link style examples in specification

## Overview

Section 9.3 of `spec/specification.md` showed inline link styling with the style tag BEFORE the opening bracket, while section 17.1 of the same document showed the correct form with the style tag INSIDE the brackets. Additionally, both corrected examples were missing delimiters (`*`, `**`, or backtick) around styled text, which are required for the parser to determine style boundaries.

## Problem Frame

Two independent implementors would produce different parsers from the contradictory normative statements. Section 9.3 showed `<!--style:Link-->[here](url)` while section 17.1 showed `[<!--style:CustomLink-->*Link text*](url)`. The `tests/sample-full.md` test fixture also mixed both conventions, compounding the ambiguity.

The normative rule is: for links, the style tag goes inside the link text brackets (the one exception to the general inline placement rule). This is confirmed by `spec/element-interactions.md`, `spec/attachment-rule.md`, and `plugins/.../references/syntax-reference.md`.

## Requirements Trace

- R1. The incorrect example at specification.md section 9.3 uses the inside-brackets form with delimiters
- R2. `tests/sample-full.md` line 58 uses the inside-brackets form with delimiters
- R3. `grep -rn '<!--style:.*-->\[' spec/ examples/ plugins/` returns zero results outside of fenced code blocks
- R4. The normative rule (inside-brackets) is not changed

## Scope Boundaries

- The actual normative rule (inside-brackets is correct) is not changed
- `spec/element-interactions.md` is not modified (already correct)
- `spec/attachment-rule.md` is not modified (already correct)

## Context & Research

### Relevant Code and Patterns

- `spec/specification.md` section 17.1 (lines 1071-1082): Authoritative correct pattern with delimiters
- `spec/element-interactions.md` (links section): Confirms link exception to general inline placement rule
- `spec/attachment-rule.md` (line 17): Documents the link exception clause
- `plugins/.../references/syntax-reference.md` (lines 1014-1024): Correct pattern in reference docs

### Institutional Learnings

- `docs/solutions/documentation-gaps/element-interaction-refinements-2026-04-08.md`: Documents the link style placement exception and recommends comparison tables showing all inline elements' placement rules side by side
- `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`: Warns against maintaining parallel descriptions that inevitably diverge — single source of truth for critical rules
- `docs/solutions/logic-errors/embedded-spaces-in-style-marker-names-2026-04-08.md`: "When one spec document has to explain why another document's rule 'doesn't apply,' that is a strong signal the rule is wrong" — relevant pattern for detecting spec-internal contradictions

## Key Technical Decisions

- **Inside-brackets with delimiters**: The correct form is `[<!--style:Name-->*text*](url)`, not `<!--style:Name-->[text](url)` or `[<!--style:Name-->text](url)`. Delimiters are required for the parser to determine style boundaries.
- **Patch version bump**: This is a spec documentation fix, warranting a patch bump per GOVERNANCE.md versioning rules.

## Implementation Units

- [x] **Unit 1: Fix link style placement**

  **Goal:** Move style tag inside brackets in specification.md section 9.3 and sample-full.md line 58

  **Requirements:** R1, R2, R4

  **Files:**
  - Modify: `spec/specification.md` (section 9.3, line 415)
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-full.md` (line 58)

  **Approach:**
  - Replace `<!--style:Link-->[here](url)` with `[<!--style:Link-->*here*](url)` in specification.md
  - Replace `<!--style:ImportantLink-->[styled link](url)` with `[<!--style:ImportantLink-->*styled link*](url)` in sample-full.md
  - Both corrections add italic delimiters to match the normative pattern in section 17.1

  **Patterns to follow:**
  - Section 17.1 pattern: `[<!--style:CustomLink-->*Link text*](topics/file.md#anchor "Title")`

  **Verification:**
  - R3: `grep -rn '<!--style:.*-->\[' spec/ examples/ plugins/` returns zero results
  - Section 9.3 example matches section 17.1 pattern
  - sample-full.md uses consistent inside-brackets form throughout

- [x] **Unit 2: Version bump**

  **Goal:** Bump patch version for the spec fix

  **Requirements:** Project convention (CLAUDE.md)

  **Files:**
  - Modify: `.claude-plugin/marketplace.json`
  - Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

  **Verification:**
  - Both manifest files show the same incremented patch version

## Risks & Dependencies

- None. This is a self-contained documentation fix with no downstream behavioral impact.

## Sources & References

- Related issue: #64
- Related code: `spec/specification.md` sections 9.3 and 17.1
- Related learning: `docs/solutions/documentation-gaps/element-interaction-refinements-2026-04-08.md`
