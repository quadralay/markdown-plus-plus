---
date: 2026-04-08
topic: hashmark-monogram-logo
---

# Hashmark Monogram Logo for Markdown++

## Problem Frame

Markdown++ has no visual identity. The repo contains zero visual assets — no logo, favicon, or brand mark. The format needs a distinctive, recognizable icon that communicates its relationship to Markdown and its "additive extension" philosophy. The primary usage context is GitHub, web documentation, npm/marketplace listings, and shields.io badges.

## Requirements

- R1. The logo is a geometric monogram where two `+` signs, offset and overlapping, form a shape that also reads as a `#` (hash/octothorpe). The `++` reading should be primary; the `#` is a secondary discovery.
- R2. The mark must work as a standalone icon — recognizable without an accompanying wordmark. It must be legible at 16x16 (favicon), 32x32 (badge), and 128x128+ (documentation header).
- R3. The mark must work in monochrome as a baseline. Color treatment is open for the designer to explore, but single-color on transparent background must be a supported variant.
- R4. The mark must be clearly distinct from Slack's former octothorpe logo. The `++` duality, geometric style, stroke proportions, or container treatment must make the difference obvious at a glance.
- R5. The mark should feel like it belongs in the Markdown ecosystem — it extends Markdown's visual language rather than departing from it. It should not look like a competing format.
- R6. The mark must work on both light and dark backgrounds without modification (or with a simple inversion).

## Success Criteria

- A developer seeing the mark for the first time reads "++" before "#"
- Someone familiar with Markdown connects it to the Markdown ecosystem within seconds
- The mark is distinct from Slack's old # at a glance (different proportions, weight, or framing)
- The mark is legible and recognizable at favicon size (16x16)
- The mark works in monochrome, dark mode, and light mode

## Scope Boundaries

- **In scope:** Icon mark design, basic color exploration, size/context variants (favicon, badge, header)
- **Out of scope:** Full brand identity system, typography/font selection for wordmark, marketing materials, animation, merchandise

## Key Decisions

- **++ reading is primary, # is secondary:** The mark leads with "two overlapping plus signs" and rewards closer inspection with the hash discovery. This inverts the naive approach (a # that secretly contains ++) to avoid the Slack association and to lead with the format's core message (additive extension).
- **Standalone icon, not paired lockup:** The mark must work solo — favicon, avatar, badge icon. A wordmark companion is optional but not the primary deliverable.
- **Color left open for design exploration:** Only constraint is monochrome must work as a baseline. Designer may propose single-color, two-tone (emphasizing ++ duality), or other treatments.
- **GitHub & web is the primary context:** Digital-first, small-to-medium sizes. Print and enterprise decks are secondary.

## Outstanding Questions

### Deferred to Planning

- [Affects R1][Needs research] What stroke weight ratio and intersection treatment make the ++ reading primary while preserving the # discovery? This is the core geometric challenge.
- [Affects R4][Needs research] Should the mark use a container shape (rounded rectangle, circle) or stand alone as pure geometry? A container differentiates from Slack's containerless # but adds complexity at small sizes.
- [Affects R3][Technical] What file formats are needed? SVG (scalable), PNG (raster at key sizes), ICO (favicon)? Where do they live in the repo?

## Next Steps

→ `/ce:plan` for structured implementation planning — or hand this brief to a graphic designer directly.
