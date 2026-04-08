---
date: 2026-04-08
topic: cross-file-link-resolution
---

# Cross-File Link Reference Resolution Semantics

## Problem Frame

Markdown++ enables multi-file document assembly through `<!-- include: -->` directives, and provides a semantic cross-reference pattern using CommonMark link reference definitions bridged to alias IDs. The whitepaper says "the publishing tool resolves `[getting-started]` across all included files" — but no specification defines the resolution algorithm.

Without a specification, implementors must guess at fundamental questions:

1. **Scope visibility** — Are link reference definitions from an included file visible to the parent document? To sibling includes?
2. **Conflict resolution** — What happens when two included files define the same slug with different target IDs?
3. **Include order** — Does the order of includes affect resolution priority?
4. **Assembled vs. per-file** — Are link references resolved within each file individually or after the full document is assembled?

The processing model (`spec/processing-model.md`) already defines a two-phase pipeline: Phase 1 assembles all includes into a single text, Phase 2 parses that text as CommonMark. Link reference definitions are a CommonMark construct resolved during Phase 2 parsing. The answers to these four questions follow directly from the existing architecture — they just need to be explicitly specified.

The ePublisher parser's behavior of inheriting link definitions across the assembled document (parser.py lines 1125-1126) is consistent with this model, but implementation behavior is not specification.

## Requirements

### Resolution scope

- R1. The spec MUST define link reference resolution as **document-global after assembly**. Link reference definitions from all included files are visible throughout the entire assembled document. This is a direct consequence of the two-phase processing model: Phase 1 expands all includes into a single text, Phase 2 parses that text as CommonMark, and CommonMark resolves link reference definitions at document scope.

- R2. The spec MUST state explicitly that a link reference definition in any included file is visible to (a) the parent document, (b) sibling includes, and (c) descendant includes. There is no per-file scoping for link references — the assembled document is one CommonMark document.

### Conflict resolution

- R3. The spec MUST define that when multiple link reference definitions use the same slug, the **first definition in assembled document order wins**. This follows CommonMark 0.30 semantics (section 4.7: "If there are several matching definitions, the first one takes precedence").

- R4. The spec MUST define that assembled document order is determined by the depth-first recursive include expansion specified in the processing model. The order of `<!-- include: -->` directives in a file directly determines which definition takes precedence.

- R5. The spec SHOULD define a diagnostic (e.g., **MDPP014**) emitted when a duplicate link reference slug is detected across different source files. Severity: Warning. Rationale: duplicate slugs across files are likely unintentional and can cause confusing resolution behavior, even though the first-wins rule makes the outcome deterministic.

### Interaction with the processing model

- R6. The spec MUST place link reference resolution within the existing Phase 2 (Markdown Parsing) of the processing model. Link reference definitions are standard CommonMark constructs — not Markdown++ extensions — and are resolved by the CommonMark parser during Phase 2. The spec defines no new processing phase.

- R7. The spec MUST document the interaction between conditions and link references: if a link reference definition appears inside a condition block that evaluates to Hidden, the definition is removed during Phase 1 (per-file condition evaluation) and is not present in the assembled text that Phase 2 parses. This means conditions can control which link reference definitions are active.

- R8. The spec MUST document that variables inside link reference definitions are substituted during Phase 1, Step 2 (variable substitution), before CommonMark parsing. A link reference definition like `[slug]: $base_url;/page "Title"` resolves the variable first, producing a complete URL for CommonMark to parse.

### Worked examples

- R9. The spec MUST include at least two worked examples demonstrating cross-file link reference resolution:
  - (a) A multi-file assembly where a reference in one included file resolves to a link reference definition in a sibling include, showing document-global visibility.
  - (b) A conflict scenario where two included files define the same slug, showing first-definition-wins behavior based on include order.

### Documentation updates

