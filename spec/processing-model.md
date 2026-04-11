---
date: 2026-04-08
status: active
---

# The Processing Model

## Introduction

This document specifies how a conformant Markdown++ processor evaluates extensions to produce deterministic output. It defines the character encoding requirement, processing pipeline, evaluation order, scoping rules, error behavior, and output model that all conformant implementations MUST follow.

The [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) defines what each extension looks like. This document defines how those extensions are evaluated at processing time. The [Attachment Rule](attachment-rule.md) defines how block-level tags bind to content elements. [Format Versioning](versioning.md) defines how documents declare their target specification version and how processors handle version mismatches. Together, these four documents form the normative specification for the Markdown++ format.

The processing model formalizes the two-phase pipeline that the ePublisher Markdown++ adapter has used in production. By extracting and standardizing this model, Markdown++ becomes a format that other tools can implement with confidence.

## Definitions

**Document** -- A Markdown++ source file (`.md`) containing CommonMark content and zero or more Markdown++ extensions (variables, conditions, styles, includes, markers, aliases, multiline tables).

**Processor** -- A software tool that reads a Markdown++ document, evaluates its extensions according to this specification, and produces an output tree. A processor accepts a document, a variable map, and a condition set as inputs.

**Variable map** -- A key-value collection where each key is a variable name (matching the naming rule `[a-zA-Z_][a-zA-Z0-9_\-]*`) and each value is a string. The variable map is provided to the processor at build time. This specification does not prescribe how the map is populated -- environment variables, configuration files, CLI flags, and API parameters are all valid sources.

**Condition set** -- A collection of condition names, each assigned a state of **Visible** or **Hidden**. A condition name not defined in the condition set is **Unset** (undefined). The condition set is provided to the processor at build time. This specification does not prescribe how the set is populated.

**Condition state** -- One of three values:

| State | Meaning |
|-------|---------|
| **Visible** | The condition is active. Content inside the condition block is included in output. |
| **Hidden** | The condition is suppressed. Content inside the condition block is removed from output. |
| **Unset** | The condition name is not defined in the condition set. The condition block passes through without evaluation -- the opening tag, content, and closing tag are preserved as-is in the output. |

**Attachment** -- The relationship between a Markdown++ comment tag and the content element it modifies. See the [Attachment Rule](attachment-rule.md) for the complete definition.

**Include chain** -- The sequence of files from the root document through each nested include to the current file being processed. Used for cycle detection and depth tracking.

**Recognized comment** -- An HTML comment whose content matches at least one Markdown++ command pattern (style, alias, marker, condition, include, or multiline). Comments that do not match any pattern are treated as regular HTML comments and ignored by the processor. See [Comment Disambiguation](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md#comment-disambiguation) in the syntax reference.

**Conformance keywords** -- The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt). All conformance statements apply to processors, not to document authors.

## Character Encoding

