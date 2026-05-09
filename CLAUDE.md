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

## Working with Markdown++ files

Most `.md` files in this repo are Markdown++ source documents. The
`markdown-plus-plus:markdown-plus-plus` skill auto-activates on files
containing distinguishing Markdown++ signals -- but auto-activation
depends on the routing layer seeing those signals at decision time.
Two workflow conventions close the gaps where the routing layer cannot
see a signal on its own:

1. **Read before edit.** Any agent working on a `.md` file in this
   repo should `Read` the file before editing it. Reading brings the
   file's frontmatter and Markdown++ directives into routing context,
   which lets the skill auto-activate on the actual signals in the
   document. Edit-without-read flows bypass this surfacing entirely.

2. **Load the skill explicitly when the prompt is generic.** Prompts
   like "update the docs" or "add a row to that table" do not carry
   the file-content signals the routing layer keys on. When working
   on Markdown++ files in this repo, invoke
   `/markdown-plus-plus:markdown-plus-plus` (or load the skill
   through whatever routing surface is available) before editing.

This guidance is expectation-setting for human authors and AI agents,
not a runtime contract -- the routing layer is not bound by anything
written here. The convention exists because the alternative is silent
authoring failures on documents the skill should have caught and didn't.

**Suggested language for downstream consumers.** Repositories that
author Markdown++ documents are encouraged to copy the two rules above
into their own `CLAUDE.md` so the same routing-context discipline
applies wherever Markdown++ is authored. The
`references/best-practices.md` file in this skill carries the same
guidance for downstream reference. See
[`tests/auto-activation/cases.md`](plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md)
for the manual-verification suite that exercises these conventions.

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

## Example locations

Markdown++ examples live in three places with distinct roles:

| Location | Role | Form | Audience |
|----------|------|------|----------|
| `examples/` | Standalone specimen documents | Real Markdown++ directives (not code blocks) | Humans and tools -- open, preview, validate |
| `plugins/.../references/examples.md` | Scenario pattern library | Fenced code blocks showing syntax | Claude Code AI skill context |
| `plugins/.../references/best-practices.md` | Prescriptive style guide | Minimal do/don't snippets | Authors learning conventions |

**Where to add new examples:**
- A new standalone, feature-focused specimen document: `examples/`
- A new realistic scenario combining multiple extensions: `references/examples.md`
- A new rule illustration or anti-pattern: `references/best-practices.md`

Avoid duplicating identical table data or scenarios across locations.

## Ecosystem context

Markdown++ is an open documentation format. WebWorks ePublisher is one tool that processes it, but the format is not tied to any single vendor or product.

- Format specification and skill: this repo
