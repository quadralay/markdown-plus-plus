---
date: 2026-05-11
status: completed
type: docs
origin: docs/brainstorms/2026-05-11-alias-slug-linkref-recommended-requirements.md
issue: 96
---

# docs: Make alias+slug+linkref the Recommended Cross-Reference Idiom

## Summary

Issue #96 has two coordinated parts:

1. **Mechanical example fixes.** The conflict-resolution example in
   `spec/cross-file-link-resolution.md` (lines 65-86) and the MDPP014
   trigger example in
   `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
   (lines 421-430) show `[slug]: #target` link reference definitions
   without ever showing the alias on a heading that would produce those
   targets. The fix adds `<!-- style:HeadingN; #target -->` plus a
   heading above each definition so the targets resolve. This makes the
   examples internally consistent with Examples A and B in
   `spec/cross-file-link-resolution.md` and with the canonical pattern
   in `spec/whitepaper.md` Section 3.

2. **Editorial position shift.** The spec treats alias+slug+linkref as
   the idiomatic Markdown++ cross-reference. The skill's best-practices
   currently file the whole link-reference family under "advanced
   patterns" and lead with "generally not recommended". This plan
   splits the framing: general-purpose link references stay marked as
   advanced, while the alias+slug+linkref triple on topic-defining
   headings is promoted to recommended. The shift is reinforced in
   `syntax-reference.md` (a paired-pattern note in Custom Aliases) and
   `SKILL.md` (an authoring directive in the Custom Aliases
   subsection). A patch-level version bump ships the change.

The brainstorm (see origin: `docs/brainstorms/2026-05-11-alias-slug-linkref-recommended-requirements.md`)
resolved every nontrivial decision: keep the slug-collision narrative
in the MDPP014 example, keep descriptive target names in the
conflict-resolution example, place the SKILL.md directive inside
Custom Aliases rather than as a new section, and treat the convention
as recommendation (not lint-enforced rule).

---

## Problem Frame

The spec positions alias+slug+linkref as "the primary use case for
cross-file link reference resolution" and demonstrates it consistently
in Worked Examples A and B. Two surfaces contradict that positioning:

- **Spec self-contradiction.** The Conflict Resolution > Definition
  Order example in `spec/cross-file-link-resolution.md` defines
  `[slug]` targets that no heading produces. A reader following the
  whitepaper's pattern would expect `<!-- style:Heading1; #root-target -->`
  above a heading; the example omits it. The MDPP014 trigger example
  in `error-codes.md` has the same defect.

- **Skill framing inversion.** The skill's `best-practices.md` Link
  References section opens with "generally not recommended" and treats
  the alias+slug+linkref pattern as one of several advanced use cases.
  An AI agent reading this guidance will not pair an alias with a link
  reference definition by default, even when the heading is obviously
  meant to be externally referenceable.

The intent of attaching a custom alias to a heading already implies
the intent to make that heading externally referenceable. The natural
pairing is alias on the heading + link reference definition with a
semantic slug + the slug used in references throughout the assembly.

---

## Requirements (carried from origin)

| ID | Requirement | Units |
|----|-------------|-------|
| R1 | Spec example correction in `spec/cross-file-link-resolution.md` Conflict Resolution > Definition Order (lines 65-86) | U1 |
| R2 | MDPP014 trigger example correction in `error-codes.md` (lines 421-430) | U2 |
| R3 | Best-practices reframing: split general-purpose vs alias+slug+linkref subsections | U3 |
| R4 | Syntax-reference paired-pattern note in Custom Aliases | U4 |
| R5 | SKILL.md authoring directive in Custom Aliases subsection | U5 |
| R6 | Patch-level plugin version bump | U6 |

See origin document for full success criteria and rationale.

---

## Scope Boundaries

