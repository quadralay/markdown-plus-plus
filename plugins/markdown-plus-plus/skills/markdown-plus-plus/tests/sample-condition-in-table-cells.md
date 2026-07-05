---
mdpp-version: 1.0
date: 2026-07-05
status: active
---

# MDPP019 fixture -- condition tags inside table cells

Fixtures for the MDPP019 validator warning (issue #126). Run the validator
against this file; the expected outcome is documented in each section.

```bash
python scripts/validate-mdpp.py tests/sample-condition-in-table-cells.md
```

Expected: exactly **three** MDPP019 warnings -- one on each positive-case row
below -- and exit code 0 (warning severity, not error).

Conditional rows are the supported granularity for conditions in tables. A
condition block MAY wrap complete physical rows (standard table) or complete
logical rows (multiline table), or an entire table. MDPP019 fires only when a
condition open or close tag is embedded **within** a table row line -- an
in-cell span or a conditional cell -- never when a full-line condition tag sits
between rows.

## Wrong -- in-cell span in a multiline table (triggers MDPP019)

The span opens and closes within a single cell on one physical line. Phase 1
evaluates it, but the span is an unbreakable atomic unit for line wrapping and
corrupts the table if a wrapping tool splits it across physical lines. Prefer a
conditional row variant or a variable.

<!-- multiline -->
| Channel | How to reach us |
| ------- | --------------- |
| Support | Contact <!--condition:web-->email<!--/condition--> now. |
| | |
| Sales | Call the main office. |

## Wrong -- in-cell span in a standard table (triggers MDPP019)

The same in-cell span in a plain (non-multiline) table. The line is a pipe row
carrying a condition tag, so it is flagged.

| Channel | How to reach us |
| ------- | --------------- |
| Support | Contact <!--condition:web-->email<!--/condition--> now. |
| Sales | Call the main office. |

## Wrong -- conditional cell (span containing a | delimiter) (triggers MDPP019)

The span stretches across an unescaped `|` cell delimiter. Hiding it removes a
cell boundary and changes the row's column count -- the resulting table
structure is corrupt. Authors MUST NOT author this.

| Plan | Web contact | Phone contact |
| ---- | ----------- | ------------- |
| Pro | <!--condition:web-->email | phone<!--/condition--> | landline |
| Free | forum | community |

## Right -- condition wraps a complete logical row (no MDPP019)

The condition block wraps a complete logical row of a multiline table -- the
first row, its continuation row, and its trailing whitespace-only separator
row. The tags sit on their own lines between rows, so no row line carries a
condition tag.

<!-- multiline -->
| Feature | Description |
| ------- | ----------- |
| Core | Available on all plans. |
| | - Basic analytics |
| | |
<!--condition:enterprise-->
| Enterprise | Premium features: |
| | - SSO integration |
| | |
<!--/condition-->
| Community | Free tier features. |
| | - Forum access |

## Right -- condition wraps a complete physical row in a standard table (no MDPP019)

The condition block wraps a complete physical row of a standard table. Phase 1
sees whole lines, so wrapping the row works identically. The tags are full-line
tags between rows -- not embedded in any row.

| Feature | Availability |
| ------- | ------------ |
| Core features | Included in every plan. |
<!--condition:enterprise-->
| Single sign-on | Enterprise plans only. |
<!--/condition-->
| Community forum | Free tier and above. |

## Right -- condition wraps an entire table (no MDPP019)

The condition block wraps the whole table. Again the tags are full-line tags
outside every row.

<!--condition:print-->
| Setting | Default |
| ------- | ------- |
| Verbose | false |
| Telemetry | false |
<!--/condition-->

## Right -- inline span in prose (no MDPP019)

An in-cell-style span in a normal paragraph is not a table row (no border
pipes), so MDPP019 does not fire. This is the ordinary, supported use of inline
condition spans outside tables.

Contact <!--condition:web-->our support team<!--/condition--> for help.

## Right -- in-cell span inside a fenced code example (no MDPP019)

Everything inside a fenced code block is skipped, including a row that would
otherwise trigger MDPP019 outside the fence.

```markdown
| Channel | How to reach us |
| ------- | --------------- |
| Support | Contact <!--condition:web-->email<!--/condition--> now. |
```
