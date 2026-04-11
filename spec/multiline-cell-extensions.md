---
date: 2026-04-08
status: active
---

# Extensions in Multiline Table Cells

## Introduction

This document specifies which Markdown++ extensions are valid inside multiline table cells, how they interact with the table context, and what restrictions apply. It complements the [Processing Model](processing-model.md), which defines the two-phase pipeline, and the [Attachment Rule](attachment-rule.md), which defines how tags bind to content elements. The [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) provides authoring examples including styled content in multiline table cells.

Multiline table cells are parsed as full Markdown documents -- the processor creates a separate parsing context per cell. This means any Markdown and potentially any Markdown++ extension could appear inside a cell. This document defines which extensions are valid, which are prohibited, and how the processing model's phase ordering determines cell behavior.

The conformance keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Phase-Ordering Principle

The [Processing Model](processing-model.md) defines a two-phase pipeline that determines all extension interactions with multiline table cells:

- **Phase 1** (pre-processing) operates on raw text before any Markdown parsing occurs. Phase 1 extensions -- includes, conditions, and variables -- see the raw pipe-delimited table rows as plain text. They do not know they are operating inside a table.

- **Phase 2** (Markdown parsing with extension extraction) parses the Phase 1 output text as CommonMark. The multiline table directive is recognized during Phase 2, and each cell's content is parsed as a separate Markdown document. Phase 2 extensions -- styles, aliases, markers, and combined commands -- operate during this per-cell parsing.

This phase ordering is the organizing principle for the rest of this document. Whether an extension works in a cell, and how it works, follows directly from which phase processes it.

## Extension Summary

| Extension | Phase | Category | Notes |
|-----------|:-----:|----------|-------|
| Variables | 1 | Supported | Resolved before table is recognized |
| Conditions | 1 | Supported | Operate on raw text; partial row wrapping produces undefined structure |
| Includes | 1 | Not supported | MUST NOT appear inside cell content |
| Block styles | 2 | Supported | Directive on continuation row attaches to following content |
| Inline styles | 2 | Supported | Standard inline attachment rule applies |
| Aliases | 2 | Valid but not recommended | Do not participate in document navigation usefully |
| Markers | 2 | Supported | Attach metadata to block elements within cells |
| Nested multiline tables | 2 | Not supported | MUST NOT appear inside cell content |
| Combined commands | 2 | Supported | Same evaluation order as outside cells |

## Phase 1 Extensions in Cells

### Variables

Variables work in multiline table cells. Variable tokens (`$name;`) are resolved in Phase 1, Step 2 (variable substitution) before Markdown parsing. By the time the multiline table is recognized in Phase 2, all variable tokens have been replaced with their values. Variable values appear as literal cell content.

A conformant processor MUST resolve variable tokens inside table rows identically to variable tokens anywhere else in the document.

**Example -- variable in a cell:**

```markdown
<!-- multiline -->
| Product      | Version                  |
|--------------|--------------------------|
| $Product;    | $Version;                |
|              | Released: $ReleaseDate;  |
```

With the variable map `Product = "WidgetPro"`, `Version = "3.2"`, `ReleaseDate = "2026-01-15"`, Phase 1 resolves the table to:

```markdown
<!-- multiline -->
| Product      | Version                  |
|--------------|--------------------------|
| WidgetPro    | 3.2                      |
|              | Released: 2026-01-15     |
```

Phase 2 then parses the resolved table normally.

### Conditions

Conditions work in multiline table cells at the raw-text level. Condition blocks are evaluated per-file in Phase 1, Step 1 before table parsing. Conditions see the table rows as plain text lines and remove, keep, or pass them through (with condition tags preserved) based on the condition set.

#### Wrapping Complete Rows

A condition block that wraps complete table rows -- including the first row, all continuation rows, and the row separator -- works correctly. The hidden rows are removed before Phase 2 sees the table.

A conformant processor MUST evaluate condition blocks that wrap complete table rows identically to condition blocks anywhere else in the document.

**Example -- condition wrapping complete rows (correct):**

