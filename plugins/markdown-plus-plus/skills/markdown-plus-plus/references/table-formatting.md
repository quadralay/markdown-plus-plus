---
date: 2026-05-09
status: active
---

# Markdown++ Table Formatting

Reformatting rules for Markdown tables in Markdown++ documents. The
companion script is
[`scripts/format-tables.py`](../scripts/format-tables.py); the script is
the conformance authority. This document explains the rules in prose so
human authors and AI agents can apply them during in-flow editing
without re-running the script for every change.

## Why This Rule Set Exists

Hand-authored or migrated Markdown tables typically have inconsistent
column widths and long single-line cells that overflow editor windows.
Two pains compound:

- **Read time.** Reviewers either side-scroll through long rows or skip
  the table entirely. Neither produces real review of the content.
- **Diff time.** A one-character edit to a long cell rewrites the whole
  row, hiding the actual change inside whitespace churn. PR diffs cannot
  communicate what changed semantically.

The rule set below produces tables with fixed-width columns, vertically
aligned pipes, and (for `<!-- multiline -->` tables) word-wrapped
continuation rows. A one-character cell edit changes only the affected
row's relevant tokens; column widths stay stable across edits.

## The Rule Set

The numbered rules below correspond to the requirements R1-R10 the
formatter ships against. Each rule has a worked example.

### R1 -- Fixed-width columns, vertically aligned pipes

Every row -- header, separator, data, continuation -- is padded to
identical column widths so the `|` delimiters line up across the entire
table.

```markdown
| Term            | Abbreviation | Status     |
| --------------- | ------------ | ---------- |
| SteelHead       | N/A          | Available  |
| SteelHead Cloud | N/A          | Available  |
```

### R2 -- Separator dashes span the full column width; alignment markers preserved

The separator row uses `-` characters spanning each column's full inner
width. Alignment markers (`:---`, `---:`, `:---:`) are preserved through
formatting.

```markdown
| Left        | Center | Right |
| :---------- | :----: | ----: |
| a           | b      | c     |
| longer text | middle | 42    |
```

### R3 -- Empty rows preserved with whitespace-only cells padded

A row whose cells are all whitespace-only is preserved as a visually
blank row, with each cell padded to the full column width. This is the
common case of an "empty separator row" between logical groups in a
multiline table.

```markdown
<!-- multiline -->
| Term            | Abbreviation | Meaning   |
| --------------- | ------------ | --------- |
| SteelHead       | N/A          | First.    |
|                 |              |           |
| SteelHead Cloud | N/A          | Second.   |
```

### R4 -- Multiline directive line preserved verbatim

A `<!-- multiline -->` directive (or any combined-commands form
including `multiline`) immediately above a table is preserved
byte-identical through formatting.

```markdown
<!-- style:DataTable ; multiline ; #my-table -->
| Name  | Description  |
| ----- | ------------ |
| Alpha | First entry. |
```

### R5 -- Auto column widths derived from widest content up to `max_cell_width`

Under the default `auto` strategy, each column's width is the maximum
content length across every row in that column, clamped to
`max_cell_width` (default 78) for multiline tables. Standard tables
widen to fit the actual cell width and emit a stderr warning when a cell
exceeds `max_cell_width` (see R7). The column floor is the larger of
`min_col_width` (default 3) and the header text length.

### R6 -- Multiline tables word-wrap long content into continuation rows

In a `<!-- multiline -->` table, cells longer than the planned column
width wrap to continuation rows. The wrap point falls between
whitespace-delimited tokens; each continuation row leaves the preceding
columns blank (whitespace-padded to their full width) so that one
logical row visually owns its run of continuation rows.

```markdown
<!-- multiline -->
| Term      | Meaning                                                 |
| --------- | ------------------------------------------------------- |
| SteelHead | The physical or virtual appliance that, together with   |
|           | other appliances, provides optimization and other       |
|           | services.                                               |
```

### R7 -- Standard tables: align-only with warning when cell exceeds `max_cell_width`

A standard (non-multiline) table never produces continuation rows. When
a cell exceeds `max_cell_width`, the formatter aligns the column at the
actual cell width (no truncation) and prints a stderr warning naming the
row and column. The author retains control over whether to add a
`<!-- multiline -->` directive; the formatter never inserts one
silently.

```text
WARNING: cell exceeds max_cell_width (153 chars > 78) at row 3, column 2 ("Description")
```

### R8 -- Inline-formatting tokens are atomic during word-wrap

