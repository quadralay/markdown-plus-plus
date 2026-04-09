---
date: 2026-04-08
topic: standalone-plus-plus-logo
---

# Standalone ++ Glyph Logo for Markdown++

## Problem Frame

Same as the Hashmark Monogram brief: Markdown++ has no visual identity, needs a distinctive icon for GitHub/web contexts. This is an alternative concept that bets entirely on the `++` operator as the brand mark — no M, no rectangle, no hash. Pure increment.

## Requirements

- R1. The logo is two geometric `+` signs arranged in a rising-step layout: the second `+` is elevated above and offset to the right of the first, creating a visual rhythm of increment/progression.
- R2. The mark must work as a standalone icon — recognizable without an accompanying wordmark. Legible at 16x16 (favicon), 32x32 (badge), and 128x128+ (documentation header).
- R3. Monochrome must work as a baseline. Color treatment is open for designer exploration.
- R4. The visual quality should be geometric precision — clean, mathematical strokes. Conveys a specification standard, not a casual tool.
- R5. The mark should feel like it belongs in the Markdown ecosystem without literally referencing Markdown's existing iconography. It communicates "increment what exists" rather than "replace with something new."
- R6. The mark must work on both light and dark backgrounds without modification (or with a simple inversion).
- R7. The rising-step offset must be pronounced enough to read as intentional at small sizes, not as a rendering artifact or misalignment.

## Success Criteria

- A developer seeing the mark reads "++" (increment/extension) not "two random plus signs"
- The rising-step layout is perceptible at 32x32 and reads as deliberate progression
- The mark is distinctive enough to not be confused with a generic increment operator, math symbol, or medical cross
- Works in monochrome, dark mode, and light mode

## Scope Boundaries

- **In scope:** Icon mark design, basic color exploration, size/context variants
- **Out of scope:** Full brand identity system, wordmark design, marketing materials, animation

## Key Decisions

- **Pure ++ with no Markdown reference:** This is the bold bet — the mark stands on the strength of the increment metaphor alone. If it needs a wordmark to make sense, that's acceptable but not the goal.
- **Rising-step, not side-by-side or overlapping:** The elevation conveys progression, not just duplication. This is the concept's visual hook and differentiator.
- **Geometric precision, not typographic warmth:** Squared or clean terminals, consistent stroke weight, mathematical proportions. This is a spec standard, not a fun tool.
- **Same constraints as Hashmark brief:** Standalone icon, monochrome baseline, GitHub/web primary, dark+light mode.

## Comparison with Hashmark Monogram

| Dimension | Hashmark Monogram | Standalone ++ |
|-----------|------------------|---------------|
| Concept | Dual reading (# and ++) in one symbol | Pure ++ as the entire mark |
| Markdown connection | # is Markdown's heading character | Indirect — ++ means "extend what exists" |
| Memorability | Hidden-element discovery (FedEx arrow effect) | Bold simplicity, extreme recognition at tiny sizes |
| Risk | May read as "just a hash" | May read as "just two plus signs" |
| Distinctiveness | High — no other format uses # as a logo | Lower — ++ is generic without context |
| Execution difficulty | Medium-high (geometric dual reading) | Low-medium (layout and proportions) |

## Outstanding Questions

### Deferred to Planning

- [Affects R1][Needs research] What exact elevation angle and offset ratio make the rising step read as "progression" rather than "disordered"? This is a proportions question best answered by design iteration.
- [Affects R7][Needs research] At 16x16, can a rising step be perceived, or does it collapse into two overlapping blobs? May need a simplified favicon variant.
- [Affects R4][Technical] Same file format question as Hashmark brief: SVG, PNG at key sizes, ICO. Where in the repo?

## Next Steps

→ `/ce:plan` for structured implementation planning — or hand this brief to a graphic designer directly.
