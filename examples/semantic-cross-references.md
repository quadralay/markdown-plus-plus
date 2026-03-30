---
date: 2026-03-29
status: active
---

<!-- style:Heading1; markers:{"Keywords": "cross-references, aliases, links"}; #200001 -->
# Semantic cross-references

[semantic-cross-references]: #200001 "Semantic cross-references"

This example demonstrates how Markdown++ cross-references work across every output context -- standard Markdown viewers, standalone publishing, and multi-file composite assemblies.

## The pattern

Every linkable heading uses three parts:

1. A **combined command** with a style and a numeric alias ID
2. The **heading text** on the next line
3. A **link reference definition** that bridges a semantic slug to the alias ID

<!-- style:Heading2; #200002 -->
## Getting started

[getting-started]: #200002 "Getting started"

This section introduces the basics. The alias `#200002` is a stable identifier assigned by the authoring tool or author. The semantic slug `getting-started` is derived from the heading text and is what other documents use to link here.

## Same-document references

Link to the section above using the semantic slug:

See [Getting started][getting-started] for an introduction.

The link resolves in every context:

- **Standard Markdown viewer** -- the slug matches the heading anchor, producing a working in-page link
- **Publishing tool** -- the alias ID (`#200002`) resolves to the correct output location
- **Composite assembly** -- the alias ID resolves across all included files

## Cross-document references

In a multi-file documentation set, cross-document references use the same semantic slug pattern. The link reference definition lives in the target document.

**Source document (`configuration.md`):**

```markdown
For background, see [Getting started][getting-started].
```

**Target document (`getting-started.md`):**

```markdown
<!-- style:Heading1; #200010 -->
# Getting started

[getting-started]: #200010 "Getting started"
```

The publishing tool resolves `[getting-started]` across all included files. In a standard Markdown viewer, the link works as a heading anchor within the same page (or as a relative file link if the author adds a fallback).

<!-- style:Heading2; markers:{"IndexMarker": "cross-references: heading rename"}; #200003 -->
## Surviving heading renames

[surviving-heading-renames]: #200003 "Surviving heading renames"

In standard Markdown, heading links are auto-generated from the heading text. Rename a heading, break every link that points to it. In Markdown++, the semantic slug and alias ID decouple the link target from the heading text.

If this heading were renamed from "Surviving heading renames" to "Stable links across renames", the alias `#200003` stays the same. Update the link reference definition and the semantic slug once:

```markdown
[stable-links-across-renames]: #200003 "Stable links across renames"
```

All existing references using the old slug need updating, but the alias ID in the combined command stays fixed -- no changes needed in the publishing project or cross-file linking infrastructure.

<!-- style:Heading2; #200004 -->
## Multiple aliases on one heading

[multiple-aliases]: #200004 "Multiple aliases on one heading"

A heading can have multiple link reference definitions pointing to the same alias. This is useful when a section is known by more than one name:

```markdown
<!-- style:Heading2; #200004 -->
## Multiple aliases on one heading

[multiple-aliases]: #200004 "Multiple aliases on one heading"
[multi-alias-example]: #200004 "Multiple aliases on one heading"
```

Both `[multiple-aliases]` and `[multi-alias-example]` resolve to the same heading.

<!-- style:Heading2; markers:{"IndexMarker": "cross-references: topic map"}; #200005 -->
## Topic map with cross-references

[topic-map-cross-references]: #200005 "Topic map with cross-references"

In a composite document assembled with `<!-- include: -->`, cross-references work across all included files without any special configuration:

```markdown
<!-- Top-level book file: user-guide.md -->

<!--include:chapters/overview.md-->
<!--include:chapters/installation.md-->
<!--include:chapters/configuration.md-->
<!--include:chapters/troubleshooting.md-->
```

Each chapter defines its own aliases and link reference definitions. A reference in `troubleshooting.md` to `[installation]` resolves to the heading in `installation.md` because the publishing tool sees all included files as one document.

## Summary

| Component | Purpose | Example |
|-----------|---------|---------|
| Alias ID | Stable numeric identifier in combined command | `#200002` |
| Semantic slug | Human-readable link key derived from heading text | `getting-started` |
| Link reference definition | Bridges the slug to the alias ID | `[getting-started]: #200002 "Getting started"` |
| Cross-reference | Uses the semantic slug to link | `[Getting started][getting-started]` |

One reference pattern, every output context.
