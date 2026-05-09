---
date: 2026-05-09
status: active
---

# Markdown++ Skill Auto-Activation Cases

This directory holds a manual-verification suite for the Markdown++
skill's auto-activation behavior. Each case pairs a verbatim prompt with
a fixture file in this directory and records the expected outcome.

## What This Suite Is (And Is Not)

This is **not** a CI test suite. Skill auto-activation is a model-routing
decision that happens in the Claude Code runtime; no in-repo facility
can simulate it. There is no harness that exercises the routing layer
from a script.

Instead, the suite is a **manual checklist** you run by hand in a fresh
Claude Code session. The fixtures and prompts are the inputs; the
expected outcomes are the assertions; observation is the evaluation.

The suite exists so future revisions to the skill — especially to the
`description:` frontmatter in
[`SKILL.md`](../../SKILL.md) — can be regression-checked against the
five gap patterns the brainstorm enumerated. See the [routing-context
principle learning](../../../../../docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md)
for the principles behind these cases.

This suite is also distinct from the sibling `tests/sample-*.md`
fixtures, which feed `validate-mdpp.py`. Those test syntax validation;
these test routing-layer activation.

## How to Run a Case

1. Open a fresh Claude Code session in this repository (so prior
   conversation context cannot influence routing).
2. Paste the case's verbatim prompt. Where the prompt names a fixture
   path, use the path as written.
3. Observe whether the `markdown-plus-plus:markdown-plus-plus` skill
   auto-loads before the agent acts on the file.
4. Record the result for each case in the placeholder below or in your
   PR description.

For G2 specifically, run the case twice: once with the repository's
top-level `CLAUDE.md` loaded as user context (the default for sessions
opened in this repo), and once in a context where it is not (e.g., a
sub-agent flow that does not auto-load CLAUDE.md). The expected
contrast is the closure path's whole point.

## Cases

### G1 — Derivative file creation

**Prompt:**

```
Create a 2.5 release notes file like fixture-derivative-source.md.
```

**Fixture:** [`fixture-derivative-source.md`](fixture-derivative-source.md)

**Expected behavior:** Skill auto-loads. The file the user names contains
multiple distinguishing signals (`<!--style:-->`, `<!-- multiline -->`,
`mdpp-version:`), and the SKILL.md description's derivative-file clause
covers the "create a file modeled after another" framing.

**Rationale:** Issue #84 added the derivative-file clause to the skill
description specifically to close this case. The fixture exists so any
future revision that drops or weakens that clause is detectable.

**Closure path:** (D) Out of scope — the description-level fix shipped
in #84 already covers this. Fixture is regression-only.

### G2 — Vague prompt with no path

**Prompt:**

```
Update the docs to mention the new install URL.
```

**Fixture:** [`fixture-vague-prompt-target.md`](fixture-vague-prompt-target.md)
(the file the user *intends* but does not name)

**Expected behavior:**

- **With this repo's `CLAUDE.md` in context:** Skill auto-loads. The
  CLAUDE.md "Working with Markdown++ files" section directs the agent
  to invoke the skill before editing any `.md` file in this repo.
- **Without this repo's `CLAUDE.md`** (sub-agent flows, headless
  contexts that suppress CLAUDE.md): Skill may not auto-load. This is
  a known limitation — there are no Markdown++ signals in the prompt
  for the routing layer to match on.

**Rationale:** Vague prompts cannot be matched by the skill's
`description:` because the distinguishing signals do not exist in the
prompt text. Closure has to live in the consuming repo's project
guidance, where prompt-shape conventions can override description-only
matching.

**Closure path:** (C) Project-level CLAUDE.md guidance. Mirrored as
suggested language in `references/best-practices.md` for downstream
repositories.

### G3 — Buried `<!-- multiline -->` directive (no sentinel)

**Prompt:**

```
Add a row for `/projects/{id}/permissions` to the endpoint table in
fixture-multiline-table-buried.md.
```

**Fixture:** [`fixture-multiline-table-buried.md`](fixture-multiline-table-buried.md)

**Expected behavior:** Skill activation is unreliable when the agent's
read excerpt stops before the `<!-- multiline -->` line. The fixture
deliberately omits `mdpp-version:` from the frontmatter to make this
visible. Compare against G4.

