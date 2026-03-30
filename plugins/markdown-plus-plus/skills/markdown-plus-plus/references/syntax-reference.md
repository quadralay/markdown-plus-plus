---
date: 2026-03-29
status: active
---

# Markdown++ Syntax Reference

Complete reference for all Markdown++ extensions. This document provides detailed syntax rules, edge cases, and validation requirements.

## Base Specification

Markdown++ extends **CommonMark 0.30** with additional features. Standard CommonMark syntax works as expected. GitHub Flavored Markdown (GFM) tables are also supported. All extensions use HTML comments or inline tokens that standard renderers treat as invisible -- Markdown++ files remain valid `.md` documents that work in any Markdown tool.

## Attachment Rules

Markdown++ comment tags must be **associated with a paragraph element** -- they cannot float alone separated by whitespace. A blank line between a comment tag and its element breaks the association, causing the tag to pass through as a regular HTML comment with no Markdown++ effect.

The following table summarizes attachment requirements for each command type:

| Command | Attachment Required | Blank Line Permitted | Can Be Standalone |
|---------|:-------------------:|:--------------------:|:-----------------:|
| Styles (`style:`) | Yes | No | No |
| Aliases (`#name`) | Yes | No | No |
| Markers (`marker:`/`markers:`) | Yes | No | No |
| Conditions (`condition:`) | N/A (wraps content) | Yes (within block) | Yes |
| Includes (`include:`) | N/A (standalone directive) | N/A | Yes |
| Multiline (`multiline`) | Yes (above table) | No | No |

**Correct -- tag attached to element (no blank line):**
```markdown
<!-- marker:IndexMarker="setup" ; #getting-started -->
## Getting Started
```

**Correct -- document-level markers attached to the Title paragraph:**
```markdown
<!-- markers:{"Keywords": "api, docs", "Description": "API reference"} -->
Heading Title
=============
```

**Wrong -- blank line breaks the association:**
```markdown
## Getting Started

<!-- marker:IndexMarker="setup" ; #getting-started -->

This paragraph will not receive the marker or alias.
```

---

## Variables

### Syntax

```
$variable_name;
```

### Rules

| Rule | Description |
|------|-------------|
| Start | Must begin with `$` |
| Name | Alphanumeric characters, hyphens (`-`), underscores (`_`) |
| End | Must end with semicolon (`;`) |
| Spaces | Not allowed in variable names |
| Case | Case-sensitive (`$Product;` ≠ `$product;`) |
| Length | No explicit limit, but keep names reasonable |
| Escaping | Use `\$` to prevent variable interpretation |

### Valid Examples

```markdown
$product_name;
$version;
$release-date;
$my_var_2;
$_internal;
```

### Invalid Examples

```markdown
$product name;     # Space in name
$product           # Missing semicolon
$123start;         # Cannot start with number (recommended)
$ variable;        # Space after $
```

### Usage Context

Variables can appear:
- In paragraphs: `Welcome to $product_name;.`
- In headings: `# $product_name; User Guide`
- In lists: `- Version: $version;`
- In links: `[$product_name;](https://example.com)`
- Inside formatting: `**$product_name;**`

Variables remain as literals in the source and are resolved during publishing by a processing tool.

---

## Custom Styles

### Syntax

```
<!--style:StyleName-->
```

### Placement Rules

| Element Type | Placement | Example |
|--------------|-----------|---------|
| Block (heading, paragraph, list, blockquote, code block, table) | Line directly above, no blank line | See below |
| Inline (bold, italic, link, code span) | Immediately before, no space | See below |

### Block-Level Placement

```markdown
<!--style:CustomHeading-->
# Heading Text

<!--style:NoteBlock-->
> Blockquote content

<!--style:CodeExample-->
```python
code here
```

<!--style:CustomList-->
- Item 1
- Item 2

<!--style:CustomTable-->
| A | B |
|---|---|
| 1 | 2 |
```

**Important:** Block commands must be attached to the element (no blank line between). Comment tags must be associated with a paragraph - they cannot float alone separated by whitespace.

**Wrong - blank line breaks the association:**
```markdown
<!--style:CustomHeading-->

# Heading Text
```

### Nested List Styling

For nested lists, use proper indentation to match the list level:

```markdown
<!-- style:BulletList1 -->
- Bullet 1

  <!-- style:BulletList2 -->
  - Bullet 2

    <!-- style:BulletList3 -->
    - Bullet 3
```

