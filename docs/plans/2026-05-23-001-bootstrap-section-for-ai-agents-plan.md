---
date: 2026-05-23
status: active
issue: 110
plan_type: docs
---

# docs: Add Bootstrap Section for AI Agents

## Summary

Add a new top-level **For AI agents** section to `README.md` (placed
above the existing `## Tools` section) that documents two ingestion
paths into the Markdown++ skill: the Claude-Code-specific marketplace
install (the existing slash commands, reframed) and a
generic-harness path that names
[`plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md)
as the entry point and the sibling
[`references/`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/)
directory as the payload an agent should load.

Add a one-line pointer near the top of `CLAUDE.md` so an agent reading
that file first sees the hand-off to the new README section early
rather than having to infer it from the in-repo authoring discipline
content. Bump the plugin patch version (`1.7.0 → 1.7.1`) and record
the change in `CHANGELOG.md` under **Documentation**.

---

## Problem Frame

A customer support exchange on 2026-05-22 surfaced the gap. The
customer asked how to get their agent harness to ingest the
`markdown-plus-plus` skill from a cold clone of the repo. There was
no documented bootstrap statement to point them at:

- The existing slash commands at `README.md` lines 46-49 are framed as
  *marketplace install* instructions, useful only to users already
  inside a Claude Code session. They are not framed as bootstrap
  guidance for a generic agent harness.
- `CLAUDE.md` is scoped to in-repo authoring discipline -- how agents
  *editing* this repo should behave. It does not route an outside
  harness to the skill payload.

The result: agents arriving from a cold clone cannot self-orient. The
fix is a documentation breadcrumb -- no spec change, no skill change,
no tooling change. Two surfaces, two short additions.

This issue is sequenced behind [#108](https://github.com/quadralay/markdown-plus-plus/issues/108)
(Unicode-letter aliases) so the README and `CLAUDE.md` pointers added
here can reference a stable skill payload without merge churn from
the parallel grammar updates to `syntax-reference.md` and
`error-codes.md`.

---

## Requirements

Carried forward from the issue body. The plan does not introduce new
requirements; it sequences and operationalizes R1-R8.

- **R1.** `README.md` gains a clearly labeled section
  (**"For AI agents"**) placed above the existing `## Tools` section
  so it is discoverable before the marketplace install commands.
- **R2.** The section documents two ingestion paths:
  - **Claude Code path.** Reframes the existing slash commands at
    `README.md` lines 46-49 as the recommended approach when the
    user's harness is Claude Code. The slash commands themselves are
    not rewritten -- they are pointed at from the new section and
    remain verbatim in `## Tools`.
  - **Generic harness path.** Points at
    [`plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md)
    as the entry point. States that its YAML frontmatter declares
    trigger signals and that the sibling `references/` directory
    contains the syntax-reference, examples, and best-practices
    payload an agent should load. One short paragraph is sufficient.
- **R3.** The `SKILL.md` path is formatted as a clickable Markdown
  link, not a bare path.
- **R4.** `CLAUDE.md` gains a one-line pointer to the new README
  section. Placement: at the end of the existing `## Overview` block
  (the first content a cold-clone agent reads after the title).
  Wording is the implementor's call; the intent is that an agent
  reading `CLAUDE.md` first sees the hand-off to README early.
- **R5.** `README.md` continues to render correctly on GitHub: no
  broken links, no malformed code blocks, no orphan anchors. The
  existing `## Tools` section is left intact -- its install commands
  are now contextually positioned as the Claude-Code-specific path
  but the verbatim commands are preserved.
- **R6.** No changes outside `README.md` and `CLAUDE.md` other than
  the version bump and `CHANGELOG.md` entry required by repo
  convention. Spec files, skill files, scripts, and tests are
  unaffected.
- **R-bump.** Bump plugin version `1.7.0 → 1.7.1` via
  `scripts/bump-version.sh patch` (documentation update, no behavior
  change) and add a 1.7.1 entry under **Documentation** in
  `CHANGELOG.md`.

---

## Scope Boundaries

### In scope

- New **For AI agents** section in `README.md` above `## Tools`.
- One-line pointer in `CLAUDE.md`'s `## Overview` block.
- Version bump to 1.7.1 (`plugin.json` + `marketplace.json` via the
  bump script) and a `CHANGELOG.md` entry.

### Deferred to Follow-Up Work

- **Top-level `AGENTS.md` file.** Some harnesses auto-read `AGENTS.md`,
  and that path is worth considering. Deferred because (a) it would
  partly duplicate `CLAUDE.md` content, and (b) most cold-clone users
  land on `README.md` first, so the README breadcrumb resolves the
  immediate gap. If non-README-reading harnesses become a documented
  need, a separate issue can add `AGENTS.md` as a thin pointer to the
  same README section.

### Outside this issue's identity

- **Modifying `SKILL.md` frontmatter or its declared trigger
  signals.** The new README section points *at* `SKILL.md` as the
  canonical entry; it does not restate the trigger logic. The skill's
  description and frontmatter are unchanged.
- **Changes to the skill's internal references**
  (`syntax-reference.md`, `examples.md`, `best-practices.md`,
  `error-codes.md`, `comment-manipulation.md`, `table-formatting.md`).
  The README section names the `references/` directory but does not
  enumerate or modify its contents.
- **Marketplace install command changes.** The slash commands at
  `README.md` lines 46-49 are reframed in context, not rewritten.
  They remain verbatim in `## Tools`.
- **`docs/solutions/` learning entry.** This is a small documentation
  breadcrumb; the cleanup phase decides whether a learning is
  warranted. The plan does not pre-commit to one.

---

## Context & Research

### Verification of referenced surfaces

- **`README.md`** exists. The slash commands at lines 46-49 are inside
  the `## Tools` → `### Claude Code plugin` block:
  ```
  /plugin marketplace add quadralay/markdown-plus-plus
  /plugin install markdown-plus-plus@markdown-plus-plus
  ```
  Confirmed by reading the file. Insertion point for the new section:
  immediately before the existing `## Tools` heading (currently after
  the `## What's in this repo` bullet list).
- **`CLAUDE.md`** exists. The `## Overview` block is the first content
  block (lines 3-7). Insertion point for the one-line pointer: at the
  end of the `## Overview` block, separated by a blank line before
  the next `##` heading (`## Directory structure`).
- **`SKILL.md`** exists at
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`.
  Its YAML frontmatter declares the auto-activation trigger signals
  (the `description:` field enumerates `<!--style:-->`,
  `<!--multiline-->`, `<!--condition:-->`, `<!--include:-->`,
  `<!--marker:-->`, `<!--markers:-->`, `<!--#alias-->`,
  `$variable;`, and `mdpp-version:` in YAML frontmatter). The new
  README section paraphrases this list briefly for the Claude Code
  path and links to `SKILL.md` itself for the generic-harness path.
- **`references/`** directory exists at
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/`
  and contains: `best-practices.md`, `comment-manipulation.md`,
  `error-codes.md`, `examples.md`, `syntax-reference.md`,
  `table-formatting.md`. The new README section names this directory
  as a payload pointer (not an enumeration) to avoid drift if the
  reference set grows.
- **`#108` dependency.** Per the issue's *Ordering note*, this issue
  is sequenced behind #108 so the README and `CLAUDE.md` pointers
  reference a stable skill payload. The #108 work has merged
  (commits `4f9e66e`, `a3db708`, `eb6f4be`, `b776dc8`); the skill
  payload is now stable.

### Relevant repo conventions

- **`CLAUDE.md` § Conventions → File naming.** Kebab-case, with date
  prefix for time-bound content. This plan file follows the
  `YYYY-MM-DD-NNN-{slug}-plan.md` convention used by prior plans
  (e.g., `2026-05-22-002-unicode-alias-letter-class-plan.md`).
- **`CLAUDE.md` § Version Management.** Patch bump for documentation
  updates. The script updates `plugin.json` and `marketplace.json`
  in lockstep. The implementation commit `cf9717a` confirms both
  files moved from `1.7.0 → 1.7.1` together.
- **`CLAUDE.md` § Example locations.** The repo has explicit
  authoring locations (`examples/`,
  `plugins/.../references/examples.md`,
  `plugins/.../references/best-practices.md`). The new README section
  does not introduce a new example location; it points at the
  existing `references/` directory.

### Institutional learnings

- `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md`
  -- the skill's `description:` field carries the auto-activation
  trigger signals. The README's Claude Code path summarizes these
  signals without restating the full enumeration (which lives in
  `SKILL.md` frontmatter and would drift if duplicated). The link to
  the `## Tools` section keeps the install commands in one place.
- `docs/solutions/conventions/skill-reference-docs-capture-cleanup-knowledge-2026-05-11.md`
  -- the `references/` directory is the canonical skill payload. The
  README's generic-harness path names the directory (not individual
  files) so the breadcrumb stays correct as the reference set
  evolves.

