---
date: 2026-03-29
status: active
---

# Markdown++ Best Practices

Guidelines for effective use of Markdown++ extensions in documentation projects.

## Start with Markdown, extend where needed

Every Markdown++ file is a valid Markdown file. Start by writing standard Markdown -- headings, paragraphs, lists, tables, links, images -- using any editor or previewer you already know. Add Markdown++ extensions only where they provide value: a `<!-- style: -->` directive when you need custom output formatting, a `$variable;` when a value repeats across documents, a `<!-- condition: -->` block when content varies by audience or output format. Standard Markdown tools remain part of your workflow throughout. The extensions are additive, not a replacement for the Markdown you already write.

## When to Use Each Extension

### Variables

**Use variables for:**
- Product names that might change
- Version numbers updated per release
- URLs that may be environment-specific
- Repeated content across multiple documents
- Values defined centrally in a publishing project

**Avoid variables for:**
- One-time text that won't repeat
- Content that varies significantly between uses
- Complex formatted content (use includes instead)

**Example - Good:**
```markdown
Welcome to $product_name; version $version;.
Download from $download_url;.
```

**Escaping variables:**

When you need a literal `$name;` in published output, use one of two mechanisms:

```markdown
The variable syntax is \$variable_name; with a trailing semicolon.
```

Or use inline code when showing syntax examples:

```markdown
Use the `$variable_name;` syntax to define variables.
```

Use backslash escaping (`\$`) for running prose; use inline code for syntax examples and code references.

**Example - Avoid:**
```markdown
$intro_paragraph;  <!-- Too much content in a variable -->
```

### Custom Styles

**Use styles for:**
- Consistent formatting across documents
- Semantic meaning beyond basic Markdown
- Output format-specific rendering
- Tables, code blocks, callouts that need custom treatment

**Avoid styles for:**
- Every heading and paragraph (overuse)
- Content where standard Markdown formatting suffices
- Styles that aren't defined in your publishing configuration

**Block vs. Inline:**
- Use **block styles** for headings, paragraphs, lists, code blocks, tables
- Use **inline styles** for emphasized text within paragraphs
- Block commands must be attached (no blank line between command and element)
- Inline commands have no space before the styled element

**Example - Good:**
```markdown
<!--style:WarningBox-->
> **Warning:** This action cannot be undone.

This is <!--style:UIElement-->**Settings** button.
```

**Example - Wrong (blank line breaks association):**
```markdown
<!--style:CustomParagraph-->

This paragraph will NOT receive the style.
```

**Nested list styling (proper indentation):**
```markdown
<!-- style:BulletList1 -->
- Bullet 1

  <!-- style:BulletList2 -->
  - Bullet 2
```

**Example - Avoid:**
```markdown
<!--style:NormalParagraph-->
This is just regular text that doesn't need a style.
```

### Custom Aliases

**Aliases are block-level only** -- they must appear on their own line above a block element. Inline aliases are not supported.

**Use aliases for:**
- **All important headings** to ensure stable URL endpoints
- Stable links that survive document restructuring
- Cross-document linking
- Links to non-heading elements
- Section anchors with custom names

**Avoid aliases for:**
- Temporary content
- Internal drafts

**Keep alias values unique within each file.** The validation script checks for duplicates.

**Aliases must be attached to their element** (no blank line between). The same attachment rule that applies to styles applies to aliases and element-level markers. See `syntax-reference.md` for the complete attachment rules table.

**Example - Good:**
```markdown
<!--#api-authentication-->
## Authenticating with the API

Later: See [Authentication](#api-authentication) for details.
```

**Generate aliases automatically:**
```bash
python scripts/add-aliases.py document.md --levels 1,2,3
```

### Conditions

**Use conditions for:**
- Platform-specific content (Windows/Mac/Linux)
- Output format differences (web/print/PDF)
- Audience-specific content (beginner/advanced)
- Development vs. production content
- Internal vs. external documentation

**Avoid conditions for:**
- Minor text differences (use variables instead)
- Content that should always appear
- Deeply nested conditions (hard to maintain)

**Example - Good:**
```markdown
<!--condition:windows-->
Download the `.exe` installer.
<!--/condition-->

<!--condition:mac-->
Download the `.dmg` disk image.
<!--/condition-->
```

**Example - Avoid:**
```markdown
<!--condition:windows-->
Click <!--condition:windows10-->Start<!--/condition--><!--condition:windows11-->the Windows icon<!--/condition-->...
<!--/condition-->
```

### File Includes

**Use includes for:**
- Topic map structure (top-level file includes chapters)
- Reusable content blocks
- Modular documentation structure
- Common examples or code snippets
- Boilerplate legal text

**Avoid includes for:**
- Very small content (inline it instead)
- Content that varies significantly per use
- Creating deeply nested include chains

