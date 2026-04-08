---
title: "feat: Add standard element interactions specification"
type: feat
status: active
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-element-interactions-requirements.md
---

# feat: Add standard element interactions specification

## Overview

Create `spec/element-interactions.md` -- the normative specification for how Markdown++ extensions interact with each standard CommonMark element. This document defines the style type taxonomy, default style names, compound naming rules for nested containers, heading alias auto-generation, and element-specific behavioral details that authors and implementors need to produce correct output.

## Problem Frame

Markdown++ extends CommonMark 0.30 with style tags, aliases, markers, and other extensions. The syntax reference documents extension syntax. The attachment rule defines how tags bind to elements. The processing model defines evaluation order. But none of these documents specify what happens *after* a style tag attaches to a specific element type -- what style type it produces, what default name a processor generates, how compound names form when content is nested inside containers, or how heading aliases are auto-generated.

Without this specification:
- Authors cannot predict the style name a processor generates for styled content inside blockquotes or lists
- The four-part style type taxonomy (Paragraph, Character, Graphic, Table) is undocumented
- The heading alias auto-generation algorithm is undocumented, making cross-references fragile
- Compound naming rules for nested containers are absent
- Several standard elements (setext headings, horizontal rules, indented code blocks, block/inline HTML) have no Markdown++ documentation at all

The legacy ePublisher documentation contains 15 detailed pages covering these interactions. This effort formalizes that information as part of the open specification.

(see origin: [docs/brainstorms/2026-04-08-element-interactions-requirements.md](../brainstorms/2026-04-08-element-interactions-requirements.md))

## Requirements Trace

- R1. Define four style types: Paragraph, Character, Graphic, Table
- R2. Complete mapping from every CommonMark element to its style type, default name, and style tag acceptance
- R3. Setext headings (titles): style tags, "Title 1"/"Title 2", Paragraph type
- R4. ATX headings: style tags, "Heading 1"-"Heading 6", Paragraph type
- R5. Heading alias auto-generation algorithm
- R6. Paragraphs: style tags, "Paragraph", Paragraph type
- R7. Blockquotes as content islands: style tags, "Blockquote", Paragraph type, compound naming
- R8. Ordered lists: style tags, "OList"/"OList Item", Paragraph type, compound naming
- R9. Unordered lists: style tags, "UList"/"UList Item", Paragraph type, unlike-marker list breaking
- R10. Indented code blocks: style tags, "Code Block", Paragraph type
- R11. Fenced code blocks: style tags, "Code Fence", Paragraph type
- R12. Horizontal rules: style tags, "Horizontal Rule", Paragraph type
- R13. Block HTML / inline HTML: style tags, output-format dependency
- R14. Compound style naming rule for nested content in containers
- R15. Nested list style non-inheritance
- R16. Bold, italic, strikethrough, code spans: inline style tags, Character type
- R17. Links: inline style tags, Character type, cross-document alias linking
- R18. Images: inline style tags, Graphic type
- R19. Tables: style tags, Table type, three-name generation pattern
- R20. TOC level mapping (informational)

## Scope Boundaries

- **In scope**: Complete element-by-element catalog with style types, default names, and behavioral details
- **In scope**: Style type taxonomy (Paragraph, Character, Graphic, Table)
- **In scope**: Compound style naming rules for containers (blockquotes, lists)
- **In scope**: Heading alias auto-generation algorithm
- **In scope**: Nested list style non-inheritance behavior
- **In scope**: Unlike-marker list-breaking behavior for unordered lists
- **Out of scope**: Modifying the existing syntax reference -- this is an additive specification document
- **Out of scope**: Defining new extension syntax -- this documents existing behavior
- **Out of scope**: Output-format-specific rendering (HTML, PDF, XML details) -- only the abstract style model
- **Out of scope**: Multiline table cell interactions -- already covered in the syntax reference
- **Out of scope**: Processing pipeline or evaluation order -- covered by the processing model spec

## Context & Research

### Relevant Code and Patterns

