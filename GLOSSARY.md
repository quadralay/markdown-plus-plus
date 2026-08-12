---
date: 2026-05-13
status: active
---

# Markdown++ Glossary

Canonical definitions for Markdown++ terminology. Each entry names a term, gives a one-paragraph definition lifted from its canonical surface, and links to the full treatment. Entries are pointers; the canonical surface owns the definition.

## Conventions

Each entry has three parts:

- The **term** as a level-3 heading. The heading text determines the anchor (GitHub kebab-cases the heading) that other surfaces link to. Synonyms go in the entry body so they stay out of the anchor.
- A one-paragraph definition lifted from the canonical surface.
- A "Full treatment" line pointing to the canonical surface with a repo-relative link.

When a term is introduced or renamed in a PR, the term's canonical surface owns the definition and this glossary tracks the term name plus a pointer.

## Repeatable Audit

To add a new term:

1. Decide on the canonical surface (typically the spec section, best-practices section, or dedicated spec file that already discusses the pattern in prose).
2. Add an entry below with the term, a one-paragraph definition lifted from that surface, and a "Full treatment" link.
3. Grep the term across the entry-point surfaces (`README.md`, `spec/`, `examples/`, `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`, and the skill `references/` directory).
4. For each (term, surface) pair, decide one of: (a) use the term and link to the glossary anchor on first prose use, (b) leave the surface untouched. Skip surfaces that do not currently discuss the pattern in prose; the audit surfaces existing terminology rather than authoring new content.

Surfaces that already link directly to the canonical surface (not the glossary) do not need an additional glossary link.

## Entries

### triple

**Synonym:** `alias+slug+linkref`.