The style comment tag must be indented to match the nested list item.

### Inline Placement

```markdown
This is <!--style:Emphasis-->**bold text**.
Use <!--style:Code-->`inline code` here.
Click <!--style:Link-->[here](url) to continue.
```

**Wrong - space breaks the association:**
```markdown
This is <!--style: Emphasis--> **bold text**.
```

### Style Name Rules

| Rule | Description |
|------|-------------|
| Characters | Alphanumeric, hyphens, underscores |
| Spaces | Not allowed in style names |
| Case | Typically PascalCase by convention |

---

## Custom Aliases

### Syntax

```
<!--#alias-name-->
```

### Rules

| Rule | Description |
|------|-------------|
| Start | Must begin with `#` inside the comment |
| Name | Alphanumeric, hyphens, underscores |
| Spaces | Not allowed (alias ends at first space) |
| Case | Case-sensitive |

### Creating Aliases

Place the alias tag on the line directly above the target element with **no blank line** between them. See [Attachment Rules](#attachment-rules) for placement requirements.

```markdown
<!--#introduction-->
## Introduction

This is the introduction section.
```

### Using Aliases in Links

```markdown
# Same document
See [Introduction](#introduction) for details.

# Cross-document
See [API Auth](api-reference.md#authentication) for auth info.
```

**Note:** Reference-style links (`[text][ref]` with `[ref]: url`) are supported but generally not recommended. See the **Advanced Patterns** section in [best-practices.md](best-practices.md#link-references) for guidance on when to use them.

### Alias vs. Heading IDs

Standard Markdown auto-generates IDs from headings. Custom aliases:
- Override the auto-generated ID
- Allow multiple aliases per element
- Work on non-heading elements

---

## Conditions

### Syntax

```
<!--condition:expression-->
content
<!--/condition-->
```

### Condition Expressions

| Operator | Symbol | Meaning | Precedence |
|----------|--------|---------|------------|
| NOT | `!` | Negate condition | Highest (1) |
| AND | space | All must be visible | Medium (2) |
| OR | `,` | Any can be visible | Lowest (3) |

### Expression Examples

| Expression | Interpretation |
|------------|----------------|
| `web` | Show when "web" is visible |
| `!web` | Show when "web" is hidden |
| `web print` | Show when "web" AND "print" are visible |
| `web,print` | Show when "web" OR "print" is visible |
| `!internal,web` | Show when "internal" is hidden OR "web" is visible |
| `!draft,web production` | `(!draft) OR (web AND production)` |

### Condition Name Rules

| Rule | Description |
|------|-------------|
| Characters | Alphanumeric, hyphens, underscores |
| Spaces | Separator for AND operator |
| Commas | Separator for OR operator |
| Case | Condition names are case-sensitive |

### Block Conditions

```markdown
<!--condition:web-->
## Web-Only Section

This entire section only appears in web output.

- Web feature 1
- Web feature 2
<!--/condition-->
```

### Inline Conditions

```markdown
Contact us at <!--condition:web-->[email](mailto:x@x.com)<!--/condition--><!--condition:print-->the address below<!--/condition-->.
```

### Nesting Conditions

Conditions can be nested:

```markdown
<!--condition:web-->
## Web Content

<!--condition:production-->
This appears in web AND production.
<!--/condition-->

<!--/condition-->
```

### Common Errors

| Error | Problem |
|-------|---------|
| Missing closing tag | `<!--condition:web-->` without `<!--/condition-->` |
| Typo in closing | `<!--condition-->` instead of `<!--/condition-->` |
| Mismatched nesting | Overlapping conditions |

---

## File Includes

### Syntax

```
<!--include:path/to/file.md-->
```

### Path Resolution

Paths are **relative to the containing file's directory**.

| File Location | Include Statement | Resolves To |
|---------------|-------------------|-------------|
| `docs/guide.md` | `<!--include:intro.md-->` | `docs/intro.md` |
| `docs/guide.md` | `<!--include:shared/header.md-->` | `docs/shared/header.md` |
| `docs/guide.md` | `<!--include:../common/footer.md-->` | `common/footer.md` |

### Rules

| Rule | Description |
|------|-------------|
| Placement | Must be alone on its line |
| Path | Relative to containing file |
| Extension | Typically `.md` but any text file works |
| Recursion | Included files can include other files |
| Circular | Circular includes are detected and prevented |

### Conditional Includes

```markdown
<!--condition:advanced-->
<!--include:advanced-topics.md-->
<!--/condition-->
```

### Include Processing

Included content:
- Is parsed for Markdown++ extensions
- Inherits variable context from parent
- Maintains relative paths for nested includes

### Error Handling

| Condition | Behavior |
|-----------|----------|
| File not found | Warning; include tag passes through as HTML comment |
| Circular include | Error; include is skipped with warning |

---

## Markers (Metadata)

### Syntax Options

**Preferred format (single key-value):**
```
<!--marker:Key="value"-->
```

**JSON format (multiple keys):**
```
<!--markers:{"Key1": "value1", "Key2": "value2"}-->
```

Use `marker:key="value"` for single markers, JSON format for multiple.

### JSON Format Rules

- Must be valid JSON object
- Keys and string values in double quotes
- Supports strings, numbers, booleans, arrays

```markdown
<!--markers:{"Keywords": "api, docs", "Priority": 1, "Published": true}-->
```

### Simple Format Rules

- Key followed by `=` and quoted value
- Value in double quotes
- No spaces around `=`

```markdown
<!--marker:Keywords="api, documentation"-->
```

### Placement

Markers must be on the line directly above the target element with no blank line between. See [Attachment Rules](#attachment-rules) for placement requirements.

At the start of a file, markers are typically placed above the Title paragraph -- they are attached to the Title, not floating standalone.

**Correct -- marker attached to heading:**
```markdown
<!-- marker:IndexMarker="setup:initial" -->
### Installation
```

**Correct -- marker attached to Title paragraph at document start:**
```markdown
<!-- markers:{"Keywords": "api", "Description": "API guide"} -->
API Reference
=============
```

### Common Use Cases

| Marker | Purpose |
|--------|---------|
| `Keywords` | Search keywords, maps to HTML meta tags in web output |
| `Description` | Document description, maps to HTML meta tags in web output |
| `IndexMarker` | Index entries (see below) |
| `Author` | Document author |
| `Category` | Content categorization |
| `Passthrough` | Content that bypasses processing |

### Index Markers

Index markers create entries in generated indexes (back-of-book style).

**Single entry:**
```markdown
<!--marker:IndexMarker="creating projects"-->
## Creating Projects
```

**Multiple entries** (comma-separated):
```markdown
<!--marker:IndexMarker="projects:creating,output:generating,targets"-->
```

**Sub-entries** (colon for nesting):
```markdown
<!--marker:IndexMarker="source documents:opening,documents:opening from Manager"-->
```

**Format:**
- `primary` -- Top-level index entry
- `primary:secondary` -- Nested entry appears under primary
- Comma separates multiple independent entries

---

## Multiline Tables

### Syntax

```
<!-- multiline -->
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell content here        |
|          | - Continuation line 1    |
|          | - Continuation line 2    |
|          |                          |
| Cell 2   | Next row starts here     |
```

### Structure Rules

Multiline tables use a specific row structure:

1. **First content row** - Contains the row identifier in the first cell
2. **Continuation rows** - Empty first cell (`|          |`) continues the previous row
3. **Row separator** - Empty row with cell borders separates table rows

### Basic Example

```markdown
<!-- multiline -->
| Name | Details                  |
|------|--------------------------|
| Bob  | Lives in Dallas.         |
|      | - Enjoys cycling         |
|      | - Loves cooking          |
|      |                          |
| Mary | Lives in El Paso.        |
|      | - Works as a teacher     |
|      | - Likes painting         |
```

### Lists in Cells

```markdown
<!-- multiline -->
| Feature    | Capabilities             |
|------------|--------------------------|
| Variables  | Reusable content:        |
|            | - Product names          |
|            | - Version numbers        |
|            | - URLs                   |
|            |                          |
| Conditions | Control visibility:      |
|            | 1. Platform-specific     |
|            | 2. Output format         |
|            | 3. Audience level        |
```

### Blockquotes in Cells

```markdown
<!-- multiline -->
| Topic   | Notes                    |
|---------|--------------------------|
| Warning | Important information:   |
|         | > **Note:** Be careful   |
|         | > when editing configs.  |
|         |                          |
| Tip     | Helpful hint:            |
|         | > Use aliases for stable |
|         | > URL endpoints.         |
```

### Styled Content in Cells

Block styles go on the preceding line, then the styled content follows:

```markdown
<!-- multiline -->
| Name | Details                  |
|------|--------------------------|
| Bob  | Lives in Dallas.         |
|      | <!-- style:Hobbies -->   |
|      | - Enjoys cycling         |
|      | - Loves cooking          |
|      |                          |
| Mary | Lives in El Paso.        |
|      | - Works as a teacher     |
```

For inline styles, no space between command and element:

```markdown
<!-- multiline -->
| Topic | Description              |
|-------|--------------------------|
| Intro | This is                  |
|       | <!--style:Emphasis-->**important** text. |
```

### Alignment

Standard Markdown alignment syntax works:

```markdown
<!-- multiline -->
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| L-align  | Centered | R-align  |
|          | text     | content  |
```

### With Custom Styles

```markdown
<!-- style:DataTable ; multiline -->
| Feature | Description              |
|---------|--------------------------|
| API     | REST endpoints.          |
|         | - GET /users             |
|         | - POST /users            |
|         |                          |
| Auth    | OAuth 2.0 support.       |
```

---

## Combined Commands

### Syntax

Multiple commands in one comment, separated by semicolons:

```
<!-- command1 ; command2 ; command3 -->
```

### Order Priority

When combining commands, use this order for consistency:

1. `style:StyleName` - Custom style
2. `multiline` - Multiline table indicator
3. `marker:Key="value"` - Markers (one or more)
4. `#alias-name` - Custom alias

### Supported Combinations

| Command | Syntax in Combined |
|---------|-------------------|
| Style | `style:StyleName` |
| Multiline | `multiline` |
| Marker (simple) | `marker:Key="value"` |
| Alias | `#alias-name` |

### Examples

```markdown
<!-- style:CustomHeading ; marker:Keywords="intro" ; #introduction -->
# Introduction with Style, Marker, and Alias

<!-- style:DataTable ; multiline ; #feature-table -->
| Column | Data |
|--------|------|
| Cell   | Multi-line content |

<!-- style:NoteBox ; marker:Priority="high" ; #important-note -->
> Important note with all attributes
```

### Whitespace

Spaces around semicolons are optional but recommended for readability:

```markdown
<!-- style:A;#b;marker:C="d" -->      # Valid
<!-- style:A ; #b ; marker:C="d" -->  # Valid, more readable
```

---

## Inline Styles for Images and Links

### Images

Place style immediately before the image syntax:

```markdown
<!--style:CustomImage-->![Logo](images/logo.png "Company Logo")

<!--style:ScreenshotStyle-->![Settings Screen](images/settings.png)

<!--style:IconImage-->![Warning](icons/warning.svg)
```

### Links (Style Inside Link Text)

Place style inside the link text brackets:

```markdown
[<!--style:CustomLink-->*Link text*](topics/file.md#anchor "Title")

See the [<!--style:ImportantLink-->**API Reference**](api.md#auth) for details.

Read the [<!--style:ExternalLink-->documentation](https://example.com).
```

The style applies to the formatted text within the link.

---

## Content Islands (Blockquotes)

Blockquotes create "content islands" - self-contained content blocks. See [SKILL.md](../SKILL.md#content-islands-blockquotes) for examples.

**Supported content within blockquotes:**
- Headings
- Lists (ordered and unordered)
- Code blocks (fenced)
- Nested formatting (bold, italic, links)
- Other Markdown++ extensions (variables, conditions, inline styles)

**Styling:** Place `<!--style:StyleName-->` on the line above the blockquote to apply a custom style.

---

## Validation Checks

The validation script checks for these issues:

| Code | Check | Severity |
|------|-------|----------|
| MDPP001 | Unclosed condition block | Error |
| MDPP002 | Invalid variable name | Error |
| MDPP003 | Malformed marker JSON | Error |
| MDPP004 | Invalid style placement (reserved, not yet implemented) | Warning |
| MDPP005 | Circular include (reserved, not yet implemented) | Error |
| MDPP006 | Missing include file | Warning |
| MDPP007 | Invalid condition syntax | Error |
| MDPP008 | Duplicate alias within file | Error |
| MDPP009 | Orphaned comment tag (not attached to element) | Warning |

---

## External References

- [CommonMark Specification](https://spec.commonmark.org/0.30/)
