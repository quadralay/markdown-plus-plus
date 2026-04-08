---
name: markdown-plus-plus
description: >
  AUTHORITATIVE REFERENCE for Markdown++ syntax. Use when working with
  .md files containing <!--style:-->, <!--condition:-->, $variable;, <!--include:-->,
  <!--marker:-->, or <!--#alias--> patterns. Use for editing, validating,
  migrating, or auditing Markdown++ source documents.
---

<objective>

# markdown-plus-plus

Read and write Markdown++ documents - an extended Markdown format with variables, conditions, custom styles, file includes, and markers.

**Do not use training data for Markdown++.** This is an extended documentation format built on CommonMark. Markdown++ is fully backward compatible with CommonMark -- all extensions use HTML comment tags and are ignored by standard Markdown parsers. Use only this skill's references for extension syntax and behavior rules.
</objective>

<overview>

## Overview

Markdown++ extends CommonMark with HTML comment-based extensions. All extensions (except variables) use HTML comments for backward compatibility with standard Markdown renderers.

### Quick Reference

- **Variables**: `$variable_name;` -- Inline, reusable content
- **Styles**: `<!--style:Name-->` -- Block (above) or Inline (before)
- **Aliases**: `<!--#alias-name-->` -- Anchor for `[text](#alias-name)` links
- **Conditions**: `<!--condition:name-->...<!--/condition-->` -- Show/hide content by format
- **Includes**: `<!--include:path/to/file.md-->` -- Insert file contents
- **Markers**: `<!--markers:{"Key": "val"}-->` -- Metadata for search/processing
- **Multiline Tables**: `<!-- multiline -->` -- Enable block content in cells

</overview>

<syntax_examples>

## Syntax Examples

### Variables

Variables store reusable values across documents. They use `$name;` syntax (dollar sign, name, semicolon).

```markdown
Welcome to $product_name;, version $version;.
The **$product_name;** application supports...
```

