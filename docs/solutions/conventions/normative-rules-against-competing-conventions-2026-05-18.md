---
title: State load-bearing structural rules normatively when readers carry competing conventions from a parent format
date: 2026-05-18
category: conventions
module: plugins/markdown-plus-plus/skills/markdown-plus-plus
problem_type: convention
component: documentation
severity: medium
applies_when:
  - Authoring or revising guidance for an idiom whose meaning depends on a non-obvious structural property (placement, ordering, adjacency, grouping)
  - The format extends or builds on a parent format that has its own established convention for the same structural property
  - The example in the docs already shows the correct shape, but the surrounding prose describes it with grouping verbs like "combines," "pairs with," or "together with" rather than positional language
  - The validator or other automated check cannot detect a violation of the rule
  - Investigating a report where an agent produced a layout that is technically valid under the parent format but breaks the idiom's intended behavior
  - Reviewing a recommended pattern that pairs multiple directives whose maintainability depends on co-location
tags:
  - skill-authoring
  - normative-framing
  - placement-rules
  - commonmark-inheritance
  - show-by-example-failure
  - markdown-plus-plus
  - copy-paste-templates
---

# State load-bearing structural rules normatively when readers carry competing conventions from a parent format

## Context

The `markdown-plus-plus` skill recommends the **alias+slug+linkref triple** as the cross-reference idiom for topic-defining headings: an `<!-- style:HeadingN; #target -->` directive on one line, the heading on the next, a blank line, then a `[semantic-slug]: #target "Title"` link reference definition. The three pieces sit adjacent in source on purpose -- if a section moves, all three pieces move with it, and the slug stays bound to the heading it names.

That adjacency is **load-bearing**: it preserves the contract that "moving the heading moves the slug." But across `references/best-practices.md`, `SKILL.md`, and `examples/semantic-cross-references.md`, the rule was *shown* by example and *described* with grouping verbs -- "combines three pieces," "the paired definition," "the link reference definition below it" -- but never stated as a positional rule. A reader carrying CommonMark instincts has a strong competing convention: link reference definitions conventionally collect at the bottom of the file in a single block. Nothing in the skill pushed back against that instinct.

The failure case was reproducible. An AI agent applying the skill across 16 topic files authored the directive correctly on every heading, then collected every link reference definition into a bottom-of-file block per CommonMark convention. The agent rationalized the choice in ways the skill did not contradict: "CommonMark allows link reference definitions anywhere"; "bottom-of-file is conventional Markdown style"; "placing the definition between a Glossary Term and its Glossary Def paragraph breaks the visual pair in source." The validator passed both layouts. The user caught it manually and the agent moved every definition back. The failure was not an agent reasoning error -- it was a docs-load-bearing assumption that the docs never wrote down.

## Guidance

When an idiom's behavior depends on a structural property the parent format does not constrain, state the property as a positional rule, not just a grouping description. Apply these rules:

**1. Use positional language, not grouping verbs.** "Combines," "pairs with," "together with," and "below it" describe relationship; they do not describe placement. A reader who already knows the parent format's competing convention reads grouping language as "the two work together somewhere in the document," not "the two sit at specific positions relative to each other." Replace grouping verbs with explicit positional language: "on the line directly above," "on the next non-blank line after," "separated by a single blank line," "adjacent in source."

**2. Name the competing convention and contrast it explicitly.** A reader inheriting from a parent format brings the parent's conventions with them. Naming the competing convention and stating that the idiom diverges from it is more effective than silently presenting a different shape. Add a contrast note: "general-purpose link reference definitions are conventionally grouped at the bottom of the file (standard CommonMark style); the triple's link reference definition lives adjacent to its heading. Both are valid CommonMark, but the conventions encode different intent." The contrast makes the rule survive the reader's existing instincts.

**3. Surface the maintainability rationale that makes the rule load-bearing.** A normative line answers "what is the rule"; a rationale answers "why does breaking it matter." For the triple, the rationale is "when a section moves, all three pieces move as a unit." Without the rationale bullet, the placement rule reads as a stylistic preference; with it, the rule reads as a contract the layout enforces. Add the rationale to the existing "Why this is the recommended idiom" list -- alongside any other rationale bullets -- so a reader scanning the rationale sees the maintainability claim that depends on the layout.

