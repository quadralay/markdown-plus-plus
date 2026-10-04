---
title: Build markdown-table formatters for source-control friendliness, not pretty-printing
date: 2026-05-09
category: tooling-decisions
module: plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts
problem_type: tooling_decision
component: tooling
severity: medium
applies_when:
  - Building or revising a tool that rewrites Markdown source files in place
  - Defining a "readable" shape for tables in a documentation repo
  - Designing CLI tools that may be invoked by Windows authors and Linux CI
  - Choosing between an external dependency and an in-repo stdlib script
  - Adding a `--check` mode for use in pre-commit hooks or CI gates
tags:
  - markdown
  - table-formatting
  - cross-platform
  - idempotency
  - cli-design
  - python-stdlib
  - tooling
  - markdown-plus-plus
---

# Build markdown-table formatters for source-control friendliness, not pretty-printing

## Context

Markdown++ tables authored by hand or migrated from other formats arrive
with inconsistent column widths and long single-line cells. They render
fine in HTML, but the *source* form is hostile to the workflows that
matter most to a documentation repo: editor reading, PR review, and
version-control diffs. A one-character edit to a long cell rewrites the
entire row in `git diff`; a long row off-screen forces side-scrolling
during code review. Issue #91 asked for a capability to reformat both
standard and `<!-- multiline -->` tables into a consistent readable
shape, with the design constraint that the tool must run on Windows
authoring machines and Linux CI alike.

A pretty-printer that produces visually nicer output but breaks
idempotency, mangles line endings, or hides edge cases as silent failures
is worse than no tool at all -- it weaponizes itself against the
diff-friendliness it was supposed to deliver.

## Guidance

When building a Markdown table formatter (or any tool that rewrites
documentation source in place), make the following choices up-front
rather than discovering them as bugs:

**1. Stdlib-only Python beats an external dependency.**
A formatter that runs from `python scripts/format-tables.py` with no
`pip install` step is invokable from any agent, any CI image, and any
contributor's machine without setup friction. The `markdown-plus-plus`
skill ships `format-tables.py` as Python 3 stdlib only -- no PyYAML, no
`mistune`, no `markdown-it-py`. The cost is reimplementing a small inline
tokenizer; the benefit is zero supply-chain surface and zero install
friction for downstream consumers who only need to format their own
tables.

**2. Preserve the source file's line-ending style.**
This is the bug that almost shipped. On Windows, Python's text-mode
stdout silently translates `\n` to `\r\n`, and an `--in-place` round
trip on an LF file rewrote it as CRLF -- byte-different, idempotency
broken. The fix:

```python
def _detect_newline(text: str) -> str:
    return '\r\n' if '\r\n' in text else '\n'

# Read with newline='' so Python doesn't normalize on input:
with open(path, 'r', encoding='utf-8', newline='') as f:
    original = f.read()

# Write with newline='' (or via sys.stdout.buffer for stdout) so Python
# doesn't translate on output:
sys.stdout.buffer.write(formatted.encode('utf-8'))
```

The detector picks the predominant style; the read/write paths suppress
Python's auto-translation on both ends. Without the binary stdout path,
piping `format-tables.py file.md > file.md.new` on Windows produces a
file that fails its own `--check`.

**3. Use atomic write for `--in-place`.**

```python
fd, tmp = tempfile.mkstemp(prefix=basename + '.', suffix='.tmp', dir=dirname)
with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
    f.write(content)
os.replace(tmp, path)
```

`os.replace` is atomic on POSIX and Windows. A `Ctrl-C` mid-write can no
longer leave a half-written `.md` file in the user's editor. **Known
gap:** the temp file inherits `mkstemp`'s 0600 mode rather than the
original file's mode, so an `--in-place` rewrite of a 0644 file silently
becomes 0600 on Linux. If you adopt this pattern, also `os.chmod()` the
temp file (or use `shutil.copymode()`) before `os.replace`.

**4. Tokenize inline formatting as atomic units before word-wrap.**
A naive word-wrap on a multiline-table cell will happily split
`` `code-span` ``, `**bold**`, or `` **`compound`** `` mid-token,
producing rendering bugs that vary by Markdown processor. Tokenize first
with most-specific-first regex ordering:

