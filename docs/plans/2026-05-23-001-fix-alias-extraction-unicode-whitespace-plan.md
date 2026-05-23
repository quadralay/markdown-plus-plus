---
title: "fix: Tighten alias extraction so Unicode whitespace surfaces MDPP002"
type: fix
status: active
date: 2026-05-23
---

# fix: Tighten alias extraction so Unicode whitespace surfaces MDPP002

## Summary

Tighten the alias body character class in `PATTERNS['alias']` from `[^\s;>]+?` (Python-Unicode `\s`) to `[^ \t\n\r;>]+?` (ASCII whitespace only) so non-ASCII whitespace -- U+00A0 (NBSP), U+202F (NARROW NBSP), U+3000 (IDEOGRAPHIC SPACE), and other Unicode whitespace code points -- flows into the captured alias name and trips MDPP002 instead of silently bypassing validation. The trailing `(?=\s*;|\s*-->)` lookahead remains Unicode-permissive on purpose so that layout whitespace between the alias and the terminator is still tolerated.

---

## Problem Frame

Issue #115 surfaced a pre-existing bug in `scripts/validate-mdpp.py`. The alias extraction regex used `[^\s;>]+?` as its body character class. Because Python 3's `\s` defaults to Unicode mode, the character class excluded both ASCII whitespace *and* every non-ASCII whitespace code point (U+00A0, U+202F, U+3000, and the rest of `\p{Z}` plus the control-character whitespace).

When a non-ASCII whitespace character appears between alias-name characters -- e.g., `<!-- #foo bar -->` with a NO-BREAK SPACE between `foo` and `bar` -- the body class cannot consume it. The non-greedy body stopped after `foo`. The lookahead `(?=\s*;|\s*-->)` then needed `;` or `-->` after intervening whitespace, but the next non-whitespace byte was `b`. The whole regex failed to match. The malformed alias was never extracted, MDPP002 (invalid alias name) never fired, and MDPP008 (duplicate alias) could not fire either because no alias key was ever registered.

This was a pre-existing issue. The regex shape predates the #108/#109 Unicode-letter NCName extension. The Unicode-letter work did not introduce or change the extraction regex. Surfaced as residual finding 7 on PR #109 review.

---

## Requirements

- R1. Replace the alias body character class with an ASCII-whitespace-only enumeration so non-ASCII whitespace inside an alias name flows into the capture and surfaces through MDPP002.
- R2. Preserve the trailing `(?=\s*;|\s*-->)` lookahead's Unicode-permissive behavior so layout whitespace between the alias and the terminator continues to be tolerated.
- R3. Add a test fixture exercising at least three Unicode-whitespace code points (U+00A0, U+202F, U+3000) and at least one ASCII-whitespace positive control showing valid aliases continue to pass.
- R4. Audit the remaining `PATTERNS` entries and `add-aliases.py` `ALIAS_PATTERN` to confirm no other extractor has the same `\s`-inside-body shape; document the audit result in the commit message.
- R5. Update `references/error-codes.md` § MDPP002 to note that Unicode whitespace inside an alias name is caught the same way illegal punctuation is.
- R6. Record the change in `CHANGELOG.md` as a bug fix that strengthens MDPP002 coverage without changing the grammar.
- R7. Compatibility floor: every existing alias in `examples/`, `tests/`, and downstream documents continues to validate without new MDPP002 emissions. The fix only adds coverage; it does not relax any prior check.

---

## Scope Boundaries

- The leading `\s*` in every `PATTERNS` extraction template -- whether ASCII-only whitespace should be required between the comment opener and the directive keyword is a related but distinct question. This plan does not change leading-whitespace handling.
- Other extraction patterns that do not use `\s` inside a body character class. Audit confirms only `'alias'` had the bug; if a future audit finds another pattern with the same shape, it belongs in a follow-up.
- The combined-command terminator lookahead `(?=\s*;|\s*-->)`. Leaving this Unicode-permissive is intentional: after the capture stops at the first ASCII whitespace, trailing Unicode whitespace before `;` or `-->` should still be tolerated.
- ASCII-whitespace-inside-name aliases (e.g., `<!--#foo bar-->` with a plain ASCII space). The regex still fails to match these entirely because the lookahead cannot find `;` or `-->` after the captured prefix; that remains a separate follow-up.
- The MDPP002 error message stays as-is. Naming the offending Unicode code point in the message is a nice-to-have suggested by the issue but is not adopted -- the validator's existing "Invalid alias name: #<text>" message plus the trimmed `alias_name` rule reference is sufficient.

