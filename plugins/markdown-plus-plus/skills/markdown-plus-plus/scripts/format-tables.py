#!/usr/bin/env python3
"""
format-tables.py

Reformat Markdown tables (standard and `<!-- multiline -->`) into a
readable, fixed-width column layout suitable for source control diffing
and human review.

Usage:
    python format-tables.py <input_file> [options]

Options:
    --help                  Show this help message
    --in-place              Rewrite the input file with formatted output
    --check                 Exit non-zero with a unified diff if input is
                            not already formatted (does not modify file)
    --max-line-width N      Maximum total line width including pipes (default: 110)
    --max-cell-width N      Maximum characters per cell before wrapping (default: 78)
    --min-col-width N       Minimum column width (default: 3)
    --col-width-strategy S  How to size columns: auto | fixed | proportional (default: auto)
    --col-widths CSV        Comma-separated integer widths for `fixed` strategy
                            (e.g., 30,12,55). Must match every table's column count.
    --verbose               Print effective parameter values to stderr

Exit Codes:
    0 - Success (no changes needed, or changes written successfully)
    1 - File error (not found, not readable, write failure)
    2 - Invalid arguments
    3 - Parse error (malformed table, --col-widths column-count mismatch)
    4 - --check mismatch (file would be reformatted)
"""

import argparse
import difflib
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Optional


# ANSI color codes (mirrors validate-mdpp.py)
class Colors:
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


# ---------------------------------------------------------------------------
# Default configuration values (R11)
# ---------------------------------------------------------------------------

DEFAULT_MAX_LINE_WIDTH = 110
DEFAULT_MAX_CELL_WIDTH = 78
DEFAULT_MIN_COL_WIDTH = 3
DEFAULT_COL_WIDTH_STRATEGY = 'auto'


@dataclass
class FormatterConfig:
    """Effective configuration for one formatter run."""
    max_line_width: int = DEFAULT_MAX_LINE_WIDTH
    max_cell_width: int = DEFAULT_MAX_CELL_WIDTH
    min_col_width: int = DEFAULT_MIN_COL_WIDTH
    col_width_strategy: str = DEFAULT_COL_WIDTH_STRATEGY
    col_widths: Optional[list[int]] = None  # only used when strategy == 'fixed'


# ---------------------------------------------------------------------------
# Block scanner (U2)
# ---------------------------------------------------------------------------

# A row line: starts with optional whitespace and a pipe, ends with a pipe.
TABLE_ROW_RE = re.compile(r'^\s*\|.*\|\s*$')

# Separator row: cells contain only whitespace, dashes, colons, and pipes.
SEPARATOR_RE = re.compile(r'^\s*\|[\s:|\-]+\|\s*$')

# Code fence opening/closing pattern (CommonMark 0.30) -- mirrors validate-mdpp.py.
CODE_FENCE_RE = re.compile(r'^\s{0,3}(`{3,}|~{3,})')

# A line that is *only* a multiline directive (or combined-commands form
# including multiline) and nothing else.
MULTILINE_DIRECTIVE_LINE_RE = re.compile(
    r'^\s*<!--\s*[^>]*?\bmultiline\b[^>]*?-->\s*$'
)

# Cell splitter: split on `|` but not on `\|` (R9).
# Use a regex that matches `|` not preceded by an odd number of backslashes.
# We approximate the simple case: split on `|` not preceded by `\`.
CELL_SPLIT_RE = re.compile(r'(?<!\\)\|')


@dataclass
class TableBlock:
    """A pipe-table block scanned from the source."""
    start_line: int = 0          # 1-based line number of header row
    directive_line: Optional[str] = None  # original directive line, if any
    is_multiline: bool = False
    rows: list[list[str]] = field(default_factory=list)
    separator_cells: list[str] = field(default_factory=list)  # raw separator cells
    raw_lines: list[str] = field(default_factory=list)        # original block lines (for fall-back)


@dataclass
class TextBlock:
    """A non-table block (prose, code fence, HTML, blank lines)."""
    lines: list[str] = field(default_factory=list)


