---
title: "feat: Add table formatting capability to markdown-plus-plus skill"
type: feat
status: active
date: 2026-05-09
plan_id: 2026-05-09-004
origin: docs/brainstorms/2026-05-09-table-formatting-capability-requirements.md
issue: 91
---

# feat: Add table formatting capability to markdown-plus-plus skill

## Summary

Ship a deterministic Markdown table beautifier as three coordinated deliverables: a Python 3 script (`format-tables.py`) that reformats both standard and `<!-- multiline -->` tables into fixed-width vertically aligned columns (with word-wrap into continuation rows for multiline tables), a reference document (`references/table-formatting.md`) that pins the rule set with worked before/after examples, and a short pointer in `references/best-practices.md` so Claude applies the same rules during in-flow edits. The script lives alongside `validate-mdpp.py` and `add-aliases.py` (same domain — Markdown content tooling), uses only the Python standard library, and is idempotent so CI can enforce it via `--check`.

(see origin: [docs/brainstorms/2026-05-09-table-formatting-capability-requirements.md](../brainstorms/2026-05-09-table-formatting-capability-requirements.md))

---

## Problem Frame

Markdown++ documents commonly carry large hand-authored or migrated tables. Two pains compound across this repo and downstream consumers (the prior-art reference is the `epublisher-docs` repository, where the readable-table pattern is already in ad hoc use):

- **Read-time cost.** Compact rows with long single-line cells overflow editor windows and PR review panes. Reviewers either side-scroll or skip the table — neither produces real review of the content.
- **Diff-time cost.** A one-character edit to a long cell rewrites the whole row, hiding the actual change inside whitespace churn. PR diffs cannot communicate what changed semantically.

The pattern that solves both problems — padded fixed-width columns with vertically aligned pipes, and (for multiline tables) long content wrapped to continuation rows — is applied inconsistently because there is no tool, no documented rule set, and no skill-side guidance for Claude to follow when editing tables.

---

## Requirements & Traceability

| ID  | Requirement (abbreviated)                                              | Implementation Units |
|-----|------------------------------------------------------------------------|----------------------|
| R1  | Reformat standard or multiline tables to fixed-width aligned columns   | U2, U3, U4           |
| R2  | Separator row dashes span full column width; alignment markers preserved | U3                 |
| R3  | Empty rows preserved with whitespace-only cells padded to column widths | U3                 |
| R4  | `<!-- multiline -->` directive (incl. combined-commands) preserved verbatim | U2, U3           |
| R5  | Auto column widths derived from widest content up to `max_cell_width`  | U3                   |
| R6  | Multiline tables: word-wrap long content into continuation rows        | U4                   |
| R7  | Standard tables: align-only with warning when cell exceeds `max_cell_width` | U4              |
| R8  | Inline formatting tokens are atomic during word-wrap                   | U4                   |
| R9  | Escaped pipes (`\|`) preserved as literal cell content                 | U2                   |
| R10 | Idempotent output                                                      | U3, U4, U6           |
| R11 | Four configurable parameters with defaults                             | U5                   |
| R12 | `auto` / `fixed` / `proportional` strategies                           | U5                   |
| R13 | Python 3 script processes a Markdown file                              | U5                   |
| R14 | `--in-place` / `--check` / default-stdout invocation modes             | U5                   |
| R15 | Each parameter exposed as CLI flag; `--verbose` reports effective values | U5                 |
| R16 | Non-table content passed through byte-for-byte                         | U2                   |
| R17 | Reference document with worked before/after examples                   | U7                   |
| R18 | Reference doc names every default and documents tokenizer limitations  | U7                   |
| R19 | Skill guidance section linking to the reference doc                    | U8                   |

A/F/AE coverage from origin: AE1–AE7 are addressed in U6 test scenarios.

---

## Scope Boundaries

### In scope
- New script `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py` (Python 3, stdlib only).
- New reference document `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md`.
- A short subsection in `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` linking to the new reference and stating the in-flow-editing rule.
- A one-line entry in the SKILL.md references list pointing to `references/table-formatting.md`.
- Test fixtures under `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/` covering AE1–AE7.

### Out of scope (preserved from origin Scope Boundaries)
- Reflowing Markdown content outside tables.
- Validating cell content as well-formed Markdown beyond what the four-class tokenizer needs.
- Auto-detecting which tables to format — the formatter processes every pipe-delimited table it finds.
- Editor integrations (VS Code, JetBrains, LSP).
- Installing or configuring git pre-commit hooks. (Documentation may show how to wire one up; the script does not install one.)
- Full CommonMark inline parsing. The tokenizer handles the four named classes; deeper nesting falls back to whitespace tokenization.
- Multi-file batch globs in v1 — the shell handles globbing; the script accepts one file per invocation.
- Reformatting tables embedded inside fenced code blocks or HTML blocks (passed through unchanged per R16).
- Detection or repair of malformed tables (unequal column counts, missing separator) — the formatter reports a parse error rather than guessing.

