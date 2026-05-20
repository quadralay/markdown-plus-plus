---
title: Capture cleanup/inverse-direction rules in skill reference docs when consumer repos discover them
date: 2026-05-11
category: conventions
module: plugins/markdown-plus-plus/skills/markdown-plus-plus
problem_type: convention
component: documentation
severity: medium
applies_when:
  - A consumer repository discovers cleanup, removal, or simplification rules for a Markdown++ surface through migration or refactor work that the skill does not document
  - The skill currently covers only the authoring direction of a directive family and is silent on the inverse direction
  - The rules are durable enough to outlive a single consumer's implementation language (Python today, JavaScript or Ruby tomorrow)
  - An AI agent or human author needs guidance for the cleanup half of the document lifecycle, not just authoring
  - Cleanup work in one consumer repo is likely to recur in others (epublisher-docs today, future migrated-document corpora later)
tags:
  - skill-authoring
  - reference-docs
  - lifecycle-coverage
  - knowledge-transfer
  - markdown-plus-plus
  - cleanup-rules
  - documentation-pattern
---

# Capture cleanup/inverse-direction rules in skill reference docs when consumer repos discover them

## Context

The `markdown-plus-plus` skill arrived strong on the authoring direction.
`best-practices.md` and `examples.md` teach an author how to *write* a
`<!--style:Name-->` directive, attach a `<!--#alias-->`, place a
`<!--marker:name-->`, and structure a `<!-- multiline -->` table. The
skill said nothing about the inverse direction: when a document already
carries directives that are redundant against the surrounding Markdown
structure, what is safe to remove or simplify, and what carries semantic
weight that must be preserved?

Issue #94 surfaced the gap. The `epublisher-docs` repository, working
through Phase II of a FrameMaker-to-Markdown++ migration, had built a
suite of Python scripts (`detect-removable-block-styles.py`,
`detect-reducible-styles.py`, `detect-removable-anchors.py`,
`detect-removable-inline-styles.py`, plus a `markdown_table_utils.py`
helper library) that encoded a substantial body of cleanup rules:
which block styles map 1:1 to Markdown structure and can be removed,
which families reduce to a canonical base form (`ChapterTitle` ->
`Title`, `NoteIndent2` -> `Note`), which inline styles are subsumed by
Markdown's own formatting tokens, which anchors are durable structure
versus migration leftovers, and a half-dozen non-obvious table-cell
edge cases that make hand-removal error-prone (cell-width preservation,
escaped pipes, partial-cell merges, bare-list-marker continuations,
underline-style heading detection).

That knowledge had been earned by one consumer through real migration
work. Without capturing it in the skill, every future consumer doing a
similar cleanup pass — and every AI agent asked to "remove these
redundant directives" — would have to rediscover the rules from
scratch. The skill would silently fail on the cleanup half of the
document lifecycle.

## Guidance

When a consumer repository's work surfaces durable cleanup or
removal rules for a directive family the skill currently teaches only
to *author*, capture those rules in the skill as a dedicated reference
document. Follow this shape:

**1. Create a new sibling reference doc, not an appendix to
`best-practices.md`.** The authoring story and the cleanup story
should not merge into one file. Authors learning to write directives
read `best-practices.md` top to bottom; authors operating on the
cleanup half land on the dedicated reference doc directly. The two
docs cross-reference each other (see step 4) but stay structurally
independent so each can grow without crowding the other. Examples
include `comment-manipulation.md` as the inverse of `best-practices.md`
and the table-formatting/comment-manipulation pair as a wider
authoring/cleanup decomposition.

**2. Keep the rules language-agnostic in the skill; implementation
stays in the consumer repo.** The skill reference doc names the
*rules* (`<!--style:BodyText-->` over a paragraph is removable;
`<!--style:Note-->` over a blockquote is keep-by-default) and the
*principles* behind them (a style comment whose name maps 1:1 to a
Markdown structural element is redundant). It does not duplicate the
consumer's Python, JavaScript, or shell implementation. A
re-implementer in a different language reads the rules without script
names cluttering each subsection. The implementation pointers live in
a single "Reference Implementation" section at the end of the doc,
with the explicit caveat that those scripts live in a separate
repository and may evolve independently.

**3. Lead with the underlying principle, then enumerate the
illustrative families.** Style names like `Heading1`, `CellBullet`,
or `ChapterTitle` are FrameMaker / ePublisher conventions surfaced by
one toolchain. They are useful concrete examples but they are not
canonical — a consumer repo with a different style family applies the
same test (does the style name map 1:1 to a Markdown structural
element?) to its own names. State that caveat at the top of the
principle section *and* restate it at each illustrative list, so a
reader landing on the list directly still sees the disclaimer.

**4. Cross-reference from the authoring docs without merging.** Add a
short, located cross-reference in `best-practices.md` — the natural
location is the densest concentration of authoring-vs-removal
collisions the file already covers (in our case, the Attachment Rule
under "Common Mistakes to Avoid"). The cross-reference points
readers who land on a removal-shaped problem at the dedicated doc;
it does not summarize the cleanup rules inline.

**5. Wire the doc into `SKILL.md` references list as a single
bullet.** No separate prose section in the SKILL.md body. The
description already names the directive families; the references list
is the index. A new prose section would either duplicate the
description or fragment the authoring story.

**6. Bump the plugin to a minor version, not patch.** A new reference
doc that adds a previously absent capability surface (cleanup
guidance) is a feature addition, not a documentation polish. Use
`scripts/bump-version.sh minor` to keep `plugin.json` and
`marketplace.json` synchronized and signal the capability change to
marketplace consumers.

## Why This Matters

