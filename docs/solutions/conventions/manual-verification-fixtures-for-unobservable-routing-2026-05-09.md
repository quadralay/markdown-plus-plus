---
title: Use manual-verification fixture suites to regression-check unobservable routing behavior
date: 2026-05-09
category: conventions
module: plugins/markdown-plus-plus/skills
problem_type: convention
component: tooling
severity: medium
applies_when:
  - A system property depends on the Claude Code routing layer or another runtime no in-repo harness can simulate
  - Regression coverage matters but no automated test can fail when the property regresses
  - Multiple gap patterns need to be tracked over time so future contributors can re-check them
  - Authoring or revising a Claude Code skill that relies on auto-activation from file content
  - A learning doc enumerates failure shapes that need future verification
tags:
  - manual-testing
  - regression-fixtures
  - skill-activation
  - claude-code-plugin
  - testing-methodology
  - markdown-plus-plus
---

# Use manual-verification fixture suites to regression-check unobservable routing behavior

## Context

Claude Code skill auto-activation is a routing-layer decision made by the
runtime, not by anything in the repository. There is no in-repo harness
that exercises the routing layer from a script, so a regression like
"the skill stopped auto-firing on derivative-file prompts" produces no
test failure. Discovery of the regression depends on a user happening to
hit the failing case and noticing the skill did not load.

Issue #85 enumerated five distinct gap patterns where the
Markdown++ skill might not auto-activate (derivative file creation,
vague prompts, buried directives, edit-without-prior-read, and non-`.md`
extensions). Each gap has a closure path (description completeness,
project-level CLAUDE.md guidance, or frontmatter sentinel — see
the [routing-context principle learning](skill-activation-description-completeness-2026-05-09.md)).
Without a documented way to re-check those gaps after future SKILL.md
edits, the closure paths would silently rot and the gap patterns would
have to be rediscovered from scratch each time someone reported the
symptom.

## Guidance

When a system property cannot be exercised by any automated test
available in the repo, build a **manual-verification fixture suite**
alongside the learning that documents the property. The suite has three
parts:

1. **Fixture files** — minimal real artifacts that exhibit the conditions
   under test. Each fixture isolates one gap pattern. Keep them small
   enough to read at a glance; larger fixtures invite drift between
   what the file *demonstrates* and what the case description *claims*
   it demonstrates.
2. **A `cases.md` checklist** — pairs each fixture with a verbatim
   prompt, an expected outcome, and the rationale for the case. The
   verbatim prompt matters: paraphrased prompts run the verifier in a
   subtly different context than the original failure. Use a fenced code
   block so future runners can copy-paste without ambiguity.
3. **A "What this is and is not" preamble** — states explicitly that
   the suite is manual, names the runtime that owns the behavior under
   test, and explains why no automation is possible. Without this, the
   next contributor will assume the suite is broken because nothing
   runs it on PR.

The `cases.md` file should also document **how to run a case**: open a
fresh session (so prior context cannot influence routing), paste the
prompt verbatim, observe the outcome, record the result. Specify any
context-dependent variants — e.g., for cases where project-level
`CLAUDE.md` is the closure path, run the case twice (with and without
the file loaded into routing context) so the contrast is visible.

For each case, also classify the **closure path** explicitly: which of
the available mitigations (description, frontmatter, CLAUDE.md, or
"out of scope") is supposed to catch the gap. This converts the suite
from a passive regression check into an active diagnostic — when a
case fails, the closure-path label tells the contributor where to look.

## Why This Matters

The cost of a manual suite is the wall-clock time to run it (minutes,
not hours). The cost of *not* having one when the property is
unobservable in CI is that every regression presents as a vague user
report ("the skill didn't fire"), and the diagnosis starts from zero
each time. The fixtures and cases freeze the gap patterns in a form
future contributors can re-execute without reconstructing them from
the original brainstorm.

This methodology compounds in a specific way: each new gap pattern
discovered in the field becomes one more fixture and one more case,
permanently. The suite grows monotonically with discovered failure
shapes; nothing requires it to be re-derived. Contrast this with
inline mentions in a learning doc, which are passive and tend to be
skipped during routine SKILL.md edits.

The methodology generalizes beyond skill auto-activation. Any system
property that depends on a runtime decision the repo cannot simulate
benefits from the same shape: paired fixture + verbatim prompt +
expected outcome + closure-path label. Examples include LLM
classification thresholds, model-driven feature flags, or any agent
behavior whose decision boundary is opaque from the repo's vantage.

## When to Apply

- Whenever a learning doc enumerates failure modes whose detection
  depends on a runtime the repo does not control.
- When closing a "skill didn't fire" report — pair the fix with a
  fixture and a case so the next regression is detectable.
- When introducing a closure path that depends on context being loaded
  into routing (a CLAUDE.md section, a sentinel frontmatter field) —
  the manual suite is the only way to verify the closure path
  actually closes the gap.
- Before committing to a SKILL.md description rewrite — re-running the
  existing cases against the proposed wording catches over-triggering
  and under-triggering before the change ships.

## Examples

The Markdown++ skill ships a manual-verification suite at
[`plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md).
It covers five gap patterns (G1-G5) with five fixture files and the
`cases.md` checklist.

A representative case:

```markdown
### G1 — Derivative file creation

**Prompt:**

    Create a 2.5 release notes file like fixture-derivative-source.md.

**Fixture:** fixture-derivative-source.md

**Expected behavior:** Skill auto-loads. The file the user names contains
multiple distinguishing signals (<!--style:-->, <!-- multiline -->,
mdpp-version:), and the SKILL.md description's derivative-file clause
covers the "create a file modeled after another" framing.

**Closure path:** (D) Out of scope — the description-level fix shipped
in #84 already covers this. Fixture is regression-only.
```

The four other cases follow the same shape, each isolating a single
gap pattern, each labelled with its closure path so a future failure
points the diagnosing contributor at the responsible mitigation.

The fixtures themselves are intentionally small (~10-30 lines) and
each contains exactly the signals or the absence-of-signals the case
under test relies on. The `.txt` fixture for G5 (non-`.md` extension)
is intentionally excluded from `validate-mdpp.py` runs because
validating it would defeat the purpose of the case.

## Related

- [`skill-activation-description-completeness-2026-05-09.md`](skill-activation-description-completeness-2026-05-09.md) — the routing-context principle this suite operationalizes
- [`plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`](../../../plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md) — the suite itself
- GitHub issue #85 — the gap-investigation issue that produced the suite
- GitHub issue #84 — the original failure case that prompted the description-completeness learning
- Plan: [`docs/plans/2026-05-09-003-docs-skill-auto-invocation-gaps-plan.md`](../../plans/2026-05-09-003-docs-skill-auto-invocation-gaps-plan.md)
