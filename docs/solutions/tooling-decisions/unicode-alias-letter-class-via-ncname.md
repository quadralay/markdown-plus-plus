---
title: "Adopt XML NCName as the Markdown++ alias letter class"
date: 2026-05-22
category: tooling-decisions
module: markdown-plus-plus-spec
problem_type: tooling_decision
component: tooling
severity: medium
applies_when:
  - "Extending a Markdown++ identifier grammar to permit non-ASCII letters"
  - "Choosing a Unicode letter class for an identifier that must round-trip across XML, HTML, URL fragments, JavaScript, and CSS selectors"
  - "Comparing aliases (or any identifier) for duplicate-detection when authors may use different normalization forms"
  - "Writing source files that contain non-ASCII characters and need to survive editors, transit, and tooling without silent NFC re-encoding"
tags:
  - alias
  - ncname
  - unicode
  - mdpp002
  - mdpp008
  - validator
  - normalization
  - naming-rule
---

# Adopt XML NCName as the Markdown++ alias letter class

## Context

The Markdown++ custom-alias name (`<!-- #name -->`) was originally restricted
to `[a-zA-Z0-9_][a-zA-Z0-9_-]*` -- ASCII only. Authors writing non-English
documentation could not mint native-script alias identifiers even though
aliases are opaque HTML-comment anchors that never appear in user-visible
output. This decision captures why **XML 1.0 NCName** is the right basis
for the extension (over `\p{L}` and HTML-ID-legal), why the duplicate-alias
detector (MDPP008) was tightened to compare under Unicode NFC + case-fold,
and the source-hygiene conventions used to keep Unicode constants intact
through editors and tooling.

Three options were on the table:

1. **HTML-ID-legal** -- "any character except whitespace and URL delimiters",
   `[^\s/?#]+`. This is what the ePublisher Reverb landmark resolver accepts
   at the *output* surface.
2. **`\p{L}`** -- the Unicode "Letter" general category. Concise and covers
   the intuitive sense of "letter".
3. **XML 1.0 NCName `NameStartChar` letter ranges** -- the explicit Unicode
   ranges that XML uses to define identifier characters.

NCName was selected. The rest of this doc explains why, and the tooling
conventions that fell out of the choice.

## Guidance

### Choose NCName over HTML-ID-legal and over `\p{L}`

- **HTML-ID-legal is the wrong layer.** It is an *output safety bar* (will
  it serialize cleanly into `id="..."`?), not an *authoring grammar*. It
  admits punctuation, symbols, and effectively any non-whitespace
  character, which compounds round-tripping risk across XML, XSLT,
  JavaScript object keys, URL fragments, and CSS selectors.
- **`\p{L}` is concise but tool-fragile.** Python `re` requires the
  third-party `regex` package for it; mixing `\w` with stdlib `re` is
  worse because `\w` matches letters *and* digits *and* underscore,
  collapsing the first-position vs. subsequent-position distinction
  (letters and digits behave differently in the first position of an
  alias) and introducing off-by-one debugging hazards.
- **NCName is the well-defined Unicode-aware identifier grammar designed
  for exactly this purpose.** Every code point NCName admits is also
  HTML-ID-legal, so an NCName alias always round-trips. NCName already
  excludes characters (`/`, `?`, `#`, whitespace, most punctuation) that
  would break identifier usage downstream.

The XML 1.0 `NameStartChar` letter ranges are (W3C `#xHHHH` form):

```
"_" | [A-Z] | [a-z] | [#xC0-#xD6] | [#xD8-#xF6] | [#xF8-#x2FF] |
[#x370-#x37D] | [#x37F-#x1FFF] | [#x200C-#x200D] | [#x2070-#x218F] |
[#x2C00-#x2FEF] | [#x3001-#xD7FF] | [#xF900-#xFDCF] |
[#xFDF0-#xFFFD] | [#x10000-#xEFFFF]
```

These define `alias_name_start_char`. The body production
`alias_name_char` adds digit, `-`, and the NCName combining-mark ranges
(`#x0300-#x036F`, `#x203F-#x2040`) so decomposed accented forms parse
the same as their precomposed counterparts.

### Use explicit `\u` / `\U` escapes, never literal Unicode, when defining the character class in source

