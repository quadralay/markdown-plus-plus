---
title: "docs: Document multiline table separator pattern, headers, and dedent"
type: feat
status: completed
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-multiline-table-separators-requirements.md
---

# docs: Document multiline table separator pattern, headers, and dedent

## Overview

Document three undocumented or misdocumented multiline table behaviors: the exact row separator pattern (pipes required), multiline header support, and the cell content dedent algorithm. Update all files that describe multiline table behavior to use precise, consistent terminology.

## Problem Frame

Authors writing multiline tables need to understand how row boundaries work. The current documentation describes row separators as "empty rows" or rows "with cell borders," which is ambiguous. The ePublisher parser requires pipe characters in separator rows — a truly blank line (no pipes) **ends the table entirely**, it does not separate rows. Additionally, multiline header rows and the dedent algorithm are supported but completely undocumented. (See origin: `docs/brainstorms/2026-04-08-multiline-table-separators-requirements.md`)

## Requirements Trace

- R1. Document the exact row separator pattern: pipe characters with only whitespace between them, matching `^ {0,3}\|(?:[ ]*\|)+[ ]*$`
- R2. Clarify that a completely blank line (no pipes) ends the table, not separates rows
- R3. Document multiline header support with at least one example
- R4. Document the cell content dedent algorithm (minimum common leading whitespace stripping)

## Scope Boundaries