**Rationale:** When the only signal in a file sits past the routing
layer's read window, the description has nothing to match on. The
mitigation is the frontmatter sentinel from G4, not a description
revision.

**Closure path:** (B) Frontmatter sentinel convention. Promote
`mdpp-version: 1.0` from SHOULD to **strongly recommended** in
`references/best-practices.md` so files using extensions surface a
signal in their first 3-5 lines.

### G4 — Edit without prior Read (sentinel present)

**Prompt:**

```
Add a row for the `permissions` subcommand to the subcommand table in
fixture-edit-without-read.md.
```

**Fixture:** [`fixture-edit-without-read.md`](fixture-edit-without-read.md)

**Expected behavior:** Skill auto-loads when the file is read.
`mdpp-version: 1.0` in the frontmatter surfaces a Markdown++ signal in
the first 3-5 lines, so even a partial-read excerpt brings a
distinguishing signal into routing context.

The CLAUDE.md "Working with Markdown++ files" section also directs the
agent to Read before editing any `.md` file in this repo, which
guarantees the sentinel is surfaced.

**Rationale:** This is the contrast case for G3. The two files are
structurally similar; only the frontmatter differs. The contrast
between G3 and G4 demonstrates the sentinel mitigation in action.

**Closure path:** (B) sentinel + (C) read-before-edit guidance. Both
mitigations apply and reinforce each other.

### G5 — Markdown++ syntax in non-`.md` extension

**Prompt:**

```
Update fixture-no-md-extension.txt to add a Step 3 row.
```

**Fixture:** [`fixture-no-md-extension.txt`](fixture-no-md-extension.txt)

**Expected behavior:** Skill **does not auto-activate**, by design.
This is the documented intentional outcome.

**Rationale:** Markdown++ is a `.md`-only format. Listing additional
extensions in the SKILL.md description would over-trigger on plain
CommonMark `.txt` files that happen to use dollar-sign-and-semicolon
tokens or HTML comments. The cost of over-triggering on every
release-notes `.txt` in every consuming repo outweighs the benefit of
catching stray Markdown++ syntax in non-`.md` files.

**Closure path:** (D) Out of scope — document the position. This case
exists in the suite to foreclose well-meaning future PRs that try to
"fix" G5 by widening the description's extension list.

## Results Placeholder

Use this template when running the suite. Paste a populated copy into
your PR description.

| Case | Expected           | Observed | Notes                       |
|------|--------------------|----------|-----------------------------|
| G1   | Activates          |          |                             |
| G2a  | Activates (CLAUDE) |          | With CLAUDE.md in context   |
| G2b  | May not activate   |          | Without CLAUDE.md           |
| G3   | Unreliable         |          | Compare to G4               |
| G4   | Activates          |          | Sentinel in frontmatter     |
| G5   | Does not activate  |          | Intentional — by design     |

## Regression Discipline

Future revisions to `SKILL.md`'s `description:` frontmatter must run
this checklist and record the results in the PR. Any revision that
breaks an expected outcome must explain the regression in its PR
description and justify the trade-off.

The G5 expected outcome is non-negotiable in particular: revising the
description to make the skill auto-fire on `.txt` files (or any other
non-`.md` extension) will over-trigger on plain CommonMark and is not
the right closure for that gap.

## Related

- [`SKILL.md`](../../SKILL.md) — the skill whose description these
  cases exercise
- [`references/best-practices.md`](../../references/best-practices.md) — the
  `mdpp-version: 1.0` recommendation that closes G3 and reinforces G4
- [Top-level `CLAUDE.md`](../../../../../CLAUDE.md) — the "Working
  with Markdown++ files" section that closes G2 and reinforces G4
- [Routing-context principle learning](../../../../../docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md)
  — the institutional knowledge that explains why these closures are
  shaped this way
- GitHub issue [#85](https://github.com/quadralay/markdown-plus-plus/issues/85)
  — the issue that scoped this work
- GitHub issue [#84](https://github.com/quadralay/markdown-plus-plus/issues/84)
  — the predecessor that closed G1 via the description rewrite
