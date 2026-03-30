---
title: "docs: Neutralize WebWorks product references in whitepaper"
type: docs
status: completed
date: 2026-03-30
origin: docs/brainstorms/2026-03-30-neutralize-whitepaper-requirements.md
---

# docs: Neutralize WebWorks product references in whitepaper

## Overview

Remove WebWorks product references (ePublisher, AutoMap, Reverb) from `spec/whitepaper.md` so the whitepaper presents Markdown++ as a vendor-neutral open documentation format. Update stale links to point to this repo. Soften marketing tone in the historical section while preserving factual origin context.

## Problem Frame

The whitepaper is the public-facing introduction to Markdown++. It currently contains WebWorks product names, ePublisher sales pitches, and a stale link to the `webworks-claude-skills` plugin (which no longer contains the Markdown++ skill after PR #2 migration). These references undermine Markdown++'s positioning as an open format. (see origin: `docs/brainstorms/2026-03-30-neutralize-whitepaper-requirements.md`)

## Requirements Trace

- R1. Replace "WebWorks AutoMap" reference (~line 120) with generic "command-line build tools" language
- R2. Neutralize ePublisher multi-format output section (~lines 128-135) — keep format list, remove product branding, describe Reverb generically as "responsive HTML5 online help"
- R3. Replace ePublisher-specific Word migration guidance (~line 246) with generic publishing tool language
- R4. Remove/rewrite "Try it" ePublisher sales pitch (~line 450) with vendor-neutral publishing bullet
- R5. Remove "Already using ePublisher?" sales pitch bullet (~line 452)
- R6. Update tooling link (~line 454) from `webworks-claude-skills` to this repo's `markdown-plus-plus` plugin
- R7. Update "Learn the syntax" link (~line 446) to point to in-repo syntax reference
- R8. Soften historical section tone (~lines 33-43) — preserve factual origin story, reduce marketing feel

## Scope Boundaries

- **In scope:** Text edits to `spec/whitepaper.md` only
- **Not in scope:** Plugin, skill, script, or example file changes
- **Not in scope:** Restructuring or rewriting beyond vendor neutrality
- **Preserve:** All WebWorks/Quadralay mentions in the historical section (R8) as factual context
- **Preserve:** The whitepaper's persuasive tone advocating for Markdown++ adoption

## Context & Research

### Relevant Code and Patterns

- `spec/whitepaper.md` — the sole file to edit (459 lines, frontmatter date `2026-03-28`, status `draft`)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` — confirmed to exist; target for R7 link update
- Repo URL for R6: `https://github.com/quadralay/markdown-plus-plus`

### Institutional Learnings

- None — no `docs/solutions/` directory exists in this repo

## Key Technical Decisions

- **Generic output format descriptions (R2):** Replace branded names with descriptive terms — "Reverb 2.0" becomes "responsive HTML5 online help," product-specific generation capability sentence is removed entirely. The format list itself (HTML help, PDF, Dynamic HTML, CHM, Eclipse Help) stays as examples of what publishing tools can target.
- **Word migration rewrite (R3):** Describe the capability generically ("a publishing tool that supports both Word input and Markdown++ output") without naming ePublisher. Keep the migration path credible.
- **Sales bullet handling (R4, R5):** R4 gets rewritten as a vendor-neutral "publish" bullet describing multi-format output capability. R5 is removed entirely — there is no vendor-neutral equivalent of "already using ePublisher?"
- **Syntax reference link format (R7):** Use a relative GitHub-friendly path or reference the repo's examples. The syntax reference lives at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` — link text should reference this repo's documentation rather than external ePublisher docs.
- **Historical section approach (R8):** Light-touch tone edits only. The three subsection paragraphs (Structured authoring, Online help output, Markdown and Markdown++) contain factual history that establishes credibility. Soften phrases that read as company marketing ("the product of Quadralay / WebWorks" → more neutral framing) while keeping all factual claims.

## Implementation Units

- [x] **Unit 1: Neutralize body references (R1, R2, R3)**

  **Goal:** Replace WebWorks product names in the CI/CD bullet (R1), multi-format output section (R2), and Word migration section (R3) with vendor-neutral language.

  **Requirements:** R1, R2, R3

  **Dependencies:** None

  **Files:**
  - Modify: `spec/whitepaper.md`

  **Approach:**
  - R1 (~line 120): Replace `(such as WebWorks AutoMap)` with generic phrasing, e.g., "Command-line build tools run automated builds..."
  - R2 (~lines 128-135): Rewrite the section opener from "WebWorks ePublisher, for example, produces:" to a generic "A Markdown++ publishing pipeline can produce:" framing. Replace "WebWorks Reverb 2.0" with "Responsive HTML5 online help" and its description with a generic one (full-text search, TOC, index). Remove the Reverb lineage parenthetical. Remove the final sentence about ePublisher generating Markdown++ from other formats (product-specific capability). Keep the remaining format entries (PDF, Dynamic HTML, CHM, Eclipse Help) with their existing descriptions.
  - R3 (~line 246): Replace "If you already use ePublisher to process Word documents, the migration path is direct. ePublisher generates Markdown++ output from Word input..." with generic language about publishing tools that support Word-to-Markdown++ conversion.

  **Verification:**
  - No occurrences of "ePublisher" or "AutoMap" outside lines 33-43
  - The multi-format output section lists the same formats but without product branding
  - The Word migration section describes the same capability generically

- [x] **Unit 2: Rewrite Getting Started section (R4, R5, R6, R7)**

  **Goal:** Remove sales pitches, update stale links, and make the Getting Started section vendor-neutral.

  **Requirements:** R4, R5, R6, R7

  **Dependencies:** None (can be done in parallel with Unit 1)

  **Files:**
  - Modify: `spec/whitepaper.md`

  **Approach:**
  - R7 (~line 446): Replace the ePublisher docs URL with a link to the syntax reference in this repo. Use a GitHub-relative link to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` or reference the repo's documentation.
  - R4 (~line 450): Rewrite the "Try it" bullet as a vendor-neutral "Publish" bullet describing that publishing tools process Markdown++ into multiple output formats (HTML, PDF, CHM, etc.).
  - R5 (~line 452): Remove the "Already using ePublisher?" bullet entirely.
  - R6 (~line 454): Replace `[webworks-claude-skills](https://github.com/quadralay/webworks-claude-skills)` with `[markdown-plus-plus](https://github.com/quadralay/markdown-plus-plus)` and update the description to reflect AI-assisted authoring with Markdown++ syntax awareness (drop ePublisher project management and AutoMap build automation mentions).

  **Verification:**
  - "Learn the syntax" link points to this repo's syntax reference
  - No "free trial" or sales language remains
  - "Already using ePublisher?" bullet is gone
  - Tooling link points to `quadralay/markdown-plus-plus`

- [x] **Unit 3: Soften historical section tone (R8)**

  **Goal:** Adjust marketing-tone phrases in the historical section (~lines 33-43) so it reads as credibility context rather than a company pitch.

  **Requirements:** R8

  **Dependencies:** None (can be done in parallel with Units 1-2)

  **Files:**
  - Modify: `spec/whitepaper.md`

  **Approach:**
  - Review each paragraph in the section for phrases that read as promotional rather than contextual
  - The opening paragraph (~lines 33-35) is the primary target — "It is the product of Quadralay / WebWorks" and "a company that has been solving technical publishing problems since the early 1990s" could be softened to emphasize the format's heritage rather than the company
  - The three subsection paragraphs (Structured authoring, Online help output, Markdown and Markdown++) are mostly factual history — apply minimal changes, only where wording crosses from "here's where this expertise comes from" into "here's why WebWorks is great"
  - The closing paragraph (~line 43) "Markdown++ is not theoretical -- it is production software with a long lineage" is format-focused and can stay
  - Keep all factual claims (dates, product generations, format support timeline)

  **Verification:**
  - WebWorks/Quadralay names remain in this section (they are factual)
  - Section reads as origin story / credibility context
  - No factual claims were removed or altered

- [x] **Unit 4: Update frontmatter date**

  **Goal:** Update the whitepaper's frontmatter date to reflect the edit date.

  **Requirements:** Repo convention (CLAUDE.md)

  **Dependencies:** Units 1-3

  **Files:**
  - Modify: `spec/whitepaper.md`

  **Approach:**
  - Change `date: 2026-03-28` to `date: 2026-03-30`

  **Verification:**
  - Frontmatter `date` field is `2026-03-30`

## Risks & Dependencies

- **Line number drift:** The brainstorm references specific line numbers. These should be verified against the current file before editing (confirmed accurate as of this plan's writing).
- **Tone subjectivity (R8):** "Marketing tone" is subjective. The approach is conservative — only change phrases that clearly read as promotional rather than contextual. When in doubt, preserve the original wording.
- **Link format (R7):** GitHub renders relative links from the repo root. The syntax reference path is long (`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`). Consider linking to the repo root or examples directory as an alternative if the deep path is unwieldy in the whitepaper context.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-03-30-neutralize-whitepaper-requirements.md](../brainstorms/2026-03-30-neutralize-whitepaper-requirements.md)
- **Target file:** `spec/whitepaper.md`
- **Syntax reference:** `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- Related issue: #3
- Related PR: #2 (migration of Markdown++ skill to this repo)
