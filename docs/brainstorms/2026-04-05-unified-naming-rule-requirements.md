---
date: 2026-04-05
topic: unified-naming-rule
---

# Unified Naming Rule for All Markdown++ Name Types

## Problem Frame

The Markdown++ specification documents naming rules inconsistently across extension types. Each name type section in `syntax-reference.md` states "Alphanumeric, hyphens, underscores" without specifying start-character requirements. The validation script (`validate-mdpp.py`) enforces the correct pattern for variables and conditions but has gaps: aliases allow digit-first names, and styles/marker keys have no name validation at all.

This inconsistency creates ambiguity for parser implementors and risks divergent behavior across tools.

## Requirements

- R1. Define one naming rule in `syntax-reference.md` and reference it from each extension section (variables, conditions, styles, aliases, marker keys) instead of repeating partial rules
- R2. The unified rule is: first character must be a letter or underscore; subsequent characters may be letters, digits, hyphens, or underscores. Regex: `[a-zA-Z_][a-zA-Z0-9_\-]*`. **Exception:** Alias names may also begin with a digit (`[a-zA-Z0-9_][a-zA-Z0-9_\-]*`), since aliases often map to numeric identifiers (e.g., `#04499224`)
- R3. Update the validation script so MDPP002 applies to all five name types. Variables, conditions, styles, and marker keys use the standard regex. Aliases use the digit-first-allowed variant. Currently missing: style name validation, marker key validation
- R4. Verify no existing examples or whitepaper content violates the rule (audit complete: no violations found)
- R5. Marker *values* (e.g., index entry text, keyword lists) are explicitly excluded from this rule -- they are free-form content with their own syntax (colons for nesting, commas for separators)

## Success Criteria

- A single "Naming Rules" or "Identifier Grammar" section exists in `syntax-reference.md` with the definitive rule
- Each extension section references that shared rule instead of stating its own partial version
- `validate-mdpp.py` enforces the standard regex for variables, conditions, styles, and marker keys, and the digit-first-allowed variant for aliases
- All existing examples and whitepaper content pass validation without changes

## Scope Boundaries

- Parser-side regex changes in the ePublisher adapter are tracked in issue #27 (separate repo)
- Formal grammar production (`identifier`) is tracked in issue #11
- MDPP002 error code documentation is tracked in issue #14
- No new error codes are introduced here; R3 extends existing MDPP002 coverage

## Key Decisions

- **Single shared section over per-extension rules:** Reduces drift and makes the spec easier to maintain. Each extension section will say "Names follow the [unified naming rule](#naming-rules)" rather than restating constraints.
- **Alias digit-first exception:** Aliases may begin with a digit because they often reference numeric identifiers (e.g., `#04499224` for a topic ID or build number). All other name types require a letter or underscore first.
- **Marker values excluded:** Values like `"IPsec: peering connections"` are free-form text, not identifiers. The naming rule applies only to keys.
- **Non-English note:** The structural rule (letter-first, then letters/digits/hyphens/underscores) applies using the language's UTF-8 letter values for non-English content. This is stated in the spec but not enforced in `validate-mdpp.py` (ASCII-only validation is acceptable for the current tooling).

## Deferred to Planning

- [Affects R3][Technical] Exact placement and wording of the shared naming rule section in `syntax-reference.md`
- [Affects R3][Technical] Whether style name validation should extract the name from `style:NAME` or validate inline with the tag pattern
- [Affects R1][Technical] How to cross-reference the shared rule from each extension section (anchor link vs. repeated one-liner)

## Next Steps

-> `/ce:plan` for structured implementation planning
