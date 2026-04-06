---
title: "feat: Unified naming rule for all Markdown++ name types"
type: feat
status: active
date: 2026-04-06
origin: docs/brainstorms/2026-04-05-unified-naming-rule-requirements.md
---

# feat: Unified naming rule for all Markdown++ name types

## Overview

Define a single naming grammar for all Markdown++ named entities and enforce it consistently in both the specification and validation tooling. Currently each extension section states its own partial rules, and the validator only checks variable and condition names. This change consolidates the rule into one shared section, cross-references it from every extension, and extends MDPP002 validation to cover style names, alias names, and marker key names.

## Problem Frame

The Markdown++ specification documents naming rules inconsistently across extension types. Each section independently states "Alphanumeric, hyphens, underscores" without specifying start-character requirements. The validation script (`validate-mdpp.py`) enforces the correct pattern for variables and conditions but has gaps: styles and marker keys have no name validation at all, and aliases allow digit-first names via the regex pattern but lack an explicit format check. This inconsistency creates ambiguity for parser implementors and risks divergent behavior across tools. (see origin: `docs/brainstorms/2026-04-05-unified-naming-rule-requirements.md`)

## Requirements Trace

- R1. Define one naming rule in `syntax-reference.md` and reference it from each extension section
- R2. Unified rule regex: `[a-zA-Z_][a-zA-Z0-9_\-]*`. **Exception:** Alias names may begin with a digit: `[a-zA-Z0-9_][a-zA-Z0-9_\-]*`
- R3. Extend MDPP002 in `validate-mdpp.py` to cover all five name types (standard regex for variables, conditions, styles, marker keys; digit-first variant for aliases)
- R4. Verify no existing examples or whitepaper content violates the rule (audit complete: no violations found)
- R5. Marker *values* are excluded from this rule -- they are free-form content

## Scope Boundaries

- Parser-side regex changes in the ePublisher adapter: issue #27 (separate repo)
- Formal grammar production (`identifier`): issue #11
- MDPP002 error code documentation: issue #14
- No new error codes introduced; this extends existing MDPP002 coverage

## Context & Research

### Relevant Code and Patterns

- `syntax-reference.md` lines 14-49: "Attachment Rules" section -- precedent for a shared rule section defined once and cross-referenced by multiple extension sections
- `syntax-reference.md` lines 61-70: Per-extension "Rules" tables that independently state "Alphanumeric, hyphens, underscores"
- `validate-mdpp.py` lines 61-72: `PATTERNS` dict with compiled regexes for each extension type
- `validate-mdpp.py` lines 75-77: `validate_variable_name()` -- already uses the correct regex `^[a-zA-Z_][a-zA-Z0-9_-]*$`
- `validate-mdpp.py` lines 80-104: `validate_condition_expression()` -- uses the same regex after splitting on operators, reports as MDPP007
- `validate-mdpp.py` lines 205-309: Main validation loop -- processes variables, conditions, markers JSON, includes, and aliases but lacks style name and marker key name validation
- `tests/sample-orphaned-tags.md`: Test file pattern with POSITIVE CASES / NEGATIVE CASES sections and numbered cases

### Existing Name Conventions in Content

| Entity type | Convention | Examples |
|---|---|---|
| Variable | `snake_case` / `kebab-case` | `$product_name;`, `$release-date;` |
| Style | `PascalCase` | `CustomHeading`, `BQ_Warning`, `NoteBlock` |
| Alias | `kebab-case` / numeric | `#introduction`, `#316492` |
| Condition | `lowercase` | `web`, `print`, `!draft` |
| Marker key | `PascalCase` | `Keywords`, `IndexMarker`, `Author` |

All existing names in examples, tests, and the whitepaper comply with the unified rule. Numeric aliases (e.g., `#316492`) require the alias digit-first exception.

## Key Technical Decisions