### Deferred to Follow-Up Work
- `wcwidth`-based column-width measurement for non-ASCII content (CJK wide chars, ZWJ emoji, combining marks). v1 measures by Python string length, which is correct for ASCII and most Latin-script content but undercounts wide characters and overcounts ZWJ sequences. The reference doc names this as a known limitation. Resolving it requires either pulling in `wcwidth` (violates the stdlib-only posture) or shipping a stripped-down width table; either way, it's a separate scope decision.
- Multi-file batch globs as a script feature.
- Pre-commit hook installer.
- An `--auto-multiline` flag that synthesizes a `<!-- multiline -->` directive when a standard table has cells exceeding `max_cell_width`. The v1 design surfaces a warning instead so authors stay in control.

---

## Output Structure

```
plugins/markdown-plus-plus/skills/markdown-plus-plus/
├── scripts/
│   └── format-tables.py                      # New: CLI entry + table reformatting
├── references/
│   └── table-formatting.md                   # New: rule set + worked examples
├── references/best-practices.md              # Edit: add table-formatting subsection
├── SKILL.md                                  # Edit: add reference-list entry
└── tests/
    ├── sample-tables-multiline.md            # New: AE1, AE3, AE4 fixtures
    ├── sample-tables-standard-warn.md        # New: AE2 fixture
    └── sample-tables-already-formatted.md    # New: AE5 idempotency fixture
```

The fixtures directory is shared with existing `sample-*.md` files used by `validate-mdpp.py`. The new `sample-tables-*` files extend that pattern; nothing is moved or renamed.

---

## High-Level Technical Design

*This section illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

The script is a four-stage pipeline:

```
file bytes
  │
  ▼
[1] Block scanner ──► non-table blocks ────────────────────┐
  │   - identifies pipe-table blocks                       │
  │   - leaves fenced code blocks, HTML blocks, prose      │
  │     unchanged                                          │
  │   - captures any preceding directive line              │
  │     (<!-- multiline --> or combined-commands form)     │
  ▼                                                        │
[2] Cell parser                                            │
  │   - splits each row on unescaped `|`                   │
  │   - preserves `\|` as literal content                  │
  │   - normalizes leading/trailing pipe state             │
  ▼                                                        │
[3] Width planner                                          │
  │   - computes per-column widths per col_width_strategy  │
  │   - auto: max(content_len) clamped to max_cell_width   │
  │   - fixed: user-supplied widths                        │
  │   - proportional: weighted by sum(content_len)         │
  ▼                                                        │
[4] Renderer                                               │
  │   - multiline: tokenize cell, word-wrap into           │
  │     continuation rows, expand column locally for       │
  │     atomic tokens that exceed width                    │
  │   - standard: align-only; warn on over-width cells     │
  │   - emit separator row with dashes (alignment markers  │
  │     preserved)                                         │
  ▼                                                        │
formatted file ◄──── reassembled with non-table blocks ────┘
```

**Tokenizer for inline-formatting atomicity (R8).** A small finite-state tokenizer recognizes the four classes the issue names — backtick code spans, `**bold**`, `*italic*` / `_italic_`, and `**\`compound\`**` — by greedy matching against pre-compiled regular expressions. Anything outside these classes is treated as whitespace-tokenizable text. The tokenizer's output is a list of `(text, atomic)` tuples; the wrap algorithm consumes that list and never breaks inside an atomic span.

**Idempotency (R10).** Achieved by determinism, not byte-comparison: each stage's output depends only on its input and the configuration, with no state-carrying side effects. The U6 test suite proves it empirically by running the formatter twice and asserting byte equality.

---

## Key Technical Decisions

- **Script location: skill-internal `scripts/` directory.** `format-tables.py` lives at `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`, alongside `validate-mdpp.py` and `add-aliases.py`. **Rationale:** All three scripts operate on Markdown++ content and target the same audience (skill consumers, documentation authors). Top-level `scripts/` currently holds `bump-version.sh`, which is plugin-infrastructure tooling — different audience and lifecycle. Co-locating with the skill also keeps the SKILL.md cross-reference path short and stable. Resolves origin Outstanding Question on script location.

- **Standard-library only; no third-party dependencies.** Python 3.10+ (matches `validate-mdpp.py`), uses `re`, `argparse`, `difflib`, `sys`, `unicodedata`. No `wcwidth`, no `mistune`, no `markdown-it-py`. **Rationale:** Mirrors `requirements.txt`'s explicit "no external dependencies required" posture. A formatter that needs `pip install` before running adds friction to the documentation-author workflow that the script is meant to remove.

- **Width measurement: Python string length (v1), `wcwidth` deferred.** Cell widths are computed by `len(s)` after stripping ANSI/control characters. Wide-character semantics (CJK, ZWJ emoji) are documented as a known limitation in `references/table-formatting.md`. **Rationale:** Pulling in `wcwidth` violates the stdlib-only decision. Reimplementing East Asian Width by hand from `unicodedata.east_asian_width` is feasible but expands v1 scope. The repo's existing tables are ASCII-dominant; correctness for CJK-heavy documents is a follow-up. Resolves origin Outstanding Question on display-width measurement.

- **`--col-widths` shape: comma-separated integers.** `--col-widths 30,12,55` overrides per-column widths when `--col-width-strategy fixed`. Argument count must equal the table's column count; mismatch is a parse error. The `proportional` strategy distributes `max_line_width − pipe_and_separator_overhead` across columns by ratio of total content length per column, with `min_col_width` as a floor. **Rationale:** Comma-separated integers are unambiguous, easy to type, and match the format used in similar tools (`column -t -s`, `prettier --print-width` cousins). JSON would be heavier; per-column flags would clutter the CLI. Resolves origin Outstanding Question on fixed/proportional CLI shape.

