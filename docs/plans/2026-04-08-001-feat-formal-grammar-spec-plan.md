---
title: "feat: Add formal EBNF/PEG grammar for Markdown++ extensions"
type: feat
status: completed
date: 2026-04-08
origin: docs/brainstorms/2026-04-08-formal-grammar-requirements.md
---

# feat: Add formal EBNF/PEG grammar for Markdown++ extensions

## Overview

Create a formal grammar specification for all Markdown++ extension constructs using EBNF as the primary notation and PEG as a secondary transliteration. The grammar covers only the Markdown++ extensions -- it does not re-specify CommonMark 0.30. It defines how Markdown++ constructs are recognized within a CommonMark document.

## Problem Frame

Markdown++ syntax is currently defined through prose descriptions in `syntax-reference.md`, examples, and regex patterns in `validate-mdpp.py`. This is insufficient for third-party parser authors who need an unambiguous, machine-readable specification. The whitepaper positions Markdown++ as an open documentation format welcoming third-party tool support -- a formal grammar is the standard mechanism for delivering on that promise.

Without a formal grammar, parser authors must reverse-engineer behavior from prose and regex, edge cases remain ambiguous, and there is no authoritative definition for testing implementations. (see origin: `docs/brainstorms/2026-04-08-formal-grammar-requirements.md`)

## Requirements Trace

- R1. EBNF grammar covering all Markdown++ extension constructs, placed in `spec/`
- R2. Two identifier productions -- standard identifier and alias-specific variant (digit-first allowed)
- R3. Condition expression sub-grammar with explicit operator precedence (NOT > AND > OR)
- R4. Combined-command semicolon syntax, including unrecognized segments as inline comments
- R5. Attachment/placement rules as structural constraints referenced by the grammar
- R6. Variable escaping specification (`\$` and inline code span exclusion)
- R7. PEG transliteration as secondary format
- R8. Reference JSON spec (RFC 8259) for `markers:` JSON values
- R9. File path production for `include:` directives
- R10. Validate grammar against existing examples and tests

## Scope Boundaries

- **In scope:** All Markdown++ extension syntax (variables, styles, aliases, conditions, includes, markers, multiline, combined commands)
- **In scope:** Structural constraint documentation for attachment rules and inline placement
- **Out of scope:** CommonMark 0.30 grammar -- the Markdown++ grammar defines how extensions are recognized within a CommonMark document
- **Out of scope:** Semantic processing rules (variable resolution, condition evaluation, include processing)
- **Out of scope:** UTF-8 letter support beyond ASCII -- the grammar uses a placeholder `letter` production extensible later
- **Out of scope:** Updating `validate-mdpp.py` regex patterns to match the grammar (separate issue)

## Context & Research

### Relevant Code and Patterns