**4. Touch every surface a reader loads when authoring the idiom.** Skill authoring usually loads three surfaces in sequence: the high-level recommendation (here, `SKILL.md`'s Custom Aliases section), the deep reference (`references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings* and § *Advanced Patterns → Link References*), and the canonical specimen (`examples/semantic-cross-references.md`). State the rule on **every** surface that recommends the idiom, not only the deepest one. A reader loading only `SKILL.md` should learn the placement rule from that surface alone -- they cannot rely on having loaded the reference doc that holds the canonical statement.

**5. Make specimens function as copy-paste templates.** When a specimen file already demonstrates the correct shape on every heading, the specimen is naturally read as a copy-paste template. Add a brief callout inside the existing structure-explanation section (do not introduce a new section) that names the placement rule explicitly and links to the deep rationale. A specimen with a placement-rule callout copies safely; a specimen without one copies whatever shape the reader's prior conventions encourage.

**6. Forbid the failure mode by name.** When one specific anti-pattern recurs across reports, name it: "do not migrate the link reference definitions to a block at the bottom of the file in conventional CommonMark style." Naming the anti-pattern in the same paragraph as the rule closes the gap an agent would otherwise fill by reaching for its prior convention. Cite the parent format's competing convention by name so the agent recognizes the pattern it should not apply here.

**7. Apply the version-bump convention even on small text changes.** The change is content-only and does not modify the format or any directive. A `scripts/bump-version.sh patch` bump is appropriate under `CLAUDE.md` § Version Management -- "documentation updates" map to patch. Ship the CHANGELOG entry in the same PR.

## Why This Matters

Show-by-example documentation works when the reader has no competing convention to fall back on. It fails silently when the reader inherits from a parent format that constrains the same structural property differently. The reader sees the example, sees the surrounding prose describe the pieces with grouping language, and assembles a mental model that satisfies the grouping description while honoring their prior convention. The result is a layout that is technically valid under the parent format and technically broken under the idiom. Neither the validator nor the parent format's tooling can detect the mismatch -- the validator sees a valid Markdown++ document with valid CommonMark link reference definitions, and CommonMark sees a perfectly normal link reference table at the bottom of the file.

The cost is paid in failed authoring sessions, manual user corrections, and (in this case) 16 files that had to be relocated by hand. The cost was invisible until the user inspected the output. A normative line stating the placement rule, plus a contrast note naming the competing convention, plus a maintainability rationale, would have prevented the failure outright. The cost of writing those three additions is one paragraph per surface and one new bullet in an existing rationale list. The cost of not writing them is recurring silent breakage every time an agent applies the idiom while carrying CommonMark instincts.

The contrast note in rule 2 matters specifically because it works *with* the reader's existing knowledge rather than against it. A reader who already knows "CommonMark link reference definitions go at the bottom" gets the more useful framing: "this idiom diverges from that convention on purpose, here is why." A reader who does not know the CommonMark convention loses nothing -- they read the contrast as a clarification rather than a competing pull. Either reader leaves with the right model.

The maintainability rationale in rule 3 matters because rules without rationale invite "harmless exceptions." A reader who sees only "the three pieces sit adjacent" reads the rule as stylistic and may decide a specific case justifies an exception (e.g., "the link ref would interrupt the Glossary Term / Def pair in source"). A reader who also sees "the three pieces move as a unit when a section moves; splitting them lets a section move silently desync the slug from its target" understands the cost of the exception and is less likely to take it.

## When to Apply

- The idiom's behavior depends on a structural property (placement, ordering, adjacency, grouping) that is not enforceable by the validator or any other automated check.
- The format extends or builds on a parent format with its own established convention for the same structural property -- and the parent's convention is more familiar to most readers than the idiom's.
- The current docs describe the pieces with grouping verbs ("combines," "pairs with," "below it") rather than positional language.
- A report or PR review shows an author -- human or agent -- producing the parent format's convention instead of the idiom's shape, and the validator did not catch it.
- A canonical specimen file demonstrates the correct shape on every instance but lacks a callout naming the placement rule.

Do **not** apply when:

- The structural property is actually enforced by the validator or by a linter. Validators that enforce the rule are sufficient -- the failure mode this convention guards against is the *silent* kind. If the rule fires loudly when broken, the docs do not need to over-state it.
- The idiom does not extend or inherit from a parent format. With no competing convention to displace, show-by-example carries the placement rule without needing positional language. Use judgment -- the cost of over-stating is small, but the framing is most justified when there is a competing convention to displace.
- The structural property is purely stylistic (no behavior or maintainability contract depends on it). The cost-benefit favors letting authors choose. Only escalate to normative framing when violating the rule produces a silent behavioral or maintainability failure.

## Examples

### The triple's three load-bearing surfaces

The placement rule for the alias+slug+linkref triple now appears in positional language on three surfaces a reader would naturally load:

`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` § *Semantic Cross-References on Topic-Defining Headings*, immediately after the canonical example block:

```markdown
**All three pieces appear adjacent:** the directive on the line directly above
the heading, the heading itself, a single blank line, then the link reference
definition on the next line. Co-location is part of the pattern, not a layout
choice -- do not migrate the link reference definitions to a block at the
bottom of the file in conventional CommonMark style.
```

The same file's "Why this is the recommended idiom" list, expanded with the maintainability rationale:

```markdown
- **The three pieces move as a unit when a section moves.** Because they sit
  adjacent in source, a heading rename, deletion, or reordering carries the
  directive and the link reference definition with it. Splitting them across
  the file -- for example, collecting all link reference definitions in a
  block at the bottom -- means a section move can silently desync the slug
  from its target, and the validator cannot detect the mismatch.
```

The same file's § *Advanced Patterns → Link References* section, with the contrast note:

```markdown
**Placement differs from the triple pattern.** General-purpose link reference
definitions are conventionally grouped at the bottom of the file -- the
standard CommonMark style. The triple's link reference definition, by
contrast, lives adjacent to its heading [...]. Both placements are valid
CommonMark, but the conventions encode different intent: grouped definitions
signal "this is a shared URL table that many parts of the document point
at"; adjacent definitions signal "this is the semantic slug for *this*
heading, and the two move together." Do not migrate triple definitions into
the bottom-of-file block.
```

`SKILL.md` Custom Aliases recommended-pattern bullet, rewritten in positional language:

```markdown
- **What to author:** all three pieces, adjacent in source -- the
  <!-- style:HeadingN; #target --> directive on the line directly above
  the heading, the heading itself, and a [semantic-slug]: #target "Title"
  link reference definition on the line directly after the heading
  (separated by a single blank line). Do not migrate the link reference
  definition to a block at the bottom of the file.
```

`examples/semantic-cross-references.md` § *The pattern*, with the placement-rule callout:

```markdown
**The three pieces sit adjacent in source on every linkable heading:**
directive line, heading line, blank line, link reference definition. The
headings below show the shape -- copy this layout, do not collect the link
reference definitions in a block at the bottom of the file.
```

### The grouping-verb wording the change replaced

The wording the rewrite displaced -- preserved here as the recognizable failure shape:

```markdown
- **What to author:** all three pieces -- the <!-- style:HeadingN; #target -->
  directive on the heading, the heading itself, and a [semantic-slug]:
  #target "Title" link reference definition below it.
```

"Below it" is the load-bearing failure -- it reads as a constraint about which side of the heading the definition lives on, not as a constraint about the line immediately following. A reader who interprets "below" as "anywhere below in the file" is reading the sentence reasonably; the sentence does not pin them down. The rewrite in the preceding subsection swaps "below it" for "on the line directly after the heading (separated by a single blank line)" -- positional language that does not survive misreading.

### What this does not say

The convention does **not** say all show-by-example documentation should be hardened with positional language. It says positional language is justified when the idiom's behavior depends on a structural property the parent format does not constrain, and when readers carry a competing convention from that parent format. For idioms with no parent-format competition, show-by-example carries the pattern fine.

The convention also does **not** advocate pushing the rule into the spec. The placement rule is a recommended idiom, not a syntactic requirement -- CommonMark allows link reference definitions anywhere, and Markdown++ inherits that. Pushing adjacency into the spec would imply the validator should enforce it, which is explicitly deferred. The right home for the normative line is the prescriptive style guide (`best-practices.md`) and the surfaces that recommend the idiom (`SKILL.md`, `examples/`); the spec stays silent because the rule is not a parser concern.

## Related

- [[imperative-anchor-section-for-skill-syntax-drift]] -- a sibling convention covering a different lever for the same broad failure class (agent drift on documented patterns). That doc covers adding an imperative anchor *section* high in SKILL.md when the body content is technically complete but the patterns are scattered. This doc covers rewording *existing* prose from grouping verbs to positional language when readers carry competing conventions from a parent format. The two are complementary: the anchor section gives the canonical copy-paste form a high-visibility home; positional framing makes the rule survive misreading wherever it appears.
- [[skill-activation-description-completeness]] -- the routing-time analogue for a different class of silent failure (skill does not fire). That doc covers the description frontmatter as a routing contract; this doc covers the skill body as a normative contract once routing succeeds.
- [[skill-reference-docs-capture-cleanup-knowledge]] -- covers when a consumer repo's discoveries should become a new reference doc. This doc covers when an existing reference doc's prose should be rewritten to make a load-bearing rule explicit. Both deal with the "the skill teaches the pattern but the pattern still fails downstream" pattern, from different angles.
- GitHub issue #103 -- this issue. Origin: an agent's 16-file misapplication of the triple, caught and corrected by the user.
- GitHub issue #96 -- made the alias+slug+linkref pattern recommended; established the canonical example.
- GitHub issue #99 -- audited the "triple" terminology across repo surfaces; established the named term.
- Brainstorm: `docs/brainstorms/2026-05-18-triple-adjacent-placement-requirements.md`
- Plan: `docs/plans/2026-05-18-001-docs-triple-adjacent-placement-plan.md`
- Work commit: `1e66214` on `claude/issue-103` -- the three-surface rewrite that motivated this convention.
