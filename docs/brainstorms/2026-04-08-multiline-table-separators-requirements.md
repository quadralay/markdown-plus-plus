---
date: 2026-04-08
topic: multiline-table-separators
---

# Multiline Table Row Separator Pattern

## Problem Frame

Authors writing multiline tables need to understand how row boundaries work. The current documentation describes row separators as "empty rows" or rows that are "empty or contain only whitespace," which is misleading. The ePublisher parser requires pipe characters to be present -- a truly blank line (no pipes) does not separate rows but instead **ends the table entirely**.

Additionally, two behaviors that the multiline algorithm supports are undocumented: multiline header rows and the cell content dedent algorithm.

## Requirements

- R1. **Document the exact row separator pattern.** A row separator is a table row where every cell contains only whitespace. Pipe characters must be present (e.g., `|   |   |`). The parser pattern is `^ {0,3}\|(?:[ ]*\|)+[ ]*$` -- up to 3 leading spaces, then pipe-delimited cells containing only spaces.

- R2. **Clarify that blank lines end the table.** A completely blank line (no pipe characters) terminates the multiline table. It does not function as a row separator. This distinction must be explicit in the syntax reference and any place that describes separator behavior.

- R3. **Document multiline header support.** The multiline row algorithm applies to both header rows (above the delimiter row) and body rows (below it). A header can span multiple physical lines using the same continuation-row pattern (empty first cell). Document this with an example.

- R4. **Document the cell content dedent algorithm.** When a multiline cell spans multiple physical lines, the processor strips the minimum common leading whitespace across all lines of that cell's content. This "dedent" normalization ensures that indentation used for visual alignment in the source table does not produce unwanted leading spaces in the output. Document this behavior with a before/after example.

## Success Criteria

- A reader of the syntax reference can distinguish a row separator (pipes with whitespace) from a blank line (which ends the table)
- Multiline header rows are documented with at least one example
- The dedent algorithm is explained clearly enough that an author can predict the output whitespace for a given input

## Scope Boundaries

- **In scope:** Documentation updates to the syntax reference, SKILL.md, best practices, examples, and spec documents (whitepaper, processing model, formal grammar) as needed
- **Out of scope:** Parser code changes, new features, test automation
- **Out of scope:** Extensions inside multiline table cells (covered by #21)

## Key Decisions

- **Document parser-actual behavior, not idealized behavior:** The regex pattern is the source of truth. Documentation must match what the parser does, not what might seem intuitive.
- **Multiline headers are supported:** The algorithm applies uniformly to header and body rows. This is existing behavior to document, not a new feature to design.
- **Dedent is minimum-common-whitespace stripping:** The algorithm finds the minimum leading whitespace across all lines in a cell and strips that amount from each line. This preserves relative indentation within the cell.

## Dependencies / Assumptions

- The parser regex `^ {0,3}\|(?:[ ]*\|)+[ ]*$` is the authoritative definition of a row separator (from ePublisher implementation)
- The dedent algorithm uses minimum common leading whitespace (standard dedent approach)
- Related: #11 (formal grammar) and #21 (extensions inside multiline cells)

## Outstanding Questions

### Deferred to Planning

- [Affects R1, R2][Needs research] Which specific files and sections need updates? The planner should audit all locations where multiline table separators are described (syntax-reference.md, SKILL.md, best-practices.md, whitepaper.md, processing-model.md, formal-grammar.md, examples/multiline-tables.md).
- [Affects R3][Needs research] Should the formal grammar in formal-grammar.md be extended with multiline header productions, or is the current `multiline_cmd` production sufficient?
- [Affects R4][Technical] Should the dedent algorithm be added to the processing model spec as a conformance requirement, or documented only in the syntax reference as guidance?

## Next Steps

-> `/ce:plan` for structured implementation planning
