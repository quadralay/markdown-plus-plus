---
title: "feat: Add processing model specification"
type: feat
status: active
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-processing-model-requirements.md
---

# feat: Add processing model specification

## Overview

Create `spec/processing-model.md` -- the normative specification for how a conformant Markdown++ processor evaluates extensions. This formalizes the two-phase pipeline (pre-processing text transforms, then Markdown parsing with extension extraction) that the ePublisher implementation already follows, making it possible for other tools to implement Markdown++ with confidence.

## Problem Frame

Markdown++ defines syntax for seven extension types but has no specification of runtime evaluation semantics. The syntax reference describes what each extension looks like; it does not describe the processing order, scoping rules, error behavior, or output model. Without a processing model, every implementor must guess at fundamental questions -- making it impossible to build a second conformant implementation or reason about document behavior when extensions interact.

The ePublisher adapter contains an implicit processing model that has been in production use. This effort extracts and formalizes that model as the normative standard.

(see origin: [docs/brainstorms/2026-04-08-processing-model-requirements.md](../brainstorms/2026-04-08-processing-model-requirements.md))

## Requirements Trace

- R1. Deterministic, ordered processing pipeline with two major phases
- R2. Phase 1 specifies three sequential steps: include expansion with per-file condition evaluation, variable substitution, handoff to Phase 2
- R3. Critical ordering implications stated explicitly (variables in false conditions never resolved; variable values cannot contain condition syntax; can contain Markdown syntax)
- R4. Include expansion is depth-first recursive with cycle detection
- R5. Path resolution is relative to containing file's directory
- R6. Per-file condition scoping: conditions evaluated per-file before splicing
- R7. Included content inserted with block-level separation, inherits variable context
- R8. Maximum include depth recommendation
- R9. Tri-state condition model (Visible/Hidden/Unset)
- R10. Operator precedence: NOT > AND > OR
- R11. Condition blocks cannot span include boundaries
- R12. Variable input model: key-value map at build time
- R13. Undefined variables pass through with warning
- R14. Two escaping mechanisms: backslash and inline code spans
- R15. Variable values can contain Markdown syntax, not condition syntax
- R16. Extension extraction during parsing with attachment rule cross-reference
- R17. Combined command evaluation order: style, multiline, marker(s), alias
- R18. Abstract output model: CommonMark tree + metadata
- R19. Fatal errors vs. recoverable warnings
- R20. MDPP diagnostic codes for processing errors
- R21. Processors should collect all diagnostics rather than halting on first error
- R22. Conformance definition: required vs. optional features
- R23. Test suite reference for conformance verification

## Scope Boundaries

- **In scope**: Processing phases, evaluation order, extension semantics, error model, conformance definition, MDPP code registry extension
- **In scope**: Formalizing the ePublisher processing model as normative
- **Out of scope**: Prescribing how variable maps or condition sets are configured (CLI, config files, etc.)
- **Out of scope**: Defining a specific output format (HTML, PDF, XML)
- **Out of scope**: Modifying the syntax reference -- the processing model references existing syntax
- **Out of scope**: Building a reference implementation or test suite (follow-up work)
- **Out of scope**: Defining a formal grammar (BNF/PEG)

## Context & Research

### Relevant Code and Patterns

- **`spec/attachment-rule.md`** -- Established pattern for spec documents: YAML frontmatter (`date`, `status`), RFC 2119 language (MUST/SHOULD/MAY), markdown tables for structured rules, numbered formal statements, edge case sections with wrong/right code examples, cross-references to validation codes. The processing model should follow this exact pattern.
- **`spec/whitepaper.md`** -- Draft whitepaper describing the format's design philosophy and capabilities. Uses `date`/`status` frontmatter.
- **`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`** -- Comprehensive syntax reference with all seven extension types. The processing model must be consistent with this document's rules.
- **`plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`** -- Validation script with existing MDPP codes 000-009. New processing-phase codes extend this registry.

### Existing MDPP Diagnostic Codes (from validate-mdpp.py)

| Code | Description | Severity |
|------|-------------|----------|
| MDPP000 | File not found / cannot read | Error |
| MDPP001 | Unclosed/unmatched condition block | Error |
| MDPP002 | Invalid name (variable, style, alias, marker key) | Error |
| MDPP003 | Malformed marker JSON | Error |
| MDPP004 | Invalid style placement (reserved) | Warning |
| MDPP005 | Circular include (reserved) | Error |
| MDPP006 | Missing include file | Warning |
| MDPP007 | Invalid condition syntax | Error |
| MDPP008 | Duplicate alias within file | Error |
| MDPP009 | Orphaned comment tag | Warning |

### Institutional Learnings

