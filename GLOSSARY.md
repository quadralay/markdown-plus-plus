---
date: 2026-05-13
status: active
---

# Markdown++ Glossary

Canonical definitions for Markdown++ terminology. Each entry names the term, gives a one-paragraph definition extracted from its canonical surface, and links to the full treatment. Entries are pointers, not new prose -- the canonical surface is the source of truth.

## Conventions

Every entry has three parts:

- The **term** as a level-3 heading. The heading text determines the anchor (GitHub kebab-cases the heading) that other surfaces link to. Synonyms appear in the entry body so they do not pollute the anchor.
- A one-paragraph definition extracted (not paraphrased loosely) from the canonical surface.
- A "Full treatment" line pointing to the canonical surface with a repo-relative link.

When a term is introduced or renamed in a PR, the term's canonical surface owns the definition and this glossary tracks the term name plus a pointer.

## Repeatable Audit

To add a new term:

1. Decide on the canonical surface (typically the spec section, best-practices section, or dedicated spec file that already discusses the pattern in prose).
2. Add an entry below with the term, a one-paragraph definition extracted from that surface, and a "Full treatment" link.
3. Grep the term across the entry-point surfaces (`README.md`, `spec/`, `examples/`, `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`, and the skill `references/` directory).
4. For each (term, surface) pair, decide one of: (a) use the term and link to the glossary anchor on first prose use, (b) leave the surface untouched. Skip surfaces that do not currently discuss the pattern in prose -- this is a surfacing pass, not an authoring pass.

Surfaces that already link directly to the canonical surface (not the glossary) do not need an additional glossary link.

## Entries

### triple

**Synonym:** `alias+slug+linkref`.

The recommended Markdown++ pattern for cross-referenceable headings. The **triple** combines three pieces on a single heading: a `<!-- style:HeadingN; #alias -->` directive that attaches a stable alias to the heading, the heading text itself, and a `[semantic-slug]: #alias "Title"` link reference definition below it. The alias is a stable identifier that survives heading-text renames; the semantic slug is what other documents link with; the link reference definition binds the slug to the alias and supplies a default link text. The same reference works in standalone preview, single-file publishing, and multi-file assembly.

Full treatment: [Semantic Cross-References on Topic-Defining Headings](plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings).

### Unset

A condition state representing the absence of a definition. Each condition name has one of three states: **Visible** and **Hidden** are assigned states (set in the condition set provided at build time); **Unset** means the condition name is not defined in the condition set. Before evaluating a condition expression, a conformant processor MUST check whether all condition names are defined; if any operand is Unset, the entire block passes through as-is (opening tag, content, and closing tag preserved). This allows implementations to surface or resolve undefined conditional content downstream rather than silently including it. Variable substitution still applies to the block's content because the content survives Phase 1, Step 1 into Phase 1, Step 2.

Full treatment: [Section 11.3 Condition State Model](spec/specification.md#condition-state-model).

### attachment rule

The rule that governs how Markdown++ comment tags bind to the content elements they modify. A tag is **attached** to a target element when the tag and the element appear on immediately adjacent lines with zero blank lines between them. A blank line silently breaks attachment -- the tag passes through as a regular HTML comment with no Markdown++ effect and no visible error in standard Markdown preview. This is the most common source of Markdown++ authoring errors. The attachment rule applies to styles, aliases, markers, and combined commands. Conditions (which wrap content) and includes (standalone directives) are exempt.

Full treatment: [The Attachment Rule](spec/attachment-rule.md).

### content island

A self-contained content block created by applying a Markdown++ custom style to a CommonMark blockquote. Content islands provide a mechanism for callouts, notes, warnings, and other visually distinct content areas using standard blockquote syntax with a style convention -- they are not a new syntactic form. The style name determines how the processor renders the island (callout box, warning panel, information card, etc.); the rendering is implementation-defined. Blockquotes support rich nested content within an island (headings, lists, code blocks, nested formatting, other Markdown++ extensions).

Full treatment: [Section 15 Content Islands](spec/specification.md#15-content-islands).

### block content

**Scope:** block content inside multiline table cells.

Block-level content -- lists, blockquotes, styled elements, and other multi-line constructs -- inside a multiline table cell. Standard GFM tables limit each cell to a single line; the `<!-- multiline -->` directive enables continuation rows so that cells can hold block content. Multiline table cells are parsed as full Markdown documents with a separate parsing context per cell. Which extensions are valid inside a cell follows from the processing model's phase ordering: Phase 1 extensions (variables, conditions) operate on raw pipe-delimited text before the table is recognized; Phase 2 extensions (styles, aliases, markers, combined commands) operate during per-cell parsing.

Full treatment: [Extensions in Multiline Table Cells](spec/multiline-cell-extensions.md).
