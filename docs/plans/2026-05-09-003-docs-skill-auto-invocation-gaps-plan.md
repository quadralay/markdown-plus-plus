---
date: 2026-05-09
status: active
type: docs
plan_id: 2026-05-09-003
origin: docs/brainstorms/2026-05-09-skill-auto-invocation-gaps-requirements.md
issue: 85
---

# docs: Close Skill Auto-Invocation Gaps with a Manual-Verification Suite

## Summary

Close the four remaining auto-activation gaps (G2-G5) left after issue #84's `description:` rewrite by:

1. Checking in a regression suite of `(prompt, fixture)` pairs for G1-G5 under `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/`, indexed by a `cases.md` checklist.
2. Adding "Working with Markdown++ files" guidance to the top-level `CLAUDE.md` (closes G2 and reinforces G4).
3. Promoting `mdpp-version: 1.0` from SHOULD to strongly recommended in `references/best-practices.md` (closes G3 and reinforces G4).
4. Extending the existing convention learning to capture the routing-context principle (R6).

No edit to `SKILL.md`. No plugin version bump (the published skill surface is unchanged).

---

## Problem Frame

Issue #84 closed the directly-observed activation failure by rewriting the SKILL.md `description:` to enumerate every distinguishing Markdown++ signal. That fixed cases where the routing layer can see the signal in either the prompt or the file. A separate class of failures remains: when no signal is in the prompt and the file's signal is buried, missing, or in a non-`.md` extension, the routing layer has nothing to match on regardless of how good the description is.

The brainstorm enumerates five gap patterns (G1-G5). G1 was already addressed by #84's "derivative file" clause; the remaining four need a closure decision and a regression fixture. See origin: `docs/brainstorms/2026-05-09-skill-auto-invocation-gaps-requirements.md`.

---

## Requirements & Traceability

| ID | Requirement | Implementation Units |
|----|-------------|----------------------|
| R1 | Demonstrate G1-G5 with `(prompt, fixture)` pairs | U1, U2 |
| R2 | Choose one closure path per gap | Decisions section (carried from origin) |
| R3 | Suite checked into `plugins/.../tests/auto-activation/` with a `cases.md` index | U1, U2 |
| R4 | Document the manual-verification protocol explicitly | U2 |
| R5 | Apply the chosen closure paths; no version bump if all closures are (B)/(C)/(D) | U3, U4 (no bump per origin) |
| R6 | Update or add a sibling learning capturing the routing-context principle | U5 |

---

## Scope Boundaries

### In scope
- New directory `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/` with five fixture files and a `cases.md` index.
- Edit to top-level `CLAUDE.md` adding a "Working with Markdown++ files" section.
- Addition to `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md` promoting `mdpp-version: 1.0` from SHOULD to strongly recommended for any file using Markdown++ extensions.
- Extension of `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md` (or a sibling) capturing the routing-context principle.

### Out of scope
- Any rewrite of the SKILL.md `description:` frontmatter. #84 already shipped the canonical activation surface; remaining gaps are not closable by adding more signal names.
- Plugin version bump. None of the chosen closure paths modify the shipped skill description.
- The `webworks-claude-skills:markdown-plus-plus` sibling skill. Coordination is a follow-up.
- Any change to `validate-mdpp.py` or `add-aliases.py`. Auto-activation is not a validation problem.
- Automated activation testing in CI. There is no model-routing simulator available in-repo.

### Deferred to Follow-Up Work
- Coordinating with `webworks-claude-skills` repo to align its `markdown-plus-plus` skill description.
- A `validate-mdpp.py` warning when a file uses Markdown++ extensions without declaring `mdpp-version:` frontmatter.

---

## Output Structure

```
plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/
├── cases.md                              # G1-G5 case index + manual-verification protocol
├── fixture-derivative-source.md          # G1: source for "create a file like this one"
├── fixture-multiline-table-buried.md     # G3: <!-- multiline --> directive buried mid-file
├── fixture-edit-without-read.md          # G4: file with mdpp-version sentinel in frontmatter
├── fixture-no-md-extension.txt           # G5: Markdown++ syntax in non-.md extension
└── fixture-vague-prompt-target.md        # G2: a target for "update the docs" with no path
```

The `auto-activation/` directory is a sibling of the existing `tests/sample-*.md` fixtures (which feed `validate-mdpp.py`). They serve different purposes and should not be confused — `cases.md` makes that explicit.

---

## Key Technical Decisions

These are carried verbatim from the origin brainstorm's Key Decisions section. See origin: `docs/brainstorms/2026-05-09-skill-auto-invocation-gaps-requirements.md`.

