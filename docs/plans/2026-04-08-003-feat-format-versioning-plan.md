---
title: "feat: Add format versioning mechanism to Markdown++ specification"
type: feat
status: active
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-format-versioning-requirements.md
---

# feat: Add format versioning mechanism to Markdown++ specification

## Overview

Create `spec/versioning.md` -- the normative specification for how Markdown++ documents declare their target spec version and how processors handle version mismatches. This adds a YAML frontmatter field (`mdpp-version: MAJOR.MINOR`), defines same-major and cross-major compatibility rules, registers version-related MDPP diagnostic codes, and establishes `1.0` as the initial spec version. Supporting updates propagate the versioning mechanism into the formal grammar (scope note), processing model (preamble phase and diagnostic codes), syntax reference, whitepaper, and examples.

## Problem Frame

Markdown++ has no document-level version identifier. Documents cannot declare which spec version they target, and processors have no mechanism to detect version mismatches. This creates forward compatibility risk (new extensions silently fail as invisible HTML comments), an enterprise adoption barrier (no contract between document and processor), and tooling interoperability gaps (no capability negotiation). Mature formats solve this: CommonMark (0.30), DITA (`@ditaversion`), DocBook (`version` attributes).

GOVERNANCE.md already defines SemVer for the spec and backward compatibility guarantees, but no spec document codifies these rules or provides the document-level declaration mechanism.

(see origin: [docs/brainstorms/2026-04-08-format-versioning-requirements.md](../brainstorms/2026-04-08-format-versioning-requirements.md))

## Requirements Trace

- R1. Spec versioning scheme: SemVer (MAJOR.MINOR.PATCH) codified in the spec itself
- R2. Document-level version declaration via YAML frontmatter field `mdpp-version: MAJOR.MINOR`
- R3. Version declaration is optional; omission is not an error
- R4. `mdpp-version` is the only spec-defined frontmatter field (frontmatter is not a third extension mechanism)
- R5. Same-major compatibility: backward compatible within major series, best-effort for newer minor versions with diagnostic
- R6. Cross-major compatibility: warning on major mismatch, processor MAY refuse
- R7. Initial spec version is `1.0`
- R8. Versioning mechanism documented in the spec itself, not only in GOVERNANCE.md

## Scope Boundaries

- **In scope**: Version declaration syntax, processor behavior for version mismatches, initial version assignment, spec document updates, MDPP diagnostic code registration, formal grammar scope note, processing model preamble, syntax reference and whitepaper updates
- **Out of scope**: Tool-specific frontmatter fields beyond `mdpp-version` (e.g., `title`, `author`, `date`)
- **Out of scope**: Version negotiation protocols between tools in a publishing pipeline
- **Out of scope**: Migration tooling for updating documents across major versions
- **Not changing**: GOVERNANCE.md versioning scheme, backward compatibility guarantees, deprecation process

## Context & Research

### Relevant Code and Patterns

- `spec/processing-model.md` -- Two-phase pipeline (Phase 1: pre-processing, Phase 2: Markdown parsing). MDPP diagnostic code registry (MDPP000-MDPP014). Conformance section with required/optional features. RFC 2119 normative language throughout.
- `spec/formal-grammar.md` -- Covers only Markdown++ extensions (inline variable tokens and HTML comment directives). Explicitly scoped; frontmatter is neither syntactic form. Conformance section lists what the grammar does and does not define.
- `spec/attachment-rule.md` -- Established pattern for standalone spec documents: introduction, scope, formal rules with RFC 2119 language, edge cases with examples, conformance, references.
- `spec/cross-file-link-resolution.md` -- Most recent spec addition. Demonstrates the pattern for extending the MDPP diagnostic registry (MDPP014) and cross-referencing other spec documents.
- `spec/whitepaper.md` -- High-level format description and rationale (~460 lines). Versioning section would be added to establish the concept before directing readers to the normative spec.
- `GOVERNANCE.md` -- Already defines SemVer for the spec (lines 47-58), backward compatibility guarantees (lines 60-63), deprecation process (lines 66-73), and relationship between spec and implementations (lines 76-82).

### Institutional Learnings

