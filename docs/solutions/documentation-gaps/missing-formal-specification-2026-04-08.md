---
title: Missing formal Markdown++ specification for tool implementers
date: 2026-04-08
last_updated: 2026-04-11
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - "No formal specification existed — only a persuasive whitepaper in spec/"
  - "Tool authors had to reverse-engineer format from scattered sources (whitepaper, plugin skill, examples)"
  - "Ambiguities across sources risked incompatible third-party implementations"
  - "No normative language (RFC 2119) defining conformance requirements"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
related_components:
  - tooling
tags:
  - specification
  - markdown-plus-plus-1.0
  - rfc-2119
  - conformance-levels
  - formal-grammar
  - processing-model
  - attachment-rule
---

# Missing formal Markdown++ specification for tool implementers

## Problem

The `spec/` directory contained only a whitepaper -- a persuasive document aimed at decision-makers -- with no formal specification defining grammar, parsing rules, processing semantics, or conformance requirements for Markdown++. Tool authors wanting to implement Markdown++ support had no normative reference to build against.

## Symptoms

- **No single source of truth.** A tool implementer had to cross-reference three unrelated documents (whitepaper, plugin skill reference, scattered examples) to piece together the format's behavior, with no guarantee of completeness.
- **Ambiguous edge cases.** Questions like "what happens when a style tag has a blank line before its target?" or "are variable tokens inside code spans resolved?" had no documented answers. Different implementers would produce different behavior.
- **Conformance undefined.** There was no way to test whether a processor was "correct" because no conformance levels, diagnostic codes, or required behaviors were defined.
- **Audience mismatch.** The whitepaper spoke to managers evaluating format adoption. The syntax reference spoke to an AI agent authoring documents. Neither spoke to the developer writing a parser.
- **Reverse-engineering required.** Implementers had to read example files and infer rules from patterns -- slow, error-prone, and guaranteed to produce incompatible implementations.

## What Didn't Work

- **Inlining the sub-specifications.** The four prerequisite documents (formal grammar, attachment rule, processing model, cross-file link resolution) totaled significant content. A single monolithic document would have exceeded 3,000+ lines, creating navigation, review, and merge-conflict problems.
- **Elevating the whitepaper.** The whitepaper's persuasive structure (benefits, comparisons, adoption arguments) is fundamentally incompatible with specification structure (definitions, conformance requirements, error semantics). The two serve different audiences.
- **Elevating the syntax reference.** The plugin's `syntax-reference.md` was scoped to AI-assisted authoring, not tool implementation. It lacked conformance levels, a processing model, diagnostic codes, and edge-case definitions. Expanding it would have broken its role as a plugin skill reference.
- **Bottom-up assembly from examples.** Building a spec by cataloging example behaviors inverts the correct relationship: the specification should define the format, not codify whatever behaviors happen to be demonstrated.

## Solution

Created `spec/specification.md` -- a 1,208-line unified Markdown++ 1.0 specification with 19 sections:

**Front matter (sections 1-4):** Scope, relationship to CommonMark 0.30, two conformance levels (pass-through and full), 13 defined terms, RFC 2119 boilerplate.

**Core mechanics (sections 5-7):** Extension comment syntax, the attachment rule, and the two-phase processing model. Each provides a self-contained summary then makes a normative reference to the detailed sub-specification using "as specified in [Sub-spec](sub-spec.md)."

**Extension definitions (sections 8-15):** Eight extensions -- Variables, Custom Styles, Custom Aliases, Conditions, File Includes, Markers/Metadata, Multiline Tables, and Content Islands. Each follows a consistent template: Purpose, Syntax, Semantics, Interactions, Attachment Requirements, Diagnostics, Examples.

**Integration features (sections 16-17):** Combined commands and advanced topics (inline styling, book assembly, link reference definitions, semantic cross-references).

