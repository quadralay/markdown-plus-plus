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

# A line that is *only* a full-line HTML comment (e.g. a condition open/close
# tag or a stray directive). Inside a table run these are pass-through member
# lines: preserved byte-verbatim in place with row accumulation continuing
# past them (issue #122).
COMMENT_LINE_RE = re.compile(r'^\s*<!--.*-->\s*$')

# Cell splitter: split on `|` but not on `\|` (R9).
# Use a regex that matches `|` not preceded by an odd number of backslashes.
# We approximate the simple case: split on `|` not preceded by `\`.
CELL_SPLIT_RE = re.compile(r'(?<!\\)\|')


@dataclass
class TableBlock:
    """A pipe-table block scanned from the source.

    `members` is the ordered body of the block: each entry is either
    ('row', cells) for a genuine data row (header included) or
    ('comment', raw_line) for a full-line HTML comment that is passed
    through byte-verbatim in place (issue #122). Width planning considers
    only the 'row' members; renderers walk `members` in order so comment
    lines land at their original position.
    """
    start_line: int = 0          # 1-based line number of header row
    directive_line: Optional[str] = None  # original directive line, if any
    is_multiline: bool = False
    members: list[tuple] = field(default_factory=list)
    separator_cells: list[str] = field(default_factory=list)  # raw separator cells

    @property
    def rows(self) -> list[list[str]]:
        """The genuine data rows (header + data), comment members excluded."""
        return [cells for kind, cells in self.members if kind == 'row']


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
            tb.members.append(('row', split_cells(line)))

            sep_line = lines[i + 1]
            tb.separator_cells = split_cells(sep_line)

            j = i + 2
            while j < n and not CODE_FENCE_RE.match(lines[j]):
                if TABLE_ROW_RE.match(lines[j]):
                    tb.members.append(('row', split_cells(lines[j])))
                    j += 1
                    continue
                if COMMENT_LINE_RE.match(lines[j]):
                    # A full-line comment mid-table is a pass-through member,
                    # UNLESS it is a multiline directive that opens a brand-new
                    # adjacent table (directive + header + separator ahead), in
                    # which case the current table closes here (issue #122).
                    if (
                        MULTILINE_DIRECTIVE_LINE_RE.match(lines[j])
                        and j + 2 < n
                        and TABLE_ROW_RE.match(lines[j + 1])
                        and SEPARATOR_RE.match(lines[j + 2])
                    ):
                        break
                    tb.members.append(('comment', lines[j]))
                    j += 1
                    continue
                break
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

# Ordered most-specific-first. The first regex that matches wins. Classes
# added for #120 (links, bare URLs) and #121 (HTML comments / directives,
# inline condition spans) are listed before the older inline-formatting
# classes so a comment or link is never mis-tokenized as bold/italic/code.
_TOKEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # WHOLE inline condition span: <!--condition:expr-->...<!--/condition-->
    # opening and closing on the SAME physical line (no newline inside). The
    # entire span is atomic (#121 item 4) -- a wrap point anywhere inside it
    # would create a cross-line raw-text span that Phase 1 removal corrupts.
    ('condition_span',
     re.compile(r'<!--\s*condition:[^>]*?-->.*?<!--\s*/condition\s*-->')),
    # Markdown inline link: [text](url) -- brackets may not nest a ']'.
    ('link_inline', re.compile(r'\[[^\]]*\]\([^)\s]*\)')),
    # Markdown reference link: [text][ref] (and the shortcut/collapsed forms
    # [text][] ). Link-reference *definitions* never appear inside cells.
    ('link_ref', re.compile(r'\[[^\]]*\]\[[^\]]*\]')),
    # Bare URL: http(s)://, file://, mailto: -- runs to the next whitespace.
    ('url', re.compile(r'(?:https?://|file://|mailto:)\S+')),
    # Full HTML comment (covers directive comments and plain comments).
    ('comment', re.compile(r'<!--.*?-->')),
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

