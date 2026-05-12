---
date: 2026-05-09
topic: table-formatting-capability
---

# Table Formatting Capability for Markdown++

## Summary

Add a deterministic Markdown table beautifier to the markdown-plus-plus skill: a Python script that reformats both standard and `<!-- multiline -->` tables into fixed-width, vertically aligned columns (with word-wrap into continuation rows for multiline tables), backed by a reference document that pins the rule set and a short SKILL.md pointer so Claude applies the same rules during in-flow edits.

---

## Problem Frame

Markdown++ documents commonly contain large hand-authored or migrated tables. Two pains compound in this repo and downstream consumers (e.g., the `epublisher-docs` repo, where the `preparing-dita-files.md` table is the prior-art reference cited by issue #91):

- **Read-time cost.** Compact rows with long single-line cells overflow editor windows and PR review panes. Reviewers either side-scroll or skip the table — neither produces real review of the content.
- **Diff-time cost.** A one-character edit to a long cell rewrites the whole row, hiding the actual change inside whitespace churn. PR diffs cannot communicate what changed semantically.

The pattern that solves both problems is already in use ad hoc: padded fixed-width columns with vertically aligned pipes, and (for multiline tables) long content wrapped to continuation rows. Authors apply it inconsistently because there is no tool, no documented rule set, and no skill-side guidance for Claude to follow when editing tables.

---

## Assumptions

*This requirements doc was authored without synchronous user confirmation. The items below are agent inferences that fill gaps in the input — un-validated bets that should be reviewed before planning proceeds.*

- All three deliverable shapes from the issue's Scope section ship together (script + reference doc + SKILL pointer). The script alone leaves authoring without in-flow guidance; the doc alone has no enforcement path. The bet is that the three reinforce each other and any single shape ships incomplete.
- Defaults: `max_line_width=110`, `max_cell_width=78`, `min_col_width` defaults to the header text's display width, `col_width_strategy=auto`. These are taken from the ranges named in the issue's Configurable Parameters table.
- The script is named `format-tables.py` and lives at the repo top level alongside `scripts/bump-version.sh` rather than inside the skill's `plugins/.../scripts/` directory. The bet is that table formatting is a repo-wide maintenance utility (operators may want to run it on `examples/`, `spec/`, `docs/`), not a skill-internal helper. Planning may revisit if a single canonical location is preferred.
- CLI shape: positional file argument; `--in-place` rewrites the file; `--check` exits non-zero when the file is not already formatted (CI mode); default behavior writes to stdout. Single file per invocation; the shell handles globbing.
- Standard (non-multiline) tables receive alignment-only formatting. Continuation rows are illegal without `<!-- multiline -->`, so cells longer than `max_cell_width` are aligned at maximum width but not wrapped. A warning surfaces when a standard-table cell exceeds the cap so authors know to add `<!-- multiline -->` if wrapping is wanted.
- The inline-formatting tokenizer recognizes only the four classes the issue names: backtick-fenced code spans, `**bold**`, `*italic*` (and `_italic_`), and `**\`compound\`**`. Anything more nested is documented as a known limitation; the formatter falls back to whitespace-tokenized wrapping for those cases rather than failing.
- The reference doc lives at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md` (sibling of `best-practices.md`), and the SKILL.md pointer is a short paragraph that links to it rather than duplicating the rules.

---

## Requirements

**Formatting behavior**
- R1. Reformat any GFM-style pipe-delimited Markdown table (standard or `<!-- multiline -->`) into fixed-width column form: every row padded with trailing spaces so all `|` delimiters align vertically across rows, including the separator row.
- R2. The separator row's dashes span the full computed column width (`-` characters, plus optional leading `:` / trailing `:` / both for alignment markers if present in the input — alignment markers are preserved).
- R3. Empty rows (rows with pipes but only whitespace between them) are preserved as empty rows padded to the same column widths as the rest of the table.
- R4. The `<!-- multiline -->` directive line, including any combined-commands form (e.g., `<!-- style:Name ; multiline ; #alias -->`), is preserved verbatim above the reformatted table.
- R5. Auto column widths derive from the widest content in each column up to `max_cell_width`. When all column max-widths fit within `max_line_width` (including pipes and separator spaces), columns expand to fit content. When they do not, cells exceeding `max_cell_width` trigger wrapping (multiline) or capped alignment (standard).
- R6. For `<!-- multiline -->` tables, content longer than the column's allocated width word-wraps into continuation rows: a continuation row has empty cells in every column except the column whose content is being continued.
- R7. For standard (non-multiline) tables, no continuation rows are generated. Long cells align at maximum cell width; the formatter prints a warning naming the row and column when a standard-table cell exceeds `max_cell_width`.
- R8. Inline formatting tokens — backtick-fenced code spans, `**bold**`, `*italic*` / `_italic_`, and `**\`compound\`**` — are atomic during word-wrap: they are never split across continuation rows. If a token alone exceeds the column width, the token starts on a new continuation row and the column width is locally extended for that row only (the column stays aligned with the rest of the table for all other rows).
- R9. Escaped pipes (`\|`) inside cell content are treated as literal pipe characters and preserved through formatting; they are never interpreted as column delimiters.
- R10. The formatter is idempotent: running it on already-formatted output produces byte-identical output.

**Configurable parameters**
- R11. Expose four parameters with defaults: `max_line_width` (default 110), `max_cell_width` (default 78), `min_col_width` (default: header text display width), `col_width_strategy` with values `auto` (default), `fixed`, `proportional`.
- R12. `col_width_strategy=auto` derives widths from content as in R5. `fixed` uses author-supplied per-column widths (the script accepts a comma-separated `--col-widths` argument). `proportional` distributes `max_line_width` across columns by content-weighted ratio.

**Script (CLI)**
- R13. Provide a Python 3 script that reads a Markdown file, locates every pipe-delimited table in it, applies R1–R10, and emits the modified file.
- R14. Default invocation writes the formatted file to stdout. `--in-place` rewrites the source file. `--check` exits 0 when no changes would be made, non-zero with a diff summary when changes would be made (CI mode).
- R15. Each configurable parameter from R11 is exposed as a CLI flag with its default; the script reports the effective values when `--verbose` is set.
- R16. Non-table content in the file is passed through byte-for-byte unchanged.

**Reference documentation**
- R17. A reference document captures the rule set in prose suitable for human and AI authors, with worked before/after examples covering: standard table alignment, multiline word-wrap, inline-formatting atomicity, escaped-pipe handling, and the empty-row preservation case from the issue.
- R18. The reference document names every default value from R11 and documents the known-limitations behavior described in the inline-formatting Assumption (nested formatting beyond the four named classes falls back to whitespace tokenization).

**SKILL guidance**
- R19. SKILL.md (or `references/best-practices.md`, whichever the planning phase determines is the better surface) gains a short section that links to the table-formatting reference and states the rule that table edits should produce output matching the formatter's idempotent shape.

---

## Acceptance Examples

- AE1. **Covers R1, R2, R3, R6, R8.** Given the multiline table from the issue's Desired Behavior section, when the formatter runs with default parameters, the output matches the issue's "readable, fixed-width format" example byte-for-byte: column widths 30/12/55, separator dashes spanning the full column width, the empty separator row preserved with whitespace-only cells, the long `Meaning` cell wrapped across three continuation rows, and the `SteelHead Cloud` row's empty cells preserved.
- AE2. **Covers R7.** Given a standard (non-multiline) table whose largest cell is 120 characters wide and `max_cell_width=78`, when the formatter runs, the output has every cell padded to 120 characters (no wrapping) and stderr contains a warning naming the row and column.
- AE3. **Covers R8.** Given a multiline table cell containing `Use the **\`Set-ExecutionPolicy\`** cmdlet to enable scripts.` with `max_cell_width=20`, when the formatter wraps, the `**\`Set-ExecutionPolicy\`**` token appears on its own continuation row (since the token itself is 28 chars > 20) and the column is locally widened to fit it on that row only.
- AE4. **Covers R9.** Given a cell containing `pipe \| character`, when the formatter runs, the output cell content remains `pipe \| character` and the row continues to have the same number of column delimiters as other rows.
- AE5. **Covers R10.** Given any input file, when the formatter runs twice in succession (output → input → output again), the second output is byte-identical to the first.
- AE6. **Covers R14.** Given a correctly formatted file, when invoked with `--check`, the script exits 0 with no output. Given an incorrectly formatted file, `--check` exits non-zero and prints a unified diff summary.
- AE7. **Covers R4.** Given an input table preceded by `<!-- style:DataTable ; multiline ; #my-table -->`, when the formatter runs, that directive line is byte-identical in the output (no whitespace normalization, no comment reformatting).

---

## Success Criteria

- A documentation author can run `python scripts/format-tables.py path/to/file.md --in-place` and get a readable, diff-friendly table without hand-editing column widths.
- A reviewer reading a PR that touches one cell sees a one-line diff for that cell, not a whole-row rewrite, because all other rows kept their byte-identical formatting.
- Claude editing a Markdown++ table during an authoring session produces output that the formatter would consider already formatted (the rule set is the same; the formatter just enforces it deterministically).
- A CI step running `format-tables.py --check` on changed files passes for properly formatted tables and fails with a clear diff for unformatted ones.
- A downstream agent reading this document can implement the script without inventing product behavior: every configurable parameter has a default, every formatting rule has a worked example, and every edge case the issue raised (escaped pipes, inline-formatting atomicity, empty separator rows, the `<!-- multiline -->` directive line) is named in a requirement.

---

## Scope Boundaries

- Reflowing Markdown content outside tables (paragraphs, lists, code blocks).
- Validating that cell content is well-formed Markdown beyond what's needed to tokenize the four inline-formatting classes.
- Auto-detecting which tables to format and which to leave alone — the formatter processes every pipe-delimited Markdown table it finds in the file.
- Editor integrations (VS Code, JetBrains, etc.) and language-server protocol support.
- Installing or configuring git pre-commit hooks. Documentation may show how to wire the script into a hook, but the formatter itself does not install one.
- Full CommonMark inline parsing. The tokenizer recognizes only the four formatting classes the issue names; deeper nesting falls back to whitespace tokenization with a documented limitation.
- Multi-file batch globs as a script feature in v1. The shell handles globbing; the script accepts one file per invocation.
- Reformatting tables embedded inside fenced code blocks or HTML blocks. Code-block content is passed through unchanged per R16.
- Detection or repair of malformed tables (unequal column counts across rows, missing separator). The formatter assumes the input is a valid pipe-delimited Markdown table and reports a parse error rather than guessing.

---

## Key Decisions

- Three deliverables ship together (script + reference doc + SKILL pointer): a script without prose drifts from skill behavior; prose without a script has no enforcement path. The reference doc is the source of truth that both the script and the skill follow.
- Auto column-width strategy is the default because it matches the prior-art pattern in `epublisher-docs` and is the only strategy that requires no per-table author input.
- Standard (non-multiline) tables get alignment-only treatment with a warning rather than synthesized continuation rows: continuation rows are illegal in standard tables per the Markdown++ spec, and silently inserting them would change the document's parse tree.
- Inline-formatting atomicity is a hard rule (R8) rather than a heuristic. Splitting `**bold**` across rows would break the rendered output; the formatter widens the column locally for outsized tokens to keep the rendering correct.
- The script's location (top-level `scripts/` vs inside the skill's `scripts/`) is left to planning. Both are defensible; the reference doc's cross-reference is what matters for skill-time discovery.

