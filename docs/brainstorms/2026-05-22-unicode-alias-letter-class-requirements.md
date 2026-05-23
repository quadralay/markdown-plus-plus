---
date: 2026-05-22
topic: unicode-alias-letter-class
status: draft
issue: 108
---

# Unicode-Letter Custom Alias Names

## Summary

Extend the Markdown++ custom-alias letter class from ASCII `[a-zA-Z]` to the XML 1.0 NCName `NameStartChar` letter ranges, so authors of non-English documentation can use native-script alias identifiers. The variable, condition, style, and marker-key patterns stay ASCII for now and are deferred to a follow-up audit. Every alias valid under today's grammar remains valid; the new grammar is a strict superset.

---

## Problem Frame

Markdown++ aliases are opaque HTML-comment anchors (`<!-- #name -->`) used as cross-reference targets. They never appear in user-visible output — they are routed into HTML `id=` attributes and URL fragments by the downstream emitter, not rendered as prose. Today the spec's MDPP002 triggering condition restricts alias names to `[a-zA-Z0-9_][a-zA-Z0-9_-]*`, ASCII-only.

Authors writing Japanese, German, Greek, or Cyrillic documentation cannot mint native-script aliases (e.g., `<!-- #インストール -->`) even though:

- The downstream HTML target (`id=`) accepts any non-whitespace character per HTML5.
- WebWorks ePublisher's Reverb 2.0 and 3.0 landmark resolvers were widened to accept Unicode IDs in changeset r35807, explicitly naming "Unicode NCNames such as concepts written in Japanese or German" as the motivation.
- The ePublisher Markdown++ adapter already sanitizes alias candidates with a Python 3 Unicode-aware pattern that preserves Unicode letters.

The bottleneck is the Markdown++ spec validation surface — MDPP002 — and the Python validator that enforces it. Authors hit MDPP002 during static validation and stop, even though every downstream surface in the WebWorks pipeline would accept the alias cleanly. The spec's `references/syntax-reference.md` § Non-English Content even notes "UTF-8 letter support is a future goal" — that future arrives here, for the alias case.

---

## Requirements

**Grammar definition (spec)**

- R1. `spec/specification.md` § 18.1 (the MDPP002 row of the Static Validation Codes table) is updated so the alias-name pattern cites the XML 1.0 NCName `NameStartChar` letter ranges instead of `[a-zA-Z0-9_][a-zA-Z0-9_-]*`. The standard, style, and marker-key patterns in the same triggering-condition cell stay ASCII.
- R2. `spec/formal-grammar.md` adds new `alias_name_start_char` and `alias_name_char` productions that expand to the XML NCName letter ranges and the existing `_`, `0-9`, `-` characters; the existing `alias_name` production rewrites to use them. The shared `letter` production at line 55 keeps its ASCII definition; its accompanying comment is updated to record that the alias case is now resolved while standard/style remain deferred.
- R3. The formal-grammar regex summary (currently around line 98) and the PEG grammar (currently around lines 419-423) are updated so the alias forms match the new EBNF.
- R4. The new alias grammar is a strict superset of the old grammar: every alias name that passes today's `[a-zA-Z0-9_][a-zA-Z0-9_-]*` MUST still pass.

**Documentation surfaces**

- R5. `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` § Naming Rules § Alias Name is rewritten to document the new grammar. § Non-English Content is rewritten to describe what is now supported for aliases and what remains deferred for variables, conditions, styles, and marker keys.
- R6. `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` § Naming Rule table (currently lines 41-67) and the MDPP002 entry are updated. The naming-rule prose paragraph at the end of that section that begins "For non-English content, the same structural rules apply..." is rewritten to match § Non-English Content in syntax-reference.md (currently both surfaces hedge identically; this issue resolves the alias half).
- R7. `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md` line 453 (the example regex `r'<!--\s*(#[a-zA-Z0-9_-]+)\s*-->'`) is updated to reflect the new alias grammar, or annotated as a deliberately-ASCII example with a note pointing to the canonical Unicode-aware pattern.
- R8. `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` and `spec/whitepaper.md` and `spec/processing-model.md` are checked for any restated alias pattern and updated if found. (No occurrences were found during the brainstorm scan; this requirement exists as a verification step, not as a known edit.)