Four classes of inline-formatting tokens are treated as atomic units
that cannot be split across continuation rows:

1. Compound: `` **`text`** ``
2. Code spans: `` `text` `` (single-backtick form)
3. Bold: `**text**`
4. Italic: `*text*` or `_text_`

If a single atomic token's length exceeds the planned column width, the
wrapper emits that token alone on its continuation row and the renderer
locally widens the column for that one row only. Other rows in the same
column keep their planned width.

```markdown
<!-- multiline -->
| Action | Detail               |
| ------ | -------------------- |
| Enable | Use the              |
|        | **`Set-ExecutionPolicy`** |
|        | cmdlet to enable     |
|        | scripts.             |
```

The formatter does not implement a full CommonMark inline parser. Deeper
nesting (e.g., bold containing italic containing a code span) falls back
to whitespace tokenization for the unrecognized structure -- the cell
still wraps, but the nested formatting may end up split across rows.

### R9 -- Escaped pipes preserved as literal cell content

A `\|` inside a cell is a literal pipe character, not a column
delimiter. The formatter splits rows on unescaped `|` only.

```markdown
| Symbol            | Description                   |
| ----------------- | ----------------------------- |
| pipe \| character | A literal pipe inside a cell. |
```

### R10 -- Idempotent output

Running the formatter twice on the same file produces byte-identical
output across both runs. This is the property that makes the
`--check` mode useful in CI: the formatter's output is deterministic, so
a "would reformat" diagnostic is reliable evidence the file is not yet
formatted.

### R17 -- Full-line HTML comments inside a table are pass-through members

> The prose rules are numbered R1-R10; R11-R16 are internal
> requirement numbers the script uses in its own comments (config
> defaults, `--check` exit codes, non-table pass-through, and so on).
> This rule takes the next free number, R17.

A full-line HTML comment encountered while accumulating a table's rows --
a line matching `^\s*<!--.*-->\s*$` -- no longer terminates the table.
It becomes a **pass-through member** of the block: preserved
byte-verbatim in place (no re-indent, no re-pad), with row accumulation
continuing on the line after it. Column widths are planned across the
genuine data rows on **both** sides of the comment, so one aligned grid
spans the whole block; the comment line itself contributes nothing to
the widths.

This covers two authoring patterns:

1. **Condition tags wrapping complete rows.** Full-line
   `<!--condition:name-->` / `<!--/condition-->` tags between logical
   rows of a `<!-- multiline -->` table -- the spec-sanctioned *Wrapping
   Complete Rows* pattern (`spec/multiline-cell-extensions.md` §
   Conditions). The rows inside the condition span align with the rows
   outside it because widths are planned across the entire block.
2. **A stray mid-table `<!-- multiline -->` (or any full-line)
   comment.** The formatter is not a validator. Mid-table, an orphaned
   directive comment is just a comment; it is passed through in place
   rather than silently splitting the table (the resolution of the
   former known limitation -- see *Known Limitations*).

**New-table lookahead exception.** A mid-table comment that matches the
multiline-directive form is *not* passed through when it is immediately
followed by a header row and then a separator row (`<!-- multiline -->`
then `| ... |` then `| --- |`). In that one case the directive is
opening a fresh **adjacent** table, so the current block closes at the
directive line and the directive becomes the leading directive of the
next table. This preserves the existing adjacent-tables behavior: each
table plans its widths from its own rows only.

```markdown
<!-- multiline -->
| Feature    | Description             |
| ---------- | ----------------------- |
| Core       | Available on all plans. |
|            | - Basic analytics       |
<!--condition:enterprise-->
| Enterprise | Premium features:       |
|            | - SSO integration       |
<!--/condition-->
| Community  | Free tier features.     |
```

The `Feature` column is 10 wide because `Enterprise` -- a row *inside*
the condition span -- is the widest cell in that column; the condition
tags do not break width planning. A full worked example (including the
lookahead exception) appears under *Worked Examples*.

## Configurable Parameters

| Parameter             | Default | Description                                                                       |
|-----------------------|---------|-----------------------------------------------------------------------------------|
| `--max-line-width`    | 110     | Maximum total line width including pipes and padding.                             |
| `--max-cell-width`    | 78      | Maximum characters per cell before multiline tables wrap to continuation rows.    |
| `--min-col-width`     | 3       | Minimum column width (also bounded below by header text length).                  |
| `--col-width-strategy`| `auto`  | One of `auto`, `fixed`, or `proportional` (see below).                            |
| `--col-widths`        | --      | Comma-separated integer widths for the `fixed` strategy (e.g., `30,12,55`).       |

