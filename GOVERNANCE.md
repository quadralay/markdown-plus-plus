---
date: 2026-04-07
status: active
---

# Governance

This document describes how the Markdown++ specification is maintained, how changes are proposed and accepted, and how the format evolves over time.

## Maintainership

Markdown++ is maintained by [Quadralay Corporation](https://github.com/quadralay), the organization that created the format. Quadralay maintainers have final decision authority on specification changes.

### Path to multi-stakeholder governance

As adoption grows, governance will expand to include additional stakeholders:

1. **Current phase: Single maintainer.** Quadralay maintains the spec, reviews all proposals, and makes final decisions. Community input is welcomed through GitHub issues and pull requests.
2. **Advisory contributors.** Active contributors who demonstrate sustained, high-quality engagement may be invited as advisory contributors with review authority on pull requests.
3. **Steering group.** If multiple organizations adopt Markdown++ as a primary documentation format, a steering group may be formed to share decision authority over spec changes. The criteria and process for this transition will be documented when it becomes relevant.

## Decision-making process

### Proposal

All substantive changes begin as a GitHub issue. The issue must describe:

- The problem or gap in the current specification
- The proposed solution
- The impact on backward compatibility
- Any interaction with existing features

### Review

Maintainers evaluate proposals against these criteria:

- **Backward compatibility** -- Does the change preserve existing documents? Markdown++ files authored before the change must continue to work as expected.
- **Invisible extension principle** -- Does the change use HTML comments or inline tokens that are invisible to standard Markdown renderers? Changes that break CommonMark compatibility will not be accepted.
- **Simplicity** -- Does the change add the minimum necessary complexity? Markdown++ favors fewer, composable features over many specialized ones.
- **Real-world need** -- Is the feature driven by actual documentation requirements, not theoretical use cases?

### Acceptance

Maintainers merge approved changes into `main`. All spec changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## Spec versioning

The Markdown++ specification uses [Semantic Versioning](https://semver.org/):

- **Patch** (1.0.x) -- Clarifications, typo fixes, and documentation improvements that don't change format behavior.
- **Minor** (1.x.0) -- New extensions or features that are backward compatible. Existing documents continue to work unchanged.
- **Major** (x.0.0) -- Changes that alter the behavior of existing syntax or remove features. These require a deprecation cycle.

### Version release process

1. Changes accumulate on `main` and are tracked in the `[Unreleased]` section of the changelog.
2. When a release is warranted, a maintainer runs the version bump script (`scripts/bump-version.sh`) and updates the changelog with a release date.
3. The release is tagged in Git and noted in the changelog.

### Backward compatibility guarantees

- **Patch and minor releases** will not change the meaning of existing Markdown++ syntax. Documents authored against a previous version in the same major series will produce the same output.
- **Processing tools** should specify which spec version they support. A tool supporting "Markdown++ 1.x" must correctly handle all features in any 1.x release.

## Deprecation and breaking changes

Breaking changes -- those that alter the behavior of existing syntax or remove features -- follow a deprecation cycle:

1. **Deprecation notice.** The feature is marked as deprecated in the specification and changelog. The deprecation notice includes the reason, the recommended alternative, and the target major version for removal.
2. **Deprecation period.** The deprecated feature continues to work for at least one full minor release cycle. Processing tools should emit warnings for deprecated syntax during this period.
3. **Removal.** The feature is removed in the next major version. The removal is documented in the changelog with migration guidance.

This process ensures that authors and tool implementers have time to adapt before breaking changes take effect.

## Relationship between spec and implementations

Markdown++ is an open documentation format. The specification defines the syntax and its semantics. Implementations (publishing tools, editors, validators) interpret the specification independently.

- **The spec is authoritative.** When an implementation's behavior conflicts with the specification, the specification is correct.
- **Vendor extensions are separate.** Tool vendors may add proprietary extensions beyond the Markdown++ specification. These must not use the `<!-- command: -->` syntax reserved by the spec. Vendor extensions should be clearly documented as non-standard.
- **Conformance is per-feature.** An implementation may support a subset of the specification. It should document which features it supports and which spec version it targets.
- **Test files are informative.** The example and test files in this repository demonstrate expected behavior but are not a formal conformance test suite (yet).

## Amendments to this document

This governance document may be updated through the same pull request process as any other change to the repository. Substantive changes to governance (e.g., expanding decision authority) will be discussed in a GitHub issue before implementation.
