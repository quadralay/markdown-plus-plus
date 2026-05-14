---
date: 2026-05-13
topic: terminology-surfacing-audit
status: active
---

# Terminology Surfacing Audit: "triple" and Adjacent Terms

## Problem Frame

PR #94 introduced the **alias+slug+linkref "triple"** as a name for the
recommended cross-reference pattern. The term is well-defined in
`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
(the "Semantic Cross-References on Topic-Defining Headings" section,
line 573 onward) and referenced briefly in
`plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
("the recommended pattern for referenceable headings").

A targeted grep shows the term `triple` appears in only **three current
surfaces**: `best-practices.md`, `SKILL.md`, and `CHANGELOG.md`. Every
other surface that discusses the pattern either uses different language
("the recommended Markdown++ cross-reference idiom", "the semantic
cross-reference pattern", "three parts", "three elements") or describes
the pattern in prose without naming it. Most readers, contributors, and
AI agents enter Markdown++ through one of those other surfaces.

Downstream content is starting to reference Markdown++ patterns by name --
the WebWorks brain repo's Reverb 2026.1 Source IDs blog draft is the
concrete trigger -- and inconsistent upstream terminology forces
downstream authors to either pick a winning surface, invent their own
framing, or guess. A canonical home that every surface links to prevents
that drift.

The same gap exists for several other terms (Unset/pass-through,
attachment rule, content island, block content in multiline cells), and
the discipline gap that produced this state will reproduce on the next
PR that introduces a term unless the team has a routine check at PR
time. This brainstorm covers both: the term audit itself, and the
mechanism to keep it from drifting again.

## Out of Scope

- Changing the meaning, behavior, or syntax of any term.
- Renaming `triple`, `Unset`, `attachment rule`, `content island`, or
  any other established term.
- Cross-repo propagation: the brain repo, the marketing whitepaper, the
  website. Those follow once the upstream canonical surface lands.
- Adding glossary entries for terms that have **zero current presence**
  in this repo (e.g., "Source ID" -- a Reverb 2026.1 concept that lives
  in downstream drafts, not yet here). Defer until the term lands
  upstream in either spec or skill content.

## Requirements

### R1. Create `GLOSSARY.md` at the repo root

A single canonical home for Markdown++ terminology with one-paragraph
definitions and a "Full treatment" pointer per term. Selected over
elevating the best-practices section because:

- The issue lists six other terms in the same state -- scaling beats
  canonicalizing one section.
- Surfaces that need only a short definition can link to one place;
  surfaces that need the long form continue to link to the spec or
  best-practices section.
- A repo-root `GLOSSARY.md` is the conventional location and is
  reachable from `README.md`, the spec, and the skill.

**Frontmatter:** `date`, `status: active`. Follows the repo's
frontmatter rule for non-README docs.

**Initial entries** (terms with current presence in the repo):

| Term | Canonical definition lives at |
|------|-------------------------------|
| **triple** (alias+slug+linkref) | `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings` |
| **alias+slug+linkref** | Same as above (synonym -- one entry, both forms named) |
| **Unset** / pass-through condition | `spec/specification.md` Section 11.3 (Condition State Model) |
| **attachment rule** | `spec/attachment-rule.md` |
| **content island** | `spec/specification.md` Section 15 |
| **block content** in multiline cells | `spec/multiline-cell-extensions.md` |

Each entry: term, one-paragraph definition (extractable from the
canonical surface), and a "Full treatment" link to that surface. No new
content is authored -- the glossary is a directory, not a textbook.

### R2. Surface-by-surface audit -- minimal, targeted edits

For each surface, add the term **only where the pattern is already
discussed in prose**. Surfaces that don't currently cover the pattern
are not edited (no speculative content).

| Surface | Current state | Action |
|---------|---------------|--------|
| `README.md` | No mention of the cross-reference pattern at all | **No edit** -- not the right surface for a deep-link pattern. Add a `See [GLOSSARY.md](GLOSSARY.md) for terminology.` line where contributing/specs are introduced. |
| `spec/specification.md` Section 17.3 | "The Semantic Cross-Reference Pattern" heading, describes "three elements" | Add `(the **alias+slug+linkref triple**)` and link to `GLOSSARY.md#triple` |
| `spec/cross-file-link-resolution.md` | Uses "semantic cross-reference pattern" | Add `(the **triple**)` once on first use; link to `GLOSSARY.md#triple` |
| `spec/whitepaper.md` | (grep returned no current mention of "semantic cross-reference" / "triple") | **No edit** unless audit finds a discussion of the pattern. Out of scope to add new whitepaper content. |
| `examples/semantic-cross-references.md` | Says "three parts" | Replace with "Every linkable heading uses the **alias+slug+linkref triple**" and link to `GLOSSARY.md#triple` |
| `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` | Line 464 says "recommended Markdown++ cross-reference idiom" | Add `(the **triple**)` and link to glossary |
| `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md` | No pattern-catalog entry for cross-references at all | **No edit** -- adding a new scenario is content authoring, not surfacing. Could be a follow-up issue. |
| `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` | Already uses "alias+slug+linkref triple" | Add a one-line link to `GLOSSARY.md#triple` near the existing reference (no rewrite) |

**Edits for other terms** (Unset, attachment rule, content island,
block content) are limited to **adding the GLOSSARY.md link** where the
term is already used and the link is missing. No new prose, no
rewrites.

### R3. Add a PR-time discipline mechanism

Create `.github/PULL_REQUEST_TEMPLATE.md` -- the `.github/` directory
does not exist today. Standard PR template content with a terminology
checkbox added:

```markdown
## Terminology

- [ ] If this PR introduces or renames a Markdown++ term, `GLOSSARY.md`
      and at least one entry-point surface (README, spec, or skill) have
      been updated.
```

Selected over a `CONTRIBUTING.md` addition because:

- The check fires at PR-open time, which is where the gap was
  discovered.
- A PR template is the conventional surface for PR-time checklists.
- `CONTRIBUTING.md` is read once; a PR template appears every time.

A short note in `CONTRIBUTING.md` pointing to the template is
reasonable but optional.

### R4. Repeatability for the audit itself

A brief paragraph in `GLOSSARY.md` (or alongside it as a comment) names
the audit's repeatable form: grep the term across the surface list
above, decide per (term, surface) pair whether to use the term + link
to glossary or leave it untouched. This is documentation of the
process, not a runnable script.

## Assumptions (Inferred during synthesis)

- **GLOSSARY.md beats elevating best-practices** as the canonical home.
  Driven by the issue's enumeration of other terms in the same state.
- **"Source ID" is deferred from v1.** Grep returned no current
  presence in this repo; adding a glossary entry for a term that lives
  only in downstream drafts is over-reach for a surfacing audit. Add
  when the term lands upstream.
- **The discipline mechanism is a PR template**, not a CONTRIBUTING.md
  addition. Surfaces the check at the right moment.
- **The audit does not author new prose** in surfaces that don't
  currently discuss the pattern. The README and whitepaper get a glossary
  pointer at most; the examples.md catalog gets nothing.
- **One synonym entry handles both `triple` and `alias+slug+linkref`.**
  They name the same thing.

## Success Criteria

1. `GLOSSARY.md` exists at the repo root with six initial entries
   (triple/alias+slug+linkref, Unset, attachment rule, content island,
   block content), each linking to its canonical surface.
2. Every surface in R2 that currently discusses the cross-reference
   pattern names it as **the triple** (or **alias+slug+linkref triple**)
   and links to `GLOSSARY.md#triple`.
3. `.github/PULL_REQUEST_TEMPLATE.md` exists with a terminology
   checkbox.
4. The `CHANGELOG.md` records the addition under a 1.5.0 entry (minor:
   new doc surface, no behavior change).
5. The plugin version is bumped to 1.5.0 via `scripts/bump-version.sh
   minor` before PR.
6. The change closes #99 and does not modify the meaning of any
   existing term.

## Open Questions (for planning)

None blocking. The following are minor and can be decided during
implementation:

- Whether to include a `## Conventions` paragraph in `GLOSSARY.md`
  describing the entry shape, or to let the entries speak for
  themselves. Default: include one short paragraph.
- Whether the PR template should include other standard sections
  (summary, test plan, checklist) beyond the terminology check. Default:
  include a minimal summary section to keep the template usable for
  non-terminology PRs.

## Handoff

Next step: `/ce-plan` (or direct implementation). The work is small,
mostly mechanical, and the surfaces and decisions are enumerated. A
heavyweight planning pass is probably overkill.
