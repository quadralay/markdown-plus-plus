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

## [Unreleased]

### Spec

- Added format versioning mechanism: `mdpp-version` frontmatter field for document-level version declaration, compatibility rules, MDPP015/MDPP016 diagnostic codes, and initial spec version 1.0 ([#25](https://github.com/quadralay/markdown-plus-plus/issues/25))

### Tooling

### Project

- Added CONTRIBUTING.md, CHANGELOG.md, and GOVERNANCE.md ([#26](https://github.com/quadralay/markdown-plus-plus/issues/26))

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

[Unreleased]: https://github.com/quadralay/markdown-plus-plus/compare/main...HEAD
[1.1.4]: https://github.com/quadralay/markdown-plus-plus/compare/v1.0.0...main
[1.0.0]: https://github.com/quadralay/markdown-plus-plus/releases/tag/v1.0.0
