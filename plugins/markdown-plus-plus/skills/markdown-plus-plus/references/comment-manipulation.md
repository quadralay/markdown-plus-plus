---
date: 2026-05-11
status: active
---

# Markdown++ Comment Manipulation

Rules for safely removing or simplifying Markdown++ directive comments
during cleanup, migration, or refactoring passes. This is the inverse of
the authoring guidance in [`best-practices.md`](best-practices.md): how
to *take directives out* of a document without breaking its structure or
losing meaning.

## When to Use This Reference

Reach for this document when you are operating on the *cleanup* half of
the Markdown++ lifecycle:

- **Migration aftermath.** A FrameMaker, DITA, or other source-format
  document was converted to Markdown++ and arrived dense with style
  comments (`<!--style:BodyText-->`, `<!--style:Heading1-->`,
  `<!--style:CellBullet-->`) that add nothing beyond what the markdown
  structure already encodes.
- **Periodic style-cleanup pass.** Existing Markdown++ documents
  accumulate redundant directives over time as authors copy patterns
  forward. A periodic sweep collapses these to the minimum useful set.
- **Authoring-session refactor.** An AI agent or human author is
  rewriting a passage and needs to decide whether to keep, simplify, or
  remove existing directive comments alongside the content edit.

This document is **not** a Markdown++ spec change. It captures rules
that have proven useful in practice; the [Markdown++
specification](../../../../../spec/specification.md) retains exclusive
authority over what *is* valid syntax. If a rule below conflicts with
the spec, the spec wins.

For *authoring* guidance (how to write directives correctly), see
[`best-practices.md`](best-practices.md). For *table layout* (column
widths, pipe alignment), see [`table-formatting.md`](table-formatting.md).

## The Core Principle

Every removal and reduction rule below derives from one principle:

> A style comment whose name maps 1:1 to a Markdown structural element
> (paragraph, heading level, bullet list, ordered list, code block,
> table cell) is **redundant** -- the markdown structure already
> conveys the same meaning. A style comment that carries semantic
> distinction the markdown structure cannot express (callout type,
> definition-list role, procedure step, table title, figure title,
> API-documentation category, inline semantic role) is **not
> redundant** and must be preserved.

The illustrative style-name lists in the sections below are FrameMaker
and ePublisher conventions surfaced by particular migration toolchains.
The principle is the durable knowledge -- consumer repositories with
different style families apply the same test to their own names.

## Removing Block Style Comments

A block-style comment placed above a paragraph, heading, list, code
block, or table can be removed when its style name maps to the
structural element directly below it. Once removed, the markdown
structure alone carries the same meaning.

### Illustrative removable block-style families

The following style names, drawn from migrated FrameMaker / ePublisher
documents, are routinely safe to remove:

- **Paragraph / body**: `Body`, `Normal`, `Default`, `BodyText`,
  `BodyIndent`, `BodyIndent2`, `BodyListIntro`
- **Heading levels**: `Heading1`, `Heading2`, `Heading3`, `Heading4`
- **Table-cell defaults**: `CellBody`, `CellHeading`, `CellBullet`,
  `Table Normal`, `TableLines`, `TableLinesIndent`
- **Procedure / list defaults**: `ProcedureStep1`, `ProcedureStep`,
  `ProcedureSubStep1`, `ProcedureBullet`, `Bullet`, `Bullet2`
- **Code defaults**: `Code`, `CodeFirst`, `CodeLast`, `CodeSingle`,
  `Preformatted`
- **Anchor-only paragraph styles**: `Anchor`, `AnchorIndent`,
  `AnchorIndent2` (anchor handling itself is covered separately below)

*Illustrative, not canonical.* The names above are concrete examples
from one migration toolchain. Apply the principle, not the list, to
your own style families.

### Worked example

**Before:**

```markdown
<!--style:BodyText-->
The application processes incoming requests asynchronously.

<!--style:Heading2-->
## Configuration

<!--style:Bullet-->
- Enable telemetry
- Configure timeouts
```

**After:**

```markdown
The application processes incoming requests asynchronously.

## Configuration

- Enable telemetry
- Configure timeouts
```

Each removed directive named a structural role (paragraph, heading
level, bullet) that the markdown syntax already expresses.

## Reducing Block Style Comments

Some style families differ only by an indent or layout suffix that the
rendering pipeline collapses to the same output. Replace the variant
with the canonical base form.

### Illustrative reducible families

