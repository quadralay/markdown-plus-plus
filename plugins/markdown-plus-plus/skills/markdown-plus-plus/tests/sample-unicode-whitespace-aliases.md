---
date: 2026-05-23
status: active
---

# Unicode-whitespace alias rejection corpus

Issue #115: the alias extraction regex in `validate-mdpp.py` previously used
`[^\s;>]+?` for the body character class. Python's `\s` is Unicode-aware, so
non-ASCII whitespace inside an alias name caused the regex to silently fail --
the alias was never extracted and MDPP002 never fired. The fix tightens the
body class to `[^ \t\n\r;>]+?` so non-ASCII whitespace is captured and
surfaces through MDPP002.

This fixture exercises three Unicode-whitespace code points known to trip
the pre-fix regex and a positive control (alias with no embedded whitespace)
to confirm valid aliases continue to pass.

---

## POSITIVE CONTROL (should NOT trigger MDPP002 or MDPP008)

### Case W0: Plain ASCII alias -- EXPECT no error

<!--#plain-ascii-alias-->
## Plain ASCII Alias Heading

---

## NEGATIVE CASES (should trigger MDPP002)

### Case W1: NBSP (U+00A0) inside alias name -- EXPECT MDPP002

NO-BREAK SPACE between `foo` and `nbsp`. Pre-fix, the extraction regex
failed to match this comment entirely and the malformed alias was invisible
to validation. Post-fix, MDPP002 fires because U+00A0 is not in the alias
`NameChar` class.

<!--#foo nbsp-->
### NBSP-containing Heading

### Case W2: NARROW NO-BREAK SPACE (U+202F) inside alias name -- EXPECT MDPP002

<!--#foo narrow-->
### Narrow-NBSP-containing Heading

### Case W3: IDEOGRAPHIC SPACE (U+3000) inside alias name -- EXPECT MDPP002

<!--#foo　ideographic-->
### Ideographic-Space-containing Heading

### Case W4: NBSP in spaced-form alias -- EXPECT MDPP002

NBSP appears inside the name and the trailing layout whitespace is ASCII.
The fix captures `foo<NBSP>bar`; the lookahead matches the trailing ASCII
space and `-->`.

<!-- #foo bar -->
### Spaced-Form NBSP Heading
