---
title: Multiline table cell extensions -- normative rules for extension behavior in cells
date: 2026-04-08
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - No spec text addressed which Markdown++ extensions are valid inside multiline table cells
  - Authors had no authoritative reference for using extensions in cells
  - Implementors had no basis for consistent cross-processor behavior
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - multiline-tables
  - table-cells
  - extensions
  - processing-model
  - phase-ordering
  - attachment-rule
---

# Multiline Table Cell Extensions -- Normative Rules for Extension Behavior in Cells

## Problem

The Markdown++ specification defined multiline table cells but did not specify which extensions are valid within them, how they interact with the table context, or what restrictions apply. Since the ePublisher parser creates a temporary WifMarkdown instance per cell (making each cell a full Markdown document), any extension could theoretically appear inside a cell -- but authors and implementors had no normative guidance.

## Symptoms

- No spec text addressed variables, conditions, includes, nested tables, headings, aliases, markers, block styles, inline styles, or combined commands in the context of multiline table cells.
- Authors attempting to use these features had no authoritative reference for correct usage patterns.
- Implementors had no basis for consistent behavior across processors -- whether an extension should work in a cell was left to implementation discretion.

## What Didn't Work

The approach was largely straightforward, with one course correction: nested tables and includes were initially left as open questions during requirements gathering (R3 as "not recommended," R8 as "SHOULD be strongly discouraged"). Maintainer feedback from mcdow-webworks clarified both are explicitly unsupported and must be MUST NOT. This avoided speccing behavior the implementation cannot support. Lesson: gather maintainer input on implementation constraints during requirements, not after drafting.

## Solution

Created `spec/multiline-cell-extensions.md`, a normative specification organized around the processing model's two-phase pipeline, with three-tier categorization (supported / valid-but-not-recommended / not supported):

**Phase 1 extensions** (operate on raw text before table parsing):
- **Variables**: MUST resolve identically -- tokens are replaced before Phase 2 sees the table
- **Conditions**: Must wrap complete logical rows (first row + all continuation rows + separator); partial row wrapping produces undefined structure
- **Includes**: MUST NOT appear inside cell content -- expanded content will not maintain pipe-delimited syntax

**Phase 2 extensions** (operate during per-cell Markdown parsing):
- **Block styles**: MUST apply identically -- directive on continuation row attaches to following content per the attachment rule
- **Inline styles**: MUST apply identically -- standard inline attachment rule applies
- **Aliases**: SHOULD NOT -- don't participate in document navigation usefully; use table-level aliases via combined commands instead
- **Markers**: MUST recognize -- valid use case for attaching metadata to block elements within cells
- **Nested multiline tables**: MUST NOT -- pipe delimiter conflicts make syntax nearly impossible to parse
- **Combined commands**: MUST evaluate in same fixed order as outside cells

**Standard Markdown**:
- Block and inline elements (paragraphs, lists, blockquotes, inline formatting) work normally
- Headings: SHOULD use bold text or styled paragraphs instead (headings don't contribute to document outline from inside a cell)
- Fenced code blocks: Valid but can be tricky due to pipe-delimiter constraints

**Edge cases documented**: empty cells, single vs. multiple continuation rows, styles with lists, conditions wrapping entire tables.

Cross-reference added to `spec/processing-model.md` Phase 2 section pointing to the new document.

## Why This Works

The phase-ordering principle from the processing model is the organizing key. Phase 1 extensions operate on raw text before table structure is parsed -- they have no awareness of being inside a table. Phase 2 extensions operate in the per-cell parsing context via the WifMarkdown instance. Every extension's behavior in cells follows directly from which phase processes it, giving a principled answer to each case rather than requiring ad hoc rules per extension.

This framework also makes the spec self-maintaining: when new extensions are added, their cell behavior can be derived by asking "which phase processes this extension?"

## Prevention

- When adding a new structural feature to the spec (tables, includes, conditional blocks), immediately audit how existing extensions interact with it and create a companion normative document if the interaction surface is non-trivial.
- Consult the processing model's phase ordering first -- it often resolves ambiguous interaction cases without requiring implementation research.
- Gather maintainer input on implementation constraints during requirements gathering, not after drafting, to avoid speccing unsupported behavior.
- Use the three-tier categorization (supported / valid-but-not-recommended / not supported) to clearly communicate implementation expectations.

## Related Issues

- [#24](https://github.com/quadralay/markdown-plus-plus/issues/24) -- Document which extensions work inside multiline table cells (this issue)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Processing model (phase ordering determines what works in cells)
- [#20](https://github.com/quadralay/markdown-plus-plus/issues/20) -- Multiline table row separators (sibling spec gap)
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Element interactions
- [#12](https://github.com/quadralay/markdown-plus-plus/issues/12) -- Graceful degradation (should incorporate cell-specific constraints from this work)
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` -- Parent learning (general processing model spec)
- `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md` -- Related learning (attachment rule referenced by cell extension spec)
