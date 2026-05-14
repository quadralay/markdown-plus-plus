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

## [1.6.1] - 2026-05-13

### Tooling

- Clarified the multiline table row-continuation mechanism across `SKILL.md`, `references/syntax-reference.md`, `references/best-practices.md`, `references/examples.md`, and `examples/multiline-tables.md` by naming the two structural roles (row separator vs continuation row) and making explicit that every pipe-bearing row continues the current logical row by default — the empty first cell on continuation rows is a readability convention, not the trigger. Also added a "List markers in multi-line cells" readability subsection to `references/syntax-reference.md`. No syntax, semantics, or processing behavior changed ([#92](https://github.com/quadralay/markdown-plus-plus/issues/92))

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