- **Shared section placement:** Insert a "Naming Rules" section immediately after "Attachment Rules" (after line 50) and before "Variables" (line 52). This follows the established pattern where "Attachment Rules" is a shared rule section referenced by multiple extension sections.
- **Cross-reference style:** Each extension's Rules table replaces the "Characters" / "Name" row with a reference: `"Must follow [Naming Rules](#naming-rules)"`. Keeps each section scannable while eliminating drift.
- **MDPP002 for all name types:** Extend the existing MDPP002 error code rather than introducing new codes. The error message will identify which entity type has the invalid name (e.g., "Invalid style name: ..." vs. "Invalid variable name: ..."). This is consistent with MDPP002's purpose ("invalid name") and avoids error code proliferation.
- **Condition names stay on MDPP007:** `validate_condition_expression()` already reports invalid condition names under MDPP007 ("Invalid condition syntax"). Since the condition check also validates expression structure (operators, empty expressions), it makes sense to keep it as MDPP007 rather than splitting into MDPP002 + MDPP007. The naming rule is already correct there.
- **Style name extraction:** The existing `style` regex captures with `([^->]+?)`. The validator will strip whitespace from the captured group and validate the trimmed name. No regex change needed for the capture pattern.
- **Marker key extraction for simple format:** The `marker_simple` pattern captures `([^=]+)` for the key. Trim and validate the captured key name.
- **Marker key extraction for JSON format:** Parse the JSON (already done for MDPP003), then validate each key against the naming rule. This reuses the existing JSON parse result.
- **Alias regex pattern update:** The current `alias` pattern uses `[a-zA-Z0-9_-]+` which is close to the digit-first-allowed variant but missing the underscore-first and structural rule. Add a `validate_alias_name()` function using `^[a-zA-Z0-9_][a-zA-Z0-9_-]*$` and call it during the existing alias duplicate-check loop.

## Open Questions

### Resolved During Planning

- **Where to place the shared section?** After "Attachment Rules", before "Variables". This is the natural location following the precedent of shared rule sections at the top of the reference.
- **How to cross-reference from each extension section?** Replace the "Characters"/"Name" row in each Rules table with a link to the shared section anchor. Keeps each section self-contained enough to read standalone while deferring the authoritative definition.
- **Should style name extraction change the regex?** No. The capture group `([^->]+?)` is intentionally permissive to catch invalid names for error reporting. Validation happens after extraction, not in the pattern.

### Deferred to Implementation

- Exact wording of the shared "Naming Rules" section prose (editorial, will finalize during writing)
- Whether `validate_condition_expression()` error message should additionally mention the naming rule section (minor UX polish)

## Implementation Units

- [ ] **Unit 1: Add shared "Naming Rules" section to syntax-reference.md**

  **Goal:** Create the authoritative naming rule definition in one place

  **Requirements:** R1, R2

  **Dependencies:** None

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

  **Approach:**
  - Insert a new `## Naming Rules` section after "Attachment Rules" (after line 50, before the `---` and `## Variables`)
  - Document the standard rule with regex: `[a-zA-Z_][a-zA-Z0-9_\-]*`
  - Document the alias exception with regex: `[a-zA-Z0-9_][a-zA-Z0-9_\-]*`
  - Include a brief rationale for why aliases allow digit-first (numeric identifiers)
  - Include the non-English note: structural rule applies using the language's UTF-8 letter values
  - Add valid/invalid examples to make the rule concrete

  **Patterns to follow:**
  - "Attachment Rules" section structure (shared rule, referenced by multiple extensions)

  **Verification:**
  - A `## Naming Rules` section exists with the `#naming-rules` anchor
  - Both the standard and alias-exception regexes are documented
  - The section is self-contained (a reader can understand the rule without jumping elsewhere)

- [ ] **Unit 2: Update extension sections to cross-reference the shared rule**

  **Goal:** Replace per-extension naming rules with references to the shared section

  **Requirements:** R1

  **Dependencies:** Unit 1

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

  **Approach:**
  - **Variables section** (line 62-70): Replace the "Name" row in the Rules table with a reference to `[Naming Rules](#naming-rules)`. Keep the Start (`$`), End (`;`), Spaces, Case, Length, and Escaping rows.
  - **Custom Styles section** (line 183-190): Replace the "Characters" row in Style Name Rules table with a reference. Keep Spaces and Case rows.
  - **Custom Aliases section** (line 201-208): Replace the "Name" row in Rules table with a reference that notes the digit-first exception. Keep Start (`#`), Spaces, and Case rows.
  - **Conditions section** (line 271-278): Replace the "Characters" row in Condition Name Rules table with a reference. Keep Spaces, Commas, and Case rows.
  - **Markers section**: There is no explicit "Marker Key Rules" table currently. Add a brief note in the "Simple Format Rules" area that marker key names follow the naming rule.
  - Update the "Invalid Examples" under Variables (line 88): Change the comment on `$123start;` from "(recommended)" to a definitive statement referencing the naming rule

  **Patterns to follow:**
  - Existing cross-reference style: `See [Attachment Rules](#attachment-rules)`

  **Verification:**
  - No extension section independently defines character rules for names
  - Each section links to `#naming-rules`
  - The Variables invalid example `$123start;` comment is now definitive

