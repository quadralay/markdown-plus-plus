---
title: "feat: Document extension behavior in multiline table cells"
type: feat
status: completed
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-multiline-cell-extensions-requirements.md
---

# feat: Document extension behavior in multiline table cells

## Overview

Create `spec/multiline-cell-extensions.md` — a normative specification documenting which Markdown++ extensions are valid inside multiline table cells, how they interact with the table context, and what restrictions apply. The document is organized around the processing model's phase ordering: Phase 1 extensions operate on raw text before table recognition, Phase 2 extensions operate during per-cell Markdown parsing.

## Problem Frame

Multiline table cells are parsed as full Markdown documents — the ePublisher parser creates a temporary `WifMarkdown` instance per cell. This means any Markdown and potentially any Markdown++ extension could appear inside a cell. But the spec doesn't define which extensions are valid within cells or how they interact with the table context.

Without this documentation, implementors must guess which extensions are valid in cells, authors don't know what they can safely put in table cells, and edge cases (conditions wrapping rows, nested tables, includes in cells) have no normative guidance.

(see origin: [docs/brainstorms/2026-04-08-multiline-cell-extensions-requirements.md](../brainstorms/2026-04-08-multiline-cell-extensions-requirements.md))

## Requirements Trace

- R1. Variables work in cells — resolved in Phase 1 before table parsing
- R2. Conditions work in cells at raw-text level — wrapping complete rows is valid, partial row wrapping produces undefined structure
- R3. Include directives inside cells are NOT supported (MUST NOT)
- R4. Block styles work in cells — directive on continuation row attaches to following content
- R5. Inline styles work in cells — standard inline attachment rule applies
- R6. Aliases are syntactically valid but not recommended in cells (SHOULD NOT)
- R7. Markers are syntactically valid but unusual in cells
- R8. Nested multiline tables are NOT supported (MUST NOT)
- R9. Standard Markdown block elements work in cells
- R10. Headings in cells are syntactically valid but semantically questionable
- R11. Fenced code blocks in cells require careful formatting
- R12. Phase-ordering principle determines all extension interactions with cells
- R13. Combined commands within cells follow standard evaluation order

## Scope Boundaries

- **In scope**: Enumerating which extensions work in cells, documenting restrictions, providing guidance on edge cases
- **In scope**: Explaining why each extension does or doesn't work based on the processing model's phase ordering
- **Out of scope**: Changing the processing model or the multiline table syntax
- **Out of scope**: Defining new MDPP diagnostic codes for cell-specific errors (follow-up work if needed)
- **Out of scope**: Modifying the syntax reference examples (though the spec section may reference them)

## Context & Research

### Relevant Code and Patterns

- **`spec/processing-model.md`** — The normative processing model. Phase 1 (includes, conditions, variables) and Phase 2 (Markdown parsing with extension extraction) determine which extensions work in cells and how. The new spec document cross-references this as the authoritative source for phase ordering.
- **`spec/attachment-rule.md`** — Established pattern for spec documents: YAML frontmatter (`date`/`status`), RFC 2119 language, numbered formal statements, edge case sections with code examples, cross-references to MDPP codes. The new document follows this exact pattern.
- **`spec/formal-grammar.md`** — Formal grammar for extension syntax. The new document does not modify the grammar — grammar productions are context-free and already apply within cells.
- **`plugins/.../references/syntax-reference.md` (lines 726–776)** — Existing examples of styled content in multiline table cells (block styles, inline styles, combined commands). These are normative examples that the new spec formalizes and extends.

### Institutional Learnings

- **Processing model specification** (`docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`): Established the two-phase pipeline and phase-ordering principle. The cell extensions spec applies this same principle to the specific context of multiline table cells.
- **Attachment rule formal spec** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Established the document pattern for formal spec documents within the `spec/` directory.

## Key Technical Decisions

- **Standalone `spec/multiline-cell-extensions.md`**: The content (13 requirements, examples, edge cases) is too large for a subsection of `processing-model.md` (already 515 lines). A dedicated document follows the `spec/attachment-rule.md` pattern — focused, self-contained, cross-referenced. If issue #9 (element interactions) is addressed later, it can reference this document. **Rationale:** Avoids bloating the processing model while keeping cell-specific guidance discoverable.

