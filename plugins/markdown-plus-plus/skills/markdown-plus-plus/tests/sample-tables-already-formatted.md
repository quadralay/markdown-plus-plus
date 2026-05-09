---
date: 2026-05-09
status: active
mdpp-version: 1.0
---

# Already-Formatted Multiline Table Fixtures (AE5, AE6)

This is the formatter's idempotency fixture: every table in this file is
already in the canonical formatted shape. Running `format-tables.py
sample-tables-already-formatted.md --check` exits 0 (AE6 happy path).
Running the formatter twice on this file produces byte-identical output
across both runs (AE5).

The tables here mirror those in `sample-tables-multiline.md` after a
single formatter pass (default `auto` widths). See
[`format-tables-cases.md`](format-tables-cases.md) for the verification
protocol.

## AE3 -- atomic inline-formatting token outsizes column

<!-- multiline -->
| Action | Detail                                                      |
| ------ | ----------------------------------------------------------- |
| Enable | Use the **`Set-ExecutionPolicy`** cmdlet to enable scripts. |
| Save   | Click the **Save and Continue** button to commit.           |
| Run    | Run `npm install --save-dev` first.                         |
| Italic | Note the _emphasis_ form.                                   |

## AE4 -- escaped pipe in a cell round-trips

<!-- multiline -->
| Symbol            | Description                   |
| ----------------- | ----------------------------- |
| pipe \| character | A literal pipe inside a cell. |
| Other             | Plain content.                |

## AE7 -- combined-commands directive line is preserved verbatim

<!-- style:DataTable ; multiline ; #my-table -->
| Name  | Description                                              |
| ----- | -------------------------------------------------------- |
| Alpha | First entry.                                             |
| Beta  | Second entry, with longer content that fits on one line. |