```python
_TOKEN_PATTERNS = [
    ('compound', re.compile(r'\*\*`[^`]+`\*\*')),  # match before `code` or `**bold**`
    ('code',     re.compile(r'`[^`]+`')),
    ('bold',     re.compile(r'\*\*[^*]+\*\*')),
    ('italic_star',  re.compile(r'(?<!\*)\*[^*\s][^*]*\*(?!\*)')),
    ('italic_under', re.compile(r'(?<!_)_[^_\s][^_]*_(?!_)')),
]
```

When an atomic token is wider than the planned column, the renderer
**locally widens** that one row's column rather than hard-breaking the
token. Document this as an explicit behavior, not an accident -- a
reader seeing a single row wider than the rest needs to understand it
is intentional.

**Superseded in #120/#121 (2026-07-05).** The four-class atomic set
(compound/code/bold/italic) was too narrow and the per-row local widening
misaligned pipes. #120/#121 extended the atomic classes to also cover
inline links `[t](u)`, reference links `[t][ref]`, bare URLs
(`https?://`, `file://`, `mailto:`), full HTML/directive comments, and
whole same-line inline condition spans, plus a **glue rule** that fuses a
directive comment to an immediately adjacent following token so an inline
style is never split from what it styles. The per-row local widening was
replaced by a **soft width rule**: each multiline column is floored at
its widest atomic token (or verbatim in-cell fence line), so the *whole*
column widens and pipes align on every row; when the capped widths still
overrun `--max-line-width` the columns shrink toward those floors until
the line fits. The original text above is kept as the historical record
of the first implementation; the current rules live in
`references/table-formatting.md` R5 and R8.

**5. Define `--check` with a unique exit code distinct from generic
errors.** `format-tables.py --check` exits **4** on diff mismatch, not
1. Generic file errors are 1, argparse errors are 2, parse errors are 3,
diff-mismatch is 4. A pre-commit hook or CI gate can distinguish "the
tool crashed" from "the file needs reformatting" without parsing
stderr. The cost is one line of documentation; the benefit is automation
that doesn't conflate these cases.

**6. Pass non-table content through byte-for-byte.** Walk the input
line-by-line, group it into `TableBlock` and `TextBlock` instances, and
emit text blocks unchanged. Code fences, HTML blocks, prose, and YAML
frontmatter must round-trip identically. The block scanner detects code
fences by the CommonMark 0.30 rule (`^\s{0,3}(\`{3,}|~{3,})`) so that a
pipe table inside a fenced code block is *not* reformatted.

**7. Idempotency is the test that catches everything.**
The single most useful regression check is: format the file, format it
again, byte-compare. This catches the CRLF bug, the silent column-shrink
bug under `auto` strategy, the trailing-whitespace bug, and any future
regression in the renderer. Run it across every Markdown file in
`examples/` and `spec/` as a fuzz pass before shipping.

## Why This Matters

Documentation tooling that rewrites source has a higher correctness bar
than tooling that produces output (HTML, PDF). A buggy HTML renderer
shows wrong output until you fix it; a buggy in-place formatter
**corrupts your source file** and the corruption ships in the next
commit. Three categories of bug are particularly insidious:

- **Cross-platform divergence.** A formatter that works on the author's
  Mac and corrupts files on a Windows contributor's machine creates a
  trust failure that's hard to recover from. `--in-place` must be
  byte-identical across platforms. CRLF/LF handling is the most common
  failure mode; preserve, don't normalize.
- **Non-idempotency.** If `format` then `format` produces different
  output, the formatter cannot be safely run in CI or pre-commit. Every
  contributor will see "format" diffs they didn't introduce.
- **Silent edge-case failures.** Tables with extra cells in a row,
  Windows paths with even backslash counts in cells, BOMs at the top of
  the file, or mid-table `<!-- multiline -->` directives can each
  produce wrong output without any error. A pretty-printer that fails
  loudly is recoverable; one that fails silently is a time bomb.

These constraints are what separate a tool you can wire into
`pre-commit` from a tool that authors run defensively once and abandon.

## When to Apply

- When building any tool in the `markdown-plus-plus` skill that rewrites
  Markdown files (current and future formatters, alias-injectors,
  link-rewriters, version-bumpers)
- When choosing between adopting an external library and writing a
  small stdlib script for a documentation-repo capability
- When designing a `--check` mode for any tool intended for CI use
- When the tool will be invoked from Windows authoring environments

This guidance is **not** universally applicable to all CLI tools.
External dependencies are the right call when the surface area is
large (full Markdown parser, full YAML serializer); stdlib-only is the
right call when the surface area is bounded and the install friction
matters more than the line count saved.

## Examples

**Cross-platform idempotency contract.**

```python
def format_text(text: str, config: FormatterConfig) -> tuple[str, list[str]]:
    newline = _detect_newline(text)
    has_trailing_newline = text.endswith('\n')
    normalized = text.replace('\r\n', '\n')
    # ... do all work on LF-normalized text ...
    formatted = '\n'.join(out_lines)
    if has_trailing_newline:
        formatted += '\n'
    if newline != '\n':
        formatted = formatted.replace('\n', newline)
    return formatted, all_warnings
```

