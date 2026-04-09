---
module: multiline-tables
date: 2026-04-08
problem_type: documentation_gap
component: documentation
symptoms:
  - "Row separator described as 'empty or whitespace-only' omitted required pipe characters"
  - "Blank lines incorrectly described as row separators instead of table terminators"
  - "Multiline header support completely undocumented"
  - "Cell content dedent algorithm undocumented"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - multiline-tables
  - row-separator
  - pipe-pattern
  - dedent-algorithm
  - multiline-headers
  - specification
  - issue-20
---

# Multiline table separator pattern, headers, and dedent documentation

## Problem

The Markdown++ documentation across 8 files described multiline table row separators as "empty rows" or rows that are "empty or contain only whitespace," but the ePublisher parser's actual regex (`^ {0,3}\|(?:[ ]*\|)+[ ]*$`) requires pipe characters to be present. A truly blank line terminates the table entirely. Additionally, multiline headers and the cell content dedent algorithm were completely undocumented.

## Symptoms

- **Misleading terminology:** Files used phrases like "empty row separates records," "empty row with cell borders separates table rows," and "empty separator rows marking cell boundaries" -- all suggesting a blank line could serve as a separator.
- **Silent table truncation risk:** An author inserting a genuinely blank line (no pipes) between rows would unknowingly end their table, producing broken output with no error message.
- **Undiscoverable features:** Multiline headers (continuation rows above the delimiter) and the dedent algorithm (minimum common whitespace stripping from merged cell content) worked in the parser but had zero documentation.
- **Ambiguous conformance requirement:** The processing model's required feature #7 said only "Recognition and processing of `multiline` commands on table elements" with no testable definition of what that entails.

## What Didn't Work

The root problem was the "empty row" terminology that had propagated across 8 files:

- **syntax-reference.md** used "Empty row with cell borders separates table rows" -- "empty row" was misleading and "cell borders" obscured the pipe requirement.
- **SKILL.md** used "empty row separates records" -- even more abbreviated and misleading.
- **best-practices.md** used "Empty row with borders separates table rows."
- **examples.md** used "separated by an empty row with cell borders."
- **whitepaper.md** used "empty separator rows marking cell boundaries."
- **examples/multiline-tables.md** used "Empty separator rows mark cell boundaries."

All shared the same flaw: the word "empty" suggests a blank line, but the parser requires pipe characters. The terminology had drifted from the implementation.

## Solution

Updated 8 documentation/specification files with precise, consistent terminology. Key changes:

**Terminology replacement (applied across all files):**

| Before | After |
|--------|-------|
| "empty row separates records" | "a row with pipes and whitespace-only cells separates rows (a blank line ends the table)" |
| "Empty row with borders separates table rows" | "Row separator: pipes with whitespace-only cells (blank line ends the table)" |
| "empty separator rows marking cell boundaries" | "separator rows (pipes with whitespace-only cells) marking row boundaries. A completely blank line ends the table" |

**syntax-reference.md (canonical source):**

- Row separator definition with the exact regex pattern `^ {0,3}\|(?:[ ]*\|)+[ ]*$`
- Blockquote callout: "A completely blank line (no pipe characters) **ends the table entirely** -- it does not separate rows."
- New "Multiline Headers" subsection with continuation row example
- New "Cell Content Dedent" subsection with before/after whitespace stripping example

**processing-model.md (conformance requirements):**

Required feature #7 expanded from one line to four RFC 2119 sub-requirements:

- (a) Row separator recognition (with pattern)
- (b) Continuation row merging (including headers above delimiter)
- (c) Blank-line termination (blank line ends table, does not separate)
- (d) Cell content dedent (minimum common leading whitespace stripping)

**formal-grammar.md:**

Added prose structural constraint explaining that `multiline_cmd` defines only the directive keyword; row-level behaviors are defined in the processing model.

**Review-phase corrections:**

- Dedent example text: "two leading spaces" corrected to "single leading space" to match the visible example
- Continuation row description clarified to mention empty first cell
- Plan document file count corrected from "seven" to "eight"

## Why This Works

The root cause was **documentation drift from implementation**: the parser's regex was precise about requiring pipe characters, but documentation used colloquial shorthand ("empty row") that did not capture this requirement. The imprecise language propagated across files without anyone noticing the mismatch.

The fix works because:

1. **Single source of truth architecture:** syntax-reference.md contains detailed canonical definitions (with the actual regex pattern), and all other files use corrected short-form terminology that references it. One place to update if parser behavior changes.

2. **Precise terminology eliminates ambiguity:** "A row with pipes and whitespace-only cells" is unambiguous. The explicit warning about blank lines ending the table addresses the most dangerous failure mode.

3. **Normative conformance sub-requirements:** The processing model enumerates exactly what "multiline table processing" means with RFC 2119 MUST language, enabling independent implementers to build conformant processors.

4. **Documenting existing features:** Multiline headers and dedent were working behaviors that authors could not discover or reason about. Examples make the feature self-describing.

## Prevention

- **Parser-documentation parity:** When parser behavior is described in documentation, include the actual regex or algorithm as a reference anchor that can be compared against parser source.

- **Terminology consistency audits:** When updating any cross-cutting feature's documentation, audit all files that reference it. The plan document's audit table listing all affected files with their current language and line numbers is a useful template.

- **Single source of truth discipline:** Detailed behavioral definitions live in one canonical file (syntax-reference.md for syntax, processing-model.md for conformance). Other files use brief summaries that reference the canonical source, limiting the blast radius of drift.

- **Decompose complex conformance features:** The processing model's required features should break complex behaviors into testable sub-requirements. A one-line stub like "Recognition and processing of multiline commands" is not actionable -- the four-part expansion (7a-7d) is.

- **Distinguish terminators from separators:** Any time a format has both an internal separator and a terminator, documentation must explicitly distinguish them. The blank-line-ends-table vs. separator-row-separates-rows distinction is the canonical Markdown++ example.

- **Verify docs against implementation, not against other docs:** The original "empty row" language was self-consistent across all 8 files. Consistency alone is not correctness -- reviews should verify claims against the implementation.

## Related Issues

- [#20](https://github.com/quadralay/markdown-plus-plus/issues/20) -- This issue (multiline table separator pattern)
- [#11](https://github.com/quadralay/markdown-plus-plus/issues/11) -- Formal grammar (multiline table syntax in scope)
- [#24](https://github.com/quadralay/markdown-plus-plus/issues/24) -- Extensions inside multiline table cells (follow-on)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Processing model specification (R7a-d added here)
- `docs/solutions/documentation-gaps/processing-model-specification-2026-04-08.md` -- Processing model spec work that added R7a-d conformance requirements (moderate overlap, complementary scope)
