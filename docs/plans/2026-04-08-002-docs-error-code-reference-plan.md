---
title: "docs: Add standalone error code reference for MDPP000-MDPP009"
type: feat
status: completed
date: 2026-04-08
---

# docs: Add standalone error code reference for MDPP000-MDPP009

## Overview

Create a standalone, implementation-independent error code reference document for Markdown++ validation codes MDPP000 through MDPP009. This enables alternative validator implementations without reverse-engineering `validate-mdpp.py`, and gives authors a single place to look up error meanings, triggers, and fixes.

## Problem Frame

Error codes MDPP001-MDPP009 are defined only in `validate-mdpp.py` and summarized briefly in `syntax-reference.md`. There is no standalone reference that a third-party validator author could use as a specification. The processing model (`spec/processing-model.md`) establishes the diagnostic code registry but defers static validation code details to the plugin references layer.

## Requirements Trace

- R1. Standalone error code reference document at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
- R2. Quick-reference summary table for all ten codes (MDPP000-MDPP009)
- R3. Per-code sections with: severity, description, detection logic, trigger examples, and suggested fix
- R4. Reserved codes (MDPP004, MDPP005) documented with intended detection logic
- R5. Unified naming rule documented as shared grammar for MDPP002
- R6. General rule: all checks skip fenced code blocks
- R7. Cross-reference from `syntax-reference.md` to the new document
- R8. MDPP000 added to `syntax-reference.md` validation table (was missing)
- R9. CHANGELOG entry under `[Unreleased]`
- R10. Solution doc for institutional learning

## Scope Boundaries

- **In scope:** Static validation codes MDPP000-MDPP009 (the complete inventory from the issue)
- **In scope:** Cross-referencing between `syntax-reference.md` and the new document
- **In scope:** CHANGELOG and solution doc
- **Out of scope:** Processing-phase codes MDPP010-MDPP013 (owned by `spec/processing-model.md`)
- **Out of scope:** Test coverage gaps (separate follow-up work per issue)
- **Out of scope:** Extending MDPP002 validation in `validate-mdpp.py` to cover all name types (separate follow-up work per issue)
- **Out of scope:** Updating `validate-mdpp.py` implementation

## Context & Research

### Relevant Code and Patterns

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` -- Existing validation checks table (lines 910-926); authoritative naming rules section
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` -- Reference implementation of all eight implemented codes
- `spec/processing-model.md` -- Diagnostic code registry (lines 450-478); classifies MDPP000-009 as static validation, MDPP010+ as processing-phase
- `spec/attachment-rule.md` -- Formal spec for MDPP009 semantics (orphaned tag handling)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` -- Sibling reference doc; formatting pattern to follow
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md` -- Sibling reference doc; formatting pattern to follow

### Institutional Learnings

- **Unified naming rule** (`docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`): MDPP002 scope expanded from variable-only to all named entities. The error-codes.md must reflect the expanded scope.
- **Attachment rule formalization** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Prevention rule -- "Every validation check should have a corresponding user-facing specification." This issue directly fulfills that principle.
- **Processing model specification** (`docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`): Established the MDPP diagnostic code registry through MDPP013. Static validation codes (000-009) are delegated to the plugin reference layer.

## Key Technical Decisions