- **Skill guidance lives in `references/best-practices.md`, not SKILL.md.** A new "Table Formatting" subsection in `best-practices.md` (matching the existing "When to Use Each Extension" structure) carries the prescriptive guidance and links to `references/table-formatting.md` for the full rule set. SKILL.md gains only a one-line entry in its references list. **Rationale:** SKILL.md is the canonical activation surface — its `description:` frontmatter and inline content are what the routing layer reads. Adding a scenario-specific guidance section there bloats the trigger surface for a single feature. `best-practices.md` is the right layer for prescriptive authoring rules; the table-formatting rule fits cleanly with the existing block-vs-inline-style guidance and naming conventions there. Resolves origin Outstanding Question on SKILL guidance surface.

- **`--check` emits unified diff.** When the file is not already formatted, `--check` exits non-zero and prints `difflib.unified_diff(original, formatted, fromfile=path, tofile=path+' (formatted)')` to stdout. **Rationale:** CI logs are the dominant consumer; a unified diff lets a developer paste the failing diff back into review or grep for the offending row. A "N tables would be reformatted" summary is too lossy when the CI run is the only artifact a reviewer sees. Matches the convention used by `black --check`, `gofmt -d`, and `prettier --check`. Resolves origin Outstanding Question on `--check` diff format.

- **Inline-formatting token classes are exactly four.** The tokenizer recognizes backtick code spans, `**bold**`, `*italic*` / `_italic_`, and `**\`compound\`**`. Anything more nested falls back to whitespace tokenization. **Rationale:** Origin's R8 names exactly these classes. Implementing a CommonMark-compliant inline parser would re-implement `markdown-it-py` and is well outside v1 scope. The four classes cover the overwhelming majority of formatting in Markdown++ tables; the fallback is documented as a known limitation in the reference doc.

- **Standard-table over-width behavior: warn, don't auto-promote.** When a standard table cell exceeds `max_cell_width`, the formatter prints a stderr warning naming the row and column but produces aligned output at the actual cell width (no truncation). It does **not** silently insert `<!-- multiline -->`. **Rationale:** Auto-promotion would change the document's parse tree without author consent. A warning is loud enough that CI surfaces the problem; the author retains control over whether to add the directive. Preserves R7 from origin.

---

## Patterns to Follow

- **`plugins/.../scripts/validate-mdpp.py`** — argparse setup, `Colors` ANSI helpers, top-of-file docstring describing usage and exit codes, dataclass-based diagnostic objects, `--json` and `--verbose` conventions. Mirror this shape for `format-tables.py`.
- **`plugins/.../scripts/add-aliases.py`** — file read/write pattern, `--in-place` vs. stdout, `--dry-run` precedent (the new script uses `--check` with the same spirit).
- **`plugins/.../references/syntax-reference.md` and `best-practices.md`** — frontmatter format (`date: YYYY-MM-DD`, `status: active`), heading structure, do/don't snippets in fenced code blocks. Follow this shape for `table-formatting.md`.
- **`docs/plans/2026-04-08-002-feat-multiline-cell-extensions-plan.md`** — recent plan in this repo demonstrating the level of detail expected for a feature plan in this codebase.

---

## System-Wide Impact

- **Skill consumers.** A new script and a new reference document. No breaking changes to existing scripts or reference files. The `best-practices.md` addition is additive.
- **Plugin version.** The plugin's published surface gains a new script and a new reference. **Bump minor** (`scripts/bump-version.sh minor`) — this is a new feature added to the skill.
- **CLAUDE.md guidance.** No changes required. The existing routing-context discipline (read-before-edit, explicit skill load) already covers Markdown++ files; the new feature operates within that flow.
- **Downstream `epublisher-docs` repository.** Once the script ships, `epublisher-docs` can adopt it directly (same Markdown++ format). No coordination required for v1; a follow-up could wire it into that repo's CI.
- **Tests directory.** Three new fixtures under `plugins/.../tests/`. The existing `validate-mdpp.py` test fixtures are untouched.

---

## Implementation Units

### U1. Skeleton: argparse, file I/O, pass-through mode

**Goal:** Establish the script's CLI surface and outermost shell. The script reads a file, identifies non-table blocks, and emits the file unchanged. This proves the file-I/O harness, the argparse layer, and the byte-for-byte pass-through guarantee (R16) before any reformatting logic exists.

**Requirements:** R13, R14 (default-stdout mode only), R15 (CLI flags exposed but no-op for now), R16

**Dependencies:** None

