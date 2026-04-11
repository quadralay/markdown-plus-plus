---
title: Unset condition handling consolidated into single pre-evaluation check
date: 2026-04-11
category: logic-errors
module: specification
problem_type: logic_error
component: documentation
symptoms:
  - Unset condition handling duplicated across ~20 locations in 3 spec files
  - OR operator Unset behavior was semantically incorrect
  - Per-operator Unset propagation created redundancy and inconsistency risk
  - Specification complexity inflated by repeated three-valued operator definitions
root_cause: logic_error
resolution_type: documentation_update
severity: medium
tags:
  - specification
  - conditional-processing
  - unset-conditions
  - boolean-logic
  - spec-simplification
  - processing-model
---

# Unset condition handling consolidated into single pre-evaluation check

## Problem

The Markdown++ specification embedded Unset condition handling (what happens when a condition name is not defined in the condition set) into every operator definition, every worked example, and every interaction section across three spec files. This scattered a single cross-cutting rule across ~20 locations, creating redundancy, inconsistency risk, and a semantic bug in the OR operator.

## Symptoms

- **Redundant language in every operator row.** Each of the three operators (NOT, AND, OR) carried an identical clause: "If [any] operand is Unset, block passes through." This appeared in the operator tables of `spec/processing-model.md`, `spec/specification.md`, and `references/syntax-reference.md` -- nine repetitions of the same rule.
- **Verbose expression examples.** The Expression Examples table in `syntax-reference.md` had 10 rows, with 4 dedicated to Unset variants, each restating "any Unset operand forces pass-through" with slightly different wording.
- **Dedicated "counter-intuitive" worked examples.** Both `specification.md` and `processing-model.md` contained a full "Compound Expression with Mixed Assigned/Unset Operands" section (input, output, explanation) -- 18 lines per file -- solely to explain why `web mobile` passes through even when `web=Visible`.
- **Three-valued operator definitions.** Operator behavior columns described three outcomes (true, false, pass-through) instead of pure boolean (true, false), making the spec harder to reason about.
- **OR semantic bug.** The OR operator stated "If any operand is Unset, block passes through." But for OR, if one operand is already Visible, the expression is true under standard boolean logic. The blanket pass-through was wrong for that case.
- **Editorial bloat from documentation efforts.** Issue #79 / PR #81 tried to fix confusion by adding more documentation -- compound expression examples, interaction subsections, expression example table rows -- across 10 items (F1-F10). This made the problem worse by increasing the surface area.

## What Didn't Work

- **Per-operator Unset propagation (PR #78, issue #72).** The original fix changed Unset from "evaluates as Visible" to "causes pass-through," but embedded this into every operator's behavior column. This required every operator to describe three outcomes, every worked example to demonstrate the Unset case, and every interaction section to mention Unset behavior. ~70 lines of Unset-specific language across three files.

- **More documentation for the same approach (issue #79).** When readers found the per-operator Unset behavior confusing (especially the "counter-intuitive" OR case), the response was to add explanatory content: compound expression examples, interaction tables, expression example rows, best-practices guidance, and test specimens. This grew the documentation without addressing the root cause.

- **Three-valued (Kleene) logic.** Considered as a formal framework for the OR bug, but rejected because it would make the spec more complex: every operator would need a full three-valued truth table.

## Solution

Replaced all per-operator Unset propagation with a single **Unset Pre-Evaluation Check**.

**Before -- Unset embedded in every operator (three files x three operators):**

```markdown
| NOT | `!` | Inverts the state. If `name` is Unset, the block passes through. |
| AND | ` ` | All must be true. If any operand is Unset, the block passes through. |
| OR  | `,` | Any must be true. If any operand is Unset, the block passes through. |
```

Plus 18-line "Compound Expression with Mixed Assigned/Unset Operands" worked examples in two files.

**After -- single pre-check, pure boolean operators:**

```markdown
##### Unset Pre-Evaluation Check
Before evaluating a condition expression, a processor MUST check whether all
condition names are defined. If any name is Unset, the block passes through
as-is. Otherwise, evaluate using standard boolean logic (Visible=true,
Hidden=false).

| NOT | `!` | Inverts the value. True when operand is Hidden. |
| AND | ` ` | All operands must be true (Visible). |
| OR  | `,` | Any operand must be true (Visible). |
```

One inline sentence replaces the 18-line worked examples.

Changes applied across `spec/processing-model.md`, `spec/specification.md`, and `references/syntax-reference.md`. Net removal of 28 lines.

## Why This Works

The key insight is that Unset is not an operator-level concern -- it is a pre-condition for evaluation. Operators should never encounter Unset values because the check fires before they run.

1. **Single rule, single location.** The pre-check section is the one place that defines pass-through behavior. Everything else cross-references it.
2. **Operators become pure boolean.** Once the pre-check passes, the processor works with exactly two values: true (Visible) and false (Hidden). Operator definitions need only describe boolean behavior.
3. **The OR bug disappears structurally.** The bug existed because per-operator Unset handling forced OR to choose between "pass through" (wrong when another operand is Visible) and "evaluate" (wrong because it silently ignores the Unset name). With the pre-check, OR only runs when all operands are defined.
4. **Counter-intuitive cases need no special explanation.** The behavior is self-evident: the check found an undefined name, so evaluation never started.

## Prevention

- **Define cross-cutting rules at one location with cross-references.** When a rule applies to all operators uniformly, it belongs in a shared pre-condition section, not in each operator's behavior column. The duplication signal: if you're copy-pasting the same clause into N table cells, extract it.
- **Express uniform constraints as pre-conditions, not per-operator behavior.** The architectural question: "Does this concern belong inside operator logic or before it?" If the answer is the same regardless of which operator runs, it's a pre-condition.
- **Test spec edits for editorial bloat.** If a new concept adds language to N locations, ask: "Is there a single-location alternative?" The bloat signal is needing "counter-intuitive" worked examples -- if readers need special explanation for routine cases, the architecture is pushing complexity to the wrong level.
- **Resist the instinct to document around a structural problem.** When users find behavior confusing, question the architecture first, not add more documentation for the existing architecture.
- **Watch for three-valued logic as a complexity smell.** If your boolean operators need a third value, check whether that third value is a pre-condition that should be resolved before operators run.

## Related Issues

- [#79](https://github.com/quadralay/markdown-plus-plus/issues/79) -- Complete Unset condition documentation (the documentation effort this simplification made partially unnecessary)
- [#72](https://github.com/quadralay/markdown-plus-plus/issues/72) -- Fix Unset condition semantics (established pass-through behavior)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Define the processing model (where the condition evaluation pipeline is formally specified)
- `docs/solutions/documentation-gaps/unset-passthrough-condition-semantics-2026-04-11.md` -- Describes the per-operator documentation effort (F1-F10) that this consolidation replaced
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` -- Parent specification where the pre-evaluation check is defined