def split_cells(row: str) -> list[str]:
    """
    Split a table row line on unescaped `|`, returning the list of cell
    contents (interior cells only — leading/trailing pipes are stripped).
    """
    # Strip optional leading/trailing whitespace, but preserve interior content.
    stripped = row.rstrip('\n').rstrip('\r')
    parts = CELL_SPLIT_RE.split(stripped)
    # Drop the leading/trailing empty strings that come from the outer pipes.
    if parts and parts[0].strip() == '':
        parts = parts[1:]
    if parts and parts[-1].strip() == '':
        parts = parts[:-1]
    # Trim incidental whitespace around each cell; preserve internal spacing.
    return [c.strip() for c in parts]


def _scan_blocks(lines: list[str]) -> list[object]:
    """
    Walk through the input line-by-line and group it into TableBlock and
    TextBlock instances. Code fences and HTML-like blocks are passed through
    as TextBlock content (R16).

    A table block is detected when:
      - Line N matches TABLE_ROW_RE (header row)
      - Line N+1 matches SEPARATOR_RE (separator row)
    The directive line (if any) is the immediately preceding line that
    matches MULTILINE_DIRECTIVE_LINE_RE.
    """
    blocks: list[object] = []
    text_buf: list[str] = []
    in_fence = False
    fence_char: Optional[str] = None
    fence_count = 0

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Code fence handling: pass through fenced blocks unchanged.
        m = CODE_FENCE_RE.match(line)
        if m:
            char = m.group(1)[0]
            count = len(m.group(1))
            if not in_fence:
                in_fence = True
                fence_char = char
                fence_count = count
                text_buf.append(line)
                i += 1
                continue
            elif char == fence_char and count >= fence_count:
                in_fence = False
                fence_char = None
                fence_count = 0
                text_buf.append(line)
                i += 1
                continue

        if in_fence:
            text_buf.append(line)
            i += 1
            continue

        # Detect table: header row + separator row.
        if (
            TABLE_ROW_RE.match(line)
            and i + 1 < n
            and SEPARATOR_RE.match(lines[i + 1])
        ):
            # Capture preceding directive line if applicable.
            directive_line: Optional[str] = None
            if text_buf and MULTILINE_DIRECTIVE_LINE_RE.match(text_buf[-1]):
                directive_line = text_buf[-1]
                # Pull the directive line out of the text buffer; it now belongs to the table.
                text_buf = text_buf[:-1]
            # Flush text buffer.
            if text_buf:
                blocks.append(TextBlock(lines=text_buf))
                text_buf = []

            tb = TableBlock(
                start_line=i + 1,
                directive_line=directive_line,
                is_multiline=directive_line is not None,
            )
            tb.raw_lines.append(line)
            tb.rows.append(split_cells(line))

            sep_line = lines[i + 1]
            tb.raw_lines.append(sep_line)
            tb.separator_cells = split_cells(sep_line)

            j = i + 2
            while j < n and TABLE_ROW_RE.match(lines[j]) and not CODE_FENCE_RE.match(lines[j]):
                tb.raw_lines.append(lines[j])
                tb.rows.append(split_cells(lines[j]))
                j += 1
            blocks.append(tb)
            i = j
            continue

        text_buf.append(line)
        i += 1

    if text_buf:
        blocks.append(TextBlock(lines=text_buf))
    return blocks


# ---------------------------------------------------------------------------
# Inline tokenizer (U4)
# ---------------------------------------------------------------------------

# Ordered most-specific-first. The first regex that matches wins.
_TOKEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # Compound: **`...`**
    ('compound', re.compile(r'\*\*`[^`]+`\*\*')),
    # Code span (single backtick form)
    ('code', re.compile(r'`[^`]+`')),
    # Bold: **...**
    ('bold', re.compile(r'\*\*[^*]+\*\*')),
    # Italic: *...*
    ('italic_star', re.compile(r'(?<!\*)\*[^*\s][^*]*\*(?!\*)')),
    # Italic: _..._
    ('italic_under', re.compile(r'(?<!_)_[^_\s][^_]*_(?!_)')),
]


@dataclass
class Token:
    text: str
    atomic: bool


