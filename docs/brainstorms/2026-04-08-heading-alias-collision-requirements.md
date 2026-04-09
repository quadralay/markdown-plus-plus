---
date: 2026-04-08
topic: heading-alias-collision
---

# Heading Alias Collision Behavior

## Problem Frame

When two or more headings in a Markdown++ document produce the same auto-generated alias (e.g., two `## Setup` headings both generating `setup`), the spec does not define what happens. Authors of multi-section documents routinely reuse heading text (e.g., "Overview", "Setup", "Examples" repeated per chapter), so collisions are common in practice and must resolve deterministically.

## Requirements

- R1. When multiple headings in the assembled document produce the same auto-generated alias after the 6-step algorithm, a conformant processor MUST disambiguate by appending a counter suffix to subsequent occurrences.
- R2. The first heading in document order claims the bare alias. The second heading with the same alias receives `-2`, the third `-3`, and so on.
- R3. Counter suffixing applies only to auto-generated aliases. Custom aliases (`<!-- #name -->`) remain governed by MDPP008 (duplicate = error).
- R4. The spec MUST include at least one worked example showing the collision resolution with multiple duplicate headings.
- R5. The behavior MUST be consistent with the alias supplement semantics from issue #18 — a custom alias on a heading with a collision-suffixed auto-generated alias still supplements (both anchors are valid).

## Success Criteria

- The spec defines the resolution strategy unambiguously enough that two independent implementations produce the same aliases for the same document
- At least one worked example demonstrates the collision behavior
- The strategy is consistent with existing MDPP008 and #18 supplement semantics

## Scope Boundaries

- Custom alias collisions (user-defined `#alias` duplicates) are out of scope — already covered by MDPP008
- Changes to the ePublisher parser implementation are out of scope
- Cross-file alias collisions are out of scope for this change

## Key Decisions

- **Counter suffix starting at -2**: Matches the existing `add-aliases.py` tool implementation (`make_unique_alias` function, lines 84-92) and common industry practice (GitHub, GitLab). Starting at -2 (not -1) keeps the first occurrence clean and avoids ambiguity about whether `-1` means "first duplicate" or "only instance."
- **Silent resolution, not error**: Unlike custom alias duplicates (MDPP008 = error), auto-generated collisions are silently resolved because authors cannot always control heading text uniqueness across large assembled documents.

## Next Steps

→ Implement directly — scope is lightweight and all decisions are resolved.
