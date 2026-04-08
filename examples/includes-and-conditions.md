---
mdpp-version: 1.0
date: 2026-03-29
status: active
---

<!-- style:Heading1; #100002 -->
# Includes and conditional content

[includes-and-conditions]: #100002 "Includes and conditional content"

This example demonstrates file assembly and conditional content in Markdown++.

## Book assembly with includes

A book structure file assembles individual documents into a publication:

```markdown
<!-- include:../content/chapter-01-overview.md -->
<!-- include:../content/chapter-02-getting-started.md -->
<!-- include:../content/chapter-03-configuration.md -->
<!-- include:../common/boilerplate/trademarks.md -->
```

Each included file is a standalone document that can be edited and previewed independently. The book file is purely an assembly manifest.

## Conditional content

<!-- condition:online -->
This paragraph only appears in online output formats. Use conditions to tailor content for different audiences or delivery channels.
<!-- /condition -->

<!-- condition:pdf -->
This paragraph only appears in PDF output. Print-specific instructions, page references, and formatting notes belong here.
<!-- /condition -->

Content outside any condition block appears in all output formats.

## Cross-references

Link to other sections using semantic slugs that work in every context:

See [Styles and variables][styles-and-variables] for details on custom styling.

The slug resolves as a heading anchor in standard Markdown viewers and as a cross-file link in composite assemblies.
