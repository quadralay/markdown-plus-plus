---
date: 2026-04-08
status: active
---

# Markdown++ Error Code Reference

Implementation-independent reference for all Markdown++ validation error codes. Validator implementations should use this document as the authoritative source for error code behavior, severity, and detection logic.

## Quick Reference

| Code | Name | Severity | Description |
|------|------|----------|-------------|
| MDPP000 | File error | Error | File not found or not readable |
| MDPP001 | Unmatched condition block | Error | Opening without closing, or stray close |
| MDPP002 | Invalid name | Error | Name with illegal characters in any named entity |
| MDPP003 | Malformed marker JSON | Error | `<!--markers:{...}-->` fails to parse |
| MDPP004 | *(Reserved)* | Warning | Formerly "Invalid style placement" — covered by MDPP009 (orphaned comment tag) |
| MDPP005 | Circular include | Error | Include chain references itself |
| MDPP006 | Missing include file | Warning | Referenced file does not exist |
| MDPP007 | Invalid condition syntax | Error | Illegal characters or empty expression |
| MDPP008 | Duplicate alias | Error | Same alias appears twice in one file |
| MDPP009 | Orphaned comment tag | Warning | Tag not followed by content element |

## General Rules

All line-based checks skip lines inside fenced code blocks. A fenced code block opens with three or more backticks or tildes and closes with the same character at the same or greater count (per CommonMark 0.30).

## Naming Rule

Markdown++ defines three naming patterns. The pattern applied depends on the entity type:

| Form | Regex | Used By | Spaces |
|------|-------|---------|--------|
| **Standard identifier** | `^[a-zA-Z_][a-zA-Z0-9_\-]*$` | Variables, conditions | No |
| **Alias name** | `^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$` | Aliases (digit-first permitted) | No |
| **Style/marker name** | `^[a-zA-Z_][a-zA-Z0-9_ \-]*$` (trimmed) | Styles, marker keys (embedded spaces permitted) | Yes, embedded |

### Standard Identifier

**Regex:** `^[a-zA-Z_][a-zA-Z0-9_\-]*$`

- First character must be a letter (`a-z`, `A-Z`) or underscore (`_`)
- Subsequent characters may be letters, digits (`0-9`), hyphens (`-`), or underscores (`_`)
- Minimum length is 1 character
- No whitespace or punctuation characters
- Used by: variable names (`$name;`), condition names

### Alias Name

Alias names may also begin with a digit, since aliases often map to numeric identifiers (e.g., `<!--#04499224-->`).

**Regex:** `^[a-zA-Z0-9_][a-zA-Z0-9_\-]*$`

Used by: alias names (`<!--#name-->`).

### Style/Marker Name

Style names and marker key names permit embedded spaces to support compound names (e.g., `Code Block`, `Blockquote Paragraph`) and legacy style systems.

**Regex:** `^[a-zA-Z_][a-zA-Z0-9_ \-]*$` applied after trimming leading/trailing spaces.

- First character must be a letter or underscore (same as standard)
- Subsequent characters may include embedded spaces in addition to letters, digits, hyphens, and underscores
- Leading and trailing spaces are stripped before validation
- Used by: style names (`<!--style:name-->`), marker key names (`<!--markers:{...}-->`, `<!--marker:key="value"-->`)

For non-English content, the same structural rules apply using the language's UTF-8 letter values in place of `a-zA-Z`.

---

## MDPP000 -- File Error

**Severity:** Error

**Description:** The input file does not exist or cannot be read (permissions, encoding errors).

**Detection logic:** Checked before any content validation. If the file path does not resolve to a readable file, emit MDPP000 and halt. No further checks run.

**Trigger examples:**

```bash
# File does not exist
python validate-mdpp.py nonexistent.md
# MDPP000: File not found

# File exists but is not readable
python validate-mdpp.py /root/restricted.md
# MDPP000: Cannot read file: [Errno 13] Permission denied
```

**Suggested fix:** Verify the file path and ensure the file exists with appropriate read permissions and UTF-8 encoding.

---

## MDPP001 -- Unmatched Condition Block

**Severity:** Error

**Description:** A condition block is opened without a matching close, or a closing tag appears without a preceding open. Condition blocks must form properly matched pairs and MUST NOT be nested.

