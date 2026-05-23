---
title: "spec/tooling: Extend custom-alias letter class to Unicode (XML NCName NameStartChar)"
type: spec+tooling
status: active
date: 2026-05-22
origin: docs/brainstorms/2026-05-22-unicode-alias-letter-class-requirements.md
issue: 108
---

# spec/tooling: Extend custom-alias letter class to Unicode (XML NCName NameStartChar)

## Summary

Replace the custom-alias letter class `[a-zA-Z]` with the XML 1.0 NCName `NameStartChar` ranges so authors of non-English documentation can mint native-script alias identifiers (`<!-- #インストール -->`, `<!-- #Café -->`, etc.). The standard, style, and marker-key patterns stay ASCII pending a separate audit. Update MDPP002's triggering condition and prose, add alias-specific productions to the formal grammar, rewrite the syntax-reference and error-codes naming-rule surfaces, update `validate-mdpp.py` (alias acceptance + MDPP008 NFC/case-fold normalization) and `add-aliases.py` (recognition only -- slug generation stays ASCII), add a positive/negative Unicode test corpus, bump the plugin minor version, and record the change in `CHANGELOG.md`.

---

## Problem Frame

The brainstorm
([`docs/brainstorms/2026-05-22-unicode-alias-letter-class-requirements.md`](../brainstorms/2026-05-22-unicode-alias-letter-class-requirements.md))
documents a single bottleneck: MDPP002's ASCII-only alias letter class blocks non-English-language authors from minting native-script aliases, even though every surface downstream of validation (CommonMark renderers, HTML `id=` emission, the ePublisher Markdown++ adapter, Reverb 2.0/3.0 landmark resolvers) already accepts Unicode IDs. ePublisher precedent (changeset r35807) widened the same surface and explicitly named XML NCName as the basis.

The fix is a coordinated change across (a) the spec validation surface that defines the letter class, (b) the formal-grammar productions that bind it, (c) the skill reference surfaces that document it, (d) the Python validator that enforces it, (e) the alias-injection helper that recognizes it, and (f) the test corpus that exercises it. The new grammar is a strict superset of today's -- every existing valid alias remains valid.

---

## Requirements

Carried forward verbatim from the brainstorm. The plan does not introduce new requirements; it sequences and operationalizes the brainstorm's R1-R19.

- R1. `spec/specification.md` § 18.1 MDPP002 row updated; standard/style/marker patterns stay ASCII.
- R2. `spec/formal-grammar.md` adds `alias_name_start_char` and `alias_name_char` productions citing XML NCName; the existing `letter` production keeps its ASCII definition and its comment is updated to record that the alias case is resolved while standard/style remain deferred; `alias_name` production rewrites to use the new productions.
- R3. `formal-grammar.md` regex summary (line 98) and PEG grammar (line 421) updated to match.
- R4. Strict-superset preservation: every alias name accepted by the old pattern remains accepted.
- R5. `references/syntax-reference.md` § Alias Name rewritten; § Non-English Content rewritten to describe what is supported (aliases) versus deferred (standard/style/marker).
- R6. `references/error-codes.md` § Naming Rule table + § Alias Name subsection + the trailing "For non-English content..." paragraph rewritten; MDPP002 entry's prose updated; MDPP008 entry's detection-logic prose updated to reflect normalization.
- R7. `references/comment-manipulation.md` standalone-anchor example regex (line 453) updated, or annotated as a deliberately-ASCII illustration with a pointer to the canonical pattern.
- R8. Verification scan of `SKILL.md`, `spec/whitepaper.md`, `spec/processing-model.md`, `spec/element-interactions.md` for any alias-pattern citation. The Plan's *Verification Scan Results* subsection records that no such occurrences require editing.
- R9. `validate-mdpp.py` `ALIAS_NAME_RE` (line 76) rebuilt as an explicit character class spelled from XML 1.0 NCName productions. `\w` is not used.
- R10. `validate-mdpp.py` MDPP002 alias message/suggestion updated to describe the broader class without becoming unwieldy.
- R11. `validate-mdpp.py` MDPP008 duplicate-alias check compares aliases under Unicode NFC + case-fold normalization.
- R12. **Resolved by planning verification.** MDPP014 is NOT implemented in the current `validate-mdpp.py` (grep for `MDPP014` returns no match in the script). The validator's MDPP014 surface does not exist, so MDPP014 normalization is out of scope for this issue. The plan records this under *Verification Scan Results*; the inconsistency between the spec (which defines MDPP014) and the validator (which does not yet enforce it) predates this issue and is not in scope.
- R13. `add-aliases.py` `ALIAS_PATTERN` (line 41) and `EXISTING_ALIAS_LINE` (line 42) updated to recognize Unicode-letter aliases. `slugify()` (line 45-65) is intentionally NOT updated -- slug *generation* stays ASCII-only per the brainstorm's *Scope Boundaries*; only alias *recognition* is extended.
- R14. Positive Unicode test samples per major script -- Japanese, German with combining accent, Greek, Cyrillic.
- R15. Negative samples that MUST still fail MDPP002: whitespace inside alias, alias containing punctuation outside `-_`, alias starting with `.`.
- R16. At least one positive sample exercises MDPP008 normalization: NFC-different but canonical-equivalent forms flagged as duplicates.
- R17. `CHANGELOG.md` entry under the next minor-version release (1.7.0).
- R18. Follow-up GitHub issue filed for extending Unicode-letter support to variable, condition, style, and marker-key patterns; the follow-up issue's number and link recorded in the changelog entry. Per `CLAUDE.md`, the windworker handles issue creation -- the plan records the follow-up's intended scope so the engineering phase can file it.
- R19. Plugin version bumped via `scripts/bump-version.sh minor` (1.6.3 → 1.7.0).

---

## Scope Boundaries

