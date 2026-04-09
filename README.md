<p align="center">
  <img src="brand/logo.svg" alt="Markdown++ logo" width="128" height="128">
</p>

# Markdown++

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Markdown++ is an open documentation format built on [CommonMark](https://commonmark.org). It adds professional publishing features -- styles, variables, conditional content, cross-references, content assembly, metadata -- through HTML comment directives and inline tokens that are invisible to standard Markdown renderers.

Every Markdown++ file is a valid CommonMark document. No proprietary syntax, no custom file extension, no build step required to preview your content.

## Quick look

```markdown
<!-- style:Note -->
This paragraph is styled as a note in published output, but renders
as a normal paragraph in GitHub, VS Code, or any Markdown viewer.

<!-- condition:online -->
This content only appears in online output formats.
<!-- /condition -->

The current version is $product_version;, released $release_date;.
```

HTML comments are invisible to renderers. Inline tokens (`$variable;`) pass through as literal text. The extensions activate only when processed by a publishing tool.

## What's in this repo

This is the home of the Markdown++ format standard -- its specification, examples, and tooling.

- **[spec/](spec/)** -- The [Markdown++ whitepaper](spec/whitepaper.md) explaining the format, its design rationale, and how it compares to DITA, FrameMaker, Word, and other documentation formats.
- **[examples/](examples/)** -- Sample `.md` files demonstrating Markdown++ features.
- **[Syntax reference](plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md)** -- Complete reference for all extensions, rules, and validation codes.

## Tools

### Claude Code plugin

[![Claude Code](https://img.shields.io/badge/Claude-Code-purple)](https://claude.ai/code)

A Claude Code marketplace plugin for AI-assisted Markdown++ authoring.

```
/plugin marketplace add quadralay/markdown-plus-plus
/plugin install markdown-plus-plus@markdown-plus-plus
```

| Feature | Description |
|---------|-------------|
| **Syntax reference** | Authoritative reference for all extensions (variables, conditions, styles, aliases, includes, markers, multiline tables) |
| **Validation** | Python script to check syntax errors, unclosed conditions, invalid variables, malformed JSON markers, duplicate aliases, orphaned tags |
| **Alias generation** | Script to auto-generate unique aliases for headings |
| **Best practices** | Naming conventions, document structure patterns, common mistakes |

### Other tools

- **[asciidoctor-mdpp](https://github.com/quadralay/asciidoctor-mdpp)** -- Convert AsciiDoc documents to Markdown++.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to report issues, propose spec changes, and submit pull requests.

For governance, spec versioning, and the decision-making process, see [GOVERNANCE.md](GOVERNANCE.md).

For a history of changes, see [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