- [ ] **Unit 3: Update MDPP002 description in Validation Checks table**

  **Goal:** Reflect that MDPP002 now covers all name types, not just variables

  **Requirements:** R1, R3

  **Dependencies:** Unit 2

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

  **Approach:**
  - Change the MDPP002 row description from "Invalid variable name" to "Invalid name (variable, style, alias, or marker key)"
  - This aligns the spec with the expanded validation coverage

  **Verification:**
  - MDPP002 description in the Validation Checks table reflects all name types

- [ ] **Unit 4: Add name validation functions for styles, aliases, and marker keys in validate-mdpp.py**

  **Goal:** Add the validation functions needed to enforce the naming rule across all entity types

  **Requirements:** R2, R3

  **Dependencies:** None (can be done in parallel with spec units)

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`

  **Approach:**
  - Add `validate_style_name(name: str) -> bool` using `^[a-zA-Z_][a-zA-Z0-9_-]*$` (same as `validate_variable_name`)
  - Add `validate_alias_name(name: str) -> bool` using `^[a-zA-Z0-9_][a-zA-Z0-9_-]*$` (digit-first allowed)
  - Add `validate_marker_key(name: str) -> bool` using `^[a-zA-Z_][a-zA-Z0-9_-]*$` (same as standard)
  - Place these near the existing `validate_variable_name()` function (around line 75)
  - Consider whether `validate_variable_name` and `validate_marker_key` can share the same regex constant to reduce duplication

  **Patterns to follow:**
  - `validate_variable_name()` function signature and regex style
  - `validate_condition_expression()` for the pattern of extracting then validating

  **Test scenarios:**
  - `validate_style_name("CustomHeading")` -> True
  - `validate_style_name("BQ_Warning")` -> True
  - `validate_style_name("123Invalid")` -> False
  - `validate_alias_name("introduction")` -> True
  - `validate_alias_name("316492")` -> True (digit-first allowed)
  - `validate_alias_name("-invalid")` -> False (hyphen-first)
  - `validate_marker_key("Keywords")` -> True
  - `validate_marker_key("123Key")` -> False

  **Verification:**
  - All four validation functions exist and use the correct regex per R2

- [ ] **Unit 5: Wire validation into the main loop for styles, aliases, and marker keys**

  **Goal:** Call the new validation functions during document processing and report MDPP002 for invalid names

  **Requirements:** R3

  **Dependencies:** Unit 4

  **Files:**
  - Modify: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`

  **Approach:**
  - **Style names:** In the main validation loop, after matching `PATTERNS['style']`, extract and trim the name, call `validate_style_name()`. Report MDPP002 with message "Invalid style name: {name}".
  - **Alias names:** In the existing alias duplicate-check block (around line 294), after extracting `alias_name`, call `validate_alias_name()`. Report MDPP002 with message "Invalid alias name: #{name}". This runs before the duplicate check so both errors can be reported.
  - **Marker keys (simple format):** After matching `PATTERNS['marker_simple']`, extract the key (group 1), trim it, call `validate_marker_key()`. Report MDPP002 with message "Invalid marker key name: {name}".
  - **Marker keys (JSON format):** After the existing `validate_json()` call succeeds, parse the JSON again (or reuse the parsed result), iterate over keys, call `validate_marker_key()` on each. Report MDPP002 per invalid key.
  - Update the MDPP002 suggestion text to reference the naming rule: "Names must start with a letter or underscore, followed by letters, digits, hyphens, or underscores"
  - For alias MDPP002, adjust suggestion to note digit-first is allowed

  **Patterns to follow:**
  - Existing MDPP002 reporting block for variables (lines 208-222)
  - Existing alias processing block (lines 294-309)

  **Test scenarios:**
  - Style `<!--style:123Bad-->` on a heading -> MDPP002
  - Style `<!--style:GoodName-->` on a heading -> no error
  - Alias `<!--#-bad-start-->` on a heading -> MDPP002
  - Alias `<!--#04499224-->` on a heading -> no error (digit-first allowed)
  - Marker `<!--marker:123Key="value"-->` on a heading -> MDPP002
  - Marker `<!--markers:{"123Bad": "val"}-->` on a heading -> MDPP002
  - Marker `<!--markers:{"Keywords": "api"}-->` on a heading -> no error

  **Verification:**
  - Running `validate-mdpp.py` on a file with invalid style/alias/marker names reports MDPP002
  - Running on existing test files (`sample-basic.md`, `sample-full.md`) produces no new errors