- **Variable, condition, style, and marker-key patterns stay ASCII.** Out of scope; deferred to the follow-up issue (R18). The brainstorm's *Scope Boundaries* names this as a deliberate decision with its own audit shape.
- **NCName `NameChar` extras (`.`, middle dot `#xB7`, combining marks `#x0300-#x036F`, `#x203F-#x2040`) stay excluded.** Only the letter class extends. Non-first-position `.` and combining-mark allowances are a separate scoping decision.
- **HTML5 `id` superset stays excluded.** NCName is a subset of HTML-ID-legal; widening to the HTML5 superset (which permits punctuation and symbols) is out of scope.
- **Heading-alias auto-generation algorithm (`spec/element-interactions.md` § Heading Alias Auto-Generation, lines 199-210) is unchanged.** The custom-alias path and the auto-generated-alias path remain deliberately decoupled. Whether to flip auto-generation's "MAY extend to Unicode" to "MUST" stays a deferred question for the follow-up audit. The plan touches this section ONLY for verification (R8) -- no edits.
- **`slugify()` in `add-aliases.py` stays ASCII-only for generation.** R13 updates only the *recognition* regexes (`ALIAS_PATTERN`, `EXISTING_ALIAS_LINE`). Whether to extend slug generation to Unicode is a follow-up question.
- **No third-party `regex` dependency.** Stdlib `re` with an explicit character-class string built from XML 1.0 NCName productions. The brainstorm explicitly rejected `\w`-based shortcuts and the third-party `regex` package.
- **MDPP014 normalization stays out of scope.** Verified during planning that the current `validate-mdpp.py` does not implement MDPP014; the validator-vs-spec gap predates this issue. R11 covers MDPP008 only.
- **No retrofit of existing alias values in `examples/` or `tests/`.** Today's ASCII aliases remain unchanged. Strict-superset preservation (R4) makes this load-bearing -- nothing breaks.

---

## Context & Research

### Verification Scan Results

The brainstorm flagged several surfaces as "needs verification during planning." Results:

- **`SKILL.md`** -- `grep "a-zA-Z"` returns no matches. No alias-pattern citation exists in the skill prompt. No edit required (the existing references to `references/syntax-reference.md#naming-rules` and `GLOSSARY.md#triple` are sufficient pointers; they pick up the new grammar automatically once the destination surface is rewritten).
- **`spec/whitepaper.md`** -- `grep "a-zA-Z"` returns no matches. No alias-pattern citation. No edit required.
- **`spec/processing-model.md`** -- two `a-zA-Z` matches, both restating the standard identifier pattern for variable names (lines 22 and 316). Neither cites the alias pattern. No edit required.
- **`spec/element-interactions.md`** -- one `a-zA-Z` match (line 551) restating the style/marker pattern in the *Compound Names and Identifier Validation* subsection. No alias citation. No edit required. The Heading Alias Auto-Generation algorithm (lines 199-210) references "ASCII letters (a-z)" but is explicitly out of scope per *Scope Boundaries*.
- **`validate-mdpp.py` MDPP014** -- `grep "MDPP014"` in the script returns no match. The validator does not implement MDPP014 today. R12 is resolved: MDPP014 normalization stays out of scope.
- **`references/error-codes.md` alias-pattern occurrences** -- six `a-zA-Z` matches: the Quick Reference table row (line 22 -- entity-agnostic prose, no edit needed), the *Naming Rule* table at line 44, the *Alias Name* subsection at line 61, the trailing non-English paragraph at line 76, the MDPP002 *Detection logic* at line 149, and the MDPP002 *Suggested fix* at line 182. All six are in scope for U4.
- **`references/comment-manipulation.md` line 453 context** -- the surrounding text frames the snippet as "Standalone anchor" with companion-logic checklists for production cleanup tooling. The brainstorm flagged this as "authoritative pattern or illustrative example?" -- resolved by planning: the surrounding prose describes the pattern as for "production cleanup tooling," so it is authoritative for downstream agents. U5 updates the pattern to reflect the new grammar with a single anchored note pointing readers to the canonical syntax-reference surface.

### Relevant Code and Patterns

- **Validator regex line 76**: `ALIAS_NAME_RE = re.compile(r'^[a-zA-Z0-9_][a-zA-Z0-9_-]*$')`. U6 replaces this with an explicit NCName-derived character class spelled in Python `\u`/`\U` escapes.
- **Validator alias-extraction pattern line 65**: `'alias': re.compile(r'<!--\s*#([^\s;>]+?)(?=\s*;|\s*-->)')`. Already permissive (negative class `[^\s;>]+`), so it extracts Unicode aliases unchanged. The bottleneck is the post-extraction `validate_alias_name()` check (line 93) which calls `ALIAS_NAME_RE.match()`. Only `ALIAS_NAME_RE` needs editing; the extraction pattern is unchanged.
- **Validator MDPP008 line 392-403**: `if alias_name in alias_locations: ...` -- byte-exact comparison. U6 introduces an `_alias_key(name)` helper that returns `unicodedata.normalize('NFC', name).casefold()` and changes both the storage key and the lookup to use the helper. The dictionary still stores the original alias name as the *display* value (for error messages) but is keyed by the normalized form.
- **`add-aliases.py` recognition line 41**: `ALIAS_PATTERN = re.compile(r'<!--\s*#([a-zA-Z0-9_-]+)')`. The capture group has the ASCII class. U7 rebuilds this with the NCName-derived character class.
- **`add-aliases.py` recognition line 42**: `EXISTING_ALIAS_LINE = re.compile(r'^<!--\s*#[a-zA-Z0-9_-]+.*-->\s*$')`. Same ASCII class. U7 rebuilds.
- **`add-aliases.py` slug generation line 57**: `text = re.sub(r'[^a-z0-9]+', '-', text)`. ASCII-only. U7 does NOT touch this -- slug generation stays ASCII per *Scope Boundaries*. The result: a Japanese heading still gets no auto-generated slug from `add-aliases.py`, but if a custom Unicode alias already exists on a sibling heading, `add-aliases.py` will now see it and avoid generating a colliding ASCII slug.
- **Spec MDPP002 triggering condition** in `spec/specification.md` line 1237 -- the cell that today reads `[a-zA-Z0-9_][a-zA-Z0-9_-]*` for the alias variant. U1 rewrites this cell to cite the NCName-derived form.
- **Spec § 4.2 Naming Rules table** in `spec/specification.md` line 163. U1 rewrites the alias row.
- **Spec § 10.2 alias-name MUST** in `spec/specification.md` line 483. U1 rewrites the regex citation in that paragraph.
- **Spec § 17.3.1 cross-reference pattern** in `spec/specification.md` line 1217. The prose "The alias `sh-ug-installation` satisfies the alias-name rule enforced by **MDPP002** (`[a-zA-Z0-9_][a-zA-Z0-9_-]*`)" contains an alias-pattern citation. U1 rewrites the parenthetical to point to the new grammar.
- **Formal grammar `letter` production** at `spec/formal-grammar.md` line 55-57. The "Future versions may extend to Unicode Letter categories for non-English identifier support" comment is updated by U2 to record that the alias case is now resolved while standard/style stay deferred.
- **Formal grammar `alias_name` production** at line 91. U2 rewrites in terms of the new `alias_name_start_char` / `alias_name_char` productions.
- **Formal grammar regex summary** at line 98. U2 rewrites the alias-name sentence to reference the NCName form.
- **Formal grammar PEG `alias_name`** at line 421. U2 rewrites; the explicit PEG character ranges are spelled in the same form as the EBNF.
- **`scripts/bump-version.sh`** -- standard tooling per `CLAUDE.md` § Version Management. U10 invokes it as `scripts/bump-version.sh minor`. Current `1.6.3` → target `1.7.0`. Both `plugin.json` and `marketplace.json` update in lockstep.
- **`CHANGELOG.md` entry shape** -- a Tooling/Spec multi-bullet entry. The 1.6.3 entry (lines 16-20) is a single-bullet aggregate; the 1.5.0 entry (lines 40-57) is multi-section. U10 uses the multi-section form since this change touches both Spec (specification, formal grammar) and Tooling (validator, add-aliases, syntax-reference, error-codes, tests).

