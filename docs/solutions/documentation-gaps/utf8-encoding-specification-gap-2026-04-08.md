---
title: UTF-8 character encoding requirement missing from specification
date: 2026-04-08
category: documentation-gaps
module: spec/processing-model
problem_type: documentation_gap
component: documentation
symptoms:
  - "Specification did not declare a required character encoding"
  - "Tools could disagree on handling non-ASCII characters in variable names, condition names, and file paths"
  - "No diagnostic code defined for encoding validation failures"
  - "CommonMark 0.30 UTF-8 requirement not explicitly inherited by Markdown++"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - utf-8
  - character-encoding
  - processing-model
  - specification
  - commonmark
  - conformance
  - mdpp017
  - bom-handling
---

# UTF-8 character encoding requirement missing from specification

## Problem

The Markdown++ specification lacked any normative statement about character encoding, meaning tools could disagree on how to handle non-ASCII characters in variable names, condition names, style names, marker values, and file paths — breaking internationalized documentation workflows.

## Symptoms

- No guarantee that two conforming processors would interpret the same document identically when it contained non-ASCII characters (e.g., accented letters in variable names, CJK characters in condition names).
- Include chains mixing encodings could produce silent data corruption — one file in ISO-8859-1, another in UTF-8, with no diagnostic emitted.
- UTF-8 BOM bytes could appear mid-document after include expansion, corrupting content or causing parser errors depending on the tool.
- The unified naming rule already permitted non-English letter values, but without an encoding requirement, "letter" had no well-defined meaning across implementations.
- Implementation-specific fallback behavior (e.g., ePublisher's ISO-8859-1 fallback) was undocumented, making conformance testing impossible.

## What Didn't Work

- **Requiring BOM**: Rejected because most modern UTF-8 files omit the BOM; requiring it would force unnecessary file modifications across existing documentation sets.
- **Forbidding BOM**: Rejected because real-world files (especially those created on Windows) frequently include a BOM; forbidding it would break existing workflows.
- **Mandating a specific fallback encoding (e.g., ISO-8859-1)**: Rejected because prescribing recovery strategy would over-constrain implementations and create a false sense of reliability — invalid encoding corrupts character boundaries, making any automatic recovery unreliable.
- **Placing encoding rules in a separate specification document**: Rejected because the processing model already owns the pipeline, diagnostics registry, and conformance requirements — a separate document would fragment normative content.

## Solution

Added a "Character Encoding" section to `spec/processing-model.md` (between Definitions and Pipeline Overview) with four subsections, plus cross-reference and conformance updates throughout the document.

**Core specification additions:**

- **Encoding Requirement**: "Markdown++ documents MUST be encoded in UTF-8" — aligned with CommonMark 0.30 Section 2.2.
- **BOM Handling**: Leading U+FEFF BOM is OPTIONAL; processors MUST strip it before parsing; BOMs from included files are stripped during include expansion.
- **MDPP017 Diagnostic**: New Error-severity code triggered on the first invalid UTF-8 byte sequence in any document (root or included). Recovery behavior is explicitly implementation-defined. Processors MAY collect additional errors but MUST NOT use decoded content from an invalid file for further pipeline processing.
- **Include Chain Encoding Consistency**: All files in an include chain MUST be UTF-8. MDPP017 includes the offending file's path.

**Cross-reference updates:**

- Algorithm step 1 updated to reference encoding validation and BOM stripping at file read time.
- Algorithm step 4e added: encoding failure in an included file leaves the include tag in place (consistent with MDPP006 behavior for missing files).
- MDPP017 registered in the Processing-Phase Codes table.
- Fatal error classification table updated with MDPP017, noting implementation-defined recovery.
- Introduction scope list updated to include character encoding.
- Required feature #11 added to conformance: encoding validation with BOM handling and MDPP017 emission.
- Line number guidance added for MDPP017 diagnostics (byte offset of first invalid sequence).

**Review-phase refinements (6 fixes applied):**

1. Added step 4e — encoding failure leaves include tag in place.
2. Resolved MUST/MAY contradiction — MAY collect errors but MUST NOT use decoded content for pipeline.
3. Broadened MDPP017 triggering condition to cover root document (not just included files).
4. Fatal error table updated to allow implementation-defined recovery.
5. Added line number guidance for MDPP017 diagnostics.
6. Simplified algorithm step 1 to cross-reference the Character Encoding section.

## Why This Works

UTF-8 is the universal encoding for web content and is already required by CommonMark 0.30, which Markdown++ extends. By making UTF-8 normative, the spec establishes a single, unambiguous interpretation of every byte in a document. MDPP017 catches encoding violations early (at file-read time, before parsing begins) because invalid UTF-8 corrupts character boundaries — once byte boundaries are wrong, no subsequent parsing step can produce reliable results. Making BOM OPTIONAL with mandatory stripping is the pragmatic middle ground: it accepts files from any platform without letting stray BOM bytes contaminate content after include expansion. Leaving recovery implementation-defined acknowledges that different tools have legitimate reasons for different strategies (abort, fallback, lossy substitution) while still requiring that the error is detected and reported.

## Prevention

- **Encoding inheritance audit**: When a format extends another specification (as Markdown++ extends CommonMark), systematically review what normative requirements the parent spec makes and ensure each is either explicitly inherited, overridden, or declared out of scope.
- **Feature matrix for extended specs**: Maintain a checklist of foundational concerns (encoding, line endings, maximum sizes, error handling) that any document format must address — use it as a gap-detection tool when drafting new specification sections.
- **Include-chain analysis**: Any time the spec adds a feature that combines content from multiple files (includes, transclusion, imports), verify that all file-level invariants (encoding, BOM, line endings) are specified for the combined result, not just individual files.
- **Diagnostic code reservation**: When adding new diagnostic codes, check for collisions with existing codes immediately — this issue's implementation required two follow-up fixes to resolve MDPP014/MDPP015 code collisions that occurred because the code was assigned without checking the full registry.
- **Cross-reference completeness**: When adding a new normative requirement, systematically update every section that could reference it: the algorithm steps, the diagnostic registry, the error classification table, the conformance requirements, and the introduction's scope statement.

## Related Issues

- [#23](https://github.com/quadralay/markdown-plus-plus/issues/23) — Add UTF-8 character encoding requirement to specification (this issue)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) — Formal specification (encoding section)
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) — Unified naming rule (UTF-8 letter support, deferred)
- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) — Standalone error code reference (MDPP017 extends the code range)
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` — Processing model foundation (diagnostic registry now extended to MDPP017)
- `docs/solutions/documentation-gaps/format-versioning-mechanism-2026-04-08.md` — Sibling diagnostic registry extension (MDPP015-016)
- `docs/solutions/documentation-gaps/cross-file-link-resolution-semantics-2026-04-08.md` — Include chain behavior pattern (MDPP014)
