---
date: 2026-05-22
status: active
---

# Unicode alias acceptance and rejection test corpus

Issue #108: the alias letter class extends to the XML 1.0 NCName
`NameStartChar` ranges; non-first positions additionally accept the
NCName combining-mark ranges so decomposed accented forms accept under
MDPP002 at the raw-byte level. This fixture exercises positive samples
per major script and negative samples that MUST still trip MDPP002.

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

---

## NEGATIVE CASES (should trigger MDPP002)

### Case U6: Alias containing period -- EXPECT MDPP002

<!--#foo.bar-->
### Period-Containing Heading

### Case U7: Alias starting with period -- EXPECT MDPP002

<!--#.hidden-->
### Period-Leading Heading

### Case U8: Alias containing colon -- EXPECT MDPP002

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