### Institutional Learnings

- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` -- when the three naming patterns are restated across surfaces, drift between surfaces is a recurring failure mode. The plan's per-unit checklist for U1, U3, U4 verifies that every surface restating any portion of the alias regex updates in lockstep.
- `docs/solutions/documentation-gaps/error-codes-naming-rule-three-pattern-gap-2026-04-11.md` -- `references/error-codes.md` historically lagged behind `references/syntax-reference.md` on the three-pattern split. U3 and U4 land in the same PR so the two surfaces stay synchronized.
- `docs/solutions/conventions/normative-rules-against-competing-conventions-2026-05-18.md` -- when Markdown++ defines a stricter version of a parent-format convention (NCName as a stricter version of HTML5-ID-legal), the doc surface should name the parent convention and explain why the stricter version applies. U3's *Non-English Content* rewrite includes a sentence naming HTML5-ID-legal as the runtime safety bar and NCName as the authoring grammar.

### External References

- **XML 1.0 NCName specification** -- https://www.w3.org/TR/REC-xml-names/#NT-NCName -- the formal grammar definition cited by U2's new productions.
- **Unicode NFC and case-fold algorithms** -- Python `unicodedata.normalize('NFC', s)` and `str.casefold()` per Python 3.8+ stdlib. No external library required.
- **CommonMark 0.30 link-reference-definition slug matching** -- the brainstorm cites this as the precedent for NFC + case-fold normalization. U6 implements the same equivalence for MDPP008.
- **ePublisher Platform changeset r35807** -- referenced in the issue body, not in this repo. The new productions cite XML NCName by name (the changeset's framing); no link to changeset r35807 lives in the spec or skill text (it is a development artifact in a private repo).

---

## Key Technical Decisions

- **Letter-class basis: XML 1.0 NCName `NameStartChar`.** Locked by the brainstorm. The plan's job is to spell the ranges identically across U1 (spec table), U2 (formal grammar EBNF and PEG), U3 (syntax-reference), and U6 (validator Python source). To prevent drift, the plan establishes a **single canonical character-class string** that every surface re-states. The canonical form is the issue body's listing:

  ```
  "_" | [A-Z] | [a-z] | [#xC0-#xD6] | [#xD8-#xF6] | [#xF8-#x2FF] |
  [#x370-#x37D] | [#x37F-#x1FFF] | [#x200C-#x200D] | [#x2070-#x218F] |
  [#x2C00-#x2FEF] | [#x3001-#xD7FF] | [#xF900-#xFDCF] |
  [#xFDF0-#xFFFD] | [#x10000-#xEFFFF]
  ```

  Every surface uses this same enumeration. The validator's Python string is the same ranges spelled with `\u` and `\U` escapes (see U6 details).

- **Validator implementation: explicit Python character class, no `\w`.** Per brainstorm. The Python ALIAS_NAME_RE is built by string-concatenating a module-level `_NCNAME_START_CHAR` constant. The constant is defined once and reused. This avoids `\w`-based shortcuts (which would conflate letters with digits) and avoids the third-party `regex` package.

- **MDPP008 normalization: NFC + casefold, applied as the dictionary key.** The plan implements this by introducing a helper `_alias_dedup_key(name: str) -> str` that returns `unicodedata.normalize('NFC', name).casefold()`. The `alias_locations` dictionary is keyed by the helper's return value; the *value* stored is `(line_num, original_name)` so error messages show the user-authored form. Both occurrences of the alias (the first definition and the duplicate detection site) call the helper.

- **Cross-validator helper consolidation.** The helper is `_alias_dedup_key()` rather than a generic `_normalize()` because the same casefold/NFC combination is not yet applied elsewhere. Naming it specifically signals that it is an MDPP008-scoped helper; if a future MDPP014 implementation lands, that PR can rename or generalize.

- **Validator MDPP002 alias message wording.** Per brainstorm R10, planning chooses between *enumerate-the-ranges* (precise, unwieldy) and *describe-the-class* (terse, useful). The plan defaults to descriptive prose: `"Alias names may use letters in any script (XML NCName letter class), digits, underscore (_), and hyphen (-). Letters and digits are permitted in any position; hyphen is permitted only in non-first positions; other punctuation is not permitted."` The suggestion string mirrors the description without restating the regex.

- **Anchor in `comment-manipulation.md` -- update the pattern + add a note.** Per *Verification Scan Results*, the surrounding prose frames the snippet as authoritative for production tooling. The plan updates the regex inline (spelling the NCName character class) and adds a one-line note linking to `references/syntax-reference.md#alias-name` as the canonical surface. The updated regex is spelled compactly (using `\u` escapes) to keep the snippet readable.

- **Test corpus placement: new file `tests/sample-unicode-aliases.md`.** Per the brainstorm's *Integration Notes*, planning chooses placement. A single new specimen file holds all four positive script samples (Japanese, German with combining accent, Greek, Cyrillic) and the new negative cases (whitespace inside alias, leading `.`, additional punctuation that is not already covered by the existing `#bad.alias` case in `sample-invalid-names.md`). The MDPP008 normalization sample (NFC-different but canonical-equivalent) lives in a new file `tests/sample-unicode-duplicate-aliases.md` rather than in the existing `sample-duplicate-aliases.md`, because the existing file's expected behavior is byte-exact duplicate detection and mixing in normalization-equivalent cases would obscure either test's intent. This is a planning-time judgment call; an implementer may consolidate the two files into one if the resulting layout is clearer.

- **Verification scan for "Non-English Content" wording symmetry.** R5 (syntax-reference) and R6 (error-codes) both rewrite paragraphs that hedge identically on UTF-8 letter support. The plan requires the two surfaces to read consistently after the change: both name what is supported (aliases under NCName), what is deferred (variable, condition, style, marker-key patterns), and link to the follow-up issue.

- **Order of operations across units.** U1 and U2 (spec surfaces) land first because U3, U4, U5, U6, U7 reference them. U6 (validator) lands before U8 (tests) so the test corpus can be run against the updated validator immediately. U10 (changelog + version bump) lands last in the commit set per `CLAUDE.md` § Version Management.

- **Follow-up issue scope.** R18 names the follow-up's scope: extending NCName-derived letter classes to the standard identifier pattern (variables, conditions) and to the style/marker pattern. The follow-up should audit the same five concerns (round-tripping in XML/XSLT/JS/URL/CSS, downstream emitter behavior, normalization semantics, test corpus, version bump). The follow-up is referenced by issue number in U10's changelog entry; if the issue is filed during the engineering phase, the changelog entry is written with the number; if not, the changelog entry uses a placeholder that the windworker resolves on PR creation.

---

## Open Questions

### Resolved During Planning

- **R12: Does `validate-mdpp.py` implement MDPP014?** Resolved: no (grep returns no matches in the script). MDPP014 normalization stays out of scope.
- **R7 framing: Is `comment-manipulation.md` line 453 authoritative or illustrative?** Resolved: authoritative for production cleanup tooling per the surrounding "production cleanup tooling must also..." prose. Update the regex and link to the canonical syntax-reference surface.
- **R8: Do `SKILL.md`, `whitepaper.md`, `processing-model.md`, or `element-interactions.md` cite the alias pattern?** Resolved: no. No edits required to those surfaces in this PR. (Element-interactions § Heading Alias Auto-Generation references ASCII-only behavior but is explicitly out of scope.)
- **Test-corpus placement**: Resolved: new files `tests/sample-unicode-aliases.md` (positive + negative) and `tests/sample-unicode-duplicate-aliases.md` (MDPP008 normalization). Avoids mixing intent with the existing `sample-invalid-names.md` and `sample-duplicate-aliases.md`.

### Deferred to Implementation

- **Exact wording of the MDPP002 alias message string.** Plan defaults to the descriptive form (see *Key Technical Decisions*); implementer may shorten if the error reads better in a terminal. The constraint is that the message MUST NOT restate the full character class enumeration (too long for stderr).
- **Multi-section vs. single-bullet `CHANGELOG.md` entry.** Plan defaults to multi-section (Spec + Tooling) since the change touches both. Implementer may consolidate to a single bullet if the entry reads naturally that way.
- **Whether to file the follow-up issue (R18) during this PR or after merge.** Plan defaults to "during" so the changelog entry can cite the issue number. If the windworker dispatches this issue before the follow-up is filed, the changelog entry uses a placeholder (`[#XXX]`) that the engineering phase resolves.
- **PEG-rule formatting for the alias character class.** EBNF spelling (W3C `#xHHHH` form) and PEG spelling (typically `\uHHHH`-style) differ across PEG tool conventions. The PEG section in `formal-grammar.md` currently uses ASCII-only character classes `[a-zA-Z0-9_-]`. U2 chooses between (a) spelling the PEG ranges in the same W3C `#x...` form as the EBNF (uniform reading), or (b) using PEG-conventional `\u` escapes (matches typical PEG-tool input). Plan recommends (a) for surface symmetry with the EBNF; implementer may switch to (b) if the resulting PEG reads more naturally for tool-implementer audiences.

---

## Implementation Units

### U1. Update spec/specification.md alias-pattern citations

**Goal:** Three citations of the old alias regex in the canonical specification become citations of the new NCName-derived form. The Naming Rules table, the § 10.2 normative requirement, the § 17.3.1 cross-reference example, and the § 18.1 MDPP002 triggering condition row all update in lockstep.

**Files:** `spec/specification.md`.

**Changes:**

- Line 163 (Naming Rules table, alias row): change `[a-zA-Z0-9_][a-zA-Z0-9_-]*` to the NCName-derived form. Use the form `[NCName-letter | "_" | digit][NCName-letter | "_" | digit | "-"]*` in the table cell, with a footnote or trailing pointer to the formal-grammar productions for the full enumeration. The table cell stays compact; the full enumeration lives in `formal-grammar.md`.
- Line 483 (§ 10.2 alias normative): rewrite the sentence "The alias name MUST match the alias name pattern: `[a-zA-Z0-9_][a-zA-Z0-9_-]*`" to reference the formal-grammar `alias_name` production by name, citing the NCName basis.
- Line 1217 (§ 17.3.1 cross-reference paragraph): the parenthetical `(`[a-zA-Z0-9_][a-zA-Z0-9_-]*`)` becomes a forward reference to the alias-name rule defined in `formal-grammar.md`. The body of the paragraph reads naturally either way; the alias example `sh-ug-installation` is still valid under the new grammar (it is pure ASCII).
- Line 1237 (§ 18.1 MDPP002 row, Triggering Condition cell): the cell currently reads `Name violates `[a-zA-Z_][a-zA-Z0-9_-]*` (standard), `[a-zA-Z0-9_][a-zA-Z0-9_-]*` (alias), or `[a-zA-Z_][a-zA-Z0-9_ -]*` trimmed (style/marker)`. Rewrite so the standard and style/marker forms stay ASCII (verbatim), and the alias form references the formal-grammar `alias_name` production. The cell stays terse; the formal grammar carries the enumeration.

**Acceptance:**

- The four updated locations no longer state `[a-zA-Z0-9_]` for aliases.
- The standard and style/marker forms in line 163, line 1237, and elsewhere are unchanged.
- Every existing ASCII alias in this file's examples (`#sh-ug-installation`, `#04499224`, `#316492`, etc.) is still described as valid under the new grammar.

---

### U2. Update spec/formal-grammar.md productions and PEG

**Goal:** The formal grammar gets the alias-specific productions that the rest of the spec references by name. The shared `letter` production keeps its ASCII definition; only the alias case extends.

**Files:** `spec/formal-grammar.md`.

**Changes:**

- Line 55-57 (`letter` production comment): the comment `/* ASCII letters. Future versions may extend to Unicode Letter categories for non-English identifier support. */` becomes `/* ASCII letters. Extended to XML 1.0 NCName NameStartChar for aliases only (see alias_name_start_char). Standard and style/marker patterns remain ASCII pending a separate audit (issue #XXX). */`. The "issue #XXX" placeholder is replaced by the follow-up issue number during engineering.
- After line 57, add two new lexical productions defining `alias_name_start_char` and `alias_name_char`. The productions enumerate the XML 1.0 NCName ranges verbatim (the canonical character-class string from *Key Technical Decisions*). Format:

  ```ebnf
  alias_name_start_char ::= "_" | [A-Z] | [a-z]
                          | [#xC0-#xD6] | [#xD8-#xF6] | [#xF8-#x2FF]
                          | [#x370-#x37D] | [#x37F-#x1FFF]
                          | [#x200C-#x200D] | [#x2070-#x218F]
                          | [#x2C00-#x2FEF] | [#x3001-#xD7FF]
                          | [#xF900-#xFDCF] | [#xFDF0-#xFFFD]
                          | [#x10000-#xEFFFF]
                            /* XML 1.0 NCName NameStartChar letter ranges.
                               Aliases also permit a leading digit (see alias_name). */

  alias_name_char       ::= alias_name_start_char | digit | "-"
  ```

- Line 91 (`alias_name` production): rewrite as `alias_name ::= (alias_name_start_char | digit) (alias_name_char)*`. The previous form `(letter | digit | "_") (letter | digit | "-" | "_")*` is replaced.
- Line 98 (regex summary): the alias-name sentence becomes `The alias name corresponds to the explicit character class defined by `alias_name_start_char` and `alias_name_char` above; see the production definitions for the complete enumeration. The standard identifier corresponds to the regex `[a-zA-Z_][a-zA-Z0-9_\-]*`. The style name corresponds to the regex `[a-zA-Z_][a-zA-Z0-9_\- ]*` applied after trimming.`
- Line 100 (Rationale paragraph): no text change required; the rationale (digit-first permitted for numeric CMS IDs) still applies.
- Line 421 (PEG `alias_name`): rewrite to mirror the EBNF. The PEG form spells the character ranges using the W3C `#xHHHH` notation for surface symmetry with the EBNF (per *Open Questions* implementation default). If the implementer chooses (b) `\u` escapes, the layout follows PEG-conventional notation. Either way, the production count remains one (the PEG keeps `alias_name` as a single line referencing inline ranges, or splits into `alias_name`, `alias_name_start_char`, `alias_name_char` if the inline form exceeds reasonable line length).
- Lines 502-509 (*Constructs Rejected* table): no edits to existing rows. The existing row for `<!--#-bad-start-->` (hyphen-first) and `<!--#bad.alias-->` (period not in character class) remain valid rejections under the new grammar.

**Acceptance:**

- Two new productions exist in `formal-grammar.md`.
- `alias_name` references them.
- The regex summary at line 98 no longer states `[a-zA-Z0-9_][a-zA-Z0-9_\-]*` for the alias form.
- The PEG alias_name production updates in lockstep.
- The existing *Constructs Accepted* and *Constructs Rejected* tables remain valid -- no row needs to flip categories.

---

### U3. Update references/syntax-reference.md naming-rules surface

**Goal:** The skill's prose surface for naming rules documents the new alias grammar and rewrites the *Non-English Content* note to describe what is supported (aliases) versus deferred (others). The standard and style/marker subsections stay verbatim.

**Files:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`.

**Changes:**

- Lines 186-192 (*Alias Name* subsection): rewrite. The new body reads:

  > Alias names use the XML 1.0 NCName `NameStartChar` letter class -- which includes ASCII letters and letters from non-Latin scripts (Japanese, German with combining accents, Greek, Cyrillic, and others) -- plus digits, underscore, and hyphen. Aliases additionally permit a leading digit, since aliases often map to numeric identifiers (e.g., `<!-- #04499224 -->`).
  >
  > See [`spec/formal-grammar.md`](../../../../../spec/formal-grammar.md) `alias_name_start_char` and `alias_name_char` productions for the complete character enumeration. The alias namespace is a strict superset of the prior ASCII-only grammar -- every alias valid under the previous grammar remains valid.
  >
  > **Applies to:** Aliases

  (The relative-path link target is the same form used elsewhere in this file; verify the depth at implementation time.)

- Lines 207-223 (*Valid Name Examples* table): add three new rows -- `<!-- #インストール -->`, `<!-- #установка -->`, `<!-- #Café -->` (precomposed `é`) -- with the "Why Valid" column reading "Japanese alias (NCName letter class)", "Cyrillic alias (NCName letter class)", "German alias with accent (NCName letter class)".
- Lines 225-233 (*Invalid Name Examples* table): add two rows -- `<!-- #foo.bar -->` ("Period not in alias character class -- aliases permit only `-` and `_` punctuation"), `<!-- #.hidden -->` ("Period cannot start an alias name"). The existing `has space`, `special!char` etc. rows are unaffected; they document the cross-cutting whitespace and punctuation prohibitions.
- Lines 235-237 (*Non-English Content* subsection): rewrite. New body:

  > **Aliases:** Alias names accept Unicode letters from non-Latin scripts via the XML 1.0 NCName letter class (see *Alias Name* above). Authors writing Japanese, German, Greek, Cyrillic, or other non-English documentation can use native-script identifiers for alias anchors.
  >
  > **Variables, conditions, styles, and marker keys:** These four naming patterns currently accept ASCII letters only (`a-zA-Z`). Extension to Unicode letters is a separate audit tracked in [issue #XXX]. Authors with non-ASCII identifier requirements for these entities should track that issue.
  >
  > **HTML5-id-legal vs. NCName:** HTML5 `id` attributes permit any non-whitespace character, but Markdown++ aliases follow the stricter NCName grammar so an alias round-trips cleanly across XML, XSLT, JavaScript, URL fragments, and CSS selectors. Every valid alias lands cleanly in HTML `id=` output.

  The "issue #XXX" placeholder resolves to the R18 follow-up issue number.

**Acceptance:**

- *Alias Name* subsection no longer cites `[a-zA-Z0-9_][a-zA-Z0-9_-]*`.
- *Non-English Content* subsection no longer reads "UTF-8 letter support is a future goal."
- Positive examples (Japanese, Cyrillic, German precomposed) appear in the Valid table.
- Negative examples (`#foo.bar`, `#.hidden`) appear in the Invalid table.

---

### U4. Update references/error-codes.md

**Goal:** The error-codes reference's naming-rule surface and the MDPP002/MDPP008 entries reflect the new grammar and the MDPP008 normalization update.

**Files:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`.

**Changes:**

- Line 44 (*Naming Rule* table, alias row): replace `^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$` with a citation of the `alias_name` production from `spec/formal-grammar.md`, mirroring U1's line-163 treatment in `specification.md`. Keep the row compact; the full enumeration is in formal-grammar.
- Lines 57-63 (*Alias Name* subsection): rewrite to match U3's *Alias Name* subsection wording, framed for the error-codes audience (validator implementer). Mention NCName-letter-class membership and the strict-superset preservation guarantee.
- Line 76 (trailing non-English note): rewrite to mirror U3's *Non-English Content* subsection (aliases supported, standard/style/marker deferred, NCName-vs-HTML5-id rationale).
- Lines 145-152 (MDPP002 *Detection logic* bullets): the *Alias names* bullet currently reads `Alias names: The name in <!--#name--> (alias rule -- digit-first allowed)`. Update parenthetical to `(alias rule -- digit-first allowed; XML NCName letter class extends to non-ASCII scripts)`.
- Line 168 (trigger example block): the comment `<!-- NOTE: alias may start with a digit -- digit-first is valid for aliases -->` gets an additional example after it: a Japanese, Greek, or Cyrillic alias annotated as `<!-- NOTE: aliases accept Unicode letters from non-Latin scripts (XML NCName letter class) -->`.
- Lines 179-184 (*Suggested fix* paragraph): the *Aliases* bullet currently reads `Aliases (alias rule): Same as standard, but may also start with a digit.`. Update to `Aliases (alias rule): Permit letters from any script (XML NCName letter class), digits, underscores, and hyphens. Aliases may start with a digit. Subsequent characters may include hyphen in addition to the start-character set.`
- Lines 282-298 (MDPP008 entry): the *Detection logic* paragraph currently reads "A dictionary tracks alias names to their first-seen line number. When an alias is encountered, it is looked up in the dictionary." Update to: "A dictionary tracks aliases to their first-seen line number, keyed by a normalized form -- Unicode NFC followed by case-fold -- so canonical-equivalent variants (precomposed vs. decomposed accented letters; uppercase vs. lowercase) are detected as duplicates. When an alias is encountered, it is normalized and looked up." Add a new *Trigger examples* entry showing two aliases on different headings that are NFC-different (precomposed `Café` vs decomposed `Café`) and are flagged.

**Acceptance:**

- The Naming Rule table's alias row no longer cites the ASCII-only regex.
- The Alias Name subsection no longer cites `^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$`.
- The trailing non-English paragraph no longer hedges identically with `syntax-reference.md` -- both now describe what is supported vs deferred.
- The MDPP002 entry describes the new alias class.
- The MDPP008 entry describes the NFC + casefold normalization.

---

### U5. Update references/comment-manipulation.md anchor-extraction example

**Goal:** The standalone-anchor example regex used by production cleanup tooling reflects the new grammar; a one-line note directs readers to the canonical surface for the full enumeration.

**Files:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`.

**Changes:**

- Line 453 (standalone anchor regex):  change `r'<!--\s*(#[a-zA-Z0-9_-]+)\s*-->'` to a Unicode-aware form. Two acceptable shapes per *Open Questions*: (a) the explicit `\u` enumeration in the same form U6's `_NCNAME_START_CHAR` constant uses, or (b) a Python `\w`-with-`re.UNICODE` form -- the plan defaults to (a) for surface symmetry with the validator, and because `\w` permits underscore + digits which already match this pattern but would also pull in characters NCName excludes. Implementer chooses based on snippet readability.
- Immediately after the updated snippet (before line 456), add a one-sentence note: "Aliases follow the XML NCName-derived letter class defined in [`references/syntax-reference.md`](syntax-reference.md#alias-name); update both this pattern and any downstream tooling in lockstep when the grammar changes." The existing "Companion logic must verify..." paragraph at line 456 is unchanged.

**Acceptance:**

- The standalone-anchor regex no longer hardcodes `[a-zA-Z0-9_-]`.
- A pointer to the canonical syntax-reference surface accompanies the snippet.

---

### U6. Update validate-mdpp.py: alias acceptance and MDPP008 normalization

**Goal:** The validator accepts Unicode-letter aliases (MDPP002 no longer fires for valid NCName-letter forms) and the MDPP008 duplicate-alias check compares aliases under Unicode NFC + casefold.

**Files:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`.

**Changes:**

- Add `import unicodedata` near the existing imports (line 23-28 block).
- Add a module-level constant near line 73:

  ```python
  # XML 1.0 NCName NameStartChar letter ranges (issue #108).
  # See spec/formal-grammar.md alias_name_start_char production.
  _NCNAME_START_CHAR = (
      "_A-Za-z"
      "À-ÖØ-öø-˿"
      "Ͱ-ͽͿ-῿"
      "‌‍"
      "⁰-↏"
      "Ⰰ-⿯"
      "、-퟿"
      "豈-﷏"
      "ﷰ-�"
      "\U00010000-\U000EFFFF"
  )
  ```

- Line 76: rewrite `ALIAS_NAME_RE` to use the new character class:

  ```python
  ALIAS_NAME_RE = re.compile(
      f'^[{_NCNAME_START_CHAR}0-9][{_NCNAME_START_CHAR}0-9-]*$'
  )
  ```

  `STANDARD_NAME_RE` (line 75) and `STYLE_NAME_RE` (line 77) are unchanged -- ASCII per *Scope Boundaries*.

- After line 95 (after `validate_alias_name`), add the dedup-key helper:

  ```python
  def _alias_dedup_key(name: str) -> str:
      """Normalization key for MDPP008 duplicate detection.

      Applies Unicode NFC + casefold so canonical-equivalent variants
      (precomposed vs. decomposed accents; upper vs. lower case) compare
      equal. Matches the equivalence relation used by CommonMark 0.30's
      link-reference-definition slug matching.
      """
      return unicodedata.normalize('NFC', name).casefold()
  ```

- Line 228 (alias_locations dict declaration): keep the dictionary's type as `dict[str, int]`. The KEY changes to the normalized form; the VALUE remains the first-seen line number. Add an additional dict `alias_display: dict[str, str]` mapping the normalized key to the *original* alias text for error message display:

  ```python
  alias_locations: dict[str, int] = {}      # normalized alias key -> first line number
  alias_display: dict[str, str] = {}        # normalized alias key -> original alias text (display)
  ```

- Lines 380-405 (alias-check block): update to use the normalization helper. The MDPP002 invalid-name check (lines 382-391) compares the *raw* alias against `ALIAS_NAME_RE` and is unchanged (the regex now accepts Unicode). The MDPP008 duplicate-check (lines 392-403) compares using `_alias_dedup_key(alias_name)` as the dictionary key. When emitting MDPP008, the message includes the original alias text via `alias_name`, and the "first defined on line X" suggestion references the original definition via `alias_display[key]` if the canonical form differs from the new raw form (e.g., one heading uses precomposed Café, another uses decomposed Café -- the message should help the author see the discrepancy). The MDPP008 message wording becomes:

  ```python
  message=(
      f"Duplicate alias: #{alias_name} "
      f"(matches #{alias_display[key]} under Unicode NFC + case-fold normalization)"
      if alias_display[key] != alias_name
      else f"Duplicate alias: #{alias_name}"
  )
  ```

  -- alternatively, the implementer may use a fixed-form message and rely on the suggestion field to call out the normalization. Plan defers exact wording to implementation.

- Lines 384-391 (MDPP002 alias suggestion): update the suggestion field to reflect the broader class:

  ```python
  suggestion=(
      "Alias names may use letters from any script (XML NCName letter "
      "class), digits, underscore (_), and hyphen (-). Hyphen is "
      "permitted only in non-first positions."
  )
  ```

**Acceptance:**

- The validator accepts an alias `<!-- #インストール -->` without emitting MDPP002.
- The validator accepts every alias from the existing test corpus without regression (`sample-full.md`, `sample-basic.md`, etc. validate the same way they did before).
- A document with two headings carrying NFC-different but canonical-equivalent aliases emits MDPP008.
- The validator rejects `<!-- #foo.bar -->`, `<!-- #foo:bar -->`, `<!-- #.hidden -->`, and `<!-- # has space -->` -- all four still emit MDPP002.

---

### U7. Update add-aliases.py recognition regexes

**Goal:** `add-aliases.py` recognizes Unicode-letter aliases when scanning a file for existing aliases. Slug generation stays ASCII-only.

**Files:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py`.

**Changes:**

- Add a module-level `_NCNAME_START_CHAR` constant identical to U6's (or import it from `validate-mdpp.py` if the two scripts are made to share a module -- plan does not require this; duplication is acceptable given the constant is small and stable).
- Line 41 (`ALIAS_PATTERN`): rewrite to use the new character class:

  ```python
  ALIAS_PATTERN = re.compile(
      f'<!--\\s*#([{_NCNAME_START_CHAR}0-9][{_NCNAME_START_CHAR}0-9-]*)'
  )
  ```

- Line 42 (`EXISTING_ALIAS_LINE`): same character-class rebuild:

  ```python
  EXISTING_ALIAS_LINE = re.compile(
      f'^<!--\\s*#[{_NCNAME_START_CHAR}0-9][{_NCNAME_START_CHAR}0-9-]*.*-->\\s*$'
  )
  ```

- Line 45-65 (`slugify`): **no changes.** Slug generation stays ASCII-only per *Scope Boundaries*. Note: this means a Japanese-titled heading still gets no auto-generated slug from `add-aliases.py`. If a custom Unicode alias already exists above a sibling heading, `add-aliases.py` will now recognize it (so the new ASCII slug won't accidentally duplicate); if a Japanese-titled heading has no alias above it, `slugify()` produces an empty string and `add-aliases.py` falls back to its existing `heading` placeholder (line 145).

**Acceptance:**

- Given a file with a pre-existing `<!-- #インストール -->` heading, `add-aliases.py` recognizes it (`has_alias_above()` returns true) and does NOT insert a new ASCII alias above the same heading.
- The script's behavior on ASCII-only inputs is unchanged.

---

### U8. Add Unicode test corpus

**Goal:** Validator behavior is verified against positive and negative Unicode samples.

**Files:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-aliases.md` (new), `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-unicode-duplicate-aliases.md` (new).

**Changes:**

- Create `sample-unicode-aliases.md` with frontmatter (`---\ndate: 2026-05-22\nstatus: active\n---`) followed by positive cases:

  - Case U1: Japanese alias `<!-- #インストール -->` above an H2 heading -- EXPECT no error.
  - Case U2: German alias `<!-- #Café -->` (precomposed `é`, U+00E9) above an H2 heading -- EXPECT no error.
  - Case U3: German alias `<!-- #Café -->` (decomposed `e` + combining acute, U+0065 U+0301) above an H2 heading -- EXPECT no error (NFC normalization happens at MDPP008 comparison time, not at MDPP002 acceptance time -- both raw forms accept).
  - Case U4: Greek alias `<!-- #εγκατάσταση -->` above an H2 heading -- EXPECT no error.
  - Case U5: Cyrillic alias `<!-- #установка -->` above an H2 heading -- EXPECT no error.

  Followed by negative cases:

  - Case U6: alias containing a period `<!-- #foo.bar -->` -- EXPECT MDPP002 (already covered by `sample-invalid-names.md` Case 16, but included here so all Unicode coverage lives in one file).
  - Case U7: alias starting with a period `<!-- #.hidden -->` -- EXPECT MDPP002.
  - Case U8: alias containing a colon `<!-- #foo:bar -->` -- EXPECT MDPP002.
  - Case U9: alias containing whitespace `<!-- #foo bar -->` -- EXPECT MDPP002 (note: the alias extraction regex stops at whitespace, so the alias here is `foo`, but the parser then likely treats `bar` as a separate token; the test documents the validator's actual behavior). Implementer verifies the resulting error message on first run; the plan accepts whatever the validator reports as long as the line is flagged.

- Create `sample-unicode-duplicate-aliases.md` with frontmatter, then two headings:
  - H1 with `<!-- #Café -->` precomposed (`Café`).
  - H2 with `<!-- #Café -->` decomposed (`Café`).
  - EXPECT MDPP008 on the second occurrence under NFC + casefold normalization.
  - Add a third case: two headings with `<!-- #FOO -->` and `<!-- #foo -->` -- EXPECT MDPP008 on the second under casefold normalization.

**Acceptance:**

- Running `validate-mdpp.py sample-unicode-aliases.md` emits MDPP002 for each negative case and emits no errors for the positive cases.
- Running `validate-mdpp.py sample-unicode-duplicate-aliases.md` emits MDPP008 for the second occurrence of each duplicate pair.

---

### U9. Verify backward compatibility against the existing test corpus

**Goal:** No regression against ASCII-only inputs.

**Files:** No file changes. This unit is a verification step.

**Changes:**

- Run `validate-mdpp.py` against every existing file in `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/` -- particularly `sample-basic.md`, `sample-full.md`, `sample-custom-alias-priority.md`, `sample-duplicate-aliases.md`, `sample-invalid-names.md`, `sample-orphaned-tags.md`. Each file's diagnostic output before and after the change must match.
- Run `validate-mdpp.py` against every file in `examples/` (`semantic-cross-references.md`, `styles-and-variables.md`, etc.). Each must validate the same way it did before the change.
- Run `add-aliases.py --dry-run` against `sample-full.md` and any file in `examples/` that has headings without aliases. Output must match the pre-change dry-run output.

**Acceptance:**

- Zero new errors, warnings, or info messages on any file that validated before the change.
- Identical alias-generation behavior on ASCII-only inputs.

---

### U10. Bump version, file follow-up issue, and add CHANGELOG entry

**Goal:** Plugin version reflects the new feature; downstream consumers can pin to the new minor; the follow-up audit for the other three naming patterns is tracked.

**Files:** `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (via script), `.claude-plugin/marketplace.json` (via script), `CHANGELOG.md`.

**Changes:**

- Run `scripts/bump-version.sh minor` to bump 1.6.3 → 1.7.0 in both `plugin.json` and `marketplace.json`. The script updates both files in lockstep per `CLAUDE.md` § Version Management.
- File the follow-up issue (R18) using the windworker / `gh issue create` workflow. The follow-up's intended scope:
  - Title: "Extend Unicode-letter support to variable, condition, style, and marker-key naming patterns"
  - Body: cite this PR (issue #108) as precedent. Describe the audit shape (the same five concerns: round-tripping across XML/XSLT/JS/URL/CSS, downstream emitter behavior, normalization semantics, test corpus, version bump). Note that auto-generation of heading aliases (`spec/element-interactions.md` § Heading Alias Auto-Generation) should be audited alongside, since its MAY-extend-to-Unicode allowance becomes a less consistent default once the custom-alias path supports Unicode.
- Add a `CHANGELOG.md` entry at the top of the file:

  ```markdown
  ## [1.7.0] - 2026-05-22

  ### Spec

  - Extended the custom-alias letter class from ASCII (`[a-zA-Z]`) to the XML 1.0 NCName `NameStartChar` letter ranges so authors of non-English documentation can mint native-script alias identifiers (e.g., `<!-- #インストール -->`, `<!-- #Café -->`, `<!-- #установка -->`). The standard, style, and marker-key patterns remain ASCII pending a separate audit ([#XXX-followup]). Updated `spec/specification.md` § 4.2, § 10.2, § 17.3.1, § 18.1; `spec/formal-grammar.md` adds `alias_name_start_char` and `alias_name_char` productions and updates the regex summary and PEG transliteration. Every alias valid under the previous ASCII-only grammar remains valid -- the new grammar is a strict superset ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).

  ### Tooling

  - `validate-mdpp.py` accepts Unicode-letter aliases under the new grammar and rejects only the same invalid forms that were previously rejected (punctuation outside `-_`, whitespace, period-first). MDPP008 (duplicate alias) now compares aliases under Unicode NFC + case-fold normalization so canonical-equivalent variants (precomposed vs. decomposed accented letters, upper vs. lower case) are flagged as duplicates -- matching the equivalence relation used by CommonMark 0.30 link-reference-definition slug matching ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).
  - `add-aliases.py` recognizes Unicode-letter aliases when scanning a file for existing aliases, so the script does not generate a colliding ASCII slug above a heading whose sibling already has a Unicode alias. Slug *generation* remains ASCII-only -- a Japanese-titled heading still gets a placeholder slug from `slugify()` ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).
  - Updated `references/syntax-reference.md` § Naming Rules § Alias Name and § Non-English Content; `references/error-codes.md` § Naming Rule table, § Alias Name, and the MDPP002/MDPP008 entries; `references/comment-manipulation.md` standalone-anchor example. Added `tests/sample-unicode-aliases.md` and `tests/sample-unicode-duplicate-aliases.md` covering Japanese, German (precomposed + decomposed), Greek, and Cyrillic samples, plus negative cases for whitespace, punctuation outside `-_`, and leading `.` ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).
  ```

  The `[#XXX-followup]` placeholder is replaced with the follow-up issue number after it is filed.

**Acceptance:**

- `plugin.json` and `marketplace.json` both report `1.7.0`.
- `CHANGELOG.md` has a `[1.7.0]` entry with Spec and Tooling sections.
- The follow-up issue is filed (or the changelog cites a placeholder that resolves before merge).

---

## Success Criteria (PR-level)

- Every requirement R1-R19 has a corresponding unit that lands in this PR.
- A Markdown++ document containing `<!-- #インストール -->`, `<!-- #Café -->`, `<!-- #εγκατάσταση -->`, or `<!-- #установка -->` validates without MDPP002.
- A Markdown++ document containing two NFC-different but canonical-equivalent aliases emits MDPP008.
- Every alias valid under the previous ASCII-only grammar continues to validate.
- The follow-up issue (R18) is filed (or referenced as a placeholder).
- `plugin.json` and `marketplace.json` both report `1.7.0`.