```markdown
<!-- multiline -->
| Feature     | Description              |
|-------------|--------------------------|
| Core        | Available on all plans.  |
|             | - Basic analytics        |
|             | - Email support          |
|             |                          |
<!--condition:enterprise-->
| Enterprise  | Premium features:        |
|             | - SSO integration        |
|             | - Dedicated support      |
|             |                          |
<!--/condition-->
| Community   | Free tier features.      |
|             | - Forum access           |
```

When `enterprise` is Hidden, the entire Enterprise row (first row + continuation rows + separator) is removed. Phase 2 sees a valid two-row table with Core and Community rows.

#### Partial Row Wrapping

A condition block that wraps some but not all continuation rows within a single logical row produces undefined table structure. The condition engine removes lines correctly, but the resulting table has orphaned continuation rows that do not belong to any first row. Authors SHOULD avoid partial row wrapping.

**Example -- condition wrapping partial rows (incorrect):**

```markdown
<!-- multiline -->
| Feature     | Description              |
|-------------|--------------------------|
| Analytics   | Usage tracking:          |
<!--condition:advanced-->
|             | - Funnel analysis        |
|             | - Cohort reports         |
<!--/condition-->
|             | - Basic dashboards       |
```

When `advanced` is Hidden, the two continuation rows are removed, leaving "Basic dashboards" as an orphaned continuation row that may or may not associate correctly with the Analytics row. The resulting table structure is undefined.

**Correct approach** -- wrap the entire logical row and provide separate rows per condition:

```markdown
<!-- multiline -->
| Feature     | Description              |
|-------------|--------------------------|
<!--condition:advanced-->
| Analytics   | Usage tracking:          |
|             | - Funnel analysis        |
|             | - Cohort reports         |
|             | - Basic dashboards       |
|             |                          |
<!--/condition-->
<!--condition:!advanced-->
| Analytics   | Usage tracking:          |
|             | - Basic dashboards       |
|             |                          |
<!--/condition-->
```

### Includes

Include directives inside multiline table cells are NOT supported. Implementations MUST NOT process include directives that appear within table cell content.

Although includes are expanded in Phase 1, Step 1 before table parsing, the expanded content would need to conform to the pipe-delimited table row format to preserve table structure. Since included file content is unlikely to maintain valid pipe-delimited syntax, and the result is fragile and unportable, this usage is prohibited.

**Example -- include in a cell (prohibited):**

```markdown
<!-- multiline -->
| Topic       | Details                  |
|-------------|--------------------------|
| Overview    | <!-- include:intro.md -->  |
```

The included file's content would be spliced into the raw text as-is. Unless the file contains properly formatted pipe-delimited continuation rows, the table structure will break. Authors MUST use alternative approaches such as placing the include outside the table or restructuring the content.

## Phase 2 Extensions in Cells

### Block Styles

Block styles (`<!-- style:Name -->`) work in multiline table cells. A style directive on a continuation row attaches to the content element on the following continuation row within the same cell. This follows the standard [Attachment Rule](attachment-rule.md) -- the directive MUST appear on the line directly above the target element with no intervening blank line.

A conformant processor MUST apply block styles within cells identically to block styles outside cells.

**Example -- block style in a cell:**

```markdown
<!-- multiline -->
| Name | Details                  |
|------|--------------------------|
| Bob  | Lives in Dallas.         |
|      | <!-- style:Hobbies -->   |
|      | - Enjoys cycling         |
|      | - Loves cooking          |
```

The `style:Hobbies` directive attaches to the unordered list that follows it. The list receives the "Hobbies" style within Bob's Details cell.

See the [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) Styled Content in Cells section for additional examples.

### Inline Styles

Inline styles (`<!--style:Name-->`) work in multiline table cells. An inline style directive immediately before a styled element on the same line works per the standard inline [Attachment Rule](attachment-rule.md) -- no space between the closing `-->` and the element.

A conformant processor MUST apply inline styles within cells identically to inline styles outside cells.

**Example -- inline style in a cell:**

```markdown
<!-- multiline -->
| Topic | Description              |
|-------|--------------------------|
| Intro | This is                  |
|       | <!--style:Emphasis-->**important** text. |
```

