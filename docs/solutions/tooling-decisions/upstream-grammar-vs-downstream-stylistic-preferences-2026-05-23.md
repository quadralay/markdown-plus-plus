---
title: "Don't project downstream stylistic preferences onto upstream identifier grammar"
date: 2026-05-23
category: tooling-decisions
module: markdown-plus-plus-spec
problem_type: tooling_decision
component: tooling
severity: medium
applies_when:
  - "Curating a subset of a well-defined identifier class (NCName, NMTOKEN, XML Name) because some downstream surface finds the full class awkward to consume"
  - "Weighing whether to permit a character in an authoring grammar based on whether it requires escaping in CSS, JavaScript, regex, or any other downstream consumer"
  - "Extending a position-aware identifier grammar where the same character has different meanings in first vs. non-first positions"
  - "Reframing an existing position-dependent rule that was previously stated as a flat allow/deny"
  - "Updating a multi-surface specification (spec prose, EBNF, PEG, validator regex, skill references, fixtures) where any one surface might drift from the others"
tags:
  - alias
  - mdpp002
  - grammar-framing
  - position-dependent-rules
  - spec-paired-updates
  - test-fidelity
  - ncname-namechar
---

# Don't project downstream stylistic preferences onto upstream identifier grammar

## Context

Issue #111 closed the gap between the Markdown++ custom-alias non-first
character class and the full XML NCName `NameChar` production. PR #109
had extended the *letter class* to NCName `NameStartChar` but stopped
short of adding `.` (period), `#xB7` (middle dot), combining marks, and
connector punctuation in non-first positions -- leaving a hybrid
grammar with no documented rationale for the omissions.

The deciding argument for closing the gap was **architectural**, not
typographic. CSS-selector friction (`document.querySelector('#foo\.bar')`
requires escaping the `.`) is a real consideration, but it belongs to
the stylesheet/JavaScript layer that consumes the alias as a CSS
selector. The upstream Markdown++ authoring grammar should not pre-filter
for that downstream consumer's stylistic preference. Every other
downstream surface that the alias must round-trip through -- HTML5
`id=`, URL fragments per RFC 3986, XML NCName -- accepts the full
`NameChar` class without modification.

The hybrid grammar's cost was twofold: authoring friction (DocBook-style
dotted-hierarchy identifiers like `#chapter.1.intro` and `#api.v1.users`
are idiomatic in XML-derived documentation, and the upstream WebWorks
ePublisher landmark resolver already accepts them), and specification
drift (the divergence from NCName `NameChar` had no recorded rationale,
so future contributors could not tell whether the omissions were
intentional or accidental).

This decision is the generalizable principle that flipped the trade-off,
plus the spec-paired-update disciplines that the PR #109 → #111 review
cycle surfaced.

## Guidance

### Don't pre-filter the authoring grammar for downstream stylistic preferences

When extending or curating an identifier grammar, the decision basis
should be: does the character round-trip safely through every
*conformant* downstream surface? Not: is the character convenient to
type in every *stylistic* downstream context?

The two questions sound similar and produce different answers:

- **Round-trip safety** is a property of the surface specification:
  HTML5 `id=`, RFC 3986 URL fragments, XML NCName. If every surface
  accepts the character per its own spec, the grammar can admit it.
- **Stylistic convenience** is a property of consumer code conventions:
  whether a stylesheet author prefers to avoid `\.` in selectors,
  whether a JavaScript author prefers `document.getElementById` over
  `document.querySelector`. These conventions vary across projects and
  belong in *project* style guides, not in the upstream authoring
  grammar.

If the grammar narrows for a stylistic preference, two failure modes
follow. Authors of the documentation format get a smaller set of
identifiers than the underlying standard provides, for reasons that are
invisible at the authoring layer (the connection between
`#chapter.1.intro` being rejected and CSS-selector ergonomics is not
self-evident to someone writing Markdown). And the format diverges from
the standard it claims to align with, requiring spec text to enumerate
the divergence and future maintainers to remember it.

The right place to document downstream friction is a downstream-friction
note in the authoring guide: "aliases containing `.` require escaping
in CSS selectors and `document.querySelector` calls; authors who use
aliases as CSS selectors may prefer to avoid `.` for that reason." That
puts the choice in the author's hands, transparently, without baking it
into the acceptance grammar.

### Frame position-dependent rules as position-dependent permissions, not flat allow/deny

