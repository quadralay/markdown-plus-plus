---
title: Format versioning mechanism for Markdown++ specification
date: 2026-04-08
category: documentation-gaps
module: spec
problem_type: documentation_gap
component: documentation
symptoms:
  - "No way for documents to declare which Markdown++ version they target"
  - "No mechanism for processors to detect or handle version mismatches"
  - "Enterprise adoption blocked by lack of format versioning"
  - "No diagnostic codes for version-related warnings or errors"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: high
tags:
  - versioning
  - specification
  - frontmatter
  - mdpp-version
  - processing-model
  - enterprise-adoption
---

# Format versioning mechanism for Markdown++ specification

## Problem

The Markdown++ specification lacked a format versioning mechanism. Documents had no way to declare which spec version they target, and processors had no way to detect version mismatches -- blocking enterprise adoption where format stability guarantees are essential.

## Symptoms

- No document-level declaration of which Markdown++ spec version a document was authored against
- Processors could not warn authors when a document targets a newer or incompatible spec version
- GOVERNANCE.md defined SemVer and compatibility promises at the project level, but no technical mechanism bridged that policy to individual documents
- Organizations evaluating Markdown++ for enterprise use had no answer to "how do we know our documents will remain valid as the format evolves?"
- Multi-file assemblies had no defined authority for which version governs the whole assembly
- Mature peer formats (CommonMark 0.30, DITA `@ditaversion`, DocBook `version`) all had this capability; Markdown++ did not

## What Didn't Work

- **Making version declaration required** -- Rejected because Markdown++ already treats YAML frontmatter as optional. Forcing a required field would break the format's existing optional-frontmatter convention and penalize simple single-file documents that don't need versioning.
- **Adding frontmatter as a grammar production in `formal-grammar.md`** -- Rejected because YAML frontmatter is metadata, not an extension construct. Including it in the formal grammar would conflate two concerns and complicate the grammar for no parsing benefit.
- **Embedding versioning rules inside `processing-model.md` as a new phase** -- Rejected in favor of a standalone `spec/versioning.md` document, following the repository's one-concern-per-spec-document pattern. Version checking was added as a "Preamble" step rather than a numbered phase, keeping the processing model's phase structure intact.
- **Using full MAJOR.MINOR.PATCH in document declarations** -- Rejected because patch-level changes do not alter format behavior. Including patch numbers would create false mismatch warnings with no benefit.

## Solution

Created a versioning mechanism spanning six areas of the spec and tooling:

**Core specification (`spec/versioning.md`):** Defines `mdpp-version: MAJOR.MINOR` as a YAML frontmatter field -- the only spec-defined frontmatter field. Declaration is optional; omission is not an error. Same-major compatibility means documents are backward-compatible within a major series (processor emits MDPP015 warning for newer minor versions). Cross-major triggers MDPP016 warning and the processor MAY refuse. For multi-file assemblies, the root document's declaration is authoritative. Malformed values are treated as absent. Initial spec version is 1.0.

**Processing model (`spec/processing-model.md`):** Added a "Preamble: Version Check" step before Phase 1. Registered two diagnostics -- MDPP015 (minor version mismatch, Warning) and MDPP016 (major version mismatch, Warning). Updated the introduction to list versioning in the normative document set. Scoped diagnostic requirements to features the processor actually implements, resolving a contradiction with version checking being optional.

**Formal grammar (`spec/formal-grammar.md`):** Added a scope note clarifying YAML frontmatter is outside the grammar, and added frontmatter to the "does not define" conformance list.

**Whitepaper (`spec/whitepaper.md`):** Added a non-normative "Format versioning" section with rationale and cross-references.

**Tooling and examples:** Added "Version Declaration" to the syntax reference. Added `mdpp-version: 1.0` to all five example files and to the SKILL.md Quick Reference. Added cross-references in GOVERNANCE.md and a CHANGELOG.md entry.

**Review fixes:** Corrected processing-model.md so required feature #10 and conformance text properly scope diagnostic requirements to implemented features only. Added explicit behavior for malformed `mdpp-version` values in versioning.md. Updated SKILL.md Quick Reference.

## Why This Works

The root cause was a gap between governance policy (SemVer promises in GOVERNANCE.md) and technical mechanism (no document-level declaration or processor behavior rules). The solution bridges that gap with a concrete, spec-defined field and registered diagnostics.

The design follows Markdown++ principles: `mdpp-version` in YAML frontmatter is invisible to standard Markdown renderers, preserving CommonMark interchangeability. The mechanism separates spec version from tool version (two independent versioning tracks), uses the existing frontmatter convention rather than inventing new syntax, and makes version checking optional for conformance -- so lightweight processors can ignore it while enterprise toolchains can enforce it. Root-document authority for multi-file assemblies avoids conflict resolution complexity when included files declare different versions.

## Prevention

- **Pair every governance policy with a technical mechanism.** When GOVERNANCE.md defines compatibility guarantees, a corresponding spec document should define the syntax and processor behavior that enforce those guarantees. Treat governance commitments as requirements that need spec coverage.
- **Maintain a spec coverage checklist.** Each normative concept (extensions, versioning, conformance, processing) should map to exactly one spec document. Review the checklist when adding new governance or compatibility promises.
- **Use the diagnostic registry as a forcing function.** If a new feature implies processors should warn or error, register the MDPP codes in `processing-model.md` at the same time. The act of writing diagnostic definitions surfaces missing behavioral specifications.
- **Apply the "enterprise adoption" lens during spec review.** Before marking a spec area as complete, ask: "Can an organization pin their documents to a specific version and get predictable behavior?" If not, the mechanism is incomplete.
- **Follow the one-concern-per-document pattern consistently.** When a new cross-cutting concern emerges (like versioning), give it its own spec document immediately rather than scattering rules across existing documents.

## Related Issues

- [#25](https://github.com/quadralay/markdown-plus-plus/issues/25) -- Define format versioning mechanism (this issue)
- [#7](https://github.com/quadralay/markdown-plus-plus/issues/7) -- Write a formal Markdown++ specification (versioning is a major section)
- [#14](https://github.com/quadralay/markdown-plus-plus/issues/14) -- Standalone error code reference (MDPP range now extends to MDPP016)
- [#8](https://github.com/quadralay/markdown-plus-plus/issues/8) -- Define the processing model (versioning extends it with preamble step)
- [#11](https://github.com/quadralay/markdown-plus-plus/issues/11) -- Create formal grammar (versioning added frontmatter scope note)
- Related learning: [processing-model-specification-2026-04-08.md](processing-model-specification-2026-04-08.md) -- Processing model spec (now extended with MDPP015/016 and version check preamble; note: that doc's references to "MDPP000-013" and "2 optional features" are now stale)
- Related learning: [formal-ebnf-peg-grammar-for-extensions-2026-04-08.md](formal-ebnf-peg-grammar-for-extensions-2026-04-08.md) -- Grammar spec (now includes frontmatter scope note)
- Related learning: [cross-file-link-resolution-semantics-2026-04-08.md](cross-file-link-resolution-semantics-2026-04-08.md) -- Cross-file link resolution (MDPP014 precedent; range now extends to MDPP016)