- **Processing model specification** (`docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`): MDPP diagnostic codes are registered in `spec/processing-model.md`. New codes must specify severity and triggering condition.
- **Formal grammar** (`docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md`): Grammar-first rule -- any new syntactic form needs a grammar production. However, frontmatter is not a new syntactic form, so a scope note is appropriate instead.
- **Cross-file link resolution** (`docs/solutions/documentation-gaps/cross-file-link-resolution-semantics-2026-04-08.md`): MDPP014 precedent for adding new diagnostic codes. Review caught SHOULD/MUST contradictions -- consistency of normative language is critical.
- **Document interchangeability** (`docs/solutions/documentation-gaps/document-interchangeability-messaging-2026-03-30.md`): Any new mechanism must preserve the guarantee that Markdown++ files remain valid CommonMark. YAML frontmatter is handled by most Markdown renderers (hidden or parsed), so `mdpp-version` preserves interchangeability.
- **Attachment rule** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Single source of truth pattern -- define a rule once in a spec document, have all other references point to it.

## Key Technical Decisions

- **Standalone `spec/versioning.md` over whitepaper section or processing model integration**: Each existing spec document covers one well-defined concern. Versioning is a distinct concern (declaration syntax, compatibility semantics, version lifecycle). The processing model is already ~516 lines and should only receive the preamble step and diagnostic codes. The whitepaper gets a brief versioning section that points to the normative spec.

- **Formal grammar gets a scope note, not a new production**: The grammar covers Markdown++ extension constructs (HTML comment directives and inline variable tokens). YAML frontmatter is document metadata, not an extension construct. Adding a grammar production would contradict the grammar's stated scope and blur the distinction between metadata and content extensions. The grammar's conformance section should explicitly note that frontmatter processing is outside its scope and defined in `spec/versioning.md`.

- **Add MDPP015 and MDPP016 diagnostic codes**: MDPP015 for minor version mismatch (Warning) and MDPP016 for major version mismatch (Warning). Both are warnings, not errors -- consistent with the brainstorm's R5 (best-effort processing) and R6 (processor MAY refuse but the diagnostic itself is a warning). This follows the MDPP014 precedent for extending the registry.

- **Processing model gets a "Version Check" preamble, not a new phase**: Version checking is a precondition that runs before the two-phase pipeline, not a new processing phase. It reads frontmatter, extracts `mdpp-version`, compares against the processor's supported version, and emits diagnostics. The two-phase model remains intact. This is documented as a preamble step in the processing model.

- **Two versioning tracks remain distinct**: The format spec version (`mdpp-version: 1.0`) is separate from the plugin/tooling version (`1.1.x` in plugin.json). The versioning spec must explicitly state this distinction to prevent confusion.

- **Version declaration applies to the root document only**: In a multi-file assembly (includes), only the root document's `mdpp-version` declaration is authoritative. Included files MAY contain `mdpp-version` fields, but a processor SHOULD use the root document's declaration. This avoids version conflict resolution across included files while allowing standalone files to carry their own version.

## Open Questions

### Resolved During Planning

- **Should the formal grammar include an EBNF production for `mdpp-version`?** No. Frontmatter is document metadata, not an extension construct. The grammar adds a scope note. (Rationale: grammar explicitly covers only HTML comment directives and inline variable tokens.)

- **Where should the versioning section live?** Standalone `spec/versioning.md`. (Rationale: one concern per spec document; processing model receives only the preamble step and diagnostic codes.)

- **Should the spec define MDPP diagnostic codes for version mismatches?** Yes. MDPP015 (minor version ahead, Warning) and MDPP016 (major version mismatch, Warning). (Rationale: follows MDPP014 precedent; structured diagnostics are more useful than ad-hoc messages.)

- **What happens with `mdpp-version` in included files?** Root document's declaration is authoritative. Included files' `mdpp-version` fields are informational. No conflict resolution needed -- processor uses root document's version.

### Deferred to Implementation

- **Exact EBNF-style notation for frontmatter field validation in `spec/versioning.md`**: The versioning spec will define the syntax of the `mdpp-version` field value (MAJOR.MINOR format), but the exact notation style should follow what works best in prose context rather than being pre-decided here.
- **Worked example selection**: The spec needs concrete examples (version match, minor mismatch, major mismatch, no declaration). Exact document content deferred to implementation.

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

