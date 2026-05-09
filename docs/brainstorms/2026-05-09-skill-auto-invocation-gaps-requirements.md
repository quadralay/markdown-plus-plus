---
date: 2026-05-09
topic: skill-auto-invocation-gaps
status: active
---

# Close Remaining Gaps in markdown-plus-plus Skill Auto-Invocation

## Problem Frame

GitHub issue #84 rewrote the `description:` frontmatter in `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` to enumerate every distinguishing Markdown++ signal exhaustively, cover whitespace-irrelevance, and add a derivative-file clause. That change closed the directly-observed failure case.

A separate class of failures remains because skill auto-activation depends on signals being **visible to the routing layer at the time it decides**. When the user's prompt is generic, when the model has not yet read the file, or when the file's distinguishing signals live deep inside a long document, the routing layer has nothing to match on — the description can be perfect and still not fire.

The issue lists five candidate gap patterns:

1. **G1. Derivative-file creation** — "Create a file like this one" plus a Markdown++ template. The new file has no signals yet; the source file does.
2. **G2. Vague task descriptions** — "Update the docs" with no Markdown++ mention and no file attached.
3. **G3. Signal buried in file body** — "Add a row to this table" where the file uses `<!-- multiline -->` somewhere mid-document and the prompt names neither the directive nor a path.
4. **G4. Edit-without-read flows** — the model attempts an edit before any Read surfaces the file's contents to the routing context.
5. **G5. Non-`.md` extensions** — files with no extension or `.markdown`, `.mdown`, `.txt` that contain Markdown++ syntax.

Of these, G1 was already addressed in #84 by the "Also use when creating a `.md` file modeled after another file containing any of these signals" clause. The remaining four need a closure decision and a regression fixture.

## Requirements

- **R1.** Demonstrate each of G1-G5 with a concrete (prompt, file fixture) pair. The pair must be reproducible: the fixture is a real file checked into the repo, and the prompt is the verbatim user input.
- **R2.** Choose exactly one closure path per gap from these three options:
  - (A) Tighter description wording in `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`.
  - (B) In-repo conventions — top-of-file sentinel, filename pattern, or recommended frontmatter that surfaces a signal even on a partial read.
  - (C) Project-level guidance in `CLAUDE.md` files (this repo and recommended language for downstream consumers).
  - (D) Document as out-of-scope with explicit rationale (allowed when extending coverage would over-trigger or solve a non-problem).
- **R3.** Check the (prompt, fixture) pairs into the repo as a regression suite. The suite must be discoverable by future SKILL.md authors: a top-level `cases.md` index plus the fixture files, located under `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/`.
- **R4.** Document the manual-verification protocol for the suite. State explicitly that activation cannot be tested in CI — it is a model-routing decision — so the suite is a **human checklist** future revisions of SKILL.md must run through before merging.
- **R5.** Apply the chosen closure paths. If the closure path for any gap is (A), bump the plugin version per `CLAUDE.md` § Version Management; if all closures are (C) or (D) only, no version bump is needed (the skill ship surface is unchanged).
- **R6.** Update `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md` (or write a sibling learning) to capture the routing-context principle behind G3/G4: signals must surface to the routing layer, and frontmatter sentinels are the most reliable single mitigation because they sit in the first few lines of every file.

## Success Criteria

- Each of G1-G5 has a checked-in fixture and a documented expected outcome.
- A reader of `tests/auto-activation/cases.md` can reproduce every case manually in a fresh Claude Code session and verify whether the skill auto-loads.
- The closure paths are written down such that a future contributor revising the skill description (or the project CLAUDE.md, or the recommended frontmatter) can re-run the suite and notice regressions before merging.
- The repo's stance on G5 (non-`.md` extensions) is explicit: Markdown++ is a `.md`-only format and the skill should not auto-fire on other extensions because that would over-trigger on plain CommonMark.

## Scope Boundaries

