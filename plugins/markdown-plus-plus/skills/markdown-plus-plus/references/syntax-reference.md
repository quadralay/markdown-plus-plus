---
date: 2026-03-29
status: active
---

# Markdown++ Syntax Reference

Complete reference for all Markdown++ extensions. This document provides detailed syntax rules, edge cases, and validation requirements.

## Base Specification

Markdown++ extends **CommonMark 0.30** with additional features. Standard CommonMark syntax works as expected. GitHub Flavored Markdown (GFM) tables are also supported. All extensions use HTML comments or inline tokens -- HTML comments are invisible to standard renderers, and inline tokens pass through as plain text. Markdown++ files remain valid `.md` documents that work in any Markdown tool.

## Version Declaration

Markdown++ documents can declare which specification version they target using the `mdpp-version` field in YAML frontmatter:

```yaml
---
mdpp-version: 1.0
date: 2026-04-08
status: active
---
```

### Rules

| Rule | Description |
|------|-------------|
| Field name | `mdpp-version` |
| Format | `MAJOR.MINOR` (e.g., `1.0`, `1.2`) |
| Required | No -- omitting `mdpp-version` is valid |
| Scope | Only spec-defined frontmatter field |
| Multi-file | Root document's declaration is authoritative |

### Current Version

The current Markdown++ specification version is **1.0**. Documents authored against the current specification should declare `mdpp-version: 1.0`.

### What It Does

When a processing tool encounters a document with `mdpp-version`, it compares the declared version against its own supported version:

| Situation | Result |
|-----------|--------|
| Versions match | Process normally |
| Document minor version ahead | Warning (MDPP015), best-effort processing |
| Different major version | Warning (MDPP016), processor may refuse |
| No `mdpp-version` field | Process normally, no diagnostic |

### Note

The specification version (`mdpp-version: 1.0`) is separate from tool/plugin versions. Document authors declare the specification version, not a tool version.

For the complete normative rules, see the [Format Versioning specification](../../../../../spec/versioning.md).

---

## Attachment Rules

> **This is the most important rule in Markdown++.** A blank line between a comment tag and its target element silently breaks the association. The tag passes through as a regular HTML comment with no visible error in standard preview. See the [formal Attachment Rule specification](../../../../../spec/attachment-rule.md) for the complete definition, all edge cases, and validation details.

Markdown++ comment tags must be **attached** to their target element -- they cannot float alone separated by whitespace. **"Attached" means the tag and target appear on immediately adjacent lines with zero blank lines between them.** Tags attach downward only; a tag placed below content does not apply to the content above it.

### Attachment Requirements by Command

| Command | Attachment Required | Blank Line Permitted | Can Be Standalone |
|---------|:-------------------:|:--------------------:|:-----------------:|
| Styles (`style:`) | Yes | No | No |
| Aliases (`#name`) | Yes | No | No |
| Markers (`marker:`/`markers:`) | Yes | No | No |
| Combined commands (`;`) | Yes | No | No |
| Multiline (`multiline`) | Yes (above table) | No | No |
| Conditions (`condition:`) | N/A (wraps content) | Yes (within block) | Yes |
| Includes (`include:`) | N/A (standalone directive) | N/A | Yes |

### Correct -- tag attached to element (no blank line)

```markdown
<!-- marker:IndexMarker="setup" ; #getting-started -->
## Getting Started
```

### Correct -- document-level markers attached to the Title paragraph

```markdown
<!-- markers:{"Keywords": "api, docs", "Description": "API reference"} -->
Heading Title
=============
```

### Wrong -- blank line breaks attachment

```markdown
<!-- style:NoteBox -->

> This blockquote will NOT receive the style.
```

### Wrong -- tag below content (tags attach downward only)

```markdown
## Getting Started
<!-- #getting-started -->
```

The alias does not attach to the heading above it. Place the tag on the line **above** the heading.