**Rules:**
- Names must follow [Naming Rules](references/syntax-reference.md#naming-rules) (letter or underscore first)
- Must end with semicolon
- No spaces in variable names
- Case-sensitive: `$Product;` differs from `$product;`
- Escape with `\$` to prevent variable interpretation, or use inline code (`` `$name;` ``)

**Valid:** `$product_name;`, `$version-2;`, `$my_var;`
**Invalid:** `$product name;` (space), `$product` (no semicolon)

### Custom Styles

Styles override default formatting. Placement depends on element type.

**Block-level** (place on line directly above element, no blank line):
```markdown
<!--style:CustomHeading-->
# My Heading

<!--style:NoteBlock-->
> This is a styled blockquote.
```

**IMPORTANT:** Block commands must be attached to the element (no blank line between). A blank line breaks the association and passes through as a regular Markdown comment with no Markdown++ association/effect.

**Inline** (place immediately before the element, no space):
```markdown
This is <!--style:Emphasis-->**important text**.
```

See `references/syntax-reference.md` for nested list indentation rules and table styling.

### Custom Aliases

Aliases create stable internal link anchors. **Aliases are block-level only** -- they must appear on their own line above a block element, not inline.

```markdown
<!--#getting-started-->
## Getting Started

See [Getting Started](#getting-started) for an introduction.
```

**Cross-document links:** `[API Reference](api.md#authentication)`

**Rules:**
- Block-level only -- must be on its own line above a block element (inline aliases are not supported)
- Names must follow [Naming Rules](references/syntax-reference.md#naming-rules) (digit-first allowed for aliases)
- No spaces (alias ends at first space)
- Must start with `#` inside the comment
- Keep alias values unique within each file
- Must be attached to an element (no blank line between alias and element) -- same rule as styles

Use `scripts/add-aliases.py` to auto-generate aliases for headings.

### Conditions

Conditions show or hide content based on output format.

```markdown
<!--condition:web-->
Visit our [website](https://example.com) for updates.
<!--/condition-->
```

**Operators:** Space (AND), Comma (OR), Exclamation (NOT). Precedence: NOT > AND > OR.

```markdown
<!--condition:!draft,web production-->
Means: (!draft) OR (web AND production)
<!--/condition-->
```

**Inline:** `Contact us at <!--condition:web-->email<!--/condition--><!--condition:print-->the back cover<!--/condition-->.`

### File Includes

Insert content from other Markdown++ files.

```markdown
<!--include:shared/header.md-->
```

**Rules:** Paths relative to containing file. Recursive includes supported; circular includes detected and prevented. Must be alone on its line. Can be wrapped in conditions.

### Markers (Metadata)

Attach metadata to document elements for search, processing, or custom behavior.

**Single key-value:**
```markdown
<!--marker:Keywords="api, documentation"-->
```

**JSON format (multiple keys):**
```markdown
<!--markers:{"Keywords": "api, documentation", "Description": "API reference guide"}-->
```

**Index markers** create entries in generated indexes:
```markdown
<!--marker:IndexMarker="creating projects"-->
## Creating Projects
```

Format: `primary` for top-level, `primary:secondary` for nested, comma-separated for multiple entries. See `references/syntax-reference.md` for detailed marker examples.

### Multiline Tables

Enable block content (lists, blockquotes, styled elements) inside table cells.

```markdown
<!-- multiline -->
| Name | Details |
|------|---------|
| Bob  | Lives in Dallas. |
|      | - Enjoys cycling |
```

Empty first cell continues previous row; empty row separates records. Combine with style: `<!-- style:DataTable ; multiline -->`. See `references/syntax-reference.md` for multiline table rules.

### Combined Commands

Multiple commands in a single comment, separated by semicolons. Order: style, multiline, marker(s), #alias.

```markdown
<!-- style:CustomHeading ; marker:Keywords="intro" ; #introduction -->
# Introduction
```

### Inline Styling for Images and Links

```markdown
<!--style:CustomImage-->![Logo](images/logo.png "Company Logo")
[<!--style:CustomLink-->*Link text*](topics/file.md#anchor "Title")
```

### Content Islands (Blockquotes)

Blockquotes with custom styles create configurable content islands for callouts and notes.

```markdown
<!--style:BQ_Warning-->
> **Warning:** This is a styled warning block.
>
> Take note of the following:
> 1. First consideration
> 2. Second consideration
```

### Nested Lists with Styling

```markdown
<!--style:ProcedureList-->
1. First step
   - Sub-item A
   - Sub-item B
2. Second step
3. Third step
```

### Document Structure

**Topic map pattern** -- use includes to organize multi-chapter documents with conditional sections. See `references/examples.md` (Example 3) for a complete topic map example.

</syntax_examples>

<validation>

## Validation

Use the validation script to check Markdown++ syntax:

```bash
python scripts/validate-mdpp.py document.md
```

**Options:**
- `--verbose` - Show detailed output
- `--json` - Output errors as JSON
- `--strict` - Treat warnings as errors

**Common errors detected:**
- Unclosed condition blocks
- Invalid names — variables, styles, aliases, marker keys (see [Naming Rules](references/syntax-reference.md#naming-rules))
- Malformed marker JSON
- Circular file includes
- Duplicate alias values within a file
- Orphaned comment tags (tag not attached to element)

## Alias Generation

Generate unique aliases for headings:

```bash
python scripts/add-aliases.py document.md --levels 1,2,3
```

**Options:**
- `--levels` - Comma-separated heading levels to process (e.g., `1,2,3`)
- `--dry-run` - Preview changes without modifying file
- `--prefix` - Add prefix to generated aliases

See `references/syntax-reference.md` for complete syntax rules.

</validation>

<common_mistakes>

## Common Mistakes

### 1. Blank Line Breaks Tag Attachment (The Attachment Rule)

**This is the #1 source of Markdown++ errors.** A blank line between a comment tag and its target element silently breaks the association. The tag passes through as a regular HTML comment with no visible error. This applies to styles, aliases, markers, and combined commands equally. Only conditions (which wrap content) and includes (standalone directives) are exempt.

**Wrong -- blank line breaks attachment:**
```markdown
<!-- style:NoteBox -->

> This blockquote will NOT receive the style.
```

**Right -- tag directly above target, no blank line:**
```markdown
<!-- style:NoteBox -->
> This blockquote receives the style.
```

**Wrong -- tag below content (tags attach downward only):**
```markdown
## Getting Started
<!-- #getting-started -->
```

**Right -- tag above content:**
```markdown
<!-- #getting-started -->
## Getting Started
```

**Wrong -- stacked tags (top tag is orphaned):**
```markdown
<!-- style:CustomHeading -->
<!-- #my-alias -->
## Heading
```

**Right -- combine with semicolons:**
```markdown
<!-- style:CustomHeading ; #my-alias -->
## Heading
```

See the [Attachment Rule specification](../../../../spec/attachment-rule.md) for the formal definition and all edge cases.

### 2. Mismatched Indentation on Nested Lists

**Indentation of Markdown++ comment tags must match the content line.** In nested lists, if the comment tag is indented but the following content is not (or vice versa), the style passes through as a regular Markdown comment and is not applied.

### 3. Missing Semicolon on Variables

**Variables without a trailing semicolon are not recognized.** `$product_name` is literal text; `$product_name;` is a variable reference. The semicolon is required.

</common_mistakes>

<references>

## Reference Files

- `references/syntax-reference.md` - Detailed syntax rules, edge cases, and validation codes
- `references/examples.md` - Real-world document examples
- `references/best-practices.md` - Usage guidance, naming conventions, and common mistakes
- `../../../spec/formal-grammar.md` - Formal EBNF/PEG grammar for parser implementation
- `../../../spec/graceful-degradation.md` - Graceful degradation behavior in standard CommonMark renderers

</references>

<success_criteria>

## Success Criteria

- Markdown++ document uses correct syntax for all extensions
- All named entities follow [Naming Rules](references/syntax-reference.md#naming-rules)
- Conditions have matching opening and closing tags
- File includes use valid relative paths
- Markers contain valid JSON (for `markers:` format)
- No circular includes detected
</success_criteria>
