---
date: 2026-05-18
topic: triple-adjacent-placement
status: active
---

# Make Adjacent Placement Part of the alias+slug+linkref Triple Rule

## Problem Frame

The **alias+slug+linkref triple** is now the recommended cross-reference
idiom for topic-defining headings (delivered by #96, surfaced as a
named term by #99). The canonical example shows the three pieces in one
adjacent block:

```markdown
<!-- style:Heading2; #200020 -->
## Installation

[installation]: #200020 "Installation"
```

The placement rule -- that the three pieces sit adjacent to each other --
is **load-bearing**: it preserves co-location so a heading move, rename,
or deletion moves all three pieces as a unit. But no current surface
*states* that rule. It is shown by example only. The prose around the
example says the three pieces are "combined" or "work together," which
a CommonMark-literate reader can reasonably read as "exist somewhere in
the same document."

### Concrete failure case

An AI agent applying the skill across 16 topic files authored the
alias-on-heading directive correctly on every heading, but collected
every link reference definition into a single block at the **bottom of
each file** -- the conventional CommonMark style for link-ref tables.
The agent rationalized the choice in ways the skill does not push back
against:

- "CommonMark allows link reference definitions anywhere in the document."
- "Bottom-of-file is conventional Markdown style for link refs."
- "Putting a link ref between a Glossary Term heading and its Glossary
  Def paragraph would visually break the pair in source."

The user's correction was direct: *"The whole purpose of the triple is
to keep the custom-alias, paragraph content, and semantic slug
together. Why were you putting the semantic slugs in a different
location?"* -- after which the agent moved every link ref back to
immediately follow its target heading.

The validator was happy with both layouts, so the validator did not
catch it. The failure is reproducible from the current docs alone --
not an agent reasoning error so much as a docs-load-bearing assumption
that is not written down.

### What in the docs allowed the misreading

Four contributing factors, ordered by impact:

1. **The placement rule is shown by example but never stated.**
   `references/best-practices.md` § *Semantic Cross-References on
   Topic-Defining Headings* says *"The pattern combines three pieces"*
   and shows the example block. "Combines" suggests grouping but does
   not normatively state adjacency. A reader can interpret it as "the
   three pieces work together" without inferring "the three pieces sit
   next to each other."

2. **`SKILL.md` framing is ambiguous.** The Custom Aliases recommended
   pattern says *"a `[semantic-slug]: #target \"Title\"` link
   reference definition below it. Just an alias (without the paired
   definition) makes the heading internally addressable but does not
   establish a semantic cross-reference."* The word "below" reads as
   "exists somewhere below in the file" rather than "on the next
   non-blank line after the heading." The presence/absence framing
   emphasizes that the definition *exists*, not where it *lives*.

3. **The Advanced Patterns → Link References section shows
   general-purpose link reference definitions collected at the bottom
   of the file** -- the conventional Markdown style. The contrast with
   the triple is intentional (different patterns, different placements),
   but the docs do not call out the placement difference as a
   deliberate convention. A reader carrying CommonMark instincts plus
   this example naturally migrates triple link refs to the bottom too.

4. **The maintainability rationale for co-location is not surfaced.**
   The "Why this is the recommended idiom" bullets in best-practices.md
   cover *standalone vs. assembled rendering*, *slug stays semantic
   when heading text changes*, and *alias implies intent*. They do not
   cover the most important author-facing benefit: **when a section
   moves, all three pieces move as a unit because they are physically
   together**. That benefit exists only if the placement rule is
   followed, and the docs never connect those dots.

## Requirements

### R1. Make the placement rule explicit (highest leverage)

In `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
§ *Semantic Cross-References on Topic-Defining Headings*, after the
canonical example block:

- Add a normative line stating adjacency: the directive sits on the
  line directly above the heading, the heading itself follows, a single
  blank line separates the heading from the link reference definition,
  and the link reference definition follows on the next line.
  Co-location is part of the pattern, not just a layout choice.
- Add a *Why co-location matters* bullet alongside the existing
  rationale: when a section moves, all three pieces move as a unit.
  Splitting them across the file means a heading rename, deletion, or
  section move can silently desync the slug from its target -- which
  the validator cannot detect.

### R2. Tighten the `SKILL.md` wording

In `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`, in
the *Recommended pattern for referenceable headings* paragraph under
Custom Aliases, replace *"a `[semantic-slug]: #target \"Title\"` link
reference definition below it"* with wording that communicates
placement, not just existence -- e.g., *"a `[semantic-slug]: #target
\"Title\"` link reference definition on the line directly after the
heading (separated by a single blank line)."* The sentence should
communicate the placement rule.

### R3. Contrast the placements in Advanced Patterns → Link References

In `references/best-practices.md` § *Advanced Patterns → Link
References*, add a short note distinguishing the two patterns'
placement conventions. The note should:

- Reference the triple section by anchor.
- State that general-purpose link reference definitions are
  conventionally grouped at the bottom of the file, while the triple's
  link reference definition lives adjacent to its heading.
- Explain that both are valid CommonMark but encode different intent:
  grouped definitions signal "this is a shared URL table"; adjacent
  definitions signal "this is the semantic slug for *this* heading, and
  the two move together."

### R4. Strengthen the canonical specimen as a copy-paste template

In `examples/semantic-cross-references.md`, the standalone specimen
already demonstrates co-location on every heading. To make the file
unambiguous as a copy-paste template:

- Add a short callout in the **The pattern** section (after the
  numbered three-piece list) naming the placement rule explicitly, so
  a reader copying from the file knows the adjacent shape is the
  pattern -- not a stylistic accident.
- The callout should be brief; the file's role is specimen, not
  tutorial. Link to the best-practices section for the full rationale.

### R5. Patch-level version bump

Per `CLAUDE.md` § Version Management, this PR ships through skill
`references/*.md`, `SKILL.md`, and `examples/` content. The change is
forward-looking documentation guidance with no format or directive
change, so `patch` is appropriate. Run `scripts/bump-version.sh patch`
to advance from 1.6.1 to 1.6.2.

## Success Criteria

- A reader who has only seen the relevant sections (best-practices.md
  *Semantic Cross-References...*, SKILL.md recommended-pattern
  guidance, the examples specimen) can correctly answer *"where should
  the link reference definition for a triple be placed?"* without
  having to infer from an example.
- All four contributing factors are addressed: best-practices.md states
  adjacency normatively and adds the co-location rationale; SKILL.md
  uses placement-bearing wording; the Advanced Patterns section
  explicitly contrasts the two placement conventions; the specimen
  file names the placement rule.
- `examples/semantic-cross-references.md` is unambiguous as a
  copy-paste template -- a reader who copies it gets the adjacent
  shape by default.
- `CHANGELOG.md` records the placement-rule clarification under a
  1.6.2 entry.
- Plugin version is bumped to 1.6.2 via
  `scripts/bump-version.sh patch` before PR.

## Scope Boundaries

**In scope:**

- Edits to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
  -- normative adjacency line, co-location rationale bullet, and
  Advanced Patterns placement-contrast note.
- Edit to `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
  -- replace "below it" wording with placement-bearing wording.
- Edit to `examples/semantic-cross-references.md` -- add a brief
  placement-rule callout in the **The pattern** section.
- `CHANGELOG.md` entry under 1.6.2.
- Patch-level version bump via `scripts/bump-version.sh patch`.

**Out of scope** (explicit in the issue):

- Changing the syntax of the triple.
- Renaming the term "triple" or "alias+slug+linkref."
- Anything covered by #96 (making the pattern recommended) or #99
  (terminology surfacing across surfaces). This issue is downstream
  placement-clarification work.
- A `mdpp` validator lint rule that warns when a link reference
  definition has the same slug as a custom alias defined elsewhere in
  the file but does not sit adjacent. The issue flags this as a
  separate suggestion worth filing on its own; out of scope here.
- Retrofitting existing topic files in the repo to enforce adjacency.
  The change is forward-looking guidance; existing files that already
  follow the pattern need no edits, and any that drift are caught by
  future authoring.
- Coordinating with the sibling `webworks-claude-skills:markdown-plus-plus`
  skill in the WebWorks plugin repo. That repo manages its own release
  cadence.

## Key Decisions

- **Normative adjacency wording goes in best-practices.md, not the
  spec.** The placement rule is a *recommended idiom*, not a syntactic
  requirement. CommonMark allows link reference definitions anywhere,
  and Markdown++ inherits that. Pushing adjacency into the spec would
  imply the validator should enforce it, which the issue explicitly
  defers. Best-practices.md is the right home: it is the canonical
  surface for the triple as a recommended idiom.

- **SKILL.md edit is wording-tightening, not restructuring.** The
  Custom Aliases section already names the triple, links to the
  best-practices section, and recommends the pattern. The fix is a
  single-sentence rewording that swaps "below it" for placement-bearing
  language. No reorganization needed.

- **The specimen file gets a callout, not a new section.** A new
  section ("Placement Rule" or similar) risks making the specimen feel
  like documentation. Specimens are meant to be opened, previewed, and
  copied. A brief callout inside the existing **The pattern** section
  preserves that role.

- **The validator rule is deferred, not rejected.** The issue flags it
  as worth filing separately. A future issue (not this one) can scope
  the lint rule: triggering conditions, false-positive risk on
  internal-only anchors, error code allocation (likely MDPP015 or
  later), and CLI surfacing.

- **Patch bump, not minor.** Per `CLAUDE.md` § Version Management,
  "Bug fixes, documentation updates, minor improvements" map to
  `patch`. This change is documentation-only clarification of an
  existing recommended pattern -- no new feature, no syntax change.

## Assumptions

- **A normative-sounding adjacency line in best-practices.md is
  sufficient to fix the agent failure mode.** The issue's *Done when*
  clause sets the bar at "a reader can correctly answer the placement
  question." That bar is met by explicit prose plus the existing
  example, without needing a runtime check. If a future audit shows
  the failure persists despite the prose, the validator rule (deferred
  from R5/optional) becomes the next escalation.

- **The Advanced Patterns placement-contrast note will not confuse
  readers about whether general-purpose link refs are still valid.**
  The contrast names *both* conventions as valid CommonMark; the
  framing is "different intent, different placement." A reader who
  needs general-purpose link refs (version redirection, long URLs)
  still has them.

- **No edits are needed to `examples.md` (the AI-skill scenario
  library) or to the spec.** The triple is documented prescriptively
  in `best-practices.md` and named in `SKILL.md`. The spec's role is
  syntactic/processing; adjacency is recommendation, not syntax.

## Open Questions

None blocking. The issue's *Proposed changes* enumerates the edits in
sufficient detail to plan against. Minor decisions deferred to
implementation:

- The exact wording of the normative adjacency line in
  best-practices.md. The issue suggests a draft sentence; the
  implementer may refine it to match surrounding tone without changing
  intent.
- Whether the *Why co-location matters* bullet goes at the top or
  bottom of the existing "Why this is the recommended idiom" list.
  Implementer judgement; both placements work.

## Next Step

Hand off to `/compound-engineering:ce-plan` to produce the file-by-file
edit plan, or implement directly with the standard `ce-work` flow --
the surfaces and edits are enumerated, the scope is small, and a
heavyweight planning pass would likely be over-ceremony. Version bump
via `scripts/bump-version.sh patch` lands in the same PR per
`CLAUDE.md` § Version Management.
