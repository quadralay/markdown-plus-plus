---
title: Spec incorrectly described unrecognized combined command segments as silently discarded
date: 2026-04-11
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - Spec described unrecognized combined command segments as "silently discarded, functioning as inline comments"
  - Six locations across specification.md and formal-grammar.md taught authors incorrect behavior
  - The word "invisible" in specification.md:1024 contradicted PassThrough marker emit semantics
  - syntax-reference.md still used "silently ignored as inline comments" in three places after the initial spec fix
  - Disambiguation sentence at specification.md:771 conflated three distinct cases after the targeted fix
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
related_components:
  - tooling
tags:
  - combined-commands
  - unrecognized-segments
  - passthrough
  - specification
  - formal-grammar
  - syntax-reference
  - implementation-defined
---

# Spec incorrectly described unrecognized combined command segments as silently discarded

## Problem

The Markdown++ specification described unrecognized segments in combined commands (e.g., `<!-- style:Heading ; TODO: add markers -->`) as "silently discarded, functioning as inline comments within the directive." The correct behavior — consistent with the implementation and design intent — is that the disposition of unrecognized segments is **implementation-defined**: processors MUST NOT let them affect CommonMark content processing, but MAY pass them through as HTML comments, inject them as markers, or discard them.

## Symptoms

- `spec/specification.md:214` used the phrase "silently discarded, functioning as inline comments" to describe unrecognized combined command segments.
- `spec/specification.md:1024` used RFC 2119 MUST language instructing processors to "silently ignore" unrecognized segments.
- `spec/specification.md:1024` described unrecognized segment handling as producing "invisible" output — contradicting PassThrough emit semantics, since PassThrough marker values are emitted as-is and are not invisible.
- `spec/formal-grammar.md:137` described unrecognized segments without acknowledging their implementation-defined disposition.
- `spec/formal-grammar.md:168` labeled the segment in the validation table as "one discarded inline comment" instead of "one unrecognized segment (disposition implementation-defined)."
- `spec/formal-grammar.md:415` — PEG comment described the catch-all production as handling "inline comments" rather than unrecognized segments.
- `spec/formal-grammar.md:537` described the edge case as "plus one discarded segment."
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md` — the primary agent-facing reference — described unrecognized segments as "silently ignored as inline comments" in three locations, which would have led AI-assisted authoring guidance to contradict the corrected spec.
- The disambiguation sentence at `spec/specification.md:771` did not distinguish between three distinct cases after the fix, leaving the corrected text ambiguous.

## What Didn't Work

**Initial scope: spec files only (6 locations).** The first fix pass targeted `specification.md` and `formal-grammar.md` and corrected all six identified locations. This was not sufficient because:

- `syntax-reference.md` — the file Claude reads when assisting Markdown++ authors — was not included in the first pass and still carried "silently ignored as inline comments" in three places. Authors getting AI-assisted help would still receive incorrect guidance even after the spec was fixed.
- The word "invisible" at `specification.md:1024` was not caught; it directly contradicted the established PassThrough emit contract (a PassThrough marker value is emitted as-is in the output and is not invisible).
- The disambiguation sentence at `specification.md:771` was not updated after the fix; it did not account for the three distinct cases that now needed distinguishing.

**Initial framing: MUST inject as PassThrough markers.** The original issue described the fix as mandating that processors MUST inject unrecognized segments as PassThrough markers. During implementation this was revised: prescribing a single required disposition was over-constraining. Processors legitimately differ in what they do with unrecognized segments. The correct normative language is that processors MUST NOT let unrecognized segments affect content processing, and their disposition is implementation-defined (MAY pass through as HTML comments, MAY inject as markers, MAY discard).

## Solution

**`spec/specification.md:214`**

Before:
```
Unrecognized segments are silently discarded, functioning as inline comments within the directive.
```

After:
```
Unrecognized segments MUST NOT affect the CommonMark processing of the attached content. The disposition of unrecognized segments is implementation-defined — implementations MAY pass them through as HTML comments, inject them as markers, or discard them. This allows authors to embed metadata (status notes, review flags, tracking info) alongside directives.
```

**`spec/specification.md:771`** (disambiguation sentence)

Updated to distinguish all three distinct PassThrough-related cases:
1. Explicit `Passthrough` marker directive (`<!-- marker:Passthrough="..." -->`)
2. Unrecognized segments in combined commands (section 16.4) — disposition implementation-defined
3. Standalone unrecognized HTML comments (section 5.2) — ignored by the attachment rule

**`spec/specification.md:1024`** (section 16.4)

Before:
```
A processor MUST interpret recognized segments normally and MUST silently ignore unrecognized segments. Unrecognized segments function as invisible inline comments within the directive.
```

After:
```
A processor MUST interpret recognized segments normally. Unrecognized segments MUST NOT affect the CommonMark processing of the attached content. The disposition of unrecognized segments is implementation-defined — implementations MAY pass them through as HTML comments, inject them as markers, or discard them. This allows authors to embed metadata (status notes, review flags, tracking info) alongside directives.
```

**`spec/formal-grammar.md:137`** (Command List section prose)

Before: described unrecognized segments without acknowledging their implementation-defined disposition.

After: "Unrecognized segments MUST NOT affect the CommonMark processing of the attached content. Their disposition is implementation-defined — implementations MAY pass them through as HTML comments, inject them as markers, or discard them."

**`spec/formal-grammar.md:168`** (validation table)

Before: `style:X ; TODO: add markers ; #alias` → "Two commands + one discarded inline comment"

