---
date: 2026-05-23
status: active
plan_type: feat
issue: 111
predecessor_issues: [108, 109]
---

# feat: Extend alias NameChar to full XML NCName production

**Target issue:** [#111](https://github.com/quadralay/markdown-plus-plus/issues/111)

**Source:** Issue body authored as a deferred follow-up to PR #109. No upstream `*-requirements.md` brainstorm exists; the issue body itself is the origin document and supplied a complete scope and architectural rationale.

**Plan depth:** Standard (specification change with multiple surfaces: spec text, formal grammar, two skill scripts, three skill references, two test fixtures). External contract surfaces touched: published spec, MDPP002 acceptance grammar, validator regex, alias-scanner regex.

---

## Problem Frame

PR #109 (closes #108) extended the alias *letter class* to the XML 1.0 NCName `NameStartChar` ranges -- aliases now accept Japanese, Greek, Cyrillic, and other non-Latin script letters in any position. PR #109 also opportunistically added the NCName combining-mark ranges (`#x0300-#x036F`) and connector-punctuation ranges (`#x203F-#x2040`) to the *non-first* character class so decomposed accented forms accept under MDPP002 at the raw-byte level (MDPP008 then NFC-normalizes for duplicate detection).

PR #109 explicitly stopped short of two additional NCName `NameChar` extras: period (`.`, `#x2E`) and middle dot (`#xB7`). The result was a hybrid grammar -- the alias letter class matched NCName but the non-first character class did not. The issue body cites this gap and proposes closing it by making `alias_name_char` a direct alias of the XML NCName `NameChar` production, with the digit-first allowance in `alias_name` itself remaining as the sole documented deviation from NCName.

The hybrid grammar had two costs:

1. **Authoring friction.** Dotted-hierarchy identifiers (`#chapter.1.intro`, `#api.v1.users`) are idiomatic in XML-derived documentation systems (DocBook, DITA), and the upstream WebWorks ePublisher landmark resolver already accepts them via [changeset r35807](https://factory.webworks.com/ePublisher_Platform/changeset/35807). Markdown++'s grammar rejected them despite every downstream surface accepting them.
2. **Specification drift.** The MDPP002 acceptance grammar diverged from the NCName production it was modeled on without an explicit rationale, leaving future contributors to wonder whether the omissions were intentional or accidental.

## Architectural Rationale

The alias is an opaque HTML-comment anchor (`<!-- #name -->`) invisible to standard CommonMark renderers. Its only purpose is to round-trip through the downstream pipeline as an `id=` attribute, URL fragment, or XML landmark. All three downstream surfaces accept NCName-conformant identifiers without modification:

- HTML5 `id` attributes permit any non-whitespace character (superset of NCName).
- URL fragments per RFC 3986 permit `.` in `pchar`/`unreserved`.
- XML NCName is, by construction, NCName.

CSS-selector escaping (`#foo\.bar`) is a concern for stylesheet/JavaScript authors, not for the upstream authoring grammar. Markdown++ should not project downstream stylistic preferences onto the source-document syntax -- that decision belongs to the project's CSS/JS conventions, not the format specification. This framing is what flips the trade-off from "curated subset of NCName NameChar" to "full NCName NameChar alignment".

---

## Scope

### In Scope

Extend the alias `NameChar` (non-first position) character class to the full XML NCName `NameChar` production:

```
NCNameChar ::= NCNameStartChar | "-" | "." | [0-9] | #xB7 | [#x0300-#x036F] | [#x203F-#x2040]
```

Concretely this adds, for non-first positions only:

- `.` (period, `#x2E`)
- `#xB7` (middle dot)
- `#x0300-#x036F` (combining diacritical marks) -- *already accepted under #109; retained verbatim*
- `#x203F-#x2040` (connector punctuation: undertie, character tie) -- *already accepted under #109; retained verbatim*

The net behavioral delta from PR #109 is **period and middle dot only**; the framing change is "direct alias of NCName NameChar" rather than "curated subset". The framing change matters for the spec text and the rationale that future contributors read.

### Out of Scope

- **Leading-digit allowance is preserved.** NCName forbids digit-first identifiers; Markdown++ aliases have always permitted them and this plan does not change that. After this change, leading-digit is the sole documented deviation from NCName.
- **Variable, condition, style, and marker-key patterns stay ASCII.** Same deferral as #108 -- those patterns share a grammar with deliberate variations and need their own audit.
- **CSS-selector escaping documentation.** A short downstream-friction note is in scope (one paragraph in `references/syntax-reference.md`), but a CSS-authoring tutorial is not.

### Deferred to Follow-Up Work

- **Audit and extend the standard-identifier and style/marker patterns to Unicode letters.** Tracked separately; will follow the same XML NCName / authoring-grammar framing established here.

---

## Key Technical Decisions

1. **`alias_name_char` becomes a direct alias of XML NCName `NameChar`.** The EBNF and PEG productions in `spec/formal-grammar.md` are rewritten to enumerate the full NCName `NameChar` extras (digit, hyphen, period, middle dot, combining marks, connector punctuation). The comment block explicitly names the one deviation (`alias_name` accepts a leading digit; NCName does not) so future readers do not have to reverse-engineer the omission.

2. **Validator and scanner regexes are extended via a new `_NCNAME_PUNCT` constant.** PR #109 already introduced `_NCNAME_COMBINING` (combining marks + connectors). The new `_NCNAME_PUNCT = ".·"` constant sits alongside it, keeping the regex assembly readable and the source-hygiene convention (literal Unicode-escaped middle dot rather than raw `·` byte) consistent with every other non-ASCII range in the module.

3. **Negative fixture `<!--#bad.alias-->` flips to positive.** This was the strongest signal that the prior grammar was not aligned with the intent. Case 16 in `sample-invalid-names.md` is rewritten to `<!--#.bad-alias-->` (leading period, still invalid). The original case is migrated to `sample-unicode-aliases.md` as positive Case U12.

4. **CSS-selector friction is documented but not avoided.** `references/syntax-reference.md` gains a short downstream-friction note explaining that aliases containing `.` require escaping in CSS selectors and `document.querySelector` calls. This is framed as a downstream stylesheet concern, not a grammar constraint, so authors can decide for themselves whether dotted aliases fit their project conventions.

5. **MDPP008 normalization is unchanged.** NFC + casefold normalization for duplicate-alias detection already runs over alias keys post-#109 and continues to apply. The `<!-- #Cáfé -->` (decomposed) vs `<!-- #Café -->` (precomposed) duplicate-detection case from #109 remains correct under the extended grammar -- both forms parse, then both normalize to NFC, then MDPP008 catches the collision.

6. **Plugin version bump is `minor` (1.7.3 → 1.8.0).** New feature in the acceptance grammar; no breaking changes (every alias valid under the post-#109 grammar remains valid).

---

## System-Wide Impact

| Surface | Change | Risk |
|---|---|---|
| `spec/specification.md` § 4.2, § 10.2, § 18.1 | Prose describing the alias `NameChar` production; valid examples expanded; MDPP002 row updated | Low -- spec text only |
| `spec/formal-grammar.md` `alias_name_char` EBNF + PEG productions | Direct alias of NCName `NameChar`; rationale comment rewritten; Case 16 row in "Constructs Rejected" updated to leading-period | Low -- specification only |
| `references/syntax-reference.md` § Alias Name | Bullet list reframed as position-dependent permissions; example tables gain `chapter.1.intro` (valid) and reframe `.hidden` (still invalid with corrected reasoning); `foo.bar` removed from invalid table; new CSS-selector friction note | Medium -- authors read this most often, so rewording must avoid implying the old rules still apply |
| `references/error-codes.md` § Naming Rule Table, § Alias Name, MDPP002 entry | Naming-rule table entry rewritten for the position-dependent permissions; MDPP002 triggering example updated to leading period; non-English content note updated for CSS-selector partial exception | Medium -- error suggestion text must accurately describe the new rule |
| `references/comment-manipulation.md` line 453-area example regex | `_NCNAME_PUNCT` added alongside `_NCNAME_COMBINING` so the example mirrors the validator's actual grammar | Low -- example regex only |
| `scripts/validate-mdpp.py` `ALIAS_NAME_RE`, MDPP002 suggestion message | `_NCNAME_PUNCT` constant added; regex extended; suggestion message updated | High -- this is the acceptance grammar; tests must cover the new behavior |
| `scripts/add-aliases.py` `ALIAS_PATTERN`, `EXISTING_ALIAS_LINE` | Mirror the validator's grammar so the scanner recognizes dotted aliases; without this, the script would silently truncate dotted aliases and could regenerate them as duplicates | High -- silent truncation is the worst failure mode |
| `scripts/test_add_aliases.py` | New tests for dotted-hierarchy capture and leading-period non-capture | Low -- new tests only |
| `tests/sample-unicode-aliases.md` | New positive cases U11-U15 (dotted hierarchy, period in non-first, connector, combining mark, middle dot); `<!--#foo.bar-->` relocated from negative to positive; rationale paragraphs added | Low -- fixture file |
| `tests/sample-invalid-names.md` Case 16 | Rewritten from `<!--#bad.alias-->` (now valid) to `<!--#.bad-alias-->` (still invalid: leading period) with corrected explanation | Low -- fixture file |
| `CHANGELOG.md` | Entry under 1.8.0 documenting MDPP002 grammar extension and NCName alignment | Low -- changelog |
| `marketplace.json`, `plugin.json` | Version bumped 1.7.3 → 1.8.0 (minor) | Low -- version bump only |

The two **High-risk** surfaces (validator regex and alias-scanner regex) ship with positive and negative test coverage in the same commit. The Medium-risk reference surfaces are caught by the document-reading conventions in `CLAUDE.md` plus the issue's success-criteria checklist.

---

## Implementation Units

### U1. Extend validator regex and MDPP002 suggestion message

**Goal:** `ALIAS_NAME_RE` in `validate-mdpp.py` accepts the full XML NCName `NameChar` production in non-first positions; MDPP002 suggestion text describes the new permissions.

**Requirements:** Issue #111 success criterion 1 (`<!-- #chapter.1.intro -->` accepted), criterion 2 (non-first combining mark / middle dot accepted), criterion 3 (`<!-- #.hidden -->` still rejected), criterion 4 (whitespace, `:`, `!`, `?` still rejected).

**Dependencies:** None.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`

**Approach:**

- Introduce `_NCNAME_PUNCT = ".·"` as a new module-level constant, mirroring the existing `_NCNAME_COMBINING` constant. Use the `·` escape rather than the literal middle-dot byte, per the source-hygiene convention applied to every other non-ASCII range in the module.
- Splice `_NCNAME_PUNCT` into the non-first character class of `ALIAS_NAME_RE` alongside `_NCNAME_COMBINING`.
- Rewrite the MDPP002 suggestion string for invalid aliases to describe the position-dependent permission set: first-position characters (NCName letter class, digit, underscore) and non-first additions (hyphen, period, middle dot, combining marks, connector punctuation).

**Patterns to follow:** Mirror the existing `_NCNAME_COMBINING` constant's docstring-style comment block explaining the source (XML NCName `NameChar`), the reason it is non-first-only, and the source-hygiene rationale for the Unicode escape.

**Test scenarios** (covered by U6):

- Validate-time: `<!-- #chapter.1.intro -->` produces no MDPP002.
- Validate-time: `<!-- #api.v1.users -->` produces no MDPP002.
- Validate-time: `<!-- #foo·bar -->` (middle dot in non-first position) produces no MDPP002.
- Validate-time: `<!-- #.hidden -->` continues to produce MDPP002.
- Validate-time: `<!-- #foo:bar -->` continues to produce MDPP002 (NCName excludes colon by construction).
- Validate-time: `<!-- #has space -->` continues to produce MDPP002.

**Verification:** Running `validate-mdpp.py` against `tests/sample-unicode-aliases.md` produces exactly two MDPP002 errors -- Case U7 (`#.hidden`) and Case U8 (`#foo:bar`) -- matching the corpus's NEGATIVE CASES section, and zero errors against any of Cases U11-U15.

---

### U2. Mirror grammar extension in `add-aliases.py` scanner regexes

**Goal:** `ALIAS_PATTERN` and `EXISTING_ALIAS_LINE` in `add-aliases.py` recognize the same alias forms the validator accepts. Without this, the scanner silently truncates dotted aliases at the first `.` (producing partial keys in `get_existing_aliases`) and `EXISTING_ALIAS_LINE` fails to detect dotted aliases as already-present, leading to regeneration and duplicates.

**Requirements:** Issue #111 success criterion "Every alias valid under the post-#109 grammar remains valid" plus the implementation-note about avoiding silent truncation by the scanner.

**Dependencies:** Should follow U1 conceptually (same grammar) but the file edits are independent.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py`

**Approach:**

- Introduce `_NCNAME_PUNCT = ".·"` matching `validate-mdpp.py`'s constant. The two scripts deliberately do not share a module (the skill scripts are standalone for easy distribution), so the constants live in both places, in sync.
- Splice `_NCNAME_PUNCT` into both `ALIAS_PATTERN` and `EXISTING_ALIAS_LINE` character classes alongside `_NCNAME_COMBINING`.
- Add a comment block to the new constant calling out the silent-truncation failure mode that motivates keeping it in sync with the validator.

**Patterns to follow:** Mirror the existing `_NCNAME_COMBINING` constant in `add-aliases.py` for shape; mirror `validate-mdpp.py`'s new constant for content.

**Test scenarios** (covered by U6):

- `get_existing_aliases("<!--#chapter.1.intro-->")` returns `{"chapter.1.intro"}` (whole-key capture, no truncation).
- `get_existing_aliases("<!--#.hidden-->")` returns `set()` (leading period correctly fails to start a capture).

**Verification:** New unit tests in `test_add_aliases.py` (U6) pass.

---

### U3. Update formal grammar productions and rejected-constructs table

**Goal:** `spec/formal-grammar.md` documents `alias_name_char` as a direct alias of XML NCName `NameChar`, with an explicit rationale block naming the one deviation (digit-first in `alias_name`). The "Constructs Rejected" verification table reflects the relocated Case 16.

**Requirements:** Issue #111 success criterion "`spec/formal-grammar.md` documents the digit-first allowance as the sole intentional deviation from NCName".

**Dependencies:** None.

**Files:**

- `spec/formal-grammar.md`

**Approach:**

- In the EBNF block: extend the `alias_name_char` right-hand side to include `"." | #xB7` alongside the existing combining-mark and connector ranges. Rewrite the comment block to (a) name the production as a direct alias of XML NCName `NameChar`, (b) call out the digit-first allowance as the one deviation, (c) preserve the existing rationale for the combining-mark range (decomposed forms accept under MDPP002; MDPP008 normalizes for duplicate detection).
- In the PEG block: same extension to the alternation, same rewritten comment.
- In the introductory prose paragraph that enumerates the three identifier forms: update the alias-name bullet to describe the non-first character class as a direct alias of NCName `NameChar` with the digit-first deviation.
- In the "Constructs Rejected" verification table: replace the Case 16 row (`<!--#bad.alias-->` -- period not in character set) with the new Case 16 (`<!--#.bad-->` -- period not permitted in first position).

**Patterns to follow:** The existing structure of the EBNF/PEG blocks and the rationale comment style established by PR #109.

**Test scenarios:** `Test expectation: none -- spec text only; production behavior is exercised by U6 fixtures against the implementation in U1/U2.`

**Verification:** Reading the formal-grammar productions in isolation, an independent implementer can construct `alias_name_char` correctly without needing to read the validator source.

---

### U4. Update specification prose and MDPP002 table

**Goal:** `spec/specification.md` describes the alias name's non-first character class as the full XML NCName `NameChar` production; valid examples and MDPP002 row are aligned.

**Requirements:** Issue #111 "Surfaces to update" -- spec § 18.1 MDPP002 triggering condition.

**Dependencies:** None.

**Files:**

- `spec/specification.md`

**Approach:**

- § 4.2 (identifier forms table and surrounding prose): expand the prose paragraph describing the alias exception to call out the full NCName `NameChar` alignment and enumerate the new non-first characters (digit, hyphen, period, middle dot, combining marks, connector punctuation).
- § 10.2 (custom alias syntax): rewrite the alias-name MUST clause to describe the position-dependent permission set; expand the valid-examples list to include `<!-- #chapter.1.intro -->` and `<!-- #api.v1.users -->`.
- § 18.1 MDPP002 row in the error-code table: update the alias clause from "XML NCName letter class plus digit-first" to "XML NCName `NameChar` end-to-end plus digit-first".

**Patterns to follow:** The existing § 10.2 prose convention of stating the production reference, then the human-readable description, then the valid examples.

**Test scenarios:** `Test expectation: none -- spec prose; production behavior is exercised by U6 fixtures.`

**Verification:** § 4.2, § 10.2, and § 18.1 each describe the same grammar; valid-examples list in § 10.2 includes at least one dotted-hierarchy form.

---

### U5. Update skill references (syntax-reference, error-codes, comment-manipulation)

**Goal:** The three skill reference documents that authors and the validator suggestion text reach for describe the new grammar correctly. The CSS-selector friction note is added once (in `syntax-reference.md`) and cross-referenced.

**Requirements:** Issue #111 "Surfaces to update" -- skill references; success criterion "`references/syntax-reference.md` reframes the alias rule statement so that `.` is described as a *position-dependent* permission rather than a flat prohibition".

**Dependencies:** None.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`

**Approach:**

- **`syntax-reference.md` § Alias Name:** Rewrite the bullet list to describe position-dependent permissions. Add `chapter.1.intro` to the valid-name examples table. Remove `foo.bar` from the invalid-name examples table (it is now valid). Reframe `.hidden`'s explanation to "Period not permitted in first position of an alias name (NCName excludes `.` from `NameStartChar`)" -- the prior wording "Period cannot start an alias name" was ambiguous about whether period was allowed elsewhere. Add a short downstream-friction note explaining that `.` in an alias requires CSS-selector escaping; frame as a downstream stylesheet concern, not a grammar constraint. In the Non-English Content section, update the HTML5-id-legal vs. NCName explanation to note that CSS selectors are a partial exception (escape needed for `.`), with the back-reference to the friction note.
- **`error-codes.md` Naming Rule Table and Alias Name:** Rewrite the alias row of the naming-rule table to describe the position-dependent permission set, citing the formal grammar. Update the Alias Name prose section similarly. In the MDPP002 entry, replace the triggering example `<!--#my.section-->` (now valid) with `<!--#.my-section-->` and add a note showing a valid dotted form. In the Suggested fix bullet for aliases, describe the new non-first permissions. In the Non-English content paragraph (mirrors syntax-reference), add the CSS-selector partial exception.
- **`comment-manipulation.md` example regex:** Add `_NCNAME_PUNCT` constant to the documented standalone-anchor regex example so it mirrors the validator's grammar.

**Patterns to follow:** Existing reference style in each file -- bullet lists for permission rules, tables for valid/invalid examples, plain-prose explanatory paragraphs.

**Test scenarios:** `Test expectation: none -- reference documentation; production behavior is exercised by U6.`

**Verification:** A new author reading `syntax-reference.md` § Alias Name learns that `.` is permitted in non-first positions and that CSS-selector escaping is a downstream concern. A reader of `error-codes.md` MDPP002 entry sees a triggering example that actually trips MDPP002 under the new grammar.

---

### U6. Update test fixtures and add scanner unit tests

**Goal:** The validator and scanner positive corpora cover the new dotted-hierarchy forms; the negative corpus retains coverage for leading-period and other always-invalid characters.

**Requirements:** Issue #111 "Tests" section.

**Dependencies:** U1, U2 (the validator and scanner must already accept the new grammar before the fixtures are flipped).

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-aliases.md`
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-invalid-names.md`
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/test_add_aliases.py`

**Approach:**

- **`sample-unicode-aliases.md`:** Update the front-matter intro to cite both #108 and #111. Add positive Cases U11-U15:
  - U11: `<!--#chapter.1.intro-->` (dotted hierarchy)
  - U12: `<!--#foo.bar-->` (relocated from former Case U6 in the negative corpus)
  - U13: `<!--#foo‿bar-->` (connector punctuation U+203F undertie; already accepted under #109, made explicit here)
  - U14: `<!--#foè-bar-->` (combining grave U+0300; already accepted under #109, made explicit here)
  - U15: `<!--#foo·bar-->` (middle dot U+00B7)
  - Each case carries a short rationale paragraph naming the relevant NCName production range.
  - The former negative Case U6 (`<!--#foo.bar-->`) is removed from the negative section; the negative section retains U7 (leading period -- `<!--#.hidden-->`) and U8 (colon -- `<!--#foo:bar-->`) with expanded rationale.
- **`sample-invalid-names.md` Case 16:** Rewrite from `<!--#bad.alias-->` to `<!--#.bad-alias-->` with a rationale paragraph explaining the flip (period now valid in non-first positions; leading period still invalid).
- **`test_add_aliases.py`:** Add two new unit tests:
  - `test_dotted_hierarchy_alias_compact`: `get_existing_aliases("<!--#chapter.1.intro-->")` returns `{"chapter.1.intro"}`.
  - `test_leading_period_alias_is_not_captured`: `get_existing_aliases("<!--#.hidden-->")` returns `set()`.

**Patterns to follow:** Existing case-numbering convention (Case U1, U2, ...) in `sample-unicode-aliases.md`; existing `unittest` patterns in `test_add_aliases.py`.

**Test scenarios:**

- Running `validate-mdpp.py` against the updated `sample-unicode-aliases.md` produces exactly two MDPP002 errors (Cases U7 and U8) and zero errors for Cases U11-U15.
- Running `validate-mdpp.py` against the updated `sample-invalid-names.md` produces an MDPP002 error for Case 16 with the leading-period context.
- Running `python -m unittest test_add_aliases.py` passes all tests including the two new ones.

**Verification:** All three commands above succeed with the expected error counts and pass/fail outcomes.

---

### U7. Update CHANGELOG and bump plugin version

**Goal:** `CHANGELOG.md` records the extension under a new minor-version entry citing MDPP002 and the NCName `NameChar` alignment; `marketplace.json` and `plugin.json` are synchronized to the new minor version.

**Requirements:** Issue #111 success criterion "`CHANGELOG.md` records the extension under the next minor-version entry, naming MDPP002 and citing the NCName `NameChar` alignment".

**Dependencies:** U1-U6 (the changelog entry should describe shipped behavior).

**Files:**

- `CHANGELOG.md`
- `.claude-plugin/marketplace.json`
- `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

**Approach:**

- Add a `## [1.8.0] - 2026-05-23` heading above the existing 1.7.3 entry.
- Under Spec: one bullet describing the alias grammar extension, naming MDPP002, citing the NCName `NameChar` alignment, the digit-first deviation, the dotted-hierarchy examples, the leading-period rejection, the spec sections updated, and the architectural framing (don't pre-filter for CSS-selector preferences).
- Under Tooling: one bullet describing the validator regex extension via `_NCNAME_PUNCT`, the scanner regex sync to avoid silent truncation, the reference-doc updates, and the test-fixture relocations.
- Run `scripts/bump-version.sh minor` (or manually edit both JSON files) to bump 1.7.3 → 1.8.0. Verify both JSONs report the same version.

**Patterns to follow:** The existing CHANGELOG entry structure (Spec / Tooling / Project subsections, issue link at end of each bullet).

**Test scenarios:** `Test expectation: none -- documentation and version metadata.`

**Verification:** `grep -E '"version"' .claude-plugin/marketplace.json plugins/markdown-plus-plus/.claude-plugin/plugin.json` reports `"1.8.0"` in both files; `CHANGELOG.md` contains a `## [1.8.0]` heading dated 2026-05-23.

---

## Verification Strategy

Run, in this order, after the implementation units land:

1. `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-aliases.md` -- expect exactly two errors (Cases U7 and U8).
2. `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-invalid-names.md` -- expect an error for Case 16 with the leading-period context.
3. `python -m unittest plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/test_add_aliases.py` -- expect all 9 tests to pass (7 existing + 2 new).
4. Grep both plugin JSON files for the new version string.
5. Re-read `references/syntax-reference.md` § Alias Name as a first-time author: the rules should describe position-dependent permissions, with `.` permitted only in non-first positions, plus an explicit CSS-selector friction note.

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Author confusion over "position-dependent" framing | Medium | Low | Three reference documents (syntax-reference, error-codes, formal-grammar) describe the rule consistently; valid and invalid examples in `syntax-reference.md` tables anchor the rule with concrete cases. |
| Scanner regex drift from validator regex (re-introducing silent truncation) | Low | High | `add-aliases.py` carries a comment in its `_NCNAME_PUNCT` constant explicitly naming the silent-truncation failure mode that motivates keeping it in sync. Future contributors who change one must change the other. The two new scanner unit tests in `test_add_aliases.py` would catch a truncation regression. |
| CSS-selector friction surprising authors who use aliases as CSS IDs | Medium | Low | The new friction note in `syntax-reference.md` calls this out; authors can choose to avoid `.` in aliases if their project uses aliases as CSS selectors directly. The format does not impose this choice. |
| MDPP008 normalization missing a new precomposed/decomposed pair | Low | Medium | NFC + casefold normalization is unchanged from PR #109; the new characters (period, middle dot) have no precomposed/decomposed variants in Unicode (they are not letters). The combining-mark cases from #109 continue to work as before. |
| Plugin version skew between `marketplace.json` and `plugin.json` | Low | Low | Use `scripts/bump-version.sh minor` rather than hand-editing; the script updates both files atomically. |

---

## Out-of-Scope Items Recorded (for the next plan to pick up)

- Variable, condition, style, and marker-key Unicode support audit (tracked under the post-#108 follow-up referenced in `CHANGELOG.md`).
- Cross-file slug normalization (MDPP014) review beyond what #109 established (no change needed for this plan).
- Best-practices guide section on "when to use dotted aliases vs. hyphenated aliases" (optional; deferred unless an author reports confusion in practice).
