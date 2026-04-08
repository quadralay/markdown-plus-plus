---
title: "feat: Add cross-file link reference resolution specification"
type: feat
status: completed
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-cross-file-link-resolution-requirements.md
---

# feat: Add cross-file link reference resolution specification

## Overview

Create `spec/cross-file-link-resolution.md` -- the normative specification for how link reference definitions resolve across files in a multi-file Markdown++ document assembly. This formalizes the resolution algorithm that emerges from the existing two-phase processing model: include expansion assembles a single text, CommonMark parsing resolves link references at document scope. The spec makes this behavior explicit and defines conflict resolution rules, scope visibility, and diagnostic reporting.

## Problem Frame

Markdown++ enables multi-file document assembly through `<!-- include: -->` directives and provides a semantic cross-reference pattern using CommonMark link reference definitions bridged to alias IDs. The whitepaper says "the publishing tool resolves `[getting-started]` across all included files" but does not define the resolution algorithm. Without a specification, implementors must guess at scope visibility, conflict behavior, include ordering effects, and whether resolution is per-file or document-global.

The processing model (`spec/processing-model.md`) already establishes that Phase 1 assembles all includes into a single text and Phase 2 parses that text as CommonMark. Link reference definitions are a CommonMark construct resolved during Phase 2. The answers to the four open questions follow directly from this architecture -- they just need to be explicitly specified.

(see origin: [docs/brainstorms/2026-04-08-cross-file-link-resolution-requirements.md](../brainstorms/2026-04-08-cross-file-link-resolution-requirements.md))

## Requirements Trace

- R1. Link reference resolution is document-global after assembly (consequence of two-phase model)
- R2. Link reference definitions from any included file are visible to the parent, siblings, and descendants
- R3. First-definition-wins for duplicate slugs (follows CommonMark 0.30 section 4.7)
- R4. Assembled document order is determined by depth-first recursive include expansion
- R5. Warning diagnostic MDPP014 for cross-file duplicate slugs
- R6. Link reference resolution belongs in Phase 2 (no new processing phase)
- R7. Conditions can control which link reference definitions are active
- R8. Variables in link reference definitions are substituted in Phase 1, Step 2
- R9. At least two worked examples (sibling visibility + conflict resolution)
- R10. Syntax reference updated with cross-file resolution behavior
- R11. Spec references the processing model for include expansion mechanics

## Scope Boundaries