```
Document Lifecycle with Version Check:

  ┌─────────────────────────────────────┐
  │  Input: Markdown++ Document (.md)   │
  │  ┌─────────────────────────────┐    │
  │  │ ---                         │    │
  │  │ mdpp-version: 1.0           │    │
  │  │ ---                         │    │
  │  │ # Document content...       │    │
  │  └─────────────────────────────┘    │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  Preamble: Version Check            │
  │                                     │
  │  1. Extract mdpp-version from       │
  │     root document frontmatter       │
  │  2. Parse as MAJOR.MINOR            │
  │  3. Compare against processor's     │
  │     supported spec version          │
  │  4. Emit MDPP015 or MDPP016        │
  │     if mismatch detected            │
  │  5. Continue processing             │
  │     (or refuse if cross-major       │
  │      and processor opts out)        │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  Phase 1: Pre-Processing            │
  │  (Include expansion, variable sub)  │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  Phase 2: Markdown Parsing          │
  │  (Extension extraction)             │
  └─────────────────────────────────────┘
```

**Compatibility Matrix:**

| Document Version | Processor Version | Behavior |
|-----------------|-------------------|----------|
| (none)          | any               | Process normally, no diagnostic |
| 1.0             | 1.0               | Process normally, no diagnostic |
| 1.0             | 1.2               | Process normally (backward compatible) |
| 1.2             | 1.0               | Process best-effort, emit MDPP015 |
| 2.0             | 1.x               | Emit MDPP016, MAY refuse |

## Implementation Units

- [ ] **Unit 1: Create `spec/versioning.md` -- the normative versioning specification**

  **Goal:** Define the complete versioning mechanism as a standalone spec document following established patterns.

  **Requirements:** R1, R2, R3, R4, R5, R6, R7, R8

  **Dependencies:** None

  **Files:**
  - Create: `spec/versioning.md`

  **Approach:**
  - Follow the established spec document structure: frontmatter, H1 title, introduction with scope, relationship to other spec documents, definitions, normative rules with RFC 2119 language, edge cases with worked examples, conformance section, references
  - Sections to include:
    - Introduction and scope (what this document covers, relationship to GOVERNANCE.md and other spec docs)
    - Definitions (spec version, document version declaration, processor version support)
    - Versioning scheme (SemVer MAJOR.MINOR.PATCH for the spec; MAJOR.MINOR in document declarations)
    - Document-level version declaration syntax (`mdpp-version: MAJOR.MINOR` in YAML frontmatter)
    - The "only spec-defined frontmatter field" boundary (R4)
    - Compatibility rules with numbered requirements (same-major R5, cross-major R6)
    - Multi-file assembly behavior (root document authoritative)
    - Initial version designation (1.0)
    - Worked examples: valid declaration, no declaration, minor version ahead, major version mismatch
    - CommonMark interchangeability note (YAML frontmatter is hidden or parsed by most renderers)
    - Conformance section
    - References (GOVERNANCE.md, processing-model.md, formal-grammar.md, RFC 2119)
  - Explicitly distinguish format spec version from plugin/tooling version
  - Use RFC 2119 normative language consistent with other spec documents

  **Patterns to follow:**
  - `spec/cross-file-link-resolution.md` -- most recent spec addition, same structure
  - `spec/attachment-rule.md` -- established single-concern spec pattern
  - `spec/processing-model.md` -- normative language and requirement numbering style

  **Test scenarios:**
  - Document with `mdpp-version: 1.0` and processor supporting 1.0 -- no diagnostic
  - Document with no `mdpp-version` field -- processed without error
  - Document with `mdpp-version: 1.2` and processor supporting 1.0 -- MDPP015 warning, best-effort processing
  - Document with `mdpp-version: 2.0` and processor supporting 1.x -- MDPP016 warning, processor MAY refuse
  - Multi-file assembly where root declares 1.0 and include declares 1.2 -- root version is authoritative

  **Verification:**
  - The spec document follows the established structure pattern
  - All eight requirements (R1-R8) from the brainstorm are addressed
  - RFC 2119 language is consistent (no SHOULD/MUST contradictions)
  - Cross-references to other spec documents are accurate