**Detection logic:** Stack-based tracking of `<!--condition:EXPR-->` / `<!--/condition-->` pairs. On an opening tag, push to the stack; if stack depth exceeds 1, emit "nested condition block." On a closing tag, pop the stack; if the stack is empty, emit "closing without opening." After processing all lines, any remaining entries on the stack emit "unclosed condition block."

**Trigger examples:**

```markdown
<!-- ERROR: closing tag with no matching open -->
<!--/condition-->

<!-- ERROR: open without close -->
<!--condition:print-->
This content is conditional.
<!-- missing <!--/condition--> -->

<!-- ERROR: nested condition block -->
<!--condition:web-->
Outer content.
<!--condition:advanced-->
Nested content — not permitted.
<!--/condition-->
<!--/condition-->
```

**Suggested fix:**
- For a stray closing tag: remove it, or add a matching `<!--condition:name-->` above
- For an unclosed block: add `<!--/condition-->` to close the block
- For a nested block: replace with a logical expression, e.g. `<!--condition:web advanced-->` instead of nesting

---

## MDPP002 -- Invalid Name

**Severity:** Error

**Description:** A named entity (variable, condition name, style, marker key, or alias) contains characters that violate the naming rule for its entity type.

**Detection logic:** Each name is tested against the naming rule regex for its entity type. The check applies to:

- **Variables:** The name portion of `$name;` references (standard identifier rule)
- **Condition names:** Individual names within condition expressions (standard identifier rule; see also MDPP007)
- **Alias names:** The name in `<!--#name-->` (alias rule — digit-first allowed)
- **Style names:** The name in `<!--style:name-->` (style/marker rule — embedded spaces allowed)
- **Marker key names:** Keys inside `<!--markers:{...}-->` and `<!--marker:key="value"-->` (style/marker rule — embedded spaces allowed)

**Trigger examples:**

```markdown
<!-- ERROR: variable name starts with digit -->
$1foo;

<!-- ERROR: variable name contains space (variables use standard identifier rule) -->
$my variable;

<!-- ERROR: style name with punctuation (periods not in style/marker rule) -->
<!--style:My.Style-->

<!-- ERROR: marker key starts with digit (style/marker rule still requires letter/underscore first) -->
<!--markers:{"1key": "value"}-->

<!-- ERROR: alias name contains invalid character (period not allowed) -->
<!--#my.section-->

<!-- NOTE: alias may start with a digit — digit-first is valid for aliases -->
<!--#04499224-->

<!-- NOTE: embedded spaces in style/marker names are valid -->
<!--style:Code Block-->
<!--markers:{"Table Cell Head": "value"}-->
```

**Suggested fix:** The required characters depend on the entity type:

- **Variables and conditions (standard identifier rule):** Start with a letter or underscore; subsequent characters may be letters, digits, hyphens, or underscores. No spaces.
- **Aliases (alias rule):** Same as standard, but may also start with a digit.
- **Style names and marker keys (style/marker rule):** Start with a letter or underscore; subsequent characters may include embedded spaces as well as letters, digits, hyphens, and underscores. Leading/trailing spaces are stripped.

---

## MDPP003 -- Malformed Marker JSON

**Severity:** Error

**Description:** The JSON payload inside a `<!--markers:{...}-->` directive fails to parse.

**Detection logic:** The JSON substring (the `{...}` portion) is extracted and passed to a JSON parser. If parsing fails, the decode error is emitted. If parsing succeeds, individual key names are further validated against the style/marker name rule (see MDPP002).

**Trigger examples:**

```markdown
<!-- ERROR: single quotes instead of double quotes -->
<!--markers:{'key': 'value'}-->

<!-- ERROR: trailing comma -->
<!--markers:{"key": "value",}-->

<!-- ERROR: unquoted key -->
<!--markers:{key: "value"}-->
```

**Suggested fix:** Ensure JSON uses double-quoted keys and values with no trailing commas. Use a JSON linter to validate the payload.

---

## MDPP004 -- Reserved

**Severity:** Warning

**Description:** Reserved. This code was originally designated for "Invalid style placement" but that condition is fully covered by MDPP009 (orphaned comment tag), which detects any directive tag not properly attached to a content element. MDPP004 is retained as a placeholder to preserve code numbering stability.

---

## MDPP005 -- Circular Include

**Severity:** Error

**Description:** An include chain forms a cycle, where a file directly or indirectly includes itself.

**Detection logic:** Track the include chain as a set of resolved file paths. Before processing each `<!--include:path-->`, check whether the resolved path is already in the chain. If so, emit MDPP005.