A skill that covers only the authoring direction is half-complete in a
way that is invisible until a consumer needs the other half. Authors
writing fresh documents never see the gap. Migration consumers,
periodic-cleanup consumers, and AI agents asked to "remove these
redundant comments" hit it immediately — and they hit it without any
error, warning, or test that flags the gap. The symptom is a wrong
output the agent produces because it had no guidance for the removal
half, and a user who has to either invoke the skill manually with
extra context or revert the change.

Capturing the rules in the skill compounds the cost of one consumer's
discovery work into a permanent resource for every future consumer.
Capturing them as a *separate* reference doc — rather than folding
them into `best-practices.md` — keeps each surface focused enough that
authors learning to write directives are not flooded with cleanup
rules they do not need yet, and cleanup operators are not buried under
authoring guidance they have already passed.

Keeping the rules language-agnostic means the skill doc survives the
consumer reimplementing its scripts in a different language, splitting
them across multiple tools, or replacing them with an LSP-driven
quick-fix. The skill is the contract; the consumer's implementation is
one realization of it.

## When to Apply

- A consumer repo's migration or refactor work produces a working set
  of cleanup or removal rules that the skill does not document, and
  the rules show signs of being more than one-off (cover multiple
  directive families, involve non-trivial edge cases, or are likely to
  recur in other consumer corpora).
- The skill already has authoring-direction coverage of the same
  directive family, and the gap is specifically on the inverse
  direction.
- The rule set is large enough to warrant a dedicated file but small
  enough to fit in a single focused reference doc (rough target:
  350-500 lines; document the rationale if the doc lands above).
- The skill version bump can ship in the same PR as the new reference
  doc to keep marketplace consumers' upgrade signal clean.

This guidance is **not** universally applicable. When a single rule
is small enough to live as a one-paragraph addition to
`best-practices.md`, do that instead — a new top-level reference doc
has a discoverability tax that only pays back when the rule set is
substantial. Use judgment.

## Examples

**Locating the new doc.** The naming convention used here was
`comment-manipulation.md`, matching the surface area it covers (any
manipulation of the `<!-- ... -->` directive family — removal and
reduction in this pass, but the file name leaves room for future
manipulation rules to land in the same file rather than fragmenting
across `comment-removal.md`, `comment-reduction.md`, etc.).

**Cross-reference pattern.** A two-sentence pointer attached to the
densest related mistake in `best-practices.md`:

```markdown
If you are removing directives rather than authoring them, see
[`comment-manipulation.md`](comment-manipulation.md) for safe-removal
rules and the table-cell edge cases that make hand-removal
error-prone.
```

The pointer does not summarize the rules; it points at them. The
authoring doc stays authoring-focused; the cleanup doc stays
cleanup-focused.

**SKILL.md references-list bullet.** A single line in the
`<references>` block, placed near sibling reference docs of similar
scope:

```markdown
- comment-manipulation.md — Rules for safely removing or simplifying
  Markdown++ directive comments during cleanup or migration passes
```

**The "Reference Implementation" pattern.** End-of-doc section names
the consumer-repo scripts and helper-function inventory, with the
explicit independence caveat:

```markdown
## Reference Implementation

A working implementation of these rules exists in the `epublisher-docs`
repository under `.claude/scripts/`. Those scripts live in a separate
repository and may evolve independently of this reference; the rules
above are the durable contract.
```

This shape keeps the skill doc language-agnostic while still pointing
a re-implementer at a working reference.

## Practical gotchas surfaced during this work

Two specific gotchas earned by the issue #94 work, recorded here so
future skill-reference-doc authors do not rediscover them:

**1. `validate-mdpp.py` does not skip inline code spans.** The
validator strips fenced code blocks before checking directive syntax,
but it does **not** strip inline code spans. Prose-embedded placeholder
directives like `` `<!--style:...-->` `` or `` `<!--#alias-->` ``
will surface as MDPP002 validation errors because `...` is not a
valid style or alias name. Use valid placeholder names instead:
`` `<!--style:Name-->` ``, `` `<!--#cell-anchor-->` ``. The same
issue affects `best-practices.md` — checking the validator's behavior
on an existing reference doc before drafting a new one confirms this
is not a defect specific to the new doc.

**2. Relative path depth from `references/` to `spec/` is 5 levels,
not 4.** From any `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/*.md`
file, the path to `spec/specification.md` is
`../../../../../spec/specification.md`. Verify the depth against
`best-practices.md`'s existing cross-references rather than counting
directory levels by hand — it is easy to be off by one.

**3. Run `format-tables.py --in-place` during authoring, not as a
pre-commit fix step.** If the new doc contains Markdown tables (an
anchor decision table, a Markdown-token pairings table, etc.),
authoring directly in canonical table format avoids a noisy "format
the tables I just wrote" commit. The skill's own
`format-tables.py --check` is what `ce-code-review` will run; matching
its output during authoring keeps the review pass quiet.

## Related

- New reference doc shipped by this work:
  [`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md)
- Sibling skill-authoring convention covering the description surface:
  [`skill-activation-description-completeness-2026-05-09.md`](skill-activation-description-completeness-2026-05-09.md)
- Tooling-decision doc covering the table-formatter design that backs
  the formatting gotcha above:
  [`../tooling-decisions/markdown-table-formatter-design-2026-05-09.md`](../tooling-decisions/markdown-table-formatter-design-2026-05-09.md)
- GitHub issue #94 — origin of the comment-manipulation reference doc
- Plan commit: `be83329` (`docs(plans): plan comment manipulation knowledge reference doc (#94)`)
- Brainstorm commit: `d63a6f1` (`docs(brainstorms): capture comment manipulation knowledge requirements (#94)`)
- Work commits: `6bfca29` (feat), `77b4737` (autofix) on `claude/issue-94`