def tokenize_inline(text: str) -> list[Token]:
    """
    Tokenize cell text for word-wrap purposes. Recognized inline-formatting
    classes are emitted as atomic tokens. Everything else is split on
    whitespace into word tokens. Whitespace runs are preserved as their own
    (non-atomic) tokens so renderer output matches the wrap algorithm's
    expectations.

    Returns a list of (text, atomic) tokens.
    """
    tokens: list[Token] = []
    i = 0
    n = len(text)

    # We scan character by character. At each position we check if any atomic
    # pattern matches. If so, emit it and skip past. Otherwise, walk the
    # current run of plain text until the next atomic match begins.
    while i < n:
        # Try atomic match at position i.
        atomic_match = None
        for _name, pat in _TOKEN_PATTERNS:
            m = pat.match(text, i)
            if m:
                atomic_match = m
                break
        if atomic_match:
            tokens.append(Token(atomic_match.group(0), atomic=True))
            i = atomic_match.end()
            continue

        # Find the next atomic match start, if any.
        next_start = n
        for _name, pat in _TOKEN_PATTERNS:
            m = pat.search(text, i)
            if m and m.start() < next_start:
                next_start = m.start()

        plain = text[i:next_start]
        # Split plain into whitespace-delimited tokens, preserving the
        # whitespace runs as their own (non-atomic) tokens. This makes wrap
        # decisions explicit.
        for part in re.findall(r'\s+|\S+', plain):
            tokens.append(Token(part, atomic=False))
        i = next_start

    return tokens


def wrap_tokens(tokens: list[Token], width: int) -> list[str]:
    """
    Greedy word-wrap. Returns a list of line strings, each <= width except
    when a single atomic token alone exceeds width (in which case that line
    contains only the atomic token, and the renderer is expected to widen
    the column locally).

    Whitespace tokens are absorbed at line boundaries (they don't appear at
    the start of a continuation line).
    """
    if width <= 0:
        width = 1

    lines: list[str] = []
    current = ''

    def flush():
        nonlocal current
        if current != '':
            lines.append(current.rstrip())
            current = ''

    for tok in tokens:
        if tok.text.isspace():
            # Only add whitespace if we already have content on this line.
            if current:
                # Collapse internal whitespace runs to a single space.
                if not current.endswith(' '):
                    current += ' '
            # Otherwise, drop leading whitespace.
            continue

        # Non-whitespace token. Will it fit?
        candidate = current + tok.text if current else tok.text
        if len(candidate) <= width:
            current = candidate
            continue

        # Token doesn't fit on current line.
        if current:
            # Flush current line, start a new one with this token.
            flush()
            if len(tok.text) <= width or tok.atomic:
                current = tok.text
            else:
                # Plain (non-atomic) token longer than width: hard-break it.
                # Emit lines of width chars.
                t = tok.text
                while len(t) > width:
                    lines.append(t[:width])
                    t = t[width:]
                current = t
        else:
            # No current content; token itself is bigger than width.
            if tok.atomic:
                # Emit it on its own line. The renderer detects this and
                # locally widens the column for that single row.
                lines.append(tok.text)
            else:
                t = tok.text
                while len(t) > width:
                    lines.append(t[:width])
                    t = t[width:]
                current = t

    flush()
    return lines


# ---------------------------------------------------------------------------
# Width planner (U3, U5)
# ---------------------------------------------------------------------------

def _alignment_marker(separator_cell: str) -> str:
    """
    Read the alignment marker from a separator cell ('---', ':---', '---:',
    ':---:'). Returns one of: 'left', 'right', 'center', 'none'.
    """
    s = separator_cell.strip()
    starts = s.startswith(':')
    ends = s.endswith(':')
    if starts and ends:
        return 'center'
    if ends:
        return 'right'
    if starts:
        return 'left'
    return 'none'


def _format_separator_cell(width: int, alignment: str) -> str:
    """
    Render a separator cell of the requested visible width with the given
    alignment markers. Visible width = inner cell width (excludes the
    surrounding ' ' padding spaces and pipe characters).

    For width=3 with alignment 'left', returns ':--'.
    For width=3 with alignment 'right', returns '--:'.
    For width=3 with alignment 'center', returns ':-:' (when width >= 3).
    For width=3 with alignment 'none', returns '---'.

    Width is clamped to a minimum that can still carry the alignment marker.
    """
    if alignment == 'center':
        if width < 3:
            width = 3
        return ':' + ('-' * (width - 2)) + ':'
    if alignment == 'left':
        if width < 2:
            width = 2
        return ':' + ('-' * (width - 1))
    if alignment == 'right':
        if width < 2:
            width = 2
        return ('-' * (width - 1)) + ':'
    # none
    if width < 1:
        width = 1
    return '-' * width


