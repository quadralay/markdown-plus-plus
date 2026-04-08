---
title: Standalone error code reference for MDPP000-MDPP009
date: 2026-04-08
category: documentation-gaps
module: plugins/markdown-plus-plus
problem_type: documentation_gap
component: documentation
symptoms:
  - Error codes defined only in validate-mdpp.py implementation
  - syntax-reference.md had a brief summary table but no detailed detection logic
  - Alternative validator implementations would need to reverse-engineer Python script
  - MDPP000 was missing from the syntax-reference.md table entirely
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - error-codes
  - validation
  - specification
  - validate-mdpp
---

# Standalone error code reference for MDPP000-MDPP009

## Problem

Markdown++ validation codes MDPP000 through MDPP009 were defined only in the `validate-mdpp.py` script and summarized briefly in `syntax-reference.md`. There was no standalone, implementation-independent reference document. Anyone building an alternative validator would need to reverse-engineer the Python script to understand what each code means, when it triggers, and how to fix the underlying issue.

## Symptoms

- No single document a validator author could use as a specification for error codes
- `syntax-reference.md` listed codes in a summary table but omitted detection logic, trigger examples, and suggested fixes
- MDPP000 (file error) was missing from the `syntax-reference.md` validation table entirely
- The unified naming rule for MDPP002 was documented in a solution doc but not in any user-facing reference
- Reserved codes (MDPP004, MDPP005) had no documented intended behavior

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
- Naming rule section defining the shared grammar (`^[a-zA-Z_][a-zA-Z0-9_-]*$`) used by MDPP002 and MDPP007
- Per-code sections (`## MDPPnnn -- Name`) with severity, description, detection logic, trigger examples, and suggested fixes
- Reserved codes (MDPP004, MDPP005) documented with intended detection logic and reserved status

**Cross-referencing updates:**

- `syntax-reference.md` updated to cross-reference the new document for detailed error code information
- MDPP000 added to the `syntax-reference.md` validation checks table (was previously missing)

## Why This Works

The error code reference separates the specification of what codes mean from how any particular tool implements them. By documenting detection logic as algorithms (stack-based tracking, JSON parse attempts, path resolution) rather than code, alternative implementations can achieve behavioral parity without reading Python. The unified naming rule is documented once and referenced by the codes that use it, preventing drift between MDPP002 and MDPP007 validation.

This also fulfills the principle established in the attachment rule solution doc: "Every validation check should have a corresponding user-facing specification."

## Prevention

- **Document error codes alongside implementation:** When adding a new validation check, create the reference entry at the same time as the code. The error-codes.md document provides the template for new entries.
- **Keep detection logic implementation-independent:** Describe algorithms in terms of data structures and conditions, not language-specific constructs, so the reference serves any implementation language.
- **Maintain the diagnostic code registry:** The processing model (`spec/processing-model.md`) owns the registry of all MDPP codes. Static validation codes (000-009) are detailed in `error-codes.md`; processing-phase codes (010-013) are detailed in the processing model itself.

## Related Issues

- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) -- Add standalone error code reference (this issue)
- [#15](https://github.com/quadralay/markdown-plus-plus/issues/15) -- Implement unified naming rule (resolved; naming grammar documented in error-codes.md)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Define processing model (resolved; established diagnostic code registry)
- [#10](https://github.com/quadralay/markdown-plus-plus/issues/10) -- Formalize attachment rule (resolved; MDPP009 semantics cross-referenced)
- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` -- MDPP002 scope expansion
- `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md` -- Prevention principle fulfilled
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` -- Diagnostic code registry
