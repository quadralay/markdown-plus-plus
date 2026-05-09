---
date: 2026-05-09
status: active
mdpp-version: 1.0
---

# Multiline Table Fixtures (Unformatted)

Source fixtures for `format-tables.py` covering AE3, AE4, and AE7. These
tables are intentionally unformatted -- running the formatter against this
file is the test. See [`format-tables-cases.md`](format-tables-cases.md)
for invocations and expected outcomes. AE1 is documented inline in
`format-tables-cases.md` because it requires a fixed column-width
invocation that doesn't match the column counts of the other fixtures.

## AE3 -- atomic inline-formatting token outsizes column

<!-- multiline -->
| Action | Detail |
| ------ | ------ |
| Enable | Use the **`Set-ExecutionPolicy`** cmdlet to enable scripts. |
| Save | Click the **Save and Continue** button to commit. |
| Run | Run `npm install --save-dev` first. |
| Italic | Note the _emphasis_ form. |

## AE4 -- escaped pipe in a cell round-trips

<!-- multiline -->
| Symbol | Description |
| ------ | ----------- |
| pipe \| character | A literal pipe inside a cell. |
| Other | Plain content. |

## AE7 -- combined-commands directive line is preserved verbatim

<!-- style:DataTable ; multiline ; #my-table -->
| Name | Description |
| ---- | ----------- |
| Alpha | First entry. |
| Beta | Second entry, with longer content that fits on one line. |
