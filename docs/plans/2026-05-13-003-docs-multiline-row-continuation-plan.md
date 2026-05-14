---
date: 2026-05-13
status: active
issue: 92
plan_type: docs
origin: docs/brainstorms/2026-05-13-multiline-row-continuation-docs-requirements.md
---

# docs: Clarify Multiline Table Row-Continuation Mechanism

## Summary

Reframe the multiline-table row-continuation mechanism across five surfaces
in the `markdown-plus-plus` skill and `examples/` so that the **trigger**
for each behavior is named explicitly, in evaluation order, aligned with
the normative `spec/processing-model.md` §7 text.

Today the skill repeatedly describes "empty first cell continues previous
row" as if the empty first cell were the *trigger* for continuation. That
phrasing is technically accurate (per spec §7.b) but encourages LLM
authors to mis-model the mechanism — emitting a no-pipe blank line
between records (which actually terminates the table) instead of a
pipe-delimited whitespace-only separator row. Issue #92 collected the
observable failure modes.

The rewrite names three structural triggers — row separator, continuation
row, new logical row — and promotes the existing "no-pipe blank line ends
the table" warning to higher visibility on every surface that carries the
legacy phrasing. A small new subsection documents the `- ` list-marker
readability convention used in scenario tables.

This plan does **not** change any spec text and does **not** introduce
the issue's suggested "Convention" framing (which would assert behavior
the spec is silent on). See Key Technical Decisions and Scope Boundaries.

---

## Problem Frame

`SKILL.md`, `references/syntax-reference.md`, `references/best-practices.md`,
`references/examples.md`, and `examples/multiline-tables.md` all carry
variations of "empty first cell continues previous row." Issue #92 reports
that this phrasing causes two observable LLM failure modes:

1. **No-pipe blank line between records.** LLMs treat record separation
   as a CommonMark paragraph boundary and emit a fully blank line. Per
   `spec/processing-model.md` §7.c this terminates the table entirely
   rather than separating rows.
2. **Empty-first-cell as policed trigger.** LLMs treat the empty cell as
   something they must *cause* in source, rather than as the natural
   consequence of "this physical line belongs to the row above."

The fix is presentation, not semantics. The skill reference, skill summary,
best-practices note, examples intro, and the standalone multiline-tables
example all need their prose aligned to the same triple of named triggers,
in the same evaluation order as the spec.

---

## Requirements

Carried forward verbatim from origin (`docs/brainstorms/2026-05-13-multiline-row-continuation-docs-requirements.md`):

- **R1.** Rewrite the Structure Rules in `references/syntax-reference.md`
  (lines 818-822 region) to name the three triggers in evaluation order:
  row separator, continuation row, new logical row. Add an "Important"
  callout for the blank-line-terminates-table warning. Cross-reference
  `spec/processing-model.md` §7. Reject the issue's suggested "Convention"
  bullet (see KTD-1).
- **R2.** Rewrite the `SKILL.md` line 248 summary to lead with the
  three-way distinction. Same length budget (one to two sentences). Keep
  the "no-pipe blank line ends the table" subordinate clause.
- **R3.** Add a "List markers in multi-line cells" subsection to
  `references/syntax-reference.md` immediately after "Cell Content Dedent"
  (around line 863). One short before/after pair; cross-reference
  `references/examples.md`.
- **R4.** Sweep three adjacent legacy-phrasing surfaces:
  - `references/best-practices.md` line 278 (bullet rephrase)
  - `references/examples.md` line 216 (intro prose rephrase, tables
    unchanged)
  - `examples/multiline-tables.md` line 29 (trailing prose rephrase,
    tables unchanged)
- **R5.** Run `scripts/validate-mdpp.py` against every modified file
  (including the brainstorm doc itself). Manually re-verify the
  auto-activation suite at `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`.
  Visually confirm example tables still render under graceful
  degradation.
- **R-bump.** Bump plugin version `patch` via `scripts/bump-version.sh
  patch` and add a CHANGELOG entry under **Tooling** (or
  **Documentation**, matching repo convention). Doc-only clarification,
  no behavior change.

---

## Scope Boundaries

### In scope

- Edits to the five files named in R1-R4 plus the new subsection in R3.
- `scripts/bump-version.sh patch` and the matching `CHANGELOG.md` entry.
- Validation pass per R5.

### Deferred to Follow-Up Work

- A separate brainstorm proposing a spec change that would explicitly
  permit content in the first cell of a continuation row. The issue's
  "Convention" framing and counter-example belong there, not here. The
  origin doc records this explicitly under its own "Out of Scope"
  section.
