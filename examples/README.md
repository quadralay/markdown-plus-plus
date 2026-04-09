# Examples

Standalone specimen documents demonstrating Markdown++ features using real directives.

## Purpose

These files are **executable Markdown++ documents** -- not fenced code blocks showing syntax, but actual `.md` files that humans and tools can open, preview, and validate. Each file focuses on one feature area and uses real Markdown++ directives throughout.

Use these files to:

- **Preview** how Markdown++ renders in any standard Markdown viewer
- **Validate** syntax with the validation script (`python scripts/validate-mdpp.py <file>`)
- **Learn** how features work by reading real documents, not just syntax descriptions

## Files

| File | Feature area |
|------|-------------|
| `styles-and-variables.md` | Custom styles, variables, content islands |
| `includes-and-conditions.md` | Book assembly with includes, conditional content |
| `multiline-tables.md` | Basic and styled multiline tables, multiline headers |
| `semantic-cross-references.md` | Aliases, semantic slugs, link reference definitions |
| `markers-and-metadata.md` | Markers, JSON format, index entries, passthrough |
| `combined-commands.md` | Multiple extensions composed in single directives |
| `inline-image-and-link-styles.md` | Inline styles applied to images and links |
| `nested-lists.md` | Styled nested lists and procedures |

## Related locations

Markdown++ examples live in three places, each serving a different audience:

- **`examples/`** (this directory) -- Standalone specimen documents with real directives. For humans and tools to open, preview, and validate.
- **`plugins/.../references/examples.md`** -- Scenario-oriented patterns in fenced code blocks. Curated context for the Claude Code AI skill.
- **`plugins/.../references/best-practices.md`** -- Prescriptive guidance with minimal do/don't snippets illustrating rules.

New standalone examples belong here. New scenario patterns for AI context belong in `references/examples.md`.