**Validator implementation**

- R9. `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` updates `ALIAS_NAME_RE` (currently line 76) to accept the new letter class. The implementation builds an explicit character class string from the XML 1.0 NCName productions; `\w` is not used because it conflates letters with digits and underscores in a way that breaks the digit-first-allowed rule for aliases.
- R10. The validator's existing MDPP002 message and suggestion strings for invalid alias names are updated to reflect the broader character class without becoming unwieldy. Implementation may decide whether to enumerate ranges or simply describe the class ("letters in any script, digits, underscore, hyphen").
- R11. The MDPP008 (duplicate alias within file) check in `validate-mdpp.py` compares aliases after Unicode NFC normalization and case-fold so that variant-equivalent forms (e.g., precomposed vs decomposed accented letters) are caught as duplicates. The current byte-exact `if alias_name in alias_locations:` check is replaced with a normalized-key comparison.
- R12. If `validate-mdpp.py` carries any cross-file slug normalization for MDPP014, the same NFC + case-fold normalization applies. (Scan during planning to confirm whether the current validator has this surface; if absent, MDPP014 normalization stays out of scope and the inconsistency is noted under Outstanding Questions.)
- R13. `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/add-aliases.py` regex patterns (currently lines 41-42) that scan for existing custom aliases are updated to recognize Unicode-letter aliases, so the script does not mistakenly consider a Unicode-letter alias absent and inject a duplicate ASCII slug above the same heading.

**Test corpus**

- R14. `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/` gains at least one positive sample per major script — Japanese (`<!-- #インストール -->`), German with combining accent (`<!-- #Café -->` precomposed and decomposed variants), Greek (`<!-- #εγκατάσταση -->`), Cyrillic (`<!-- #установка -->`).
- R15. The same `tests/` location gains negative samples that MUST still fail MDPP002: alias containing whitespace, alias containing punctuation outside `-_` (e.g., `<!-- #foo.bar -->`, `<!-- #foo:bar -->`), alias starting with `.` (e.g., `<!-- #.hidden -->`).
- R16. At least one positive sample exercises the MDPP008 normalization path: two aliases in the same file that are NFC-different but case-fold-equivalent or canonical-equivalent SHOULD be flagged as duplicates.

**Changelog and follow-up**

- R17. `CHANGELOG.md` records the change under the next minor-version entry, naming MDPP002, the new alias letter class, and the MDPP008 normalization update.
- R18. A follow-up GitHub issue is filed (or referenced if already filed) for the question of extending Unicode-letter support to variable, condition, style, and marker-key patterns. The follow-up issue title and link, if filed during this work, are recorded in CHANGELOG.md alongside R17.
- R19. The plugin version is bumped via `scripts/bump-version.sh minor` before the PR per `CLAUDE.md`'s version management section.

---

## Acceptance Examples

- AE1. **Covers R1, R9.** Given a Markdown++ document containing `<!-- #インストール -->` attached to a heading, when validated by the updated `validate-mdpp.py`, the validator exits 0 with no MDPP002 emitted.
- AE2. **Covers R11.** Given a Markdown++ document with `<!-- #Café -->` (precomposed `é`) on one heading and `<!-- #Café -->` (decomposed `e` + combining acute) on another heading, when validated, the validator emits MDPP008 (duplicate alias) for the second occurrence.
- AE3. **Covers R15.** Given a Markdown++ document containing `<!-- #foo.bar -->`, when validated, the validator emits MDPP002 with severity error, because `.` is not in the NCName-derived letter class or the explicit `-_` set.
- AE4. **Covers R4.** Given any alias that was valid under the prior `[a-zA-Z0-9_][a-zA-Z0-9_-]*` grammar (e.g., `<!-- #04499224 -->`, `<!-- #sh-ug-installation -->`, `<!-- #_internal -->`), when validated with the new grammar, the alias passes MDPP002.
- AE5. **Covers R13.** Given a heading "インストール" with no existing alias, when `add-aliases.py` runs against the file, it does not produce a duplicate alias by failing to recognize a pre-existing Unicode-letter alias on a sibling heading.

---

## Success Criteria

