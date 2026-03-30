---
date: 2026-03-30
topic: neutralize-whitepaper
---

# Neutralize Whitepaper: Remove WebWorks Product References

## Problem Frame

The whitepaper (`spec/whitepaper.md`) is the public-facing document that introduces Markdown++ as a documentation format. It currently contains WebWorks product references (ePublisher, AutoMap, Reverb) and links to the now-migrated `webworks-claude-skills` plugin. These references position Markdown++ as a WebWorks product rather than an open format, undermining its vendor-neutral value proposition. The `webworks-claude-skills` plugin reference is also stale — the Markdown++ skill was migrated to this repo in PR #2.

## Requirements

- R1. Replace the WebWorks AutoMap reference (line 120) with generic "command-line build tools" language. The CI/CD bullet should describe the capability without naming a specific vendor tool.

- R2. Replace the ePublisher-specific multi-format output section (lines 128-135) with a vendor-neutral description of what a Markdown++ publishing pipeline can produce. Keep the output format list (HTML help, PDF, Dynamic HTML, CHM, Eclipse Help) as examples of what publishing tools can target, but decouple them from ePublisher specifically. Remove the "ePublisher can generate Markdown++ from any of its supported input formats" sentence (line 135) — this is product-specific functionality, not format capability.

- R3. Replace the ePublisher-specific Word migration guidance (line 246) with a generic description. The migration section should describe what a publishing tool does (convert Word to Markdown++) without naming ePublisher as the tool that does it.

- R4. Remove or rewrite the "Try it" bullet (line 450) that is a sales pitch for ePublisher's free trial. Replace with a vendor-neutral "publish" bullet describing that publishing tools process Markdown++ into multiple output formats.

- R5. Remove the "Already using ePublisher?" bullet (lines 452). This is a sales pitch for existing ePublisher customers and does not belong in a format specification whitepaper.

- R6. Update the tooling link (line 454) from `webworks-claude-skills` to `[markdown-plus-plus](https://github.com/quadralay/markdown-plus-plus)` plugin for Claude Code. The old plugin no longer contains the Markdown++ skill.

- R7. Update the "Learn the syntax" link (line 446) from the ePublisher hosted docs to the syntax reference in this repo (`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`). Use a relative GitHub link or reference the repo's examples directory.

- R8. Review the historical section (lines 33-43) for tone. Preserve the factual origin story (Quadralay/WebWorks created the format, three decades of publishing expertise) but soften any language that reads as a company pitch rather than credibility context. The history of FrameMaker, Word, DITA support, and seven generations of online help output is valuable factual context — the tone should be "here's where this expertise comes from" rather than "here's why WebWorks is great."

## Scope Boundaries

- **In scope:** Whitepaper text changes only (`spec/whitepaper.md`)
- **Not in scope:** Changes to the plugin, skill, or any other files
- **Not in scope:** Restructuring or rewriting sections beyond what is needed for vendor neutrality
- **Not in scope:** Removing all mention of WebWorks/Quadralay — the historical section (R8) should preserve the origin story as factual context
- **Preserve:** The whitepaper's persuasive tone and structure. This is still a document that advocates for Markdown++ adoption — just not for a specific vendor's tool

## Key Decisions

- **Keep the historical section:** Lines 33-43 establish credibility through real history. Removing them entirely would weaken the whitepaper. The decision is to preserve the facts and adjust only the tone where it reads as marketing rather than context.
- **Keep output format list:** The formats (Reverb/HTML help, PDF, CHM, Eclipse Help, Dynamic HTML) are real publishing targets. They should be listed as what publishing tools can produce, not what ePublisher specifically produces. Reverb should be described generically as "responsive HTML5 online help" rather than by brand name.
- **Generic migration guidance:** Migration sections should describe what is possible with publishing tools, not how to do it with ePublisher specifically. This keeps the migration paths credible while remaining vendor-neutral.
- **Link to repo syntax reference:** The syntax reference lives in this repo at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`. This is preferable to linking to external vendor docs for a format specification whitepaper.

## Success Criteria

- No WebWorks product names (ePublisher, AutoMap, Reverb) appear outside the historical section (lines 33-43)
- The historical section reads as origin context, not a company pitch
- All external links point to this repo or vendor-neutral resources
- The whitepaper still makes a compelling case for Markdown++ adoption
- The document remains factually accurate — no capabilities are claimed that don't exist

## Next Steps

-> `/ce:plan` for structured implementation planning