---

## Key Technical Decisions

- **Section title: "For AI agents".** The issue offers two candidates
  ("For AI agents" or "Bootstrapping AI agents"). Plan chooses the
  shorter form -- it is scan-friendlier in the table of contents
  GitHub auto-generates, and it parallels the existing top-level
  headings (`## Quick look`, `## What's in this repo`, `## Tools`,
  `## Contributing`). The implementation in `cf9717a` uses this form.
- **Placement above `## Tools`, below `## What's in this repo`.** The
  issue requires placement above `## Tools` so the bootstrap guidance
  is discoverable before the marketplace install commands. The plan
  positions it after `## What's in this repo` so readers first see
  what the repo contains, then how an agent ingests it. This matches
  the typical README flow: orientation → bootstrap → install
  commands.
- **Two subsections, not one paragraph.** The issue calls out two
  distinct paths (Claude Code, generic harness). Plan uses two `###`
  subsections so a reader skimming for "what do I tell my agent"
  finds the right instruction without trial-and-error -- the issue's
  R2 success criterion.
- **Claude Code path links forward to `## Tools` rather than
  restating the commands.** The slash commands stay verbatim in
  `## Tools` (R5). The Claude Code subsection of **For AI agents**
  links to the `[Tools](#tools)` anchor and explains the post-install
  auto-activation behavior. This avoids duplication and keeps the
  install commands as a single source of truth.
