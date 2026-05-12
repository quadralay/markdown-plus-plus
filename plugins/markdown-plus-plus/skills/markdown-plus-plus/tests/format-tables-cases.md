---
date: 2026-05-09
status: active
---

# Format-Tables Verification Cases (AE1-AE7)

Manual-verification protocol for `format-tables.py`. There is no
automated test runner in this repo; each case below is a `bash` invocation
with an expected outcome (stdout / stderr / exit code). A human can step
through every case in under five minutes to verify the formatter ships
correctly.

The cases are organized by the Acceptance Examples (AE1-AE7) carried over
from the issue and the planning brainstorm. AE5 (idempotency) is the last
case because it depends on every other fixture being well-formed.

## Setup

All commands assume the working directory is
`plugins/markdown-plus-plus/skills/markdown-plus-plus/`. Adjust paths if
running from the repo root.

```bash
cd plugins/markdown-plus-plus/skills/markdown-plus-plus
```

## Case AE1 -- Multiline reformat matches issue #91 byte-for-byte

The issue's "Desired Behavior" example uses fixed column widths of
30/12/55. To reproduce that exact output, the fixture is documented inline
here so the `--col-width-strategy fixed --col-widths 30,12,55` invocation
applies cleanly.

**Input** (write this to a temp file, e.g. `/tmp/ae1-input.md`):

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
python scripts/format-tables.py /tmp/ae1-input.md \
    --col-width-strategy fixed --col-widths 30,12,55
```

**Expected stdout (byte-for-byte):**

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

**Expected stderr:** empty.
**Expected exit code:** 0.

This case verifies R1, R2, R3, R4, R6, and R10 (separator dashes span the
full column width, alignment markers are preserved, the empty separator
row is preserved as a whitespace-only row, the multiline directive is
preserved verbatim, the long cell wraps into continuation rows, and an
empty trailing cell is padded to the column width).

## Case AE2 -- Standard table with over-width cell

Verifies R7: when a standard (non-multiline) table has a cell wider than
`max_cell_width`, the formatter aligns the column at the actual cell width
and emits a stderr warning naming the row and column. No `<!-- multiline
-->` directive is added.

**Fixture:** [`sample-tables-standard-warn.md`](sample-tables-standard-warn.md)

**Invocation:**

```bash
python scripts/format-tables.py tests/sample-tables-standard-warn.md
```

**Expected stdout:** the file's prose preserved, then the table formatted
at column widths that fit the longest cell (column 2 at ~153 chars, plus
column 1 at the header floor). All pipes align vertically.

**Expected stderr (one line):**

```
WARNING: cell exceeds max_cell_width (153 chars > 78) at row 3, column 2 ("Description")
```

**Expected exit code:** 0.

## Case AE3 -- Atomic inline-formatting token outsizes the column

Verifies R8: a `**\`Set-ExecutionPolicy\`**` token (28 chars) inside a
cell with `--max-cell-width 20` appears alone on its own continuation row,
with the column locally widened to fit the token. Other rows in the same
column stay at their planned width.

**Fixture:** [`sample-tables-multiline.md`](sample-tables-multiline.md)
(AE3 section).

**Invocation:**

```bash
python scripts/format-tables.py tests/sample-tables-multiline.md --max-cell-width 20
```

**Expected stdout fragment** (AE3 section only):

```markdown
<!-- multiline -->
| Action | Detail               |
| ------ | -------------------- |
| Enable | Use the              |
|        | **`Set-ExecutionPolicy`** |
|        | cmdlet to enable     |
|        | scripts.             |
| Save   | Click the            |
|        | **Save and Continue** |
|        | button to commit.    |
| Run    | Run                  |
|        | `npm install --save-dev` |
|        | first.               |
| Italic | Note the _emphasis_  |
|        | form.                |
```

The compound `**\`Set-ExecutionPolicy\`**`, the bold `**Save and
Continue**`, and the code span `` `npm install --save-dev` `` each
appear on their own continuation row and are never split mid-token.

**Expected stderr:** empty.
**Expected exit code:** 0.

## Case AE4 -- Escaped pipe in cell round-trips

Verifies R9: `\|` inside cell content is preserved as a literal pipe
character and is not interpreted as a column delimiter.