- **Phase ordering as organizing principle**: Rather than an arbitrary lookup table, the document explains that Phase 1 vs. Phase 2 determines everything. This gives authors and implementors a mental model. **Rationale:** The processing model is already the authoritative source; this document applies it to the specific cell context.

- **Three-tier categorization: supported / valid-but-not-recommended / not supported**: Extensions fall into distinct tiers. Variables, conditions, styles, markers, standard Markdown elements, combined commands, and fenced code blocks are supported. Aliases in cells are valid but not recommended. Nested tables and includes in cells are explicitly not supported. **Rationale:** Clear categories with RFC 2119 language prevent author confusion and give implementors unambiguous conformance requirements.

- **Partial condition wrapping as undefined behavior, not error**: A condition block that wraps some but not all continuation rows within a logical row produces undefined table structure. This is specified as "SHOULD avoid" rather than a new MDPP error code, because the condition engine operates correctly — it's the resulting table structure that is incoherent. **Rationale:** Avoids new error codes for what is fundamentally an authoring mistake, not a processing failure.

- **Cross-reference existing syntax reference examples**: The styles-in-cells examples already in the syntax reference (lines 726–776) establish normative precedent. The spec formalizes this behavior rather than replacing those examples. **Rationale:** Avoids contradicting existing documentation.

## Open Questions

### Resolved During Planning

- **Partial condition wrapping** (affects R2): Undefined behavior that authors SHOULD avoid. Conditions remove/keep lines correctly, but removing some continuation rows within a logical row leaves incoherent table structure. No new MDPP code — specify as SHOULD NOT with a clear example.

- **Where should this specification live?** (affects all): Dedicated `spec/multiline-cell-extensions.md`. Content too large for a processing-model.md subsection. Follows the focused-document pattern of `spec/attachment-rule.md`. Issue #9 can reference it later.

- **Nested tables** (affects R8): MUST NOT — resolved by maintainer direction. No plans to support nested multiline tables in cells.

- **Includes in cells** (affects R3): MUST NOT — resolved by maintainer direction. No plans to support include directives within table cell content.

### Deferred to Implementation

- **Fenced code blocks practical behavior** (affects R11): The parsing model predicts that fenced code blocks on continuation rows should work. The spec should state this is valid with formatting guidance, but note that implementation verification is recommended.
- **Exact wording of RFC 2119 conformance statements**: The spec writer should use MUST/SHOULD/MAY consistently; precise phrasing is an authoring decision during implementation.

## Implementation Units

- [x] **Unit 1: Document skeleton with frontmatter, introduction, and phase-ordering framework**

**Goal:** Create `spec/multiline-cell-extensions.md` with the document structure, introduction explaining purpose and scope, and the phase-ordering principle (R12) that organizes the rest of the document.

**Requirements:** R12

**Dependencies:** None

**Files:**
- Create: `spec/multiline-cell-extensions.md`

**Approach:**
- YAML frontmatter: `date: 2026-04-08`, `status: draft`
- Introduction: why this spec exists, relationship to processing model and syntax reference
- Phase-ordering framework section establishing the organizing principle: Phase 1 extensions operate on raw text containing the table rows before the table is recognized; Phase 2 extensions operate during per-cell Markdown parsing after table structure has been identified
- Summary table listing all extensions with their phase, category (supported / valid-but-not-recommended / not supported), and brief rationale
- Conformance keywords statement (RFC 2119)

**Patterns to follow:**
- `spec/attachment-rule.md` for frontmatter format, heading structure, and RFC 2119 boilerplate
- `spec/processing-model.md` for cross-reference format and definitions

**Test scenarios:**
- Document renders cleanly as standard Markdown
- Summary table accurately categorizes all extensions per requirements R1-R13
- Cross-references to processing-model.md use correct relative paths

**Verification:**
- File exists at `spec/multiline-cell-extensions.md` with correct frontmatter
- Phase-ordering principle is stated clearly enough that a reader can predict the category of any extension based on its processing phase

---

- [x] **Unit 2: Phase 1 extensions in cells — variables, conditions, includes**

**Goal:** Write the Phase 1 extensions section covering variables (R1), conditions (R2), and includes (R3), with examples and edge cases for each.

