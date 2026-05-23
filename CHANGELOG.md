---
date: 2026-04-07
status: active
---

# Changelog

All notable changes to the Markdown++ specification and tooling are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Changes are grouped into three categories:

- **Spec** -- Changes to the Markdown++ format specification (whitepaper, syntax reference, formal rules).
- **Tooling** -- Changes to the Claude Code plugin, validation scripts, and other tools.
- **Project** -- Repository structure, documentation, and governance changes.

## [1.8.0] - 2026-05-23

### Spec

- Extended the custom-alias non-first character class to the full XML 1.0 NCName `NameChar` production -- aliases now accept `.` (period), `#xB7` (middle dot), combining marks (`#x0300-#x036F`), and connector punctuation (`#x203F-#x2040`) in non-first positions. After this change Markdown++ aliases align with XML NCName end-to-end, with one explicit and documented deviation: aliases continue to permit a leading digit because the existing numeric-identifier convention (`<!-- #04499224 -->`) is load-bearing. Dotted-hierarchy identifiers like `<!-- #chapter.1.intro -->` and `<!-- #api.v1.users -->` are now valid under MDPP002. Leading `.` (e.g., `<!-- #.hidden -->`) remains rejected because NCName excludes `.` from `NameStartChar`. Updated `spec/specification.md` § 4.2, § 10.2, § 18.1; `spec/formal-grammar.md` `alias_name_char` production (EBNF + PEG) and the "Constructs Rejected" validation note. The architectural framing is that Markdown++ should not pre-filter for downstream CSS-selector stylistic preferences -- escaping is the responsibility of the stylesheet/JavaScript author, not the format specification ([#111](https://github.com/quadralay/markdown-plus-plus/issues/111)).

### Tooling

- `validate-mdpp.py` `ALIAS_NAME_RE` extended to accept `.` and middle dot via a new `_NCNAME_PUNCT` constant alongside the existing `_NCNAME_COMBINING`. The MDPP002 suggestion message updated to describe the new non-first-position permissions. `add-aliases.py` `ALIAS_PATTERN` and `EXISTING_ALIAS_LINE` mirror the validator's extension so the script recognizes dotted aliases when scanning for existing ones; without this update the script would silently truncate dotted aliases and could inject duplicates ([#111](https://github.com/quadralay/markdown-plus-plus/issues/111)).
- Updated `references/syntax-reference.md` § Naming Rules § Alias Name (rewrote the rule statement so `.` is described as a position-dependent permission; removed the invalid example `foo.bar` since it is now valid; corrected the explanation for `.hidden` to "Period not permitted in first position"; added valid examples `chapter.1.intro` and `api.v1.users`); `references/error-codes.md` § Naming Rule table, § Alias Name, MDPP002 entry and triggering example, § Non-English content; `references/comment-manipulation.md` standalone-anchor example regex (adds the new `_NCNAME_PUNCT` constant alongside `_NCNAME_COMBINING`). Added positive samples for `<!--#chapter.1.intro-->`, `<!--#foo.bar-->`, connector punctuation, combining marks in non-first position, and middle dot to `tests/sample-unicode-aliases.md`; relocated the `<!--#foo.bar-->` case from the negative corpus. Updated `tests/sample-invalid-names.md` Case 16 from `#bad.alias` (now valid) to `#.bad-alias` (still invalid: leading period) ([#111](https://github.com/quadralay/markdown-plus-plus/issues/111)).

## [1.7.4] - 2026-05-23

### Tooling

- Tightened `validate-mdpp.py` alias extraction so Unicode whitespace inside alias names is caught by MDPP002 instead of silently bypassing validation. The `PATTERNS['alias']` body character class previously used `[^\s;>]+?`, and because Python 3 `\s` is Unicode-aware, it excluded not only ASCII whitespace but also U+00A0 (NO-BREAK SPACE), U+202F (NARROW NO-BREAK SPACE), U+3000 (IDEOGRAPHIC SPACE), and other Unicode whitespace code points. Any alias comment containing one of those characters caused the regex to fail entirely -- the alias was never extracted and MDPP002 (invalid alias name) and MDPP008 (duplicate alias) never fired on it. The fix replaces the body class with `[^ \t\n\r;>]+?` so non-ASCII whitespace flows into the capture and trips the alias `NameChar` check. The trailing `(?=\s*;|\s*-->)` lookahead stays Unicode-permissive on purpose -- after the capture stops at the first ASCII whitespace, trailing Unicode whitespace before the terminator (a layout choice, not part of the name) is still tolerated. Added `tests/sample-unicode-whitespace-aliases.md` with NBSP / NARROW NBSP / IDEOGRAPHIC SPACE cases and a plain-ASCII positive control; updated Case U9 of `tests/sample-unicode-aliases.md` to cross-reference the new fixture and clarify that ASCII-whitespace-in-name remains a separate follow-up. Audit of the other `PATTERNS` entries: `variable`/`variable_invalid`/`condition_open`/`condition_close`/`include`/`markers_json`/`marker_simple`/`multiline`/`style` all use enumerated character classes (`[a-zA-Z_…]`, `[^>]+?`, `[^=]+`, `[^}]+`, `[^;]*`, etc.) or pure whitespace skipping -- none use `\s` inside an extracting body class. `add-aliases.py` `ALIAS_PATTERN` uses the enumerated NCName-based class and never used `\s` for body matching, so it was also unaffected ([#115](https://github.com/quadralay/markdown-plus-plus/issues/115)).

## [1.7.3] - 2026-05-23

### Tooling

- Clarified two documentation surfaces that overstated the scope of the 1.7.0 alias-grammar change. `references/error-codes.md` § *Alias Name* and `references/syntax-reference.md` § *Naming Rules > Alias Name* both characterized the new grammar as a "strict superset of the prior ASCII-only pattern." The claim is true for MDPP002 *acceptance* but misleading for *whole-document validation*, because MDPP008 (duplicate alias) tightened in 1.7.0 from byte-exact comparison to NFC + casefold -- documents with previously-distinct aliases like `<!--#FOO-->` and `<!--#foo-->` now fail MDPP008 as canonical-equivalent duplicates. Reframed both surfaces to scope the superset claim to MDPP002 and added an explicit *Migration note (1.7.0)* in `references/error-codes.md` cross-referencing the three MDPP008 sub-state messages. Also corrected the `_alias_dedup_key` docstring in `scripts/validate-mdpp.py`, which claimed CommonMark 0.30 equivalence -- CommonMark 0.30 §4.7 mandates casefold only; the Markdown++ implementation is stricter because it adds NFC. No syntax, semantics, or validator behavior changed (residual findings 3 and 5 from PR [#109](https://github.com/quadralay/markdown-plus-plus/pull/109) review).

## [1.7.2] - 2026-05-23

### Tooling

- `add-aliases.py` `ALIAS_PATTERN` now stops capture at the comment terminator, so compact-form aliases like `<!--#intro-->` extract as `intro` rather than `intro--`. The body character class contained `-` without a terminating lookahead, causing `get_existing_aliases` to greedily consume the `-->` closing sequence for any alias without whitespace between the name and the closing `-->`. `validate-mdpp.py` was unaffected (its extraction regex already used a terminating lookahead), so MDPP002/MDPP008 detection has always been correct. The impact was on `add-aliases.py` deduplication: when running the script against a file already containing compact-form aliases, the script saw the existing alias under a different name (`intro--`) than the validator (`intro`) and could inject a duplicate. Added the first `test_add_aliases.py` unit-test file (stdlib `unittest`, no new dependencies) covering compact, spaced, hyphenated, digit-first, Unicode-letter, and combined-command alias extraction (PR review finding on [#108](https://github.com/quadralay/markdown-plus-plus/pull/109)).

## [1.7.1] - 2026-05-23

### Project

- Added a **For AI agents** section to `README.md` (above `## Tools`) and a one-line cold-clone pointer to `CLAUDE.md`'s Overview block documenting two skill-ingestion paths for AI agents arriving at the repo: the Claude Code marketplace install (the existing slash commands, reframed in context) and a generic-harness path pointing at `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` as the entry point and the sibling `references/` directory as the payload. Documentation breadcrumb only -- no spec, skill, script, or test changes ([#110](https://github.com/quadralay/markdown-plus-plus/issues/110)).

## [1.7.0] - 2026-05-22

### Spec

- Extended the custom-alias letter class from ASCII (`[a-zA-Z]`) to the XML 1.0 NCName `NameStartChar` letter ranges so authors of non-English documentation can mint native-script alias identifiers (e.g., `<!-- #インストール -->`, `<!-- #Café -->`, `<!-- #установка -->`). Non-first positions additionally accept the NCName combining-mark ranges (`#x0300-#x036F`, `#x203F-#x2040`) so decomposed accented forms (e.g., `e` + U+0301) parse the same as their precomposed counterparts. The standard, style, and marker-key patterns remain ASCII pending a separate audit. Updated `spec/specification.md` § 4.2, § 10.2, § 17.3.1, § 18.1; `spec/formal-grammar.md` adds `alias_name_start_char` and `alias_name_char` productions (EBNF + PEG) and updates the regex summary. Every alias valid under the previous ASCII-only grammar remains valid -- the new grammar is a strict superset for MDPP002 acceptance ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).

### Tooling

- `validate-mdpp.py` accepts Unicode-letter aliases under the new grammar and continues to reject the same invalid forms that were previously rejected (punctuation outside `-_`, whitespace, period-first). MDPP008 (duplicate alias) now compares aliases under Unicode NFC + case-fold normalization so canonical-equivalent variants (precomposed vs. decomposed accented letters, upper vs. lower case) are flagged as duplicates -- matching the equivalence relation used by CommonMark 0.30 link-reference-definition slug matching. The MDPP008 error message distinguishes three sub-states (byte-exact, case-fold, NFC-equivalent) so authors can self-diagnose ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).
- `add-aliases.py` recognizes Unicode-letter aliases when scanning a file for existing aliases, so the script does not generate a colliding ASCII slug above a heading whose sibling already has a Unicode alias. Slug *generation* remains ASCII-only -- a Japanese-titled heading still gets a placeholder slug from `slugify()` ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).
- Updated `references/syntax-reference.md` § Naming Rules § Alias Name and § Non-English Content; `references/error-codes.md` § Naming Rule table, § Alias Name, and the MDPP002/MDPP008 entries; `references/comment-manipulation.md` standalone-anchor example. Added `tests/sample-unicode-aliases.md` (positive: Japanese, German precomposed, Greek, Cyrillic, ZWJ; negative: whitespace, punctuation outside `-_`, leading `.`) and `tests/sample-unicode-duplicate-aliases.md` (MDPP008 byte-exact, case-fold, NFC-equivalent sub-state coverage) ([#108](https://github.com/quadralay/markdown-plus-plus/issues/108)).

A follow-up audit will consider extending Unicode-letter support to the variable, condition, style, and marker-key naming patterns.

## [1.6.3] - 2026-05-22

### Tooling

- Audited every cross-reference doc surface so a reader with unique-by-construction generated anchors and within-assembly inline anchor links can answer "what does the triple add for me?" without cross-referencing other surfaces. Documented the *slug = alias value* variant alongside the existing *semantic slug + opaque alias* variant as a recommended degree of freedom for generated/automated anchors. In `references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings*, restructured *Why this is the recommended idiom* into three labeled benefit groups (*Cross-context resolution*, *Anti-drift* with two named axes *Heading-rename drift* and *Section-move drift*, *Intent signal*), added a new *Choosing the slug* subsection with a worked example for each variant, added an *Inline anchor links vs. the triple* comparison table for readers already operating with `[text](#anchor)`, and added a *For generated-anchor and pipeline workflows* callout for automation pipelines. Reframed `GLOSSARY.md` § *triple*, `spec/whitepaper.md` § 3, and `examples/semantic-cross-references.md` § *Surviving heading renames* so cross-context resolution leads and rename-survival reads as one of several anti-drift properties. Added a paired worked example in `spec/specification.md` § 17.3.1 showing the slug = alias variant alongside the existing opaque-alias example, a slug-variant note in `spec/cross-file-link-resolution.md` § *Alias IDs in Link Reference Definitions*, a slug-variant pointer and benefit-stack pitch in `SKILL.md` § *Custom Aliases / Recommended pattern*, a slug-variant + comparison pointer in `references/syntax-reference.md` § *Custom Aliases*, and a new H2 section *Slug equals alias value (pipeline-generated anchors)* in `examples/semantic-cross-references.md`. Forward-looking documentation guidance only -- no syntax, semantics, processing, or validator behavior changed ([#106](https://github.com/quadralay/markdown-plus-plus/issues/106))

## [1.6.2] - 2026-05-18

### Tooling

- Made the **adjacent placement rule** of the `alias+slug+linkref` triple normative across `SKILL.md`, `references/best-practices.md`, and `examples/semantic-cross-references.md`. The directive, heading, and link reference definition sit adjacent in source -- co-location is part of the pattern, so a heading rename, deletion, or section move carries all three pieces as a unit. Also added a placement-contrast note in `references/best-practices.md` § *Advanced Patterns → Link References* explaining why general-purpose link reference definitions (conventionally grouped at the bottom of a file) and the triple's adjacent link reference definition encode different authoring intent. Forward-looking documentation guidance only -- no syntax, semantics, processing, or validator behavior changed ([#103](https://github.com/quadralay/markdown-plus-plus/issues/103))

## [1.6.1] - 2026-05-13

### Tooling

- Clarified the multiline table row-continuation mechanism across `SKILL.md`, `references/syntax-reference.md`, `references/best-practices.md`, `references/examples.md`, and `examples/multiline-tables.md` by naming the two structural roles (row separator vs continuation row) and stating the mechanism positively: every pipe-bearing row continues the current logical row, and only an all-whitespace separator row starts a new one. Cells appear empty on continuation lines when their column has no more content to flow; no cell is privileged. Also added a "List markers in multi-line cells" readability subsection to `references/syntax-reference.md`. No syntax, semantics, or processing behavior changed ([#92](https://github.com/quadralay/markdown-plus-plus/issues/92))

## [1.6.0] - 2026-05-13

### Tooling

- Added a high-visibility Command Block Syntax anchor section to `SKILL.md` with MUST/ALWAYS/NEVER framing for the canonical `style + alias` and `markers + alias` combined directive patterns, plus a NEVER list for the three most common authoring mistakes (blank line after directive, alias on a separate line, inconsistent spacing). The new section is additive -- existing detailed sections in `<syntax_examples>`, `<common_mistakes>`, and `references/syntax-reference.md` are unchanged ([#93](https://github.com/quadralay/markdown-plus-plus/issues/93))

## [1.5.0] - 2026-05-13

### Project

- Added `GLOSSARY.md` at the repo root with canonical definitions for six Markdown++ terms (`triple`/`alias+slug+linkref`, `Unset`, `attachment rule`, `content island`, `block content`), each linking to its full-treatment surface, plus a repeatable audit procedure for adding new terms ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))
- Added `.github/PULL_REQUEST_TEMPLATE.md` with a terminology surfacing checkbox so PRs introducing or renaming Markdown++ terms update the glossary and at least one entry-point surface ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))

### Spec

- Named the `alias+slug+linkref triple` pattern on first prose use in `spec/specification.md` Section 17.3, `spec/cross-file-link-resolution.md`, and `spec/whitepaper.md`, with a glossary link from each ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))
- Added a glossary link from the `block content` reference in `spec/specification.md` Section 14.1 ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))

### Tooling

- Added a glossary link from the existing `alias+slug+linkref` reference in `SKILL.md`, and from the recommended-idiom note in `references/syntax-reference.md` ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))
- Labeled the standalone example in `examples/semantic-cross-references.md` as the `alias+slug+linkref triple` with a glossary link ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))
- Backfilled glossary links for `Unset`, `attachment rule`, and `content island` on first prose use in `SKILL.md`, `references/best-practices.md`, `references/syntax-reference.md`, and `references/examples.md` ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))
- Added a `GLOSSARY.md` pointer to `README.md`'s repo-contents list ([#99](https://github.com/quadralay/markdown-plus-plus/issues/99))

