---
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

Continuation rows (empty first cell) extend a logical row across multiple physical lines. Empty separator rows mark cell boundaries.

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
