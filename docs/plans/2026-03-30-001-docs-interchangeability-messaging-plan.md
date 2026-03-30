---
title: "docs: Weave interchangeability messaging into existing documentation"
type: feat
status: completed
date: 2026-03-30
origin: docs/brainstorms/2026-03-30-interchangeability-messaging-requirements.md
---

# docs: Weave interchangeability messaging into existing documentation

## Overview

Introduce "interchangeability" as a named, affirmative concept across the whitepaper, syntax reference, and best practices. The current documentation frames Markdown++'s relationship to standard Markdown defensively ("invisible to standard renderers," "doesn't break"). This work shifts the framing to an affirmative capability story: Markdown++ files *are* Markdown files, and the tool ecosystem is a spectrum from Markdown-only to Markdown++-aware.

## Problem Frame

New users and evaluators may perceive Markdown++ as a proprietary format requiring specialized tooling. The existing documentation emphasizes backward compatibility but does not name or explain the interchangeability principle -- that authors can use any Markdown tool for their full workflow and incrementally adopt `++` extensions where they add value. This creates an unnecessary adoption barrier. (see origin: `docs/brainstorms/2026-03-30-interchangeability-messaging-requirements.md`)

## Requirements Trace

- R1. Name the interchangeability concept explicitly -- distinct from "backward compatibility"
- R2. Communicate the tool spectrum (Markdown-only to Markdown++-aware) as a continuum
- R3. Reinforce in the whitepaper introduction so readers encounter it in the first few paragraphs
- R4. Strengthen the "Full CommonMark backward compatibility" benefit section
- R5. Reinforce in migration paths -- teams are not leaving the Markdown ecosystem
- R6. Address in plugin reference materials (syntax reference or best practices)

## Scope Boundaries

- **In scope:** `spec/whitepaper.md`, `plugins/.../references/best-practices.md`, `plugins/.../references/syntax-reference.md`, `README.md` (minor reinforcement only)
- **Out of scope:** New standalone documents, `examples/` directory, `SKILL.md` structure, plugin metadata
- **Out of scope:** Changing the README's structure -- it already communicates compatibility well

## Context & Research

### Relevant Code and Patterns

**Current defensive framing in the whitepaper:**
- Line 18: "extensions that are invisible to standard Markdown renderers"
- Line 29: "Standard Markdown renderers treat HTML comments as invisible"
- Line 31: "Authors are never locked into a proprietary format"
- Line 47: Section heading "Full CommonMark backward compatibility"
- Line 49: "syntactically invisible to standard renderers"
- Line 58: "renders this cleanly in standard tools"

**Current tone/voice:** Assertive, confident, declarative. Em dashes for asides. "Standard Markdown" is the canonical phrase for the baseline. Bold for key terms. No contractions.

**best-practices.md patterns:** "Use X for / Avoid X for" structure per extension. The "Avoid" lists already implicitly communicate "use plain Markdown when sufficient" (lines 47, 202) -- these are natural expansion points.

**syntax-reference.md:** Opens with "Markdown++ extends **CommonMark 0.30**" (line 12). Terse technical reference voice. Brief interchangeability note fits at the Base Specification section.

**README.md:** Lines 5-7 already communicate the core message well. Only minor reinforcement warranted.

### Institutional Learnings

No `docs/solutions/` directory exists. No prior institutional knowledge to draw from.

### External References

Skipping external research -- this is pure documentation messaging work with strong local patterns to follow. No framework or API decisions involved.

## Key Technical Decisions

- **"Interchangeability" as the term:** Use "interchangeability" as the named concept per the issue and brainstorm. In context, supplement with concrete phrasing like "the tool spectrum" and "incremental adoption" to make the abstract term tangible. Do not introduce competing terminology.

- **best-practices.md is the primary home for R6 (plugin reference guidance):** Its "When to Use Each Extension" section and advisory tone are the natural place for incremental adoption guidance. syntax-reference.md gets a brief note at the Base Specification section to establish the principle, but detailed guidance belongs in best practices.

- **Weave into existing section flow, don't add new top-level sections to the whitepaper:** The interchangeability concept should appear within existing sections (introduction, "What is Markdown++?", benefits, migration paths, getting started) rather than as a new standalone section. This keeps the narrative arc intact and ensures readers encounter the concept naturally.

