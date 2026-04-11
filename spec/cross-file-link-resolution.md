---
date: 2026-04-08
status: active
---

# Cross-File Link Reference Resolution

## Introduction

This document specifies how link reference definitions resolve across files in a multi-file Markdown++ document assembly. It defines the resolution scope, conflict rules, and diagnostic behavior that all conformant processors MUST follow when processing link references in assembled documents.

The [Processing Model](processing-model.md) defines the two-phase pipeline that governs all Markdown++ processing. Phase 1, Step 1 assembles all included files into a single text via depth-first recursive include expansion. Phase 2 parses that assembled text as [CommonMark 0.30](https://spec.commonmark.org/0.30/). Link reference definitions are a CommonMark construct resolved during Phase 2. Cross-file link reference resolution is a direct consequence of this architecture -- it requires no additional processing phase.

The [syntax reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) defines Markdown++ extensions including custom aliases. Link reference definitions are a standard [CommonMark 0.30](https://spec.commonmark.org/0.30/#link-reference-definitions) construct. This document defines how link reference definitions behave when multiple files contribute definitions to the same assembled document.

## Definitions

**Link reference definition** -- A CommonMark construct that defines a link target associated with a slug. Syntax: `[slug]: url "optional title"`. See [CommonMark 0.30 section 4.7](https://spec.commonmark.org/0.30/#link-reference-definitions).

**Slug** -- The bracketed label in a link reference definition (e.g., `getting-started` in `[getting-started]: #200002`). Slug matching is case-insensitive per CommonMark 0.30.

**Link reference** -- A reference to a link reference definition, using the slug as a key. CommonMark defines three forms: full (`[text][slug]`), collapsed (`[slug][]`), and shortcut (`[slug]`).

**Assembled document** -- The single text produced by Phase 1 of the processing pipeline after all includes are expanded, conditions are evaluated, and variables are substituted. This is the input to Phase 2.

**Source file** -- The original file in which a link reference definition was authored, before include expansion assembled it into the parent document.

**Conformance keywords** -- The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt). All conformance statements apply to processors, not to document authors.

## Resolution Scope

Link reference definitions are resolved at **document-global scope** after assembly. A conformant processor MUST resolve link references against the complete set of link reference definitions present in the assembled document, regardless of which source file contributed each definition.

This behavior is a direct consequence of the two-phase processing model:

1. **Phase 1, Step 1** assembles all included files into a single text via depth-first recursive include expansion.
2. **Phase 2** parses that single text as CommonMark 0.30.
3. CommonMark 0.30 collects all link reference definitions from the entire document and resolves references against them.

There is no per-file link reference scope. By the time Phase 2 begins, the assembled document is a single text with no file boundaries.

### Scope Visibility

Link reference definitions from **any** file in the include tree are visible to **all** other content in the assembled document. Specifically:

1. A link reference definition in an included file is visible to the parent document.
2. A link reference definition in an included file is visible to sibling includes.
3. A link reference definition in a parent document is visible to included files.
4. A link reference definition in a deeply nested include is visible to the root document and all other includes.

A link reference in any file MAY resolve to a link reference definition in any other file, provided both are present in the assembled document after Phase 1 completes.

## Conflict Resolution

When two or more link reference definitions in the assembled document use the same slug, the **first definition wins**. This follows [CommonMark 0.30 section 4.7](https://spec.commonmark.org/0.30/#link-reference-definitions), which specifies that if there are multiple definitions with the same slug, the first one takes precedence.

### Definition Order in Assembled Documents

The order of link reference definitions in the assembled document is determined by the depth-first recursive include expansion algorithm defined in the [Processing Model](processing-model.md), Phase 1, Step 1. Concretely:

1. Content from the root document appears first (up to the first include directive).
2. Each include directive is replaced by the included file's content, recursively.
3. Content from the root document after an include directive follows the included content.

Given this root document:

```markdown
# Root content

[slug]: #root-target

<!-- include:chapter-a.md -->
<!-- include:chapter-b.md -->
```

And `chapter-a.md`:

```markdown
[slug]: #chapter-a-target
```

And `chapter-b.md`:

```markdown
[slug]: #chapter-b-target
```

The assembled document order is: root content, then chapter-a content, then chapter-b content. The root document's definition of `[slug]` appears first and wins.

### Include Order Determines Priority

Because first-definition-wins applies to the assembled document, the **order of include directives** in the parent document affects which definition takes precedence when siblings define the same slug. Reordering includes can change which definition wins.

A processor MUST NOT reorder include content during assembly. The assembled document order MUST match the depth-first traversal order of the include tree.

## Diagnostic Reporting

### MDPP014: Duplicate Link Reference Slug Across Files

When two or more link reference definitions with the same slug originate from **different source files** in the assembled document, a conformant processor MUST emit diagnostic **MDPP014**.

| Property | Value |
|----------|-------|
| **Code** | MDPP014 |
| **Description** | Duplicate link reference slug across files |
| **Severity** | Warning |
| **Phase** | Phase 2 |
| **Triggering condition** | Two or more link reference definitions with the same slug originate from different source files in the assembled document |

MDPP014 is a **warning**, not a fatal error. The first-definition-wins rule ensures deterministic output even when duplicates exist. The diagnostic alerts authors that a slug conflict exists, which is likely unintentional.

MDPP014 applies only to cross-file duplicates. Duplicate slugs within a single file are standard CommonMark behavior (first-definition-wins with no diagnostic) and are not flagged by this code.

**Note:** To emit MDPP014, a processor MUST track which source file contributed each link reference definition during Phase 1 include expansion. This provenance information is used in Phase 2 when duplicate slugs are detected.

## Interaction with Other Processing Features

### Conditions and Link Reference Definitions

Condition evaluation occurs during Phase 1, Step 1, before link reference definitions are collected in Phase 2. A link reference definition inside a condition block that evaluates to Hidden is removed from the assembled text and is **not** part of the definition set.

This means conditions can control which link reference definitions are active in the assembled document. Authors can use conditions to provide platform-specific or audience-specific link targets:

```markdown
<!--condition:web-->
[download-link]: https://example.com/download "Download"
<!--/condition-->

<!--condition:pdf-->
[download-link]: #appendix-downloads "Download"
<!--/condition-->
```

When `web` is Visible and `pdf` is Hidden, only the web definition is present in the assembled document. The first-definition-wins rule does not apply because only one definition survives condition evaluation.

### Variables in Link Reference Definitions

Variable substitution occurs in Phase 1, Step 2, after include expansion but before Phase 2 parsing. Variable tokens in link reference definitions are substituted before the definitions are collected:

```markdown
[api-docs]: $docs_base_url;/api/v2 "API Documentation"
```

If the variable map contains `docs_base_url` = `https://docs.example.com`, the assembled text seen by Phase 2 is:

```markdown
[api-docs]: https://docs.example.com/api/v2 "API Documentation"
```

### Link Reference Definitions in Variable Values

Because variable substitution (Phase 1, Step 2) runs before CommonMark parsing (Phase 2), a variable value that contains a complete link reference definition **is** recognized by the Phase 2 parser. However, this pattern is NOT RECOMMENDED because it obscures the definition from authors and tools that inspect the source files.

### Alias IDs in Link Reference Definitions

The semantic cross-reference pattern in Markdown++ uses link reference definitions to bridge human-readable slugs to numeric alias IDs:

```markdown
<!-- style:Heading2; #200010 -->
## Getting Started

[getting-started]: #200010 "Getting Started"
```

In a multi-file assembly, this pattern works across files because:

1. The alias command (`#200010`) attaches to the heading in Phase 2.
2. The link reference definition (`[getting-started]: #200010`) is collected at document-global scope in Phase 2.
3. A reference (`[Getting Started][getting-started]`) in any file in the assembly resolves to `#200010`.

This is the primary use case for cross-file link reference resolution.

## Worked Examples

### Example A: Sibling Visibility

This example demonstrates that a link reference defined in one included file resolves when referenced from a sibling include.

**Root file (`user-guide.md`):**

```markdown
# User Guide

<!-- include:chapters/overview.md -->
<!-- include:chapters/installation.md -->
<!-- include:chapters/configuration.md -->
```

**`chapters/overview.md`:**

```markdown
<!-- style:Heading2; #200010 -->
## Overview

[overview]: #200010 "Overview"

Welcome to the product. See [Installation][installation] for setup
instructions, or skip ahead to [Configuration][configuration].
```

**`chapters/installation.md`:**

```markdown
<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"

Follow these steps to install the product.
For background, see [Overview][overview].
```

**`chapters/configuration.md`:**

```markdown
<!-- style:Heading2; #200030 -->
## Configuration

[configuration]: #200030 "Configuration"

Configure the product after installation.
See [Installation][installation] if you haven't installed yet.
```

**Assembled document after Phase 1:**

```markdown
# User Guide

<!-- style:Heading2; #200010 -->
## Overview

[overview]: #200010 "Overview"

Welcome to the product. See [Installation][installation] for setup
instructions, or skip ahead to [Configuration][configuration].

<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"

Follow these steps to install the product.
For background, see [Overview][overview].

<!-- style:Heading2; #200030 -->
## Configuration

[configuration]: #200030 "Configuration"

Configure the product after installation.
See [Installation][installation] if you haven't installed yet.
```

**Resolution in Phase 2:**

All three link reference definitions (`overview`, `installation`, `configuration`) are collected at document-global scope. Every `[slug]` reference in the assembled document resolves, regardless of which source file defined the slug or which source file contains the reference:

- `[Installation][installation]` in `overview.md` resolves to `#200020` (defined in `installation.md`)
- `[Configuration][configuration]` in `overview.md` resolves to `#200030` (defined in `configuration.md`)
- `[Overview][overview]` in `installation.md` resolves to `#200010` (defined in `overview.md`)
- `[Installation][installation]` in `configuration.md` resolves to `#200020` (defined in `installation.md`)

No diagnostics are emitted. Each slug has exactly one definition.

### Example B: Conflict Resolution with MDPP014

This example demonstrates what happens when two included files define the same slug with different targets.

**Root file (`guide.md`):**

```markdown
# Guide

<!-- include:team-a/setup.md -->
<!-- include:team-b/setup.md -->
```

**`team-a/setup.md`:**

```markdown
<!-- style:Heading2; #300010 -->
## Setup (Team A)

[setup]: #300010 "Setup"

Team A's setup instructions.
```

**`team-b/setup.md`:**

```markdown
<!-- style:Heading2; #300020 -->
## Setup (Team B)

[setup]: #300020 "Setup"

Team B's setup instructions.
See [Setup][setup] for the canonical setup guide.
```

**Assembled document after Phase 1:**

```markdown
# Guide

<!-- style:Heading2; #300010 -->
## Setup (Team A)

[setup]: #300010 "Setup"

Team A's setup instructions.

<!-- style:Heading2; #300020 -->
## Setup (Team B)

[setup]: #300020 "Setup"

Team B's setup instructions.
See [Setup][setup] for the canonical setup guide.
```

**Resolution in Phase 2:**

Two definitions for `[setup]` exist in the assembled document. The first-definition-wins rule applies:

- `[setup]: #300010` from `team-a/setup.md` appears first in the assembled document (because `team-a/setup.md` is included before `team-b/setup.md`)
- `[setup]: #300020` from `team-b/setup.md` appears second and is **ignored**
- All references to `[setup]` resolve to `#300010`

The processor emits **MDPP014** because the duplicate definitions originate from different source files:

```
MDPP014 Warning: Duplicate link reference slug across files
  Slug: "setup"
  First definition: team-a/setup.md (target: #300010)
  Duplicate: team-b/setup.md (target: #300020)
```

**Corrective action:** The author should rename one of the slugs to be unique (e.g., `[team-a-setup]` and `[team-b-setup]`), or consolidate the definitions into a shared file.

## Edge Cases

### 1. Definition in Conditionally-Excluded Content

A link reference definition inside a condition block that evaluates to Hidden is removed during Phase 1 and does not participate in Phase 2 resolution.

```markdown
<!--condition:v2-->
[api-ref]: https://docs.example.com/v2/api "API Reference"
<!--/condition-->

<!--condition:v1-->
[api-ref]: https://docs.example.com/v1/api "API Reference"
<!--/condition-->
```

If `v2` is Visible and `v1` is Hidden, only the v2 definition survives into the assembled document. No conflict exists, and MDPP014 is not emitted.

If both `v2` and `v1` are Visible, both definitions are present. The v2 definition appears first and wins. If they originate from different source files, MDPP014 is emitted.

### 2. Definition in a Deeply Nested Include

A link reference definition in a file included three levels deep is visible to the root document and all other files in the assembly. Include depth does not affect visibility.

```
root.md
  └── include:part-1.md
        └── include:chapter-1.md
              └── include:shared/refs.md    ← defines [glossary]: #glossary
```

A reference to `[glossary]` anywhere in the assembled document -- including `root.md` -- resolves to the definition in `shared/refs.md`.

### 3. Slug Matching Is Case-Insensitive

Per CommonMark 0.30, slug matching is case-insensitive. The definitions `[API-Docs]: url` and `[api-docs]: url` are considered duplicates. If they originate from different source files, MDPP014 is emitted.

### 4. Link Reference Definition After All References

CommonMark does not require link reference definitions to appear before references to them. A definition at the end of the assembled document resolves references earlier in the document. This means a shared definitions file included last still provides definitions for all preceding content:

```markdown
<!-- include:chapters/intro.md -->
<!-- include:chapters/guide.md -->
<!-- include:shared/link-defs.md -->
```

References in `intro.md` and `guide.md` resolve to definitions in `link-defs.md`.

## Conformance

### Processor Requirements

A conformant processor that implements include expansion (as defined in the [Processing Model](processing-model.md), Phase 1, Step 1) MUST:

1. Resolve link references at document-global scope on the assembled document.
2. Apply the first-definition-wins rule from CommonMark 0.30 section 4.7.
3. Not reorder include content during assembly.
4. Track link reference definition provenance (source file) during include expansion.
5. Emit **MDPP014** when duplicate slugs originate from different source files.

Requirements 1-3 are satisfied by any correct implementation of the two-phase processing model. Requirements 4-5 are specific to cross-file duplicate detection.

### Relationship to the Processing Model

This specification does not introduce a new processing phase. Cross-file link reference resolution is a consequence of the existing two-phase pipeline:

- Phase 1 produces a single assembled text.
- Phase 2 parses that text as CommonMark 0.30, which includes link reference resolution at document scope.

The only new processor responsibility is tracking definition provenance for MDPP014 diagnostic reporting.
