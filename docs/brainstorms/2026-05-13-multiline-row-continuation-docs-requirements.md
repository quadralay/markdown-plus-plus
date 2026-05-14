---
date: 2026-05-13
topic: multiline-row-continuation-docs
status: active
issue: 92
---

# Multiline Table Row-Continuation Mechanism: Doc Clarification

## Problem Frame

Several Markdown++ surfaces describe multiline-table row continuation in
a way that reads as "the empty first cell is what makes a row continue."
The legacy phrasing appears in three places that AI authors and human
contributors hit first:

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
  line 248 -- "Empty first cell continues previous row; a row with
  pipes and whitespace-only cells separates rows ..."
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
  lines 820-822 -- numbered "Structure Rules" listing "Continuation
  rows -- Empty first cell (`|          |`) continues the previous row."
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
  line 278 -- "Continuation rows use empty first cell (`|      |`)."
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md`
  line 216 -- "Each row uses continuation lines (empty first cell) and
  is separated by a row with pipes and whitespace-only cells."

Issue #92 reports that this phrasing causes LLM authors to mis-model
the mechanism in two observable ways:

1. They emit a no-pipe blank line between records (which actually
   terminates the table, MDPP behavior per `spec/processing-model.md`
   §7.c) instead of a pipe-delimited whitespace-only separator row.
2. They treat the first cell's emptiness as a *meaningful trigger*
   they must police, rather than a side-effect of "this line belongs
   to the row above."

The author's proposed reframe -- "rows automatically continue until
an all-blank-cells row is encountered" -- is partially in tension
with the authoritative spec text. `spec/processing-model.md` §7.b is
explicit that "a table row whose first cell is empty MUST be merged
into the preceding logical row," and §7.a defines the row separator
as a row where every cell is whitespace. The spec is **silent** on
what a processor MUST do when a row has content in its first cell
mid-table; every existing example treats that case as the start of
a new logical row.

This brainstorm covers the doc-level fix. It deliberately separates
the parts of the issue that are pure clarification from the part that
would change semantics, because the second category needs a real spec
decision before docs land.

## Out of Scope

- Changes to `spec/processing-model.md`, `spec/multiline-cell-extensions.md`,
  or any other normative spec text.
- Changes to `scripts/format-tables.py` (the formatter is line-
  pass-through for multiline tables; it never decides what a logical
  row is).
- Adding the issue's suggested counter-example showing content in the
  first cell of a continuation line. That example would teach a
  semantic the spec does not currently define and that no existing
  test or example endorses. **It is deferred to a separate brainstorm
  that proposes the spec change explicitly.**
- Cross-repo propagation (webworks-claude-skills `markdown-integration`,
  downstream WebWorks brain documentation). Those follow once this
  upstream phrasing lands.
- Rewriting `examples/multiline-tables.md` body. Only the trailing
  prose ("Continuation rows (empty first cell) extend a logical row...")
  needs phrasing alignment, not the table data itself.
- Auto-validator MDPP error code for "no-pipe blank line inside a
  multiline table." A separate diagnostic might prevent the LLM
  failure mode, but adding diagnostics is a separate workstream.

## Requirements

### R1. Rewrite the Structure Rules in `references/syntax-reference.md`

The current numbered list (lines 820-822) treats "first content row"
and "continuation row" as parallel structural types, which encourages
the reading that the empty first cell is the trigger. Replace with
a triple that names the **trigger** for each behavior, in evaluation
order, aligned with `spec/processing-model.md` §7:

1. **Row separator** -- A table row where every cell contains only
   whitespace. Matches `^ {0,3}\|(?:[ ]*\|)+[ ]*$`. Marks the boundary
   between two logical rows.
2. **Continuation row** -- A table row whose first cell is empty and
   that is not a row separator. Merged into the preceding logical row.
3. **New logical row** -- A table row whose first cell contains
   content. Starts a new logical row.

Add an explicit "Important" callout immediately below the list
restating the existing line 824 warning: a completely blank line (no
pipe characters) ends the table; only pipe-bearing whitespace-only
rows are separators. Promote that warning visually -- the LLM failure
mode in #92 is exactly this confusion.

Cross-reference `spec/processing-model.md` §7 directly so readers who
need the normative phrasing can find it.

**Why "convention" framing is rejected.** The issue suggests adding a
"Convention" item: "Typically only the first line of a row has content
in the first cell, but this is for readability -- any cell can have
content on any line." That sentence is a spec-change claim. Adding it
to the rules section without changing `spec/processing-model.md` would
create a documented behavior that the spec does not require any
processor to implement. The clarification this requirement delivers
is structural, not permissive.

### R2. Update the `SKILL.md` summary

The current `SKILL.md` line 248 reads:

> Empty first cell continues previous row; a row with pipes and
> whitespace-only cells separates rows (a blank line ends the table).
> Combine with style: `<!-- style:DataTable ; multiline -->`. See
> `references/syntax-reference.md` for multiline table rules.

Rewrite the first clause to lead with the three-way distinction,
matching R1, without leaking the full rules into SKILL.md. Target
length: one to two sentences, no longer than the current. The
"a blank line ends the table" subordinate clause must remain, because
it is the failure mode #92 reports.

Suggested rewrite (not normative -- implementation picks final
phrasing during PR):

> Each multiline-table row continues the previous logical row when
> its first cell is empty; a row where every cell is whitespace is a
> row separator; a no-pipe blank line ends the table. Combine with
> style: `<!-- style:DataTable ; multiline -->`. See
> `references/syntax-reference.md` for multiline table rules.

### R3. Document `- ` list markers as a readability technique

Add a brief readability subsection to `references/syntax-reference.md`
(immediately after "Cell Content Dedent" reads naturally) named
"List markers in multi-line cells" or similar. Content:

- State the technique: prefixing each value with `- ` on its own
  continuation line makes multi-value cells visually scannable,
  especially when rows have varying numbers of continuation lines.
- Show one short before/after pair: the same cell with bare values
  vs. dashed values.
- Note that the dash is a CommonMark list marker, so each line also
  renders correctly under graceful degradation (see
  `spec/processing-model.md` reference for fallback behavior).
- Cross-reference: this is the same convention as
  `references/examples.md` already shows in its scenario tables.

This requirement is independent of R1/R2 and could ship by itself if
the rule rewrites need more review. It is a pure addition with no
existing prose to displace.

### R4. Sweep the adjacent legacy phrasings

Three other surfaces carry the same "empty first cell continues"
phrasing and will read as drift if R1 and R2 ship without them:

| Surface | Line | Treatment |
|---------|------|-----------|
| `references/best-practices.md` | 278 | Rephrase to match R1 triple; keep brief (this is a bullet, not a rules section). |
| `references/examples.md` | 216 | Rephrase the intro prose to match R1; do not change the example tables themselves. |
| `examples/multiline-tables.md` | 29 | Rephrase the trailing one-sentence explanation; do not touch the tables. |

Each is a one-sentence edit. Bundling them with R1/R2 prevents the
next contributor from copy-pasting the old phrasing back in.

### R5. Validation pass

After the writes:

- Run `scripts/validate-mdpp.py` against every file touched, including
  the brainstorm doc itself. No new MDPP diagnostics should appear.
- Re-run the auto-activation suite at
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`
  manually. None of the cases describe row-continuation language
  directly, but the routing layer should still pick up these files
  as Markdown++ on the strength of unchanged signals (the
  `<!-- multiline -->` directive in examples is still present).
