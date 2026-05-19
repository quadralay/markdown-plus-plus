---
date: 2026-05-18
status: active
type: docs
plan_depth: standard
origin: docs/brainstorms/2026-05-18-triple-adjacent-placement-requirements.md
issue: 103
---

# Plan: Make Adjacent Placement Part of the alias+slug+linkref Triple Rule

## Summary

Make the **adjacent placement rule** of the alias+slug+linkref triple normative in the docs. Today the canonical example shows the three pieces (directive, heading, link reference definition) sitting together, but no surface *states* that they must. A reasonable reader -- including an AI agent following the skill -- can read the prose as "the three pieces exist somewhere in the file" and migrate every link reference definition to the bottom of the file in conventional CommonMark style. The validator accepts both layouts, so this misreading is reproducible from the docs alone.

This plan addresses the four contributing factors enumerated in the brainstorm by editing three surfaces (`best-practices.md`, `SKILL.md`, `examples/semantic-cross-references.md`), recording the clarification in `CHANGELOG.md`, and bumping the plugin to `1.6.2` (patch). No syntax, validator, or processing change. No retrofit of existing topic files.

---

## Problem Frame

The brainstorm (`docs/brainstorms/2026-05-18-triple-adjacent-placement-requirements.md`) captures the full failure mode. Short version:

- The triple is now the recommended cross-reference idiom (#96) and is surfaced as a named term (#99).
- The placement rule -- the three pieces sit adjacent to each other -- is **load-bearing** for the maintainability benefit: a heading move, rename, or deletion moves all three pieces as a unit.
- But the placement rule is only **shown by example**. The prose says "combined" or "work together." A CommonMark-literate reader (or AI agent) can reasonably read that as "exist somewhere in the same document" and group link refs at the bottom of the file -- conventional CommonMark style -- without violating any stated rule.
- The validator does not catch the drift (both layouts are valid CommonMark; both pass MDPP checks).

Four contributing factors, in order of impact:

1. The placement rule is shown by example but never stated in `references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings*.
2. `SKILL.md` says the link reference definition goes "below it" -- ambiguous between "next line" and "anywhere later in the file."
3. `references/best-practices.md` § *Advanced Patterns → Link References* shows general-purpose link refs collected at the bottom of the file. The contrast with the triple is intentional, but the placement difference is not called out.
4. The maintainability rationale for co-location is not surfaced. The "Why this is the recommended idiom" bullets cover other benefits but not the move-as-a-unit benefit -- the most direct reason for adjacency.

---

## Scope

### In scope

- Edit `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` -- normative adjacency line + co-location rationale bullet (R1); placement-contrast note in Advanced Patterns → Link References (R3).
- Edit `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` -- replace "below it" with placement-bearing wording (R2).
- Edit `examples/semantic-cross-references.md` -- brief placement-rule callout inside the existing **The pattern** section (R4).
- Add a `1.6.2` entry to `CHANGELOG.md`.
- Run `scripts/bump-version.sh patch` to bump `plugin.json` and `marketplace.json` from `1.6.1` to `1.6.2` (R5).

### Out of scope (carried from origin)

- Changing the syntax of the triple.
- Renaming the term "triple" or "alias+slug+linkref."
- Anything covered by #96 (making the pattern recommended) or #99 (terminology surfacing across surfaces).
- A `mdpp` validator lint rule that warns when a link reference definition has the same slug as a custom alias defined elsewhere in the file but does not sit adjacent. Worth filing separately; out of scope here.
- Retrofitting existing topic files to enforce adjacency. Forward-looking guidance only.
- Coordinating with the sibling `webworks-claude-skills:markdown-plus-plus` skill in the WebWorks plugin repo. Separate release cadence.

### Deferred to Follow-Up Work

- Validator lint rule for slug/adjacency mismatch (see Out of scope above). A future issue can scope: triggering conditions, false-positive risk on internal-only anchors, error code allocation (likely MDPP015 or later), and CLI surfacing.

---

## Requirements Traceability

| Origin Req | Description | Implementation Unit |
|------------|-------------|---------------------|
| R1 | Normative adjacency line + co-location rationale bullet in best-practices.md *Semantic Cross-References* | U1 |
| R2 | Tighten SKILL.md wording -- replace "below it" with placement-bearing wording | U2 |
| R3 | Placement-contrast note in Advanced Patterns → Link References | U3 |
| R4 | Placement-rule callout in `examples/semantic-cross-references.md` § *The pattern* | U4 |
| R5 | Patch-level version bump to 1.6.2 + CHANGELOG entry | U5 |

---

## Key Technical Decisions

- **Normative wording lives in `best-practices.md`, not the spec.** The placement rule is a *recommended idiom*, not a syntactic requirement. CommonMark allows link reference definitions anywhere; Markdown++ inherits that. Pushing adjacency into the spec would imply the validator should enforce it, which the brainstorm explicitly defers (see origin: docs/brainstorms/2026-05-18-triple-adjacent-placement-requirements.md § Key Decisions).

- **SKILL.md edit is wording-tightening, not restructuring.** Single-sentence rewording in the existing *Recommended pattern for referenceable headings* paragraph. No reorganization, no new section.

- **The specimen file gets a callout, not a new section.** A new section in `examples/semantic-cross-references.md` would push the file from specimen toward tutorial. A brief callout inside the existing **The pattern** section preserves the specimen role -- the file stays openable, previewable, and copy-pasteable.

- **Patch bump, not minor.** Per `CLAUDE.md` § Version Management: "Bug fixes, documentation updates, minor improvements" → `patch`. Documentation-only clarification of an existing recommended pattern. No new feature, no syntax change. Goes from `1.6.1` to `1.6.2`.

---

## Implementation Units

### U1. Add normative adjacency line and co-location rationale to best-practices.md

**Goal:** Make the placement rule explicit in `references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings*. After the canonical example block, state that the three pieces are adjacent. Add the move-as-a-unit benefit to the "Why this is the recommended idiom" list.

**Requirements:** R1

**Dependencies:** None.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` (modify; around lines 572-606)

**Approach:**
- After the canonical example block (currently ends at line 583) and before the numbered "1./2./3." annotation list, OR immediately after the numbered list ends, add a short prose paragraph stating the adjacency rule. Wording should communicate:
  - The directive sits on the line directly above the heading.
  - The heading follows.
  - A single blank line separates the heading from the link reference definition.
  - The link reference definition follows on the next line.
  - Co-location is part of the pattern, not a layout choice.
- Implementer judgement on exact wording -- match the surrounding tone of the section, which is prescriptive but not jargony.
- In the **Why this is the recommended idiom** bullet list (around lines 596-599), add a bullet naming the move-as-a-unit benefit: when a section moves, all three pieces move together because they are physically adjacent; splitting them across the file means a heading rename, deletion, or section move can silently desync the slug from its target, which the validator cannot detect.
- Bullet placement (top vs bottom of the existing list) is implementer judgement. Both positions work; placing it last keeps the existing reading order intact, placing it first signals priority. Either is fine.

**Patterns to follow:**
- Existing tone of `best-practices.md` § *Semantic Cross-References on Topic-Defining Headings*: prescriptive prose, short paragraphs, bullet lists for "Why," "When the rule fires," "When the rule does not fire."

**Test scenarios:**
- Test expectation: none -- this is documentation prose. Verification is by reading; see Verification below.

**Verification:**
- A reader who has only seen the edited section can answer "where should the link reference definition for a triple be placed?" without inferring from the example block.
- The "Why this is the recommended idiom" list now includes the move-as-a-unit benefit.
- `python3 plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` passes (the file already has frontmatter and existing structure -- no Markdown++ directives in this section, so validator is mostly checking that no new syntactic problems were introduced).

---

### U2. Tighten SKILL.md wording from "below it" to placement-bearing language

**Goal:** In `SKILL.md`, replace the ambiguous "below it" in the *Recommended pattern for referenceable headings* paragraph with wording that communicates the placement rule, not just the existence requirement.

**Requirements:** R2

**Dependencies:** None. (Independent of U1, but the two changes reinforce each other -- doing both in the same PR is the intent.)

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` (modify; line 169)

**Approach:**
- Locate the sentence at line 169 currently reading: *"...all three pieces -- the `<!-- style:HeadingN; #target -->` directive on the heading, the heading itself, and a `[semantic-slug]: #target \"Title\"` link reference definition below it."*
- Replace the trailing clause *"...link reference definition below it"* with placement-bearing wording. Suggested form from the brainstorm: *"...link reference definition on the line directly after the heading (separated by a single blank line)."* Implementer may refine to match flow with the surrounding "Just an alias..." sentence.
- Do not restructure the surrounding paragraph or the bulleted "When the rule fires / What to author / When the rule does NOT fire" list. This is a single-sentence rewording.

**Patterns to follow:**
- Existing tone of the *Recommended pattern for referenceable headings* paragraph: prescriptive, compressed, with parenthetical clarifications for tight technical points.

**Test scenarios:**
- Test expectation: none -- this is documentation prose. Verification is by reading; see Verification below.

**Verification:**
- The sentence at line 169 now states placement, not just existence.
- A reader skimming only the *Recommended pattern* paragraph in SKILL.md can answer "where should the link reference definition be placed?" without consulting best-practices.md.
- The bulleted list below the example (lines 168-170) remains unchanged in shape.

---

### U3. Add placement-contrast note in Advanced Patterns → Link References

**Goal:** In `references/best-practices.md` § *Advanced Patterns → Link References*, add a short note distinguishing the two patterns' placement conventions so the contrast becomes a deliberate convention rather than a hidden one.

**Requirements:** R3

**Dependencies:** U1 (the note links back to the *Semantic Cross-References on Topic-Defining Headings* anchor, which U1's normative line strengthens; both edits should land together for consistent reader experience).

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` (modify; around lines 607-653)

**Approach:**
- Add a short paragraph or callout block inside the existing § *Advanced Patterns → Link References* section. Natural insertion point: after the existing intro paragraph (line 611) and before the "Standard inline links (recommended)" subsection, OR at the end of the section before the `---` horizontal rule. Implementer judgement.
- The note should:
  - Reference the triple section by anchor (`[Semantic Cross-References on Topic-Defining Headings](#semantic-cross-references-on-topic-defining-headings)`).
  - State that general-purpose link reference definitions are conventionally grouped at the bottom of the file, while the triple's link reference definition lives adjacent to its heading.
  - Explain that both are valid CommonMark, but encode different intent: grouped definitions signal "this is a shared URL table"; adjacent definitions signal "this is the semantic slug for *this* heading, and the two move together."
- Keep it short -- this is a contrast note, not a tutorial. The brainstorm § R3 provides a concrete draft of the explanatory sentences; implementer may refine wording.

**Patterns to follow:**
- Existing tone of § *Advanced Patterns → Link References*: contrastive, with **bold-tagged** subsection labels and short prose paragraphs.

**Test scenarios:**
- Test expectation: none -- this is documentation prose. Verification is by reading; see Verification below.

**Verification:**
- The Advanced Patterns → Link References section now names the placement convention difference as a deliberate intent signal, not just a stylistic accident.
- The anchor link to *Semantic Cross-References on Topic-Defining Headings* renders correctly (Markdown anchor for the existing H2 heading).
- A reader who already groups link refs at the bottom of the file out of CommonMark habit gets a clear pointer: the triple's link ref is the exception, and adjacency is intentional.

---

### U4. Strengthen `examples/semantic-cross-references.md` as a copy-paste template

**Goal:** Add a brief placement-rule callout in the existing **The pattern** section of `examples/semantic-cross-references.md` so a reader copying from the file knows the adjacent shape is the pattern -- not a stylistic accident.

**Requirements:** R4

**Dependencies:** None. (Specimen edit is independent of the skill-doc edits; could land in any order. Grouped with the others for review coherence.)

**Files:**
- `examples/semantic-cross-references.md` (modify; lines 14-20)

**Approach:**
- Locate the **The pattern** section (line 14). After the existing numbered three-piece list (lines 18-20), add a short callout naming the placement rule:
  - The three pieces appear adjacent on every linkable heading: directive, heading, blank line, link reference definition.
  - Link to `../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings* for the full rationale (use the relative path from `examples/` to the best-practices file; the spec file in the same section uses a similar relative-path convention at `../../../../../spec/cross-file-link-resolution.md`, but from `examples/` it is shorter).
- Keep the callout short -- the file's role is specimen, not tutorial. A single sentence or two suffices.
- Do **not** add a new top-level section like "## Placement rule." A callout inside **The pattern** preserves the specimen feel.

**Patterns to follow:**
- Existing tone of `examples/semantic-cross-references.md`: short prose paragraphs introducing each technique, real directives demonstrated inline. The file's voice is "look how this works," not "here is how to do this." The callout should match.
- For the relative link to best-practices.md, mirror the relative-path style used elsewhere in `examples/`. From `examples/semantic-cross-references.md`, the path to best-practices.md is `../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`. Implementer should verify this resolves correctly when previewing in a Markdown viewer.

**Test scenarios:**
- Test expectation: none for behavioral testing. Specimen file passes existing validation: `python3 plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py examples/semantic-cross-references.md`.

**Verification:**
- The **The pattern** section now names the placement rule explicitly.
- A reader who opens the specimen with no prior context understands that the adjacent shape is the pattern, not a layout choice.
- The relative link to best-practices.md resolves when previewing the file in a Markdown viewer.
- `validate-mdpp.py` still passes on the file.

---

### U5. Add CHANGELOG entry and bump plugin version to 1.6.2

**Goal:** Record the placement-rule clarification in `CHANGELOG.md` under a new `1.6.2` entry, and bump `plugin.json` + `marketplace.json` from `1.6.1` to `1.6.2` via the official bump script.

**Requirements:** R5

**Dependencies:** U1, U2, U3, U4 (the changelog entry summarizes what the version ships; bump runs last in the PR).

**Files:**
- `CHANGELOG.md` (modify; insert new `## [1.6.2] - 2026-05-18` section above the existing `## [1.6.1] - 2026-05-13` section)
- `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (modify; via `scripts/bump-version.sh patch`)
- `.claude-plugin/marketplace.json` (modify; via `scripts/bump-version.sh patch`)

**Approach:**
- **Add CHANGELOG entry:** Insert above the existing `## [1.6.1] - 2026-05-13` entry. Follow the format used by the existing entries:
  - Heading: `## [1.6.2] - 2026-05-18`
  - Category: `### Tooling`
  - One bullet summarizing the placement-rule clarification across `SKILL.md`, `references/best-practices.md`, and `examples/semantic-cross-references.md`. Reference the issue: `([#103](https://github.com/quadralay/markdown-plus-plus/issues/103))`.
  - Match the tone of recent entries (descriptive sentence, ends with the issue link in parens).
  - Note that the change is forward-looking documentation guidance -- no syntax, semantics, processing, or validator behavior change.
- **Run the bump script:** `scripts/bump-version.sh patch` from the repo root. The script updates both `plugin.json` and `marketplace.json` together. The brainstorm § R5 confirms `patch` is the correct level.
- Verify after running:
  - `plugins/markdown-plus-plus/.claude-plugin/plugin.json` → `"version": "1.6.2"`.
  - `.claude-plugin/marketplace.json` → matching version field is `1.6.2`.

**Patterns to follow:**
- Existing CHANGELOG entry style: `## [1.6.1] - 2026-05-13` and prior entries. Categories (Spec / Tooling / Project) per the file's stated convention.
- `scripts/bump-version.sh` is the canonical version-bump tool (per `CLAUDE.md` § Version Management). Do not hand-edit `plugin.json` or `marketplace.json`.

**Test scenarios:**
- Test expectation: none for behavioral testing. Verification is by inspecting the resulting files.

**Verification:**
- `CHANGELOG.md` has a new `## [1.6.2] - 2026-05-18` entry above the `1.6.1` entry, with a Tooling bullet summarizing the placement-rule clarification.
- `plugin.json` and `marketplace.json` both report version `1.6.2` after running the bump script.
- The bump script ran without errors.

---

## System-Wide Impact

- **Reader experience:** A reader of any single surface (`SKILL.md` Custom Aliases paragraph, `best-practices.md` § *Semantic Cross-References*, the `examples/` specimen) can correctly infer the placement rule from prose, not just example. Cross-surface consistency improves.
- **AI-agent experience:** The failure mode that motivated this issue (an AI agent placing link refs at the bottom of every file across 16 topics) becomes harder to reproduce because the rule is named in the surfaces the agent loads as skill context (`SKILL.md` directly; `best-practices.md` as the linked rationale).
- **Existing topic files:** Not affected. The change is forward-looking guidance. Existing files that already follow the pattern need no edits. The brainstorm explicitly defers retrofit work.
- **Validator behavior:** Unchanged. No new lint rule is introduced; the existing validator continues to accept both layouts as valid CommonMark.
- **Downstream consumers** (the WebWorks plugin repo's sibling skill, ePublisher integration): Unaffected. Documentation-only change in the upstream Markdown++ format repo; downstream consumers consume the same Markdown++ syntax with no contract change.

---

## Risks and Mitigations

- **Risk: Wording drift between the three surfaces.** The placement rule needs to read consistently across `SKILL.md`, `best-practices.md`, and the specimen callout. Wording that conflicts (e.g., "next non-blank line" vs. "directly after the heading") creates a new ambiguity instead of resolving the existing one.
  - **Mitigation:** During implementation, draft the normative line in `best-practices.md` first (U1), then mirror its phrasing in `SKILL.md` (U2) and the specimen callout (U4). Review all three together before opening the PR.

- **Risk: The placement-contrast note in Advanced Patterns reads as a discouragement of general-purpose link refs.** The Advanced Patterns section currently positions general-purpose link refs as "generally not recommended" already. Adding a contrast note could be misread as further discouragement.
  - **Mitigation:** The contrast note frames both conventions as valid CommonMark with different intent. Wording from the brainstorm § R3 is deliberately neutral on the "should you use general-purpose link refs at all" question -- it only names the placement difference. Implementer should keep that neutrality.

- **Risk: Implementer adds a new H2 section in `examples/semantic-cross-references.md` instead of a callout.** This would push the file from specimen toward tutorial and violate the file's role.
  - **Mitigation:** U4 explicitly forbids a new top-level section. The callout lives inside the existing **The pattern** section.

---

## Open Questions

None blocking. Minor implementation-time judgement calls:

- Exact wording of the normative adjacency line in `best-practices.md` (U1). Brainstorm suggests a draft; implementer may refine to match surrounding tone.
- Whether the *Why co-location matters* bullet goes at the top or bottom of the existing "Why this is the recommended idiom" list (U1). Either works.
- Exact insertion point of the contrast note in § *Advanced Patterns → Link References* (U3): after intro paragraph vs. at the end of the section. Either works.

---

## Done When

- All four contributing factors named in the brainstorm are addressed: best-practices.md states adjacency normatively and adds the co-location rationale; SKILL.md uses placement-bearing wording; Advanced Patterns section explicitly contrasts the two placement conventions; the specimen file names the placement rule.
- A reader who has only seen the relevant sections (best-practices.md § *Semantic Cross-References*, SKILL.md *Recommended pattern* paragraph, `examples/semantic-cross-references.md` § *The pattern*) can correctly answer "where should the link reference definition for a triple be placed?" without having to infer from an example.
- `examples/semantic-cross-references.md` is unambiguous as a copy-paste template -- a reader who copies it gets the adjacent shape by default.
- `CHANGELOG.md` records the placement-rule clarification under a `1.6.2` entry.
- Plugin version is bumped to `1.6.2` via `scripts/bump-version.sh patch` before PR.
- `validate-mdpp.py` passes on edited files.
