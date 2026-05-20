---
title: Anchor high-frequency syntax patterns in a SKILL.md body section with imperative MUST/ALWAYS/NEVER framing
date: 2026-05-13
category: conventions
module: plugins/markdown-plus-plus/skills/markdown-plus-plus
problem_type: convention
component: documentation
severity: medium
applies_when:
  - Authoring a Claude Code SKILL.md body where the existing detail content already covers a rule but AI agents still drift on it
  - A consumer repo has been forced to hand-author template files to teach Claude patterns the skill already documents
  - One or two combined directive forms account for most of the drift, even though many forms exist
  - The detail content uses soft "must" / "should" language and there is no single copy-paste-ready block agents can mentally cache
  - Revising a skill in response to repeated downstream syntax-fix commits on the same pattern family
tags:
  - skill-authoring
  - skill-body
  - anchor-section
  - imperative-framing
  - markdown-plus-plus
  - agent-drift
---

# Anchor high-frequency syntax patterns in a SKILL.md body section with imperative MUST/ALWAYS/NEVER framing

## Context

The `markdown-plus-plus` SKILL.md already documented every Markdown++ command block rule across `<syntax_examples>`, `<common_mistakes>`, and `references/syntax-reference.md`. Detail content was technically complete: attachment rule covered, combined-command priority covered, whitespace handling covered, every directive form illustrated. Despite that, downstream authoring sessions kept producing the same three mistakes on the two highest-frequency combined directive forms (`style + alias`, `markers + alias`):

- Blank line inserted between the directive comment and its target content (silently breaks the attachment rule)
- Alias placed on a separate stacked HTML comment instead of combined with `;`
- Spacing varied arbitrarily inside `<!-- ... -->`

The downstream evidence was concrete: PR `quadralay/epublisher-express-trial#1` required four-plus syntax-fix commits, and the consumer repo's authors had hand-authored a `TOPIC-TEMPLATE.md` file inside their own repo to give Claude a copy-paste anchor — a workaround for skill content the agent had read but could not reliably reassemble from multiple sections under vague prompts.

The skill's content was right. Its **presentation** was the gap. An agent reading the SKILL.md top-to-bottom encountered the canonical combined patterns scattered across detail-heavy sections written in soft "must" / "should" voice, with no single high-visibility "this is the form, copy it" block to anchor to.

## Guidance

When a SKILL.md body is technically complete but agents still drift on a small number of high-frequency patterns, add a single imperative **anchor section** between the overview and the detail content. The anchor is not a rewrite of the detail — it is a navigational landmark with the canonical copy-paste patterns and an explicit list of mistakes to never make.

Shape the section by these rules:

1. **Place it early, between the overview and the deep examples.** Wrap it in its own semantic block tag matching the file's existing convention (here, `<command_block_syntax>` between `</overview>` and `<syntax_examples>`). Early placement is what makes it an anchor rather than buried trivia.
2. **Use imperative MUST / ALWAYS / NEVER voice.** The detail content can keep its softer normative voice — the anchor is the place where the rules are harder to skim past. The lede states the format and the no-blank-line attachment requirement in two sentences.
3. **Cover only the highest-frequency patterns.** Two combined patterns (the ones the drift evidence cites) plus three compact single-directive forms is enough. Showing every possible combination dilutes the anchor back into a reference table.
4. **End with an explicit NEVER list keyed to the observed drift.** Each bullet names the mistake, then states the consequence in plain terms (e.g., "the directive passes through as a regular HTML comment with no effect"). The consequence is what makes the rule memorable.
5. **Cite the spec; don't invent new rules.** Every NEVER bullet must trace back to existing documented behavior in `references/syntax-reference.md` or the spec. The act of writing imperative framing is where it is easiest to over-prescribe — see the [Examples](#examples) section for a concrete near-miss.
6. **Match the recommended form to the existing repo convention.** If the reference doc says spaces around `;` are recommended, the canonical patterns in the anchor use spaces around `;`. If the no-space form is also valid, say so in one short sentence rather than promoting one form to the only form.
7. **End with a "see also" line, not a duplication of detail.** Link to the existing detail sections (`<common_mistakes>`, `references/syntax-reference.md`, the normative spec). Duplicated content drifts; references do not.
8. **Keep the section under ~50 lines.** Anchors lose their anchoring quality once they grow into another reference. If it grows past that, the new material belongs in the detail sections, not the anchor.

## Why This Matters

Technically-complete documentation is not the same as agent-discoverable documentation. The routing layer brings the skill into context, but the model still has to assemble a canonical pattern from whatever sections it weighs most heavily in its current turn. On a vague prompt ("add a row to that table"), the model often weights the closest example over the rule that governs it, and produces output that fits a section it skimmed past the canonical form.

The cost of the gap is paid in the consumer's repo, not the skill repo, and is invisible from the skill side until someone reports a pattern of syntax-fix commits or a hand-authored template. By that point the user has paid for several rounds of correction on rules the skill already documented. A single high-visibility anchor block is cheap to add and inexpensive to maintain — it does not change the spec, it does not change any rule, and the detail content keeps doing its job.

