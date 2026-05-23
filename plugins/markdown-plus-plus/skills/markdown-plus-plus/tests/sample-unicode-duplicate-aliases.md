---
date: 2026-05-22
status: active
---

# MDPP008 duplicate detection under NFC + casefold

Issue #108: MDPP008 compares aliases under Unicode NFC followed by
case-fold, matching the equivalence relation used by CommonMark 0.30
link-reference-definition slug matching. This fixture verifies that the
validator detects:

- Byte-exact duplicates (today's baseline behavior).
- Case-fold-equivalent duplicates (#FOO vs. #foo).
- NFC-equivalent duplicates (precomposed vs. decomposed accented letters
  that render identically).

Each case below has a first occurrence (no error) and a second
occurrence that MUST emit MDPP008. The error message must distinguish
the sub-state.

---

## Case D1: Byte-exact duplicate alias

<!--#introduction-->
## Introduction

<!-- The next alias is identical byte-for-byte -- baseline MDPP008 case -->

<!--#introduction-->
## Repeated Introduction

---

## Case D2: Case-fold duplicate (#FOO vs. #foo)

<!--#FOO-->
## Uppercase Foo

<!-- The next alias is the lowercase form -- casefold collision under
     the updated MDPP008 normalization -->

<!--#foo-->
## Lowercase Foo

---

## Case D3: NFC-equivalent duplicate (precomposed vs. decomposed Cafe)

The first `Café` below uses U+00E9 (precomposed). The second uses
U+0065 followed by U+0301 (decomposed e + combining acute). Both render
identically but are distinct byte sequences. NFC normalization should
collapse them so MDPP008 fires on the second.

<!--#Café-->
## Cafe Module (precomposed e-acute)

<!--#Café-->
## Cafe Module (decomposed e + combining acute)