The `style:Emphasis` directive attaches to the bold text "important" on the same line. There MUST be no space between `-->` and the styled element.

See the [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) Styled Content in Cells section for additional examples.

### Aliases

Aliases (`#name`) are syntactically valid inside multiline table cells but are not recommended. Since each cell is parsed as a full Markdown document, an alias directive is recognized and processed. However, aliases are navigational anchors intended for cross-referencing to block-level elements in the document outline. An alias inside a table cell does not participate in the document's navigation structure in a useful way.

Authors SHOULD NOT use aliases inside cells. Table-level aliases on the `<!-- multiline -->` directive itself via combined commands are the intended mechanism for cross-referencing tables.

**Example -- table-level alias (recommended):**

```markdown
<!-- #pricing ; multiline -->
| Plan     | Price                    |
|----------|--------------------------|
| Basic    | $19/month                |
|          | - 5 users included       |
```

The alias `#pricing` is on the multiline directive and attaches to the table element, making it a navigational anchor in the document outline.

**Example -- alias inside a cell (not recommended):**

```markdown
<!-- multiline -->
| Plan     | Price                    |
|----------|--------------------------|
| Basic    | <!-- #basic-plan -->     |
|          | $19/month                |
```

The alias `#basic-plan` is recognized but does not produce a useful navigational anchor because it is inside a cell's parsing context rather than at the document level.

### Markers

Markers (`marker:Key="value"`, `markers:{json}`) are syntactically valid inside multiline table cells. Markers attach metadata to block elements, and attaching them to elements within a cell is a valid use case -- for example, marking specific cell content for indexing or conditional processing by downstream tools.

A conformant processor MUST recognize marker directives within cells and attach them to the target element per the standard [Attachment Rule](attachment-rule.md).

**Example -- marker in a cell:**

```markdown
<!-- multiline -->
| Term        | Definition               |
|-------------|--------------------------|
| API         | <!-- marker:Keywords="api,rest" --> |
|             | Application Programming  |
|             | Interface. A set of      |
|             | protocols for building   |
|             | software.                |
```

The marker attaches to the paragraph that follows it within the API cell, tagging that content with the keyword metadata.

### Nested Multiline Tables

Nested multiline tables inside multiline table cells are NOT supported. Although each cell is parsed as a full Markdown document, implementations MUST NOT support nested multiline tables within cells.

The authoring constraints of pipe-delimited continuation rows make nested tables extremely difficult to write, read, and maintain. A nested table's pipe characters would conflict with the outer table's column delimiters, producing ambiguous structure.

Authors requiring tabular content within a table cell MUST use alternative approaches:

- Restructure the content to avoid nesting
- Use separate tables with cross-references
- Use styled lists to present structured data within cells

### Combined Commands

Combined commands within cells follow the same evaluation order as outside cells. The [Processing Model](processing-model.md) defines the recommended evaluation order: style (1), multiline (2), marker (3), alias (4). A combined command on a continuation row within a cell is valid and SHOULD be evaluated in this same order for readability and consistency. Processors MAY evaluate segments in any order.

**Example -- combined command in a cell:**

```markdown
<!-- multiline -->
| Section  | Content                  |
|----------|--------------------------|
| Notes    | General notes:           |
|          | <!-- style:Important ; marker:Keywords="critical" --> |
|          | > This information is    |
|          | > essential for setup.   |
```

The combined command applies the style "Important" and the marker `Keywords="critical"` to the blockquote that follows. Style is evaluated first (order 1), then marker (order 3), per the standard evaluation order.

## Standard Markdown in Cells

### Block and Inline Elements

Standard Markdown block and inline elements work in multiline table cells. Each cell is parsed as a full Markdown document, so all CommonMark content is valid:

- **Paragraphs** -- Text on continuation rows forms paragraphs within the cell.
- **Unordered lists** -- Lines starting with `-`, `*`, or `+` on continuation rows.
- **Ordered lists** -- Lines starting with `1.`, `2.`, etc. on continuation rows.
- **Blockquotes** -- Lines starting with `>` on continuation rows.
- **Inline formatting** -- Bold, italic, links, code spans, and images within cell content.

