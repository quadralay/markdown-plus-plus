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
    'style': re.compile(r'<!--\s*style:([^>]+?)(?:\s*;|\s*-->)'),
    'alias': re.compile(r'<!--\s*#([^\s;>]+?)(?=\s*;|\s*-->)'),
    'condition_open': re.compile(r'<!--\s*condition:([^>]+?)\s*-->'),
    'condition_close': re.compile(r'<!--\s*/condition\s*-->'),
    'include': re.compile(r'<!--\s*include:([^>]+?)\s*-->'),
    'markers_json': re.compile(r'<!--\s*markers:(\{[^}]+\})\s*-->'),
    'marker_simple': re.compile(r'<!--\s*marker:([^=]+)="([^"]+)"'),
    'multiline': re.compile(r'<!--\s*multiline\s*-->'),
}


STANDARD_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_-]*$')
ALIAS_NAME_RE = re.compile(r'^[a-zA-Z0-9_][a-zA-Z0-9_-]*$')


def validate_variable_name(name: str) -> bool:
    """Check if a variable name is valid."""
    return bool(STANDARD_NAME_RE.match(name))


def validate_style_name(name: str) -> bool:
    """Check if a style name is valid."""
    return bool(STANDARD_NAME_RE.match(name))


def validate_alias_name(name: str) -> bool:
    """Check if an alias name is valid (digit-first allowed)."""
    return bool(ALIAS_NAME_RE.match(name))


def validate_marker_key(name: str) -> bool:
    """Check if a marker key name is valid."""
    return bool(STANDARD_NAME_RE.match(name))


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


# Pattern matching non-exempt MDPP comment tags (style, alias, marker, multiline)
MDPP_TAG_PATTERN = re.compile(
    r'<!--\s*(?:style:|#[^\s;>]+|markers?:|multiline)'
)

# Code fence opening/closing pattern (CommonMark 0.30)
CODE_FENCE_PATTERN = re.compile(r'^\s{0,3}(`{3,}|~{3,})')


def _is_mdpp_tag_line(line: str) -> bool:
    """True if line's only non-whitespace content is an MDPP comment tag."""
    stripped = line.strip()
    if not stripped.startswith('<!--') or not stripped.endswith('-->'):
        return False
    return bool(MDPP_TAG_PATTERN.match(stripped))


def _is_content_line(line: str) -> bool:
    """True if line is a non-blank, non-MDPP-tag content element."""
    if not line.strip():
        return False
    return not _is_mdpp_tag_line(line)


def _iter_outside_fences(lines: list[str]) -> Iterator[tuple[int, str]]:
    """Yield (1-based line_num, line) for lines outside fenced code blocks.

    Tracks opening fence character and count per CommonMark 0.30:
    closing fence must use the same character and at least as many repetitions.
    """
    in_fence = False
    fence_char: str | None = None
    fence_count = 0
    for line_num, line in enumerate(lines, start=1):
        m = CODE_FENCE_PATTERN.match(line)
        if m:
            char = m.group(1)[0]
            count = len(m.group(1))
            if not in_fence:
                in_fence = True
                fence_char = char
                fence_count = count
                continue
            elif char == fence_char and count >= fence_count:
                in_fence = False
                fence_char = None
                continue
        if not in_fence:
            yield line_num, line


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

    # Track aliases for uniqueness check
    alias_locations: dict[str, int] = {}  # alias -> first line number

    for line_num, line in _iter_outside_fences(lines):

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

        # Check for invalid style names
        for match in PATTERNS['style'].finditer(line):
            style_name = match.group(1).strip()
            if not validate_style_name(style_name):
                issues.append(ValidationIssue(
                    type=Severity.ERROR.value,
                    code="MDPP002",
                    message=f"Invalid style name: {style_name}",
                    file=filepath,
                    line=line_num,
                    context=line.strip()[:60],
                    suggestion="Names must start with a letter or underscore, followed by letters, digits, hyphens, or underscores"
                ))

        # Check condition opens
        for match in PATTERNS['condition_open'].finditer(line):
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
            if verbose:
                print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: Condition opened: {expr}")

        # Check condition closes
        for match in PATTERNS['condition_close'].finditer(line):
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

        # Check markers JSON
        for match in PATTERNS['markers_json'].finditer(line):
            json_str = match.group(1)
            parsed, error_msg = validate_json(json_str)
            if error_msg:
                issues.append(ValidationIssue(
                    type=Severity.ERROR.value,
                    code="MDPP003",
                    message=f"Malformed marker JSON: {error_msg}",
                    file=filepath,
                    line=line_num,
                    context=match.group(0)[:60],
                    suggestion="Ensure JSON is valid with double-quoted keys and values"
                ))
            else:
                # Validate marker key names in valid JSON
                if isinstance(parsed, dict):
                    for key in parsed:
                        if not validate_marker_key(key):
                            issues.append(ValidationIssue(
                                type=Severity.ERROR.value,
                                code="MDPP002",
                                message=f"Invalid marker key name: {key}",
                                file=filepath,
                                line=line_num,
                                context=line.strip()[:60],
                                suggestion="Names must start with a letter or underscore, followed by letters, digits, hyphens, or underscores"
                            ))

        # Check simple marker key names
        for match in PATTERNS['marker_simple'].finditer(line):
            marker_key = match.group(1).strip()
            if not validate_marker_key(marker_key):
                issues.append(ValidationIssue(
                    type=Severity.ERROR.value,
                    code="MDPP002",
                    message=f"Invalid marker key name: {marker_key}",
                    file=filepath,
                    line=line_num,
                    context=line.strip()[:60],
                    suggestion="Names must start with a letter or underscore, followed by letters, digits, hyphens, or underscores"
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

        # Check aliases for name validity and duplicates
        for match in PATTERNS['alias'].finditer(line):
            alias_name = match.group(1)
            if not validate_alias_name(alias_name):
                issues.append(ValidationIssue(
                    type=Severity.ERROR.value,
                    code="MDPP002",
                    message=f"Invalid alias name: #{alias_name}",
                    file=filepath,
                    line=line_num,
                    context=match.group(0),
                    suggestion="Alias names must start with a letter, digit, or underscore, followed by letters, digits, hyphens, or underscores"
                ))
            if alias_name in alias_locations:
                issues.append(ValidationIssue(
                    type=Severity.ERROR.value,
                    code="MDPP008",
                    message=f"Duplicate alias: #{alias_name}",
                    file=filepath,
                    line=line_num,
                    context=match.group(0),
                    suggestion=f"First defined on line {alias_locations[alias_name]}. Use unique alias values."
                ))
            else:
                alias_locations[alias_name] = line_num
                if verbose:
                    print(f"{Colors.CYAN}[VERBOSE]{Colors.NC} Line {line_num}: Alias defined: #{alias_name}")

    # MDPP009: Check for orphaned comment tags (second pass)
    for line_num, line in _iter_outside_fences(lines):
        if not _is_mdpp_tag_line(line):
            continue

        # The very next line must be a content element
        next_line_idx = line_num  # 0-based index of next line (line_num is 1-based)
        if next_line_idx >= len(lines) or not _is_content_line(lines[next_line_idx]):
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
