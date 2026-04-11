---
title: "fix: Replace silent discard language with PassThrough marker injection for unrecognized combined command segments"
type: fix
status: active
date: 2026-04-10
origin: docs/brainstorms/2026-04-10-passthrough-marker-injection-requirements.md
---

# fix: Replace silent discard language with PassThrough marker injection for unrecognized combined command segments

## Overview

The spec incorrectly describes unrecognized segments in combined commands as "silently discarded, functioning as inline comments." The correct behavior — matching the implementation — is that unrecognized segments are collected and injected as **PassThrough markers** attached to the target element. All six incorrect locations across `spec/specification.md` and `spec/formal-grammar.md` must be updated.

## Problem Frame

This is a spec-vs-implementation divergence. The PassThrough marker injection behavior is intentional design: it provides an invisible means for authors to embed metadata (status notes, review flags, tracking info) in rendered output. The spec language describes the opposite behavior (silent discard), which is incorrect and misleading to implementors. (see origin: `docs/brainstorms/2026-04-10-passthrough-marker-injection-requirements.md`)

## Requirements Trace

- R1. All references to "silently discarded" or "inline comments" for unrecognized combined command segments replaced with PassThrough marker injection behavior
- R2. Formal grammar `unrecognized_text` production comment reflects PassThrough injection
- R3. Validation table example describes correct behavior (PassThrough marker, not discarded inline comment)
- R4. Spec states that rendering of PassThrough marker content from unrecognized segments is implementation-defined

## Scope Boundaries

- No changes to PassThrough marker behavior itself
- No changes to combined command parsing rules
- No changes to the `unrecognized_text` grammar production (only its descriptive comment)

## Context & Research

### Relevant Code and Patterns

- `spec/specification.md` section 11.3 defines Passthrough marker semantics — the replacement language must be consistent with this terminology
- `spec/specification.md` section 16.4 covers unrecognized segments in combined commands
- `spec/formal-grammar.md` defines the `unrecognized_text` production and its descriptive comments
- Existing spec uses "PassThrough" (PascalCase) when referring to the marker injection behavior and "Passthrough" when referring to the marker key name — both conventions appear in the spec

### Institutional Learnings

- No prior solutions documented for this specific issue

## Key Technical Decisions

- **Use "PassThrough markers" (PascalCase, two words):** Consistent with how the spec refers to the injection mechanism in section 16.4 and the formal grammar
- **Add "implementation-defined" qualifier:** The rendering of PassThrough marker content is left to the processor, which must be stated explicitly per R4
- **Preserve existing example text:** The example `TODO: add Keywords markers` / `TODO: add markers` is retained — only the description of what happens to it changes

## Implementation Units

- [ ] **Unit 1: Update specification.md (2 locations)**

**Goal:** Replace incorrect "silently discarded" / "inline comments" language in specification.md with PassThrough marker injection semantics

**Requirements:** R1, R4

**Dependencies:** None

**Files:**
- Modify: `spec/specification.md` (section 5.3, ~line 214; section 16.4, ~line 1024)

**Approach:**
- Section 5.3: Replace the sentence about silent discard with language describing PassThrough marker injection and implementation-defined rendering
- Section 16.4: Replace the processor conformance requirement from "silently ignore" to "collect for injection as PassThrough markers"; update the example description from "discarded" to "injected as a PassThrough marker"

**Patterns to follow:**
- Match terminology from section 11.3 (Passthrough Marker) for consistency
- Use RFC 2119 language (MUST) consistent with existing conformance requirements

**Verification:**
- No instance of "silently discarded" or "inline comments" in reference to unrecognized combined command segments
- Language is consistent with existing Passthrough marker terminology in section 11.3

- [ ] **Unit 2: Update formal-grammar.md (4 locations)**

**Goal:** Replace incorrect "silently discarded" / "inline comments" language in formal-grammar.md with PassThrough marker injection semantics

**Requirements:** R1, R2, R3

**Dependencies:** None (can be done in parallel with Unit 1)

**Files:**
- Modify: `spec/formal-grammar.md` (~lines 137, 168, 415, 537)

**Approach:**
- Line 137: Replace command list description from "inline comments" to PassThrough marker injection with implementation-defined rendering
- Line 168: Update validation table row from "discarded inline comment" to "PassThrough marker injection"
- Line 415: Update PEG comment from "inline comments" to "PassThrough marker injection"
- Line 537: Update edge case description from "discarded segment" to "injected as a PassThrough marker"

**Patterns to follow:**
- Match terminology used in the EBNF and PEG sections for consistency

**Verification:**
- No instance of "silently discarded" or "inline comments" in reference to unrecognized combined command segments
- Validation table correctly describes PassThrough marker injection
- PEG grammar comment reflects the correct behavior

## Risks & Dependencies

- **Terminology consistency:** The spec uses both "PassThrough" and "Passthrough" in different contexts. The replacement text must use the correct casing for each context (PascalCase "PassThrough" for the injection mechanism).

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-10-passthrough-marker-injection-requirements.md](../brainstorms/2026-04-10-passthrough-marker-injection-requirements.md)
- Related code: `spec/specification.md` sections 5.3, 11.3, 16.4
- Related code: `spec/formal-grammar.md` command list and PEG grammar sections
