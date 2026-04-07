# CLAUDE.md -- Markdown++

## Overview

`quadralay/markdown-plus-plus` is the public repository for the Markdown++ open documentation format. It hosts the format specification, examples, and a Claude Code plugin for AI-assisted authoring.

This is a specification and tooling repo -- no application code.

## Directory structure

```
markdown-plus-plus/
├── .claude/
│   ├── agents/                 # Agent definitions for ideation teams
│   ├── prompts/                # Reusable prompt templates
│   └── external-sources.conf   # Cross-repo resource paths
├── .claude-plugin/
│   └── marketplace.json        # Marketplace manifest
├── docs/
│   └── solutions/              # Past solutions and learnings
├── scripts/
│   └── bump-version.sh         # Version bump utility
├── spec/                       # Whitepaper and eventual formal specification
├── examples/                   # Sample .md files demonstrating features
├── CHANGELOG.md                # Format and tooling change history
├── CONTRIBUTING.md             # How to report issues and propose changes
├── GOVERNANCE.md               # Spec maintainership and versioning process
├── SECURITY.md                 # Security policy and contact
└── plugins/
    └── markdown-plus-plus/
        ├── .claude-plugin/
        │   └── plugin.json     # Plugin metadata
        └── skills/
            └── markdown-plus-plus/
                ├── SKILL.md    # Claude Code skill for Markdown++ authoring
                ├── references/ # Syntax reference, examples, best practices
                ├── scripts/    # validate-mdpp.py, add-aliases.py
                └── tests/      # Sample .md files for validation testing
```

## Conventions

### Document frontmatter

All markdown files (except README.md and LICENSE) must include YAML frontmatter:

```yaml
---
date: YYYY-MM-DD
status: draft | active | archived
---
```

### File naming

- Kebab-case for all filenames (e.g., `multiline-tables.md`)
- Date prefix for time-bound content (e.g., `2026-03-28-whitepaper.md`)
- Slug-only for evergreen content (e.g., `whitepaper.md`)

## Git workflow

- **Primary branch:** `main`
- **Feature branches** for all PRs -- never commit directly to `main`
- **Branch prefixes:** `feature/`, `fix/`, `docs/`, `refactor/`

## Version Management

Bump the plugin version before creating a PR using the bump script:

```bash
scripts/bump-version.sh patch  # 1.0.0 -> 1.0.1 (bug fixes)
scripts/bump-version.sh minor  # 1.0.0 -> 1.1.0 (new features)
scripts/bump-version.sh major  # 1.0.0 -> 2.0.0 (breaking changes)
```

The script updates both `plugin.json` and `marketplace.json` to keep versions synchronized.

**When to bump:**
- `patch`: Bug fixes, documentation updates, minor improvements
- `minor`: New skills, new features, enhancements
- `major`: Breaking changes, major restructuring

**Workflow:**
1. Make your changes
2. Run `scripts/bump-version.sh <type>`
3. Include the version bump in your PR
4. Merge PR - version is already updated

## External Sources

Cross-repo resource locations are defined in `.claude/external-sources.conf`.
Paths reference environment variables from the operator's ~/.claude/settings.json.

## Ecosystem context

Markdown++ is an open documentation format. WebWorks ePublisher is one tool that processes it, but the format is not tied to any single vendor or product.

- Format specification and skill: this repo