- Cross-repo propagation to `webworks-claude-skills/markdown-integration`
  and downstream WebWorks brain documentation. Those follow once this
  upstream phrasing lands.
- An MDPP diagnostic code for "no-pipe blank line inside a multiline
  table." A separate auto-validator workstream may want this; it is not
  in scope here.

### Outside this product's identity

- Changes to `spec/processing-model.md`, `spec/multiline-cell-extensions.md`,
  or any other normative spec text. This plan must not contradict the
  spec or introduce behaviors the spec does not require.
- Changes to `scripts/format-tables.py`. The formatter is line-pass-
  through for multiline tables — it does not decide what a logical row
  is, so it does not need to change for this clarification.
- Body edits to `examples/multiline-tables.md` table content. Only the
  trailing prose explanation needs phrasing alignment.

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **KTD-1.** Reject the issue's "Convention" bullet ("any cell can have content on any line — empty first cell is just readability"). | The spec (`spec/processing-model.md` §7.b) requires merging when the first cell is empty, but is **silent** on what happens when a continuation line has content in the first cell. Every existing example in the repo treats that as starting a new logical row. Adding the "Convention" bullet would document a behavior the spec does not require any processor to implement — a spec-change claim disguised as a clarification. The origin doc rejects this in R1, explicitly. |
| **KTD-2.** Order the three triggers as separator → continuation → new row. | This is the spec's evaluation order (§7.a defines separator first, §7.b defines continuation, then the residual case of "first cell has content" is treated everywhere as a new row). It is also the order an implementer would code: check separator pattern first (deterministic regex), then check empty-first-cell (continuation), and only then assume new row. |
| **KTD-3.** Promote the "no-pipe blank line ends the table" warning to an explicit "Important" callout, on every surface that carries the legacy phrasing. | The issue identifies this exact confusion as the primary LLM failure mode. The current warning exists at `references/syntax-reference.md` line 824 but is easy to miss — promoting it visually is what addresses the failure mode, not just rewording the rules above it. |
| **KTD-4.** Keep the SKILL.md rewrite under the existing one-to-two-sentence budget. | SKILL.md is the in-context summary; it must stay scannable. The rules section in `references/syntax-reference.md` carries the full triple; SKILL.md links there. |
| **KTD-5.** Add the list-marker subsection in `references/syntax-reference.md`, not in `references/best-practices.md`. | The list-marker convention is structural readability inside the existing multiline-tables section. It belongs next to "Cell Content Dedent" because both describe how content within continuation rows is shaped. Best-practices bullets are pointers, not the canonical home for new prose. |
| **KTD-6.** Patch-level version bump. | Doc-only clarification. No new feature, no new syntax, no behavior change. Per `CLAUDE.md` Version Management guidance, "Bug fixes, documentation updates, minor improvements" → `patch`. |

---

## Patterns to Follow

- **Origin doc style.** The brainstorm doc itself uses the
  numbered-list-with-bold-name format the rewritten Structure Rules
  should use (`1. **Row separator** -- …`). Match it.
- **Existing callout convention.** `references/syntax-reference.md` line
  824 already uses the `> **Important:** …` blockquote style for the
  blank-line-terminates warning. The R1 rewrite should keep this exact
  syntax and tighten the prose inside.
- **Cross-reference style.** `references/syntax-reference.md` cross-
  refs the spec with phrases like "See `spec/processing-model.md` §7"
  (no link, just path + section). Match this for the R1 cross-ref.
- **Plan and brainstorm prose style.** Both this plan and the origin
  brainstorm use 72-column wrapping, double-dash em substitution
  (`--`), and reference-style file paths in backticks. Maintain.
- **CHANGELOG entry.** Most recent doc patches in `CHANGELOG.md` use
  imperative one-line entries under a versioned heading. Match the
  most recent doc-only entry's shape.

---

## Implementation Units

### U1. Rewrite Structure Rules in `references/syntax-reference.md`

**Goal:** Replace the three numbered list items at lines 820-822 with the
triple of named triggers in evaluation order, and promote the
blank-line-terminates warning to an explicit "Important" callout.

**Requirements:** R1.

**Dependencies:** None.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
  (modify — replace lines 820-822 list and adjust the surrounding
  intro/cross-ref prose)

**Approach:**

- Keep the section heading "Structure Rules" and the lead-in sentence
  "Multiline tables use a specific row structure:".