- **`spec/attachment-rule.md`** -- Established spec document pattern: YAML frontmatter (`date`, `status`), RFC 2119 language, markdown tables for structured rules, edge case sections with code examples, cross-references to other spec docs and syntax-reference.md. The element interactions spec should follow this exact pattern.
- **`spec/processing-model.md`** -- Defines the output model as "CommonMark document tree annotated with Markdown++ metadata." The element interactions spec defines what that metadata looks like for each element type. Cross-references the attachment rule and syntax reference.
- **`spec/formal-grammar.md`** -- Defines the EBNF grammar for extension constructs. Consistent frontmatter and cross-reference style.
- **`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`** -- Comprehensive syntax reference. Shows style tag placement for block and inline elements, content islands, combined commands. The element interactions spec builds on top of what the syntax reference defines syntactically.

### Institutional Learnings

- **Attachment rule formal spec** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Established the pattern for moving scattered implementation details into a single authoritative spec document. Key lesson: enumerate all edge cases before writing, cross-reference from existing docs, align validation codes with user-facing spec.
- **Processing model specification** (`docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`): Demonstrated how to formalize implicit behavior from the ePublisher implementation with RFC 2119 normative language and numbered requirements.
- **Unified naming rule** (`docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`): Compound style names (e.g., `"Blockquote Heading 1"`) contain spaces and fall outside both `STANDARD_NAME_RE` and `ALIAS_NAME_RE`. The element interactions spec must explicitly document that compound names are structural compositions of individual identifier names, not bare identifiers subject to the naming rule regex.

## Key Technical Decisions

- **Spec location is `spec/element-interactions.md`**: Alongside `attachment-rule.md`, `processing-model.md`, and `formal-grammar.md`. This is normative specification content, not skill-level guidance. (see origin)
- **Single comprehensive document**: One reference covering all element types. Authors need a single place to look up any element's behavior; implementors need a complete catalog for conformance. (see origin)
- **Style type taxonomy is normative**: The four-type system (Paragraph, Character, Graphic, Table) is part of the format specification, not an ePublisher implementation detail. Style types determine how output processors handle styled content. (see origin)
- **Compound naming uses space separator**: Container + element names are joined with a space (`"Blockquote Heading 1"`). Matches established ePublisher convention. (see origin)
- **Auto-generated aliases supplement custom aliases**: Custom aliases via `<!--#name-->` create additional anchors alongside the auto-generated heading alias. Both are valid anchors. (see origin)
- **TOC section is informational, not normative**: TOC generation is output-specific behavior. The spec documents the mapping as a SHOULD-level recommendation rather than a MUST requirement. Rationale: different output formats may handle TOC differently.
- **Block/inline HTML output-format dependency noted as processor-defined**: The spec notes that HTML element styling availability depends on the output format, with a SHOULD-level recommendation. Rationale: this is genuinely processor-dependent behavior.
- **Compound names are compositions, not identifiers**: Compound style names contain spaces (`"Blockquote Heading 1"`) and do not match the `STANDARD_NAME_RE` naming rule. The spec must define compound names as structural compositions of individual identifier names (each component conforming to the naming rule) joined by spaces, with a formal composition rule. Cross-reference the syntax reference Naming Rules section rather than redefining identifier constraints.

## Open Questions

### Resolved During Planning

- **Heading alias algorithm -- consecutive spaces**: Consecutive spaces collapse to a single hyphen. (Affects R5)
- **Heading alias algorithm -- empty headings**: Headings with no remaining alphanumeric characters after processing produce no auto-generated alias. (Affects R5)
- **Deeply nested compound naming**: Compounding applies recursively at each container boundary. A paragraph inside a blockquote inside another blockquote produces `"BQ1 BQ2 Paragraph"`. There is no depth limit on compounding. (Affects R14)
- **Multiline table three-name pattern**: The three-name pattern (Table, Table Cell Head, Table Cell Body) applies identically to both standard and multiline tables. The `multiline` directive is a processing instruction, not a structural change to naming. (Affects R19)
- **TOC normative level**: TOC level mapping is informational (SHOULD), not normative (MUST). (Affects R20)
- **Block/inline HTML output dependency**: Noted as processor-defined behavior. The spec states that block/inline HTML styling availability MAY depend on the output format. (Affects R13)

### Deferred to Implementation

