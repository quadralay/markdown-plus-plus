---
date: 2026-03-30
topic: interchangeability-messaging
---

# Document Markdown and Markdown++ Interchangeability

## Problem Frame

New users and evaluators encounter Markdown++ and may perceive it as a proprietary format that requires specialized tooling. The existing documentation emphasizes backward compatibility defensively -- "extensions are invisible," "doesn't break in standard renderers" -- but does not affirmatively communicate that Markdown and Markdown++ are interchangeable across the entire tool spectrum. This framing gap creates an unnecessary adoption barrier: users may not realize they can start with standard Markdown tools and incrementally adopt Markdown++ extensions where they add value.

The concept of interchangeability -- that Markdown++ files *are* Markdown files, and the ecosystem is a spectrum from Markdown-only tools to Markdown++-aware tools -- deserves explicit naming and consistent reinforcement across the documentation.

## Requirements

- R1. **Name the concept explicitly.** Introduce "interchangeability" (or equivalent clear term) as a named principle in the whitepaper, distinct from the existing "backward compatibility" framing. Backward compatibility says "it doesn't break." Interchangeability says "it actively works everywhere, and you choose how much power you want."

- R2. **Communicate the tool spectrum.** Document that the tool ecosystem is a spectrum: a Markdown-only tool ignores extensions (they are HTML comments), a Markdown++-aware tool interprets them for richer output, and both are valid workflows. This reframes the relationship from binary (supports/doesn't support) to a continuum.

- R3. **Reinforce in the whitepaper introduction.** The opening sections (the dilemma framing and "What is Markdown++?") should introduce interchangeability early so readers understand it as a foundational property, not an afterthought.

- R4. **Strengthen the "Full CommonMark backward compatibility" benefit.** Section 4.1 already covers tool compatibility but frames it as "works cleanly in" various tools. Strengthen this to also communicate that authors can use standard Markdown tools for their full workflow and selectively add Markdown++ extensions.

- R5. **Reinforce in migration paths.** Each migration section should make clear that teams migrating to Markdown++ are not leaving the Markdown ecosystem -- they are gaining optional power on top of it. The Word migration section (updated in PR #4) already touches this; other migration paths should be consistent.

- R6. **Address in the syntax reference or best practices.** The plugin's reference materials should include brief guidance on interchangeability for authors using the Claude Code skill -- specifically that they can write plain Markdown and add Markdown++ syntax incrementally.

## Success Criteria

- A reader encountering Markdown++ for the first time understands within the first few paragraphs that their existing Markdown tools and skills transfer fully.
- The documentation consistently communicates that Markdown++ is additive, not alternative -- you are still writing Markdown.
- The tool spectrum concept (Markdown-only to Markdown++-aware) appears explicitly at least once in the whitepaper and once in the reference materials.
- No existing messaging about CommonMark compatibility or invisible extensions is weakened or contradicted.

## Scope Boundaries

- **In scope:** Whitepaper text, syntax reference, best practices -- all existing documentation files that discuss the format's relationship to standard Markdown.
- **In scope:** README.md if minor reinforcement is warranted (it already communicates this reasonably well).
- **Out of scope:** Creating new standalone documents (e.g., a separate "interchangeability guide"). The concept should be woven into existing materials.
- **Out of scope:** Changes to the examples/ directory. The examples demonstrate features, not messaging.
- **Out of scope:** Changes to the SKILL.md file structure or plugin metadata.

## Key Decisions

- **Weave, don't create:** Interchangeability messaging should be integrated into existing sections rather than creating new standalone documents. This avoids redundancy and ensures readers encounter the concept naturally.
- **Affirmative framing over defensive:** Shift from "doesn't break in standard tools" to "works across the full spectrum of Markdown tools." Both are true; the affirmative framing is more compelling for adoption.
- **Incremental adoption is the key message:** The most important thing to communicate is that authors can start with plain Markdown and add Markdown++ syntax only where they need it. This lowers the perceived adoption cost.

## Outstanding Questions

### Deferred to Planning

- [Affects R1][Needs research] What specific term best captures this concept? "Interchangeability" is the working term from the issue, but "Markdown compatibility spectrum" or "incremental extension" might land better in specific contexts. The planner should evaluate during editing.
- [Affects R3][Technical] Identify the exact insertion points in the whitepaper introduction where interchangeability messaging fits naturally without disrupting the existing narrative flow.
- [Affects R6][Needs research] Determine which reference file (syntax-reference.md or best-practices.md) is the better home for interchangeability guidance for plugin users.

## Next Steps

All outstanding questions are deferred to planning -- no blocking questions remain.

-> `/ce:plan` for structured implementation planning
