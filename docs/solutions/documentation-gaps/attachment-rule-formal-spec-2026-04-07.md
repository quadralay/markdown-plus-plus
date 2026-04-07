---
title: "Attachment rule was undocumented as a formal specification"
date: 2026-04-07
category: documentation-gaps
module: markdown-plus-plus-spec
problem_type: documentation_gap
component: documentation
symptoms:
  - "Blank line between tag and target silently breaks association with no visible error"
  - "Users encounter inconsistent fragments of the rule across multiple files"
  - "No single document covers all edge cases (stacking, end-of-file, nested indentation, condition blocks)"
  - "Validator MDPP009 enforces the rule but no user-facing spec explains what it checks"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
tags:
  - attachment-rule
  - blank-line
  - orphaned-tags
  - mdpp009
  - specification
  - comment-tags
---

# Attachment rule was undocumented as a formal specification

## Problem

The Markdown++ "attachment rule" -- that comment tags must appear on the line immediately before their target element with no intervening blank line -- was the number one source of user errors but had no single authoritative definition. The rule was scattered across six or more locations with inconsistent coverage, and a single blank line silently breaks the association with no visible error in standard Markdown preview.

## Symptoms

- Users insert a blank line between a Markdown++ comment tag and its target element, silently breaking the tag-to-element association
- The tag passes through as a regular HTML comment with no visible error -- the custom style, alias, or marker simply does nothing
- Users find fragments of the rule in different files (syntax reference, best practices, SKILL.md, validation code) that cover different subsets of scenarios
- No single document explains the complete picture including edge cases, exempt tags, and target element types
- Validator check MDPP009 enforces the rule in code but has no corresponding user-facing specification

## What Didn't Work

The attachment rule existed as an implementation detail spread across multiple files:

- `syntax-reference.md` had a summary table and two examples but did not cover all edge cases (stacking, end-of-file, nested indentation, tags inside condition blocks, multiple blank lines)
- `best-practices.md` split the rule across two separate "Common Mistakes" items (#2 for styles, #7 for orphaned aliases/markers) that each only showed one scenario
- `SKILL.md` mentioned it in a single paragraph with no examples
- `validate-mdpp.py` enforced MDPP009 but the detection logic lived only in code, not in user-facing documentation
- `tests/sample-orphaned-tags.md` had test cases but no explanatory context

No document covered which tags are exempt and why, no document explained all seven edge cases, and the inconsistency meant users encountered different fragments depending on which file they read first.

## Solution

Created a new canonical specification document (`spec/attachment-rule.md`, 200 lines) and updated all existing documentation to reference it.

The spec document contains:

1. **Core definition** -- "attached" means tag and target on immediately adjacent lines with zero blank lines
2. **Formal statement** -- four numbered rules (block above, inline before, blank breaks, downward only)
3. **Tags requiring attachment** -- table covering style, alias, marker, multiline, and combined commands
4. **Exempt tags** -- table with rationale (conditions wrap content, includes are standalone)
5. **Target element types** -- table of eight element types (heading, paragraph, lists, blockquote, code fence, table, setext heading)
6. **Seven edge cases** -- each with wrong/right code examples (stacked tags, blank line before content, tag below content, tag at end of file, nested indentation, tags inside condition blocks, multiple blank lines)
7. **Validation cross-reference** -- links to MDPP009
8. **Relationship to comment disambiguation** -- clarifies that attachment is independent of comment recognition

Three existing documents were updated to point to the spec:

- **SKILL.md** -- expanded Common Mistakes from a single paragraph to numbered items, with attachment rule as #1 including multiple wrong/right examples and a link to the spec
- **best-practices.md** -- consolidated old mistakes #2 and #7 into a single comprehensive #1 covering blank lines, ordering, stacking, and exemptions
- **syntax-reference.md** -- added a prominent callout block and additional examples for downward-only and stacking scenarios

A follow-up commit fixed relative link paths (five levels of `../` instead of four, needed because the `references/` directory adds an extra level of nesting).

## Why This Works

The root cause was inadequate documentation architecture: a critical rule governing the fundamental syntax mechanism (tag-to-element binding) existed only as scattered fragments without a single source of truth. The fix applies the documentation equivalent of "don't repeat yourself" -- one authoritative spec document owns the complete definition, and all other documents link to it rather than maintaining independent copies that inevitably diverge. The spec is comprehensive enough to cover every edge case a user might encounter, while existing documents retain enough context (examples, callout blocks) to flag the rule's importance where users are most likely to encounter it.

## Prevention

1. **Single source of truth for critical rules.** When a rule affects multiple features (styles, aliases, markers, combined commands), define it once in a spec-grade document and have all other references point to it. Do not maintain parallel descriptions.
2. **Edge case inventory before writing.** Before documenting any behavioral rule, enumerate all edge cases (stacking, ordering, boundary conditions like end-of-file, nesting, and interactions with exempt constructs). If the edge cases cannot fit in the current document's scope, create a dedicated spec.
3. **Cross-reference audit on new features.** When adding a new command type that requires attachment, update the canonical spec's "Which Tags Require Attachment" table rather than documenting the rule inline in the new feature's section.
4. **Validation alignment.** Every validation check (like MDPP009) should have a corresponding user-facing specification that the check references, so users can look up exactly what the validator is enforcing and why.

## Related Issues

- [#10](https://github.com/quadralay/markdown-plus-plus/issues/10) -- Formalize and prominently document the attachment rule (the issue this work addresses)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Write a formal Markdown++ specification (Section 4 "Attachment rules" now has a formal definition at `spec/attachment-rule.md`)
- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) -- Create a standalone error code reference for MDPP001-MDPP009 (MDPP009 semantics now formally defined)
- [#11](https://github.com/quadralay/markdown-plus-plus/issues/11) -- Create a formal grammar for Markdown++ extensions (can reference `spec/attachment-rule.md` for prose definition of attachment constraints)
