---
date: 2026-04-08
status: active
version: "1.0"
---

# Markdown++ 1.0 Specification

## Table of Contents

1. [Introduction and Scope](#1-introduction-and-scope)
2. [Conformance](#2-conformance)
3. [Terminology](#3-terminology)
4. [Notation and Conventions](#4-notation-and-conventions)
5. [Extension Comment Syntax](#5-extension-comment-syntax)
6. [The Attachment Rule](#6-the-attachment-rule)
7. [The Processing Model](#7-the-processing-model)
8. [Variables](#8-variables)
9. [Custom Styles](#9-custom-styles)
10. [Custom Aliases](#10-custom-aliases)
11. [Conditions](#11-conditions)
12. [File Includes](#12-file-includes)
13. [Markers and Metadata](#13-markers-and-metadata)
14. [Multiline Tables](#14-multiline-tables)
15. [Content Islands](#15-content-islands)
16. [Combined Commands](#16-combined-commands)
17. [Advanced Topics](#17-advanced-topics)
18. [Diagnostic Registry](#18-diagnostic-registry)
19. [References](#19-references)

---

## 1. Introduction and Scope

Markdown++ is an extended documentation format built on [CommonMark 0.30][commonmark]. A Markdown++ document is a valid CommonMark document. Markdown++ extensions are purely additive -- they introduce no syntax that alters or conflicts with CommonMark processing.

Markdown++ adds two syntactic forms to CommonMark:

1. **Inline variable tokens** -- `$name;` references that are resolved to values from a variable map during processing.
2. **HTML comment directives** -- `<!-- command -->` comments that carry style, alias, marker, condition, include, and multiline commands.

A standard CommonMark renderer that does not recognize Markdown++ extensions will render the document correctly: comment directives are invisible (standard HTML comment behavior), and variable tokens appear as literal text. This backward compatibility is the core design principle of the format.

Markdown++ also supports [GitHub Flavored Markdown (GFM)][gfm] tables as a baseline table syntax, extended by the multiline table feature defined in this specification.

### 1.1 Relationship to CommonMark

All constructs defined by [CommonMark 0.30][commonmark] are valid in a Markdown++ document and retain their standard semantics. Markdown++ extensions operate through mechanisms that CommonMark already defines:

- **HTML comments** (`<!-- ... -->`) -- CommonMark treats these as raw HTML. Markdown++ gives semantic meaning to comments whose content matches a recognized command pattern.
- **Inline tokens** (`$name;`) -- CommonMark treats these as literal text. Markdown++ interprets them as variable references.

This specification does not redefine any CommonMark behavior. Where this specification is silent on a construct, CommonMark 0.30 governs.

### 1.2 Normative References

This specification is defined across five documents. The present document is the primary specification. The following four documents are **normative references** -- a conformant processor MUST implement the rules defined therein:

| Document | Scope |
|----------|-------|
| [Formal Grammar](formal-grammar.md) | W3C EBNF and PEG grammar for all extension constructs |
| [Attachment Rule](attachment-rule.md) | Tag-to-element binding rules and edge cases |
| [Processing Model](processing-model.md) | Two-phase processing pipeline, evaluation order, error handling |
| [Cross-File Link Reference Resolution](cross-file-link-resolution.md) | Link reference scope, conflict resolution, and diagnostics in multi-file assemblies |

### 1.3 Version

This document defines **Markdown++ 1.0**.

---

## 2. Conformance

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this specification are to be interpreted as described in [RFC 2119][rfc2119]. All conformance statements apply to processors, not to document authors.

This specification defines two conformance levels.

### 2.1 Pass-through Conformance

A **pass-through conformant renderer** is a tool that renders Markdown++ documents as standard CommonMark without evaluating Markdown++ extensions. A pass-through conformant renderer:

1. MUST NOT alter or strip HTML comment directives that contain Markdown++ commands.
2. MUST NOT alter or strip inline variable tokens (`$name;`).
3. MUST render the document as valid CommonMark 0.30, with extensions visible as HTML comments and literal text.

Pass-through conformance is solely about preservation. MDPP diagnostic codes are not applicable to pass-through renderers -- they do not parse or evaluate Markdown++ extensions.

Any standard CommonMark renderer that does not modify HTML comments satisfies pass-through conformance.

### 2.2 Full Conformance

A **fully conformant processor** is a tool that evaluates all Markdown++ extensions as defined in this specification and its normative references. A fully conformant processor MUST implement all required features defined in the [Processing Model conformance section](processing-model.md#conformance), including:

1. Include expansion with cycle detection and per-file condition evaluation.
2. Condition evaluation with the tri-state model and three-operator precedence.
3. Variable substitution with both escaping mechanisms.
4. Style, alias, marker, and multiline extraction and attachment.
5. Attachment rule enforcement for block-level and inline tags.
6. Comment disambiguation between recognized directives and regular HTML comments.
7. Emission of all MDPP diagnostic codes defined in this specification at their specified severity levels.

A fully conformant processor that also implements one or more optional features (such as version checking) is a **fully conformant processor with extensions** and SHOULD document which optional features are supported.

> **Note:** The [Processing Model](processing-model.md#conformance) uses the equivalent terms "conformant Markdown++ processor" and "conformant Markdown++ processor with extensions" for the same conformance levels defined here.

### 2.3 Determinism Guarantee

Given the same input document, variable map, and condition set, a fully conformant processor MUST produce the same output. The processing pipeline is deterministic -- there is no implementation-defined ordering or randomness in extension evaluation.

---

## 3. Terminology

The following terms are used normatively throughout this specification.

**Assembled document** -- The single text produced by Phase 1 of the processing pipeline after all includes are expanded, defined conditions are evaluated (Unset condition blocks pass through as-is), and variables are substituted. This is the input to Phase 2.

**Attachment** -- The positional relationship between a Markdown++ comment tag and the content element it modifies. A tag is attached when it appears on the line immediately above (block-level) or immediately before (inline) its target element with no intervening blank line or space. See [section 6](#6-the-attachment-rule).

**Block-level element** -- A CommonMark structural element that occupies its own line(s): headings, paragraphs, lists, blockquotes, code blocks, tables, and thematic breaks.

**Combined command** -- A single HTML comment containing multiple Markdown++ commands separated by semicolons. See [section 16](#16-combined-commands).

**Condition set** -- A collection of condition names, each assigned a state of **Visible** or **Hidden**. A condition name not defined in the condition set is **Unset** (undefined). Provided to the processor at build time.

**Content island** -- A blockquote element styled with a Markdown++ custom style, creating a self-contained content block. See [section 15](#15-content-islands).

**Directive** -- A Markdown++ command expressed as an HTML comment whose content matches a recognized command pattern. Synonymous with "recognized comment."

**Extension comment** -- An HTML comment that contains one or more Markdown++ commands. Distinguished from a regular HTML comment by pattern matching. See [section 5](#5-extension-comment-syntax).

**Inline element** -- A CommonMark element that appears within a line of text: emphasis, strong emphasis, links, images, code spans, and line breaks.

**Orphaned tag** -- A recognized Markdown++ comment tag that fails to attach to a content element. Orphaned tags produce diagnostic MDPP009 and do not affect the output tree. See [section 6.3](#63-orphaned-tags).

**Output tree** -- The structured representation of a processed Markdown++ document produced by a conformant processor. The output tree contains content elements with attached metadata (styles, aliases, markers) as defined by Phase 2 processing.

**Processor** -- A software tool that reads a Markdown++ document, evaluates its extensions according to this specification, and produces an output tree.

**Recognized comment** -- An HTML comment whose content matches at least one Markdown++ command pattern. Comments that do not match any pattern are regular HTML comments and are ignored by the processor.

**Variable map** -- A key-value collection where each key is a variable name and each value is a string. Provided to the processor at build time.

**Variable token** -- An inline `$name;` reference in a Markdown++ document that is resolved to a value from the variable map during processing.

---

## 4. Notation and Conventions

### 4.1 Grammar Notation

The formal grammar for all Markdown++ extensions is defined in the [Formal Grammar](formal-grammar.md) specification using **W3C EBNF notation**, the same variant used by the XML and CSS specifications. A PEG transliteration is also provided for parser authors who prefer PEG-based tools.

Grammar productions referenced in this document use the names defined in the formal grammar (e.g., `identifier`, `alias_name`, `command_list`).

### 4.2 Naming Rules

Markdown++ defines three identifier forms used across all named entities:

| Form | Pattern | Used By | Spaces |
|------|---------|---------|--------|
| **Standard identifier** | `[a-zA-Z_][a-zA-Z0-9_-]*` | Variables, conditions | No |
| **Alias name** | `[a-zA-Z0-9_][a-zA-Z0-9_-]*` | Aliases (digit-first permitted) | No |
| **Style/marker name** | `[a-zA-Z_][a-zA-Z0-9_ -]*` trimmed | Styles, markers (embedded spaces permitted) | Yes, embedded |

The alias exception is an intentional design choice. Aliases frequently serve as numeric content identifiers (e.g., CMS record IDs like `#04499224`), and requiring a letter prefix would force unnatural naming. The style/marker name exception allows embedded spaces to support processor-defined compound names (e.g., `Blockquote Paragraph`, `Table Cell Head`) and legacy systems with space-embedded style names. Leading and trailing spaces are stripped before validation. Variables and conditions use the standard identifier to avoid ambiguity with numeric literals.

Names are case-sensitive. `$Product;` and `$product;` are distinct variable references. `style:Note` and `style:note` are distinct style names.

### 4.3 RFC 2119 Keywords

See [section 2](#2-conformance) for the interpretation of RFC 2119 keywords used in this specification.

---

## 5. Extension Comment Syntax

Markdown++ extensions (other than variable tokens) are expressed as HTML comment directives. This section summarizes the syntactic forms. The complete formal grammar is defined in the [Formal Grammar](formal-grammar.md) specification. A conformant processor MUST accept all strings that match the productions defined therein.

### 5.1 Two Syntactic Forms

Markdown++ adds two syntactic forms to CommonMark:

1. **Variable tokens**: `$name;` -- a `$` prefix, a standard identifier, and a terminating semicolon.
2. **Comment directives**: `<!-- command -->` -- HTML comment delimiters enclosing one or more commands.

All content that does not match one of these forms is standard CommonMark.

### 5.2 Comment Disambiguation

A processor MUST distinguish recognized Markdown++ directives from regular HTML comments. A comment is recognized as a directive only when its content matches at least one known command pattern:

| Pattern | Command Type |
|---------|-------------|
| `style:Name` | Custom style |
| `#name` | Custom alias |
| `marker:Key="value"` | Simple marker |
| `markers:{...}` | JSON markers |
| `condition:expr` | Condition open |
| `/condition` | Condition close |
| `include:path` | File include |
| `multiline` | Multiline table |

Regular HTML comments (e.g., `<!-- TODO: fix this -->`) that do not match any command pattern MUST be ignored by the processor. They are not directives, are not subject to the attachment rule, and produce no diagnostics.

### 5.3 Combined Command Syntax

Multiple commands MAY be joined in a single comment using semicolons as separators:

```
<!-- command1 ; command2 ; command3 -->
```

Within a combined command, each semicolon-delimited segment is either a recognized command or unrecognized text. Unrecognized segments are silently discarded, functioning as inline comments within the directive. See [section 16](#16-combined-commands) for the complete definition.

### 5.4 Whitespace

Whitespace (spaces and horizontal tabs) between the comment delimiters and the command content is optional. Both `<!--style:Name-->` and `<!-- style:Name -->` are valid. Whitespace around semicolons in combined commands is optional but recommended for readability.

---

## 6. The Attachment Rule

The attachment rule governs the positional relationship between Markdown++ comment tags and the content elements they modify. This section states the core rules. The complete definition, including all edge cases, is in the [Attachment Rule](attachment-rule.md) specification. A conformant processor MUST implement the rules defined therein.

### 6.1 Core Rules

1. **Block-level tags** MUST appear on the line directly above the target element with no intervening blank line.
2. **Inline tags** MUST appear immediately before the styled element on the same line, with no space between the closing `-->` and the element.
3. A single blank line between a tag and its target breaks attachment. Multiple blank lines have the same effect as one.
4. Tags attach **downward only** -- a tag placed below content does not attach to the content above it.

### 6.2 Attachment Requirements by Command

| Command | Attachment Required | Notes |
|---------|:-------------------:|-------|
| `style:` (block and inline) | Yes | Block: line above. Inline: immediately before, no space. |
| `#alias` | Yes | Block-level only. Line directly above target. |
| `marker:` / `markers:` | Yes | Line directly above target. |
| `multiline` | Yes | Line directly above the table. |
| Combined commands (`;`) | Yes | Same rules as the individual commands within. |
| `condition:` / `/condition` | No | Wraps content. Blank lines within the block are permitted. |
| `include:` | No | Standalone directive. Inserts file contents at its position. |

### 6.3 Orphaned Tags

A recognized Markdown++ tag that fails attachment is an **orphaned tag**. Orphaned tags MUST produce diagnostic **MDPP009** (severity: Warning) and MUST NOT affect the output tree. Common causes include blank lines between the tag and its target, tags at the end of a file, and stacked tags where only the bottom tag attaches to content.

The combined command syntax (semicolons) is the solution for applying multiple commands to a single element. See [section 16](#16-combined-commands).

---

## 7. The Processing Model

Processing a Markdown++ document is a two-phase operation. This section summarizes the pipeline. The complete specification is in the [Processing Model](processing-model.md). A conformant processor MUST implement the pipeline as defined therein.

### 7.1 Pipeline Summary

**Phase 1: Pre-Processing** (text-level transforms, before any Markdown parsing)

1. **Include Expansion** -- Recursively resolve `<!-- include:path -->` directives using depth-first traversal. Each included file's conditions are evaluated per-file before its content is spliced into the parent.
2. **Variable Substitution** -- Replace `$name;` tokens with values from the variable map. Backslash escapes (`\$`) are resolved before scanning. Code spans are excluded from scanning.

**Phase 2: Markdown Parsing with Extension Extraction**

3. **Parsing and Rendering** -- Parse the assembled document as CommonMark 0.30 with GFM table support. During parsing, extract style, alias, marker, and multiline commands from recognized HTML comments and attach them to target elements per the attachment rule.

The phases are strictly sequential -- Phase 2 MUST NOT begin until Phase 1 is complete.

### 7.2 Processing Order

The sequential ordering of the pipeline has critical implications:

1. Conditions are evaluated before variable substitution. Variables inside Hidden condition blocks are never resolved. Variables inside Unset (pass-through) condition blocks are resolved, because the block's content survives into variable substitution.
2. Includes are expanded before variable substitution. Variable values cannot contain include syntax.
3. Variable values cannot contain condition syntax (defined conditions are already evaluated).
4. Variable values CAN contain Markdown syntax (variable substitution runs before Markdown parsing).

### 7.3 Error Model

The processing model defines two error classes:

- **Fatal errors**: Prevent meaningful output for the affected construct. The processor MUST report the error and SHOULD continue processing the remainder of the document.
- **Recoverable warnings**: The processor MUST report the warning and continue with a documented fallback behavior.

A conformant processor SHOULD collect all diagnostics rather than halting on the first error. See [section 18](#18-diagnostic-registry) for the complete diagnostic code registry.

---

## 8. Variables

### 8.1 Purpose

Variables provide reusable inline content tokens. A variable reference in a document is replaced with its value from the variable map during Phase 1 processing. Variables enable single-source management of product names, version numbers, URLs, and other content that appears in multiple locations.

### 8.2 Syntax

A variable reference consists of a `$` prefix, a standard identifier, and a terminating semicolon:

```
$variable_name;
```

Variable names MUST match the standard identifier pattern: `[a-zA-Z_][a-zA-Z0-9_-]*`. Variable references are case-sensitive.

**Valid examples:** `$product_name;`, `$version;`, `$release-date;`, `$_internal;`

**Invalid examples:** `$123start;` (digit-first), `$name` (missing semicolon), `$has space;` (whitespace in name)

### 8.3 Semantics

Variable substitution is performed during Phase 1, Step 2 of the processing pipeline, as specified in the [Processing Model](processing-model.md#phase-1-step-2-variable-substitution).

For each `$name;` token in the text produced by the preceding steps:

1. The processor MUST look up the variable name in the variable map.
2. If the name exists, the processor MUST replace the entire token with the variable's value.
3. If the name does not exist, the processor MUST leave the token as literal text and MUST emit diagnostic **MDPP010** (severity: Warning).

#### Escaping

Two mechanisms prevent variable interpretation. A conformant processor MUST support both.

**Backslash escaping:** The sequence `\$name;` prevents the token from being recognized as a variable reference. The backslash is consumed: the result is the literal text `$name;`. Backslash escapes are resolved before variable scanning.

**Code span exclusion:** Variable tokens inside CommonMark code spans (`` ` ``) MUST NOT be scanned for variable substitution. Code spans are excluded from variable scanning entirely.

| Mechanism | Use Case |
|-----------|----------|
| `\$name;` | Literal `$name;` in running prose |
| `` `$name;` `` | Showing syntax examples or code |

#### Usage Contexts

Variables MAY appear in paragraphs, headings, list items, link text, link URLs, and within formatting spans. Variables remain as literal tokens in the source and are resolved during processing.

### 8.4 Interaction with Other Extensions

**Variables and Conditions:** Variable substitution runs after condition evaluation (Phase 1, Step 2 follows Step 1). Variables inside Hidden condition blocks are never resolved -- the content is removed before variable scanning occurs. Variables inside Unset (pass-through) condition blocks are resolved, because the block's content survives into variable substitution. Variable values cannot contain condition syntax; such content passes through as literal text into Phase 2.

**Variables and Includes:** The variable map is document-global. All files in an include tree share the same variable map. Variable substitution runs after all includes are expanded. Variable values cannot contain include syntax; such content passes through as literal text into Phase 2.

These ordering implications are specified normatively in the [Processing Model](processing-model.md#processing-order).

### 8.5 Attachment Requirements

Variables are inline tokens, not comment directives. The attachment rule does not apply to variables. A variable token MAY appear anywhere within text content.

### 8.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP002** | Variable name does not match the standard identifier pattern | Error |
| **MDPP010** | Variable reference has no corresponding entry in the variable map | Warning |

### 8.7 Examples

```markdown
Welcome to $product_name;, version $version;.

# $product_name; User Guide

- Version: $version;
- Release date: $release-date;

The syntax is \$variable_name; with a trailing semicolon.

Use `$variable_name;` in your documents.
```

---

## 9. Custom Styles

### 9.1 Purpose

Custom styles associate a named style with a block-level or inline content element. The style name is metadata attached to the element during Phase 2 parsing. How a processor renders styled elements is implementation-defined -- the specification defines the association mechanism, not the visual output.

### 9.2 Syntax

```
<!-- style:StyleName -->
```

The style name MUST match the style/marker name pattern: `[a-zA-Z_][a-zA-Z0-9_ -]*` (trimmed, no leading or trailing spaces). Embedded spaces are permitted to support compound names and legacy systems. Style names are conventionally PascalCase (e.g., `CustomHeading`, `NoteBlock`, `BQ_Warning`, `Code Block`).

### 9.3 Semantics

A style command associates a named style with the attached content element. The association is extracted during Phase 2 parsing. The style name becomes metadata on the element in the output tree.

#### Block-Level Placement

A block-level style tag MUST appear on the line directly above the target element with no blank line between them. The target element may be any block-level element: heading, paragraph, list, blockquote, code block, or table.

```markdown
<!-- style:CustomHeading -->
# Heading Text

<!-- style:NoteBlock -->
> Blockquote content

<!-- style:CodeExample -->
```python
code here
```
```

#### Inline Placement

An inline style tag MUST appear immediately before the styled inline element on the same line, with no space between the closing `-->` and the element.

```markdown
This is <!--style:Emphasis-->**bold text** in a paragraph.
Use <!--style:Code-->`inline code` here.
Click [<!--style:Link-->*here*](url) to continue.
```

#### Nested List Styling

When styling a nested list item, the tag MUST be indented to match the nesting level of the target list item:

```markdown
<!-- style:BulletList1 -->
- Top-level item

  <!-- style:BulletList2 -->
  - Nested item
```

### 9.4 Interaction with Other Extensions

**Styles and Combined Commands:** A style MAY be combined with markers, aliases, and the multiline indicator using combined command syntax. In the recommended evaluation order, the style is evaluated first. See [section 16](#16-combined-commands).

**Styles and Multiline Tables:** A style MAY apply to a multiline table by placing it above the `<!-- multiline -->` tag via a combined command (`<!-- style:DataTable ; multiline -->`), or to content within table cells using inline or block placement within the cell.

**Styles and Content Islands:** A style above a blockquote creates a content island -- a styled, self-contained content block. See [section 15](#15-content-islands).

**Styles and Conditions:** Style tags within a Hidden condition block are removed along with the rest of the block's content. Style tags within Unset (pass-through) condition blocks are preserved as-is in the output.

### 9.5 Attachment Requirements

Style commands require attachment. Block-level styles follow the standard block attachment rule. Inline styles follow the inline attachment rule (no space between `-->` and the element). An unattached style is orphaned.

Inline placement applies only to `style:` commands; all other commands that require attachment operate at block level only, as specified in the [Formal Grammar structural constraints](formal-grammar.md#structural-constraints).

### 9.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP002** | Style name does not match the standard identifier pattern | Error |
| **MDPP004** | Invalid style placement | Warning |
| **MDPP009** | Orphaned style tag (not attached to an element) | Warning |

### 9.7 Examples

```markdown
<!-- style:CustomHeading -->
## Section Title

This paragraph contains <!--style:Emphasis-->**emphasized text** inline.

<!-- style:DataTable -->
| Column A | Column B |
|----------|----------|
| Cell 1   | Cell 2   |
```

---

## 10. Custom Aliases

### 10.1 Purpose

Custom aliases assign stable anchor identifiers to block-level elements. Unlike auto-generated heading IDs (which change when heading text changes), aliases provide fixed identifiers for cross-referencing. Aliases are the foundation of the semantic cross-reference pattern used in multi-file document assemblies.

### 10.2 Syntax

```
<!-- #alias-name -->
```

The alias name MUST match the alias name pattern: `[a-zA-Z0-9_][a-zA-Z0-9_-]*`. Aliases permit a leading digit, unlike other named entities. Alias names are case-sensitive.

**Valid examples:** `<!-- #introduction -->`, `<!-- #getting-started -->`, `<!-- #316492 -->`, `<!-- #04499224 -->`

### 10.3 Semantics

An alias command registers a navigational anchor identifier on the attached block-level element during Phase 2 parsing. The alias identifier is metadata on the element in the output tree.

**Aliases are block-level only.** An alias MUST appear as a standalone HTML comment on its own line, directly above the target block element. Inline aliases (e.g., `<!--#name-->` embedded within a paragraph or beside inline formatting) MUST NOT be supported. A processor encountering an alias pattern in inline position SHOULD treat it as an unrecognized command.

An alias supplements the auto-generated heading ID -- both the alias and the heading ID are valid anchors. Aliases also work on non-heading block elements (paragraphs, tables, lists, blockquotes).

### 10.4 Interaction with Other Extensions

**Aliases and Link References:** Aliases create anchor IDs that link reference definitions can target. This is the semantic cross-reference pattern: a combined command assigns an alias to a heading, and a link reference definition bridges a human-readable slug to that alias ID. In multi-file assemblies, cross-file link reference resolution (as specified in [Cross-File Link Reference Resolution](cross-file-link-resolution.md)) enables references from any file to resolve to alias-anchored headings in any other file.

**Aliases and Combined Commands:** An alias MAY be combined with styles and markers using combined command syntax. In the recommended evaluation order, the alias is evaluated last. See [section 16](#16-combined-commands).

**Aliases and Conditions:** Alias tags within a Hidden condition block are removed along with the rest of the block's content. Alias tags within Unset (pass-through) condition blocks are preserved as-is in the output.

### 10.5 Attachment Requirements

Alias commands require block-level attachment. The alias tag MUST appear on the line directly above the target element with no blank line. A combined command is required when both a style and an alias apply to the same element.

### 10.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP002** | Alias name does not match the alias name pattern | Error |
| **MDPP008** | Duplicate alias identifier within the same file | Error |
| **MDPP009** | Orphaned alias tag (not attached to an element) | Warning |

### 10.7 Examples

```markdown
<!-- #introduction -->
## Introduction

See [Introduction](#introduction) for details.

<!-- style:Heading2; #200010 -->
## Getting Started

[getting-started]: #200010 "Getting Started"
```

---

## 11. Conditions

### 11.1 Purpose

Conditions control content visibility. A condition block wraps content that is included, excluded, or passed through based on the condition set provided at build time. Conditions enable single-source authoring for multiple output formats, audiences, or platforms.

### 11.2 Syntax

```
<!-- condition:expression -->
content
<!-- /condition -->
```

A condition block consists of an opening tag with a condition expression and a closing tag. Every opening `<!-- condition:expr -->` MUST have a corresponding `<!-- /condition -->`. Condition blocks MUST NOT nest or overlap.

### 11.3 Semantics

Condition evaluation occurs during Phase 1, Step 1 of the processing pipeline, on a per-file basis during include expansion. The complete evaluation rules are specified in the [Processing Model](processing-model.md#per-file-condition-evaluation).

#### Tri-State Model

Each condition name has one of three states:

| State | Meaning |
|-------|---------|
| **Visible** | Content inside the block is included in output. |
| **Hidden** | Content inside the block is removed from output. |
| **Unset** | The condition name is not defined in the condition set. The condition block passes through without evaluation -- the opening tag, content, and closing tag are preserved as-is in the output. |

When a condition expression references an undefined (Unset) name, the processor MUST NOT evaluate the expression. The entire condition block -- opening tag, content, and closing tag -- passes through as-is. This allows the implementation to surface or resolve undefined conditional content downstream rather than silently including it.

For example, given the condition set `{web: Visible}` and input:

```markdown
<!--condition:web-->
Web content here.
<!--/condition-->

<!--condition:mobile-->
Mobile content here.
<!--/condition-->
```

The output is:

```markdown
Web content here.

<!--condition:mobile-->
Mobile content here.
<!--/condition-->
```

The `web` block is evaluated (Visible, so its content is included without tags). The `mobile` block passes through as-is because `mobile` is not defined in the condition set.

#### Expression Operators

Condition expressions support three operators with explicit precedence:

| Operator | Symbol | Precedence | Behavior |
|----------|--------|:----------:|----------|
| NOT | `!` (prefix) | 1 (highest) | Inverts the condition state. `!name` is true when `name` is Hidden, false when Visible. If `name` is Unset, the block passes through. |
| AND | ` ` (space) | 2 (medium) | All operands must be true. `a b` is true when both `a` and `b` are Visible. If any operand is Unset, the block passes through. |
| OR | `,` (comma) | 3 (lowest) | Any operand must be true. `a,b` is true when either `a` or `b` is Visible. If any operand is Unset, the block passes through. |

A processor MUST parse condition expressions according to this precedence. The expression `!draft,web production` MUST be parsed as `(!draft) OR (web AND production)`.

Condition names MUST match the standard identifier pattern. Condition names are case-sensitive.

#### Nesting

Condition blocks MUST NOT be nested. To express multi-condition logic, use logical expressions with AND (space), OR (comma), and NOT (`!`) operators in condition expressions (see [Expression Operators](#expression-operators) above). For example, instead of nesting a `web` condition inside an `advanced` condition, use `<!--condition:web advanced-->` to require both.

#### Block and Inline Usage

Conditions MAY be used at block level (wrapping paragraphs, headings, lists) or inline (wrapping spans within a line):

```markdown
Contact us at <!--condition:web-->[email](mailto:x@x.com)<!--/condition--><!--condition:print-->the address below<!--/condition-->.
```

### 11.4 Interaction with Other Extensions

Conditions have the broadest interaction surface of any Markdown++ extension. Content within a Hidden condition block is removed before any other extension processes it. Content within an Unset (pass-through) condition block is preserved along with the condition tags -- embedded extension directives within the block survive into Phase 2 as regular HTML comments.

**Conditions and Variables:** Conditions are evaluated before variable substitution. Variables inside Hidden blocks are never resolved. Variables inside Unset (pass-through) condition blocks are resolved, because the block's content survives into variable substitution. Variable values cannot contain condition syntax. See [section 7.2](#72-processing-order).

**Conditions and Includes:** Condition evaluation is per-file during include expansion. A condition block that opens in one file and closes in another is a fatal error (MDPP012). A condition block MAY wrap an include directive; if the condition is Hidden, the include is never processed. If the condition is Unset, the entire block -- including the include directive -- passes through as-is; the include is not processed.

**Conditions and Styles/Aliases/Markers:** All directive tags within a Hidden condition block are removed along with the content. Tags within Visible condition blocks follow normal attachment rules. Tags within Unset (pass-through) condition blocks are preserved as-is in the output.

**Conditions and Multiline Tables:** Condition blocks MAY appear within multiline table cells. Defined condition content is evaluated during Phase 1 before table parsing in Phase 2. Unset condition blocks within table content pass through as-is, including the condition tags.

**Conditions and Content Islands:** Conditions MAY wrap or appear within content islands (styled blockquotes). If a condition wrapping or within a content island is Unset, the condition block passes through as-is.

### 11.5 Attachment Requirements

Condition tags are **exempt** from the attachment rule. Conditions wrap content rather than attaching to it. Blank lines within a condition block are permitted and expected.

### 11.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP001** | Unclosed condition block (missing `<!-- /condition -->`) or unmatched closing tag | Error |
| **MDPP007** | Invalid condition expression syntax | Error |
| **MDPP012** | Condition block spans across an include boundary (opens in one file, closes in another) | Error |

### 11.7 Examples

```markdown
<!-- condition:web -->
## Web-Only Section

This section only appears in web output.
<!-- /condition -->

<!-- condition:!draft,web production -->
This appears when draft is Hidden, OR when both web and production are Visible.
<!-- /condition -->

<!-- condition:advanced -->
<!-- include:appendix.md -->
<!-- /condition -->
```

---

## 12. File Includes

### 12.1 Purpose

File includes enable multi-file document assembly. An include directive inserts the contents of another file at the directive's position, enabling authors to compose large documents from independently editable components.

### 12.2 Syntax

```
<!-- include:path/to/file.md -->
```

The file path is any non-empty sequence of characters (excluding `>`). Paths are resolved relative to the directory containing the file in which the include directive appears.

### 12.3 Semantics

Include expansion is performed during Phase 1, Step 1 of the processing pipeline using depth-first recursive traversal. The complete algorithm is specified in the [Processing Model](processing-model.md#phase-1-step-1-include-expansion).

#### Path Resolution

Include paths MUST be resolved relative to the directory containing the file in which the include directive appears, not relative to the root document.

| File Location | Include Statement | Resolves To |
|---------------|-------------------|-------------|
| `docs/guide.md` | `<!-- include:intro.md -->` | `docs/intro.md` |
| `docs/guide.md` | `<!-- include:shared/header.md -->` | `docs/shared/header.md` |
| `docs/guide.md` | `<!-- include:../common/footer.md -->` | `common/footer.md` |

#### Block-Level Separation

A processor MUST insert included content with block-level separation -- the included content MUST be surrounded by blank lines on both sides when spliced into the parent document.

#### Cycle Detection

A processor MUST track the include chain and MUST detect circular references. When a cycle is detected, the processor MUST skip the circular include, leave the include tag in place as a regular HTML comment, and emit diagnostic **MDPP013**.

#### Include Depth

Implementations MAY impose a maximum include depth to prevent resource exhaustion. If a maximum depth is enforced, a depth of **10** is RECOMMENDED. When the limit is exceeded, the processor MUST skip the include and emit diagnostic **MDPP011**.

#### File Not Found

When an included file does not exist or cannot be read, the processor MUST emit diagnostic **MDPP006** (severity: Warning) and leave the include tag in place as a regular HTML comment.

### 12.4 Interaction with Other Extensions

**Includes and Conditions:** Condition evaluation is per-file during include expansion. Each file's condition blocks are evaluated before its content is spliced into the parent. A condition block MAY wrap an include directive -- if the condition is Hidden, the include is not processed; if the condition is Unset, the entire block (including the include directive) passes through as-is and the include is not processed. Cross-file condition spans (opening in one file, closing in another) are a fatal error (MDPP012).

**Includes and Variables:** Included files inherit the variable map from the parent document. All files in an include tree share the same variable map. Variable substitution runs after all includes are expanded.

**Includes and Link References:** After include expansion produces a single assembled text, link reference definitions from all files are visible at document-global scope. Resolution rules are specified in [Cross-File Link Reference Resolution](cross-file-link-resolution.md).

### 12.5 Attachment Requirements

Include directives are **exempt** from the attachment rule. An include is a standalone directive -- it inserts file contents at its position and does not attach to adjacent content.

### 12.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP005** | Circular include detected (static analysis) | Error |
| **MDPP006** | Missing or unreadable include file | Warning |
| **MDPP011** | Maximum include depth exceeded | Error |
| **MDPP013** | Include cycle detected during processing | Error |

MDPP005 and MDPP013 cover the same underlying problem (circular includes) at different phases: MDPP005 for static analysis tools that inspect the source before processing, and MDPP013 for runtime detection during Phase 1 expansion.

### 12.7 Examples

```markdown
<!-- include:chapters/introduction.md -->
<!-- include:chapters/getting-started.md -->
<!-- include:chapters/configuration.md -->

<!-- condition:advanced -->
<!-- include:appendix.md -->
<!-- /condition -->
```

---

## 13. Markers and Metadata

### 13.1 Purpose

Markers attach metadata key-value pairs to block-level elements. Markers provide a mechanism for associating structured data (keywords, descriptions, index entries, passthrough content) with content elements for use by publishing processors.

### 13.2 Syntax

Markdown++ defines two marker syntax forms.

#### Simple Marker

For a single key-value pair:

```
<!-- marker:Key="value" -->
```

The key MUST match the style/marker name pattern (`[a-zA-Z_][a-zA-Z0-9_ -]*`, trimmed). Embedded spaces are permitted in marker keys. The value is enclosed in double quotes. Empty values (`""`) are permitted. Escaped double quotes within values are not supported.

#### JSON Markers

For multiple key-value pairs:

```
<!-- markers:{"Key1": "value1", "Key2": "value2"} -->
```

The JSON content MUST be a valid JSON object as defined by [RFC 8259][rfc8259]. Keys within the JSON object MUST be strings conforming to the standard identifier pattern. Values MAY be any JSON type (string, number, boolean, array, object, null). A conformant processor MUST use a standards-compliant JSON parser for the JSON markers production.

### 13.3 Semantics

Markers are extracted and attached to elements during Phase 2 parsing. The marker key-value pairs become metadata on the attached element in the output tree.

#### Passthrough Marker

The `Passthrough` marker key has special semantics. Its value is emitted as-is in the output with no Markdown parsing or variable substitution. The Passthrough marker enables injection of format-specific markup (e.g., custom HTML elements, processing instructions) that should not be interpreted as Markdown.

```markdown
<!-- marker:Passthrough="<a id='legacy-anchor'></a>" -->
## Migration Guide
```

The Passthrough marker is a recognized Markdown++ directive -- it matches the `marker:Key="value"` pattern. It is distinct from the general behavior where unrecognized HTML comments are ignored.

#### Index Markers

The `IndexMarker` key creates entries in generated indexes. Index entries use colon-separated nesting for sub-entries and comma separation for multiple entries:

- `primary` -- Top-level entry
- `primary:secondary` -- Nested entry under primary
- Comma separates multiple independent entries

```markdown
<!-- marker:IndexMarker="source documents:opening,documents:opening from Manager" -->
```

### 13.4 Interaction with Other Extensions

**Markers and Combined Commands:** Markers MAY be combined with styles and aliases using combined command syntax. In the recommended evaluation order, markers are evaluated third (after style and multiline, before alias). See [section 16](#16-combined-commands).

**Markers and Conditions:** Marker tags within a Hidden condition block are removed along with the rest of the block's content. Marker tags within Unset (pass-through) condition blocks are preserved as-is in the output.

**Markers and Aliases:** Markers and aliases are frequently combined on the same element via combined commands, particularly for headings in the semantic cross-reference pattern.

### 13.5 Attachment Requirements

Marker commands require block-level attachment. The marker tag MUST appear on the line directly above the target element with no blank line. At the start of a file, markers are typically placed above the title paragraph -- they are attached to the title, not floating standalone.

### 13.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP002** | Marker key does not match the style/marker name pattern | Error |
| **MDPP003** | Malformed JSON in `markers:` command | Error |
| **MDPP009** | Orphaned marker tag (not attached to an element) | Warning |

### 13.7 Examples

```markdown
<!-- marker:Keywords="api, documentation" -->
## API Reference

<!-- markers:{"Keywords": "setup", "Description": "Installation guide", "Priority": 1} -->
## Installation

<!-- marker:IndexMarker="creating projects" -->
## Creating Projects

<!-- marker:Passthrough="<custom-element />" -->
## Custom Section
```

---

## 14. Multiline Tables

### 14.1 Purpose

Multiline tables extend GFM table syntax to support block-level content within table cells. Standard GFM tables limit each cell to a single line. The multiline table indicator enables continuation rows, allowing lists, blockquotes, styled elements, and other block content within cells.

### 14.2 Syntax

The `<!-- multiline -->` directive is placed on the line immediately above a GFM table:

```
<!-- multiline -->
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Content  |
```

### 14.3 Semantics

A multiline table uses a specific row structure:

1. **First content row** -- Contains the row identifier in the first cell. This marks the beginning of a new table row.
2. **Continuation rows** -- An empty first cell (`| |`) continues the content of the previous row. Content in other cells is appended to the corresponding cell of the current row.
3. **Row separator** -- An empty row with cell borders (all cells empty) separates table rows.

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
```

#### Cell Content

Multiline table cells MAY contain:

- Lists (ordered and unordered)
- Blockquotes
- Styled elements (using block or inline style placement within the cell)
- Code blocks
- Standard inline formatting

#### Alignment

Standard Markdown alignment syntax (`:---`, `:---:`, `---:`) works in multiline tables.

### 14.4 Interaction with Other Extensions

**Multiline Tables and Styles:** A style MAY apply to the table as a whole via a combined command (`<!-- style:DataTable ; multiline -->`) or to content within individual cells using standard style placement rules.

**Multiline Tables and Variables:** Variable tokens within multiline table cells are substituted during Phase 1, before table parsing in Phase 2.

**Multiline Tables and Conditions:** Condition blocks MAY appear within multiline table cells. Defined condition content is evaluated during Phase 1 before table parsing in Phase 2. Unset condition blocks within table content pass through as-is, including the condition tags.

**Multiline Tables and Combined Commands:** In the recommended evaluation order, the `multiline` indicator is second (after style, before markers and alias). See [section 16](#16-combined-commands).

### 14.5 Attachment Requirements

The multiline directive requires block-level attachment. The `<!-- multiline -->` tag MUST appear on the line directly above the table with no blank line.

### 14.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP009** | Orphaned multiline tag (not attached to a table element) | Warning |

### 14.7 Examples

```markdown
<!-- multiline -->
| Feature    | Capabilities             |
|------------|--------------------------|
| Variables  | Reusable content:        |
|            | - Product names          |
|            | - Version numbers        |
|            |                          |
| Conditions | Control visibility:      |
|            | 1. Platform-specific     |
|            | 2. Output format         |

<!-- style:DataTable ; multiline ; #feature-table -->
| Column | Data |
|--------|------|
| API    | REST endpoints.          |
|        | - GET /users             |
|        | - POST /users            |
```

---

## 15. Content Islands

### 15.1 Purpose

Content islands are self-contained content blocks created by applying a Markdown++ custom style to a blockquote. They provide a mechanism for callouts, notes, warnings, and other visually distinct content areas using standard CommonMark blockquote syntax with a style convention.

Content islands are not a new syntactic form. They are styled blockquotes -- standard CommonMark with a Markdown++ style applied.

### 15.2 Syntax

A content island is a standard CommonMark blockquote with a style tag on the line above:

```markdown
<!-- style:NoteBox -->
> Note content here.
```

### 15.3 Semantics

A content island is a blockquote element that carries a style annotation in the output tree. The style name determines how the processor renders the content island (e.g., as a callout box, warning panel, or information card). The rendering is implementation-defined.

#### Supported Nested Content

Blockquotes in CommonMark support rich nested content. Within a content island, the following are supported:

- Headings
- Lists (ordered and unordered)
- Code blocks (fenced)
- Nested formatting (bold, italic, links)
- Other Markdown++ extensions (variables, conditions, inline styles)

### 15.4 Interaction with Other Extensions

**Content Islands and Styles:** The style tag above the blockquote follows standard block-level attachment rules.

**Content Islands and Variables:** Variable tokens within the blockquote are substituted during Phase 1.

**Content Islands and Conditions:** Conditions MAY wrap or appear within content islands (styled blockquotes). If a condition wrapping or within a content island is Unset, the condition block passes through as-is.

### 15.5 Attachment Requirements

Content islands use standard block-level style attachment. The style tag MUST appear on the line directly above the blockquote with no blank line.

### 15.6 Diagnostics

| Code | Description | Severity |
|------|-------------|----------|
| **MDPP009** | Orphaned style tag above a blockquote (blank line breaks attachment) | Warning |

### 15.7 Examples

```markdown
<!-- style:NoteBox -->
> **Note:** This is an important note.
> It can span multiple lines.

<!-- style:WarningBox -->
> ## Warning
>
> - Check your configuration
> - Verify permissions
> - Test in staging first
```

---

## 16. Combined Commands

### 16.1 Purpose

Combined commands allow multiple Markdown++ directives to be applied to a single element through a single HTML comment. This is necessary because the attachment rule causes stacked tags to orphan the top tag -- only the bottom tag attaches to the content element.

### 16.2 Syntax

Multiple commands are joined in a single comment using semicolons as separators:

```
<!-- command1 ; command2 ; command3 -->
```

Whitespace around semicolons is optional but RECOMMENDED for readability.

The following commands MAY appear in a combined command:

| Command | Syntax |
|---------|--------|
| Style | `style:StyleName` |
| Multiline | `multiline` |
| Marker (simple) | `marker:Key="value"` |
| Alias | `#alias-name` |

Conditions (`condition:`/`/condition`) and includes (`include:`) MUST NOT appear in combined commands. They are standalone directives with distinct scoping rules.

### 16.3 Evaluation Order

When a combined command contains multiple recognized commands, a processor SHOULD evaluate them in the following order for readability and consistency, regardless of the order in which they appear in the comment. Processors MAY evaluate segments in any order.

| Order | Command | Effect |
|:-----:|---------|--------|
| 1 | `style:Name` | Associates a custom style with the target element |
| 2 | `multiline` | Marks the target table for multiline cell processing |
| 3 | `marker:Key="value"` | Attaches metadata key-value pairs |
| 4 | `#alias` | Assigns a navigational alias anchor |

### 16.4 Unrecognized Segments

Within a combined command, each semicolon-delimited segment is either a recognized command or unrecognized text. A processor MUST interpret recognized segments normally and MUST silently ignore unrecognized segments. Unrecognized segments function as **inline comments** within the directive.

```markdown
<!-- style:CustomHeading ; #alias-here ; TODO: add Keywords markers -->
# My Heading Text
```

The segments `style:CustomHeading` and `#alias-here` are recognized and applied. The segment `TODO: add Keywords markers` is unrecognized and discarded.

### 16.5 Conformance Note

Combined commands are classified as a REQUIRED feature in the [Processing Model conformance section](processing-model.md#required-features). A conformant processor MUST support combined commands. The evaluation order specified above is RECOMMENDED for author readability but processors MAY evaluate segments in any order.

### 16.6 Examples

```markdown
<!-- style:CustomHeading ; marker:Keywords="intro" ; #introduction -->
# Introduction

<!-- style:DataTable ; multiline ; #feature-table -->
| Feature | Description |
|---------|-------------|
| API     | REST endpoints. |

<!-- style:NoteBox ; marker:Priority="high" ; Reviewed 2026-03 -->
> Important information here.
```

---

## 17. Advanced Topics

### 17.1 Inline Styling for Images and Links

Style commands apply to images and links using inline placement.

#### Images

Place the style tag immediately before the image syntax on the same line with no space:

```markdown
<!--style:CustomImage-->![Logo](images/logo.png "Company Logo")
<!--style:ScreenshotStyle-->![Settings](images/settings.png)
```

The style attaches to the image element.

#### Links (Style Inside Link Text)

For links, place the style inside the link text brackets:

```markdown
[<!--style:CustomLink-->*Link text*](topics/file.md#anchor "Title")
See the [<!--style:ImportantLink-->**API Reference**](api.md#auth) for details.
```

The style applies to the formatted text within the link.

The image pattern (style before the image syntax) and the link pattern (style inside the link text brackets) are distinct. Both follow the inline attachment rule: no space between the closing `-->` and the element.

### 17.2 Book Assembly

Book assembly is the pattern of using a root document with `<!-- include: -->` directives to compose chapters into a publication. Book assembly uses the include expansion mechanism defined in the [Processing Model](processing-model.md#phase-1-step-1-include-expansion) -- it introduces no additional processing behavior.

A typical book assembly structure:

```markdown
<!-- Root file: user-guide.md -->
<!-- include:chapters/overview.md -->
<!-- include:chapters/installation.md -->
<!-- include:chapters/configuration.md -->
<!-- include:common/trademarks.md -->
```

Each included file is a standalone document that can be edited and previewed independently. The root file is purely an assembly manifest.

Cross-document concerns in assembled documents:

- **Variable scope**: All files share the same variable map.
- **Condition evaluation**: Conditions are evaluated per-file during include expansion.
- **Link references**: Definitions from all files are visible at document-global scope after assembly. See [section 17.3](#173-link-reference-definitions).

Cross-document numbering and pagination are processor-specific output concerns, outside the scope of this specification.

### 17.3 Link Reference Definitions

Link reference definitions are a standard [CommonMark 0.30][commonmark] construct. In multi-file Markdown++ assemblies, link reference resolution operates at document-global scope as a consequence of the two-phase processing model. The complete rules are defined in [Cross-File Link Reference Resolution](cross-file-link-resolution.md). A conformant processor MUST implement the rules defined therein.

#### Document-Global Scope

After Phase 1 assembles all included files into a single text, Phase 2 parses that text as CommonMark. Link reference definitions from any file in the include tree are visible to all other content in the assembled document. There is no per-file link reference scope.

#### First-Definition-Wins

When two or more definitions use the same slug, the first definition in the assembled document takes precedence, per [CommonMark 0.30 section 4.7][commonmark]. The order is determined by the depth-first include expansion. Slug matching is case-insensitive per CommonMark.

When duplicate slugs originate from different source files, a conformant processor MUST emit diagnostic **MDPP014** (severity: Warning).

#### The Semantic Cross-Reference Pattern

The recommended pattern for cross-referenceable headings combines three elements:

1. A **combined command** with a style and a numeric alias ID.
2. The **heading text**.
3. A **link reference definition** bridging a semantic slug to the alias ID.

```markdown
<!-- style:Heading2; #200010 -->
## Getting Started

[getting-started]: #200010 "Getting Started"
```

References from any file use the semantic slug:

```markdown
See [Getting Started][getting-started] for an introduction.
```

This pattern works in every context: standard Markdown viewers (slug matches heading anchor), publishing tools (alias ID resolves), and composite assemblies (cross-file resolution).

---

## 18. Diagnostic Registry

This section consolidates all MDPP diagnostic codes into a single registry. Code MDPP000 and codes MDPP001 through MDPP009 are defined for static validation. Codes MDPP010 through MDPP014 are defined for processing-phase diagnostics. Recovery behavior for each code is specified in the [Processing Model](processing-model.md#error-handling).

A fully conformant processor MUST emit all diagnostics at their specified severity levels. Pass-through conformant renderers are not required to emit diagnostics.

Implementations MAY define additional diagnostic codes for implementation-specific checks. Custom codes SHOULD use numbers MDPP100 and above to avoid conflicts with future specification-defined codes.

### 18.1 Static Validation Codes

| Code | Name | Severity | Phase | Description | Triggering Condition |
|------|------|----------|-------|-------------|---------------------|
| **MDPP000** | File not found or cannot be read | Error | Pre-processing | The input file does not exist or cannot be read | Root document path is invalid or inaccessible |
| **MDPP001** | Unclosed condition block | Error | Pre-processing | A condition block is missing its closing tag, or a closing tag has no matching opening tag | `<!-- condition:expr -->` without `<!-- /condition -->`, or vice versa |
| **MDPP002** | Invalid name | Error | Any | A named entity (variable, style, alias, or marker key) does not match its required identifier pattern | Name violates `[a-zA-Z_][a-zA-Z0-9_-]*` (standard), `[a-zA-Z0-9_][a-zA-Z0-9_-]*` (alias), or `[a-zA-Z_][a-zA-Z0-9_ -]*` trimmed (style/marker) |
| **MDPP003** | Malformed marker JSON | Error | Phase 2 | The JSON content in a `markers:` command is not valid JSON | `markers:{invalid}` |
| **MDPP004** | Invalid style placement | Warning | Phase 2 | A style command appears in a position where it cannot be applied | Style in unsupported context |
| **MDPP005** | Circular include (static) | Error | Pre-processing | Static analysis detects a circular include chain | File A includes B which includes A |
| **MDPP006** | Missing include file | Warning | Phase 1, Step 1 | An included file does not exist or cannot be read | `<!-- include:nonexistent.md -->` |
| **MDPP007** | Invalid condition syntax | Error | Phase 1, Step 1 | A condition expression cannot be parsed | `<!-- condition: -->` (empty) or malformed expression |
| **MDPP008** | Duplicate alias | Error | Phase 2 | Two alias commands in the same file use the same identifier | Two `<!-- #name -->` with the same name |
| **MDPP009** | Orphaned comment tag | Warning | Phase 2 | A recognized tag fails attachment (blank line, end of file, stacked tags) | Tag with no attached target element |

### 18.2 Processing-Phase Codes

| Code | Name | Severity | Phase | Description | Triggering Condition |
|------|------|----------|-------|-------------|---------------------|
| **MDPP010** | Undefined variable | Warning | Phase 1, Step 2 | A `$name;` token references a name not in the variable map | Variable map lacks the referenced key |
| **MDPP011** | Max include depth exceeded | Error | Phase 1, Step 1 | Include nesting exceeds the processor's configured maximum | Depth > configured limit (RECOMMENDED default: 10) |
| **MDPP012** | Cross-file condition span | Error | Phase 1, Step 1 | A condition block opens in one file and closes in another | `<!-- condition:x -->` in parent, `<!-- /condition -->` in included file |
| **MDPP013** | Include cycle detected | Error | Phase 1, Step 1 | A file appears in its own include chain during recursive expansion | Runtime cycle detection during Phase 1 |
| **MDPP014** | Duplicate link reference slug | Warning | Phase 2 | Two or more link reference definitions with the same slug originate from different source files | Cross-file slug conflict in assembled document |

---

## 19. References

### 19.1 Normative References

| Reference | Title | URL |
|-----------|-------|-----|
| [CommonMark 0.30][commonmark] | CommonMark Specification, Version 0.30 | https://spec.commonmark.org/0.30/ |
| [RFC 2119][rfc2119] | Key words for use in RFCs to Indicate Requirement Levels | https://www.ietf.org/rfc/rfc2119.txt |
| [RFC 8259][rfc8259] | The JavaScript Object Notation (JSON) Data Interchange Format | https://www.rfc-editor.org/rfc/rfc8259 |
| [Formal Grammar](formal-grammar.md) | Formal Grammar for Markdown++ Extensions | (this repository) |
| [Processing Model](processing-model.md) | The Processing Model | (this repository) |
| [Attachment Rule](attachment-rule.md) | The Attachment Rule | (this repository) |
| [Cross-File Link Reference Resolution](cross-file-link-resolution.md) | Cross-File Link Reference Resolution | (this repository) |

### 19.2 Informative References

| Reference | Title | URL |
|-----------|-------|-----|
| [GFM][gfm] | GitHub Flavored Markdown Spec | https://github.github.com/gfm/ |
| [Whitepaper](whitepaper.md) | Markdown++ Whitepaper | (this repository) |
| [Syntax Reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) | Markdown++ Syntax Reference | (this repository) |

---

[commonmark]: https://spec.commonmark.org/0.30/
[rfc2119]: https://www.ietf.org/rfc/rfc2119.txt
[rfc8259]: https://www.rfc-editor.org/rfc/rfc8259
[gfm]: https://github.github.com/gfm/
