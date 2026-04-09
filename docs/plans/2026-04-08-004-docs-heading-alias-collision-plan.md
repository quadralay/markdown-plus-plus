---
title: "docs: Define heading alias collision resolution strategy"
type: docs
status: active
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-heading-alias-collision-requirements.md
---

# docs: Define heading alias collision resolution strategy

## Overview

Define how a conformant Markdown++ processor resolves duplicate auto-generated heading aliases when two or more headings produce the same slug after the 6-step algorithm. The chosen strategy -- counter-suffix disambiguation (`setup`, `setup-2`, `setup-3`) -- is documented in the spec with normative language, a worked example, and cross-references from the SKILL.md, error codes, and syntax reference.

## Problem Frame

When headings like `## Setup` appear multiple times in an assembled document, the auto-generated alias algorithm produces the same slug for each. Without a defined resolution strategy, two independent implementations could produce different aliases for the same document -- breaking cross-references and interoperability.

(see origin: [docs/brainstorms/2026-04-08-heading-alias-collision-requirements.md](../brainstorms/2026-04-08-heading-alias-collision-requirements.md))

## Requirements Trace

- R1. Counter-suffix disambiguation: first heading gets bare alias, second gets `-2`, third gets `-3`, etc.
- R2. First-in-document-order wins the bare alias
- R3. Counter suffixing applies only to auto-generated aliases; custom alias duplicates remain governed by MDPP008
- R4. At least one worked example showing the collision resolution
- R5. Consistent with alias supplement semantics from issue #18

## Scope Boundaries

- Custom alias collisions (`<!-- #name -->` duplicates) -- already covered by MDPP008
- Changes to the ePublisher parser implementation
- Cross-file alias collisions

## Context & Research

### Relevant Code and Patterns

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py` -- `make_unique_alias` function (lines 84-92) implements the counter-suffix strategy starting at `-2`
- `spec/element-interactions.md` -- Heading Alias Auto-Generation section is the insertion point for the new subsection
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` -- MDPP008 entry needs a note distinguishing custom from auto-generated aliases
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` -- Alias section needs cross-reference
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` -- Alias usage section needs summary

### Institutional Learnings

- `docs/solutions/documentation-gaps/element-interactions-spec-gap-2026-04-08.md` -- established the pattern for the Heading Alias Auto-Generation section that this work extends

## Key Technical Decisions

- **Counter starts at -2, not -1**: Matches `add-aliases.py`, GitHub, and GitLab conventions. Starting at -2 avoids ambiguity about whether `-1` means "first duplicate" or "only instance."
- **Silent resolution (no diagnostic)**: Auto-generated collisions are expected in multi-section documents. Unlike MDPP008 (custom alias duplicates = error), auto-generated collisions resolve silently because authors cannot always control heading uniqueness.
- **Document order = assembled document order**: Collision resolution uses the assembled document after Phase 1 processing (include expansion, condition evaluation, variable substitution), following depth-first recursive include expansion.
- **Custom aliases supplement suffixed auto-generated aliases**: A heading with both `<!-- #db-setup -->` and a collision-suffixed auto-generated alias `setup-2` has two valid anchors -- consistent with existing supplement semantics.

## Implementation Units

- [x] **Unit 1: Add Duplicate Alias Resolution subsection to spec**

**Goal:** Define normative collision resolution rules in `spec/element-interactions.md`

**Requirements:** R1, R2, R3, R4, R5

**Dependencies:** None

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- Add `### Duplicate Alias Resolution` subsection after the existing `### Scope` subsection within the Heading Alias Auto-Generation section
- Include three normative rules (first=bare, second=-2, third=-3)
- Define document order as assembled document after Phase 1 processing
- State that resolution is silent (no diagnostic) with explicit contrast to MDPP008
- Add worked example with three `## Setup` headings and an alias results table
- Add `#### Interaction with Custom Aliases` sub-subsection demonstrating supplement behavior with collision-suffixed aliases

**Patterns to follow:**
- RFC 2119 normative language used throughout `spec/element-interactions.md`
- Example/table format matching the existing Heading Alias Auto-Generation examples table

**Verification:**
- The subsection uses MUST/MUST NOT correctly per RFC 2119
- The example table shows unambiguous alias assignments for all headings
- The custom alias interaction example is consistent with the Relationship to Custom Aliases section above it

- [x] **Unit 2: Update supporting references**

**Goal:** Cross-reference the new spec section from SKILL.md, error codes, and syntax reference

**Requirements:** R3, R5

**Dependencies:** Unit 1

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

**Approach:**
- SKILL.md: Add one-paragraph summary of collision behavior to the alias usage section
- error-codes.md: Add note to MDPP008 clarifying it applies only to custom aliases, with link to spec
- syntax-reference.md: Add paragraph in the alias section noting counter-suffix disambiguation with link to spec

**Patterns to follow:**
- Existing cross-reference style in SKILL.md and syntax-reference.md (e.g., "See `spec/element-interactions.md` for...")
- error-codes.md note format matching other clarifying notes

**Verification:**
- All three files link back to the Duplicate Alias Resolution section
- MDPP008 note clearly distinguishes custom alias errors from silent auto-generated resolution

- [x] **Unit 3: Version bump**

**Goal:** Bump patch version for the documentation update

**Requirements:** None (housekeeping)

**Dependencies:** Units 1-2

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

**Approach:**
- Run `scripts/bump-version.sh patch`

**Verification:**
- Both files show the same incremented patch version

## Risks & Dependencies

- None -- all implementation units are complete on the current branch (`916e148`)

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-heading-alias-collision-requirements.md](../brainstorms/2026-04-08-heading-alias-collision-requirements.md)
- Related code: `add-aliases.py:make_unique_alias` (lines 84-92)
- Related issues: #9, #18, #49
- Related learning: [element-interactions-spec-gap](../solutions/documentation-gaps/element-interactions-spec-gap-2026-04-08.md)
