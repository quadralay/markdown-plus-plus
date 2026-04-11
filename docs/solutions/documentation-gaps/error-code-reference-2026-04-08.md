---
title: Standalone error code reference for MDPP000-MDPP017
date: 2026-04-08
last_updated: 2026-04-11
category: documentation-gaps
module: plugins/markdown-plus-plus
problem_type: documentation_gap
component: documentation
symptoms:
  - Error codes defined only in validate-mdpp.py implementation
  - syntax-reference.md had a brief summary table but no detailed detection logic
  - Alternative validator implementations would need to reverse-engineer Python script
  - MDPP000 was missing from the syntax-reference.md table entirely
  - MDPP004 and MDPP005 incorrectly marked as "Reserved -- not yet implemented" (corrected 2026-04-11; see follow-up below)
  - error-codes.md and syntax-reference.md missing MDPP010-MDPP017 despite all 18 codes being defined in normative spec (corrected 2026-04-11; see follow-up below)
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - error-codes
  - validation
  - specification
  - validate-mdpp
  - spec-alignment
  - spec-consistency
  - reserved-codes
  - diagnostic-codes
---

# Standalone error code reference for MDPP000-MDPP017

## Problem

Markdown++ validation codes MDPP000 through MDPP009 were defined only in the `validate-mdpp.py` script and summarized briefly in `syntax-reference.md`. There was no standalone, implementation-independent reference document. Anyone building an alternative validator would need to reverse-engineer the Python script to understand what each code means, when it triggers, and how to fix the underlying issue.

## Symptoms

- No single document a validator author could use as a specification for error codes
- `syntax-reference.md` listed codes in a summary table but omitted detection logic, trigger examples, and suggested fixes
- MDPP000 (file error) was missing from the `syntax-reference.md` validation table entirely
- The unified naming rule for MDPP002 was documented in a solution doc but not in any user-facing reference
- Reserved codes (MDPP004, MDPP005) had no documented intended behavior
- Wording inconsistency: MDPP001 was called "Unclosed" in some places and "Unmatched" in others
- The alias naming exception (digit-first allowed for aliases like `<!--#04499224-->`) was undocumented, meaning alternative validators would silently reject valid alias names

## What Didn't Work

Before this solution, understanding error codes required multiple sources:

- **`validate-mdpp.py`** contained the authoritative implementation but required Python knowledge to interpret and was tied to one specific implementation
- **`syntax-reference.md`** had a summary table but lacked the depth needed for reimplementation -- no detection algorithms, no trigger examples, no fix guidance
- **Solution docs** captured individual decisions (unified naming rule, attachment rule) but were scattered across files and not structured as a reference
- **The processing model** (`spec/processing-model.md`) established the diagnostic code registry and classified codes as static validation vs. processing-phase, but intentionally delegated static code details to the plugin references layer

## Solution

Created `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` -- a standalone reference document covering all ten static validation codes (MDPP000-MDPP009).

**Document structure:**

- Quick-reference summary table with code, name, severity, and description for all ten codes
- General rules section documenting that all checks skip fenced code blocks
- Naming rule section defining the shared grammar (`^[a-zA-Z_][a-zA-Z0-9_-]*$`) used by MDPP002 and MDPP007 — **note:** originally documented as a single-regex grammar; expanded to a three-pattern table (standard identifier, alias name, style/marker name) in follow-up correction below
- Per-code sections (`## MDPPnnn -- Name`) with severity, description, detection logic, trigger examples, and suggested fixes
- Reserved codes (MDPP004, MDPP005) documented with intended detection logic and reserved status — **note:** this was later found to be incorrect; see "Follow-up Correction" below

**Cross-referencing updates:**

- `syntax-reference.md` updated to cross-reference the new document for detailed error code information
- MDPP000 added to the `syntax-reference.md` validation checks table (was previously missing)
- `SKILL.md` updated with `error-codes.md` in the references section and a validation cross-reference link

**Review-phase refinements:**

- MDPP002 section enhanced with alias naming exception (`^[a-zA-Z0-9_][a-zA-Z0-9_-]*$` for aliases, allowing digit-first) — **note:** MDPP002 was later revised to reference per-entity-type rules rather than one regex for all entity types; see follow-up correction below
- MDPP001 wording unified to "Unmatched" across all documents (was inconsistently "Unclosed" in some files)

### Follow-up Correction (2026-04-11): MDPP004 and MDPP005 promoted, then MDPP004 re-reserved and MDPP013 removed