# Token classes that participate in the GLUE rule (#121 item 2) as the
# *leading* member: a directive/HTML comment immediately adjacent (no
# whitespace) to a following token wraps as a single unit with it, so an
# inline-style directive can never be separated from the element it styles.
_GLUE_LEAD_CLASSES = frozenset({'comment'})


@dataclass
class Token:
    text: str
    atomic: bool
    cls: Optional[str] = None  # token class name (glue rule uses it)


def _apply_glue(tokens: list[Token]) -> list[Token]:
    """
    Apply the #121 glue rule: a directive/HTML-comment token immediately
    adjacent (no intervening whitespace token) to a following non-whitespace
    token is merged with it into a single atomic unit. This keeps an inline
    style directive (`<!--style:X-->`) fused to the element it styles
    (`**bold**`) so wrapping can never split the pair and silently drop the
    style (`spec/attachment-rule.md`).
    """
    merged: list[Token] = []
    i = 0
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if (
            tok.cls in _GLUE_LEAD_CLASSES
            and i + 1 < n
            and not tokens[i + 1].text.isspace()
        ):
            glued_text = tok.text + tokens[i + 1].text
            merged.append(Token(glued_text, atomic=True, cls='glue'))
            i += 2
            continue
        merged.append(tok)
        i += 1
    return merged


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
        atomic_cls = None
        for name, pat in _TOKEN_PATTERNS:
            m = pat.match(text, i)
            if m:
                atomic_match = m
                atomic_cls = name
                break
        if atomic_match:
            tokens.append(
                Token(atomic_match.group(0), atomic=True, cls=atomic_cls)
            )
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
            tokens.append(Token(part, atomic=False, cls=None))
        i = next_start

    return _apply_glue(tokens)


