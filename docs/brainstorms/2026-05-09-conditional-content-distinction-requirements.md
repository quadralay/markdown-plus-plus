---
date: 2026-05-09
topic: conditional-content-distinction
---

# Whitepaper: Distinguish Markdown++ Inline Conditional Directives from DITA's Attribute-Filter Model

## Problem Frame

The whitepaper currently presents Markdown++ conditional content and DITA conditional processing as parallel mechanisms expressed in different syntaxes. Two locations carry the topic — §4 defines the directive (line 112) and §7's comparison table juxtaposes `@audience`/`@platform` attributes against `<!-- condition: -->` (line 151) — but neither surfaces the structural difference that matters to evaluating teams.

Markdown++ wraps content directly with inline directives; DITA tags content with attributes and resolves them at build time via separate DITAVAL filter files. The mechanisms produce meaningfully different authoring, review, and maintenance experiences, and that difference is part of why technical writers find Markdown++ conditional content easier to maintain. The whitepaper should make this design distinction visible without changing any spec mechanics.

## Requirements

- R1. Add a short paragraph in `spec/whitepaper.md` §7 immediately after the comparison table (around line 162) that elaborates on the inline-vs-filter distinction for conditional content. The paragraph must describe locality, diff visibility, and authoring ergonomics as the practical consequences.
- R2. Frame the distinction as a difference in design philosophy — inline gating vs. attribute filtering with external rules — not as a value judgment. Both approaches must be presented as valid.
- R3. Add a brief clause to the conditional content bullet in §4 (line 112) noting that the directive wraps content inline, contrasting with attribute-based filter systems used by XML formats. The clause must be short enough that the bullet remains readable.
- R4. Tone must match the whitepaper's existing DITA-respectful framing (e.g., the §7 paragraph beginning at line 162 that acknowledges "DITA's ecosystem tooling remains deeper").
- R5. No changes to spec mechanics, the directive syntax, or any Markdown++ extension behavior. Migration Paths (§"From DITA XML") requires no edits — it already correctly maps DITA conditional processing to `<!-- condition: -->`.

## Success Criteria

- A reader of §7 understands that the difference between Markdown++ and DITA conditional content is not just syntax but a structural choice about where condition logic lives (next to content vs. in external filter files).
- A reader of §4 encounters the inline-locality property at the point the directive is introduced.
- The whitepaper continues to present DITA fairly — the new prose elaborates on a design distinction without disparaging attribute-filter systems.
- No directive examples, syntax descriptions, or migration guidance is altered.

## Scope Boundaries

- Out of scope: editing the comparison table row itself (the two-cell `@audience` vs. `<!-- condition: -->` summary is correct as-is).
- Out of scope: adding DITAVAL syntax examples or DITA configuration details. The paragraph names DITAVAL only as the location where DITA's filter rules live.
- Out of scope: any change to §"From DITA XML" Migration Paths text.
- Out of scope: any spec or extension mechanic change.
- Out of scope: marketing claims about which approach is "better." The text frames trade-offs neutrally.

## Key Decisions

- **Both locations get touched, but with different weights.** A substantive paragraph lands in §7 (the natural home for DITA comparison elaboration); a single clause lands in §4 (establishes the inline-locality property at first introduction). This avoids bloating §4's bullet list while keeping the design choice visible early.
- **§7 paragraph placed after the table, not inside it.** A new table row would force terse phrasing that loses the design-philosophy framing. A paragraph below the table is the established pattern (the existing post-table paragraph already discusses what DITA features Markdown++ does not cover).
- **Three named consequences: locality, diff visibility, authoring ergonomics.** These are the differences the issue identifies and the differences technical writing teams notice in practice. They cover review-time, edit-time, and runtime experiences without overlapping.
- **Affirmative, neutral framing.** The paragraph names what is true about each approach rather than ranking them. This is consistent with the document-interchangeability messaging conventions used elsewhere in the whitepaper.

## Assumptions

These were inferred without user confirmation in autonomous mode and should be validated during planning or review:

- **Both placements are wanted.** The issue presents the two locations as either/or with no strong preference. The doubled-up approach (clause in §4, paragraph in §7) is my judgment about the highest-value change. If reviewer feedback prefers a single location, the §7 paragraph alone is the higher-leverage half.
- **DITAVAL is the right anchor term.** The issue uses "DITAVAL filter files" as the canonical name for DITA's external rule files. I assume the whitepaper audience either knows this term or accepts it as a precise pointer. If the term is too DITA-insider, "external filter rules" is an acceptable substitute.
- **No table row split.** Splitting the conditional content row into a multi-row breakdown would mechanically encode the locality/diff/ergonomics distinction but at the cost of readability and table consistency. I keep the table single-row and explain the distinction in prose.

## Next Steps

→ Proceed directly to work — scope is lightweight, deliverables are well-defined, and assumptions are recorded for review.
