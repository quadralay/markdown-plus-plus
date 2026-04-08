---
title: Cross-file link reference resolution semantics
date: 2026-04-08
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - No specification for how link reference definitions resolve across included files
  - Ambiguity around scope visibility (parent, sibling, descendant files)
  - No defined conflict resolution rule for duplicate slugs across files
  - Unclear whether resolution is per-file or document-global after assembly
  - Implementors must reverse-engineer cross-file behavior from ePublisher parser code
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
tags:
  - cross-file-resolution
  - link-references
  - specification
  - includes
  - processing-model
---

# Cross-file link reference resolution semantics

## Problem

Markdown++ enables multi-file document assembly through `<!-- include: -->` directives and provides a semantic cross-reference pattern using CommonMark link reference definitions bridged to alias IDs. The whitepaper says "the publishing tool resolves `[getting-started]` across all included files" but does not define the resolution algorithm. Four questions were unanswered:

1. **Scope visibility**: Are link reference definitions in an included file visible to the parent document? To sibling includes?
2. **Conflict resolution**: What happens when two included files define the same slug with different target IDs?
3. **Include order**: Does the order of includes affect resolution priority?
4. **Assembled vs. per-file**: Are link references resolved within each file individually or after the full document is assembled?

## Symptoms

- Implementors building new Markdown++ processors had no normative reference for cross-file link reference behavior
- The ePublisher parser's `WifMarkdown` instance inheritance of link definitions was implementation behavior, not specification
- Authors could not predict resolution outcomes in multi-file assemblies without testing
- No diagnostic was defined for the common mistake of duplicate slugs across files

## What Didn't Work

- **Whitepaper language** described the feature at a high level ("resolves across all included files") but didn't define the algorithm
- **Example files** showed cross-references working but didn't clarify edge cases or conflict behavior
- **Source code inspection** revealed that the ePublisher parser shares link definitions at document scope, but this was implementation detail, not specification

## Solution

Created `spec/cross-file-link-resolution.md` — a normative specification defining cross-file link reference resolution as a direct consequence of the existing two-phase processing model.

**Key decisions:**

- **Document-global scope**: Link references resolve on the assembled document, not per-file. By Phase 2, the assembled document is a single text with no file boundaries. This is not a new rule — it follows directly from the processing model's two-phase architecture.

- **First-definition-wins**: Follows CommonMark 0.30 section 4.7 semantics. The definition that appears first in assembled document order (determined by depth-first include expansion) takes precedence. This gives authors deterministic control through include ordering.

- **MDPP014 diagnostic**: A new warning-level diagnostic for duplicate link reference slugs originating from different source files. Warning, not error — the first-definition-wins rule ensures deterministic output even with duplicates.

- **Full interaction documentation**: Specified how conditions gate link reference definitions, how variables substitute in definitions, and how the semantic cross-reference pattern (combined command + heading + link reference definition) works across files.

**Deliverables:**

1. `spec/cross-file-link-resolution.md` — normative spec with resolution scope, conflict rules, MDPP014 definition, interaction with conditions/variables, two worked examples, and four edge cases
2. MDPP014 registered in `spec/processing-model.md` diagnostic code registry
3. `plugins/.../references/syntax-reference.md` — expanded note on cross-file visibility with spec cross-reference
4. `plugins/.../references/best-practices.md` — new cross-file cross-reference example in the Link References section

## Why This Works

The key insight is that cross-file link reference resolution is not a separate feature — it is a direct consequence of the two-phase processing model. Phase 1 assembles all includes into a single text. Phase 2 parses that text as CommonMark 0.30, which collects link reference definitions at document scope. The "cross-file" behavior is entirely a Phase 1 artifact. By Phase 2, the parser sees one document.

Formalizing this as a standalone spec (rather than appending to the processing model) keeps each spec document focused on one concern while making the derived behavior explicit. The spec answers all four open questions with normative language and concrete examples.

## Prevention

- **Specify derived behaviors explicitly**: When a feature's behavior follows from an underlying model (as cross-file resolution follows from two-phase processing), the derived behavior should still be explicitly specified. Correct behavior that is "obvious" to the spec author is not obvious to implementors.
- **Define diagnostics for common mistakes**: Cross-file duplicate slugs are an authoring mistake that is easy to make and hard to debug. MDPP014 catches this at build time.
- **Use worked examples as conformance inputs**: The two examples in the spec serve double duty — they explain the feature to readers and provide test inputs for implementors.

## Related Issues

- [#22](https://github.com/quadralay/markdown-plus-plus/issues/22) — Define cross-file link reference resolution semantics (this issue)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) — Processing model specification (dependency — defines the two-phase pipeline)
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) — Element interactions (cross-reference behavior)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) — Formal specification (cross-referencing is a major spec section)
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` — Related specification pattern
