---
title: "Custom alias priority -- custom vs. auto-generated alias collisions had no specified resolution"
date: 2026-04-08
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - "No specification for what happens when a custom alias collides with an auto-generated heading alias on a different element"
  - "Custom alias <!-- #setup --> on one heading and auto-generated slug setup from ## Setup on another heading created ambiguous anchors"
  - "Implementors had to guess whether custom or auto-generated alias wins the collision"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - heading-alias
  - custom-alias
  - collision-priority
  - specification-gap
  - element-interactions
---

# Custom alias priority -- custom vs. auto-generated alias collisions had no specified resolution

## Problem

The Markdown++ specification defined collision behavior for auto-generated heading aliases that collide with each other (issue #53), but never specified what happens when a custom alias (`<!-- #setup -->`) on one element produces the same identifier as an auto-generated heading alias (`setup` from `## Setup`) on a different element. This left a gap between the custom alias supplement semantics (#18) and the duplicate auto-generated resolution (#53).

## Symptoms

- A custom alias `<!-- #setup -->` on a heading and an auto-generated alias `setup` from a different `## Setup` heading would both claim the same identifier.
- Different processors could resolve the collision differently -- some might let the auto-generated alias win (document order), others might give priority to the custom alias.
- Cross-references using `#setup` would be non-deterministic across implementations.
- The existing global uniqueness check in duplicate alias resolution mentioned custom aliases but did not define the priority when a bare (unsuffixed) auto-generated alias collides with a custom alias.

## What Didn't Work

This was a spec-writing exercise extending the collision framework from #53. No failed debugging approaches were needed. The gap existed because #53 focused on auto-vs-auto collisions and deferred the custom-vs-auto case.

The alternative of "document order wins" was considered and rejected. Document order is appropriate for auto-vs-auto collisions (where both aliases are equally fragile), but inappropriate for custom-vs-auto collisions because the custom alias is an intentional authorial choice that should not be displaced by an incidental heading slug.

## Solution

Added a normative **Custom Alias Priority** subsection to `spec/element-interactions.md`, placed after the existing "Interaction with Custom Aliases" subsection within "Duplicate Alias Resolution."

**Core normative rule:**

When a custom alias and an auto-generated heading alias produce the same identifier, the custom alias takes priority. The auto-generated alias is displaced and receives a counter suffix using the same algorithm as duplicate auto-generated alias resolution.

**Processing order requirement:**

A conformant processor MUST resolve custom aliases before auto-generated heading aliases during Phase 2. This ensures custom aliases claim their identifiers first, regardless of document order.

**Silent resolution:** Conformant processors MUST NOT emit a diagnostic for this collision. The custom alias is an intentional authorial choice; the auto-generated one adjusts around it.

**Worked example** -- custom alias colliding with auto-generated alias:

| Heading | Anchors |
|---------|---------|
| `## Installation` (with `<!-- #setup -->`) | `installation` (auto-generated), `setup` (custom alias) |
| `## Setup` | `setup-2` (suffixed auto-generated) |

**Composition with duplicate resolution** -- both collision types in one document:

| Heading | Anchors |
|---------|---------|
| `## Installation` (with `<!-- #setup -->`) | `installation` (auto-generated), `setup` (custom alias) |
| `## Setup` (first) | `setup-2` (suffixed -- displaced by custom alias) |
| `## Setup` (second) | `setup-3` (suffixed -- next available counter) |

**Supporting cross-references updated in:** syntax-reference.md (collision summary paragraph), error-codes.md (MDPP008 scope note).

## Why This Works

The priority rule is the natural consequence of the design intent behind custom aliases:

1. **Intentional vs. incidental** -- Custom aliases are deliberately assigned by the author to be stable, permanent anchors. Auto-generated aliases are derived from heading text and change when the heading text changes. The intentional assignment should always win.
2. **Consistent with supplement semantics** -- When there is no collision, custom and auto-generated aliases coexist (supplement). When there is a collision, the custom alias claims the name and the auto-generated alias adjusts. The supplement model is preserved -- the heading still has both an auto-generated alias (suffixed) and the custom alias.
3. **Composable with existing rules** -- The same counter-suffix algorithm from #53 handles the displaced auto-generated alias. No new resolution mechanism is needed.
4. **Deterministic** -- Processing custom aliases first ensures every conformant processor produces the same result regardless of document order.

## Prevention

- **Collision matrix completeness:** When defining collision behavior for identifiers, enumerate all pairwise combinations (auto-auto, custom-custom, custom-auto) and specify each. Issue #53 covered auto-auto, MDPP008 covers custom-custom, and this change covers custom-auto.
- **Priority principle documentation:** When two identifier sources can collide, always document which source has priority and why. The principle "intentional assignments beat derived identifiers" applies broadly.

## Related Issues

- [#55](https://github.com/quadralay/markdown-plus-plus/issues/55) -- This issue (custom alias priority)
- [#53](https://github.com/quadralay/markdown-plus-plus/issues/53) -- Heading alias collision (auto-generated vs. auto-generated)
- [#18](https://github.com/quadralay/markdown-plus-plus/issues/18) -- Alias supplement vs. replace semantics
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Element interactions
- `docs/solutions/documentation-gaps/heading-alias-collision-resolution-2026-04-08.md` -- Auto-generated collision resolution (this doc extends that work)