The validator constant is spelled with escape sequences in every range,
including the BMP ranges where literal characters would technically work:

<!-- The escape-sequence form below is intentional. Do not "modernize"
     this block by substituting the literal characters -- that is exactly
     the silent-corruption pattern the surrounding guidance is teaching. -->

```python
_NCNAME_START_CHAR = (
    "_A-Za-z"
    "\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF"
    "\u0370-\u037D\u037F-\u1FFF"
    "\u200C-\u200D"
    "\u2070-\u218F"
    "\u2C00-\u2FEF"
    "\u3001-\uD7FF"
    "\uF900-\uFDCF"
    "\uFDF0-\uFFFD"
    "\U00010000-\U000EFFFF"
)
```

Literal Unicode characters in source survive most tooling but not all
of it. An editor that normalizes to NFC on save, a copy-paste through a
clipboard that mangles supplementary-plane characters, a tool round
trip that re-encodes -- any of these can silently substitute a code
point and the validator's grammar would drift from the spec. The
supplementary-plane range `\U00010000-\U000EFFFF` is especially
exposed because the upper bound U+EFFFF cannot be expressed as a
literal in many editors without surrogate-pair handling; the wrong
glyph (U+FFFD replacement) lands silently and the regex compiles
without complaint. Escape sequences do not have this failure mode:
`À` is the same six bytes no matter what touches the file.

Mirror the constant verbatim into any sibling script that needs it.
`add-aliases.py` defines the same `_NCNAME_START_CHAR` and
`_NCNAME_COMBINING` constants, with a comment noting the deliberate
duplication -- the two scripts are intentionally standalone so each can
be vendored independently of the other.

### Build the alias regex from the constant; do not use `\w`

Python stdlib `re` does not natively understand Unicode property
classes, but it does understand explicit character ranges spelled into
a character class. Build the alias regex by composing the constants:

```python
ALIAS_NAME_RE = re.compile(
    f'^[{_NCNAME_START_CHAR}0-9]'
    f'[{_NCNAME_START_CHAR}0-9{_NCNAME_COMBINING}-]*$'
)
```

The first position accepts NCName letters plus digit (digit-first is an
alias-specific allowance for numeric IDs). Subsequent positions add
hyphen and the combining-mark ranges.

### Compare aliases under NFC + case-fold for duplicate detection (MDPP008)

The alias *acceptance* regex matches the raw byte sequence. Two strings
that render identically can differ at the byte level (precomposed `é`
U+00E9 vs. decomposed `e` U+0065 + U+0301), and authors should not be
allowed to mint two visually identical aliases in the same file. Key
the duplicate-detection dictionary by a normalized form:

```python
import unicodedata

def _alias_dedup_key(name: str) -> str:
    """NFC + casefold; stricter than CommonMark 0.30 (casefold only)."""
    return unicodedata.normalize('NFC', name).casefold()
```

This is *stricter* than CommonMark 0.30 link-reference-definition
matching, which mandates case-fold but not NFC. The extra NFC pass
collapses precomposed/decomposed duplicates. Document the strictness
explicitly so future maintainers see what was deliberate rather than
copy CommonMark verbatim.

A side effect: documents with case-distinct ASCII aliases like `#FOO`
and `#foo` -- previously accepted under byte-exact comparison -- now
fail MDPP008. The new acceptance grammar is a strict superset of the
old one (every alias valid before is valid now), but whole-document
validation is *not* a strict superset because the duplicate-detection
key changed. Surface this in the error-codes documentation; do not
characterize the whole change as "strict superset" without qualifying
which surface.

### Emit distinct error messages for byte-exact, case-fold, and NFC-equivalent duplicates

A single "duplicate alias" message is insufficient when normalization
is involved. Authors need to see whether the duplicate is because they
typed the same name twice, because they typed it in different case, or
because two visually identical aliases use different Unicode byte
sequences. Three sub-state messages:

1. **Byte-exact** -- raw strings identical.
2. **Case-fold** -- differ only in letter case (e.g., `#FOO` vs.
   `#foo`). Name both forms so authors who minted them expecting
   distinctness see the new behavior explicitly.