- **Document lives in plugin references, not spec/**: Static validation codes are tooling-layer concerns. The processing model delegates their detailed documentation to the plugin references. Processing-phase codes (MDPP010+) are owned by `spec/processing-model.md`.
- **Per-code section structure**: Follows the pattern `## MDPPnnn -- Name` with bold field labels (`**Severity:**`, `**Detection logic:**`, etc.) consistent with the sibling reference document style.
- **Naming rule as shared section**: Rather than repeating the regex in every code that uses it, a single `## Naming Rule` section defines the grammar once, and MDPP002/MDPP007 reference it.
- **Reserved codes get shorter entries**: MDPP004 and MDPP005 use `**Status:** Reserved` and `**Intended detection logic:**` instead of trigger examples and suggested fixes.

## Open Questions

### Resolved During Planning

- **Should MDPP010-MDPP013 be included?** No. The processing model explicitly separates static validation (000-009) from processing-phase codes (010+). The error-codes.md covers the static validation layer. Processing-phase codes are documented in `spec/processing-model.md`.
- **Should the document include test coverage status?** No. Test coverage is tracked in the issue description and is a separate follow-up concern. The reference document is implementation-independent.

### Deferred to Implementation

- None. All decisions are resolved.

## Implementation Units

- [x] **Unit 1: Create standalone error code reference**

**Goal:** Create the complete error-codes.md document with all ten codes.

**Requirements:** R1, R2, R3, R4, R5, R6

**Dependencies:** None

**Files:**
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`

**Approach:**
- YAML frontmatter with `date: 2026-04-08` and `status: active`
- Quick-reference summary table as first content after intro
- General rules section (fenced code block skipping)
- Naming rule section (shared grammar)
- One `## MDPPnnn -- Name` section per code, separated by horizontal rules
- Reserved codes (MDPP004, MDPP005) get abbreviated entries

**Patterns to follow:**
- Sibling reference docs: `syntax-reference.md`, `best-practices.md`, `examples.md`
- Em-dashes as `--` (double hyphen), not Unicode
- Fenced code blocks with language annotations

**Test scenarios:**
- Document renders correctly in GitHub markdown preview
- All ten codes (MDPP000-MDPP009) present with complete fields
- Naming rule regex matches `validate-mdpp.py` `STANDARD_NAME_RE`

**Verification:**
- File exists at the specified path with all required sections
- Quick-reference table has 10 rows
- Per-code sections cover all implemented codes with detection logic, trigger examples, and suggested fixes

**Status:** Completed in commit `f395afe`.

- [x] **Unit 2: Update syntax-reference.md cross-references**

**Goal:** Replace the self-contained validation table with a cross-reference to the new document, and add the missing MDPP000 row.

**Requirements:** R7, R8

**Dependencies:** Unit 1

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

**Approach:**
- Add descriptive text linking to `error-codes.md` for full details
- Add MDPP000 row to the validation checks table
- Keep the summary table for quick scanning but point to error-codes.md for depth

**Patterns to follow:**
- Relative link format: `[Error Code Reference](error-codes.md)`

**Test scenarios:**
- Cross-reference link resolves correctly
- MDPP000 present in the table

**Verification:**
- Line 912 contains the cross-reference text
- MDPP000 row appears in the validation checks table

**Status:** Completed in commit `f395afe`.

- [x] **Unit 3: Version bump**

**Goal:** Bump plugin version for the new reference document.

**Requirements:** Per CLAUDE.md conventions

**Dependencies:** Units 1-2

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

**Approach:**
- Patch bump (1.1.5 -> 1.1.6) since this is a documentation addition

**Verification:**
- Both files show version `1.1.6`

**Status:** Completed in commit `f395afe`.

- [x] **Unit 4: Add CHANGELOG entry**

**Goal:** Document the new error code reference in the project changelog.

**Requirements:** R9

**Dependencies:** Units 1-2

**Files:**
- Modify: `CHANGELOG.md`

**Approach:**
- Add entry under `[Unreleased]` > `Tooling` section
- Reference issue #14 in the entry
- Keep entry concise: one line describing the new document

**Patterns to follow:**
- Existing CHANGELOG entries: `- Description ([#NN](url))`

**Test scenarios:**
- Entry appears under the correct section heading

**Verification:**
- `[Unreleased]` > `Tooling` section contains the error code reference entry

- [x] **Unit 5: Write solution doc**

**Goal:** Capture institutional learning from this work for future reference.

**Requirements:** R10

**Dependencies:** Units 1-4

**Files:**
- Create: `docs/solutions/documentation-gaps/error-code-reference-2026-04-08.md`

**Approach:**
- Follow existing solution doc format with YAML frontmatter
- Document the problem (error codes only in implementation), solution (standalone reference), and prevention guidance
- Cross-reference related issues and specs
- Note that MDPP010-MDPP013 exist in the processing model for future reference expansion

**Patterns to follow:**
- Existing solution docs in `docs/solutions/documentation-gaps/`

**Test scenarios:**
- Solution doc follows the established frontmatter and section pattern

**Verification:**
- File exists with correct frontmatter
- Related issues section references #14

## System-Wide Impact

- **Interaction graph:** The new `error-codes.md` is referenced by `syntax-reference.md` (line 912). The processing model (`spec/processing-model.md`, line 452) references the syntax reference for static validation codes, creating an indirect chain: processing-model -> syntax-reference -> error-codes.
- **API surface parity:** The error-codes.md covers the same codes as `validate-mdpp.py` and the processing model registry. Any future code additions must update all three locations.
- **Documentation coverage:** This document fills the gap identified in three separate solution docs (attachment rule, unified naming rule, processing model) that all listed issue #14 as related work.

## Risks & Dependencies

- **Low risk:** The primary deliverable is already committed and reviewed. Only CHANGELOG and solution doc remain.
- **Future maintenance:** When new MDPP codes are added (e.g., implementing MDPP004 or MDPP005), `error-codes.md` must be updated to promote them from reserved to implemented status.

## Sources & References

- Related issue: [#14](https://github.com/quadralay/markdown-plus-plus/issues/14)
- Related code: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`
- Related spec: `spec/processing-model.md` (diagnostic code registry)
- Related spec: `spec/attachment-rule.md` (MDPP009 semantics)
- Solution doc: `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`
- Solution doc: `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`
- Solution doc: `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md`
