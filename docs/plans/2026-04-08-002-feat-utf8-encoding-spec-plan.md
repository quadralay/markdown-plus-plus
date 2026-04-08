---
title: "feat: Add UTF-8 character encoding requirement to specification"
type: feat
status: completed
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-utf8-encoding-requirements.md
---

# feat: Add UTF-8 character encoding requirement to specification

## Overview

Add a normative UTF-8 encoding requirement to the Markdown++ processing model specification. This includes the encoding requirement itself, BOM handling rules, encoding error diagnostic (MDPP017), and conformance updates. The change ensures that processors agree on how to decode document bytes before any Markdown++ processing begins.

## Problem Frame

The Markdown++ specification defines a formal grammar, processing model, attachment rule, and conformance requirements — but never states a required character encoding. CommonMark 0.30 specifies UTF-8, and Markdown++ should explicitly inherit this requirement.

Without an encoding requirement, processors may disagree on how to decode non-ASCII bytes in document content, include expansion may produce garbled text when files use different encodings, and internationalized documentation teams have no spec-backed guarantee their content will round-trip correctly. (see origin: `docs/brainstorms/2026-04-08-utf8-encoding-requirements.md`)

## Requirements Trace

- R1. Normative UTF-8 requirement — Markdown++ documents MUST be encoded in UTF-8
- R2. BOM handling — UTF-8 BOM is OPTIONAL; processors MUST strip/ignore a leading BOM; mid-file BOM is not valid content
- R3. Encoding error diagnostic MDPP017 (severity: Error) emitted on invalid UTF-8
- R4. Encoding error recovery is implementation-defined; no mandated fallback encoding
- R5. Include chain encoding consistency — all files MUST be UTF-8; MDPP017 includes the offending file path

## Scope Boundaries

