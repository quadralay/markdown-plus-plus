---
title: Formal EBNF/PEG grammar for Markdown++ extensions
date: 2026-04-08
category: documentation-gaps
module: spec/formal-grammar
problem_type: documentation_gap
component: documentation
symptoms:
  - "No formal machine-readable grammar existed for Markdown++ extensions"
  - "Syntax defined only through prose descriptions and regex patterns in validation script"
  - "Third-party parser authors lacked unambiguous specification for implementation"
  - "Operator precedence for condition expressions was undocumented formally"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - ebnf
  - peg
  - grammar
  - formal-specification
  - parser
  - condition-expressions
---

# Formal EBNF/PEG grammar for Markdown++ extensions

## Problem

Markdown++ syntax was defined only through prose descriptions in `syntax-reference.md`, scattered examples, and regex patterns in `validate-mdpp.py`. Third-party parser authors had no unambiguous, machine-readable specification to build conformant implementations against, despite the whitepaper positioning Markdown++ as an open format welcoming third-party tools.

## Symptoms

- Parser authors had to reverse-engineer syntax behavior from prose and regex, with no guarantee of completeness or correctness.
- Edge cases remained ambiguous -- whether `$123start;` is a valid variable, whether alias names can start with digits, and how operator precedence works in condition expressions like `!draft,web production`.
- The regex patterns in `validate-mdpp.py` had known gaps (e.g., `markers_json` used `r'\{[^}]+\}'` which cannot handle nested braces in JSON), but there was no authoritative specification to distinguish implementation limitation from intended behavior.
- No formal conformance definition existed -- implementors could not objectively verify whether their parser was correct.
- Combined-command parsing rules (semicolons as segment delimiters, unrecognized segments silently discarded, JSON objects consuming semicolons greedily) were described only in prose.

## What Didn't Work

Three prior artifacts existed but were individually insufficient:

1. **Prose descriptions in `syntax-reference.md`**: Natural language is inherently ambiguous for syntax specification. The naming rules section described two identifier patterns, but the precedence relationship among condition operators (NOT > AND/space > OR/comma) required careful reading to extract. The combined-command semicolon syntax and its interaction with JSON markers containing semicolons was particularly difficult to convey unambiguously in prose.

2. **Regex patterns in `validate-mdpp.py`**: The validator's regex patterns served as a partial reference implementation, but they had known limitations. The `markers_json` regex cannot handle nested JSON objects. Regex patterns cannot express recursive structures or operator precedence in condition expressions. Implementors who treated the regex as spec would build parsers with the same limitations.

3. **Example files**: The five example files and two test files demonstrated correct and incorrect usage, but examples alone cannot specify boundary conditions exhaustively. An implementor looking at examples cannot determine whether an unlisted pattern is valid or invalid.

The fundamental gap was that none of these artifacts provided a single, authoritative, compositional definition of the syntax that a parser author could implement directly.

## Solution

Created `spec/formal-grammar.md` (539 lines), a formal grammar specification containing:

**W3C EBNF grammar**: Uses W3C EBNF notation (the same variant used by XML and CSS specifications). The top-level production `mdpp_extension ::= variable | escaped_variable | mdpp_comment` establishes that Markdown++ adds exactly two syntactic forms to CommonMark: inline variable tokens and HTML comment directives.

**Three identifier productions**: `identifier ::= (letter | "_") (letter | digit | "-" | "_")*` for variables and conditions, `alias_name ::= (letter | digit | "_") (letter | digit | "-" | "_")*` for aliases (digit-first supports CMS record IDs like `#04499224`), and `style_name ::= (letter | "_") (letter | digit | "-" | "_" | " ")*` for styles and markers (embedded spaces support compound names like `Blockquote Paragraph`). These correspond to the validator's `STANDARD_NAME_RE`, `ALIAS_NAME_RE`, and `STYLE_NAME_RE`. The third production was added by #52 to correct the original two-pattern system's overreach in forbidding spaces for styles and markers.

**Condition expression sub-grammar with operator precedence**: Layered productions encode precedence structurally: `or_expr ::= and_expr (ws? "," ws? and_expr)*`, `and_expr ::= unary_expr (ws unary_expr)*`, `unary_expr ::= "!"? identifier`. This means NOT (prefix `!`) binds tightest, AND (space) is medium, OR (comma) is lowest. Example: `!draft,web production` parses as `(NOT "draft") OR ("web" AND "production")`.