3. **NFC-equivalent** -- visually identical, different byte sequences.
   Include a plain-English gloss so the failure mode is obvious without
   the author having to know about Unicode normalization.

### Generate test fixtures with explicit code-point sequences and byte-verify

Editor and tool normalization is the dominant risk for any test fixture
that depends on decomposed Unicode. The MDPP008 NFC test must contain
the raw `e` + U+0301 byte sequence (`65 cc 81`); if the file is
silently NFC-normalized to precomposed `é` (`c3 a9`) the test trivially
passes for the wrong reason.

Generate such fixtures via a Python script using explicit code-point
escapes rather than by writing the characters directly. After writing,
byte-verify with `xxd` or equivalent that both `c3 a9` and `65 cc 81`
sequences are present. This is also the only reliable way to author
ZWJ, ZWNJ, and supplementary-plane test inputs.

### Scope the extension narrowly; leave sibling identifier classes ASCII for now

The standard identifier (variables, conditions) and the style/marker
name patterns remain ASCII-only. The three patterns are documented as
a shared grammar with deliberate variations; widening them in lockstep
needs its own audit. The alias case is unambiguous because aliases are
opaque, never user-visible, and downstream processors already accept
Unicode IDs at the conformant-processor level. The other patterns
surface differently (variables are written into output content; style
names are matched against processor catalogs) and have different
round-tripping constraints.

Track the deferral in the spec body so future maintainers see it as
deliberate rather than oversight:

> The standard and style/marker patterns remain ASCII-only pending a
> separate audit.

## Why This Matters

- **Round-trip safety is a property of the identifier class, not the
  output stage.** Picking the most permissive class (HTML-ID-legal)
  defers correctness to "does this happen to serialize OK?" Picking
  NCName makes round-trip safety a property of acceptance, so any
  alias that gets in the front door is guaranteed to make it through
  XML, XSLT, JavaScript, URL fragments, and CSS selectors.
- **Acceptance grammar and duplicate-detection equivalence must
  agree.** If the acceptance grammar permits two byte sequences that
  render identically, duplicate detection must collapse them.
  Otherwise authors mint two aliases that look identical in the source
  but resolve to different anchors -- a silent authoring failure.
- **Unicode constants in source are a silent-corruption surface.**
  The cost of escape-sequence constants is a few extra keystrokes; the
  cost of a literal-Unicode constant getting NFC-normalized or
  truncated to U+FFFD by some intermediate tool is a grammar drift
  that may not surface for months. Escape sequences are cheap
  insurance.
- **A narrow, justified extension is easier to expand than a broad,
  poorly justified one.** Future requests to extend Unicode-letter
  support to variable and style names will land against a known
  pattern (NCName) and a known set of conventions (explicit escapes,
  NFC + case-fold for dedup, test-fixture byte verification) rather
  than reopening every design question.

## When to Apply

- When extending any Markdown++ identifier grammar to a non-ASCII
  letter class, default to NCName unless the identifier has a specific
  reason to use a different class.
- When defining a character-class constant in any language that
  includes non-ASCII code points, use explicit numeric escapes for
  *every* range, not just supplementary-plane ones.
- When adding duplicate-detection to an identifier surface that accepts
  Unicode, key by NFC + case-fold, and document the strictness
  relative to CommonMark explicitly.
- When writing test fixtures that depend on decomposed Unicode or other
  byte-sensitive sequences, generate them programmatically and
  byte-verify after writing.

## Examples

### Spec grammar (`spec/formal-grammar.md`)

```ebnf
alias_name_start_char ::= "_" | [A-Z] | [a-z]
                        | [#xC0-#xD6] | [#xD8-#xF6] | [#xF8-#x2FF]
                        | [#x370-#x37D] | [#x37F-#x1FFF]
                        | [#x200C-#x200D] | [#x2070-#x218F]
                        | [#x2C00-#x2FEF] | [#x3001-#xD7FF]
                        | [#xF900-#xFDCF] | [#xFDF0-#xFFFD]
                        | [#x10000-#xEFFFF]

alias_name_char       ::= alias_name_start_char | digit | "-"
                        | [#x0300-#x036F] | [#x203F-#x2040]

alias_name            ::= (alias_name_start_char | digit) (alias_name_char)*
```