- **Attachment rule formal spec** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Established the pattern for moving scattered implementation details into a single authoritative spec document. Key lesson: enumerate all edge cases before writing, cross-reference from existing docs, align validation codes with user-facing spec.
- **Variable escaping mechanism** (`docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md`): Formalized the two escaping mechanisms and their processing order. The processing model must reference this established behavior.

## Key Technical Decisions

- **Document follows `spec/attachment-rule.md` conventions**: Same frontmatter format (`date`/`status`), RFC 2119 language, edge case examples with code blocks, cross-references to validation codes. Rationale: consistency within the `spec/` directory.
- **Recommended max include depth of 10**: Accommodates practical nested structures (book > chapter > section > shared content) with headroom. Implementations MAY impose their own limit. Rationale: prevents resource exhaustion while allowing reasonable nesting.
- **New MDPP codes start at MDPP010**: Extends the existing registry without gaps. Processing-phase diagnostics are MDPP010-MDPP013 initially, with room for expansion. Rationale: continuity with existing validation codes.
- **Required vs. optional features**: Core seven extensions (variables, conditions, styles, includes, markers, aliases, multiline tables) are required for conformance. Combined commands and max depth enforcement are optional. Rationale: multiline tables are already part of the core extension set; combined commands are syntactic sugar.
- **Single document, not multiple**: The processing model is one file (`spec/processing-model.md`), not split across multiple spec files. Rationale: the pipeline is inherently sequential and cross-referencing between phases is frequent; splitting would fragment the narrative.

## Open Questions

### Resolved During Planning

- **Maximum include depth**: RECOMMENDED 10. Implementations MAY impose their own limit. (Affects R8)
- **New MDPP codes**: MDPP010 (undefined variable), MDPP011 (max include depth exceeded), MDPP012 (cross-file condition span), MDPP013 (include cycle detected at processing time). Existing MDPP005 is reserved for static analysis; MDPP013 covers runtime detection. (Affects R20)
- **Required vs. optional features for conformance**: All seven extension types are required. Combined commands and max depth enforcement are optional. (Affects R22)
- **Test suite format**: Deferred to follow-up work item. The conformance section references the concept without prescribing format. (Affects R23)

### Deferred to Implementation

- Exact wording of RFC 2119 conformance statements -- the spec writer should use MUST/SHOULD/MAY consistently but the precise phrasing is an authoring decision
- Whether to include a summary table or flowchart for the pipeline overview -- depends on document length and readability
- Exact structure of the MDPP code registry table -- may evolve as codes are written

## Implementation Units

- [ ] **Unit 1: Document skeleton with frontmatter, introduction, and definitions**

**Goal:** Create `spec/processing-model.md` with the document structure, introduction explaining purpose and scope, and a definitions section establishing terminology used throughout.

**Requirements:** R1 (pipeline overview)

**Dependencies:** None

**Files:**
- Create: `spec/processing-model.md`

**Approach:**
- YAML frontmatter: `date: 2026-04-08`, `status: draft`
- Introduction: why this spec exists, relationship to syntax reference and attachment rule
- Definitions section: document, processor, variable map, condition set, condition state (Visible/Hidden/Unset), attachment, conformance levels (MUST/SHOULD/MAY per RFC 2119)
- Pipeline overview paragraph describing the two-phase architecture at a high level before detailed sections

**Patterns to follow:**
- `spec/attachment-rule.md` for frontmatter format, heading structure, and RFC 2119 language
- Whitepaper's explanatory prose style for the introduction

**Test scenarios:**
- Document renders cleanly as standard Markdown (no broken formatting)
- Terminology definitions are unambiguous and cover all terms used later in the spec

**Verification:**
- File exists at `spec/processing-model.md` with correct frontmatter
- All terms referenced in later units are defined in this section

---

- [ ] **Unit 2: Phase 1 specification -- include expansion with per-file condition evaluation**

**Goal:** Write the Phase 1, Step 1 section covering include expansion, per-file condition evaluation during include processing, cycle detection, path resolution, and depth limits.

**Requirements:** R2, R4, R5, R6, R7, R8, R9, R10, R11

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Section 3.1: Include Expansion
  - Depth-first recursive algorithm description
  - Path resolution: relative to containing file's directory
  - Per-file condition evaluation: each included file's conditions are evaluated *before* its content is spliced into the parent
  - Block-level separation: included content surrounded by blank lines
  - Variable context inheritance: included files share the parent's variable map
  - Cycle detection: processor tracks the include chain and skips circular references with MDPP013 warning
  - Depth limit: RECOMMENDED max of 10, implementations MAY impose their own
  - Error recovery: missing files produce MDPP006 warning, include tag passes through
- Section 3.1.1: Per-File Condition Evaluation
  - Tri-state model: Visible, Hidden, Unset (always renders)
  - Operator precedence: NOT > AND (space) > OR (comma)
  - Condition blocks must open and close within the same file
  - Cross-file spans are a fatal error (MDPP012)
  - Nested conditions are supported within a single file
