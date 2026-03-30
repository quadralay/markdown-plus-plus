#!/usr/bin/env python3
"""
add-aliases.py

Add unique alias values to headings in a Markdown++ document.

Usage:
    python add-aliases.py <input_file> [options]

Options:
    --help          Show this help message
    --levels        Comma-separated heading levels to process (e.g., 1,2,3)
    --dry-run       Preview changes without modifying file
    --prefix        Add prefix to generated aliases (e.g., "doc-")
    --output        Write to different file instead of modifying in-place

Exit Codes:
    0 - Success
    1 - File error (not found, not readable)
    2 - Invalid arguments
"""

import argparse
import os
import re
import sys
from typing import Optional


# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[0;32m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


# Regex patterns
HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
ALIAS_PATTERN = re.compile(r'<!--\s*#([a-zA-Z0-9_-]+)')
EXISTING_ALIAS_LINE = re.compile(r'^<!--\s*#[a-zA-Z0-9_-]+.*-->\s*$')


def slugify(text: str) -> str:
    """Convert heading text to a URL-friendly slug."""
    # Remove markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # italic
    text = re.sub(r'`([^`]+)`', r'\1', text)        # code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links

    # Convert to lowercase
    text = text.lower()

    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    # Collapse multiple hyphens
    text = re.sub(r'-+', '-', text)

    return text


def has_alias_above(lines: list[str], line_idx: int) -> bool:
    """Check if the line above contains an alias definition."""
    if line_idx == 0:
        return False
    prev_line = lines[line_idx - 1].strip()
    return bool(EXISTING_ALIAS_LINE.match(prev_line))


def get_existing_aliases(content: str) -> set[str]:
    """Extract all existing alias names from the content."""
    aliases = set()
    for match in ALIAS_PATTERN.finditer(content):
        aliases.add(match.group(1))
    return aliases


def make_unique_alias(base: str, existing: set[str]) -> str:
    """Generate a unique alias by appending a number if needed."""
    if base not in existing:
        return base

    counter = 2
    while f"{base}-{counter}" in existing:
        counter += 1
    return f"{base}-{counter}"


def process_file(
    filepath: str,
    levels: set[int],
    prefix: str = "",
    dry_run: bool = False,
    output_path: Optional[str] = None,
    verbose: bool = False
) -> tuple[int, list[str]]:
    """
    Process a Markdown++ file and add aliases to headings.

    Returns:
        Tuple of (number of aliases added, list of changes made)
    """
    if not os.path.exists(filepath):
        print(f"{Colors.RED}Error:{Colors.NC} File not found: {filepath}", file=sys.stderr)
        return -1, []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        print(f"{Colors.RED}Error:{Colors.NC} Cannot read file: {e}", file=sys.stderr)
        return -1, []

    existing_aliases = get_existing_aliases(content)
    new_lines = []
    changes = []
    aliases_added = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        match = HEADING_PATTERN.match(line)

        if match:
            heading_level = len(match.group(1))
            heading_text = match.group(2).strip()

            if heading_level in levels:
                # Check if this heading already has an alias above
                if has_alias_above(lines, i):
                    if verbose:
                        print(f"{Colors.CYAN}[SKIP]{Colors.NC} Line {i + 1}: Already has alias")
                    new_lines.append(line)
                else:
                    # Generate alias
                    base_alias = prefix + slugify(heading_text)
                    if not base_alias:
                        base_alias = f"{prefix}heading"

                    unique_alias = make_unique_alias(base_alias, existing_aliases)
                    existing_aliases.add(unique_alias)

                    alias_line = f"<!--#{unique_alias}-->"
                    new_lines.append(alias_line)
                    new_lines.append(line)
                    aliases_added += 1

                    change_msg = f"Line {i + 1}: Added <!--#{unique_alias}--> for '{heading_text[:40]}...'" if len(heading_text) > 40 else f"Line {i + 1}: Added <!--#{unique_alias}--> for '{heading_text}'"
                    changes.append(change_msg)

                    if verbose:
                        print(f"{Colors.GREEN}[ADD]{Colors.NC} {change_msg}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

        i += 1

    if aliases_added > 0 and not dry_run:
        output_file = output_path or filepath
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print(f"{Colors.GREEN}Success:{Colors.NC} Added {aliases_added} alias(es) to {output_file}")
        except Exception as e:
            print(f"{Colors.RED}Error:{Colors.NC} Cannot write file: {e}", file=sys.stderr)
            return -1, changes
    elif aliases_added > 0 and dry_run:
        print(f"{Colors.YELLOW}Dry run:{Colors.NC} Would add {aliases_added} alias(es)")

    return aliases_added, changes


def parse_levels(levels_str: str) -> set[int]:
    """Parse comma-separated levels string into a set of integers."""
    levels = set()
    for part in levels_str.split(','):
        part = part.strip()
        if part.isdigit():
            level = int(part)
            if 1 <= level <= 6:
                levels.add(level)
    return levels


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add unique alias values to headings in Markdown++ documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python add-aliases.py document.md --levels 1,2,3
  python add-aliases.py document.md --levels 1,2 --prefix "doc-"
  python add-aliases.py document.md --levels 1,2,3 --dry-run
  python add-aliases.py document.md --levels 2 --output output.md
"""
    )
    parser.add_argument('input_file', help='Markdown++ file to process')
    parser.add_argument('--levels', '-l', required=True,
                        help='Comma-separated heading levels to process (e.g., 1,2,3)')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Preview changes without modifying file')
    parser.add_argument('--prefix', '-p', default='',
                        help='Add prefix to generated aliases')
    parser.add_argument('--output', '-o',
                        help='Write to different file instead of modifying in-place')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    levels = parse_levels(args.levels)
    if not levels:
        print(f"{Colors.RED}Error:{Colors.NC} No valid heading levels specified. Use 1-6.", file=sys.stderr)
        return 2

    if args.verbose:
        print(f"{Colors.CYAN}Processing:{Colors.NC} {args.input_file}")
        print(f"{Colors.CYAN}Levels:{Colors.NC} {sorted(levels)}")
        if args.prefix:
            print(f"{Colors.CYAN}Prefix:{Colors.NC} {args.prefix}")

    count, changes = process_file(
        args.input_file,
        levels=levels,
        prefix=args.prefix,
        dry_run=args.dry_run,
        output_path=args.output,
        verbose=args.verbose
    )

    if count < 0:
        return 1

    if args.dry_run and changes:
        print(f"\n{Colors.CYAN}Changes that would be made:{Colors.NC}")
        for change in changes:
            print(f"  {change}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