---

## Context & Research

### Relevant Code and Patterns

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` -- `PATTERNS` dict at module top; the `'alias'` entry's body character class is the single point of change.
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py` -- the sibling script's `ALIAS_PATTERN`, audited for the same shape.
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-aliases.md` -- Case U9 documented the pre-fix Unicode-whitespace edge case; updated here to cross-reference the new fixture.
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-invalid-names.md` -- the existing fixture for MDPP002 illegal-name coverage; not modified because the new fixture is a more focused vehicle for the Unicode-whitespace cases.

### Institutional Learnings

- `docs/solutions/` does not contain a prior entry on this specific regex shape. The closest related history is PR #108/#109 (Unicode-letter NCName extension), which surfaced the residual finding that prompted this issue.
- Python's `re` module defaults to Unicode-aware `\s` in Python 3. The `re.ASCII` flag would change `\s` semantics globally for the pattern; the safer fix for a single character class is enumeration.

### External References

- XML 1.0 NCName `NameChar` production (the alias-name acceptance grammar). Non-ASCII whitespace is not in `NameChar`, so MDPP002 correctly rejects it once the regex captures it.
- CommonMark 0.30 link-reference-definition slug matching (referenced for MDPP008 NFC + casefold equivalence -- not changed here, but the alias key normalization continues to apply).

---

## Key Technical Decisions

- **Character-class enumeration over `re.ASCII` flag**: Replacing `[^\s;>]+?` with `[^ \t\n\r;>]+?` localizes the change to the body class. Adding `re.ASCII` to the pattern's flags would also affect any future expansion of the regex and is heavier than needed. Rationale: surgical fix matches the surgical bug.
- **Lookahead stays Unicode-permissive**: The capture stops at the first ASCII whitespace by design; whatever Unicode whitespace follows the capture before `;` or `-->` is a layout choice, not part of the name. Keeping the lookahead at `\s*` preserves that tolerance without re-introducing the silent-swallow bug.
- **Error message unchanged**: The validator emits "Invalid alias name: #<captured-text>" plus the alias-name rule explanation. The captured text now contains the offending Unicode whitespace, which makes the offending byte visible in the message context even without explicitly naming the code point. Adding code-point identification would require an extra pass over the captured text and is not warranted for a one-line regex fix.
- **New fixture file vs. extending sample-invalid-names.md**: A new focused fixture (`tests/sample-unicode-whitespace-aliases.md`) groups the NBSP / NNBSP / IDEO cases plus the positive control in one place, mirrors the structure of `sample-unicode-aliases.md`, and keeps `sample-invalid-names.md` focused on punctuation-class invalid names.
- **Patch-level version bump**: The change strengthens MDPP002 coverage but does not change the alias grammar, the validator's CLI, or any error code. It is a bug fix. Plugin version moves from 1.7.3 to 1.7.4.

---

## Implementation Units

### U1. Tighten `PATTERNS['alias']` body character class

**Goal:** Replace the alias body character class so non-ASCII whitespace flows into the capture instead of failing the match entirely.

**Requirements:** R1, R2

**Dependencies:** None

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`

**Approach:**
- Change `PATTERNS['alias']` body class from `[^\s;>]+?` to `[^ \t\n\r;>]+?`.
- Leave the trailing `(?=\s*;|\s*-->)` lookahead untouched.
- Add an inline comment immediately above the pattern explaining why the body class is ASCII-only while the lookahead remains Unicode-permissive. This is the kind of non-obvious WHY that survives renaming and refactoring.
- Audit the other entries in `PATTERNS` (`variable`, `variable_invalid`, `style`, `condition_open`, `condition_close`, `include`, `markers_json`, `marker_simple`, `multiline`) and `MDPP_TAG_PATTERN`; document the audit result in the commit message. Confirm that none use `\s` inside a body character class that captures.

**Patterns to follow:**
- Existing inline comments in the same `PATTERNS` dict that explain non-obvious regex shape (none currently present; this is the first).

**Test scenarios:**
- *Edge case:* `<!--#foo nbsp-->` (U+00A0 between `foo` and `nbsp`) -- the regex matches and the captured name is `foo<NBSP>nbsp`, which trips MDPP002 because U+00A0 is not in the alias `NameChar` class.
- *Edge case:* `<!--#foo narrow-->` (U+202F) -- matches and emits MDPP002.
- *Edge case:* `<!--#foo　ideographic-->` (U+3000) -- matches and emits MDPP002.
- *Edge case:* `<!-- #foo bar -->` (U+00A0 between `foo` and `bar`, ASCII spaces flanking the alias) -- captures `foo<NBSP>bar`, the lookahead absorbs the trailing ASCII space and `-->`, MDPP002 fires.
- *Happy path:* `<!--#plain-ascii-alias-->` -- continues to validate cleanly with no MDPP002 emission.
- *Happy path / negative control:* `<!--#foo bar-->` (plain ASCII space) -- behavior unchanged: the regex still fails to match because the lookahead cannot find `;` or `-->` after the captured prefix. This is the deferred ASCII-whitespace-in-name follow-up; the fix does not regress it.

