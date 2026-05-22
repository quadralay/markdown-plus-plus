---
mdpp-version: 1.0
date: 2026-03-29
status: active
---

<!-- style:Heading1; markers:{"Keywords": "cross-references, aliases, links"}; #200001 -->
# Semantic cross-references

[semantic-cross-references]: #200001 "Semantic cross-references"

This example demonstrates how Markdown++ cross-references work across every output context -- standard Markdown viewers, standalone publishing, and multi-file composite assemblies.

## The pattern

Every linkable heading uses the **alias+slug+linkref triple** (see [GLOSSARY.md](../GLOSSARY.md#triple)):

1. A **combined command** with a style and a numeric alias ID
2. The **heading text** on the next line
3. A **link reference definition** that bridges a semantic slug to the alias ID

**The three pieces sit adjacent in source on every linkable heading:** directive line, heading line, blank line, link reference definition. The headings below show the shape -- copy this layout, do not collect the link reference definitions in a block at the bottom of the file. See [`references/best-practices.md` § Semantic Cross-References on Topic-Defining Headings](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings) for the full rationale.

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

The triple's main benefit is cross-context resolution -- the same reference works standalone, single-file, and assembled. Drift resistance is a second benefit, and it comes in two flavors: the alias decouples the link target from heading text (heading-rename drift), and the three pieces sit adjacent in source so they move as a unit when a section moves, is deleted, or reordered (section-move drift). The example below covers the heading-rename case. In standard Markdown, heading links are auto-generated from the heading text; rename a heading, and every link that points to it breaks. In Markdown++, the semantic slug and alias ID decouple the link target from the heading text.

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

<!-- style:Heading2; #sh-ug-pipeline -->
## Slug equals alias value (pipeline-generated anchors)

[sh-ug-pipeline]: #sh-ug-pipeline "Slug equals alias value (pipeline-generated anchors)"

When the alias is hand-authored from a publishing tool's numeric registry, the slug supplies the human-readable handle the alias lacks -- and the two values look different on purpose. When the alias is itself a unique-by-construction semantic identifier (generated by an authoring agent, a pipeline minting contextual IDs, or a hash-derived slug scheme), the link reference definition can reuse the alias value as its slug. That gives the heading one identifier instead of two, with no parallel naming vocabulary to keep in sync.

The H2 directly above this paragraph is itself an example of the variant: the alias is `#sh-ug-pipeline` and the link reference definition is `[sh-ug-pipeline]: #sh-ug-pipeline "..."`. Both forms are conformant under the same triple rules -- the only difference is whether the slug introduces a separate semantic name.

**Opaque alias + semantic slug** (the hand-authored pattern shown elsewhere in this file):

```markdown
<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"
```

**Slug equals alias value** (the pipeline-generated pattern):

```markdown
<!-- style:Heading2; #sh-ug-installation -->
## Installation

[sh-ug-installation]: #sh-ug-installation "Installation"
```

The alias is the only difference between the two forms. References from elsewhere in the assembly use the slug in each case (`[Installation][installation]` or `[Installation][sh-ug-installation]`), so the call-site shape is identical apart from the slug value. See [`references/best-practices.md` § *Choosing the slug*](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#choosing-the-slug) for the rule of thumb on when each variant fits.

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