- **G1 closure: (D) Out of scope, fixture-only.** #84 shipped the derivative-file clause. We add the fixture pair so future description revisions cannot silently regress this case.
- **G2 closure: (C) Project-level CLAUDE.md guidance.** "Update the docs" with no file attachment cannot be matched by description signals — they don't exist in the prompt. Closure lives in the consuming repo's `CLAUDE.md`. Mirror as suggested language in `references/best-practices.md` for downstream repositories.
- **G3 closure: (B) Frontmatter sentinel convention.** Promote `mdpp-version: 1.0` from SHOULD to **strongly recommended**. The sentinel sits in the first 3-5 lines of the file and surfaces in any reasonable Read excerpt, including partial reads.
- **G4 closure: (B) + (C) combined.** Both reinforcing mitigations apply: the `mdpp-version:` sentinel from G3, plus a top-level CLAUDE.md note that says "when modifying any `.md` file in this repo, Read it first."
- **G5 closure: (D) Out of scope, document the position.** Markdown++ is a `.md`-only format. Listing additional extensions would over-trigger on plain CommonMark.
- **Test harness shape: human checklist, not automated test.** Auto-activation is a model-routing decision; no in-repo facility can simulate it. The harness is a structured manual checklist.
- **No version bump.** Closures land in CLAUDE.md, references/best-practices.md, test fixtures, and a learning doc. The plugin's published surface is unchanged.

---

## Implementation Units

### U1. Create G1-G5 fixture files

**Goal:** Land five reproducible fixture files that demonstrate each gap pattern. Each fixture is a real file authored to be the input side of a `(prompt, fixture)` pair.

**Requirements:** R1, R3.

**Dependencies:** None.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/fixture-derivative-source.md` (G1)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/fixture-vague-prompt-target.md` (G2)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/fixture-multiline-table-buried.md` (G3)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/fixture-edit-without-read.md` (G4)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/fixture-no-md-extension.txt` (G5)

**Approach:**

Each `.md` fixture begins with the standard YAML frontmatter (`date: 2026-05-09`, `status: active`) per the repo's document-frontmatter convention. Add `mdpp-version: 1.0` only where the case requires it (G4 explicitly demonstrates the sentinel mitigation; G3 deliberately omits it so the contrast is visible against G4).

Per-fixture content sketches:

- **fixture-derivative-source.md (G1)**: A short release-notes-style document modeled on the failure case from #84. Uses `<!-- multiline -->` above a table plus a `<!--style:NoteBox-->`-annotated callout. Frontmatter declares `mdpp-version: 1.0`. Purpose: a future regression check that "create a file like this one" still triggers auto-activation now that #84 added the derivative-file clause.
- **fixture-vague-prompt-target.md (G2)**: A short Markdown++ doc with at least two distinguishing signals (e.g., one `$variable;` and one `<!--condition:-->` block). Frontmatter declares `mdpp-version: 1.0`. Purpose: the *target* of a "update the docs" prompt that does not attach the path. The expected outcome is that the skill does not auto-fire on the prompt alone — only the CLAUDE.md guidance closes the gap.
- **fixture-multiline-table-buried.md (G3)**: A longer document (50-80 lines) where the `<!-- multiline -->` directive sits past line 30, after a long preamble of plain CommonMark. Frontmatter intentionally omits `mdpp-version:` to demonstrate the failure mode the sentinel mitigates.
- **fixture-edit-without-read.md (G4)**: A file analogous in shape to G3 (long preamble, `<!-- multiline -->` mid-document), but with `mdpp-version: 1.0` in frontmatter. Purpose: demonstrate that the sentinel surfaces the signal even on partial reads, and reinforce the "Read before edit" expectation that closes the rest of the gap via CLAUDE.md.
- **fixture-no-md-extension.txt (G5)**: Plain text containing `<!--style:NoteBox-->`, `$variable;`, and a `<!--multiline-->` table. No frontmatter (the `.txt` extension is the point). Purpose: document the explicit position that the skill should *not* auto-fire on non-`.md` extensions.

**Patterns to follow:**
- Existing fixture conventions: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-*.md`. Match their tone (concise, comment-annotated where helpful).
- Repo document-frontmatter convention: `CLAUDE.md` § Conventions / Document frontmatter.

**Test scenarios:** Test expectation: none -- these *are* test fixtures, not behavior-bearing code. Verification is procedural (see Verification Strategy).