- **Author outcome.** A non-English-language documentation author can write `<!-- #ネイティブスクリプト -->` (or the equivalent in German with accents, Greek, Cyrillic, etc.), validate the document with the project's `validate-mdpp.py`, and see no MDPP002. The cross-reference `[label][ネイティブスクリプト]` resolves in CommonMark 0.30+ renderers and in the WebWorks pipeline without further intervention.
- **Downstream-agent handoff.** A planner reading this document does not need to invent (a) the letter-class source, (b) the test corpus shape, (c) the MDPP008 normalization semantics, (d) which surfaces restate the pattern, or (e) whether the auto-generation path is in scope. All five are pinned by Requirements, Scope Boundaries, or Outstanding Questions.
- **Compatibility floor.** Every existing valid alias in the repository's `examples/`, `tests/`, and any consuming downstream document continues to validate. R4 makes this load-bearing.
- **Format symmetry.** The MDPP002 row no longer hedges differently from MDPP008 about non-ASCII. After this change, both codes apply to the same character-class universe.

---

## Scope Boundaries

- **Variable, condition, style, and marker-key patterns stay ASCII.** The three patterns are documented as a shared grammar with deliberate variations, and changing them in lockstep needs its own audit. Deferred to the follow-up issue referenced in R18.
- **NCName `NameChar` extras stay excluded.** NCName's `NameChar` permits `.`, middle dot (`#xB7`), and Unicode combining marks (`#x0300-#x036F`, `#x203F-#x2040`) in non-first positions. The current Markdown++ alias grammar does not permit any of these, and this issue leaves that decision for later. Scope is the letter class only.
- **HTML5 `id` superset stays excluded.** HTML5 permits punctuation and symbols in `id` attributes; that is the output-safety bar, not the authoring grammar. NCName is the well-defined Unicode-aware identifier grammar designed for this purpose, and it is a subset of HTML-ID-legal, so every NCName-valid alias lands cleanly in HTML.
- **Heading-alias auto-generation algorithm stays as specified.** `spec/element-interactions.md` § Heading Alias Auto-Generation currently strips non-ASCII characters as MUST behavior with Unicode as a MAY extension. Whether to flip Unicode from MAY to MUST is a separate decision tracked under Outstanding Questions. The custom-alias path and the auto-generated-alias path are deliberately decoupled in this issue.
- **`add-aliases.py` slug generator stays ASCII-only for generation.** R13 only updates the *recognition* regex so the script can see Unicode-letter aliases that already exist; it does not change `slugify()` (currently line 45-60) to emit Unicode slugs. Whether to extend slug *generation* to Unicode is tracked under Outstanding Questions.
- **No third-party `regex` dependency.** Implementation uses stdlib `re` with an explicit character class spelled from the XML 1.0 NCName productions. The issue's "regex (third-party, supports `\p{L}` natively)" mention is rejected as a needless dependency.

---

## Key Decisions

- **Letter-class basis: XML NCName `NameStartChar`, not HTML5-ID-legal, not `\p{L}`.** NCName is the named, well-defined Unicode-aware identifier grammar that motivated the ePublisher precedent (r35807 commit message names it directly), is a subset of HTML-ID-legal (so HTML emission is safe), and is bounded enough to spell as an explicit character class in stdlib `re`. `\p{L}` would require the third-party `regex` package; HTML5-ID-legal would let in punctuation and symbols that NCName forbids.
- **Strict-superset preservation.** Every alias valid under the old grammar remains valid. This is a non-negotiable to avoid breaking existing documents and downstream toolchain expectations.
- **Normalization semantics for MDPP008/MDPP014: NFC + Unicode case-fold.** This matches CommonMark 0.30's link-reference-definition slug-matching semantics, so cross-reference resolution and duplicate detection use the same equivalence relation.
- **Custom-alias path decoupled from auto-generation path.** The issue's scope is custom aliases. The auto-generation algorithm is governed by `spec/element-interactions.md` § Heading Alias Auto-Generation and is currently a MAY-extend-to-Unicode rule. Leaving auto-generation alone in this issue means a Japanese-titled heading still gets no auto-generated alias by default, but a custom Japanese alias on the same heading is now permitted. This asymmetry is intentional for v1 of the change — it is recorded under Outstanding Questions as a follow-up, not silently accepted.

---

## Dependencies / Assumptions

