---
date: 2026-04-08
topic: graceful-degradation
---

# Graceful Degradation Documentation

## Problem Frame

Markdown++ positions CommonMark backward compatibility as a core value proposition. The whitepaper claims files "render cleanly in GitHub, VS Code, MkDocs, and any other Markdown viewer." However, degradation is not uniform across extensions — some are truly invisible, others leave visible artifacts, and some lose content entirely. Authors, reviewers, and teams evaluating Markdown++ have no systematic reference for what each extension actually looks like in a plain CommonMark renderer.

## Requirements

- R1. Create a spec appendix (`spec/graceful-degradation.md`) containing a degradation matrix that documents each extension's syntax, what happens in a standard CommonMark renderer, and a graceful/partial/no rating
- R2. The matrix must cover all eleven extension categories: custom styles, custom aliases, markers, conditions, file includes, variables, multiline tables, combined commands, inline styles, content islands, and link references
- R3. Categorize extensions into three tiers: **Fully graceful** (invisible or equivalent rendering), **Partially graceful** (readable but with visible differences), **Not graceful** (missing content or visible raw tokens)
- R4. For partially and not-graceful extensions, describe the specific artifact or gap a reader would see
- R5. Add a brief summary table or note to the whitepaper's compatibility section that acknowledges the degradation tiers without undermining the interchangeability message
- R6. Add a "CommonMark Rendering" note to relevant sections of the syntax reference so authors encounter degradation info at point of use

## Success Criteria

- A reader can look up any Markdown++ extension and immediately understand what it looks like in GitHub/VS Code preview
- The whitepaper's compatibility claims are accurate and qualified where needed
- Authors using variables or file includes are warned about visible artifacts

## Scope Boundaries

- Out of scope: changing extension syntax to improve degradation
- Out of scope: building tooling to preview degradation
- Out of scope: testing against specific renderers (the matrix describes CommonMark-spec behavior)

## Key Decisions

- **Affirmative framing over defensive**: Consistent with the interchangeability solution doc — describe what renders and how, not what "breaks"
- **Three-tier categorization**: Fully graceful / Partially graceful / Not graceful — matches the issue proposal and is intuitive
- **Spec appendix as primary artifact**: The full matrix belongs in `spec/` alongside the whitepaper, with lighter references woven into existing docs

## Next Steps

→ Proceed directly to work — scope is clear, deliverables are well-defined
