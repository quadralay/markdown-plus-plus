---
date: 2026-04-08
topic: processing-model
---

# Processing Model for Markdown++ Extensions

## Problem Frame

Markdown++ defines syntax for seven extension types (variables, conditions, styles, includes, markers, aliases, and multiline tables), but there is no specification of how a conformant processor should evaluate them. The syntax reference describes what each extension looks like; it does not describe the runtime semantics a tool must implement to produce correct output.

Without a processing model, every implementor must guess at fundamental questions — processing order, include scoping, condition evaluation, variable resolution, and error handling. This makes it impossible to build a second conformant implementation or to reason about document behavior when extensions interact.

The ePublisher Markdown++ adapter contains an implicit processing model that has been in production use. This effort extracts and formalizes that model as the normative specification for the format.

## Requirements

### Phase pipeline

- R1. The spec MUST define a deterministic, ordered processing pipeline that all conformant processors follow. The pipeline has two major phases: **Phase 1 (pre-processing)** operates on raw text before Markdown parsing; **Phase 2 (parsing and rendering)** operates on the Markdown AST with extension-aware grammars.
- R2. Phase 1 MUST specify three sequential steps in this order: (1) include expansion with per-file condition evaluation, (2) variable substitution, (3) handoff to Phase 2.
- R3. The spec MUST state the critical ordering implications explicitly: variables inside false condition blocks are never resolved; variable values cannot contain condition syntax; variable values can contain Markdown syntax.

### Include expansion

- R4. Include expansion MUST be specified as depth-first recursive, with cycle detection that skips circular includes and emits a warning.
- R5. The spec MUST define path resolution as relative to the containing file's directory.
- R6. The spec MUST define per-file condition scoping: each included file's conditions are evaluated individually before its content is spliced into the parent. Condition start and end tags must both exist within the same file — a condition cannot span an include boundary.
- R7. The spec MUST define that included content is inserted with block-level separation (surrounded by blank lines) and inherits the parent's variable context.
- R8. The spec SHOULD define a maximum include depth (or state that implementations MAY impose one) to prevent resource exhaustion from deeply nested includes.

### Condition evaluation

- R9. The spec MUST formalize the tri-state condition model: each condition name evaluates to Visible, Hidden, or Unset. Unset conditions always render their content (document-default behavior).
- R10. The spec MUST define operator precedence: NOT (highest) > AND (space-separated) > OR (comma-separated). Example: `!a b,c` parses as `((!a) AND b) OR c`.
- R11. The spec MUST state that condition blocks cannot span across include boundaries (consequence of R6).

### Variable resolution

- R12. The spec MUST define the variable input model: variables are resolved from a key-value map provided to the processor at build time. The spec does not prescribe how the map is populated (environment, config file, CLI flags are all valid).
- R13. The spec MUST define behavior for undefined variables: the `$name;` token passes through unresolved (preserved as literal text) with a warning.
- R14. The spec MUST define two escaping mechanisms: (1) backslash escaping (`\$name;`) resolved before variable substitution, and (2) inline code spans (`` `$name;` ``) excluded from variable scanning.
- R15. The spec MUST state that variable values can contain Markdown syntax (substituted before Markdown parsing) but cannot contain condition syntax (conditions are already resolved).

### Extension extraction (Phase 2)

- R16. The spec MUST define how style, alias, marker, and multiline commands are extracted from HTML comments during Markdown parsing, including the attachment rule (cross-reference to `spec/attachment-rule.md`).
- R17. The spec MUST define the combined command evaluation order when multiple commands appear in a single comment separated by semicolons: style, then multiline, then marker(s), then alias.

### Output model

- R18. The spec MUST define the output of processing in implementation-agnostic terms: a CommonMark document tree annotated with Markdown++ metadata (styles, markers, aliases). The spec does not prescribe the final rendered format (HTML, PDF, XML are all valid targets).

### Error handling

- R19. The spec MUST distinguish between fatal errors (processing cannot continue) and recoverable warnings (processing continues with degraded output).
- R20. The spec MUST define required diagnostic categories with MDPP codes, extending the existing validation pattern (e.g., MDPP009 for orphaned tags).
- R21. The spec SHOULD specify that processors collect all diagnostics rather than halting on first error, to support batch authoring workflows.

### Conformance

- R22. The spec MUST define what constitutes a conformant Markdown++ processor: minimum required features and optional features.
- R23. The spec SHOULD reference or define a test suite that implementations can use to verify conformance.

## Success Criteria

- A developer can read `spec/processing-model.md` and implement a conformant Markdown++ processor without consulting the ePublisher source code
- All six question categories from issue #8 are answered with normative statements
- The spec is consistent with the existing `spec/attachment-rule.md` and `syntax-reference.md` — no contradictions
- The processing pipeline is deterministic: given the same input document, variable map, and condition set, any conformant processor produces the same output

## Scope Boundaries

- **In scope**: Processing phases, evaluation order, extension semantics, error model, conformance definition
- **In scope**: Formalizing the ePublisher processing model as the normative standard
- **Out of scope**: Prescribing how variable maps or condition sets are configured (CLI flags, config files, etc.)
- **Out of scope**: Defining a specific output format (HTML, PDF, XML) — only the abstract output model
- **Out of scope**: Modifying the syntax reference — the processing model references existing syntax, it does not redefine it
- **Out of scope**: Building a reference implementation or test suite (those are follow-up work items)
- **Out of scope**: Defining a formal grammar (BNF/PEG) for Markdown++ syntax

## Key Decisions

- **Tri-state conditions are normative**: The Visible/Hidden/Unset model is part of the format spec, not an ePublisher implementation detail. Rationale: the "unset = render" behavior is fundamental to how authors write conditional content and cannot be left to implementor discretion.
- **Per-file condition scoping is normative**: Conditions are evaluated per-file during include expansion, not globally after all includes are resolved. Rationale: this is the existing behavior, and global scoping would create confusing cross-file dependencies.
- **Undefined variables pass through**: An undefined `$name;` is preserved literally with a warning, rather than being replaced with empty string or causing a fatal error. Rationale: this enables incremental authoring where not all variables are defined at every build stage.
- **Output model is abstract**: The spec defines a CommonMark tree + metadata, not a specific rendered format. Rationale: Markdown++ is a source format consumed by multiple publishing tools.
- **Spec location**: `spec/processing-model.md`, following the pattern established by `spec/attachment-rule.md`.

## Dependencies / Assumptions

- Assumes `spec/attachment-rule.md` remains the authoritative source for tag attachment semantics — the processing model references it rather than duplicating
- Assumes the syntax reference (`syntax-reference.md`) continues to define the syntax for all seven extension types — the processing model defines evaluation semantics only
- The ePublisher two-phase pipeline (pre-processing → Markdown parsing) is the correct model to formalize, as it is the only production implementation

## Outstanding Questions

### Deferred to Planning

- [Affects R8][Technical] What specific maximum include depth should be recommended? Need to balance practical nested documentation structures against resource exhaustion.
- [Affects R20][Needs research] What is the complete set of MDPP diagnostic codes? Need to inventory existing codes from `validate-mdpp.py` and define new ones for processing errors (circular includes, undefined variables, unclosed conditions, etc.).
- [Affects R22][Technical] What features are required vs. optional for conformance? Candidate optional features: multiline tables, combined commands, maximum include depth enforcement.
- [Affects R23][Needs research] What format should conformance test cases take? Need to research how other specification projects (CommonMark, CSS) structure their test suites.

## Next Steps

→ `/ce:plan` for structured implementation planning
