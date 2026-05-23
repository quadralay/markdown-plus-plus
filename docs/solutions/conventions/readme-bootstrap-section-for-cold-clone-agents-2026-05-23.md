---
title: Surface cold-clone agent bootstrap paths in README, split by harness type
date: 2026-05-23
status: active
category: conventions
module: README.md, CLAUDE.md
problem_type: convention
component: documentation
severity: medium
applies_when:
  - A repository ships a Claude Code skill (or any AI agent payload) and a customer or partner asks how to point a generic agent harness at it
  - The existing README install instructions are framed for users already inside a specific harness (e.g., Claude Code slash commands) and do not address agents arriving from a cold clone
  - CLAUDE.md is scoped to in-repo authoring discipline and does not route an outside harness to the skill payload
  - The skill's entry file uses harness-specific framing (Claude Code SKILL.md frontmatter, XML-tagged sections) but the references/ payload is harness-agnostic
  - A single customer support ticket surfaces a "my agent can't ingest this" gap without an existing answer to point at
tags:
  - documentation-pattern
  - agent-onboarding
  - skill-discovery
  - readme-conventions
  - cold-clone-bootstrap
  - markdown-plus-plus
  - claude-code-plugin
---

# Surface cold-clone agent bootstrap paths in README, split by harness type

## Context

The `markdown-plus-plus` skill ships as a Claude Code marketplace
plugin. Up through plugin version 1.7.0, the only README guidance for
agents was two slash commands in a `## Tools` section:

```
/plugin marketplace add quadralay/markdown-plus-plus
/plugin install markdown-plus-plus@markdown-plus-plus
```

Those commands only help a user who is already inside a Claude Code
session. They presume the agent's runtime is Claude Code and that the
user knows what `/plugin marketplace add` does. The repo's `CLAUDE.md`
was scoped to in-repo authoring discipline -- how agents editing the
repo should behave -- and did not route an outside harness to the
skill payload.

Issue #110 surfaced the gap through a customer support exchange on
2026-05-22: a customer asked how to get their agent harness to ingest
the Markdown++ skill from a cold clone. There was no bootstrap
statement in `README.md` or `CLAUDE.md` to point them at. The customer
could not self-serve, and the support response had to be
hand-assembled rather than linked.

The fix was a documentation breadcrumb -- no spec change, no skill
change, no tooling change. Two surfaces, two short additions: a new
**For AI agents** section in `README.md` above `## Tools`, and a
one-line pointer at the top of `CLAUDE.md` handing off to it.

## Guidance

When a repository ships a Claude Code skill (or any AI agent payload)
and discovers via a support exchange that a generic agent harness
cannot self-orient from a cold clone, add the bootstrap breadcrumb at
the surface a cold-clone agent reads first -- the README -- and hand
off to it from the in-repo authoring entry point. Follow this shape:

**1. Add a top-level README section above the install instructions,
not below.** A cold-clone agent skimming the README for "how do I
ingest this" should hit the bootstrap section before the existing
install commands, because the install commands silently presume a
specific harness. Placing the new section above `## Tools` (or
whatever heading carries the install commands) puts harness-agnostic
ingestion guidance before harness-specific guidance. Name the section
explicitly for its audience -- **"For AI agents"** worked here; the
goal is that an agent or human pointing an agent at the repo finds the
section by skim, not by full-text search.

**2. Split the section by harness, not by content type.** A reader
skimming for "what do I tell my agent" wants a single path, not a
matrix. Two subsections work well in practice:

- **If your agent runs in Claude Code.** Point at the existing
  install commands by anchor link (e.g., `[Tools](#tools)`) -- do not
  rewrite or duplicate them. The slash commands stay verbatim in
  their original section; the new section only contextualizes them
  as the Claude-Code-specific path. State that the skill
  auto-activates on file content signals after install, so the reader
  knows no further wiring is needed.
- **If your agent runs in another harness.** Name the skill's entry
  file with an explicit clickable Markdown link to its repo path
  (e.g., `[`plugins/.../SKILL.md`](path)`). State that the YAML
  frontmatter declares trigger signals and that the sibling
  `references/` directory is the payload the agent should load. One
  short paragraph is sufficient -- this is a breadcrumb, not a
  tutorial.

**3. Point generic harnesses at the references/ directory, not only
the entry file.** A Claude Code SKILL.md is structured for Claude
Code's loader -- its YAML `description:` field is the auto-activation
trigger and its XML-tagged sections (`<objective>`, `<overview>`,
etc.) are skill conventions. A generic harness will ingest it as
plain Markdown and will miss the activation semantics. The durable,
harness-agnostic payload is the `references/` directory (syntax
reference, error codes, examples, best practices). The README
breadcrumb names SKILL.md as the entry point but also names
`references/` explicitly so a generic-harness operator knows where the
ingestible content actually lives. Document the framing limitation in
the plan or a follow-up so a future doc pass can refine it once the
breadcrumb has been exercised.

