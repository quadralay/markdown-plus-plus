---
date: 2026-05-23
status: active
---

# Unicode alias acceptance and rejection test corpus

Issues #108 and #111: the alias letter class extends to the XML 1.0
NCName `NameStartChar` ranges; non-first positions additionally accept
the full XML NCName `NameChar` extras (combining marks, connector
punctuation, period, middle dot) so aliases align with NCName end-to-end
with one explicit deviation -- leading digit is still permitted because
the existing numeric-identifier convention (`<!-- #04499224 -->`) is
load-bearing for documents that map aliases to numeric source IDs.

This fixture exercises positive samples per major script and negative
samples that MUST still trip MDPP002.

All positive aliases are chosen to be NFC-normalized + casefold-unique
so MDPP008 does not fire between them.

---

## POSITIVE CASES (should NOT trigger MDPP002 or MDPP008)

### Case U1: Japanese alias -- EXPECT no error

<!--#インストール-->
## Installation (Japanese)

### Case U2: German alias with precomposed accent -- EXPECT no error

<!--#Café-->
## Cafe Module (precomposed e-acute, U+00E9)

### Case U4: Greek alias -- EXPECT no error

<!--#εγκατάσταση-->
## Installation (Greek)

### Case U5: Cyrillic alias -- EXPECT no error

<!--#установка-->
## Installation (Cyrillic)

### Case U10: ZWJ in non-first position -- EXPECT no error

ZWJ (U+200D) is permitted in NCName `NameStartChar`. This case verifies
the validator accepts ZWJ between alias letters without crashing.
Whether authors should mint such aliases is a separate question -- the
test documents observed behavior under the current grammar.

<!--#foo‍bar-->
## ZWJ joined alias

### Case U11: Dotted-hierarchy alias -- EXPECT no error (issue #111)

Period (`.`) is part of XML NCName `NameChar` in non-first positions.
Dotted-hierarchy identifiers are idiomatic in XML-derived systems and
this case anchors the new behavior under MDPP002.

<!--#chapter.1.intro-->
## Chapter 1 Intro (dotted hierarchy)

### Case U12: Alias containing period in non-first position -- EXPECT no error (issue #111)

Negative-flipped from the prior corpus -- a `foo` dot `bar` alias is
now valid because `.` is permitted as a non-first NameChar.

<!--#foo.bar-->
## Period-Containing Heading

### Case U13: Alias containing connector punctuation -- EXPECT no error (issue #111)

Undertie (U+203F) is part of XML NCName `NameChar` (`#x203F-#x2040`) in
non-first positions. This case verifies the validator accepts connector
characters between alias letters.

<!--#foo‿bar-->
## Connector-Containing Heading

### Case U14: Alias containing combining mark in non-first position -- EXPECT no error (issue #111)

Combining grave accent (U+0300) is in NCName's combining-mark range
(`#x0300-#x036F`). The `e` below carries the combining mark; the
result is a decomposed `è`. MDPP002 accepts the raw bytes; MDPP008
NFC-normalizes for duplicate detection.

<!--#foè-bar-->
## Combining-Mark Heading

### Case U15: Alias containing middle dot -- EXPECT no error (issue #111)

Middle dot (U+00B7) is part of XML NCName `NameChar` in non-first
positions. Common in Catalan orthography (`l·l`) and other contexts.

<!--#foo·bar-->
## Middle-Dot Heading

---

## NEGATIVE CASES (should trigger MDPP002)

### Case U7: Alias starting with period -- EXPECT MDPP002

Period is permitted only in non-first positions (XML NCName excludes
`.` from `NameStartChar`). A leading `.` therefore still trips MDPP002.

<!--#.hidden-->
### Period-Leading Heading

### Case U8: Alias containing colon -- EXPECT MDPP002

Colon is excluded from XML NCName by construction (NCName ::= NameChar
- ':'). Aliases inherit that exclusion.

<!--#foo:bar-->
### Colon-Containing Heading

### Case U9: Alias containing ASCII whitespace -- KNOWN edge case (no error fired)

The alias extraction regex stops at ASCII whitespace and requires the
match to be terminated by `;` or `-->`. With ASCII space inside the
alias body, neither end-of-name condition is satisfied at any prefix of
`foo bar`, so the regex fails entirely and the alias is never extracted.
MDPP002 does not fire because no alias is registered. MDPP009 does not
fire because the line attaches to the heading below.

Non-ASCII whitespace inside alias names IS now caught by MDPP002 (issue
#115) -- see `sample-unicode-whitespace-aliases.md` for the NBSP /
narrow NBSP / ideographic space cases. The ASCII case below remains a
separate follow-up: a robust fix would require either replacing the
lookahead-anchored extraction with a comment-tokenizer pass or relaxing
the alias body class to ASCII space and then flagging it.

<!--#foo bar-->
### Whitespace-Containing Heading
