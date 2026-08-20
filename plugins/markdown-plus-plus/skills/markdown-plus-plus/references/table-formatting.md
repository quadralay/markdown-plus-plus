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

The numbered rules below correspond to the requirements the formatter
ships against: R1-R10 from the original #91 capability, R17 from #122,
and R18-R20 from #120/#121 (the link-reference rewrite, list/blockquote
continuation indentation, and in-cell fence skip). Each rule has a
worked example.

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

### R5 -- Auto column widths: soft width rule with budget shrink (multiline)

Standard tables keep the simple `auto` rule: each column widens to the
widest actual cell (no wrapping), with `min_col_width` (default 3) and
the header text length as floors, and a stderr warning when a cell
exceeds `max_cell_width` (see R7). Nothing below changes for standard
tables.

`<!-- multiline -->` tables follow the **soft width rule** (issue #120).
Each column's inner width is computed as:

```text
width_c = max( min(max_content_c, max_cell_width),
               header_len_c, min_col_width, col_floor_c )
```

where `col_floor_c` is the column's **irreducible floor** -- the widest
atomic token (R8) any cell in the column carries, or the full length of
an in-cell fenced-code line that must be emitted verbatim (R20). Prose is
not part of the floor; it can always wrap. So a column is first sized to
its widest content, capped at `max_cell_width`, then raised to whatever
its unsplittable content demands.

**Then the budget shrink runs.** If the total rendered line width (all
columns plus pipes and padding) exceeds `max_line_width` (default 110),
columns are trimmed toward their floors -- the column with the most slack
above its floor first -- until the line fits or every column is already
at its floor. When nothing can shrink further, the table exceeds the
budget by exactly what the unsplittable content demands, and it stays
fully aligned; the excess is never hard-broken.

**The cap-before-budget interplay matters.** The `max_cell_width` cap is
applied to each column *before* the budget shrink. Very wide prose (for
example the ported URL-split specimen, whose widest column is long prose
with no atomic token wider than the cap) is capped at 78 first, so the
line already fits `max_line_width` and the budget shrink never fires --
the cell simply wraps at 78. A table with two genuinely wide columns
whose capped widths still overrun the budget (the ported blockquote
specimen) *does* trigger the shrink: both columns are pulled below their
capped width, toward their floors, until the row fits. Same rule, two
outcomes, decided by whether the capped widths already fit.

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

### R8 -- Atomic tokens widen the whole column (not one row)

Word-wrap treats these inline classes as **atomic** units that are never
split across continuation rows (matched most-specific-first, so a link or
comment is never mis-read as bold/italic/code):

1. Inline links: `[text](url)`
2. Reference links: `[text][ref]` (and the shortcut form `[text][]`)
3. Bare URLs: `https://…`, `http://…`, `file://…`, `mailto:…`
   (runs to the next whitespace)
4. Full HTML comments, including directive comments:
   `<!-- style:X -->`, `<!--markers:{…}-->`
5. Whole inline condition spans:
   `<!--condition:expr-->…<!--/condition-->` that open and close on the
   **same** physical line (the entire span is one unit; a wrap point
   inside it would create a cross-line raw-text span that condition
   removal corrupts)
6. Compound: `` **`text`** ``
7. Code spans: `` `text` `` (single-backtick form)
8. Bold: `**text**`
9. Italic: `*text*` or `_text_`

Classes 1-5 are the issue #120/#121 extensions to the original
four-class recognizer (6-9).

**GLUE rule (issue #121).** A directive/HTML-comment token that is
immediately adjacent -- no intervening whitespace -- to the following
token is fused with it into a single atomic unit. This keeps an inline
style directive welded to the element it styles
(`<!--style:Emphasis-->**important**`), so wrapping can never separate
the two and silently drop the style (see `spec/attachment-rule.md`).

**Whole-column widening replaces the old local row widening.** When an
atomic token (or a glued pair) is wider than a column's planned width,
the column is not locally widened for that one row. Instead the column's
floor already accounts for the widest atomic token it carries (the soft
width rule, R5), so the *entire* column -- header, separator, and every
data and continuation row -- is planned at that one width. The token
lands alone on its continuation row and the pipes align on **every** row.
There is now exactly one width per column; the per-row `effective_width`
special case is gone.

**Input** with `--max-cell-width 20`:

```markdown
<!-- multiline -->
| Action | Detail |
| ------ | ------ |
| Enable | Use the **`Set-ExecutionPolicy`** cmdlet to enable scripts. |
| | |
| Run | Run `npm install --save-dev` first. |
```

**Output:**

```markdown
<!-- multiline -->
| Action | Detail                    |
| ------ | ------------------------- |
| Enable | Use the                   |
|        | **`Set-ExecutionPolicy`** |
|        | cmdlet to enable scripts. |
|        |                           |
| Run    | Run                       |
|        | `npm install --save-dev`  |
|        | first.                    |
```

The `Detail` column floors at its widest atomic token,
`` **`Set-ExecutionPolicy`** `` (25 chars), and the whole column renders
at 25 -- header, separator, and every row aligned -- even though
`--max-cell-width 20` was requested. Under `fixed` widths the same rule
holds: the supplied width acts as a floor that flexes up only when an
atomic token in the column demands more.

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

### R18 -- Over-budget inline links are rewritten to reference form

An inline link `[text](url)` in a multiline cell is rewritten to the
short reference form `[text][id]`, with the definition `[id]: url` (plus
`"title"` when the source had one) emitted after the table, **only** when
both hold:

1. the cell content is longer than `max_cell_width` (so it would wrap),
   **and**
2. rewriting its links actually brings the cell within that budget.

Condition (2) is what keeps a short link atomic at a deliberately tiny
`--max-cell-width`: if the reference form still overflows the cap, the
link stays inline and the soft width rule (R5) widens the column for it
instead. The rewrite runs **before** width planning, so the shortened
cell drives the column floor and flex is rare in practice.

The reference ID is `table-<slug>-<n>`. The slug is resolved in priority
order: the table directive's own alias (`<!-- #config ; multiline -->`
-> `config`), else the nearest preceding heading's slug, else the
file-level fallback `table`. `<n>` is a per-table counter starting at 1
(minted even for a single link); a minted ID that already exists as a
definition anywhere in the file is skipped in favour of the next `n`
(collision handling). No title is emitted when the source link had none,
and an already-rewritten input passes through unchanged (R10 idempotence
-- the seeded used-ID set means a second pass mints nothing).

**Input:**

```markdown
<!-- #config ; multiline -->
| Setting | Reference |
| ------- | --------- |
| Docs | See [the complete configuration guide](https://example.com/docs/configuration/complete-guide) now. |
```

**Output:**

```markdown
<!-- #config ; multiline -->
| Setting | Reference                                                   |
| ------- | ----------------------------------------------------------- |
| Docs    | See [the complete configuration guide][table-config-1] now. |

[table-config-1]: https://example.com/docs/configuration/complete-guide
```

The 98-char source cell exceeds `max_cell_width` (78) and the reference
form (59 chars) fits, so the rewrite fires; the definition follows the
table after one blank line.

**Definition placement with condition-wrapped tails.** Definitions are
emitted after the *fully rendered* block. When a table's final rows are
wrapped in `<!--condition:…-->…<!--/condition-->`, the rendered block
ends with the `<!--/condition-->` close tag, so a definition for a link
in a still-visible row lands *outside* the span -- it never vanishes when
the condition is Hidden.

### R19 -- List and blockquote continuation indentation is preserved

When a multiline cell's content begins with a list marker or blockquote
prefix, the wrapped continuation lines keep the marker's indentation so
the remainder still reads as part of the item or blockquote. The body
after the prefix is wrapped to `width - len(prefix)` and each line is
re-prefixed -- the first line with the literal marker, continuation lines
with the hang indent -- so no rendered line exceeds the column width.

Recognized prefixes (`detect_content_prefix`):

- `- item` / `* item` / `+ item` -> marker then a 2-space hang
- `1. item` -> numbered hang (`10. ` -> 4 spaces)
- `> text` / `>> text` -> the blockquote marker (verbatim, `>> ` not
  `> > `) repeats on every wrapped line at the authored nesting depth
- `> - item` -> blockquote plus list hang (`>   ` continuation)

**Input** with `--max-cell-width 22`:

```markdown
<!-- multiline -->
| Feature | Details |
| ------- | ------- |
| Core | - Enable the optional analytics feature in settings |
```

**Output:**

```markdown
<!-- multiline -->
| Feature | Details                |
| ------- | ---------------------- |
| Core    | - Enable the optional  |
|         |   analytics feature in |
|         |   settings             |
```

The continuation lines are indented two spaces under the list body.

### R20 -- In-cell fenced code is emitted verbatim (never re-wrapped)

A `<!-- multiline -->` cell may hold a fenced code block spanning
continuation rows (a `` ``` `` or `~~~` delimiter line, the content lines
between the delimiters, and the closing delimiter). The formatter tracks
fence state independently down each column across the table's data rows
-- the document-level fence scanner scoped to one column -- and emits
every protected line **verbatim**: never re-wrapped, never re-indented.
Each protected line's full length is a hard floor for the column (R5), so
the column widens to fit the widest code line.

**Input** with `--max-cell-width 20`:

````markdown
<!-- multiline -->
| Language | Example |
| -------- | ------- |
| Python | Greeting: |
|        | ```python |
|        | print("hello, world!") |
|        | ``` |
````

**Output:**

````markdown
<!-- multiline -->
| Language | Example                |
| -------- | ---------------------- |
| Python   | Greeting:              |
|          | ```python              |
|          | print("hello, world!") |
|          | ```                    |
````

The 22-char code line would wrap at `--max-cell-width 20`, but fence
protection keeps it intact and the column floors at 22. `Greeting:`
(prose above the fence) is unaffected.

## Configurable Parameters

| Parameter             | Default | Description                                                                       |
|-----------------------|---------|-----------------------------------------------------------------------------------|
| `--max-line-width`    | 110     | Total line-width budget. Multiline columns shrink toward their atomic-token floors to fit it (R5); an unsplittable floor may still overrun it. |
| `--max-cell-width`    | 78      | Per-cell width cap applied *before* the line-width budget; multiline cells wider than this wrap (or drive a link rewrite, R18). |
| `--min-col-width`     | 3       | Minimum column width (also bounded below by header text length).                  |
| `--col-width-strategy`| `auto`  | One of `auto`, `fixed`, or `proportional` (see below).                            |
| `--col-widths`        | --      | Comma-separated integer widths for the `fixed` strategy (e.g., `30,12,55`).       |

### Strategies

- **`auto`** (default) -- per-column width is the max content length up
  to `max_cell_width`, with `min_col_width` and the header floor as
  lower bounds. For multiline tables the soft width rule (R5) adds the
  widest-atomic-token floor and the `max_line_width` budget shrink.
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

### Whole-column widening for an atomic token (R8)

**Input** with `--max-cell-width 20`:

```markdown
<!-- multiline -->
| Action | Detail |
| ------ | ------ |
| Enable | Use the **`Set-ExecutionPolicy`** cmdlet to enable scripts. |
| | |
| Run | Run `npm install --save-dev` first. |
```

**Output:**

```markdown
<!-- multiline -->
| Action | Detail                    |
| ------ | ------------------------- |
| Enable | Use the                   |
|        | **`Set-ExecutionPolicy`** |
|        | cmdlet to enable scripts. |
|        |                           |
| Run    | Run                       |
|        | `npm install --save-dev`  |
|        | first.                    |
```

The compound `` **`Set-ExecutionPolicy`** `` (25 chars) is the widest
atomic token in the `Detail` column, so the *whole* column is planned at
25 -- header, separator, and every row aligned -- not just the row that
holds the token. The `Run` row's code span wraps into the same
25-wide column.

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
- **`auto`-strategy fragment-shrink non-idempotency.** Under the default
  `auto` strategy, when a multiline table is wrapped because its content
  exceeds `max_cell_width`, a *second* pass reads the already-wrapped
  shorter fragments as the column content and can shrink the column by
  one -- for example a `>   ` list-hang continuation collapsing to `> `.
  The #120 wrap fixes (atomic links/URLs, structure-preserving wrap)
  landed and the earlier link/blockquote *corruption* is gone; this
  residual re-flow is the auto-strategy limitation, not a corruption. Use
  `--col-width-strategy fixed --col-widths …` for a diff-stable layout.
  The idempotency sweep exempts the two specimens that exhibit it
  (`ae1-multiline-fixed-widths` and `port-blockquote-large-line`) via
  `tests/format-tables/idempotency-allowlist.txt`; each case's own golden
  pins the deterministic single-pass output.
- **Incomplete inline nesting.** The atomic-token recognizer (R8) covers
  links, bare URLs, HTML/directive comments, condition spans, compound,
  code spans, bold, and italic. Deeper nesting (e.g., `**bold _italic_
  inside**`) still falls back to whitespace tokenization for the
  unrecognized structure. The cell wraps; the nested formatting may end
  up split across rows.
- **Single-file invocation.** `format-tables.py` accepts one input file
  per invocation. Multi-file batches are the shell's job (`for f in
  *.md; do ...`).
- **No malformed-table repair.** When a table's column counts are
  inconsistent across rows, the formatter takes the widest row's cell
  count as the table's column count and pads every shorter row -- the
  header and separator included -- with empty cells (a benign repair),
  but does not attempt to detect or fix more serious malformations. A
  header row without a matching separator row is treated as prose, not
  as a malformed table.

## CLI Quick Reference

| Flag                       | Default | Purpose                                                         |
|----------------------------|---------|-----------------------------------------------------------------|
| `--in-place`, `-i`         | off     | Rewrite the input file with formatted output (atomic write).    |
| `--check`                  | off     | Exit 0 if already formatted, 4 with unified diff if not.        |
| `--max-line-width N`       | 110     | Total line-width budget; multiline columns shrink toward floors to fit. |
| `--max-cell-width N`       | 78      | Per-cell cap (applied before the budget) before multiline wrap. |
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
  by `adjacent-tables-directive-boundary` (the lookahead exception). The
  soft width rule (R5/R8) and the #120/#121 extensions are pinned by the
  `i120-*` and `i121-*` fixtures (soft-width flex, atomic links/URLs,
  link-reference rewrite, list/blockquote indent, fence skip, directive
  atomicity, glue, condition-span atomicity) and by `ae3-atomic-token-
  local-widening` (whole-column widening).
- [`tests/format-tables-cases.md`](../tests/format-tables-cases.md) --
  the human-readable AE1-AE7 protocol, superseded as the regression
  gate by the golden-file suite above.
- [`references/best-practices.md`](best-practices.md) -- the in-flow
  authoring guidance that points back to this document.