### Wrong -- stacked tags (top tag is orphaned)

```markdown
<!-- style:CustomHeading -->
<!-- #my-alias -->
## Heading Text
```

Only `#my-alias` attaches to the heading. The style tag is orphaned because its next line is another tag, not content. Use combined commands instead:

```markdown
<!-- style:CustomHeading ; #my-alias -->
## Heading Text
```

---

## Comment Disambiguation

Markdown++ directives use HTML comment syntax (`<!-- ... -->`), which creates a question: how does a processor distinguish a Markdown++ directive from a regular HTML comment?

### Recognition Rule

A processor recognizes an HTML comment as a Markdown++ directive only when its content matches a known command pattern. The recognized patterns are:

| Pattern | Directive Type | Example |
|---------|---------------|---------|
| `style:Name` | Custom style | `<!-- style:Note -->` |
| `#name` | Custom alias | `<!-- #introduction -->` |
| `marker:Key="value"` | Simple marker | `<!-- marker:Keywords="api" -->` |
| `markers:{...}` | JSON markers | `<!-- markers:{"Key": "value"} -->` |
| `condition:expr` | Condition open | `<!-- condition:web -->` |
| `/condition` | Condition close | `<!-- /condition -->` |
| `include:path` | File include | `<!-- include:chapter.md -->` |
| `multiline` | Multiline table | `<!-- multiline -->` |

