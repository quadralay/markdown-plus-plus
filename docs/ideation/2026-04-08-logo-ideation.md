---
date: 2026-04-08
topic: logo
focus: Visual identity and branding for the Markdown++ format
---

# Ideation: Markdown++ Logo

## Codebase Context

**Project shape:** Specification and tooling repo (no application code). Markdown, JSON, Python validation scripts. MIT licensed, hosted at `quadralay/markdown-plus-plus`.

**Visual identity status:** Zero visual assets exist. No PNG, SVG, JPG, ICO, or GIF. No logo, favicon, or color palette. The README uses text-only shields.io badges.

**Brand-relevant differentiators:**
- The "++" naming echoes C++ extending C -- purely additive, backward-compatible
- Core mechanism: HTML comment directives (`<!-- -->`) invisible to standard renderers
- Every Markdown++ file is a valid .md file -- "works everywhere" is the core value prop
- Three-tier graceful degradation (fully graceful / partially / not graceful)
- Messaging deliberately shifted from defensive ("doesn't break") to affirmative ("works everywhere")
- The abbreviation "mdpp" is used alongside "markdown++"
- Format is a standard, not a tool -- the logo represents a specification

**Learnings applied:**
- Interchangeability is the core identity -- "weave, don't isolate" (from `document-interchangeability-messaging-2026-03-30.md`)
- Affirmative framing over defensive (from same)
- Three audiences: decision-makers, developers, AI agents (from `missing-formal-specification-2026-04-08.md`)
- Enterprise adoption is a stated goal -- needs both approachable and serious

**Peer format logos for differentiation:** DITA (geometric), AsciiDoc (geometric), MDX (geometric), rST (geometric), CommonMark (M with down arrow in rounded rectangle)

## Ranked Ideas

### 1. The Hashmark Monogram
**Description:** A `#` symbol geometrically constructed so its overlapping strokes simultaneously read as two `+` signs sharing crossing points. At a glance it's a hash; on second look the ++ emerges. Squared terminals, single weight, geometric precision.
**Rationale:** Dual reading in one symbol -- `#` is Markdown's most iconic character (headings), `++` is the format's increment. Like the FedEx arrow, once you see it you can't unsee it. Generates organic word-of-mouth.
**Downsides:** Requires careful geometric execution to make the dual reading work. Risk of looking like Slack's old # mark if not differentiated. The # meaning may not register for non-Markdown audiences.
**Confidence:** 75%
**Complexity:** Medium
**Status:** Explored

### 2. The Comment Bracket Frame
**Description:** The `<!-- -->` comment delimiters abstracted into a geometric container shape with "M++" or just "++" centered inside. Angular notches on left and right edges evoke comment syntax. Subtle at small sizes, recognizable at larger sizes.
**Rationale:** Encodes the actual technical mechanism directly into the brand mark. No other format can claim this visual. Technical audiences get an instant "aha"; general audiences see a distinctive frame.
**Downsides:** The `<!-- -->` reference may be too inside-baseball for decision-makers. Requires skilled execution to avoid looking like generic angle brackets.
**Confidence:** 70%
**Complexity:** Medium
**Status:** Unexplored

### 3. The Augmented M (MD Icon + ++)
**Description:** The standard Markdown rounded rectangle with "M" and down-arrow, with "++" appended as a superscript in the upper-right corner. The ++ uses a lighter weight or complementary color.
**Rationale:** Instant category recognition. Anyone who knows the Markdown icon immediately parses "Markdown, but more." Zero explanation needed. The safest option with the widest appeal.
**Downsides:** Conservative -- may not be distinctive enough. Superscript ++ may be too small at favicon sizes.
**Confidence:** 85%
**Complexity:** Low
**Status:** Unexplored

### 4. The Elevation Arrow
**Description:** The Markdown "M" with its down-arrow, plus a second arrow pointing upward -- paired arrows creating visual tension. Down = simplify content; Up = elevate to publishing-grade.
**Rationale:** Recontextualizes the existing Markdown icon with a narrative. More memorable than a plain ++ append.
**Downsides:** The original down-arrow was arbitrary. Two arrows in a small space could look cluttered.
**Confidence:** 65%
**Complexity:** Medium
**Status:** Unexplored