- `ChapterTitle` -> `Title`
- `NoteIndent`, `NoteIndent2` -> `Note`
- `Short Description` -> `Description`
- `DefineListDescription` -> `DefineListDefinition`
- `Definition Term` -> `DefineListTerm`
- `Definition Description` -> `DefineListDefinition`
- `d_caption` -> `FigureTitle`

*Illustrative, not canonical.* The reductions above are the patterns
observed in FrameMaker / ePublisher migrations. Apply the principle:
when two style names render identically, prefer the canonical base name.

### Worked example -- ChapterTitle to Title

**Before:**

```markdown
<!--style:ChapterTitle-->
Installation
```

**After:**

```markdown
<!--style:Title-->
Installation
```

### Worked example -- NoteIndent2 to Note

**Before:**

```markdown
<!--style:NoteIndent2-->
> Configuration changes take effect after restart.
```

**After:**

```markdown
<!--style:Note-->
> Configuration changes take effect after restart.
```

The indent variant collapses to the base form; the semantic distinction
(this blockquote is a note) is preserved.

## Removing Inline Style Comments

An inline-style comment placed before a span of text can be removed when
a standard Markdown inline-formatting token already conveys the
directive's meaning.

### Markdown-token pairings

The following inline directives are routinely safe to remove when paired
with the indicated Markdown token:

| Directive       | Removable when paired with |
| --------------- | -------------------------- |
| `GUIControl`    | `**bold**`                 |
| `Variable`      | `*italic*` or `` `code` `` |
| `Emphasis`      | `*italic*`                 |
| `FileAndFolder` | `` `code` ``               |
| `Command`       | `` `code` ``               |
| `Parameter`     | `` `code` ``               |
| `Filename`      | `` `code` ``               |
| `Code`          | `` `code` ``               |
| `Literal`       | `` `code` ``               |
| `BookTitle`     | `*italic*`                 |

*Illustrative, not canonical.* Apply the principle: when the Markdown
inline token alone communicates the same distinction, the inline
directive is redundant.

### Worked example

**Before:**

```markdown
Click the <!--style:GUIControl-->**Settings** button to open the panel.
```

**After:**

```markdown
Click the **Settings** button to open the panel.
```

The `**bold**` token already marks the GUI-control distinction; the
inline directive carries no additional meaning.

## Keep-by-Default Semantic Styles

Some style comments carry semantic distinction that no Markdown
structure can express. Keep these by default. Removing them silently
discards meaning the rendering pipeline relies on.

### Illustrative keep-by-default families

- **Callouts**: `Note`, `Warning` -- the Markdown blockquote alone
  cannot distinguish a tip, note, warning, or caution box. The style
  name is the callout type.
- **Definition lists**: `DefineListTerm`, `DefineListTermDropDown`,
  `DefineListDefinition` -- standard Markdown has no definition-list
  syntax; the style names carry the term/definition role.
- **Procedure titles**: `ProcedureTitle` -- distinguishes a procedure
  heading from a generic heading at the same level.
- **Titles and captions**: `Title`, `TableTitle`, `FigureTitle` --
  semantic title-vs-heading distinction; render to different elements
  in downstream output.
- **Semantic inline roles**: `IfClause`, `NewTerm` -- a `*new term*` in
  prose is grammatical italics; `<!--style:NewTerm-->*new term*` is a
  glossary entry. The directive is the distinction.
- **API documentation**: all `API_*` styles -- API-specific semantic
  roles (parameter name, return type, exception, etc.) that downstream
  toolchains key on.

*Illustrative, not canonical.* The principle: if the style name carries
information that the Markdown structure does not, keep the directive.

## Anchor Handling

Anchors (`<!--#alias-->`) follow their own rules. Whether an anchor is
removable depends on (a) whether it stands alone or is combined with a
style and (b) whether the targeted element is a heading.

| Context                                    | Action                            |
| ------------------------------------------ | --------------------------------- |
| Standalone anchor on a heading             | Keep                              |
| Combined (style + anchor) on a heading     | Keep the anchor; remove the style |
| Standalone anchor not on a heading         | Remove                            |
| Combined (style + anchor) not on a heading | Remove the whole comment          |

### Underline-style headings

The "on a heading" check must recognize both ATX headings (`#`-prefixed)
and Setext headings (paragraph followed by `===` or `---` on the next
line). A naive scanner that only looks at the current and previous lines
will misclassify the Setext form.

```markdown
<!--#installation-->
Installation
============
```

The anchor above is on a heading -- the `============` underline on the
next line makes the previous paragraph a level-1 Setext heading. Keep
the anchor.

### Cross-cell detection inside multiline tables

