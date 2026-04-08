---
date: 2026-04-08
topic: element-interactions
---

# Standard Element Interactions for Markdown++

## Problem Frame

Markdown++ extends CommonMark 0.30 with style tags, aliases, markers, and other extensions, but the repository does not document how these extensions interact with each standard Markdown element. The syntax reference describes extension syntax and attachment rules; it does not describe what happens when a style tag is applied to a specific element type — what style type it produces, what default name it receives, how compound names form in containers, or how heading aliases are auto-generated.

Without this documentation:
- Authors cannot predict what style name a processor will generate for styled content inside a blockquote or list
- The style type taxonomy (Paragraph, Character, Graphic, Table) is undocumented, so authors don't know how styles will behave in output
- The heading alias auto-generation algorithm is undocumented, so cross-references are fragile
- Compound naming rules for nested containers are absent, making nested styled content trial-and-error
- Several standard elements (titles, horizontal rules, indented code blocks, block/inline HTML) have no Markdown++ documentation at all

The legacy ePublisher documentation contains 15 detailed pages covering these interactions. This information is critical for any author or implementor working with Markdown++, and must be formalized as part of the open specification.

## Requirements

### Style type taxonomy

- R1. The spec MUST define four style types that Markdown++ extensions produce: **Paragraph** (block-level text elements), **Character** (inline text elements), **Graphic** (images), and **Table** (table elements). Each standard Markdown element maps to exactly one style type.
- R2. The spec MUST provide a complete mapping from every supported CommonMark element to its style type, default style name, and whether it accepts style tags.

### Block-level elements

- R3. The spec MUST document **setext headings (titles)**: they accept style tags, map to "Title 1" (double underline) and "Title 2" (single underline), and produce Paragraph style type.
- R4. The spec MUST document **ATX headings**: they accept style tags, map to "Heading 1" through "Heading 6" by default, and produce Paragraph style type. Custom style tags override the default name.
- R5. The spec MUST document the **heading alias auto-generation algorithm**: lowercase the heading text, remove all non-alphanumeric characters (except spaces), replace spaces with hyphens. Example: `# Let's Go to the Moon!` produces alias `lets-go-to-the-moon`. This algorithm applies to both ATX and setext headings. Custom aliases (via `<!--#name-->`) supplement the auto-generated alias — both are valid anchors.
- R6. The spec MUST document **paragraphs**: they accept style tags, default name is "Paragraph", and produce Paragraph style type.
- R7. The spec MUST document **blockquotes as content islands**: they accept style tags, default name is "Blockquote", and produce Paragraph style type. Content nested inside a blockquote receives compound style names (see R14).
- R8. The spec MUST document **ordered lists**: they accept style tags, default names are "OList" (for the list container) and "OList Item" (for list items), and produce Paragraph style type. Nested content within list items receives compound style names (see R14).
- R9. The spec MUST document **unordered lists**: they accept style tags, default names are "UList" (for the list container) and "UList Item" (for list items), and produce Paragraph style type. Unlike markers (switching between `-`, `*`, `+`) break the list into separate lists.
- R10. The spec MUST document **indented code blocks**: they accept style tags, default name is "Code Block", and produce Paragraph style type.
- R11. The spec MUST document **fenced code blocks**: they accept style tags, default name is "Code Fence", and produce Paragraph style type.
- R12. The spec MUST document **horizontal rules** (`---`, `***`, `___`): they accept style tags, default name is "Horizontal Rule", and produce Paragraph style type.
- R13. The spec MUST document **block HTML** and **inline HTML**: they accept style tags but are not available in PDF output. The spec should note the output-format dependency.

### Compound style naming in containers

- R14. The spec MUST define the compound style naming rule for nested content inside containers (blockquotes and lists): when content is nested inside a styled container, the style name is composed as `"ContainerStyle ElementDefault"` (space-separated). Examples:
  - A heading inside a blockquote: `"Blockquote Heading 1"`
  - A paragraph inside a custom blockquote: `"CustomBQ Paragraph"` or with both custom: `"CustomBQ CustomParagraph"`
  - A paragraph inside an ordered list: `"OList Paragraph"` or with custom list: `"OList CustomParagraph"`
- R15. The spec MUST state that **nested lists do not inherit parent custom styles**. Each nesting level requires its own style tag to receive a custom name. Without a style tag, nested content uses the default compound name.

### Inline elements

- R16. The spec MUST document **bold**, **italic**, **strikethrough**, and **code spans**: they accept inline style tags, and produce Character style type. The style tag is placed immediately before the formatted text with no space.
- R17. The spec MUST document **links**: they accept inline style tags, produce Character style type, and support cross-document alias linking (e.g., `[text](other-doc.md#alias)`).
- R18. The spec MUST document **images**: they accept inline style tags and produce **Graphic** style type — the only element type that produces this style type.

