---
date: 2026-05-09
status: active
type: docs
origin: docs/brainstorms/2026-05-09-conditional-content-distinction-requirements.md
---

# docs: Distinguish Markdown++ inline conditional directives from DITA's attribute-filter model

## Summary

Surface the structural difference between Markdown++ conditional content (inline directives that wrap content) and DITA conditional processing (content attributes resolved against external DITAVAL filter rules) in `spec/whitepaper.md`. Two edits: a brief inline-locality clause in §4's conditional content bullet, and a substantive paragraph after §7's comparison table elaborating locality, diff visibility, and authoring ergonomics. No spec mechanics change.

## Problem Frame

The whitepaper currently presents the two conditional-content mechanisms as parallel capabilities expressed in different syntaxes. §4 line 112 defines the directive; §7 line 151 juxtaposes `@audience`/`@platform` attributes against `<!-- condition: -->` in a comparison row. Neither location surfaces the design distinction that matters to evaluating teams: where condition logic lives. Markdown++ keeps the condition next to the content it gates; DITA splits the condition across content attributes and external DITAVAL filter rules. That structural difference is part of why technical writers find Markdown++ conditional content easier to maintain, and the whitepaper should make it visible.

## Requirements

Carried forward from `docs/brainstorms/2026-05-09-conditional-content-distinction-requirements.md`:

- **R1.** Add a short paragraph in `spec/whitepaper.md` §7 immediately after the comparison table (around line 162) elaborating the inline-vs-filter distinction. The paragraph must name locality, diff visibility, and authoring ergonomics as practical consequences.
- **R2.** Frame the distinction as a difference in design philosophy — inline gating vs. attribute filtering with external rules — not as a value judgment. Both approaches must be presented as valid.
- **R3.** Add a brief clause to the conditional content bullet in §4 (line 112) noting that the directive wraps content inline, contrasting with attribute-based filter systems used by XML formats. The clause must keep the bullet readable.
- **R4.** Tone must match the whitepaper's existing DITA-respectful framing (e.g., the existing §7 paragraph at line 162 acknowledging "DITA's ecosystem tooling remains deeper").
- **R5.** No changes to spec mechanics, directive syntax, or any Markdown++ extension behavior. Migration Paths (§"From DITA XML") requires no edits.

---

## Key Technical Decisions

- **Both locations get touched, with different weights.** §7 takes a substantive paragraph (the natural home for DITA comparison elaboration); §4 takes a single clause (establishes the inline-locality property at first introduction). Carried from origin.
- **§7 paragraph placed after the existing post-table paragraph, not inside the table.** A new table row would force terse phrasing that loses the design-philosophy framing. The whitepaper already establishes "elaborating paragraph after the table" as the pattern (the existing line-162 paragraph discusses what DITA features Markdown++ does not cover). The new paragraph follows that same paragraph rather than displacing it, so DITA-respectful framing remains the closing note of the table commentary.
- **Three named consequences: locality, diff visibility, authoring ergonomics.** These are the differences the issue identifies and the differences technical writing teams notice in practice. They cover review-time, edit-time, and runtime experiences without overlapping.
- **Anchor term: "DITAVAL filter files".** Use the canonical DITA term per origin. The whitepaper already references DITA tooling and ecosystem terms; readers who don't know DITAVAL specifically still get a precise pointer to "external rule file."
- **Affirmative, neutral framing.** Name what is true about each approach rather than ranking them. Consistent with the document-interchangeability conventions used elsewhere in the whitepaper.

---

## Scope Boundaries

**In scope:**

- Edits to `spec/whitepaper.md` §4 (line 112 bullet) and §7 (paragraph insertion after the existing post-table commentary near line 162).

**Out of scope (carried from origin):**

- Editing the comparison table row itself — the two-cell `@audience` vs. `<!-- condition: -->` summary is correct as-is.
- Adding DITAVAL syntax examples or DITA configuration details. The paragraph names DITAVAL only as the location where DITA's filter rules live.
- Any change to §"From DITA XML" Migration Paths text.
- Any spec or extension mechanic change.
- Marketing claims about which approach is "better." Trade-offs framed neutrally.

### Deferred to Follow-Up Work

None. The plan is single-PR scope.

---

## Implementation Units

### U1. Add inline-locality clause to §4 conditional content bullet

**Goal:** Establish the inline-locality property at the point the directive is introduced, so a reader of §4 encounters the design choice early.

**Requirements:** R3, R2, R4.

**Dependencies:** None.

**Files:**

- `spec/whitepaper.md` (modify line 112)

**Approach:**

- Append a short clause to the existing conditional content bullet that names two facts: (a) the directive wraps content inline, and (b) this contrasts with attribute-based filter systems used by XML formats.
- Keep the bullet to roughly the same visual weight as its siblings (custom styles, variables, metadata markers, multiline tables) so the bulleted list still reads as a feature inventory rather than a comparison essay.
- Do not name DITAVAL in §4 — save the canonical term for §7 where it has room to land properly. §4 says "attribute-based filter systems used by XML formats" and §7 elaborates.

**Patterns to follow:**

- Existing bullets in §4 (lines 110–114) use the format: `**Name** -- short syntax example, then a clause stating the capability.` Match that rhythm.
- Tone matches the whitepaper's existing DITA-respectful posture (the §7 line-162 paragraph is the canonical reference for tone).

**Test scenarios:**