- **In scope:** Document-level encoding requirement, BOM handling, encoding error diagnostic, include chain consistency, conformance update
- **Out of scope:** Unicode normalization (NFC/NFD) — deferred until the `letter` production is extended to Unicode categories
- **Out of scope:** Extending the `letter` production or identifier character set (tracked by issue #15)
- **Out of scope:** Variable value encoding — values come from the variable map, populated outside the spec boundary

## Context & Research

### Relevant Code and Patterns

- `spec/processing-model.md` — Owns the processing pipeline, diagnostic registry (MDPP000–MDPP013), conformance section, and error handling classification. The encoding section will be added here.
- `spec/formal-grammar.md` — Defines the `letter` production as ASCII-only with a comment noting future Unicode extension. No changes needed — encoding is a processing concern, not a grammar concern.
- `spec/whitepaper.md` — Positions Markdown++ as CommonMark-based; establishes the interchangeability principle.

### Institutional Learnings

- **Processing model specification** (`docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`): Established the two-phase pipeline, diagnostic registry, and conformance framework that this plan extends.

### External References

- [CommonMark 0.30 §2.1](https://spec.commonmark.org/0.30/#characters-and-lines): "Any sequence of characters is a valid CommonMark document... characters are Unicode code points... the line ending is a newline (U+000A), a carriage return (U+000D)... **a conformant parser may be limited to accepting only UTF-8 encoding**" — CommonMark uses UTF-8 as the expected encoding.
- [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt): Conformance keywords (MUST, SHOULD, MAY) already used by the processing model.
- [Unicode BOM FAQ](https://www.unicode.org/faq/utf_bom.html): UTF-8 BOM (EF BB BF / U+FEFF) is optional; many tools add or strip it.

## Key Technical Decisions

- **Section placement — processing model, not standalone document:** The processing model already owns the pipeline, diagnostics, and conformance. Encoding is a pre-condition for the pipeline (bytes must be decoded before Phase 1 begins). A standalone `spec/character-encoding.md` would need to cross-reference the diagnostic registry and conformance section anyway, adding indirection for no benefit.

- **Position within processing model — before Pipeline Overview:** Encoding validation is logically "Phase 0" — it happens when a file is read, before any Phase 1 processing. The section should appear after Definitions and before Pipeline Overview, establishing encoding as a pre-condition.

- **MDPP017 triggers on first invalid byte sequence:** Invalid encoding corrupts character boundaries, making further parsing of the affected file unreliable. The processor stops processing the affected file but SHOULD continue with other files in the include chain. A processor MAY attempt to collect multiple encoding errors within a single file but is not required to.

- **Encoding validated during include expansion, not before it:** The natural validation point is when a file is read (step 1 of the include algorithm). Pre-expansion validation is impractical since the full file list isn't known until expansion begins. This is consistent with how MDPP006 (missing include file) is detected during expansion.

- **No mandated fallback encoding:** The ePublisher parser falls back to ISO-8859-1, but encoding this into the spec would bless data corruption as a feature. Implementations MAY implement fallback, but the spec requires MDPP017 regardless.

- **BOM allowed but ignored, not forbidden:** Forbidding BOM would reject files from editors that add BOM by default (notably older Windows editors). Allowing-but-ignoring matches CommonMark and existing ePublisher behavior.

## Open Questions

### Resolved During Planning

- **Where should the encoding section live?** (affects all requirements): In `spec/processing-model.md` as a new section before Pipeline Overview. The processing model owns the pipeline, diagnostics, and conformance. Encoding is a pre-condition for the pipeline, not a standalone concern.

- **MDPP017 trigger behavior** (affects R3): Emit on the first invalid byte sequence. Invalid encoding corrupts character boundaries. Consistent with Error severity. Processor stops the affected file but continues with others.

- **Validate before or during include expansion?** (affects R5): During expansion. The natural validation point is file read time. Pre-expansion validation is impractical. Consistent with MDPP006 pattern.

### Deferred to Implementation

- **Exact prose for the BOM stripping requirement**: Whether to describe BOM stripping as "the processor removes the BOM before further processing" or "the BOM is not considered part of the document content." Both convey the same normative behavior; the exact wording should match the processing model's existing prose style.

## Implementation Units

- [x] **Unit 1: Add encoding section and MDPP017 to processing model**

**Goal:** Add the normative UTF-8 encoding requirement, BOM handling rules, encoding error diagnostic, and include chain encoding consistency to the processing model specification.

**Requirements:** R1, R2, R3, R4, R5

**Dependencies:** None

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Add a new "Character Encoding" section after Definitions and before Pipeline Overview
- Structure the section with subsections: Encoding Requirement, BOM Handling, Encoding Errors, Include Chain Encoding Consistency
- Encoding Requirement: normative UTF-8 statement aligned with CommonMark 0.30
- BOM Handling: OPTIONAL leading BOM, processors MUST strip/ignore, mid-file BOM after include expansion is invalid
- Encoding Errors: MDPP017 definition, Error severity, triggers on first invalid byte sequence, recovery is implementation-defined
- Include Chain Encoding Consistency: all files MUST be UTF-8, MDPP017 includes offending file path
- Register MDPP017 in the diagnostic registry table under Processing-Phase Codes (MDPP017 follows MDPP013)
- Add a note in Phase 1, Step 1 (Include Expansion) algorithm step 1 ("Read the current file's content") referencing the encoding requirement — this is where encoding validation naturally occurs

**Patterns to follow:**
- Processing model's existing diagnostic definitions (MDPP010–MDPP013) for registry entry format
- Processing model's existing error handling section for fatal vs. recoverable classification
- Processing model's RFC 2119 conformance keyword usage

**Test scenarios:**
- A UTF-8 document with no BOM processes normally (R1 baseline)
- A UTF-8 document with leading BOM processes normally after BOM stripping (R2)
- A file with invalid UTF-8 byte sequence emits MDPP017 with file path (R3, R5)
- A processor that implements ISO-8859-1 fallback still emits MDPP017 before falling back (R3, R4)
- An included file with invalid encoding emits MDPP017 with the included file's path, not the root document's path (R5)
- A mid-file BOM resulting from include expansion is treated as invalid content (R2)

**Verification:**
- The processing model contains a normative statement that documents MUST be UTF-8
- BOM handling is defined precisely enough that two independent implementations would behave identically
- MDPP017 appears in the diagnostic registry with severity Error and a clear triggering condition
- The encoding section uses RFC 2119 keywords consistently with the rest of the processing model

- [x] **Unit 2: Update conformance section and cross-references**

**Goal:** Add encoding validation as a required conformance feature and ensure cross-references are consistent.

**Requirements:** R1, R3 (conformance implications)

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Add a new required feature to the Conformance > Required Features list (item 11): "Encoding validation — UTF-8 encoding validation with BOM handling and MDPP017 emission, as specified in [Character Encoding](#character-encoding)"
- Update the introduction paragraph to mention encoding as part of the specification scope (currently lists "processing pipeline, evaluation order, scoping rules, error behavior, and output model")
- Verify the diagnostic reporting requirement (item 10) implicitly covers MDPP017 via "all MDPP diagnostic codes defined in this specification" — no change needed if the wording is already general
- Add MDPP017 to the error handling section's classification table if the existing table is exhaustive (check whether the table lists all codes or just examples)

**Patterns to follow:**
- Existing required features list structure (numbered, with brief description and spec section reference)
- Existing error classification table structure

**Test scenarios:**
- The conformance section explicitly lists encoding validation as a required feature
- A reader can trace from the conformance requirement back to the encoding section for the full specification
- MDPP017 appears in all relevant tables (diagnostic registry and error classification)

**Verification:**
- Required features list includes encoding validation
- Error classification table includes MDPP017 with correct severity
- Introduction reflects the expanded scope
- All internal cross-references resolve correctly

## Risks & Dependencies

- **Dependency on stable diagnostic registry:** MDPP017 is the next available code (MDPP000–MDPP013 allocated). If another concurrent change allocates MDPP017, renumbering will be needed. Low risk given the current development pace.
- **Risk: Normative over-specification of BOM.** The BOM stripping requirement must be precise enough for interop but not so prescriptive that it conflicts with existing tools. The "allowed but ignored" approach (matching CommonMark) mitigates this.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-utf8-encoding-requirements.md](../brainstorms/2026-04-08-utf8-encoding-requirements.md)
- Related spec: [spec/processing-model.md](../../spec/processing-model.md)
- Related spec: [spec/formal-grammar.md](../../spec/formal-grammar.md) (letter production, no changes needed)
- Learning: [docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md](../solutions/documentation-gaps/processing-model-specification-2026-04-08.md)
- External: [CommonMark 0.30 §2.1](https://spec.commonmark.org/0.30/#characters-and-lines)
- External: [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt)
- Related issue: [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) — Formal specification
- Related issue: [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) — Unified naming rule (UTF-8 letter support)
- Related issue: [#23](https://github.com/quadralay/markdown-plus-plus/issues/23) — UTF-8 encoding specification