The recommended Markdown++ pattern for cross-referenceable headings. The **triple** combines three pieces on a single heading: a `<!-- style:HeadingN; #alias -->` directive that attaches a stable alias to the heading, the heading text itself, and a `[semantic-slug]: #alias "Title"` link reference definition below it. The same reference works in standalone preview, single-file publishing, and multi-file assembly. The alias decouples the link target from heading text (heading renames don't break references); co-location keeps the three pieces together when a section moves, is deleted, or reordered. The slug may be a separate semantic name (when the alias is opaque) or reuse the alias value (when the alias is itself semantic and unique-by-construction).

Full treatment: [Semantic Cross-References on Topic-Defining Headings](plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings).

### Unset

A condition state for a name that is not defined in the condition set. Each condition name has one of three states: **Visible** and **Hidden** are assigned states (set in the condition set provided at build time); **Unset** means the condition name is not defined in the condition set. Before evaluating a condition expression, a conformant processor MUST check whether all condition names are defined; if any operand is Unset, the entire block passes through as-is (opening tag, content, and closing tag preserved). This allows implementations to surface or resolve undefined conditional content downstream rather than silently including it. Variable substitution still applies to the block's content because the content survives Phase 1, Step 1 into Phase 1, Step 2.

Full treatment: [Section 11.3 Condition State Model](spec/specification.md#condition-state-model).

### attachment rule

The rule that governs how Markdown++ comment tags bind to the content elements they modify. A tag is **attached** to a target element when the tag and the element appear on immediately adjacent lines with zero blank lines between them. A blank line silently breaks attachment -- the tag passes through as a regular HTML comment with no Markdown++ effect and no visible error in standard Markdown preview. This is the most common source of Markdown++ authoring errors. The attachment rule applies to styles, aliases, markers, and combined commands. Conditions (which wrap content) and includes (standalone directives) are exempt.

Full treatment: [The Attachment Rule](spec/attachment-rule.md).

### content island

A self-contained content block created by applying a Markdown++ custom style to a CommonMark blockquote. Content islands are how authors mark up callouts, notes, warnings, and other visually distinct content areas without inventing new syntax -- the blockquote stays a standard CommonMark blockquote, and the style name on it tells the processor how to render the island (callout box, warning panel, information card, etc.). The rendering is implementation-defined. Blockquotes support rich nested content within an island (headings, lists, code blocks, nested formatting, other Markdown++ extensions).

Full treatment: [Section 15 Content Islands](spec/specification.md#15-content-islands).

### block content

**Scope:** block content inside multiline table cells.

Block-level content -- lists, blockquotes, styled elements, and other multi-line constructs -- inside a multiline table cell. Standard GFM tables limit each cell to a single line; the `<!-- multiline -->` directive enables continuation rows so that cells can hold block content. Multiline table cells are parsed as full Markdown documents with a separate parsing context per cell. Which extensions are valid inside a cell follows from the processing model's phase ordering: Phase 1 extensions (variables, conditions) operate on raw pipe-delimited text before the table is recognized; Phase 2 extensions (styles, aliases, markers, combined commands) operate during per-cell parsing.

Full treatment: [Extensions in Multiline Table Cells](spec/multiline-cell-extensions.md).

### conditional row

The supported granularity for conditions in tables. A **conditional row** is a complete table row wrapped by a condition block: in a standard table, a condition block MAY wrap complete physical rows; in a multiline table, it MAY wrap complete logical rows -- the first row, all of its continuation rows, and its trailing whitespace-only separator row. A condition block MAY also wrap an entire table. Conditional rows evaluate identically to conditions anywhere else, because Phase 1 condition evaluation is table-blind (it operates on raw text before the table is recognized). Contrast with the in-cell condition span and conditional cell, which are authoring anti-patterns surfaced by validation (MDPP019).

Full treatment: [Conditions in Multiline Table Cells](spec/multiline-cell-extensions.md).

### in-cell condition span

A condition span that opens and closes within a single table cell on one physical line. Authors **SHOULD NOT** author an in-cell condition span. Its behavior is mechanically determined by Phase 1 raw-text evaluation -- Visible strips the tags, Hidden removes the span (the cell may become empty), Unset passes tags and content through as literal cell text -- but the pattern resists line wrapping (the span is an unbreakable atomic unit for any wrapping tool) and a span split across physical lines corrupts the table when Hidden (removal consumes the intervening newline and pipe delimiters). Prefer conditional row variants for structural differences and variables for value substitution. The validator flags it as MDPP019 (warning).

Full treatment: [Conditions in Multiline Table Cells](spec/multiline-cell-extensions.md).

### conditional cell

A condition span that contains an unescaped `|` cell delimiter. A conditional cell **MUST NOT** be authored: hiding such a span removes cell boundaries and changes the row's column count, so the resulting table structure is corrupt. Because Phase 1 condition evaluation is table-blind, a processor cannot reject the pattern -- it is an authoring requirement surfaced by validation (MDPP019, warning), not processor behavior. Use conditional rows for structural differences and variables for value substitution instead.

Full treatment: [Conditions in Multiline Table Cells](spec/multiline-cell-extensions.md).

### command

A Markdown++ instruction carried inside an HTML comment: `style:`, `#alias`, `marker:`/`markers:`, `multiline`, `condition:`/`/condition`, or `include:`. The command is the payload; the [comment tag](#comment-tag) is the `<!-- -->` container that carries it. An HTML comment whose content matches at least one recognized command pattern is an extension comment (synonym: **directive**) and is subject to Markdown++ processing; a comment matching no pattern is a regular HTML comment and is ignored. Vocabulary discipline: describe payloads as commands and reserve "tag" for the comment container -- combining is always "commands in the same comment tag, separated by `;`", never one tag placed above another (stacked tags orphan the upper tag, MDPP009).

Full treatment: [Section 5 Extension Comment Syntax](spec/specification.md#5-extension-comment-syntax).

### comment tag

The `<!-- ... -->` HTML comment container that carries one or more Markdown++ [commands](#command). Comment syntax keeps Markdown++ extensions invisible in standard Markdown renderers -- the core backward-compatibility principle of the format. A comment tag MUST stay on a single physical line, and it binds to its target element under the [attachment rule](#attachment-rule): block-level on the line directly above the element, inline immediately before the syntax with no space between. Placement rules are stated about the comment tag; payload semantics are stated about its commands.

Full treatment: [Section 5 Extension Comment Syntax](spec/specification.md#5-extension-comment-syntax).

### combined command

A single HTML comment containing multiple Markdown++ [commands](#command) separated by semicolons, e.g. `<!-- style:DataTable ; multiline -->` or `<!-- style:Heading2 ; #200020 -->`. Combined commands exist because the [attachment rule](#attachment-rule) makes stacked tags orphan the top tag -- one comment tag attaches to one element, so a combined command is the only way to apply several commands to the same element. Styles, the `multiline` indicator, markers, and aliases MAY combine; conditions and includes MUST NOT appear in a combined command. The recommended evaluation order is style, multiline, marker(s), alias, regardless of the order written in the comment.

Full treatment: [Section 16 Combined Commands](spec/specification.md#16-combined-commands).