- **Generic harness path uses bracketed Markdown links.** The
  `SKILL.md` and `references/` paths are formatted as clickable
  Markdown links per R3. Bare paths render as plain text on GitHub
  and obscure that they are clickable resources.
- **`CLAUDE.md` pointer is bold-prefixed for visual anchoring.** The
  pointer uses `**Agents bootstrapping from a cold clone:**` as the
  lead so it is visually distinct from surrounding overview prose --
  an agent skimming the file sees it without reading every line.
  Wording in implementation `cf9717a` matches.
- **Patch bump, not minor.** Documentation-only change with no
  behavior change. The `CLAUDE.md` § Version Management table assigns
  patch to "Bug fixes, documentation updates, minor improvements" --
  this is a documentation update. Implementation `cf9717a` confirms
  the patch bump.
- **`CHANGELOG.md` entry under Documentation.** The change is
  documentation-only; no Tooling or Spec change is involved. A single
  bullet under **Documentation** is sufficient.

---

## Open Questions

### Resolved during planning

- **Section title -- "For AI agents" vs. "Bootstrapping AI agents"?**
  Resolved: "For AI agents" (shorter, parallels existing top-level
  headings, scan-friendlier).
- **Where in the README does the new section land?** Resolved: after
  `## What's in this repo`, before `## Tools`. Matches the
  orientation → bootstrap → install flow and satisfies R1.
- **Where in `CLAUDE.md` does the pointer land?** Resolved: at the
  end of the existing `## Overview` block. The issue offers two
  candidates (Overview vs. Working with Markdown++ files). Plan
  chooses Overview because it is the first content block a
  cold-clone agent reads.
- **Does the generic-harness path enumerate the reference files or
  just point at the directory?** Resolved: name the directory only.
  Enumerating files (`syntax-reference.md`, `error-codes.md`,
  `examples.md`, `best-practices.md`, `comment-manipulation.md`,
  `table-formatting.md`) would drift as the set evolves. The README
  is a breadcrumb, not a tutorial.

### Deferred to implementation

- **Exact wording of the `CLAUDE.md` pointer.** The issue calls it
  "the implementor's call." Plan recommends a single sentence with a
  bold lead identifying the audience (cold-clone agents) and a
  clickable link to the README section. Final wording is in
  `cf9717a`.