**Verification:** All five files exist at the listed paths, each `.md` fixture has valid YAML frontmatter, each fixture contains the specific signal pattern its gap targets, and `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` runs cleanly on the four `.md` fixtures (the `.txt` fixture is exempt).

---

### U2. Write `cases.md` index with manual-verification protocol

**Goal:** A discoverable index that names each case, gives the verbatim prompt, points to the fixture, states the expected outcome, explains the rationale, and reserves a placeholder for manual-run results.

**Requirements:** R1, R3, R4.

**Dependencies:** U1.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/auto-activation/cases.md`

**Approach:**

Standard frontmatter (`date: 2026-05-09`, `status: active`) plus a short header explaining what the directory is, what it is *not* (i.e., not a CI test suite), and how to run the suite manually.

Document structure:

1. **Overview** — what the suite is for, why it is a manual checklist (the routing-context principle: skills auto-activate based on signals visible to the routing layer at decision time; no in-repo facility simulates that).
2. **How to run a case** — the procedural steps: open a fresh Claude Code session in this repo, paste the verbatim prompt with the fixture as attached context (or the named path), and observe whether the skill auto-loads. Record results in the per-case results placeholder for the PR description.
3. **Cases** — one section per gap with the following fields:
   - **Gap ID** (G1-G5)
   - **Prompt** (verbatim, in a fenced code block)
   - **Fixture** (relative path)
   - **Expected behavior** (skill should auto-load / skill should not auto-load)
   - **Rationale** (one paragraph explaining what the case demonstrates and which closure path applies)
   - **Results** (a placeholder table or list for the PR author to fill in)
4. **Regression discipline** — a closing section stating that future SKILL.md description revisions must run through this checklist and record results in the PR.

The `cases.md` doc must explicitly state the G5 stance: the skill should *not* auto-fire on non-`.md` extensions, by design. This forecloses well-meaning future PRs that try to "fix" G5 by extending the description.

**Patterns to follow:**
- Existing conventions for index documents in `docs/solutions/`: lead with frontmatter, plain headings, no bespoke schemas.
- Origin brainstorm's "Test Harness Shape" and "Verification Strategy" sections — translate into a runnable checklist rather than copying prose.

**Test scenarios:** Test expectation: none -- this is documentation that records test inputs and procedure, not behavior-bearing code.

**Verification:** A reader can open `cases.md`, identify each case's prompt + fixture + expected outcome without consulting the brainstorm, and run the checklist in a fresh session. The G5 case explicitly notes that the documented expectation is "skill should not auto-load."

---

### U3. Add "Working with Markdown++ files" guidance to top-level `CLAUDE.md`

**Goal:** Close G2 (vague prompts with no Markdown++ mention) and reinforce G4 (edit-without-read flows) with a short, prescriptive section in the consuming repo's `CLAUDE.md`.

**Requirements:** R2 (G2 closure), R2 (G4 closure, in tandem with U4), R5.

**Dependencies:** None.

**Files:**
- `CLAUDE.md` (top-level)

**Approach:**

Add a new section, ideally between `## Conventions` and `## Git workflow`, titled `## Working with Markdown++ files`. The section establishes two expectations and one hint:

1. **Read before edit.** Any agent working on a `.md` file in this repo should `Read` the file before editing it. This brings the file's frontmatter and Markdown++ signals into routing context and lets the skill auto-activate.
2. **Load the skill explicitly when the prompt is generic.** Prompts like "update the docs" do not carry the file-content signals the routing layer keys on. When working on Markdown++ files in this repo, invoke `/markdown-plus-plus:markdown-plus-plus` (or load the skill through whatever routing surface is available) before editing.
3. **Suggested language for downstream consumers.** A short note that downstream repositories using Markdown++ are encouraged to copy this guidance into their own `CLAUDE.md` so the same routing-context discipline applies wherever Markdown++ is authored.

The wording must not promise behavior the routing layer cannot guarantee — frame the guidance as expectation-setting for human authors and AI agents, not as a runtime contract.

**Patterns to follow:**
- Existing `CLAUDE.md` § Version Management — the prescriptive, numbered-step style is the right shape.
- The "AUTHORITATIVE REFERENCE" framing in SKILL.md — keep authoritative claims confined to the skill itself; CLAUDE.md is workflow guidance.

**Test scenarios:** Test expectation: none -- this is project guidance, not behavior-bearing code.

**Verification:** The section exists, is discoverable from the table of contents, and the language matches the closure paths in the brainstorm. Manual run of the G2 case in `cases.md` (with this CLAUDE.md loaded as user context) produces the expected outcome (skill auto-activates given the CLAUDE.md guidance).

---

