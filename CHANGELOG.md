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