**Example - Topic map pattern:**
```markdown
<!--include:introduction.md-->
<!--include:getting_started.md-->
<!--include:configuration.md-->
```

### Markers

**Use markers for:**
- Search keywords for web output
- Document metadata (author, category)
- Content that needs special processing
- Passthrough text for output formats

**Avoid markers for:**
- Information already in document content
- Excessive keyword stuffing
- Markers that aren't processed by your output format

**Preferred format (single key-value):**
```markdown
<!--marker:Keywords="installation, setup"-->
```

**JSON format (multiple markers):**
```markdown
<!--markers:{"Keywords": "installation, setup, getting started", "Category": "User Guide"}-->
```

### Multiline Tables

**Use multiline tables for:**
- Complex data requiring lists or blockquotes in cells
- Feature comparisons with detailed descriptions
- Reference tables with examples
- Content that doesn't fit in single-line cells

**Avoid multiline tables for:**
- Simple tabular data
- Tables where standard Markdown works

**Multiline table structure:**
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

- Continuation rows use empty first cell (`|      |`)
- Empty row with borders separates table rows

### Combined Commands

**Order priority:** style, multiline, marker(s), #alias

```markdown
<!-- style:ImportantHeading ; marker:Priority="high" ; #critical-section -->
## Critical Section

<!-- style:DataTable ; multiline ; #comparison-table -->
| Column | Data |
|--------|------|
```

**Avoid:** Inconsistent ordering that makes documents harder to read.

### Inline Styling for Images

**Use inline styles for:**
- Logo images requiring specific formatting
- Screenshots with consistent borders/shadows
- Icons that need size control

### Inline Styling for Links

**Use inline styles for:**
- External links that need visual distinction
- Important reference links
- UI element links

**Key rule:** Place style inside the link text brackets, not before the entire link syntax.

### Content Islands (Blockquotes)

**Use content islands for:**
- Learning boxes with multiple content types
- Warning/caution callouts with lists
- Tips with code examples
- Any "block within a block" layout

**Best practice:** Include a heading inside the blockquote for accessibility. Use custom styles when you need different types of content islands (e.g., `BQ_Learn`, `BQ_Warning`).

## Document Structure

### Recommended Organization

Use a top-level topic map file with includes and markers to organize multi-chapter documents. Place document-level markers above the Title paragraph at the start of the file.

### Condition Placement

**Do:** Keep conditions at natural content boundaries

```markdown
<!--condition:web-->
## Web-Only Section

Content here...
<!--/condition-->
```

**Don't:** Fragment content with many small conditions

```markdown
## Section
<!--condition:web-->Word<!--/condition--><!--condition:print-->Text<!--/condition--> here.
```

### Include Organization

Use the topic map pattern - a top-level file includes chapter-level files:

```
docs/
├── _user-guide.md       # Top-level topic map with includes
├── introduction.md      # Introduction chapter
├── getting_started.md   # Getting started chapter
├── configuration.md     # Configuration chapter
├── advanced_topics.md   # Advanced topics chapter
└── shared/
    └── code-samples.md  # Reusable code examples
```

The top-level file (`_user-guide.md`) contains the document title, markers, and includes for each chapter.

## Variable Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Product names | lowercase with underscores | `$product_name;` |
| Versions | descriptive | `$version;`, `$api_version;` |
| URLs | descriptive with suffix | `$download_url;`, `$support_url;` |
| Dates | descriptive | `$release_date;`, `$last_updated;` |
| Platform-specific | platform prefix | `$windows_path;`, `$mac_path;` |

## Condition Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Output format | format name | `web`, `print`, `pdf`, `chm` |
| Platform | platform name | `windows`, `mac`, `linux` |
| Audience | audience level | `beginner`, `advanced`, `admin` |
| Environment | environment name | `production`, `development`, `staging` |
| Feature flags | feature name | `feature_x`, `beta_feature` |

## Style Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Headings | `Heading` + context | `HeadingChapter`, `HeadingSection` |
| Notes/Callouts | Box type | `NoteBox`, `WarningBox`, `TipBox` |
| Code | `Code` + type | `CodeExample`, `CodeOutput` |
| Tables | `Table` + purpose | `TableData`, `TableComparison` |
| UI Elements | `UI` + element | `UIButton`, `UIMenu` |

## Common Mistakes to Avoid

### 1. Breaking the Attachment Rule (Blank Lines, Ordering, Stacking)

**The attachment rule is the most common source of Markdown++ errors.** Styles, aliases, markers, and combined commands must be on the line directly above their target element with no blank line between. A blank line silently breaks the association -- the tag passes through as a regular HTML comment with no visible error. See the [Attachment Rule specification](../../../../../spec/attachment-rule.md) for the formal definition and all edge cases.

**Wrong -- blank line breaks attachment (styles):**
```markdown
<!--style:CustomHeading-->

# Heading
```

