---
mdpp-version: 1.0
date: 2026-03-29
status: active
---

<!-- style:Heading1; #100001 -->
# Styles and variables

[styles-and-variables]: #100001 "Styles and variables"

This example demonstrates custom styles and variable references in Markdown++.

## Custom styles

<!-- style:Note -->
This paragraph is styled as a note. In a standard Markdown viewer, it renders as a normal paragraph. When processed by a publishing tool, the style directive maps it to the appropriate visual treatment.

<!-- style:Important -->
Important callouts use the same mechanism. The style name maps to output formatting defined in the publishing project.

<!-- style:Warning -->
Warnings can alert readers to potential data loss or security risks.

## Variables

The current product version is $product_version;. It was released on $release_date;.

For installation instructions, visit the $product_name; documentation portal.

Variables are defined centrally in the publishing project and resolved during output generation. In a Markdown viewer, they appear as literal text (e.g., `$product_version;`).

### Escaping variables

Two mechanisms prevent variable interpretation:

**Backslash escaping** -- use `\$` to produce a literal dollar sign:

\$not_a_variable; appears as literal text in published output.

**Inline code spans** -- content inside backticks is never treated as a variable:

Use the `$variable_name;` syntax to define reusable values.

## Content islands using blockquotes

<!--style:BQ_Tip-->
> **Tip: Preview your content**
>
> Markdown++ files render cleanly in any Markdown viewer. Use your editor's built-in preview to check content structure before publishing.

<!--style:BQ_Warning-->
> **Warning: Variable resolution**
>
> Undefined variables pass through as literal text in published output. Check your variable definitions if you see `$variable_name;` in generated pages.