**Reference material (sections 18-19):** Consolidated diagnostic registry (MDPP000-MDPP014 at initial writing; extended to MDPP000-MDPP017 by subsequent issues #23 UTF-8 encoding and #25 format versioning) split into static validation and processing-phase categories. Full normative and informative reference tables.

### Key architectural decisions

1. **Normative references rather than inlining.** Sections 5-7 summarize core mechanics in 1-2 paragraphs each, then defer to sub-specifications for complete definitions. All five documents remain independently maintainable while the primary specification stays self-navigable.

2. **Two conformance levels.** Pass-through conformance (preserve comments and tokens, render as CommonMark) gives standard renderers formal status. Full conformance (implement the complete processing model) defines what a Markdown++ processor must do.

3. **Determinism guarantee.** Section 2.3 makes an explicit normative statement: same input, same variable map, same condition set produces same output.

4. **Consistent extension section template.** Every extension section follows the same structure, making the document predictable for implementers.

### Prerequisite decomposition

Four sub-specifications were completed as prerequisites before the unified specification:

- **#11** -- Formal grammar (`spec/formal-grammar.md`): W3C EBNF and PEG transliteration
- **#10** -- Attachment rule (`spec/attachment-rule.md`): formal binding rules and edge cases
- **#8** -- Processing model (`spec/processing-model.md`): two-phase pipeline with numbered requirements
- **#22** -- Cross-file link resolution (`spec/cross-file-link-resolution.md`): derived behavior semantics

### Review findings applied

Nine review findings were addressed in a follow-up commit:

- RFC 2119 MAY/SHOULD alignment
- Conformance label equivalence note
- Content Islands template restoration
- "Output tree" terminology definition
- MDPP000 name alignment with processing model
- Diagnostic column header rename
- RFC 2119 deduplication
- Informal terminology fix
- "Orphaned tag" definition

## Why This Works

The root cause was an audience gap: existing documents addressed format evaluators (whitepaper) and AI authoring agents (syntax reference) but not tool implementers. A specification is structurally different from both -- it defines what a conformant implementation MUST do, not why to adopt the format or how to author content.

The normative-reference architecture solves the maintainability problem without sacrificing coherence. The primary specification is the entry point that a tool author reads end-to-end. When they need the exact EBNF grammar, they follow the link to `formal-grammar.md`. Each document has a single responsibility and a clear audience.

The consolidated diagnostic registry (section 18) makes the specification testable. A tool author can build a test suite with one test per MDPP code. During this work, MDPP000 (file not found) was discovered missing from the initial draft precisely because the registry required every code to be present -- the registry functions as both reference table and coverage audit.

## Prevention

- **Specification-first development.** When defining a new format or extending an existing one, write the specification before the tooling. The specification is the contract; tooling implements it.
- **Audience-labeled documents.** Every document in `spec/` should declare its audience in its introduction. When a new audience emerges, the absence of a document for that audience becomes visible.
- **Conformance levels from the start.** Defining what "correct" means should happen early, not after multiple implementations already exist.
- **Prerequisite decomposition.** Build detailed sub-specifications first, then compose the umbrella document. This ensures component rules are independently reviewed and stable before the primary specification references them.
- **Diagnostic registry as completeness check.** A consolidated registry forces specification authors to account for every error condition and functions as a coverage audit.
- **Consistent section templates.** Using a repeatable structure for each extension section prevents accidental omissions. An empty subsection signals either a gap or an intentional decision to document.

## Related Issues

- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Write a formal Markdown++ specification (this issue)
- [#11](https://github.com/quadralay/markdown-plus-plus/issues/11) -- Formal grammar (prerequisite, completed)
- [#10](https://github.com/quadralay/markdown-plus-plus/issues/10) -- Attachment rule (prerequisite, completed)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Processing model (prerequisite, completed)
- [#22](https://github.com/quadralay/markdown-plus-plus/issues/22) -- Cross-file link resolution (prerequisite, completed)
- [#23](https://github.com/quadralay/markdown-plus-plus/issues/23) -- UTF-8 encoding requirement (related, open)
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Standard element interactions (related, open)
- [#12](https://github.com/quadralay/markdown-plus-plus/issues/12) -- Graceful degradation behavior (related, open)

### Precursor solution docs

- [Formal EBNF/PEG grammar](formal-ebnf-peg-grammar-for-extensions-2026-04-08.md) -- Issue #11
- [Processing model specification](processing-model-specification-2026-04-08.md) -- Issue #8
- [Attachment rule formal spec](attachment-rule-formal-spec-2026-04-07.md) -- Issue #10
- [Cross-file link resolution semantics](cross-file-link-resolution-semantics-2026-04-08.md) -- Issue #22
