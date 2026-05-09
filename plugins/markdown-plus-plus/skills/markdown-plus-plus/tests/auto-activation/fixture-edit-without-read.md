---
date: 2026-05-09
status: active
mdpp-version: 1.0
---

# CLI Reference Overview

This fixture is the G4 counterpart to `fixture-multiline-table-buried.md`.
The structure is intentionally similar — long preamble, `<!-- multiline -->`
directive past line 30 — but this file declares `mdpp-version: 1.0` in
the frontmatter. The sentinel surfaces in the first 3-5 lines of any
read, including partial reads, so the routing layer encounters a
distinguishing Markdown++ signal even when the directive-bearing lines
are not yet in context.

## Background

The CLI ships with the desktop installer and is also available as a
standalone download for headless environments. It exposes the same
operations as the web console: project management, run inspection, and
artifact retrieval.

Configuration files live under the user's home directory. Subcommands
accept flags that override config values for one-off invocations.

Authentication uses the same tokens as the API. The CLI caches tokens
in the OS keychain on platforms that provide one and falls back to a
config file otherwise.

Output defaults to human-readable text. Most subcommands accept
`--json` for machine-readable output. Scripts should always pass
`--json` to avoid breaking when the human-readable format changes.

## Reading the Tables Below

Each subcommand table lists the name, common flags, and a one-line
summary. Run `app help <subcommand>` for the complete flag reference.

## Subcommand Index

<!-- multiline -->
| Subcommand   | Common Flags             | Summary                  |
|--------------|--------------------------|--------------------------|
| `projects`   | `--all`, `--mine`        | List or filter projects. |
|              |                          | Defaults to current org. |
|              |                          |                          |
| `runs`       | `--project`, `--status`  | Inspect build runs.      |
|              |                          | Streams logs by default. |
|              |                          |                          |
| `artifacts`  | `--run`, `--out`         | Download build outputs.  |
|              |                          | Resumes on interruption. |

## Errors

Subcommands exit with a non-zero status code on failure. The first line
of stderr is a short summary; subsequent lines provide context. Use
`--json` for structured error output.

## Changelog

CLI release notes live alongside the API changelog. The CLI version
tracks the API version it ships against.
