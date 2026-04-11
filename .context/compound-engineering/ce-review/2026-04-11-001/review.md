---
date: 2026-04-11
branch: claude/issue-70
base: main
run-id: 2026-04-11-001
verdict: ready-with-fixes
---

# CE Review — claude/issue-70

## Scope

- **Base:** `7541ca3` (main)
- **Branch:** `claude/issue-70`
- **Files changed:** 6
  - `.claude-plugin/marketplace.json` — version bump 1.1.11 → 1.1.12
  - `docs/brainstorms/2026-04-10-passthrough-marker-injection-requirements.md` — new
  - `docs/plans/2026-04-10-002-fix-passthrough-marker-injection-plan.md` — new
  - `plugins/markdown-plus-plus/.claude-plugin/plugin.json` — version bump 1.1.11 → 1.1.12
  - `spec/formal-grammar.md` — 4 locations updated
  - `spec/specification.md` — 2 locations updated (+ 2 review fixes)

## Intent

Fix a spec-vs-implementation divergence: replace "silently discarded, functioning as inline comments" language with correct "collected and injected as PassThrough markers" behavior across 6 normative locations in `spec/specification.md` and `spec/formal-grammar.md`.

## Review Team

- `correctness` (always)
- `testing` (always)
- `maintainability` (always)
- `agent-native-reviewer` (always)
- `learnings-researcher` (always)

No conditionals applied — pure documentation/spec change.

---

## Findings

### P1

| # | Title | File | Line | Reviewer | Confidence | Route | Status |
|---|-------|------|------|----------|------------|-------|--------|
| 1 | "invisible" contradicts Passthrough emit semantics | spec/specification.md | 1024 | correctness | 0.92 | gated_auto | **FIXED** |
| 2 | Stale "HTML comments are ignored" disambiguation | spec/specification.md | 771 | maintainability | 0.88 | gated_auto | **FIXED** |
| 3 | "PassThrough" vs "Passthrough" casing inconsistency | spec/specification.md | 762 | maintainability | 0.92 | manual | residual |
| 4 | PassThrough name ambiguous with marker:Passthrough | spec/specification.md | 1024 | correctness | 0.88 | manual | residual |
| 5 | No test exercises PassThrough marker injection | tests/sample-full.md | 254 | testing | 0.92 | manual | residual |

### P2

| # | Title | File | Line | Reviewer | Confidence | Route | Status |
|---|-------|------|------|----------|------------|-------|--------|
| 6 | syntax-reference.md uses old "silently ignored" language | references/syntax-reference.md | 145, 967 | testing + agent-native | 0.97 | manual | residual |
| 7 | No rule for standalone all-unrecognized comment edge case | spec/specification.md | 204 | correctness | 0.80 | manual | residual |
| 8 | examples/combined-commands.md has no unrecognized-segment example | examples/combined-commands.md | 1 | testing | 0.80 | manual | residual |
| 9 | No glossary entry for PassThrough marker injection concept | spec/specification.md | 118 | maintainability | 0.80 | manual | residual |

### P3

| # | Title | File | Line | Reviewer | Confidence | Route | Status |
|---|-------|------|------|----------|------------|-------|--------|
| 10 | PEG comment overstates unrecognized_text scope | spec/formal-grammar.md | 415 | correctness | 0.75 | manual | residual |
| 11 | Injection behavior stated in full at 5 locations | spec/specification.md | 214 | maintainability | 0.72 | advisory | residual |

---

## Applied Fixes

### Fix 1: Remove "invisible" — spec/specification.md line 1024

**Before:**
> This provides an **invisible** means for authors to embed metadata (status notes, review flags, tracking info) in rendered output.

**After:**
> This allows authors to embed metadata (status notes, review flags, tracking info) that flows through the processing pipeline.

**Why:** "invisible" contradicts section 13.3 which states that a Passthrough marker value "is emitted as-is in the output." The new phrasing matches section 5.3 exactly, achieving internal consistency.

### Fix 2: Update disambiguation — spec/specification.md line 771

**Before:**
> The Passthrough marker is a recognized Markdown++ directive — it matches the `marker:Key="value"` pattern. It is distinct from the general behavior where unrecognized HTML comments are ignored.

**After:**
> The Passthrough marker is a recognized Markdown++ directive — it matches the `marker:Key="value"` pattern. It is distinct from the automatic PassThrough marker injection for unrecognized segments in combined commands (section 16.4), and from the general behavior where standalone unrecognized HTML comments are ignored (section 5.2).

**Why:** This PR's changes made the original "ignored" disambiguation stale. The updated sentence now accurately reflects the three-way distinction: explicit Passthrough directive, auto-injected markers from combined command segments (new behavior), and standalone ignored comments.

---

## Residual Actionable Work

### High Priority

1. **Resolve "PassThrough" vs "Passthrough" casing** — spec/specification.md, spec/formal-grammar.md
   - Section 13 uses "Passthrough" (one capital); sections 5.3 and 16.4 use "PassThrough" (two capitals).
   - Decision needed: are these the same concept (same key `Passthrough`) or distinct? If the same, normalize casing. If distinct, add explicit disambiguation.

2. **Update syntax-reference.md** — `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
   - Line 145: "silently ignored as inline comments" → update to PassThrough marker injection language
   - Lines 967–976: conformance language still says "MUST silently ignore" and "function as inline comments"
   - Lines 983–986: prose and code comment frame segments as "inline comments"
   - This file is the primary agent-facing reference; stale language here means agents give authors incorrect guidance.

3. **Add PassThrough injection test to sample-full.md** — `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-full.md`
   - The formal grammar cites sample-full.md as the validation corpus but no combined command specimen includes an unrecognized segment.

### Medium Priority

4. **Clarify standalone all-unrecognized comment edge case** — spec/specification.md sections 5.2 and 16.4
   - A comment like `<!-- TODO: fix ; revisit later -->` has no recognized commands but semicolons make it parse as a command_list with two unrecognized segments. Section 5.2 says ignore it; section 16.4 says inject them. Needs an explicit resolution rule.

5. **Add example to examples/combined-commands.md**
   - No specimen shows a combined command with an unrecognized segment and the resulting PassThrough behavior.

6. **Add glossary entry for PassThrough marker injection** — spec/specification.md section 3
   - The term appears normatively in 5 locations but has no glossary anchor.

---

## Advisory

- The injection behavior description is duplicated in full at 5 locations without cross-referencing. Designating section 16.4 as canonical and shortening the others to forward references would reduce future drift risk.
- The formal-grammar.md Validation Notes claim all grammar constructs are "validated against the existing test corpus" (line 525), but the PassThrough injection edge case has no test corpus entry. This claim is now slightly misleading.

---

## Learnings / Past Solutions

- **combined-commands-conformance-classification-2026-04-10.md** — Documents the cross-file sweep pattern and warns that incomplete sweeps are a recurring failure mode. This PR's 6-location sweep is consistent with that pattern.
- **formal-ebnf-peg-grammar-for-extensions-2026-04-08.md** — Confirms the `unrecognized_text` production was always intended to capture (not discard) unrecognized segments.

---

## Coverage

- **Suppressed findings:** 0 (all fell above 0.60 confidence threshold)
- **Pre-existing findings:** 0
- **Reviewers failed/timed out:** 0

## Verdict: Ready with Fixes

The 6 targeted spec locations are correct. Two additional issues introduced by the PR's new text were identified and fixed (P1 findings 1 and 2). Residual P1 items (casing inconsistency, PassThrough naming, test gap, syntax-reference.md) should be addressed in follow-on work, with syntax-reference.md being the most urgent given it is the primary agent-facing reference.