### Validator (`plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`)

```python
import unicodedata

_NCNAME_START_CHAR = (
    "_A-Za-z"
    "\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF"
    "\u0370-\u037D\u037F-\u1FFF"
    "\u200C-\u200D"
    "\u2070-\u218F"
    "\u2C00-\u2FEF"
    "\u3001-\uD7FF"
    "\uF900-\uFDCF"
    "\uFDF0-\uFFFD"
    "\U00010000-\U000EFFFF"
)

_NCNAME_COMBINING = (
    "\u0300-\u036F"
    "\u203F-\u2040"
)

ALIAS_NAME_RE = re.compile(
    f'^[{_NCNAME_START_CHAR}0-9]'
    f'[{_NCNAME_START_CHAR}0-9{_NCNAME_COMBINING}-]*$'
)

def _alias_dedup_key(name: str) -> str:
    """NFC + casefold; stricter than CommonMark 0.30 (casefold only)."""
    return unicodedata.normalize('NFC', name).casefold()
```

### Valid aliases under the new grammar

The Japanese, Café, Russian, and Greek examples are documented in spec
prose; bytes are not significant here.

```markdown
<!-- #introduction -->
<!-- #04499224 -->
<!-- #install-jp -->   <!-- placeholder: ASCII slug for a Japanese heading -->
<!-- #Cafe -->
<!-- #install-ru -->   <!-- placeholder: ASCII slug for a Russian heading -->
```

The native-script forms (`<!-- #インストール -->`, `<!-- #Café -->`,
`<!-- #установка -->`) live in `tests/sample-unicode-aliases.md` and
`tests/sample-unicode-duplicate-aliases.md`, which are
byte-verification-checked at write time. See those test fixtures for
authoritative copies; reproducing the bytes in this learning doc would
be a normalization risk without serving the doc's purpose.

### Aliases that still fail MDPP002

```markdown
<!-- #invalid name -->     <!-- whitespace -->
<!-- #invalid.name -->     <!-- period -->
<!-- #-leading-hyphen -->  <!-- hyphen in first position -->
```

### Duplicate aliases caught by MDPP008 (NFC + casefold)

```markdown
<!-- #introduction -->     <!-- first definition -->
<!-- #INTRODUCTION -->     <!-- case-fold duplicate -->

<!-- #Cafe-precomposed --> <!-- precomposed accented char in test fixture: bytes c3 a9 -->
<!-- #Cafe-decomposed -->  <!-- decomposed e + combining acute: bytes 65 cc 81 -->
                           <!-- NFC-equivalent duplicate in the actual fixture -->
```

### Test-fixture generation pattern (defends against silent NFC)

```python
# generate-tests.py
PRECOMPOSED_CAFE = "Café"           # c3 a9 for the accented char
DECOMPOSED_CAFE  = "Café"          # 65 cc 81 for e + combining acute

with open("tests/sample-unicode-alias-duplicates.md", "w", encoding="utf-8") as f:
    f.write(f"<!-- #{PRECOMPOSED_CAFE} -->\n")
    f.write(f"<!-- #{DECOMPOSED_CAFE} -->\n")

# After writing, byte-verify:
#   xxd tests/sample-unicode-alias-duplicates.md | grep -E 'c3 a9|65 cc 81'
# Both lines must appear, or some intermediate stage NFC-normalized
# the decomposed form and the test is now trivially passing.
```

## Related

- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`
  -- the originating naming-rule unification that this work extends.
  Moderate overlap; consolidation review candidate if a follow-up
  audit widens the standard or style/marker patterns to Unicode.
- `docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md`
  -- the formal grammar this work updates with the new productions.
- `docs/solutions/documentation-gaps/utf8-encoding-specification-gap-2026-04-08.md`
  -- UTF-8 is the encoding requirement that makes Unicode-letter
  identifiers possible at all.
- `docs/solutions/documentation-gaps/error-code-reference-2026-04-08.md`
  -- the MDPP002 / MDPP008 error-code registry tightened by this work.
- Issue #108 -- the originating issue.
- ePublisher Platform changeset `r35807` (EPUB2718) -- the downstream
  precedent that widened the Reverb landmark resolver to accept
  Unicode NCNames.