**Verification:**
- Running `validate-mdpp.py` against the new fixture (U2) emits one MDPP002 per Unicode-whitespace negative case and no MDPP002 on the positive control.
- The existing test corpus (`sample-unicode-aliases`, `sample-unicode-duplicate-aliases`, `sample-invalid-names`, `sample-duplicate-aliases`, `sample-basic`, `sample-custom-alias-priority`, `sample-full`) produces the same error count before and after the change.

---

### U2. Add Unicode-whitespace alias-rejection fixture

**Goal:** Create a focused test fixture covering the three Unicode-whitespace code points named in the issue plus a positive control, and cross-reference Case U9 in the existing Unicode-alias fixture so future readers find the new corpus.

**Requirements:** R3, R7

**Dependencies:** U1

**Files:**
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-whitespace-aliases.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-aliases.md`

**Approach:**
- New fixture follows the same structure as `sample-unicode-aliases.md`: YAML frontmatter, a context paragraph linking to issue #115, a positive-control section (W0), and negative-case sections (W1, W2, W3, W4).
  - W0: plain ASCII alias -- expect no error.
  - W1: U+00A0 NBSP between `foo` and `nbsp` -- expect MDPP002.
  - W2: U+202F NARROW NBSP -- expect MDPP002.
  - W3: U+3000 IDEOGRAPHIC SPACE -- expect MDPP002.
  - W4: U+00A0 inside name with ASCII space flanking the alias (spaced-form layout) -- expect MDPP002.
- Each negative case is followed by a heading the alias would anchor to, so the fixture also exercises the orphan-tag (MDPP009) interaction implicitly.
- Update Case U9 in `sample-unicode-aliases.md` to point readers at the new fixture and clarify that ASCII-whitespace-in-name remains a separate follow-up (the regex still fails entirely on ASCII space inside the body because the lookahead cannot find `;` or `-->`).

**Patterns to follow:**
- `tests/sample-unicode-aliases.md` structure (date / status frontmatter, context paragraph, positive section, negative section, per-case headings, `<!--#alias-->` immediately above the heading it anchors).
- `tests/sample-unicode-duplicate-aliases.md` for the level of inline commentary expected in a Unicode-aware fixture.

**Test scenarios:**
- *Happy path:* Running the validator on the fixture emits exactly four MDPP002 errors (one per negative case W1-W4) and zero errors on W0.
- *Edge case:* The fixture loads cleanly as Markdown when previewed in any standard renderer -- Unicode whitespace is not visible but the fixture is still readable.

**Verification:**
- `python validate-mdpp.py tests/sample-unicode-whitespace-aliases.md` exits with code 3 and the four expected MDPP002 emissions; the positive control does not appear in the error output.
- Case U9 in `sample-unicode-aliases.md` references the new fixture by relative path.

---

### U3. Document the change in the MDPP002 reference and CHANGELOG

**Goal:** Surface the behavior change to authors and downstream consumers so the new MDPP002 coverage is discoverable from the error-code reference and the release log.

**Requirements:** R5, R6

**Dependencies:** U1, U2

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
- Modify: `CHANGELOG.md`
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (patch-bump version)
- Modify: `.claude-plugin/marketplace.json` (patch-bump version)