`syntax-reference.md` previously said "no whitespace, no punctuation
other than `-` and `_`, no leading `.`" -- a flat statement that
treated `.` as forbidden everywhere except as a leading-position special
case. The PR #111 work reframed this as: "no whitespace; `-`, `.`, `_`,
middle dot, combining marks, and connector punctuation permitted in
non-first positions; no `.` in first position." Position is now the
load-bearing dimension; the rule reads as a permission with a
first-position carve-out rather than a prohibition with a first-position
escape clause.

The flat framing decays as the grammar grows: every new permitted
character is an exception. The position-dependent framing scales: new
characters slot in as "permitted in position X."

Apply this preemptively. When writing or reviewing an identifier rule
that uses words like "except," "but not in," or "unless," check whether
the underlying constraint is actually positional. If it is, restate the
rule as a position-dependent permission and write the negative example
with a position-correct explanation. The negative example
`<!-- #.hidden -->` survives unchanged but now reads "period not
permitted in first position" instead of the ambiguous "period cannot
start an alias name."

### Move every spec surface in lockstep when the grammar changes

A multi-surface specification has at least five places the grammar is
restated: prose paragraph, table sketch, EBNF, PEG, validator regex.
A grammar change must update every one of these. Review of the #111
work caught a stale `[NCName-letter | "_" | digit | "-"]*` sketch in
`spec/specification.md` § 4.2's Naming Rules table that contradicted
the prose paragraph below it (which had been updated) and the actual
validator regex.

Two ways to defend against this:

1. **Grep for the old grammar fragment after the update.** The stale
   sketch had the literal text `NCName-letter` -- a string that should
   not survive a `NameChar` extension. A `grep -F 'NCName-letter'`
   would have caught the drift in seconds. Maintain a small list of
   "fingerprint strings" from the prior grammar and grep for them as
   the final pre-commit check.
2. **Treat the prose-paragraph and table-sketch as a paired update.**
   In review, look for the table sketch first when prose changes, and
   for the prose when the sketch changes. The two are conceptually
   one block; they should never be edited independently.

The same discipline applies to references between the spec and its
test fixtures. When `spec/formal-grammar.md` cites a fixture by name
(`<!--#.bad-->`), the citation must match the fixture's actual content
(`<!--#.bad-alias-->`). A rename or trim of a fixture body without
updating its citation creates documentation drift that no validator
catches.

### Encode Unicode-range tests with codepoints that *only* match the targeted range

A test that purports to exercise the combining-mark range
(`̀-ͯ`) must contain a codepoint from that range, not a
codepoint that happens to render the same way. The original #111
fixture for Case U14 was authored with `foè-bar` where `è` is
precomposed U+00E8 -- a single codepoint already accepted by
`_NCNAME_START_CHAR`. The test passed for an unrelated reason and the
combining-mark range was effectively untested.

The corrected fixture uses the decomposed form `e` (U+0065) +
combining grave accent (U+0300). Now a regression in the combining-mark
range would fail the fixture.

The general rule: when a test targets a specific character range,
verify that the test input is parsed *only* by that range. If the
input would also be accepted by some other range in the same regex,
the test cannot distinguish between "the targeted range works" and
"some other range happens to cover this codepoint." Use code-point
escapes (`"è"`) rather than literal characters when writing such
fixtures, and prefer characters that have no precomposed alternative
when possible.