- Edge cases with code examples:
  - Include of file with conditions
  - Conditional include (condition wrapping an include tag)
  - Nested includes with relative path resolution
  - Circular include detection

**Patterns to follow:**
- `spec/attachment-rule.md` edge case format (numbered subsections, wrong/right code blocks)
- Condition expression syntax from `syntax-reference.md` Conditions section
- Include processing rules from `syntax-reference.md` File Includes section

**Test scenarios:**
- Depth-first include order: A includes B and C, B includes D -- processing order is A, B, D, C
- Per-file condition scoping: included file's false condition removes content before splicing
- Circular include: A includes B, B includes A -- second include is skipped with warning
- Missing include: tag passes through as HTML comment
- Condition across include boundary: opening in parent, closing in included file -- MDPP012 error

**Verification:**
- All include and condition requirements (R4-R11) are covered with normative MUST/SHOULD/MAY statements
- Edge cases have code examples showing correct behavior
- Cross-reference to syntax-reference.md include and condition sections

---

- [ ] **Unit 3: Phase 1 specification -- variable substitution**

**Goal:** Write Phase 1, Step 2 covering variable resolution, escaping, undefined behavior, and the critical ordering implications.

**Requirements:** R2, R3, R12, R13, R14, R15

**Dependencies:** Unit 2

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Section 3.2: Variable Substitution
  - Input model: key-value map provided at build time, source is implementation-defined
  - Processing order: runs after include expansion and condition evaluation
  - Scanning: regex-based substitution of `$name;` tokens in the resolved text
  - Escaping: backslash (`\$name;`) resolved before variable scanning; inline code spans excluded from scanning
  - Undefined variables: token passes through as literal text with MDPP010 warning
  - Critical ordering implications (explicit normative statements):
    - Variables inside false condition blocks are never resolved (removed before variable substitution)
    - Variable values cannot contain condition syntax (conditions already resolved)
    - Variable values can contain Markdown syntax (substituted before Markdown parsing)
  - Case sensitivity: `$Product;` and `$product;` are distinct references

**Patterns to follow:**
- Variable escaping documentation from `syntax-reference.md` and `variable-escaping-mechanism-2026-04-06.md`
- Variable naming rules from `syntax-reference.md` Naming Rules section

**Test scenarios:**
- Variable in false condition block: condition removes the block, variable is never scanned
- Escaped variable: `\$name;` becomes literal `$name;` in output
- Variable in inline code: `` `$name;` `` passes through without substitution
- Undefined variable: `$unknown;` remains as literal text, MDPP010 warning emitted
- Variable value containing Markdown: value `**bold**` is substituted, then parsed as Markdown in Phase 2

**Verification:**
- All variable requirements (R12-R15) are covered with normative statements
- Ordering implications from R3 are stated explicitly as normative rules
- Cross-reference to syntax-reference.md variable section

---

- [ ] **Unit 4: Phase 2 specification -- Markdown parsing, extension extraction, and output model**

**Goal:** Write the Phase 2 section covering Markdown parsing with extension-aware grammars, the attachment rule cross-reference, combined command evaluation order, and the abstract output model.

**Requirements:** R16, R17, R18

**Dependencies:** Unit 3

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Section 3.3: Markdown Parsing with Extension Extraction
  - Input: the fully resolved text from Phase 1 (includes expanded, conditions evaluated, variables substituted)
  - Parsing: CommonMark 0.30 compliant parser extended with Markdown++ grammars
  - Comment disambiguation: recognized vs. unrecognized comments (cross-reference to syntax-reference.md)
  - Extension extraction: style, alias, marker, and multiline commands extracted from recognized HTML comments during parsing
  - Attachment resolution: cross-reference to `spec/attachment-rule.md` for tag-to-element binding rules
  - Combined command evaluation order: style first, then multiline, then marker(s), then alias
  - Orphaned tag handling: tags that fail attachment produce MDPP009 warning
- Section 4: Output Model
  - Abstract definition: a CommonMark document tree annotated with Markdown++ metadata
  - Metadata types: style associations, alias anchors, marker key-value pairs, multiline table structure
  - Implementation-agnostic: the spec does not prescribe HTML, PDF, or XML output
  - Determinism guarantee: same input document + variable map + condition set = same output tree

**Patterns to follow:**
- `spec/attachment-rule.md` for the cross-reference pattern (how that document is referenced)
- Combined command order from `syntax-reference.md` Combined Commands section
- Comment disambiguation from `syntax-reference.md`

**Test scenarios:**
- Style tag attached to heading: style metadata appears on the heading node in the output tree
- Combined command: `<!-- style:A ; marker:B="c" ; #d -->` -- all three directives apply to the target element in the specified order
- Orphaned tag: style tag with blank line below -- MDPP009 warning, tag has no effect
- Regular HTML comment: `<!-- TODO -->` -- ignored entirely, not treated as directive
- Determinism: processing the same document twice with the same inputs produces identical output

