#!/usr/bin/env python3
"""
run-tests.py -- generic golden-file test runner for the Markdown++ skill.

A "suite" is any immediate subdirectory of tests/ that contains a
``suite.json`` file. A "case" is any subdirectory of a suite that contains
an ``input.md``. The runner interprets a fixed set of per-case contract
files and ignores everything else (NOTES.txt, etc.).

Contract files per case (all optional except input.md):
  input.md                     the file passed to the formatter (required)
  expected.md                  expected stdout, compared BYTE-FOR-BYTE
  args.txt                     extra CLI flags, whitespace-separated, may span lines
  expected-exit-code.txt       a single integer; default 0 when absent
  expected-stderr-contains.txt each non-empty line must be a substring of stderr
  KNOWN_FAIL.txt               marks the case expected-to-fail today
  NOTES.txt                    free-form context; ignored by the runner

suite.json format:
  {"script": "scripts/format-tables.py"}   (path relative to the skill root)

The runner and all suites live under the skill root:
  plugins/markdown-plus-plus/skills/markdown-plus-plus/
The formatter is invoked from the skill root with the same Python
interpreter running this script (sys.executable), stdout/stderr captured
as raw bytes.

Exit codes:
  0  all good (including expected known-fails)
  1  any failure or unexpected pass
  2  bad arguments

Python 3 standard library only. Cross-platform (Windows + Linux).
"""

import argparse
import difflib
import json
import os
import subprocess
import sys
import tempfile


# ---------------------------------------------------------------------------
# Path anchors
# ---------------------------------------------------------------------------

# tests/ directory (this file lives directly inside it).
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
# Skill root is the parent of tests/. Scripts and suite `script` paths are
# resolved relative to this directory, and the formatter is invoked with it
# as the working directory.
SKILL_ROOT = os.path.dirname(TESTS_DIR)


def find_repo_root(start):
    """Walk upward from *start* to locate the repository root.

    The repo root is the directory that contains both ``examples/`` and
    ``spec/`` (the idempotency sweep targets), falling back to a directory
    containing a ``.git`` entry. Returns the discovered path, or ``None``
    if no such ancestor exists.
    """
    cur = os.path.abspath(start)
    while True:
        has_examples = os.path.isdir(os.path.join(cur, 'examples'))
        has_spec = os.path.isdir(os.path.join(cur, 'spec'))
        if has_examples and has_spec:
            return cur
        if os.path.exists(os.path.join(cur, '.git')):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


REPO_ROOT = find_repo_root(SKILL_ROOT)


# ---------------------------------------------------------------------------
# ANSI colouring (auto-disabled when stdout is not a tty)
# ---------------------------------------------------------------------------

class C:
    enabled = sys.stdout.isatty()

    @classmethod
    def wrap(cls, code, text):
        if not cls.enabled:
            return text
        return f"\033[{code}m{text}\033[0m"


def red(t):
    return C.wrap('0;31', t)


def green(t):
    return C.wrap('0;32', t)


def yellow(t):
    return C.wrap('1;33', t)


def cyan(t):
    return C.wrap('0;36', t)


def bold(t):
    return C.wrap('1', t)


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------

# Case outcome constants.
PASS = 'pass'
FAIL = 'fail'
KNOWN_FAIL = 'known-fail'          # KNOWN_FAIL case that failed (as expected)
UNEXPECTED_PASS = 'unexpected-pass'  # KNOWN_FAIL case that passed


class CaseResult:
    def __init__(self, suite, name):
        self.suite = suite
        self.name = name
        self.outcome = PASS
        self.reasons = []       # list of human-readable failure reasons
        self.diff_text = None   # optional unified diff for stdout mismatch
        self.known_fail_ref = None  # tracking ref (first line of KNOWN_FAIL.txt)

    @property
    def label(self):
        return f"{self.suite}/{self.name}"


# ---------------------------------------------------------------------------
# Contract-file helpers
# ---------------------------------------------------------------------------

def read_bytes(path):
    with open(path, 'rb') as f:
        return f.read()


def read_text(path):
    """Read a small contract text file as UTF-8 (tolerant of a BOM)."""
    with open(path, 'r', encoding='utf-8-sig') as f:
        return f.read()


def parse_args_file(path):
    """Parse args.txt into a list of tokens (whitespace-separated, may span
    lines). Blank lines and lines whose first non-space char is '#' are
    ignored so the file can carry comments."""
    tokens = []
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        tokens.extend(stripped.split())
    return tokens


def parse_expected_stderr(path):
    """Return the list of required substrings (non-empty lines)."""
    subs = []
    for line in read_text(path).splitlines():
        if line.strip():
            subs.append(line.rstrip('\r\n'))
    return subs


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