**Combined-command syntax**: `command_list ::= segment (ws? ";" ws? segment)*` with `segment ::= command | unrecognized_text`. For `markers_cmd`, the grammar requires greedy JSON parsing (matching balanced braces) before looking for the next delimiter, so semicolons within JSON string values do not split the segment.

**Variable escaping**: Two mechanisms formalized. Syntactic: `escaped_variable ::= "\" "$" identifier ";"` resolved before variable substitution. Processing: code span exclusion -- content inside CommonMark backtick delimiters is excluded from variable scanning entirely.

**PEG transliteration**: Complete idiomatic PEG grammar with ordered choice (`markers_cmd` before `marker_cmd` to avoid backtracking), negative lookahead for boundary detection, and a simplified JSON production with balanced-brace matching.

**Conformance definition**: A grammar-conformant parser must accept all matching strings, reject non-matching strings, enforce structural constraints from `spec/attachment-rule.md`, delegate JSON parsing to an RFC 8259-compliant parser, and exclude code spans and fenced code blocks from extension scanning.

**Validation**: Verified against `tests/sample-full.md` (20 line references), `tests/sample-invalid-names.md` (8 rejection + 7 valid edge cases), and all five example files. Five documented edge cases: whitespace flexibility, combined commands with unrecognized segments, JSON markers with semicolons in values, empty condition blocks, and condition close whitespace variants.

## Why This Works

The root cause was that syntax was defined through three different lenses (prose, regex, examples), each with inherent limitations: prose is ambiguous, regex cannot express recursion or precedence, and examples cannot exhaustively enumerate boundary conditions. A formal grammar resolves this because it provides a single, compositional, unambiguous definition where every valid string is derivable from the productions and every invalid string fails to derive. The layered condition expression productions make operator precedence structural rather than requiring interpretation. The explicit `segment` and `unrecognized_text` productions formalize the combined-command parsing strategy that was previously only described in prose.

## Prevention

- **Grammar-first for new syntax**: Any new Markdown++ extension construct must have a corresponding grammar production added to `spec/formal-grammar.md` before or concurrently with the prose description in `syntax-reference.md`. The grammar is the authoritative source; the validator is an implementation that may lag.
- **Validation script alignment**: Known divergences between the grammar and `validate-mdpp.py` regex patterns (e.g., nested JSON handling) are documented as implementation limitations. The validator should be updated to conform to the grammar over time (tracked as issue #27 for ePublisher adapter patterns).
- **Test corpus maintenance**: Future syntax additions should add test cases to `sample-full.md` and `sample-invalid-names.md`, verify the grammar accepts/rejects them correctly, and document validation in the "Validation Notes" section of the grammar spec.
- **Automated grammar-based testing**: Generating a parser from the PEG and running it against the test corpus would provide continuous conformance verification (future initiative).

## Related Issues

- [#11](https://github.com/quadralay/markdown-plus-plus/issues/11) -- Create a formal grammar (EBNF/PEG) for Markdown++ extensions (this issue)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Write a formal Markdown++ specification (grammar is a major deliverable toward this)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Define the processing model (grammar explicitly excludes semantic processing)
- [#23](https://github.com/quadralay/markdown-plus-plus/issues/23) -- Add UTF-8 character encoding requirement (may affect `letter` production)
- [#27](https://github.com/quadralay/markdown-plus-plus/issues/27) -- Update ePublisher adapter regex patterns to enforce unified naming rule
- [#52](https://github.com/quadralay/markdown-plus-plus/issues/52) -- Added `style_name` production for embedded spaces in style/marker names (extended two identifier forms to three)
- `docs/solutions/logic-errors/unified-naming-rule-regex-inconsistency-2026-04-06.md` -- Complementary: established the `STANDARD_NAME_RE` and `ALIAS_NAME_RE` regex patterns that the grammar formalizes as EBNF productions
- `docs/solutions/logic-errors/embedded-spaces-in-style-marker-names-2026-04-08.md` -- Extended the naming system with `STYLE_NAME_RE` for styles and markers
- `docs/solutions/documentation-gaps/attachment-rule-formal-spec-2026-04-07.md` -- Complementary: defines positional constraints referenced by the grammar's structural constraints table
- `docs/solutions/documentation-gaps/variable-escaping-mechanism-2026-04-06.md` -- Complementary: documented escaping mechanisms that the grammar formalizes as the `escaped_variable` production