**4. Hand off to the README section from CLAUDE.md in one line.** An
agent that lands on `CLAUDE.md` first (because some harnesses
auto-read it) needs the hand-off to the README bootstrap section
early -- not buried inside the in-repo authoring discipline content.
Add a single bolded sentence near the top of `CLAUDE.md`'s overview
block: name the audience ("Agents bootstrapping from a cold clone"),
link to the new README section by anchor (e.g.,
`[For AI agents](README.md#for-ai-agents)`), and state that the
remainder of `CLAUDE.md` is scoped to in-repo authoring discipline.
No duplicated content. The README owns the bootstrap story; `CLAUDE.md`
owns the in-repo authoring story; the one-liner is the bridge.

**5. Do not create AGENTS.md prematurely.** Some harnesses
auto-read a top-level `AGENTS.md` file, and that path is worth
considering. But for a first-pass breadcrumb addition, creating
`AGENTS.md` partly duplicates `CLAUDE.md` content and adds a third
authoritative surface to keep in sync. Defer `AGENTS.md` to a separate
issue if and when a non-README-reading harness becomes a documented
need. The README + CLAUDE.md pair covers the dominant cold-clone
ingestion paths; adding `AGENTS.md` before the need is observed is
speculative scope.

**6. Bump the plugin patch version and add a CHANGELOG entry.**
Documentation-only breadcrumb additions are still user-visible
changes -- marketplace consumers see the version bump as the signal
something shipped. Run `scripts/bump-version.sh patch` to keep
`plugin.json` and `marketplace.json` synchronized and add a
CHANGELOG entry under the existing **Project** category (not
**Documentation**, which is not a category in this taxonomy --
`CHANGELOG.md` uses **Spec** / **Tooling** / **Project**, with repo
documentation living under Project by precedent).

## Why This Matters

A single customer support ticket of the shape "I cannot get my agent
to ingest this from a cold clone" is rarely a documentation-depth
problem. The skill has the depth -- the references/ directory carries
the full payload. The gap is on the bootstrap surface: the agent
arrives at the repo root, scans the README, and finds install commands
that presume a runtime it may not be using. The fix is small and
located -- a breadcrumb, not an expansion -- but the cost of *not*
having it is that every customer in a similar position has to
hand-assemble the same answer with support.

Splitting the bootstrap section by harness type avoids the trap of a
single ingestion path that quietly assumes Claude Code. The two
populations (Claude Code users and generic-harness users) get distinct,
direct hits without having to filter through guidance scoped to the
other. The Claude Code path stays a two-line install; the generic
harness path stays one paragraph naming the entry file and the
references directory. Neither population pays a tax for the other.

Pointing generic harnesses at `references/` -- rather than only at
`SKILL.md` -- compounds the limitation that `SKILL.md` is framed for
Claude Code's loader. A generic harness reading `SKILL.md` will not
auto-trigger on the `description:` field; the field is just a heading
to it. But the same harness can ingest the `references/` content as
plain Markdown and use it as authoring context. Naming both gives the
generic-harness operator a working ingest path even when the entry
file's frontmatter is opaque to their runtime.

The CLAUDE.md hand-off line is the cheapest possible insurance against
the "I read CLAUDE.md but not the README" failure mode. Some harnesses
prefer CLAUDE.md as their first-loaded context file; if the bootstrap
guidance lives only in the README, those harnesses miss it. A single
bolded sentence linking out to the README section catches both
populations without duplicating the bootstrap content in two places.

## When to Apply

- A customer support exchange (or any external signal -- a partner
  question, a public issue, a documented friction report) reveals
  that an agent harness cannot self-orient to the skill from a cold
  clone.
- The existing README guidance presumes a specific runtime (Claude
  Code, Cursor, another harness) and that presumption is not
  documented at the top of the relevant section.
- The skill's entry file uses harness-specific framing (YAML frontmatter
  loaded as an activation trigger, XML-tagged sections, etc.) and the
  README points at it as a generic entry point without acknowledging
  the framing.
- `CLAUDE.md` (or `AGENTS.md`, if present) is scoped to in-repo
  authoring discipline and would mislead a cold-clone agent that
  reads it first looking for "how do I ingest this."

Conversely, **do not** add a bootstrap section if the README already
splits ingestion by harness explicitly, or if the skill is so
Claude-Code-specific that a generic-harness path would be
semantically dishonest. The breadcrumb pays back when at least two
realistic ingestion paths exist; below that threshold it adds reading
weight without adding value.

## Examples

**README section structure (the shape that landed here):**