**Wrong -- blank line breaks attachment (aliases and markers):**
```markdown
### Installation

<!-- marker:IndexMarker="setup" ; #installation -->

Follow these steps to install...
```

**Wrong -- tag below content (tags attach downward only):**
```markdown
## Getting Started
<!-- #getting-started -->
```

**Wrong -- stacked tags (top tag is orphaned):**
```markdown
<!-- style:CustomHeading -->
<!-- #my-alias -->
## Heading
```

**Right -- all commands attached directly above target:**
```markdown
<!--style:CustomHeading-->
# Heading
```

```markdown
<!-- marker:IndexMarker="setup" ; #installation -->
### Installation

Follow these steps to install...
```

```markdown
<!-- #getting-started -->
## Getting Started
```

**Right -- combine commands with semicolons instead of stacking:**
```markdown
<!-- style:CustomHeading ; #my-alias -->
## Heading
```

**Note:** Conditions (`condition:`/`/condition`) are exempt because they wrap content. Includes (`include:`) are exempt because they are standalone directives. Markers at the start of a file are not exempt -- they are attached to the Title paragraph that follows them.

### 2. Missing Semicolons on Variables

**Wrong:**
```markdown
Welcome to $product_name, version $version.
```

**Right:**
```markdown
Welcome to $product_name;, version $version;.
```

### 3. Space Before Inline Style Target

**Wrong:**
```markdown
This is <!--style:Emphasis--> **bold**.
```

**Right:**
```markdown
This is <!--style:Emphasis-->**bold**.
```

### 4. Forgetting to Close Conditions

**Wrong:**
```markdown
<!--condition:web-->
Web content here...
<!-- Forgot to close! -->
```

**Right:**
```markdown
<!--condition:web-->
Web content here...
<!--/condition-->
```

### 5. Invalid JSON in Markers

**Wrong:**
```markdown
<!--markers:{Keywords: "test"}--> <!-- Missing quotes on key -->
```

**Right:**
```markdown
<!--markers:{"Keywords": "test"}-->
```

### 6. Circular Includes

**Wrong:**
```
main.md includes header.md
header.md includes main.md  <!-- Circular! -->
```

**Right:**
Ensure include chains never loop back.

## Performance Considerations

1. **Limit include depth** - Deep nesting slows processing
2. **Avoid excessive conditions** - Each adds processing overhead
3. **Keep marker JSON simple** - Complex structures slow parsing
4. **Use variables for repeated content** - Reduces document size

## Testing Your Documents

1. Run the validation script before publishing:
   ```bash
   python scripts/validate-mdpp.py document.md
   ```

2. Test with different condition combinations

3. Verify all includes resolve correctly

4. Check that variable values are defined in your publishing project

5. Preview output before final publish

## Advanced Patterns

### Link References

Link references are a standard Markdown feature that allow defining link targets separately from their usage. While supported, they are **generally not recommended** for most documentation because they add indirection that makes content harder to understand and maintain.

**Standard inline links (recommended):**
```markdown
See [Installation](#installation) for setup instructions.
Visit the [API Documentation](https://docs.example.com/api).
```

**Link references (advanced):**
```markdown
See [Installation][install-guide] for setup instructions.
Visit the [API Documentation][api-docs].

[install-guide]: #installation
[api-docs]: https://docs.example.com/api
```

**Why inline links are preferred:**
- Self-contained and easier to understand
- AI-assisted authoring works better with explicit links
- No need to hunt for where references are defined
- Simpler mental model for authors

**When link references may be useful:**
- Redirecting links based on document context (e.g., pointing to the latest API version)
- Conditional link targets for different output formats
- Very long URLs that clutter the text
- **Semantic cross-references in multi-file assemblies** -- the primary use case for link references in Markdown++

**Example - version redirection:**
```markdown
See the [API Reference][latest-api] for endpoint details.

[latest-api]: apis/api-v2.0.md#reference
```

When a new API version is released, only the reference definition needs updating.

**Example - semantic cross-references across files:**

In multi-file documentation assembled with `<!-- include: -->`, link reference definitions bridge human-readable slugs to alias IDs across all included files:

```markdown
<!-- In chapters/installation.md -->
<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"
```

```markdown
<!-- In chapters/troubleshooting.md -->
If the issue persists, re-run [Installation][installation].
```

The reference in `troubleshooting.md` resolves to the definition in `installation.md` because all included files share document-global scope after assembly. If two files define the same slug with different targets, the first definition in assembled document order wins and the processor emits **MDPP014**. See `spec/cross-file-link-resolution.md` for the full resolution rules.

**Tradeoffs:**
- Adds complexity and indirection
- Makes AI-generated content more difficult
- Requires authors to look in multiple places
- Harder to validate link integrity