- Replace the three-item numbered list with the triple:

  1. **Row separator** -- A table row where every cell contains only
     whitespace. Matches `^ {0,3}\|(?:[ ]*\|)+[ ]*$`. Marks the boundary
     between two logical rows.
  2. **Continuation row** -- A table row whose first cell is empty and
     that is not a row separator. Merged into the preceding logical
     row.
  3. **New logical row** -- A table row whose first cell contains
     content. Starts a new logical row.

- Keep the existing "Important" blockquote at line 824 in place,
  immediately below the new list. Tighten the prose if needed but
  retain the existing pattern (`> **Important:** A completely blank
  line …`).
- Add a one-line cross-reference after the callout: "See
  `spec/processing-model.md` §7 for the normative requirements."
- Do not modify the surrounding sections ("Syntax" above, "Multiline
  Headers" below). Their examples already work under the new framing.

**Patterns to follow:** existing numbered-list-with-bold-name style;
existing `> **Important:** …` callout syntax; existing
path-plus-section cross-ref style.

**Test scenarios:** Test expectation: none -- pure prose edit, no
behavior change. Validation covered by U5 (`validate-mdpp.py` clean,
auto-activation suite still routes the file, graceful-degradation
render unchanged).

**Verification:**

- The Structure Rules section names exactly three triggers, in
  separator → continuation → new-row order.
- Every physical pipe-bearing line falls into exactly one of the three
  categories (exhaustiveness check).
- The "Important" callout is still visible immediately below the list.
- The cross-reference to `spec/processing-model.md` §7 exists.

---

### U2. Add "List markers in multi-line cells" subsection to `references/syntax-reference.md`

**Goal:** Document the `- ` list-marker readability convention with a
short before/after pair, immediately after "Cell Content Dedent" so it
reads as a natural follow-on to "how content in cells is shaped."

**Requirements:** R3.

**Dependencies:** None (could ship independently of U1; bundled here for
single-PR coherence).

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
  (modify — insert a new `### List markers in multi-line cells`
  subsection after the existing "Cell Content Dedent" section ends
  around line 863)

**Approach:**

- Insert a new `###` heading immediately after the "Cell Content
  Dedent" section closes (after the "If one line had no leading
  whitespace, no stripping would occur." sentence) and before the
  existing `### Basic Example` heading.
- Content shape (exact wording finalized at authoring time):
  - One short paragraph stating the technique: prefixing each value
    with `- ` on its own continuation line makes multi-value cells
    visually scannable, especially when rows have varying numbers of
    continuation lines.
  - A `### Without list markers` / `### With list markers` pair, each
    showing a tiny 4-line multiline table fragment with the same data,
    so the visual contrast is the point.
  - One closing sentence noting that `- ` is a CommonMark list marker,
    so each line still renders correctly under graceful degradation
    (per `spec/processing-model.md` — no specific section needed; the
    fallback behavior is the document's general topic).
  - One closing cross-reference: "See `references/examples.md` for
    scenario tables that use this convention."
- Do not introduce new directives, syntax, or rules. This is a
  readability technique, not a feature.

**Patterns to follow:** existing `### Cell Content Dedent` section
shape (heading → short prose → fenced before/after pair → closing
prose); fenced ` ```markdown ` blocks for the examples.

**Test scenarios:** Test expectation: none -- pure prose addition, no
behavior change. Validation covered by U5.

**Verification:**

- A new `### List markers in multi-line cells` subsection exists
  between "Cell Content Dedent" and "Basic Example".
- The subsection contains at least one before/after pair.
- The cross-reference to `references/examples.md` exists.
- The graceful-degradation note appears.

---

### U3. Update `SKILL.md` multiline-table summary

**Goal:** Rewrite the one-sentence summary at `SKILL.md` line 248 to
lead with the three-way distinction without leaking the full rules
into SKILL.md.

**Requirements:** R2.

**Dependencies:** U1 must define the canonical phrasing first; the
SKILL.md summary should be a one-to-two-sentence compression of the
same triple. Authoring U1 before U3 keeps the wording consistent.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
  (modify — replace the first clause of line 248; keep the rest of the
  paragraph intact)

**Approach:**

- Keep the paragraph's existing position (immediately under the
  multiline-table syntax example, before the `**Extensions in cells:**`
  paragraph).
- Replace the first clause "Empty first cell continues previous row; a
  row with pipes and whitespace-only cells separates rows" with one of
  the form: "Each multiline-table row continues the previous logical
  row when its first cell is empty; a row where every cell is
  whitespace is a row separator". The exact final wording is decided
  during authoring; the constraint is that it must (a) name the three
  cases — continuation, separator, blank-line-ends-table — and (b) fit
  in the same one-to-two-sentence budget as today.
- Keep the existing subordinate clause "a blank line ends the table"
  verbatim — it is the failure mode the issue reports.
- Keep the existing closing sentence "Combine with style: `<!-- 
  style:DataTable ; multiline -->`. See `references/syntax-reference.md`
  for multiline table rules."
- Do not touch the `**Extensions in cells:**` paragraph that follows.

**Patterns to follow:** existing SKILL.md prose style (terse, sentence-
fragment-bullet-style continuations); existing cross-reference to
`references/syntax-reference.md`.

**Test scenarios:** Test expectation: none -- pure prose edit. The
acceptance check is in U5's manual auto-activation re-verify and
KTD-3's failure-mode probe (a first-time AI author asked for a
multi-row multiline table no longer emits no-pipe blank lines between
records).

**Verification:**

- Line 248 names all three cases (continuation, separator, blank-line-
  ends-table).
- Line 248 is no longer than two sentences.
- The cross-reference to `references/syntax-reference.md` and the
  combined-style example are retained.

---

### U4. Sweep adjacent legacy phrasings (`best-practices.md`, `examples.md`, `examples/multiline-tables.md`)

**Goal:** Bring three adjacent surfaces in line with the U1/U3 phrasing
so they do not read as drift and so the next contributor cannot copy-
paste the old phrasing back in.

**Requirements:** R4.

**Dependencies:** U1 and U3 must land first (in the same PR) so the
canonical phrasing exists to mirror.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
  (modify — line 278 bullet)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md`
  (modify — line 216 intro prose, tables unchanged)
- `examples/multiline-tables.md`
  (modify — line 29 trailing prose, tables unchanged)

**Approach:**

- **best-practices.md line 278.** Replace the bullet
  "Continuation rows use empty first cell (`|      |`)" with a one-line
  bullet that names the trigger triple in compressed form — e.g.,
  "Continuation rows have an empty first cell; row separators have
  whitespace-only cells; a no-pipe blank line ends the table." Keep
  the surrounding bullets (the row-separator bullet at line 279) intact;
  consider whether they should be merged into the new bullet or kept
  separate during authoring.
- **examples.md line 216.** Replace the intro prose "Each row uses
  continuation lines (empty first cell) and is separated by a row with
  pipes and whitespace-only cells. A completely blank line ends the
  table." with prose that names the three triggers in the same order
  as U1 — e.g., "Each logical row may span multiple physical lines:
  continuation rows (empty first cell) extend the preceding row, and
  row separators (pipes with whitespace-only cells) delimit logical
  rows. A no-pipe blank line ends the table entirely."
- **examples/multiline-tables.md line 29.** Replace the trailing
  one-sentence explanation "Continuation rows (empty first cell)
  extend a logical row across multiple physical lines. Separator rows
  (pipes with whitespace-only cells) mark row boundaries. A completely
  blank line ends the table." with the matching three-way phrasing.
  Do not touch the table data above or below.

**Patterns to follow:** existing prose voice on each surface
(bullet-terse in best-practices, paragraph-prose in examples, single-
sentence-explainer in `examples/multiline-tables.md`).

**Test scenarios:** Test expectation: none -- pure prose edits. R5
validation in U5 covers regressions.

**Verification:**

- A grep for "empty first cell continues" against the repo returns
  zero hits in `references/`, `examples/`, and `SKILL.md`.
- Remaining mentions of "empty first cell" describe it as a *property*
  of a continuation row, never as the *cause* of continuation.
- No table data was changed in `references/examples.md` or
  `examples/multiline-tables.md`.

---

### U5. Validation pass

**Goal:** Confirm the prose changes do not introduce MDPP diagnostics
or break auto-activation, and that example tables still render
correctly under graceful degradation.

**Requirements:** R5.

**Dependencies:** U1, U2, U3, U4.

**Files:**

- Read-only: all files modified in U1-U4 plus
  `docs/brainstorms/2026-05-13-multiline-row-continuation-docs-requirements.md`
- Read-only: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`

**Approach:**

- Run `python scripts/validate-mdpp.py` against each file modified in
  U1-U4 and the brainstorm doc itself. Expect zero new diagnostics —
  baseline diagnostics on these files (if any) must remain unchanged.
- Re-run the manual auto-activation suite at
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`.
  None of the cases describe row-continuation language directly, but
  the routing layer should still pick these files up as Markdown++ on
  the strength of unchanged signals (frontmatter `mdpp-version:`, the
  `<!-- multiline -->` directive in examples, etc.). Record any
  routing regression as a blocker.
- Visually verify that the example tables in
  `references/examples.md` and `examples/multiline-tables.md` still
  render under graceful degradation (open in a CommonMark renderer
  and confirm the tables are readable as plain CommonMark). No
  example body changed; this is a defense-in-depth check that prose
  edits did not accidentally bleed into adjacent table syntax.

**Test scenarios:** Test expectation: none -- this unit *is* the
validation. The acceptance is "validate-mdpp clean, auto-activation
unchanged, render unchanged."

**Verification:**

- `validate-mdpp.py` exits clean on every modified file.
- Auto-activation suite still routes each modified file as Markdown++.
- Tables in `references/examples.md` and `examples/multiline-tables.md`
  render correctly under graceful degradation.

---

### U6. Patch version bump and CHANGELOG entry

**Goal:** Bump the plugin version per repo convention and record a
single-line CHANGELOG entry capturing the doc clarification.

**Requirements:** R-bump.

**Dependencies:** U1-U4 (changes must exist before bumping). U5 should
land first so the bump is not retracted if validation surfaces a
regression.

**Files:**

- `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (modified by
  the bump script)
- `.claude-plugin/marketplace.json` (modified by the bump script)
- `CHANGELOG.md` (modify — add a single entry under the new version
  heading)

**Approach:**

- Run `scripts/bump-version.sh patch` from the repo root. The script
  updates both `plugin.json` and `marketplace.json` to keep versions
  synchronized.
- Add one CHANGELOG entry under the newly created version heading,
  matching the most recent doc-patch entry's shape. Suggested wording:
  "Clarify multiline table row-continuation mechanism: name the three
  structural triggers (row separator, continuation row, new logical
  row) and add a list-marker readability subsection. Closes #92."
- Do not include any other tooling or feature notes — this entry is
  doc-only.

**Test scenarios:** Test expectation: none -- bump script and
CHANGELOG edit. Validation: `plugin.json` and `marketplace.json`
versions match; CHANGELOG has exactly one new entry under the new
version heading.

**Verification:**

- Plugin version in `plugin.json` is one patch higher than at start
  of branch.
- `marketplace.json` version matches `plugin.json`.
- CHANGELOG has one new entry under the new version heading
  referencing #92.

---

## System-Wide Impact

- **Skill consumers (AI authors).** The dominant audience. The whole
  point of the rewrite is that an LLM reading SKILL.md and the syntax
  reference produces correct multiline tables on the first try.
  Auto-activation routing is unchanged; only prose changes.
- **Human contributors.** The Structure Rules rewrite changes the
  mental model from "two parallel row types + a separator" to "three
  triggers in evaluation order." Slight learning-curve cost; long-term
  clarity benefit.
- **Downstream WebWorks docs.** `webworks-claude-skills/markdown-
  integration` and the WebWorks brain repo carry their own copies of
  the legacy phrasing. Those follow this PR; not in scope here. The
  origin doc records this explicitly under Out of Scope.
- **Reference parser (out of repo).** Unaffected. No spec change, no
  behavior change. If the reference parser implements something
  different from §7 (e.g., automatic continuation regardless of first
  cell), Assumption A1 in the origin is wrong and this plan would
  need to flip back to the issue's framing — but that is a spec
  question, not a doc question.

---

## Assumptions

These were inferred during planning without user confirmation in this
headless run. Each carries the corresponding origin assumption forward
and adds plan-time technical inference where applicable.

- **A1 (from origin).** `spec/processing-model.md` §7.b's silence on
  the "content-in-first-cell-mid-table" case means the conventional
  interpretation (start a new logical row) is correct. Every example in
  the repo reinforces this. KTD-1 depends on this being true. If the
  actual reference parser implements "automatic continuation until
  separator", the whole plan flips toward the issue's original framing
  and U1's third bullet is wrong.
- **A2 (from origin).** Issue #92's `Page.asp` and `skin.scss` cells
  are illustrative of the list-marker technique, not a constraint on
  what file types must appear in the rewritten example. U2's
  before/after pair uses syntactically-neutral content.
- **A3 (from origin).** Issues #93 and #99 (declared blockers in the
  issue body) are resolved. Commit `da94357` and the `Recent commits`
  block above confirm #93 is merged via `1ce0c6d`. #99 has not been
  re-verified in this run — the workflow's `blocked-by` automation is
  trusted to have unblocked this issue before dispatch. If #99 added
  spec text that renumbered §7, U1's cross-reference may need
  adjustment at authoring time.
- **A4 (from origin).** The four issue asks split into three doc
  clarifications (R1, R2, R3 + R4 sweep) and one deferred spec
  question (the counter-example with content in continuation-row first
  cells). If the maintainer disagrees and reads the counter-example as
  also a clarification, KTD-1 flips and a separate spec PR is needed.
- **A5 (plan-time).** The bump script is current and idempotent. The
  most recent plan (`docs/plans/2026-05-13-002-...`) used `minor`; this
  plan needs `patch`. No structural changes to the bump script are
  expected.
- **A6 (plan-time).** The existing CHANGELOG.md uses a single-line
  imperative-voice entry style per doc patch. Authoring U6 should
  read the file once and mirror the most recent patch entry's shape
  rather than inventing a new format.

---

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| R1's "new logical row" bullet contradicts the reference parser's actual behavior. | Low — every example in the repo treats first-cell-with-content as a new row. | Spec is silent; this is the conventional reading. If reference parser disagrees, scope flips to a spec PR (deferred follow-up) and this plan is rolled back. |
| Prose rewrites accidentally break the auto-activation routing for `examples/multiline-tables.md`. | Low — frontmatter and `<!-- multiline -->` directive are unchanged. | U5 explicitly re-runs the auto-activation manual suite as a regression gate. |
| Five-surface sweep misses a sixth surface that also carries the legacy phrasing. | Low — origin doc enumerated all known surfaces; brief grep at authoring time confirms. | At U4 authoring time, grep for `empty first cell` and `continues previous row` across the repo. Address any sixth hit in the same PR. |
| Validate-mdpp emits a new MDPP diagnostic on a previously-clean file because of phrasing changes. | Very low — diagnostics are content-shape rules, not prose-content rules. | U5 captures any new diagnostic as a blocker, not an acceptance. |
| The patch bump is wrong because R3's list-marker subsection counts as a new feature. | Low — list markers are a CommonMark readability convention, not a new directive or rule. | KTD-6 documents the patch rationale. If reviewer reads R3 as a new feature, escalate to `minor` at PR time; not a blocker. |

---

## Verification Strategy

This plan ships when, in order:

1. U1-U4 prose edits are committed and reviewable as a single diff per
   file.
2. U5 validation pass is clean: `validate-mdpp.py` reports no new
   diagnostics; auto-activation manual suite passes; example-table
   render unchanged under graceful degradation.
3. U6 bumps the version and records a CHANGELOG entry referencing #92.
4. The single acceptance probe holds: a first-time AI author asked to
   write a multi-row multiline table from `SKILL.md` alone produces a
   table whose record separation uses pipe-delimited whitespace-only
   rows, not no-pipe blank lines. Manual probe; the issue's failure
   mode is the success metric.

---

## Sequencing

U1 → U3 → U4 → U2 → U5 → U6.

- U1 first because it defines the canonical phrasing the SKILL.md
  summary (U3) and the three sweep surfaces (U4) compress or mirror.
- U3 before U4 so the skill's top-level summary is consistent before
  the adjacent surfaces are aligned to match.
- U4 before U2 so all prose edits are landed before the new subsection
  is added — keeps PR diff coherent (rewrites first, additions
  second).
- U2 can in principle ship independently; bundling it here gives the
  PR a single "multiline-table doc clarification" theme.
- U5 last among edits — validation gate.
- U6 absolutely last — version bump is the publish action.

All units land in a single PR.

---

## Origin Document Trace

| Origin section | Plan coverage |
|----------------|---------------|
| Problem Frame | Problem Frame section (above). |
| Out of Scope | Scope Boundaries → Outside this product's identity and Deferred to Follow-Up Work. |
| R1 | U1 (rewrite Structure Rules); KTD-1, KTD-2, KTD-3. |
| R2 | U3 (SKILL.md summary). |
| R3 | U2 (list-marker subsection); KTD-5. |
| R4 | U4 (sweep adjacent phrasings). |
| R5 | U5 (validation pass). |
| Assumptions A1-A4 | Carried forward verbatim into Assumptions section above. |
| Success Criteria | Verification Strategy + per-unit Verification fields. |
| Dependencies | None on other in-flight workstreams (origin); this plan inherits that. |
| Handoff Notes | KTD-6 (patch bump); U6 (bump + CHANGELOG); single-PR target. |