### 5. The Layered Documents
**Description:** Two overlapping rounded rectangles -- front solid (plain Markdown), back semi-transparent (publishing layer). The overlap zone uses a blend or third color.
**Rationale:** Universal document metaphor. Directly visualizes the superset/layering model.
**Downsides:** Layered-document icons are common. At favicon size, two shapes may blur. Not specific to Markdown++.
**Confidence:** 60%
**Complexity:** Low
**Status:** Unexplored

### 6. The Standalone ++ Glyph
**Description:** A bold, geometric "++" as the entire icon mark -- two plus signs with the second slightly elevated and offset to the right, creating a rising-step rhythm. No M, no rectangle. Paired with wordmark when space allows.
**Rationale:** The boldest bet. The ++ operator means increment -- take what exists and advance it. The rising offset conveys progress. Works at every size.
**Downsides:** Without context, "++" could mean anything. Requires wordmark pairing. Not immediately tied to Markdown.
**Confidence:** 55%
**Complexity:** Low
**Status:** Explored

### 7. The mdpp Ligature
**Description:** "mdpp" in a custom-drawn typeface where the two p's share a single vertical stroke. "md" primary weight; "pp" bolder or accented. Optionally in a pill shape for badges.
**Rationale:** The abbreviation is already in use. Four characters work as file extension, CLI command, package name, badge.
**Downsides:** Wordmarks are harder to make iconic. "mdpp" lacks immediate meaning. Ligature detail lost at small sizes.
**Confidence:** 50%
**Complexity:** Medium
**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Iceberg Glyph | Wrong tone (icebergs sink ships). Too complex at small sizes |
| 2 | Spectrum/Gradient Mark | Gradients fail in monochrome. Too abstract |
| 3 | Invisible Ink Quill | Writing implement doesn't scale to favicon |
| 4 | Plus-Plus Reveal | Micro-typography only works at poster size |
| 5 | Heritage Serif | Serif vs sans-serif distinction lost at small sizes |
| 6 | Pilcrow-Plus Seal | Pilcrow too obscure for developer audience |
| 7 | Dollar Wink ($;) | Too playful for enterprise. Uses least graceful syntax |
| 8 | Null Transform | Phase-transition effects can't render as static mark |
| 9 | Invisible Ink Stamp | Empty center works against recognition |
| 10 | Diff Mark | Green + looks like git diff, not format identity |
| 11 | Open Bracket Mark | Incomplete rectangle looks broken, not open |
| 12 | Superscript Specter | Ghost/transparency fails in monochrome and small sizes |
| 13 | Pass-Through Mark | Too complex for favicon, needs explanation |
| 14 | Chevron >> Mark | Too generic -- fast-forward, shell redirect. Not ownable |
| 15 | Bracket Window `<md++>` | Reads like HTML tag but format uses comments. Misleading |

## Session Log
- 2026-04-08: Initial ideation -- 39 candidates generated across 5 frames (typography, metaphor, heritage, enterprise, boldness), deduped to 22 unique, 7 survived adversarial filtering. User selected #1 (Hashmark Monogram) and #6 (Standalone ++ Glyph) for brainstorming.
- 2026-04-08: Brainstormed #1 (Hashmark Monogram) -- requirements doc at `docs/brainstorms/2026-04-08-hashmark-monogram-logo-requirements.md`. Key decisions: ++ reading primary, # secondary; standalone icon; monochrome baseline; must differentiate from Slack's old #.
- 2026-04-08: Brainstormed #6 (Standalone ++ Glyph) -- requirements doc at `docs/brainstorms/2026-04-08-standalone-plus-plus-logo-requirements.md`. Key decisions: rising-step layout; geometric precision; pure ++ with no Markdown reference; same constraints as #1.