### Strategies

- **`auto`** (default) -- per-column width is the max content length up
  to `max_cell_width`, with `min_col_width` and the header floor as
  lower bounds.
- **`fixed`** -- per-column widths come from `--col-widths`. The list
  length must match every table's column count in the input file (a
  mismatch is a parse error). Useful for matching a hand-picked layout
  byte-for-byte.
- **`proportional`** -- distributes `max_line_width` minus pipe and
  padding overhead across columns by ratio of total content length per
  column, with `min_col_width` as a floor.

## Worked Examples

### Standard-table alignment

**Input:**

```markdown
| Left | Center | Right |
| :--- | :----: | ----: |
| a | b | c |
| longer text | middle | 42 |
```

**Output:**

```markdown
| Left        | Center | Right |
| :---------- | :----: | ----: |
| a           | b      | c     |
| longer text | middle | 42    |
```

### Multiline word-wrap (issue #91 example, fixed widths 30/12/55)

**Input:**

```markdown
<!-- multiline -->
| Term | Abbreviation | Meaning |
| ---- | ------------ | ------- |
| SteelHead | N/A | The physical or virtual appliance that, together with other appliances, provides optimization and other services. |
| | | |
| SteelHead Cloud | N/A | |
```

**Invocation:**

```bash
python scripts/format-tables.py input.md \
    --col-width-strategy fixed --col-widths 30,12,55
```

**Output:**

```markdown
<!-- multiline -->
| Term                           | Abbreviation | Meaning                                                 |
| ------------------------------ | ------------ | ------------------------------------------------------- |
| SteelHead                      | N/A          | The physical or virtual appliance that, together with   |
|                                |              | other appliances, provides optimization and other       |
|                                |              | services.                                               |
|                                |              |                                                         |
| SteelHead Cloud                | N/A          |                                                         |
```

### Inline-formatting atomicity (R8)

**Input** with `--max-cell-width 20`:

```markdown
<!-- multiline -->
| Action | Detail |
| ------ | ------ |
| Enable | Use the **`Set-ExecutionPolicy`** cmdlet to enable scripts. |
```

**Output:**

```markdown
<!-- multiline -->
| Action | Detail               |
| ------ | -------------------- |
| Enable | Use the              |
|        | **`Set-ExecutionPolicy`** |
|        | cmdlet to enable     |
|        | scripts.             |
```

The compound `` **`Set-ExecutionPolicy`** `` (28 chars) appears alone on
its own continuation row; the column is locally widened to 28 just for
that row.

### Escaped pipes (R9)

**Input:**

```markdown
| Symbol | Description |
| ------ | ----------- |
| pipe \| character | A literal pipe inside a cell. |
| Other | Plain content. |
```

**Output:**

```markdown
| Symbol            | Description                   |
| ----------------- | ----------------------------- |
| pipe \| character | A literal pipe inside a cell. |
| Other             | Plain content.                |
```

### Empty separator row in a multiline table (R3)

**Input:**

```markdown
<!-- multiline -->
| Term | Meaning |
| ---- | ------- |
| Alpha | First. |
| | |
| Beta | Second. |
```

**Output:**

```markdown
<!-- multiline -->
| Term  | Meaning |
| ----- | ------- |
| Alpha | First.  |
|       |         |
| Beta  | Second. |
```

The blank middle row is preserved with whitespace-only cells padded to
each column's full inner width.

### Condition-wrapped rows and mid-table comments (R17)