def _is_blank_row(cells: list[str]) -> bool:
    return all(c.strip() == '' for c in cells)


def plan_widths(table: TableBlock, config: FormatterConfig) -> list[int]:
    """
    Compute per-column widths for a table according to the configured
    strategy. Returns a list of inner column widths (cell content area,
    excluding the surrounding ' ' padding and pipes).

    Strategies:
      - auto: max(content len) clamped to max_cell_width, with min_col_width
              floor. Header text length also serves as a floor.
      - fixed: user-supplied widths (config.col_widths); column count must
               match the table.
      - proportional: distribute (max_line_width - overhead) across columns
                      by ratio of total content length per column, with
                      min_col_width floor.
    """
    if not table.rows:
        return []
    n_cols = len(table.rows[0])

    # Pad shorter rows with empty cells for column-count consistency.
    for r in table.rows:
        while len(r) < n_cols:
            r.append('')

    # Default: auto.
    strategy = config.col_width_strategy

    if strategy == 'fixed':
        if config.col_widths is None:
            raise ValueError(
                "--col-width-strategy fixed requires --col-widths"
            )
        if len(config.col_widths) != n_cols:
            raise ValueError(
                f"--col-widths has {len(config.col_widths)} value(s), "
                f"but the table at line {table.start_line} has {n_cols} column(s)"
            )
        widths = [max(w, config.min_col_width) for w in config.col_widths]
        return widths

    # Compute content lengths per column.
    # For multiline tables, row content is wrapped, so column width is
    # capped by max_cell_width. For standard tables, the actual cell length
    # may exceed max_cell_width; we don't truncate (R7).
    header = table.rows[0]
    data_rows = table.rows[1:]

    if strategy == 'proportional':
        # Total content length per column (sum of all cells).
        sums = [0] * n_cols
        for row in table.rows:
            for c, cell in enumerate(row):
                sums[c] += len(cell)
        total = sum(sums) or 1
        # Overhead per row: '| ' for first cell, ' | ' between cells, ' |' at end
        # = 2 + 3*(n-1) + 2 = 3*n + 1 chars (border pipes + interior pipes + padding).
        overhead = 3 * n_cols + 1
        available = max(config.max_line_width - overhead, n_cols * config.min_col_width)
        # Distribute by ratio.
        raw = [available * sums[c] / total for c in range(n_cols)]
        widths = [max(int(round(r)), config.min_col_width) for r in raw]
        # Round-robin remainder to widest content columns.
        remainder = available - sum(widths)
        if remainder > 0:
            order = sorted(range(n_cols), key=lambda c: -sums[c])
            i = 0
            while remainder > 0:
                widths[order[i % n_cols]] += 1
                remainder -= 1
                i += 1
        return widths

    # auto
    widths = [config.min_col_width] * n_cols
    for c in range(n_cols):
        # Header text length is a floor (so headers always fit).
        widths[c] = max(widths[c], len(header[c]))
        # Then take max content length up to max_cell_width.
        max_content = 0
        for row in table.rows:
            cell = row[c] if c < len(row) else ''
            max_content = max(max_content, len(cell))
        if table.is_multiline:
            # For multiline tables, wrapping handles overflow; cap at max_cell_width.
            widths[c] = max(widths[c], min(max_content, config.max_cell_width))
        else:
            # For standard tables, columns expand to fit the content (R7).
            widths[c] = max(widths[c], max_content)
        widths[c] = max(widths[c], config.min_col_width)
    return widths


# ---------------------------------------------------------------------------
# Renderer (U3, U4)
# ---------------------------------------------------------------------------

def _render_cell(cell: str, width: int) -> str:
    """Render a single cell padded to the given inner width."""
    return cell + (' ' * (width - len(cell)))