A multiline-table row can carry a `<!--style:Name-->` directive in one
cell and a `<!--#cell-anchor-->` anchor in another cell on the same
line. Evaluate the two independently: the presence of a style comment
somewhere on the line does not change whether the anchor on that same
line is removable. A line-level scanner that "skips this line because a
style comment appears anywhere on it" mishandles this case.

```markdown
| <!--style:Body-->Cell A | <!--#section-anchor-->Cell B |
```

Evaluate each cell on its own merits.

## Table-Cell Edge Cases

Removing a directive from a table cell requires preserving the table's
structural shape. Five rules cover the cases that arise.

### Preserve cell width

When content shortens inside a cell, pad with trailing whitespace to
maintain the column's visible width. This keeps pipes vertically aligned
and leaves the table in a state
[`format-tables.py`](table-formatting.md) treats as already formatted.

**Before:**

```markdown
| Term     | Description                       |
| -------- | --------------------------------- |
| Alpha    | <!--style:CellBody-->First entry. |
```

**After:**

```markdown
| Term     | Description                       |
| -------- | --------------------------------- |
| Alpha    | First entry.                      |
```

The trailing whitespace in the right cell preserves the column width.

### Escaped pipes inside cells

A `\|` inside a cell is literal content, never a cell boundary. Any
cell-boundary scanner used during cleanup must skip escaped pipes when
locating the start and end of a cell. See
[`table-formatting.md` R9](table-formatting.md) for the same rule
applied to formatting.

```markdown
| Symbol            | Description                   |
| ----------------- | ----------------------------- |
| pipe \| character | A literal pipe inside a cell. |
```

The `\|` belongs to cell 1's content.

### Multiline row boundaries

In a `<!-- multiline -->` table, a row whose cells are all
whitespace-only is a logical row separator (an "empty separator row").
Cleanup operations that look "one line ahead" for content to merge
upward must respect that boundary -- a blank separator row is not a
continuation, and content beyond it belongs to the next logical row.

```markdown
<!-- multiline -->
| Term  | Meaning |
| ----- | ------- |
| Alpha | First.  |
|       |         |
| Beta  | Second. |
```

A merge operation on the `Alpha` row stops at the empty separator row;
`Beta` is a new logical row.

### Partial-cell merge

When directive removal empties exactly *one* cell in a row while other
cells remain non-empty, merge content from the corresponding cell of
the *next physical line* upward into the empty cell. Do not merge the
whole row -- only the cells that emptied.

**Before:**

```markdown
<!-- multiline -->
| Term  | Status    | Notes              |
| ----- | --------- | ------------------ |
| Alpha | <!--style:CellBody-->Active | Configured for production. |
|       |           | Reviewed quarterly.|
```

After removing `<!--style:CellBody-->` from the second cell, that cell
holds only `Active` -- still non-empty -- so no merge is needed. The
partial-merge rule fires when removal actually empties a cell. Compare
with a case where the directive *was* the cell's only content:

**Before:**

```markdown
<!-- multiline -->
| Term  | Status   | Notes              |
| ----- | -------- | ------------------ |
| Alpha | <!--style:CellBody--> | Configured for production. |
|       | Active   | Reviewed quarterly.|
```

**After (partial merge -- only the `Status` cell pulls up):**

```markdown
<!-- multiline -->
| Term  | Status   | Notes              |
| ----- | -------- | ------------------ |
| Alpha | Active   | Configured for production. |
|       |          | Reviewed quarterly.|
```

The `Notes` cell on row 1 keeps its existing content; only the empty
`Status` cell pulled content up from row 2.

### Bare-list-marker merge

When directive removal leaves a cell containing only a list marker
(`- `, `* `, `+ `, `1.`) with no following content, the marker is
incomplete. Merge content from the corresponding cell of the next
physical line upward to complete the list item.

**Before:**

```markdown
<!-- multiline -->
| Term  | Details                       |
| ----- | ----------------------------- |
| Alpha | - <!--style:CellBullet-->     |
|       | Enables async processing.     |
```

**After:**

```markdown
<!-- multiline -->
| Term  | Details                       |
| ----- | ----------------------------- |
| Alpha | - Enables async processing.   |
|       |                               |
```

The bare `-` on row 1 acquires its content from row 2; row 2's cell
becomes a whitespace-only continuation.

## Detection Patterns

The regex patterns below are *starting points* for tool authors. They
illustrate the shape of the problem; production tooling combines them
with the companion logic described after the patterns. They do **not**
replace [`spec/formal-grammar.md`](../../../../../spec/formal-grammar.md).