**Files:**
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-tables-already-formatted.md` (used in U6, but a minimal fixture lands here so U1 has something to round-trip)

**Approach:**
- Module docstring matching the `validate-mdpp.py` style: usage block, options block, exit codes block.
- `argparse.ArgumentParser` with: positional `input_file`, `--in-place`, `--check`, `--max-line-width`, `--max-cell-width`, `--min-col-width`, `--col-width-strategy {auto,fixed,proportional}`, `--col-widths`, `--verbose`, `--json` (reserved for future).
- Read file as UTF-8 (no BOM handling beyond what Python does by default).
- Pass-through implementation: write input bytes to stdout. `--in-place` is a no-op when input == output.
- Exit codes: 0 success, 1 file error, 2 invalid args, 3 reserved (parse errors land here in U2), 4 reserved (`--check` mismatch lands here in U5).

**Patterns to follow:**
- `plugins/.../scripts/validate-mdpp.py` for the docstring shape, exit-code documentation, `Colors` helper, and argparse layout.
- `plugins/.../scripts/add-aliases.py` for the file-read/write idiom and `--in-place` semantics.

**Test scenarios:**
- Happy path: feeding a Markdown file with no tables produces byte-identical stdout output.
- Edge: feeding an empty file exits 0 with empty stdout.
- Error: feeding a non-existent path exits 1 with a stderr message naming the path.
- Error: passing `--col-width-strategy garbage` exits 2 with the argparse error format.
- Edge: `--in-place` on a file with no tables leaves the file mtime updated but content byte-identical.

**Verification:**
- `python format-tables.py tests/sample-tables-already-formatted.md` writes the file unchanged to stdout.
- `--help` lists all CLI flags with their defaults visible (R15 effective-values surfacing comes in U5).

---

### U2. Block scanner: identify table boundaries; preserve directive lines and escaped pipes

**Goal:** Add the block scanner that walks the input line-by-line, classifies each line as `prose` / `code-fence` / `html-block` / `directive` / `table-row`, and groups consecutive table rows into table blocks. Each block is paired with its preceding directive line if one exists. Within a row, escaped pipes (`\|`) are preserved as literal cell content (R9) — not interpreted as column delimiters. Reformatting still uses pass-through (no width changes yet); the scanner just proves it correctly identifies and round-trips tables.

**Requirements:** R4 (directive preservation), R9 (escaped pipes), R16 (non-table pass-through)

**Dependencies:** U1

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`

