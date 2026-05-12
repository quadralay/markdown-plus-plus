---
date: 2026-05-11
topic: alias-slug-linkref-recommended
status: active
---

# Make alias+slug+linkref the Recommended Cross-Reference Idiom

## Problem Frame

The Markdown++ spec treats the **alias + slug + link-reference** triple as the
idiomatic cross-reference mechanism. `spec/whitepaper.md` Section 3
("Semantic cross-references that work everywhere") frames the pattern as the
core resilience story:

```markdown
<!-- style:Heading1; #316492 -->
## About IPsec Peering Connections

[about-ipsec-peering-connections]: #316492 "About IPsec Peering Connections"
```

`spec/cross-file-link-resolution.md` calls the same pattern "the primary use
case for cross-file link reference resolution" (line 171), and its Worked
Examples A and B use it consistently.

Two gaps undermine that positioning:

1. **Internally inconsistent spec examples.** The conflict-resolution
   example in `spec/cross-file-link-resolution.md` (lines 65-86) shows
   bare `[slug]: #root-target`, `[slug]: #chapter-a-target`, and
   `[slug]: #chapter-b-target` definitions without ever showing the alias
   on a heading that would produce those anchors. A reader following the
   whitepaper's working pattern expects `<!-- style:Heading1; #root-target -->`
   above a heading; without it, a reader could misread the example as claiming
   the heading anchor is `#root-target` (CommonMark would actually produce
   `#root-content`). The MDPP014 trigger example in
   `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md`
   (lines 421-430) has the same dangling-target defect.

2. **Best-practices framing contradicts the spec.** The Link References
   section in
   `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
   (lines 540-571) currently frames link references as "generally not
   recommended" and lists the alias+slug pattern as one of several
   **advanced** use cases. This contradicts how the spec positions the
   pattern. Authors who add a custom alias to a heading but stop short of
   the matching link-reference definition have only solved half the
   problem -- the alias creates a stable anchor, but no semantic slug
   references it.

The intent of attaching a custom alias to a heading already implies the
intent to make that heading externally referenceable. The natural pairing
is: alias on the heading + link reference definition with a semantic slug
+ the slug used in references throughout the assembly.

## Requirements

- **R1. Spec example correction (`cross-file-link-resolution.md`).** The
  Conflict Resolution > Definition Order example (lines 65-86) MUST show
  a heading with `<!-- style:HeadingN; #target -->` above each link
  reference definition so the targets actually resolve. The fix matches
  the structure of Examples A and B in the same file.

- **R2. MDPP014 example correction (`error-codes.md`).** The MDPP014
  trigger example (lines 421-430) MUST follow the same alias-on-heading
  structure so it is internally consistent with the spec.

- **R3. Best-practices reframing.** The Link References section in
  `references/best-practices.md` MUST split its framing into two
  subsections:
  - **General-purpose link references** (arbitrary URL reuse, version
    redirection, long URLs): remain marked as advanced/optional, with the
    existing rationale preserved.
  - **Alias+slug+linkref on topic-defining headings**: promoted to
    **recommended**. Recommend the pattern on file titles, primary H1s,
    and significant H2 headings, with the rationale that the same
    reference works in standalone preview, single-file publishing, and
    multi-file assembly, and survives heading text changes.

- **R4. Syntax-reference guidance.** The Custom Aliases section of
  `references/syntax-reference.md` MUST include a brief note recommending
  the paired link-reference-definition pattern when an alias is intended
  to mark a referenceable endpoint (as opposed to an internal-only
  anchor). The note links to the new best-practices subsection for
  detail.

- **R5. SKILL.md authoring directive.** `SKILL.md` MUST include explicit
  guidance directing the skill -- and AI agents using it -- to apply the
  alias+slug+linkref pattern when authoring or editing Markdown++ topic
  files with significant headings (titles, primary H1s, structurally
  important H2s). This is the highest-leverage change; newly authored
  content inherits the idiom by default.

- **R6. Plugin version bump.** Per the repo's Version Management
  conventions (`CLAUDE.md` § Version Management), this PR ships through
  the skill's `references/*.md` and `SKILL.md` surface and therefore
  requires a version bump. `patch` is appropriate -- forward-looking
  documentation guidance, no format or directive change.

## Success Criteria

- The previously-dangling example in `cross-file-link-resolution.md`
  shows a real anchor on a heading and is consistent with Examples A and
  B in the same file. A reader following the pattern can copy it
  verbatim into their own document and have it resolve.
- The MDPP014 trigger example in `error-codes.md` uses the same
  alias-on-heading structure.