- **Whether to mention specific trigger-signal examples in the
  Claude Code subsection.** The plan recommends naming at most three
  example signals (`<!--style:-->`, `$variable;`,
  `mdpp-version:` frontmatter) as a quick visual cue, with the
  authoritative enumeration left to `SKILL.md` frontmatter. The
  implementation chose this approach.

---

## Implementation Units

### U1. Add **For AI agents** section to `README.md`

**Goal:** New `## For AI agents` section placed above `## Tools`
documenting two ingestion paths.

**Steps:**

1. In `README.md`, locate the boundary between the `## What's in this
   repo` bullet list and the `## Tools` heading.
2. Insert a new section with:
   - `## For AI agents` heading.
   - One-paragraph lead: "If you're pointing an AI agent at this
     repo and want it to ingest Markdown++ for authoring or
     validation, follow the path that matches your agent's runtime."
   - `### If your agent runs in Claude Code` subsection: one
     paragraph pointing at the `## Tools` section's slash commands
     and naming three example auto-activation signals
     (`<!--...-->` directives, `$variable;` tokens, `mdpp-version:`
     frontmatter).
   - `### If your agent runs in another harness` subsection: one
     paragraph naming
     [`SKILL.md`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md)
     as the entry point and the sibling
     [`references/`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/)
     directory as the payload.
3. Leave `## Tools` and the slash commands verbatim.

**Acceptance:** R1, R2, R3, R5 satisfied. GitHub anchor for the new
section is `#for-ai-agents`. The `## Tools` anchor is unchanged.

### U2. Add one-line pointer to `CLAUDE.md`

**Goal:** Cold-clone agents reading `CLAUDE.md` first are routed to
the new README section before they hit the in-repo authoring
discipline content.

**Steps:**

1. In `CLAUDE.md`, locate the end of the `## Overview` block
   (currently line 7: "This is a specification and tooling repo -- no
   application code.").
2. Insert a blank line and then a single bolded sentence:
   `**Agents bootstrapping from a cold clone:** see the [For AI agents](README.md#for-ai-agents) section of `README.md` for ingestion paths into the Markdown++ skill. The remainder of this file documents in-repo authoring discipline, not first-time discovery.`
3. Confirm the section heading that follows (`## Directory structure`)
   is separated by a blank line.

**Acceptance:** R4 satisfied. The pointer is the third paragraph of
the file after the title and the existing two-paragraph overview, so
an agent reading the top of `CLAUDE.md` first sees the README
hand-off.

### U3. Version bump and `CHANGELOG.md` entry

**Goal:** Plugin version moves from `1.7.0` to `1.7.1`; changelog
records the documentation breadcrumb.

**Steps:**

1. Run `scripts/bump-version.sh patch`. Verify both `plugin.json` and
   `.claude-plugin/marketplace.json` show `1.7.1`.
2. Add a `1.7.1` entry to `CHANGELOG.md` under **Documentation**:
   "Add **For AI agents** section to `README.md` and a cold-clone
   pointer in `CLAUDE.md` documenting two skill-ingestion paths
   (Claude Code marketplace install vs. generic-harness skill
   loading)."

**Acceptance:** R-bump satisfied. The plugin manifests are in
lockstep at `1.7.1`. Per repo convention (#108 lineage), the
changelog entry is added in the same commit set as the documentation
change so the version increment ships with the user-visible reason.

---

## Verification

- **GitHub render:** Open the updated `README.md` on the branch in
  GitHub's web view. Confirm the **For AI agents** heading appears in
  the auto-generated table of contents, the two subsection anchors
  resolve, and the `SKILL.md` and `references/` links navigate
  correctly.
- **`CLAUDE.md` anchor:** Confirm the `[For AI agents](README.md#for-ai-agents)`
  link in `CLAUDE.md` resolves on GitHub.
- **`## Tools` integrity:** Confirm the two slash commands are
  verbatim and the existing feature table is unchanged.
- **No collateral changes:** `git diff` shows changes only in
  `README.md`, `CLAUDE.md`, `.claude-plugin/marketplace.json`,
  `plugins/markdown-plus-plus/.claude-plugin/plugin.json`, and
  `CHANGELOG.md`. No spec, skill, script, test, or example file is
  touched.