**In scope:**
- Edits to `spec/cross-file-link-resolution.md` (conflict-resolution example only).
- Edits to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` (MDPP014 trigger example only).
- Restructure of the Link References subsection in `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`.
- Targeted addition to the Custom Aliases section of `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`.
- Authoring directive added to the Custom Aliases subsection of `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`.
- Patch-level version bump via `scripts/bump-version.sh patch` (1.1.17 → 1.1.18).

**Out of scope** (carried verbatim from origin):
- Retrofitting existing Markdown++ files in this repo to apply the
  pattern. The change is forward-looking guidance, not a migration.
  The spec's Worked Examples A and B already use the pattern.
- Changing CommonMark behavior or introducing new directives.
- Coordinating with the `webworks-claude-skills:markdown-plus-plus`
  sibling skill in the WebWorks plugin repo. That repo manages its
  own release cadence.
- Adding any lint rule to `scripts/validate-mdpp.py` that flags an
  alias without a paired link-reference definition. The new guidance
  is a recommendation, not a hard rule, and a lint check would
  over-trigger on internal-only anchors.

### Deferred to Follow-Up Work

- A future audit of repo-internal Markdown++ documents (CONTRIBUTING,
  GOVERNANCE, SECURITY, brainstorms, plans) to apply the
  alias+slug+linkref pattern to their primary headings. Not required
  by the issue and explicitly out of scope.

---

## Key Technical Decisions

These are carried from origin and constrain implementation:

- **MDPP014 example keeps the slug-collision narrative.** The example
  exists to illustrate two files defining the same `overview` slug.
  Adding alias+heading lines makes the targets resolve while keeping
  the collision intact. Do not switch to numeric alias IDs (e.g.,
  `#200010`) — the example is about slug collisions, not ID format.
  (See origin: Key Decisions § "The MDPP014 trigger example keeps its
  slug-collision narrative.")

- **`best-practices.md` preserves the "Why inline links are
  preferred" rationale.** The reframing splits the section into a
  recommended (alias+slug+linkref) subsection and a general-purpose
  (still advanced) subsection. The existing rationale against
  arbitrary `[install-guide]: #installation` definitions stays —
  only the alias+slug+linkref pattern is promoted.
  (See origin: Key Decisions § "`best-practices.md` keeps the 'Why
  inline links are preferred' rationale.")

- **`SKILL.md` guidance lives inside the existing Custom Aliases
  subsection (lines 89-112).** Not a new top-level section. AI agents
  reading the alias rules see the paired-pattern recommendation in
  context. (See origin: Key Decisions § "`SKILL.md` guidance lives in
  the Custom Aliases subsection.")

- **Recommendation, not requirement.** Aliases used as internal-only
  anchors remain valid. The recommendation applies when the author's
  intent is to make a heading externally referenceable — the default
  intent for custom aliases on titles and primary headings.
  (See origin: Key Decisions § "The convention is recommendation, not
  requirement.")

### Assumptions (inferred bets carried from origin)

These are explicit bets, not decided facts, recorded so review can
scrutinize them:

- **"Significant headings" = file title H1 and structurally important
  H2s.** H3+ headings are author judgement, not blanket policy. The
  SKILL.md directive should reflect that scope explicitly to prevent
  over-application by AI agents.

- **Conflict-resolution example keeps descriptive target names**
  (`#root-target`, `#chapter-a-target`, `#chapter-b-target`) rather
  than converting to numeric alias IDs. The issue's wording matches
  Examples A and B in *structure* (heading + style+alias + link-ref
  definition), not in *ID format*. Descriptive names also keep the
  example's pedagogy distinct from Example B's slug-collision focus.

- **Patch-level version bump is correct.** The change is
  forward-looking documentation and skill guidance with no breaking
  format change — squarely in `CLAUDE.md` § Version Management's
  patch category.

---

## High-Level Pattern Reference

> This sketch illustrates the canonical pattern that all corrected
> examples and recommended-pattern guidance must produce. It is
> directional guidance for review, not implementation specification.
> Each unit follows it; the per-unit Approach fields are authoritative
> for exact placement.

The alias+slug+linkref triple, in its canonical form (per
`spec/whitepaper.md` Section 3):

```markdown
<!-- style:HeadingN; #target -->
## Heading Text

[semantic-slug]: #target "Heading Text"
```

Three coordinated pieces:

1. **Style + alias directive** above the heading attaches a stable
   anchor (`#target`) to the heading regardless of heading-text
   changes.
2. **Heading line** provides the human-visible label.
3. **Link reference definition** binds a semantic, author-chosen slug
   to the stable anchor. References elsewhere in the assembly use
   `[Display Text][semantic-slug]` (or the collapsed/shortcut forms).

`#target` can be either a numeric alias ID (preferred for
publishing-tool stability) or a descriptive name (preferred when the
example's pedagogy benefits from readable identifiers). The
conflict-resolution example uses descriptive names; the
whitepaper, Worked Examples A and B, and MDPP014 trigger example use
numeric IDs.

---

## Implementation Units

### U1. Fix dangling targets in `spec/cross-file-link-resolution.md` Conflict Resolution example

**Goal:** The Conflict Resolution > Definition Order example
(currently lines 65-86) must show a heading with `<!-- style:HeadingN; #target -->`
above each link reference definition so the targets actually resolve.
Structure matches Worked Example A in the same file.

**Requirements:** R1.

**Dependencies:** None.

**Files:**
- `spec/cross-file-link-resolution.md` (edit one example block)

**Approach:**

The current example has three fenced code blocks, one per file
(root, chapter-a.md, chapter-b.md). Each block contains only a bare
link reference definition. Add a heading and the
`<!-- style:HeadingN; #target -->` directive above each definition so
the `#root-target`, `#chapter-a-target`, and `#chapter-b-target`
anchors actually exist.

Retain the three descriptive target names. Keep the surrounding prose
(definition-order narrative, "The root document's definition of
`[slug]` appears first and wins") unchanged. The example's purpose is
to show order-of-precedence with three conflicting definitions of the
same slug; the fix only makes the targets resolvable so a reader who
copies the snippet sees the same first-definition-wins behavior in
their own preview.

The chapter-a.md and chapter-b.md filenames are inline code-block
labels, not real files in the repo. No filesystem changes required.

**Patterns to follow:**
- `spec/cross-file-link-resolution.md` Worked Example A (lines 175-264) for the canonical structure.
- `spec/whitepaper.md` Section 3 (lines 83-104) for the foundational pattern.

**Test scenarios:** none — documentation example fix; verification is
reviewer inspection. The example does not exercise the validation
script (the snippet is inside a fenced code block, never parsed as
Markdown++).

**Verification:**
- The example shows three headings (one per file), each with
  `<!-- style:HeadingN; #target -->` above it, followed by the
  matching `[slug]: #target "title"` link reference definition.
- The descriptive target names (`#root-target`, `#chapter-a-target`,
  `#chapter-b-target`) are preserved.
- The first-definition-wins narrative remains intact and the
  surrounding prose still scans against the new example.
- The example structure now mirrors Worked Examples A and B in
  the same file.

---

### U2. Fix MDPP014 trigger example in `error-codes.md`

**Goal:** The MDPP014 trigger example (currently lines 421-430) must
show alias+heading above each link reference definition so the
example illustrates a real slug collision between two files whose
targets actually exist.

**Requirements:** R2.

**Dependencies:** None. Parallel-safe with U1.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` (edit one example block)

**Approach:**

The current trigger example shows two bare `[overview]: #section-N`
definitions, one per file, with a comment marking the cross-file
duplication. Add `<!-- style:Heading2; #section-N -->` plus a heading
above each definition so the slug collision is between two real
referenceable anchors.

Keep the slug `overview` in both files — the example's purpose is to
demonstrate the cross-file duplicate diagnostic, not the pattern
itself. Keep the `<!-- file-a.md -->` and `<!-- file-b.md -->`
comment labels and the WARNING comment.

Per Key Decision § "MDPP014 trigger example keeps its
slug-collision narrative", do not switch to numeric alias IDs. Use
the existing `#section-1` and `#section-2` descriptive targets.

**Patterns to follow:**
- `spec/cross-file-link-resolution.md` Worked Example B (lines 266-340) — the same MDPP014 scenario presented at full length.

**Test scenarios:** none — documentation example fix; verification is
reviewer inspection.

**Verification:**
- The example shows two headings (one per file), each with
  `<!-- style:Heading2; #section-N -->` above it, followed by the
  `[overview]: #section-N "Overview"` link reference definition.
- The duplicate-`overview` slug remains the focal point of the
  example.
- The WARNING comment still flags the cross-file duplicate.
- The example's pedagogy mirrors the longer Worked Example B in the
  spec.

---

### U3. Restructure Link References section in `best-practices.md`

**Goal:** Split the Link References subsection (currently lines
540-606, under `## Advanced Patterns`) into two clearly distinguished
subsections: one promoting alias+slug+linkref on topic-defining
headings to **recommended**, and one keeping general-purpose link
references marked as **advanced**.

**Requirements:** R3.

**Dependencies:** None. Must land before U4 and U5 because they link
to the new subsection's anchor.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` (restructure the Link References subsection)

**Approach:**

The current structure files everything under `## Advanced Patterns` >
`### Link References`, with prose that opens "generally not
recommended". After the change, the Link References section
distinguishes two patterns:

1. **Alias+slug+linkref on topic-defining headings (recommended).**
   Promoted out of "generally not recommended" framing. Recommend the
   pattern for file titles, primary H1s, and structurally important
   H2s. Rationale: the same reference works in standalone preview,
   single-file publishing, and multi-file assembly; references survive
   heading-text renames; the spec positions this as the idiomatic
   Markdown++ cross-reference.

2. **General-purpose link references (advanced).** Preserved framing
   for arbitrary URL reuse, version redirection, long URLs, and other
   non-heading use cases. The existing "Why inline links are
   preferred" rationale stays.

Use an anchor on the recommended subsection that U4 and U5 can link
to. The current section anchor is `#link-references`. Either keep
that anchor on a parent subsection and add a child anchor like
`#alias-slug-linkref-pattern`, or rename the section structure so the
recommended pattern owns the primary anchor. The implementer chooses
based on what produces the cleanest cross-reference targets for U4
and U5.

The existing "Example - semantic cross-references across files"
(currently lines 582-599) becomes the leading example of the
recommended subsection rather than the trailing illustration of an
advanced pattern. The existing "Tradeoffs" bullets (lines 601-605)
stay attached to the general-purpose subsection.

Consider whether the recommended subsection should leave the
"Advanced Patterns" parent heading entirely. The brainstorm's R3
specifies splitting the framing but does not mandate restructuring
parent headings. The implementer should evaluate whether placing the
recommended subsection under "Advanced Patterns" sends the wrong
signal even after the framing split.

**Patterns to follow:**
- `spec/whitepaper.md` Section 3 for the framing language ("Semantic
  cross-references that work everywhere").
- `spec/cross-file-link-resolution.md` line 171 ("This is the primary
  use case for cross-file link reference resolution") for the
  positioning that the best-practices reframing should reflect.

**Test scenarios:** none — documentation editorial restructure;
verification is reviewer inspection per success criteria in the
origin document.

**Verification:**
- The Link References content is split into two clearly distinguished
  subsections: recommended (alias+slug+linkref on topic-defining
  headings) and advanced (general-purpose link references).
- The recommended subsection has a stable anchor that U4 and U5 link
  to.
- The "Why inline links are preferred" rationale is preserved on the
  general-purpose subsection.
- A reader scanning the section can tell within one paragraph which
  form is recommended and which remains advanced.
- The semantic-cross-references-across-files example is presented as
  *the* recommended pattern, not as a "may be useful" advanced case.

---

### U4. Add paired-pattern note to Custom Aliases in `syntax-reference.md`

**Goal:** The Custom Aliases section (currently starting at line 423)
should include a brief note recommending the paired link-reference
pattern when an alias is intended to make a heading externally
referenceable. The note links to U3's recommended subsection in
`best-practices.md` for full rationale and examples.

**Requirements:** R4.

**Dependencies:** U3 (target anchor must exist).

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` (add note within Custom Aliases section)

**Approach:**

A natural placement is between "Using Aliases in Links" (lines
454-466) and "Alias vs. Heading IDs" (lines 468-475), or appended to
"Using Aliases in Links" itself. The note should be short — one or
two sentences — and distinguish two intents:

- An alias used as an **internal-only anchor** (no paired link
  reference definition) — still valid.
- An alias used to mark a **referenceable endpoint** — pair with a
  link reference definition that binds a semantic slug to the alias
  target. This is the recommended Markdown++ cross-reference idiom.

The note links to the recommended subsection in
`best-practices.md#<anchor-from-U3>` for the rationale and the
canonical example. The existing reference to
`best-practices.md#link-references` (line 464, in "Note: Reference-style links...")
should be reviewed in the same edit — depending on how U3 lands the
anchors, that pointer may need to be updated to point to the
general-purpose subsection rather than the recommended one.

**Patterns to follow:**
- The existing "Note: Reference-style links..." pattern on line 464
  for tone and length.
- The cross-document linking style used elsewhere in
  `syntax-reference.md`.

**Test scenarios:** none — documentation guidance addition;
verification is reviewer inspection.

**Verification:**
- A short note exists in the Custom Aliases section recommending the
  paired link-reference pattern for externally-referenceable
  endpoints.
- The note distinguishes internal-only-anchor aliases from
  referenceable-endpoint aliases.
- The note links to the recommended subsection in
  `best-practices.md`, and the link resolves to U3's anchor.
- The existing `best-practices.md#link-references` reference still
  resolves (either retargeted to the general-purpose subsection or
  preserved depending on U3's anchor layout).

---

### U5. Add authoring directive to Custom Aliases subsection in `SKILL.md`

**Goal:** The SKILL.md Custom Aliases subsection (currently lines
89-112) must include explicit guidance directing the skill — and AI
agents using it — to apply the alias+slug+linkref pattern when
authoring or editing Markdown++ topic files with significant
headings. "Significant headings" = file title H1 and structurally
important H2 headings (per Assumptions).

**Requirements:** R5.

**Dependencies:** U3 (links to the recommended subsection in
`best-practices.md`).

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` (add directive within Custom Aliases subsection)

**Approach:**

The directive should be authored as agent-facing instruction, not
descriptive prose. Add it inside the existing Custom Aliases
subsection at lines 89-112 — not as a new top-level section, per Key
Decisions.

Cover these points:

1. **When the rule fires.** When authoring or editing a Markdown++
   topic file with significant headings (file title H1 and primary
   H2s).
2. **What to author.** The full alias+slug+linkref triple on those
   headings (per the High-Level Pattern Reference above), not just an
   alias.
3. **When the rule does NOT fire.** H3+ headings (author judgement)
   and aliases used as internal-only anchors (valid alone).
4. **Where the rule is documented.** Link to U3's recommended
   subsection in `best-practices.md`.

The directive should be concise — comparable in length to the
existing "Rules" bullet list at lines 102-108 — to keep the SKILL.md
scannable. The current `add-aliases.py` reference at line 112 should
be reviewed: that script generates alias anchors only, not link
reference definitions, so the directive should clarify when an
author's intent (referenceable endpoint vs internal-only anchor)
makes the script's output sufficient versus needing the paired
definition.

**Patterns to follow:**
- The existing directive style throughout `SKILL.md` (concise,
  agent-facing, anchored to specific rules).
- The "Rules" bullet pattern at lines 102-108 for visual structure.

**Test scenarios:** none — agent-facing guidance; verification is
reviewer inspection plus the dogfooding check below.

**Verification:**
- The Custom Aliases subsection contains an explicit, agent-facing
  directive to apply the alias+slug+linkref triple on file title H1
  and structurally important H2 headings when authoring or editing
  Markdown++ topic files.
- The directive scopes itself to significant headings (not H3+).
- The directive notes that aliases used as internal-only anchors do
  not require a paired definition.
- The directive links to the recommended subsection in
  `best-practices.md`.
- **Dogfooding check:** An AI agent loading the updated SKILL.md and
  asked to author a new Markdown++ topic file with a primary H1 and
  one H2 should produce the alias+slug+linkref triple on both
  headings without further prompting. This is a success criterion
  from the origin document; the implementer should verify it manually
  during review (load the skill, prompt for a fresh topic file, check
  the output).

---

### U6. Patch-level plugin version bump

**Goal:** Bump the plugin version from 1.1.17 → 1.1.18 per the repo's
Version Management conventions, lands in the same PR.

**Requirements:** R6.

**Dependencies:** U1–U5 (the version bump should be the final commit,
representing the cumulative documentation guidance change).

**Files:**
- `plugins/markdown-plus-plus/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

**Approach:**

Run `scripts/bump-version.sh patch` from the repo root. The script
updates both `plugin.json` and `marketplace.json` in a single
operation, keeping their versions synchronized. No manual edits.

Patch-level is correct: forward-looking documentation guidance and
skill-content edits; no format change, no directive change, no
behavior change. `CLAUDE.md` § Version Management lists `patch` for
"Bug fixes, documentation updates, minor improvements" — this PR is
both (example-bug fixes + editorial reframing).

**Patterns to follow:**
- The existing version-bump workflow documented in
  `CLAUDE.md` § Version Management.

**Test scenarios:** none — version bump only.

**Verification:**
- `plugin.json` version field reads `1.1.18`.
- `marketplace.json` version field reads `1.1.18`.
- Both files have identical version strings.
- The git diff for this unit touches only the two JSON files.

---

## System-Wide Impact

This change reshapes guidance to authors and AI agents authoring
Markdown++ topic files. It does not change format semantics or
processor behavior. Specific impacts:

- **Spec consistency.** After U1, every example in
  `spec/cross-file-link-resolution.md` uses the canonical
  alias+heading+linkref structure. After U2, the MDPP014 reference
  documentation matches.

- **AI authoring default behavior.** After U5, an AI agent loading
  the skill should produce alias+slug+linkref triples on topic-file
  primary headings without prompting. This is the highest-leverage
  change — every new topic file authored by an AI using the skill
  inherits the recommended idiom.

- **Cross-document link integrity.** The U3/U4/U5 anchor chain
  introduces a cross-document dependency: U4 (`syntax-reference.md`)
  and U5 (`SKILL.md`) both link to U3's anchor in
  `best-practices.md`. Final review must confirm the anchors resolve.

- **No retrofit obligation.** Existing files in this repo and
  downstream consumers continue to work unchanged. The new guidance
  is forward-looking only (per Scope Boundaries).

- **Downstream skill alignment.** The `webworks-claude-skills:markdown-plus-plus`
  sibling skill in the WebWorks plugin repo is explicitly out of
  scope but will need a coordinated update on its own cadence. The
  brainstorm captured this as a separate workstream.

---

## Risks and Mitigations

- **Risk: anchor drift between U3/U4/U5.** If U3 restructures
  `best-practices.md` anchors and U4 or U5 are written against the
  old anchor name, links will dangle.
  **Mitigation:** Land U3 first. U4 and U5 review their U3 link
  targets before merge. The final-review checklist in Phase 5.1
  includes "anchor links resolve".

- **Risk: SKILL.md directive over-applies.** An overly broad
  directive could push AI agents to add alias+slug+linkref triples
  to every H3 in a long topic file, producing cluttered output.
  **Mitigation:** U5's directive explicitly scopes to file title H1
  and structurally important H2 (per Assumptions). The dogfooding
  check in U5 verifies the agent does not over-apply.

- **Risk: editorial reframing in U3 strips useful guidance.** A
  careless split could lose the "Why inline links are preferred"
  rationale that protects against arbitrary
  `[install-guide]: #installation` definitions.
  **Mitigation:** Key Technical Decisions § "best-practices.md
  preserves the 'Why inline links are preferred' rationale" is
  explicit. The final-review checklist confirms the rationale is
  intact on the general-purpose subsection.

- **Risk: the conflict-resolution example after U1 reads as a
  recommendation rather than a definition-order demo.** Adding the
  alias+heading lines might make a reader think the example is
  endorsing the descriptive `#root-target` style of alias IDs.
  **Mitigation:** Keep the surrounding prose ("The root document's
  definition of `[slug]` appears first and wins") unchanged so the
  example's purpose stays clearly about precedence, not about ID
  style. The Approach in U1 calls this out.

---

## Verification Strategy

Each unit's Verification field defines its acceptance check. Plan-level
verification consists of:

1. **Anchor integrity.** Cross-document links between
   `syntax-reference.md` → `best-practices.md` (U4) and `SKILL.md` →
   `best-practices.md` (U5) resolve to the anchors U3 introduces.

2. **Origin success criteria.** Each of the six success criteria in
   `docs/brainstorms/2026-05-11-alias-slug-linkref-recommended-requirements.md`
   § Success Criteria is satisfied:
   - U1 satisfies the first three (dangling-target example fixed,
     MDPP014 fixed via U2, recommended idiom obvious in
     best-practices via U3).
   - U4 satisfies "syntax-reference directs a reader who just learned
     about custom aliases to the paired-pattern guidance".
   - U5 satisfies "SKILL.md directs AI authors to apply the pattern
     on significant headings".
   - The dogfooding check in U5 satisfies "a new Markdown++ topic
     file authored by an AI using the skill includes the
     alias+slug+linkref triple on its title and primary headings
     without further prompting".

3. **Validation script (sanity).** `scripts/validate-mdpp.py` should
   continue to pass on the edited files. The edits do not change any
   directive that the script enforces, but running it confirms no
   accidental syntax breakage.

4. **Version bump (sanity).** `plugin.json` and `marketplace.json`
   both read `1.1.18` after U6.

---

## Dependencies and Sequencing

```
U1 ─── (independent)
U2 ─── (independent, parallel-safe with U1)
U3 ─── (must land before U4 and U5 — provides anchor target)
       └── U4 (paired-pattern note in syntax-reference.md)
       └── U5 (authoring directive in SKILL.md)
U6 ─── (final, after U1–U5)
```

Recommended commit sequencing:

1. U1 + U2 in either order (or combined commit since both are
   mechanical example fixes).
2. U3 alone (editorial restructure is meaningfully a separate
   change).
3. U4 + U5 (depend on U3's anchor; can land together since both are
   small additions referencing U3).
4. U6 final.

The implementer may bundle differently if it improves diff
readability, provided U3 lands before U4/U5 and U6 is final.
