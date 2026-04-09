---
date: 2026-04-08
topic: custom-alias-priority
---

# Custom Alias Priority over Auto-Generated Heading Aliases

## Problem Frame

When a custom Markdown++ alias (`<!-- #setup -->`) on one element collides with an auto-generated heading alias (`setup` from `## Setup`) on a different element, the spec does not define which alias wins. Issue #53 resolved auto-generated vs. auto-generated collisions with counter suffixing, but the custom vs. auto-generated case remains unspecified.

## Requirements

- R1. When a custom alias and an auto-generated heading alias produce the same identifier, the custom alias MUST take priority. The auto-generated alias is displaced.
- R2. The displaced auto-generated alias MUST receive a counter suffix (`-2`, `-3`, etc.) using the same algorithm as auto-generated duplicate resolution. The alias is never silently dropped.
- R3. The resolution MUST be silent -- a conformant processor MUST NOT emit a diagnostic for this collision. The custom alias is an intentional authorial choice; the auto-generated one adjusts around it.
- R4. The spec MUST include at least one worked example showing a custom alias colliding with an auto-generated alias on a different element, and the resulting anchors.
- R5. The behavior MUST be consistent with alias supplement semantics (#18) -- when there is no collision, custom and auto-generated aliases coexist; when there is a collision across elements, the custom alias claims the name and the auto-generated alias is suffixed.

## Success Criteria

- The spec defines the priority rule unambiguously enough that two independent implementations resolve the collision identically
- At least one worked example demonstrates the cross-element collision
- Consistent with existing MDPP008 scope, #53 counter-suffix strategy, and #18 supplement semantics

## Scope Boundaries

- Auto-generated vs. auto-generated collisions are out of scope (covered by #53)
- Custom vs. custom alias collisions are out of scope (covered by MDPP008)
- Changes to the ePublisher parser implementation are out of scope

## Key Decisions

- **Custom aliases always win**: Custom aliases are intentionally assigned by the author as stable, permanent anchors. Auto-generated aliases are derived from heading text and are inherently fragile. The intentional assignment takes priority.
- **Displaced alias is suffixed, not dropped**: Dropping the auto-generated alias entirely would leave the heading without an auto-generated anchor, breaking cross-references. Suffixing preserves addressability while respecting the custom alias claim.
- **Silent resolution**: Consistent with auto-auto collision handling. The author chose the custom alias name deliberately; the processor adjusts without complaint.

## Next Steps

-> Implement directly -- scope is lightweight and all decisions are resolved.