- [ ] **Unit 2: Update `spec/processing-model.md` -- add version check preamble and diagnostic codes**

  **Goal:** Integrate the version check step into the processing pipeline and register MDPP015/MDPP016 in the diagnostic code registry.

  **Requirements:** R5, R6, R8

  **Dependencies:** Unit 1 (versioning spec defines the rules the processing model references)

  **Files:**
  - Modify: `spec/processing-model.md`

  **Approach:**
  - Add a "Preamble: Version Check" section before "Phase 1: Pre-Processing" in the Pipeline Overview. This is not a new phase -- it is a precondition step. The two-phase model remains intact
  - The preamble describes: extract `mdpp-version` from root document frontmatter, compare against processor's supported version, emit diagnostics per `spec/versioning.md`
  - Add MDPP015 and MDPP016 to the Processing-Phase Codes table:
    - MDPP015: "Document targets newer minor version than processor supports" | Warning | Preamble | `mdpp-version` minor exceeds processor's supported minor within same major
    - MDPP016: "Document targets different major version than processor supports" | Warning | Preamble | `mdpp-version` major differs from processor's supported major
  - Update the introduction to list `spec/versioning.md` as part of the normative specification set (currently: syntax reference, processing model, attachment rule)
  - Add version checking to the Optional Features section in Conformance (since R3 makes version declarations optional, version checking should be optional for conformance but recommended)
  - Add `spec/versioning.md` to the References section

  **Patterns to follow:**
  - MDPP014 addition in the Processing-Phase Codes table -- same column structure and style
  - Existing Pipeline Overview section structure for adding the preamble

  **Test scenarios:**
  - MDPP015 code has correct severity (Warning), phase (Preamble), and triggering condition
  - MDPP016 code has correct severity (Warning), phase (Preamble), and triggering condition
  - Pipeline Overview correctly shows preamble before Phase 1
  - Introduction lists the expanded set of normative documents

  **Verification:**
  - MDPP015 and MDPP016 appear in the diagnostic code registry with correct metadata
  - The preamble step is clearly described as a precondition, not a new phase
  - The introduction reflects the updated normative document set
  - Version checking appears in Optional Features

- [ ] **Unit 3: Update `spec/formal-grammar.md` -- add frontmatter scope note**

  **Goal:** Explicitly note that YAML frontmatter processing is outside the grammar's scope, directing readers to `spec/versioning.md`.

  **Requirements:** R4, R8

  **Dependencies:** Unit 1 (versioning spec must exist to reference)

  **Files:**
  - Modify: `spec/formal-grammar.md`

  **Approach:**
  - Add a note in the Scope section (after the description of the two syntactic forms) stating that YAML frontmatter, including the `mdpp-version` field, is document metadata outside the scope of this grammar. Reference `spec/versioning.md` for frontmatter processing rules
  - Add a corresponding note in the Conformance section under "The grammar does not define" list, noting that frontmatter processing is defined in `spec/versioning.md`
  - Add `spec/versioning.md` to the References section

  **Patterns to follow:**
  - Existing scope exclusions in the grammar (e.g., "does not re-specify CommonMark 0.30")
  - The "does not define" list in the Conformance section

  **Test scenarios:**
  - Scope section clearly states frontmatter is outside the grammar
  - Conformance section lists frontmatter as out of scope with reference
  - Cross-reference to `spec/versioning.md` is accurate

  **Verification:**
  - The grammar document does not introduce any new productions for frontmatter
  - Readers are directed to the correct spec document for frontmatter rules

- [ ] **Unit 4: Update `spec/whitepaper.md` -- add versioning section**

  **Goal:** Introduce the versioning concept in the whitepaper with a brief section that directs readers to the normative spec.

  **Requirements:** R8

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `spec/whitepaper.md`

  **Approach:**
  - Add a "Format Versioning" section to the whitepaper in an appropriate location (likely after the format description sections and before or near the governance references)
  - Keep it brief -- the whitepaper explains rationale and concepts, not normative rules. Cover: why versioning matters, what `mdpp-version` does, how compatibility works at a high level, and direct readers to `spec/versioning.md` for the full specification
  - Mention the distinction between spec version and tooling version
  - Reference GOVERNANCE.md for the versioning scheme and deprecation process

  **Patterns to follow:**
  - Existing whitepaper sections that introduce concepts and point to normative specs
  - The whitepaper's tone (explanatory, not normative)

  **Test scenarios:**
  - Section explains the "why" of versioning without duplicating normative rules
  - Cross-references to `spec/versioning.md` and GOVERNANCE.md are present

  **Verification:**
  - Whitepaper readers understand the versioning concept and know where to find the details
  - No normative language (MUST/SHOULD/MAY) appears in the whitepaper versioning section