def _render_row(cells: list[str], widths: list[int]) -> str:
    """Render one fully aligned row line."""
    parts = []
    for c, cell in enumerate(cells):
        parts.append(_render_cell(cell, widths[c]))
    return '| ' + ' | '.join(parts) + ' |'


def render_standard(
    table: TableBlock,
    widths: list[int],
    config: FormatterConfig,
) -> tuple[list[str], list[str]]:
    """
    Render a standard (non-multiline) table. Returns (output_lines, warnings).
    Each output line is a complete row, including the separator. Empty rows
    (all whitespace cells) are preserved with whitespace-only cells padded
    to full column width (R3).

    Cells exceeding max_cell_width emit a stderr warning (R7) but render at
    actual width without truncation.
    """
    out: list[str] = []
    warnings: list[str] = []
    n_cols = len(widths)

    # Header row.
    header = list(table.rows[0])
    while len(header) < n_cols:
        header.append('')
    out.append(_render_row(header, widths))

    # Separator row: derive alignments from the original separator cells.
    alignments = [_alignment_marker(c) for c in table.separator_cells]
    while len(alignments) < n_cols:
        alignments.append('none')
    sep_cells = [
        _format_separator_cell(widths[c], alignments[c])
        for c in range(n_cols)
    ]
    out.append(_render_row(sep_cells, widths))

    # Data rows.
    for r_idx, row in enumerate(table.rows[1:], start=2):
        # Pad row to column count.
        cells = list(row)
        while len(cells) < n_cols:
            cells.append('')

        if _is_blank_row(cells):
            # Preserve as whitespace-only padded row (R3).
            out.append(_render_row(['' for _ in widths], widths))
            continue

        # Standard-table over-width warning (R7).
        for c, cell in enumerate(cells):
            if len(cell) > config.max_cell_width:
                header_label = table.rows[0][c] if c < len(table.rows[0]) else f'col {c+1}'
                warnings.append(
                    f"WARNING: cell exceeds max_cell_width "
                    f"({len(cell)} chars > {config.max_cell_width}) "
                    f"at row {r_idx}, column {c+1} (\"{header_label}\")"
                )
        out.append(_render_row(cells, widths))

    return out, warnings


def render_multiline(
    table: TableBlock,
    widths: list[int],
    config: FormatterConfig,
) -> tuple[list[str], list[str]]:
    """
    Render a multiline table. Long cell content wraps to continuation rows
    (R6) using inline-formatting-aware tokenization (R8). When a single
    atomic token exceeds the planned column width, that one continuation
    row is emitted with the column locally widened to fit the token; other
    rows in the table keep their planned width.

    The directive line (if any) is emitted verbatim above the table (R4).
    """
    out: list[str] = []
    warnings: list[str] = []
    n_cols = len(widths)

    if table.directive_line is not None:
        out.append(table.directive_line)

    # Header row (no wrapping for the header — headers should fit by design).
    header = list(table.rows[0])
    while len(header) < n_cols:
        header.append('')
    out.append(_render_row(header, widths))

    # Separator row.
    alignments = [_alignment_marker(c) for c in table.separator_cells]
    while len(alignments) < n_cols:
        alignments.append('none')
    sep_cells = [
        _format_separator_cell(widths[c], alignments[c])
        for c in range(n_cols)
    ]
    out.append(_render_row(sep_cells, widths))

    # Data rows.
    for row in table.rows[1:]:
        cells = list(row)
        while len(cells) < n_cols:
            cells.append('')

        if _is_blank_row(cells):
            out.append(_render_row(['' for _ in widths], widths))
            continue

        # Wrap each cell.
        wrapped: list[list[str]] = []
        for c, cell in enumerate(cells):
            if cell == '':
                wrapped.append([''])
                continue
            tokens = tokenize_inline(cell)
            lines = wrap_tokens(tokens, widths[c])
            if not lines:
                lines = ['']
            wrapped.append(lines)

        max_lines = max(len(w) for w in wrapped)

        for line_idx in range(max_lines):
            row_cells: list[str] = []
            row_widths: list[int] = []
            for c in range(n_cols):
                if line_idx < len(wrapped[c]):
                    cell_text = wrapped[c][line_idx]
                else:
                    cell_text = ''
                # Local column widening when an atomic token overflows.
                effective_width = max(widths[c], len(cell_text))
                row_cells.append(cell_text)
                row_widths.append(effective_width)
            out.append(_render_row(row_cells, row_widths))

    return out, warnings


