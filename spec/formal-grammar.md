---
date: 2026-04-08
status: active
---

# Formal Grammar for Markdown++ Extensions

## Scope

This document defines a formal grammar for all Markdown++ extension constructs. It covers **only** the Markdown++ extensions -- it does not re-specify [CommonMark 0.30](https://spec.commonmark.org/0.30/), which serves as the base document format. The grammar defines how Markdown++ constructs are recognized within a CommonMark document.

Markdown++ adds two syntactic forms to CommonMark:

1. **Inline variable tokens** -- `$variable_name;` (and their escaped form `\$variable_name;`)
2. **HTML comment directives** -- `<!-- command -->` containing one or more Markdown++ commands

All other content is standard CommonMark and is outside the scope of this grammar.

YAML frontmatter, including the `mdpp-version` field defined in [Format Versioning](versioning.md), is document metadata. It is not a Markdown++ extension construct and is outside the scope of this grammar. Frontmatter processing rules are defined in the versioning specification.

## Relationship to CommonMark

A Markdown++ document is a valid CommonMark 0.30 document. Markdown++ extensions are expressed through mechanisms that CommonMark already defines:

- **HTML comments** (`<!-- ... -->`) -- CommonMark treats these as raw HTML blocks or inline HTML. Markdown++ gives semantic meaning to comments whose content matches a recognized command pattern.
- **Inline tokens** (`$name;`) -- CommonMark treats these as literal text. Markdown++ interprets them as variable references.

A CommonMark processor that does not recognize Markdown++ extensions will render the document correctly: comment directives are invisible, and variable tokens appear as literal text.

## Notation Conventions

This grammar uses **W3C EBNF notation**, the same variant used by the [XML](https://www.w3.org/TR/xml/#sec-notation) and [CSS](https://www.w3.org/TR/css-syntax-3/#tokenization) specifications.

| Symbol | Meaning |
|--------|---------|
| `::=` | Definition |
| `A B` | Sequence (A followed by B) |
| `A \| B` | Alternation (A or B) |
| `A?` | Optional (zero or one) |
| `A*` | Zero or more |
| `A+` | One or more |
| `A - B` | Exception (A but not B) |
| `[a-z]` | Character range (inclusive) |
| `[^a-z]` | Negated character class |
| `#xN` | Unicode code point in hexadecimal |
| `"..."` | Terminal string (literal characters) |
| `(...)` | Grouping |
| `/* ... */` | Comment |

Productions are listed in dependency order: lexical terminals first, then composite productions that reference them.

## Lexical Terminals

```ebnf
letter         ::= [a-zA-Z]
                    /* ASCII letters. Future versions may extend to Unicode
                       Letter categories for non-English identifier support. */

digit          ::= [0-9]

ws             ::= (#x20 | #x9)+
                    /* One or more spaces or horizontal tabs.
                       Spaces are conventional; tabs are permitted. */
```

## EBNF Grammar

### Top-Level Productions

A Markdown++ extension is either a variable reference, an escaped variable, or an HTML comment directive:

```ebnf
mdpp_extension     ::= variable
                      | escaped_variable
                      | mdpp_comment
```

These three forms are the complete set of Markdown++ syntactic extensions to CommonMark. Any content that does not match one of these productions is standard CommonMark.

### Identifiers

Markdown++ defines three identifier forms:

- The **standard identifier** is used for variables and conditions.
- The **alias name** additionally permits a leading digit, since aliases often map to numeric identifiers (e.g., `#04499224`, `#316492`).
- The **style name** additionally permits embedded spaces, since styles and markers use compound names (e.g., `Blockquote Paragraph`, `Table Cell Head`) and legacy systems use space-embedded style names.

```ebnf
identifier         ::= (letter | "_") (letter | digit | "-" | "_")*

alias_name         ::= (letter | digit | "_") (letter | digit | "-" | "_")*

style_name         ::= (letter | "_") (letter | digit | "-" | "_" | " ")*
                       /* Leading and trailing spaces are stripped before matching.
                          The trimmed result must not be empty. */
```

The standard identifier corresponds to the regex `[a-zA-Z_][a-zA-Z0-9_\-]*`. The alias name corresponds to the regex `[a-zA-Z0-9_][a-zA-Z0-9_\-]*`. The style name corresponds to the regex `[a-zA-Z_][a-zA-Z0-9_\- ]*` applied after trimming.

**Rationale for three forms:** The alias exception is an intentional design choice. Aliases frequently serve as numeric content identifiers (e.g., CMS record IDs), and requiring a letter prefix would force unnatural naming. The style name exception allows embedded spaces for processor-defined compound names and legacy compatibility. Variables and conditions use the standard identifier to avoid ambiguity with numeric literals (e.g., `$100;` is not a variable reference).

### Variables

Variables are the only Markdown++ extension that does not use HTML comment syntax. A variable reference consists of a `$` prefix, a standard identifier, and a terminating semicolon:

```ebnf
variable           ::= "$" identifier ";"

escaped_variable   ::= "\" "$" identifier ";"
```

The escaped form (`\$`) prevents variable interpretation. See [Variable Escaping](#variable-escaping) for the full specification.

**Examples:**

| Input | Production | Result |
|-------|-----------|--------|
| `$product_name;` | `variable` | Variable reference |
| `$release-date;` | `variable` | Variable reference (hyphen in name) |
| `$_internal;` | `variable` | Variable reference (underscore-first) |
| `\$product_name;` | `escaped_variable` | Literal text `$product_name;` |
| `$123start;` | *(no match)* | Not a valid variable -- digit-first |
| `$name` | *(no match)* | Not a valid variable -- missing semicolon |

### Comment Directives

All Markdown++ extensions other than variables use HTML comment syntax. A comment directive consists of the HTML comment delimiters enclosing a command list:

```ebnf
mdpp_comment       ::= "<!--" ws? command_list ws? "-->"
```

**Parsing note:** The comment boundary is determined first -- the parser finds the opening `<!--` and the nearest subsequent `-->` to extract the comment content. The `command_list` then operates on the extracted content. This two-phase approach (boundary detection, then content parsing) is consistent with how CommonMark processes HTML comments.

### Command List (Combined Commands)

A command list contains one or more segments separated by semicolons. Each segment is either a recognized command or unrecognized text. Unrecognized segments MUST NOT affect the CommonMark processing of the attached content. Their disposition is implementation-defined — implementations MAY pass them through as HTML comments, inject them as markers, or discard them.

```ebnf
command_list       ::= segment (ws? ";" ws? segment)*

segment            ::= command
                     | unrecognized_text

command            ::= style_cmd
                     | alias_cmd
                     | condition_open_cmd
                     | condition_close_cmd
                     | include_cmd
                     | marker_cmd
                     | markers_cmd
                     | multiline_cmd

unrecognized_text  ::= [^;]+
                       /* Any non-empty sequence of characters except ";".
                          This production operates on content already extracted
                          from within the comment delimiters. */
```

**Parsing note:** A conformant parser MUST first attempt to match each recognized command production against a segment. Only if no command production matches should the segment be classified as `unrecognized_text`. The `markers_cmd` production greedily consumes its JSON object (including any semicolons within JSON string values) before the next segment delimiter is considered.

**Whitespace around semicolons** is optional but recommended for readability:

| Input | Parsing |
|-------|---------|
| `style:A;#b;marker:C="d"` | Three recognized commands |
| `style:A ; #b ; marker:C="d"` | Three recognized commands (preferred style) |
| `style:X ; TODO: add markers ; #alias` | Two commands + one unrecognized segment (disposition implementation-defined) |

### Individual Commands

#### Style Command

Applies a custom style to the attached content element. The style name follows the style name rule, which permits embedded spaces.

```ebnf
style_cmd          ::= "style:" style_name
```

**Examples:** `style:CustomHeading`, `style:NoteBlock`, `style:BQ_Warning`, `style:Code Block`

#### Alias Command

Assigns a custom anchor identifier to the attached content element. The alias name permits a leading digit.

```ebnf
alias_cmd          ::= "#" alias_name
```

**Examples:** `#introduction`, `#getting-started`, `#316492`, `#04499224`

#### Condition Open Command

Opens a conditional content block. Content between the opening and closing condition tags is included, excluded, or passed through based on the condition expression and the condition set.

```ebnf
condition_open_cmd ::= "condition:" condition_expr
```

**Examples:** `condition:web`, `condition:!draft`, `condition:web,print`, `condition:!draft,web production`

#### Condition Close Command

Closes the most recently opened condition block.

```ebnf
condition_close_cmd ::= "/condition"
```

#### Include Command

Inserts the contents of another file at the directive's position. The file path is relative to the containing file's directory.

```ebnf
include_cmd        ::= "include:" file_path

file_path          ::= [^>]+
                       /* Any non-empty sequence of characters except ">".
                          File paths are resolved relative to the containing
                          file's directory. This production is intentionally
                          permissive to accommodate varied file system path
                          conventions across operating systems. */
```

**Examples:** `include:shared/header.md`, `include:../common/footer.md`, `include:chapters/introduction.md`

#### Simple Marker Command

Attaches a single key-value metadata pair to the attached content element.

```ebnf
marker_cmd         ::= "marker:" style_name '="' marker_value '"'

marker_value       ::= [^"]*
                       /* Any sequence of characters except double quote.
                          Escaped double quotes within marker values are
                          not supported. An empty value ("") is permitted. */
```

**Examples:** `marker:Keywords="api, documentation"`, `marker:IndexMarker="setup:initial"`, `marker:Passthrough="<a id='legacy-anchor'></a>"`, `marker:Index Entry="setup"`

#### JSON Markers Command

Attaches multiple key-value metadata pairs using JSON object syntax.

```ebnf
markers_cmd        ::= "markers:" json_object

json_object        ::= /* A JSON object as defined by RFC 8259.
                          Keys MUST be strings conforming to the style/marker
                          name rule. Values may be any JSON type
                          (string, number, boolean, array, object, null). */
```

The `json_object` production references [RFC 8259 (The JavaScript Object Notation Data Interchange Format)](https://www.rfc-editor.org/rfc/rfc8259). Inlining a JSON grammar would be redundant and error-prone. Conformant parsers MUST use a standards-compliant JSON parser for this production.

**Note:** The `json_object` may contain semicolons within JSON string values. A conformant parser MUST parse the complete JSON object (matching balanced braces) before looking for the next segment delimiter. The current reference implementation (`validate-mdpp.py`) uses a simplified regex pattern that does not handle nested braces -- this is a known implementation limitation, not a grammar limitation.

**Examples:**

- `markers:{"Keywords": "api, docs"}`
- `markers:{"Keywords": "test", "Priority": "high", "Published": true}`
- `markers:{"Keywords": "markers, metadata", "Description": "How to use markers"}`

#### Multiline Table Indicator

Declares that the immediately following table uses multiline row syntax with continuation rows.

```ebnf
multiline_cmd      ::= "multiline"
```

### Condition Expressions

Condition expressions support three operators with explicit precedence. The grammar uses layered productions to express precedence without ambiguity:

| Operator | Symbol | Precedence | Associativity |
|----------|--------|------------|---------------|
| NOT | `!` (prefix) | Highest (1) | Right (unary) |
| AND | ` ` (space) | Medium (2) | Left |
| OR | `,` (comma) | Lowest (3) | Left |

```ebnf
condition_expr     ::= or_expr

or_expr            ::= and_expr (ws? "," ws? and_expr)*

and_expr           ::= unary_expr (ws unary_expr)*

unary_expr         ::= "!"? identifier
```

**Parsing examples:**

| Expression | Parse Tree | Interpretation |
|------------|-----------|----------------|
| `web` | `identifier("web")` | Show when "web" is visible |
| `!draft` | `NOT identifier("draft")` | Show when "draft" is hidden |
| `web print` | `identifier("web") AND identifier("print")` | Both must be visible |
| `web,print` | `identifier("web") OR identifier("print")` | Either can be visible |
| `!internal,web` | `(NOT "internal") OR "web"` | "internal" hidden OR "web" visible |
| `!draft,web production` | `(NOT "draft") OR ("web" AND "production")` | Full three-level precedence |

The last example demonstrates all three precedence levels: `!` binds tightest (to `draft`), space binds next (`web` AND `production`), and `,` binds loosest (producing the top-level OR).

**Whitespace around commas:** Optional whitespace before and after the `,` operator is permitted for readability. The `ws?` in `or_expr` handles this. The space character within `and_expr` is the AND operator itself, not formatting whitespace.

## Structural Constraints

Several Markdown++ commands require **attachment** to a content element -- the command tag must appear on the line immediately above its target element with zero blank lines between them. Attachment is a positional relationship that EBNF/PEG cannot naturally express. The [Attachment Rule](attachment-rule.md) provides the complete formal definition.

The following table summarizes which grammar productions require attachment:

| Production | Attachment Required | Standalone Permitted |
|------------|:-------------------:|:--------------------:|
| `style_cmd` | Yes | No |
| `alias_cmd` | Yes | No |
| `marker_cmd` | Yes | No |
| `markers_cmd` | Yes | No |
| `multiline_cmd` | Yes (above table) | No |
| `condition_open_cmd` | No (wraps content) | Yes |
| `condition_close_cmd` | No (wraps content) | Yes |
| `include_cmd` | No (standalone directive) | Yes |

**Inline placement:** The `style_cmd` production may also appear in inline position, immediately before the styled inline element on the same line with no intervening space between the closing `-->` and the element. Inline placement applies only to `style_cmd`; all other commands that require attachment operate at block level only.

**Condition pairing:** `condition_open_cmd` and `condition_close_cmd` form matched pairs. Every `condition_open_cmd` MUST have a corresponding `condition_close_cmd`. Condition blocks MUST NOT nest or overlap.

**Multiline table row structure:** The `multiline_cmd` production defines only the directive keyword. Once a table is marked multiline, the row-level structural behaviors -- row separator recognition (pipe-delimited rows with whitespace-only cells), continuation row merging (empty first cell), multiline header support, blank-line termination, and cell content dedent -- are table-level behaviors that depend on CommonMark table parsing. These cannot be expressed as EBNF/PEG productions. The [Processing Model](processing-model.md) defines the complete multiline table processing requirements, including conformance sub-requirements for each behavior.

A conformant parser MUST enforce these structural constraints. The grammar defines the **syntactic** form of each construct; the structural constraints define the **positional** requirements for those constructs to take effect.

## Variable Escaping

Two mechanisms prevent variable interpretation:

### 1. Backslash Escaping (Syntactic)

The `escaped_variable` production (`\$identifier;`) is recognized during the variable-scanning phase. The backslash is consumed, the `$` becomes a literal character, and the remainder passes through without variable substitution. The result in published output is the literal text `$identifier;`.

Backslash escaping is resolved **before** variable substitution in the processing pipeline. This is distinct from CommonMark's backslash escaping, which operates during Markdown parsing in a later phase.

### 2. Code Span Exclusion (Processing Constraint)

Content inside CommonMark code spans (backtick-delimited) is excluded from variable scanning entirely. This is not expressed as a grammar production because it depends on CommonMark's code span parsing, which is outside the scope of this grammar.

A conformant Markdown++ processor MUST NOT interpret `$identifier;` sequences within code spans as variable references.

| Mechanism | Grammar Production | Use Case |
|-----------|-------------------|----------|
| `\$` | `escaped_variable` | Literal `$name;` in running prose |
| `` `$name;` `` | *(CommonMark code span)* | Showing syntax examples or code |

## Conformance

A **grammar-conformant parser** is a parser that:

1. **Accepts** all strings that match the productions in this grammar
2. **Rejects** strings that do not match any production (or classifies them as regular CommonMark content)
3. **Enforces** the structural constraints defined in [Structural Constraints](#structural-constraints) and the [Attachment Rule](attachment-rule.md)
4. **Delegates** JSON parsing in `markers_cmd` to an RFC 8259-compliant JSON parser
5. **Excludes** code spans and fenced code blocks from Markdown++ extension scanning, consistent with CommonMark's treatment of these as opaque content

The grammar defines the **syntactic form** of Markdown++ extensions. It does not define:

- **Semantic processing** -- how variables are resolved, how conditions are evaluated, or how includes are processed
- **Error recovery** -- how a parser should behave when encountering malformed constructs
- **Output generation** -- how parsed constructs map to output formats
- **Frontmatter processing** -- how YAML frontmatter (including `mdpp-version`) is parsed and interpreted. See [Format Versioning](versioning.md)

These are implementation concerns outside the scope of this grammar.

## PEG Transliteration

This section provides the same grammar in **Parsing Expression Grammar (PEG)** notation for parser authors who prefer PEG-based tools. The PEG uses idiomatic conventions rather than a mechanical 1:1 mapping from the EBNF.

### PEG Notation Legend

| Symbol | Meaning |
|--------|---------|
| `<-` | Definition (ordered) |
| `e1 / e2` | Ordered choice (try e1 first; if it fails, try e2) |
| `e1 e2` | Sequence |
| `e*` | Zero or more (greedy) |
| `e+` | One or more (greedy) |
| `e?` | Optional |
| `!e` | Not-predicate (negative lookahead; succeeds if e fails, consumes nothing) |
| `&e` | And-predicate (positive lookahead; succeeds if e matches, consumes nothing) |
| `[a-z]` | Character class |
| `'...'` | Terminal string |
| `.` | Any character |

**Key difference from EBNF:** PEG's ordered choice (`/`) is inherently prioritized -- the first matching alternative wins. EBNF's alternation (`|`) is unordered. In this grammar, the difference matters for the `segment` production: PEG tries `command` before `unrecognized_text`, ensuring recognized commands are never accidentally captured as unrecognized text.

### PEG Rules

```peg
# Top-level productions
mdpp_extension     <- variable / escaped_variable / mdpp_comment

# Variables
variable           <- '$' identifier ';'
escaped_variable   <- '\\' '$' identifier ';'

# Comment directives
mdpp_comment       <- '<!--' ws? command_list ws? '-->'

# Command list (combined commands)
command_list       <- segment (ws? ';' ws? segment)*
segment            <- command / unrecognized_text
command            <- style_cmd / alias_cmd / condition_open_cmd
                    / condition_close_cmd / include_cmd
                    / markers_cmd / marker_cmd / multiline_cmd

# Unrecognized text (catch-all; disposition is implementation-defined)
unrecognized_text  <- (!';' !close_delim .)+
close_delim        <- ws? '-->'

# Identifiers
identifier         <- [a-zA-Z_] [a-zA-Z0-9_-]*
alias_name         <- [a-zA-Z0-9_] [a-zA-Z0-9_-]*
style_name         <- [a-zA-Z_] [a-zA-Z0-9_ -]*
                      # Leading/trailing spaces stripped before matching

# Individual commands
style_cmd          <- 'style:' style_name
alias_cmd          <- '#' alias_name
condition_open_cmd <- 'condition:' condition_expr
condition_close_cmd <- '/condition'
include_cmd        <- 'include:' file_path
marker_cmd         <- 'marker:' style_name '="' marker_value '"'
markers_cmd        <- 'markers:' json_object
multiline_cmd      <- 'multiline'

# Condition expressions (precedence via layered rules)
condition_expr     <- or_expr
or_expr            <- and_expr (ws? ',' ws? and_expr)*
and_expr           <- unary_expr (ws unary_expr)*
unary_expr         <- '!'? identifier

# File paths
file_path          <- (!'>' .)+

# Marker values
marker_value       <- (!'"' .)*

# JSON objects (delegate to RFC 8259 parser)
# Simplified PEG for structural matching; production parsers
# SHOULD use a dedicated JSON parser.
json_object        <- '{' json_content '}'
json_content       <- (json_string / json_nested / !'}' .)*
json_nested        <- '{' json_content '}'
json_string        <- '"' (!'"' ('\\' . / .))* '"'

# Lexical terminals
ws                 <- [ \t]+
```

### PEG-Specific Notes

1. **Command ordering in `command`:** The ordered choice lists `markers_cmd` before `marker_cmd` because `markers:` is a longer prefix than `marker:`. If `marker_cmd` were tried first, the `marker` prefix would match and the trailing `s:` would cause a parse failure, requiring a backtrack. Listing the longer prefix first avoids unnecessary backtracking.

2. **Negative lookahead in `unrecognized_text`:** The PEG uses `!';' !close_delim .` to consume characters that are neither semicolons nor the start of the comment closing delimiter. This is more precise than the EBNF's character-class approach and naturally handles the `-->` boundary without a separate parsing phase.

3. **JSON approximation:** The PEG includes a simplified JSON production for structural matching. Production parsers SHOULD use a dedicated JSON parser for `json_object`. The simplified production handles balanced braces and quoted strings (with backslash escaping within strings) but does not validate full JSON conformance.

4. **Greedy matching:** PEG repetition operators (`*`, `+`) are inherently greedy. The `and_expr` production greedily consumes space-separated identifiers, stopping when the next token is not whitespace followed by an identifier. This correctly handles the precedence boundary between AND (space) and OR (comma).

## Validation Notes

This grammar has been validated against the existing test corpus and example files in this repository.

### Constructs Accepted

The following constructs from `tests/sample-full.md` were verified against the grammar:

| Line(s) | Construct | Production(s) |
|---------|-----------|---------------|
| 6 | `<!--markers:{...} ; #document-start-->` | `markers_cmd` + `alias_cmd` in `command_list` |
| 7 | `$product_name;` | `variable` |
| 21 | `$my-var;`, `$my_var;`, `$var2;` | `variable` (hyphenated, underscored, digit-containing) |
| 27 | `<!--style:CustomHeading-->` | `style_cmd` (no whitespace) |
| 54 | `<!--style:Emphasis-->**inline**` | `style_cmd` (inline placement) |
| 62 | `<!--#introduction-->` | `alias_cmd` |
| 88--92 | `<!--condition:web-->...<!--/condition-->` | `condition_open_cmd` / `condition_close_cmd` pair |
| 112--114 | `<!--condition:web production-->` | `and_expr` with AND operator |
| 118--120 | `<!--condition:web,print-->` | `or_expr` with OR operator |
| 129--132 | `<!--condition:!draft,web production-->` | Full `condition_expr` with all three precedence levels |
| 163--164 | `<!--markers:{"Keywords":...} ; #json-format-->` | `markers_cmd` + `alias_cmd` |
| 168--169 | `<!--marker:Keywords="api, documentation"-->` | `marker_cmd` |
| 187--188 | `<!-- multiline -->` | `multiline_cmd` (with whitespace) |
| 258 | `<!-- style:CustomHeading ; marker:Keywords="intro" ; #combined-example -->` | Three commands in `command_list` |
| 261 | `<!-- style:DataTable ; multiline ; #feature-table -->` | Three commands including `multiline_cmd` |
| 361--362 | `<!-- style:SpacedStyle -->` | `style_cmd` (extra whitespace) |

### Constructs Rejected

The following invalid cases from `tests/sample-invalid-names.md` were verified:

| Case | Construct | Rejected By |
|------|-----------|-------------|
| 1 | `$123start;` | `identifier` -- digit-first |
| 2 | `<!--style:123BadStyle-->` | `identifier` -- digit-first |
| 3 | `<!--style:Bad Style-->` | `identifier` -- space in name |
| 4 | `<!--#-bad-start-->` | `alias_name` -- hyphen-first |
| 5 | `<!--marker:123Key="value"-->` | `identifier` -- digit-first |
| 6 | `<!--markers:{"123Bad": "val"}-->` | `style_name` applied to JSON key -- digit-first |
| 16 | `<!--#bad.alias-->` | `alias_name` -- period not in character set |
| 17 | `<!--style:Bad!Style-->` | `identifier` -- exclamation not in character set |

### Valid Edge Cases Confirmed

| Case | Construct | Accepted By |
|------|-----------|-------------|
| 7 | `$_internal_var;` | `identifier` -- underscore-first |
| 8 | `<!--style:CustomHeading-->` | `identifier` -- PascalCase |
| 9 | `<!--#04499224-->` | `alias_name` -- digit-first alias |
| 10 | `<!--#316492-->` | `alias_name` -- all-digit alias |
| 11 | `<!--condition:print-only-->` | `identifier` -- hyphenated condition name |
| 14 | `<!--style:BQ_Warning-Box-->` | `identifier` -- mixed underscore and hyphen |
| 15 | `<!--#_private_anchor-->` | `alias_name` -- underscore-first alias |

### Example Files Validated

All constructs in the five example files (`examples/*.md`) parse correctly under this grammar:

- **`styles-and-variables.md`** -- Variables, escaped variables (`\$not_a_variable;`), block styles, inline styles, combined commands with style and alias
- **`includes-and-conditions.md`** -- Include directives (in examples), condition blocks with both compact (`<!--/condition-->`) and spaced (`<!-- /condition -->`) close syntax
- **`markers-and-metadata.md`** -- Simple markers, JSON markers, index markers, Passthrough markers, combined commands with style + markers + alias
- **`multiline-tables.md`** -- Multiline directives, combined commands with style + multiline + alias
- **`semantic-cross-references.md`** -- Combined commands with style + markers + alias, numeric alias IDs (`#200001` through `#200005`)

### Edge Cases Documented

1. **Whitespace flexibility:** The grammar permits optional whitespace (`ws?`) after `<!--` and before `-->`, and around semicolons in combined commands. Both `<!--style:X-->` and `<!-- style:X -->` are valid.

2. **Combined command with unrecognized segment:** `<!-- style:CustomHeading ; #alias ; TODO: add markers -->` parses as two recognized commands (`style_cmd`, `alias_cmd`) plus one unrecognized segment (`TODO: add markers`). The unrecognized segment MUST NOT affect content processing; its disposition is implementation-defined.

3. **JSON markers in combined commands:** `<!-- markers:{"Key": "val;ue"} ; #alias -->` -- the JSON object is parsed greedily (matching balanced braces), so a semicolon within a JSON string value does not split the segment.

4. **Empty condition block:** `<!--condition:test--><!--/condition-->` is syntactically valid -- the condition wraps zero content lines.

5. **Condition close whitespace:** Both `<!--/condition-->` and `<!-- /condition -->` are valid -- the `ws?` in `mdpp_comment` accommodates the whitespace.

## References

- [CommonMark 0.30 Specification](https://spec.commonmark.org/0.30/) -- Base document format
- [RFC 8259 -- The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259) -- Referenced by `markers_cmd` for JSON object syntax
- [W3C EBNF Notation](https://www.w3.org/TR/xml/#sec-notation) -- Grammar notation used in this document
- [Bryan Ford, "Parsing Expression Grammars: A Recognition-Based Syntactic Foundation" (2004)](https://bford.info/pub/lang/peg.pdf) -- PEG formalism used in the transliteration section
- [Attachment Rule](attachment-rule.md) -- Structural constraints for tag-to-element binding
- [Format Versioning](versioning.md) -- Version declaration syntax and frontmatter processing rules
- [Syntax Reference](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) -- Prose definitions and usage details for all constructs