### U4. Promote `mdpp-version: 1.0` to strongly recommended in `references/best-practices.md`

**Goal:** Close G3 (signal buried in file body) and reinforce G4 (edit-without-read) by elevating the existing `mdpp-version: 1.0` recommendation. This produces a sentinel that surfaces in the first 3-5 lines of every Markdown++ file regardless of where the directive-bearing content sits.

**Requirements:** R2 (G3 closure), R2 (G4 closure), R5.

**Dependencies:** None.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`

**Approach:**

Add a new top-of-file subsection titled `## Declare the format version in frontmatter`, placed near the top of `best-practices.md` so it is visible to anyone scanning for conventions. The subsection establishes:

1. **The recommendation:** every file using Markdown++ extensions SHOULD declare `mdpp-version: 1.0` in YAML frontmatter, and this is **strongly recommended** rather than optional.
2. **The reason:** a routing-context rationale — frontmatter sits in the first lines of the file, surfaces on partial reads, and lets the skill (and the routing layer) recognize Markdown++ documents even when the distinguishing directives appear later in the file.
3. **The relationship to the SKILL.md success criterion:** SKILL.md already lists `mdpp-version: 1.0` under success criteria; this subsection promotes it from "SHOULD" to "strongly recommended" without contradicting the skill body.
4. **Mirror language for downstream consumers:** a short sentence noting that downstream repositories using Markdown++ should adopt the same recommendation.

Cross-link to the existing format versioning spec (`spec/versioning.md`) and to SKILL.md's success criteria to keep the convention discoverable from both directions.

**Patterns to follow:**
- The existing "When to Use Each Extension" structure in `best-practices.md` — concise rule statement, brief rationale, do/don't snippet.
- The skill's success-criteria framing in SKILL.md — language that says "SHOULD declare `mdpp-version: 1.0`" should be elevated to "strongly recommended" without losing semantic compatibility.

**Test scenarios:** Test expectation: none -- this is prescriptive style guidance.

**Verification:** The new subsection is present, the recommendation is "strongly recommended" (not "MUST"), and the rationale explicitly names the routing-context reason. Manual run of the G3 case in `cases.md` against `fixture-multiline-table-buried.md` (no sentinel) and `fixture-edit-without-read.md` (sentinel present) produces visibly different routing outcomes — the sentinel-bearing fixture surfaces the Markdown++ signal even on a partial read.

---

### U5. Extend convention learning doc with the routing-context principle

**Goal:** Capture the principle behind G3/G4 closures so future skill-description authors understand why the frontmatter sentinel and read-before-edit guidance exist. This is the institutional-knowledge artifact the brainstorm names in R6.

**Requirements:** R6.

**Dependencies:** Best landed last so the doc can reference the actual files U1-U4 added.

**Files:**
- `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md` (extend in place)

**Approach:**

The existing learning is scoped to "author skill descriptions to enumerate every distinguishing signal." Extend it with a new section titled something like `## When the description is not enough: the routing-context principle`, framed as a follow-up to the original lesson. The new section establishes:

1. **The principle:** skill auto-activation depends on signals being *visible to the routing layer at the time it decides*. A perfect description still fails when the signal is in the prompt only as a generic phrase ("update the docs"), buried deep in the file body, or absent because no `Read` has happened yet.
2. **The three orthogonal mitigations** that fall out of this:
   - Project-level guidance (CLAUDE.md) for prompts the description cannot match.
   - Frontmatter sentinels for files where the directives sit deep in the body.
   - Read-before-edit discipline for workflows that bypass file content surfacing.