- Exact wording of RFC 2119 conformance statements -- consistent MUST/SHOULD/MAY phrasing is an authoring decision
- Whether to include a complete summary table at the top vs. bottom of the document -- depends on document length and flow
- Heading alias algorithm handling of Unicode characters beyond ASCII -- the spec should define the algorithm for ASCII and note that Unicode handling is implementation-defined for now
- Whether the element interactions spec should add new MDPP diagnostic codes or reference only existing ones -- depends on whether any element-specific diagnostics emerge during authoring

## Implementation Units

- [ ] **Unit 1: Document skeleton with style type taxonomy and element catalog table**

**Goal:** Create `spec/element-interactions.md` with frontmatter, introduction, relationship to other spec documents, style type taxonomy definitions, and a complete element-to-style-type mapping table.

**Requirements:** R1, R2

**Dependencies:** None

**Files:**
- Create: `spec/element-interactions.md`

**Approach:**
- YAML frontmatter: `date: 2026-04-08`, `status: draft`
- Introduction: what this spec defines, relationship to syntax reference (syntax), attachment rule (binding), processing model (evaluation), and this document (element-specific semantics)
- Style type taxonomy: four normative definitions with descriptions of what each type represents
- Complete element catalog table: every CommonMark element mapped to style type, default name, accepts style tags (yes/no), and style tag placement (block/inline)
- Use RFC 2119 language: MUST for style type assignments, MUST for default names

**Patterns to follow:**
- `spec/processing-model.md` introduction pattern (explaining how this document relates to the other spec documents)
- `spec/attachment-rule.md` table format for structured rules

**Test scenarios:**
- Every CommonMark element from the issue's gap analysis table appears in the catalog
- No element is assigned to more than one style type
- The table is consistent with the syntax reference's placement rules

**Verification:**
- File exists at `spec/element-interactions.md` with correct frontmatter
- All 14 element categories from the requirements are represented in the catalog table
- Style type taxonomy covers exactly four types

---

- [ ] **Unit 2: Block-level element specifications (titles, headings, paragraphs, horizontal rules, code blocks)**

**Goal:** Write detailed specifications for each block-level element that produces Paragraph style type, covering style tag behavior, default names, and element-specific details.

**Requirements:** R3, R4, R6, R10, R11, R12

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- One subsection per element type, each covering: style type, default name(s), style tag placement, behavioral details, and a code example
- Setext headings (R3): "Title 1" (double underline `===`) and "Title 2" (single underline `---`), Paragraph type
- ATX headings (R4): "Heading 1" through "Heading 6", custom style overrides default
- Paragraphs (R6): "Paragraph" default, simplest element interaction
- Indented code blocks (R10): "Code Block" default, distinct from fenced code blocks
- Fenced code blocks (R11): "Code Fence" default, language info string preserved
- Horizontal rules (R12): "Horizontal Rule" default, no content inside

**Patterns to follow:**
- `spec/attachment-rule.md` edge case format for code examples
- Syntax reference placement examples for consistency

**Test scenarios:**
- Each element section includes a style tag example showing correct attachment
- Default names match the ePublisher conventions documented in the requirements
- Setext vs. ATX heading distinction is clear

**Verification:**
- All six element types have complete subsections
- Each subsection states style type, default name, and includes at least one code example
- Content is consistent with syntax reference placement rules

---

- [ ] **Unit 3: Heading alias auto-generation algorithm**

**Goal:** Specify the heading alias auto-generation algorithm precisely enough that two independent implementations produce the same alias for any given heading text.

**Requirements:** R5

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- Formal algorithm steps: (1) take the heading text content, (2) convert to lowercase, (3) remove all non-alphanumeric characters except spaces, (4) replace each sequence of one or more spaces with a single hyphen, (5) trim leading/trailing hyphens
- Explicit edge cases: consecutive spaces, headings with variables (alias uses resolved text), headings that are entirely non-alphanumeric (no alias generated), headings with inline formatting (stripped for alias computation)
- Relationship to custom aliases: auto-generated alias supplements `<!--#name-->`, both are valid anchors
- Applies to both ATX and setext headings
- Unicode handling: note as implementation-defined for non-ASCII alphanumerics
- Include an examples table: heading text -> generated alias

