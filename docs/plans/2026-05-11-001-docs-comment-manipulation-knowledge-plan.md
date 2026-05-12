---
date: 2026-05-11
status: active
plan_type: docs
origin: docs/brainstorms/2026-05-11-comment-manipulation-knowledge-requirements.md
issue: 94
---

# docs: Comment Manipulation Knowledge for the Markdown++ Skill

## Summary

Add a new reference document, `references/comment-manipulation.md`, to the `markdown-plus-plus` skill that captures durable rules for *removing or simplifying* Markdown++ directive comments — the inverse of the authoring guidance the skill already provides. Wire the new doc into `SKILL.md` (references list) and `references/best-practices.md` (cross-reference under "Common Mistakes to Avoid" or "Advanced Patterns"). Bump the plugin to a minor version. No code changes; no spec changes.

The reference codifies which block styles, inline styles, and anchors can be safely removed or reduced when standard Markdown structure or formatting already conveys the same meaning, plus the table-cell edge cases that make these edits non-trivial. Consumer repos (notably `epublisher-docs`) keep their existing scripts; this doc becomes the canonical reference those scripts implement.

---

## Problem Frame

The skill today is strong on the authoring direction — how to *write* a `<!--style:Name-->` directive, attach an alias, place a marker. It is silent on the inverse: when a Markdown++ document carries directives that are redundant (the common output of a one-time migration from FrameMaker, DITA, or another source format), how does an author or AI agent safely remove or simplify them without breaking document structure?

The `epublisher-docs` Phase II style-cleanup work surfaced this gap. Migrated documents arrived dense with style comments like `<!--style:BodyText-->`, `<!--style:Heading1-->`, `<!--style:CellBullet-->` that added no information beyond what the markdown structure already encoded. The rules for safe cleanup are non-obvious:

