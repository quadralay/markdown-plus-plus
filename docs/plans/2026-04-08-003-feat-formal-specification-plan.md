---
title: "feat: Create unified Markdown++ 1.0 specification"
type: feat
status: active
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-formal-specification-requirements.md
deepened: 2026-04-08
---

# feat: Create unified Markdown++ 1.0 specification

## Overview

Create `spec/specification.md` — the unified Markdown++ 1.0 specification that ties together four existing sub-specifications (formal grammar, processing model, attachment rule, cross-file link resolution) with new per-extension normative definitions, conformance levels, terminology, and a consolidated diagnostic registry. The specification normatively references the sub-specs rather than inlining them, keeping each document independently maintainable.

## Problem Frame

Tool authors who want to implement Markdown++ support must currently reverse-engineer the format from a whitepaper (written for decision-makers), a plugin skill reference (written for an AI agent), and scattered example files. Four sub-specifications now exist — formal grammar (#11), processing model (#8), attachment rule (#10), and cross-file link resolution (#22) — but no unified document ties them together. There is no introduction, no terminology section, no conformance levels, and no per-extension normative definitions. A tool author cannot build a conformant implementation without assembling knowledge from five separate documents.

(see origin: [docs/brainstorms/2026-04-08-formal-specification-requirements.md](../brainstorms/2026-04-08-formal-specification-requirements.md))

## Requirements Trace

- R1. A single `spec/specification.md` serves as the formal Markdown++ 1.0 specification
- R2. RFC 2119 language (MUST/SHOULD/MAY) for all normative requirements
- R3. Two conformance levels: Pass-through and Full
- R4. Terminology section defining key terms used normatively
- R5. CommonMark 0.30 stated as base specification, with GFM table support
- R6. Complete definition section for each of 8 extensions
- R7. Each extension section includes: purpose, syntax, semantics, interactions, attachment requirements, diagnostics
- R8. Formal grammar incorporated by normative reference with overview in main document
- R9. Processing model incorporated by normative reference with pipeline summary in main document
- R10. Attachment rule incorporated by normative reference with core rule stated in main document
- R11. Cross-file link resolution incorporated by normative reference
- R12. Consolidated diagnostic registry (MDPP001–MDPP014) in a single table
- R13. Sections on inline styling, book assembly, and link reference definitions
- R14. Versioned as Markdown++ 1.0

## Scope Boundaries

- **In scope**: The unified specification document and its normative references to existing sub-specs
- **Out of scope**: Changes to the ePublisher parser implementation
- **Out of scope**: Tooling or editor support documentation
- **Out of scope**: Marketing, migration guidance, or competitive comparison (whitepaper's role)
- **Out of scope**: A conformance test suite (separate deliverable)
- **Out of scope**: Rewriting the existing sub-specs — they are referenced as-is
- **Out of scope**: Cross-document numbering or pagination (processor-specific output concern)

## Context & Research

### Relevant Code and Patterns

- `spec/formal-grammar.md` (537 lines) — W3C EBNF grammar for all extensions. Covers lexical terminals, identifiers, variable tokens, comment directives, combined commands. Uses RFC 2119 language, cross-references other specs.
- `spec/processing-model.md` (516 lines) — Two-phase pipeline (pre-processing → parsing), evaluation order, scoping, error behavior. Defines MDPP010-MDPP013 diagnostic codes. Uses RFC 2119 language throughout.
- `spec/attachment-rule.md` (200 lines) — Formal definition of tag-to-element binding. Edge cases for stacked tags, combined commands, nested lists. Cross-references syntax-reference.md.
- `spec/cross-file-link-resolution.md` (412 lines) — Document-global resolution scope, first-definition-wins conflicts, MDPP014 diagnostic. Built on the processing model's Phase 1 include expansion.
- `plugins/.../references/syntax-reference.md` (930 lines) — Primary source for per-extension content. Covers all 8 extensions with syntax, rules, examples, validation codes MDPP001-MDPP009.
- `spec/whitepaper.md` (459 lines) — Motivation and benefits document. Not normative, but useful for understanding the design intent behind book assembly and migration patterns.
- `examples/semantic-cross-references.md` — Demonstrates three-part cross-reference pattern with alias IDs.
- `examples/includes-and-conditions.md` — Shows file assembly with includes and cross-references.

### Institutional Learnings

- **Spec-first pattern**: Every sub-spec followed the workflow: requirements → plan → spec → syntax reference updates. The unified spec follows this same pattern.
- **Normative reference approach**: The processing model already references the attachment rule and syntax reference normatively. This establishes the cross-referencing convention.
- **Diagnostic code organization**: Static codes (MDPP001-009) live in syntax-reference.md, processing codes (MDPP010-014) in processing-model.md and cross-file-link-resolution.md. The unified spec consolidates these into one registry.
- **Content Islands are thin**: Only ~13 lines in syntax-reference.md. Content Islands are styled blockquotes — standard CommonMark with a style convention. The spec section should be proportionally brief.
- **Use relative markdown links to sub-specs, not repo-root paths**: The cross-file link resolution review caught and corrected inline code paths to relative links. Apply this consistently in the unified spec.
- **SHOULD/MUST consistency audit**: The cross-file link resolution spec had a SHOULD/MUST contradiction for MDPP014 emission that was caught in review. The unified spec must audit all RFC 2119 keywords for consistency between the main document's summaries and the sub-specs' definitions.
- **Present derived behaviors as consequences**: Cross-file link resolution is a consequence of Phase 1 assembly, not an independent feature. The unified spec should frame it this way to help implementors understand the dependency chain.
- **MDPP002 expanded scope**: Originally "Invalid variable name," now covers all named entities. The unified naming rules established `identifier` and `alias_name` as the two patterns — aliases permit digit-first names.

## Key Technical Decisions

- **Unified spec with normative references (not monolithic)**: The main specification normatively references the four existing sub-specs rather than inlining their 1,665+ lines of content. Each section that references a sub-spec includes a 1-2 paragraph summary of the key rules, then a normative reference for the complete definition. This follows the pattern used by HTML (which references CSS, DOM, etc.) and keeps sub-specs independently maintainable. (see origin: requirements doc key decisions)

- **Two conformance levels for 1.0**: "Pass-through" (renderer that preserves extensions as HTML comments/literal text) and "Full" (processor that evaluates all extensions). A "Partial" level is deferred — it adds complexity without clear demand and can be added in a future version without breaking existing conformance claims. **Diagnostic applicability**: Pass-through renderers do not parse Markdown++ extensions, so MDPP diagnostic codes are not applicable to them — the pass-through conformance requirement is solely about not altering or stripping extension syntax. Full processors MUST implement all diagnostics at their specified severity levels, consistent with the processing model's conformance section (`spec/processing-model.md` lines 481-511) which already defines required features and diagnostic reporting for conformant processors. The unified spec's conformance section should align with and reference the processing model's conformance requirements rather than redefining them.

- **Extension definitions are the primary new content**: The eight per-extension sections (R6, R7) are where most new writing happens. These draw from syntax-reference.md but elevate to specification-grade with RFC 2119 language, interaction tables, and formal examples. Each extension follows a consistent template.

- **Diagnostic registry consolidates all codes into one table**: MDPP001-MDPP009 (static) and MDPP010-MDPP014 (processing) unified into a single registry with columns: code, severity, phase, description, triggering condition, required conformance level. Recovery behavior is referenced via the processing model, not re-specified.

- **Book assembly is a pattern, not a separate mechanism**: Book assembly uses `<!-- include: -->` at the top level. The processing model already specifies include expansion. The spec section describes the assembly pattern and references the processing model for mechanics. Cross-document numbering and pagination are out of scope (processor-specific output concerns).

## Open Questions

### Resolved During Planning

- **Partial conformance level**: Two levels (Pass-through and Full) are sufficient for 1.0. A "Partial" level would require defining which subsets of extensions are valid, creating a combinatorial matrix. Defer to a future version if demand emerges.

- **Content Islands documentation sufficiency**: The syntax-reference.md has ~13 lines. This is thin but adequate — Content Islands are styled blockquotes (standard CommonMark). The spec section formalizes the styling convention, supported nested content, and attachment rule interaction. No undocumented edge cases discovered.

- **Diagnostic registry error recovery**: The processing model already defines recovery behavior for each diagnostic code. The consolidated registry references recovery behavior via the processing model rather than re-specifying it, avoiding normative duplication.

- **Book assembly detail level**: Book assembly is the `<!-- include: -->` pattern applied at the top level. The processing model specifies include expansion mechanics. The spec section describes the assembly pattern (root file including chapters) and cross-document concerns covered by cross-file link resolution. Cross-document numbering is out of scope for 1.0.

### Deferred to Implementation

- Exact wording of RFC 2119 conformance statements — will be refined during writing based on how each extension's behavior maps to normative requirements
- Whether to include a "Document Conventions" subsection within the introduction or keep it as a separate top-level section — depends on document flow during writing
- Precise table formatting for the diagnostic registry — may need iteration to fit all columns readably

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

### Document Structure

The specification follows a layered architecture:

```
┌─────────────────────────────────────────────────┐
│  spec/specification.md (this document)          │
│                                                 │
│  1. Introduction & Scope                        │
│  2. Conformance                                 │
│  3. Terminology                                 │
│  4. Notation & Conventions                      │
│  5. Extension Comment Syntax (→ formal-grammar) │
│  6. Attachment Rule (→ attachment-rule)          │
│  7. Processing Model (→ processing-model)       │
│  8–15. Extension Definitions (NEW content)      │
│  16. Combined Commands                          │
│  17. Advanced Topics                            │
│  18. Diagnostic Registry (consolidated)         │
│  19. References                                 │
└───────┬─────────┬──────────┬──────────┬─────────┘
        │         │          │          │
        ▼         ▼          ▼          ▼
  formal-    processing-  attachment-  cross-file-
  grammar.md  model.md    rule.md      link-resolution.md
```

### Per-Extension Section Template

Each of the 8 extension definition sections follows this consistent structure:

```
## N. Extension Name
### N.1 Purpose
### N.2 Syntax
### N.3 Semantics
### N.4 Interaction with Other Extensions
### N.5 Attachment Requirements
### N.6 Diagnostics
### N.7 Examples
```

### Normative Reference Pattern

Each section that references a sub-spec includes:
1. A 1-2 paragraph summary of the key rules (enough to read the spec end-to-end coherently)
2. A normative reference statement: "The complete definition is in [Sub-spec Name]. Conformant processors MUST implement the rules defined therein."

## Extension Ordering and Interaction Guidance

> *Directional guidance for implementation units 3-5. The implementing agent should use this as a reference, not as text to copy verbatim into the spec.*

### Extension Order in Specification

The 8 extensions are ordered by dependency (simple/fundamental first, complex/dependent later):

1. **Variables** — Fundamental inline token; used in examples for all other extensions. No dependency on other extensions.
2. **Custom Styles** — Referenced by multiline tables, content islands, and inline styling sections. No dependency on other extensions beyond the attachment rule.
3. **Custom Aliases** — References styles (via combined commands) and is referenced by link reference definitions. Block-level only.
4. **Conditions** — Wraps all other content types; interacts with includes (per-file evaluation, MDPP012). References variables (processing order).
5. **File Includes** — References conditions (conditional includes), variables (inherited map). Foundation for book assembly and cross-file resolution.
6. **Markers/Metadata** — Independent but references combined commands. Passthrough marker is a unique semantic.
7. **Multiline Tables** — References styles (table-level and in-cell), combined commands. Complex interaction with content within cells.
8. **Content Islands** — References styles. Simplest extension — styled blockquotes using standard CommonMark. Good closing section.

### Extension Interaction Matrix

Each extension's "Interaction with Other Extensions" subsection should cover the interactions marked below:

| Extension | Variables | Styles | Aliases | Conditions | Includes | Markers | Multiline | Content Islands |
|-----------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Variables | — | | | ✓ | ✓ | | | |
| Styles | | — | ✓ | ✓ | | | ✓ | ✓ |
| Aliases | | ✓ | — | ✓ | | | | |
| Conditions | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Includes | ✓ | | | ✓ | ✓ | | | |
| Markers | | ✓ | ✓ | ✓ | | — | | |
| Multiline | ✓ | ✓ | | ✓ | | | — | |
| Content Islands | ✓ | ✓ | | ✓ | | | | — |

Key interactions to specify normatively:
- **Variables × Conditions**: Variables in Hidden condition blocks are never resolved (processing order: conditions before variables). Variable values cannot contain condition syntax.
- **Variables × Includes**: Variable map is document-global. Variable values cannot contain include syntax. Processing order: includes → conditions → variables.
- **Styles × Combined commands**: Style can be combined with markers, aliases, multiline via semicolons. Order: style first.
- **Styles × Multiline tables**: Styles can apply to the table (above `<!-- multiline -->`) or within cells (inline within cell content).
- **Conditions × Includes**: Per-file condition evaluation before splicing. Cross-file condition span is MDPP012 (fatal).
- **Conditions × Everything**: Conditions can wrap any content containing any extension. All extensions within Hidden blocks are removed.
- **Aliases × Link references**: Aliases create anchor IDs that link reference definitions can target. Cross-file resolution via `spec/cross-file-link-resolution.md`.

## Implementation Units

- [ ] **Unit 1: Specification scaffold and front matter**

**Goal:** Create `spec/specification.md` with the complete document structure, frontmatter, introduction, scope, conformance levels, terminology, and notation sections.

**Requirements:** R1, R2, R3, R4, R5, R14

**Dependencies:** None

**Files:**
- Create: `spec/specification.md`

**Approach:**
- Frontmatter: `date: 2026-04-08`, `status: draft`, plus a version field for Markdown++ 1.0
- Introduction states CommonMark 0.30 as the base, explains the additive extension model, and lists the four normative references
- Conformance section defines two levels with clear criteria:
  - **Pass-through**: Renderer that preserves HTML comment directives and literal `$name;` tokens unchanged. MUST NOT alter or strip Markdown++ extensions. The document renders as valid CommonMark with extensions visible as comments/text. MDPP diagnostics are not applicable — pass-through conformance is solely about preservation, not analysis.
  - **Full**: Processor that evaluates all extensions per this specification and its normative references. MUST implement all required features defined in the processing model's conformance section (`spec/processing-model.md` lines 481-511). The unified spec should reference the processing model's conformance requirements rather than redefining the feature list.
- Terminology section defines: directive, attachment, block-level element, inline element, extension comment, combined command, variable token, content island, recognized comment, variable map, condition set, processor, assembled document
- Notation section references W3C EBNF (as used in formal-grammar.md) and RFC 2119 keywords

**Patterns to follow:**
- Frontmatter format from `spec/processing-model.md` and `spec/attachment-rule.md`
- RFC 2119 conformance statement format from `spec/processing-model.md` line 40
- Terminology definition format from `spec/processing-model.md` lines 18-38

**Test scenarios:**
- All terminology terms are defined before first normative use
- Conformance levels have clear, non-overlapping criteria
- CommonMark 0.30 is explicitly stated as the base

**Verification:**
- The document has valid frontmatter, a complete table of contents structure, and all preliminary sections
- RFC 2119 boilerplate is present
- Both conformance levels are defined with testable criteria

---

- [ ] **Unit 2: Cross-cutting normative reference sections (grammar, attachment, processing model)**

**Goal:** Add sections 5-7 covering extension comment syntax, the attachment rule, and the processing model — each with an inline summary and normative reference to the corresponding sub-spec.

**Requirements:** R8, R9, R10

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- **Extension Comment Syntax section**: Summarize the two syntactic forms (variable tokens and HTML comment directives), the combined command syntax with semicolons, and the comment disambiguation rule. Reference `spec/formal-grammar.md` normatively for the complete EBNF grammar.
- **Attachment Rule section**: State the core rule (comment tag on the line immediately above the target with no blank line), list which commands require attachment vs. are exempt, and note the combined command solution for stacked tags. Reference `spec/attachment-rule.md` normatively.
- **Processing Model section**: Summarize the two-phase pipeline (Phase 1: include expansion + variable substitution; Phase 2: CommonMark parsing with extension extraction), the determinism guarantee, and the error severity model. Reference `spec/processing-model.md` normatively.

**Patterns to follow:**
- Cross-reference format from `spec/cross-file-link-resolution.md` lines 10-14 (how it references the processing model)
- Summary-then-reference pattern from the requirements doc key decisions

**Test scenarios:**
- Each section provides enough context that a reader can understand the concept without leaving the main spec
- Each normative reference is clearly stated with MUST language
- No normative duplication — the main spec summarizes but does not redefine rules

**Verification:**
- All three cross-cutting concerns are covered with summaries and normative references
- A reader can follow the spec end-to-end without jumping to sub-specs for basic understanding

---

- [ ] **Unit 3: Extension definitions — Variables, Custom Styles, Custom Aliases**

**Goal:** Write complete normative definition sections for extensions 1-3 (per the ordering in "Extension Ordering and Interaction Guidance"), following the per-extension template.

**Requirements:** R6, R7

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- **Variables** (section 8): Purpose (reusable content tokens), syntax (`$name;`), semantics (Phase 1 text-level substitution from variable map), escaping mechanisms (`\$` and code spans), interaction with conditions (variables in conditioned content are only substituted if the condition is visible — processing order is conditions before variables), interaction with includes (variable map is document-global, variable values cannot contain include syntax), attachment (not applicable — inline tokens), diagnostics (MDPP002 for invalid names, MDPP010 for undefined references). Source: syntax-reference.md lines 174-253, processing-model.md Phase 1 Step 2 (lines 270-329 for processing order and escaping semantics).
- **Custom Styles** (section 9): Purpose (apply named styles to block or inline elements), syntax (`<!-- style:Name -->`), semantics (style metadata attached to the element during Phase 2 parsing), block vs. inline placement rules, interaction with multiline tables (styles within cells), interaction with content islands (style above blockquote), interaction with combined commands (style is first in order), nested list styling (indentation matching), attachment (required — block above, inline immediately before with no space), diagnostics (MDPP002 for invalid names, MDPP004 for invalid placement, MDPP009 for orphaned tags). Source: syntax-reference.md lines 255-341.
- **Custom Aliases** (section 10): Purpose (stable anchor IDs for cross-referencing), syntax (`<!-- #name -->`), semantics (alias ID registered during Phase 2 parsing), block-level only constraint (inline aliases not supported — normative MUST NOT), interaction with link references and cross-file resolution (aliases create anchors that link refs target), interaction with combined commands (alias is last in order), attachment (required — line above target), diagnostics (MDPP002 for invalid names, MDPP008 for duplicates within file, MDPP009 for orphaned tags). Source: syntax-reference.md lines 343-393.
- See "Extension Ordering and Interaction Guidance" for the interaction matrix — each section's "Interaction with Other Extensions" subsection should cover the interactions marked in that matrix.

**Patterns to follow:**
- The per-extension template from the High-Level Technical Design section
- RFC 2119 language patterns from `spec/processing-model.md`
- Syntax table format from `spec/attachment-rule.md`
- Processing order semantics from `spec/processing-model.md` lines 270-329

**Test scenarios:**
- Each extension section covers all seven template subsections
- Variable escaping semantics are precisely specified with RFC 2119 language (both mechanisms: `\$` and code spans)
- Variable processing order implications are normatively stated (4 implications from processing-model.md lines 274-282)
- Style block vs. inline distinction is unambiguous with placement rules table
- Alias block-level-only constraint is normatively stated as MUST NOT for inline aliases

**Verification:**
- A tool author can implement variable substitution, style attachment, and alias registration from these sections alone (plus normative references)
- All applicable diagnostic codes are listed per extension
- Interaction subsections cover the interactions marked in the interaction matrix

---

- [ ] **Unit 4: Extension definitions — Conditions, File Includes**

**Goal:** Write complete normative definition sections for extensions 4-5 (Conditions and File Includes), the two Phase 1 extensions.

**Requirements:** R6, R7

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- **Conditions** (section 11): Purpose (conditional content visibility), syntax (`<!-- condition:expr -->` / `<!-- /condition -->`), semantics (evaluate expression against condition set, include or exclude content), expression operators (NOT `!`, AND space, OR comma) with precedence (highest to lowest: NOT → AND → OR), three-state model (Visible/Hidden/Unset — Unset defaults to document-visible), nesting rules, block and inline usage, interaction with includes (per-file evaluation before splicing — cross-file condition span is MDPP012 fatal), interaction with variables (conditions evaluated before variable substitution — processing order), interaction with ALL other extensions (conditions can wrap content containing any extension; content in Hidden blocks is removed before other extensions process it), attachment (exempt — wraps content, blank lines permitted within), diagnostics (MDPP001 for unclosed blocks, MDPP007 for invalid syntax, MDPP012 for cross-file spans). Source: syntax-reference.md lines 395-475, processing-model.md Phase 1 Step 1.
- **File Includes** (section 12): Purpose (multi-file document assembly), syntax (`<!-- include:path -->`), semantics (Phase 1 recursive depth-first expansion), path resolution (relative to containing file's directory), recursion and cycle detection, depth limits (SHOULD default to 10), interaction with conditions (conditional includes — include within condition block), interaction with variables (inherited variable map, variable values cannot contain include syntax), interaction with link references (document-global after assembly — reference cross-file-link-resolution.md), attachment (exempt — standalone directive), diagnostics (MDPP005 for circular includes in static validation, MDPP006 for missing files, MDPP011 for max depth, MDPP013 for runtime cycle detection). Source: syntax-reference.md lines 477-527, processing-model.md Phase 1 Step 1.
- See "Extension Ordering and Interaction Guidance" for the interaction matrix. Conditions interact with ALL other extensions (the broadest interaction surface). File Includes interact with conditions, variables, and link references.

**Patterns to follow:**
- Condition expression table format from syntax-reference.md lines 406-422
- Processing model's Phase 1 description for include semantics
- Condition nesting and inline condition examples from syntax-reference.md lines 452-465

**Test scenarios:**
- Condition expression precedence is unambiguously specified with explicit example: `!draft,web production` = `(!draft) OR (web AND production)`
- The three-state condition model (Visible/Hidden/Unset) is normatively defined with Unset default behavior
- Include path resolution is precise enough to implement (relative to containing file, not root)
- Cycle detection is a MUST requirement with MDPP013
- Cross-file condition span is a fatal error (MDPP012) — normatively stated with example

**Verification:**
- A tool author can implement condition evaluation and include expansion from these sections plus the processing model reference
- All applicable diagnostic codes are listed per extension
- Processing order between conditions, includes, and variables is unambiguous

---

- [ ] **Unit 5: Extension definitions — Markers/Metadata, Multiline Tables, Content Islands**

**Goal:** Write complete normative definition sections for extensions 6-8 (the remaining Phase 2 extensions).

**Requirements:** R6, R7

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- **Markers/Metadata** (section 13): Purpose (attach metadata key-value pairs to elements), two syntax forms (simple `marker:Key="value"` and JSON `markers:{...}`), semantics (metadata association during Phase 2), key naming rules (standard identifier for simple format), JSON validation (MUST be valid JSON object), Passthrough marker semantics (raw content injection — value emitted as-is, no Markdown or variable processing), IndexMarker format (primary:secondary nesting, comma for multiple entries), interaction with styles and aliases (via combined commands), interaction with conditions (markers within condition blocks), attachment (required — line above target), diagnostics (MDPP002 for invalid key names, MDPP003 for malformed JSON, MDPP009 for orphaned tags). Source: syntax-reference.md lines 529-654.
- **Multiline Tables** (section 14): Purpose (block content within table cells), syntax (`<!-- multiline -->` above table), semantics (continuation rows identified by empty first cell, row boundaries by empty row with cell borders), supported content within cells (lists, blockquotes, styled elements with inline/block placement, code blocks), alignment (standard Markdown syntax), interaction with styles (table-level via `<!-- style:Name ; multiline -->` and in-cell via inline/block placement), interaction with variables (variable tokens within cells), interaction with conditions (within cells), interaction with combined commands (multiline is second in order after style), attachment (required — line above table), diagnostics (MDPP009 for orphaned tags). Source: syntax-reference.md lines 656-778.
- **Content Islands** (section 15): Purpose (self-contained content blocks using blockquotes), semantics (blockquotes with custom styles create configurable content areas for callouts, notes, warnings), supported nested content (headings, lists, code blocks, formatting, other Markdown++ extensions including variables and conditions), interaction with styles (style tag on line above blockquote — standard block-level attachment), attachment (standard block-level — style above blockquote), diagnostics (MDPP009 for orphaned style tags). This section will be proportionally brief (~1/3 the size of other extension sections) since Content Islands are styled blockquotes — standard CommonMark with a Markdown++ style convention, not a new syntactic form. Source: syntax-reference.md lines 895-908, SKILL.md Content Islands section.
- See "Extension Ordering and Interaction Guidance" for the interaction matrix.

**Patterns to follow:**
- Marker format tables from syntax-reference.md
- Multiline table structure rules from syntax-reference.md lines 671-677
- Passthrough marker example from syntax-reference.md lines 596-627

**Test scenarios:**
- Both marker syntax forms are normatively specified with clear rules for when to use each (simple for single key-value, JSON for multiple)
- Passthrough marker semantics are precise (raw content, no processing, distinct from unrecognized comments)
- Multiline table row boundary detection is unambiguous (empty first cell = continuation, empty row = boundary)
- Content Islands section correctly characterizes the feature as a style convention on standard blockquotes — no new syntax, no new processing model behavior
- In-cell styling within multiline tables is normatively specified (both block and inline)

**Verification:**
- A tool author can implement markers, multiline tables, and content island processing from these sections
- All applicable diagnostic codes are listed per extension
- Content Islands section does not invent new behavior beyond what exists in the source material

---

- [ ] **Unit 6: Advanced topics — Inline styling, Book assembly, Link reference definitions**

**Goal:** Add sections covering inline styling for images and links, book assembly patterns, and cross-file link reference definitions.

**Requirements:** R11, R13

**Dependencies:** Units 3-5

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- **Combined Commands** (section 16): Standalone section for the semicolon-separated combined command syntax. Covers: evaluation order (style → multiline → marker → alias), whitespace rules (spaces around semicolons optional but recommended), unrecognized segment behavior (silently ignored as inline comments — a normative MUST), and the processing model's classification of combined commands as an OPTIONAL feature (`spec/processing-model.md` lines 504-505). This warrants its own section because it has its own evaluation order, whitespace rules, and the inline comment behavior for unrecognized segments. Source: syntax-reference.md lines 780-863.
- **Inline Styling for Images and Links**: Normative definition of inline style placement for images (`<!-- style:Name -->![alt](src)`) and links (`[<!-- style:Name -->*text*](url)`). The image pattern places the style before the image syntax. The link pattern places the style inside the link text brackets. Both follow the inline attachment rule (no space between closing `-->` and element). Source: syntax-reference.md lines 865-892.
- **Book Assembly**: Describe the assembly pattern: a root document that uses `<!-- include: -->` directives to compose chapters into a publication. The processing model's Phase 1 include expansion is the assembly mechanism. Cross-document concerns (link references, variable scope, condition evaluation) are covered by the processing model and cross-file link resolution specs. This section is descriptive guidance, not new normative requirements — the normative rules are already in the processing model. Frame cross-file resolution as a derived behavior (consequence of Phase 1 assembly), not an independent feature. Note: cross-document numbering and pagination are processor-specific output concerns, out of scope.
- **Link Reference Definitions**: Summarize the cross-file link reference resolution model — document-global scope after assembly, first-definition-wins for conflicts, slug case-insensitivity per CommonMark 0.30. Describe the semantic cross-reference pattern (combined command + heading + link reference definition). Reference `spec/cross-file-link-resolution.md` normatively for the complete definition including MDPP014 diagnostic.

**Patterns to follow:**
- Inline style examples from syntax-reference.md lines 865-892
- Assembly pattern from `examples/includes-and-conditions.md`
- Cross-reference pattern from `examples/semantic-cross-references.md`

**Test scenarios:**
- Inline style placement for images vs. links is clearly distinguished
- Book assembly section references the processing model without duplicating normative content
- Link reference section references cross-file-link-resolution.md normatively

**Verification:**
- All three advanced topics are covered
- No new normative requirements are invented that should belong in existing sub-specs

---

- [ ] **Unit 7: Diagnostic registry and references**

**Goal:** Add the consolidated diagnostic code registry (MDPP001-MDPP014) and the normative/informative references section.

**Requirements:** R12

**Dependencies:** Units 3-6

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- **Diagnostic Registry**: Single table consolidating all 14 diagnostic codes with columns: Code, Name, Severity, Phase (Static/Processing), Description, Triggering Condition, Required Level (Pass-through: N/A, Full: MUST/SHOULD). Recovery behavior is referenced via the processing model, not re-specified. Sources: syntax-reference.md lines 910-925 for MDPP001-009, processing-model.md lines 452-477 for MDPP010-014. Note: MDPP002 description must use the expanded scope "Invalid name (variable, style, alias, or marker key)" not the original "Invalid variable name" — this was expanded when naming rules were unified (see `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`).
- **Normative References**: CommonMark 0.30, RFC 2119, and the four sub-specs (formal-grammar.md, processing-model.md, attachment-rule.md, cross-file-link-resolution.md)
- **Informative References**: The whitepaper, GFM spec (for table support), examples directory

**Patterns to follow:**
- Diagnostic table format from `spec/processing-model.md` lines 470-477
- Reference formatting conventions from existing sub-specs

**Test scenarios:**
- All 14 diagnostic codes are present in the registry
- No codes are missing or duplicated
- Severity levels match the source documents
- Each code maps to at least one extension or cross-cutting section

**Verification:**
- The diagnostic registry is a single, complete source of truth for all MDPP codes
- References section includes all normative and informative sources

---

- [ ] **Unit 8: Final review and cross-reference validation**

**Goal:** Review the complete specification for internal consistency, cross-reference accuracy, and completeness against requirements.

**Requirements:** R1-R14 (all)

**Dependencies:** Units 1-7

**Files:**
- Modify: `spec/specification.md`

**Approach:**
- Verify every requirement (R1-R14) is addressed in the specification
- Check all cross-references to sub-specs point to correct sections and use consistent normative language
- Verify terminology is used consistently throughout (terms match definitions in the terminology section)
- Confirm RFC 2119 keywords are used correctly (MUST for absolute requirements, SHOULD for recommendations, MAY for optional behavior). **Critical**: Audit for SHOULD/MUST inconsistencies between the main spec's summaries and sub-spec definitions — the cross-file link resolution spec had a SHOULD/MUST contradiction for MDPP014 emission that was caught in review (see `docs/solutions/documentation-gaps/cross-file-link-resolution-semantics-2026-04-08.md`)
- Check that each extension section covers all seven template subsections
- Verify the diagnostic registry matches the codes referenced in individual extension sections
- Confirm conformance levels are referenced consistently in the diagnostic registry
- Add any missing cross-references between sections within the specification

**Patterns to follow:**
- Cross-reference validation approach from the cross-file-link-resolution plan

**Test scenarios:**
- Every R1-R14 requirement has at least one corresponding section
- No broken internal cross-references
- No terminology drift (same concept always uses the same defined term)
- Diagnostic codes in extension sections match the registry

**Verification:**
- The specification is internally consistent
- A tool author reading from start to finish encounters no undefined terms, broken references, or contradictory statements
- All 14 requirements from the origin document are satisfied

## System-Wide Impact

- **Interaction graph:** The specification references four sub-specs normatively. Changes to any sub-spec automatically affect the specification's normative requirements. The specification does not modify any existing sub-spec.
- **Error propagation:** The diagnostic registry consolidates codes from two sources (syntax-reference.md and processing-model.md). If codes are added or modified in the source documents, the registry must be updated.
- **State lifecycle risks:** None — this is a documentation deliverable with no runtime state.
- **API surface parity:** The specification should be consistent with the plugin syntax-reference.md. Any normative requirement in the specification should not contradict guidance in the syntax reference.
- **Integration coverage:** The specification's internal consistency (cross-references, terminology, diagnostic codes) should be verified as a whole-document review.

## Risks & Dependencies

- **Sub-spec stability assumption**: The plan assumes all four sub-specs are complete and stable. If any sub-spec changes during implementation, the corresponding summary section and diagnostic registry must be updated. **Mitigation**: Check sub-spec file modification dates before starting each unit. If a sub-spec has been modified since planning, re-read it before writing the corresponding section.

- **Normative consistency between main spec and sub-specs**: The per-extension definitions (Units 3-5) will contain normative statements about processing behavior, diagnostic codes, and attachment rules that must be consistent with the sub-specs. For example, if the Variables section states processing order rules that slightly differ from the processing model's Phase 1 Step 2 description, implementations would face contradictory requirements. **Mitigation**: Each extension section should use "as specified in [Sub-spec Name]" for cross-cutting behavior rather than restating normative rules in different words. The interaction subsections should reference the relevant sub-spec section for processing semantics. Unit 8 (final review) explicitly validates cross-reference consistency.

- **Conformance level alignment with processing model**: The processing model (`spec/processing-model.md` lines 481-511) already defines its own conformance section with required features, optional features, and a conformance statement. The unified spec's conformance section must align with this — not contradict or supersede it. **Mitigation**: The unified spec's conformance section should define the two levels (Pass-through and Full) and reference the processing model's conformance requirements for Full-level processors rather than redefining the feature list.

- **Document length**: With eight extension definitions plus cross-cutting sections, the specification may reach 800-1200 lines. This is appropriate for a formal spec but requires careful organization to remain navigable. **Mitigation**: Use consistent heading hierarchy and the per-extension template to aid navigation. Consider adding a table of contents at the top of the document.

- **Content Islands thinness**: The syntax-reference.md has minimal Content Islands documentation (~13 lines). The spec section must formalize what exists without inventing new behavior. **Mitigation**: Keep the Content Islands section proportionally brief (~1/3 of other extension sections). If gaps are discovered during writing, flag them as open questions rather than speculatively filling them.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-formal-specification-requirements.md](../brainstorms/2026-04-08-formal-specification-requirements.md)
- Related specs: `spec/formal-grammar.md`, `spec/processing-model.md`, `spec/attachment-rule.md`, `spec/cross-file-link-resolution.md`
- Primary content source: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- Related examples: `examples/semantic-cross-references.md`, `examples/includes-and-conditions.md`
- Related issues: #7 (this issue), #8 (processing model), #10 (attachment rule), #11 (formal grammar), #22 (cross-file link resolution)
- External specs: [CommonMark 0.30](https://spec.commonmark.org/0.30/), [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt)
