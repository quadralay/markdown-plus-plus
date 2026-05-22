---
date: 2026-03-29
status: active
---

# Markdown++ Best Practices

Guidelines for effective use of Markdown++ extensions in documentation projects. Examples here are minimal do/don't snippets that illustrate rules -- not full patterns. For complete scenario patterns, see [`examples.md`](examples.md). For standalone specimen documents you can open and preview, see the [`examples/`](../../../../../examples/) directory.

## Declare the format version in frontmatter

**Strongly recommended:** every file using Markdown++ extensions should declare `mdpp-version: 1.0` in YAML frontmatter.

```yaml
---
mdpp-version: 1.0
---
```

This recommendation is stronger than a normative SHOULD because it has a routing-context payoff in addition to the format-versioning role. Frontmatter sits in the first lines of the file and surfaces in any reasonable read excerpt, including partial reads. With the sentinel present, downstream tooling (including the Markdown++ skill's auto-activation logic) can recognize a file as Markdown++ even when its distinguishing directives appear later in the document.

**Why this matters in practice.** A long document whose only Markdown++ signal is a `<!-- multiline -->` table past line 40 may not surface that signal during a partial read. The frontmatter sentinel guarantees a Markdown++ signal appears at the top of every such file regardless of where directive-bearing content sits.

The versioning role still holds: the declaration also signals the spec version this file targets, which downstream processors and validators can use for compatibility decisions. See [`spec/versioning.md`](../../../../../spec/versioning.md) for the full versioning rules and [`SKILL.md`](../SKILL.md)'s success criteria for the skill-side framing.

**Suggested language for downstream consumers.** Repositories authoring Markdown++ documents are encouraged to adopt the same recommendation in their own conventions, so the routing-context benefit applies wherever Markdown++ is authored. See [`tests/auto-activation/cases.md`](../tests/auto-activation/cases.md) for the manual-verification suite that exercises this convention.

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

**Aliases must be attached to their element** (no blank line between). The same attachment rule (see [GLOSSARY.md](../../../../../GLOSSARY.md#attachment-rule)) that applies to styles applies to aliases and element-level markers. See `syntax-reference.md` for the complete attachment rules table.

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
- Nesting condition blocks (not supported — use logical expressions instead)

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

**Undefined condition names (Unset) — authoring guidance:**

A condition name that is not included in the condition set at build time is **Unset** (see [GLOSSARY.md](../../../../../GLOSSARY.md#unset)). Unset condition blocks pass through the processor with their opening tags, content, and closing tags intact. This is intentional: it lets you author content for multiple output targets in a single source file, even if only some targets are active in a given build.

- **Define all active conditions explicitly.** An omitted name is not "off" — it is undefined. If you intend a block to be removed, set the condition to Hidden. If you leave it undefined, the block passes through to the output, which may not be what you want.
- **Unset is useful for staged or multi-pass builds.** A `mobile` condition block that passes through in a web build can be processed by a separate mobile pipeline in a later stage.
- **Variables inside Unset blocks are still resolved.** Even when the condition block passes through, `$variable;` tokens inside the block are substituted during Phase 1. Do not rely on pass-through to preserve unresolved variable references.
- **Compound expressions with any Unset operand always pass through.** `<!--condition:web mobile-->` passes through even if `web` is Visible, because `mobile` is Unset. Add all required condition names to the condition set before build if you need a compound block to be evaluated.

```markdown
<!-- Pass-through: mobile is Unset — block preserved with variable resolved -->
<!--condition:mobile-->
Download version $version; for mobile.
<!--/condition-->

<!-- Pass-through: tablet is Unset — even though print is Visible, OR is not evaluated -->
<!--condition:print,tablet-->
Available in print and tablet editions.
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

- Every pipe-bearing row automatically continues the current logical row; cells appear empty on a continuation line when their column has no more content to flow there
- Row separator: a pipe-bearing row whose cells are all whitespace -- this is the only way to start a new logical row
- A no-pipe blank line ends the table entirely (it does **not** separate rows)

### Table Formatting

**Tables in Markdown++ documents follow a fixed-width, vertically aligned shape** -- columns are padded to uniform width, pipes line up across every row, separator dashes span the full column width, and (for `<!-- multiline -->` tables) long content wraps to continuation rows. The full rule set is documented in [`table-formatting.md`](table-formatting.md); the canonical enforcement tool is `scripts/format-tables.py --in-place`.

**Why this matters.** Compact one-line tables overflow editor windows and PR review panes, and a one-character cell edit rewrites the entire row in version-control diffs. The formatter's output keeps column widths stable across edits, so a content change shows up as a content change, not as whitespace churn.

**Use the formatter for:**
- New tables before committing
- Tables migrated from another format
- Tables you've just edited by hand if column widths drifted

**Run it:**
```bash
python scripts/format-tables.py document.md --in-place
```

**In CI:**
```bash
python scripts/format-tables.py document.md --check
```
`--check` exits 0 if the file is already formatted, exit 4 with a unified diff otherwise.

**In-flow editing guidance for AI agents.** When editing a table by hand inside an authoring session, match the surrounding column widths -- pad new content with trailing spaces to the column's existing inner width and keep pipes vertically aligned. When in doubt, run the formatter rather than guessing. Both shapes are valid Markdown; the formatter exists so the same shape is produced consistently.

**Avoid:**
- Mixing formatted and unformatted tables in the same file -- pick one shape for the document
- Hand-tuning column widths that the formatter would produce automatically (it will undo your work on the next pass)
- Adding `<!-- multiline -->` to a standard table just to silence an over-width warning -- if the cell is genuinely long enough to wrap, the directive is a deliberate choice; otherwise, fix the content

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

**Use content islands (see [GLOSSARY.md](../../../../../GLOSSARY.md#content-island)) for:**
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

| Type              | Convention                 | Example                            |
| ----------------- | -------------------------- | ---------------------------------- |
| Product names     | lowercase with underscores | `$product_name;`                   |
| Versions          | descriptive                | `$version;`, `$api_version;`       |
| URLs              | descriptive with suffix    | `$download_url;`, `$support_url;`  |
| Dates             | descriptive                | `$release_date;`, `$last_updated;` |
| Platform-specific | platform prefix            | `$windows_path;`, `$mac_path;`     |

## Condition Naming Conventions

| Type          | Convention       | Example                                |
| ------------- | ---------------- | -------------------------------------- |
| Output format | format name      | `web`, `print`, `pdf`, `chm`           |
| Platform      | platform name    | `windows`, `mac`, `linux`              |
| Audience      | audience level   | `beginner`, `advanced`, `admin`        |
| Environment   | environment name | `production`, `development`, `staging` |
| Feature flags | feature name     | `feature_x`, `beta_feature`            |

## Style Naming Conventions

| Type           | Convention          | Example                            |
| -------------- | ------------------- | ---------------------------------- |
| Headings       | `Heading` + context | `HeadingChapter`, `HeadingSection` |
| Notes/Callouts | Box type            | `NoteBox`, `WarningBox`, `TipBox`  |
| Code           | `Code` + type       | `CodeExample`, `CodeOutput`        |
| Tables         | `Table` + purpose   | `TableData`, `TableComparison`     |
| UI Elements    | `UI` + element      | `UIButton`, `UIMenu`               |

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

**Removing rather than authoring directives?** Cleanup edits (removing redundant `<!--style:-->` comments, simplifying style names, deleting non-heading anchors) follow a different rule set than authoring. See [`comment-manipulation.md`](comment-manipulation.md) for the safe-removal rules and the table-cell edge cases that make hand-removal error-prone.

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

## Semantic Cross-References on Topic-Defining Headings

**Recommended** for file titles, primary H1s, and structurally important H2 headings. The alias+slug+linkref triple makes a heading externally referenceable with a stable, semantic name. The same reference works in standalone preview, single-file publishing, and multi-file assembly, and the three pieces stay aligned as content evolves.

The pattern combines three pieces:

```markdown
<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"
```

1. The `<!-- style:HeadingN; #target -->` directive attaches a stable alias (`#200020`) to the heading. The alias does not change when you reword the heading.
2. The heading line provides the human-visible label.
3. The link reference definition binds a semantic slug (`installation`) to the stable alias and supplies a default link text via the trailing title.

### Choosing the slug

Two conformant variants. Pick by where the alias comes from.

**Semantic slug + opaque alias** (hand-authored aliases, publishing-tool numeric IDs). The alias carries no human meaning; the slug supplies the readable handle:

```markdown
<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"
```

**Slug = alias value** (generated anchors, automation pipelines, agent-minted IDs). The alias is itself semantic and unique-by-construction -- meaning the minting process guarantees the value is unique across the entire assembled document, not merely within one file. The slug reuses the same value so the heading carries one identifier, not two:

```markdown
<!-- style:Heading2; #sh-ug-installation -->
## Installation

[sh-ug-installation]: #sh-ug-installation "Installation"
```

**Rule of thumb:** if the alias is opaque, pair it with a semantic slug. If the alias is itself semantic and unique-by-construction, the slug = alias variant is the cleaner fit -- one identifier per heading instead of two, and an authoring agent only has to mint and track the alias.

**All three pieces appear adjacent:** the directive on the line directly above the heading, the heading itself, a single blank line, then the link reference definition on the next line. Co-location is part of the pattern, not a layout choice -- do not migrate the link reference definitions to a block at the bottom of the file in conventional CommonMark style.

References elsewhere in the assembly use the slug:

```markdown
See [Installation][installation] for setup instructions.
If setup fails, return to [Installation][installation].
```

**Why this is the recommended idiom:**

- **Cross-context resolution.** The same reference works whether the file is rendered standalone, published as a single document, or assembled with `<!-- include: -->` into a larger document. Link reference definitions resolve at document-global scope after assembly, so references in one file resolve to definitions in another. Inline anchor links (`[text](#anchor)`) cannot give you this -- they only resolve in the standalone or single-file case.

- **Anti-drift.** Two distinct axes:

  - *Heading-rename drift.* The alias decouples the link target from heading text. Reword the heading from "Installation" to "Installing the Product" and the reference still resolves because the alias `#200020` is what binds them. An alias plus an inline anchor link gets this benefit on its own; the triple's contribution is to extend the same benefit to assembly-wide reference-style links and to readers who rely on the slug as the human-readable handle.
  - *Section-move drift.* Because the three pieces sit adjacent in source, a section move, deletion, or reorder carries the directive and the link reference definition along with the heading. Splitting them across the file -- for example, collecting all link reference definitions in a block at the bottom -- means a section move can silently desync the slug from its target. The validator cannot detect a silent slug-target desync; the layout is what prevents it. This benefit is the one inline anchor links and bottom-of-file linkref tables cannot give you.

- **Intent signal.** A custom alias on a heading already implies the heading is meant to be externally referenceable. The paired link reference definition completes that intent and tells the next author this heading is a public reference point, not an internal anchor.

**For generated-anchor and pipeline workflows:** authoring agents and publishing pipelines that mint unique anchors (contextual IDs like `sh-ug-installation`, hash-derived slugs, registry-issued identifiers) get a specific win from the slug = alias variant. The pipeline already produces one unique semantic identifier per heading; reusing it as the slug eliminates a parallel naming vocabulary and the slug<->alias mapping table the pipeline would otherwise have to maintain. The link reference definition still does real work in this variant: it gives the pipeline's anchor a cross-assembly reference handle, and the co-located placement keeps the three pieces moving together through edits.

### Inline anchor links vs. the triple

Readers already using inline anchor links (`[text](#anchor)`) within a single document or a single assembled file often ask what the triple replaces and what it adds. The two patterns overlap on within-document linking; they diverge on cross-file resolution and on what stays aligned when content moves.

| Property                       | Inline anchor link `[text](#anchor)`                                       | alias+slug+linkref triple                                                                            |
| ------------------------------ | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Within-document linking        | Works                                                                      | Works                                                                                                |
| Cross-file (assembled) linking | Does not resolve across `<!-- include: -->` boundaries                     | Resolves at document-global scope after assembly                                                     |
| Heading-rename safety          | Yes, when the anchor is a custom alias                                     | Yes, via the alias -- and slug<->alias binding survives the rename                                   |
| Section-move safety            | Partial -- the heading anchor moves with the heading, but call sites scattered through the file are not co-located and nothing binds the slug-to-anchor pairing if the anchor is renamed | Yes -- directive, heading, and link reference definition move together as a unit                     |
| Default link text              | Author writes it inline at every call site                                 | Comes from the link reference definition's trailing title                                            |
| Authoring overhead per heading | Author writes the link text at each reference                              | One link reference definition adjacent to the heading; references use the slug                       |
| Best fit for                   | Within-assembly-only references with no cross-file or future-assembly need | Cross-file resolution, future-proofing for assembly, or any heading the next author may deep-link to |

**When the inline anchor link is enough.** A document that will only ever be rendered standalone or as a single file, with anchors you control and references you can grep for, can stay on inline anchor links. The triple's cross-file resolution and section-move safety are paying for capacity you do not use.

**When the triple is worth the extra structure.** As soon as the document is a candidate for inclusion in a multi-file assembly, or the heading is one a reader (human or agent) elsewhere in the project will deep-link to, the triple's cross-context resolution and section-move safety start mattering. The pattern is forward-compatible: a triple authored today on a standalone file keeps working when the file is later assembled.

**When the rule fires:** Apply on the file's title (H1), and on H2 headings that name a major section a reader is likely to deep-link to. Below H2 is author judgement -- not blanket policy.

**When the rule does not fire:** A custom alias used only as an internal anchor (no external references expected) is valid on its own. Do not pair every alias with a link reference definition reflexively.

**Cross-file behavior:** If two files define the same slug with different targets, the first definition in assembled document order wins and the processor emits **MDPP014**. See the [Cross-File Link Reference Resolution](../../../../../spec/cross-file-link-resolution.md) specification for the full resolution rules, and Worked Examples A and B in that document for the canonical pattern at full length.

## Advanced Patterns

### Link References

Link references are a standard Markdown feature that allow defining link targets separately from their usage. Outside the topic-heading idiom in [Semantic Cross-References on Topic-Defining Headings](#semantic-cross-references-on-topic-defining-headings), link references are **generally not recommended** for general-purpose link reuse because they add indirection that makes content harder to understand and maintain.

**Placement differs from the triple pattern.** General-purpose link reference definitions are conventionally grouped at the bottom of the file -- the standard CommonMark style. The triple's link reference definition, by contrast, lives adjacent to its heading (see [Semantic Cross-References on Topic-Defining Headings](#semantic-cross-references-on-topic-defining-headings)). Both placements are valid CommonMark, but the conventions encode different intent: grouped definitions signal "this is a shared URL table that many parts of the document point at"; adjacent definitions signal "this is the semantic slug for *this* heading, and the two move together." Do not migrate triple definitions into the bottom-of-file block.

**Standard inline links (recommended):**
```markdown
See [Installation](#installation) for setup instructions.
Visit the [API Documentation](https://docs.example.com/api).
```

**General-purpose link references (advanced):**
```markdown
See [Installation][install-guide] for setup instructions.
Visit the [API Documentation][api-docs].

[install-guide]: #installation
[api-docs]: https://docs.example.com/api
```

**Why inline links are preferred for general-purpose use:**
- Self-contained and easier to understand
- AI-assisted authoring works better with explicit links
- No need to hunt for where references are defined
- Simpler mental model for authors

**When general-purpose link references may be useful:**
- Redirecting links based on document context (e.g., pointing to the latest API version)
- Conditional link targets for different output formats
- Very long URLs that clutter the text

**Example - version redirection:**
```markdown
See the [API Reference][latest-api] for endpoint details.

[latest-api]: apis/api-v2.0.md#reference
```

When a new API version is released, only the reference definition needs updating.

**Tradeoffs:**
- Adds complexity and indirection
- Makes AI-generated content more difficult
- Requires authors to look in multiple places
- Harder to validate link integrity

---

## See Also

- **[`examples/`](../../../../../examples/)** -- Standalone specimen documents with real Markdown++ directives. Open, preview, and validate these files directly.
- **[`examples.md`](examples.md)** -- Scenario-oriented patterns in fenced code blocks, curated for AI skill context.
