---
title: "Document Markdown++ interchangeability with different tools"
date: 2026-03-30
category: documentation-gaps
module: specification-docs
problem_type: documentation_gap
component: documentation
symptoms:
  - "The word 'interchangeability' appeared nowhere in the repository"
  - "Documentation used defensive framing ('doesn't break') instead of affirmative framing ('works everywhere')"
  - "No tool spectrum concept explained the range from Markdown-only to Markdown++-aware tools"
  - "Migration sections did not reinforce that migrated files work in any Markdown tool"
  - "Plugin references (best-practices, syntax-reference) had no interchangeability messaging"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: low
tags:
  - interchangeability
  - documentation-framing
  - markdown-plus-plus
  - commonmark
  - tool-spectrum
  - affirmative-framing
---

# Document Markdown++ interchangeability with different tools

## Problem

The repository's documentation described what Markdown++ *doesn't do* (break standard tools) rather than what it *does* (work across the full spectrum of Markdown tools). The interchangeability concept -- that Markdown++ files are valid `.md` files usable by any Markdown tool -- was never explicitly named or communicated.

## Symptoms

- The word "interchangeability" appeared nowhere in the repository
- Documentation used defensive framing ("doesn't break in other tools") instead of affirmative framing ("works everywhere on a spectrum")
- No "tool spectrum" concept explained the range from Markdown-only editors to Markdown++-aware publishers
- Migration sections (FrameMaker, DITA, MDX/AsciiDoc/rST) did not reinforce that migrated files continue working in any Markdown tool
- Getting Started did not establish the "write plain Markdown first, extend where needed" workflow
- Plugin reference docs (`best-practices.md`, `syntax-reference.md`) contained no interchangeability messaging

## What Didn't Work

N/A -- this was a documentation gap identified through analysis during the whitepaper neutralization work (PR #4, issue #3), not a debugging problem. The brainstorm phase identified the missing concept and the plan phase designed the weaving strategy.

## Solution

Seven implementation units across three files (README evaluated and left unchanged):

**`spec/whitepaper.md`** -- four units:
- Named "interchangeability" in the introduction and established the "tool spectrum" concept in "What is Markdown++?"
- Added incremental adoption paragraph to the CommonMark backward compatibility benefit section
- Added one reinforcement sentence each to FrameMaker, DITA, and MDX/AsciiDoc/rST migration sections
- Expanded Getting Started to state files work in every Markdown tool and that authors should write plain Markdown first

**`plugins/.../references/best-practices.md`** -- one unit:
- Added "Start with Markdown, extend where needed" framing section before "When to Use Each Extension"

**`plugins/.../references/syntax-reference.md`** -- one unit:
- Added one-sentence interchangeability note to Base Specification section, correctly distinguishing HTML comment invisibility from inline token pass-through behavior

**Review fixes applied:**
- P1: `syntax-reference.md` originally stated inline tokens are "invisible" -- corrected to distinguish that HTML comments are invisible while inline tokens pass through as plain text
- P3: Rewording at `whitepaper.md:273` from "extensions are additive" to "no standard renderer is broken by the extensions" to avoid slogan repetition
- P3: Removed parallel reassurance coda from FrameMaker migration section (DITA retains its stronger version)

## Why This Works

The root cause was a messaging gap: the documentation described what Markdown++ *doesn't do* rather than what it *does*. By explicitly naming the concept ("interchangeability"), introducing the "tool spectrum" metaphor, and weaving affirmative statements into existing sections rather than creating standalone guides, the docs now consistently communicate the key value proposition at every point a reader encounters it -- introduction, features, migration paths, getting started, and reference material.

The "weave, don't create" approach ensures readers encounter the message wherever they enter the docs, rather than needing to find a standalone page.

## Prevention

- **Name concepts explicitly.** When a key value proposition exists implicitly, give it a word ("interchangeability") and use it consistently across docs.
- **Use affirmative framing.** Review documentation for defensive language ("doesn't break," "won't cause issues") and convert to affirmative statements ("works in every tool," "remains valid").
- **Weave, don't isolate.** Major messaging themes should appear in every section where a reader might enter the docs, not in a single standalone page.
- **Distinguish HTML comments from inline tokens.** HTML comments are invisible to standard renderers; inline tokens pass through as plain text. These are different behaviors and must be described accurately.
- **Watch for slogan repetition.** When weaving a concept across multiple sections, vary the phrasing to avoid a marketing-copy feel.

## Related Issues

- [Issue #5](https://github.com/quadralay/markdown-plus-plus/issues/5) -- "Document Markdown and Markdown++ interchangeability with different tools" (origin issue)
- [Issue #3](https://github.com/quadralay/markdown-plus-plus/issues/3) -- "Neutralize whitepaper" (predecessor work that surfaced the gap)
- [PR #6](https://github.com/quadralay/markdown-plus-plus/pull/6) -- Implementation PR
- [PR #4](https://github.com/quadralay/markdown-plus-plus/pull/4) -- Whitepaper neutralization (where the feedback originated)