**Patterns to follow:**
- `spec/processing-model.md` algorithm format (numbered steps with normative language)
- Requirements doc example: `# Let's Go to the Moon!` -> `lets-go-to-the-moon`

**Test scenarios:**
- Simple heading: `# Hello World` -> `hello-world`
- Punctuation: `# Let's Go to the Moon!` -> `lets-go-to-the-moon`
- Consecutive spaces: `# Hello   World` -> `hello-world`
- Numbers: `# Chapter 3 Setup` -> `chapter-3-setup`
- All non-alphanumeric: `# ---` -> no alias generated
- Heading with inline formatting: `# **Bold** Heading` -> `bold-heading`

**Verification:**
- Algorithm steps are unambiguous and deterministic
- Examples table demonstrates all edge cases
- Relationship to custom aliases is explicitly stated

---

- [ ] **Unit 4: Container elements and compound style naming (blockquotes, lists)**

**Goal:** Specify how blockquotes and lists interact with style tags, including the compound naming rule for nested content and nested list non-inheritance behavior.

**Requirements:** R7, R8, R9, R14, R15

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- Blockquotes (R7): "Blockquote" default, content island semantics, nested content gets compound names
- Ordered lists (R8): "OList" container / "OList Item" items, nested content compound naming
- Unordered lists (R9): "UList" container / "UList Item" items, unlike-marker list-breaking behavior
- Compound naming rule (R14): formal definition -- when content is nested inside a styled container, the style name is `"ContainerStyle ElementDefault"` (space-separated). Recursive at each container boundary. Include compound naming examples table. Explicitly note that compound names are structural compositions (space-separated sequences of individual identifiers), not bare identifiers -- they fall outside `STANDARD_NAME_RE` by design. Cross-reference the syntax reference Naming Rules section for individual component naming constraints
- Non-inheritance (R15): nested lists do not inherit parent custom styles. Each nesting level requires its own style tag
- Code examples showing: simple styled container, compound naming with default names, compound naming with custom names, deeply nested compounding, non-inheritance demonstration

**Patterns to follow:**
- Syntax reference content islands section for blockquote context
- Syntax reference nested list styling for indentation patterns

**Test scenarios:**
- Styled blockquote with heading inside: `"Blockquote Heading 1"`
- Custom blockquote with paragraph inside: `"CustomBQ Paragraph"`
- Custom blockquote with custom paragraph: `"CustomBQ CustomParagraph"`
- Ordered list with paragraph: `"OList Paragraph"`
- Nested list without style tag: uses default compound name, not parent's custom name
- Deep nesting: paragraph in blockquote in blockquote: `"BQ1 BQ2 Paragraph"` (recursive)
- Unlike markers breaking unordered list into separate lists

**Verification:**
- Compound naming rule is formally stated with MUST language
- Non-inheritance behavior is explicitly stated with MUST language
- All compound naming examples from the requirements doc are covered
- Unlike-marker behavior for unordered lists is documented

---

- [ ] **Unit 5: Inline elements and special types (bold, italic, links, images, tables, HTML)**

**Goal:** Specify how inline elements (Character type), images (Graphic type), tables (Table type), and block/inline HTML interact with style tags.

**Requirements:** R13, R16, R17, R18, R19

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- Character type elements (R16): bold, italic, strikethrough, code spans -- inline style tag placement, style type is Character
- Links (R17): Character type, inline style placement, cross-document alias linking (`[text](other-doc.md#alias)`)
- Images (R18): Graphic type (unique among all elements), inline style placement
- Tables (R19): Table type, single style name generates three output names: "Name", "Name Cell Head", "Name Cell Body". Default names: "Table", "Table Cell Head", "Table Cell Body". Applies identically to standard and multiline tables
- Block/inline HTML (R13): accept style tags, output-format dependent availability. Processor MAY limit HTML styling based on output format
- Code examples for each element type showing style tag placement and resulting style name

**Patterns to follow:**
- Syntax reference inline styles section for placement patterns
- Syntax reference images and links section for inline style examples