Markdown++ documents MUST be encoded in UTF-8, consistent with [CommonMark 0.30 §2.1](https://spec.commonmark.org/0.30/#characters-and-lines). A conformant processor MUST decode document bytes as UTF-8 before any Phase 1 processing begins. This requirement applies to the root document and all files resolved through include expansion.

### BOM Handling

A UTF-8 Byte Order Mark (U+FEFF, encoded as the byte sequence `EF BB BF`) at the start of a file is OPTIONAL. A conformant processor MUST strip a leading BOM before further processing -- the BOM is not considered part of the document content.

A BOM MUST only appear at the very beginning of a file. If include expansion produces a BOM at a position other than the start of the final resolved document (for example, when an included file begins with a BOM and is spliced into the middle of a parent document), the processor MUST strip the embedded BOM during include expansion so it does not appear in the resolved text.

### Encoding Errors

When a processor encounters an invalid UTF-8 byte sequence while reading a file, it MUST emit diagnostic **MDPP017** (severity: Error). The diagnostic MUST include the file path of the file containing the invalid byte sequence. The line number SHOULD be the line containing the first invalid byte, computed from the valid bytes decoded before the error. If the processor cannot determine a meaningful line number (for example, when the error occurs before any line ending is decoded), it SHOULD report line 1.

A processor SHOULD emit **MDPP017** on the first invalid byte sequence in a file. Invalid encoding corrupts character boundaries, making further parsing of the affected file unreliable. A processor MAY attempt to collect multiple encoding errors within a single file, but MUST NOT use the file's content for further pipeline processing (variable substitution, Markdown parsing, or output generation). The processor SHOULD continue processing other files in the include chain.

Recovery behavior (such as byte substitution or fallback to an alternative encoding) is implementation-defined. A processor that implements recovery MUST still emit **MDPP017** regardless of whether recovery succeeds.

### Include Chain Encoding Consistency

All files in an include chain MUST be encoded in UTF-8. When a processor reads a file during include expansion (step 1 of the [include algorithm](#algorithm)), it MUST validate the file's encoding. If the file contains invalid UTF-8, the processor MUST emit **MDPP017** with the offending file's path -- not the path of the root document or the parent file that referenced it.

This ensures that encoding errors are traceable to their source file, even in deeply nested include chains.

## Pipeline Overview

Processing a Markdown++ document is a two-phase operation with an optional preamble step. **Phase 1** operates on raw text before any Markdown parsing occurs. **Phase 2** parses the resolved text as Markdown with extension-aware grammars. The phases are strictly sequential -- Phase 2 MUST NOT begin until Phase 1 is complete.

**Preamble: Version Check** (optional)

0. **Version Check** -- Extract the `mdpp-version` field from the root document's YAML frontmatter. If present, compare the declared version against the processor's supported specification version and emit MDPP015 or MDPP016 if a mismatch is detected. See [Format Versioning](versioning.md) for the complete rules.

**Phase 1: Pre-Processing** (text-level transforms)

1. **Include Expansion** -- Recursively resolve `<!-- include:path -->` directives, evaluating each included file's conditions per-file before splicing its content into the parent.
2. **Variable Substitution** -- Replace `$name;` tokens with values from the variable map.

**Phase 2: Markdown Parsing with Extension Extraction**

3. **Parsing and Rendering** -- Parse the Phase 1 output text as CommonMark 0.30, extracting style, alias, marker, and multiline commands from recognized HTML comments during parsing.

The output of the pipeline is a CommonMark document tree annotated with Markdown++ metadata. Given the same input document, variable map, and condition set, a conformant processor MUST produce the same output tree.

## Processing Phases

### Phase 1, Step 1: Include Expansion

Include expansion resolves all `<!-- include:path -->` directives in the document, recursively inserting the content of referenced files. This step also evaluates conditions on a per-file basis during the expansion process.

#### Algorithm

A processor MUST resolve includes using the following depth-first recursive algorithm:

1. Read the current file's content, decoding as UTF-8 and stripping any leading BOM per [Character Encoding](#character-encoding). If the file contains invalid UTF-8, emit **MDPP017** and stop processing the affected file.
2. Evaluate the current file's condition blocks using the project's condition set (see [Per-File Condition Evaluation](#per-file-condition-evaluation) below).
3. Scan the resolved content for `<!-- include:path -->` directives.
4. For each include directive, in document order:
   a. Resolve the path relative to the current file's directory.
   b. Check the include chain for cycles. If the resolved path already appears in the chain, skip the include with diagnostic **MDPP013** and leave the include tag in place as a regular HTML comment.
   c. Check the include depth. If the depth exceeds the processor's configured maximum, skip the include with diagnostic **MDPP011** and leave the include tag in place.
   d. If the file does not exist or cannot be read, emit diagnostic **MDPP006** and leave the include tag in place as a regular HTML comment.
   e. If the file contains invalid UTF-8 encoding (detected during step 1), emit diagnostic **MDPP017** and leave the include tag in place as a regular HTML comment.
   f. Otherwise, push the resolved path onto the include chain and recursively process the included file starting from step 1.
   g. Replace the include directive with the included file's resolved content, surrounded by blank lines (`\n\n`) to ensure block-level separation.
   h. Pop the resolved path from the include chain.

#### Path Resolution

Include paths MUST be resolved relative to the directory containing the file in which the include directive appears, not relative to the root document.

Given this file structure:

```
project/
  main.md              <!-- include:chapters/intro.md -->
  chapters/
    intro.md           <!-- include:shared/note.md -->
    shared/
      note.md
```

The include in `main.md` resolves to `project/chapters/intro.md`. The include in `intro.md` resolves to `project/chapters/shared/note.md` -- relative to the `chapters/` directory where `intro.md` resides.

#### Block-Level Separation

A processor MUST insert included content with block-level separation. The included content MUST be surrounded by blank lines on both sides when spliced into the parent document. This prevents the included content from merging with adjacent text in the parent.

#### Variable Context Inheritance

Included files MUST inherit the variable map from the parent document. All files in an include tree share the same variable map. Variable substitution occurs after all includes are expanded (see [Phase 1, Step 2](#phase-1-step-2-variable-substitution)).

#### Cycle Detection

A processor MUST track the include chain (the sequence of file paths from the root document to the current file) and MUST detect circular references. When a cycle is detected, the processor MUST skip the circular include, leave the include tag in place as a regular HTML comment, and emit diagnostic **MDPP013**.

**Example -- circular include:**

`parent.md`:
```markdown
# Parent Document

<!-- include:child.md -->
```

`child.md`:
```markdown
## Child Content

<!-- include:parent.md -->
```

When processing `parent.md`, the processor includes `child.md`. When processing `child.md`, the processor detects that `parent.md` is already in the include chain, skips the include with **MDPP013**, and leaves `<!-- include:parent.md -->` in place.

#### Include Depth

Implementations SHOULD impose a maximum include depth to prevent resource exhaustion from deeply nested includes. A maximum depth of **10** is RECOMMENDED. This accommodates practical documentation structures (book > part > chapter > section > shared content) with reasonable headroom.

When the maximum depth is exceeded, the processor MUST skip the include, leave the include tag in place, and emit diagnostic **MDPP011**.

#### Per-File Condition Evaluation

Condition evaluation occurs per-file during include expansion. Each file's condition blocks are evaluated using the project's condition set **before** that file's content is spliced into the parent. This is a critical scoping rule with the following implications:

1. Condition start (`<!-- condition:expr -->`) and end (`<!-- /condition -->`) tags MUST both exist within the same file. A condition block MUST NOT span across an include boundary.
2. If a processor detects an unclosed condition block at the end of a file, it MUST emit diagnostic **MDPP001**. If a processor detects a closing `<!-- /condition -->` tag without a matching opening tag, it MUST emit diagnostic **MDPP001**.
3. If a processor detects a condition block that spans an include boundary (opening in one file, closing in another), it MUST emit diagnostic **MDPP012**.

##### Tri-State Condition Model

Each condition name has one of three states:

- **Visible**: The condition evaluates to true. Content inside the block is **included** in the output.
- **Hidden**: The condition evaluates to false. Content inside the block is **removed** from the output.
- **Unset**: The condition name is not defined in the condition set. The condition block **passes through** without evaluation -- the opening tag, content, and closing tag are preserved as-is in the output.

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

##### Condition Expression Operators

Condition expressions support three operators with the following precedence (highest to lowest):

| Operator | Symbol | Precedence | Behavior |
|----------|--------|:----------:|----------|
| NOT | `!` | 1 (highest) | Inverts the condition state. `!name` is true when `name` is Hidden, false when Visible. If `name` is Unset, the block passes through. |
| AND | ` ` (space) | 2 | All operands must be true. `a b` is true when both `a` and `b` are Visible. If any operand is Unset, the block passes through. |
| OR | `,` | 3 (lowest) | Any operand must be true. `a,b` is true when either `a` or `b` is Visible. If any operand is Unset, the block passes through. |

A processor MUST parse condition expressions according to this precedence. The expression `!a b,c` MUST be parsed as `((!a) AND b) OR c`.

NOT applies to a single condition name. It inverts the evaluation: `!name` is true when the condition is Hidden, and false when the condition is Visible. If the condition is Unset, the block passes through without evaluation.

##### Nesting

Condition blocks MUST NOT be nested or overlap. To express multi-condition logic, use logical expressions with AND (space), OR (comma), and NOT (`!`) operators in condition expressions (see [Condition Expression Operators](#condition-expression-operators) above). For example, `<!--condition:web advanced-->` requires both `web` and `advanced` to be true.

#### Edge Cases

##### 1. Include of File with Conditions

When an included file contains condition blocks, the conditions are evaluated using the project's condition set before the file's content is spliced into the parent.

`parent.md`:
```markdown
# Guide

<!-- include:platform-notes.md -->
```

`platform-notes.md`:
```markdown
<!--condition:windows-->
Install using the MSI installer.
<!--/condition-->

<!--condition:linux-->
Install using apt or yum.
<!--/condition-->
```

If the condition set has `windows` = Visible and `linux` = Hidden, only the Windows content is spliced into `parent.md`.

##### 2. Conditional Include

A condition block in the parent MAY wrap an include directive. The include is only processed if the condition evaluates to true.

```markdown
<!--condition:detailed-->
<!-- include:appendix.md -->
<!--/condition-->
```

If `detailed` is Hidden, the entire block including the include directive is removed. The file `appendix.md` is never read. If `detailed` is Unset, the entire condition block -- including the `<!-- include:appendix.md -->` directive -- passes through as-is. The file `appendix.md` is not read, and the include directive survives as literal text in the output.

##### 3. Nested Includes with Relative Path Resolution

Each nested include resolves paths relative to its own containing file, not the root document.

`docs/main.md`:
```markdown
<!-- include:chapters/overview.md -->
```

`docs/chapters/overview.md`:
```markdown
<!-- include:sections/intro.md -->
```

The second include resolves to `docs/chapters/sections/intro.md`.

##### 4. Condition Across Include Boundary

Opening a condition in one file and closing it in another is a fatal error.

`parent.md`:
```markdown
<!--condition:web-->
<!-- include:content.md -->
<!--/condition-->
```

This is **correct** -- the condition block opens and closes within `parent.md`. The include directive is inside the condition block, and the included file is a complete unit.

`parent.md` (wrong):
```markdown
<!--condition:web-->
<!-- include:content.md -->
```

`content.md` (wrong):
```markdown
Some content.
<!--/condition-->
```

This is a **fatal error**. The condition opens in `parent.md` and closes in `content.md`. The processor MUST emit diagnostic **MDPP012** for the unclosed condition in `parent.md` and **MDPP001** for the unmatched closing tag in `content.md`.

### Phase 1, Step 2: Variable Substitution

After all includes are expanded and per-file conditions are evaluated (with Unset condition blocks passed through as-is), the processor performs variable substitution on the resulting text. This step replaces `$name;` tokens with values from the variable map.

#### Input Model

Variables are resolved from the variable map provided to the processor at build time. The variable map is a flat key-value collection where keys are variable names and values are strings. This specification does not prescribe how the variable map is populated -- environment variables, configuration files, CLI flags, and API parameters are all valid sources.

Variable names MUST match the naming rule `[a-zA-Z_][a-zA-Z0-9_\-]*`. Variable references are case-sensitive: `$Product;` and `$product;` are distinct references that resolve to different entries in the variable map.

#### Processing Order

Variable substitution MUST run after include expansion and condition evaluation are complete. This ordering has four critical implications that processors MUST observe:

1. **Variables inside false condition blocks are never resolved.** When a condition block evaluates to Hidden, the block's content is removed during include expansion (Phase 1, Step 1) before variable substitution runs. Any `$name;` tokens within the removed content are never scanned. However, variables inside Unset (pass-through) condition blocks are resolved, because the block's content is preserved during condition evaluation and is present when variable substitution scans the text.

2. **Variable values cannot contain condition syntax.** Because defined conditions are already evaluated before variable substitution, a variable value containing `<!--condition:name-->` will not be evaluated as a condition directive. It will pass through as literal text into Phase 2.

3. **Variable values can contain Markdown syntax.** Because variable substitution runs before Markdown parsing (Phase 2), a variable value containing `**bold**` or `[link](url)` will be parsed as Markdown in Phase 2 and rendered accordingly.

4. **Variable values cannot contain include syntax.** Because includes are already expanded before variable substitution, a variable value containing `<!-- include:path -->` will not be evaluated as an include directive. It will pass through as literal text into Phase 2.

#### Scanning and Replacement

A processor MUST scan the resolved text for tokens matching the pattern `$name;` (a `$` character, followed by a valid variable name, followed by a `;` character). For each token:

1. Look up the variable name in the variable map.
2. If the name exists, replace the entire token (`$name;`) with the variable's value.
3. If the name does not exist, leave the token as literal text and emit diagnostic **MDPP010**.

#### Escaping

Two mechanisms prevent variable interpretation. Both MUST be supported by conformant processors.

##### Backslash Escaping

A backslash immediately before the `$` character (`\$name;`) prevents the token from being recognized as a variable reference. The processor MUST resolve backslash escapes before scanning for variables. The backslash is consumed: `\$name;` becomes the literal text `$name;` in the output.

**Example:**

```markdown
Use \$Product; to reference the variable.
```

Output after variable substitution:

```markdown
Use $Product; to reference the variable.
```

##### Inline Code Spans

Variable tokens inside inline code spans (`` ` ``) MUST NOT be scanned for variable substitution. Code spans are excluded from variable scanning entirely.

**Example:**

```markdown
The variable syntax is `$name;` where name is the variable identifier.
```

The `$name;` inside the code span is preserved as literal text regardless of whether `name` exists in the variable map.

#### Undefined Variables

When a variable reference (`$name;`) has no corresponding entry in the variable map, the processor MUST leave the token as literal text (`$name;` passes through unchanged) and MUST emit diagnostic **MDPP010** (severity: Warning).

This behavior enables incremental authoring workflows where not all variables are defined at every build stage. Authors can add variable references before the variable map is complete, and a conformant processor will flag them without halting.

### Phase 2: Markdown Parsing with Extension Extraction

Phase 2 receives the text from Phase 1 -- all includes expanded, defined conditions evaluated (Unset condition blocks pass through as-is), variables substituted -- and parses it as Markdown with extension-aware grammars. For the specific behavior of extensions within multiline table cells, see [Extensions in Multiline Table Cells](multiline-cell-extensions.md).

#### Input

The input to Phase 2 is a single string of text. This text contains no include directives outside of Unset condition blocks (all reachable includes expanded), no condition blocks referencing defined condition names (all evaluated -- blocks referencing undefined names pass through as-is), and no unresolved variable tokens (all substituted or left as literal text with warnings). The text MAY contain:

- Standard CommonMark content
- Recognized Markdown++ comment tags (style, alias, marker, multiline, combined commands)
- Regular HTML comments (not matching any Markdown++ pattern)
- Unset condition blocks (condition opening tags, content, condition closing tags, and any include directives within them) that passed through Phase 1 without evaluation

#### Parsing

A conformant processor MUST parse the input as [CommonMark 0.30](https://spec.commonmark.org/0.30/) with GFM table support. During parsing, the processor extracts Markdown++ extensions from recognized HTML comments.

#### Comment Disambiguation

Before processing a comment tag, the processor MUST determine whether it is a recognized Markdown++ directive or a regular HTML comment. A comment is recognized as a Markdown++ directive only if its content matches at least one known command pattern: `style:`, `#alias`, `marker:`, `markers:`, `multiline`, or a combined command using `;` separators.

Regular HTML comments (such as `<!-- TODO: fix this -->` or `<!-- Author's note -->`) MUST be ignored by the processor. They are not directives, are not subject to the attachment rule, and produce no diagnostics.

See the [Comment Disambiguation](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md#comment-disambiguation) section of the syntax reference for the complete recognition rules.

#### Extension Extraction

For each recognized Markdown++ comment tag, the processor extracts one or more commands. The processor MUST resolve attachment for block-level tags using the rules defined in the [Attachment Rule](attachment-rule.md) specification:

1. **Block-level tags** MUST appear on the line directly above the target element with no intervening blank line.
2. **Inline tags** MUST appear immediately before the styled element on the same line, with no space between the closing `-->` and the element.
3. A tag that fails attachment (blank line below, end of file, another tag on the next line) is **orphaned**. Orphaned tags produce diagnostic **MDPP009** (severity: Warning) and have no effect on the output tree.

#### Combined Command Evaluation Order

When a single comment contains multiple commands separated by semicolons (`;`), the processor SHOULD evaluate them in the following order for readability and consistency, regardless of the order in which they appear in the comment. Processors MAY evaluate segments in any order.

| Order | Command | Effect |
|:-----:|---------|--------|
| 1 | `style:Name` | Associates a custom style with the target element |
| 2 | `multiline` | Marks the target table for multiline cell processing |
| 3 | `marker:Key="value"` | Attaches one or more metadata key-value pairs |
| 4 | `#alias` | Assigns a navigational alias anchor to the target element |

**Example:**

```markdown
<!-- #comparison ; style:DataTable ; marker:Keywords="specs" ; multiline -->
| Feature | Basic | Advanced |
|---------|-------|----------|
```

Following the recommended order, the processor evaluates: style `DataTable` first, then `multiline`, then marker `Keywords="specs"`, then alias `comparison`. All four directives attach to the table.

#### Orphaned Tag Handling

A recognized Markdown++ tag that fails attachment is an **orphaned tag**. Orphaned tags:

- MUST produce diagnostic **MDPP009** (severity: Warning)
- MUST NOT affect the output tree -- an orphaned style does not apply to any element
- MUST NOT cause processing to halt -- orphaned tags are recoverable warnings

Common causes of orphaned tags include blank lines between the tag and its target, tags at the end of a file, and stacked tags where only the bottom tag attaches. See the [Attachment Rule](attachment-rule.md) edge cases for detailed examples.

## Output Model

The output of the processing pipeline is a **CommonMark document tree annotated with Markdown++ metadata**. This specification defines the abstract output model in implementation-agnostic terms. A conformant processor MAY render the output tree as HTML, PDF, XML, or any other format.

### Document Tree

The output tree MUST be a valid CommonMark document tree as defined by [CommonMark 0.30](https://spec.commonmark.org/0.30/). All standard CommonMark elements (paragraphs, headings, lists, code blocks, blockquotes, etc.) are represented in their standard tree structure.

### Metadata Annotations

In addition to the standard tree structure, the output tree carries Markdown++ metadata annotations. These annotations do not alter the tree structure -- they attach additional information to existing nodes:

| Annotation Type | Source Command | Attached To | Content |
|----------------|----------------|-------------|---------|
| Style | `style:Name` | Any block or inline element | Style name (string) |
| Alias | `#name` | Any block element | Alias identifier (string) |
| Marker | `marker:Key="value"` | Any block element | Key-value pair(s) |
| Multiline | `multiline` | Table element | Multiline processing flag |

A single element MAY carry multiple annotations (e.g., a heading with both a style and an alias).

### Determinism Guarantee

Given the same input document, variable map, and condition set, a conformant processor MUST produce the same output tree. The processing pipeline is deterministic -- there is no implementation-defined ordering or randomness in extension evaluation.

This guarantee enables:
- Reproducible builds across different processor implementations
- Meaningful comparison of output between processors for conformance testing
- Caching and incremental build strategies that depend on input stability

## Error Handling

Processors encounter errors at various points in the pipeline. This section classifies errors by severity and defines the expected behavior for each class.

### Fatal Errors vs. Recoverable Warnings

A **fatal error** prevents the processor from producing a meaningful output tree for the affected portion of the document. A **recoverable warning** indicates a problem that the processor can work around, producing output with degraded fidelity.

| Classification | Behavior | Examples |
|---------------|----------|----------|
| **Fatal error** | Processor MUST report the error. The affected construct's content MUST NOT be used for further pipeline processing, but the processor SHOULD continue processing the remainder of the document. A processor MAY implement an implementation-defined recovery strategy (e.g., encoding fallback for MDPP017), but MUST still emit the diagnostic regardless. | Invalid UTF-8 encoding (MDPP017), cross-file condition span (MDPP012), include cycle (MDPP013), max include depth exceeded (MDPP011) |
| **Recoverable warning** | Processor MUST report the warning. Processing continues with a documented fallback behavior. | Missing include file (MDPP006), undefined variable (MDPP010), orphaned tag (MDPP009) |

### Diagnostic Collection

A conformant processor SHOULD collect all diagnostics encountered during processing rather than halting on the first error. This enables batch authoring workflows where authors can see all problems at once, rather than fixing one error and discovering the next on each build cycle.

### Diagnostic Format

Each diagnostic MUST include:

1. **MDPP code** -- The diagnostic code from the registry below.
2. **Severity** -- Either `Error` (fatal) or `Warning` (recoverable).
3. **File path** -- The path to the file where the diagnostic originated.
4. **Line number** -- The line number within the originating file (before include expansion).
5. **Message** -- A human-readable description of the problem.

### MDPP Diagnostic Code Registry

The following table defines all diagnostic codes for Markdown++ processing. Codes MDPP000 through MDPP009 are defined for static validation (see the [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md)). Codes MDPP010 and above are defined for processing-phase diagnostics.

#### Static Validation Codes

| Code | Description | Severity | Phase |
|------|-------------|----------|-------|
| **MDPP000** | File not found or cannot be read | Error | Pre-processing |
| **MDPP001** | Unclosed or unmatched condition block | Error | Pre-processing |
| **MDPP002** | Invalid name (variable, style, alias, or marker key) | Error | Any |
| **MDPP003** | Malformed marker JSON | Error | Phase 2 |
| **MDPP004** | Invalid style placement | Warning | Phase 2 |
| **MDPP005** | Circular include detected (static analysis) | Error | Pre-processing |
| **MDPP006** | Missing include file | Warning | Phase 1, Step 1 |
| **MDPP007** | Invalid condition syntax | Error | Phase 1, Step 1 |
| **MDPP008** | Duplicate alias within file | Error | Phase 2 |
| **MDPP009** | Orphaned comment tag (not attached to element) | Warning | Phase 2 |

#### Processing-Phase Codes

| Code | Description | Severity | Phase | Triggering Condition |
|------|-------------|----------|-------|---------------------|
| **MDPP010** | Undefined variable reference | Warning | Phase 1, Step 2 | A `$name;` token references a name not present in the variable map |
| **MDPP011** | Maximum include depth exceeded | Error | Phase 1, Step 1 | Include nesting exceeds the processor's configured maximum depth |
| **MDPP012** | Cross-file condition span | Error | Phase 1, Step 1 | A condition block opens in one file and closes in another |
| **MDPP013** | Include cycle detected during processing | Error | Phase 1, Step 1 | A file appears in its own include chain during recursive expansion |
| **MDPP014** | Duplicate link reference slug across files | Warning | Phase 2 | Two or more link reference definitions with the same slug originate from different source files in the assembled document. See [Cross-File Link Reference Resolution](cross-file-link-resolution.md). |
| **MDPP015** | Document targets newer minor version than processor supports | Warning | Preamble | The `mdpp-version` minor version exceeds the processor's supported minor version within the same major series. See [Format Versioning](versioning.md). |
| **MDPP016** | Document targets different major version than processor supports | Warning | Preamble | The `mdpp-version` major version differs from the processor's supported major version. See [Format Versioning](versioning.md). |
| **MDPP017** | Invalid UTF-8 encoding | Error | Phase 1, Step 1 | The root document or an included file contains an invalid UTF-8 byte sequence when read during processing. See [Encoding Errors](#encoding-errors). |

Implementations MAY define additional diagnostic codes beyond this registry for implementation-specific checks. Custom codes SHOULD use numbers MDPP100 and above to avoid conflicts with future specification-defined codes.

## Conformance

This section defines what constitutes a conformant Markdown++ processor.

### Required Features

A conformant Markdown++ processor MUST implement all of the following:

1. **Include expansion** -- Recursive depth-first expansion with cycle detection and per-file condition evaluation, as specified in [Phase 1, Step 1](#phase-1-step-1-include-expansion).
2. **Condition evaluation** -- Tri-state condition model with NOT, AND, and OR operators at the specified precedence, as specified in [Per-File Condition Evaluation](#per-file-condition-evaluation).
3. **Variable substitution** -- Token replacement from a variable map with both escaping mechanisms, as specified in [Phase 1, Step 2](#phase-1-step-2-variable-substitution).
4. **Style extraction** -- Extraction and attachment of `style:Name` commands to target elements.
5. **Alias extraction** -- Extraction and attachment of `#name` commands to target elements.
6. **Marker extraction** -- Extraction and attachment of `marker:Key="value"` and `markers:{json}` commands to target elements.
7. **Multiline table processing** -- Recognition and processing of `multiline` commands on table elements. A conformant processor MUST implement all of the following:
   a. **Row separator recognition** -- A table row where every cell contains only whitespace (matching the pattern `^ {0,3}\|(?:[ ]*\|)+[ ]*$`) MUST be recognized as a row separator that delimits logical rows.
   b. **Continuation row merging** -- A table row whose first cell is empty MUST be merged into the preceding logical row. The multiline algorithm applies to both header rows (above the delimiter) and body rows (below it).
   c. **Blank-line termination** -- A completely blank line (no pipe characters) MUST end the table. A blank line does not separate rows.
   d. **Cell content dedent** -- The processor MUST strip the minimum common leading whitespace from all lines of each cell's merged content. If all lines share N leading spaces, all N spaces are removed.
8. **Attachment rule enforcement** -- Block-level and inline attachment as specified in the [Attachment Rule](attachment-rule.md).
9. **Comment disambiguation** -- Correct identification of recognized vs. unrecognized HTML comments.
10. **Diagnostic reporting** -- Emission of MDPP diagnostic codes at their specified severity levels for all required features. Diagnostic codes associated with optional features (e.g., MDPP015, MDPP016) are required only when the processor implements those features.
11. **Encoding validation** -- UTF-8 encoding validation with BOM handling and MDPP017 emission, as specified in [Character Encoding](#character-encoding)
12. **Combined commands** -- Semicolon-separated commands in a single comment tag. The evaluation order listed in [Combined Command Evaluation Order](#combined-command-evaluation-order) is RECOMMENDED for readability but not required; processors MAY evaluate segments in any order.

### Optional Features

The following features are OPTIONAL. A conformant processor MAY implement them but is not required to:

1. **Maximum include depth enforcement** -- A processor MAY impose a maximum include depth. If it does, it SHOULD use a default of 10 and MUST emit **MDPP011** when the limit is exceeded.
2. **Version checking** -- A processor MAY implement the version check preamble described in [Format Versioning](versioning.md). If it does, it MUST emit **MDPP015** and **MDPP016** at their specified severities and follow the compatibility rules defined in that specification.

### Conformance Statement

A processor that implements all required features, handles MDPP diagnostic codes at their specified severities for all features it implements, and produces deterministic output (same input yields same output tree) is a **conformant Markdown++ processor**.

A processor that implements all required features plus one or more optional features is a **conformant Markdown++ processor with extensions** and SHOULD document which optional features are supported.

### Test Suite

Conformance verification SHOULD be performed against a test suite of Markdown++ documents with expected output trees and expected diagnostics. The format and content of the test suite are defined in a separate document. See [issue #8](https://github.com/quadralay/markdown-plus-plus/issues/8) for the tracking discussion.