### Style comment with optional anchor

```python
r'<!--\s*style:\s*([^;>]+?)(?:\s*;\s*(#[^>]+))?\s*-->'
```

Matches `<!--style:Name-->`, `<!-- style:Name -->`, and combined
`<!--style:Name ; #anchor-->` shapes. Does not handle the full combined-
command grammar (multiline, marker, marker order) -- consult
`spec/formal-grammar.md` for the canonical syntax.

### Standalone anchor

```python
r'<!--\s*(#[a-zA-Z0-9_-]+)\s*-->'
```

Matches anchors that appear on their own (not combined with a style).
Companion logic must verify the match is not inside an unclosed style
comment -- a substring `<!--#name-->` inside a longer `<!--style:Foo ;
#name-->` would otherwise match incorrectly.

### Companion logic checklist

The regex patterns above are insufficient on their own. Production
cleanup tooling must also:

1. **Verify standalone-anchor matches are not inside a style comment.**
   Inspect the surrounding text to confirm the matched `<!--` and `-->`
   actually delimit the anchor, not a larger combined directive.
2. **Evaluate each cell of a multiline-table row independently** (R11
   above). A line-level scanner that gates on "is there a style comment
   anywhere on this line?" mishandles cross-cell coexistence.
3. **Check for Setext headings** when deciding whether an anchor is on
   a heading. The `=` / `-` underline appears on the *next* line, not
   the current one.
4. **Respect multiline row boundaries** when merging content upward.
   An empty separator row stops the merge; content beyond it belongs to
   the next logical row.
5. **Handle partial-cell merges** when removal empties exactly one cell
   in a multi-cell row. Only the emptied cell pulls content up.
6. **Handle bare-list-marker merges** when removal leaves only a list
   marker behind. Merge the next line's corresponding cell content to
   complete the list item.

## Reference Implementation

The cleanup rules above are implemented by the Phase II scripts in the
`epublisher-docs` repository. The scripts are reference implementations,
not normative -- this document is the source of truth for *behavior*;
the scripts are the source of truth for *implementation in that repo*.
Those scripts live in a separate repository and may evolve
independently.

### Phase II scripts

| Script                              | Purpose                                                          |
| ----------------------------------- | ---------------------------------------------------------------- |
| `detect-removable-block-styles.py`  | Remove semantic-free block styles                                |
| `detect-reducible-styles.py`        | Simplify style names to canonical base forms                     |
| `detect-removable-anchors.py`       | Remove non-heading anchors                                       |
| `detect-removable-inline-styles.py` | Remove inline styles where a Markdown token already conveys role |
| `markdown_table_utils.py`           | Shared library for table-cell manipulation                       |

Repo-relative paths inside `epublisher-docs` are under
`.claude/scripts/`. Path stability there is the responsibility of that
repo's maintainers.

### markdown_table_utils.py helper inventory

A re-implementer building cleanup tooling in any language should expect
to need helpers shaped like the following:

- **`find_unescaped_pipe`** -- locate cell boundaries while skipping
  escaped `\|` content.
- **`replace_in_table_cell`** -- replace text inside a cell while
  preserving the cell's visible width via trailing whitespace.
- **`is_table_line_empty`** -- detect a row whose cells are all
  whitespace-only (the multiline row-boundary marker).
- **`is_bare_list_marker`** -- detect a cell containing only a list
  marker with no following content.
- **`handle_table_line_after_removal`** -- post-removal cleanup that
  decides whether a partial-cell or bare-marker merge is needed.
- **`merge_table_line_up`** -- merge content from the next physical
  line's corresponding cells into the current line's emptied cells.

The names above are the Python script's conventions; the *shapes* are
the durable knowledge. A Node, Ruby, or inline-Claude re-implementation
needs equivalent capabilities under its own names.

## See Also

- [`best-practices.md`](best-practices.md) -- authoring guidance (the
  inverse direction). Cross-references back to this document under
  Common Mistakes to Avoid.
- [`table-formatting.md`](table-formatting.md) -- column-width and
  pipe-alignment rules. Cleanup operations on table cells should leave
  tables in a state the formatter treats as already formatted.
- [`spec/multiline-cell-extensions.md`](../../../../../spec/multiline-cell-extensions.md)
  -- extension support and restrictions inside multiline table cells.
- [`spec/attachment-rule.md`](../../../../../spec/attachment-rule.md) --
  formal tag-to-element binding rule. Combined-command decomposition
  during cleanup must respect the attachment rule.