- `best-practices.md` makes it obvious which form of link reference is
  recommended (alias+slug+linkref on significant headings) and which
  remains advanced (general-purpose definitions).
- `syntax-reference.md` directs a reader who just learned about custom
  aliases to the paired-pattern guidance.
- `SKILL.md` directs AI authors to apply the pattern on significant
  headings when writing or editing topic files.
- A new Markdown++ topic file authored by an AI using the skill includes
  the alias+slug+linkref triple on its title and primary headings
  without further prompting.

## Scope Boundaries

**In scope:**
- Edits to `spec/cross-file-link-resolution.md` (conflict-resolution example only).
- Edits to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/error-codes.md` (MDPP014 trigger example only).
- Restructure of the Link References section in
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`.
- Targeted addition to the Custom Aliases section of
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`.
- Authoring directive added to `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`.
- Patch-level version bump via `scripts/bump-version.sh patch`.

**Out of scope** (explicit in the issue):
- Retrofitting existing Markdown++ files in this repo to apply the
  pattern. The change is forward-looking guidance, not a migration. The
  spec's Worked Examples A and B already use the pattern; other repo
  documents do not need to be reworked.
- Changing CommonMark behavior or introducing new directives. The
  pattern uses only existing Markdown++ and CommonMark constructs.
- Coordinating with the `webworks-claude-skills:markdown-plus-plus`
  sibling skill in the WebWorks plugin repo. That repo manages its own
  release cadence; alignment is a separate workstream.
- Adding any lint rule to `scripts/validate-mdpp.py` that flags an alias
  without a paired link-reference definition. The new guidance is a
  recommendation, not a hard rule, and a lint check would over-trigger
  on internal-only anchors.

## Key Decisions

- **The MDPP014 trigger example keeps its slug-collision narrative.**
  The example exists to illustrate two files defining the same `overview`
  slug. The fix adds the alias on a heading in each file so the targets
  resolve, but keeps the collision intact. The example does not switch
  to numeric alias IDs (e.g., `#200010`) because the collision story is
  about slugs, not about ID format choice.

- **`best-practices.md` keeps the "Why inline links are preferred"
  rationale.** The reframing splits the section, but the existing
  rationale for preferring inline links over general-purpose link
  references stays. Only the alias+slug+linkref subsection is promoted;
  the general advice against arbitrary `[install-guide]: #installation`
  reference definitions does not change.

- **`SKILL.md` guidance lives in the Custom Aliases subsection.** The
  authoring directive belongs adjacent to existing alias guidance, not
  as a new top-level section. AI agents already reading the alias rules
  will see the paired-pattern recommendation in context.

- **The convention is recommendation, not requirement.** Aliases used as
  internal-only anchors (e.g., to support `add-aliases.py`-generated
  anchors that are never linked externally) remain valid. The
  recommendation applies when the author's intent is to make the
  heading externally referenceable -- which the issue argues is the
  default intent for custom aliases on titles and primary headings.

## Assumptions

These are inferred bets from the issue body, recorded so downstream
review can scrutinize them rather than have them disappear into Key
Decisions:

- **"Significant headings" = file title H1 and structurally important
  H2s.** The issue's literal wording is "file titles, primary H1, and
  significant H2 headings (depending on document structure)." H3+
  headings are author judgement, not blanket policy. The skill
  directive should reflect that scope explicitly so AI agents do not
  over-apply.

- **The conflict-resolution example keeps descriptive target names**
  (`#root-target`, `#chapter-a-target`, `#chapter-b-target`) rather than
  converting to numeric alias IDs. The issue says "Pattern matches
  Examples A and B" in terms of structure (heading + style+alias
  directive + link-ref definition), not in terms of ID format. Keeping
  the descriptive names preserves the example's pedagogy about
  slug collisions while making the targets resolvable.

- **Patch-level version bump is correct.** The change is forward-looking
  documentation and skill guidance with no breaking format change. The
  repo's `CLAUDE.md` § Version Management lists `patch` for "Bug fixes,
  documentation updates, minor improvements"; the editorial position
  shift and the example-bug fixes both fit that category.

## Open Questions

None. The issue's acceptance criteria fully specify the intended
behavior, and the in-scope edits are mechanical apart from the
editorial framing in `best-practices.md`, which the issue body
prescribes in enough detail to plan against.

## Next Step

Hand off to `/compound-engineering:ce-plan` to produce the file-by-file
edit plan, then implement with the standard `ce-work` flow. Version
bump via `scripts/bump-version.sh patch` lands in the same PR per
`CLAUDE.md` § Version Management.
