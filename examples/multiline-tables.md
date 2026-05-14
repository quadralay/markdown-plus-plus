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

Every pipe-bearing row automatically continues the current logical row across multiple physical lines. Row separators (pipe-bearing rows with whitespace-only cells) are the only way to mark a logical-row boundary. The empty first cell on continuation rows is a readability convention, not the trigger -- any cell may carry content on any line. A no-pipe blank line ends the table entirely.

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

The header row `Feature | Description` is extended by a continuation row carrying `and Requirements` in the second cell, before the delimiter row. The empty first cell follows the readability convention; it is not what makes the row a continuation.