- **Preserve all existing compatibility messaging:** The brainstorm success criteria explicitly require that no existing messaging is weakened or contradicted. New text builds on top of existing claims, not in place of them.

- **README changes are minimal:** The README already communicates the core message. At most, add one sentence reinforcing the spectrum concept near the existing compatibility statement.

## Open Questions

### Resolved During Planning

- **Which reference file for R6?** best-practices.md -- its advisory structure ("Use X for / Avoid X for") naturally accommodates incremental adoption guidance. syntax-reference.md gets a brief note only.

- **Where in the whitepaper introduction (R3)?** Two insertion points: (1) in the resolution paragraph at line 18, where "invisible to standard Markdown renderers" can be expanded to name interchangeability; (2) in the "What is Markdown++?" section at lines 29-31, where the tool spectrum concept fits naturally alongside the existing "works in every tool" claim.

- **What framing for the tool spectrum (R2)?** A simple three-tier description: tools that process `.md` files as-is (Markdown-only), tools that understand some extensions (partially aware), and tools that fully interpret all Markdown++ directives (Markdown++-aware). This maps to concrete examples readers already know.

### Deferred to Implementation

- **Exact wording for each insertion:** The plan identifies placement and intent. The implementer should draft prose that matches the whitepaper's assertive, declarative voice and iterate on phrasing.

- **Whether the README warrants any change at all:** The implementer should re-read the README in context of the whitepaper changes and decide if reinforcement adds value or is redundant.

## Implementation Units

- [x] **Unit 1: Whitepaper introduction and "What is Markdown++?" (R1, R2, R3)**

  **Goal:** Introduce interchangeability as a named concept in the first sections readers encounter. Establish the tool spectrum.

  **Dependencies:** None

  **Files:**
  - Modify: `spec/whitepaper.md` (lines 8-31, the introduction and "What is Markdown++?" sections)

  **Approach:**
  - In the resolution paragraph (line 18), expand beyond "invisible to standard Markdown renderers" to name the interchangeability property: Markdown++ files are Markdown files, and the `++` extensions are additive.
  - In the "What is Markdown++?" section (lines 29-31), introduce the tool spectrum concept: a Markdown-only tool sees a valid document, a Markdown++-aware tool unlocks professional publishing, and the author chooses where on that spectrum to operate.
  - Use affirmative framing: "works across the full spectrum" rather than "doesn't break in."
  - Keep additions concise -- 2-4 sentences total across both insertion points. Do not bloat the introduction.

  **Patterns to follow:**
  - Match the whitepaper's assertive, declarative voice
  - Use bold for the term "interchangeability" on first use
  - Use em dashes for asides, consistent with existing style

  **Test scenarios:**
  - The word "interchangeability" (or "interchangeable") appears in the first 31 lines
  - The tool spectrum concept (Markdown-only to Markdown++-aware) is described
  - Existing claims about CommonMark validity and invisible extensions are preserved verbatim or strengthened, not weakened
  - The introduction still reads as a coherent narrative, not a list of features

  **Verification:**
  - Read the modified introduction aloud -- it should flow naturally without feeling like messaging was bolted on

- [x] **Unit 2: Strengthen "Full CommonMark backward compatibility" benefit (R2, R4)**

  **Goal:** Expand the benefits section to communicate that interchangeability means more than "renders cleanly" -- it means authors can use standard tools for their full workflow and add extensions incrementally.

  **Dependencies:** Unit 1 (the concept is now named; this section can reference it)

  **Files:**
  - Modify: `spec/whitepaper.md` (lines 47-58, section "1. Full CommonMark backward compatibility")

  **Approach:**
  - After the tool list (lines 51-56), add a paragraph that reframes the benefit from "works cleanly in these tools" to "these tools are part of your Markdown++ workflow." The point: a GitHub preview or VS Code edit session is not a degraded experience -- it's a valid, productive part of working with Markdown++.
  - Introduce the incremental adoption angle: authors start with plain Markdown and add `++` extensions only where they need professional publishing features.
  - Keep the existing "We are not aware of another documentation format..." closing sentence (line 58) as the section's anchor.

  **Patterns to follow:**
  - The existing section uses a bulleted tool list followed by a summary statement. Add the new paragraph between the list and the closing statement.

  **Test scenarios:**
  - The section communicates incremental adoption: start with Markdown, add extensions where needed
  - The existing tool list and closing comparison statement are unchanged
  - No new terminology is introduced that wasn't established in the introduction (Unit 1)

  **Verification:**
  - The section tells a progression story: backward compatible -> actively usable in standard tools -> incrementally extensible

