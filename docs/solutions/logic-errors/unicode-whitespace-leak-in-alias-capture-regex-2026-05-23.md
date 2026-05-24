---
title: Unicode whitespace silently bypassed alias capture regex
date: 2026-05-23
category: logic-errors
module: markdown-plus-plus-validator
problem_type: logic_error
component: tooling
symptoms:
  - "Aliases containing Unicode whitespace (U+00A0, U+202F, U+3000) were never extracted by the validator"
  - "MDPP002 (invalid alias name) failed to fire on malformed aliases with non-ASCII whitespace inside the name"
  - "MDPP008 (duplicate alias) could not fire when one of the duplicates contained Unicode whitespace because no alias key was registered"
  - "Validator exited with code 0 on input that should have produced errors"
  - "Only PATTERNS['alias'] had the bug; other extractors used enumerated body classes and were unaffected"
root_cause: logic_error
resolution_type: code_fix
severity: medium
tags:
  - validator
  - alias
  - regex
  - unicode-whitespace
  - mdpp002
  - mdpp008
  - silent-validation-failure
  - python-re
---

# Unicode whitespace silently bypassed alias capture regex

## Problem

The Markdown++ validator's alias-extraction regex used `[^\s;>]+?` for the alias-body character class. Because Python 3's `\s` is Unicode-aware, the pattern excluded non-ASCII whitespace (NBSP, narrow NBSP, ideographic space, etc.) from the capture, so aliases containing those characters were never extracted and MDPP002 / MDPP008 never fired — malformed input passed validation silently.

## Symptoms

- A comment like `<!-- #foo<NBSP>bar -->` (where `<NBSP>` is U+00A0) parsed cleanly: no MDPP002, no MDPP008, no diagnostic of any kind.
- Validation reported the document as valid (exit code 0) even though the alias name violated the `NameChar` grammar defined in `spec/formal-grammar.md`.
- The failure was uniform across the Unicode whitespace class: U+00A0, U+202F, and U+3000 all produced the same silent pass, because `\s` matched all of them and removed them from the captured body before `ALIAS_NAME_RE` ever saw the name.
- The bug pre-dated the #108/#109 Unicode-letter extension. Once that extension widened what was *allowed* in an alias name, the silent-extraction failure became materially more reachable — but the regex shape was wrong on `main` before either PR landed.

## What Didn't Work

Switching the whole alias regex to `re.ASCII` mode looks tempting but has a wider blast radius than the bug. The pattern's trailing lookahead is `(?=\s*;|\s*-->)`, and that `\s*` is deliberately Unicode-permissive — trailing whitespace between the alias and its terminator is a layout choice the spec tolerates. `re.ASCII` would also narrow that `\s`, changing layout behavior the fix has no business touching.

Tightening the lookahead (for example, requiring the terminator to butt directly against the alias) doesn't address the bug either. The alias body would still silently swallow non-ASCII whitespace if `\s` stayed in the body class; the failure would just relocate, not surface.

Counting on `ALIAS_NAME_RE` (the `NameChar` validator) to reject these names downstream doesn't work because there is no downstream layer in the failure case. `ALIAS_NAME_RE` only runs on what the extraction regex captures. If the extraction regex's body class refuses to match the comment at all, there is no captured name to validate — the comment is invisible to MDPP002 and MDPP008.

## Solution

One character-class swap in `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` at line 71.

Before:

```python
'alias': re.compile(r'<!--\s*#([^\s;>]+?)(?=\s*;|\s*-->)'),
```

After:

```python
'alias': re.compile(r'<!--\s*#([^ \t\n\r;>]+?)(?=\s*;|\s*-->)'),
```

The body class now excludes only the four ASCII whitespace characters that genuinely terminate an alias name. The trailing lookahead's `\s*` is unchanged on purpose — it governs layout slack before the terminator, not the name itself.

A regression fixture covering the three primary Unicode whitespace code points (plus an ASCII positive control) was added at `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-whitespace-aliases.md`. Existing corpus error counts are unchanged after the fix; the change is additive on the diagnostic surface only.

## Why This Works

Two concerns interact here:

1. **Python 3 `\s` is Unicode-aware by default.** `\s` matches U+00A0, U+202F, U+3000, and the rest of the Unicode whitespace class — not just `[ \t\n\r\f\v]`. In a *negated* class like `[^\s;>]`, that breadth means non-ASCII whitespace gets *excluded* from what the body can capture.
2. **The alias `NameChar` validator (`ALIAS_NAME_RE`) only sees what the body class captures.** Anything the body class refuses to absorb is invisible to the validator. The extraction regex IS the gate; there is no second-pass parser.

The combination meant a non-ASCII whitespace character inside an alias name caused the body to terminate early — and because the lookahead then failed to find its terminator at that position, the regex didn't match at all, and the comment was treated as not-an-alias rather than as a malformed alias. Narrowing the body's exclusion set to ASCII whitespace lets the non-ASCII whitespace flow into the captured group; `ALIAS_NAME_RE` then sees the malformed name and MDPP002 fires.

## Prevention

1. **Be deliberate about `\s` vs. enumerated ASCII whitespace.** When an extraction regex implements an ASCII-defined grammar (XML NCName, identifier-shaped tokens, the alias body), spell ASCII whitespace literally: `[ \t\n\r]`. Reserve `\s` for positions where Unicode whitespace tolerance is genuinely intended — typically layout slack around terminators, not inside captured names.

2. **Audit the `PATTERNS` table on every change.** When adding or modifying an entry in `PATTERNS` in `validate-mdpp.py`, check two things: (a) does the body class use `\s` in a negated set, and (b) does the grammar it implements admit non-ASCII whitespace? If the answer to (a) is yes and (b) is no, swap to the enumerated form. The one-time audit at fix time confirmed only `'alias'` had this shape — the other extractors (`variable`, `variable_invalid`, `style`, `condition_open`, `include`, `markers_json`, `marker_simple`) use enumerated classes or `[^>]+?` and are unaffected. `MDPP_TAG_PATTERN` uses `#[^\s;>]+` but is detection-only with no capture, so it has no downstream validator to bypass. `add-aliases.py`'s `ALIAS_PATTERN` already uses the enumerated NCName-derived class.

3. **Capture-then-validate must be ASCII-strict on the boundary.** The earlier `#15` fix established the discipline "widen capture before narrowing validation" (see `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`). That rule still holds — this fix corrects an unforeseen consequence of using `\s` to express the capture boundary. The capture boundary itself must be enumerated when the grammar is ASCII-defined; the validation regex behind it inherits Unicode behavior from its own rules (NCName, in the alias case).

4. **Cover at least one Unicode whitespace code point in fixtures for any extraction regex that captures identifier-shaped content.** The regression fixture added with this fix exercises NBSP (U+00A0), NARROW NBSP (U+202F), and IDEOGRAPHIC SPACE (U+3000) alongside an ASCII positive control. Future extraction-regex changes should extend this fixture (or one like it) rather than rely on ASCII-only test inputs.

## Related Issues

- [#115](https://github.com/quadralay/markdown-plus-plus/issues/115) — This issue: alias capture regex silently bypassed Unicode whitespace.
- [#108](https://github.com/quadralay/markdown-plus-plus/issues/108) / PR [#109](https://github.com/quadralay/markdown-plus-plus/pull/109) — Widened the alias letter class to XML NCName. The Unicode-letter extension made this latent bug materially more reachable but did not introduce it. Residual finding 7 on PR #109 surfaced this issue.
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) — `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` — Established the `[^\s;>]+?` body class and the "widen capture before narrowing validation" discipline. This fix refines the rule: when the grammar is ASCII-defined, the capture boundary must be enumerated, not `\s`-based.
- `docs/solutions/tooling-decisions/unicode-alias-letter-class-via-ncname.md` — Companion learning on the *acceptance* side of the alias surface. Together, the two docs document a coherent boundary: acceptance widened to NCName, extraction tightened to ASCII whitespace.
- Plan artifact: `docs/plans/2026-05-23-001-fix-alias-extraction-unicode-whitespace-plan.md`.
- Fix commits: `f9ae062` (character-class swap, audit, tests, docs); `fb6e851` (inline-comment clarification).
