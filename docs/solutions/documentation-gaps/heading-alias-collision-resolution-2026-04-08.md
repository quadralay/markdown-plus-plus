---
title: "Heading alias collision -- duplicate auto-generated aliases had no specified resolution strategy"
date: 2026-04-08
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - "No specification for what happens when two or more headings produce the same auto-generated alias"
  - "Duplicate heading text (e.g., multiple '## Setup' sections) created ambiguous cross-reference targets"
  - "Implementors had to guess whether to error, silently overwrite, or disambiguate"
  - "MDPP008 error code scope was unclear for auto-generated vs. custom alias duplicates"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - heading-alias
  - duplicate-resolution
  - counter-suffix
  - specification-gap
  - element-interactions
  - mdpp008
---

# Heading alias collision -- duplicate auto-generated aliases had no specified resolution strategy

## Problem

The Markdown++ specification defined a 6-step heading alias auto-generation algorithm in `spec/element-interactions.md` but never specified what should happen when two or more headings produced the same alias. This is common in real documents (e.g., multiple `## Setup` sections under different parent headings), meaning different processors could resolve the collision differently and break cross-reference interoperability.

## Symptoms

- Two or more headings with identical text (e.g., `## Setup` appearing three times) would produce the same auto-generated alias `setup`, creating ambiguous anchor targets.
- Cross-references like `[see setup](#setup)` would be non-deterministic -- a processor might link to the first, last, or any matching heading.
- Different implementations could resolve the collision differently, so a document authored against one processor would break when processed by another.
- MDPP008 scope was unclear -- did it apply to auto-generated alias collisions or only to custom alias duplicates?

## What Didn't Work

This was a clean spec-writing exercise. No failed debugging approaches were needed. The `add-aliases.py` script already had a working `make_unique_alias` function implementing counter-suffix disambiguation, but this behavior was implementation-only with no normative spec text.

The incremental spec approach (syntax reference, then attachment rule, then processing model, then element interactions) left collision behavior in a gap -- each document owned a different concern and none owned "what if two aliases collide?"

One design alternative was explicitly considered and rejected: starting the counter at `-1` instead of `-2`. Starting at `-2` was chosen because it matches the convention used by GitHub, GitLab, and the existing `add-aliases.py` implementation.

## Solution

Added a normative **Duplicate Alias Resolution** subsection to `spec/element-interactions.md`, placed after the existing "Scope" subsection within "Heading Alias Auto-Generation." Four commits across 8 files.

**Core normative rules:**

1. The **first** heading in document order claims the bare alias (no suffix).
2. The **second** heading with the same alias receives the suffix `-2`.
3. The **third** receives `-3`, and so on for each subsequent duplicate.

**Global uniqueness requirement** (added during review as a P1 fix):

> The resulting suffixed alias MUST be unique across all aliases -- both auto-generated and custom -- already assigned in the document. If a candidate suffix collides with an existing alias, the processor MUST continue incrementing the counter until a unique alias is produced.

This handles edge cases where a suffixed auto-generated alias (e.g., `setup-2`) collides with a pre-existing custom alias `<!-- #setup-2 -->`.

**Silent resolution rule:** Conformant processors MUST NOT emit a diagnostic for auto-generated alias collisions. Unlike custom alias duplicates (which trigger MDPP008), auto-generated collisions are expected behavior.

**Worked example** -- three `## Setup` headings:

| Heading | Auto-Generated Alias |
|---------|---------------------|
| `# Installation Guide` | `installation-guide` |
| `## Setup` (first) | `setup` |
| `## Configuration` | `configuration` |
| `## Setup` (second) | `setup-2` |
| `## Setup` (third) | `setup-3` |

**Custom alias interaction** -- a collision-suffixed heading with a custom alias retains both anchors:

```markdown
<!-- #db-setup -->
## Setup
```

If this is the second `## Setup`, the heading has anchors `db-setup` (custom) and `setup-2` (suffixed auto-generated), consistent with alias supplement semantics from issue #18.

**Implementation match** (`add-aliases.py` lines 84-92):

```python
def make_unique_alias(base: str, existing: set[str]) -> str:
    """Generate a unique alias by appending a number if needed."""
    if base not in existing:
        return base

    counter = 2
    while f"{base}-{counter}" in existing:
        counter += 1
    return f"{base}-{counter}"
```

**Supporting cross-references** updated in: SKILL.md (collision summary), error-codes.md (MDPP008 scope note), syntax-reference.md (cross-reference paragraph). Version bumped 1.1.6 to 1.1.7.

## Why This Works

The spec gap existed because the original heading alias auto-generation algorithm (added for issue #18) defined single-heading behavior but omitted the document-wide uniqueness constraint. The counter-suffix strategy was chosen because:

1. **Industry convention** -- GitHub, GitLab, and other Markdown processors use the same `-2`, `-3` pattern.
2. **Deterministic** -- document order plus sequential counter ensures every processor produces identical aliases.
3. **Non-breaking** -- the first occurrence keeps the bare alias, so existing cross-references continue to work.
4. **Consistent with existing tooling** -- the `add-aliases.py` script already implemented this strategy, so the spec codifies existing practice.
5. **Global uniqueness check** -- the `while` loop handles edge cases where a suffixed alias collides with a custom alias.

## Prevention

- **Spec completeness checklist:** When defining single-element behavior (e.g., alias generation for one heading), always ask: "What happens when multiple elements produce the same output?" Generation and deduplication are inseparable concerns -- document both in the same section.
- **Implementation-first validation:** When tooling implements behavior not covered by the spec, that signals a spec gap. Periodically audit `add-aliases.py` and other tooling behavior against spec coverage.
- **Multi-stage review pipeline:** This issue's brainstorm-to-plan-to-spec-to-review workflow caught the global uniqueness requirement during review (a P1 fix). Structured review phases surface edge cases that initial spec writing misses.
- **Distinguish error vs. silent resolution:** When adding collision-like behavior, explicitly document whether the condition is an error (like MDPP008 for custom duplicates) or expected behavior (like auto-generated collisions). State the contrast in both places.

## Related Issues

- [#53](https://github.com/quadralay/markdown-plus-plus/issues/53) -- This issue (heading alias collision behavior)
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) -- Element interactions (parent work that created `element-interactions.md`)
- [#18](https://github.com/quadralay/markdown-plus-plus/issues/18) -- Alias supplement vs. replace semantics (dependency)
- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) -- Error code reference (MDPP008 updated)
- [#22](https://github.com/quadralay/markdown-plus-plus/issues/22) -- Cross-file link resolution (related deterministic resolution pattern)
- `docs/solutions/documentation-gaps/element-interactions-spec-gap-2026-04-08.md` -- Broader element-interactions creation (high overlap; this doc extends that work)
