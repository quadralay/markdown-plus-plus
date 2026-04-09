---
title: "docs: Define custom alias priority over auto-generated heading aliases"
type: docs
status: completed
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-custom-alias-priority-requirements.md
---

# docs: Define custom alias priority over auto-generated heading aliases

## Overview

Define the priority rule when a custom Markdown++ alias (`<!-- #name -->`) on one element collides with an auto-generated heading alias on a different element. Custom aliases always win, and the displaced auto-generated alias receives a counter suffix. This completes the collision matrix: auto-auto (#53), custom-custom (MDPP008), and now custom-auto.

## Problem Frame

Issue #53 resolved auto-generated vs. auto-generated heading alias collisions with counter-suffix disambiguation. But a separate collision case remained unspecified: when a custom alias (`<!-- #setup -->`) on one element produces the same identifier as an auto-generated heading slug (`setup` from `## Setup`) on a different element. Without a defined priority rule, two independent implementations could resolve this differently, breaking cross-reference interoperability.

(see origin: [docs/brainstorms/2026-04-08-custom-alias-priority-requirements.md](../brainstorms/2026-04-08-custom-alias-priority-requirements.md))

## Requirements Trace

- R1. Custom alias MUST take priority over auto-generated heading alias when they produce the same identifier
- R2. Displaced auto-generated alias MUST receive a counter suffix using the same algorithm as duplicate auto-generated resolution
- R3. Resolution MUST be silent -- no diagnostic emitted (contrast with MDPP008 for custom-custom collisions)
- R4. At least one worked example showing custom-vs-auto collision and resolution
- R5. Consistent with alias supplement semantics (#18) -- coexistence when no collision, priority when collision

## Scope Boundaries

- Auto-generated vs. auto-generated collisions -- covered by #53
- Custom vs. custom alias collisions -- covered by MDPP008
- Changes to the ePublisher parser implementation

## Context & Research

### Relevant Code and Patterns

- `spec/element-interactions.md` -- Heading Alias Auto-Generation section, specifically the `### Duplicate Alias Resolution` subsection and its `#### Interaction with Custom Aliases` sub-subsection. The new content extends this hierarchy
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` -- "Alias vs. Heading IDs" paragraph in the alias section (line ~444)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` -- MDPP008 entry with existing note distinguishing custom from auto-generated aliases (line ~258)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py` -- `make_unique_alias` function (lines 84-92) implements the counter-suffix algorithm

### Institutional Learnings

- `docs/solutions/documentation-gaps/heading-alias-collision-resolution-2026-04-08.md` -- Established the counter-suffix pattern, global uniqueness requirement, and silent resolution precedent. Prevention principle: "When defining single-element behavior, always ask what happens when multiple elements produce the same output."
- `docs/solutions/documentation-gaps/element-interactions-spec-gap-2026-04-08.md` -- Established the Heading Alias Auto-Generation section structure that this work extends. Prevention: review formulas against examples as a standard step.

## Key Technical Decisions

- **Custom aliases always win**: Custom aliases are intentional authorial choices; auto-generated aliases are derived and fragile. "Document order wins" was considered and rejected because it would allow incidental heading slugs to displace intentional anchors. (see origin)
- **Displaced alias is suffixed, not dropped**: Dropping the auto-generated alias would leave the heading without an auto-generated anchor, breaking cross-references. Suffixing preserves addressability while respecting the custom alias claim.
- **Silent resolution (no diagnostic)**: Consistent with auto-auto collision handling from #53. The author chose the custom alias name deliberately; the processor adjusts without complaint. Contrasts with MDPP008 which treats custom-custom duplicates as errors.
- **Process custom aliases first**: A conformant processor MUST resolve custom aliases before auto-generated heading aliases during Phase 2. This ensures deterministic results regardless of document order.

## Open Questions

### Resolved During Planning

- **Should the displaced alias be dropped or suffixed?** Suffixed -- dropping would break addressability. The heading retains an auto-generated anchor, just suffixed. (see origin R2)
- **Should a diagnostic be emitted?** No -- silent resolution, consistent with auto-auto collisions. Custom alias is intentional, not a mistake to warn about. (see origin R3)

### Deferred to Implementation

- None -- all decisions are resolved.

## Implementation Units

- [x] **Unit 1: Add Custom Alias Priority subsection to spec**

**Goal:** Define normative custom-vs-auto collision priority rules in `spec/element-interactions.md`

**Requirements:** R1, R2, R3, R4, R5

**Dependencies:** None (builds on existing Duplicate Alias Resolution subsection from #53)

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- Add `#### Custom Alias Priority` subsection after the existing `#### Interaction with Custom Aliases` sub-subsection within `### Duplicate Alias Resolution`
- Define core normative rule: custom alias takes priority, displaced auto-generated alias MUST receive counter suffix
- Add rationale paragraph distinguishing intentional (custom) from incidental (auto-generated) aliases
- State silent resolution rule with MDPP008 contrast
- Add `##### Processing Order` sub-subsection: MUST resolve custom aliases before auto-generated during Phase 2
- Add `##### Example` with two-heading scenario: `<!-- #setup -->` on `## Installation` displacing `## Setup`'s auto-generated alias to `setup-2`, with alias results table
- Add `##### Interaction with Duplicate Auto-Generated Resolution` showing composed scenario with three headings (both collision types in one document)

**Patterns to follow:**
- RFC 2119 normative language throughout `spec/element-interactions.md`
- Example/table format matching existing Duplicate Alias Resolution examples
- Section hierarchy pattern: `####` for the subsection, `#####` for sub-subsections (matching sibling sections)

**Test scenarios:**
- Two-heading case: custom alias `<!-- #setup -->` on heading A collides with auto-generated `setup` from heading B -- heading B gets `setup-2`
- Three-heading composed case: custom alias claims `setup`, first `## Setup` gets `setup-2`, second `## Setup` gets `setup-3`
- Heading with custom alias retains both its auto-generated alias and the custom alias (supplement semantics)

**Verification:**
- MUST/MUST NOT keywords used correctly per RFC 2119
- Example tables show unambiguous alias assignments for all headings
- Custom alias interaction example is consistent with the Relationship to Custom Aliases section
- Processing order requirement ensures deterministic results regardless of document order

- [x] **Unit 2: Update supporting references**

**Goal:** Cross-reference the new spec section from syntax-reference.md and error-codes.md

**Requirements:** R3, R5

**Dependencies:** Unit 1

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`

**Approach:**
- syntax-reference.md: Expand the "Alias vs. Heading IDs" paragraph to mention custom alias priority and add cross-reference link to `#custom-alias-priority`
- error-codes.md: Expand the MDPP008 note to clarify that auto-generated aliases colliding with custom aliases are silently disambiguated (not MDPP008 errors), with cross-reference link

**Patterns to follow:**
- Existing cross-reference style in syntax-reference.md (inline links to spec sections)
- error-codes.md note format matching other clarifying notes in the document

**Verification:**
- Both files link back to the Custom Alias Priority section in the spec
- MDPP008 note clearly distinguishes custom alias errors (MDPP008) from silent custom-vs-auto resolution

- [x] **Unit 3: Document solution**

**Goal:** Record the custom alias priority resolution as an institutional learning

**Requirements:** None (knowledge preservation)

**Dependencies:** Unit 1

**Files:**
- Create: `docs/solutions/documentation-gaps/custom-alias-priority-resolution-2026-04-08.md`

**Approach:**
- Follow the existing solutions document format (YAML frontmatter with `problem_type`, `root_cause`, `resolution_type`, `severity`, `tags`)
- Document the collision matrix completeness principle as a prevention measure
- Cross-reference issues #55, #53, #18, #9

**Patterns to follow:**
- `docs/solutions/documentation-gaps/heading-alias-collision-resolution-2026-04-08.md` format and structure

**Verification:**
- Solution document captures the "intentional vs. incidental" design rationale
- Prevention section documents the collision matrix completeness principle

- [x] **Unit 4: Version bump**

**Goal:** Bump patch version for the documentation update

**Requirements:** None (housekeeping)

**Dependencies:** Units 1-3

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

**Approach:**
- Run `scripts/bump-version.sh patch`

**Verification:**
- Both files show the same incremented patch version

## Risks & Dependencies

- **Low risk**: All decisions are resolved in the requirements document. The implementation pattern is identical to the #53 work.
- **Dependency on #53**: The Duplicate Alias Resolution subsection from #53 must exist as the insertion point. This is already merged.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-custom-alias-priority-requirements.md](../brainstorms/2026-04-08-custom-alias-priority-requirements.md)
- Related plan: [docs/plans/2026-04-08-004-docs-heading-alias-collision-plan.md](2026-04-08-004-docs-heading-alias-collision-plan.md) (issue #53 -- structural pattern to follow)
- Related learning: [heading-alias-collision-resolution](../solutions/documentation-gaps/heading-alias-collision-resolution-2026-04-08.md)
- Related learning: [element-interactions-spec-gap](../solutions/documentation-gaps/element-interactions-spec-gap-2026-04-08.md)
- Related issues: #55, #53, #18, #9
