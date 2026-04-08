---
date: 2026-04-08
status: draft
---

# Format Versioning

## Introduction

This document specifies how Markdown++ documents declare which version of the format specification they target, and how processors handle version mismatches between documents and their supported specification version. It defines the version declaration syntax, compatibility rules, multi-file assembly behavior, and the initial specification version.

The [Processing Model](processing-model.md) defines the two-phase pipeline that governs all Markdown++ processing. Version checking is a preamble step that runs before Phase 1 begins. The processing model registers the diagnostic codes for version mismatches (MDPP015, MDPP016) and describes how the preamble integrates with the existing pipeline.

[GOVERNANCE.md](../GOVERNANCE.md) defines the versioning scheme, release process, backward compatibility guarantees, and deprecation cycle for the Markdown++ specification. This document codifies the technical mechanism by which documents and processors interact with that versioning scheme.

## Scope

This document covers:

- The version declaration syntax for Markdown++ documents
- Compatibility rules for same-major and cross-major version mismatches
- Multi-file assembly behavior for version declarations
- The initial specification version designation

This document does not cover:

- The versioning scheme itself, release process, or deprecation cycle (see [GOVERNANCE.md](../GOVERNANCE.md))
- Tool-specific frontmatter fields beyond `mdpp-version` (e.g., `title`, `author`, `date`)
- Version negotiation protocols between tools in a publishing pipeline
- Migration tooling for updating documents across major versions

## Definitions

**Specification version** -- The version of the Markdown++ format specification, expressed as MAJOR.MINOR.PATCH per [Semantic Versioning 2.0.0](https://semver.org/). The versioning scheme and its semantics are defined in [GOVERNANCE.md](../GOVERNANCE.md). The specification version applies to the format itself, not to any particular tool or implementation.

**Document version declaration** -- A YAML frontmatter field (`mdpp-version`) in a Markdown++ document that declares which specification version the document targets. The declaration uses MAJOR.MINOR format (patch version is omitted because patch releases do not change format behavior).

**Processor supported version** -- The specification version that a processor implements. A processor supporting specification version 1.2.0 can handle all features defined through version 1.2, and is backward compatible with documents targeting any earlier 1.x version.

**Plugin/tooling version** -- The version of a specific tool, plugin, or implementation (e.g., `1.1.5` in `plugin.json`). This is distinct from the specification version. A tool at version 3.0.0 might implement specification version 1.2. The two version tracks are independent.

**Conformance keywords** -- The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt). All conformance statements apply to processors, not to document authors.

## Versioning Scheme