Any comment containing at least one of these patterns is recognized as a directive. Multiple commands can be joined by semicolons, and unrecognized segments are silently ignored as inline comments (see [Combined Commands](#combined-commands)).

### Regular HTML Comments

An HTML comment whose content does **not** match any recognized command pattern is a regular HTML comment. Processors MUST ignore it -- the comment passes through to output or is discarded, exactly as a standard Markdown renderer would handle it.

```markdown
<!-- This is a regular HTML comment -- ignored by Markdown++ processors -->
## Heading

<!-- TODO: revise this section before release -->
Some paragraph text.
```

Neither comment above matches a command pattern, so both are treated as plain HTML comments with no Markdown++ effect. The heading and paragraph receive no directives.

### Why This Matters

Without this rule, any comment placed on a line above content could be misinterpreted as having directive intent. The pattern-matching rule ensures that authors can freely use standard HTML comments for notes, TODOs, and documentation without affecting Markdown++ processing.

### Passthrough Marker (Distinct Concept)

The `Passthrough` marker key (`<!-- marker:Passthrough="content" -->`) is a recognized Markdown++ directive -- it matches the `marker:Key="value"` pattern. It is unrelated to the pass-through behavior of unrecognized comments. See [Markers > Passthrough Marker](#passthrough-marker) for details.

---

## Naming Rules

All named entities in Markdown++ (variables, styles, aliases, conditions, and marker keys) follow a shared naming grammar.

### Standard Rule

**Regex:** `[a-zA-Z_][a-zA-Z0-9_\-]*`

- First character must be a letter (`a-z`, `A-Z`) or underscore (`_`)
- Subsequent characters may be letters, digits (`0-9`), hyphens (`-`), or underscores (`_`)
- Minimum length is 1 character
- No whitespace or punctuation

### Alias Exception

Alias names may also begin with a digit, since aliases often map to numeric identifiers (e.g., `#04499224`).

**Regex:** `[a-zA-Z0-9_][a-zA-Z0-9_\-]*`

### Valid Name Examples

| Name | Entity | Why Valid |
|------|--------|-----------|
| `product_name` | Variable | Underscore-separated |
| `release-date` | Variable | Hyphen-separated |
| `_internal` | Variable | Underscore-first |
| `CustomHeading` | Style | PascalCase |
| `BQ_Warning` | Style | Mixed with underscore |
| `introduction` | Alias | Lowercase alpha |
| `316492` | Alias | Digit-first (alias exception) |
| `web` | Condition | Single word |
| `Keywords` | Marker key | PascalCase |

### Invalid Name Examples

| Name | Why Invalid |
|------|-------------|
| `123start` | Digit-first (not an alias) |
| `-hyphen-first` | Starts with hyphen |
| `has space` | Contains whitespace |
| `special!char` | Contains punctuation |

### Non-English Content

For non-English content, the same structural rule applies using the language's UTF-8 letter values in place of `a-zA-Z`. Note: The validation script currently enforces ASCII names only; UTF-8 letter support is a future goal.

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
| Name | Must follow [Naming Rules](#naming-rules) |
| End | Must end with semicolon (`;`) |
| Spaces | Not allowed in variable names |
| Case | Case-sensitive (`$Product;` ≠ `$product;`) |
| Length | No explicit limit, but keep names reasonable |
| Escaping | Use `\$` or inline code to prevent variable interpretation |

### Escaping Variables

Two mechanisms prevent variable interpretation:

**1. Backslash escaping:**

```markdown
The syntax is \$variable_name; with a trailing semicolon.
```

The `\$` sequence is recognized and removed during processing — the backslash is consumed, the `$` becomes a literal character, and the rest of the text passes through without variable substitution. The result in published output is the literal text `$variable_name;`.

Backslash escaping is resolved *before* variable substitution in the processing pipeline. This is distinct from CommonMark's backslash escaping (which operates during Markdown parsing in a later phase).

**2. Inline code spans:**

```markdown
Use the `$variable_name;` syntax to define variables.
```

Code spans are excluded from variable scanning entirely. Content inside backticks is never interpreted as a variable reference. This is the natural choice when showing Markdown++ syntax in documentation.

**When to use each:**

| Mechanism | Use When |
|-----------|----------|
| `\$` | You want the literal text `$name;` to appear in running prose |
| `` `$name;` `` | You are showing syntax examples or code |

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
$123start;         # Violates naming rule: cannot start with digit
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

**CommonMark rendering:** Variable tokens are visible as literal text (e.g., `$product_name;` appears as-is). This is the most visible artifact of any Markdown++ extension in standard renderers.

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

**CommonMark rendering:** Style directives are hidden (HTML comments are invisible). The styled element renders with default formatting.

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
| Name | Must follow [Naming Rules](#naming-rules) |
| Spaces | Not allowed in style names |
| Case | Typically PascalCase by convention |

---

## Custom Aliases

**Aliases are block-level only.** They must appear as a standalone HTML comment on their own line, directly above the target block element. Inline aliases (e.g., `<!--#name-->` embedded within a paragraph or beside inline formatting) are not supported and will be treated as unrecognized commands by parsers.

### Syntax

```
<!--#alias-name-->
```

### Rules

| Rule | Description |
|------|-------------|
| Scope | Block-level only -- must be on its own line above a block element |
| Start | Must begin with `#` inside the comment |
| Name | Must follow [Naming Rules](#naming-rules) (digit-first allowed) |
| Spaces | Not allowed (alias ends at first space) |
| Case | Case-sensitive |

### Creating Aliases

Place the alias tag on its own line directly above the target block element with **no blank line** between them. See [Attachment Rules](#attachment-rules) for placement requirements.

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

**Note:** Reference-style links (`[text][ref]` with `[ref]: url`) are supported but generally not recommended for simple use cases. See the **Advanced Patterns** section in [best-practices.md](best-practices.md#link-references) for guidance on when to use them. In multi-file assemblies, link reference definitions from all included files are visible throughout the assembled document — this is the foundation of the semantic cross-reference pattern. See the [Cross-File Link Reference Resolution](../../../../../spec/cross-file-link-resolution.md) specification for the normative resolution rules.

**CommonMark rendering:** Alias directives are hidden (HTML comments are invisible). Standard heading IDs still work for in-page navigation.

### Alias vs. Heading IDs

Standard Markdown auto-generates IDs from headings. Custom aliases:
- Supplement the auto-generated ID (both the alias and the heading ID are valid anchors)
- Allow multiple aliases per element
- Work on non-heading block elements (paragraphs, tables, lists, etc.)

When duplicate headings produce the same auto-generated alias, the processor disambiguates with a counter suffix: the first heading keeps the bare alias, subsequent headings receive `-2`, `-3`, etc. When a custom alias collides with an auto-generated alias on a different element, the custom alias always takes priority and the auto-generated alias is suffixed. See [Duplicate Alias Resolution](../../../../../spec/element-interactions.md#duplicate-alias-resolution) and [Custom Alias Priority](../../../../../spec/element-interactions.md#custom-alias-priority) for the normative rules.

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
| Name | Must follow [Naming Rules](#naming-rules) |
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

**CommonMark rendering:** Opening and closing condition tags are hidden, but all conditional branches are visible simultaneously. Readers see content for every condition regardless of audience or output format.

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
| Extension | `.md` files required; processors MAY support additional text formats |
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

**CommonMark rendering:** Include directives are hidden (HTML comments are invisible), but included content is entirely missing. Book assembly files that consist only of include directives render as blank pages. Individual content files render normally when viewed directly.

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

- Key names must follow [Naming Rules](#naming-rules)
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
| `Passthrough` | Content that bypasses processing (see below) |

### Passthrough Marker

The `Passthrough` marker injects literal content into published output without Markdown or Markdown++ processing. The marker value is passed directly to the output format.

**Syntax:**
```markdown
<!-- marker:Passthrough="<custom-element />" -->
## Section Title
```

**Semantics:**

| Aspect | Behavior |
|--------|----------|
| Processing | The marker value is emitted as-is in the output, with no Markdown parsing or variable substitution |
| Attachment | Follows standard marker attachment rules -- must be on the line directly above the target element with no blank line |
| Target element | The passthrough content is associated with the element it is attached to; the element itself is still processed normally |
| Output format | The raw content is inserted at the position of the attached element; how it renders depends on the output format (e.g., HTML tags in HTML output) |
| Multiple values | Use JSON markers format for multiple passthrough entries |

**Use cases:**
- Injecting format-specific markup (e.g., custom HTML elements, processing instructions)
- Embedding content that should not be interpreted as Markdown
- Inserting output-format-specific directives that have no Markdown++ equivalent

**Example -- injecting a custom HTML element:**
```markdown
<!-- marker:Passthrough="<a id='legacy-anchor'></a>" -->
## Migration Guide
```

**Note:** The `Passthrough` marker is a recognized Markdown++ directive (it matches the `marker:Key="value"` pattern). It is distinct from the general behavior where unrecognized HTML comments are ignored -- see [Comment Disambiguation](#comment-disambiguation).

**CommonMark rendering:** Marker directives are hidden (HTML comments are invisible). Metadata is simply absent from the rendered view.

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

1. **First content row** -- Contains the row identifier in the first cell
2. **Continuation rows** -- Empty first cell (`|          |`) continues the previous row
3. **Row separator** -- A table row where every cell contains only whitespace (pipes must be present). Matches the pattern `^ {0,3}\|(?:[ ]*\|)+[ ]*$`

> **Important:** A completely blank line (no pipe characters) **ends the table entirely** -- it does not separate rows. Only rows with pipe characters and whitespace-only cells act as row separators.

The multiline algorithm applies to both header rows (above the delimiter) and body rows (below it).

### Multiline Headers

Header rows can span multiple physical lines using the same continuation row mechanism. Continuation rows above the delimiter row extend the header, just as continuation rows below the delimiter extend body rows.

```markdown
<!-- multiline -->
| Feature        | Description              |
|                | and additional context   |
|----------------|--------------------------|
| Authentication | OAuth 2.0 implementation |
|                | Supports:                |
|                | - Authorization Code     |
|                | - Client Credentials     |
```

In this example, the header row `Feature | Description` is extended by a continuation row with an empty first cell and `and additional context` in the second cell, before the delimiter row.

### Cell Content Dedent

When a cell spans multiple physical lines, the processor strips the minimum common leading whitespace from all lines of that cell's content. This dedent algorithm ensures that indentation used for visual alignment in the source table does not appear in the output.

**Before (source):**
```
|            | - Authorization Code     |
|            | - Client Credentials     |
|            | - Refresh tokens         |
```

**After (dedent applied):**
```
- Authorization Code
- Client Credentials
- Refresh tokens
```

The single leading space common to all three lines is stripped. If one line had no leading whitespace, no stripping would occur.

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

**CommonMark rendering:** The multiline directive is hidden. The table renders as standard GFM, but continuation rows (empty first cell) appear as separate rows. Content is readable but the intended row grouping is lost.

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

### Unrecognized Segments in Combined Commands

When a combined command contains a mix of recognized and unrecognized segments, a processor MUST interpret the recognized segments normally and silently ignore the unrecognized segments. Unrecognized segments function as **inline comments** within the directive.

```markdown
<!-- style:CustomHeading ; #alias-here ; TODO: add Keywords/Description markers -->
# My Heading Text
```

The segments `style:CustomHeading` and `#alias-here` match known command patterns and are applied to the heading. The segment `TODO: add Keywords/Description markers` does not match any command pattern, so it is ignored. The heading receives both the custom style and the alias.

**Why this is useful:** Inline comments within combined commands provide a clean, readable way to annotate directives without affecting processing. Authors can include notes, TODOs, or explanations directly alongside the commands they relate to.

```markdown
<!-- style:NoteBox ; marker:Keywords="setup" ; #getting-started ; Reviewed 2026-03 -->
## Getting Started
```

**Avoid stacking separate HTML comments.** Placing multiple HTML comments on consecutive lines above an element can cause scanning errors and reduces readability. Combining recognized commands with inline comments in a single directive is the preferred pattern:

```markdown
<!-- Good: single combined command with inline comment -->
<!-- style:Note ; marker:Priority="high" ; needs review before release -->
> Important information here.

<!-- Bad: stacked comments risk scanning errors and reduce readability -->
<!-- needs review before release -->
<!-- style:Note ; marker:Priority="high" -->
> Important information here.
```

**CommonMark rendering:** Combined command directives are hidden (HTML comments are invisible). Behaves identically to the individual commands -- all comment-based directives are invisible in standard renderers.

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

**CommonMark rendering:** Inline style directives are hidden. The formatted element (bold, italic, link, image) renders normally with default formatting.

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

**CommonMark rendering:** Style directives are hidden. Blockquotes render with default formatting. There is no visual distinction between Warning, Tip, Note, or other styled blockquote types -- all appear as standard blockquotes.

---

## Validation Checks

The validation script checks for these issues. See [Error Code Reference](error-codes.md) for full details including detection logic, trigger examples, and suggested fixes.

| Code | Check | Severity |
|------|-------|----------|
| MDPP000 | File not found or not readable | Error |
| MDPP001 | Unmatched condition block | Error |
| MDPP002 | Invalid name (variable, style, alias, or marker key) | Error |
| MDPP003 | Malformed marker JSON | Error |
| MDPP004 | Invalid style placement (reserved, not yet implemented) | Warning |
| MDPP005 | Circular include (reserved, not yet implemented) | Error |
| MDPP006 | Missing include file | Warning |
| MDPP007 | Invalid condition syntax | Error |
| MDPP008 | Duplicate alias within file | Error |
| MDPP009 | Orphaned comment tag (not attached to element) | Warning |
| MDPP014 | Duplicate link reference slug across files | Warning |

---

## External References

- [CommonMark Specification](https://spec.commonmark.org/0.30/)
