---
date: 2026-04-08
topic: utf8-encoding-requirement
---

# UTF-8 Character Encoding Requirement

## Problem Frame

The Markdown++ specification defines a formal grammar, processing model, attachment rule, and conformance requirements — but never states a required character encoding. CommonMark 0.30 specifies UTF-8, and Markdown++ should explicitly inherit or restate this requirement.

Without an encoding requirement:

- Processors may disagree on how to decode non-ASCII bytes in document content (prose, headings, link text)
- Include expansion may produce garbled text when parent and child files use different encodings
- Variable values containing non-ASCII characters have undefined behavior
- Internationalized documentation teams have no spec-backed guarantee their content will round-trip correctly

This matters now even though Markdown++ identifiers are currently ASCII-only — document *content* (paragraphs, headings, lists) can contain any Unicode character, and include expansion splices raw text from multiple files.

## Requirements

- R1. **Normative UTF-8 requirement.** A Markdown++ document MUST be encoded in UTF-8, consistent with CommonMark 0.30. This applies to both root documents and included files.

- R2. **BOM handling.** A UTF-8 Byte Order Mark (U+FEFF) at the start of a file is OPTIONAL. A conformant processor MUST strip or ignore a leading BOM before processing, consistent with CommonMark 0.30 behavior. BOM MUST NOT appear at any other position in the file (mid-file BOM after include expansion is a processing artifact, not valid content).

- R3. **Encoding error diagnostic.** When a processor encounters a byte sequence that is not valid UTF-8, it MUST emit a new diagnostic code **MDPP014** (severity: Error). This follows the existing diagnostic registry pattern in the processing model (MDPP000–MDPP013 are allocated; MDPP014 is the next available code).

- R4. **Encoding error recovery is implementation-defined.** The specification MUST NOT mandate a specific fallback encoding (e.g., ISO-8859-1). Whether and how a processor recovers from encoding errors is implementation-defined. The only normative requirement is that MDPP014 is emitted.

- R5. **Include chain encoding consistency.** All files in an include chain MUST be UTF-8. A processor that detects an encoding error in an included file MUST emit MDPP014 with the file path of the offending file, consistent with the existing diagnostic format (code, severity, file path, line number, message).

## Success Criteria

- The specification contains a normative encoding requirement that a conformance test suite can verify
- BOM behavior is defined clearly enough that two independent processor implementations will handle BOM identically
- The diagnostic code MDPP014 is registered in the processing model's diagnostic registry
- Encoding error recovery is explicitly left to implementations, avoiding spec-mandated fallback that could mask data corruption

## Scope Boundaries

- **In scope:** Document-level encoding requirement, BOM handling, encoding error diagnostic, include chain consistency
- **Out of scope:** Unicode normalization (NFC/NFD) — deferred until the `letter` production is extended to Unicode categories for non-English identifiers
- **Out of scope:** Extending the `letter` production or identifier character set — tracked separately by the formal grammar's extension point and issue #15
- **Out of scope:** Variable value encoding — variable values come from the variable map, which is populated outside the spec boundary; the spec defines tokens in the document, not the external data source

## Key Decisions

- **Align with CommonMark 0.30:** Markdown++ documents are CommonMark documents. Using the same encoding requirement avoids a conflict between the base format and its extensions.
- **BOM allowed but ignored, not forbidden:** Forbidding BOM would reject files saved by editors that add BOM by default (notably older Windows editors). Allowing-but-ignoring matches CommonMark and existing ePublisher behavior (strips BOM from included files).
- **No mandated fallback encoding:** The ePublisher parser falls back to ISO-8859-1 on UTF-8 decode failure, but encoding this into the spec would bless data corruption as a feature. Implementations MAY implement fallback, but the spec requires an error diagnostic regardless.
- **MDPP014 as Error, not Warning:** Invalid encoding can corrupt content silently across include expansion. This is a data integrity issue, not a cosmetic one. Error severity ensures processors surface it prominently.

## Dependencies / Assumptions

- The processing model's diagnostic registry (MDPP000–MDPP013) is stable and MDPP014 is available
- The conformance section of the processing model will need to reference encoding as a required feature
- The formal grammar document's `letter` production remains ASCII-only; this requirement does not change it

## Outstanding Questions

### Deferred to Planning

- [Affects R2][Technical] Where should the encoding section live — as a new `spec/character-encoding.md` or as a section within the existing `spec/processing-model.md`? The processing model already defines the pipeline, conformance, and diagnostics, so encoding may fit naturally as a pre-phase requirement there.
- [Affects R3][Technical] Should MDPP014 trigger on the first invalid byte sequence or after attempting to decode the entire file? The existing diagnostic pattern (collect all diagnostics) suggests the latter, but encoding errors may make further parsing meaningless.
- [Affects R5][Needs research] Should the spec recommend or require that processors validate encoding before include expansion begins, or is it acceptable to discover encoding errors during expansion? Early validation is safer but may not be practical for all implementations.

## Next Steps

→ `/ce:plan` for structured implementation planning