- **In scope**: Link reference resolution algorithm, scope visibility, conflict rules, interaction with includes/conditions/variables, worked examples, MDPP014 diagnostic
- **Out of scope**: Changes to the ePublisher parser implementation
- **Out of scope**: Footnote resolution semantics (separate concern)
- **Out of scope**: Heading alias auto-generation algorithm (covered by #9)
- **Out of scope**: Redefining CommonMark link reference syntax
- **Out of scope**: Per-file link reference scoping (contradicts the processing model)

## Context & Research

### Relevant Code and Patterns

- `spec/processing-model.md` -- Two-phase pipeline that this spec builds on. Phase 1, Step 1 defines depth-first recursive include expansion. Phase 2 defines CommonMark 0.30 parsing. The processing model uses RFC 2119 language, numbered requirements, MDPP diagnostic codes, and edge cases with concrete examples.
- `spec/attachment-rule.md` -- Established the spec document pattern: core definition, formal statement, edge cases with wrong/right examples, and cross-references to other specs.
- `spec/formal-grammar.md` -- Covers syntax only, deferring semantic processing to the processing model. Confirms cross-file resolution is a semantic concern, not a syntactic one.
- `examples/semantic-cross-references.md` -- Demonstrates the three-part cross-reference pattern (combined command + heading + link reference definition) with alias IDs #200001-#200005.
- `examples/includes-and-conditions.md` -- Shows file assembly with includes and cross-references using semantic slugs.
- `plugins/.../references/syntax-reference.md` line 384 -- Current note that link references are "supported but generally not recommended" with pointer to best-practices.
- `plugins/.../references/best-practices.md` lines 501-546 -- "Advanced Patterns > Link References" section with guidance on when to use link references, currently silent on cross-file behavior.

### Institutional Learnings

- **Spec-first pattern**: Every spec document (attachment-rule, processing-model, formal-grammar) followed the same workflow: requirements doc → plan → spec → syntax reference/best-practices updates. This work follows that pattern.
- **Single source of truth**: Define normative rules in one spec-grade document; all other documents cross-reference it. The syntax reference and best-practices should point to the spec, not duplicate it.
- **Edge case inventory before writing**: Enumerate all edge cases before drafting prose. The attachment rule solution emphasizes this approach.
- **MDPP code discipline**: Codes assigned sequentially. Next available: MDPP014.
- **Processing model dependency**: The processing model solution doc (`docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`) explicitly lists issue #22 as a downstream dependency.

### External References

Skipping external research -- the codebase has strong local patterns for spec writing, and cross-file link reference resolution follows directly from CommonMark 0.30 section 4.7 (link reference definition semantics). No external framework docs needed.

## Key Technical Decisions

- **Standalone spec document**: Create `spec/cross-file-link-resolution.md` rather than appending to `spec/processing-model.md`. Rationale: the processing model is already ~515 lines, and each existing spec document covers one well-defined concern. A standalone document is consistent with how the project organizes spec content.

- **Document-global scope**: Link references are resolved on the assembled document, not per-file. Rationale: the processing model establishes that Phase 2 operates on a single assembled text. Per-file resolution would require a new processing phase and would break the semantic cross-reference pattern.

- **First-definition-wins**: Follows CommonMark 0.30 section 4.7 semantics. Rationale: this is what the CommonMark parser does, and it gives authors deterministic control through include ordering.

- **Warning for cross-file duplicates (MDPP014)**: Duplicate slugs across files are warned but not fatal. Rationale: duplicates are likely unintentional, but the deterministic first-wins rule means the document still processes correctly.

- **Inline worked examples**: Examples live inline in the spec document, consistent with how the processing model handles examples (concrete input/expected-output pairs alongside normative rules).

- **Syntax reference gets brief expansion**: The syntax reference Custom Aliases note and best-practices Link References section get brief expansions with cross-references to the spec for normative details. The syntax reference stays focused on syntax, not processing semantics.

## Open Questions

### Resolved During Planning

- **MDPP code number**: MDPP014 -- next available in the sequential registry after MDPP013.
- **Inline vs. separate example files**: Inline examples in the spec, consistent with the processing model's approach.
- **Spec location**: Standalone `spec/cross-file-link-resolution.md` -- consistent with one-concern-per-document pattern.
- **Syntax reference expansion scope**: Brief note in Custom Aliases section + expanded paragraph in best-practices Link References section, both cross-referencing the spec.
- **Link reference definitions inside variable values**: Since variables are substituted in Phase 1 Step 2 and link reference parsing happens in Phase 2, a variable value containing a link reference definition IS recognized. This must be stated explicitly in the spec as an ordering implication.

### Deferred to Implementation

- **Exact edge case wording**: The precise normative language for each edge case will be refined during writing, following the processing model's established tone and RFC 2119 usage.
- **Example file structure**: The exact content of the multi-file worked examples (file names, heading text, alias IDs) will be determined during writing to be clear and self-contained.

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

The spec document follows the resolution pipeline that the processing model already implies:

```
Phase 1, Step 1: Include Expansion
  root.md
    ├── include:chapter-a.md  (depth-first, spliced in order)
    │     └── include:shared-refs.md
    └── include:chapter-b.md

  Result: single assembled text with all content from all files,
          in depth-first include order

Phase 1, Step 2: Variable Substitution
  $base_url; tokens in link reference definitions → resolved to values

Phase 2: CommonMark Parsing
  Link reference definitions collected at document scope
  First-definition-wins for duplicate slugs (CommonMark 0.30 §4.7)
  All [slug] references resolve against the full definition set
```

The "cross-file" behavior is entirely a Phase 1 artifact -- by Phase 2, the parser sees one document. The spec makes this explicit.

## Implementation Units

- [x] **Unit 1: Create `spec/cross-file-link-resolution.md`**

**Goal:** Write the normative specification for cross-file link reference resolution semantics.

**Requirements:** R1, R2, R3, R4, R5, R6, R7, R8, R9, R11

**Dependencies:** None (the processing model spec already exists)

**Files:**
- Create: `spec/cross-file-link-resolution.md`

**Approach:**
- Follow the spec document structure established by `spec/attachment-rule.md` and `spec/processing-model.md`: introduction, definitions, core algorithm, edge cases, error handling, conformance notes
- Use RFC 2119 conformance keywords (MUST, SHOULD, MAY) applied to processors
- Include frontmatter with `date: 2026-04-08` and `status: draft`
- Open with an introduction that establishes the relationship to the processing model and the problem this spec solves
- Define **resolution scope** as document-global after assembly, grounded in the two-phase pipeline
- Define **scope visibility** explicitly: definitions from any included file are visible everywhere in the assembled document
- Define **conflict resolution** as first-definition-wins per CommonMark 0.30 section 4.7, with assembled document order determined by depth-first include expansion
- Document **ordering implications**: conditions can gate definitions (Phase 1 removal), variables in definitions are substituted (Phase 1 Step 2), variable values containing link reference definitions are recognized (Phase 2 parsing)
- Include edge cases with concrete wrong/right examples:
  - Duplicate definitions across sibling includes (first in include order wins)
  - Definition in conditionally-excluded content (not present in assembled text)
  - Variable-substituted URL in a link reference definition
  - Link reference definition in a deeply nested include (visible to root)
- Define MDPP014 diagnostic for cross-file duplicate slug detection

**Patterns to follow:**
- `spec/processing-model.md` for overall structure, tone, normative language, and inline examples
- `spec/attachment-rule.md` for edge case presentation format

**Test scenarios:**
- Reader can determine resolution outcome for any multi-file assembly by following the spec
- All four questions from issue #22 have explicit normative answers
- Ordering implications are consistent with the processing model's existing ordering implications
- MDPP014 is consistent with the diagnostic format and registry conventions

**Verification:**
- The spec document is self-contained: an implementor can read it and the processing model and correctly predict link reference resolution behavior
- The four questions (scope, conflict, order, assembled vs. per-file) all have explicit normative answers
- The rules are consistent with CommonMark 0.30 section 4.7

- [x] **Unit 2: Add worked examples to the spec**

**Goal:** Provide two inline worked examples demonstrating cross-file link reference resolution.

**Requirements:** R9

**Dependencies:** Unit 1 (the spec structure must exist)

**Files:**
- Modify: `spec/cross-file-link-resolution.md`

**Approach:**
- Example A: Multi-file assembly where a reference in one included file resolves to a link reference definition in a sibling include, demonstrating document-global visibility. Show the root file, two sibling includes, the assembled text, and the resolution outcome.
- Example B: Conflict scenario where two included files define the same slug with different targets, demonstrating first-definition-wins based on include order. Show the root file with two includes, both defining the same slug, the assembled text, which definition wins, and the MDPP014 diagnostic.
- Each example should show: source files → assembled text after Phase 1 → resolution outcome in Phase 2

**Patterns to follow:**
- `spec/processing-model.md` edge case format: concrete input, expected output, explanation
- `examples/semantic-cross-references.md` for the three-part cross-reference pattern

**Test scenarios:**
- Examples are detailed enough to serve as conformance test inputs
- Examples use realistic file structures and the established cross-reference pattern

**Verification:**
- Each example shows the complete resolution chain from source files through assembly to resolved references
- The conflict example clearly shows which definition wins and why

- [x] **Unit 3: Register MDPP014 in the processing model diagnostic registry**

**Goal:** Add MDPP014 to the MDPP diagnostic code registry in `spec/processing-model.md`.

**Requirements:** R5

**Dependencies:** Unit 1 (the diagnostic must be defined in the new spec first)

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Add a new row to the Processing-Phase Codes table after MDPP013
- Follow the existing table format: Code, Description, Severity, Phase, Triggering Condition
- Code: MDPP014, Description: "Duplicate link reference slug across files", Severity: Warning, Phase: Phase 2, Triggering Condition: "Two or more link reference definitions with the same slug originate from different source files in the assembled document"
- Update the "Implementations MAY define additional diagnostic codes" note if needed (currently says MDPP100+, which remains correct)

**Patterns to follow:**
- Existing MDPP010-MDPP013 entries in the Processing-Phase Codes table

**Test scenarios:**
- MDPP014 appears in the registry with correct severity and triggering condition
- The code number is sequential (follows MDPP013)

**Verification:**
- The diagnostic code registry is complete and sequential through MDPP014
- The triggering condition accurately reflects the spec's conflict detection rule

- [x] **Unit 4: Update syntax reference and best-practices**

**Goal:** Update the syntax reference Custom Aliases note and the best-practices Link References section to describe cross-file resolution behavior.

**Requirements:** R10

**Dependencies:** Unit 1 (the spec must exist to cross-reference)

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`

**Approach:**
- **Syntax reference** (line 384): Expand the existing note about reference-style links. Add a sentence explaining that in multi-file assemblies, link reference definitions from all included files are visible throughout the assembled document. Cross-reference `spec/cross-file-link-resolution.md` for normative resolution semantics.
- **Best-practices** (lines 501-546): Add a new subsection or paragraph under "When link references may be useful" that describes the cross-file use case -- the semantic cross-reference pattern where link reference definitions bridge slugs to alias IDs across included files. Briefly mention first-definition-wins for conflicts. Cross-reference the spec for full rules.
- Keep both updates brief and focused -- the syntax reference describes what it looks like, best-practices describes when to use it, the spec describes how it works.

**Patterns to follow:**
- Existing cross-references between syntax-reference.md and spec documents (e.g., the attachment rule reference pattern)
- The existing "Note:" format at syntax-reference.md line 384

**Test scenarios:**
- A reader of the syntax reference learns that cross-file resolution exists and where to find the rules
- A reader of best-practices understands when and why to use the cross-reference pattern in multi-file assemblies

**Verification:**
- Both documents cross-reference `spec/cross-file-link-resolution.md`
- The syntax reference remains focused on syntax, not processing semantics
- Best-practices provides actionable guidance without duplicating normative rules

- [x] **Unit 5: Add solution document**

**Goal:** Document the solution for future institutional learning, following the established pattern.

**Requirements:** None (institutional convention)

**Dependencies:** Units 1-4 (all implementation complete)

**Files:**
- Create: `docs/solutions/documentation-gaps/cross-file-link-resolution-semantics-2026-04-08.md`

**Approach:**
- Follow the solution document pattern established by existing files in `docs/solutions/documentation-gaps/`
- Document: Problem (resolution algorithm unspecified), Symptoms (implementors guessing), Solution (spec document defining document-global scope, first-definition-wins, MDPP014), Why This Works (direct consequence of two-phase model), Prevention (spec-first approach for new features)
- Reference issue #22 and related issues (#8, #9, #7)

**Patterns to follow:**
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` for structure and frontmatter

**Test scenarios:**
- Solution document captures the key insight that cross-file resolution is a consequence of the two-phase model, not a separate feature

**Verification:**
- Solution follows the established frontmatter schema and section structure
- Related issues are cross-referenced

## System-Wide Impact

- **Interaction graph**: The new spec interacts with the processing model (Phase 1 include expansion feeds into Phase 2 link resolution), the attachment rule (link reference targets may use alias IDs), and the formal grammar (no changes needed -- link references are CommonMark syntax, not Markdown++ extensions).
- **Error propagation**: MDPP014 is a warning -- it does not halt processing. The first-definition-wins rule ensures deterministic output even with duplicates.
- **API surface parity**: The processing model's conformance section may need a note about cross-file link resolution conformance. This should be evaluated during implementation but is likely unnecessary since link resolution is standard CommonMark behavior.
- **Integration coverage**: The worked examples serve as integration test inputs covering cross-file resolution through the full pipeline.

## Risks & Dependencies

- **Dependency on processing model**: The spec assumes `spec/processing-model.md` is the authoritative source for include expansion and the two-phase pipeline. This dependency is already satisfied (issue #8 is complete).
- **CommonMark 0.30 alignment**: The first-definition-wins rule must match CommonMark 0.30 section 4.7. If a future CommonMark revision changes this behavior, the Markdown++ spec would need updating. Low risk -- this is a stable part of the CommonMark spec.
- **Scope creep**: The spec should not address footnote resolution (separate concern) or heading alias auto-generation (#9). The scope boundaries from the requirements doc must be maintained.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-cross-file-link-resolution-requirements.md](../brainstorms/2026-04-08-cross-file-link-resolution-requirements.md)
- Related code: `spec/processing-model.md` (two-phase pipeline), `spec/attachment-rule.md` (spec pattern), `examples/semantic-cross-references.md` (cross-reference pattern)
- Related issues: #22 (this issue), #8 (processing model -- dependency), #9 (element interactions), #7 (formal specification)
- External docs: [CommonMark 0.30 section 4.7](https://spec.commonmark.org/0.30/#link-reference-definitions)