A practical heuristic: if you can find the test's character in
[Unicode's "characters with both precomposed and decomposed forms"
list](https://www.unicode.org/Public/UCD/latest/ucd/CompositionExclusions.txt),
the test is at risk of silent NFC collapse during authoring. Either
use a different character (no precomposed alternative) or generate the
fixture programmatically with explicit codepoint sequences and
byte-verify after writing (see the predecessor doc
[`unicode-alias-letter-class-via-ncname.md`](unicode-alias-letter-class-via-ncname.md)
for the byte-verification recipe).

## Why This Matters

- **The authoring grammar is the contract authors program against.**
  Narrowing it for reasons that live three layers downstream means
  authors can't predict what's accepted without understanding the full
  consumer chain. That's the opposite of what a specification is for.
- **Aligning with a published standard (NCName, NMTOKEN, etc.) earns
  precision for free.** Every divergence is a footnote a future
  maintainer has to memorize. The leading-digit allowance in
  Markdown++ aliases is a worthwhile divergence (numeric-ID
  compatibility); the period-in-non-first-position omission was not.
- **Position-dependent rules are the natural shape of identifier
  grammars.** Flat allow/deny lists work for the simplest cases and
  fall apart the moment a character has different meanings at
  different positions. The reframing cost is small and the resulting
  rule scales.
- **Multi-surface specifications drift silently.** The validator regex
  is the only surface that's mechanically executed; everything else
  (prose, table sketch, EBNF, PEG, fixture-name references) is checked
  by reading. Fingerprint-grep and paired-update discipline are cheap
  insurance against the surfaces falling out of sync.
- **Unicode tests are unusually vulnerable to silent-pass failures.**
  A test that "passes" because the input happened to be accepted by a
  different range than the one under test is worse than a missing
  test -- it gives false confidence. Codepoint-targeted authoring is
  the only reliable defense.

## When to Apply

- When deciding whether to admit a character to an identifier grammar:
  ask whether every conformant downstream surface accepts it, not
  whether every stylistic consumer prefers it.
- When stating a rule like "no X except in position Y": rewrite it as
  "X permitted in position Y; not permitted in position Z" and check
  whether negative examples carry position-correct explanations.
- After updating any grammar surface (prose, table, EBNF, PEG,
  validator): grep the repo for the old grammar's fingerprint strings;
  the search must come back empty.
- When citing a test fixture by name in spec docs: verify the citation
  matches the fixture's current content. Fixture renames and body
  edits are the most common cause of citation drift.
- When writing a fixture for a Unicode-range test: encode the test
  input with explicit codepoints from the targeted range; verify the
  input is parsed *only* by that range.

## Examples

### Grammar curation decision (the principle in action)

The full XML NCName `NameChar` production:

```
NCNameChar ::= NCNameStartChar | "-" | "." | [0-9] | #xB7
             | [#x0300-#x036F] | [#x203F-#x2040]
```

The #111 decision: admit all of these in non-first positions of an
alias name. The downstream consumers that matter (HTML5 `id=`, RFC 3986
URL fragments, XML NCName) accept every codepoint. CSS selectors
require escaping `.`, but that is a stylesheet-author concern surfaced
in a documentation note, not a grammar constraint.

### Position-dependent rule restatement

Before (flat allow/deny):
> Alias names must contain no whitespace, no punctuation other than
> `-` and `_`, no leading `.`.

After (position-dependent permission):
> Alias names contain no whitespace. The following characters are
> permitted in non-first positions: `-`, `.`, `_`, middle dot
> (`#xB7`), combining marks (`#x0300-#x036F`), connector punctuation
> (`#x203F-#x2040`). The first position permits NCName
> `NameStartChar` and digit, but not `.` or any of the non-first
> additions.

### Fingerprint grep for stale grammar fragments

After extending `alias_name_char`, the pre-commit check:

```bash
git grep -F 'NCName-letter' spec/ plugins/markdown-plus-plus/skills/
```

If this returns hits, a surface still reflects the old grammar.

### Codepoint-targeted combining-mark test

```python
# Wrong: precomposed U+00E8, accepted by _NCNAME_START_CHAR.
FIXTURE_U14_WRONG = "foè-bar"

# Right: decomposed e (U+0065) + combining grave (U+0300),
# parseable only via _NCNAME_COMBINING.
FIXTURE_U14_RIGHT = "foè-bar"
```

After writing, byte-verify:

```bash
xxd tests/sample-unicode-aliases.md | grep -E '65 cc 80'
# Must appear exactly where the U14 case sits.
```

## Related

- [`unicode-alias-letter-class-via-ncname.md`](unicode-alias-letter-class-via-ncname.md)
  -- the predecessor decision (PR #109) that chose NCName as the
  alias letter class. This #111 doc extends that lineage by recording
  the architectural framing principle that drove the NCName
  `NameChar` alignment. Consolidation candidate if a future audit
  widens variable, condition, or style/marker patterns to Unicode
  using the same framing.
- `docs/solutions/conventions/normative-rules-against-competing-conventions-2026-05-18.md`
  -- shares the meta-pattern of "state the load-bearing rule
  positionally, not by grouping verbs or flat allow/deny."
- `docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md`
  -- the formal-grammar surface that the paired-update discipline
  applies to.
- Issue #111 -- the originating issue, with the full architectural
  rationale in the issue body.
- ePublisher Platform changeset `r35807` -- downstream precedent for
  widening the landmark resolver to accept the full HTML-ID-legal
  class (a superset of NCName).