**In scope:**
- New directory `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/` with fixtures and a `cases.md` index.
- Edit to top-level `CLAUDE.md` adding a "Working with Markdown++ files" note that captures the read-before-edit and skill-load expectation for any `.md` work in this repo.
- A short addition to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` recommending `mdpp-version: 1.0` in YAML frontmatter as a strongly preferred convention for any file using Markdown++ extensions, justified by routing-layer surfacing.
- A new or extended learning doc under `docs/solutions/conventions/` capturing the routing-context principle.

**Out of scope:**
- Any rewrite of the SKILL.md `description:` frontmatter — #84 already shipped the canonical activation surface, and the remaining gaps are not closable by adding more signal names.
- Plugin version bump — none of the chosen closure paths modify the shipped skill description.
- The `webworks-claude-skills:markdown-plus-plus` sibling skill in the WebWorks plugin repo. Coordination is a follow-up.
- Any change to `validate-mdpp.py` or `add-aliases.py`. The auto-activation problem is not a validation problem.
- Automated activation testing in CI. There is no model-routing simulator available in-repo.
- Coverage of editor-tool integrations (e.g., direct `Edit` invocations from sub-agents that bypass `Read`). The mitigation for that path is the same as G4: project-level CLAUDE.md guidance and frontmatter sentinels.

### Deferred to Follow-Up Work

- Coordinating with the `webworks-claude-skills` repo to align its `markdown-plus-plus` skill description with this one. Out of scope here because that repo manages its own release cadence.
- A `mdpp-version` lint rule in `validate-mdpp.py` that warns when a file uses Markdown++ extensions without declaring the frontmatter sentinel. Useful, but a separate workstream from the auto-activation gap closure.

## Key Decisions

- **G1 closure: (D) Out of scope here, verified by fixture only.** Issue #84 already shipped the derivative-file clause. We add a fixture pair (`fixture-derivative-source.md` plus the prompt "Create a file like this one") to the regression suite so future description revisions don't silently regress this case.

- **G2 closure: (C) Project-level CLAUDE.md guidance.** "Update the docs" with no file attachment cannot be matched by skill-description signals — the signals don't exist in the prompt. The right place to close this is the consuming repo's `CLAUDE.md`. We add a short paragraph to this repo's top-level `CLAUDE.md` and mirror the recommendation in `references/best-practices.md` as suggested language for downstream repositories that author Markdown++ documentation.

- **G3 closure: (B) Frontmatter sentinel convention.** When the user prompts "Add a row to this table" and the file uses `<!-- multiline -->`, the routing layer's behavior depends on whether the directive surfaces in the read window. Promote `mdpp-version: 1.0` from SHOULD to **strongly recommended** for any file using Markdown++ extensions. The frontmatter sentinel sits in the first 3-5 lines of the file and is therefore present in any reasonable Read excerpt, including partial reads. Update `references/best-practices.md` accordingly.

- **G4 closure: (B) + (C) combined.** Edit-without-read is a workflow problem, not a description problem. The two reinforcing mitigations are (1) the same `mdpp-version:` sentinel from G3 (so even a glance at the file surfaces the signal) and (2) a top-level CLAUDE.md note that says: when modifying any `.md` file in this repo, Read it first. Both apply.

- **G5 closure: (D) Out of scope, document the position.** Markdown++ is a `.md`-only format. Listing additional extensions in the skill description (or in CLAUDE.md) would over-trigger on plain text and CommonMark documents that happen to use the same extension. Users authoring Markdown++ in non-standard extensions can manually invoke the skill. Document this stance in the regression suite's `cases.md` so the position is explicit and future contributors know not to "fix" it.

- **Test harness shape: human checklist, not automated test.** Auto-activation is a model-routing decision; no in-repo facility can simulate the routing layer. The harness is therefore a structured manual checklist — fixture files, verbatim prompts, expected outcomes. The discipline this enforces is that future SKILL.md description changes are accompanied by a manual run-through, with results recorded in the PR.

- **No version bump.** None of the chosen closure paths modify the shipped skill description. The closures land in CLAUDE.md, references/best-practices.md, the test fixtures, and a learning doc. The plugin's published surface is unchanged. Per `CLAUDE.md` § Version Management, version bumps cover changes that ship through `plugin.json` / `marketplace.json`; documentation that does not affect the skill description does not need a bump.

## Assumptions

These were inferred without user confirmation in autonomous mode and should be validated during planning or review:

- **The "test harness" the issue calls for is a manual checklist, not automated CI.** Auto-activation is a routing-layer decision at the model level with no testable surface inside this repo. If the issue author expected an automated harness, the closest substitute is what we ship; an automated harness would require a model-routing simulator that does not exist.
- **G1 needs a fixture for regression even though #84 already addressed it.** The acceptance criteria say "test fixtures checked into the repo so future SKILL.md changes can be regression-tested." That phrasing implies all five gaps get fixtures, including the already-closed one.
- **`mdpp-version:` is the right sentinel.** It is already documented as recommended frontmatter in SKILL.md's success criteria. Promoting it to strongly recommended (in best-practices.md and CLAUDE.md) is a low-cost change. Alternative sentinels (a top-of-file `<!-- markdown-plus-plus -->` HTML comment or a filename suffix like `.mdpp.md`) were considered and rejected: the HTML comment duplicates an existing convention without leveraging it, and a filename suffix would fragment the format from CommonMark backward compatibility.
- **Downstream-repo guidance lives in best-practices, not the skill description.** Per the convention captured in `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md`, the skill description is a routing contract and should not grow non-signal prose. Recommendations for downstream consumers belong in `references/best-practices.md`, where authors look for guidance.
- **The fixture directory belongs under `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/`, not the repo's top-level `examples/` or `tests/`.** It is skill-specific tooling and lives next to the existing skill `tests/` directory. The existing `tests/sample-*.md` fixtures support `validate-mdpp.py`; the new `auto-activation/` subdirectory is a sibling concern with its own `cases.md` index so the two purposes are not confused.
- **No version bump is correct.** The patch-bump convention applies to changes that ship through `plugin.json` / `marketplace.json`. Test fixtures, the project CLAUDE.md, and reference content do not change the published skill surface. If a reviewer disagrees, the conservative move is a `patch` bump for visibility; the cost is a few lines of churn in two manifests.

## Test Harness Shape

The regression suite under `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/` contains:

- `cases.md` — index document with one section per case. Each case names: gap ID, prompt (verbatim), fixture path, expected behavior (skill should auto-load / skill should not auto-load), rationale, and a results placeholder for manual runs.
- `fixture-derivative-source.md` — a Markdown++ source for the "Create a file like this one" derivative case (G1).
- `fixture-multiline-table-buried.md` — a long-ish file with the `<!-- multiline -->` directive partway through, used for G3.
- `fixture-edit-without-read.md` — a Markdown++ file used to demonstrate G4. The test prompt asks the agent to make an edit without first reading; the fixture's frontmatter declares `mdpp-version: 1.0` to validate the sentinel mitigation.
- `fixture-no-md-extension.txt` — a file containing Markdown++ syntax in a non-`.md` extension, used for G5 to document the skill should *not* auto-load.

Each fixture begins with the standard YAML frontmatter (`date`, `status`) per the repo's document-frontmatter convention, plus `mdpp-version: 1.0` where the case requires it. The fixtures double as documentation: a future reader can open one, see what the routing layer should match against, and reason about it.

## Verification Strategy

This work has no runtime behavior to test in CI. Verification is structural and procedural:

1. **Structural:** `git diff` shows the new fixtures, the `cases.md` index, the CLAUDE.md addition, the best-practices addition, and a learning-doc update or sibling. No edits to SKILL.md, no version bumps, no script changes.
2. **Procedural:** The PR description includes results from a manual run-through of `cases.md` in a fresh Claude Code session, recording for each case whether the skill auto-activated. The expected results (per the closure decisions) are: G1 activates, G2 activates only with the CLAUDE.md guidance loaded, G3 activates when the fixture frontmatter includes `mdpp-version:`, G4 activates because the read brings the sentinel into context, G5 does not activate.
3. **Regression:** Future SKILL.md description revisions re-run the same checklist. A revision that breaks any expected outcome must explain the regression in its PR.

## Risks

- **Manual checklist drift.** A human checklist is only useful if humans run it. Mitigation: link it from `references/best-practices.md` and the SKILL.md description-completeness convention so authors revising the description encounter the checklist as part of their flow.
- **Sentinel promotion is non-binding.** Recommending `mdpp-version: 1.0` strongly does not force adoption. Existing files without the sentinel remain at risk. Mitigation: a separate follow-up could add a `validate-mdpp.py` warning when extensions appear without the frontmatter declaration; out of scope here.
- **Routing-layer behavior may change.** The five gaps are framed against the current routing layer. A future routing layer may close some of them automatically (or open new ones). The fixtures remain useful as a regression baseline, but the closure decisions may need revisiting.

## References

- Origin issue: GitHub #85
- Predecessor issue: GitHub #84 (description rewrite, merged in `1d921c0`)
- Existing learning: `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md`
- Predecessor plan: `docs/plans/2026-05-09-002-docs-skill-description-trigger-signals-plan.md`
- Skill file: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
- Existing fixture conventions: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-*.md`
- Repo convention for examples vs scenarios vs best-practices: `CLAUDE.md` § Example locations
- Version management policy: `CLAUDE.md` § Version Management

## Next Steps

→ Proceed to `/ce-plan` to break the closure work into implementation units (fixtures + `cases.md`, CLAUDE.md edit, best-practices addition, learning-doc update). Scope is bounded; assumptions are recorded for plan-time review.
