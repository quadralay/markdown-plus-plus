---
date: 2026-04-08
status: active
---

# Element Interactions

## Introduction

This document specifies how Markdown++ extensions interact with each standard CommonMark element. It defines the **style type taxonomy**, **default style names**, **compound naming rules** for nested containers, the **heading alias auto-generation algorithm**, and element-specific behavioral details that authors and implementors need to produce correct output.

The Markdown++ specification is composed of several documents, each covering a distinct aspect of the format:

- The [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) defines what each extension looks like -- the syntactic forms for styles, aliases, markers, variables, conditions, includes, and multiline tables.
- The [Attachment Rule](attachment-rule.md) defines how block-level and inline tags bind to content elements.
- The [Processing Model](processing-model.md) defines how extensions are evaluated at processing time -- the two-phase pipeline, evaluation order, scoping rules, and error behavior.
- The [Formal Grammar](formal-grammar.md) defines the EBNF grammar for all extension constructs.
- **This document** defines what happens *after* a style tag attaches to a specific element type -- what style type the element produces, what default name a processor generates, how compound names form when content is nested inside containers, and how heading aliases are auto-generated.

The conformance keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Style Type Taxonomy

Every CommonMark element that accepts a Markdown++ style tag maps to exactly one **style type**. The style type determines how output processors categorize and handle styled content. A conformant processor MUST assign the correct style type to each styled element.

Markdown++ defines four style types:

| Style Type | Description | Applies To |
|------------|-------------|------------|
| **Paragraph** | Text elements that occupy their own line or lines in the document flow. | Headings, titles, paragraphs, blockquotes, lists, code blocks, horizontal rules, block HTML, inline HTML |
| **Character** | Inline text elements that appear within a line of text, modifying a span of characters. | Bold, italic, strikethrough, code spans, links |
| **Graphic** | Embedded media elements that represent non-text content. | Images |
| **Table** | Tabular data elements with header and body cell structure. | Tables (standard and multiline) |

A processor MUST NOT assign an element to more than one style type. The style type is determined by the element type, not by the style name or tag content.

## Element Catalog

The following table provides a complete mapping from every supported CommonMark element to its style type, default style name(s), and style tag acceptance. This table is normative -- a conformant processor MUST use these default names when no custom style tag is present.