After the initial error-codes.md was created, a subsequent review ([#67](https://github.com/quadralay/markdown-plus-plus/issues/67)) promoted MDPP004 and MDPP005 from reserved to active. A further review then found:

- **MDPP004** (Invalid style placement) is fully covered by MDPP009 (orphaned comment tag). MDPP004 was re-reserved as a placeholder for code numbering stability.
- **MDPP013** (Include cycle detected during processing) was the runtime counterpart to MDPP005 (circular include). The static/runtime distinction was unnecessary — MDPP013 was removed and all circular include detection consolidated into MDPP005.

**What was corrected:**

- `error-codes.md` MDPP004 entry: re-reserved with note that MDPP009 provides full coverage
- `error-codes.md` MDPP005 entry: promoted to active, "(static analysis)" qualifier removed, MDPP013 cross-reference note removed
- `syntax-reference.md` validation checks table: MDPP004 marked *(Reserved)*, MDPP005 active
- MDPP005 heading normalized from "Circular Include Detected" to "Circular Include" (noun-phrase convention)
- MDPP013 marked as reserved in `spec/processing-model.md` and `spec/specification.md` diagnostic registries; all normative references changed to MDPP005
- Plugin version bumped 1.1.13 → 1.1.14 (patch)
- Test fixture added: `tests/sample-circular-includes.md` for MDPP005

### Follow-up Correction (2026-04-11): Three-pattern naming system

After the initial error-codes.md was created and the alias exception added during review, a subsequent audit ([#65](https://github.com/quadralay/markdown-plus-plus/issues/65)) found that the naming rule section still omitted the style/marker name pattern defined in `specification.md` §4.2. This caused MDPP002 to describe a single regex for all entity types — which would incorrectly reject valid style names and marker keys that contain embedded spaces (e.g., `<!--style:Code Block-->`).

**What was corrected:**

- `error-codes.md` naming rule section: expanded from two subsections ("Standard Identifier," "Alias Exception") to a three-pattern intro table plus three subsections ("Standard Identifier," "Alias Name," "Style/Marker Name")
- MDPP002 description: changed from a single implicit regex to "naming rule **for its entity type**" with the three patterns distinguished
- MDPP007 step 4: changed from ambiguous "naming rule regex" to "standard identifier regex (`^[a-zA-Z_][a-zA-Z0-9_\-]*$`)"
- MDPP003 cross-reference: changed from "the naming rule" to "style/marker name rule"
- Subsection headings renamed: "Alias Exception" → "Alias Name," "Style/Marker Name Exception" → "Style/Marker Name" (first-class patterns, not edge cases)
- Table header "Used by" normalized to "Used By" for capitalization consistency with the spec

**Three-pattern table (current state):**

| Form | Regex | Used By | Spaces |
|------|-------|---------|--------|
| **Standard identifier** | `^[a-zA-Z_][a-zA-Z0-9_\-]*$` | Variables, conditions | No |
| **Alias name** | `^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$` | Aliases (digit-first permitted) | No |
| **Style/marker name** | `^[a-zA-Z_][a-zA-Z0-9_ \-]*$` (trimmed) | Styles, marker keys | Yes, embedded |

### Follow-up Addition (2026-04-11): MDPP010-MDPP017 added to plugin references

A spec alignment audit ([#66](https://github.com/quadralay/markdown-plus-plus/issues/66)) found that the plugin reference documents were missing 8 processing-phase diagnostic codes defined in the normative spec (`spec/specification.md` §18 and `spec/processing-model.md`):

| Code | Severity | Name |
|------|----------|------|
| MDPP010 | Warning | Undefined variable reference |
| MDPP011 | Error | Maximum include depth exceeded |
| MDPP012 | Error | Condition block spans include boundary |
| MDPP013 | — (Reserved) | Include cycle detected during processing |
| MDPP014 | Warning | Unresolved cross-file link reference |
| MDPP015 | Warning | Unknown mdpp-version in frontmatter |
| MDPP016 | Warning | Feature requires newer spec version |
| MDPP017 | Error | Invalid UTF-8 encoding |

Note: MDPP014 was partially present in `syntax-reference.md` from prior work but absent from `error-codes.md`.

**What was added:**

- `error-codes.md`: Full detailed entries for MDPP010-MDPP017, each with severity, description, detection logic, trigger examples, and suggested fixes; quick reference table expanded from 10 to 18 codes
- `syntax-reference.md`: Validation checks table updated to include all 18 codes
- Plugin version bumped 1.1.14 → 1.1.15 (patch)

**Accuracy errors found during review and corrected:**

1. **MDPP013 name mismatch** — The first pass wrote "Circular include detected during processing"; the normative spec says "Include cycle detected during processing." Corrected in both the quick reference table and the detail section to match the spec's formal name exactly.

2. **MDPP013 severity inconsistency** — The detail section used "(Reserved)" as the severity while the quick reference table and `syntax-reference.md` used "—". Normalized to "—" throughout.

3. **MDPP014 detection logic false cross-reference** — The initial draft cited MDPP008 (Duplicate alias) as governing within-file link reference slug duplicates. MDPP008 covers only `<!--#name-->` custom HTML-comment aliases, not CommonMark `[slug]: url` link reference definitions. Within-file duplicate link references are governed by CommonMark's first-definition-wins rule. The false reference was removed; detection logic now correctly scopes MDPP014 to cross-file duplicates only.

## Why This Works

The error code reference separates the specification of what codes mean from how any particular tool implements them. By documenting detection logic as algorithms (stack-based tracking, JSON parse attempts, path resolution) rather than code, alternative implementations can achieve behavioral parity without reading Python. The unified naming rule is documented once and referenced by the codes that use it, preventing drift between MDPP002 and MDPP007 validation.

This also fulfills the principle established in the attachment rule solution doc: "Every validation check should have a corresponding user-facing specification."

## Prevention

- **Document error codes alongside implementation:** When adding a new validation check, create the reference entry at the same time as the code. The error-codes.md document provides the template for new entries.
- **Keep detection logic implementation-independent:** Describe algorithms in terms of data structures and conditions, not language-specific constructs, so the reference serves any implementation language.
- **Maintain the diagnostic code registry:** The processing model (`spec/processing-model.md`) owns the registry of all MDPP codes. Static validation codes (000-009) are detailed in `error-codes.md`; processing-phase codes (010-017) are detailed in `error-codes.md` as well. New codes must be registered in both the normative spec and the plugin references.
- **Treat wording consistency as a reviewable concern:** When a concept has a canonical name (e.g., "Unmatched" not "Unclosed" for MDPP001), grep across all documents during review to catch drift before it ships.
- **Never mark a code reserved without a spec citation.** If the normative spec defines the code, the plugin reference must reflect it. "Reserved" status is only appropriate when the spec itself designates the code as reserved. When reversing a deferral decision, explicitly supersede the prior solution doc (as done here) and treat any `error-codes.md` entry containing the word "reserved" as a review flag requiring justification.
- **Wording-drift prevention is not one-time.** The follow-up correction on 2026-04-11 materialized exactly the wording-drift risk this solution flagged. Grep for "reserved" across all skill-surface documents before any release that touches error code definitions. Test fixtures for MDPP codes make drift immediately visible — a passing fixture cannot coexist with a "reserved" placeholder.
- **Verify cross-reference scope before citing.** When detection logic for a new code references another code (e.g., "see MDPP008 for X"), check that the cited code's documented scope actually covers X. The MDPP008 entry defines its coverage as `<!--#name-->` comment syntax — a grep for its name in new entries is a quick scope-boundary check. False cross-references cause conformant implementations to misclassify constructs.
- **Audit spec-to-reference coverage before each release.** Extract the full code list from the normative spec and diff it against `error-codes.md` and `syntax-reference.md`. The MDPP010-017 gap persisted because no such audit existed. A simple count check (expect 18 entries) would have caught it immediately.

## Related Issues

- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) -- Add standalone error code reference (this issue)
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) -- Implement unified naming rule (resolved; naming grammar documented in error-codes.md)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Define processing model (resolved; established diagnostic code registry)
- [#10](https://github.com/quadralay/markdown-plus-plus/issues/10) -- Formalize attachment rule (resolved; MDPP009 semantics cross-referenced)
- [#67](https://github.com/quadralay/markdown-plus-plus/issues/67) -- Remove "reserved" annotations from MDPP004 and MDPP005 (follow-up correction to this solution; MDPP004/005 promoted to active, v1.1.14)
- [#65](https://github.com/quadralay/markdown-plus-plus/issues/65) -- Align error-codes.md naming rules with three-pattern system (resolved 2026-04-11; three-pattern naming table added)
- [#66](https://github.com/quadralay/markdown-plus-plus/issues/66) -- Add MDPP010-MDPP017 to error-codes.md and syntax-reference.md (resolved; all 18 codes documented, accuracy errors corrected; v1.1.15)
- `docs/solutions/documentation-gaps/error-codes-naming-rule-three-pattern-gap-2026-04-11.md` -- Detailed solution doc for the #65 three-pattern correction
- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` -- MDPP002 scope expansion
- `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md` -- Prevention principle fulfilled
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` -- Diagnostic code registry
- [#42](https://github.com/quadralay/markdown-plus-plus/issues/42) -- MDPP014 addition (resolved; MDPP014 detail entry added in follow-up above)
- `docs/solutions/documentation-gaps/cross-file-link-resolution-semantics-2026-04-08.md` -- MDPP014 scope detail
- `docs/solutions/documentation-gaps/utf8-encoding-specification-gap-2026-04-08.md` -- MDPP017 scope detail
- `docs/solutions/documentation-gaps/format-versioning-mechanism-2026-04-08.md` -- MDPP015/016 scope detail
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Formal specification umbrella (parent initiative)
