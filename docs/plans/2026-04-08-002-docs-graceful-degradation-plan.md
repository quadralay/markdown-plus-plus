---
title: "docs: Document graceful degradation behavior for each extension"
type: docs
status: active
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-graceful-degradation-requirements.md
---

# docs: Document graceful degradation behavior for each extension

## Overview

Add systematic documentation of how each Markdown++ extension renders in standard CommonMark viewers (GitHub, VS Code, MkDocs). The work spans three artifacts: a spec appendix with the full degradation matrix, a whitepaper summary paragraph, and per-section "CommonMark rendering" notes in the syntax reference.

## Problem Frame

Markdown++ positions CommonMark backward compatibility as a core value proposition. The whitepaper claims files "render cleanly in GitHub, VS Code, MkDocs, and any other Markdown viewer." However, degradation is not uniform -- some extensions are truly invisible, others leave visible artifacts, and some lose content entirely. Authors, reviewers, and teams evaluating Markdown++ have no systematic reference for what each extension looks like in a plain CommonMark renderer. (see origin: docs/brainstorms/2026-04-08-graceful-degradation-requirements.md)

## Requirements Trace

- R1. Create a spec appendix (`spec/graceful-degradation.md`) with a degradation matrix covering syntax, CommonMark behavior, and a graceful/partial/no rating
- R2. Cover all eleven extension categories: custom styles, custom aliases, markers, conditions, file includes, variables, multiline tables, combined commands, inline styles, content islands, and link references
- R3. Categorize into three tiers: Fully graceful, Partially graceful, Not graceful
- R4. For partially and not-graceful extensions, describe the specific artifact or gap
- R5. Add a summary paragraph to the whitepaper's compatibility section acknowledging degradation tiers with a link to the appendix
- R6. Add "CommonMark rendering" notes to each extension section in the syntax reference

## Scope Boundaries

- Out of scope: changing extension syntax to improve degradation
- Out of scope: building tooling to preview degradation
- Out of scope: testing against specific renderers (the matrix describes CommonMark-spec behavior)

## Context & Research

### Relevant Code and Patterns

- `spec/whitepaper.md` -- Section "1. Full CommonMark backward compatibility" (line 47) is the natural insertion point for a degradation summary paragraph
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` -- Each extension has a dedicated section ending before a `---` separator; notes go at the end of each section
- `spec/graceful-degradation.md` -- New file, placed alongside `whitepaper.md` in `spec/`

### Institutional Learnings

- `docs/solutions/documentation-gaps/document-interchangeability-messaging-2026-03-30.md` -- Established the affirmative framing principle: describe what renders and how, not what "breaks." This directly informs the tone of degradation descriptions.
- The interchangeability solution doc also established the distinction between HTML comment invisibility and inline token pass-through behavior, which is the foundation of the degradation tiers.

## Key Technical Decisions

- **Affirmative framing**: Describe what renders and how, consistent with the interchangeability messaging established in earlier work. Avoid defensive language like "breaks" or "fails" (see origin: docs/brainstorms/2026-04-08-graceful-degradation-requirements.md, Key Decisions).
- **Three-tier system**: Fully graceful / Partially graceful / Not graceful. Intuitive, matches the issue proposal, and maps cleanly to the two extension mechanisms (HTML comments = invisible, inline tokens = visible).
- **Spec appendix as primary artifact**: The full matrix belongs in `spec/` where it can be referenced from both the whitepaper and syntax reference without duplicating content.
- **Inline notes over cross-reference columns**: Rather than adding a column to existing tables in the syntax reference, add a bold "CommonMark rendering:" note at the end of each extension section. This is less disruptive to the existing table layouts and provides space for nuanced descriptions.
- **Link references coverage**: Link references are standard Markdown syntax, not a Markdown++ extension section in the syntax reference. They are covered in the spec appendix matrix (R2) but do not need a syntax reference note (R6) since there is no dedicated section for them.

## Implementation Units

- [x] **Unit 1: Create spec appendix with degradation matrix**

**Goal:** Create `spec/graceful-degradation.md` with the full per-extension degradation matrix, tier definitions, and author implications.

**Requirements:** R1, R2, R3, R4

**Dependencies:** None

**Files:**
- Create: `spec/graceful-degradation.md`

**Approach:**
- Open with a design principle section explaining the two extension mechanisms (HTML comments vs. inline tokens)
- Matrix table with columns: Extension, Syntax Example, CommonMark Rendering, Rating
- Order extensions by degradation tier (fully graceful first, then partial, then not graceful)
- Follow with tier definitions and an "Implications for Authors" section using three categories: "Use freely," "Use with awareness," "Use deliberately"
- Use affirmative framing throughout

**Patterns to follow:**
- Affirmative framing from the interchangeability solution doc
- Spec file structure: YAML frontmatter with date/status, then content

**Test scenarios:**
- All 11 extensions from R2 appear in the matrix
- Each partially and not-graceful extension has a specific artifact description (R4)
- Tier summaries list the correct extensions in each category

**Verification:**
- Matrix contains exactly 11 rows (one per extension category)
- Three tiers are defined with extension lists
- Language uses affirmative framing, not defensive

- [x] **Unit 2: Add degradation summary to whitepaper**

**Goal:** Add a paragraph to the whitepaper's compatibility section that acknowledges the degradation spectrum and links to the appendix.

**Requirements:** R5

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/whitepaper.md`

