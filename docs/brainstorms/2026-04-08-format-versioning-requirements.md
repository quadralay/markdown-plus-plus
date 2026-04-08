---
date: 2026-04-08
topic: format-versioning
---

# Format Versioning Mechanism for Markdown++ Documents

## Problem Frame

Markdown++ has no document-level version identifier. An individual `.md` file cannot declare which version of the Markdown++ specification it targets, and processors have no mechanism to detect version mismatches. This creates three concrete problems:

1. **Forward compatibility risk.** When the spec adds new extensions in a future minor version, a processor supporting only an earlier version has no way to know the document expects features it cannot handle. Failures are silent — unrecognized directives pass through as HTML comments, producing subtly wrong output rather than clear errors.

2. **Enterprise adoption barrier.** Organizations evaluating Markdown++ for long-term use need assurance that their documents will remain valid as the format evolves. Without version declarations, there is no contract between document and processor.

3. **Tooling interoperability.** When multiple tools process Markdown++ documents, version declarations let each tool determine whether it can handle a given document, enabling clear capability negotiation rather than best-effort guessing.

Mature formats solve this: CommonMark declares version 0.30, DITA uses `@ditaversion`, DocBook uses `version` attributes. Markdown++ needs an equivalent mechanism appropriate to its design principles.

## Requirements

- R1. **Spec versioning scheme.** The Markdown++ specification MUST use semantic versioning (MAJOR.MINOR.PATCH) as already defined in GOVERNANCE.md. This requirement codifies the existing governance decision within the spec itself, not just the governance document.

- R2. **Document-level version declaration.** A Markdown++ document SHOULD be able to declare its target spec version using a YAML frontmatter field: `mdpp-version: MAJOR.MINOR`. Only MAJOR.MINOR is declared (not PATCH), because patch releases do not change format behavior.

- R3. **Version declaration is optional.** Documents without an `mdpp-version` field remain valid Markdown++ documents. A processor encountering a document with no version declaration MUST process it using the processor's default behavior and SHOULD NOT treat the absence as an error.

- R4. **Frontmatter is metadata, not a content extension.** The `mdpp-version` field is the only YAML frontmatter field that the Markdown++ specification defines. It does not establish frontmatter as a third extension mechanism alongside HTML comment directives and inline tokens. Other frontmatter fields (e.g., `title`, `date`, `author`) are outside the scope of the Markdown++ spec and remain tool-specific conventions.

- R5. **Same-major compatibility.** Within a major version series, backward compatibility is guaranteed. A processor supporting spec version 1.x MUST correctly process any document declaring `mdpp-version: 1.y` where y ≤ x. A document declaring a higher minor version (y > x) MAY use extensions the processor does not recognize; the processor SHOULD process the document on a best-effort basis (unrecognized directives are invisible HTML comments per CommonMark) and SHOULD emit a diagnostic noting the version mismatch.

- R6. **Cross-major compatibility.** When a processor encounters a document declaring a major version it does not support, the processor SHOULD emit a warning and MAY refuse to process the document. Major version boundaries indicate potential breaking changes where directive semantics may have changed.

- R7. **Initial version number.** The first formal release of the Markdown++ specification MUST be designated version `1.0`. Documents authored against the current (pre-release) spec may retroactively add `mdpp-version: 1.0` once the spec is finalized.

- R8. **Spec document integration.** The versioning mechanism MUST be documented in the specification itself (not only in GOVERNANCE.md). This means adding a versioning section to the whitepaper or a dedicated spec document, and extending the formal grammar to recognize the frontmatter field.

## Success Criteria

- A document author can declare `mdpp-version: 1.0` in YAML frontmatter, and a conformant processor can read and act on that declaration.
- A processor encountering a document with no `mdpp-version` field processes it without error.
- A processor encountering a document with a newer minor version than it supports emits a diagnostic but still produces output.
- A processor encountering a document with a different major version emits a clear warning.
- The versioning mechanism is consistent with the invisible-extension principle: YAML frontmatter is handled by most Markdown renderers (hidden or parsed), so the version declaration does not degrade the CommonMark preview experience.

## Scope Boundaries

- **In scope:** Version declaration syntax, processor behavior for version mismatches, initial version assignment, spec document updates.
- **Out of scope:** Tool-specific frontmatter fields beyond `mdpp-version`. The spec does not define `title`, `author`, `date`, or any other metadata fields — those remain tool conventions.
- **Out of scope:** Version negotiation protocols between tools. How a publishing pipeline selects processor versions is an implementation concern.
- **Out of scope:** Migration tooling for updating documents from one major version to another. That is a tool concern, not a spec concern.
- **Not changing:** The existing GOVERNANCE.md versioning scheme (SemVer), backward compatibility guarantees, and deprecation process. This work codifies those decisions in the spec and adds the document-level declaration mechanism.

## Key Decisions

- **YAML frontmatter over HTML comment directive:** Version is document metadata, not a content processing directive. YAML frontmatter is the ecosystem standard for Markdown document metadata (Hugo, Jekyll, Pandoc, MkDocs, Docusaurus all use it). Using an HTML comment (`<!-- mdpp-version: 1.0 -->`) would be consistent with other extensions but would blur the line between metadata and content directives. Frontmatter is the right home for document-level metadata.

- **MAJOR.MINOR only in document declarations:** Patch versions don't change format behavior (they cover clarifications and typo fixes per GOVERNANCE.md), so including PATCH in document declarations would add noise without value. A document targeting `1.0` works identically with any `1.0.x` processor.

- **Optional, not required:** Making version declarations mandatory would break every existing document and create friction for casual authors. The pragmatic default is: no version field means the processor uses its own defaults. Formal environments (enterprise, CI pipelines) can enforce version declarations through tooling or style guides.

- **Single defined field:** Defining `mdpp-version` as the only spec-defined frontmatter field prevents scope creep. The spec stays focused on its core concern (format versioning) without expanding into general document metadata, which varies by tool and workflow.

## Dependencies / Assumptions

- GOVERNANCE.md already defines SemVer for the spec, backward compatibility guarantees, and the deprecation process. This work builds on those decisions.
- The formal grammar (spec/formal-grammar.md) will need a new production for the frontmatter version field, or an explicit note that frontmatter is outside the grammar's scope (since it is metadata, not a content extension).
- The processing model (spec/processing-model.md) may need a "Phase 0" or preamble step for version checking before the existing two-phase pipeline begins.

## Outstanding Questions

### Deferred to Planning

- [Affects R8][Technical] Should the formal grammar include an EBNF production for the `mdpp-version` frontmatter field, or should it explicitly note that frontmatter metadata is outside its scope (since the grammar covers content extensions only)?
- [Affects R8][Technical] Where in the spec hierarchy should the versioning section live — as a new section in the whitepaper, a new standalone spec document (`spec/versioning.md`), or integrated into the processing model as a preamble phase?
- [Affects R5][Needs research] Should the spec define specific MDPP diagnostic codes for version mismatch warnings (extending the existing MDPP code registry), or leave diagnostic formatting to implementations?

## Next Steps

→ `/ce:plan` for structured implementation planning