Test expectation: none -- this is a prose edit to a specification narrative document. Verification is editorial review (see U3).

**Verification:**

- The bullet remains a single-paragraph item readable at a glance.
- A reader of §4 alone (without continuing to §7) leaves with the inline-locality concept.
- The clause does not name "DITAVAL" or any DITA-specific configuration vocabulary.

---

### U2. Add inline-vs-filter elaboration paragraph after §7 comparison table

**Goal:** Make the structural design distinction visible to a reader of §7, going beyond the table's two-cell summary by naming the practical consequences a documentation team would feel.

**Requirements:** R1, R2, R4, R5.

**Dependencies:** None (independent of U1; either can land first).

**Files:**

- `spec/whitepaper.md` (insert after the existing post-table paragraph that ends near line 162)

**Approach:**

- Insert a new paragraph **after** the existing line-162 paragraph (the one that begins "For the capabilities that most technical writing teams use daily..." and ends with "A Markdown++ file reads like a document."). The existing paragraph remains the immediate post-table commentary; the new paragraph extends it with the conditional-content-specific design distinction.
- Open by naming the design distinction explicitly: Markdown++ wraps content with inline directives; DITA tags content with attributes (`@audience`, `@platform`, `@product`) and resolves them at build time via separate DITAVAL filter files.
- Then name the three practical consequences in order — locality, diff visibility, authoring ergonomics — each in one or two sentences. Stay concrete: locality means the condition lives next to the content it gates; diff visibility means a single-location change with a clear diff vs. paired changes across content and DITAVAL; authoring ergonomics means a writer editing the file sees what is conditional vs. reasoning about how each filter file resolves the attributes.
- Close by framing both approaches as valid design choices addressing the same need with different philosophies. Match the closing-clause cadence of the existing line-162 paragraph ("...remains deeper. For teams that need structured content without XML overhead, the readability gap is enormous.").

**Patterns to follow:**

- The existing line-162 paragraph is the tone and structure template: it acknowledges DITA's strengths, names a specific trade-off, frames it neutrally, and ends with an affirmative observation about Markdown++.
- Avoid bulleted formatting for the three consequences. The whitepaper uses prose for design-distinction elaboration and reserves bullets for feature inventories.
- Reuse vocabulary the whitepaper already establishes ("structured content," "build time," "source files") rather than introducing new terms.

**Test scenarios:**

Test expectation: none -- prose edit. Verification is editorial review (see U3).

**Verification:**

- A reader of §7 understands that the difference is not just syntax but a structural choice about where condition logic lives.
- All three consequences (locality, diff visibility, authoring ergonomics) are named in the paragraph.
- DITA is described accurately and respectfully — the paragraph does not characterize DITAVAL as a flaw, only as a different placement of the same logic.
- The paragraph reads as continuous with the existing post-table prose; a reader would not perceive a tonal shift.

---

### U3. Editorial review pass

**Goal:** Confirm both edits land correctly in their target locations, preserve whitepaper tone, and do not introduce contradictions with adjacent sections (§"From DITA XML" Migration Paths in particular).

**Requirements:** R4, R5.

**Dependencies:** U1, U2.

**Files:**

- `spec/whitepaper.md` (read-through, no further edits unless U1 or U2 introduced an issue)

**Approach:**

- Read §4 lines 106–116 in full to confirm the modified bullet sits naturally next to its siblings.
- Read §7 lines 144 through the new paragraph in full to confirm the new paragraph follows the existing post-table paragraph cleanly without redundancy.
- Re-check §"From DITA XML" Migration Paths to confirm it still maps DITA conditional processing to `<!-- condition: -->` correctly and does not contradict the new prose.
- Confirm no spec mechanics, directive syntax, or extension behavior was altered.

**Test scenarios:**

Test expectation: none -- editorial review. The check is a human read-through.

**Verification:**

- §4 bullet list still reads as a scannable feature inventory.
- §7 new paragraph extends the existing post-table commentary without duplicating its observations.
- Migration Paths section is unchanged and remains internally consistent with the new framing.
- The whitepaper's frontmatter (`status: draft`) and date remain untouched — this is content evolution within the existing draft, not a status promotion.

---

## Risks

- **Risk: Tone drift toward marketing claims.** The "Markdown++ vs. DITA" framing is easy to tilt into product advocacy. Mitigated by (a) the affirmative-neutral framing decision above, (b) following the existing line-162 paragraph as a tone template, and (c) the editorial review pass in U3 specifically checking against the whitepaper's DITA-respectful posture.
- **Risk: Inaccurate characterization of DITAVAL.** DITAVAL is a real DITA mechanism with specific semantics. The plan deliberately keeps the prose at the level of "external filter rules" rather than DITAVAL syntax detail, so the risk of misrepresenting DITAVAL behavior stays low. The single canonical-term mention ("separate DITAVAL filter files") is accurate as a description of where the rules live.
- **Risk: §4 bullet bloat.** Adding a clause to one bullet in a five-bullet inventory could make that bullet visually dominant. Mitigated by keeping the clause short (roughly one sentence fragment) and reviewing the bulleted list as a whole in U3.

---

## Verification

- Both edits land in `spec/whitepaper.md` — §4 bullet (U1) and §7 post-table paragraph (U2).
- The whitepaper reads cleanly end-to-end through §4 and §7 with the new prose in place.
- No directive examples, syntax descriptions, or migration guidance is altered.
- The `spec/whitepaper.md` frontmatter is unchanged.