- **Some directives are redundant** (a `<!--style:BodyText-->` over a paragraph that's just a paragraph), **some are reducible** (`<!--style:ChapterTitle-->` → `<!--style:Title-->`), and **some carry semantic value that markdown cannot express** (`<!--style:Note-->`, `<!--style:Warning-->`, definition-list terms, procedure titles).
- **Table cells make removal hard.** Cell width must be preserved, escaped pipes (`\|`) must not be treated as boundaries, and removing a directive from one cell in a multiline-table row can leave that cell empty while others stay full — requiring partial-cell or bare-list-marker merges from the next physical line.
- **Anchors have their own rules.** An anchor on a heading is durable structure; an anchor *not* on a heading is usually a leftover that can be removed. Combined commands carrying both a style and an anchor must be decomposed correctly.
- **The detection patterns are subtle.** A naive regex that strips `<!-- style:... -->` misfires on combined commands, cross-cell coexistence (style in one cell, anchor in another), and underline-style headings (`===` / `---`) where the heading check requires reading the *next* line.

Without this knowledge captured in the skill, every cleanup effort in every consumer repo has to rediscover the rules from scratch — and AI agents authoring or editing Markdown++ have no guidance for the cleanup half of the document lifecycle.

---

## Requirements Traceability

This plan implements the requirements in `docs/brainstorms/2026-05-11-comment-manipulation-knowledge-requirements.md`. The full R1–R22 enumeration lives in the origin document; this section names the implementation units that cover each cluster.

| Origin requirements | Topic                                      | Implementation unit |
|---------------------|--------------------------------------------|---------------------|
| R1                  | New reference doc exists with frontmatter  | U1                  |
| R4–R8               | Block/inline removal and reduction rules   | U1                  |
| R9–R11              | Anchor decision table and edge cases       | U1                  |
| R12–R16             | Table-cell preservation rules              | U1                  |
| R17–R19             | Detection patterns and companion logic     | U1                  |
| R20–R22             | `epublisher-docs` cross-references         | U1                  |
| R2                  | SKILL.md references-list pointer           | U2                  |
| R3                  | best-practices.md cross-reference          | U3                  |

Acceptance examples AE1–AE8 from the origin document map to test scenarios on U1, U2, and U3.

---

## Key Technical Decisions

The brainstorm document deferred five editorial choices to planning. Each is resolved here with rationale.

### D1. SKILL.md pointer is a one-line bullet in `<references>`; no separate prose section in the body

The minimal version (one bullet) wins for two reasons. First, the skill description already includes a comprehensive trigger list for all extension types; adding a "cleanup" prose section would either duplicate that list or fragment the authoring story. Second, `references/best-practices.md` is the natural in-flow surface where an author working on a real document encounters the cleanup guidance — discoverability flows through the existing references list and the best-practices cross-reference (D2), not a parallel SKILL.md section. *Affects: R2.*

### D2. best-practices.md cross-reference lives under "Common Mistakes to Avoid", attached to the Attachment Rule mistake (#1)

The Attachment Rule mistake at `references/best-practices.md:425` is the densest concentration of authoring-vs-removal collisions in the file: stacked tags, blank-line breaks, mis-attached aliases. A brief cross-reference there ("If you're removing directives rather than authoring them, see `comment-manipulation.md` for safe-removal rules and the table-cell edge cases that make hand-removal error-prone.") is where readers encountering removal-shaped problems are most likely to land. *Affects: R3.*

### D3. Illustrative style-name lists from the issue are reproduced verbatim, with an explicit "illustrative, not canonical" caveat

Self-containedness wins over brevity. Consumers approaching this doc want a usable rule set, not a pointer to an external issue tracker. Reproducing the full lists (block-removable, reducible, inline-removable, keep-by-default) makes the doc usable as a reference without bouncing to GitHub. The caveat — that these names are FrameMaker/ePublisher conventions and consumers with different style families apply the same *principle* to their own names — is restated at each list. *Affects: R5, R6, R7, R8.*

### D4. Detection regex patterns appear as fenced code blocks with explicit caveats

Tool authors implementing cleanup in a new language need real regex to start from, not prose paraphrase. The patterns appear in fenced code blocks. Each is annotated: "starting point, not production-ready", "requires companion logic for [specific case]", and "does not replace `spec/formal-grammar.md`". The caveats are inline next to the patterns, not buried in a footer. *Affects: R17, R18, R19.*

### D5. `epublisher-docs` cross-references live in a single end-of-doc section, not interleaved per-rule

End-of-doc placement keeps the rule body language-agnostic. A re-implementer in JavaScript or Ruby reads the rules without Python script names cluttering each subsection. The single "Reference Implementation" section names the five scripts and the helper-function inventory of `markdown_table_utils.py`, with the stated caveat that those scripts live in a separate repository and may evolve independently. *Affects: R20, R21, R22.*

### D6. Anchor decision table is the primary form; no Mermaid flowchart

The 2×2 (standalone vs combined × heading vs not-heading) maps cleanly to a small Markdown table. Mermaid would add visual weight without clarifying the four cells. Prose elaboration after the table covers the two cross-cutting edge cases (underline-style headings, cross-cell detection) that don't fit the table shape. *Affects: R9.*

### D7. Version bump is **minor** (1.3.0 → 1.4.0)

Per the project's version-bump policy in `CLAUDE.md`: *minor* is "new skills, new features, enhancements". Adding a substantial new reference document that materially expands the skill's coverage from authoring-only to authoring-plus-cleanup is an enhancement. A patch bump would understate the addition. *Affects: U4.*

---

## Output Structure

The plan modifies or adds the following files. All paths are relative to the repository root.

```
plugins/markdown-plus-plus/
├── .claude-plugin/
│   └── plugin.json                          # MODIFY: version bump 1.3.0 -> 1.4.0
└── skills/
    └── markdown-plus-plus/
        ├── SKILL.md                         # MODIFY: add bullet in <references>
        └── references/
            ├── best-practices.md            # MODIFY: cross-reference in Common Mistakes
            └── comment-manipulation.md      # CREATE: new reference doc
.claude-plugin/
└── marketplace.json                         # MODIFY: version bump 1.3.0 -> 1.4.0 (via bump script)
```

The new reference doc follows the same structural shape as `references/table-formatting.md`: YAML frontmatter (`date`, `status: active`), narrative prose, worked fenced-code examples, a "See Also" section.

---

## High-Level Technical Design

*This sketch communicates the intended section layout of the new reference document. It is directional guidance for review, not implementation specification — the implementer should adjust ordering, depth, and section names when writing produces a cleaner shape.*

```
references/comment-manipulation.md  (section outline)
================================================================

1. Frontmatter (date, status: active)
2. # Markdown++ Comment Manipulation
3. ## When to Use This Reference
       Migration / cleanup contexts; pointer to best-practices.md for
       authoring; explicit non-goal: not a spec change.
4. ## The Core Principle
       Redundant vs semantic distinction. The durable rule that drives
       every removal decision.
5. ## Removing Block Style Comments
       5.1 Illustrative removable families (verbatim list per D3)
       5.2 Worked example: <!--style:BodyText--> over a paragraph
       5.3 Caveat: principle, not name list, is the durable rule
6. ## Reducing Block Style Comments
       6.1 Illustrative reducible families with -> mappings
       6.2 Worked example: ChapterTitle -> Title
       6.3 Worked example: NoteIndent2 -> Note
7. ## Removing Inline Style Comments
       7.1 Markdown-token pairings (GUIControl + **bold**, etc.)
       7.2 Worked example: <!--style:GUIControl-->**Settings**
8. ## Keep-by-Default Semantic Styles
       8.1 Note, Warning, definition-list family, procedure titles,
           titles, IfClause, NewTerm, API_* families
       8.2 Rationale per family (what semantic distinction is lost on
           removal)
9. ## Anchor Handling
       9.1 Decision table (2x2: standalone vs combined x heading vs
           not-heading) per D6
       9.2 Underline-style heading edge case (=== / ---)
       9.3 Cross-cell detection edge case (style in cell A, anchor in
           cell B)
10. ## Table-Cell Edge Cases
        10.1 Cell-width preservation (trailing whitespace)
        10.2 Escaped pipes (\| is content)
        10.3 Multiline row boundaries (empty-separator row convention)
        10.4 Partial-cell merge (one empty cell, not whole row)
        10.5 Bare-list-marker merge (- with no content)
        10.6 Cross-references to table-formatting.md
11. ## Detection Patterns
        11.1 Style-comment regex (fenced, with caveats per D4)
        11.2 Standalone-anchor regex (fenced, with caveats per D4)
        11.3 Companion logic checklist (cross-cell, unclosed comment,
             multiline boundary, partial merge, bare marker)
12. ## Reference Implementation
        12.1 Five epublisher-docs scripts with one-sentence roles
        12.2 markdown_table_utils.py helper inventory (six functions
             named with one-sentence descriptions each)
        12.3 Stability caveat: separate repo, may evolve independently
13. ## See Also
        Cross-references to best-practices.md, table-formatting.md,
        spec/multiline-cell-extensions.md, spec/attachment-rule.md.
```

The doc is long — 350–500 lines is the expected ballpark, comparable to `references/table-formatting.md` (382 lines) and `references/best-practices.md` (642 lines). Reproducing the illustrative lists verbatim per D3 drives most of that length; the worked examples drive the rest.

---

## Implementation Units

### U1. Create `references/comment-manipulation.md`

**Goal.** Produce the new reference document covering the eleven topic sections in the high-level design above, embodying decisions D1–D6.

**Requirements.** R1, R4–R22.

**Dependencies.** None — this is the foundation. U2 and U3 reference this file.

**Files.**
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`

**Approach.**

- Open with YAML frontmatter (`date: 2026-05-11`, `status: active`) — the same shape every other reference in the directory uses.
- Lead with a one-paragraph "When to Use This Reference" framing that positions the doc as cleanup/migration guidance, distinct from the authoring guidance in `best-practices.md`. Make explicit that this is not a spec change.
- State the **Core Principle** before any list: a style comment whose name maps 1:1 to a markdown structural element (paragraph, heading level, bullet list, ordered list, code block, table cell) is redundant; a style comment that carries semantic distinction the markdown structure cannot express (callout type, definition-list role, procedure step, table title, figure title, API category, inline semantic role) is not redundant and must be preserved. Every subsequent rule derives from this principle.
- Reproduce the illustrative style-name lists verbatim from the origin document (R5: removable block, R6: reducible, R7: inline removable, R8: keep-by-default). After each list, restate the "illustrative, not canonical — apply the principle to your own style families" caveat per D3.
- Anchor handling uses a Markdown table (2×2) per D6:

  ```
  | Context                                  | Action                            |
  |------------------------------------------|-----------------------------------|
  | Standalone anchor on a heading           | Keep                              |
  | Combined (style + anchor) on a heading   | Keep the anchor; remove the style |
  | Standalone anchor not on a heading       | Remove                            |
  | Combined (style + anchor) not on heading | Remove the whole comment          |
  ```

  Follow with two prose subsections: the underline-style heading edge case (R10 — check `===` or `---` on next line) and the cross-cell detection edge case (R11 — style comment in cell A coexists with anchor in cell B; evaluate independently).

- Table-cell edge cases (R12–R16) get one short subsection each with a fenced before/after example. Cross-reference `table-formatting.md` for the escaped-pipe rule (it appears in both docs because both need it).
- Detection patterns (R17–R19) appear in fenced code blocks per D4:

  ```python
  # Style comment with optional anchor:
  r'<!--\s*style:\s*([^;>]+?)(?:\s*;\s*(#[^>]+))?\s*-->'

  # Standalone anchor (NOT inside a style comment — see companion logic):
  r'<!--\s*(#[a-zA-Z0-9_-]+)\s*-->'
  ```

  Annotate each with: starting point for tool authors, companion-logic requirements, "does not replace `spec/formal-grammar.md`".

- Reference Implementation section (R20–R22) is end-of-doc per D5, naming:
  - `detect-removable-block-styles.py` — remove semantic-free block styles
  - `detect-reducible-styles.py` — simplify style names to base forms
  - `detect-removable-anchors.py` — remove non-heading anchors
  - `detect-removable-inline-styles.py` — remove inline styles where markdown suffices
  - `markdown_table_utils.py` — shared library for table-cell manipulation

  Then the helper-function inventory: `find_unescaped_pipe`, `replace_in_table_cell`, `is_table_line_empty`, `is_bare_list_marker`, `handle_table_line_after_removal`, `merge_table_line_up`. One sentence each. Conclude with the caveat: scripts live in a separate repository, may evolve independently; this doc is source of truth for *behavior*, the scripts for *implementation in that repo*.

- "See Also" footer cross-references: `best-practices.md`, `table-formatting.md`, `../../../../spec/multiline-cell-extensions.md`, `../../../../spec/attachment-rule.md`. Use the same relative-path depth the existing references use.

**Patterns to follow.**
- Frontmatter and section shape: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md` (the most recent reference doc, same style as this one will use).
- Worked-example density: `references/best-practices.md` (do/don't snippets with brief context).
- Cross-reference path style: every existing `references/*.md` file uses `../../../../spec/...` for spec cross-references; match that depth.
- Decision-table shape: the table style in `references/best-practices.md` Variable Naming Conventions (line 395+) and Style Naming Conventions (line 414+).

**Test scenarios.**

The reference doc is a static text document, so "test scenarios" here mean readability and self-sufficiency checks the implementer (or a reviewer) can run against the rendered doc:

- Covers AE1, R4, R5, R8. Given a paragraph in a sample document carrying `<!--style:BodyText-->`, a reader using only this doc can decide it is removable; given a blockquote carrying `<!--style:Note-->`, a reader using only this doc can decide it is *not* removable. Verify both decisions are reachable from the Core Principle plus the relevant lists.
- Covers AE2, R6. The reducible-style section explicitly walks through `<!--style:ChapterTitle-->` → `<!--style:Title-->` and `<!--style:NoteIndent2-->` → `<!--style:Note-->` as worked examples.
- Covers AE3, R7. The inline-removal section walks through `This is the <!--style:GUIControl-->**Settings** button.` and shows the removal output.
- Covers AE4, R9, R10, R11. The anchor section's decision table is the primary form; each of the four cells has a one-line worked example below the table or in the prose subsections that follow.
- Covers AE5, R12, R13, R14, R15, R16. The table-cell edge cases section has at least one fenced before/after illustration per rule (five rules, five illustrations minimum). The partial-cell merge and bare-list-marker merge examples explicitly show "next physical line content moves up into the empty cell".
- Covers AE6, R17, R18, R19. The detection patterns appear as fenced code blocks with the "illustrative, not normative" caveat adjacent to the patterns and a one-paragraph companion-logic checklist following.
- Covers AE7, R20, R21, R22. The Reference Implementation section names all five scripts and all six helper functions with one-sentence roles.
- Readability check: run `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md` (or whichever invocation the repo uses) and confirm no MDPP errors. The doc itself is plain Markdown plus frontmatter; no Markdown++ directives are used inside.
- Idempotent table-formatting check: if the doc contains any data tables (the anchor decision table, the script-list table), run `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py <path> --check`; the file should already be in the formatter's idempotent output shape.

**Verification.**
- File exists at the expected path with the expected frontmatter.
- All eight acceptance examples (AE1–AE8) are demonstrably reachable from the doc's body without external context.
- `validate-mdpp.py` reports no errors on the new file.
- `format-tables.py --check` exits 0 on the new file.
- Word count and section count are in the 350–500-line ballpark; significantly shorter likely means a rule cluster was dropped, significantly longer likely means a section grew implementation guidance that belongs in `epublisher-docs`.

---

### U2. Update `SKILL.md` references list

**Goal.** Add a one-line bullet in the `<references>` section pointing readers from the skill entry point to the new doc.

**Requirements.** R2.

**Dependencies.** U1 (the file must exist before SKILL.md points to it).

**Files.**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`

**Approach.**

- In the `<references>` section (currently around line 335–354), add one bullet after the existing `references/table-formatting.md` entry. Match the existing bullet style exactly (`- `references/comment-manipulation.md` - <one-line description>`).
- Suggested description: `Rules for safely removing or simplifying Markdown++ directive comments during cleanup or migration`. Keep it parallel to the other entries (each is a noun phrase, no terminal period).
- Do not add a separate prose section in the body — per D1, the bullet plus the best-practices cross-reference are sufficient discoverability surfaces.
- Do not reorder the existing references list. Insert the new bullet after `references/table-formatting.md` (its closest topical sibling — both are recent additions covering directive-adjacent rules).

**Patterns to follow.**
- Existing bullets in the same `<references>` block at `SKILL.md:339–353` (style, punctuation, capitalization).

**Test scenarios.**
- Covers AE8, R2. Read `SKILL.md` from the top; verify the new bullet is visible in the references list and the description states the doc's role.
- Insertion order check: the new bullet sits next to `table-formatting.md`, not at the top or bottom of the list.
- No other content in `SKILL.md` is modified.

**Verification.**
- Diff to `SKILL.md` is exactly one inserted line.
- The link target resolves (the file from U1 exists).

---

### U3. Cross-reference from `references/best-practices.md`

**Goal.** Add a brief cross-reference from the in-flow authoring-guidance file to the new cleanup doc, so authors encountering removal-shaped problems land in the right place.

**Requirements.** R3.

**Dependencies.** U1 (target must exist).

**Files.**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`

**Approach.**

- Per D2, attach the cross-reference to Common Mistake #1 (Attachment Rule), the densest concentration of authoring-vs-removal collisions in the file.
- After the existing Attachment Rule mistake content but before the next numbered mistake (#2 Missing Semicolons), add a brief subsection — one short paragraph, no new heading level. Suggested text:

  > **Removing rather than authoring directives?** Cleanup edits (removing redundant `<!--style:-->` comments, simplifying style names, deleting non-heading anchors) follow a different rule set than authoring. See [`comment-manipulation.md`](comment-manipulation.md) for the safe-removal rules and the table-cell edge cases that make hand-removal error-prone.

- Do not add a separate top-level section. The point is a pointer, not a parallel narrative.
- Do not modify any other section of `best-practices.md`.

**Patterns to follow.**
- Existing cross-references in `best-practices.md`: the "Table Formatting" section (around line 282) cross-references `table-formatting.md` with a similar two-sentence framing. Match that voice.

**Test scenarios.**
- Covers AE8, R3. Read `best-practices.md` from "Common Mistakes to Avoid" forward; verify the cross-reference appears in or adjacent to Mistake #1 and the link target resolves.
- Diff size: one paragraph added, no other changes.
- The cross-reference does not duplicate content from `comment-manipulation.md`; it is a pointer, not a summary.

**Verification.**
- The link `[comment-manipulation.md](comment-manipulation.md)` resolves to the file created in U1.
- No other content in `best-practices.md` is modified.

---

### U4. Bump plugin version to 1.4.0

**Goal.** Bump the plugin from 1.3.0 to 1.4.0 to reflect the new reference doc, per the project's version policy in `CLAUDE.md`.

**Requirements.** Project version-management policy (not an R-ID from the origin doc, but required by repo convention before PR).

**Dependencies.** U1, U2, U3 (the version bump should be the last commit-adjacent step, capturing the full set of changes).

**Files.**
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json` (kept in sync by the bump script)

**Approach.**

- Per D7, run `scripts/bump-version.sh minor`. This is the canonical way to bump both `plugin.json` and `marketplace.json` together; manual edits would risk version drift between the two files.
- Confirm the script's output is the expected `1.3.0 -> 1.4.0`.
- The bump should be included in the same commit (or commit series) as the U1/U2/U3 changes — the brainstorm-issue-94 work is one logical unit.

**Patterns to follow.**
- `CLAUDE.md` Version Management section: `minor` is reserved for "new skills, new features, enhancements". A new reference document that expands the skill's coverage qualifies.

**Test scenarios.**
- Test expectation: none — pure version bump produced by an existing tool. Verification is "the two version strings now read `1.4.0` and the bump script exited cleanly".

**Verification.**
- `grep '"version"' plugins/markdown-plus-plus/.claude-plugin/plugin.json` shows `"1.4.0"`.
- `grep '"version"' .claude-plugin/marketplace.json` shows `"1.4.0"`.
- No other files modified by the bump script.

---

## Scope Boundaries

### In Scope
- One new reference document at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`.
- One bullet added to `SKILL.md`'s references list.
- One paragraph added to `references/best-practices.md`'s Common Mistakes section.
- Plugin minor version bump.

### Out of Scope (carried from origin)
- **Shipping a cleanup script in this repo.** The `epublisher-docs` Phase II scripts already exist and serve their consumer; this repo's role is to document the durable knowledge, not duplicate the implementation.
- **Curating a complete style taxonomy.** The illustrative style-name lists are FrameMaker/ePublisher conventions presented as concrete examples. Other consumers apply the same principle to their own style families.
- **Changes to the Markdown++ spec.** Cleanup rules are authoring guidance, not syntax. Nothing in `spec/` is modified.
- **A generic Markdown++ refactor engine.** The doc names patterns and edge cases; it does not propose a unified refactoring abstraction.
- **Pasting `epublisher-docs` script code into this repo.** Cross-references name files and key helpers; they do not reproduce implementation.
- **SKILL.md restructuring.** Only one bullet is added; existing sections are not reorganized.
- **Validation tooling that flags removable directives.** The doc enumerates rules a tool *could* implement; no `validate-mdpp.py` extension or new MDPP error code is proposed.

### Deferred to Follow-Up Work
- *(none — the work is bounded and ships as a single PR)*

---

## Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Reference doc becomes outdated as `epublisher-docs` scripts evolve in their own repo | Medium | Low | The doc's stability caveat in the Reference Implementation section explicitly states the scripts may evolve independently and this doc is source of truth for behavior, not implementation. No code is duplicated. |
| Doc length (350–500 lines) exceeds reader patience | Low | Low | Section structure mirrors `table-formatting.md` (which is similar length) and reads top-down: principle → rules → edge cases → patterns → reference implementation. Readers can jump to the section matching their cleanup task. |
| Illustrative regex patterns get copied into production tools without companion logic | Low | Medium | Each pattern carries inline caveats per D4. The companion-logic checklist (R18 + cross-cell + multiline boundary + partial merge + bare marker) appears adjacent to the patterns. |
| Cross-cell detection edge case (R11) is missed by reviewers as "an edge case" rather than a first-class rule | Low | Low | R11 is presented in the anchor section's main prose, not in a footnote. The brainstorm flagged this as a first-class rule (Key Decisions item 5 in the origin) because it is one of the most commonly missed cases. |
| Doc drifts from `best-practices.md` and `table-formatting.md` over time (shared rules like escaped pipes appear in both) | Medium | Low | The escaped-pipe rule (R13) explicitly cross-references `table-formatting.md` rather than restating. The "See Also" footer links the three docs. Any future change to the shared rule should be reviewed against all three docs. |

---

## System-Wide Impact

- **Plugin consumers:** A future install of `markdown-plus-plus` v1.4.0 gets the new reference automatically. No breaking changes.
- **AI agents using the skill:** Future authoring sessions on Markdown++ documents have cleanup guidance available alongside authoring guidance. No change to how the skill auto-activates (the reference is loaded when the skill is loaded; no new signal triggers it).
- **`epublisher-docs` repo:** No code changes in this repo. The `epublisher-docs` scripts continue to operate as before; this doc becomes the canonical reference *they* implement, but the implementation lives there.
- **Spec authors:** No spec change. The doc is reference material for authors and tool authors; it does not change syntax, grammar, or validation behavior.
- **Validation tooling:** `validate-mdpp.py` is unchanged. No new MDPP error code is introduced.

---

## Documentation Plan

- The new reference doc *is* the documentation deliverable; no further docs are needed.
- `CHANGELOG.md` gains an entry under the next version section (1.4.0) describing the addition: "Added `references/comment-manipulation.md`: durable rules for safely removing or simplifying Markdown++ directive comments during cleanup or migration."
- No release notes, blog post, or migration guide are required — this is an additive documentation change.

---

## Open Implementation-Time Questions

These are knowable only when writing the doc and may require small judgment calls from the implementer; they are not blockers.

- Whether the worked example for the partial-cell merge rule (R15) uses a two-column or three-column table. Pick whichever produces the clearest before/after; three-column may better show "only one cell empties while the others stay full".
- Exact phrasing of the "illustrative, not canonical" caveat. Should appear after each major style-name list with consistent wording but does not need to be identical verbatim each time.
- Whether the companion-logic checklist (after the detection patterns) is a bulleted list or a numbered list. Prefer the shape that better matches surrounding `references/*.md` conventions.

---

## See Also

- **Origin document:** [`docs/brainstorms/2026-05-11-comment-manipulation-knowledge-requirements.md`](../brainstorms/2026-05-11-comment-manipulation-knowledge-requirements.md)
- **Sibling reference doc (shape model):** [`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md)
- **Skill entry point:** [`plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md)
- **Version-bump policy:** `CLAUDE.md` § Version Management