- [ ] **Unit 5: Update syntax reference and examples**

  **Goal:** Document the `mdpp-version` frontmatter field in the syntax reference and add version declarations to example files.

  **Requirements:** R2, R7, R8

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
  - Modify: example files in `examples/` (add `mdpp-version: 1.0` to frontmatter)

  **Approach:**
  - Add a "Version Declaration" section to the syntax reference explaining the `mdpp-version` frontmatter field, its syntax, and its purpose. Reference `spec/versioning.md` for the normative rules
  - Update example files to include `mdpp-version: 1.0` in their YAML frontmatter, demonstrating the field in practice. This is optional per R3 but shows best practice for formal documents
  - Keep example updates minimal -- add the field to existing frontmatter blocks

  **Patterns to follow:**
  - Existing syntax reference sections for other features
  - Existing example file frontmatter format (`date`, `status`)

  **Test scenarios:**
  - Syntax reference explains the field clearly with a usage example
  - Example files have valid `mdpp-version: 1.0` fields
  - Example files remain valid CommonMark with the added field

  **Verification:**
  - A reader can learn how to use `mdpp-version` from the syntax reference alone
  - Example files demonstrate the versioning feature

- [ ] **Unit 6: Update GOVERNANCE.md and CHANGELOG.md -- cross-references and release notes**

  **Goal:** Add cross-reference from GOVERNANCE.md to the new versioning spec, and add the changelog entry.

  **Requirements:** R1, R8

  **Dependencies:** Units 1-5

  **Files:**
  - Modify: `GOVERNANCE.md`
  - Modify: `CHANGELOG.md`

  **Approach:**
  - In GOVERNANCE.md, add a cross-reference in the "Spec versioning" section pointing to `spec/versioning.md` as the normative specification for the versioning mechanism. The governance document defines the process; the spec defines the technical mechanism
  - In CHANGELOG.md, add an entry under `[Unreleased] > Spec` for the versioning mechanism addition
  - Ensure the two versioning tracks (spec version vs. plugin version) are clear in both documents

  **Patterns to follow:**
  - Existing cross-references between GOVERNANCE.md and spec documents
  - CHANGELOG.md entry format (Keep a Changelog style with Spec/Tooling/Project categories)

  **Test scenarios:**
  - GOVERNANCE.md links to `spec/versioning.md`
  - CHANGELOG.md entry accurately describes the addition

  **Verification:**
  - A reader of GOVERNANCE.md can find the normative versioning spec
  - The changelog reflects the new spec addition

## System-Wide Impact

- **Interaction graph:** Version checking is a preamble step that runs before the existing two-phase pipeline. It does not interact with include expansion, variable substitution, or extension extraction -- it only reads frontmatter and emits diagnostics. The processing model's introduction must be updated to include `spec/versioning.md` in the normative document set.
- **Error propagation:** MDPP015 and MDPP016 are both warnings (recoverable). Processing continues after either diagnostic. A processor MAY choose to refuse processing on MDPP016 (cross-major), but this is processor-specific behavior, not a specification requirement.
- **State lifecycle risks:** None. Version checking reads metadata once before processing begins. No state is mutated.
- **API surface parity:** The `mdpp-version` field is the only new surface. It is optional (R3), so existing documents and tools are unaffected.
- **Multi-file assembly:** Root document's `mdpp-version` is authoritative. Included files' version declarations are informational only. No version conflict resolution is needed.
- **CommonMark interchangeability:** YAML frontmatter is handled by most Markdown renderers (hidden or parsed). The `mdpp-version` field preserves the interchangeability guarantee.

## Risks & Dependencies

- **Risk: Confusion between spec version and plugin version.** Mitigation: The versioning spec explicitly states the distinction. The whitepaper section reinforces it. Example files and syntax reference demonstrate spec version usage.
- **Risk: Scope creep into general frontmatter specification.** Mitigation: R4 explicitly limits the spec to defining only `mdpp-version`. The versioning spec states this boundary clearly.
- **Dependency: GOVERNANCE.md versioning scheme.** The versioning spec codifies decisions already made in GOVERNANCE.md. If governance changes, the spec must be updated. This is a feature, not a risk -- it creates a single source of truth for the technical mechanism.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-format-versioning-requirements.md](../brainstorms/2026-04-08-format-versioning-requirements.md)
- Related spec: `spec/processing-model.md` (diagnostic codes, pipeline)
- Related spec: `spec/formal-grammar.md` (scope note)
- Related spec: `spec/cross-file-link-resolution.md` (MDPP014 precedent)
- Related spec: `spec/whitepaper.md` (rationale section)
- Related: `GOVERNANCE.md` (versioning scheme, compatibility guarantees)
- Related issue: #7 (formal specification)
- Related issue: #25 (this issue)
- External: [Semantic Versioning 2.0.0](https://semver.org/)
- External: [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt)
- External: [CommonMark 0.30](https://spec.commonmark.org/0.30/)
