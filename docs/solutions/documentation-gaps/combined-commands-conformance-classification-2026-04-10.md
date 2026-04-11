---
title: Combined commands conformance misclassification
date: 2026-04-10
category: documentation-gaps
module: spec/conformance
problem_type: documentation_gap
component: documentation
symptoms:
  - Combined commands classified as OPTIONAL despite being required for core functionality
  - Specification normative examples use combined commands while marking them optional
  - RFC 2119 keyword contradictions across specification files for evaluation order
  - Processor claiming conformance could not handle the spec's own recommended patterns
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
tags:
  - conformance
  - combined-commands
  - rfc-2119
  - specification
  - processing-model
  - evaluation-order
---

# Combined commands conformance misclassification

## Problem

The Markdown++ specification classified "combined commands" (semicolon-separated directives in a single HTML comment) as an OPTIONAL conformance feature, creating a logical contradiction: a processor could claim conformance while being unable to process the spec's own normative examples, which use combined commands pervasively.

## Symptoms

- `processing-model.md` listed combined commands under "Optional Features," meaning a processor could skip them entirely and still be called conformant.
- The spec's own heading pattern `<!-- style:Heading2 ; #200010 -->` appeared dozens of times throughout normative examples, but a conformant-without-combined-commands processor would orphan those directives.
- Due to the attachment rule (only the immediately preceding comment attaches), there was no alternative way to apply both a style and an alias to the same element without combined commands. Splitting them into two stacked comments would orphan the top one.
- `specification.md` section 2.2 cited "combined commands" as an example of an optional feature, reinforcing the incorrect classification.
- Multiple spec files used `MUST` for evaluation order of combined command segments, which was stricter than intended — the order is a readability recommendation, not a processing requirement.

## What Didn't Work

- **Promotion with strict evaluation order (commit 1).** The initial fix correctly promoted combined commands from OPTIONAL to REQUIRED but retained `MUST` language for the evaluation order. Maintainer feedback on PR #74 clarified that processors should be free to evaluate segments in any order — the listed order is a readability convention for authors, not a processing constraint.
- **Incomplete cross-file sweep (commits 1-2).** After relaxing the evaluation order in the primary locations (`processing-model.md` and `specification.md` section 16.5), the code review phase discovered six additional locations across three files where RFC 2119 keywords still contradicted the relaxed stance. This demonstrated that specification consistency fixes require systematic cross-file search for all related RFC 2119 keyword usage.

## Solution

The fix spans three specification files with changes in two categories: (A) promoting combined commands to REQUIRED, and (B) relaxing evaluation order from MUST to SHOULD/MAY.

**A. Conformance promotion**

Before (`processing-model.md`, Optional Features):
```markdown
3. **Combined commands** -- Semicolon-separated commands in a single comment tag.
   If supported, a processor MUST evaluate them in the order specified in
   Combined Command Evaluation Order.
```

After (`processing-model.md`, Required Features, item 12):
```markdown
12. **Combined commands** -- Semicolon-separated commands in a single comment tag.
    The evaluation order listed in Combined Command Evaluation Order is
    RECOMMENDED for readability but not required; processors MAY evaluate
    segments in any order.
```

Before (`specification.md` section 16.5):
```markdown
Combined commands are classified as an OPTIONAL feature...
```

After:
```markdown
Combined commands are classified as a REQUIRED feature...
```

**B. Evaluation order relaxation**

Before (`processing-model.md` line 393, `specification.md` section 16.3):
```markdown
...the processor MUST evaluate them in the following fixed order...
```

After:
```markdown
...the processor SHOULD evaluate them in the following order for readability
and consistency... Processors MAY evaluate segments in any order.
```

Cross-file fixes in `specification.md` sections 9.4, 11.4, 13.4, 14.4 (evaluation position stated as fact → prefixed with "In the recommended evaluation order") and `multiline-cell-extensions.md` (MUST → SHOULD/MAY).

## Why This Works

The root cause was a specification logic error where the conformance classification contradicted the spec's own design constraints:

- The attachment rule (only one comment attaches per element) makes combined commands the *only* mechanism for multi-directive application. Making this mechanism optional means a "conformant" processor cannot handle a fundamental use case the spec itself relies on.
- The evaluation order relaxation resolves a separate but related issue: since the directives in a combined command are independent operations (style, alias, marker, multiline all attach different metadata types), no processing order dependency exists between them. Using MUST for order was unnecessarily restrictive.
- The cross-file consistency fix ensures every RFC 2119 keyword usage across all spec files agrees on the same semantics.

## Prevention

- **Cross-file RFC 2119 audit on every conformance change.** When changing the conformance level or RFC 2119 keywords for any feature, search all spec files for every mention of that feature's name and related keywords. The grep pattern `combined command|evaluation order|evaluate.*order` would have caught all six missed locations.
- **Self-reference consistency check.** Before classifying a feature as OPTIONAL, verify that the spec's own normative examples do not depend on it. If normative examples use a feature, that feature must be REQUIRED.
- **Distinguish mechanism constraints from convention preferences.** Use MUST only when incorrect behavior would produce wrong output. Use SHOULD/MAY when the constraint is about author readability or implementation style with no functional impact on results.

## Related Issues

- [quadralay/markdown-plus-plus#68](https://github.com/quadralay/markdown-plus-plus/issues/68) — Promote combined commands from OPTIONAL to REQUIRED
- [quadralay/markdown-plus-plus#74](https://github.com/quadralay/markdown-plus-plus/pull/74) — PR implementing the fix
- [quadralay/markdown-plus-plus#8](https://github.com/quadralay/markdown-plus-plus/issues/8) — Original issue that created the processing model conformance framework
- Related doc: [processing-model-specification-2026-04-08.md](processing-model-specification-2026-04-08.md) — Created the processing model with the original (now corrected) conformance counts of 11 required / 3 optional features
