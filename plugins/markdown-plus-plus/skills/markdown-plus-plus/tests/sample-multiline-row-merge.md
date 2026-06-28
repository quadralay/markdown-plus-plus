---
mdpp-version: 1.0
date: 2026-06-27
status: active
---

# MDPP018 fixture -- multiline table silent row merge

Fixtures for the MDPP018 validator warning (issue #118). Run the validator
against this file; the expected outcome is documented in each section.

```bash
python scripts/validate-mdpp.py tests/sample-multiline-row-merge.md
```

Expected: exactly **one** MDPP018 warning -- on the directive line of the
"Wrong" table below -- and exit code 0 (warning severity, not error).

## Wrong -- no separator rows, all data rows merge (triggers MDPP018)

The directive is cosmetic: cells are single-line, there are no separator
rows, and every data row has a non-blank first cell. Under multiline
semantics all four data rows collapse into one logical row.

<!-- multiline -->
| Setting             | Default |
|---------------------|---------|
| Generate Assistant  | true    |
| Hide AI Tab         | true    |
| Enable Telemetry    | false   |
| Verbose Logging     | false   |

## Right -- separator rows between records (no MDPP018)

The same data, with a whitespace-only separator row between each record, so
each renders as its own logical row.

<!-- multiline -->
| Setting             | Default |
|---------------------|---------|
| Generate Assistant  | true    |
|                     |         |
| Hide AI Tab         | true    |
|                     |         |
| Enable Telemetry    | false   |

## Right -- genuine continuation rows (no MDPP018)

A real multiline table: the second physical line of each record carries
block content in a continuation row (blank first cell). The author clearly
understands the mechanism, so the table is not flagged.

<!-- multiline -->
| Name | Details            |
|------|--------------------|
| Bob  | Lives in Dallas.   |
|      | - Enjoys cycling   |
|      | - Loves cooking    |
|      |                    |
| Mary | Lives in El Paso.  |
|      | - Works as a teacher |

## Right -- single data row (no MDPP018)

One data row cannot merge with anything, so a separator is unnecessary.

<!-- multiline -->
| Setting            | Default |
|--------------------|---------|
| Generate Assistant | true    |

## Right -- plain table, no multiline directive (no MDPP018)

A standard table with multiple rows is not a multiline table; row merging
does not apply and the check does not fire.

| Setting            | Default |
|--------------------|---------|
| Generate Assistant | true    |
| Hide AI Tab        | true    |
