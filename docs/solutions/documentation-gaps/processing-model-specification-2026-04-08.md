---
title: Processing model specification for Markdown++ extensions
date: 2026-04-08
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - No normative reference for how conformant processors should evaluate extensions
  - Ambiguity around include recursion, cycle detection, and depth limits
  - Unclear variable resolution order when conditions and includes interact
  - No specified error classification for extension processing failures
  - Impossible to build a second conformant implementation without reverse-engineering code
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
tags:
  - processing-model
  - specification
  - conformance
  - includes
  - variables
  - conditions
  - error-handling
---

# Processing model specification for Markdown++ extensions

## Problem

Markdown++ defines syntax for seven extension types (variables, conditions, styles, includes, markers, aliases, and multiline tables), but there was no specification of how a conformant processor should evaluate them. The syntax reference described what each extension looks like but not the runtime semantics, making it impossible to build a second conformant implementation or reason about document behavior when extensions interact.

## Symptoms

- Implementors building new Markdown++ processors had no normative reference for correct behavior
- Ambiguity around include recursion, cycle detection, and depth limits
- Unclear variable resolution order when conditions and includes interact
- No specified error classification (fatal vs. recoverable) for extension processing
- Each implementation had to independently discover the correct evaluation sequence through code inspection of the ePublisher adapter

## What Didn't Work

Before this solution, understanding Markdown++ semantics required fragmented approaches:

- **Syntax references** documented what extensions look like syntactically, not how they behave at runtime
- **Example files** showed working cases but didn't clarify edge cases or interaction rules
- **Source code inspection** of the ePublisher adapter (`driver.py` → `duplicate.py` → `genxml.py`) was the only way to discover the actual processing order, but this didn't constitute a specification
- **Best practices guides** described recommendations but lacked normative RFC 2119 language backed by formal requirements
- Trial-and-error implementation was the only practical path for new implementors

## Solution

Created `spec/processing-model.md` (550 lines) — a normative two-phase processing model specification covering 23 core requirements, modeled after `spec/attachment-rule.md` conventions. The spec has grown since initial creation as subsequent issues (UTF-8 encoding, format versioning, cross-file link resolution) added sections and diagnostic codes.

**Phase 1, Step 1 — Include Expansion:**
- Depth-first recursive algorithm with cycle detection (MDPP013)
- Path resolution relative to containing file's directory
- Configurable depth limits (default 32, MDPP011)
- Per-file condition evaluation during include processing
- Tri-state condition model (Visible/Hidden/Use document value)
- Operator precedence: NOT > AND (space) > OR (comma)
- Cross-file condition span detection (MDPP012)
- Four edge cases with code examples

**Phase 1, Step 2 — Variable Substitution:**
- Input model (processor-provided key-value map)
- Four critical ordering implications:
  1. Variables in false conditions are never resolved
  2. Variable values cannot contain condition syntax
  3. Variable values can contain Markdown syntax
  4. Variable values can contain include syntax (but includes already expanded)
- Left-to-right single-pass scanning/replacement algorithm
- Two escaping mechanisms (backslash `\$name;` and code spans)
- Undefined variable handling (MDPP010)

**Phase 2 — Markdown Parsing with Extension Extraction:**
- Extension extraction from HTML comments with disambiguation rules
- Attachment rule cross-reference to `spec/attachment-rule.md`
- Combined command evaluation order (RECOMMENDED, not required): style > multiline > marker > alias
- Orphaned tag handling

**Additional sections:** Output model (abstract CommonMark tree + metadata annotations, determinism guarantee), error handling (fatal vs. recoverable, diagnostic collection, MDPP code registry MDPP000–017), and conformance (12 required features, 2 optional features).

**Review fix applied:** Added the fourth ordering implication — variable values can contain include syntax, but since includes have already been expanded, include directives in variable values are not processed.

## Why This Works

The fundamental issue was that Markdown++ had an implicit processing model embedded in the ePublisher implementation but no explicit formalization. By reverse-engineering the actual two-phase pipeline from working code and formalizing it with RFC 2119 normative language, numbered requirements, error codes (MDPP000–017), explicit ordering implications, and edge case examples, the specification now serves as a reference standard. New implementors can build conformant processors without code inspection, and existing implementations can be validated against normative requirements.

## Prevention

- **Formalize implicit models early:** When designing a format with multiple interacting features, write the processing model alongside the syntax reference rather than waiting for implementations to discover it
- **Use numbered conformance requirements:** Structure specs with traceable requirements (R1, R2, ...) tied to prose explanations, enabling checklist-based implementation validation
- **Establish an error code registry early:** Classify every error condition as fatal or recoverable from the start (MDPP000–017) to prevent implementations from guessing at failure semantics
- **Specify interaction order explicitly:** For any multi-phase system, document what information flows between phases and in what order, including what is NOT available in later phases
- **Include edge case examples:** For every normative rule involving recursion, cycles, or ordering, provide concrete input/expected-output examples to catch ambiguities that prose alone misses

## Related Issues

- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) — Define the processing model for Markdown++ extensions (this issue)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) — Write a formal Markdown++ specification (resolved; processing model is foundational work)
- [#22](https://github.com/quadralay/markdown-plus-plus/issues/22) — Define cross-file link reference resolution semantics (resolved)
- [#10](https://github.com/quadralay/markdown-plus-plus/issues/10) — Formalize the attachment rule (resolved; cross-referenced by processing model Phase 2)
- [#16](https://github.com/quadralay/markdown-plus-plus/issues/16) — Define variable escaping mechanism (resolved; formalized in processing model Phase 1, Step 2)
- `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md` — Related specification pattern
- `docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md` — Variable escaping formalized in processing model
- `docs/solutions/documentation-gaps/combined-commands-conformance-classification-2026-04-10.md` — Combined commands promoted from OPTIONAL to REQUIRED (conformance counts updated from 11/3 to 12/2)