```markdown
## For AI agents

If you're pointing an AI agent at this repo and want it to ingest
Markdown++ for authoring or validation, follow the path that matches
your agent's runtime.

### If your agent runs in Claude Code

Install the marketplace plugin using the two slash commands in the
[Tools](#tools) section below. The `markdown-plus-plus` skill then
auto-activates on `.md` files containing Markdown++ signals (HTML
comment directives, `$variable;` tokens, `mdpp-version:` frontmatter);
no further wiring is required.

### If your agent runs in another harness

Point the agent at [`plugins/.../SKILL.md`](path) as the entry point.
Its YAML frontmatter declares the trigger signals the skill should
activate on, and the sibling [`references/`](path) directory contains
the syntax reference, error-code reference, examples, and
best-practices payload an agent should load to author or validate
Markdown++ documents.
```

Note the deliberate choices: the Claude Code subsection points at the
install commands by anchor link rather than restating them
(eliminates drift between the bootstrap section and the install
section); the generic harness subsection names *both* `SKILL.md` and
`references/` (covers the harness-framing gap); both subsections are
one short paragraph each (skim-readable, not tutorial-shaped).

**CLAUDE.md hand-off line (the shape that landed here):**

```markdown
**Agents bootstrapping from a cold clone:** see the
[For AI agents](README.md#for-ai-agents) section of `README.md` for
ingestion paths into the Markdown++ skill. The remainder of this file
documents in-repo authoring discipline, not first-time discovery.
```

The bolded audience label ("Agents bootstrapping from a cold clone")
makes the line easy to scan past for agents already past bootstrap.
The trailing clause ("The remainder of this file documents in-repo
authoring discipline, not first-time discovery") tells a cold-clone
agent that `CLAUDE.md` is not where they should be looking, which
prevents them from deeply ingesting authoring discipline content they
do not need yet.

**Reframed `## Tools` section:** The two install commands stay
verbatim. No content changes -- only the contextual framing shifts,
because the new section above now positions `## Tools` as the
Claude-Code-specific path. The anchor link from the new section
(`[Tools](#tools)`) is what makes the reframing readable; without
the link, the two sections would feel disconnected.

## Practical gotchas surfaced during this work

**1. Plan documents that cite README line numbers rot the moment a
new section is inserted.** The original plan cited "lines 46-49" for
the install commands. After the **For AI agents** section was
inserted above, those commands moved to lines 59-60. The plan reviewer
flagged this; the fix was to replace line-number references with
content-based references ("the install commands in the `## Tools`
section"). For any plan that touches README structure, prefer
content-based references over line numbers from the outset.

**2. `CHANGELOG.md` taxonomy is not what you might guess.** The
project's changelog uses **Spec** / **Tooling** / **Project**
categories. Documentation changes land under **Project** by precedent
(the 1.5.0 GLOSSARY entry set the pattern). The original plan called
the category "Documentation," which the feasibility reviewer flagged
as not matching the existing taxonomy. Check `CHANGELOG.md` before
naming a category in the plan.

**3. Version bump and CHANGELOG entry need to ship in the same
commit.** The implementation commit `cf9717a` bumped `plugin.json` and
`marketplace.json` to 1.7.1 but did not add the matching CHANGELOG
entry. The feasibility reviewer flagged this and the plan-review
revision added the entry. A bump-script that wrote a skeletal
CHANGELOG entry would prevent the mismatch; absent that, treat the
CHANGELOG edit as part of the bump checklist, not a separate step.

**4. `SKILL.md` is not a fully harness-agnostic entry point.** The
adversarial reviewer flagged that the generic-harness paragraph
implies `SKILL.md` is harness-agnostic, but its YAML frontmatter
(`description:` as the auto-activation trigger) and XML-tagged sections
are Claude Code skill conventions. A generic harness will read it as
plain Markdown and miss the activation semantics. The plan-review
revision added a *Known limitation: SKILL.md framing* note pointing at
`references/` as the harness-agnostic payload. The README itself was
not rewritten in that revision -- the breadcrumb is correct in spirit
(the file IS the entry point) and a wording refinement can ride a
future doc pass once the breadcrumb has been exercised against real
harnesses.

## Related

- [`README.md`](../../../README.md) -- the new "For AI agents" section
- [`CLAUDE.md`](../../../CLAUDE.md) -- the cold-clone hand-off line
- [`plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md) -- the skill entry file the bootstrap section points at
- [`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/) -- the harness-agnostic payload directory the bootstrap section names
- [`skill-activation-description-completeness-2026-05-09.md`](skill-activation-description-completeness-2026-05-09.md) -- sibling skill-discovery learning for Claude Code's auto-activation routing layer
- [`manual-verification-fixtures-for-unobservable-routing-2026-05-09.md`](manual-verification-fixtures-for-unobservable-routing-2026-05-09.md) -- regression methodology for skill-discovery properties that no automated test can fail
- GitHub issue #110 -- the bootstrap-section issue
- Plan document: [`docs/plans/2026-05-23-001-bootstrap-section-for-ai-agents-plan.md`](../../plans/2026-05-23-001-bootstrap-section-for-ai-agents-plan.md)
- Implementation commit: `cf9717a` (`docs: add bootstrap section for AI agents (closes #110)`)
- Plan commits: `af4b199` (initial), `eca9eea` (review revisions)
