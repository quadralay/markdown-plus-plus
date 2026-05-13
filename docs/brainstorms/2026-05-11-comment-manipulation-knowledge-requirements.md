---
date: 2026-05-11
status: active
topic: comment-manipulation-knowledge
---

# Comment Manipulation Knowledge for the Markdown++ Skill

## Summary

Add a new reference document to the `markdown-plus-plus` skill that captures durable knowledge about *removing and modifying* Markdown++ directive comments — the inverse of the authoring guidance the skill already provides. The reference codifies which block styles, inline styles, and anchors can be safely removed or reduced when standard Markdown structure or formatting already conveys the same meaning, plus the table-cell edge cases that make these edits non-trivial. The skill grows the cleanup half of the authoring lifecycle without adding tooling to this repo — consumer repos (notably `epublisher-docs`) keep their existing scripts, and this doc becomes the canonical reference those scripts implement.

---

## Problem Frame

The skill today is strong on the authoring direction: how to *write* a `<!--style:Name-->` block, how to attach an alias to a heading, when to use a marker. It is silent on the inverse: when an existing Markdown++ document carries directives that are redundant — typically the output of a one-time migration from FrameMaker, DITA, or another source format — how does an author safely remove or simplify them without breaking document structure?

The `epublisher-docs` Phase II style-cleanup work surfaced this gap. Migrated documents arrived dense with style comments like `<!--style:BodyText-->`, `<!--style:Heading1-->`, `<!--style:CellBullet-->` that added no information beyond what the markdown structure already encoded. Cleanup is high-value (smaller, more readable source documents that diff cleanly) but the rules are non-obvious:

- **Some directives are redundant** (a `<!--style:BodyText-->` over a paragraph that's just a paragraph), **some are reducible** (`<!--style:ChapterTitle-->` → `<!--style:Title-->` collapses two near-duplicates into one), and **some carry semantic value the markdown structure cannot express** (`<!--style:Note-->`, `<!--style:Warning-->`, definition-list terms, procedure titles).
- **Table cells make removal hard.** Cell width must be preserved (alignment-sensitive). Escaped pipes (`\|`) must not be treated as cell delimiters. Removing a directive from one cell in a multiline-table row can leave that cell empty while others stay full, requiring content from the next line to merge upward. Bare list markers (`- `, `1.`) left behind after directive removal need the same merge treatment.
- **Anchors have their own rules.** An anchor on a heading is durable structure; an anchor *not* on a heading is usually a leftover that can be removed. A combined comment that carries both a style and an anchor must be decomposed correctly when only one of the two should survive.
- **The detection patterns are subtle.** A naive regex that strips `<!-- style:... -->` will misfire on combined commands, on rows where a style comment in one cell coexists with an anchor in another, and on the underline-style headings (`===` / `---` underlining) where the anchor-on-heading check requires looking at the *next* line.

Without this knowledge captured in the skill, every cleanup effort in every consumer repo has to rediscover the rules from scratch — and AI agents authoring or editing Markdown++ have no guidance for the cleanup half of the lifecycle.

---

## Assumptions

*This requirements doc was authored without synchronous user confirmation. The items below are agent inferences that fill gaps in the input — un-validated bets that should be reviewed before planning proceeds.*

- **One new reference document is the right surface.** It lives at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`, sibling of `best-practices.md`, `syntax-reference.md`, and `table-formatting.md`. SKILL.md gains a short pointer paragraph (mirroring how `table-formatting.md` is wired in). `best-practices.md` gains a brief cross-reference in its "Common Mistakes" or "Advanced Patterns" section. Bet: a single dedicated doc keeps the rule set discoverable and avoids fragmenting the cleanup story across three existing references.
- **The specific style-name lists from the issue are illustrative, not canonical.** Names like `BodyText`, `ChapterTitle`, `CellBullet`, `NoteIndent`, `ProcedureStep1` are FrameMaker/ePublisher conventions surfaced by a particular migration toolchain. The reference doc presents them as concrete examples that ground the rules, but states explicitly that the *principle* (a style comment whose name maps 1:1 to a markdown structural element is redundant; a style comment that carries semantic meaning beyond structure is not) is the durable knowledge. Consumer repos with different style families apply the same principle with their own names.
- **The detection regex patterns are illustrative, not normative.** The patterns from the issue (`<!--\s*style:\s*([^;>]+?)(?:\s*;\s*(#[^>]+))?\s*-->` for style+anchor, etc.) appear in the doc as starting points for tool authors with caveats: they don't handle every combined-command order, they require companion logic for "is this anchor inside a style comment in another cell?", and they don't replace the formal Markdown++ grammar in `spec/formal-grammar.md`. They are not added to the spec.
- **The reference doc reproduces the *rules and edge cases*, not the script implementations.** The `epublisher-docs` Phase II scripts (`detect-removable-block-styles.py`, `detect-reducible-styles.py`, `detect-removable-anchors.py`, `detect-removable-inline-styles.py`, `markdown_table_utils.py`) are the canonical implementation; the doc cross-references them with their repo-relative paths and names the key helper functions (`find_unescaped_pipe`, `replace_in_table_cell`, `is_table_line_empty`, `is_bare_list_marker`, `handle_table_line_after_removal`, `merge_table_line_up`) as the algorithmic shapes a re-implementer should follow. No script code is pasted in or duplicated.
- **No cleanup script ships in this repo.** The table-formatting capability shipped `scripts/format-tables.py` because formatting is a write-time concern on every authoring pass. Cleanup is a one-time-per-document migration concern that consumer repos already own. Bet: shipping a cleanup script here would force this repo to also own the consumer-specific style taxonomy that drives it.
- **The anchor decision table is the primary reference shape for anchor handling.** The 2×2 matrix in the issue (standalone vs combined × heading vs not-heading) maps cleanly to a small markdown table; the doc presents it that way with prose elaboration on each cell. The matrix is the canonical form; prose walks through each row.
- **Table-cell edge cases live in the comment-manipulation doc, not the table-formatting doc.** `table-formatting.md` is about producing diff-stable column widths; comment-manipulation is about safely *removing content from cells* while keeping cell boundaries and column widths intact. Both touch table cells but solve different problems. Cross-references go both ways: cleanup operations should leave tables in a state the formatter would consider already formatted.
- **The doc follows the existing reference-doc shape.** YAML frontmatter (`date`, `status: active`), narrative prose with worked examples, code-block snippets for regex and table-cell illustrations. No new file format, no per-rule schema.

---

## Requirements

**Surface and structure**
- R1. A new reference document exists at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/comment-manipulation.md`, with YAML frontmatter declaring `date` and `status: active`.
- R2. SKILL.md gains a short paragraph in the `<references>` section (and, if planning determines it adds value, a brief pointer in the relevant body section) that links to `references/comment-manipulation.md` and states its role: durable rules for safely removing or simplifying directive comments from Markdown++ documents during cleanup or migration.
- R3. `references/best-practices.md` gains a brief cross-reference (within the "Common Mistakes" or "Advanced Patterns" section, whichever planning judges the better fit) pointing to the new doc as the source of truth for cleanup rules.

**Content — removal and reduction rules**
- R4. The doc names the *principle* governing removal: a style comment whose name maps 1:1 to a markdown structural element (paragraph, heading level, bullet list, ordered list, code block, table cell) is redundant — the markdown structure already conveys the same meaning. A style comment that carries semantic distinction the markdown structure cannot express (callout type, definition-list role, procedure step, table title, figure title, API-documentation category, inline semantic role) is not redundant and must be preserved.
- R5. The doc enumerates the illustrative removable block-style families from the issue (`Body`, `Normal`, `Default`, `BodyText`, `BodyIndent`, `Heading1`–`Heading4`, `CellBody`, `CellHeading`, `CellBullet`, `Table Normal`, `TableLines`, `ProcedureStep1`, `ProcedureBullet`, `Bullet`, `Bullet2`, `Code`, `CodeFirst`, `CodeLast`, `CodeSingle`, `Preformatted`, `Anchor`, `AnchorIndent`) with a stated caveat that the list is illustrative — consumer repos apply the underlying principle to their own style families.
- R6. The doc names reducible-style patterns (style families that have a "base form" — e.g., `ChapterTitle` → `Title`, `NoteIndent` / `NoteIndent2` → `Note`, `DefineListDescription` → `DefineListDefinition`, `d_caption` → `FigureTitle`) and the rule that drives reduction: when a family of style names differs only by an indent or layout suffix that the rendering pipeline collapses to the same output, the canonical base form replaces the variants.
- R7. The doc enumerates inline-style removal rules: when a markdown inline-formatting token (`**bold**`, `*italic*`, `` `code` ``) already conveys the directive's meaning, the directive can be removed. Example mappings from the issue: `GUIControl` paired with `**bold**`, `Variable` paired with `*italic*` or `` `code` ``, `FileAndFolder` / `Command` / `Parameter` / `Filename` / `Literal` paired with `` `code` ``, `BookTitle` paired with `*italic*`.
- R8. The doc enumerates the keep-by-default semantic styles from the issue (`Note`, `Warning`, `DefineListTerm`, `DefineListTermDropDown`, `DefineListDefinition`, `ProcedureTitle`, `Title`, `TableTitle`, `FigureTitle`, `IfClause`, `NewTerm`, and all `API_*` styles) with the rationale that each carries semantic distinction beyond what standard Markdown structure expresses.

**Content — anchor handling**
- R9. The doc presents anchor-handling rules as a decision table covering the four cases from the issue:
  | Context | Action |
  |---------|--------|
  | Standalone anchor on a heading | Keep |
  | Combined-command (style + anchor) on a heading | Keep the anchor; remove the style |
  | Standalone anchor not on a heading | Remove |
  | Combined-command (style + anchor) not on a heading | Remove the whole comment |
- R10. The doc names the underline-style heading edge case: anchor-on-heading detection must check both `#`-prefixed headings *and* paragraphs followed by `===` or `---` underlines on the next line.
- R11. The doc names the cross-cell detection edge case: a multiline-table row may have a `<!--style:...-->` directive in one cell and a `<!--#alias-->` anchor in another cell. The two must be evaluated independently — the presence of a style comment somewhere on the line does not change whether the anchor on that same line is removable.

**Content — table-cell preservation**
- R12. The doc names the cell-width preservation rule: when content shortens inside a table cell, trailing whitespace is added to maintain the column's visible width, so the table's pipe-alignment shape stays valid for the formatter (see `table-formatting.md`).
- R13. The doc names the escaped-pipe rule: `\|` inside a cell is literal content, never a cell boundary; any cell-boundary scanner must skip escaped pipes (cross-references the same rule in `table-formatting.md`).
- R14. The doc names the multiline-table row-boundary rule: in a `<!-- multiline -->` table, a row whose cells are all whitespace-only is a logical row separator. Cleanup operations that look "one line ahead" for content to merge upward must respect that boundary.
- R15. The doc names the partial-cell merging rule: when directive removal empties exactly one cell in a row while other cells in the same row remain non-empty, content from the corresponding cell of the next physical line is merged upward into the empty cell — not the whole row.
- R16. The doc names the bare-list-marker rule: when directive removal leaves a cell containing only a list marker (`- `, `* `, `+ `, `1.`, etc.) with no following content, the marker is incomplete and the next physical line's corresponding cell content is merged upward to complete the list item.

**Content — detection patterns**
- R17. The doc reproduces the illustrative regex patterns from the issue for style comments (with optional anchor): `<!--\s*style:\s*([^;>]+?)(?:\s*;\s*(#[^>]+))?\s*-->` and for standalone anchors: `<!--\s*(#[a-zA-Z0-9_-]+)\s*-->`.
- R18. The doc names the companion-logic requirement: standalone-anchor detection must verify the anchor is not inside an unclosed style comment by inspecting the surrounding text (anchors appearing between `<!--` and `-->` of a style comment are part of that comment, not standalone).
- R19. The doc states explicitly that the regex patterns are starting points for tool authors and do not replace `spec/formal-grammar.md`. They illustrate the shape of the problem; production tooling combines them with the companion logic described in R11, R14, R15, R16, and R18.

**Content — reference implementation pointers**
- R20. The doc cross-references the `epublisher-docs` Phase II scripts as the canonical reference implementation, naming each script's purpose:
  - `detect-removable-block-styles.py` — remove semantic-free block styles
  - `detect-reducible-styles.py` — simplify style names to base forms
  - `detect-removable-anchors.py` — remove non-heading anchors
  - `detect-removable-inline-styles.py` — remove inline styles where markdown suffices
  - `markdown_table_utils.py` — shared library for table-cell manipulation
- R21. The doc names the algorithmic shapes encoded in `markdown_table_utils.py` (`find_unescaped_pipe`, `replace_in_table_cell`, `is_table_line_empty`, `is_bare_list_marker`, `handle_table_line_after_removal`, `merge_table_line_up`) as the helper-function inventory a re-implementer should expect to build, with one-sentence descriptions of each.
- R22. Script paths in the cross-reference are repo-relative within the `epublisher-docs` repository (e.g., `.claude/scripts/detect-removable-block-styles.py`), with a stated caveat that those scripts live in a separate repository and may evolve independently — the source of truth for *behavior* is this reference document.

---

## Acceptance Examples

- AE1. **Covers R4, R5, R8.** A reader of the reference doc, presented with a paragraph carrying `<!--style:BodyText-->`, can decide from the doc alone that the directive is removable, and can decide from the same doc that `<!--style:Note-->` on a blockquote is not.
- AE2. **Covers R6.** A reader presented with `<!--style:ChapterTitle-->` over a Title paragraph can decide from the doc alone to reduce it to `<!--style:Title-->`, and a reader presented with `<!--style:NoteIndent2-->` on a blockquote can decide to reduce it to `<!--style:Note-->`.
- AE3. **Covers R7.** A reader presented with `This is the <!--style:GUIControl-->**Settings** button.` can decide from the doc that the directive is removable because `**bold**` already conveys the GUI-control distinction.
- AE4. **Covers R9, R10, R11.** A reader presented with each of the four anchor-handling rows (standalone anchor on heading, combined on heading, standalone not-on-heading, combined not-on-heading) can derive the correct action from the decision table in the doc, and the underline-style-heading and cross-cell cases are explicit prose under the table.
- AE5. **Covers R12, R13, R14, R15, R16.** A reader writing or reviewing a script that removes directives from table cells finds in the doc: (a) a worked example showing trailing-whitespace padding to preserve cell width, (b) the escaped-pipe rule with a one-line example, (c) the multiline row-boundary rule with a before/after example, (d) the partial-cell merge example, and (e) the bare-list-marker merge example. Each rule has at least one fenced-code-block illustration.
- AE6. **Covers R17, R18, R19.** A reader implementing a detection tool finds both regex patterns in the doc, the explicit caveat that they are illustrative, and a one-paragraph description of the companion logic needed for production use.
- AE7. **Covers R20, R21, R22.** A reader looking for the canonical implementation finds a single section listing the five `epublisher-docs` scripts with their roles, the helper-function inventory of `markdown_table_utils.py`, and the caveat that those scripts live in a separate repository.
- AE8. **Covers R2, R3.** A reader entering the skill via SKILL.md sees a pointer to `comment-manipulation.md` in the references list, and a reader entering via `best-practices.md` sees a cross-reference to the same doc.

---

## Success Criteria

- A consumer-repo author starting a new style-cleanup pass in a Markdown++ project (analogous to the `epublisher-docs` Phase II work) can re-derive the rule set from this doc alone, without reading the original Phase II scripts.
- An AI agent editing a Markdown++ document during an authoring session can decide, from the skill's reference content, whether a given directive comment is safe to remove or simplify — without re-discovering the principles from first principles.
- A future contributor to `epublisher-docs` (or any other consumer repo) implementing cleanup logic in a different language than the Phase II Python scripts (e.g., a Node script, a Ruby task, an inline-Claude transformation) has the algorithmic shapes documented in language-agnostic prose rather than tied to the Python implementation.
- The Markdown++ spec is not modified. The new doc is reference material for authors and tool authors; it does not change syntax, grammar, or validation behavior.

---

## Scope Boundaries

- **Out of scope: shipping a cleanup script in this repo.** The `epublisher-docs` Phase II scripts already exist and serve their consumer; this repo's role is to document the durable knowledge those scripts implement, not duplicate them.
- **Out of scope: curating a complete style taxonomy.** The illustrative style-name lists from the issue are presented as examples drawn from one consumer's stationery (FrameMaker/ePublisher migrations). Other consumers have other style families; the doc documents the *principles* by which any consumer decides what's removable.
- **Out of scope: changes to the Markdown++ spec.** Cleanup rules are authoring guidance, not syntax. Nothing in `spec/` is modified by this work.
- **Out of scope: a generic Markdown++ refactor engine.** The doc names patterns and edge cases; it does not propose a unified refactoring abstraction for tools to share.
- **Out of scope: pasting `epublisher-docs` script code into this repo.** Cross-references name the script files and key helper functions; they do not reproduce the implementation. If the `epublisher-docs` scripts evolve, this doc remains the source of truth for *behavior* and the scripts remain the source of truth for *implementation in that repo*.
- **Out of scope: SKILL.md restructuring.** Only a small pointer is added; the `<references>` section grows by one bullet. Existing sections are not reorganized.
- **Out of scope: validation tooling that flags removable directives.** The doc enumerates rules a tool *could* implement; it does not propose a `validate-mdpp.py` extension or a new MDPP error code for "redundant style directive."

---

## Key Decisions

- **One new reference doc (`references/comment-manipulation.md`)** is the right surface, mirroring how `references/table-formatting.md` was wired in. The alternative — folding all this content into `best-practices.md` — would bury cleanup rules inside authoring guidance and inflate that file past its current scope.
- **Knowledge in this repo; tooling in consumer repos.** The issue's reference implementation is Python scripts in `epublisher-docs`. Documenting those scripts here without duplicating them gives consumers a shared rule set while preserving each repo's freedom to implement cleanup in its own toolchain.
- **Illustrative, not normative, examples.** The specific style names (`BodyText`, `ChapterTitle`, `NoteIndent`) are presented as concrete examples that ground the rules. The reference doc states explicitly that the *principle* is the durable knowledge and the specific names are FrameMaker/ePublisher conventions, so consumers with different style families know how to apply the rules to their own names.
- **Anchor handling as a decision table.** The 2×2 from the issue maps cleanly to a small Markdown table. Prose elaboration after the table covers the two cross-cutting edge cases (underline-style headings, cross-cell detection) that don't fit the table shape.
- **Cross-cell directive detection is a first-class rule (R11), not an edge case footnote.** Consumer experience showed this is one of the easier rules to get wrong — a naive line-level scanner that "skips this line if a style comment appears anywhere on it" mishandles every multiline-table row with directives in multiple cells.

---

## Dependencies / Assumptions

- The `epublisher-docs` Phase II scripts referenced by this doc live in a separate repository under that project's `.claude/scripts/` directory. Their path stability inside `epublisher-docs` is the responsibility of that repo's maintainers; cross-references here are descriptive, not contractual.
- The illustrative style names from the issue (FrameMaker / ePublisher conventions) are durable enough as examples to outlive any specific migration toolchain — they describe a category of pattern that recurs across documentation projects migrated from desktop publishing tools.
- The Markdown++ multiline-table parsing rules in `spec/multiline-cell-extensions.md` remain stable; the table-cell edge cases (escaped pipes, multiline row boundaries, continuation-row mechanics) rely on those rules and the empty-separator-row convention.
- The reference doc's role is descriptive, not normative: it captures rules that have proven useful in practice. The Markdown++ spec retains exclusive authority over what *is* valid syntax.

---

## Outstanding Questions

### Resolve Before Planning

- *(none — the open product decisions in the synthesis above are recorded as Inferred in Assumptions and routed for planning-time confirmation rather than blocking the brainstorm.)*

### Deferred to Planning

- [Affects R2, R3][User decision] Whether the SKILL.md pointer is a one-line bullet in the `<references>` list only, or also includes a sentence in the body (e.g., in `<common_mistakes>` or a new `<cleanup>` section). The minimal version adds one bullet; the more discoverable version surfaces the doc in a prose passage too. Planning should choose based on the current skill's information-architecture conventions.
- [Affects R5, R6, R7, R8][Editorial] How exhaustively the illustrative style-name lists are reproduced. Two options: (a) reproduce the full lists from the issue verbatim for completeness, (b) abbreviate to a few canonical examples per category and link to the issue or to the `epublisher-docs` scripts for the full inventory. The tradeoff is doc length vs self-containedness.
- [Affects R17, R18, R19][Editorial] Whether the regex patterns appear as fenced code blocks with a "do not copy these into production untested" caveat, or in prose ("the shape of the detection regex is..."). The former is more useful to tool authors; the latter is more conservative about presenting un-vetted code.
- [Affects R20, R21, R22][Editorial] Whether the `epublisher-docs` cross-references are a single section near the end of the doc or are interleaved with each rule. End-of-doc keeps the rules language-agnostic; interleaving gives each rule a direct implementation link.
- [Affects R9][Editorial] Whether the anchor decision table is the primary form or is supplemented by a small flowchart. Pure-Markdown surfaces favor the table; a Mermaid diagram could be added if planning judges the visual aid worthwhile.