- [x] **Unit 3: Reinforce in migration paths (R5)**

  **Goal:** Add brief interchangeability reinforcement to migration path sections so teams understand they are not leaving the Markdown ecosystem.

  **Dependencies:** Unit 1 (terminology established)

  **Files:**
  - Modify: `spec/whitepaper.md` (lines 239-271, migration sections)

  **Approach:**
  - The Word migration section (lines 242-247) already touches this concept from PR #4. Verify it aligns with the new framing and adjust if needed.
  - For FrameMaker (lines 249-255) and DITA (lines 257-263) migrations, add a brief sentence to each "What you gain" or closing paragraph reinforcing that the migrated files remain standard Markdown files usable in any Markdown tool.
  - The MDX/AsciiDoc/rST section (lines 265-271) already positions Markdown++ favorably on compatibility. Add one sentence about the tool spectrum if it fits naturally.
  - Keep additions minimal -- one sentence per migration section. These are reinforcement touches, not new subsections.

  **Patterns to follow:**
  - Each migration section follows: "What you gain / What you keep / How you migrate" structure. Interchangeability fits most naturally in "What you gain" or as a closing sentence.

  **Test scenarios:**
  - Each migration section communicates that migrated files work in standard Markdown tools
  - The Word section's existing PR #4 language is preserved or improved, not contradicted
  - No migration section grows by more than 2 sentences

  **Verification:**
  - A reader of any single migration section understands they are gaining capabilities without losing Markdown ecosystem compatibility

- [x] **Unit 4: Reinforce in "Getting started" section (R3)**

  **Goal:** Ensure the Getting Started section makes interchangeability clear to new users -- they can start writing in any editor with no setup, and their files work everywhere.

  **Dependencies:** Unit 1 (terminology established)

  **Files:**
  - Modify: `spec/whitepaper.md` (lines 443-457, "Getting started" section)

  **Approach:**
  - The section's opening line (445) says "Markdown++ is an open documentation format built on CommonMark." Expand this to explicitly state that Markdown++ files are standard `.md` files that work in every Markdown tool.
  - The "Author" bullet (449) says "Open any text editor and start writing." This is already good. Consider adding a brief note that authors can write plain Markdown and add extensions incrementally as their needs grow.
  - Keep changes minimal -- this section is already well-structured as a quick-start guide.

  **Patterns to follow:**
  - The section uses bold labels with em-dash introductions. Follow the same pattern.

  **Test scenarios:**
  - A new user reading only the Getting Started section understands they can start with any Markdown editor and any Markdown knowledge they already have
  - The incremental adoption message appears: start simple, add extensions when needed

  **Verification:**
  - The section answers the question "Do I need special tools to use Markdown++?" with a clear no