The constraint to cite the spec (rule 5) matters specifically because imperative framing is also the form most likely to harden a model's own paraphrase into a new rule. During this change, a draft of the NEVER list included "pick one form and stay consistent within a document" for spacing — a plausible-sounding directive that the reference doc does not require. The cross-reviewer caught it before merge. Without that catch, the anchor would have shipped with a hallucinated per-document consistency rule and the skill would have started teaching something the spec does not say.

## When to Apply

- The skill body already documents a rule, but downstream PRs show repeated commits fixing the same syntax mistake on the same pattern.
- A consumer repo has authored its own `TOPIC-TEMPLATE.md`-style file inside its own tree as a workaround for patterns the skill already covers.
- The skill content uses soft normative voice and lacks a single copy-paste-ready block for the highest-frequency combined forms.
- Adding the section does not require touching `<syntax_examples>`, `<common_mistakes>`, or the reference docs — if it does, the change is a content revision, not an anchor addition.

Do **not** apply when:

- The drift is on a rare or low-frequency pattern. Anchor sections work because they cover the two or three patterns that account for most of the drift; broadening to "every pattern" dissolves the anchor.
- The detail content is wrong or incomplete. Fix the detail first; an anchor cannot rescue underlying gaps.
- The drift is in the description frontmatter or routing surface. That class of failure is covered by [[skill-activation-description-completeness]] — a different lever.

## Examples

### The anchor section as shipped

The block added to `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` between `</overview>` (formerly line 40) and `<syntax_examples>` (now line 89) — see commit `8a1d057` for the full text. The structure:

```
<command_block_syntax>

## Command Block Syntax (MUST follow exactly)

ALWAYS use this format -- no variations. Content MUST follow the
directive on the very next line with no blank line between them.

### Style + alias (combined)
  (canonical pattern, spaces around `;`, content on next line)

### Markers + alias (combined)
  (canonical pattern, spaces around `;`, heading on next line)

### Single-directive forms
  (style alone, marker alone, alias alone)

### NEVER
  - Blank line between directive and content (consequence: silently breaks attachment)
  - Alias on separate stacked comment (consequence: top comment orphaned)
  - Inconsistent spacing (consequence: cites spec for recommended form, no-space form also valid)

See `references/syntax-reference.md` (Attachment Rules, Combined Commands)
and the `<common_mistakes>` section below. See `../../../../spec/attachment-rule.md`
for the normative definition.

</command_block_syntax>
```

### The near-miss caught by review

A draft of the third NEVER bullet read, in part:

> The canonical form has spaces around each `;`. Pick one form and stay consistent within a document.

The phrase **"pick one form and stay consistent within a document"** is not in `references/syntax-reference.md`. The reference says spaces around `;` are "optional but recommended for readability" and marks both forms valid; it does not require per-document consistency. The cross-reviewer flagged this as a fabricated rule (cross-reviewer promotion to 100% confidence), and the fix was to rewrite the bullet to cite the spec directly:

> The canonical form has a space after `<!--`, a space before `-->`, and spaces around each `;`. The no-space form (`<!--style:A;#b-->`) is also valid; the spaced form is recommended for readability per `references/syntax-reference.md` (Combined Commands -> Whitespace).

Same imperative anchor, no invented constraint. Commit `89c0246` for the fix.

The lesson generalizes: write the anchor section's imperative bullets while looking at the corresponding sentences of the reference doc, not from memory of "what the rule probably is." The act of compressing detail into an imperative bullet is where new constraints sneak in.

### Version & changelog discipline that ships with the anchor

The skill change is content, not behavior, but it is substantive author-facing guidance. The `scripts/bump-version.sh minor` bump (`1.5.0 -> 1.6.0`) and CHANGELOG entry under **Tooling** are part of the same change set so downstream marketplace consumers get a clean signal that the skill body changed.

## Related

- [[skill-activation-description-completeness]] — the **routing-time** analogue. That doc covers the `description:` field as the routing contract; this doc covers the **body** as the agent's working anchor once routing has succeeded. The two are complementary levers for the same class of silent-failure problem.
- [[skill-reference-docs-capture-cleanup-knowledge]] — when a downstream repo discovers patterns the skill should document, that doc covers capturing inverse-direction rules in `references/`; this doc covers when to surface a frontline anchor in the SKILL.md body instead.
- [[manual-verification-fixtures-for-unobservable-routing]] — anchor-section effectiveness is itself unobservable from in-repo automated tests; a future fixture suite could regression-check agent behavior on the same vague-prompt scenarios that produced the drift.
- Issue #93, plan commit `013c973` (`docs(plan): capture command block syntax anchor plan for #93`), implementation commits `8a1d057` (anchor added) and `89c0246` (invented-rule fix).
- Downstream evidence: PR `quadralay/epublisher-express-trial#1` (the four-plus syntax-fix commits that prompted this work).
