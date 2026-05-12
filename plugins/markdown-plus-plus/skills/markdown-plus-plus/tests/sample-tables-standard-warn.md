---
date: 2026-05-09
status: active
mdpp-version: 1.0
---

# Standard Table With Over-Width Cell (AE2 Fixture)

A standard (non-multiline) table whose largest cell exceeds the default
`max_cell_width` of 78 characters. The formatter should still align all
columns at the actual cell width and emit a stderr warning naming the row
and column.

## Standard table with one ~120-char cell

| Name | Description |
|------|-------------|
| short | A relatively short cell. |
| oversize | This is an extremely long cell that exceeds the configured maximum cell width and should trigger a warning to stderr but still align to its actual width. |
