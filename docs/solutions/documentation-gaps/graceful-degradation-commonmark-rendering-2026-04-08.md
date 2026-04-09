---
title: "Document graceful degradation behavior for Markdown++ extensions in CommonMark renderers"
date: 2026-04-08
category: documentation-gaps
module: specification
problem_type: documentation_gap
component: documentation
symptoms:
  - "Whitepaper claims files render cleanly without qualifying which extensions produce artifacts"
  - "Authors discover variable tokens visible in GitHub previews only by accident"
  - "No systematic reference for per-extension CommonMark rendering behavior"
  - "PR reviewers see all conditional branches with no indication content is conditional"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - graceful-degradation
  - commonmark
  - rendering
  - compatibility
  - whitepaper
  - extensions
  - html-comments
  - variables
---

# Document graceful degradation behavior for Markdown++ extensions in CommonMark renderers

## Problem

The whitepaper claimed Markdown++ files "render cleanly" in standard viewers without systematic per-extension documentation of what that actually means. Authors, reviewers, and teams evaluating the format had no way to know which extensions produce invisible output, which produce different-but-readable output, and which produce raw artifacts or missing content.

## Symptoms

- The whitepaper's blanket "renders cleanly" claim was inaccurate for a subset of extensions
- Variables produce literal `$product_name;` tokens in plain CommonMark renderers with no documentation warning authors
- File includes cause content to disappear entirely in standard views
- Conditions cause all branches to appear simultaneously in GitHub file views and PR diffs
- Multiline table continuation rows render as flat, separate rows
- No systematic reference existed for any of these behaviors

## What Didn't Work

- The first version of the corrected whitepaper paragraph (commit `2e646d6`) inaccurately classified conditions and multiline tables as "fully hidden," grouping them with comment-based extensions when they actually produce visible but different output. This was caught during the review phase and corrected in commit `0facb95`.
- A binary graceful/not-graceful classification was considered and rejected because it would have collapsed the meaningful distinction between "content present but looks different" (conditions, multiline tables) and "content missing or raw tokens visible" (variables, includes).

## Solution

Five coordinated documentation changes addressed the gap:

1. **Created `spec/graceful-degradation.md`** -- Full degradation matrix covering all 11 extensions across three tiers (fully graceful, partially graceful, not graceful). Includes a design principle section explaining the two underlying extension mechanisms (HTML comment directives vs. inline token syntax), tier definitions, and an "Implications for Authors" section with actionable guidance organized as "Use freely," "Use with awareness," and "Use deliberately."

2. **Updated `spec/whitepaper.md`** -- Replaced the blanket compatibility claim with a paragraph that accurately distinguishes four behaviors: comment-based extensions (fully hidden per CommonMark spec), conditions and multiline tables (visible but different), inline token extensions like variables (literal text visible), and processing-dependent content like file includes (absent). Links to the new appendix for the full breakdown.

3. **Added `**CommonMark rendering:**` notes to the syntax reference** -- 10 notes across all extension sections in `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`, giving authors degradation information at the point of use.

4. **Updated `SKILL.md`** -- Added a spec reference to `graceful-degradation.md` so agents can discover and cite the degradation matrix when advising authors.

5. **Bumped plugin version** 1.1.5 to 1.1.6 to reflect the documentation update.

## Why This Works

The root cause was a documentation gap, not a code defect. The whitepaper's claim was not wrong in spirit -- comment-based extensions (custom styles, aliases, markers, combined commands, inline styles, content islands) genuinely are invisible in CommonMark renderers. But the claim overgeneralized to all extensions. The fix replaces a single undifferentiated claim with a tiered, per-extension matrix grounded in the actual CommonMark rendering behavior of each mechanism. The three-tier system (fully graceful / partially graceful / not graceful) maps cleanly to the two extension mechanisms: HTML comments are hidden, inline tokens pass through, and processing-dependent content requires a Markdown++ processor.

The solution applied "affirmative framing" from the interchangeability messaging solution doc -- describing what renders and how rather than what "breaks" -- ensuring the degradation documentation supports rather than undermines the format's positioning.

## Prevention

- **New extension checklist:** When adding new extensions to the spec, update both `spec/graceful-degradation.md` (matrix row) and the syntax reference (`**CommonMark rendering:**` note) in the same PR. This keeps degradation documentation co-located with syntax documentation.
- **Whitepaper compatibility claims** should reference specific tiers from the matrix rather than making blanket assertions, so new extensions do not silently invalidate the claim.
- **Classify at design time:** Apply the three-tier classification (fully graceful / partially graceful / not graceful) to any new extension during design, before the spec is finalized, so degradation behavior is a deliberate choice rather than a discovered side effect.

## Related Issues

- [Issue #12](https://github.com/quadralay/markdown-plus-plus/issues/12) -- the originating documentation gap issue
- [Interchangeability messaging solution](document-interchangeability-messaging-2026-03-30.md) -- predecessor that established the "tool spectrum" concept and affirmative framing principle; this solution deepens and qualifies the interchangeability messaging
- [Issue #7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- formal spec effort; the graceful degradation appendix is a spec deliverable
- [Issue #8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- processing model; defines runtime behavior while the degradation matrix defines what users see in standard renderers
