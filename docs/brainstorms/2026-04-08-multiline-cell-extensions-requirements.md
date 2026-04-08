---
date: 2026-04-08
topic: multiline-cell-extensions
---

# Extensions in Multiline Table Cells

## Problem Frame

Multiline table cells are parsed as full Markdown documents — the ePublisher parser creates a temporary `WifMarkdown` instance per cell. This means any Markdown and potentially any Markdown++ extension could appear inside a cell. But the spec doesn't define which extensions are valid within cells or how they interact with the table context.

The processing model (issue #8) establishes a two-phase pipeline: Phase 1 operates on raw text (includes, conditions, variables), Phase 2 parses Markdown with extension extraction (styles, aliases, markers, multiline). The phase ordering determines which extensions work in cells and how — Phase 1 extensions are resolved before the table is even recognized, while Phase 2 extensions are recognized during per-cell Markdown parsing.

Without this documentation:
- Implementors must guess which extensions are valid in cells
- Authors don't know what they can safely put in table cells
- Edge cases (conditions wrapping rows, includes in cells, nested tables) have no normative guidance

## Requirements

### Phase 1 extensions in cells

- R1. The spec MUST document that **variables** work in multiline table cells. Variables are resolved in Phase 1, Step 2 (text-level substitution) before Markdown parsing. By the time the multiline table is recognized in Phase 2, all `$name;` tokens have been replaced with their values. Variable values appear as literal cell content.

- R2. The spec MUST document that **conditions** work in multiline table cells at the raw-text level. Conditions are evaluated per-file in Phase 1, Step 1 before table parsing. A condition block that wraps complete table rows (first row + continuation rows + separator) works correctly — the hidden rows are removed before Phase 2 sees the table. The spec MUST document that a condition block wrapping partial rows (e.g., some continuation rows but not others within a logical row) produces undefined table structure and SHOULD be avoided.

- R3. The spec MUST document that **include** directives are expanded in Phase 1, Step 1 before table parsing. An include directive in a cell position is technically expanded, but the included content would need to conform to the pipe-delimited table row format to preserve table structure. The spec SHOULD document this as not recommended because expanded content is unlikely to maintain valid table syntax, and the result is fragile and unportable.

### Phase 2 extensions in cells

- R4. The spec MUST document that **block styles** (`<!-- style:Name -->`) work in multiline table cells. A style directive on a continuation row attaches to the content element on the following continuation row within the same cell. This is already demonstrated in the syntax reference but should be formally specified.

- R5. The spec MUST document that **inline styles** (`<!--style:Name-->**text**`) work in multiline table cells. An inline style directive immediately before a styled element on the same line within a cell works per the standard inline attachment rule. This is already demonstrated in the syntax reference but should be formally specified.

- R6. The spec MUST document that **aliases** (`#name`) are syntactically valid inside multiline table cells but are not recommended. Since each cell is parsed as a full Markdown document, an alias would be recognized. However, aliases are navigational anchors intended for cross-referencing to block-level elements in the document outline. An alias inside a table cell does not participate in the document's navigation structure in a useful way. The spec SHOULD note that table-level aliases (on the `<!-- multiline -->` directive itself via combined commands) are the intended mechanism for cross-referencing tables.

- R7. The spec MUST document that **markers** (`marker:Key="value"`, `markers:{json}`) are syntactically valid inside multiline table cells but are unusual. Markers attach metadata to block elements, and attaching them to elements within a cell is a valid but uncommon use case (e.g., marking a specific cell's content for indexing).

- R8. The spec MUST document that **nested multiline tables** are technically possible since each cell is parsed as a full Markdown document, but SHOULD be strongly discouraged. The authoring constraints of pipe-delimited continuation rows make nested tables extremely difficult to write, read, and maintain. The spec SHOULD note that alternative approaches (restructuring content, using separate tables, or using styled lists) are preferred.

### Standard Markdown in cells

- R9. The spec MUST document that standard Markdown block elements work in multiline table cells: paragraphs, lists (ordered and unordered), blockquotes, inline formatting (bold, italic, links, code spans, images). These are already demonstrated in existing examples.

- R10. The spec MUST document that **headings** in multiline table cells are syntactically valid but semantically questionable. Headings inside cells do not participate in the document outline and may confuse readers and tools that expect headings to define document structure. The spec SHOULD recommend using bold text or styled paragraphs instead of headings within cells.

- R11. The spec MUST document that **fenced code blocks** in multiline table cells require careful formatting. The opening and closing fence lines must appear on continuation rows, and the code content must fit within the cell's column boundaries. This is valid but may be difficult to author cleanly.

### Interaction rules

- R12. The spec MUST document the general principle: Phase 1 extensions (variables, conditions, includes) operate on the raw text that contains the table rows, before the table is recognized. Phase 2 extensions (styles, aliases, markers, multiline) operate during per-cell Markdown parsing after the table structure has been identified. This phase-ordering principle determines all extension interactions with cells.

- R13. The spec MUST document that **combined commands** within cells follow the same evaluation order as outside cells: style (1), multiline (2), marker (3), alias (4). A combined command on a continuation row within a cell is valid.

## Success Criteria

- A Markdown++ author can consult the spec to determine whether a given extension is valid inside a multiline table cell and what restrictions apply
- An implementor can read the spec and correctly handle all extension types within multiline table cells
- The documentation is consistent with the processing model (`spec/processing-model.md`) and the formal grammar (`spec/formal-grammar.md`)
- Edge cases (conditions wrapping rows, nested tables, headings in cells) have clear normative guidance

## Scope Boundaries

- **In scope**: Enumerating which extensions work in cells, documenting restrictions, providing guidance on edge cases
- **In scope**: Explaining why each extension does or doesn't work based on the processing model's phase ordering
- **Out of scope**: Changing the processing model or the multiline table syntax
- **Out of scope**: Defining new MDPP diagnostic codes for cell-specific errors (follow-up work if needed)
- **Out of scope**: Modifying the syntax reference examples (though the spec section this produces may reference them)

## Key Decisions

- **Phase ordering is the organizing principle**: Rather than an arbitrary list of "works / doesn't work," the document should explain that Phase 1 vs. Phase 2 determines everything. This gives authors and implementors a mental model, not just a lookup table. **Why:** The processing model is already the authoritative source for phase ordering; this document applies that model to the specific context of cells. **How to apply:** Structure the spec section around Phase 1 extensions in cells vs. Phase 2 extensions in cells.

- **"Valid but not recommended" is a useful category**: Some extensions (aliases in cells, nested tables, includes in cells) are syntactically valid but practically problematic. The spec should acknowledge validity while providing clear guidance. **Why:** Forbidding valid syntax creates spec/implementation divergence; silently allowing it creates author confusion. **How to apply:** Use SHOULD NOT or "not recommended" language rather than MUST NOT for these cases.

- **Existing syntax reference examples are normative**: The styles-in-cells examples already in the syntax reference establish that block and inline styles work in cells. This requirements document formalizes and extends that. **Why:** Avoids contradicting existing documentation. **How to apply:** Reference existing examples rather than replacing them.

## Dependencies / Assumptions

- Depends on the processing model (`spec/processing-model.md`) for the phase ordering that determines extension behavior in cells
- Assumes the ePublisher behavior (per-cell WifMarkdown instance) is the model to formalize, as it is the only production implementation
- Assumes the formal grammar (`spec/formal-grammar.md`) does not need modification — grammar productions are context-free and already apply within cells
- Related to issue #9 (element interactions) — this document covers one specific interaction context (multiline table cells) that #9 would cover more broadly
- Related to issue #20 (multiline table row separators) — row separator syntax affects how conditions can wrap rows

## Outstanding Questions

### Deferred to Planning

- [Affects R2][Needs research] How should the spec handle a condition block that wraps some but not all continuation rows within a logical row? The Phase 1 text removal could leave orphaned continuation rows. Need to determine whether to specify this as an error (with a diagnostic code) or simply as "undefined behavior that authors should avoid."
- [Affects R8][Technical] Should nested multiline tables be explicitly prohibited with a MUST NOT, or merely discouraged with SHOULD NOT? The difference affects conformance testing — MUST NOT requires implementations to detect and reject, SHOULD NOT allows but discourages.
- [Affects R11][Needs research] What is the practical behavior of fenced code blocks inside multiline table cells in the ePublisher parser? Need to verify this works before specifying it.
- [Affects all][Technical] Where should this specification live? Options: (a) a new subsection in `spec/processing-model.md` under Phase 2, (b) a dedicated `spec/multiline-cell-extensions.md`, or (c) integrated into a broader `spec/element-interactions.md` when issue #9 is addressed. Planning should evaluate based on document size and cross-referencing needs.

## Next Steps

→ `/ce:plan` for structured implementation planning