---

## MDPP006 -- Missing Include File

**Severity:** Warning

**Description:** A file referenced in an `<!--include:path-->` directive does not exist at the resolved path.

**Detection logic:** The include path is resolved relative to the directory of the containing file. The resolved path is tested with a file-existence check. If the file does not exist, emit MDPP006.

**Trigger examples:**

```markdown
<!-- WARNING: referenced file does not exist -->
<!--include:missing-chapter.md-->

<!-- WARNING: path is relative to containing file -->
<!--include:../sections/deleted-section.md-->
```

**Suggested fix:** Verify the include path. Paths are resolved relative to the directory containing the current file.

---

## MDPP007 -- Invalid Condition Syntax

**Severity:** Error

**Description:** A condition expression contains illegal characters, is empty, or has an invalid structure.

**Detection logic:** The expression inside `<!--condition:EXPR-->` is split on commas (OR) and whitespace (AND). Each resulting part is stripped and validated:

1. If the expression is empty after trimming, emit "Empty condition expression"
2. If a part starts with `!` (NOT operator), the `!` is removed before checking
3. If a part is empty after removing the NOT operator, emit "Empty condition after NOT operator"
4. Each part (after NOT removal) is validated against the standard identifier regex (`^[a-zA-Z_][a-zA-Z0-9_\-]*$`)

**Trigger examples:**

```markdown
<!-- ERROR: empty condition expression -->
<!--condition:-->

<!-- ERROR: invalid characters in condition name -->
<!--condition:my condition-->

<!-- ERROR: empty after NOT operator -->
<!--condition:!-->
```

**Suggested fix:** Use valid condition names (alphanumeric with hyphens and underscores). Separate multiple conditions with commas (OR) or spaces (AND). Use `!` as a prefix for NOT.

---

## MDPP008 -- Duplicate Alias

**Severity:** Error

**Description:** The same alias name appears more than once in a single file. Alias names must be unique within a file to allow unambiguous cross-referencing.

**Detection logic:** A dictionary tracks alias names to their first-seen line number. When an alias is encountered, it is looked up in the dictionary. If already present, emit MDPP008 referencing the first occurrence. Otherwise, record the alias and its line number.

**Trigger examples:**

```markdown
<!-- First definition: OK -->
<!--#introduction-->
## Introduction

<!-- ERROR: same alias defined again -->
<!--#introduction-->
## Another Section
```

**Suggested fix:** Use a unique alias name for each element. The error message includes the line number of the first definition.

**Note:** MDPP008 applies only to custom aliases (`<!-- #name -->`). Auto-generated heading aliases that collide with each other are silently disambiguated with a counter suffix (`-2`, `-3`, etc.) rather than triggering an error. When a custom alias and an auto-generated alias share the same identifier, both exist independently in separate namespaces -- the custom alias takes resolution priority (no suffix is applied to the auto-generated alias). See [Duplicate Alias Resolution](../../../../../spec/element-interactions.md#duplicate-alias-resolution) and [Custom Alias Priority](../../../../../spec/element-interactions.md#custom-alias-priority).

---

## MDPP009 -- Orphaned Comment Tag

**Severity:** Warning

**Description:** An MDPP comment tag (style, alias, marker, or multiline) is not followed by a content element on the next line. A blank line or end-of-file between the tag and its target element means the tag has no effect.

**Detection logic:** Second pass over lines outside fenced code blocks. For each line that contains only an MDPP comment tag:

1. Check if the next line exists
2. Check if the next line is a non-blank, non-tag content line
3. If the next line is blank, missing, or another MDPP tag without intervening content, emit MDPP009

Tags checked: `<!--style:...-->`, `<!--#alias-->`, `<!--markers:...-->`, `<!--marker:...-->`, `<!--multiline-->`

Tags exempt from this check: `<!--condition:...-->`, `<!--/condition-->`, `<!--include:...-->`, variable references (`$name;`)

**Trigger examples:**

```markdown
<!-- WARNING: blank line separates tag from content -->
<!--style:Note-->

This paragraph is not styled because of the blank line.

<!-- WARNING: tag at end of file with no following content -->
<!--style:Footer-->
```

**Suggested fix:** Remove the blank line between the tag and the element it applies to. If multiple tags apply to the same element, combine them on one line using semicolons: `<!--style:Note; #my-note-->`.