| Element | Style Type | Default Name(s) | Accepts Style Tag | Placement |
|---------|------------|------------------|:-----------------:|-----------|
| Setext heading (`===`) | Paragraph | Title 1 | Yes | Block |
| Setext heading (`---`) | Paragraph | Title 2 | Yes | Block |
| ATX heading (`#`) | Paragraph | Heading 1 | Yes | Block |
| ATX heading (`##`) | Paragraph | Heading 2 | Yes | Block |
| ATX heading (`###`) | Paragraph | Heading 3 | Yes | Block |
| ATX heading (`####`) | Paragraph | Heading 4 | Yes | Block |
| ATX heading (`#####`) | Paragraph | Heading 5 | Yes | Block |
| ATX heading (`######`) | Paragraph | Heading 6 | Yes | Block |
| Paragraph | Paragraph | Paragraph | Yes | Block |
| Blockquote | Paragraph | Blockquote | Yes | Block |
| Ordered list | Paragraph | OList, OList Item | Yes | Block |
| Unordered list | Paragraph | UList, UList Item | Yes | Block |
| Indented code block | Paragraph | Code Block | Yes | Block |
| Fenced code block | Paragraph | Code Fence | Yes | Block |
| Horizontal rule | Paragraph | Horizontal Rule | Yes | Block |
| Block HTML | Paragraph | Block HTML | Yes | Block |
| Inline HTML | Paragraph | Inline HTML | Yes | Inline |
| Bold (`**` / `__`) | Character | Bold | Yes | Inline |
| Italic (`*` / `_`) | Character | Italic | Yes | Inline |
| Strikethrough (`~~`) | Character | Strikethrough | Yes | Inline |
| Code span (`` ` ``) | Character | Code | Yes | Inline |
| Link (`[]()`) | Character | Link | Yes | Inline |
| Image (`![]()`) | Graphic | Image | Yes | Inline |
| Table | Table | Table, Table Cell Head, Table Cell Body | Yes | Block |

## Block-Level Elements

This section specifies how each block-level element interacts with Markdown++ style tags. All block-level elements produce **Paragraph** style type unless otherwise noted.

For all block-level elements, the style tag MUST appear on the line directly above the target element with no intervening blank line, as defined by the [Attachment Rule](attachment-rule.md).

### Setext Headings (Titles)

**Style type:** Paragraph
**Default names:** "Title 1" (double underline `===`), "Title 2" (single underline `---`)

Setext headings -- also called "titles" -- accept style tags. A custom style tag overrides the default name. Setext headings produce the same style type as ATX headings but use distinct default names.

A processor MUST assign "Title 1" to setext headings with double-underline (`===`) and "Title 2" to setext headings with single-underline (`---`).

```markdown
<!-- style:DocumentTitle -->
My Document Title
=================
```

The heading receives the custom style "DocumentTitle" (Paragraph type) instead of the default "Title 1".

```markdown
Chapter Overview
----------------
```

Without a style tag, this setext heading receives the default style "Title 2" (Paragraph type).

Setext headings also support alias auto-generation. See [Heading Alias Auto-Generation](#heading-alias-auto-generation) for the algorithm.

### ATX Headings

**Style type:** Paragraph
**Default names:** "Heading 1" through "Heading 6", corresponding to `#` through `######`

ATX headings accept style tags. A custom style tag overrides the default name. The heading level determines the default name: `#` maps to "Heading 1", `##` maps to "Heading 2", and so on through `######` mapping to "Heading 6".

A processor MUST assign the default name corresponding to the heading level when no custom style tag is present.

```markdown
<!-- style:ChapterHeading -->
## Chapter One
```

The heading receives the custom style "ChapterHeading" (Paragraph type) instead of the default "Heading 2".

```markdown
### Section Title
```

Without a style tag, this heading receives the default style "Heading 3" (Paragraph type).

ATX headings also support alias auto-generation. See [Heading Alias Auto-Generation](#heading-alias-auto-generation) for the algorithm.

### Paragraphs

**Style type:** Paragraph
**Default name:** "Paragraph"

Paragraphs accept style tags. A custom style tag overrides the default name.

A processor MUST assign "Paragraph" as the default style name when no custom style tag is present.

```markdown
<!-- style:Introduction -->
This is the introductory paragraph of the document.
```

The paragraph receives the custom style "Introduction" (Paragraph type) instead of the default "Paragraph".

### Indented Code Blocks

**Style type:** Paragraph
**Default name:** "Code Block"

Indented code blocks (four spaces or one tab of indentation) accept style tags. A custom style tag overrides the default name. Indented code blocks are distinct from fenced code blocks and use a different default name.

A processor MUST assign "Code Block" as the default style name for indented code blocks when no custom style tag is present.

```markdown
<!-- style:TerminalOutput -->
    $ ls -la
    total 48
    drwxr-xr-x  5 user group 4096 Apr  8 10:00 .
```

The code block receives the custom style "TerminalOutput" (Paragraph type) instead of the default "Code Block".

### Fenced Code Blocks

**Style type:** Paragraph
**Default name:** "Code Fence"

Fenced code blocks (delimited by `` ``` `` or `~~~`) accept style tags. A custom style tag overrides the default name. The language info string (e.g., `python`, `javascript`) is preserved as metadata independent of the style name.

A processor MUST assign "Code Fence" as the default style name for fenced code blocks when no custom style tag is present.

```markdown
<!-- style:CodeExample -->
```python
def hello():
    print("Hello, World!")
```
```

The code fence receives the custom style "CodeExample" (Paragraph type) instead of the default "Code Fence". The language info string `python` is preserved separately.

### Horizontal Rules

**Style type:** Paragraph
**Default name:** "Horizontal Rule"

Horizontal rules (`---`, `***`, or `___`) accept style tags. A custom style tag overrides the default name. Horizontal rules have no content -- the style controls only the visual presentation of the rule itself.

A processor MUST assign "Horizontal Rule" as the default style name when no custom style tag is present.

```markdown
<!-- style:SectionBreak -->
---
```

The horizontal rule receives the custom style "SectionBreak" (Paragraph type) instead of the default "Horizontal Rule".

## Heading Alias Auto-Generation

Both ATX headings and setext headings automatically generate an alias anchor from the heading text. This auto-generated alias enables cross-references within and between documents. Custom aliases created with `<!-- #name -->` supplement the auto-generated alias -- both are valid anchors for the heading.

### Algorithm

A conformant processor MUST generate heading aliases using the following algorithm. Given the heading's text content:

1. **Strip inline formatting.** Remove all inline markup (bold, italic, strikethrough, code spans, links, images) and retain only the plain text content. For links, retain the link text; for images, retain the alt text.
2. **Resolve variables.** If the heading contains variable references (`$name;`), use the resolved text after variable substitution.
3. **Convert to lowercase.** Convert all characters to their lowercase equivalents.
4. **Remove non-alphanumeric characters.** Remove all characters that are not ASCII letters (`a-z`), ASCII digits (`0-9`), or spaces.
5. **Replace spaces with hyphens.** Replace each sequence of one or more consecutive spaces with a single hyphen (`-`).
6. **Trim hyphens.** Remove any leading or trailing hyphens from the result.

If the result after step 6 is an empty string, no auto-generated alias is produced for that heading.

Unicode handling beyond ASCII is implementation-defined. A processor MAY extend steps 3-4 to support Unicode letters and digits, but MUST at minimum support ASCII as defined above.

### Examples

| Heading Text | Auto-Generated Alias |
|-------------|---------------------|
| `# Hello World` | `hello-world` |
| `# Let's Go to the Moon!` | `lets-go-to-the-moon` |
| `# Chapter 3 Setup` | `chapter-3-setup` |
| `# Hello   World` | `hello-world` |
| `# **Bold** Heading` | `bold-heading` |
| `# $product_name; User Guide` | *(depends on resolved variable value)* |
| `# ---` | *(no alias -- empty after processing)* |
| `## A & B: Partners` | `a-b-partners` |

### Relationship to Custom Aliases

Custom aliases created with `<!-- #name -->` are independent of auto-generated aliases. When a heading has both, both aliases are valid anchors:

```markdown
<!-- #getting-started -->
## Getting Started with $product_name;
```

This heading has two valid anchors:
- `getting-started` -- the custom alias
- The auto-generated alias (e.g., `getting-started-with-acme` if `$product_name;` resolves to "Acme")

A processor MUST NOT replace the auto-generated alias with a custom alias, and MUST NOT replace a custom alias with the auto-generated alias. Both MUST be available as valid link targets.

### Scope

Heading alias auto-generation applies to both ATX headings (`#` through `######`) and setext headings (`===` and `---` underlines). The algorithm is identical for both heading types.

### Duplicate Alias Resolution

When two or more headings in the assembled document produce the same auto-generated alias after the 6-step algorithm, a conformant processor MUST disambiguate by appending a counter suffix to subsequent occurrences:

1. The **first** heading in document order claims the bare alias (no suffix).
2. The **second** heading with the same alias receives the suffix `-2`.
3. The **third** receives `-3`, and so on for each subsequent duplicate.

The resulting suffixed alias MUST be unique across all aliases -- both auto-generated and custom -- already assigned in the document. If a candidate suffix collides with an existing alias, the processor MUST continue incrementing the counter until a unique alias is produced.

Document order is determined by the assembled document after Phase 1 processing (all includes are expanded, defined conditions are evaluated (Unset condition blocks pass through as-is), and variables are substituted). For multi-file documents, this follows the depth-first recursive include expansion order defined in the [Processing Model](processing-model.md).

This resolution is **silent** -- a conformant processor MUST NOT emit a diagnostic for auto-generated alias collisions. Unlike custom alias duplicates (which trigger [MDPP008](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md#mdpp008----duplicate-alias) as an error), auto-generated collisions are expected in documents that reuse heading text across sections.

#### Example

Given the following document:

```markdown
# Installation Guide

## Setup

Install the required packages.

## Configuration

Configure the application.

## Setup

Configure the database connection.

## Setup

Verify the installation.
```

A conformant processor produces the following auto-generated aliases:

| Heading | Auto-Generated Alias |
|---------|---------------------|
| `# Installation Guide` | `installation-guide` |
| `## Setup` (first) | `setup` |
| `## Configuration` | `configuration` |
| `## Setup` (second) | `setup-2` |
| `## Setup` (third) | `setup-3` |

All three Setup headings are independently addressable via their respective aliases: `#setup`, `#setup-2`, and `#setup-3`.

#### Interaction with Custom Aliases

Duplicate alias resolution applies only to auto-generated aliases. Custom aliases remain governed by MDPP008 -- duplicate custom aliases within a file are an error regardless of whether the auto-generated aliases would collide.

When a heading with a collision-suffixed auto-generated alias also has a custom alias, both are valid anchors. The custom alias supplements the suffixed auto-generated alias, consistent with the [alias supplement semantics](#relationship-to-custom-aliases):

```markdown
<!-- #db-setup -->
## Setup

Configure the database connection.
```

If this is the second `## Setup` heading in the document, the heading has two valid anchors:
- `db-setup` -- the custom alias
- `setup-2` -- the suffixed auto-generated alias

#### Custom Alias Priority

Custom aliases and auto-generated heading aliases occupy **separate namespaces**. When a custom alias (`<!-- #name -->`) on one element produces the same identifier string as an auto-generated heading alias on a different element, there is no collision -- both aliases exist independently. The auto-generated alias is NOT displaced or suffixed.

The distinction matters at **resolution time**: when a link references an ambiguous identifier (e.g., `[link](#setup)` where both a custom alias and an auto-generated alias resolve to `setup`), a conformant processor MUST resolve to the custom alias target. Custom aliases are intentionally assigned by the author as stable, permanent anchors. Auto-generated aliases are derived from heading text and change when the heading text changes. The intentional assignment wins at resolution time.

This resolution is **silent** -- a conformant processor MUST NOT emit a diagnostic when a custom alias and an auto-generated alias share the same identifier string. Unlike custom alias duplicates (which trigger [MDPP008](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md#mdpp008----duplicate-alias) as an error), custom-vs-auto-generated overlap is resolved by priority, not by suffixing.

##### Resolution Order

A conformant processor MUST check custom aliases before auto-generated heading aliases when resolving a link target. This ensures that custom aliases always win resolution priority regardless of document order.

Note: auto-generated aliases are still generated normally for all headings. The processor does not skip or modify auto-generation based on custom alias values. Priority applies only at the point of link resolution.

##### Example

Given the following document:

```markdown
<!-- #setup -->
## Installation

Install the required packages.

## Setup

Configure the application.
```

The custom alias `<!-- #setup -->` assigns the identifier `setup` to the "Installation" heading. The "Setup" heading auto-generates the slug `setup` independently. Both aliases exist:

| Heading | Anchors |
|---------|---------|
| `## Installation` | `installation` (auto-generated), `setup` (custom alias) |
| `## Setup` | `setup` (auto-generated) |

A link `[see setup](#setup)` resolves to the "Installation" heading because custom aliases take priority over auto-generated aliases. The "Setup" heading remains addressable by its auto-generated alias when no custom alias competes for the same identifier in a given resolution context, or by any other custom alias explicitly assigned to it.

##### Reverse Document Order

Custom alias priority applies regardless of document order. Even when the heading with the overlapping auto-generated alias appears first, the custom alias still wins at resolution time:

```markdown
## Setup

Configure the application.

<!-- #setup -->
## Installation

Install the required packages.
```

Both headings have an alias resolving to `setup`, but the custom alias takes priority:

| Heading | Anchors |
|---------|---------|
| `## Setup` | `setup` (auto-generated, de-prioritized by custom alias) |
| `## Installation` | `installation` (auto-generated), `setup` (custom alias) |

A link `[see setup](#setup)` resolves to the "Installation" heading regardless of document order.

##### Interaction with Duplicate Auto-Generated Resolution

Custom alias priority composes with [duplicate auto-generated alias resolution](#duplicate-alias-resolution). Duplicate auto-generated aliases within the auto-generated namespace still receive counter suffixes as normal. Custom alias priority then applies separately at resolution time.

Given the following document:

```markdown
<!-- #setup -->
## Installation

Install the required packages.

## Setup

Configure the application.

## Setup

Verify the installation.
```

A conformant processor produces the following aliases:

| Heading | Anchors |
|---------|---------|
| `## Installation` | `installation` (auto-generated), `setup` (custom alias) |
| `## Setup` (first) | `setup` (auto-generated, de-prioritized by custom alias) |
| `## Setup` (second) | `setup-2` (suffixed -- duplicate auto-generated resolution) |

The first `## Setup` heading keeps its bare auto-generated alias `setup` because it is the first heading to produce that slug. The second `## Setup` heading receives `setup-2` per the normal [duplicate alias resolution](#duplicate-alias-resolution) algorithm. The custom alias `setup` on "Installation" does not affect auto-generation -- it only wins at resolution time when a link targets `#setup`.

## Container Elements

Container elements -- blockquotes and lists -- hold nested content. When a style tag is applied to a container, it affects both the container itself and the style names generated for nested content through **compound naming**.

### Blockquotes

**Style type:** Paragraph
**Default name:** "Blockquote"

Blockquotes act as **content islands** -- self-contained content blocks that can hold headings, paragraphs, lists, code blocks, and other Markdown++ extensions. A style tag on a blockquote overrides the container's default name and affects compound names for all nested content.

A processor MUST assign "Blockquote" as the default style name when no custom style tag is present.

```markdown
<!-- style:NoteBox -->
> This is a styled blockquote.
> It can contain multiple paragraphs.
>
> > Nested blockquotes are also supported.
```

The blockquote receives the custom style "NoteBox" (Paragraph type). Content nested inside the blockquote receives compound style names (see [Compound Style Naming](#compound-style-naming)).

### Ordered Lists

**Style type:** Paragraph
**Default names:** "OList" (list container), "OList Item" (list items)

Ordered lists accept style tags. A custom style tag overrides both the container name and the item name prefix. Nested content within list items receives compound style names.

A processor MUST assign "OList" as the default container name and "OList Item" as the default item name when no custom style tag is present.

```markdown
<!-- style:StepList -->
1. First step
2. Second step
3. Third step
```

The list container receives "StepList" and list items receive "StepList Item".

### Unordered Lists

**Style type:** Paragraph
**Default names:** "UList" (list container), "UList Item" (list items)

Unordered lists accept style tags. A custom style tag overrides both the container name and the item name prefix. Nested content within list items receives compound style names.

A processor MUST assign "UList" as the default container name and "UList Item" as the default item name when no custom style tag is present.

```markdown
<!-- style:FeatureList -->
- Feature one
- Feature two
- Feature three
```

The list container receives "FeatureList" and list items receive "FeatureList Item".

#### Unlike-Marker List Breaking

In CommonMark, unordered list items can use `-`, `*`, or `+` as markers. When the marker character changes between consecutive items, the list is broken into separate lists. Each segment is an independent list with its own style scope.

```markdown
- Item with dash
- Another dash item
* Item with asterisk
* Another asterisk item
```

This produces two separate unordered lists: one with the first two items (using `-`) and one with the last two items (using `*`). Each list receives its own default "UList" style independently.

### Nested List Styling

For nested lists, the style tag MUST be indented to match the nesting level of the target list item, as defined by the [Attachment Rule](attachment-rule.md).

```markdown
<!-- style:BulletList1 -->
- Outer item

  <!-- style:BulletList2 -->
  - Nested item

    <!-- style:BulletList3 -->
    - Deeply nested item
```

Each nesting level requires its own style tag. See [Nested List Style Non-Inheritance](#nested-list-style-non-inheritance) for why styles do not cascade across nesting levels.

## Compound Style Naming

When content is nested inside a styled container (blockquote or list), the style names for nested elements are **compound names** -- formed by combining the container's style name with the nested element's style name.

### Naming Rule

A processor MUST generate compound style names using the following rule:

> **Compound name = ContainerStyle + space + ElementStyle**

Where:
- **ContainerStyle** is the container's custom style name (or default name if no custom style is applied)
- **ElementStyle** is the nested element's custom style name if a style tag is present, or the default style name if no custom style tag is applied

The two components are joined by a single space character. This rule applies recursively at each container boundary.

### List Item Naming Sub-Rule

List items are a special case of compound naming. When a style tag is applied to a list (ordered or unordered), the list items receive a name formed by appending the fixed suffix **"Item"** to the list's style name:

> **List item name = ListStyle + space + "Item"**

Where **ListStyle** is the custom style name if a style tag is present, or the default name ("OList" or "UList") if no custom style is applied.

A processor MUST generate list item names using this sub-rule:

| List Type | Style Tag | Container Name | Item Name |
|-----------|-----------|----------------|-----------|
| Ordered | *(none)* | OList | OList Item |
| Unordered | *(none)* | UList | UList Item |
| Ordered | `<!-- style:StepList -->` | StepList | StepList Item |
| Unordered | `<!-- style:FeatureList -->` | FeatureList | FeatureList Item |

The "Item" suffix is a fixed structural component -- it is not a style name that authors can independently customize. There is no mechanism to apply a separate style tag to individual list items to change the "Item" portion of the name. The item name is always derived from the list container's style.

This sub-rule is distinct from the general compound naming rule, which governs content nested *within* list items (paragraphs, headings, code blocks, etc.). Both rules can apply simultaneously. For example, given a styled ordered list that contains a paragraph within a list item:

```markdown
<!-- style:StepList -->
1. First step

   This paragraph provides additional detail.

2. Second step
```

The names produced are:

| Element | Name | Rule Applied |
|---------|------|--------------|
| List container | StepList | Custom style tag |
| List items | StepList Item | List item naming sub-rule |
| Nested paragraph | StepList Paragraph | General compound naming rule |

The list item naming sub-rule applies identically to ordered and unordered lists. The only difference is the default container name ("OList" vs. "UList") when no custom style tag is present.

### Compound Names and Identifier Validation

Compound style names contain embedded spaces (e.g., `"Blockquote Heading 1"`) and conform to the **style/marker name** pattern (`[a-zA-Z_][a-zA-Z0-9_\- ]*`, trimmed). This pattern was introduced specifically to support processor-defined compound names and legacy systems with space-embedded style names. Each component of a compound name MUST individually conform to the standard identifier rule defined in the [Naming Rules](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md#naming-rules), and the composed result is validated as a style/marker name with embedded spaces.

### Examples

| Container | Nested Element | Compound Name |
|-----------|---------------|---------------|
| Blockquote (default) | Heading 1 | Blockquote Heading 1 |
| Blockquote (default) | Paragraph | Blockquote Paragraph |
| CustomBQ (custom) | Paragraph | CustomBQ Paragraph |
| CustomBQ (custom) | CustomParagraph (custom) | CustomBQ CustomParagraph |
| OList (default) | Paragraph | OList Paragraph |
| OList (default) | CustomParagraph (custom) | OList CustomParagraph |
| UList (default) | Heading 2 | UList Heading 2 |

### Blockquote Compound Naming

```markdown
<!-- style:NoteBox -->
> ## Section Inside Note
>
> This paragraph is inside the note.
```

The blockquote receives "NoteBox". The nested elements receive compound names:
- The heading receives "NoteBox Heading 2"
- The paragraph receives "NoteBox Paragraph"

With both container and content styled:

```markdown
<!-- style:NoteBox -->
> <!-- style:NoteHeading -->
> ## Custom Heading
>
> Regular paragraph inside note.
```

- The heading receives "NoteBox NoteHeading"
- The paragraph receives "NoteBox Paragraph"

### List Compound Naming

```markdown
<!-- style:StepList -->
1. First step

   Additional paragraph in the first item.

2. Second step
```

- The list container receives "StepList"
- List items receive "StepList Item"
- The nested paragraph receives "StepList Paragraph"

### Recursive Compounding

Compound naming applies recursively at each container boundary. When containers are nested inside other containers, each level adds its name as a prefix.

```markdown
> > Deeply nested paragraph.
```

With default styles, the inner paragraph receives:
- Outer blockquote contributes: "Blockquote"
- Inner blockquote contributes: "Blockquote"
- Paragraph contributes: "Paragraph"
- Result: "Blockquote Blockquote Paragraph"

With custom styles:

```markdown
<!-- style:Outer -->
> <!-- style:Inner -->
> > This is a deeply nested paragraph.
```

- Result for the paragraph: "Outer Inner Paragraph"

There is no depth limit on recursive compounding. A processor MUST apply the compound naming rule at every container boundary regardless of nesting depth.

### Nested List Style Non-Inheritance

Nested lists do **not** inherit the parent list's custom style. Each nesting level MUST receive its own style tag to get a custom name. Without a style tag, nested content uses the default compound name.

```markdown
<!-- style:MainList -->
- Outer item
  - Inner item (does NOT inherit "MainList")
```

The outer list receives "MainList". The inner list receives the default "UList" -- **not** "MainList". The inner items receive the compound name "MainList UList Item" (the outer custom name combined with the inner default name).

To apply a custom style to a nested list:

```markdown
<!-- style:MainList -->
- Outer item

  <!-- style:SubList -->
  - Inner item (receives "SubList")
```

Now the inner list receives "SubList", and inner items receive "MainList SubList Item".

A processor MUST NOT propagate a container's custom style to nested containers. Each container boundary requires an explicit style tag for customization.

## Inline Elements

Inline elements appear within a line of text. Inline style tags MUST appear immediately before the styled element on the same line, with no space between the closing `-->` and the element, as defined by the [Attachment Rule](attachment-rule.md).

**Link exception:** Links are an exception to this general placement rule. For links, the style tag is placed *inside* the link text brackets (`[...]`), not immediately before the opening bracket. See [Links](#links) for the full rule and rationale.

### Bold, Italic, Strikethrough, and Code Spans

**Style type:** Character
**Default names:** "Bold", "Italic", "Strikethrough", "Code"

These inline formatting elements accept inline style tags. A custom style tag overrides the default name. The style type is Character -- distinct from block-level elements, which produce Paragraph type.

A processor MUST assign the Character style type to all inline formatting elements.

```markdown
This is <!--style:Emphasis-->**important text** in a paragraph.

Use <!--style:KeyboardInput-->`Ctrl+C` to copy.

This is <!--style:Highlight-->*emphasized text* for clarity.

This text has <!--style:Removed-->~~deprecated content~~ in it.
```

- The bold text receives "Emphasis" (Character type) instead of the default "Bold"
- The code span receives "KeyboardInput" (Character type) instead of the default "Code"
- The italic text receives "Highlight" (Character type) instead of the default "Italic"
- The strikethrough receives "Removed" (Character type) instead of the default "Strikethrough"

### Links

**Style type:** Character
**Default name:** "Link"

Links accept inline style tags. Links produce Character style type.

A processor MUST assign "Link" as the default style name and Character as the style type for links.

#### Placement Exception

Links are the **one exception** to the general inline placement rule. For all other inline elements (bold, italic, strikethrough, code spans, images), the style tag appears immediately *before* the element's opening delimiter. For links, the style tag MUST be placed **inside the link text brackets**, before the link text content:

```
General inline rule:  <!--style:Name-->**element**
Link exception:       [<!--style:Name-->link text](url)
```

The tag appears after the opening `[` and before the link text. This placement is required because the style applies to the *text content* of the link, not to the link as a structural element. Placing the tag before the opening `[` is not valid for link styling.

A processor MUST recognize style tags inside link text brackets. A processor MUST NOT require style tags to appear before the opening `[` of a link.

#### Examples

```markdown
See the [<!--style:APILink-->**API Reference**](api.md#auth) for details.

Read the [<!--style:ExternalLink-->documentation](https://example.com).
```

- The first link receives "APILink" (Character type) instead of the default "Link"
- The second link receives "ExternalLink" (Character type) instead of the default "Link"

#### Comparison with Other Inline Elements

| Element | Style Tag Placement | Example |
|---------|-------------------|---------|
| Bold | Before element | `<!--style:Name-->**text**` |
| Italic | Before element | `<!--style:Name-->*text*` |
| Strikethrough | Before element | `<!--style:Name-->~~text~~` |
| Code span | Before element | `` <!--style:Name-->`text` `` |
| Image | Before element | `<!--style:Name-->![alt](src)` |
| **Link** | **Inside brackets** | `[<!--style:Name-->text](url)` |

#### Cross-Document Alias Linking

Links can reference aliases in other documents using the standard Markdown link syntax with a fragment identifier:

```markdown
See [Getting Started](other-doc.md#getting-started) for setup instructions.
```

The fragment `#getting-started` references an alias (either auto-generated or custom) in `other-doc.md`. Cross-document alias linking works with both auto-generated heading aliases and custom aliases created with `<!-- #name -->`.

### Images

**Style type:** Graphic
**Default name:** "Image"

Images accept inline style tags. Images are the only element type that produces **Graphic** style type -- all other styled elements produce Paragraph, Character, or Table type.

A processor MUST assign "Image" as the default style name and Graphic as the style type for images.

```markdown
<!--style:Screenshot-->![Settings Screen](images/settings.png)

<!--style:Logo-->![Company Logo](images/logo.png "Company Logo")
```

- The first image receives "Screenshot" (Graphic type) instead of the default "Image"
- The second image receives "Logo" (Graphic type) instead of the default "Image"

## Tables

**Style type:** Table
**Default names:** "Table", "Table Cell Head", "Table Cell Body"

Tables accept style tags and produce **Table** style type. A single style tag on a table generates three style names in the output: one for the table itself, one for header cells, and one for body cells.

A processor MUST generate three style names from a table's style:

| Component | Default Name | Custom Name Pattern |
|-----------|-------------|-------------------|
| Table container | Table | *Name* |
| Header cells | Table Cell Head | *Name* Cell Head |
| Body cells | Table Cell Body | *Name* Cell Body |

Where *Name* is the custom style name (or "Table" if no custom style is applied).

```markdown
<!-- style:DataTable -->
| Feature | Status |
|---------|--------|
| API     | Active |
| CLI     | Beta   |
```

This table generates three style names:
- "DataTable" -- for the table container
- "DataTable Cell Head" -- for the header cells ("Feature", "Status")
- "DataTable Cell Body" -- for the body cells ("API", "Active", "CLI", "Beta")

Without a custom style:

```markdown
| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
```

This table uses the defaults: "Table", "Table Cell Head", "Table Cell Body".

### Multiline Tables

The three-name generation pattern applies identically to both standard tables and multiline tables. The `multiline` directive is a processing instruction that affects how cell content is parsed -- it does not change the naming behavior.

```markdown
<!-- style:PersonTable ; multiline -->
| Name | Details          |
|------|------------------|
| Bob  | Lives in Dallas. |
|      | - Enjoys cycling |
```

This generates "PersonTable", "PersonTable Cell Head", and "PersonTable Cell Body" -- the same pattern as a standard table.

## Block HTML and Inline HTML

**Style type:** Paragraph
**Default names:** "Block HTML", "Inline HTML"

Block HTML and inline HTML elements accept style tags. However, the availability of HTML element styling in output MAY depend on the output format. A processor SHOULD apply style tags to HTML elements when the output format supports it, and MAY omit styling when the output format does not support it (e.g., PDF output).

```markdown
<!-- style:CustomHTML -->
<div class="notice">
  This is a custom HTML block.
</div>
```

The block HTML element receives "CustomHTML" (Paragraph type) when the output format supports HTML styling.

A processor MUST recognize style tags on HTML elements regardless of output format. Whether the style has a visible effect in the rendered output is output-format dependent.

## Table of Contents Integration

This section is **informational** (SHOULD-level), not normative (MUST-level). Table of contents generation is output-specific behavior that varies across processors and output formats.

### Heading Level to TOC Depth Mapping

A processor that generates a table of contents SHOULD map heading levels to TOC depth as follows:

| Heading | TOC Depth |
|---------|:---------:|
| Heading 1 / Title 1 | 1 |
| Heading 2 / Title 2 | 2 |
| Heading 3 | 3 |
| Heading 4 | 4 |
| Heading 5 | 5 |
| Heading 6 | 6 |

### Custom Styles and TOC

Custom heading styles do not change the heading's level for TOC purposes. A `## Heading` with a custom style is still a level-2 heading in the TOC hierarchy. How custom heading styles interact with TOC presentation (e.g., formatting of TOC entries) is processor-defined.

## Relationship to Other Specifications

This document is part of the Markdown++ specification suite. The following table summarizes how the specifications relate:

| Document | Defines | This Spec Depends On |
|----------|---------|---------------------|
| [Syntax Reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) | Extension syntax, naming rules, placement rules | Style tag syntax, naming rule for individual identifiers |
| [Attachment Rule](attachment-rule.md) | How tags bind to content elements | Block and inline attachment mechanics |
| [Processing Model](processing-model.md) | Evaluation pipeline, variable substitution, condition evaluation | Output model (annotated document tree) |
| [Formal Grammar](formal-grammar.md) | EBNF grammar for extension constructs | Grammar productions for style, alias, and marker commands |
| **Element Interactions** (this document) | Style types, default names, compound naming, alias generation | -- |

The processing pipeline defined by the [Processing Model](processing-model.md) produces "a CommonMark document tree annotated with Markdown++ metadata." This document defines what that metadata looks like for each element type -- the style type, default name, and compound naming behavior that annotate each node in the output tree.
