---
date: 2026-04-07
status: active
---

# The Attachment Rule

## Definition

The **Attachment Rule** governs the relationship between Markdown++ comment tags and the content elements they modify. A comment tag is **attached** to a target element when the tag and the element appear on immediately adjacent lines with zero blank lines between them.

A blank line between a tag and its intended target **breaks attachment silently**. The tag passes through as a regular HTML comment with no Markdown++ effect, and no error is visible in standard Markdown preview. This makes the attachment rule the most common source of Markdown++ authoring errors.

## Formal Statement

1. **Block-level tags** MUST appear on the line directly **above** the target element with no intervening blank line.
2. **Inline tags** MUST appear immediately **before** the styled element on the same line, with no space between the closing `-->` and the element.
3. A single blank line between a tag and its target breaks the attachment. Multiple blank lines have the same effect as one.
4. Tags attach **downward only** -- a tag placed below content does not attach to the content above it.

## Which Tags Require Attachment

| Tag Type | Requires Attachment | Notes |
|----------|:-------------------:|-------|
| `style:` (block) | Yes | Line directly above target element |
| `style:` (inline) | Yes | Immediately before target, no space |
| `#alias` | Yes | Line directly above target element |
| `marker:` / `markers:` | Yes | Line directly above target element |
| `multiline` | Yes | Line directly above the table |
| Combined commands (`;`) | Yes | Same rules as individual commands |

## Exempt Tags

| Tag Type | Why Exempt |
|----------|-----------|
| `condition:` / `/condition` | Wraps content -- blank lines within the condition block are permitted and expected |
| `include:` | Standalone directive -- inserts file contents at the tag's position |

## What "Target Element" Means

The target element is the first content-bearing line immediately following the tag. The element type determines what receives the tag's effect:

| Target Element | Starts With | Example |
|---------------|-------------|---------|
| Heading | `#` | `## Section Title` |
| Paragraph | Text (no prefix) | `This is a paragraph.` |
| Unordered list | `-`, `*`, `+` | `- List item` |
| Ordered list | `1.`, `2.`, etc. | `1. First step` |
| Blockquote | `>` | `> Quoted text` |
| Code fence | ` ``` ` | ` ```python ` |
| Table | `\|` (header row) | `\| Column A \| Column B \|` |
| Setext heading | Text followed by `===` or `---` | `Title` (with underline on next line) |

## Edge Cases

### 1. Two Tags in Sequence

When two separate tags appear on consecutive lines above content, only the **bottom tag** attaches to the content. The top tag is orphaned because its next line is another tag, not a content element.

**Problem:**
```markdown
<!-- style:CustomHeading -->
<!-- #my-alias -->
## Heading Text
```

The style tag is orphaned -- its next line is the alias tag, not the heading. Only the alias attaches to the heading.

**Solution -- combine with semicolons:**
```markdown
<!-- style:CustomHeading ; #my-alias -->
## Heading Text
```

Both commands apply to the heading.

### 2. Tag, Blank Line, Content

The most common error. A blank line between the tag and its target breaks attachment.

**Wrong:**
```markdown
<!-- style:NoteBox -->

> Important information here.
```

**Right:**
```markdown
<!-- style:NoteBox -->
> Important information here.
```

### 3. Tag Below Content

Tags attach downward only. A tag placed after content does not apply to the content above it.

**Wrong:**
```markdown
## Getting Started
<!-- #getting-started -->

This paragraph does not receive the alias, and neither does the heading.
```

**Right:**
```markdown
<!-- #getting-started -->
## Getting Started
```

### 4. Tag at End of File

A tag with no following content is orphaned. There is no element to attach to.

**Orphaned:**
```markdown
Some final paragraph.

<!-- style:Trailing -->
```

### 5. Nested List Indentation

When styling a nested list item, the tag must be indented to match the nesting level of the target list item.

**Wrong -- tag at wrong indentation:**
```markdown
<!-- style:BulletList2 -->
  - Nested item
```

**Right:**
```markdown
  <!-- style:BulletList2 -->
  - Nested item
```

The tag's indentation must match the content line's indentation.

### 6. Tags Inside Condition Blocks

Tags inside condition blocks still follow the attachment rule. The condition wrapper does not change how styles, aliases, or markers attach to their target elements.

**Right:**
```markdown
<!--condition:print-->
<!-- style:PrintHeading -->
## Print-Only Heading
<!--/condition-->
```

**Wrong:**
```markdown
<!--condition:print-->
<!-- style:PrintHeading -->

## Print-Only Heading
<!--/condition-->
```

The blank line inside the condition block breaks the style's attachment to the heading.

### 7. Multiple Blank Lines

Multiple blank lines have the same effect as a single blank line -- attachment is broken. There is no "closer means more attached" behavior.

**Wrong (all equivalent):**
```markdown
<!-- style:Custom -->

## Heading

<!-- style:Custom -->


## Heading

<!-- style:Custom -->



## Heading
```

All three are broken. Only zero blank lines preserves attachment.

## Validation

The validation script (`validate-mdpp.py`) detects orphaned tags as check **MDPP009** (severity: Warning). A tag is orphaned when:

- A blank line follows the tag before the next content line
- The tag is at the end of the file with no following content
- The tag's next line is another tag (the top tag in a stacked pair)

## Relationship to Comment Disambiguation

The attachment rule is independent of comment disambiguation. A comment must first be **recognized** as a Markdown++ directive (by matching a known command pattern). Only recognized directives are subject to the attachment rule. Regular HTML comments that do not match any command pattern are ignored entirely -- they are neither attached nor orphaned.

See the [Comment Disambiguation](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md#comment-disambiguation) section of the syntax reference for how processors distinguish directives from regular comments.