3. **What is *not* a mitigation:** extending the description with non-signal text, or listing more file extensions. Both over-trigger.
4. **References:** link the new test fixture suite (`tests/auto-activation/cases.md`), the CLAUDE.md addition, the best-practices addition, and the origin issue (#85).

Whether this extends the existing 2026-05-09 doc in place or lands as a sibling (e.g., `routing-context-skill-activation-2026-05-09.md`) is an implementation-time judgment call. **Decision:** extend in place. The original doc is dated 2026-05-09 and the new principle is a direct follow-up to the same investigation; splitting would obscure that arc. The added section is ~30-50 lines and the original doc is small.

**Patterns to follow:**
- Existing structure of `skill-activation-description-completeness-2026-05-09.md`: Context, Guidance, Why This Matters, When to Apply, Examples, Related.
- Mirror that structure for the new section so the doc reads as a coherent two-part learning.
- Frontmatter `applies_when:` list should be extended to include the new triggers (e.g., "diagnosing a 'skill didn't fire' report on a vague prompt").

**Test scenarios:** Test expectation: none -- this is institutional knowledge, not behavior-bearing code.

**Verification:** The new section exists within the same file, references the new fixture suite and CLAUDE.md/best-practices changes by repo-relative path, and a contributor revising SKILL.md who reads this doc would understand why CLAUDE.md guidance and frontmatter sentinels exist as complements (not alternatives) to a complete description.

---

## System-Wide Impact

| Surface | Affected? | Notes |
|---------|-----------|-------|
| `SKILL.md` | No | #84 already shipped the canonical activation surface. |
| `plugin.json` / `marketplace.json` (version) | No | Closures do not modify shipped skill description; per origin's "No version bump" decision. |
| `validate-mdpp.py` / `add-aliases.py` | No | Auto-activation is not a validation problem. |
| `CLAUDE.md` (top-level) | Yes | New "Working with Markdown++ files" section (U3). |
| `references/best-practices.md` | Yes | New "Declare the format version in frontmatter" subsection (U4). |
| `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md` | Yes | Extended with routing-context principle (U5). |
| `plugins/.../tests/auto-activation/` | Yes (new) | Five fixtures + `cases.md` (U1, U2). |
| `webworks-claude-skills:markdown-plus-plus` sibling | No (deferred) | Coordination is follow-up work, per origin Scope Boundaries. |
| Downstream consumer repos | Indirect | Best-practices.md and CLAUDE.md include suggested language to copy; no enforced contract. |

---

## Verification Strategy

This work has no runtime behavior to test in CI. Verification is structural and procedural, mirroring the origin's Verification Strategy:

1. **Structural** — `git diff` shows the new fixtures, the `cases.md` index, the `CLAUDE.md` addition, the `best-practices.md` addition, and the extension to the existing convention learning doc. No edits to `SKILL.md`. No version bumps.
2. **Procedural** — the PR description includes results from a manual run-through of `cases.md` in a fresh Claude Code session, recording for each case whether the skill auto-activated. The expected results per the closure decisions are:
   - **G1:** activates (#84's derivative-file clause already covers this).
   - **G2:** activates *only* when the CLAUDE.md guidance is loaded as user context.
   - **G3:** activates more reliably when the fixture's frontmatter declares `mdpp-version:` than when it does not. The two G3 fixtures (`fixture-multiline-table-buried.md` without sentinel, `fixture-edit-without-read.md` with sentinel) make the contrast visible.
   - **G4:** activates because the read brings the sentinel into context.
   - **G5:** does *not* activate. This is the documented intentional outcome.
3. **Regression** — future SKILL.md description revisions re-run the same checklist. Any revision that breaks an expected outcome must explain the regression in its PR.
4. **Validation** — the four `.md` fixtures pass `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`. The `.txt` fixture is exempt.

---

## Risks

- **Manual checklist drift.** A human checklist is only useful if humans run it. Mitigation: link `cases.md` from `references/best-practices.md` and from the convention learning doc so revisions to SKILL.md encounter the checklist as part of their flow.
- **Sentinel promotion is non-binding.** Recommending `mdpp-version: 1.0` strongly does not force adoption. Mitigation: a follow-up `validate-mdpp.py` warning when extensions appear without the frontmatter declaration is recorded in Deferred Follow-Up Work.
- **Routing-layer behavior may change.** The five gaps are framed against the current routing layer. A future routing-layer revision may close some gaps automatically or open new ones. The fixtures remain useful as a regression baseline; closure decisions may need revisiting.
- **G2 closure depends on the consuming repo loading our CLAUDE.md.** In contexts where CLAUDE.md is not auto-loaded (some headless / sub-agent flows), G2 may still fail. Mitigation: documented as a known limitation in `cases.md`. The frontmatter sentinel from G3 provides a partial backstop.
- **Misclassifying a fixture.** A future contributor could misread `fixture-no-md-extension.txt` as a bug rather than the documented G5 stance. Mitigation: `cases.md` states the position explicitly with the rationale.

---

## References

- Origin requirements: `docs/brainstorms/2026-05-09-skill-auto-invocation-gaps-requirements.md`
- Origin issue: GitHub #85
- Predecessor issue: GitHub #84
- Predecessor plan: `docs/plans/2026-05-09-002-docs-skill-description-trigger-signals-plan.md`
- Existing learning: `docs/solutions/conventions/skill-activation-description-completeness-2026-05-09.md`
- Skill file: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
- Existing fixture conventions: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-*.md`
- Repo conventions for docs: `CLAUDE.md` § Conventions, § Example locations, § Version Management
