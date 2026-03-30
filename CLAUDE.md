# CLAUDE.md -- Markdown++

## Overview

`quadralay/markdown-plus-plus` is the public repository for the Markdown++ open documentation format. It hosts the format specification, examples, and a Claude Code plugin for AI-assisted authoring.

This is a specification and tooling repo -- no application code.

## Directory structure

```
markdown-plus-plus/
├── spec/           # Whitepaper and eventual formal specification
├── examples/       # Sample .md files demonstrating features
└── plugins/
    └── markdown-plus-plus/
        └── skills/
            └── markdown-plus-plus/
                └── SKILL.md    # Claude Code skill for Markdown++ authoring
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

## Ecosystem context

Markdown++ is an open documentation format. WebWorks ePublisher is one tool that processes it, but the format is not tied to any single vendor or product.

- Format specification and skill: this repo
- ePublisher-specific workflows: `quadralay/webworks-claude-skills`
- Business strategy and marketing: `quadralay/webworks-brain` (private)
