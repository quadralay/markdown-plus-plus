---
date: 2026-04-08
topic: formal-grammar
---

# Formal Grammar (EBNF/PEG) for Markdown++ Extensions

## Problem Frame

Markdown++ syntax is currently defined through prose descriptions, examples, and regex patterns in `validate-mdpp.py`. This is insufficient for third-party parser authors who need an unambiguous, machine-readable specification. The whitepaper positions Markdown++ as an open documentation format welcoming third-party tool support — a formal grammar is the standard mechanism for delivering on that promise.

Without a formal grammar:
- Parser authors must reverse-engineer behavior from prose, examples, and regex patterns
- Edge cases are ambiguous (e.g., whitespace handling in combined commands, condition expression precedence)
- There is no authoritative definition for testing implementations
- The existing regex patterns in `validate-mdpp.py` are a de facto grammar but are incomplete and have known gaps (e.g., `markers_json` doesn't handle nested braces)

## Requirements

- R1. Produce an EBNF grammar covering all Markdown++ extension constructs, placed in `spec/` alongside the whitepaper and attachment rule
- R2. Define two identifier productions — a standard identifier rule and an alias-specific variant that permits digit-first names (per the existing alias exception documented in `syntax-reference.md` and enforced by `validate-mdpp.py`)
- R3. Define the condition expression sub-grammar with explicit operator precedence: NOT (highest, prefix `!`), AND (medium, space-separated), OR (lowest, comma-separated)
- R4. Specify the combined-command semicolon syntax, including that unrecognized segments between semicolons are silently ignored as inline comments (per `syntax-reference.md` "Unrecognized Segments" section)
- R5. Document the attachment rule and inline placement rule as structural constraints referenced by the grammar but not expressed as pure syntax productions (attachment is positional/contextual, not syntactic)
- R6. Specify variable escaping: backslash (`\$`) processed before variable substitution, and inline code span exclusion
- R7. Provide a PEG transliteration as a secondary format alongside the primary EBNF
- R8. Reference the JSON specification (RFC 8259) for `markers:` JSON values rather than inlining a JSON grammar
- R9. Define the file path production for `include:` directives (forward slashes, relative paths, `.md` extension)
- R10. Validate the grammar against all existing examples in `examples/` and test files in `tests/`

## Success Criteria

- A third-party developer can implement a Markdown++ extension recognizer from the grammar alone, without consulting prose documentation
- The grammar correctly accepts all valid constructs found in `examples/` and `tests/sample-full.md`
- The grammar correctly rejects the invalid constructs in `tests/sample-invalid-names.md`
- Edge cases documented in the attachment rule spec and syntax reference are either expressed in the grammar or explicitly referenced as structural constraints

## Scope Boundaries

- **In scope:** All Markdown++ extension syntax (variables, styles, aliases, conditions, includes, markers, multiline, combined commands)
- **In scope:** Structural constraint documentation for attachment rules and inline placement
- **Out of scope:** CommonMark 0.30 grammar — the Markdown++ grammar defines how extensions are recognized within a CommonMark document, not the document itself
- **Out of scope:** Semantic processing rules (variable resolution, condition evaluation, include processing)
- **Out of scope:** UTF-8 letter support beyond ASCII — the syntax reference notes this is a future goal; the grammar should use a placeholder production (`letter`) that can be extended later
- **Out of scope:** Updating `validate-mdpp.py` regex patterns to match the grammar (separate issue)

## Key Decisions

- **EBNF primary, PEG secondary**: EBNF is more widely understood for specification; PEG is more directly implementable. Providing both serves different audiences.
- **Two identifier productions**: The alias exception (digit-first allowed) is an intentional design choice documented in the syntax reference and enforced in the validator. The grammar must reflect this rather than force a single unified rule.
- **Attachment as structural constraint, not syntax**: Attachment depends on line adjacency and blank lines — positional relationships that EBNF/PEG cannot naturally express. Document as normative prose constraints that reference the grammar productions.
- **Reference JSON spec for markers**: Inlining a JSON grammar would be redundant and error-prone. Reference RFC 8259 and note that the validator's current nested-brace limitation is an implementation gap, not a grammar limitation.
- **Unrecognized segments are inline comments**: This is a key interoperability decision already documented in the syntax reference. The grammar must express that a command list can contain non-matching segments that are silently discarded.

## Dependencies / Assumptions

- The existing syntax reference (`references/syntax-reference.md`) and attachment rule spec (`spec/attachment-rule.md`) are authoritative for the current behavior the grammar must formalize
- The existing regex patterns in `validate-mdpp.py` are a reference implementation but have known gaps — the grammar is the specification, not the regex
- The grammar assumes CommonMark 0.30 as the base document format

## Outstanding Questions

### Deferred to Planning

- [Affects R1][Technical] Exact EBNF notation variant to use — ISO 14977, W3C EBNF, or a widely-used informal variant. Planning should survey what other specifications (CommonMark, CSS, etc.) use and choose accordingly.
- [Affects R4][Needs research] How to formally express "unrecognized segment" in the grammar — whether as an explicit catch-all production or as a prose constraint on command list parsing.
- [Affects R9][Technical] Whether the file path production should restrict to specific characters or use a permissive "not `-->` or `>`" boundary, matching the current regex approach.
- [Affects R7][Technical] Whether the PEG transliteration should be a mechanical transliteration or an idiomatic PEG that takes advantage of PEG-specific features (ordered choice, greedy matching).

## Next Steps

→ `/ce:plan` for structured implementation planning