# ---------------------------------------------------------------------------
# Top-level formatter (U2-U5)
# ---------------------------------------------------------------------------

def _detect_newline(text: str) -> str:
    """
    Detect the predominant line ending style. Returns '\\r\\n' if the text
    contains any CRLF line endings, otherwise '\\n'. A file with no line
    endings at all is treated as LF.
    """
    return '\r\n' if '\r\n' in text else '\n'


def format_text(text: str, config: FormatterConfig) -> tuple[str, list[str]]:
    """
    Format the input Markdown text. Returns (formatted_text, warnings).
    Non-table content is passed through byte-for-byte (R16). The returned
    text preserves the original trailing-newline state and the original
    line-ending style (CRLF vs LF).
    """
    newline = _detect_newline(text)
    # Normalize internal representation to LF-only for processing.
    has_trailing_newline = text.endswith('\n')
    normalized = text.replace('\r\n', '\n')
    if normalized.endswith('\n'):
        body = normalized[:-1]
    else:
        body = normalized
    lines = body.split('\n') if body != '' else []

    blocks = _scan_blocks(lines)

    out_lines: list[str] = []
    all_warnings: list[str] = []

    for block in blocks:
        if isinstance(block, TextBlock):
            out_lines.extend(block.lines)
            continue

        # TableBlock
        widths = plan_widths(block, config)
        if block.is_multiline:
            rendered, warnings = render_multiline(block, widths, config)
        else:
            rendered, warnings = render_standard(block, widths, config)
        out_lines.extend(rendered)
        all_warnings.extend(warnings)

    formatted = '\n'.join(out_lines)
    if has_trailing_newline:
        formatted += '\n'
    if newline != '\n':
        formatted = formatted.replace('\n', newline)
    return formatted, all_warnings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_col_widths(value: str) -> list[int]:
    """Parse a comma-separated integer list (used by --col-widths)."""
    parts = [p.strip() for p in value.split(',') if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError(
            "--col-widths must be a comma-separated list of integers"
        )
    out: list[int] = []
    for p in parts:
        if not p.lstrip('-').isdigit() or int(p) <= 0:
            raise argparse.ArgumentTypeError(
                f"--col-widths value '{p}' is not a positive integer"
            )
        out.append(int(p))
    return out


def write_atomic(path: str, content: str) -> None:
    """
    Write `content` to `path` atomically: write to a temp file in the same
    directory, then `os.replace`. This prevents leaving a partial file on
    SIGINT mid-write.
    """
    directory = os.path.dirname(os.path.abspath(path)) or '.'
    fd, tmp = tempfile.mkstemp(
        prefix=os.path.basename(path) + '.',
        suffix='.tmp',
        dir=directory,
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reformat Markdown tables (standard and multiline) into "
            "fixed-width vertically aligned columns."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0  Success
  1  File error (not found, not readable, write failure)
  2  Invalid arguments
  3  Parse error (--col-widths column count mismatch, etc.)
  4  --check mismatch (file would be reformatted)

Examples:
  python format-tables.py document.md
  python format-tables.py document.md --in-place
  python format-tables.py document.md --check
  python format-tables.py document.md --max-line-width 120 --max-cell-width 60
  python format-tables.py document.md --col-width-strategy fixed --col-widths 30,12,55
  python format-tables.py document.md --col-width-strategy proportional
"""
    )
    parser.add_argument('input_file', help='Markdown file to format')
    parser.add_argument('--in-place', '-i', action='store_true',
                        help='Rewrite the input file with formatted output')
    parser.add_argument('--check', action='store_true',
                        help='Exit non-zero with a unified diff if input is not already formatted')
    parser.add_argument('--max-line-width', type=int, default=DEFAULT_MAX_LINE_WIDTH,
                        help=f'Maximum total line width (default: {DEFAULT_MAX_LINE_WIDTH})')
    parser.add_argument('--max-cell-width', type=int, default=DEFAULT_MAX_CELL_WIDTH,
                        help=f'Maximum cell width before wrapping (default: {DEFAULT_MAX_CELL_WIDTH})')
    parser.add_argument('--min-col-width', type=int, default=DEFAULT_MIN_COL_WIDTH,
                        help=f'Minimum column width (default: {DEFAULT_MIN_COL_WIDTH})')
    parser.add_argument(
        '--col-width-strategy',
        choices=['auto', 'fixed', 'proportional'],
        default=DEFAULT_COL_WIDTH_STRATEGY,
        help=f'Column-width strategy (default: {DEFAULT_COL_WIDTH_STRATEGY})',
    )
    parser.add_argument('--col-widths', type=parse_col_widths, default=None,
                        help='Comma-separated integer widths (e.g., 30,12,55) for `fixed` strategy')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print effective parameter values to stderr')

    args = parser.parse_args()

    if args.in_place and args.check:
        print(
            f"{Colors.RED}Error:{Colors.NC} --in-place and --check are mutually exclusive",
            file=sys.stderr,
        )
        return 2

    if args.col_widths is not None and args.col_width_strategy != 'fixed':
        print(
            f"{Colors.YELLOW}Warning:{Colors.NC} --col-widths is ignored "
            f"unless --col-width-strategy fixed is set",
            file=sys.stderr,
        )

    if not os.path.exists(args.input_file):
        print(
            f"{Colors.RED}Error:{Colors.NC} File not found: {args.input_file}",
            file=sys.stderr,
        )
        return 1

    try:
        with open(args.input_file, 'r', encoding='utf-8', newline='') as f:
            original = f.read()
    except Exception as e:
        print(
            f"{Colors.RED}Error:{Colors.NC} Cannot read file: {e}",
            file=sys.stderr,
        )
        return 1

    config = FormatterConfig(
        max_line_width=args.max_line_width,
        max_cell_width=args.max_cell_width,
        min_col_width=args.min_col_width,
        col_width_strategy=args.col_width_strategy,
        col_widths=args.col_widths,
    )

    if args.verbose:
        print(
            f"{Colors.CYAN}Effective parameters:{Colors.NC} "
            f"max_line_width={config.max_line_width}, "
            f"max_cell_width={config.max_cell_width}, "
            f"min_col_width={config.min_col_width}, "
            f"col_width_strategy={config.col_width_strategy}"
            + (
                f", col_widths={','.join(str(w) for w in config.col_widths)}"
                if config.col_widths is not None
                else ''
            ),
            file=sys.stderr,
        )

    try:
        formatted, warnings = format_text(original, config)
    except ValueError as e:
        print(
            f"{Colors.RED}Error:{Colors.NC} {e}",
            file=sys.stderr,
        )
        return 3

    for w in warnings:
        print(f"{Colors.YELLOW}{w}{Colors.NC}", file=sys.stderr)

    if args.check:
        if formatted == original:
            return 0
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            formatted.splitlines(keepends=True),
            fromfile=args.input_file,
            tofile=args.input_file + ' (formatted)',
        )
        sys.stdout.write(''.join(diff))
        return 4

    if args.in_place:
        if formatted == original:
            return 0
        try:
            write_atomic(args.input_file, formatted)
        except Exception as e:
            print(
                f"{Colors.RED}Error:{Colors.NC} Cannot write file: {e}",
                file=sys.stderr,
            )
            return 1
        if args.verbose:
            print(
                f"{Colors.GREEN}Reformatted:{Colors.NC} {args.input_file}",
                file=sys.stderr,
            )
        return 0

    # Default: write to stdout. Use binary write to preserve the exact
    # byte stream regardless of platform line-ending translation in the
    # text-mode stdout layer.
    try:
        sys.stdout.flush()
        sys.stdout.buffer.write(formatted.encode('utf-8'))
        sys.stdout.buffer.flush()
    except BrokenPipeError:
        # Downstream consumer (e.g., `head`) closed the pipe early.
        # Suppress Python's default traceback and exit cleanly.
        try:
            sys.stdout.close()
        except Exception:
            pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
