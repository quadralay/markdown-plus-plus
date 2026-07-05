---
date: 2026-07-03
status: active
---

# format-tables test suite

Golden-file regression suite for
[`scripts/format-tables.py`](../../scripts/format-tables.py), driven by the
generic runner [`tests/run-tests.py`](../run-tests.py). This suite is the
regression gate for issues #120, #121, and #122, superseding the manual
AE1–AE7 protocol in [`tests/format-tables-cases.md`](../format-tables-cases.md)
(kept as human-readable documentation of the original cases).

The runner is Python 3 **standard library only** and runs unchanged on
Windows authoring machines and Linux CI.

## Suite layout

A *suite* is any immediate subdirectory of `tests/` that contains a
`suite.json`. This directory (`tests/format-tables/`) is the first suite.
Adding a future suite (for example `validate-mdpp.py`) requires only a new
sibling directory with its own `suite.json` and cases — **no changes to the
runner core**.

```
tests/
├── run-tests.py                # generic runner (all suites share it)
└── format-tables/
    ├── suite.json              # {"script": "scripts/format-tables.py"}
    ├── idempotency-allowlist.txt
    ├── README.md               # this file
    ├── smoke-basic/            # trivial green case validating the runner
    │   ├── input.md
    │   └── expected.md
    └── <case-name>/            # one directory per case
        └── ...
```

`suite.json` names the script under test, relative to the **skill root**
(`plugins/markdown-plus-plus/skills/markdown-plus-plus/`):

```json
{"script": "scripts/format-tables.py"}
```

## Case format contract

Each test case is one kebab-case directory under the suite root. It
contains the following files; only `input.md` is required. The runner
interprets **only** these files and ignores anything else (`NOTES.txt`
included).

| File | Required | Meaning |
|------|----------|---------|
| `input.md` | yes | The file passed to the formatter. |
| `expected.md` | no | Expected stdout, compared **byte-for-byte** (line endings matter). |
| `args.txt` | no | Extra CLI flags for `format-tables.py`, whitespace-separated, may span lines. Blank lines and `#` comment lines are ignored. |
| `expected-exit-code.txt` | no | A single integer; default `0` when absent. |
| `expected-stderr-contains.txt` | no | Each non-empty line must appear as a **substring** of stderr. |
| `KNOWN_FAIL.txt` | no | Marks the case expected-to-fail today. First line: tracking ref (e.g. `#120` or `design-doc known limitation`); remaining lines: one-sentence reason. |
| `NOTES.txt` | no | Free-form context for humans; the runner ignores it. |

### Execution semantics

For each case, from the **skill root**, the runner executes:

```
python scripts/format-tables.py <abs path to case>/input.md <args...>
```

using the same Python interpreter that runs the runner (`sys.executable`),
capturing stdout and stderr as **bytes**. It then compares:

1. **stdout** to `expected.md` bytes (only when `expected.md` is present),
2. **exit code** to `expected-exit-code.txt` (default `0`),
3. **stderr** substrings from `expected-stderr-contains.txt` (each required
   line must be a substring of decoded stderr).

Stdout mismatches print a readable unified diff (decoded UTF-8 with
`errors='replace'`). All comparisons that gate pass/fail are done on raw
bytes, so CRLF vs LF and trailing-newline differences are real failures.

### Fixture frontmatter

`input.md` and `expected.md` should start with the repo-standard YAML
frontmatter block:

```yaml
---
date: 2026-07-03
status: active
---
```

The formatter passes non-table content through byte-for-byte, so
`expected.md` carries the identical block. Ported messy specimens and
byte-sensitive cases (BOM, CRLF) are exempt — use judgement and record the
exemption in `NOTES.txt`.

### Generating goldens (byte fidelity)

**Never** generate `expected.md` via PowerShell/shell redirection — it
re-encodes bytes and rewrites line endings. Generate goldens with a small
Python one-off run from the skill root:

```python
import subprocess, sys
r = subprocess.run(
    [sys.executable, 'scripts/format-tables.py', '<case>/input.md'],
    capture_output=True,
)
open('<case>/expected.md', 'wb').write(r.stdout)
```