- **In scope:** Documentation updates to syntax reference, SKILL.md, best practices, examples, whitepaper, processing model, and formal grammar
- **Out of scope:** Parser code changes, new features, test automation
- **Out of scope:** Extensions inside multiline table cells (covered by #21)

## Context & Research

### Relevant Code and Patterns

Files requiring updates, with current problematic language:

| File | Current Language | Lines |
|------|-----------------|-------|
| `plugins/.../references/syntax-reference.md` | "Empty row with cell borders separates table rows" | ~677 |
| `plugins/.../SKILL.md` | "empty row separates records" | ~169 |
| `plugins/.../references/best-practices.md` | "Empty row with borders separates table rows" | ~240 |
| `plugins/.../references/examples.md` | "separated by an empty row with cell borders" | ~214 |
| `spec/whitepaper.md` | "empty separator rows marking cell boundaries" | ~237 |
| `spec/formal-grammar.md` | No row structure productions or constraints | ~255-261 |
| `spec/processing-model.md` | "Recognition and processing of multiline commands" (undefined) | ~494 |
| `examples/multiline-tables.md` | "Empty separator rows mark cell boundaries" | ~28 |

### Institutional Learnings

- **Grammar-first principle** (`docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md`): Grammar productions should accompany prose documentation. For multiline table structure, a prose structural constraint (like attachment rules) is more appropriate than EBNF since row structure depends on CommonMark table parsing.
- **Single source of truth** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Designate one canonical location and reference it from others. The syntax reference will be the primary detailed location.
- **Coordinated updates** (`docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md`): Update all touchpoints together — syntax-reference.md, whitepaper.md, examples, best-practices.md, SKILL.md.

## Key Technical Decisions

- **Syntax reference is the canonical detailed location:** The full row separator pattern, multiline header documentation, and dedent algorithm will be documented in detail in `syntax-reference.md`. Other files will use corrected terminology and reference the syntax reference for details.
- **Formal grammar gets a structural constraint, not EBNF:** Row separator detection and continuation row merging are table-level structural behaviors that depend on CommonMark table parsing. They belong as prose structural constraints (like attachment rules in Section "Structural Constraints"), not EBNF/PEG productions.
- **Processing model defines multiline processing sub-requirements:** Required feature #7 ("Multiline table processing") currently lacks definition. It should enumerate: row separator recognition, continuation row merging, blank-line termination, and cell content dedent as conformance sub-requirements.
- **Document parser-actual behavior:** The regex `^ {0,3}\|(?:[ ]*\|)+[ ]*$` is the source of truth. Documentation must match what the parser does.

## Open Questions

### Resolved During Planning

- **Which files need updates?** All eight files identified in the audit table above. `tests/sample-full.md` does not need changes (code examples already show correct separator rows; no prose to update).
- **Should formal-grammar.md get EBNF productions for row structure?** No — add a prose structural constraint note instead. Row structure depends on CommonMark table parsing, which is outside Markdown++'s grammar scope. This follows the same pattern as attachment rules.
- **Should dedent go in the processing model?** Yes — as a conformance sub-requirement under required feature #7. The processing model should define what "multiline table processing" means.

### Deferred to Implementation

- **Exact wording for the structural constraint in formal-grammar.md:** The implementer should follow the style of the existing "Structural Constraints" section.
- **Whether to include the regex pattern literally in the processing model:** The syntax reference should show it; the processing model may describe the behavior normatively without the regex.

## Implementation Units

- [x] **Unit 1: Update syntax-reference.md — canonical multiline table documentation**

  **Goal:** Replace the ambiguous "Structure Rules" section with precise documentation covering all four requirements. This is the primary detailed location that other files will reference.

  **Requirements:** R1, R2, R3, R4

  **Dependencies:** None

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

  **Approach:**
  - Replace the "Structure Rules" list (lines 672-677) to:
    - Define "row separator" precisely: a table row where every cell contains only whitespace, pipe characters must be present (show the pattern)
    - Explicitly state that a completely blank line (no pipes) ends the table
    - Add a "caution" or "important" callout for the blank-line-ends-table distinction
  - Add a new subsection "### Multiline Headers" after the basic example, with an example showing a header row that spans multiple physical lines using continuation rows
  - Add a new subsection "### Cell Content Dedent" explaining minimum common leading whitespace stripping, with a before/after example showing source table content and the resulting output content
  - Keep examples consistent with existing style (aligned columns, descriptive content)

  **Patterns to follow:**
  - Existing subsection structure in the Multiline Tables section (### heading, code block, brief explanation)
  - Annotation style used in other sections for important distinctions

  **Test scenarios:**
  - A reader can distinguish `|      |      |` (row separator) from a blank line (table terminator)
  - The multiline header example clearly shows continuation rows above the delimiter
  - The dedent example shows that `"  line1\n  line2"` becomes `"line1\nline2"` after stripping 2 common leading spaces

  **Verification:**
  - The section covers all four requirements (R1-R4)
  - No instance of "empty row" without qualification remains in the Multiline Tables section
  - Examples are syntactically valid Markdown++ tables

- [x] **Unit 2: Update SKILL.md — concise corrected summary**

  **Goal:** Fix the misleading "empty row separates records" language in the SKILL.md quick reference.

  **Requirements:** R1, R2

  **Dependencies:** Unit 1 (for consistent terminology)

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`

  **Approach:**
  - Replace the sentence at line 169 with precise language: separator rows require pipes with whitespace-only cells; blank lines end the table
  - Keep it concise — SKILL.md is a quick reference, not the detailed spec
  - Reference syntax-reference.md for full details (already does this)

  **Patterns to follow:**
  - Existing terse style of SKILL.md descriptions

  **Test scenarios:**
  - The updated text accurately distinguishes separator rows from blank lines
  - No new subsections or verbose explanations added (keep SKILL.md concise)

  **Verification:**
  - Line 169 area uses corrected terminology
  - Reference to syntax-reference.md for details is preserved

- [x] **Unit 3: Update best-practices.md and examples.md — corrected terminology**

  **Goal:** Fix misleading terminology in both reference files.

  **Requirements:** R1, R2

  **Dependencies:** Unit 1 (for consistent terminology)

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md`

  **Approach:**
  - `best-practices.md` line 240: Replace "Empty row with borders separates table rows" with precise language about pipe-delimited whitespace-only rows as separators, and note that blank lines end the table
  - `examples.md` line 214: Replace "separated by an empty row with cell borders" with corrected terminology

  **Patterns to follow:**
  - Keep the brief, practical tone of both files
  - Do not add detailed explanations — reference syntax-reference.md

  **Test scenarios:**
  - No instance of unqualified "empty row" remains in either file's multiline table descriptions

  **Verification:**
  - Both files use terminology consistent with the syntax reference

- [x] **Unit 4: Update examples/multiline-tables.md — add multiline header example**

  **Goal:** Fix terminology and add a multiline header example to the standalone example file.

  **Requirements:** R1, R2, R3

  **Dependencies:** Unit 1 (for consistent terminology and header example pattern)

  **Files:**
  - Modify: `examples/multiline-tables.md`

  **Approach:**
  - Line 28: Replace "Empty separator rows mark cell boundaries" with corrected terminology
  - Add a new section "## Multiline header" demonstrating a header row that spans multiple physical lines using continuation rows above the delimiter row
  - Keep the example practical and consistent with the existing feature-comparison and format-comparison themes

  **Patterns to follow:**
  - Existing section structure in the file: `## Section heading`, brief prose, then a styled multiline table example

  **Test scenarios:**
  - The multiline header example is a valid Markdown++ table
  - The header shows continuation rows above the delimiter (empty first cell pattern in the header area)

  **Verification:**
  - The file demonstrates all three documented patterns: continuation rows, separator rows, and multiline headers

- [x] **Unit 5: Update spec/whitepaper.md — precise terminology**

  **Goal:** Fix the "empty separator rows" language in the whitepaper.

  **Requirements:** R1, R2

  **Dependencies:** Unit 1 (for consistent terminology)

  **Files:**
  - Modify: `spec/whitepaper.md`

  **Approach:**
  - Line 237: Replace "with empty separator rows marking cell boundaries" with language that specifies separator rows contain pipe characters with whitespace-only cells
  - Keep the change minimal — the whitepaper provides rationale, not detailed syntax rules

  **Patterns to follow:**
  - Existing whitepaper prose style (explanatory, not normative)

  **Test scenarios:**
  - The whitepaper does not imply that blank lines separate rows

  **Verification:**
  - Line 237 area uses corrected terminology consistent with the syntax reference

- [x] **Unit 6: Update spec/processing-model.md — define multiline table processing**

  **Goal:** Expand required feature #7 from a one-line stub to a defined conformance requirement that specifies what "multiline table processing" means.

  **Requirements:** R1, R2, R4

  **Dependencies:** Unit 1 (for consistent definitions)

  **Files:**
  - Modify: `spec/processing-model.md`

  **Approach:**
  - Expand required feature #7 (line 494) to enumerate the sub-requirements of multiline table processing using RFC 2119 language:
    - Row separator recognition: a row matching the pipe-delimited whitespace pattern separates logical rows
    - Continuation row merging: rows with an empty first cell are merged into the preceding logical row
    - Blank-line termination: a completely blank line (no pipes) ends the table
    - Cell content dedent: the processor MUST strip the minimum common leading whitespace from all lines of each cell's content
  - Add this as an enumerated sub-list under item 7, following the pattern of other required features that reference specific phases
  - Note that the multiline algorithm applies to both header rows (above the delimiter) and body rows (below it)

  **Patterns to follow:**
  - Existing required feature descriptions (items 1-6, 8-10) that reference specific processing phases and use RFC 2119 language
  - Sub-requirements should be lettered (a, b, c, d) under the main item

  **Test scenarios:**
  - A conformant processor implementer can determine exactly what "multiline table processing" requires
  - The dedent algorithm is specified precisely enough that two independent implementations would produce identical output

  **Verification:**
  - Required feature #7 now defines four concrete sub-requirements
  - RFC 2119 language (MUST) is used consistently

- [x] **Unit 7: Update spec/formal-grammar.md — structural constraint for multiline tables**

  **Goal:** Add a prose note in the Structural Constraints section describing multiline table row structure behavior, following the pattern used for attachment rules.

  **Requirements:** R1, R2, R3

  **Dependencies:** Unit 1, Unit 6 (for consistent definitions)

  **Files:**
  - Modify: `spec/formal-grammar.md`

  **Approach:**
  - Add a paragraph after the existing `multiline_cmd` production (line 261) or in the Structural Constraints section (line 298+) explaining:
    - The `multiline_cmd` production defines only the directive keyword
    - Multiline table row structure (separator rows, continuation rows, multiline headers) is a table-level structural behavior defined in the [processing model](processing-model.md), not an EBNF production
    - Brief summary of the key structural behaviors for cross-reference
  - This follows the same pattern as attachment rules: "Several Markdown++ commands require attachment... Attachment is a positional relationship that EBNF/PEG cannot naturally express."

  **Patterns to follow:**
  - The "Structural Constraints" section pattern: prose explaining what EBNF cannot express, then a reference to the authoritative document

  **Test scenarios:**
  - A grammar reader understands that multiline table row structure is intentionally outside the EBNF scope
  - The cross-reference to the processing model is accurate

  **Verification:**
  - The formal grammar acknowledges multiline table structure without attempting EBNF productions for it
  - The processing model is referenced as the authoritative source

## System-Wide Impact

- **Interaction graph:** No runtime behavior changes — documentation only. The syntax reference, SKILL.md, and spec documents are consumed by human authors and Claude Code agents.
- **Error propagation:** N/A (no code changes)
- **State lifecycle risks:** N/A
- **API surface parity:** All seven files that describe multiline table behavior will be updated to use consistent terminology
- **Integration coverage:** Verify terminology consistency across all updated files

## Risks & Dependencies

- **Terminology drift risk:** Seven files must use consistent language. Mitigation: Unit 1 establishes the canonical definitions; subsequent units reference and align to them.
- **Dependency on issue #11 (formal grammar):** The formal grammar may be evolving. Mitigation: Unit 7 adds only a prose structural constraint, not EBNF productions, minimizing conflict.
- **Dependency on issue #21 (extensions in cells):** Out of scope per requirements. No conflict — this work documents row-level behavior, not cell content extensions.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-multiline-table-separators-requirements.md](docs/brainstorms/2026-04-08-multiline-table-separators-requirements.md)
- Related issues: #11 (formal grammar), #21 (extensions inside multiline cells)
- Parser regex: `^ {0,3}\|(?:[ ]*\|)+[ ]*$` (ePublisher implementation, source of truth)
- Institutional learnings: `docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md`, `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`
