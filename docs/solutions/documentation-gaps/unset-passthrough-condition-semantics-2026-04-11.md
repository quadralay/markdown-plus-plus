---
title: Unset Condition Pass-Through Documentation Gaps
date: 2026-04-11
category: docs/solutions/documentation-gaps/
module: conditions
problem_type: documentation_gap
component: documentation
symptoms:
  - Missing normative statement about Phase 2 treatment of condition/include tags from Unset blocks
  - Unset condition state not represented in Expression Examples table in agent-facing reference
  - Lack of compound expression examples mixing defined and Unset operands
  - Incomplete coverage of Unset interactions with variables, includes, and styles in SKILL.md and syntax-reference.md
  - Residual "Tri-State Model" terminology inconsistency with Unset semantics
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - unset-conditions
  - pass-through
  - conditions
  - specification
  - condition-states
  - phase-2
  - variable-substitution
  - tri-state
---

# Unset Condition Pass-Through Documentation Gaps

## Problem

After PR #78 (issue #72) established that Unset conditions (undefined variable names) cause pass-through behavior rather than truthiness-based evaluation, the documentation in `spec/`, `plugins/.../references/`, and the test suite still contained gaps and inconsistencies that made the specification unclear for both spec readers and AI agents using the documentation.

The fixes landed across 10 items (F1–F10) tracked in issue #79, plus review-phase corrections for residual gaps caught post-commit.

## Symptoms

- "Regular HTML comments" phrasing in spec/specification.md §11.4 did not explain how condition tags from Unset blocks interact with Phase 2 processing
- No normative MUST statement in spec/processing-model.md that Phase 2 ignores condition/include tags that passed through Phase 1 inside an Unset block
- "Tri-State Model" heading implied Unset was a peer state alongside Visible and Hidden, contradicting the definition that Unset = absence of assignment
- "Passes through as-is" language in processing-model.md was ambiguous — readers could not tell whether variable substitution still applied
- Expression Examples table in syntax-reference.md had six rows with zero Unset scenarios (agents had no quick reference)
- No worked example in spec for compound expressions with mixed Visible+Unset operands — the most counter-intuitive behavior
- No test specimen file exercising Unset pass-through (undefined names, compound expressions, variable inside Unset block)
- Conformance checklist in processing-model.md still used "Tri-state condition model" after heading was renamed

## What Didn't Work

Early formulations tried to describe pass-through using a **tri-state parity model**: treating Visible, Hidden, and Unset as three symmetrical states, each with equal agency. This made pass-through behavior appear arbitrary — it was unclear why a `web,mobile` expression where `web=Visible` and `mobile=Unset` would not be evaluated at all.

Documenting the behavior without first documenting the *model* left readers without a conceptual anchor. The initial "Tri-State Model" heading also gave reviewers no signal that the three states were not equal peers, so the inconsistency persisted through multiple rounds of spec work before issue #79 specifically targeted it.

## Solution

Fixes were applied in two commits (`04392c4` and `3404c85`).

### F1 — HTML comment phrasing clarified (spec/specification.md §11.4)

**Before:**
```
embedded extension directives within the block survive into Phase 2 as regular HTML comments
```

**After:**
```
embedded extension directives within the block survive into Phase 2 as HTML comments
that Phase 2 does not act on. (Phase 2 recognizes only `style:`, `#alias`, `marker:`,
`markers:`, `multiline`, and combined commands; condition and include tags from
pass-through blocks are treated as unrecognized HTML comments and ignored.)
```

### F2 — Normative Phase 2 statement added (spec/processing-model.md §Comment Disambiguation)

Added MUST-level normative paragraph:
```
A conformant processor MUST treat condition opening tags (<!--condition:expr-->),
condition closing tags (<!--/condition-->), and include directives (<!--include:path-->)
that passed through Phase 1 as part of an Unset condition block as unrecognized
HTML comments.
```

### F3 — Unset rows added to Expression Examples table (syntax-reference.md)

Three new rows added to the agent-facing quick-reference table:

| Expression | Result |
|------------|--------|
| `mobile` | Pass through — `mobile` is Unset |
| `web mobile` | Pass through — any Unset operand forces pass-through |
| `web,mobile` | Pass through — any Unset operand forces pass-through |

### F4 — Compound expression worked example (spec/specification.md + spec/processing-model.md)

Added "Compound Expression with Mixed Assigned/Unset Operands" showing `<!--condition:web mobile-->` where `web=Visible` but `mobile=Unset` — the entire block passes through with tags and content preserved. This is the most counter-intuitive scenario and needed a dedicated normative example.

### F5 — Test specimen created (plugins/.../tests/sample-unset-passthrough.md)

New 91-line file covering all major Unset scenarios:
- Simple Unset pass-through (undefined name)
- Variable substitution inside Unset block (substitution still applies)
- AND expression with one Unset operand → pass-through
- OR expression with one Unset operand → pass-through (counter-intuitive)
- AND with all operands Unset
- NOT with Unset operand → pass-through
- Include inside Unset block (not re-processed)

### F6 — Authoring guidance and worked scenario (best-practices.md + examples.md)

**best-practices.md** added "Undefined condition names (Unset)" section with four rules and do/don't snippets.

**examples.md** added Example 12 (Unset pass-through) demonstrating a multi-target source where `web`/`print` are defined and `mobile`/`tablet` are Unset.

### F7 — Worked examples expanded in specification.md §11.7

Section 11.7 grew from one combined block to four annotated examples:
1. Simple Visible condition (basic inclusion)
2. Complex expression (operator precedence)
3. Conditional include (Hidden removal)
4. Unset pass-through (simple Unset + compound Unset AND)

### F8 — Interaction subsection added (syntax-reference.md + SKILL.md)

**syntax-reference.md** gained "Interaction with Other Extensions for Unset Blocks" table:

| Feature | Behavior inside Unset block |
|---------|----------------------------|
| Variables | IS applied — Phase 1 Step 2 still resolves `$variable;` tokens |
| Includes | NOT processed — include directives pass through as unrecognized comments |
| Styles/Aliases/Markers | Survive as unrecognized HTML comments in Phase 2 output |
| Phase 2 condition tags | Not recognized as directives — treated as plain HTML comments |

**SKILL.md** renamed heading and added variable-substitution paragraph.

### F9 — Heading renamed from "Tri-State Model" (spec/ + SKILL.md)

**Before:** `#### Tri-State Model`