---

## Dependencies / Assumptions

- Python 3.x, no external dependencies beyond the standard library (mirrors `validate-mdpp.py`'s posture and `scripts/requirements.txt`).
- The Markdown++ multiline-table parsing rules in `spec/multiline-cell-extensions.md` are stable; the formatter relies on the continuation-row mechanism (empty leading cells extend the prior row) and the empty-separator-row convention.
- The combined-commands form `<!-- style:Name ; multiline ; #alias -->` is parsed as a single directive line and preserved as a single line.

---

## Outstanding Questions

### Resolve Before Planning

- *(none — the open product decisions in the synthesis above are recorded as Inferred in Assumptions and routed for planning-time confirmation rather than blocking the brainstorm.)*

### Deferred to Planning

- [Affects R13][Technical] Script location: top-level `scripts/format-tables.py` or `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`? Planning should weigh the discoverability vs skill-co-location tradeoff and pick one.
- [Affects R8][Needs research] Display-width measurement for non-ASCII content (CJK wide characters, combining marks, ZWJ emoji). Pinning column widths to character count vs `wcwidth`-based display width changes the formatter's correctness on internationalized content. Planning should determine whether `wcwidth` is in scope for v1 or a known limitation.
- [Affects R12][Technical] `col_width_strategy=fixed` and `proportional` behaviors are named in the issue but not exemplified. Planning should pin the exact CLI shape for `--col-widths` (comma list, JSON, or per-column flag) and the proportional algorithm.
- [Affects R19][User decision] Whether the SKILL guidance lives in `SKILL.md` directly or in `references/best-practices.md`. Both are reasonable surfaces; planning should pick the one that fits the existing skill's information architecture.
- [Affects R14][Technical] `--check` diff format: unified diff (`difflib.unified_diff`) vs minimal "N tables would be reformatted" summary. CI ergonomics differ between the two.