def wrap_tokens(tokens: list[Token], width: int) -> list[str]:
    """
    Greedy word-wrap. Returns a list of line strings, each <= width except
    when a single atomic token alone exceeds width (in which case that line
    contains only the atomic token). Under the #120 soft width rule the
    column is planned wide enough for its widest atomic token, so in practice
    the over-width line still fits its column; this remains a safety net for
    callers that pass a narrower width than the column floor.

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
                # Emit it on its own line. The column was planned wide enough
                # for its widest atomic token (soft width rule), so this line
                # fits its column; it is never hard-broken.
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
# Structure preservation (#120 items 2-3): list/blockquote continuation
# indentation and in-cell code-fence skipping.
# ---------------------------------------------------------------------------

# A cell whose *entire* content is a code-fence delimiter (``` or ~~~,
# optionally with an info string on the opening fence). Leading whitespace up
# to three spaces is allowed, mirroring CODE_FENCE_RE at the document level.
FENCE_CELL_RE = re.compile(r'^\s{0,3}(`{3,}|~{3,})')


def detect_content_prefix(content: str) -> tuple[str, str]:
    """
    Detect a leading list marker or blockquote prefix and return
    ``(first_prefix, cont_prefix)`` -- the exact string that leads the first
    wrapped line and the (equal-length) indent that leads every continuation
    line. Returns ``('', '')`` when the cell begins with neither.

    Derived from the retired epublisher-docs ``wrap-table-lines.py``
    (``detect_content_prefix``), the prior art named in #120, but returning
    both prefixes so the cell *body* is wrapped to ``width - len(prefix)``
    and each output line re-prefixed -- keeping every rendered line within
    the planned column width (the prior art wrapped the whole marker+body
    string, which could overflow once the continuation indent was added):

      - "- item"      -> ("- ",   "  ")     list: marker then 2-space hang
      - "1. item"     -> ("1. ",  "   ")    numbered hang ("10. " -> 4)
      - "> text"      -> ("> ",   "> ")     blockquote marker on every line
      - ">> text"     -> (">> ",  ">> ")    nested level preserved
      - "> - item"    -> ("> - ", ">   ")   blockquote + list hang
      - ">>> 1. item" -> (">>> 1. ", ">>>    ")  nested bq + numbered list
    """
    # Blockquotes first (a blockquote may itself contain a list marker).
    bq = re.match(r'^(>+)\s', content)
    if bq:
        markers = bq.group(1)
        inner = content[len(markers) + 1:]
        lm = re.match(r'^[-*+]\s', inner)
        if lm:
            first = markers + ' ' + lm.group(0)
            cont = markers + ' ' * (len(first) - len(markers))
            return first, cont
        num = re.match(r'^(\d+)\.\s', inner)
        if num:
            first = markers + ' ' + num.group(0)
            cont = markers + ' ' * (len(first) - len(markers))
            return first, cont
        # Plain blockquote: marker (with its single following space) repeats.
        return markers + ' ', markers + ' '

    # Bare list markers: -, *, +
    lm = re.match(r'^[-*+]\s', content)
    if lm:
        first = lm.group(0)
        return first, ' ' * len(first)

    # Numbered lists: 1., 2., 10., ...
    num = re.match(r'^(\d+)\.\s', content)
    if num:
        first = num.group(0)
        return first, ' ' * len(first)

    return '', ''


def wrap_cell(content: str, width: int) -> list[str]:
    """
    Wrap one multiline cell's content to *width*, preserving list/blockquote
    structure (#120 items 2-3). When the content leads with a list marker or
    blockquote prefix, the body after the marker is wrapped to
    ``width - len(prefix)`` and each line re-prefixed -- the first line with
    the literal marker, continuation lines with the hang/marker indent -- so
    every rendered line stays within the planned column width and the
    wrapped remainder still reads as part of the item or blockquote.
    """
    first, cont = detect_content_prefix(content)
    if not first:
        return wrap_tokens(tokenize_inline(content), width)

    body = content[len(first):]
    body_width = max(width - len(first), 1)
    body_lines = wrap_tokens(tokenize_inline(body), body_width)
    if not body_lines:
        return [first.rstrip()]
    out = [first + body_lines[0]]
    for ln in body_lines[1:]:
        out.append(cont + ln)
    return out


def atomic_floor(cell: str) -> int:
    """
    Return the width of the widest unsplittable unit in *cell*: the longest
    atomic token (link, URL, code span, directive comment, condition span,
    glued directive+element, ...). Non-atomic prose contributes nothing --
    it can always wrap. Used by the soft width rule (#120 Proposal item 4)
    as a per-column floor so an atomic token never has to be split.
    """
    floor = 0
    for tok in tokenize_inline(cell):
        if tok.atomic and len(tok.text) > floor:
            floor = len(tok.text)
    return floor


def column_protected_flags(members_rows: list[list[str]], n_cols: int) -> list[list[bool]]:
    """
    Per (data-row, column) flag marking cells that must be emitted verbatim
    (never wrapped): in-cell fenced-code delimiter lines and the content
    lines between them (#120 item 3). Fences are tracked independently down
    each column across the table's data rows, mirroring the document-level
    fence scanner but scoped to a single cell column.
    """
    flags = [[False] * n_cols for _ in members_rows]
    for c in range(n_cols):
        in_fence = False
        fence_char = None
        fence_count = 0
        for r, row in enumerate(members_rows):
            cell = row[c] if c < len(row) else ''
            m = FENCE_CELL_RE.match(cell)
            if m:
                char = m.group(1)[0]
                count = len(m.group(1))
                if not in_fence:
                    in_fence = True
                    fence_char = char
                    fence_count = count
                    flags[r][c] = True
                    continue
                if char == fence_char and count >= fence_count:
                    in_fence = False
                    fence_char = None
                    fence_count = 0
                    flags[r][c] = True
                    continue
                # A fence-looking line of a different kind while open: still
                # protected content.
                flags[r][c] = True
                continue
            if in_fence:
                flags[r][c] = True
    return flags


# ---------------------------------------------------------------------------
# Link-reference rewrite (#120 Proposal item 1)
# ---------------------------------------------------------------------------
#
# An over-budget multiline cell that carries an inline link `[text](url)` is
# rewritten to hold only the short reference form `[text][id]`, with the
# definition `[id]: url "title"` emitted after the table. This runs BEFORE
# width planning so the shortened cell drives the column floors and the soft
# width rule rarely has to flex (#120 Proposal item 4, pipeline ordering).
#
# TRIGGER (never unconditional): a cell only rewrites when (a) its content is
# longer than the per-cell width budget (max_cell_width) so it would wrap, AND
# (b) rewriting its inline links actually brings the cell within that budget.
# Condition (b) is what keeps a short atomic link at a deliberately tiny
# --max-cell-width (e.g. the i120-link-atomic-narrow fixture: a 21-char link
# whose reference form still overflows a width-12 cap) atomic and un-rewritten
# -- the soft width rule widens the column for it instead.

# Inline link with optional CommonMark title: [text](url "title") /
# [text](url 'title') / [text](url). The URL is the first whitespace-run-free
# token; a quoted title may follow. Reference links [text][id] and bare URLs
# are intentionally NOT matched here (only [text](url) inline links rewrite).
INLINE_LINK_RE = re.compile(
    r'\[(?P<text>[^\]]*)\]'
    r'\((?P<url>[^)\s]+)'
    r'(?:\s+(?P<title>"[^"]*"|\'[^\']*\'))?\)'
)

# An existing link-reference *definition* line: `[id]: url "optional title"`.
# Used to seed the per-file used-ID set so a fresh rewrite never mints an ID
# that already exists in the document (collision -> next n; also the R10
# idempotence guard: a definition emitted on pass 1 is seen on pass 2).
LINK_DEF_RE = re.compile(r'^\s*\[([^\]]+)\]:\s+\S')

# Alias in a directive comment: `#slug` (letters/digits then word chars).
DIRECTIVE_ALIAS_RE = re.compile(r'#([A-Za-z0-9][A-Za-z0-9_-]*)')

# ATX heading line: `# Heading text` (1-6 leading '#').
ATX_HEADING_RE = re.compile(r'^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$')


def _slugify(text: str) -> str:
    """
    Convert heading text to a URL-friendly slug (mirrors
    ``add-aliases.py``'s ``slugify``): strip inline formatting, lowercase,
    collapse non-alphanumerics to single hyphens, trim.
    """
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)          # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)              # italic
    text = re.sub(r'`([^`]+)`', r'\1', text)                # code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)    # links
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def collect_used_link_ids(lines: list[str]) -> set[str]:
    """
    Return the set of link-reference IDs already defined anywhere in the
    document. Seeds the rewrite's uniqueness counter so a minted ID never
    collides with an existing definition (and so an already-rewritten
    document round-trips unchanged -- R10).
    """
    used: set[str] = set()
    for line in lines:
        m = LINK_DEF_RE.match(line)
        if m:
            used.add(m.group(1).strip())
    return used


def table_slug(table: TableBlock, heading_slug: Optional[str]) -> str:
    """
    Resolve the slug used to build reference IDs for *table*
    (``table-<slug>-<n>``), in priority order (#120 Proposal item 1):

      1. the table directive's own alias (``<!-- #config ; multiline -->``);
      2. the nearest preceding heading's slug;
      3. a file-level fallback (``table``).
    """
    if table.directive_line:
        m = DIRECTIVE_ALIAS_RE.search(table.directive_line)
        if m:
            return m.group(1)
    if heading_slug:
        return heading_slug
    return 'table'


def rewrite_cell_links(
    cell: str,
    slug: str,
    counter: list[int],
    used_ids: set[str],
    definitions: list[str],
) -> str:
    """
    Rewrite every inline ``[text](url)`` link in *cell* to reference form
    ``[text][id]`` and append the matching ``[id]: url "title"`` line to
    *definitions*. Reference IDs are ``table-<slug>-<n>`` with ``n`` taken
    from *counter* (a single-element list used as a mutable per-table cursor),
    skipping any ID already in *used_ids* (collision -> next n). Returns the
    rewritten cell text.

    The caller decides *whether* to keep the result (the trigger's fit test);
    this function performs the mechanical substitution only.
    """
    def repl(m: 're.Match[str]') -> str:
        text = m.group('text')
        url = m.group('url')
        title = m.group('title')
        # Mint the next free ID for this table.
        while True:
            ref_id = f'table-{slug}-{counter[0]}'
            counter[0] += 1
            if ref_id not in used_ids:
                break
        used_ids.add(ref_id)
        if title:
            definitions.append(f'[{ref_id}]: {url} {title}')
        else:
            definitions.append(f'[{ref_id}]: {url}')
        return f'[{text}][{ref_id}]'

    return INLINE_LINK_RE.sub(repl, cell)


def rewrite_table_links(
    table: TableBlock,
    config: FormatterConfig,
    heading_slug: Optional[str],
    used_ids: set[str],
) -> list[str]:
    """
    Rewrite over-budget inline links in *table*'s multiline cells to
    reference form (mutating the cells in place) and return the ordered list
    of definition lines to emit after the table.

    Only cells whose content exceeds ``max_cell_width`` are candidates, and a
    cell's links are rewritten only when doing so brings the cell within that
    budget -- otherwise the links stay inline/atomic and the soft width rule
    widens the column for them (see the module TRIGGER note). Fence-protected
    cells are never touched. Links are processed in row-then-column document
    order so IDs number deterministically.
    """
    if not table.is_multiline or not table.rows:
        return []

    n_cols = len(table.rows[0])
    protected = column_protected_flags(table.rows, n_cols)
    slug = table_slug(table, heading_slug)
    counter = [1]  # per-table link counter (n starts at 1)
    definitions: list[str] = []

    # Walk the genuine data rows in order; header is rows[0] (never wrapped,
    # never rewritten). row_idx indexes table.rows for the fence flags.
    row_idx = -1
    for kind, member in table.members:
        if kind != 'row':
            continue
        row_idx += 1
        if row_idx == 0:
            continue  # header row
        for c in range(len(member)):
            cell = member[c]
            if protected[row_idx][c]:
                continue
            if len(cell) <= config.max_cell_width:
                continue
            if not INLINE_LINK_RE.search(cell):
                continue
            # Trial rewrite on a throwaway counter/def list; commit only if it
            # brings the cell within budget (the trigger's fit test).
            trial_counter = list(counter)
            trial_defs: list[str] = []
            trial_used = set(used_ids)
            rewritten = rewrite_cell_links(
                cell, slug, trial_counter, trial_used, trial_defs
            )
            if len(rewritten) > config.max_cell_width:
                continue  # rewrite does not help; leave the cell atomic
            # Commit: re-run against the real counter/used-set so IDs are
            # minted for keeps in document order.
            member[c] = rewrite_cell_links(
                cell, slug, counter, used_ids, definitions
            )

    return definitions


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

    # Per-column irreducible floor for multiline tables (#120 soft width
    # rule): the widest atomic token any cell in the column carries, or the
    # full length of a fence-protected cell (its content is emitted verbatim
    # and cannot wrap). A column may never be planned narrower than this or
    # an atomic token / protected line would have to be split.
    protected = (
        column_protected_flags(table.rows, n_cols)
        if table.is_multiline else None
    )

    def col_floor(c: int) -> int:
        if not table.is_multiline:
            return 0
        floor = 0
        for r, row in enumerate(table.rows):
            cell = row[c] if c < len(row) else ''
            if protected[r][c]:
                # Verbatim fence line: its whole length is a hard floor.
                floor = max(floor, len(cell))
            else:
                floor = max(floor, atomic_floor(cell))
        return floor

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
        # Fixed widths act as floors that flex up only when an atomic token
        # in a multiline column demands more (#120: "fixed widths act as
        # floors that flex only when an atomic token demands it").
        widths = [max(w, config.min_col_width) for w in config.col_widths]
        for c in range(n_cols):
            widths[c] = max(widths[c], col_floor(c))
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
    #
    # Standard tables keep R5/R7: columns expand to the widest actual cell,
    # no wrapping, over-width warnings handled at render time.
    #
    # Multiline tables follow the #120 soft width rule (Proposal item 4):
    #   width_c = max( min(max_content_c, max_cell_width),
    #                  header_len_c, min_col_width, col_floor_c )
    # where col_floor_c is the widest unsplittable atomic token / protected
    # fence line in the column. If the resulting total line width exceeds
    # max_line_width, columns shrink toward their floors until the total
    # fits or every column is already at its floor -- so the table exceeds
    # the budget by exactly what unsplittable content demands, fully aligned.
    widths = [config.min_col_width] * n_cols
    floors = [config.min_col_width] * n_cols
    for c in range(n_cols):
        header_len = len(header[c])
        max_content = 0
        for row in table.rows:
            cell = row[c] if c < len(row) else ''
            max_content = max(max_content, len(cell))
        if table.is_multiline:
            fl = max(header_len, config.min_col_width, col_floor(c))
            floors[c] = fl
            widths[c] = max(
                fl, min(max_content, config.max_cell_width)
            )
        else:
            # For standard tables, columns expand to fit the content (R7).
            widths[c] = max(
                config.min_col_width, header_len, max_content
            )
            floors[c] = widths[c]

    if table.is_multiline:
        _shrink_to_budget(widths, floors, n_cols, config.max_line_width)
    return widths


def _line_width(widths: list[int]) -> int:
    """Total rendered line width for a row: content + '| ', ' | ', ' |'."""
    return sum(widths) + 3 * len(widths) + 1


def _shrink_to_budget(
    widths: list[int], floors: list[int], n_cols: int, budget: int
) -> None:
    """
    Shrink columns toward their floors (in place) until the total line width
    fits *budget* or every column is at its floor. Widest-above-floor column
    is trimmed first so slack is removed evenly; when nothing can shrink the
    table simply exceeds the budget by exactly what unsplittable content
    demands (#120 soft width rule).
    """
    while _line_width(widths) > budget:
        # Pick the column with the most slack above its floor.
        best = -1
        best_slack = 0
        for c in range(n_cols):
            slack = widths[c] - floors[c]
            if slack > best_slack:
                best_slack = slack
                best = c
        if best < 0:
            break  # everything at floor; unsplittable content wins
        widths[best] -= 1


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
    header_cells = table.rows[0]

    # Walk members in order: format data rows, pass comment lines through
    # byte-verbatim in place (issue #122). The header is the first 'row'
    # member; the separator is derived and emitted right after it.
    r_idx = 0
    header_emitted = False
    for kind, member in table.members:
        if kind == 'comment':
            out.append(member)
            continue

        # kind == 'row'
        r_idx += 1
        cells = list(member)
        while len(cells) < n_cols:
            cells.append('')

        if not header_emitted:
            # Header row.
            out.append(_render_row(cells, widths))
            # Separator row: derive alignments from the original separator cells.
            alignments = [_alignment_marker(c) for c in table.separator_cells]
            while len(alignments) < n_cols:
                alignments.append('none')
            sep_cells = [
                _format_separator_cell(widths[c], alignments[c])
                for c in range(n_cols)
            ]
            out.append(_render_row(sep_cells, widths))
            header_emitted = True
            continue

        if _is_blank_row(cells):
            # Preserve as whitespace-only padded row (R3).
            out.append(_render_row(['' for _ in widths], widths))
            continue

        # Standard-table over-width warning (R7).
        for c, cell in enumerate(cells):
            if len(cell) > config.max_cell_width:
                header_label = header_cells[c] if c < len(header_cells) else f'col {c+1}'
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
    (R6) using inline-formatting-aware tokenization (R8), preserving
    list/blockquote continuation structure and never re-wrapping in-cell
    fenced code (#120 items 2-3). Every row of a column shares the one
    planned width, so pipes align on every row (the old per-row local
    widening of R8 is gone -- the column itself widened during planning per
    the #120 soft width rule).

    The directive line (if any) is emitted verbatim above the table (R4).
    """
    out: list[str] = []
    warnings: list[str] = []
    n_cols = len(widths)

    # Per (data-row, column) verbatim flags for in-cell code fences, indexed
    # against table.rows (header at index 0).
    protected = column_protected_flags(table.rows, n_cols)

    if table.directive_line is not None:
        out.append(table.directive_line)

    # Walk members in order: format data rows (wrapping long cells), pass
    # comment lines through byte-verbatim in place (issue #122). row_idx
    # tracks position into table.rows so fence flags line up.
    header_emitted = False
    row_idx = -1
    for kind, member in table.members:
        if kind == 'comment':
            out.append(member)
            continue

        # kind == 'row'
        row_idx += 1
        cells = list(member)
        while len(cells) < n_cols:
            cells.append('')

        if not header_emitted:
            # Header row (no wrapping for the header — headers fit by design).
            out.append(_render_row(cells, widths))
            # Separator row.
            alignments = [_alignment_marker(c) for c in table.separator_cells]
            while len(alignments) < n_cols:
                alignments.append('none')
            sep_cells = [
                _format_separator_cell(widths[c], alignments[c])
                for c in range(n_cols)
            ]
            out.append(_render_row(sep_cells, widths))
            header_emitted = True
            continue

        if _is_blank_row(cells):
            out.append(_render_row(['' for _ in widths], widths))
            continue

        # Wrap each cell.
        wrapped: list[list[str]] = []
        for c, cell in enumerate(cells):
            if cell == '':
                wrapped.append([''])
                continue
            if protected[row_idx][c]:
                # In-cell fenced-code delimiter or content: emit verbatim,
                # never re-wrapped (#120 item 3).
                wrapped.append([cell])
                continue
            lines = wrap_cell(cell, widths[c])
            if not lines:
                lines = ['']
            wrapped.append(lines)

        max_lines = max(len(w) for w in wrapped)

        for line_idx in range(max_lines):
            row_cells: list[str] = []
            for c in range(n_cols):
                if line_idx < len(wrapped[c]):
                    cell_text = wrapped[c][line_idx]
                else:
                    cell_text = ''
                row_cells.append(cell_text)
            # One planned width per column on every row: pipes always align.
            out.append(_render_row(row_cells, widths))

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

    # Seed the per-file used-ID set from every link-reference definition
    # already in the document so a minted reference ID never collides with an
    # existing one and an already-rewritten document round-trips (R10).
    used_ids = collect_used_link_ids(lines)

    out_lines: list[str] = []
    all_warnings: list[str] = []
    last_heading_slug: Optional[str] = None

    for block in blocks:
        if isinstance(block, TextBlock):
            out_lines.extend(block.lines)
            # Track the nearest preceding heading's slug for the ID fallback
            # when a table directive carries no alias (#120 item 1).
            for line in block.lines:
                hm = ATX_HEADING_RE.match(line)
                if hm:
                    last_heading_slug = _slugify(hm.group(2))
            continue

        # TableBlock. Rewrite over-budget inline links to reference form
        # BEFORE width planning so the shortened cells drive the floors
        # (#120 Proposal item 1). Definitions are emitted after the fully
        # rendered table -- for a condition-wrapped tail that lands after the
        # <!--/condition--> close tag, outside the span (#120 <-> #122).
        definitions = rewrite_table_links(
            block, config, last_heading_slug, used_ids
        )
        widths = plan_widths(block, config)
        if block.is_multiline:
            rendered, warnings = render_multiline(block, widths, config)
        else:
            rendered, warnings = render_standard(block, widths, config)
        out_lines.extend(rendered)
        if definitions:
            out_lines.append('')
            out_lines.extend(definitions)
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