**Requirements:** R1, R2, R3

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/multiline-cell-extensions.md`

**Approach:**
- **Variables (R1):** Document that variables work because they are resolved in Phase 1, Step 2 before table parsing. Variable values appear as literal cell content. Provide example showing `$Product;` in a cell resolved to its value.
- **Conditions (R2):** Document that conditions work at the raw-text level. A condition wrapping complete table rows (first row + continuation rows + separator) works correctly — hidden rows are removed before Phase 2. Document that partial row wrapping (some continuation rows within a logical row) produces undefined table structure and SHOULD be avoided. Provide correct and incorrect examples.
- **Includes (R3):** Document that include directives inside cells are NOT supported (MUST NOT). Explain why: expanded content would need to conform to pipe-delimited format, making results fragile and unportable.

**Patterns to follow:**
- `spec/processing-model.md` Phase 1 sections for the explanatory pattern of stating the rule, then explaining why via phase ordering
- `spec/attachment-rule.md` edge case format (correct/incorrect code blocks with explanation)

**Test scenarios:**
- Variable in cell: `$version;` in a cell resolves to the variable value
- Condition wrapping complete rows: hidden rows removed, table structure intact
- Condition wrapping partial rows: orphaned continuation rows produce incoherent table
- Include in cell: clearly prohibited with rationale

**Verification:**
- All Phase 1 extension requirements (R1, R2, R3) covered with normative MUST/SHOULD/MAY statements
- Each extension has at least one code example
- The condition edge case (partial wrapping) has both correct and incorrect examples

---

- [x] **Unit 3: Phase 2 extensions in cells — styles, aliases, markers, nested tables, combined commands**

**Goal:** Write the Phase 2 extensions section covering block styles (R4), inline styles (R5), aliases (R6), markers (R7), nested tables (R8), and combined commands (R13).

**Requirements:** R4, R5, R6, R7, R8, R13

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/multiline-cell-extensions.md`

**Approach:**
- **Block styles (R4):** Document that a style directive on a continuation row attaches to the content element on the following continuation row within the same cell. Cross-reference existing syntax reference examples (lines 726–741).
- **Inline styles (R5):** Document that inline style directives work per the standard inline attachment rule. Cross-reference existing syntax reference example (lines 745–751).
- **Aliases (R6):** Document as syntactically valid but not recommended (SHOULD NOT). Aliases are navigational anchors for the document outline; an alias inside a cell does not participate in navigation structure usefully. Note that table-level aliases (on the `<!-- multiline -->` directive via combined commands) are the intended mechanism.
- **Markers (R7):** Document as syntactically valid and supported, though unusual. Markers attach metadata to block elements within cells — valid for use cases like marking specific cell content for indexing.
- **Nested tables (R8):** Document as NOT supported (MUST NOT). Note alternative approaches: restructuring content, using separate tables, or using styled lists.
- **Combined commands (R13):** Document that combined commands within cells follow the same evaluation order as outside cells: style (1), multiline (2), marker (3), alias (4). A combined command on a continuation row within a cell is valid.

**Patterns to follow:**
- `spec/processing-model.md` Combined Command Evaluation Order section for the table format
- Syntax reference styled content in cells examples for cross-referencing

**Test scenarios:**
- Block style in cell: style directive on continuation row attaches to next element
- Inline style in cell: no-space attachment rule works within pipe-delimited content
- Alias in cell: valid syntax but documented as not recommended
- Nested multiline table: clearly prohibited with rationale and alternatives
- Combined command in cell: evaluation order consistent with top-level behavior

**Verification:**
- All Phase 2 extension requirements (R4–R8, R13) covered with normative statements
- Cross-references to syntax-reference.md styled content examples use correct relative paths
- Aliases and markers are clearly distinguished (not recommended vs. supported-but-unusual)

---

- [x] **Unit 4: Standard Markdown in cells, edge cases, and cross-references**

**Goal:** Write the standard Markdown section (R9, R10, R11), add edge case documentation, and finalize cross-references to the processing model and syntax reference.

**Requirements:** R9, R10, R11

**Dependencies:** Unit 3

**Files:**
- Modify: `spec/multiline-cell-extensions.md`