- Visually verify that the example tables in `references/examples.md`
  and `examples/multiline-tables.md` still render under graceful
  degradation -- no example body changed, but the surrounding prose
  framing did.

## Assumptions

These were inferred in autonomous mode without user confirmation. Each
should be re-validated when this requirements doc enters planning.

- **A1.** `spec/processing-model.md` §7.b's silence on the
  "content-in-first-cell-mid-table" case means the conventional
  interpretation (start a new logical row) is correct. Every example
  in the repo reinforces this. If the actual reference parser (which
  is not in this repo) implements "automatic continuation until
  separator", R1's third bullet ("new logical row") is wrong and the
  whole brainstorm flips toward the issue's original framing.
- **A2.** Issue #92's reference to a `Page.asp` and `skin.scss` table
  is illustrative only -- those file extensions are outside the
  Markdown++ ecosystem and the suggestion uses them as plausible
  workload artifacts. Treat the example as a syntax-only demonstration
  of the list-marker convention; the actual file types are not
  required to land in any rewritten example.
- **A3.** Issues #93 and #99, listed as blockers in the issue body,
  are merged (commit `1ce0c6d` merges #93; #99 status not directly
  visible but the issue header has not been updated to reflect any
  remaining block). Proceed without re-checking. If the merge actually
  leaves a dependency unfinished, R1's reference to
  `spec/processing-model.md` §7 may need adjustment for any newly-
  introduced spec section numbering.
- **A4.** The four issue asks were prioritized on the assumption that
  asks #1, #2, #4 are doc clarifications and ask #3 (the counter-
  example) is a spec change. If the project maintainer reads ask #3
  as also a clarification (i.e., the actual reference implementation
  is permissive about content in continuation rows), then R1's
  "new logical row" bullet should be replaced with the issue's
  "Convention" bullet, R3 still ships unchanged, and a new spec PR
  should be opened to update `spec/processing-model.md` §7.b in the
  same release.

## Success Criteria

- A first-time AI author reading `SKILL.md` does not produce a
  multiline table with no-pipe blank lines between records when asked
  for a multi-row multiline table. Verify by manual probe after
  changes land.
- `references/syntax-reference.md` "Structure Rules" names a row
  *separator*, a *continuation row*, and a *new logical row* with the
  trigger for each, and the three triggers are exhaustive (every
  pipe-bearing physical line falls into exactly one category).
- `references/best-practices.md`, `references/examples.md`, and
  `examples/multiline-tables.md` no longer carry the legacy "empty
  first cell continues previous row" phrasing. Grep verification:
  the only remaining mentions of "empty first cell" describe it as
  a *property of a continuation row*, never as the *cause* of
  continuation.
- A list-marker subsection exists in `references/syntax-reference.md`
  with at least one before/after example, and it is linked from the
  body of the multiline tables section.

## Dependencies

- None on other in-flight workstreams. R1/R4 touch files that are
  not currently being edited by an open PR in this branch context.
- The brainstorm intentionally does **not** depend on `spec/processing-
  model.md` changing. If the maintainer decides A1 is wrong, this
  requirements doc must be revised before planning proceeds.

## Handoff Notes

- This is a doc-tier change, scope **Standard**. The path forward is
  `/ce-plan` against this requirements doc, then a single PR that
  touches the four files listed in R1, R2, R4 plus the new subsection
  in R3.
- Version bump expected: `patch`. No new feature; no breaking change.
- Recommended PR title: "Closes #92: Clarify multiline table row-
  continuation mechanism."
