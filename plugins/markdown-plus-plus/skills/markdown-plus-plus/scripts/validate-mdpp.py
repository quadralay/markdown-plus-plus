#!/usr/bin/env python3
"""
validate-mdpp.py

Validate Markdown++ document syntax.

Usage:
    python validate-mdpp.py <input_file> [options]

Options:
    --help          Show this help message
    --verbose       Enable verbose output
    --json          Output errors as JSON
    --strict        Treat warnings as errors

Exit Codes:
    0 - Valid document (no errors)
    1 - File error (not found, not readable)
    2 - Invalid arguments
    3 - Validation errors found
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, asdict
from enum import Enum
from collections.abc import Iterator


# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """Represents a validation error, warning, or info message."""
    type: str
    code: str
    message: str
    file: str
    line: int
    context: str
    suggestion: str | None = None


# Regex patterns for Markdown++ extensions
PATTERNS = {
    'variable': re.compile(r'(?<!\\)\$([a-zA-Z_][a-zA-Z0-9_-]*);'),
    'variable_invalid': re.compile(r'(?<!\\)\$([^;]*);'),
    'condition_open': re.compile(r'<!--\s*condition:([^>]+?)\s*-->'),
    'condition_close': re.compile(r'<!--\s*/condition\s*-->'),
    'include': re.compile(r'<!--\s*include:([^>]+?)\s*-->'),
    'multiline': re.compile(r'<!--\s*multiline\s*-->'),
}

# A comment tag: `<!--` up to the nearest `-->` on the same line. The comment
# boundary is found before the commands are parsed (spec formal grammar), so a
# `-->` inside a marker value ends the comment.
COMMENT_TAG_RE = re.compile(r'<!--(.*?)-->')

# An alias command: `#` immediately followed by a name character. The name
# runs to the end of the command; a `#` followed by whitespace is prose
# (`<!-- # TODO -->`), not an alias.
ALIAS_COMMAND_RE = re.compile(r'#[^ \t\n\r;>]')

# Commands that attach to the element that follows (subject to MDPP009).
ATTACHING_PREFIXES = ('style:', 'marker:', 'markers:')
# Every recognized command prefix. A comment with no recognized command is a
# regular HTML comment and is ignored (spec section 5.2).
RECOGNIZED_PREFIXES = ATTACHING_PREFIXES + ('condition:', '/condition', 'include:')


# XML 1.0 NCName NameStartChar letter ranges (issue #108).
# See spec/formal-grammar.md alias_name_start_char production.
# Spelled with \u / \U escapes -- literal Unicode in source is prone
# to silent corruption in transit.
_NCNAME_START_CHAR = (
    "_A-Za-z"
    "\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF"
    "\u0370-\u037D\u037F-\u1FFF"
    "\u200C-\u200D"
    "\u2070-\u218F"
    "\u2C00-\u2FEF"
    "\u3001-\uD7FF"
    "\uF900-\uFDCF"
    "\uFDF0-\uFFFD"
    "\U00010000-\U000EFFFF"
)

# Combining-mark ranges from XML 1.0 NCName NameChar production. Permitted
# only in non-first positions of an alias name. Including these here lets
# decomposed forms like U+0065 U+0301 ("e" + combining acute) accept under
# MDPP002 at the raw-byte level; MDPP008 then normalizes for duplicate
# detection. Combining marks are NOT in _NCNAME_START_CHAR -- they cannot
# lead an alias.
_NCNAME_COMBINING = (
    "\u0300-\u036F"
    "\u203F-\u2040"
)

# Period and middle dot from XML 1.0 NCName NameChar production (issue #111).
# Permitted only in non-first positions of an alias name. Period (`.`) enables
# dotted-hierarchy identifiers (`#chapter.1.intro`, `#api.v1.users`) so
# aliases align with XML NCName end-to-end. Middle dot (#xB7) is included
# for the same reason -- NCName explicitly permits it as a non-first NameChar.
# Middle dot uses \u escape per the source-hygiene convention applied to
# every other non-ASCII range in this module (literal Unicode in source is
# prone to silent corruption in transit).
_NCNAME_PUNCT = ".\u00B7"

STANDARD_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_-]*$')
ALIAS_NAME_RE = re.compile(
    f'^[{_NCNAME_START_CHAR}0-9]'
    f'[{_NCNAME_START_CHAR}0-9{_NCNAME_COMBINING}{_NCNAME_PUNCT}-]*$'
)
STYLE_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_ -]*$')


def validate_variable_name(name: str) -> bool:
    """Check if a variable name is valid."""
    return bool(STANDARD_NAME_RE.match(name))


def validate_style_name(name: str) -> bool:
    """Check if a style name is valid (embedded spaces allowed)."""
    trimmed = name.strip()
    if not trimmed:
        return False
    return bool(STYLE_NAME_RE.match(trimmed))


def validate_alias_name(name: str) -> bool:
    """Check if an alias name is valid (digit-first allowed)."""
    return bool(ALIAS_NAME_RE.match(name))


def _alias_dedup_key(name: str) -> str:
    """Normalization key for MDPP008 duplicate detection.

    Applies Unicode NFC + casefold so canonical-equivalent variants
    (precomposed vs. decomposed accents; upper vs. lower case) compare
    equal. Stricter than CommonMark 0.30 link-reference-definition
    slug matching, which mandates casefold only (no NFC). The NFC step
    is added so decomposed-accent aliases collide with their
    precomposed counterparts -- safer for cross-system alias stability
    than CommonMark's looser equivalence.
    """
    return unicodedata.normalize('NFC', name).casefold()


def validate_marker_key(name: str) -> bool:
    """Check if a marker key name is valid (embedded spaces allowed)."""
    trimmed = name.strip()
    if not trimmed:
        return False
    return bool(STYLE_NAME_RE.match(trimmed))


def validate_condition_expression(expr: str) -> tuple[bool, str | None]:
    """
    Validate a condition expression.
    Returns (is_valid, error_message).
    """
    expr = expr.strip()
    if not expr:
        return False, "Empty condition expression"

    # Split by comma (OR) and space (AND)
    # Check each condition name
    parts = re.split(r'[,\s]+', expr)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Remove NOT operator for checking
        if part.startswith('!'):
            part = part[1:]
        if not part:
            return False, "Empty condition after NOT operator"
        if not STANDARD_NAME_RE.match(part):
            return False, f"Invalid condition name: {part}"

    return True, None


def validate_json(json_str: str) -> tuple[object | None, str | None]:
    """Validate and parse JSON string. Returns (parsed_object, None) on success or (None, error_message) on failure."""
    try:
        return json.loads(json_str), None
    except json.JSONDecodeError as e:
        return None, str(e)


def split_commands(content: str) -> tuple[list[str], bool]:
    """Split a comment tag's content into its commands.

    A `;` separates commands only outside a command's own value: a `;` inside
    a quoted simple-marker value (`marker:K="a; b"`) or inside a `markers:`
    JSON object (string-aware, balanced braces) belongs to that command.

    Returns (segments, unterminated). `unterminated` is True when the content
    ends inside a quoted marker value or an unbalanced JSON object -- for
    example when a `-->` inside a value ended the comment early.
    """
    segments: list[str] = []
    buf: list[str] = []
    depth = 0           # JSON brace depth inside a markers: command
    in_string = False   # inside a JSON string
    escaped = False     # previous character was a backslash inside a string
    in_quote = False    # inside a simple-marker quoted value

    for ch in content:
        if depth:
            buf.append(ch)
            if in_string:
                if escaped:
                    escaped = False
                elif ch == '\\':
                    escaped = True
                elif ch == '"':
                    in_string = False
            elif ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            continue
        if in_quote:
            buf.append(ch)
            if ch == '"':
                in_quote = False
            continue
        if ch == ';':
            segments.append(''.join(buf))
            buf = []
            continue
        current = ''.join(buf).lstrip()
        if ch == '{' and current.startswith('markers:') and current.rstrip() == 'markers:':
            depth = 1
        elif ch == '"' and current.startswith('marker:') and current.endswith('='):
            in_quote = True
        buf.append(ch)

    segments.append(''.join(buf))
    return segments, bool(depth or in_quote)


def _is_alias_segment(segment: str) -> bool:
    return bool(ALIAS_COMMAND_RE.match(segment))


def _is_recognized_segment(segment: str) -> bool:
    return (
        segment == 'multiline'
        or segment.startswith(RECOGNIZED_PREFIXES)
        or _is_alias_segment(segment)
    )


def _is_attaching_segment(segment: str) -> bool:
    return (
        segment == 'multiline'
        or segment.startswith(ATTACHING_PREFIXES)
        or _is_alias_segment(segment)
    )


# Container prefixes. A tag inside a blockquote carries the quote's `>`
# prefix, and a tag can start a list item on the item's marker line
# (Attachment Rule edge cases 8 and 9).
BLOCKQUOTE_PREFIX_RE = re.compile(r'^[ \t]*>[ ]?')
LIST_ITEM_RE = re.compile(r'^([ ]*)([-*+]|\d{1,9}[.)])([ \t]+|$)')


def _strip_blockquote_prefixes(line: str) -> str:
    """Remove leading blockquote markers (`>`, `> >`)."""
    while True:
        m = BLOCKQUOTE_PREFIX_RE.match(line)
        if not m:
            return line
        line = line[m.end():]


def _strip_container_prefixes(line: str) -> str:
    """Remove leading blockquote markers and list-item markers."""
    while True:
        line = _strip_blockquote_prefixes(line)
        m = LIST_ITEM_RE.match(line)
        if not m or not m.group(3):
            return line
        line = line[m.end():]


# A run of three or more backticks or tildes opening or closing a fence.
FENCE_RUN_RE = re.compile(r'(`{3,}|~{3,})(.*)$')


def _skip_mask(lines: list[str]) -> list[bool]:
    """Per line, True when the line is skipped: YAML front matter, a fence
    delimiter, or a line inside a fenced code block.

    Front matter is metadata, not Markdown content, so directive-like text in
    it (a `description:` that mentions `<!--style:-->`) is not checked.

    Fences follow CommonMark 0.30 at **list-relative** indentation: a fence
    may be indented up to three spaces past the content column of the list
    item it belongs to, so a fence indented four spaces under `1.` is a fence,
    not indented code. Blockquote prefixes are stripped first. A backtick
    fence's info string cannot contain a backtick. A closing fence uses the
    opening character at least as many times, with nothing after it.
    """
    mask = [False] * len(lines)
    in_fence = False
    fence_char = ''
    fence_len = 0
    fence_col = 0
    list_cols: list[int] = []   # content columns of the open list items

    start = 0
    if lines and lines[0].rstrip('\r') == '---':
        for end in range(1, len(lines)):
            if lines[end].rstrip('\r') in ('---', '...'):
                for k in range(end + 1):
                    mask[k] = True
                start = end + 1
                break

    for idx in range(start, len(lines)):
        raw = lines[idx]
        body = _strip_blockquote_prefixes(raw.expandtabs(4)).rstrip('\r')
        stripped = body.strip()
        indent = len(body) - len(body.lstrip(' '))

        if in_fence:
            # A fence runs to its closing fence. (A dedented line is not taken
            # to end the list item: content indented with non-breaking spaces
            # would close the fence early and mis-pair every later fence.)
            m = FENCE_RUN_RE.match(stripped)
            if (
                m
                and m.group(1)[0] == fence_char
                and len(m.group(1)) >= fence_len
                and not m.group(2).strip()
                and indent - fence_col <= 3
            ):
                in_fence = False
            mask[idx] = True
            continue

        if not stripped:
            continue

        base = 0
        rest = body
        m = LIST_ITEM_RE.match(body)
        if m and m.group(3):
            marker_indent = len(m.group(1))
            while list_cols and list_cols[-1] > marker_indent:
                list_cols.pop()
            gap = len(m.group(3).expandtabs(4))
            width = gap if 1 <= gap <= 4 else 1
            content_col = marker_indent + len(m.group(2)) + width
            list_cols.append(content_col)
            base = content_col
            rest = ' ' * content_col + body[m.end():] if gap <= 4 else body
        else:
            while list_cols and indent < list_cols[-1]:
                list_cols.pop()
            base = list_cols[-1] if list_cols else 0

        rest_indent = len(rest) - len(rest.lstrip(' '))
        if 0 <= rest_indent - base <= 3:
            fm = FENCE_RUN_RE.match(rest.lstrip(' '))
            if fm and not (fm.group(1)[0] == '`' and '`' in fm.group(2)):
                in_fence = True
                fence_char = fm.group(1)[0]
                fence_len = len(fm.group(1))
                fence_col = base
                mask[idx] = True

    return mask


# --- Multiline-table row-merge detection (MDPP018) ---------------------------
# A pipe-table row: optional indent, a leading pipe, a trailing pipe.
TABLE_ROW_RE = re.compile(r'^\s*\|.*\|\s*$')
# GFM delimiter row: interior cells contain only whitespace, dashes, colons.
TABLE_DELIMITER_RE = re.compile(r'^\s*\|[\s:|\-]+\|\s*$')
# A line whose only content is a multiline directive -- bare
# (`<!-- multiline -->`) or combined-commands form
# (`<!-- style:X ; multiline ; #y -->`). Mirrors format-tables.py.
MULTILINE_DIRECTIVE_LINE_RE = re.compile(
    r'^\s*<!--\s*[^>]*?\bmultiline\b[^>]*?-->\s*$'
)
# Split a row on unescaped pipes (a `\|` is a literal pipe inside a cell).
TABLE_CELL_SPLIT_RE = re.compile(r'(?<!\\)\|')

# --- In-cell / conditional-cell condition detection (MDPP019) ----------------
# A condition open (`<!--condition:EXPR-->`) or close (`<!--/condition-->`) tag,
# anchored anywhere within a line. Used to detect a condition tag embedded in a
# table row (an in-cell span or a conditional cell), as opposed to a full-line
# condition tag between rows -- the supported granularity, which never matches
# TABLE_ROW_RE because it carries no pipes.
CONDITION_TAG_RE = re.compile(
    r'<!--\s*(?:condition:[^>]+?|/condition)\s*-->'
)


def _is_mdpp_tag_line(line: str) -> bool:
    """True if the line's only content is a comment tag with an attaching command.

    Blockquote prefixes and a list-item marker are stripped first, so
    `> <!-- style:Note -->` and `2. <!-- style:BQ_Note ; #q -->` are tag lines.
    """
    stripped = _strip_container_prefixes(line).strip()
    m = COMMENT_TAG_RE.fullmatch(stripped)
    if not m:
        return False
    segments, _ = split_commands(m.group(1))
    return any(_is_attaching_segment(s.strip()) for s in segments)


def _blockquote_depth(line: str) -> tuple[int, str]:
    """Return (number of leading blockquote markers, remainder)."""
    depth = 0
    while True:
        m = BLOCKQUOTE_PREFIX_RE.match(line)
        if not m:
            return depth, line
        depth += 1
        line = line[m.end():]


def _opens_container(line: str, tag_line: str) -> bool:
    """True if `line` opens a blockquote or list item below `tag_line`.

    A tag above a list or blockquote attaches to that container even when the
    container's first line is itself a tag (`<!-- style:CustomUList -->` above
    `- <!-- style:CustomParagraph -->`).
    """
    depth, rest = _blockquote_depth(line)
    tag_depth, tag_rest = _blockquote_depth(tag_line)
    if depth > tag_depth and rest.strip():
        return True
    m = LIST_ITEM_RE.match(rest)
    if m and m.group(3) and rest[m.end():].strip():
        tag_item = LIST_ITEM_RE.match(tag_rest)
        return not (tag_item and tag_item.group(3))
    return False


def _is_content_line(line: str, tag_line: str | None = None) -> bool:
    """True if line is a non-blank, non-MDPP-tag content element.

    A line holding only blockquote markers (`>`) is blank inside the quote.
    When `tag_line` is given, a line that opens a blockquote or list item
    below it counts as content even if its own first block is a tag.
    """
    if not _strip_container_prefixes(line).strip():
        return False
    if tag_line is not None and _opens_container(line, tag_line):
        return True
    return not _is_mdpp_tag_line(line)


def _iter_outside_fences(
    lines: list[str], mask: list[bool] | None = None
) -> Iterator[tuple[int, str]]:
    """Yield (1-based line_num, line) for lines outside fenced code blocks."""
    if mask is None:
        mask = _skip_mask(lines)
    for line_num, line in enumerate(lines, start=1):
        if not mask[line_num - 1]:
            yield line_num, line


def _split_table_cells(row: str) -> list[str]:
    """Split a pipe-table row into its interior cell contents.

    Splits on unescaped `|`, drops the empty strings produced by the leading
    and trailing border pipes, and trims incidental whitespace around each
    cell. Mirrors format-tables.py split_cells() so the two tools agree on
    what counts as a cell.
    """
    stripped = row.rstrip('\n').rstrip('\r')
    parts = TABLE_CELL_SPLIT_RE.split(stripped)
    if parts and parts[0].strip() == '':
        parts = parts[1:]
    if parts and parts[-1].strip() == '':
        parts = parts[:-1]
    return [c.strip() for c in parts]


def _scan_multiline_row_merge(
    lines: list[str], filepath: str
) -> list[ValidationIssue]:
    """Detect multiline tables whose data rows will all merge (MDPP018).

    Under `<!-- multiline -->`, logical rows are separated only by a
    whitespace-only separator row; every other pipe-bearing row continues
    the current logical row. A table written with regular-table semantics --
    one record per pipe line, no separator rows -- therefore collapses every
    data row into a single logical row, with no error from any other check.

    The smoking-gun pattern (issue #118) is a multiline table whose body has
    >= 2 rows with a non-blank first cell, zero whitespace-only separator
    rows, and zero continuation rows (blank first cell). That exact gate
    guarantees no false positives: a single data row cannot merge, a present
    separator row proves the author knows the mechanism, and a present
    continuation row likewise demonstrates awareness. (The row-continuation
    mechanism itself keys on whole-row whitespace, not the first cell; the
    first-cell test here is only a heuristic for author intent.)

    The diagnostic anchors to the directive line, where the fix applies.

    Tables inside a blockquote (`> | a | b |`) and a directive on a list
    item's marker line are recognized: container prefixes are stripped before
    matching.
    """
    issues: list[ValidationIssue] = []
    mask = _skip_mask(lines)
    rows = [_strip_blockquote_prefixes(line) for line in lines]

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Directives and tables inside fenced code blocks are skipped.
        if mask[i]:
            i += 1
            continue

        # A multiline directive immediately above a header row that is
        # immediately above a GFM delimiter row marks a multiline table.
        if (
            MULTILINE_DIRECTIVE_LINE_RE.match(_strip_container_prefixes(line))
            and i + 2 < n
            and TABLE_ROW_RE.match(rows[i + 1])
            and not TABLE_DELIMITER_RE.match(rows[i + 1])
            and TABLE_DELIMITER_RE.match(rows[i + 2])
        ):
            directive_line_num = i + 1  # 1-based line number of the directive

            separator_rows = 0
            continuation_rows = 0
            content_first_rows = 0

            j = i + 3
            while (
                j < n
                and TABLE_ROW_RE.match(rows[j])
                and not mask[j]
            ):
                cells = _split_table_cells(rows[j])
                if not cells or all(c == '' for c in cells):
                    separator_rows += 1
                elif cells[0] == '':
                    continuation_rows += 1
                else:
                    content_first_rows += 1
                j += 1

            if (
                content_first_rows >= 2
                and separator_rows == 0
                and continuation_rows == 0
            ):
                issues.append(ValidationIssue(
                    type=Severity.WARNING.value,
                    code="MDPP018",
                    message=(
                        "Multiline table has no separator rows; all "
                        f"{content_first_rows} data rows will merge into one "
                        "logical row"
                    ),
                    file=filepath,
                    line=directive_line_num,
                    context=line.strip()[:60],
                    suggestion=(
                        "Under <!-- multiline --> every pipe-bearing row "
                        "continues the current logical row; only a "
                        "whitespace-only separator row (e.g. `|  |  |`) starts "
                        "a new one. Add separator rows between records, or -- "
                        "if the cells are single-line -- drop the multiline "
                        "directive and use a plain table."
                    ),
                ))

            i = j
            continue

        i += 1

    return issues


def _scan_condition_in_table_cells(
    lines: list[str], filepath: str
) -> list[ValidationIssue]:
    """Detect condition tags embedded in a table row line (MDPP019).

    Conditional rows are the supported granularity for conditions in tables: a
    condition block MAY wrap complete physical rows (standard table) or complete
    logical rows (multiline table), or an entire table. Those supported forms
    put the `<!--condition:EXPR-->` / `<!--/condition-->` tag on its **own line**
    between rows, so the tag line carries no pipe delimiters.

    Two unsupported patterns instead place a condition tag **inside** a table
    row line:

    - **In-cell condition span** -- a span that opens and closes within a single
      cell on one physical line (e.g. `Contact <!--condition:web-->email<!--/condition--> now.`).
      Its behavior is mechanically determined by Phase 1 raw-text evaluation, but
      the span is an unbreakable atomic unit for line-wrapping tools and a split
      across physical lines corrupts the table when Hidden. Authors SHOULD NOT
      author it.
    - **Conditional cell** -- a condition span that contains an unescaped `|`
      cell delimiter. Hiding it removes cell boundaries and changes the row's
      column count; the resulting table structure is corrupt. Authors MUST NOT
      author it.

    Phase 1 condition evaluation is table-blind (it operates on raw text), so a
    processor cannot reject these -- they are authoring requirements surfaced by
    validation, not processor behavior. Detection therefore keys on line shape:
    a line that is both a pipe-table row (leading and trailing `|`, per
    TABLE_ROW_RE) **and** contains a condition open or close tag. A full-line
    condition tag between rows never matches (no border pipes), and an inline
    condition span in prose never matches (no border pipes), so the row-shape
    heuristic alone excludes every supported pattern -- a genuine
    table-detection pass would add no precision here. One diagnostic is emitted
    per offending row line, anchored to that line, regardless of how many tags
    it carries or whether the span crosses a cell delimiter.

    A condition tag written inside a backtick inline-code span is documentation
    *about* the syntax, not a live directive -- inline code is verbatim, so
    Phase 1 never treats it as a condition span. Such tags are excluded: a tag
    preceded by an odd number of backticks on the line sits inside an open code
    span. This keeps MDPP019 off the many spec and reference tables whose cells
    quote `<!--condition:...-->` as example code.
    """
    issues: list[ValidationIssue] = []
    for line_num, raw in _iter_outside_fences(lines):
        line = _strip_blockquote_prefixes(raw)
        if not TABLE_ROW_RE.match(line):
            continue
        if TABLE_DELIMITER_RE.match(line):
            # A GFM delimiter row cannot carry a condition tag (its interior is
            # whitespace, dashes, and colons only); skip it defensively.
            continue
        # Fire only on a live directive tag -- one not inside a backtick
        # inline-code span. A tag with an odd number of backticks before it on
        # the line is inside an open code span and is verbatim documentation.
        has_live_tag = any(
            line[:m.start()].count('`') % 2 == 0
            for m in CONDITION_TAG_RE.finditer(line)
        )
        if not has_live_tag:
            continue
        issues.append(ValidationIssue(
            type=Severity.WARNING.value,
            code="MDPP019",
            message=(
                "Condition tag inside a table row; conditional rows are the "
                "supported granularity for conditions in tables, not in-cell "
                "spans or conditional cells"
            ),
            file=filepath,
            line=line_num,
            context=line.strip()[:60],
            suggestion=(
                "A condition span that contains an unescaped | delimiter "
                "(conditional cell) MUST NOT be authored -- hiding it removes "
                "cell boundaries and corrupts the table. A span that opens and "
                "closes within one cell (in-cell span) SHOULD NOT be authored -- "
                "it resists line wrapping and corrupts the table if split across "
                "lines. Wrap complete rows instead (a condition block MAY wrap "
                "complete physical rows, or a multiline table's complete logical "
                "rows including the trailing whitespace-only separator row, or an "
                "entire table), or use a variable for value substitution."
            ),
        ))
    return issues


MARKER_KEY_SUGGESTION = (
    "Marker key names must start with a letter or underscore, followed by "
    "letters, digits, hyphens, underscores, or spaces (no leading/trailing spaces)"
)


def _check_comment_commands(
    line: str,
    line_num: int,
    filepath: str,
    alias_locations: dict[str, int],
    alias_display: dict[str, str],
    verbose: bool,
) -> list[ValidationIssue]:
    """Check every command in every comment tag on the line.

    Combined tags are split with split_commands(), so a style, marker,
    markers, or alias command is checked wherever it appears in the tag, not
    only first. A comment with no recognized command is a regular HTML comment
    and is skipped. Conditions and includes are checked separately.
    """
    issues: list[ValidationIssue] = []

    def add(severity: Severity, code: str, message: str, context: str,
            suggestion: str) -> None:
        issues.append(ValidationIssue(
            type=severity.value, code=code, message=message, file=filepath,
            line=line_num, context=context[:60], suggestion=suggestion,
        ))

    # A tag quoted inside an inline code span is documentation about the
    # syntax, not a live directive.
    live = INLINE_CODE_RE.sub(lambda m: ' ' * len(m.group(0)), line)
    for tag in COMMENT_TAG_RE.finditer(live):
        raw_segments, _unterminated = split_commands(tag.group(1))
        segments = [s.strip() for s in raw_segments]
        if not any(_is_recognized_segment(s) for s in segments):
            continue
        context = tag.group(0)

        for seg in segments:
            if seg.startswith('style:'):
                style_name = seg[len('style:'):].strip()
                if not validate_style_name(style_name):
                    add(Severity.ERROR, "MDPP002",
                        f"Invalid style name: {style_name}", context,
                        "Style names must start with a letter or underscore, "
                        "followed by letters, digits, hyphens, underscores, or "
                        "spaces (no leading/trailing spaces)")

            elif seg.startswith('markers:'):
                payload = seg[len('markers:'):].strip()
                parsed, error_msg = (None, None)
                if not (payload.startswith('{') and payload.endswith('}')):
                    error_msg = "expected a JSON object in braces"
                    if payload.startswith('{'):
                        error_msg += " (a --> inside a value ends the comment early)"
                else:
                    parsed, error_msg = validate_json(payload)
                    if error_msg is None and not isinstance(parsed, dict):
                        error_msg = "the value must be a JSON object"
                if error_msg:
                    add(Severity.ERROR, "MDPP003",
                        f"Malformed marker JSON: {error_msg}", context,
                        "Ensure JSON is valid with double-quoted keys and "
                        "values; write a double quote inside a value as \\\" "
                        "and the > of --> as \\u003e")
                    continue
                for key in parsed:
                    if not validate_marker_key(key):
                        add(Severity.ERROR, "MDPP002",
                            f"Invalid marker key name: {key}", context,
                            MARKER_KEY_SUGGESTION)

            elif seg.startswith('marker:'):
                body = seg[len('marker:'):]
                split_at = body.find('="')
                if split_at < 0:
                    add(Severity.WARNING, "MDPP020",
                        "Malformed simple marker: expected marker:Key=\"value\"",
                        context,
                        "Write the marker as marker:Key=\"value\", or use the "
                        "markers:{...} JSON form")
                    continue
                key = body[:split_at]
                if not validate_marker_key(key):
                    add(Severity.ERROR, "MDPP002",
                        f"Invalid marker key name: {key.strip()}", context,
                        MARKER_KEY_SUGGESTION)
                value_part = body[split_at + 2:]
                if not value_part.endswith('"'):
                    add(Severity.WARNING, "MDPP020",
                        f"Simple marker value for {key.strip()} has no closing "
                        "double quote", context,
                        "A --> inside a value ends the comment tag early. Use "
                        "the markers:{...} JSON form and write the > of --> as "
                        "\\u003e")
                elif '"' in value_part[:-1]:
                    add(Severity.WARNING, "MDPP020",
                        f"Double quote inside the simple marker value for "
                        f"{key.strip()}", context,
                        "A simple-form value cannot contain a double quote. Use "
                        "the markers:{...} JSON form and write the quote as \\\"")

            elif _is_alias_segment(seg):
                alias_name = seg[1:]
                if re.search(r'[ \t\n\r]', alias_name):
                    # An alias ends at the first ASCII whitespace; text after
                    # it is not part of a valid alias command.
                    continue
                if not validate_alias_name(alias_name):
                    add(Severity.ERROR, "MDPP002",
                        f"Invalid alias name: #{alias_name}", context,
                        "Alias names may use letters from any script (XML "
                        "NCName letter class), digits, and underscore (_). "
                        "Hyphen (-), period (.), middle dot, combining marks, "
                        "and connector punctuation are permitted only in "
                        "non-first positions.")
                key = _alias_dedup_key(alias_name)
                if key in alias_locations:
                    first_line = alias_locations[key]
                    first_name = alias_display[key]
                    if first_name == alias_name:
                        msg = f"Duplicate alias: #{alias_name}"
                    elif first_name.casefold() == alias_name.casefold():
                        msg = (
                            f"Duplicate alias: #{alias_name} "
                            f"(case-insensitive match with #{first_name} on "
                            f"line {first_line})"
                        )
                    else:
                        msg = (
                            f"Duplicate alias: #{alias_name} "
                            f"(matches #{first_name} on line {first_line}; "
                            f"the two forms are visually identical but use "
                            f"different Unicode byte sequences for an accented "
                            f"character)"
                        )
                    add(Severity.ERROR, "MDPP008", msg, context,
                        f"First defined on line {first_line} as "
                        f"#{first_name}. Use a unique alias, or remove "
                        "the duplicate. Comparison uses Unicode NFC + "
                        "case-fold (CommonMark 0.30 slug matching).")
                else:
                    alias_locations[key] = line_num
                    alias_display[key] = alias_name
                    if verbose:
                        print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: Alias defined: #{alias_name}")

    return issues


# Inline code spans: a backtick run, content, and the same run. Their content
# is verbatim text, so a `-->` quoted in prose is not a comment delimiter.
INLINE_CODE_RE = re.compile(r'(`+)(?!`).*?(?<!`)\1(?!`)')


def _scan_stray_comment_close(
    lines: list[str], filepath: str, mask: list[bool]
) -> list[ValidationIssue]:
    """Detect a `-->` with no `<!--` that opens it (MDPP021).

    The usual cause is a `-->` inside a marker value: the first `-->` ends the
    comment tag, and the rest of the tag, with its own `-->`, is left behind as
    text. HTML comments may span lines, so comment state carries across lines.
    Fenced code and inline code spans are skipped.
    """
    issues: list[ValidationIssue] = []
    in_comment = False
    for idx, raw in enumerate(lines):
        if mask[idx]:
            continue
        line = INLINE_CODE_RE.sub(lambda m: ' ' * len(m.group(0)), raw)
        pos = 0
        flagged = False
        while True:
            if in_comment:
                end = line.find('-->', pos)
                if end < 0:
                    break
                in_comment = False
                pos = end + 3
                continue
            start = line.find('<!--', pos)
            end = line.find('-->', pos)
            if end >= 0 and (start < 0 or end < start):
                if not flagged:
                    issues.append(ValidationIssue(
                        type=Severity.WARNING.value,
                        code="MDPP021",
                        message="Comment closing delimiter --> with no <!-- that opens it",
                        file=filepath,
                        line=idx + 1,
                        context=raw.strip()[:60],
                        suggestion=(
                            "A --> inside a marker value ends the comment tag "
                            "early and leaves the rest of the tag as text. Use "
                            "the markers:{...} JSON form and write the > of --> "
                            "as \\u003e."
                        ),
                    ))
                    flagged = True
                pos = end + 3
                continue
            if start < 0:
                break
            in_comment = True
            pos = start + 4
    return issues


def validate_file(filepath: str, verbose: bool = False) -> list[ValidationIssue]:
    """Validate a Markdown++ file."""
    issues = []

    if not os.path.exists(filepath):
        issues.append(ValidationIssue(
            type=Severity.ERROR.value,
            code="MDPP000",
            message="File not found",
            file=filepath,
            line=0,
            context="",
            suggestion="Check the file path"
        ))
        return issues

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        issues.append(ValidationIssue(
            type=Severity.ERROR.value,
            code="MDPP000",
            message=f"Cannot read file: {e}",
            file=filepath,
            line=0,
            context="",
            suggestion="Check file permissions and encoding"
        ))
        return issues

    # Track open conditions for matching
    condition_stack = []

    # Track aliases for uniqueness check (MDPP008).
    # Keyed by NFC + casefold normalized form; values store the first-seen
    # line and the original spelling for error messages.
    alias_locations: dict[str, int] = {}  # normalized key -> first line
    alias_display: dict[str, str] = {}    # normalized key -> original spelling

    mask = _skip_mask(lines)

    for line_num, line in _iter_outside_fences(lines, mask):

        # Check for invalid variable names
        for match in PATTERNS['variable_invalid'].finditer(line):
            var_content = match.group(1)
            if not validate_variable_name(var_content):
                # Check if it might be a valid variable
                valid_match = PATTERNS['variable'].search(match.group(0))
                if not valid_match:
                    issues.append(ValidationIssue(
                        type=Severity.ERROR.value,
                        code="MDPP002",
                        message=f"Invalid variable name: ${var_content};",
                        file=filepath,
                        line=line_num,
                        context=line.strip()[:60],
                        suggestion="Names must start with a letter or underscore, followed by letters, digits, hyphens, or underscores"
                    ))

        # Process condition opens and closes in document order (by position on the line)
        # so that adjacent inline conditions like <!--condition:a-->...<!--/condition--><!--condition:b-->
        # are not falsely flagged as nested.
        condition_events = (
            [(m.start(), 'open', m) for m in PATTERNS['condition_open'].finditer(line)] +
            [(m.start(), 'close', m) for m in PATTERNS['condition_close'].finditer(line)]
        )
        condition_events.sort(key=lambda e: e[0])

        for _pos, event_type, match in condition_events:
            if event_type == 'open':
                expr = match.group(1).strip()
                is_valid, error_msg = validate_condition_expression(expr)
                if not is_valid:
                    issues.append(ValidationIssue(
                        type=Severity.ERROR.value,
                        code="MDPP007",
                        message=f"Invalid condition syntax: {error_msg}",
                        file=filepath,
                        line=line_num,
                        context=match.group(0),
                        suggestion="Condition names must be alphanumeric with hyphens/underscores"
                    ))
                condition_stack.append((line_num, expr))
                if len(condition_stack) > 1:
                    outer_line, outer_expr = condition_stack[-2]
                    issues.append(ValidationIssue(
                        type=Severity.ERROR.value,
                        code="MDPP001",
                        message=f"Nested condition block not permitted (outer block opened at line {outer_line} with expression '{outer_expr}')",
                        file=filepath,
                        line=line_num,
                        context=match.group(0),
                        suggestion="Condition blocks MUST NOT be nested. Use a logical expression instead, e.g. <!--condition:outer inner--> requires both"
                    ))
                if verbose:
                    print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: Condition opened: {expr}")

            else:  # close
                if condition_stack:
                    opened_line, opened_expr = condition_stack.pop()
                    if verbose:
                        print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: Condition closed (opened at line {opened_line})")
                else:
                    issues.append(ValidationIssue(
                        type=Severity.ERROR.value,
                        code="MDPP001",
                        message="Closing condition tag without matching opening tag",
                        file=filepath,
                        line=line_num,
                        context=match.group(0),
                        suggestion="Remove this tag or add a matching <!--condition:name--> above"
                    ))

        # Check every style, marker, markers, and alias command in every
        # comment tag, including combined tags (MDPP002, MDPP003,
        # MDPP008, MDPP020).
        issues.extend(_check_comment_commands(
            line, line_num, filepath, alias_locations, alias_display, verbose
        ))

        # Check includes (warning if file doesn't exist)
        for match in PATTERNS['include'].finditer(line):
            include_path = match.group(1).strip()
            base_dir = os.path.dirname(filepath)
            full_path = os.path.normpath(os.path.join(base_dir, include_path))

            if not os.path.exists(full_path):
                issues.append(ValidationIssue(
                    type=Severity.WARNING.value,
                    code="MDPP006",
                    message=f"Include file not found: {include_path}",
                    file=filepath,
                    line=line_num,
                    context=match.group(0),
                    suggestion=f"Check path relative to {base_dir}"
                ))
            elif verbose:
                print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: Include found: {include_path}")

    # MDPP009: Check for orphaned comment tags (second pass)
    for line_num, line in _iter_outside_fences(lines, mask):
        if not _is_mdpp_tag_line(line):
            continue

        # The very next line must be a content element
        next_line_idx = line_num  # 0-based index of next line (line_num is 1-based)
        if next_line_idx >= len(lines) or not _is_content_line(lines[next_line_idx], tag_line=line):
            issues.append(ValidationIssue(
                type=Severity.WARNING.value,
                code="MDPP009",
                message="Orphaned comment tag (not attached to element)",
                file=filepath,
                line=line_num,
                context=line.strip()[:60],
                suggestion="Remove the blank line between this tag and the element "
                           "it applies to, or combine with an adjacent tag using "
                           "semicolons"
            ))
            if verbose:
                print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: "
                      f"Orphaned tag detected")

    # MDPP018: Multiline tables with no separator rows (silent row merge).
    issues.extend(_scan_multiline_row_merge(lines, filepath))

    # MDPP019: Condition tags embedded in a table row (in-cell span /
    # conditional cell) rather than wrapping complete rows.
    issues.extend(_scan_condition_in_table_cells(lines, filepath))

    # MDPP021: A --> with no <!-- that opens it.
    issues.extend(_scan_stray_comment_close(lines, filepath, mask))

    # Check for unclosed conditions
    for opened_line, opened_expr in condition_stack:
        issues.append(ValidationIssue(
            type=Severity.ERROR.value,
            code="MDPP001",
            message=f"Unclosed condition block: {opened_expr}",
            file=filepath,
            line=opened_line,
            context=f"<!--condition:{opened_expr}-->",
            suggestion="Add <!--/condition--> to close this block"
        ))

    return issues


def print_issue(issue: ValidationIssue, use_color: bool = True) -> None:
    """Print a validation issue to stderr."""
    if use_color:
        if issue.type == Severity.ERROR.value:
            prefix = f"{Colors.RED}[ERROR]{Colors.NC}"
        elif issue.type == Severity.WARNING.value:
            prefix = f"{Colors.YELLOW}[WARNING]{Colors.NC}"
        else:
            prefix = f"{Colors.CYAN}[INFO]{Colors.NC}"
    else:
        prefix = f"[{issue.type.upper()}]"

    print(f"{prefix} {issue.code}: {issue.message}", file=sys.stderr)
    print(f"  File: {issue.file}:{issue.line}", file=sys.stderr)
    if issue.context:
        print(f"  Context: {issue.context}", file=sys.stderr)
    if issue.suggestion:
        print(f"  Suggestion: {issue.suggestion}", file=sys.stderr)
    print(file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Markdown++ document syntax",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0  Valid document (no errors)
  1  File error (not found, not readable)
  2  Invalid arguments
  3  Validation errors found

Examples:
  python validate-mdpp.py document.md
  python validate-mdpp.py document.md --verbose
  python validate-mdpp.py document.md --json
  python validate-mdpp.py document.md --strict
"""
    )
    parser.add_argument('input_file', help='Markdown++ file to validate')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--json', '-j', action='store_true',
                        help='Output errors as JSON')
    parser.add_argument('--strict', '-s', action='store_true',
                        help='Treat warnings as errors')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        if args.json:
            print(json.dumps({
                "valid": False,
                "errors": [{
                    "code": "MDPP000",
                    "message": "File not found",
                    "file": args.input_file
                }]
            }))
        else:
            print(f"{Colors.RED}Error:{Colors.NC} File not found: {args.input_file}",
                  file=sys.stderr)
        return 1

    if args.verbose:
        print(f"{Colors.CYAN}Validating:{Colors.NC} {args.input_file}")

    issues = validate_file(args.input_file, verbose=args.verbose)

    # Filter by severity if strict mode
    errors = [i for i in issues if i.type == Severity.ERROR.value]
    warnings = [i for i in issues if i.type == Severity.WARNING.value]

    if args.strict:
        errors.extend(warnings)
        warnings = []

    if args.json:
        output = {
            "valid": len(errors) == 0,
            "errors": [asdict(i) for i in errors],
            "warnings": [asdict(i) for i in warnings]
        }
        print(json.dumps(output, indent=2))
    else:
        for issue in issues:
            print_issue(issue)

        if not issues:
            print(f"{Colors.GREEN}Valid:{Colors.NC} No issues found in {args.input_file}")
        else:
            error_count = len(errors)
            warning_count = len(warnings)
            summary_parts = []
            if error_count:
                summary_parts.append(f"{error_count} error(s)")
            if warning_count:
                summary_parts.append(f"{warning_count} warning(s)")
            print(f"Found {', '.join(summary_parts)} in {args.input_file}")

    if errors:
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