See the [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) Multiline Tables section for examples of lists and blockquotes in cells.

### Headings

Headings (`#`, `##`, etc.) in multiline table cells are syntactically valid but semantically questionable. Since each cell is parsed as a full Markdown document, heading syntax is recognized. However, headings inside cells do not participate in the document outline and may confuse readers and tools that expect headings to define document structure.

Authors SHOULD use bold text or styled paragraphs instead of headings within cells.

**Example -- heading in a cell (not recommended):**

```markdown
<!-- multiline -->
| Section  | Content                  |
|----------|--------------------------|
| Details  | ## Overview              |
|          | This section covers...   |
```

**Example -- styled paragraph alternative (recommended):**

```markdown
<!-- multiline -->
| Section  | Content                  |
|----------|--------------------------|
| Details  | <!-- style:CellHeading --> |
|          | Overview                 |
|          | This section covers...   |
```

The styled paragraph achieves the visual distinction of a heading without disrupting the document outline.

### Fenced Code Blocks

Fenced code blocks in multiline table cells are valid per the parsing model. The opening and closing fence lines appear on continuation rows, and the code content appears on additional continuation rows between them. This is valid because each cell is parsed as a full Markdown document.

Authors SHOULD be aware that fenced code blocks in cells can be difficult to author cleanly due to the pipe-delimited format. The code content, opening fence, and closing fence must all fit within the cell's column boundaries.

**Example -- fenced code block in a cell:**

```markdown
<!-- multiline -->
| Language | Example                  |
|----------|--------------------------|
| Python   | A simple greeting:       |
|          | ```python                |
|          | print("Hello, world!")   |
|          | ```                      |
```

The fenced code block is recognized during per-cell Markdown parsing. Implementation verification is recommended for this usage, as practical behavior may vary across processors.

## Edge Cases

### Empty Cells

A cell with no content (empty first-row cell) or a cell with only whitespace on continuation rows produces an empty cell in the output. This is standard multiline table behavior and is not affected by extensions.

### Single vs. Multiple Continuation Rows

A cell with a single continuation row is valid. Extensions on that single continuation row follow the same rules as in cells with multiple continuation rows. The attachment rule applies regardless of how many continuation rows a cell contains.

### Styles and Lists in the Same Cell

A style directive within a cell attaches to the next content element per the attachment rule. When the next element is a list, the entire list receives the style.

```markdown
<!-- multiline -->
| Feature  | Details                  |
|----------|--------------------------|
| Setup    | Configuration steps:     |
|          | <!-- style:StepList -->  |
|          | 1. Install package       |
|          | 2. Run setup wizard      |
|          | 3. Verify installation   |
```

The `style:StepList` directive attaches to the ordered list. The preceding paragraph ("Configuration steps:") is not affected by the style.

### Conditions Wrapping the Entire Table

A condition block MAY wrap an entire multiline table, including the `<!-- multiline -->` directive. This is a standard Phase 1 operation -- the condition removes, keeps, or passes through all the table rows (with condition tags preserved) as raw text before Phase 2 sees them.

```markdown
<!--condition:show-comparison-->
<!-- multiline -->
| Feature     | Basic | Advanced |
|-------------|-------|----------|
| Storage     | 10GB  | 100GB    |
|             |       |          |
| Support     | Email | Priority |
<!--/condition-->
```

When `show-comparison` is Hidden, the entire table is removed.

## Related Specifications

- [The Processing Model](processing-model.md) -- Defines the two-phase pipeline and phase-ordering principle that determines all extension interactions with cells.
- [The Attachment Rule](attachment-rule.md) -- Defines how block-level and inline tags bind to content elements, including within cells.
- [Formal Grammar](formal-grammar.md) -- Defines the grammar for all Markdown++ extension constructs. Grammar productions are context-free and apply within cells without modification.
- [Syntax Reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) -- Provides authoring examples including multiline tables and styled content in cells.