class Suite:
    def __init__(self, name, path, script_rel):
        self.name = name
        self.path = path            # absolute path to suite dir
        self.script_rel = script_rel  # script path relative to skill root


def discover_suites():
    """Return a list of Suite for every immediate subdir of tests/ that has
    a suite.json."""
    suites = []
    for entry in sorted(os.listdir(TESTS_DIR)):
        sdir = os.path.join(TESTS_DIR, entry)
        if not os.path.isdir(sdir):
            continue
        cfg_path = os.path.join(sdir, 'suite.json')
        if not os.path.isfile(cfg_path):
            continue
        try:
            cfg = json.loads(read_text(cfg_path))
        except (ValueError, OSError) as e:
            print(red(f"ERROR: cannot parse {cfg_path}: {e}"), file=sys.stderr)
            continue
        script_rel = cfg.get('script')
        if not script_rel:
            print(red(f"ERROR: {cfg_path} missing 'script' key"), file=sys.stderr)
            continue
        suites.append(Suite(entry, sdir, script_rel))
    return suites


def discover_cases(suite):
    """Return a sorted list of case names (subdirs containing input.md)."""
    cases = []
    for entry in sorted(os.listdir(suite.path)):
        cdir = os.path.join(suite.path, entry)
        if os.path.isdir(cdir) and os.path.isfile(os.path.join(cdir, 'input.md')):
            cases.append(entry)
    return cases


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def run_formatter(script_rel, input_path, extra_args):
    """Invoke the formatter from the skill root. Returns (stdout_bytes,
    stderr_bytes, exit_code)."""
    cmd = [sys.executable, script_rel, input_path] + list(extra_args)
    proc = subprocess.run(
        cmd,
        cwd=SKILL_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout, proc.stderr, proc.returncode


def evaluate_case(suite, name):
    """Execute one case and return a CaseResult."""
    cdir = os.path.join(suite.path, name)
    result = CaseResult(suite.name, name)

    input_path = os.path.join(cdir, 'input.md')
    args_path = os.path.join(cdir, 'args.txt')
    expected_path = os.path.join(cdir, 'expected.md')
    exit_path = os.path.join(cdir, 'expected-exit-code.txt')
    stderr_path = os.path.join(cdir, 'expected-stderr-contains.txt')
    known_fail_path = os.path.join(cdir, 'KNOWN_FAIL.txt')

    known = os.path.isfile(known_fail_path)
    if known:
        kf_text = read_text(known_fail_path)
        first = kf_text.splitlines()
        result.known_fail_ref = first[0].strip() if first else '(no ref)'

    extra_args = parse_args_file(args_path) if os.path.isfile(args_path) else []

    stdout, stderr, code = run_formatter(suite.script_rel, input_path, extra_args)

    failures = []

    # 1. Exit code.
    expected_code = 0
    if os.path.isfile(exit_path):
        raw = read_text(exit_path).strip()
        try:
            expected_code = int(raw)
        except ValueError:
            failures.append(
                f"expected-exit-code.txt is not an integer: {raw!r}")
    if code != expected_code:
        failures.append(f"exit code {code} != expected {expected_code}")

    # 2. Stdout bytes (only when expected.md is present).
    if os.path.isfile(expected_path):
        expected_bytes = read_bytes(expected_path)
        if stdout != expected_bytes:
            failures.append("stdout does not match expected.md (byte-for-byte)")
            result.diff_text = build_diff(expected_bytes, stdout,
                                          f"{result.label}/expected.md",
                                          "actual-stdout")

    # 3. Stderr substrings.
    if os.path.isfile(stderr_path):
        stderr_text = stderr.decode('utf-8', errors='replace')
        for sub in parse_expected_stderr(stderr_path):
            if sub not in stderr_text:
                failures.append(f"stderr missing substring: {sub!r}")

    result.reasons = failures

    if known:
        # A KNOWN_FAIL case is executed normally; failing is expected.
        if failures:
            result.outcome = KNOWN_FAIL
        else:
            result.outcome = UNEXPECTED_PASS
    else:
        result.outcome = FAIL if failures else PASS

    return result


def build_diff(expected_bytes, actual_bytes, fromname, toname):
    exp = expected_bytes.decode('utf-8', errors='replace').splitlines(keepends=True)
    act = actual_bytes.decode('utf-8', errors='replace').splitlines(keepends=True)
    diff = difflib.unified_diff(exp, act, fromfile=fromname, tofile=toname)
    text = ''.join(diff)
    if not text and expected_bytes != actual_bytes:
        # Difference is only in line endings / trailing bytes that
        # splitlines collapsed. Surface a byte-level note.
        text = (f"--- {fromname}\n+++ {toname}\n"
                f"(no textual diff; byte streams differ -- likely line-ending "
                f"or trailing-newline mismatch)\n"
                f"expected {len(expected_bytes)} bytes, got {len(actual_bytes)} bytes\n")
    return text


# ---------------------------------------------------------------------------
# Idempotency sweep
# ---------------------------------------------------------------------------

def load_allowlist():
    """Return a set of repo-relative paths (normalised with forward slashes)
    to skip during the idempotency sweep."""
    allow = set()
    path = os.path.join(TESTS_DIR, 'format-tables', 'idempotency-allowlist.txt')
    if not os.path.isfile(path):
        return allow
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        allow.add(stripped.replace('\\', '/'))
    return allow


def repo_rel(path):
    """Repo-relative path with forward slashes, for display and allowlisting."""
    if REPO_ROOT is None:
        return path.replace('\\', '/')
    try:
        rel = os.path.relpath(path, REPO_ROOT)
    except ValueError:
        return path.replace('\\', '/')
    return rel.replace('\\', '/')


def gather_sweep_targets(suites):
    """Return an ordered, de-duplicated list of absolute paths to sweep:
    all .md under examples/ and spec/, plus every non-KNOWN_FAIL case's
    input.md across all suites."""
    targets = []
    seen = set()

    def add(p):
        ap = os.path.abspath(p)
        if ap not in seen:
            seen.add(ap)
            targets.append(ap)

    if REPO_ROOT is not None:
        for sub in ('examples', 'spec'):
            base = os.path.join(REPO_ROOT, sub)
            if os.path.isdir(base):
                for root, _dirs, files in os.walk(base):
                    for fn in sorted(files):
                        if fn.endswith('.md'):
                            add(os.path.join(root, fn))

    for suite in suites:
        for name in discover_cases(suite):
            cdir = os.path.join(suite.path, name)
            if os.path.isfile(os.path.join(cdir, 'KNOWN_FAIL.txt')):
                continue
            add(os.path.join(cdir, 'input.md'))

    return targets


def sweep_one(script_rel, path, tmpdir):
    """Run the two-pass idempotency check on *path*. Returns
    ('idempotent'|'nonidempotent'|'error', detail)."""
    out1, err1, code1 = run_formatter(script_rel, path, [])
    if code1 != 0:
        return 'error', f"pass 1 exit {code1}: {err1.decode('utf-8', 'replace').strip()}"
    tmp = os.path.join(tmpdir, 'pass1-' + os.path.basename(path))
    # Ensure uniqueness if basenames collide across dirs.
    n = 0
    while os.path.exists(tmp):
        n += 1
        tmp = os.path.join(tmpdir, f'pass1-{n}-' + os.path.basename(path))
    with open(tmp, 'wb') as f:
        f.write(out1)
    out2, err2, code2 = run_formatter(script_rel, tmp, [])
    if code2 != 0:
        return 'error', f"pass 2 exit {code2}: {err2.decode('utf-8', 'replace').strip()}"
    if out1 == out2:
        return 'idempotent', ''
    return 'nonidempotent', 'pass 1 and pass 2 differ'


def run_idempotency(suites, script_rel, verbose):
    """Run the idempotency sweep. Returns True if all non-allowlisted
    targets are idempotent."""
    allow = load_allowlist()
    targets = gather_sweep_targets(suites)

    idempotent = 0
    nonidempotent = 0
    allowlisted = 0
    errors = 0
    failures = []

    print(bold(cyan("== Idempotency sweep ==")))
    with tempfile.TemporaryDirectory(prefix='mdpp-idem-') as tmpdir:
        for path in targets:
            rel = repo_rel(path)
            if rel in allow:
                allowlisted += 1
                if verbose:
                    print(f"  {yellow('allowlisted')} {rel}")
                continue
            status, detail = sweep_one(script_rel, path, tmpdir)
            if status == 'idempotent':
                idempotent += 1
                if verbose:
                    print(f"  {green('idempotent ')} {rel}")
            elif status == 'nonidempotent':
                nonidempotent += 1
                failures.append((rel, detail))
                print(f"  {red('NON-IDEMPOTENT')} {rel}: {detail}")
            else:  # error
                errors += 1
                failures.append((rel, detail))
                print(f"  {red('ERROR')} {rel}: {detail}")

    print()
    print(bold("Idempotency summary:"))
    print(f"  idempotent   : {idempotent}")
    print(f"  non-idempotent: {nonidempotent}")
    print(f"  errors        : {errors}")
    print(f"  allowlisted   : {allowlisted}")
    if REPO_ROOT is None:
        print(yellow("  (repo root not found; examples/ and spec/ were not swept)"))

    return nonidempotent == 0 and errors == 0


# ---------------------------------------------------------------------------
# Reporting for the normal (case) run
# ---------------------------------------------------------------------------

def print_case_result(result, verbose):
    if result.outcome == PASS:
        if verbose:
            print(f"  {green('PASS')}        {result.label}")
    elif result.outcome == KNOWN_FAIL:
        print(f"  {yellow('known fail')}  {result.label} "
              f"(tracked: {result.known_fail_ref})")
        if verbose:
            for r in result.reasons:
                print(f"      - {r}")
    elif result.outcome == UNEXPECTED_PASS:
        print(f"  {red('UNEXPECTED PASS')} {result.label} "
              f"-- remove KNOWN_FAIL.txt to promote")
    else:  # FAIL
        print(f"  {red('FAIL')}        {result.label}")
        for r in result.reasons:
            print(f"      - {r}")
        if result.diff_text:
            for line in result.diff_text.splitlines():
                print(f"      | {line}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog='run-tests.py',
        description='Generic golden-file test runner for the Markdown++ skill.',
    )
    p.add_argument('suite', nargs='?', default=None,
                   help='optional suite name filter (e.g. format-tables)')
    p.add_argument('--filter', metavar='SUBSTR', default=None,
                   help='run only cases whose name contains SUBSTR')
    p.add_argument('--list', action='store_true',
                   help='enumerate discovered cases without running them')
    p.add_argument('--idempotency', action='store_true',
                   help='run the idempotency sweep instead of the case suite')
    p.add_argument('--verbose', '-v', action='store_true',
                   help='verbose output (per-pass detail, passing cases)')
    return p


def main(argv):
    parser = build_parser()
    # argparse exits with code 2 on bad args, which matches our contract.
    args = parser.parse_args(argv)

    all_suites = discover_suites()

    if args.suite is not None:
        selected = [s for s in all_suites if s.name == args.suite]
        if not selected:
            names = ', '.join(s.name for s in all_suites) or '(none)'
            print(red(f"No suite named {args.suite!r}. Available: {names}"),
                  file=sys.stderr)
            return 2
    else:
        selected = all_suites

    if not selected:
        print(yellow("No suites discovered under tests/ (need a suite.json)."),
              file=sys.stderr)
        # Nothing to do is not an error condition per se, but signals a
        # misconfiguration for the case run. Return 0 for --list, else 1.
        return 0 if args.list else 1

    # --- idempotency sweep mode ---------------------------------------
    if args.idempotency:
        # The sweep uses the first selected suite's script (the formatter
        # under test). All current suites share format-tables.py; if
        # multiple suites exist, sweep with each distinct script in turn.
        scripts = []
        for s in selected:
            if s.script_rel not in scripts:
                scripts.append(s.script_rel)
        ok = True
        for script_rel in scripts:
            if not run_idempotency(selected, script_rel, args.verbose):
                ok = False
        return 0 if ok else 1

    # --- list mode -----------------------------------------------------
    if args.list:
        total = 0
        for suite in selected:
            names = discover_cases(suite)
            if args.filter:
                names = [n for n in names if args.filter in n]
            print(bold(cyan(f"{suite.name}  (script: {suite.script_rel})")))
            for n in names:
                cdir = os.path.join(suite.path, n)
                tag = ''
                if os.path.isfile(os.path.join(cdir, 'KNOWN_FAIL.txt')):
                    tag = yellow(' [KNOWN_FAIL]')
                print(f"  {n}{tag}")
                total += 1
        print()
        print(f"{total} case(s).")
        return 0

    # --- normal case run ----------------------------------------------
    n_pass = n_fail = n_known = n_unexpected = 0

    for suite in selected:
        names = discover_cases(suite)
        if args.filter:
            names = [n for n in names if args.filter in n]
        if not names:
            continue
        print(bold(cyan(f"== Suite: {suite.name} ==")))
        for name in names:
            result = evaluate_case(suite, name)
            print_case_result(result, args.verbose)
            if result.outcome == PASS:
                n_pass += 1
            elif result.outcome == FAIL:
                n_fail += 1
            elif result.outcome == KNOWN_FAIL:
                n_known += 1
            elif result.outcome == UNEXPECTED_PASS:
                n_unexpected += 1
        print()

    print(bold("== Summary =="))
    print(f"  pass           : {n_pass}")
    print(f"  fail           : {n_fail}")
    print(f"  known-fail     : {n_known}")
    print(f"  unexpected-pass: {n_unexpected}")

    ok = (n_fail == 0 and n_unexpected == 0)
    if ok:
        print(green(bold("ALL GREEN")))
    else:
        print(red(bold("FAILURES PRESENT")))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