This release is documentation surfacing only -- no Markdown++ syntax, semantics, or processing behavior changed.

## [1.4.0] - 2026-05-13

### Tooling

- Added `references/comment-manipulation.md` rule set documenting safe removal and simplification of Markdown++ directive comments during cleanup, migration, or refactoring passes — block-style removal and reduction, inline-style removal when a Markdown token already conveys the role, keep-by-default semantic styles, anchor handling (standalone vs combined, ATX vs Setext, cross-cell detection inside multiline tables), table-cell preservation (width, escaped pipes, multiline row boundaries, partial-cell and bare-marker merges), and detection regex patterns with a companion-logic checklist ([#94](https://github.com/quadralay/markdown-plus-plus/issues/94))
- Added pointer to `references/comment-manipulation.md` in `SKILL.md` and cross-reference in `references/best-practices.md` ([#94](https://github.com/quadralay/markdown-plus-plus/issues/94))

## [1.3.1] - 2026-05-11

### Spec

- Fixed dangling link reference targets in the conflict-resolution example in `spec/cross-file-link-resolution.md` so each `[slug]` definition pairs with the alias directive that produces its target, restoring consistency with Examples A and B in the same file ([#96](https://github.com/quadralay/markdown-plus-plus/issues/96))

### Tooling

- Promoted the alias+slug+linkref pattern from "advanced" to recommended for topic-defining headings (titles, primary H1s, structurally important H2s) in `references/best-practices.md`; general-purpose link references for arbitrary URL reuse remain marked as advanced ([#96](https://github.com/quadralay/markdown-plus-plus/issues/96))
- Added recommendation in the Custom Aliases section of `references/syntax-reference.md` to pair aliases with link reference definitions when marking referenceable endpoints ([#96](https://github.com/quadralay/markdown-plus-plus/issues/96))
- Added explicit guidance in `SKILL.md` directing AI authors to apply the alias+slug+linkref triple on significant headings when authoring or editing Markdown++ topic files ([#96](https://github.com/quadralay/markdown-plus-plus/issues/96))
- Fixed the same dangling-target issue in the MDPP014 trigger example in `references/error-codes.md` for consistency with the spec ([#96](https://github.com/quadralay/markdown-plus-plus/issues/96))

## [1.3.0] - 2026-05-09

### Tooling

- Added `format-tables.py` script for deterministic Markdown table reformatting (standard and `<!-- multiline -->`), with idempotent output, configurable column-width strategies (`auto` / `fixed` / `proportional`), `--in-place` and `--check` modes, and inline-formatting-aware word wrap ([#91](https://github.com/quadralay/markdown-plus-plus/issues/91))
- Added `references/table-formatting.md` rule set documenting fixed-width column conventions, configurable parameters, and known limitations ([#91](https://github.com/quadralay/markdown-plus-plus/issues/91))
- Added Table Formatting subsection to `references/best-practices.md` covering in-flow editing guidance ([#91](https://github.com/quadralay/markdown-plus-plus/issues/91))
- Added test fixtures `sample-tables-multiline.md`, `sample-tables-standard-warn.md`, `sample-tables-already-formatted.md`, and the AE1-AE7 verification protocol `format-tables-cases.md` ([#91](https://github.com/quadralay/markdown-plus-plus/issues/91))

## [1.2.0] - 2026-04-12

### Spec

- Written formal Markdown++ specification (`spec/specification.md`) covering all extensions, naming rules, diagnostics, and conformance requirements ([#7](https://github.com/quadralay/markdown-plus-plus/issues/7))
- Defined two-phase processing model with normative requirements, error codes MDPP010-MDPP013, and conformance checklist ([#8](https://github.com/quadralay/markdown-plus-plus/issues/8))
- Created formal EBNF/PEG grammar for all Markdown++ extension syntax ([#11](https://github.com/quadralay/markdown-plus-plus/issues/11))
- Defined cross-file link reference resolution semantics with MDPP014 diagnostic ([#22](https://github.com/quadralay/markdown-plus-plus/issues/22))
- Added UTF-8 character encoding requirement with MDPP017 diagnostic ([#23](https://github.com/quadralay/markdown-plus-plus/issues/23))
- Specified which extensions work inside multiline table cells ([#24](https://github.com/quadralay/markdown-plus-plus/issues/24))
- Defined empty-row separator pattern for multiline tables ([#20](https://github.com/quadralay/markdown-plus-plus/issues/20))
- Added format versioning mechanism: `mdpp-version` frontmatter field, compatibility rules, MDPP015/MDPP016 diagnostics ([#25](https://github.com/quadralay/markdown-plus-plus/issues/25))
- Defined heading alias collision resolution behavior ([#53](https://github.com/quadralay/markdown-plus-plus/issues/53))
- Defined custom alias priority over auto-generated heading aliases ([#55](https://github.com/quadralay/markdown-plus-plus/issues/55))
- Allowed embedded spaces in style and marker names (three-pattern naming system) ([#52](https://github.com/quadralay/markdown-plus-plus/issues/52))
- Refined element interactions: list item naming, default names, alias collisions, link style placement ([#49](https://github.com/quadralay/markdown-plus-plus/issues/49))
- Fixed link style placement contradiction -- inline styles inside brackets require delimiters ([#64](https://github.com/quadralay/markdown-plus-plus/issues/64))
- Promoted combined commands from OPTIONAL to REQUIRED conformance; relaxed evaluation order from MUST to RECOMMENDED ([#68](https://github.com/quadralay/markdown-plus-plus/issues/68))
- Changed unrecognized combined command segments from mandated PassThrough injection to implementation-defined disposition ([#70](https://github.com/quadralay/markdown-plus-plus/issues/70))
- Removed nested condition support -- use logical expressions (AND/OR/NOT) instead ([#71](https://github.com/quadralay/markdown-plus-plus/issues/71))
- Fixed Unset condition semantics: pass through without evaluation, not truthiness-based inclusion ([#72](https://github.com/quadralay/markdown-plus-plus/issues/72))
- Simplified Unset condition handling to single pre-evaluation check; operators use pure boolean logic ([#79](https://github.com/quadralay/markdown-plus-plus/issues/79))
- Re-reserved MDPP004 (covered by MDPP009); promoted MDPP005; removed MDPP013 (consolidated into MDPP005) ([#67](https://github.com/quadralay/markdown-plus-plus/issues/67))
- Aligned error-codes.md naming rules with three-pattern system from specification §4.2 ([#65](https://github.com/quadralay/markdown-plus-plus/issues/65))
- Added MDPP010-MDPP017 entries to error-codes.md and syntax-reference.md ([#66](https://github.com/quadralay/markdown-plus-plus/issues/66))

### Tooling

- Added standalone error code reference for MDPP000-MDPP009 ([#14](https://github.com/quadralay/markdown-plus-plus/issues/14))
- Updated SKILL.md with references to new spec documents ([#50](https://github.com/quadralay/markdown-plus-plus/issues/50))
- Added cross-file link resolution to SKILL.md and MDPP014 to validation table ([#42](https://github.com/quadralay/markdown-plus-plus/issues/42))
- Consolidated and clarified the example documentation strategy ([#13](https://github.com/quadralay/markdown-plus-plus/issues/13))
- Added nested condition detection to validate-mdpp.py (MDPP001 nesting check with document-order event processing)
- Added test fixtures: sample-circular-includes.md, sample-unset-passthrough.md

### Project

- Added CONTRIBUTING.md, CHANGELOG.md, and GOVERNANCE.md ([#26](https://github.com/quadralay/markdown-plus-plus/issues/26))
- Documented graceful degradation behavior for each extension ([#12](https://github.com/quadralay/markdown-plus-plus/issues/12))
- Documented Markdown++ interactions with standard Markdown elements ([#9](https://github.com/quadralay/markdown-plus-plus/issues/9))
- Promoted all spec documents from draft to active status ([#69](https://github.com/quadralay/markdown-plus-plus/issues/69))
- Updated GOVERNANCE.md with formal steering group participation language
- Created ePublisher conformance gaps document for adapter development ticketing

## [1.1.4] - 2026-04-06

### Spec

- Defined PassThrough behavior for unrecognized commands in HTML comments ([#21](https://github.com/quadralay/markdown-plus-plus/issues/21))
- Specified alias behavior on inline elements ([#19](https://github.com/quadralay/markdown-plus-plus/issues/19))
- Specified whether custom aliases supplement or replace auto-generated heading IDs ([#18](https://github.com/quadralay/markdown-plus-plus/issues/18))
- Defined include file type restrictions ([#17](https://github.com/quadralay/markdown-plus-plus/issues/17))
- Defined and implemented variable escaping mechanism ([#16](https://github.com/quadralay/markdown-plus-plus/issues/16))
- Formalized the attachment rule as a named specification

### Tooling

- Implemented unified naming rule for all Markdown++ name types ([#15](https://github.com/quadralay/markdown-plus-plus/issues/15))

## [1.0.0] - 2026-03-30

### Spec

- Published Markdown++ whitepaper with format rationale and comparisons
- Neutralized vendor-specific references in specification ([#3](https://github.com/quadralay/markdown-plus-plus/issues/3))
- Wove interchangeability messaging across documentation ([#5](https://github.com/quadralay/markdown-plus-plus/issues/5))

### Tooling

- Migrated Claude Code skill from webworks-claude-skills repository
- Added validation script (`validate-mdpp.py`) and alias generator (`add-aliases.py`)
- Added marketplace configuration and version management tooling

### Project

- Initialized repository with specification, examples, and directory structure
- Added syntax reference, best practices, and example files
- Added SECURITY.md and .gitignore

[1.2.0]: https://github.com/quadralay/markdown-plus-plus/compare/v1.1.4...v1.2.0
[1.1.4]: https://github.com/quadralay/markdown-plus-plus/compare/v1.0.0...v1.1.4
[1.0.0]: https://github.com/quadralay/markdown-plus-plus/releases/tag/v1.0.0