After: → "Two commands + one unrecognized segment (disposition implementation-defined)"

**`spec/formal-grammar.md:415`** (PEG comment)

Before: `# Unrecognized text (catch-all for inline comments)`

After: `# Unrecognized text (catch-all; disposition is implementation-defined)`

**`spec/formal-grammar.md:537`** (edge cases)

Before: "parses as two recognized commands...plus one discarded segment."

After: "The unrecognized segment MUST NOT affect content processing; its disposition is implementation-defined."

**`plugins/.../references/syntax-reference.md`** (three locations in Combined Commands section)

All three locations updated from "silently ignored as inline comments" to the implementation-defined language consistent with the corrected spec.

## Why This Works

The original spec was written without a complete understanding of the design intent behind how unrecognized segments flow through the pipeline. The author treated them as a simple discard mechanism — analogous to HTML comments — rather than recognizing that different implementations legitimately handle them differently.

The key behavioral invariant is narrow and clear: unrecognized segments MUST NOT affect the CommonMark processing of the attached content. What happens to the segment text after that invariant is satisfied is implementation-defined. Some processors may discard it silently; others may expose it as a PassThrough marker for downstream tools; others may emit it as an HTML comment for debugging. All three behaviors are valid.

The "invisible" adjective was an additional error: it was correct only for the discard case and contradicted the PassThrough injection case, where the value is emitted as-is.

The `syntax-reference.md` fix is especially important because it is the primary document Claude reads when assisting Markdown++ authors. A correct spec with an incorrect agent-facing reference would cause AI-assisted guidance to contradict the actual processing behavior.

## Prevention

**When writing spec language for any "unrecognized input" case:**
- Ask explicitly: is this a hard discard, or does the implementation define what happens? Never default to "discard" without verifying against the implementation or a recorded design decision.
- Avoid adjectives like "invisible," "silent," "discarded," and "ignored" without checking whether they accurately describe ALL conformant implementations. These words imply a single required disposition and will contradict any implementation that takes a different valid approach.

**When reviewing spec changes that touch behavior descriptions:**
- Check ALL files that reference the changed behavior. For this repo, any change to combined command behavior must be verified in: `specification.md`, `formal-grammar.md`, AND `syntax-reference.md` at minimum.
- After any targeted fix, re-read the surrounding paragraphs for disambiguation sentences or adjectives that may now be incomplete or contradictory.
- Search for "MUST" statements adjacent to the changed behavior and verify each one is still normatively correct.

**Treating `syntax-reference.md` as a normative artifact:**
- The agent-facing `syntax-reference.md` must be included in any checklist for spec changes affecting authoring behavior — it is the document most likely to produce incorrect author guidance if stale.
- Consider adding explicit cross-reference links in `syntax-reference.md` that point to the governing spec section for each described behavior, so reviewers know which spec location is authoritative.

**When framing a fix, distinguish the invariant from the disposition:**
- Separate the MUST constraint (what processors are forbidden from doing) from the MAY freedom (what processors are permitted to do with the input). Over-prescribing the disposition (e.g., MUST inject as PassThrough markers) produces a spec that is stricter than needed and may not match all valid implementations.
- Run a global search for "discard," "ignored," "inline comment," and "invisible" across all spec files when any unrecognized-input behavior is revised.

## Related Issues

- [quadralay/markdown-plus-plus#70](https://github.com/quadralay/markdown-plus-plus/issues/70) — This issue
- [docs/solutions/documentation-gaps/formal-ebnf-peg-grammar-for-extensions-2026-04-08.md](formal-ebnf-peg-grammar-for-extensions-2026-04-08.md) — Created `spec/formal-grammar.md`; line 37 referenced "unrecognized segments silently discarded" as the then-current prose description (now corrected)
- [docs/solutions/documentation-gaps/combined-commands-conformance-classification-2026-04-10.md](combined-commands-conformance-classification-2026-04-10.md) — Fixed combined commands conformance classification (OPTIONAL → REQUIRED) and RFC 2119 evaluation order language; complementary spec consistency fix