### Tables

- R19. The spec MUST document that **tables** accept style tags and produce **Table** style type. A single custom style name on a table generates three style names in output: `"Name"` (for the table itself), `"Name Cell Head"` (for header cells), and `"Name Cell Body"` (for body cells). Default names are "Table", "Table Cell Head", and "Table Cell Body".

### TOC integration

- R20. The spec SHOULD document how heading levels map to table-of-contents depth, and how custom heading styles interact with TOC generation.

## Success Criteria

- An author can look up any standard Markdown element and immediately know: what style type it produces, what its default style name is, whether it accepts style tags, and how nesting affects the generated name
- The heading alias auto-generation algorithm is specified precisely enough that two independent implementations produce the same alias for the same heading text
- The compound naming rules are unambiguous — given a styled container with nested styled content, the resulting style names are deterministic
- The document is consistent with the existing syntax reference, attachment rule spec, and processing model spec — no contradictions
- All 14 element categories from the issue's gap analysis table are addressed

## Scope Boundaries

- **In scope**: Complete element-by-element catalog with style types, default names, and behavioral details
- **In scope**: Style type taxonomy (Paragraph, Character, Graphic, Table)
- **In scope**: Compound style naming rules for containers (blockquotes, lists)
- **In scope**: Heading alias auto-generation algorithm
- **In scope**: Nested list style non-inheritance behavior
- **In scope**: Unlike-marker list-breaking behavior for unordered lists
- **Out of scope**: Modifying the existing syntax reference — this is an additive specification document
- **Out of scope**: Defining new extension syntax — this documents existing behavior
- **Out of scope**: Output-format-specific rendering (HTML, PDF, XML details) — only the abstract style model
- **Out of scope**: Multiline table cell interactions — already covered in the syntax reference
- **Out of scope**: Processing pipeline or evaluation order — covered by the processing model spec

## Key Decisions

- **Spec location**: `spec/element-interactions.md`, alongside `attachment-rule.md`, `processing-model.md`, and `formal-grammar.md`. Rationale: this is normative specification content defining how the format behaves, not skill-level guidance. The skill references can cross-reference it.
- **Single document, not scattered sections**: One comprehensive reference is more useful than adding sections to multiple existing files. Rationale: authors need a single place to look up any element's behavior; implementors need a complete catalog for conformance.
- **Style type taxonomy is normative**: The four-type system (Paragraph, Character, Graphic, Table) is part of the format specification, not an ePublisher implementation detail. Rationale: style types determine how output processors handle styled content, and must be consistent across implementations.
- **Compound naming is space-separated**: Container + element names are joined with a space (`"Blockquote Heading 1"`, not `"Blockquote-Heading-1"` or `"BlockquoteHeading1"`). Rationale: this matches the existing ePublisher behavior and is the established convention.
- **Auto-generated aliases supplement, not replace**: Custom aliases via `<!--#name-->` create additional anchors alongside the auto-generated heading alias. Rationale: this preserves backward compatibility and matches existing behavior documented in the syntax reference.

## Dependencies / Assumptions

- Assumes the legacy ePublisher documentation accurately describes the intended behavior for all element interactions — this is the only production implementation
- Assumes `spec/attachment-rule.md` remains authoritative for tag attachment mechanics — the element interactions spec defines what happens after attachment, not the attachment itself
- Assumes the syntax reference continues to define extension syntax — the element interactions spec defines element-specific semantics
- The processing model spec (R18 output model) defines that processing produces "a CommonMark document tree annotated with Markdown++ metadata" — the element interactions spec defines what that metadata looks like for each element type

## Outstanding Questions

### Deferred to Planning

- [Affects R5][Needs research] Verify the exact heading alias auto-generation algorithm against the ePublisher implementation. Specifically: how are consecutive spaces handled? How are Unicode characters handled? What happens with empty headings or headings that are entirely non-alphanumeric?
- [Affects R14][Needs research] Verify compound naming behavior for deeply nested containers (e.g., a list inside a blockquote inside another blockquote). Does compounding continue recursively (`"BQ1 BQ2 Paragraph"`) or is there a depth limit?
- [Affects R19][Technical] Verify whether the three-name table pattern applies to multiline tables identically to standard tables, or if multiline tables have different naming behavior.
- [Affects R13][Needs research] Clarify exactly which output formats support block/inline HTML styling. The legacy docs say "not available in PDF" — confirm whether this is a format-level constraint or an ePublisher-specific limitation.
- [Affects R20][Technical] Determine whether TOC level mapping behavior should be normative (required for all processors) or informational (describing common behavior). TOC generation may be too output-specific for the format spec.

## Next Steps

→ `/ce:plan` for structured implementation planning