**Fixture:** [`sample-tables-multiline.md`](sample-tables-multiline.md)
(AE4 section).

**Invocation:**

```bash
python scripts/format-tables.py tests/sample-tables-multiline.md
```

**Expected stdout fragment:**

```markdown
<!-- multiline -->
| Symbol            | Description                   |
| ----------------- | ----------------------------- |
| pipe \| character | A literal pipe inside a cell. |
| Other             | Plain content.                |
```

The `\|` survives the cell-split round-trip.

**Expected stderr:** empty.
**Expected exit code:** 0.

## Case AE6 -- `--check` mode

Two sub-cases.

**AE6a -- already-formatted file (exit 0, no output):**

```bash
python scripts/format-tables.py tests/sample-tables-already-formatted.md --check
echo "exit=$?"
```

Expected: empty stdout, exit code 0.

**AE6b -- unformatted file (exit 4 with unified diff):**

```bash
python scripts/format-tables.py tests/sample-tables-multiline.md --check
echo "exit=$?"
```

Expected: a unified diff on stdout (lines beginning with `---`, `+++`,
`@@`, `-`, `+`), exit code 4.

## Case AE7 -- Combined-commands directive line preserved verbatim

Verifies R4: a directive line of the form `<!-- style:DataTable ;
multiline ; #my-table -->` above a table is preserved byte-identical
through formatting.

**Fixture:** [`sample-tables-multiline.md`](sample-tables-multiline.md)
(AE7 section).

**Invocation:**

```bash
python scripts/format-tables.py tests/sample-tables-multiline.md
```

**Expected stdout fragment:**

```markdown
<!-- style:DataTable ; multiline ; #my-table -->
| Name  | Description                                              |
| ----- | -------------------------------------------------------- |
| Alpha | First entry.                                             |
| Beta  | Second entry, with longer content that fits on one line. |
```

The directive line is unchanged from the input.

**Expected stderr:** empty.
**Expected exit code:** 0.

## Case AE5 -- Idempotency (run last)

Verifies R10: running the formatter twice on any fixture produces
byte-identical second-pass output.

**Procedure:** for each fixture below, run the formatter once with
`--in-place` to produce a formatted file, then run `--check` to verify the
second pass is a no-op.

```bash
# AE3, AE4, AE7 fixture (already formatted by the AE5 setup)
python scripts/format-tables.py tests/sample-tables-already-formatted.md --check
echo "exit=$?"   # expect 0

# AE2 fixture: format in place, then re-check.
cp tests/sample-tables-standard-warn.md /tmp/ae5-warn.md
python scripts/format-tables.py /tmp/ae5-warn.md --in-place 2>/dev/null
python scripts/format-tables.py /tmp/ae5-warn.md --check
echo "exit=$?"   # expect 0

# AE1 inline fixture.
cat > /tmp/ae5-multiline.md <<'EOF'
<!-- multiline -->
| Term | Abbreviation | Meaning |
| ---- | ------------ | ------- |
| SteelHead | N/A | The physical or virtual appliance that, together with other appliances, provides optimization and other services. |
| | | |
| SteelHead Cloud | N/A | |
EOF
python scripts/format-tables.py /tmp/ae5-multiline.md --in-place \
    --col-width-strategy fixed --col-widths 30,12,55
python scripts/format-tables.py /tmp/ae5-multiline.md --check \
    --col-width-strategy fixed --col-widths 30,12,55
echo "exit=$?"   # expect 0
```

All three sub-checks should report `exit=0`. If any reports `exit=4`,
that fixture has lost idempotency and the formatter has a bug.

## Coverage Summary

| AE  | Requirement(s)        | Fixture                                                  |
|-----|-----------------------|----------------------------------------------------------|
| AE1 | R1, R2, R3, R4, R6    | inline (above)                                           |
| AE2 | R7                    | sample-tables-standard-warn.md                           |
| AE3 | R8                    | sample-tables-multiline.md (AE3 section)                 |
| AE4 | R9                    | sample-tables-multiline.md (AE4 section)                 |
| AE5 | R10                   | every fixture, run twice                                 |
| AE6 | R14                   | sample-tables-already-formatted.md, sample-tables-multiline.md |
| AE7 | R4 (combined form)    | sample-tables-multiline.md (AE7 section)                 |