**Approach:**
- **Standard Markdown (R9):** Document that paragraphs, lists (ordered/unordered), blockquotes, inline formatting (bold, italic, links, code spans, images) all work in cells. Cross-reference existing syntax reference examples.
- **Headings (R10):** Document as syntactically valid but semantically questionable. Headings in cells do not participate in the document outline. Recommend bold text or styled paragraphs as alternatives.
- **Fenced code blocks (R11):** Document as valid per the parsing model. Opening/closing fence lines appear on continuation rows. Note formatting difficulty and recommend implementation verification.
- **Edge cases section:** Consolidate key edge cases with clear correct/incorrect examples. Include: empty cells, cells with only whitespace, single continuation row vs. multiple, interaction between styles and lists within cells.
- **Cross-references:** Add a "Related Specifications" section linking to processing-model.md, attachment-rule.md, formal-grammar.md, and the syntax reference multiline tables section. Add cross-reference from processing-model.md Phase 2 section pointing to this document for cell-specific behavior.
- Final consistency pass: verify all 13 requirements are covered, cross-references resolve correctly, RFC 2119 language is consistent

**Patterns to follow:**
- `spec/attachment-rule.md` Related Specifications section format
- `spec/processing-model.md` cross-reference format

**Test scenarios:**
- Heading in cell: valid syntax, documented as semantically questionable with alternative recommendation
- Fenced code block in cell: valid with formatting guidance
- Cross-references from processing-model.md resolve to correct anchors in the new document
- All 13 requirements (R1–R13) have coverage in the completed document

**Verification:**
- Document is internally consistent: no undefined terms or broken cross-references
- All requirements from the origin document have normative coverage
- processing-model.md has a cross-reference to the new document
- Document follows the established spec/ directory conventions

## System-Wide Impact

- **Interaction graph:** The new document cross-references `spec/processing-model.md`, `spec/attachment-rule.md`, `spec/formal-grammar.md`, and the syntax reference. A minor cross-reference addition to `processing-model.md` (Phase 2 section) points to this document for cell-specific behavior. No other documents require modification.
- **Error propagation:** No new MDPP diagnostic codes are introduced. Partial condition wrapping in cells is specified as undefined behavior (authoring guidance), not as a processing error requiring a diagnostic code.
- **API surface parity:** The formal grammar (`spec/formal-grammar.md`) does not need modification — grammar productions are context-free and already apply within cells. The new document is a semantic specification layered on top of the grammar.
- **Integration coverage:** The specification's correctness is grounded in the ePublisher parser's per-cell `WifMarkdown` instance behavior. Full verification requires testing against the ePublisher implementation, which is out of scope for this spec-writing task.

## Risks & Dependencies

- **Consistency risk**: The new spec must not contradict the processing model, attachment rule, or syntax reference. Mitigation: Unit 4 includes an explicit cross-reference verification pass, and the document is structured around the same phase ordering already established in the processing model.
- **Completeness risk**: The ePublisher parser may have undocumented cell-specific behaviors not captured in the requirements. Mitigation: RFC 2119 language distinguishes required behavior from implementation-defined behavior, allowing future amendments.
- **Fenced code block uncertainty**: The spec states fenced code blocks are valid per the parsing model, but practical behavior hasn't been verified against the ePublisher parser. Mitigation: the spec includes a note recommending implementation verification, and uses SHOULD rather than MUST for formatting guidance.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-multiline-cell-extensions-requirements.md](../brainstorms/2026-04-08-multiline-cell-extensions-requirements.md)
- Related spec: [spec/processing-model.md](../../spec/processing-model.md)
- Related spec: [spec/attachment-rule.md](../../spec/attachment-rule.md)
- Related spec: [spec/formal-grammar.md](../../spec/formal-grammar.md)
- Related reference: [syntax-reference.md](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) (Multiline Tables section, lines 656–776)
- Related solution: [docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md](../solutions/documentation-gaps/processing-model-specification-2026-04-08.md)
- Related issue: [#24](https://github.com/quadralay/markdown-plus-plus/issues/24) — Extensions in multiline table cells
- Related issue: [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) — Processing model specification
- Related issue: [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) — Element interactions
- Related issue: [#20](https://github.com/quadralay/markdown-plus-plus/issues/20) — Multiline table row separators