- [ ] **Unit 6: Add test file for name validation (sample-invalid-names.md)**

  **Goal:** Create a targeted test file that exercises MDPP002 for all name types

  **Requirements:** R3

  **Dependencies:** Unit 5

  **Files:**
  - Create: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-invalid-names.md`

  **Approach:**
  - Follow the established test file pattern from `sample-orphaned-tags.md` and `sample-duplicate-aliases.md`
  - Include YAML frontmatter
  - POSITIVE CASES section: names that should trigger MDPP002
    - Variable with digit-first name
    - Style with digit-first name
    - Style with space in name
    - Alias starting with hyphen
    - Marker key with digit-first name (simple format)
    - Marker key with digit-first name (JSON format)
  - NEGATIVE CASES section: names that should pass validation
    - Variable with underscore-first name
    - Style with PascalCase name
    - Alias with digit-first name (valid exception)
    - Alias with numeric-only name
    - Condition with hyphenated name
    - Marker key with PascalCase name
  - Each case should have a heading explaining what it tests and an `EXPECT MDPP002` or `EXPECT no error` annotation

  **Patterns to follow:**
  - `tests/sample-orphaned-tags.md` structure (POSITIVE/NEGATIVE cases, numbered, annotated)

  **Verification:**
  - Running `validate-mdpp.py` on the test file produces MDPP002 for all positive cases and no MDPP002 for negative cases

- [ ] **Unit 7: Verify existing content compliance**

  **Goal:** Confirm no existing examples or whitepaper content violates the unified rule

  **Requirements:** R4

  **Dependencies:** Unit 5

  **Files:**
  - Validate: `spec/whitepaper.md`
  - Validate: `examples/*.md`
  - Validate: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-basic.md`
  - Validate: `plugins/markdown-plus-plus/skills/markdown-plus-plus/tests/sample-full.md`

  **Approach:**
  - Run `validate-mdpp.py` against each file
  - Confirm no new MDPP002 errors appear
  - The requirements doc notes the audit is complete with no violations found; this unit is a mechanical confirmation after the validator is updated

  **Verification:**
  - All existing files pass validation with zero new MDPP002 errors

## System-Wide Impact

- **Interaction graph:** The naming rule touches the spec reference, validation script, and test suite. No callbacks or observers -- this is a documentation/tooling repo.
- **Error propagation:** MDPP002 errors are reported in the validation output. No cascading failure risk.
- **API surface parity:** The ePublisher adapter regex updates are tracked separately in issue #27. Once this lands, issue #27 should reference the canonical regex from the spec.
- **Integration coverage:** Running `validate-mdpp.py` against all existing `.md` files confirms no false positives. The new test file confirms detection of true positives.

## Risks & Dependencies

- **Risk:** Changing MDPP002's description from "Invalid variable name" to cover all name types could affect downstream tooling that parses validator output by code. **Mitigation:** The error *code* (MDPP002) is unchanged; only the human-readable message and description change. JSON output consumers should key on the code, not the message text.
- **Dependency:** Issue #14 (error code documentation) should be updated after this lands to reflect MDPP002's expanded scope.
- **Dependency:** Issue #27 (ePublisher adapter) should reference the unified rule regex from the updated spec.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-05-unified-naming-rule-requirements.md](docs/brainstorms/2026-04-05-unified-naming-rule-requirements.md)
- Related code: `plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py`
- Related code: `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- Related issues: #11 (formal grammar), #14 (error codes), #27 (ePublisher adapter)