Files that need exact CRLF or BOM bytes must be written with Python
`open(path, 'wb')`, not an editor that normalises line endings.

## Runner CLI

Run from the **skill root**:

```bash
cd plugins/markdown-plus-plus/skills/markdown-plus-plus
python tests/run-tests.py [suite] [--filter SUBSTR] [--list] [--idempotency] [--verbose]
```

| Argument | Effect |
|----------|--------|
| `[suite]` | Optional positional suite-name filter (e.g. `format-tables`). Omit to run all discovered suites. |
| `--filter SUBSTR` | Run only cases whose directory name contains `SUBSTR` — the tight inner loop while implementing. |
| `--list` | Enumerate discovered cases without running them (known-fail cases are tagged). |
| `--idempotency` | Run the idempotency sweep (below) instead of the case suite. |
| `--verbose` | Show passing cases and per-target sweep detail. |

**Exit codes:** `0` = all good (including expected known-fails); `1` = any
failure or unexpected pass; `2` = bad arguments.

The summary footer reports counts of pass / fail / known-fail /
unexpected-pass (and idempotent / non-idempotent / allowlisted in sweep
mode).

## KNOWN_FAIL workflow (red → green loop)

A case carrying a `KNOWN_FAIL.txt` is **executed normally**, but its result
is interpreted against the expectation that it currently fails:

- If it **fails**, the runner reports `known fail (tracked: <first line>)`
  and does **not** fail the run. This is what lets red fixtures for
  #120/#121/#122 and pre-existing bugs live in the suite without blocking
  the gate.
- If it **passes**, the runner reports `UNEXPECTED PASS — remove
  KNOWN_FAIL.txt to promote` **and fails the run**. An unexpected pass means
  the behavior was fixed and the fixture should be promoted to green.

### The loop for #120 / #121 / #122

1. **Red.** Author a failing fixture: `input.md`, the target `expected.md`
   (the shape you *want* the formatter to produce), any `args.txt`, and a
   `KNOWN_FAIL.txt` whose first line is the tracking issue (e.g. `#120`) and
   whose second line states the one-sentence reason. Commit it. The gate
   stays green because known-fails don't fail the run.

   ```bash
   python tests/run-tests.py format-tables --filter <case>   # reports "known fail"
   ```

2. **Implement.** Do the formatter work in the issue's PR. Re-run the tight
   loop:

   ```bash
   python tests/run-tests.py format-tables --filter <case>
   ```

   While the behavior is still wrong the case reports `known fail`. Once the
   implementation is correct the case reports **`UNEXPECTED PASS`** and the
   run goes red — that red is the signal that the fix landed.

3. **Green.** Delete the case's `KNOWN_FAIL.txt`. Re-run: the case now
   reports `PASS` and the whole suite is green again. Commit the deletion in
   the same PR as the fix.

This keeps `main` continuously green while still committing the target
behavior up front as an executable specification.

### AE3 caveat

The design doc notes AE3 encodes R8 local row widening, which #120's
soft-width rule intentionally replaces. If an AE3-derived golden is present,
it is committed as-is and **regenerated in the #120 PR** — the framework
must not fossilize the old R8 behavior as sacred.

## Idempotency sweep

```bash
python tests/run-tests.py --idempotency
```

For each target the runner formats it once with **default flags** (pass 1),
writes those bytes to a temp file, formats the temp file (pass 2), and
byte-compares pass 1 vs pass 2. The design doc calls this "the test that
catches everything."

**Targets:** every `.md` under `<repo root>/examples/` and
`<repo root>/spec/`, plus every non-`KNOWN_FAIL` case's `input.md` across
all suites.

**Allowlist:** paths listed in
[`idempotency-allowlist.txt`](idempotency-allowlist.txt) (one repo-relative
path per line, `#` comments allowed) are skipped and reported as
`allowlisted`. Use it only for genuinely known, tracked non-idempotency
(e.g. the documented `auto`-strategy limitation), never to paper over a
fixture bug.

## smoke-basic

[`smoke-basic/`](smoke-basic/) is the one trivial green case that validates
the runner end-to-end: a small standard table that needs realignment, with
its golden generated per the byte-fidelity rules above. If `smoke-basic`
fails, suspect the runner or the environment before the formatter.
