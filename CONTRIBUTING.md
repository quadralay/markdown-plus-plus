---
date: 2026-04-07
status: active
---

# Contributing to Markdown++

Thank you for your interest in contributing to the Markdown++ open documentation format. This document explains how to report issues, propose changes, and submit pull requests.

## Reporting issues

Open an issue on [GitHub Issues](https://github.com/quadralay/markdown-plus-plus/issues) for:

- **Bug reports** -- Problems with the specification, examples, or tooling. Include the specific section or file affected and what you expected vs. what you found.
- **Spec ambiguities** -- Places where the specification is unclear or could be interpreted multiple ways.
- **Feature requests** -- New extensions or capabilities you'd like to see in the format.

Use descriptive titles and include enough context for maintainers to understand the issue without back-and-forth.

## Proposing spec changes

Markdown++ is a documentation format specification. Changes to the spec affect every implementation and every document authored in the format, so they follow a structured review process.

### Minor changes

Typo fixes, clarifications that don't change behavior, and documentation improvements can go directly through a pull request.

### Substantive changes

Changes that add, modify, or remove format behavior follow this process:

1. **Open an issue** describing the problem and the proposed change. Explain the use case -- why the current spec is insufficient.
2. **Discussion** -- Maintainers and community members discuss the proposal on the issue. This is where scope, backward compatibility, and interaction with existing features are evaluated.
3. **Pull request** -- Once the approach is agreed upon, submit a PR with the spec changes, updated examples, and validation updates as needed.
4. **Review** -- Maintainers review for correctness, backward compatibility, and consistency with the format's design principles.
5. **Merge** -- Approved changes are merged into `main`.

All spec changes must preserve backward compatibility unless they go through the deprecation process defined in [GOVERNANCE.md](GOVERNANCE.md#deprecation-and-breaking-changes).

## Branch and PR conventions

- **Primary branch:** `main`
- **Feature branches** for all PRs -- never commit directly to `main`
- **Branch prefixes:** `feature/`, `fix/`, `docs/`, `refactor/`
- Keep PRs focused on a single change. A spec clarification, a new example, and a tooling fix should be separate PRs.
- Include relevant issue numbers in PR descriptions (e.g., "Fixes #26").

## What to contribute

Contributions are welcome in several areas:

- **Spec clarifications** -- If something in the whitepaper or syntax reference is ambiguous, a clarification PR is valuable.
- **Examples** -- New example files demonstrating Markdown++ features, especially real-world patterns.
- **Tooling** -- Improvements to the validation script, alias generator, or Claude Code skill.
- **Documentation** -- Corrections, improvements, or translations.

## Code of conduct

We expect all participants to be respectful and constructive. Harassment, personal attacks, and unconstructive criticism are not tolerated. Maintainers may remove or edit comments, commits, or contributions that violate these expectations.

For security vulnerabilities, do not open a public issue. Follow the process in [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE) that covers this repository.