**Approach:**
- In `references/error-codes.md` § MDPP002, add a "Whitespace inside alias names" paragraph after the "Suggested fix" block. It states that non-ASCII whitespace inside an alias name is caught the same way illegal punctuation is, names the four most likely code points (U+00A0, U+202F, U+3000, and "other Unicode whitespace"), and back-references the pre-1.7.4 silent-swallow bug with a link to issue #115.
- In `CHANGELOG.md`, add a `[1.7.4]` section under `### Tooling` describing the regex tightening, the new fixture, the Case U9 update, and the audit of the other `PATTERNS` entries. Include the `add-aliases.py` audit result.
- Use `scripts/bump-version.sh patch` to bump both `plugin.json` and `marketplace.json` from 1.7.3 to 1.7.4.

**Patterns to follow:**
- The CHANGELOG entries for 1.7.0 / 1.7.1 / 1.7.2 / 1.7.3 set the precedent for prose-dense single-bullet entries that capture the WHY in addition to the WHAT.
- The MDPP002 section already carries a "Trigger examples" block and a "Suggested fix" block; the new whitespace paragraph slots in immediately below "Suggested fix".

**Test scenarios:**
- *Test expectation: none -- documentation update with no behavioral change.*

**Verification:**
- `references/error-codes.md` § MDPP002 mentions Unicode whitespace explicitly.
- `CHANGELOG.md` 1.7.4 entry names the regex change, the fixture, the documentation update, and the `PATTERNS` / `add-aliases.py` audit result.
- `plugin.json` and `marketplace.json` both show version 1.7.4.

---

## System-Wide Impact

- **Interaction graph:** The change touches only `PATTERNS['alias']`. The orphan-tag check (`MDPP_TAG_PATTERN`) uses a parallel `#[^\s;>]+` shape but is detection-only with no capture, so its behavior is unchanged. MDPP008 (duplicate alias) continues to receive whatever alias names MDPP002 accepts and applies NFC + casefold normalization for its dedup key.
- **Error propagation:** No change. MDPP002 fires through the same severity / context / suggestion path it always has.
- **State lifecycle risks:** None. The validator is stateless across files; per-file state (the `alias_locations` dict for MDPP008) is unaffected.
- **API surface parity:** No CLI surface change. The validator's exit codes, JSON output schema, and severity classification are all untouched.
- **Integration coverage:** The new fixture covers the regex / MDPP002 / MDPP008 interaction. The MDPP009 (orphan tag) interaction is exercised incidentally by the per-case headings.
- **Unchanged invariants:** The alias acceptance grammar (XML NCName `NameChar`-based, digit-first permitted). MDPP008 NFC + casefold equivalence. The validator's set of error codes. All previously-valid aliases continue to validate.

---

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| A document somewhere in the wild relied on the silent-swallow behavior to "hide" an invalid alias from validation. | The pre-fix behavior was a bug; the new behavior is what the validator's contract advertises. Any document depending on the silent swallow was already broken and is now surfaced for repair. The CHANGELOG entry calls this out explicitly. |
| Another `PATTERNS` extractor has the same `\s`-inside-body shape and was not caught by the audit. | The audit enumerates every entry in `PATTERNS` plus `MDPP_TAG_PATTERN` and `add-aliases.py` `ALIAS_PATTERN`. If a future regex addition introduces the shape, a `re.ASCII`-aware lint rule (or simply re-running this audit) would catch it. Out of scope for this plan. |
| The alias capture now includes a leading non-printable Unicode whitespace byte in the error message, which may render poorly in some terminals. | The validator's error message already passes the captured text verbatim. NBSP and similar code points display as a space or a placeholder glyph in most terminals; the rule reference in the suggestion text makes the diagnosis clear without the user having to identify the code point visually. |

---

## Sources & References

- Issue: [#115](https://github.com/quadralay/markdown-plus-plus/issues/115)
- PR review that surfaced the finding: [#109 review comment](https://github.com/quadralay/markdown-plus-plus/pull/109#issuecomment-4524143918)
- Related prior work: PR #108 / #109 (Unicode-letter NCName alias grammar) -- predates the bug; did not introduce or change the extraction regex.
- Related code: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` (`PATTERNS['alias']`), `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py` (`ALIAS_PATTERN`, audited).
- Spec reference: [`spec/formal-grammar.md`](../../spec/formal-grammar.md) `alias_name`, `alias_name_start_char`, `alias_name_char` productions.