The Markdown++ specification uses [Semantic Versioning 2.0.0](https://semver.org/) with MAJOR.MINOR.PATCH numbering:

- **MAJOR** -- Changes that alter the behavior of existing syntax or remove features. Documents targeting one major version may not be compatible with processors supporting a different major version.
- **MINOR** -- New extensions or features that are backward compatible. Existing documents continue to work unchanged. A processor supporting version 1.2 can process documents targeting 1.0 or 1.1 without loss.
- **PATCH** -- Clarifications, typo fixes, and documentation improvements that do not change format behavior. Patch versions do not affect document compatibility.

The versioning scheme, release process, backward compatibility guarantees, and deprecation cycle are defined in [GOVERNANCE.md](../GOVERNANCE.md). This document does not redefine those rules -- it provides the document-level mechanism for interacting with them.

### Two Version Tracks

The specification version and tool/plugin versions are independent:

| Version Track | What It Identifies | Example |
|---------------|-------------------|---------|
| **Specification version** | The Markdown++ format specification | `1.0`, `1.2`, `2.0` |
| **Tool/plugin version** | A specific implementation or tool | `1.1.5` in `plugin.json` |

A tool at version 5.0 might implement specification version 1.2. A different tool at version 1.0 might also implement specification version 1.2. The specification version describes the format; the tool version describes the implementation.

Document authors declare the **specification version** they target, not any tool version.

## Document-Level Version Declaration

### Syntax

A Markdown++ document MAY declare its target specification version using the `mdpp-version` field in YAML frontmatter:

```yaml
---
mdpp-version: 1.0
date: 2026-04-08
status: active
---
```

The `mdpp-version` field value MUST be a MAJOR.MINOR version string: one or more digits, a period, one or more digits. The patch version is omitted because patch releases do not change format behavior and are irrelevant to document compatibility.

Valid values: `1.0`, `1.2`, `2.0`, `10.3`

Invalid values: `1`, `1.0.0`, `v1.0`, `1.0-beta`, `latest`

### Optional Declaration

The `mdpp-version` field is OPTIONAL. A document without an `mdpp-version` field is valid Markdown++. Omitting the field is not an error and does not produce a diagnostic.

When no `mdpp-version` field is present, a processor MUST process the document without emitting a version-related diagnostic. The document is processed according to the processor's supported specification version.

### Spec-Defined Frontmatter Boundary

The `mdpp-version` field is the only frontmatter field defined by the Markdown++ specification. YAML frontmatter is a document metadata mechanism, not a third extension mechanism alongside HTML comment directives and inline variable tokens.

Other frontmatter fields (e.g., `date`, `status`, `title`, `author`) are conventions used by tools and workflows. They are outside the scope of this specification and are not processed by the Markdown++ extension pipeline.

## Compatibility Rules

### Same-Major Compatibility

Within a major version series, Markdown++ guarantees backward compatibility per [GOVERNANCE.md](../GOVERNANCE.md):

**Document targets same or earlier minor version than processor supports:**

A processor MUST process the document normally with no version-related diagnostic. The processor's supported version is a superset of the document's target version within the same major series.

| Document | Processor | Result |
|----------|-----------|--------|
| `1.0` | `1.0` | Process normally, no diagnostic |
| `1.0` | `1.2` | Process normally, no diagnostic |
| `1.1` | `1.2` | Process normally, no diagnostic |

**Document targets newer minor version than processor supports:**

The document may use features that the processor does not recognize. A processor MUST emit diagnostic **MDPP015** (Warning) and SHOULD continue processing on a best-effort basis. Unrecognized features will pass through as regular HTML comments or literal text, consistent with the invisible extension design.

| Document | Processor | Result |
|----------|-----------|--------|
| `1.2` | `1.0` | Emit MDPP015, process best-effort |
| `1.3` | `1.1` | Emit MDPP015, process best-effort |

Best-effort processing means the processor applies all features it supports and passes through unrecognized extensions per the standard fallback behavior. Because Markdown++ extensions are invisible to standard Markdown renderers, unrecognized features degrade gracefully -- they appear as hidden HTML comments or literal text rather than causing errors.

### Cross-Major Compatibility

When a document targets a different major version than the processor supports, the document may use syntax whose meaning has changed or features that have been removed. A processor MUST emit diagnostic **MDPP016** (Warning).

A processor MAY refuse to process the document after emitting MDPP016. Whether to refuse is a processor-specific decision, not a specification requirement. If the processor continues, it SHOULD process the document on a best-effort basis.

| Document | Processor | Result |
|----------|-----------|--------|
| `2.0` | `1.0` | Emit MDPP016, processor MAY refuse |
| `1.0` | `2.0` | Emit MDPP016, processor MAY refuse |
| `3.1` | `1.2` | Emit MDPP016, processor MAY refuse |

Cross-major mismatches are more significant than minor mismatches because major version increments may change the meaning of existing syntax, not just add new features.

## Multi-File Assembly Behavior

In a multi-file assembly using `<!-- include:path -->` directives, the **root document's** `mdpp-version` declaration is authoritative. A processor MUST use the root document's version declaration for version checking.

Included files MAY contain `mdpp-version` fields in their frontmatter. These declarations are informational -- they indicate what version the included file was authored against. A processor MUST NOT use an included file's `mdpp-version` to override or conflict with the root document's declaration.

A processor SHOULD NOT emit version diagnostics (MDPP015, MDPP016) based on included files' `mdpp-version` declarations. Version checking applies to the root document only.

**Rationale:** Multi-file assemblies combine files that may have been authored at different times and may carry different `mdpp-version` values. Using the root document as the single source of truth avoids version conflict resolution across the include tree. Authors who assemble files into a publication take responsibility for compatibility at the root level.

### Example: Multi-File Assembly

Root document (`user-guide.md`):

```yaml
---
mdpp-version: 1.0
---
```

```markdown
# User Guide

<!-- include:chapters/overview.md -->
<!-- include:chapters/configuration.md -->
```

Included file (`chapters/overview.md`):

```yaml
---
mdpp-version: 1.2
date: 2026-04-01
---
```

```markdown
## Overview

This chapter was authored against spec version 1.2.
```

The processor uses `mdpp-version: 1.0` from the root document for version checking. The `mdpp-version: 1.2` in the included file is informational and does not trigger diagnostics.

## Initial Version

The initial Markdown++ specification version is **1.0**. All spec documents in this repository at the time of this designation constitute the 1.0 specification.

Documents authored against the current specification SHOULD declare `mdpp-version: 1.0`:

```yaml
---
mdpp-version: 1.0
---
```

## CommonMark Interchangeability

YAML frontmatter (including the `mdpp-version` field) is handled by most Markdown renderers -- either parsed and hidden, or displayed as a simple text block. Adding `mdpp-version` to frontmatter does not change how the document renders in standard Markdown viewers.

The `mdpp-version` field preserves the Markdown++ interchangeability guarantee: Markdown++ files remain valid CommonMark documents that render cleanly in GitHub, VS Code, MkDocs, and any other Markdown tool.

## Worked Examples

### Example 1: Exact Version Match

A document targeting 1.0 processed by a processor supporting 1.0:

```yaml
---
mdpp-version: 1.0
---
```

The processor compares document version 1.0 against its supported version 1.0. The versions match. No diagnostic is emitted. Processing continues normally.

### Example 2: No Version Declaration

A document without an `mdpp-version` field:

```yaml
---
date: 2026-04-08
status: active
---
```

The processor finds no `mdpp-version` field. No version check is performed. No diagnostic is emitted. The document is processed according to the processor's supported specification version.

### Example 3: Minor Version Ahead (MDPP015)

A document targeting 1.2 processed by a processor supporting 1.0:

```yaml
---
mdpp-version: 1.2
---
```

The processor compares document version 1.2 against its supported version 1.0. Same major version (1), but the document's minor version (2) exceeds the processor's minor version (0). The processor emits:

```
MDPP015 Warning: Document targets newer minor version than processor supports
  Document version: 1.2
  Processor version: 1.0
```

Processing continues on a best-effort basis. Features introduced in 1.1 and 1.2 that the processor does not recognize pass through as hidden HTML comments or literal text.

### Example 4: Major Version Mismatch (MDPP016)

A document targeting 2.0 processed by a processor supporting 1.2:

```yaml
---
mdpp-version: 2.0
---
```

The processor compares document version 2.0 against its supported version 1.2. Different major versions (2 vs. 1). The processor emits:

```
MDPP016 Warning: Document targets different major version than processor supports
  Document version: 2.0
  Processor version: 1.2
```

The processor MAY refuse to continue processing. If it continues, it processes on a best-effort basis, but results may be incorrect because major version changes can alter the meaning of existing syntax.

## Conformance

### Processor Requirements

A conformant processor that implements version checking MUST:

1. Extract the `mdpp-version` field from the root document's YAML frontmatter, if present.
2. Parse the field value as a MAJOR.MINOR version string.
3. Compare the document's declared version against the processor's supported specification version.
4. Emit **MDPP015** when the document targets a newer minor version within the same major series.
5. Emit **MDPP016** when the document targets a different major version.
6. Not emit version-related diagnostics when the `mdpp-version` field is absent.
7. Use the root document's `mdpp-version` as authoritative in multi-file assemblies.

### Optional Feature

Version checking is an OPTIONAL feature for conformance purposes. A conformant processor is not required to implement version checking. However, a processor that does implement version checking MUST follow the rules defined in this document.

A processor that does not implement version checking simply ignores the `mdpp-version` frontmatter field, which is consistent with the general treatment of frontmatter as tool-specific metadata.

### Relationship to Other Specifications

This specification does not introduce a new processing phase. Version checking is a preamble step described in the [Processing Model](processing-model.md) that runs before the two-phase pipeline begins.

The [Formal Grammar](formal-grammar.md) covers Markdown++ extension constructs (HTML comment directives and inline variable tokens). YAML frontmatter, including `mdpp-version`, is document metadata outside the grammar's scope.

## References

- [GOVERNANCE.md](../GOVERNANCE.md) -- Versioning scheme, release process, backward compatibility guarantees, deprecation cycle
- [Processing Model](processing-model.md) -- Two-phase pipeline, version check preamble, MDPP015/MDPP016 diagnostic codes
- [Formal Grammar](formal-grammar.md) -- Scope note on frontmatter exclusion
- [Semantic Versioning 2.0.0](https://semver.org/) -- Versioning scheme
- [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) -- Conformance keywords
- [CommonMark 0.30](https://spec.commonmark.org/0.30/) -- Base document format