- [x] **Unit 5: Add interchangeability guidance to best-practices.md (R6)**

  **Goal:** Add author-facing guidance on incremental adoption and the Markdown/Markdown++ spectrum to the plugin's best practices reference.

  **Dependencies:** Unit 1 (terminology established, though this file can stand alone)

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`

  **Approach:**
  - Add a new subsection near the top of the document (after the opening paragraph at line 8, before "When to Use Each Extension") titled something like "Start with Markdown, extend where needed" or "The interchangeability principle."
  - Content should communicate: (1) every Markdown++ file is a valid Markdown file, (2) authors should start with standard Markdown and add extensions only where they provide value, (3) standard Markdown tools remain part of the workflow.
  - This frames the entire best practices document: the extension-specific guidance that follows is about when to reach for each tool, not about replacing standard Markdown.
  - The existing "Avoid X for" guidance already implies this principle -- the new section makes it explicit.
  - Keep it to 5-10 lines. This is a framing paragraph, not a tutorial.

  **Patterns to follow:**
  - Match the document's direct, advisory tone
  - Use the established "Use/Avoid" pattern if listing guidance points

  **Test scenarios:**
  - The interchangeability principle appears before any extension-specific guidance
  - The guidance is actionable: authors know to start with Markdown and add extensions incrementally
  - The tone matches the rest of the document (advisory, not marketing)

  **Verification:**
  - Reading the new section followed by any extension section (e.g., Variables) should feel like a natural progression from general principle to specific guidance

- [x] **Unit 6: Brief note in syntax-reference.md Base Specification (R6)**

  **Goal:** Establish the interchangeability principle at the top of the syntax reference so authors encounter it before diving into extension syntax.

  **Dependencies:** None (standalone)

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` (lines 10-12, Base Specification section)

  **Approach:**
  - After "Standard CommonMark syntax works as expected" (line 12), add 1-2 sentences noting that Markdown++ extensions are designed to be invisible to standard renderers -- files remain valid `.md` documents that work in any Markdown tool. Extensions activate only when processed by a Markdown++-aware tool.
  - This is a brief factual note, not a marketing paragraph. The syntax reference voice is terse and technical.

  **Patterns to follow:**
  - Match the syntax reference's terse, factual tone
  - No bold emphasis on "interchangeability" here -- save the named concept for the whitepaper and best practices

  **Test scenarios:**
  - The Base Specification section communicates that files remain valid Markdown
  - The note is 1-2 sentences, consistent with the reference's terse style
  - No duplication of the detailed tool spectrum description from the whitepaper

  **Verification:**
  - The section reads as a factual property of the format, not a value proposition

- [x] **Unit 7: Evaluate and optionally reinforce README.md (R3)**

  **Goal:** Assess whether the README benefits from minor interchangeability reinforcement after the whitepaper changes are complete.

  **Dependencies:** Units 1-4 (whitepaper work complete, giving context for what the README should echo)

  **Files:**
  - Modify (conditionally): `README.md` (lines 5-7)

  **Approach:**
  - Re-read the README in context of the completed whitepaper changes.
  - The README already says: "Every Markdown++ file is a valid CommonMark document. No proprietary syntax, no custom file extension, no build step required to preview your content." (line 7)
  - If this already captures the interchangeability message adequately after the whitepaper work, no change is needed.
  - If a brief reinforcement of the spectrum concept or incremental adoption adds value, add at most one sentence.
  - The README should remain concise -- it is a landing page, not a whitepaper.

  **Patterns to follow:**
  - README uses short, punchy sentences. Match that.

  **Test scenarios:**
  - If modified, the README remains under 65 lines
  - The README does not duplicate whitepaper prose verbatim
  - The core value proposition in the first paragraph is strengthened, not diluted

  **Verification:**
  - A reader scanning the README in 30 seconds understands that Markdown++ files work in standard Markdown tools

## System-Wide Impact

- **Interaction graph:** Changes are pure documentation text. No code, build, or CI/CD impacts.
- **Error propagation:** N/A -- no runtime behavior.
- **State lifecycle risks:** None.
- **API surface parity:** The Claude Code skill (`SKILL.md`) references the syntax reference and best practices. No changes to `SKILL.md` are in scope, but the skill will benefit from improved reference content automatically.
- **Integration coverage:** The validation script (`validate-mdpp.py`) is unaffected -- it validates syntax, not prose.

## Risks & Dependencies

- **Voice consistency risk:** New interchangeability prose must match the whitepaper's assertive, declarative voice. Inconsistent tone would undermine the messaging. Mitigation: the implementer should re-read surrounding paragraphs before and after drafting each insertion.
- **Over-messaging risk:** Repeating the interchangeability concept too aggressively could make the whitepaper feel like a marketing document rather than a technical whitepaper. Mitigation: each insertion should be 1-3 sentences. The concept should be named once and then reinforced through specific examples, not restated abstractly.
- **Narrative flow disruption:** Inserting text into an existing narrative risks breaking paragraph transitions. Mitigation: each unit specifies insertion points and the implementer should read the full surrounding section to ensure flow.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-03-30-interchangeability-messaging-requirements.md](../brainstorms/2026-03-30-interchangeability-messaging-requirements.md)
- Related issue: #5
- Related PR: #4 (whitepaper neutralization, which prompted this work)