A `<!-- multiline -->` table with a condition-wrapped logical row (the
spec's *Wrapping Complete Rows* pattern). The condition tags pass through
verbatim in place, and widths are planned across the rows on both sides
of them, so the whole table aligns as one grid.

**Input:**

```markdown
<!-- multiline -->
| Feature | Description |
|-----|------------|
| Core | Available on all plans. |
|      | - Basic analytics |
|   | - Email support |
|  |  |
<!--condition:enterprise-->
| Enterprise | Premium features: |
|     | - SSO integration |
|         | - Dedicated support |
|   |   |
<!--/condition-->
| Community | Free tier features. |
|    | - Forum access |
```

**Output:**

```markdown
<!-- multiline -->
| Feature    | Description             |
| ---------- | ----------------------- |
| Core       | Available on all plans. |
|            | - Basic analytics       |
|            | - Email support         |
|            |                         |
<!--condition:enterprise-->
| Enterprise | Premium features:       |
|            | - SSO integration       |
|            | - Dedicated support     |
|            |                         |
<!--/condition-->
| Community  | Free tier features.     |
|            | - Forum access          |
```

The `Feature` column is padded to 10 characters because `Enterprise`,
which lives inside the `<!--condition:enterprise-->` span, is the widest
cell in that column -- width planning sees it despite the condition tags
between it and the header.

**New-table lookahead exception.** When a `<!-- multiline -->` comment is
immediately followed by a header row and a separator row, it opens a new
adjacent table instead of passing through:

**Input:**

```markdown
| Term | Meaning |
| ---- | ------- |
| Alpha | First entry. |
<!-- multiline -->
| Feature | Description |
| ------- | ----------- |
| Beta | Second entry that runs a little longer. |
```

**Output:**

```markdown
| Term  | Meaning      |
| ----- | ------------ |
| Alpha | First entry. |
<!-- multiline -->
| Feature | Description                             |
| ------- | --------------------------------------- |
| Beta    | Second entry that runs a little longer. |
```

The `<!-- multiline -->` line closes the first (standard) table and
becomes the directive of the second (multiline) table; each plans its
widths from its own rows only.

## Known Limitations

- **ASCII-dominant width measurement.** The formatter measures column
  widths by Python `len(s)`. This is correct for ASCII and most
  Latin-script content but undercounts CJK wide characters and
  overcounts ZWJ-joined emoji. Tables containing internationalized
  content may render with visibly misaligned pipes in editors that use
  East-Asian-Width-aware font metrics. The formatter's output is still
  byte-deterministic; only the visual alignment is affected. Resolving
  this requires either pulling in `wcwidth` (which conflicts with the
  stdlib-only posture) or shipping a stripped-down width table -- a
  separate scope decision.
- **Four-class inline tokenizer.** The atomic-token recognizer (R8)
  handles compound `` **`text`** ``, code spans, bold, and italic.
  Deeper nesting (e.g., `**bold _italic_ inside**`) falls back to
  whitespace tokenization for the unrecognized structure. The cell
  still wraps; the nested formatting may end up split across rows.
- **Single-file invocation.** `format-tables.py` accepts one input file
  per invocation. Multi-file batches are the shell's job (`for f in
  *.md; do ...`).
- **No malformed-table repair.** When a table's column counts are
  inconsistent across rows, the formatter pads the shorter rows with
  empty cells (a benign repair) but does not attempt to detect or fix
  more serious malformations. A header row without a matching separator
  row is treated as prose, not as a malformed table.

## CLI Quick Reference

| Flag                       | Default | Purpose                                                         |
|----------------------------|---------|-----------------------------------------------------------------|
| `--in-place`, `-i`         | off     | Rewrite the input file with formatted output (atomic write).    |
| `--check`                  | off     | Exit 0 if already formatted, 4 with unified diff if not.        |
| `--max-line-width N`       | 110     | Maximum total line width including pipes and padding.           |
| `--max-cell-width N`       | 78      | Maximum cell width before multiline tables wrap.                |
| `--min-col-width N`        | 3       | Minimum column width.                                           |
| `--col-width-strategy S`   | `auto`  | One of `auto`, `fixed`, `proportional`.                         |
| `--col-widths CSV`         | --      | Comma-separated integer widths for `fixed` strategy.            |
| `--verbose`, `-v`          | off     | Print effective parameter values to stderr.                     |

Run `python scripts/format-tables.py --help` for the full reference.

## See Also

- [`scripts/format-tables.py`](../scripts/format-tables.py) -- the
  conformance authority. The script's behavior is the rule set; this
  document trails the script when they disagree.
- [`tests/format-tables/`](../tests/format-tables/) -- the golden-file
  regression suite (run `python tests/run-tests.py` from the skill
  root; add `--idempotency` for the R10 sweep). R17 is pinned by the
  `i122-condition-midtable`, `i122-condition-midtable-standard`, and
  `kl-midtable-multiline-directive` fixtures (pass-through members) and
  by `adjacent-tables-directive-boundary` (the lookahead exception).
- [`tests/format-tables-cases.md`](../tests/format-tables-cases.md) --
  the human-readable AE1-AE7 protocol, superseded as the regression
  gate by the golden-file suite above.
- [`references/best-practices.md`](best-practices.md) -- the in-flow
  authoring guidance that points back to this document.
