---
mdpp-version: 1.0
date: 2026-03-29
status: active
---

<!-- style:Heading1; #100003 -->
# Multiline tables

[multiline-tables]: #100003 "Multiline tables"

This example demonstrates rich table content using the `<!-- multiline -->` directive.

## Basic multiline table

<!-- style:DataTable ; multiline ; #basic-multiline -->
| Feature        | Description              | Status      |
|----------------|--------------------------|-------------|
| Authentication | OAuth 2.0 implementation |             |
|                | Supports:                | Complete    |
|                | - Authorization Code     |             |
|                | - Client Credentials     |             |
|                | - Refresh tokens         |             |
|                |                          |             |
| Rate Limiting  | Per-endpoint limits      |             |
|                | - Default: 100 req/min   | In Progress |
|                | - Maximum: 1000 req/min  |             |

Continuation rows (empty first cell) extend a logical row across multiple physical lines. Separator rows (pipes with whitespace-only cells) mark row boundaries. A completely blank line ends the table.

## Styled table with combined directives

<!-- style:ComparisonTable ; multiline ; #format-comparison -->
| Format     | Pros                         | Cons                        |
|------------|------------------------------|-----------------------------|
| DITA XML   | Structured content reuse     |                             |
|            | - conref/conkeyref           | XML overhead                |
|            | - Specialization             | - Verbose syntax            |
|            | - Relationship tables        | - Requires XML expertise    |
|            |                              |                             |
| Markdown++ | Plain text readability       |                             |
|            | - CommonMark compatible      | Narrower ecosystem          |
|            | - Invisible extensions       | - Fewer processing tools    |
|            | - Git-friendly diffs         | - No schema validation      |

Multiple directives (style, multiline, alias) compose on a single line, separated by semicolons.

## Multiline header

Headers can span multiple physical lines using continuation rows above the delimiter.

<!-- style:DataTable ; multiline ; #multiline-header -->
| Feature        | Description              |
|                | and Requirements         |
|----------------|--------------------------|
| Authentication | OAuth 2.0 implementation |
|                | - Authorization Code     |
|                | - Client Credentials     |
|                |                          |
| Rate Limiting  | Per-endpoint limits      |
|                | - Default: 100 req/min   |

The header row `Feature | Description` is extended by a continuation row with an empty first cell and `and Requirements` in the second cell, before the delimiter row.
