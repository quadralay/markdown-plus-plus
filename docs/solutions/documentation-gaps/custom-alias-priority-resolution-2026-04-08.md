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
last_updated: 2026-04-08
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

- A custom alias `<!-- #setup -->` on a heading and an auto-generated alias `setup` from a different `## Setup` heading would both produce the same identifier string.
- Different processors could resolve a link to `#setup` differently -- some might resolve to the auto-generated alias target (document order), others might give priority to the custom alias target.
- Cross-references using `#setup` would be non-deterministic across implementations.
- The existing duplicate alias resolution mentioned custom aliases but did not define the resolution priority when an auto-generated alias and a custom alias share the same identifier string.

## What Didn't Work

**Suffix/displacement semantics (shared namespace model).** The initial implementation borrowed the collision-resolution pattern from duplicate auto-generated aliases (#53) and applied it to the custom-vs-auto case. Under this model, custom and auto-generated aliases occupied a single shared namespace. When a custom alias `<!-- #setup -->` existed and another heading auto-generated the slug `setup`, the auto-generated alias would be displaced and given a counter suffix (e.g., `setup` becomes `setup-1`).

This approach was fundamentally wrong for three reasons:

1. **It mutated the auto-generated alias value.** Renaming `setup` to `setup-1` would break any existing links that correctly pointed at the heading via its auto-generated slug. The displacement imposed a cost on authors who had done nothing wrong.
2. **It conflated two different systems.** Custom aliases are intentional, author-specified identifiers. Auto-generated aliases are incidental byproducts of heading text slugification. Treating them as peers in a shared namespace erased this semantic distinction.
3. **It resolved the collision at the wrong layer.** The real conflict is not at alias generation time (both aliases can coexist without contradiction) but at link resolution time (a `#setup` link must choose one target). Suffix/displacement "solved" a problem at the wrong layer.

The alternative of "document order wins" was also considered and rejected. Document order is appropriate for auto-vs-auto collisions (where both aliases are equally fragile), but inappropriate for custom-vs-auto overlap because the custom alias is an intentional authorial choice that should always take resolution priority over an incidental heading slug.

## Solution

Added a normative **Custom Alias Priority** subsection to `spec/element-interactions.md`, placed after the existing "Interaction with Custom Aliases" subsection within "Duplicate Alias Resolution."

**Core normative rule:**

Custom aliases and auto-generated heading aliases occupy separate namespaces. When both produce the same identifier string, both exist independently -- the auto-generated alias is NOT displaced or suffixed. At link resolution time, the custom alias takes priority: a link to `#setup` resolves to the custom alias target, not the auto-generated alias target.

**Resolution order requirement:**

A conformant processor MUST check custom aliases before auto-generated heading aliases when resolving a link target. This ensures custom aliases always win resolution priority regardless of document order. Auto-generated aliases are still generated normally for all headings -- the processor does not modify auto-generation based on custom alias values.

**Silent resolution:** Conformant processors MUST NOT emit a diagnostic when a custom alias and an auto-generated alias share the same identifier string. The custom alias is an intentional authorial choice that wins at resolution time.

**Worked example** -- custom alias overlapping with auto-generated alias:

| Heading | Anchors |
|---------|---------|
| `## Installation` (with `<!-- #setup -->`) | `installation` (auto-generated), `setup` (custom alias) |
| `## Setup` | `setup` (auto-generated, de-prioritized by custom alias) |

**Composition with duplicate resolution** -- both overlap types in one document:

| Heading | Anchors |
|---------|---------|
| `## Installation` (with `<!-- #setup -->`) | `installation` (auto-generated), `setup` (custom alias) |
| `## Setup` (first) | `setup` (auto-generated, de-prioritized by custom alias) |
| `## Setup` (second) | `setup-2` (suffixed -- duplicate auto-generated resolution) |

**Supporting cross-references updated in:** syntax-reference.md (collision summary paragraph), error-codes.md (MDPP008 scope note).

## Why This Works

The priority rule is the natural consequence of the design intent behind custom aliases:

1. **Intentional vs. incidental** -- Custom aliases are deliberately assigned by the author to be stable, permanent anchors. Auto-generated aliases are derived from heading text and change when the heading text changes. The intentional assignment should always win at resolution time.
2. **Separate namespaces preserve both aliases** -- Custom aliases and auto-generated aliases coexist in separate namespaces. Neither displaces the other. The auto-generated alias still exists and is still valid -- it is simply de-prioritized when a custom alias shares the same identifier.
3. **Composable with existing rules** -- Duplicate auto-generated alias resolution (#53) operates entirely within the auto-generated namespace and is unaffected by custom alias values. Custom alias priority is a separate concern applied only at link resolution time.
4. **Deterministic** -- Checking custom aliases first during resolution ensures every conformant processor produces the same result regardless of document order.

## Prevention

- **Collision matrix completeness:** When defining collision behavior for identifiers, enumerate all pairwise combinations (auto-auto, custom-custom, custom-auto) and specify each. Issue #53 covered auto-auto, MDPP008 covers custom-custom, and this change covers custom-auto.
- **Distinguish namespaces before designing collision rules.** When two features can produce the same identifier, ask: "Are these the same namespace or different namespaces?" If they have different provenance, semantics, or levels of author intent, they are likely separate namespaces and should not share displacement/suffix mechanics.
- **Locate the collision at the right layer.** Ask: "Where does the ambiguity actually matter?" If two aliases can coexist without contradiction until something tries to choose between them, the collision belongs at the resolution layer, not at the generation layer.
- **Apply the principle of least mutation.** A spec rule that modifies an existing value (renaming `setup` to `setup-1`) has a higher burden of proof than one that leaves all values intact and applies priority at lookup time.
- **Test the analogy before reusing a pattern.** The suffix/displacement approach was borrowed from duplicate auto-generated alias handling (#53). That pattern works when both colliding aliases have the same provenance. It does not transfer to cross-provenance collisions. Before reusing a collision-resolution pattern, verify that the new context shares the same structural properties.
- **Use "what breaks?" as a design smell test.** The suffix/displacement approach would have broken existing links to the auto-generated alias. Any spec rule that silently invalidates previously-correct links should be treated as a strong signal that the design is wrong.

## Related Issues

- [#55](https://github.com/quadralay/markdown-plus-plus/issues/55) -- This issue (custom alias priority)
- [#53](https://github.com/quadralay/markdown-plus-plus/issues/53) -- Heading alias collision (auto-generated vs. auto-generated)
- [#18](https://github.com/quadralay/markdown-plus-plus/issues/18) -- Alias supplement vs. replace semantics
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Element interactions
- `docs/solutions/documentation-gaps/heading-alias-collision-resolution-2026-04-08.md` -- Auto-generated collision resolution (this doc extends that work)