The boundary discipline: **detect on read, normalize internally, restore
on write**. Applies equally to line endings, trailing whitespace, BOM
preservation, and any other byte-level convention the file carries.

**Distinct exit codes for `--check`.**

```bash
format-tables.py file.md --check
# exit 0: already formatted
# exit 1: file not found / not readable
# exit 2: bad arguments
# exit 3: parse error (e.g., --col-widths column-count mismatch)
# exit 4: would reformat -- diff written to stdout
```

A `pre-commit` hook can react: exit 4 -> instruct the user to run
`--in-place`; any other non-zero -> show the stderr and stop.

## Known Limitations (residual review findings)

These were surfaced by `ce-code-review` on the initial implementation
and are routed for future work; documented here so the next contributor
doesn't re-discover them:

- **`auto` strategy is non-idempotent on multiline tables that wrap
  when `--max-cell-width` is below the original cell length.**
  `plan_widths` reads the wrapped cell on the second pass and shrinks
  the column. Workaround for now: use `--col-width-strategy fixed
  --col-widths ...` for tables that hit this case. **Still open after
  #120/#121.** The wrap *corruption* those issues targeted (links split
  at spaces, long URLs hard-broken mid-character, dropped list/blockquote
  continuation indentation) is resolved -- links/URLs and directive
  comments are now atomic, and `wrap_cell` re-prefixes list/blockquote
  continuations. The residual fragment-shrink re-flow is a plain
  auto-strategy limitation, not corruption; the idempotency sweep exempts
  the two specimens that exhibit it via
  `tests/format-tables/idempotency-allowlist.txt`, and each case's golden
  pins the deterministic single-pass output.
- **Links, bare URLs, and structure split when wrapping multiline cells
  (#120) / directive comments split and inline styles detached (#121).**
  The original tokenizer wrapped `[text](url)`, `https://…`, list
  markers, blockquotes, and `<!-- … -->` directives as plain
  whitespace-delimited text, so wrapping a `<!-- multiline -->` cell
  could break a link, hard-break a URL mid-character, drop list/blockquote
  continuation indentation, or detach an inline style from its target.
  **Resolved in #120/#121:** links, reference links, bare URLs, HTML/
  directive comments, and whole same-line condition spans are atomic;
  a glue rule keeps a directive fused to its adjacent styled element;
  `detect_content_prefix` preserves list/blockquote continuation
  indentation; and in-cell fenced code is emitted verbatim. Over-budget
  inline links are additionally rewritten to reference form with the
  definition emitted after the table (outside any condition span).
- **`IndexError` when a row has more cells than the header.** The
  renderer indexes `widths[c]` past the end. Add column-count
  validation before render. **Resolved:** the column count now comes
  from the widest row rather than the header, via
  `TableBlock.normalize_columns()`, so the surplus cell widens the
  table -- header and separator included -- and every per-column list
  is sized for it. The multiline path reached the count a second time
  in `rewrite_table_links()` (the fence-flag matrix) and crashed there
  before width planning ran; both sites share the one normalizer now.
- **Cell-split regex misses escaped pipes after even backslash counts**
  (e.g., `C:\\path\\|\\thing`). Use a stateful split rather than a
  lookbehind regex.
- **Mid-table `<!-- multiline -->` directives silently split the
  table.** The block scanner closes the table at the directive line;
  rows below render as raw prose. Either reject mid-table directives
  with a parse error or treat them as in-table comments. **Resolved in
  #122** as pass-through comment members: any full-line HTML comment
  mid-table (a stray directive, or the spec's condition open/close tags
  wrapping complete rows) is preserved byte-verbatim in place with row
  accumulation continuing past it and widths planned across both sides,
  except that a `<!-- multiline -->` line immediately followed by a
  header row and a separator row still closes the block to open a new
  adjacent table.
- **UTF-8 BOM defeats table detection.** Open with `utf-8-sig` to strip
  on read, then preserve-or-not on write per a config flag.
- **Atomic write does not preserve original file mode** (becomes 0600
  on Linux). Add `os.chmod` or `shutil.copymode` before `os.replace`.

## Related

- [`scripts/format-tables.py`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/format-tables.py)
  -- the formatter implementation
- [`references/table-formatting.md`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/table-formatting.md)
  -- the R1-R10 rule set and worked examples
- [`tests/format-tables-cases.md`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/format-tables-cases.md)
  -- AE1-AE7 acceptance protocol
- Issue #91 -- original capability request and "Desired Behavior"
  byte-for-byte target
