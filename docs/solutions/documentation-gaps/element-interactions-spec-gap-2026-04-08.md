---
title: "Element interactions specification gap -- style types, default names, compound naming, and heading aliases undocumented"
date: 2026-04-08
category: documentation-gaps
module: specification
problem_type: documentation_gap
component: documentation
symptoms:
  - "No specification coverage for how Markdown++ extensions interact with standard CommonMark elements"
  - "Style type taxonomy (Paragraph, Character, Graphic, Table) undocumented in open spec"
  - "Compound naming rules for nested containers absent from specification"
  - "Heading alias auto-generation algorithm not documented"
  - "Five standard elements (setext headings, horizontal rules, indented code blocks, block/inline HTML) had no Markdown++ documentation"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
tags:
  - element-interactions
  - commonmark
  - style-taxonomy
  - compound-naming
  - heading-alias
  - specification-gap
---

# Element interactions specification gap -- style types, default names, compound naming, and heading aliases undocumented

## Problem

The Markdown++ open specification documented extension syntax, tag-to-element binding, evaluation order, and formal grammar, but never specified what happens after a style tag attaches to an element -- the style type taxonomy, default style names, compound naming for nested containers, and heading alias auto-generation algorithm were entirely absent, even though this information existed across 15 pages of legacy ePublisher documentation.

## Symptoms

- Authors had no way to know the four style types (Paragraph, Character, Graphic, Table) that determine how output processors categorize styled content
- Default style names were undiscoverable -- authors could not predict that a blockquote defaults to "Blockquote", an `##` heading to "Heading 2", or a setext `===` heading to "Title 1"
- Compound names formed automatically when content was nested inside containers (e.g., "Blockquote Heading 1", "OList CustomParagraph"), but no rules were documented for how compounding worked, whether custom styles participated, or whether styles inherited across nesting levels
- The heading alias auto-generation algorithm (lowercase, strip non-alphanumeric, spaces to hyphens) was critical for cross-references but unspecified -- implementors had to reverse-engineer it from ePublisher code
- Five CommonMark element types had zero specification coverage: setext headings (titles), horizontal rules, indented code blocks, block HTML, and inline HTML
- Building a second conformant Markdown++ processor required guessing at these behaviors or inspecting proprietary source code

## What Didn't Work

The incremental specification approach -- building the spec document by document (syntax reference, then attachment rule, then processing model, then formal grammar) -- left a critical semantic layer undocumented. Each spec document covered its own concern cleanly, but no document owned the "what does the binding produce?" question:

- The **syntax reference** defined what extensions look like but not the style type or default name produced
- The **attachment rule** defined how tags bind but not what the binding produces
- The **processing model** defined evaluation order and the output tree concept but not what annotations each element type carries
- The **formal grammar** defined valid syntax productions but not the semantic output
- **Legacy ePublisher documentation** contained all the detail but as proprietary implementation docs, not an open specification
- **Example files** demonstrated working cases but could not communicate normative rules or algorithmic details

The gap persisted because each new spec document felt complete in its own scope, masking the missing semantic layer.

## Solution

Created `spec/element-interactions.md` (636 lines) as the fifth document in the Markdown++ specification suite, covering all 20 requirements from issue #9:

- **Style type taxonomy** -- four normative types (Paragraph, Character, Graphic, Table) with definitions and element mappings
- **Element catalog table** -- every supported CommonMark element mapped to style type, default name(s), style tag acceptance, and placement
- **Block-level elements** -- setext headings, ATX headings, paragraphs, indented/fenced code blocks, horizontal rules with style type, default name, and examples
- **Heading alias auto-generation** -- deterministic 6-step algorithm (strip formatting, resolve variables, lowercase, remove non-alphanumeric, spaces to hyphens, trim) with 8-row examples table
- **Container elements** -- blockquotes and lists with compound style naming, unlike-marker list breaking, and nested list styling
- **Compound naming rule** -- formal definition (`ContainerStyle + space + ElementStyle`), recursive compounding, relationship to `STANDARD_NAME_RE`, and non-inheritance rule
- **Inline elements** -- bold, italic, strikethrough, code spans (Character type), links with cross-document alias linking, images (Graphic type)
- **Tables** -- three-name generation pattern (container, Cell Head, Cell Body) for standard and multiline tables
- **Block/inline HTML** -- style tag recognition normative (MUST), output availability output-format dependent (MAY)
- **TOC integration** -- SHOULD-level informational guidance
- **Relationship table** -- cross-references connecting to the other four spec documents

Review fixes applied (commit `fd4fa81`):

1. Compound naming formula corrected from `ElementDefault` to `ElementStyle` ("custom style name if present, or default style name otherwise") -- the original formula contradicted examples
2. Setext heading section gained missing cross-reference to heading alias auto-generation
3. Paragraph style type "Applies To" list updated to include inline HTML
4. Section heading renamed from "Compound Names and the Naming Rule" to "Compound Names and Identifier Validation" to eliminate ambiguity

## Why This Works

The root cause was a documentation architecture gap: the spec suite covered syntax, binding, evaluation, and grammar, but no document owned the semantic layer connecting "a style tag attached to an element" to "the style type, default name, and compound name the processor must produce." By creating a dedicated element interactions document using the same RFC 2119 normative language and established patterns as the other spec documents, the specification suite now covers the complete pipeline from syntax through element-specific output semantics. New implementors can build conformant processors without reverse-engineering legacy code.

## Prevention

- **Map the full semantic pipeline before writing individual specs.** When designing a multi-document specification, explicitly identify every layer (syntax, binding, evaluation, element semantics, output) and ensure each has an owning document. The incremental approach masked this gap because each document felt complete in isolation.
- **Maintain an element coverage matrix.** A table of all supported elements crossed with all specification concerns (syntax, binding rules, style type, default name, compound naming, alias behavior) makes empty cells -- documentation gaps -- immediately visible. The five uncovered elements would have been caught early.
- **Transfer legacy knowledge with a checklist.** When formalizing a specification from proprietary documentation, track every topic in the legacy docs and confirm each has been transferred. The 15 pages of ePublisher element interaction documentation should have had corresponding tracking items.
- **Review formulas against examples.** The compound naming formula bug (`ElementDefault` vs. `ElementStyle`) was only caught because a code review compared formula text against the examples table. Include formula-to-example consistency checks as a standard review step for normative specifications.
- **Cross-reference parallel sections symmetrically.** When two spec sections describe parallel elements (ATX headings and setext headings), verify they have matching cross-references. The missing setext alias cross-reference was caught by comparing the two heading sections side by side.

## Related Issues

- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Document how Markdown++ interacts with standard Markdown elements (primary issue)
- [#18](https://github.com/quadralay/markdown-plus-plus/issues/18) -- Specify whether custom aliases supplement or replace auto-generated heading IDs (resolved by heading alias section)
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) -- Enforce unified naming rule across all Markdown++ name types (compound naming section extends this)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Write a formal Markdown++ specification (parent umbrella)
- Related learning: [Attachment rule formal spec](attachment-rule-formal-spec-2026-04-07.md) -- established the pattern for formalizing scattered implementation details into a single spec document
- Related learning: [Processing model specification](processing-model-specification-2026-04-08.md) -- demonstrated how to formalize implicit behavior with RFC 2119 language
- Related learning: [Unified naming rule](../logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md) -- compound style names extend this rule; element interactions spec clarifies the relationship
- Related learning: [Formal grammar](formal-ebnf-peg-grammar-for-extensions-2026-04-08.md) -- defines syntax that element interactions spec gives semantics to