- **Assumed:** CommonMark 0.30 normalizes link-reference slugs via Unicode case-fold and whitespace collapse before matching. The current `validate-mdpp.py` MDPP008 comparison is byte-exact; whether it carries any MDPP014 implementation at all is unverified at brainstorm time and is checked under R12.
- **Assumed:** Python 3.8+ stdlib `re` supports the explicit code-point ranges spelled from XML 1.0 NCName. (The ranges `[#x10000-#xEFFFF]` need `re` astral-plane support, which Python 3 has natively. Verified by Python docs; no implementation-time surprise expected.)
- **Verified:** `examples/`, `tests/`, and the repo's existing alias usage are ASCII-only at the time of this brainstorm. No backward-compat migration of existing documents is required.
- **Verified:** The ePublisher precedent (changeset r35807) is referenced in the issue body, not in this repo. No internal cross-link needs to be updated.
- **Dependency:** `scripts/bump-version.sh minor` runs cleanly and produces a synchronized `plugin.json` / `marketplace.json` bump (R19). The version-bump path is well-trodden per `CLAUDE.md`.

---

## Outstanding Questions

### Resolve Before Planning

*(none — the issue body resolved all blocking product decisions before this brainstorm started)*

### Deferred to Planning

- **[Affects R12][Technical]** Does `validate-mdpp.py` currently implement an MDPP014 (cross-file slug conflict) check? If yes, NFC + case-fold normalization extends to it. If no, the planner records this as a known gap and leaves MDPP014 normalization out of scope for this issue.
- **[Affects R6][Technical]** Does `error-codes.md` contain any other prose paragraph that restates the alias pattern beyond the § Naming Rule table and the § Non-English Content note? Planning's surface-scan pass should grep the file for `[a-zA-Z` and verify.
- **[Affects R7][Needs research]** Is the `comment-manipulation.md` line 453 regex an authoritative pattern that downstream agents copy, or just an example to illustrate concept? If authoritative, update the pattern; if illustrative, annotate it with a "for full grammar see syntax-reference.md" pointer. Planning reads the surrounding context to decide.
- **[Affects R8][Needs research]** Manual grep of `spec/whitepaper.md`, `spec/processing-model.md`, and `SKILL.md` for any direct citation of the alias pattern. The brainstorm scan found none; planning should confirm.
- **[Affects scope boundary][Needs research]** Should `spec/element-interactions.md` § Heading Alias Auto-Generation (currently lines 199-210) flip its Unicode allowance from MAY to MUST? Status quo asymmetry: custom aliases support Unicode after this change; auto-generated aliases still strip Unicode by spec MUST. Tracked here as a deferred question rather than a scope addition because it is a separate decision with its own audit shape. If the answer is "yes, flip it," the follow-up issue is the right place — same audit that handles variables/conditions/styles/markers.
- **[Affects add-aliases.py][Technical]** Should `slugify()` in `add-aliases.py` (currently line 45-60, regex `[^a-z0-9]+`) be extended to preserve Unicode letters when *generating* aliases from heading text? Linked to the heading-alias-auto-gen question above. Status quo for this issue: leave `slugify()` ASCII-only; only update the *recognition* regex per R13.

---

## Integration Notes for Planning

These are not new requirements; they are pointers planning should hold onto while sequencing the work.

- **The alias-pattern surfaces are not all literal regexes.** Some surfaces (e.g., `error-codes.md`'s naming-rule prose, `syntax-reference.md`'s "Non-English Content" note, `formal-grammar.md`'s `letter`-production comment) discuss the pattern in prose. Planning should not chase only regex-shaped occurrences.
- **Three identifier forms, one shared `letter` production.** `formal-grammar.md`'s `letter` production is referenced by `identifier`, `alias_name`, and `style_name`. The new alias productions stand alongside `letter`, not replacing it. Keep the existing `letter` definition; add alias-specific productions next to it; update the comment on `letter` to record that the alias case is now resolved.
- **The validator's MDPP002 message string is author-facing.** R10 leaves enumeration-vs-description as a planning choice. The decision affects how the error reads in a terminal — a planner should weigh terseness vs precision for that surface.
- **Test sample placement.** `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/` already has `auto-activation/cases.md` per `CLAUDE.md`. The new Unicode samples need their own subdirectory or naming convention so they do not collide with the auto-activation suite. Planning chooses the layout.
