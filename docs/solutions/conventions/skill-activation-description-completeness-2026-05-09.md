---
title: Author skill descriptions to enumerate every distinguishing signal, not a partial list
date: 2026-05-09
category: conventions
module: plugins/markdown-plus-plus/skills
problem_type: convention
component: tooling
severity: medium
applies_when:
  - Authoring or revising the description frontmatter of a Claude Code SKILL.md
  - A skill must auto-activate from file content patterns rather than slash invocation
  - The skill is one of multiple sibling skills competing for the same routing slot
  - Adding a new distinguishing directive or syntax surface to the skill's domain
tags:
  - skill-authoring
  - skill-description
  - auto-activation
  - claude-code-plugin
  - markdown-plus-plus
  - frontmatter
---

# Author skill descriptions to enumerate every distinguishing signal, not a partial list

## Context

A Claude Code skill's `description:` frontmatter is the routing layer's primary input for deciding whether to auto-activate the skill on a given turn. The Markdown++ skill description originally listed six activation signals (`<!--style:-->`, `<!--condition:-->`, `$variable;`, `<!--include:-->`, `<!--marker:-->`, `<!--#alias-->`) but omitted three more — `<!--multiline-->` table directives, the `<!--markers:-->` plural form, and `mdpp-version:` YAML frontmatter — that are equally distinguishing. It also showed signals with no internal whitespace (`<!--style:-->`) while real files routinely use `<!-- style:Title -->`, and it said nothing about derivative-file cases where a user asks for a new file modeled on an existing one.

The result: a real failure case where a user asked the agent to create a new release-notes file modeled on an existing one that used `<!-- multiline -->` before its table. The skill did not auto-activate, the agent produced a malformed single-row table, and the user had to invoke the skill manually to recover. The description had been "good enough" for the obvious cases but silently wrong for the long tail.

## Guidance

Treat the `description:` field as a routing contract, not marketing copy. When authoring or revising it:

1. **Enumerate every distinguishing signal exhaustively.** Cross-check the description against the skill body's reference content (syntax tables, directive lists, frontmatter fields). Anything documented in the body as a directive or token of the format must appear in the description's signal list. Partial lists train the routing layer to fire only on the obvious cases.
2. **List both singular and plural directive forms explicitly** (e.g., `<!--marker:-->` *and* `<!--markers:-->`). Don't assume the model will infer the pair.
3. **Cover whitespace variants explicitly.** Real-world files use `<!-- style:Title -->` with internal whitespace; the canonical form in docs is `<!--style:-->` without it. Add a parenthetical clause stating that whitespace inside HTML comments is irrelevant to matching, rather than relying on the routing layer to be lenient.
4. **Include frontmatter-based signals**, not just inline directives. If the skill recommends a YAML frontmatter field for new files (here: `mdpp-version:`), it is a distinguishing signal and belongs in the description.
5. **Cover derivative-file creation explicitly.** When a user asks to create a `.md` file modeled on an existing one, the new file may not yet contain the signals — but the source file does. Add a clause: "Also use when creating a `.md` file modeled after another file containing any of these signals."
6. **Preserve the lede that the routing layer keys on.** Don't redefine the skill while extending the trigger list. The "AUTHORITATIVE REFERENCE for X syntax" framing and the closing "Use for editing, validating, migrating, or auditing" intent clause should stay byte-stable across revisions of the signal list.
7. **Bump the plugin version** when the description changes (`scripts/bump-version.sh patch` for routing-only edits). The description ships through `plugin.json` and `marketplace.json`; a version bump keeps both manifests synchronized and gives downstream marketplace consumers a clean upgrade signal.

## Why This Matters

A skill description that misses signals fails silently. There is no error, no warning, and no test in this repo that can detect under-activation — the symptom only appears when a user encounters a real document the routing layer should have caught and didn't. By the time the gap is noticed, the agent has already produced wrong output and the user has had to debug *why the skill didn't fire* on top of whatever they were originally trying to do.

The cost of a complete signal list is one paragraph of folded YAML. The cost of a partial list is a class of silent failures that recur every time the format grows a new directive or the user works with a derivative file. Exhaustive enumeration also documents the format's surface area in a single place that the routing layer, the model, and human readers all consume — drift between the description and the skill body becomes a visible diff rather than an invisible behavior gap.

The whitespace and derivative-file clauses matter for the same reason: they close gaps the model would otherwise have to bridge by inference, and inference under routing latency is unreliable.

## When to Apply

- Every revision of a SKILL.md `description:` field, not just the initial authoring pass.
- When the skill grows a new directive, frontmatter field, or token surface — update the description in the same change.
- When investigating any "the skill didn't fire when it should have" report — diagnose the description first, before assuming the routing layer is at fault.
- When auditing sibling skills that compete for the same routing slot (e.g., `markdown-plus-plus:markdown-plus-plus` and `webworks-claude-skills:markdown-plus-plus`); divergent descriptions across siblings are an activation hazard.

## Examples

**Before** — partial signal list, no whitespace clause, no derivative-file coverage:

```yaml
description: >
  AUTHORITATIVE REFERENCE for Markdown++ syntax. Use when working with
  .md files containing <!--style:-->, <!--condition:-->, $variable;, <!--include:-->,
  <!--marker:-->, or <!--#alias--> patterns. Use for editing, validating,
  migrating, or auditing Markdown++ source documents.
```

**After** — exhaustive signal list, whitespace-irrelevance clause, derivative-file clause, lede and closing preserved:

```yaml
description: >
  AUTHORITATIVE REFERENCE for Markdown++ syntax. Use when reading or writing
  .md files that contain any of these signals (whitespace inside the HTML
  comment is irrelevant): <!--style:--> directives, <!--multiline--> table
  directives, <!--condition:--> blocks, <!--include:--> directives,
  <!--marker:--> or <!--markers:-->, <!--#alias--> anchors, $variable; tokens,
  or mdpp-version: in YAML frontmatter. Also use when creating a .md file
  modeled after another file containing any of these signals. Use for editing,
  validating, migrating, or auditing Markdown++ source documents.
```

The diff is confined to the `description: >` folded scalar; `name:`, the `---` delimiters, and the SKILL.md body stay byte-identical. The version bumps `1.1.15 → 1.1.16` in both `plugins/markdown-plus-plus/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` via `scripts/bump-version.sh patch`.

## Related

- GitHub issue #84 — original report of the auto-activation failure case
- Plan: `docs/plans/2026-05-09-002-docs-skill-description-trigger-signals-plan.md`
- Work commit: `1d921c0` on `claude/issue-84`
- `CLAUDE.md` § Version Management — the patch-bump convention applied here
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` — the file whose description this convention governs