**Approach:**
- A `BlockScanner` class consumes lines and yields `Block` objects (`TableBlock`, `ProseBlock`, `CodeBlock`, `HtmlBlock`).
- Table detection: a line is a candidate row if it matches `^\s*\|.*\|\s*$` (allowing escaped pipes inside). A table block is a sequence of two-or-more candidate rows where the second row is the separator (`^\s*\|[\s:|-]+\|\s*$`).
- Directive line: the line immediately preceding a table block, if it matches `<!--\s*multiline\s*-->` or any combined-commands form including `multiline`, becomes part of the table block's metadata. Combined commands are matched by the existing `multiline` token within a `<!--\s*[^>]*?-->` comment.
- Code fences (```) and HTML blocks (`<...>`) suppress table detection inside them — code-block content passes through unchanged per R16.
- Cell splitter: a regex that splits on `|` but not on `\|`. Using `re.split(r'(?<!\\)\|', row)` and trimming the leading/trailing empty captures from the table edges.

**Patterns to follow:**
- `validate-mdpp.py` line-iteration pattern (`for line_num, line in enumerate(lines, 1)`).
- `spec/multiline-cell-extensions.md` for the multiline directive's exact syntax (including combined-commands form).

**Test scenarios:**
- Happy path: a file with one multiline table, one standard table, and prose paragraphs round-trips byte-identically.
- Edge: a table with a row containing `pipe \| character` cells round-trips with the `\|` preserved (this is the AE4 setup; full assertion lands in U6).
- Edge: a table directly preceded by `<!-- style:DataTable ; multiline ; #my-alias -->` round-trips with the directive byte-identical (this is the AE7 setup; full assertion lands in U6).
- Edge: a fenced code block containing what looks like a Markdown table is passed through unchanged (R16).
- Edge: two tables separated by a blank line are recognized as two separate blocks, not one merged block.
- Error: a file where the second line of a candidate table block does not match the separator pattern is treated as prose (no table detection), not a parse error — the formatter only signals errors when the input *looks* like a table but is malformed.

**Verification:**
- A test file with mixed content (prose, fences, HTML, two tables, escaped pipes, directive lines) emits byte-identical output through the U2 scanner with U3/U4 still pass-through.

---

### U3. Width planner and aligned renderer for standard (non-multiline) tables

**Goal:** Compute per-column widths from cell content and emit each row padded to those widths with vertically aligned pipes. This unit handles standard tables only — no continuation-row generation. Empty rows (R3) are preserved as whitespace-padded rows. Separator dashes span the full computed column width; alignment markers (`:---`, `---:`, `:---:`) are preserved (R2). Cells exceeding `max_cell_width` are still printed at their actual width (R7's "no continuation rows for standard tables") with a warning deferred to U4 — this unit just proves the alignment math.

**Requirements:** R1, R2, R3, R5, R10 (idempotency for standard tables)

**Dependencies:** U2

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`

**Approach:**
- `WidthPlanner` consumes a list of parsed rows and computes `col_widths[i] = max(len(cell[i]) for cell in rows)` clamped to `max_cell_width` (the auto strategy). `min_col_width` defaults to the header text's display width — implemented as `col_widths[i] = max(col_widths[i], len(header_cells[i]))`.
- `Renderer.render_standard(rows, col_widths)` emits each row as `| ` + ` | `.join(cell.ljust(col_widths[i])) + ` |`. The separator row uses `-` characters to span `col_widths[i]`; alignment markers from the input separator (`:`, `:` `:`) are preserved.
- Empty rows: a row whose cells are all whitespace-only is emitted as `| ` + ` | `.join(' ' * col_widths[i]) + ` |`.

**Test scenarios:**
- Happy path: a 3-column standard table with mixed-length cells produces output where all `|` characters align in identical columns across all rows including the separator.
- AE3 prerequisite (no wrapping yet, just alignment): a header `| Term | Abbreviation | Meaning |` produces a separator with dashes spanning the full computed width of each column.
- Edge: an empty row (`| | | |` with whitespace-only cells) is preserved as an empty row padded to full width — output retains the visually blank gap between data rows. (Covers AE1's empty-row preservation case at the alignment level; multiline-specific aspects come in U4.)
- Edge: alignment markers in the separator (`:---`, `---:`, `:---:`) are preserved through reformatting.
- Idempotency: running the formatter twice on a U3-only standard table produces byte-identical output.
- Edge: a single-row table with only a header and separator (no data rows) round-trips correctly with column widths derived from the header.

**Verification:**
- Visual: opening a reformatted standard table in any text editor shows pipes aligning vertically across all rows.
- Idempotency: `python format-tables.py file.md > formatted.md && python format-tables.py formatted.md | diff -u formatted.md -` produces no diff.

---

### U4. Multiline rendering: word-wrap, continuation rows, inline-formatting atomicity, standard-table over-width warning

**Goal:** Add the multiline-table renderer that wraps long cell content into continuation rows (R6), respects inline-formatting atomicity (R8) by tokenizing the four named classes as atomic units, and locally widens the column when an atomic token exceeds the planned width. Also adds the standard-table over-width warning (R7) — when a standard-table cell exceeds `max_cell_width`, stderr gets a warning naming the row and column, but output still aligns at the actual cell width.

**Requirements:** R6, R7, R8, R10 (idempotency for multiline tables)

**Dependencies:** U3

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`

**Approach:**
- `InlineTokenizer` recognizes (in this priority order):
  1. Compound: `\*\*`backtick`[^`]+`backtick`\*\*`
  2. Code spans: backtick`[^`]+`backtick (single-backtick form; multi-backtick form is a known limitation)
  3. Bold: `\*\*[^*]+\*\*`
  4. Italic: `\*[^*]+\*` or `_[^_]+_`
  5. Plain whitespace-delimited word
- Each match emits a `(text, atomic: bool)` tuple. Plain words are `atomic=False`; the four formatting classes are `atomic=True`.
- `Wrapper.wrap(tokens, width)` greedily packs tokens into lines, never breaking inside an `atomic=True` token. If a single atomic token's length exceeds `width`, the wrapper emits a line containing only that token; the renderer detects this case and locally widens the column for that one continuation row only. Other rows in the table keep their planned width.
- `Renderer.render_multiline(rows, col_widths, directive_line)`:
  - Emits the directive line verbatim above the table.
  - For each row, calls `Wrapper.wrap(tokenize(cell), col_widths[i])` per cell.
  - Determines `max_lines = max(len(wrapped[i]) for i in cols)`. Emits `max_lines` rows: the first row has all cells; subsequent rows have empty cells (whitespace-padded) in every column except the column whose wrapped content continues.
- Standard-table warning: when `Renderer.render_standard` encounters a cell whose length exceeds `max_cell_width`, emit `WARNING: cell exceeds max_cell_width (N chars > M)` to stderr, naming the row index (1-based) and column index (1-based, header text quoted).

**Patterns to follow:**
- `validate-mdpp.py`'s `Colors` for stderr warning formatting.
- The existing `PATTERNS` regex dict in `validate-mdpp.py` for the bold/italic/code-span shape.

**Test scenarios:**
- Covers AE1. Happy path: the multiline table from issue #91's "compact format" example is reformatted to the issue's "readable, fixed-width format" output byte-for-byte: column widths 30/12/55, separator dashes span the full column width, the empty separator row is preserved with whitespace-only cells, the long `Meaning` cell wraps across three continuation rows, and the `SteelHead Cloud` row's empty cells are preserved.
- Covers AE3. Edge — atomic-token outsizes column: a multiline cell containing `Use the **\`Set-ExecutionPolicy\`** cmdlet to enable scripts.` with `--max-cell-width 20` produces output where `**\`Set-ExecutionPolicy\`**` appears alone on its own continuation row (token is 28 chars > 20), with the column locally widened to 28 for that row only — other rows in the same column stay at their planned width.
- Edge — bold token splitting prevention: a multiline cell containing `Click the **Save and Continue** button` with column width 14 wraps so that `**Save and Continue**` (the atomic token) is not split mid-token; either the whole token fits on one line or it occupies its own continuation row.
- Edge — code span splitting prevention: a multiline cell containing `Run \`npm install --save-dev\` first` with column width 18 keeps `\`npm install --save-dev\`` intact across the wrap.
- Edge — italic underscore form: a multiline cell containing `_emphasis_` is recognized as atomic.
- Covers AE2 (R7). Standard-table over-width: a standard table whose largest cell is 120 characters wide with `--max-cell-width 78` produces output where every cell is padded to 120 characters (no wrapping) and stderr contains a warning naming row and column.
- Edge — multiple atomic tokens in one cell: `Use **bold** and \`code\` together` wraps with both tokens preserved as atomic units.
- Edge — fallback to whitespace tokenization: a cell containing nested formatting outside the four classes (e.g., `**bold _italic_ inside**`) does not crash; the wrapper falls back to whitespace tokenization for the unrecognized structure. Documented limitation.
- Idempotency: running the formatter twice on a multiline table produces byte-identical output (full AE5 assertion lands in U6).

**Verification:**
- Visual: opening the reformatted issue #91 example matches the issue's "Desired Behavior" output byte-for-byte.
- Stderr: running on a standard table with an over-width cell prints exactly one warning line per offending cell.

---

### U5. Wire CLI flags into formatter; implement `--in-place`, `--check`, `--verbose`, and width strategies

**Goal:** Connect the argparse layer (U1) to the formatter (U3, U4). Implement `--in-place` (rewrite the file), `--check` (exit non-zero with unified diff when output differs from input), and `--verbose` (print effective parameter values to stderr). Implement `--col-width-strategy` for `auto` (default), `fixed` (uses `--col-widths`), and `proportional` (distributes `max_line_width` by content-length-weighted ratio).

**Requirements:** R11, R12, R14, R15

**Dependencies:** U4

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`

**Approach:**
- `--in-place`: write formatted bytes back to the source file. Use a temp-file + atomic-rename pattern (write to `<file>.tmp`, then `os.replace`).
- `--check`: compute formatted output, compare to input bytes, exit 0 with no output if equal, exit 4 with `difflib.unified_diff(input_lines, formatted_lines, fromfile=path, tofile=path+' (formatted)')` printed to stdout if different.
- `--verbose`: print `Effective parameters: max_line_width=N, max_cell_width=N, min_col_width=N, col_width_strategy=X` to stderr before processing.
- `--col-width-strategy fixed`: requires `--col-widths` (comma-separated integers). If the count of widths doesn't match a table's column count, exit 2 with a parse error naming the table location and expected/actual column counts.
- `--col-width-strategy proportional`: compute `available = max_line_width − (n_cols + 1) − (n_cols * 2)` (pipes plus single-space padding on each side of each cell). Distribute by `col_widths[i] = max(min_col_width, round(available * sum_content_len[i] / total_content_len))`. Round-robin any remainder to the widest content columns.
- `--col-widths` is parsed once at startup and applies to *every* table the script processes. If multiple tables in the file have different column counts, the formatter exits 2.

**Test scenarios:**
- Covers AE6. `--check` happy path: a correctly formatted file exits 0 with no output.
- Covers AE6. `--check` mismatch: an incorrectly formatted file exits 4 (non-zero) and prints a unified diff to stdout.
- Happy path: `--in-place` rewrites the file and the rewrite is atomic (a SIGINT during the write does not leave a partial file at the original path).
- Happy path: `--verbose` prints the effective parameter values to stderr.
- Edge: `--col-width-strategy fixed --col-widths 30,12,55` overrides auto widths for a 3-column table.
- Edge: `--col-width-strategy fixed --col-widths 30,12` against a 3-column table exits 2 with a clear error.
- Edge: `--col-width-strategy proportional` with `max_line_width=110` on a table where one column has 5x the content of the others gets ~5x the width allocation.
- Edge: `--col-widths` set without `--col-width-strategy fixed` is ignored with a stderr warning.

**Verification:**
- `python format-tables.py file.md --check` returns shell exit 0 on a formatted file and shell exit 4 on an unformatted file.
- `python format-tables.py file.md --in-place` modifies the file when it has unformatted tables and leaves it untouched when it doesn't (no spurious mtime changes).

---

### U6. Test fixtures: AE1–AE7 coverage

**Goal:** Land the test fixtures and a verification protocol that exercises every Acceptance Example. The fixtures live next to the existing `validate-mdpp.py` samples but are clearly named (`sample-tables-*`) so they don't get confused. There is no automated test runner in this repo (the existing samples are also manual verification fixtures), so the protocol is a documented sequence in `tests/format-tables-cases.md`.

**Requirements:** R10 (idempotency proof), AE1–AE7 coverage

**Dependencies:** U5

**Execution note:** Coverage scenarios named on each preceding unit (U1–U5) are the implementer's source of truth for the exhaustive test surface. This unit consolidates the AE-level fixtures and the manual-run protocol; do not duplicate the granular per-unit scenarios here.

**Files:**
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-tables-multiline.md` (AE1, AE3, AE4, AE7 fixtures)
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-tables-standard-warn.md` (AE2 fixture)
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-tables-already-formatted.md` (add AE5 idempotency scenarios)
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/format-tables-cases.md` (manual-verification protocol)

**Approach:**
- Each fixture file pairs an "input" table block with a "expected output" table block, separated by a `## Expected output` heading.
- `format-tables-cases.md` lists each AE with: source fixture, exact CLI invocation, expected stdout, expected stderr, expected exit code. Mirrors the structure of `tests/auto-activation/cases.md`.
- AE5 idempotency: the protocol's last entry runs every fixture twice through the formatter and asserts byte-equality between the two runs.

**Test scenarios:**
- Covers AE1. Multiline-table fixture matches the issue #91 "Desired Behavior" example byte-for-byte after formatting.
- Covers AE2. Standard-table fixture with a 120-char cell produces aligned output and stderr warning.
- Covers AE3. Multiline cell with `**\`Set-ExecutionPolicy\`**` and `--max-cell-width 20` puts the atomic token on its own continuation row.
- Covers AE4. Cell containing `pipe \| character` round-trips with the escaped pipe preserved.
- Covers AE5. Every fixture, when formatted twice, produces byte-identical second-pass output.
- Covers AE6. `--check` on the already-formatted fixture exits 0; `--check` on the unformatted multiline fixture exits 4 with a unified diff.
- Covers AE7. Multiline fixture with `<!-- style:DataTable ; multiline ; #my-table -->` directive line preserves the directive byte-identical through formatting.

**Verification:**
- `format-tables-cases.md` lists every AE with a runnable command and an expected outcome.
- A human can step through the protocol in under five minutes and verify all seven AEs pass.

---

### U7. Reference document: `references/table-formatting.md`

**Goal:** Pin the formatting rule set in prose suitable for both human and AI authors. Includes worked before/after examples for every behavior the formatter ships, names every default value, and documents the known limitations (the four-class tokenizer, ASCII-dominant width measurement). This is the source of truth that both the script and the skill follow.

**Requirements:** R17, R18

**Dependencies:** U6 (the worked examples in this doc reuse the test fixtures' input/output pairs)

**Files:**
- Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md`

**Approach:**
- YAML frontmatter: `date: 2026-05-09`, `status: active`, `type: reference`.
- Sections:
  1. **Why this rule set exists** — the read-time and diff-time problems from origin.
  2. **The rule set** — R1–R10 as numbered prose statements with a code-block example for each.
  3. **Configurable parameters** — R11/R12, naming every default and giving an example invocation per strategy.
  4. **Worked before/after examples** — at minimum: standard table alignment (AE2 shape minus the warning), multiline word-wrap (AE1), inline-formatting atomicity (AE3), escaped pipes (AE4), empty separator rows (from AE1 fixture).
  5. **Known limitations** — the four-class tokenizer's fallback; the ASCII-dominant width measurement; the no-batch-globs constraint.
  6. **CLI invocation** — a short reference table mapping flags to defaults; full documentation lives in the script's `--help` output.

**Patterns to follow:**
- `references/syntax-reference.md` heading shape and code-block-per-example layout.
- `references/best-practices.md` do/don't snippet style.
- `spec/multiline-cell-extensions.md` for the spec-document tone (RFC 2119 keywords are NOT used here — this is a reference, not a normative spec; the script is the conformance authority).

**Test scenarios:**
- Test expectation: none — pure documentation. Verification is by U6's fixtures matching the worked examples and by `python validate-mdpp.py references/table-formatting.md` passing.
- Manual review check: every default value from R11 is named in the doc; every R1–R10 rule has at least one worked example; every limitation in the brainstorm's Assumptions section is documented.

**Verification:**
- File exists at `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md`.
- All worked examples are byte-identical to their corresponding U6 fixture outputs.
- `validate-mdpp.py` reports zero errors on the file.

---

### U8. Skill guidance: best-practices subsection and SKILL.md cross-reference

**Goal:** Give Claude a short, actionable rule for table edits during in-flow authoring sessions, with a link to the full reference. Add a one-line entry in SKILL.md's references list so the new doc is discoverable from the skill's index. No edit to SKILL.md's `description:` frontmatter — the routing surface is unchanged (no plugin re-trigger needed).

**Requirements:** R19

**Dependencies:** U7

**Files:**
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
- Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`

**Approach:**
- `best-practices.md`: add a new top-level subsection, "Table Formatting" (alongside the existing "When to Use Each Extension" subsections). Three to five paragraphs:
  1. The rule: table edits should produce output matching the formatter's idempotent shape (fixed-width columns, vertically aligned pipes, multiline tables wrap to continuation rows).
  2. Why: read-time and diff-time costs.
  3. How: link to `references/table-formatting.md` for the full rule set; mention `scripts/format-tables.py --in-place` as the canonical enforcement tool.
  4. In-flow guidance for AI agents: when editing a table by hand, match the surrounding column widths; when in doubt, run the formatter.
- `SKILL.md`: add one bullet to the existing `<references>` block:
  - `references/table-formatting.md` — Readable-table conventions and the `format-tables.py` rule set
- No frontmatter `description:` change.

**Test scenarios:**
- Test expectation: none — pure documentation edits. Verification is by review and by the existing auto-activation test suite (`tests/auto-activation/cases.md`) continuing to pass unchanged.
- Manual review check: the new `best-practices.md` subsection follows the existing "Use X for / Avoid X for" do/don't shape used by the surrounding subsections.
- Manual review check: the SKILL.md references list still renders correctly (no broken anchors, no formatting drift from the surrounding bullets).

**Verification:**
- `validate-mdpp.py` reports zero errors on both edited files.
- `SKILL.md`'s references list includes the new entry in alphabetical order alongside the others.

---

### U9. Plugin version bump and changelog entry

**Goal:** Bump the plugin version and record the change in `CHANGELOG.md`. This is the last unit before PR creation per the repo's version-management workflow.

**Requirements:** Repo workflow (CLAUDE.md "Version Management")

**Dependencies:** U8

**Files:**
- Modify: `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (via bump script)
- Modify: `.claude-plugin/marketplace.json` (via bump script)
- Modify: `CHANGELOG.md`

**Approach:**
- Run `scripts/bump-version.sh minor` — new feature added to the skill (new script + new reference doc + new best-practices subsection).
- Add a `CHANGELOG.md` entry under the new version: "Added `format-tables.py` script for deterministic Markdown table reformatting; added `references/table-formatting.md` rule set; added Table Formatting subsection to `references/best-practices.md`. Closes #91."

**Test scenarios:**
- Test expectation: none — version bump and changelog edit. Verification is the bump script's own success exit and a `git diff --stat` showing only the expected files changed.

**Verification:**
- `plugin.json` and `marketplace.json` versions are equal and reflect the bump.
- `CHANGELOG.md` has an entry naming the issue and the three deliverables.

---

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| The four-class tokenizer's fallback to whitespace tokenization mishandles a real-world table during in-flow editing, producing output the formatter then doesn't recognize as already formatted | Medium | Medium | Document the limitation in `references/table-formatting.md`. The standard-table warning at U4 catches the worst case (over-width without wrap). For multiline tables, the worst outcome is a continuation row with a slightly broken inline format — `validate-mdpp.py` will not catch this, but a human reading the rendered output will. |
| ASCII-dominant width measurement undercounts CJK or wide-character content, producing visibly misaligned output for internationalized tables | Low (no current i18n content in repo) | Low (visual only — semantics unchanged) | Document as known limitation in `references/table-formatting.md`. The `wcwidth` deferred work item is the path to resolution if a downstream consumer reports it. |
| `--check` unified diff output is too noisy on large files, drowning out the actual offending row in CI logs | Medium | Low | The unified diff format is the CI-ergonomic choice; if noise becomes a problem, an `--check-summary` flag is a small follow-up. |
| Plugin minor-version bump triggers unrelated downstream churn for skill consumers | Low | Low | The bump is appropriate for a new feature; the published skill description is unchanged. Consumers see new files, not changed behavior in existing files. |
| Idempotency assumption fails on an edge-case input we don't anticipate (e.g., trailing whitespace inside a code span that the tokenizer absorbs differently across runs) | Low | High (breaks the CI use case) | U6's AE5 fixture runs every test fixture twice and asserts byte-equality. Add a fuzzing-light step in the protocol: feed each `examples/` and `spec/` Markdown file through the formatter twice and assert byte-equality. Done as part of U6 verification. |

---

## Documentation Plan

- **`references/table-formatting.md`** (U7) — the canonical rule-set document.
- **`references/best-practices.md`** (U8) — short prescriptive guidance for in-flow authoring.
- **`SKILL.md`** (U8) — one-line cross-reference; no `description:` change.
- **`CHANGELOG.md`** (U9) — release-note entry naming the three deliverables and closing #91.
- **`tests/format-tables-cases.md`** (U6) — manual-verification protocol for AE1–AE7.

---

## Operational / Rollout Notes

- No runtime infrastructure changes. The script runs locally per-author or per-CI-job.
- No coordination required with downstream `epublisher-docs` for v1; that repo can adopt the script after merge.
- A follow-up issue may wire `format-tables.py --check` into this repo's CI on changed `.md` files. Out of scope for this plan.

---

## Open Questions

### Resolved During Planning

- **Script location** (affects R13): Skill-internal `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py`. Same domain as `validate-mdpp.py` and `add-aliases.py`. Top-level `scripts/` is reserved for plugin-infrastructure tooling like `bump-version.sh`.
- **Display-width measurement** (affects R8): Python `len(s)` for v1; `wcwidth` deferred to follow-up. Documented as a limitation in `references/table-formatting.md`.
- **`--col-widths` shape** (affects R12): Comma-separated integers (e.g., `--col-widths 30,12,55`).
- **`proportional` algorithm** (affects R12): `max_line_width − pipe_overhead` distributed by content-length-weighted ratio with `min_col_width` as a floor; remainder round-robin to widest content columns.
- **SKILL guidance surface** (affects R19): `references/best-practices.md` (new subsection) plus a one-line cross-reference in `SKILL.md`'s references list. SKILL.md's `description:` frontmatter is unchanged.
- **`--check` output format** (affects R14): Unified diff via `difflib.unified_diff`. Exit code 4 on mismatch.

### Deferred to Implementation

- **Exact regex for the four-class inline tokenizer**: the brainstorm names the classes; the regexes will be tuned during U4 against the AE3 fixture and adjacent edge cases.
- **Atomic-rename idiom for `--in-place`**: `os.replace` semantics on Windows vs. POSIX is well-known but the temp-file naming convention is left to the implementer.
- **Standard-table warning exact format**: the U4 description names the content; the precise wording (column "header" identification, color codes) is an implementation choice mirroring `validate-mdpp.py`'s style.
- **`--verbose` output's exact wording**: the U5 description names the contents; phrasing is the implementer's call.
- **Whether the AE1 fixture lives inline in `tests/sample-tables-multiline.md` or is split across multiple sample files**: the U6 description allows either; the implementer picks based on what reads cleanly.
