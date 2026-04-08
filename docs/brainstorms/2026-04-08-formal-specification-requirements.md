---
date: 2026-04-08
topic: formal-specification
---

# Formal Markdown++ Specification

## Problem Frame

Tool authors who want to implement Markdown++ support must currently reverse-engineer the format from a whitepaper (written for decision-makers), a plugin skill reference (written for an AI agent), and scattered example files. Four sub-specifications exist — formal grammar (#11), processing model (#8), attachment rule (#10), and cross-file link resolution (#22) — but no unified document ties them together with an introduction, terminology, conformance levels, or per-extension definitions. This makes third-party adoption unnecessarily difficult and guarantees incompatible implementations.

## Requirements

- R1. A single `spec/specification.md` document MUST serve as the formal Markdown++ 1.0 specification
- R2. The specification MUST use RFC 2119 language (MUST/SHOULD/MAY) for all normative requirements
- R3. The specification MUST define conformance levels for processors (at minimum: a base level that passes extensions through unchanged, and a full level that processes all extensions)
- R4. The specification MUST include a terminology section defining key terms: directive, attachment, block-level element, inline element, extension comment, combined command, variable token, content island, and any other terms used normatively
- R5. The specification MUST state that CommonMark 0.30 is the base specification and that all CommonMark constructs are valid Markdown++, with GFM table support
- R6. The specification MUST contain a complete definition section for each extension: Variables, Custom Styles, Custom Aliases, Conditions, File Includes, Markers/Metadata, Multiline Tables, and Content Islands
- R7. Each extension definition section MUST include: purpose, syntax (with examples), semantics, interaction with other extensions, attachment requirements, and applicable diagnostic codes
- R8. The specification MUST incorporate the formal grammar (spec/formal-grammar.md) by normative reference, with an overview of the extension comment syntax in the main document
- R9. The specification MUST incorporate the processing model (spec/processing-model.md) by normative reference, with a summary of the two-phase pipeline in the main document
- R10. The specification MUST incorporate the attachment rule (spec/attachment-rule.md) by normative reference, with the core rule stated in the main document
- R11. The specification MUST incorporate cross-file link resolution (spec/cross-file-link-resolution.md) by normative reference
- R12. The specification MUST include a validation and conformance section that consolidates all diagnostic codes (MDPP001–MDPP014) into a single registry with severity, triggering condition, and required vs. optional status
- R13. The specification MUST include sections on inline styling (images and links), book assembly (composite documents), and link reference definitions for cross-referencing
- R14. The specification MUST be versioned as Markdown++ 1.0

## Success Criteria

- A tool author can implement a conformant Markdown++ processor using only the specification and its normative references, without consulting the whitepaper, plugin skill reference, or example files
- All normative requirements use RFC 2119 keywords consistently
- Every Markdown++ extension has a self-contained definition section
- Conformance levels are defined with clear criteria for each level
- The diagnostic code registry is complete and consolidated in one place
- The specification is internally consistent with its normative references (no contradictions between the main document and sub-specs)

## Scope Boundaries

- **Out of scope:** Changes to the ePublisher parser implementation
- **Out of scope:** Tooling or editor support documentation
- **Out of scope:** Marketing, migration guidance, or competitive comparison (that's the whitepaper's role)
- **Out of scope:** A conformance test suite (that's a separate deliverable)
- **Out of scope:** Rewriting the existing sub-specs — they are referenced as-is
- **In scope:** The unified specification document and its normative references to existing sub-specs

## Key Decisions

- **Unified spec with normative references (not monolithic):** The main specification normatively references the four existing sub-specs rather than inlining their full content. This avoids duplicating 1500+ lines of already-formalized content, keeps sub-specs maintainable as independent documents, and follows the pattern used by major specifications (HTML references CSS, DOM, etc.). The main spec includes overview/summary content for each referenced topic so it reads coherently end-to-end. **Why:** The sub-specs are each 200-500+ lines, already use RFC 2119 language, and cross-reference each other. Inlining would create a 3000+ line document with duplicated normative text. **How to apply:** Each section that references a sub-spec should include a 1-2 paragraph summary of the key rules, then a normative reference for the complete definition.

- **Extension definitions are the primary new content:** The eight per-extension sections (R6, R7) are where most new writing happens. These draw from `syntax-reference.md` but elevate the content to specification-grade with RFC 2119 language, complete interaction tables, and formal examples. **Why:** The existing sub-specs cover cross-cutting concerns (grammar, processing, attachment, cross-file links) but no existing document provides per-extension normative definitions. **How to apply:** Each extension section follows a consistent template: purpose, syntax, semantics, interactions, attachment requirements, diagnostics.

- **Two conformance levels:** "Pass-through" (renderer that preserves extensions as HTML comments) and "Full" (processor that evaluates all extensions). A third "Partial" level is deferred — it adds complexity without clear value for 1.0. **Why:** The issue requests conformance levels; two levels cover the most important distinction (renderers vs. processors) without over-specifying. **How to apply:** Define clear criteria for each level in the conformance section.

- **Diagnostic code registry consolidates both static and processing codes:** Static validation codes (MDPP001-MDPP009 from syntax-reference.md) and processing-phase codes (MDPP010-MDPP014 from processing-model.md and cross-file-link-resolution.md) are consolidated into a single table. **Why:** Currently split across two documents, making it impossible to see the complete picture. **How to apply:** Single table with columns: code, severity, phase (static/processing), description, triggering condition, required level (which conformance levels must implement it).

## Dependencies / Assumptions

- The four sub-specs (formal-grammar.md, processing-model.md, attachment-rule.md, cross-file-link-resolution.md) are assumed to be complete and stable. The specification references them as normative — any changes to sub-specs automatically affect the specification.
- CommonMark 0.30 is the base specification. The Markdown++ spec does not redefine CommonMark behavior.
- The syntax-reference.md in the plugin directory is the primary source for per-extension content that will be elevated to specification grade.

## Outstanding Questions

### Deferred to Planning

- [Affects R3][Technical] Should the conformance section define a "Partial" level for processors that implement only a subset of extensions, or are two levels (Pass-through and Full) sufficient for 1.0?
- [Affects R6][Needs research] For Content Islands — is the current documentation in syntax-reference.md sufficient to write a complete normative definition, or are there undocumented edge cases?
- [Affects R12][Technical] Should the diagnostic registry specify error recovery behavior (what a processor does after encountering each diagnostic), or only detection requirements?
- [Affects R13][Needs research] How much detail does the book assembly section need? The processing model covers the include mechanism, but assembly-level concerns (document ordering, cross-document numbering) may need additional specification.

## Next Steps

→ `/ce:plan` for structured implementation planning