**Verification:**
- Phase 2 requirements (R16-R18) covered with normative statements
- Cross-references to attachment-rule.md and syntax-reference.md are correct relative paths
- Output model is implementation-agnostic

---

- [ ] **Unit 5: Error handling, conformance, and document finalization**

**Goal:** Write the error handling section with MDPP diagnostic codes, the conformance section with required/optional feature definitions, and add cross-references and a summary table.

**Requirements:** R19, R20, R21, R22, R23

**Dependencies:** Unit 4

**Files:**
- Modify: `spec/processing-model.md`

**Approach:**
- Section 5: Error Handling
  - Fatal errors: processing cannot continue (e.g., malformed syntax that prevents parsing)
  - Recoverable warnings: processing continues with degraded output (e.g., missing include, undefined variable)
  - Diagnostic collection: processors SHOULD collect all diagnostics rather than halting on first error (R21)
  - MDPP code registry: table extending MDPP000-009 with new processing-phase codes:
    - MDPP010: Undefined variable reference (Warning)
    - MDPP011: Maximum include depth exceeded (Error)
    - MDPP012: Cross-file condition span (Error)
    - MDPP013: Include cycle detected during processing (Error)
  - Error reporting: processors MUST include file path, line number, and MDPP code in diagnostics
- Section 6: Conformance
  - Required features: all seven extension types (variables, conditions, styles, includes, markers, aliases, multiline tables)
  - Optional features: combined commands (semicolon syntax), maximum include depth enforcement
  - Conformance statement: a conformant processor MUST implement all required features and MUST handle all MDPP diagnostic codes defined in this spec
  - Test suite: reference concept for verification, defer format to follow-up work
- Final pass:
  - Add summary pipeline table/diagram at the top of Section 3 showing the flow
  - Ensure all cross-references use correct relative paths
  - Verify consistency with syntax-reference.md and attachment-rule.md

**Patterns to follow:**
- MDPP code table format from `syntax-reference.md` Validation Checks section
- `spec/attachment-rule.md` Validation section for cross-referencing MDPP codes

**Test scenarios:**
- All existing MDPP codes (000-009) are listed accurately
- New codes (010-013) have clear descriptions, severities, and triggering conditions
- Conformance requirements are testable: an implementor can determine pass/fail
- Fatal vs. warning classification is consistent across all codes

**Verification:**
- All error handling and conformance requirements (R19-R23) covered
- MDPP code table is complete and consistent with existing validate-mdpp.py codes
- Document is internally consistent: no section references an undefined term or missing section
- Cross-references to syntax-reference.md and attachment-rule.md resolve correctly

## System-Wide Impact

- **Interaction graph:** The processing model cross-references `spec/attachment-rule.md` and `syntax-reference.md`. No modifications to those documents are required -- the processing model references them as authoritative sources for attachment semantics and syntax definitions respectively.
- **Error propagation:** New MDPP codes (010-013) extend the existing registry. The `validate-mdpp.py` script currently implements static analysis (MDPP000-009); the processing-phase codes defined here are for runtime processing, not static validation. A future work item may add processing-phase diagnostics to the validation tool.
- **API surface parity:** The MDPP code registry table in the processing model must remain consistent with the table in `syntax-reference.md`. If codes are added, both tables need to reflect the same set.
- **Integration coverage:** The processing model's correctness can only be fully verified by a conformance test suite (deferred to follow-up). During authoring, manual verification against the ePublisher implementation's known behavior serves as the validation mechanism.

## Risks & Dependencies

- **Consistency risk**: The processing model must not contradict the syntax reference or attachment rule. Mitigation: Unit 5 includes an explicit cross-reference verification pass.
- **Completeness risk**: The ePublisher implementation may have undocumented edge cases not captured in the issue description or requirements. Mitigation: the spec uses RFC 2119 language to distinguish required behavior from implementation-defined behavior, giving room for future amendments.
- **Adoption risk**: A spec that is too prescriptive may be difficult for alternative implementations. Mitigation: the output model is abstract (CommonMark tree + metadata), and the input model (variable map, condition set) is deliberately implementation-agnostic.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-processing-model-requirements.md](../brainstorms/2026-04-08-processing-model-requirements.md)
- Related spec: [spec/attachment-rule.md](../../spec/attachment-rule.md)
- Related reference: [syntax-reference.md](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md)
- Related solution: [docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md](../solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md)
- Related solution: [docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md](../solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md)
- Validation script: [validate-mdpp.py](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py)
- Related issue: [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Processing model specification
- Related issue: [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Formal Markdown++ specification
- Related issue: [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) -- Standalone error code reference