- `spec/whitepaper.md` -- Positions Markdown++ extensions as HTML comments and inline tokens; establishes the CommonMark 0.30 base
- `spec/attachment-rule.md` -- Formal spec for tag-to-element binding; the grammar should reference this for structural constraints rather than re-defining attachment
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` -- Authoritative prose definition of all constructs, naming rules, condition expressions, combined commands, and comment disambiguation
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py` -- Reference implementation with regex patterns; has known gaps (e.g., `markers_json` doesn't handle nested braces)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-full.md` -- Comprehensive test file exercising all features
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-invalid-names.md` -- Positive/negative test cases for naming rules

### Institutional Learnings

- **Unified naming rule** (`docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md`): Established `STANDARD_NAME_RE` and `ALIAS_NAME_RE` as the authoritative patterns. The grammar's identifier productions must match these exactly. Key insight: the alias exception (digit-first allowed) is intentional, not a bug.
- **Attachment rule formalization** (`docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md`): Attachment is positional/contextual, not syntactic. The grammar should reference `spec/attachment-rule.md` rather than attempt to express attachment in EBNF.
- **Variable escaping** (`docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md`): Two mechanisms -- `\$` (resolved before variable substitution) and inline code spans (excluded from scanning). The grammar should express the `\$` escape as a production and note code span exclusion as a prose constraint.

### External References

- W3C EBNF notation (used by XML and CSS specifications)
- RFC 8259 (JSON specification) -- referenced by `markers:` JSON values
- CommonMark 0.30 specification -- base document format
- Bryan Ford, "Parsing Expression Grammars" (2004) -- PEG formalism

## Key Technical Decisions

- **W3C EBNF as primary notation**: W3C EBNF is widely understood by parser implementers and used by XML, CSS, and web specifications. ISO 14977 is too verbose for readability; informal variants lack precision. W3C EBNF provides the right balance.

- **Two identifier productions, not one**: The alias exception (digit-first allowed) is an intentional design choice, not a simplification gap. The grammar defines `identifier` (standard) and `alias_name` (digit-first permitted) as separate productions. This matches the existing `STANDARD_NAME_RE` and `ALIAS_NAME_RE` in the validator.

- **Unrecognized segments as explicit catch-all production**: Combined commands contain segments separated by semicolons. Segments not matching any known command are silently ignored. The grammar expresses this with a `segment` production that captures any text between semicolons/boundaries, and a `command_list` production where each segment is either a recognized command or discarded. This is more precise than prose-only treatment.

- **File path as permissive boundary production**: The `file_path` production matches any non-empty sequence not containing `-->`, consistent with the current regex `[^>]+?`. Over-restricting path characters would break valid file paths on various operating systems.

- **Idiomatic PEG transliteration**: The PEG version uses ordered choice (`/`) and greedy matching idiomatically rather than mechanical 1:1 EBNF mapping. This serves PEG-literate implementers who want a directly usable grammar, not just an alternate rendering of the EBNF.

- **Attachment as referenced structural constraint**: Attachment depends on line adjacency and blank lines -- positional relationships that EBNF/PEG cannot naturally express. The grammar references `spec/attachment-rule.md` and documents which productions require attachment, but does not attempt syntactic productions for positional rules.

- **Reference JSON spec for markers**: Inlining a JSON grammar would be redundant and error-prone. The grammar references RFC 8259 and defines `json_object` as a terminal referencing that spec. The validator's current nested-brace limitation is an implementation gap, not a grammar limitation.

- **Single document with EBNF and PEG sections**: Both notations live in one `spec/formal-grammar.md` document. This avoids synchronization issues between separate files and lets readers see both representations in context.

## Open Questions

### Resolved During Planning

- **EBNF notation variant** (affects R1): W3C EBNF. Used by XML, CSS, and web specs. Widely understood by parser implementers. ISO 14977 is too verbose; informal variants lack precision.

- **Unrecognized segment representation** (affects R4): Explicit catch-all production. A `segment` production captures any semicolon-delimited text; the `command_list` attempts to match each segment against known commands and discards non-matches. This is expressible in grammar notation and matches the documented behavior in the syntax reference.

- **File path production** (affects R9): Permissive boundary approach. `file_path` matches any non-empty character sequence not containing `-->`. File paths can include a wide variety of characters; restricting further would be over-specification relative to current behavior.

- **PEG transliteration style** (affects R7): Idiomatic PEG. Takes advantage of ordered choice and greedy matching. A mechanical transliteration adds no value over the EBNF for someone who already reads EBNF; an idiomatic PEG serves the PEG-literate parser-author audience.

### Deferred to Implementation

- **Exact whitespace handling in productions**: The grammar will use a `ws` production for optional whitespace within comment directives. The exact definition (spaces only, or spaces and tabs) should be determined by testing against `sample-full.md` during implementation.

- **Marker value escaping**: The simple marker format uses `marker:Key="value"`. Whether `value` can contain escaped double quotes needs to be determined by checking current parser behavior. The grammar should define `marker_value` conservatively and note any escaping rules discovered.

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

```ebnf
(* Top-level: Markdown++ extends CommonMark with two syntactic forms *)
mdpp_extension     ::= variable | escaped_variable | mdpp_comment

(* Variables: the only non-comment extension syntax *)
variable           ::= "$" identifier ";"
escaped_variable   ::= "\" "$" identifier ";"

(* Comment directives: all other extensions use HTML comment syntax *)
mdpp_comment       ::= "<!--" ws? command_list ws? "-->"

(* Combined commands: semicolon-separated, unrecognized segments discarded *)
command_list       ::= segment ( ws? ";" ws? segment )*
segment            ::= command | unrecognized_text
command            ::= style_cmd | alias_cmd | condition_open_cmd
                     | condition_close_cmd | include_cmd
                     | marker_cmd | markers_cmd | multiline_cmd

(* Two identifier forms *)
identifier         ::= ( letter | "_" ) ( letter | digit | "-" | "_" )*
alias_name         ::= ( letter | digit | "_" ) ( letter | digit | "-" | "_" )*

(* Condition expressions with explicit precedence *)
condition_expr     ::= or_expr
or_expr            ::= and_expr ( "," and_expr )*
and_expr           ::= unary_expr ( " " unary_expr )*
unary_expr         ::= "!"? identifier

(* Individual commands *)
style_cmd          ::= "style:" identifier
alias_cmd          ::= "#" alias_name
condition_open_cmd ::= "condition:" condition_expr
condition_close_cmd::= "/condition"
include_cmd        ::= "include:" file_path
marker_cmd         ::= "marker:" identifier '="' marker_value '"'
markers_cmd        ::= "markers:" json_object  (* RFC 8259 *)
multiline_cmd      ::= "multiline"
```

The PEG transliteration will express the same grammar using PEG conventions: `<-` for definitions, `/` for ordered choice, `!` for negative lookahead, and `*`/`+`/`?` for repetition.

## Implementation Units

- [x] **Unit 1: Create EBNF grammar specification document**

**Goal:** Produce the complete EBNF grammar covering all Markdown++ extension constructs as a formal specification document in `spec/`.

**Requirements:** R1, R2, R3, R4, R5, R6, R8, R9

**Dependencies:** None

**Files:**
- Create: `spec/formal-grammar.md`

**Approach:**
- Document structure: frontmatter, introduction (scope, relationship to CommonMark, notation conventions), lexical conventions, EBNF productions, structural constraints, and conformance notes
- Start with lexical terminals: `letter`, `digit`, `ws`, then build up to `identifier` and `alias_name`
- Define each command production matching the syntax reference exactly
- Define `condition_expr` with explicit precedence using the standard technique of layered productions (or_expr > and_expr > unary_expr)
- Define `command_list` with the unrecognized segment catch-all
- Define `variable` and `escaped_variable` as top-level productions
- Document `file_path` with permissive boundary matching
- Reference RFC 8259 for `json_object` in markers
- Add a "Structural Constraints" section referencing `spec/attachment-rule.md` for attachment rules, with a table mapping which productions require attachment
- Add a "Variable Escaping" section explaining both mechanisms (backslash as syntax, code span exclusion as processing constraint)
- Add a "Conformance" section defining what it means for a parser to be grammar-conformant
- Use W3C EBNF notation with a notation legend at the top

**Patterns to follow:**
- `spec/attachment-rule.md` -- for document structure, frontmatter, and specification prose style
- `spec/whitepaper.md` -- for positioning and cross-references to CommonMark
- `syntax-reference.md` naming rules section -- authoritative source for identifier patterns

**Test scenarios:**
- Every production should accept the valid examples from `sample-full.md`
- `identifier` should reject digit-first names per `sample-invalid-names.md` cases 1, 2, 5, 6
- `alias_name` should accept digit-first names per `sample-invalid-names.md` cases 9, 10
- `condition_expr` should correctly parse `!draft,web production` as `(!draft) OR (web AND production)` per the precedence rules
- Combined command with unrecognized segments should parse `<!-- style:CustomHeading ; #alias ; TODO: add markers -->` as two recognized commands plus one discarded segment
- `escaped_variable` should match `\$variable_name;`
- `file_path` should accept `shared/header.md`, `../common/footer.md`, `chapters/introduction.md`

**Verification:**
- Every construct in `syntax-reference.md` has a corresponding grammar production
- Every regex pattern in `validate-mdpp.py` has a corresponding grammar production that accepts a superset of valid inputs (the grammar is the spec; the regex may have implementation limitations)
- The grammar is internally consistent -- no undefined non-terminals, no unreachable productions

- [x] **Unit 2: Add PEG transliteration section**

**Goal:** Provide an idiomatic PEG grammar as a secondary format within the same document, enabling parser authors who prefer PEG to work directly from a PEG-native notation.

**Requirements:** R7

**Dependencies:** Unit 1

**Files:**
- Modify: `spec/formal-grammar.md`

**Approach:**
- Add a "PEG Transliteration" section after the EBNF grammar
- Use standard PEG notation: `<-` for definitions, `/` for ordered choice, `!` and `&` for lookahead, `*`/`+`/`?` for repetition
- Translate idiomatically: use ordered choice to express command matching priority, use negative lookahead for boundary detection (e.g., `file_path` uses `!("-->")`)
- Add a brief notation legend for PEG-specific operators
- Note any semantic differences between EBNF and PEG formulations (e.g., PEG's ordered choice is inherently prioritized while EBNF alternation is not)

**Patterns to follow:**
- Bryan Ford PEG paper notation conventions
- The EBNF section's production naming (same names, PEG notation)

**Test scenarios:**
- PEG grammar should recognize the same language as the EBNF grammar
- Every production in the EBNF section has a corresponding PEG rule
- PEG-specific features (ordered choice for command matching, negative lookahead for boundaries) are used where they improve clarity

**Verification:**
- 1:1 production correspondence between EBNF and PEG sections
- PEG section has its own notation legend
- Any semantic differences between the two notations are explicitly documented

- [x] **Unit 3: Validate grammar against test corpus**

**Goal:** Systematically verify the grammar correctly accepts all valid constructs and rejects known invalid constructs across the existing example and test files.

**Requirements:** R10

**Dependencies:** Unit 1, Unit 2

**Files:**
- Modify: `spec/formal-grammar.md` (add validation results appendix or conformance notes)

**Approach:**
- Walk through each construct in `tests/sample-full.md` and verify the grammar produces the correct parse
- Walk through each invalid case in `tests/sample-invalid-names.md` and verify the grammar rejects it at the correct production
- Spot-check constructs in `examples/*.md` files for coverage
- Document any edge cases discovered during validation as additional notes in the grammar spec
- If any construct in the test corpus cannot be parsed by the grammar, update the grammar to accommodate it (the test corpus reflects current valid Markdown++)

**Patterns to follow:**
- `sample-invalid-names.md` positive/negative case structure for validation approach

**Test scenarios:**
- `sample-full.md` line 6: combined command with JSON markers and alias -- should parse as `markers_cmd` + `alias_cmd`
- `sample-full.md` line 62: alias `#introduction` -- should parse with `alias_name`
- `sample-full.md` line 129: complex condition `!draft,web production` -- should parse as `or_expr` with correct precedence
- `sample-full.md` line 258: combined command `style:CustomHeading ; marker:Keywords="intro" ; #combined-example` -- three recognized commands
- `sample-invalid-names.md` case 1: `$123start;` -- rejected by `identifier` (digit-first)
- `sample-invalid-names.md` case 9: `#04499224` -- accepted by `alias_name` (digit-first alias exception)
- All five example files in `examples/` -- all constructs parseable

**Verification:**
- All valid constructs in `sample-full.md` are accepted
- All invalid constructs in `sample-invalid-names.md` are rejected
- No construct in `examples/` fails to parse
- Validation findings documented in the grammar spec

## System-Wide Impact

- **Interaction graph:** The grammar is a specification document -- it does not execute. It is referenced by future parser implementations and serves as the authoritative definition that `validate-mdpp.py` should conform to.
- **Error propagation:** N/A -- specification document, no runtime behavior.
- **State lifecycle risks:** None.
- **API surface parity:** The grammar must accept a superset of what `validate-mdpp.py` currently accepts. Known validator gaps (e.g., `markers_json` nested braces) are implementation limitations, not grammar limitations.
- **Integration coverage:** Grammar validation is manual for this issue. Automated grammar-based testing would be a separate future initiative.

## Risks & Dependencies

- **Risk: Grammar/validator divergence.** The grammar is the specification; the validator is an implementation. Known gaps (nested braces in JSON markers, validator's `[\w]+` for variables) are already documented. The grammar must be the authoritative source, with validator updates tracked as a separate issue.
- **Risk: Ambiguity in combined-command parsing.** The unrecognized-segment catch-all could theoretically match partial command prefixes. The grammar should use precise command matching so that `style:` only matches when followed by a valid identifier, preventing false catch-all matches.
- **Dependency:** The grammar relies on `spec/attachment-rule.md` for structural constraint definitions. That document is already complete and active.
- **Dependency:** The grammar references the syntax reference for prose definitions. That document is active and stable.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-08-formal-grammar-requirements.md](../brainstorms/2026-04-08-formal-grammar-requirements.md)
- Related spec: [spec/attachment-rule.md](../../spec/attachment-rule.md)
- Related spec: [spec/whitepaper.md](../../spec/whitepaper.md)
- Syntax reference: [plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md)
- Validator: [plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py)
- Test corpus: [plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/](../../plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/)
- Learning: [docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md](../solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md)
- Learning: [docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md](../solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md)
- Learning: [docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md](../solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md)
- External: [W3C EBNF notation](https://www.w3.org/TR/xml/#sec-notation)
- External: [RFC 8259 - JSON specification](https://www.rfc-editor.org/rfc/rfc8259)
- External: [CommonMark 0.30 specification](https://spec.commonmark.org/0.30/)
- Related issue: [#11](https://github.com/quadralay/markdown-plus-plus/issues/11)
