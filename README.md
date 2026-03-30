# Markdown++

Markdown++ is an open documentation format built on [CommonMark](https://commonmark.org). It adds professional publishing features -- styles, variables, conditional content, cross-references, content assembly, metadata -- through HTML comment directives and inline tokens that are invisible to standard Markdown renderers.

Every Markdown++ file is a valid CommonMark document. No proprietary syntax, no custom file extension, no build step required to preview your content.

## What's in this repo

- **[spec/](spec/)** -- The [Markdown++ whitepaper](spec/whitepaper.md) explaining the format, its design rationale, and how it compares to DITA, FrameMaker, Word, and other documentation formats.
- **[examples/](examples/)** -- Sample `.md` files demonstrating Markdown++ features.
- **[plugins/](plugins/)** -- Claude Code marketplace plugin with a skill for AI-assisted Markdown++ authoring.

## Quick look

Markdown++ extensions use two mechanisms:

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

## Syntax reference

The [Markdown++ User's Guide](https://static.webworks.com/docs/epublisher/latest/help/#context/md-intro) provides the complete syntax reference.

## License

[MIT](LICENSE)