- R10. The syntax reference (`syntax-reference.md`) MUST be updated to describe cross-file resolution behavior in the Custom Aliases and/or Advanced Patterns sections. The current text says link references are "supported but generally not recommended" — this should be expanded to explain how they interact with includes.

- R11. The spec document MUST reference the processing model (`spec/processing-model.md`) for how include expansion creates the assembled document that feeds into link reference resolution.

## Success Criteria

- An implementor can read the spec and correctly predict the outcome of link reference resolution in any multi-file assembly
- The four questions from issue #22 (scope, conflict, order, assembled vs. per-file) all have explicit normative answers
- The resolution rules are consistent with CommonMark 0.30 section 4.7 (link reference definition semantics)
- The resolution rules are consistent with the existing two-phase processing model — no contradictions
- The worked examples are detailed enough to serve as conformance test inputs

## Scope Boundaries

- **In scope**: Link reference resolution algorithm, scope visibility, conflict rules, interaction with includes/conditions/variables, worked examples
- **In scope**: New diagnostic code for cross-file duplicate slugs
- **Out of scope**: Changes to the ePublisher parser implementation
- **Out of scope**: Footnote resolution semantics (separate concern, as noted in issue #22)
- **Out of scope**: Heading alias auto-generation algorithm (covered by #9)
- **Out of scope**: Redefining CommonMark link reference syntax — Markdown++ uses standard CommonMark link references as-is
- **Out of scope**: Per-file link reference scoping — this was considered but rejected because it contradicts the processing model's single-document-after-assembly design

## Key Decisions

- **Document-global after assembly**: Link references are resolved on the assembled document, not per-file. Rationale: the processing model already establishes that Phase 2 operates on a single assembled text. Per-file resolution would require a new processing phase and would break the semantic cross-reference pattern that the whitepaper describes.

- **First-definition-wins for conflicts**: Follows CommonMark 0.30 semantics. Rationale: this is what the CommonMark parser will do anyway, and it gives authors deterministic control through include ordering.

- **Warning diagnostic for cross-file duplicates**: Duplicate slugs across files are warned but not fatal. Rationale: duplicates are likely unintentional, but the deterministic first-wins rule means the document still processes correctly. Halting on duplicate slugs would be too strict for large documentation sets where accidental collisions may occur.

- **No new Markdown++ syntax**: Cross-file link resolution uses existing CommonMark link reference definitions plus existing Markdown++ aliases and includes. No new extension syntax is needed. Rationale: the behavior emerges from combining existing features — adding syntax would be unnecessary complexity.

- **Spec location**: New section within `spec/processing-model.md` or a companion spec document in `spec/`. The resolution algorithm is fundamentally about how the processing model handles CommonMark link references, so it belongs in or near the processing model spec.

## Dependencies / Assumptions

- Assumes the processing model (`spec/processing-model.md`, issue #8) is the authoritative source for include expansion and the two-phase pipeline — this spec builds on it
- Assumes CommonMark 0.30 link reference definition semantics (section 4.7) apply unchanged within Phase 2
- Assumes the existing semantic cross-reference pattern (alias + slug + link reference definition) as shown in `examples/semantic-cross-references.md` is the intended authoring pattern

## Outstanding Questions

### Deferred to Planning

- [Affects R5][Technical] What MDPP diagnostic code number should be assigned for cross-file duplicate slugs? Need to check the existing registry in the processing model to find the next available code.
- [Affects R9][Technical] Should the worked examples live inline in the spec document, or as separate example files in `examples/`? The existing processing model spec uses inline examples.
- [Affects R10][Technical] How much should the syntax reference's "Advanced Patterns > Link References" section expand? Need to balance completeness against keeping the syntax reference focused on syntax rather than processing semantics.
- [Affects spec location][Technical] Should this be a new section appended to `spec/processing-model.md` or a standalone `spec/cross-file-link-resolution.md`? Both are viable — the processing model spec is already substantial.

## Next Steps

→ `/ce:plan` for structured implementation planning