**Approach:**
- Insert a paragraph after the "productive parts of a Markdown++ workflow" statement (line 58) and before "We are not aware of another documentation format..."
- Briefly distinguish comment-based extensions (fully hidden), inline tokens (literal text), and processing-dependent content (absent)
- Link to `graceful-degradation.md` for the full breakdown
- Keep it to one paragraph -- the appendix has the detail

**Patterns to follow:**
- Whitepaper's existing tone and structure
- Relative link format: `[Graceful Degradation appendix](graceful-degradation.md)`

**Test scenarios:**
- Paragraph does not undermine the "renders cleanly" claim but qualifies it accurately
- Link to appendix resolves correctly (same directory)

**Verification:**
- New paragraph exists between lines 58-62 area
- Contains link to `graceful-degradation.md`

- [x] **Unit 3: Add CommonMark rendering notes to syntax reference**

**Goal:** Add a "CommonMark rendering" note to each extension section in the syntax reference so authors encounter degradation info at point of use.

**Requirements:** R6

**Dependencies:** Unit 1 (for consistent descriptions)

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

**Approach:**
- Add a bold `**CommonMark rendering:**` note at the end of each extension section, before the `---` separator
- Use consistent format across all sections
- Keep each note to 1-2 sentences -- brief and factual
- Sections to annotate: Variables, Custom Styles, Custom Aliases, Conditions, File Includes, Markers, Multiline Tables, Combined Commands, Inline Styles, Content Islands (10 sections)
- Link references are not a separate section, so no note needed there

**Patterns to follow:**
- Match the description text from the spec appendix for consistency
- Bold prefix pattern: `**CommonMark rendering:**` followed by the note

**Test scenarios:**
- All 10 extension sections in the syntax reference have a CommonMark rendering note
- Notes are consistent with the spec appendix descriptions
- No note contradicts the appendix matrix

**Verification:**
- Grep for `**CommonMark rendering:**` returns 10 matches in syntax-reference.md
- Each note appears at the logical end of its section

- [x] **Unit 4: Bump plugin version**

**Goal:** Bump the plugin version to reflect the documentation update.

**Requirements:** None (convention)

**Dependencies:** Units 1-3

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`

**Approach:**
- Patch bump (1.1.5 → 1.1.6) since this is a documentation update with no new features or breaking changes

**Verification:**
- Both files show the same version number

## System-Wide Impact

- **Interaction graph:** No code changes. Documentation-only impact across three files.
- **Error propagation:** N/A
- **State lifecycle risks:** N/A
- **API surface parity:** N/A
- **Integration coverage:** Cross-file link from whitepaper to appendix must resolve correctly (both in `spec/` directory).

## Risks & Dependencies

- **Whitepaper tone**: The degradation paragraph must qualify the "renders cleanly" claim without undermining the marketing message. The affirmative framing approach from prior work mitigates this.
- **Consistency**: Syntax reference notes must match the spec appendix. Writing the appendix first (Unit 1) and using it as the source of truth for Unit 3 ensures consistency.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-graceful-degradation-requirements.md](../brainstorms/2026-04-08-graceful-degradation-requirements.md)
- Related solution: [docs/solutions/documentation-gaps/document-interchangeability-messaging-2026-03-30.md](../solutions/documentation-gaps/document-interchangeability-messaging-2026-03-30.md)
- Related issue: #12