**Test scenarios:**
- Bold with inline style: Character type, style name applied
- Image with inline style: Graphic type confirmed
- Table with custom style "DataTable": generates "DataTable", "DataTable Cell Head", "DataTable Cell Body"
- Cross-document link: `[text](other-doc.md#alias)` with inline style
- Block HTML with style tag: noted as output-format dependent

**Verification:**
- All inline elements have correct style type assignment
- Table three-name pattern is formally specified with MUST language
- Image Graphic type distinction is explicit
- HTML output-format dependency is noted with appropriate MAY/SHOULD language

---

- [ ] **Unit 6: TOC integration, cross-references, and document finalization**

**Goal:** Add the informational TOC section, ensure all cross-references to other spec documents are correct, and verify internal consistency of the complete document.

**Requirements:** R20

**Dependencies:** Units 1-5

**Files:**
- Modify: `spec/element-interactions.md`

**Approach:**
- TOC integration (R20): informational section on how heading levels map to TOC depth. SHOULD-level language. Note that custom heading styles interact with TOC generation in processor-specific ways
- Cross-references: verify all links to `attachment-rule.md`, `processing-model.md`, `formal-grammar.md`, and `syntax-reference.md` use correct relative paths
- Consistency check: verify element catalog table matches all element-specific sections, no contradictions with existing spec documents
- Add a relationship section explaining how this document fits with the other three spec documents (syntax reference, attachment rule, processing model, formal grammar)

**Patterns to follow:**
- `spec/processing-model.md` conformance section for relationship language
- `spec/processing-model.md` introduction for cross-reference format

**Test scenarios:**
- All relative paths to other spec documents resolve correctly from `spec/`
- TOC section uses SHOULD language, not MUST
- No element in the catalog table lacks a corresponding detailed section
- No contradictions between this spec and the syntax reference or processing model

**Verification:**
- Document is internally consistent -- every element in the catalog has a detailed section
- Cross-references to other spec documents use correct relative paths
- TOC section is clearly marked as informational
- Document renders cleanly as standard Markdown

## System-Wide Impact

- **Interaction graph:** The element interactions spec cross-references `spec/attachment-rule.md` (for attachment mechanics), `spec/processing-model.md` (for evaluation semantics and output model), and `syntax-reference.md` (for syntax definitions). No modifications to those documents are required -- this spec builds on top of them as an additive layer.
- **Error propagation:** This spec does not define new MDPP diagnostic codes. Element interaction rules are semantic constraints that build on top of existing attachment (MDPP009) and processing (MDPP010-013) diagnostics.
- **API surface parity:** The style type taxonomy and compound naming rules defined here become normative. Future updates to the syntax reference or processing model should remain consistent with these definitions.
- **Integration coverage:** Correctness can be verified by checking that the element catalog is complete (all CommonMark elements covered) and that compound naming examples produce deterministic results. A future conformance test suite should include element interaction test cases.

## Risks & Dependencies

- **Consistency risk**: The element interactions spec must not contradict the syntax reference, attachment rule, or processing model. Mitigation: Unit 6 includes an explicit cross-reference verification pass against all three existing spec documents.
- **Completeness risk**: The ePublisher implementation may have undocumented edge cases for specific element combinations. Mitigation: the spec uses RFC 2119 language to distinguish required behavior from implementation-defined behavior, and defers Unicode handling to future specification work.
- **Compound naming ambiguity**: Deeply nested containers with mixed custom and default styles create complex compound names. Mitigation: the compound naming rule is defined formally with a recursive definition and an examples table covering the most common cases.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-element-interactions-requirements.md](../brainstorms/2026-04-08-element-interactions-requirements.md)
- Related spec: [spec/attachment-rule.md](../../spec/attachment-rule.md)
- Related spec: [spec/processing-model.md](../../spec/processing-model.md)
- Related spec: [spec/formal-grammar.md](../../spec/formal-grammar.md)
- Related reference: [syntax-reference.md](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md)
- Related solution: [docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md](../solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md)
- Related solution: [docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md](../solutions/documentation-gaps/processing-model-specification-2026-04-08.md)
- Related solution: [docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md](../solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md)
- Related issue: [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Document standard element interactions
- Related issue: [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Write a formal Markdown++ specification