**After:**
```markdown
#### Condition State Model

Visible and Hidden are **assigned states** — explicitly set in the condition set
provided at build time. Unset is **not an assigned state**; it represents the
absence of a definition.
```

### F10 — "As-is" qualified in all Unset rows (spec/ + syntax-reference.md)

Every instance of "passes through as-is" in Unset row descriptions now carries:
```
As-is refers to condition evaluation only; variable substitution (Phase 1, Step 2)
still applies to the block's content.
```

### Review-phase fixes (commit 3404c85)

| Fix | Location | What was missed |
|-----|----------|----------------|
| Conformance checklist | spec/processing-model.md:556 | Still said "Tri-state condition model" after heading rename |
| Condition States table | syntax-reference.md:497 | Unset row missing as-is qualifier added to spec tables |
| Expression Examples table | syntax-reference.md:519 | `!mobile` (NOT with Unset) row absent |
| Test specimen | sample-unset-passthrough.md | OR with Visible+Unset operand (`web,mobile`) missing |

## Why This Works

The documentation was inconsistent because **two mental models** were competing without being named:

1. **Tri-state parity** (misleading): Visible, Hidden, and Unset are three symmetrical states. Makes pass-through seem arbitrary.
2. **Assignment model** (correct): Visible/Hidden are build-time assignments. Unset is the *absence* of an assignment. When the processor encounters an undefined name, there is nothing to evaluate against — pass-through is the only principled outcome.

The fixes shift all documentation toward the assignment model:

- Renaming "Tri-State Model" removes the false symmetry signal
- Adding "Visible and Hidden are **assigned states**; Unset is **not an assigned state**" makes the model explicit
- The compound-expression worked example cements the rule for the counter-intuitive case
- Qualifying "as-is" with "condition evaluation only" focuses the concept on *what is skipped* rather than *what nothing happens*
- Adding normative Phase 2 language closes the loop for processor implementers

## Prevention

1. **Document the model before the rules.** Before listing state behavior, write one sentence defining the conceptual model (e.g., "two assigned states plus an absence"). The Tri-State heading persisted for several PRs because nothing explicitly stated Unset was not a peer state.

2. **Create test specimens before finalizing spec language.** The absence of `sample-unset-passthrough.md` meant counter-intuitive cases (Visible+Unset AND, Visible+Unset OR) were never grounded in examples during early review. Creating specimen files for each major behavior branch first makes gaps visible.

3. **Require agent-facing references to cover all spec cases.** When a spec defines N major scenarios, agent quick-reference tables should have N rows. Use a review checklist: "spec has 4 condition state scenarios; does syntax-reference.md Expression Examples table have rows for all 4?"

4. **Qualify "as-is" immediately.** Whenever a spec says "X is preserved as-is," add parenthetical scope: "as-is = [aspect] only; [other processing] still applies." Implicit scope causes readers to over-generalize.

5. **Conformance checklists must be updated in the same PR as heading changes.** The residual "Tri-state condition model" in the conformance section slipped through because the checklist was maintained separately from the content it described. Co-locate or cross-reference.

6. **Validate terminology consistency across all 8 artifact types.** This gap existed in: spec/specification.md, spec/processing-model.md, plugins/.../syntax-reference.md, SKILL.md, examples.md, best-practices.md, tests/, and the conformance checklist. A post-merge grep sweep for renamed terms (`tri-state`, `tristate`) would have caught the residuals immediately.

## Related Issues

- [Issue #79](https://github.com/quadralay/markdown-plus-plus/issues/79) — Tracking issue for all F1–F10 items
- [PR #78 / Issue #72](https://github.com/quadralay/markdown-plus-plus/issues/72) — Established the Unset pass-through semantics this documentation describes
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` — Foundational spec document defining the Condition State Model
- `docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md` — Variable substitution (Phase 1 Step 2) that still applies inside Unset blocks
- `docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md` — Condition expression operator precedence (NOT > AND > OR); verify no residual tri-state references
