---
title: "docs: Cross-reference documentation audit -- when, why, and how to use the triple"
type: docs
status: active
date: 2026-05-22
origin: docs/brainstorms/2026-05-22-cross-reference-when-why-how-audit.md
---

# docs: Cross-reference documentation audit -- when, why, and how to use the triple

## Summary

Edit eight cross-reference doc surfaces so a reader with a working
custom-anchor + inline-link setup can answer "what does the triple add for me?"
without cross-referencing other surfaces. Land the canonical treatment in
`references/best-practices.md` (labeled benefit groups, two slug variants
with a *Choosing the slug* subsection, an inline-anchor-vs-triple comparison,
and an agent/pipeline callout); update every other surface as a lighter pointer
to that canonical home; bump the plugin to 1.6.3 with a CHANGELOG entry.

---

## Problem Frame

The brainstorm
([`docs/brainstorms/2026-05-22-cross-reference-when-why-how-audit.md`](../brainstorms/2026-05-22-cross-reference-when-why-how-audit.md))
documents five doc gaps that all land on the same reader: someone with
unique-by-construction generated anchors and within-assembly inline anchor
links who cannot tell from any current surface what the triple adds for them.
The fix is documentation-only -- no syntax change, no validator change, no
new spec rule. The triple's *adjacent placement* (settled by #103) and
*term name* (settled by #99) are untouched.

---

## Requirements

- R1. Restructure `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings* as the canonical treatment, with four sub-changes (R1.a-R1.d).
- R2. Reframe the `GLOSSARY.md` § *triple* entry so cross-context resolution leads and rename-survival is one of several anti-drift benefits.
- R3. Tighten `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` § *Custom Aliases / Recommended pattern* with a slug-variant pointer and a benefit-stack pitch.
- R4. Add a paired worked-example to `spec/specification.md` § 17.3.1 showing the slug = alias variant alongside the existing opaque-alias example.
- R5. Reframe `spec/whitepaper.md` § 3 so cross-context resolution leads and rename-survival is secondary.
- R6. Add a slug = alias variant section to `examples/semantic-cross-references.md` and soften the existing *Surviving heading renames* intro.
- R7. Add a single-sentence slug-variant note to `spec/cross-file-link-resolution.md` § *Alias IDs in Link Reference Definitions*.
- R8. Append a single-sentence pointer to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` § *Custom Aliases* paired-pattern note.
- R9. (No-op) Leave `README.md` and `examples/README.md` untouched -- they do not currently discuss the triple in prose.
- R10. Bump plugin version `1.6.2 -> 1.6.3` via `scripts/bump-version.sh patch`; add a 1.6.3 entry to `CHANGELOG.md`.

---

## Scope Boundaries

- No change to the triple's syntax, the adjacent-placement rule (settled by #103), or the recommendation level (settled by #96).
- No new term, no rename of "triple", no glossary restructure beyond the targeted reframe of the existing entry (#99 owns the glossary structure).
- No retrofit of existing topic files in the repo to use the slug = alias variant. The variant is forward-looking guidance; the opaque-alias variant remains canonical for existing hand-authored content.
- No validator rule change. Both variants are already accepted; cross-file conflict detection (MDPP014) is unaffected.
- No new standalone `examples/` specimen for the slug = alias variant. The variant is added to the existing cross-reference specimen.
- No coordination with the sibling `webworks-claude-skills:markdown-plus-plus` skill in the WebWorks plugin repo. That repo manages its own release cadence.
- No inline-anchor-vs-triple comparison content added to surfaces beyond `references/best-practices.md`. The brainstorm's success criterion is "at least once on a surface a reader will land on"; best-practices is the canonical home and other surfaces link to it.

---

## Context & Research

### Relevant Code and Patterns

- **Canonical treatment surface**: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings* (lines 572-608). The current section already establishes "The pattern combines three pieces", "All three pieces appear adjacent", "Why this is the recommended idiom", "When the rule fires", "When the rule does not fire", and "Cross-file behavior". R1's restructure inserts new subsections inside this section without breaking the existing flow.
- **Existing benefit-list shape**: Same section, "Why this is the recommended idiom" bullet list (lines 598-602). R1.a splits this flat list into three labeled groups (cross-context resolution, anti-drift with two named axes, intent signal).
- **Existing co-location prose**: Same section's "All three pieces appear adjacent" paragraph (line 589) and the section-move bullet (line 602). R1.a's labeled split makes the section-move-vs-rename-drift distinction explicit.
- **GLOSSARY entry shape**: `GLOSSARY.md` lines 33-39 (the *triple* entry). The reframe preserves the single-paragraph form; only the lead claim moves.
- **SKILL recommended-pattern block**: `SKILL.md` lines 159-174 (the *Recommended pattern for referenceable headings* subsection inside *Custom Aliases*). R3 keeps the block; the change is appending a sentence to *What to author* and replacing the trailing cross-file pitch.
- **Spec § 17.3.1 example**: `spec/specification.md` lines 1181-1203 (the *Semantic Cross-Reference Pattern* subsection). R4 adds a paired example after the existing one, framed as conformant under the resolution rules.
- **Whitepaper § 3 reframe target**: `spec/whitepaper.md` lines 83-104. The existing paragraph "This single reference resolves correctly in every context..." (line 102) is the cross-context lead that R5 promotes; the "In standard Markdown, heading links are auto-generated..." paragraph (line 100) is the rename-survival narrative that R5 demotes.
- **Existing example specimen**: `examples/semantic-cross-references.md` (124 lines). Existing H2 sections include *The pattern*, *Same-document references*, *Cross-document references*, *Surviving heading renames* (line 65), *Multiple aliases on one heading* (lines 80 and 88 -- note duplicate H2 in current file), *Topic map with cross-references* (line 97), *Summary*. R6 inserts a new H2 between *Multiple aliases on one heading* and *Topic map with cross-references*, and softens the *Surviving heading renames* intro paragraph (lines 69-77).
- **Spec/cross-file-link-resolution.md surface**: lines 161-178 (the *Alias IDs in Link Reference Definitions* subsection). R7 adds a single sentence after the existing example, before the multi-file-assembly bullet list.
- **Syntax-reference.md surface**: lines 423-466 (*Custom Aliases* section). The existing "Note:" paragraph at line 464 already links to best-practices for the triple. R8 appends one sentence to that note.
- **Version bump script**: `scripts/bump-version.sh patch` increments both `plugins/markdown-plus-plus/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (per `CLAUDE.md` § Version Management). Current version is `1.6.2`.
- **CHANGELOG entry shape**: `CHANGELOG.md` 1.6.2 entry (lines 17-21) is a single-bullet "Tooling" entry with a one-paragraph summary and an issue-link suffix. R10's 1.6.3 entry follows the same shape.

### Institutional Learnings

- `docs/solutions/conventions/normative-rules-against-competing-conventions-2026-05-18.md` -- when a Markdown++ convention competes with a parent-format convention (CommonMark bottom-of-file link reference tables vs. the triple's adjacent placement), the doc surfaces should explicitly name the competing convention and explain why the Markdown++ rule overrides it. R1.c's inline-anchor-vs-triple comparison applies the same pattern to a competing *authoring pattern* rather than a competing layout.
- `docs/solutions/conventions/imperative-anchor-section-for-skill-syntax-drift-2026-05-13.md` -- the SKILL.md cross-reference subsection should land guidance imperatively (do this, not consider this) and link to the prescriptive guide rather than restating the rationale. R3 keeps SKILL.md as a directive pointer; the rationale stays in best-practices.
- `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md` -- the skill's auto-activation signals are not edited here; the audit is content-only inside surfaces the skill already covers.

### External References

- None. The work is entirely internal documentation editing; no external library, framework, or third-party reference is involved.

---

## Key Technical Decisions

- **Sequence U1 (best-practices.md) before all other content units.** The other surfaces link to best-practices subsections by name (*Choosing the slug*, the inline-anchor-vs-triple comparison). Drafting U1 first establishes the wording the other units cite. Within a single PR the editor can land any order, but a planning-time canonical-first sequence prevents pointer drift if the section names are revised during U1.
- **U7 (CHANGELOG + version bump) lands last in the PR but in the same commit set.** Per `CLAUDE.md` § Version Management, the bump goes in the same PR as the change. Running the bump script last avoids re-bumping if other units force a redraft.
- **One unit per surface (R7 + R8 grouped) instead of per-requirement.** The brainstorm enumerates R1-R10 by requirement. The plan groups R7 + R8 into a single "spec-side pointers" unit because both are single-sentence additions to reference-style surfaces and their wording is parallel. R3 stays its own unit because the SKILL touches two paragraphs and uses different framing language than the spec pointers.
- **The slug-variant terminology is "semantic slug + opaque alias" vs. "slug = alias value", per the brainstorm.** Every surface uses these two labels consistently. No surface invents a new label (e.g., "uniform-identifier triple"). The naming question is explicitly an open question (see *Open Questions*); if a future PR adopts a shorter label, it touches all surfaces at once.
- **The labeled benefit groups in R1.a use these three names: *Cross-context resolution*, *Anti-drift* (with two named axes: *Heading-rename drift* and *Section-move drift*), and *Intent signal*.** Other surfaces (GLOSSARY R2, SKILL R3) reference these axis names verbatim where they refer back to the framework. The GLOSSARY entry names both anti-drift axes in a single sentence (not the labels in bold) so the entry stays prose, not a sub-list.
- **The inline-anchor-vs-triple comparison uses a table in best-practices.md.** The brainstorm presents it as a table with seven rows; the *Open Questions* section flags that a paragraph form might read better depending on surrounding style. The plan defaults to the table form (the brainstorm's recommendation) and notes the paragraph alternative as an implementer judgment call.
- **R6 placement of the new slug = alias section in `examples/semantic-cross-references.md` follows the brainstorm's recommendation: between *Multiple aliases on one heading* and *Topic map with cross-references*.** The file is a sequence of H2 sections each demonstrating a distinct property; the variant fits that pattern. The alternative (inside *The pattern*) would shrink the section into a sub-aside.
- **R6 keeps the existing *Surviving heading renames* H2 title.** The brainstorm leans toward keeping the title and softening the intro paragraph rather than retitling or splitting into a *Heading-rename drift* + *Section-move drift* pair. The example body covers the rewrite mechanics, which is the section's pedagogical value; the intro change is what reframes it as "one of several anti-drift properties."

---

## Open Questions

### Resolved During Planning

- **What unit granularity?** Resolved: one unit per surface, with R7 + R8 grouped because both are single-sentence pointer additions. R1's four sub-changes (R1.a-R1.d) stay in one unit because they all edit the same canonical section in a coordinated restructure.
- **Plan ordering vs. PR ordering?** Resolved: the plan orders units canonical-first (U1) for sequencing clarity, but they land in one PR with the version bump (U7) last in the commit set.
- **Where does the inline-anchor-vs-triple comparison live?** Resolved: only in `references/best-practices.md` § *Semantic Cross-References*, per brainstorm key decision. Other surfaces link to it.

### Deferred to Implementation

- **Table vs. paragraph for the inline-anchor-vs-triple comparison in R1.c.** The brainstorm's *Open Questions* leaves this to implementer judgment; the plan defaults to the table form, but the implementer should verify the surrounding best-practices style accommodates a seven-row table without forcing a global shape change. If the table looks out of place, switch to a paragraph or side-by-side example form.
- **Whether `examples/semantic-cross-references.md` § *Surviving heading renames* should be renamed.** Plan defaults to keeping the title and softening the intro paragraph (brainstorm-leaning option). Implementer may retitle to *Anti-drift mechanics* or split into a pair if the softened intro reads awkwardly against the section's title.
- **Duplicate H2 *Multiple aliases on one heading* in the existing specimen file (lines 80 and 88).** The current file appears to have the heading on both line 80 and line 88 -- line 88 is inside a fenced code block (a code example *showing* the H2 syntax), but `grep -n "^## "` matches both. This is not an authoring bug; it is the example demonstrating multiple aliases on the same heading. The implementer should leave the existing structure unchanged; the new slug = alias section is inserted *after* the closing of that example, between line 94 (end of the example block + "Both ... resolve to the same heading." paragraph) and line 96 (the start of *Topic map with cross-references*). Verify on edit.

---

## Implementation Units

### U1. Restructure `references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings*

**Goal:** Land the canonical treatment of the triple's *when / why / how* for the post-audit reader: labeled benefit groups, two slug variants with a *Choosing the slug* subsection, an inline-anchor-vs-triple comparison, and a generated-anchor/pipeline callout. Every other surface in this plan links back to subsections this unit creates.

**Requirements:** R1.a, R1.b, R1.c, R1.d

**Dependencies:** None. Land first so other units' pointers reference settled subsection names.

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`

**Approach:**

Four coordinated edits inside the existing § *Semantic Cross-References on Topic-Defining Headings* section. Existing structural elements (the *Recommended* lead paragraph, *The pattern combines three pieces* block, *All three pieces appear adjacent* paragraph, *When the rule fires* / *does not fire* paragraphs, *Cross-file behavior* paragraph) all stay. The new content slots in between them.

1. **R1.a** -- Replace the flat *Why this is the recommended idiom* bullet list (currently 4 bullets) with three labeled benefit groups:
   - *Cross-context resolution* (carries the existing "same reference works in standalone preview, single-file publishing, multi-file assembly" claim).
   - *Anti-drift* with two named sub-axes:
     - *Heading-rename drift* -- the alias decouples link targets from heading text. Includes the explicit note: "an alias plus inline link gets this benefit on its own; the triple's contribution is to extend the benefit to assembly-wide reference-style links and to readers who rely on the slug as the human-readable handle."
     - *Section-move drift* -- co-location keeps directive + heading + linkref together as a unit when a section moves, is deleted, or reordered. Includes the explicit note: "the validator cannot detect a silent slug-target desync; the layout is what prevents it. This benefit is the one inline anchor links and bottom-of-file linkref tables cannot give you."
   - *Intent signal* (carries the existing "custom alias + linkref expresses externally-referenceable intent" claim).

2. **R1.b** -- Add a new *Choosing the slug* subsection between *The pattern combines three pieces* (existing block) and *All three pieces appear adjacent* (existing paragraph). The subsection documents two conformant variants with a worked example for each:
   - *Semantic slug + opaque alias* (hand-authored, publishing-tool numeric IDs) -- the existing example shape (`#200020` with slug `installation`).
   - *Slug = alias value* (generated anchors, automation pipelines) -- new example (`#sh-ug-installation` with slug `sh-ug-installation`).
   - Closes with a one-sentence rule of thumb: "If the alias is opaque, pair it with a semantic slug. If the alias is itself semantic and unique-by-construction, the slug = alias variant is the cleaner fit -- fewer identifiers to keep in sync, and authoring agents can treat the alias as the single source of truth for the heading."

3. **R1.c** -- Add a new *Inline anchor links vs. the triple* subsection between the new labeled benefit groups and *When the rule fires*. Uses a comparison table with the seven columns from the brainstorm: within-document linking, cross-file (assembled) linking, heading-rename safety, section-move safety, default link text, authoring overhead per heading, best fit for. Follows the table with two paragraphs naming when each pattern fits (within-assembly-only vs. cross-file-resolution-or-future-proofing).

4. **R1.d** -- Add a *For generated-anchor and pipeline workflows* callout paragraph immediately after the labeled benefit groups, before *Choosing the slug*. One paragraph naming the audience explicitly and explaining why the slug = alias variant fits.

Final section flow after this unit: *Recommended* lead -> *The pattern combines three pieces* block -> *Choosing the slug* (NEW) -> *All three pieces appear adjacent* -> References-elsewhere block -> *Why this is the recommended idiom* (RESTRUCTURED with three labels) -> *For generated-anchor and pipeline workflows* callout (NEW) -> *Inline anchor links vs. the triple* (NEW) -> *When the rule fires* -> *When the rule does not fire* -> *Cross-file behavior*.

**Patterns to follow:**
- Existing `best-practices.md` heading hierarchy and inline-code formatting.
- The lineage established by #96/#99/#103: best-practices owns the prescriptive treatment; the spec is informative.

**Verification:**
- The four sub-changes (R1.a-d) are all present in the section.
- The labeled benefit group names match the names cited by U2 (GLOSSARY) and U3 (SKILL) when they reference back -- specifically *Cross-context resolution*, *Anti-drift* with *Heading-rename drift* and *Section-move drift*, and *Intent signal*.
- The *Choosing the slug* subsection name matches the name cited by U6 (SKILL R3) and U2 (cross-file-link-resolution R7).
- `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` passes with no new errors.
- If the new inline-anchor-vs-triple table is included, run `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md --check` and accept the formatter's output if it suggests changes (per `references/table-formatting.md`).

**Test expectation:** none -- documentation-only change. Verification above replaces test scenarios.

---

### U2. Reframe `GLOSSARY.md` § *triple* entry

**Goal:** Lead with cross-context resolution; demote heading-text-rename survival to one of two named anti-drift axes; add a one-sentence pointer to the two slug variants.

**Requirements:** R2

**Dependencies:** U1 (anti-drift axis names land in best-practices first so the GLOSSARY entry can reference them by name).

**Files:**
- Modify: `GLOSSARY.md`

**Approach:**

Rewrite the single paragraph in the *triple* entry (lines 37-39) per the brainstorm's R2 specification. Keep the entry single-paragraph; do not introduce sub-bullets or expand the entry into a tutorial. The "Full treatment" line at line 39 stays unchanged.

Lead claim becomes: the triple's same reference works in standalone preview, single-file publishing, and multi-file assembly (cross-context resolution).

Rename-survival is recast as: "The alias decouples the link target from heading text (heading renames don't break references); co-location keeps the three pieces together when a section moves, deletes, or reorders." (Two distinct anti-drift axes named in one sentence.)

Add one closing sentence: "The slug may be a separate semantic name (when the alias is opaque) or reuse the alias value (when the alias is itself semantic and unique-by-construction)."

**Patterns to follow:**
- The other GLOSSARY entries' single-paragraph + "Full treatment" link shape (see *Unset*, *attachment rule*, *content island*, *block content*).

**Verification:**
- Lead claim of the entry is cross-context resolution.
- Both anti-drift axes are named in one sentence (no sub-list, no axis-name bolding).
- Closing sentence names the two slug variants.
- Length stays a single paragraph.
- "Full treatment" link still resolves to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings`.

**Test expectation:** none -- documentation-only change.

---

### U3. Add paired worked example to `spec/specification.md` § 17.3.1

**Goal:** Show the slug = alias variant alongside the existing opaque-alias example in the spec, framed as conformant under the same resolution rules. The spec change is informative, not normative.

**Requirements:** R4

**Dependencies:** U1 (the spec's pointer back to *Choosing the slug* uses the subsection name landed in U1).

**Files:**
- Modify: `spec/specification.md` (§ 17.3.1 *The Semantic Cross-Reference Pattern*, lines 1181-1203)

**Approach:**

After the existing fenced example block (currently ending at line 1194 with `[getting-started]: #200010 "Getting Started"`), add a paragraph framing the second variant and a paired fenced example showing `<!-- style:Heading2; #sh-ug-installation -->` with slug = alias. Follow with one sentence: "Both forms are conformant. The choice depends on whether the alias carries semantic meaning of its own; see `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` *Choosing the slug* for guidance."

Do not change the existing example. Do not change the cross-file resolution rules. Do not change the diagnostic registry. The change is informative-only, adding a second worked example in parallel with the first.

**Patterns to follow:**
- The existing example's fenced-block formatting (line 1189-1194).
- Spec convention of informative examples following normative rules.

**Verification:**
- Original opaque-alias example is unchanged.
- New paired example uses the brainstorm's `sh-ug-installation` form.
- The framing sentence explicitly calls both forms conformant.
- The pointer link uses the full path to best-practices.md.
- No normative language ("MUST", "SHOULD", "MAY") was added or removed.

**Test expectation:** none -- documentation-only spec change.

---

### U4. Reframe `spec/whitepaper.md` § 3 *Semantic cross-references that work everywhere*

**Goal:** Promote the cross-context-resolution paragraph to the lead so the section's prose matches its title; demote the rename-survival narrative to a secondary anti-drift benefit. No new example; the existing example covers both intents once the framing leads with cross-context resolution.

**Requirements:** R5

**Dependencies:** None (the whitepaper edit is self-contained; it does not cite best-practices subsection names).

**Files:**
- Modify: `spec/whitepaper.md` (§ 3, lines 83-104)

**Approach:**

Reorder paragraphs within the existing section:
- Promote the paragraph currently at line 102 ("This single reference resolves correctly in every context...") to the lead position immediately after the existing fenced example and "The semantic slug..." paragraph.
- Demote the paragraph currently at line 100 ("In standard Markdown, heading links are auto-generated...") to a secondary position with a single-sentence framing that names it as one of several anti-drift properties rather than the headline.
- Keep the closing sentence "One reference, every output context." (line 104) intact -- the reframe brings the opening into agreement with the existing conclusion.

The existing fenced example (lines 87-92) and the "The semantic slug is derived..." paragraph (lines 94-98) stay unchanged. The reframe is sentence-and-paragraph-level only.

**Patterns to follow:**
- The whitepaper's narrative voice; this is a reframe, not a rewrite.

**Verification:**
- Section's lead claim (after the fenced example and slug-derivation paragraph) is cross-context resolution.
- Rename-survival is preserved as a benefit but framed as one of several anti-drift properties.
- Closing line "One reference, every output context." is still the section closer.
- No new fenced examples added; no examples removed.

**Test expectation:** none -- documentation-only whitepaper edit.

---

### U5. Add slug = alias variant section and soften rename-section intro in `examples/semantic-cross-references.md`

**Goal:** Demonstrate the slug = alias variant end-to-end on its own H2 section; soften the existing *Surviving heading renames* intro so rename-survival reads as one of several anti-drift properties rather than the headline benefit.

**Requirements:** R6

**Dependencies:** None (the example file stands alone and doesn't cite best-practices subsection names by anchor).

**Files:**
- Modify: `examples/semantic-cross-references.md`

**Approach:**

Two coordinated edits:

1. **Add a new H2 section** titled *Slug equals alias value (pipeline-generated anchors)*, inserted between the existing *Multiple aliases on one heading* example block (which closes around line 94 with "Both `[multiple-aliases]` and `[multi-alias-example]` resolve to the same heading.") and the existing *Topic map with cross-references* H2 (line 97). The new section:
   - Uses the slug = alias variant on its own H2 heading (per brainstorm: `<!-- style:Heading2; #sh-ug-pipeline -->`, slug `sh-ug-pipeline` reusing the alias value).
   - Body explains in two short paragraphs what the variant is, when it fits (generated/automated anchors, unique-by-construction semantic IDs), and that it is conformant with the same rules as the opaque-alias form.
   - Includes a brief before/after contrast in fenced code blocks showing the same heading authored with both variants, illustrating that the alias is the only difference.

2. **Soften the existing *Surviving heading renames* intro paragraph** (lines 69-77) so it reads as "one of several anti-drift properties" rather than "the headline reason to use the pattern." The worked example body (lines 71-77 showing the link-reference rewrite mechanics) stays intact -- the change is the intro framing only.

Per the brainstorm's *Open Questions* discussion (also captured in this plan's *Open Questions / Deferred to Implementation*), the existing *Surviving heading renames* H2 title stays; only the intro framing changes. The implementer may revisit if the softened intro reads awkwardly against the section title.

**Patterns to follow:**
- The existing specimen file's structure: H2-per-property, with the triple pattern on every section heading.
- The existing H2 sections demonstrate properties one-at-a-time -- the new section follows that shape.

**Verification:**
- The new H2 section appears between *Multiple aliases on one heading* (existing) and *Topic map with cross-references* (existing).
- The new section's H2 heading itself uses the slug = alias variant as a worked demonstration.
- The before/after contrast in the new section shows the two variants on the same heading.
- The *Surviving heading renames* intro reads as one-of-several anti-drift properties; the worked example mechanics are unchanged.
- `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py examples/semantic-cross-references.md` passes.

**Test expectation:** none -- documentation-only example.

---

### U6. Tighten `SKILL.md` and append pointer to `references/syntax-reference.md`

**Goal:** Update the skill's recommended-pattern block with a slug-variant pointer and benefit-stack pitch; append a one-sentence variant-pointer to the syntax reference's Custom Aliases note. Both are pointer-only changes that keep best-practices as the deep treatment.

**Requirements:** R3, R8

**Dependencies:** U1 (both files cite the *Choosing the slug* subsection name landed in U1).

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` (§ *Custom Aliases / Recommended pattern for referenceable headings*, lines 159-174)
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` (§ *Custom Aliases* paired-pattern note, line 464)

**Approach:**

**SKILL.md (R3):**
- At the end of the *What to author* bullet (line 169), append: "The slug may be a separate semantic name (as in the example above) or the alias value itself when the alias is already semantic and unique. See the *Choosing the slug* guidance in `references/best-practices.md` § Semantic Cross-References on Topic-Defining Headings."
- Replace the one-line cross-file pitch following the bullet list (the line currently pointing at *Semantic Cross-References on Topic-Defining Headings* at line 172) with a benefit-stack pointer: "The triple gives cross-context resolution (standalone, single-file, assembly), section-move safety through co-location, and -- for automation pipelines that mint unique anchors -- a single identifier per heading via the slug = alias variant. See the linked best-practices section for the full rationale and the inline-anchor-vs-triple comparison."

No restructure of the SKILL recommended-pattern block. The block stays a directive pointer; the deep treatment stays in best-practices (matching the *imperative anchor section* learning at `docs/solutions/conventions/imperative-anchor-section-for-skill-syntax-drift-2026-05-13.md`).

**syntax-reference.md (R8):**
- After the existing "Note:" sentence at line 464 that points to best-practices for the triple, append: "That section also covers the two slug variants (semantic slug or slug = alias) and an inline-anchor vs. triple comparison for readers choosing between the two patterns."

No restructure. The reference doc's role is reference; the choice guidance stays in best-practices.

**Patterns to follow:**
- SKILL.md keeps its imperative voice -- "apply the triple", not "consider the triple". The benefit-stack pitch is a one-paragraph pointer, not a tutorial.
- `references/syntax-reference.md` keeps its reference-style voice -- the appended sentence is a pointer, not new normative content.

**Verification:**
- SKILL.md *What to author* bullet has a new closing sentence naming both slug variants and pointing to *Choosing the slug*.
- SKILL.md's cross-file pitch is replaced by a benefit-stack pitch naming cross-context resolution + section-move safety + slug = alias for pipelines.
- The benefit-stack pitch's pointer link still resolves to `references/best-practices.md#semantic-cross-references-on-topic-defining-headings`.
- syntax-reference.md's *Custom Aliases* note has the appended slug-variant + inline-anchor-comparison sentence.
- No restructure of either file beyond the targeted prose changes.

**Test expectation:** none -- documentation-only pointer additions.

---

### U7. Add single-sentence slug-variant note to `spec/cross-file-link-resolution.md`

**Goal:** Append a one-sentence pointer naming both slug variants to the *Alias IDs in Link Reference Definitions* subsection. Worked Examples A and B keep the opaque-alias variant unchanged.

**Requirements:** R7

**Dependencies:** U1 (cites the *Choosing the slug* subsection name landed in U1).

**Files:**
- Modify: `spec/cross-file-link-resolution.md` (§ *Alias IDs in Link Reference Definitions*, lines 161-178)

**Approach:**

After the existing example block (line 170 closes the fenced example), before the "In a multi-file assembly, this pattern works across files because:" paragraph (line 172), insert a single sentence: "The slug may be a separate semantic name (as shown above) or reuse the alias value when the alias is unique-by-construction (see the *Choosing the slug* guidance in `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`)."

Worked Examples A and B (lines 180+) stay unchanged. Their pedagogy is about cross-file resolution and the MDPP014 diagnostic, not the slug-variant choice.

**Patterns to follow:**
- The spec file's existing prose voice and pointer-style cross-references.

**Verification:**
- The new sentence appears between the existing example and the multi-file-assembly bullet list.
- The pointer link uses the full repo-relative path to best-practices.md.
- Worked Examples A and B are unchanged.
- MDPP014 prose elsewhere in the file is unchanged.

**Test expectation:** none -- documentation-only spec note.

---

### U8. Version bump and CHANGELOG entry

**Goal:** Bump plugin version `1.6.2 -> 1.6.3` and add a CHANGELOG entry describing the cross-reference documentation audit.

**Requirements:** R10

**Dependencies:** U1, U2, U3, U4, U5, U6, U7 (all content edits should be in place before bumping; the CHANGELOG entry describes the landed changes).

**Files:**
- Run: `scripts/bump-version.sh patch` (updates `plugins/markdown-plus-plus/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` from `1.6.2` to `1.6.3`).
- Modify: `CHANGELOG.md`

**Approach:**

Run the version bump script:

```bash
scripts/bump-version.sh patch
```

Verify both files were updated to `1.6.3` (the script keeps them synchronized).

Add a new top-of-file CHANGELOG entry under `## [1.6.3] - 2026-05-22` with a single "Tooling" subsection, matching the shape of the existing 1.6.2 entry (single bullet, one paragraph, issue-link suffix). The entry should cover:
- The slug = alias variant as a documented degree of freedom.
- The benefit-axis restructure in `references/best-practices.md` (labeled cross-context-resolution / anti-drift / intent-signal groups, with the two named anti-drift axes).
- The inline-anchor-vs-triple comparison in best-practices.
- The agent/pipeline callout.
- Reframes in GLOSSARY, SKILL, whitepaper, spec § 17.3.1, cross-file-link-resolution, syntax-reference, and the new example section in `examples/semantic-cross-references.md`.
- Explicit "no syntax / semantics / processing / validator behavior changed" statement (matches the 1.6.2 entry's framing).
- Issue link: `([#106](https://github.com/quadralay/markdown-plus-plus/issues/106))`.

**Patterns to follow:**
- 1.6.2 CHANGELOG entry shape (lines 17-21 of `CHANGELOG.md`).
- `CLAUDE.md` § Version Management: patch bump for documentation updates.

**Verification:**
- `plugins/markdown-plus-plus/.claude-plugin/plugin.json` shows `"version": "1.6.3"`.
- `.claude-plugin/marketplace.json` is also updated to `1.6.3`.
- CHANGELOG entry under `## [1.6.3] - 2026-05-22` follows the 1.6.2 entry's shape.
- Entry references issue #106.
- Entry explicitly states no syntax/semantics/processing/validator behavior changed.

**Test expectation:** none -- version bump and CHANGELOG entry are mechanical.

---

## System-Wide Impact

The change is documentation-only and affects only cross-reference doc surfaces. Downstream effects to consider:

- **The sibling `webworks-claude-skills:markdown-plus-plus` skill in the WebWorks plugin repo** carries its own copy of the SKILL.md and references guidance. Downstream propagation is explicitly out of scope per the brainstorm's Scope Boundaries -- the WebWorks repo manages its own release cadence. This plan does not coordinate that propagation; a separate workstream will pick it up.
- **Existing in-repo `examples/` files using the opaque-alias variant** are not retrofitted. The slug = alias variant is forward-looking guidance; the opaque-alias variant remains canonical for existing hand-authored content. Per the brainstorm's Scope Boundaries, no retrofit is in scope.
- **Existing readers who internalized the rename-survival framing** still find rename-survival in the rationale -- it just stops leading. The new framing groups it under *Anti-drift / heading-rename drift*, which is a more accurate but still rename-survival-bearing label.
- **The validator (`scripts/validate-mdpp.py`)** is unchanged. Both slug variants are already syntactically valid; no new check is needed. MDPP014 (cross-file slug conflict) fires regardless of which variant is used.
- **The auto-aliases script (`scripts/add-aliases.py`)** is unchanged. The script mints aliases for unaliased headings; how the author chooses to use those alias values as slugs is an authoring decision, not a script change.

---

## Sources & References

- **Origin brainstorm**: [`docs/brainstorms/2026-05-22-cross-reference-when-why-how-audit.md`](../brainstorms/2026-05-22-cross-reference-when-why-how-audit.md)
- **Issue**: [#106](https://github.com/quadralay/markdown-plus-plus/issues/106)
- **Lineage**:
  - [#96](https://github.com/quadralay/markdown-plus-plus/issues/96) introduced the alias+slug+linkref triple as a named idiom.
  - [#99](https://github.com/quadralay/markdown-plus-plus/issues/99) surfaced "triple" as a term in `GLOSSARY.md`.
  - [#103](https://github.com/quadralay/markdown-plus-plus/issues/103) made the adjacent-placement rule normative.
- **Related institutional learnings**:
  - [`docs/solutions/conventions/normative-rules-against-competing-conventions-2026-05-18.md`](../solutions/conventions/normative-rules-against-competing-conventions-2026-05-18.md) -- pattern for naming a competing parent-format convention and explaining why the Markdown++ rule overrides it. R1.c (inline-anchor-vs-triple comparison) applies the same shape to a competing authoring pattern.
  - [`docs/solutions/conventions/imperative-anchor-section-for-skill-syntax-drift-2026-05-13.md`](../solutions/conventions/imperative-anchor-section-for-skill-syntax-drift-2026-05-13.md) -- SKILL.md should land guidance imperatively and link to the prescriptive guide. R3 keeps SKILL.md as a directive pointer.
- **Version management**: `CLAUDE.md` § Version Management -- patch bump for documentation updates.
