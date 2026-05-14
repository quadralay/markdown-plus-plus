---
title: "Multiline table row-continuation mechanism: state it positively, don't privilege the first cell"
date: 2026-05-13
category: documentation-gaps
module: markdown-plus-plus-skill
problem_type: documentation_gap
component: documentation
severity: medium
applies_when:
  - "Writing or reviewing skill documentation that describes multiline-table row continuation"
  - "Authoring LLM-facing reference prose where the trigger for a behavior matters more than its side effects"
  - "Sweeping legacy phrasing across multiple surfaces (SKILL.md, references/, examples/) in one PR"
symptoms:
  - "LLM authors emit no-pipe blank lines between records, which terminates the table per spec/processing-model.md Conformance > Required Features item 7"
  - "LLM authors treat empty-first-cell as a trigger they must police rather than a property of a continuation row"
  - "Doc prose treats empty/content cells as parallel row-classifying triggers instead of stating the mechanism positively"
root_cause: inadequate_documentation
resolution_type: documentation_update
related_components:
  - tooling
tags:
  - markdown-plus-plus
  - multiline-tables
  - skill-documentation
  - llm-authoring
  - row-continuation
  - issue-92
---

# Multiline table row-continuation mechanism: state it positively, don't privilege the first cell

## Context

Markdown++ skill docs framed multi-line table row continuation as "an empty first cell continues the previous row." The phrasing is technically consistent with `spec/processing-model.md` (*Conformance > Required Features* item 7, lines 547-551) but treats two parallel categories -- "first content row" and "continuation row" -- as if the empty cell were the *trigger* that caused continuation. Issue #92 documented two failure modes this framing produced in LLM-authored tables:

1. **No-pipe blank line between records.** LLMs interpreted record separation as a CommonMark paragraph boundary and emitted a fully blank line between logical rows. Per the spec, a no-pipe blank line terminates the table entirely rather than separating rows.
2. **Empty-first-cell as a policed trigger.** LLMs treated the empty cell as something they had to *cause* and *protect*, rather than as the natural consequence of "this physical line belongs to the row above." Some inferred that content in a continuation line's first cell would silently be promoted to a new row.

The legacy phrasing appeared on five surfaces (`SKILL.md` line 248, `references/syntax-reference.md` Structure Rules around line 815, `references/best-practices.md` line 278, `references/examples.md` line 216, `examples/multiline-tables.md` line 29), all reinforcing the same incomplete mental model.

A first reframe attempt named "three structural triggers in evaluation order" — row separator, continuation row (first cell empty), new logical row (first cell has content). That preserved the underlying error: it still made "the first cell" the classifier and implied that content in the first cell of a physical line would start a new logical row. The actual mechanism does not look at the first cell. It does not look at any specific cell. The classifier is whether *every* cell on the line is whitespace.

## Guidance

Frame multiline-table row continuation as **two structural roles**, and state the mechanism positively:

1. **Row separator** -- A row where every cell contains only whitespace (regex `^ {0,3}\|(?:[ ]*\|)+[ ]*$`). Starts a new logical row. This is the only way to signal a new logical row.
2. **Continuation row** -- Any other pipe-bearing row. Merged into the current logical row.

A no-pipe blank line is a third case that ends the table entirely — promote that warning to an `> **Important:**` callout immediately under the rules, on every surface.

**Explain empty cells as a consequence, not a trigger.** Cells appear empty on a continuation line when their column has no more content to flow there. The presence or absence of content in any particular cell — including the first cell — is not what determines continuation. State this once in the canonical structure-rules section; do not repeat it in every example.

**Avoid the "first cell" idiom entirely** in prose that describes the mechanism. Singling out the first cell preserves the misconception that the first cell is privileged. Example tables often happen to have empty first cells on continuation lines because the first column is a record-label column with no multiline content — that is incidental to the example, not part of the rule.

Cross-reference the normative text as `spec/processing-model.md`, *Conformance > Required Features* item 7 (lines 547-551) -- not "§7". The "§7" form was an autofix correction during code review; the spec has no `§7` heading.

**Secondary readability teaching.** When a continuation row carries several values for one cell across multiple physical lines, prefixing each value with `- ` (a CommonMark list marker) makes the entries scannable and preserves graceful-degradation rendering as a bulleted list inside the cell column. This is a readability convention, not a structural rule, and it is separate from the row-continuation mechanism.

## Why This Matters

- **AI authoring correctness.** The dominant audience of the skill is an LLM author. Stating the mechanism positively ("every pipe-bearing row continues; only an all-whitespace row separates") lets a first-time AI author produce correct multi-row multiline tables on the first try. The no-pipe-blank-line failure mode is unrecoverable because it silently terminates the table.
- **The "first cell" reframe trap.** Even reformers fall into the "first cell" framing because the canonical examples make the empty first cell visually salient. The first cell is not special. State the rule in terms of "all cells whitespace" vs "any other pipe-bearing row" and let cell-emptiness fall out as a consequence.
- **Graceful-degradation correctness.** Multiline tables must render correctly under plain CommonMark. The `- ` list-marker convention preserves that rendering; mis-framed continuation rules cause LLMs to emit tables that render as broken CommonMark. See [graceful-degradation-commonmark-rendering-2026-04-08](graceful-degradation-commonmark-rendering-2026-04-08.md).
- **Doc-sweep completeness.** Five surfaces carried the legacy phrasing; missing any one of them leaves a contradiction the LLM will surface as a question or a wrong inference. Treat multi-surface phrasing fixes as one unit of work.

## When to Apply

- Editing or adding to any of the five canonical multiline-table doc surfaces (`SKILL.md`, the three `references/*.md` files, `examples/multiline-tables.md`).
- Reviewing AI-authored multiline tables -- flag any table separated by no-pipe blank lines.
- Writing a one-to-two-sentence skill summary that mentions row continuation: lead with the positive statement ("every pipe-bearing row continues; an all-whitespace row separates") and always retain the "no-pipe blank line ends the table" subordinate clause.
- Authoring downstream WebWorks docs (e.g., `webworks-claude-skills/markdown-integration`) that mirror this phrasing.
- Reviewing PRs that touch multiline-table prose -- grep for `empty first cell`, `first cell is empty`, `first cell contains content`, and `three structural triggers`, and reject re-introductions of any of those.

## Examples

**Canonical Structure Rules** in `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` (around line 818):

```markdown
Multiline tables classify each physical pipe-bearing line by one of
two structural roles:

1. **Row separator** -- A table row where every cell contains only
   whitespace. Matches the pattern `^ {0,3}\|(?:[ ]*\|)+[ ]*$`.
   Starts a new logical row. This is the only way to signal a new
   logical row.
2. **Continuation row** -- Any other pipe-bearing row. Merged into
   the current logical row. Cells appear empty on a continuation
   line when their column has no more content to flow there; the
   presence or absence of content in any particular cell is not
   what determines continuation.

> **Important:** A completely blank line (no pipe characters) **ends
> the table entirely** -- it does not separate rows. Logical-row
> separation requires a pipe-bearing row with whitespace-only cells,
> not a blank line.

See `spec/processing-model.md`, *Conformance > Required Features* item
7, for the normative requirements.
```

**With-list-markers example** for multi-value cells (same file, new "List markers in multi-line cells" subsection around line 867):

```markdown
<!-- multiline -->
| Component | Notes               |
|-----------|---------------------|
| Database  | PostgreSQL 14+      |
|           | - 4 GB RAM minimum  |
|           | - 50 GB disk space  |
```

The `- ` prefix is a CommonMark list marker, so each continuation line still renders as a list item under graceful degradation -- readers viewing the source as plain CommonMark see a bulleted list inside the cell column rather than a stream of values.

**SKILL.md summary rewrite** (line 248):

> Every pipe-bearing row continues the current logical row. A row whose cells are all whitespace starts a new logical row — that's the only way to signal one. A no-pipe blank line ends the table. Cells on a continuation line appear empty when their column has no more content to flow there. Combine with style: `<!-- style:DataTable ; multiline -->`. See `references/syntax-reference.md` for multiline table rules.

The summary holds a one-to-two-sentence budget while stating the mechanism positively, naming the table-terminating subordinate clause, and explaining empty cells as a consequence of column content flow rather than a trigger.

## Related

- [multiline-table-separator-pattern-docs-2026-04-08](multiline-table-separator-pattern-docs-2026-04-08.md) -- sibling terminology fix from issue #20 that corrected "empty-row" separator framing in the same surfaces; addresses a different framing axis than #92
- [multiline-cell-extensions-spec-2026-04-08](multiline-cell-extensions-spec-2026-04-08.md) -- establishes the "logical row" vocabulary that this guidance reinforces
- [graceful-degradation-commonmark-rendering-2026-04-08](graceful-degradation-commonmark-rendering-2026-04-08.md) -- underpins why the `- ` list-marker convention is more than cosmetic
- [../conventions/imperative-anchor-section-for-skill-syntax-drift-2026-05-13.md](../conventions/imperative-anchor-section-for-skill-syntax-drift-2026-05-13.md) -- skill-presentation pattern for high-drift syntax surfaces
- [../conventions/skill-reference-docs-capture-cleanup-knowledge-2026-05-11.md](../conventions/skill-reference-docs-capture-cleanup-knowledge-2026-05-11.md) -- reference-doc lifecycle coverage
- GitHub: issue #92 (this work), #20 (origin of the April separator-pattern doc)
