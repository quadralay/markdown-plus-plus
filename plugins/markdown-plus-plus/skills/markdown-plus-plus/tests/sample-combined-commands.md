---
mdpp-version: 1.0
date: 2026-10-03
status: active
---

# Combined-command and container fixture

Fixtures for issue #136: the validator checks every command in a combined comment
tag, sees tags inside blockquotes and on list-item marker lines, and recognizes
code fences at list-relative indentation. Run the validator against this file;
each section states its expected outcome.

```bash
python scripts/validate-mdpp.py tests/sample-combined-commands.md
```

Expected, in line order: MDPP002 (marker key), MDPP003 (broken JSON), MDPP008
(duplicate alias), MDPP002 (alias name), MDPP002 (empty-value marker key),
MDPP003 (unescaped quotes in JSON), MDPP002 (JSON key), MDPP020 (quote in a
simple value), MDPP018 (multiline table in a blockquote), MDPP009 (orphaned tag
in a blockquote), and MDPP020 plus MDPP021 for a `-->` inside a simple value:
seven errors and five warnings, exit code 3. The "Right" sections produce
nothing.

## Wrong -- a marker key in a non-first command (MDPP002)

<!-- style:Note ; marker:1Bad="x" -->
The marker command follows a style command in the same comment tag.

## Wrong -- broken JSON in a non-first command (MDPP003)

<!-- style:Note ; markers:{"Keywords": broken} ; #a1 -->
The JSON object is not the last command in the tag.

## Wrong -- a duplicate of an alias written in a combined tag (MDPP008)

<!-- style:Note ; #dup -->
The first alias is the second command in its tag.

<!-- #dup -->
This alias repeats it.

## Wrong -- an invalid alias name in a combined tag (MDPP002)

<!-- style:Note ; #-bad -->
An alias cannot start with a hyphen.

## Wrong -- an invalid key with an empty value (MDPP002)

<!-- marker:123Bad="" -->
The empty value is allowed; the key is not.

## Wrong -- unescaped quotes inside a JSON value (MDPP003)

<!-- markers:{"Keywords":"alpha", "Description":"say "hi""}; #p1 -->
The inner quotes need to be written as JSON escapes.

## Wrong -- an invalid JSON key followed by an alias (MDPP002)

<!-- markers:{"Bad Key!":"x"}; #p2 -->
The key contains an exclamation mark.

## Wrong -- a quote inside a simple marker value (MDPP020)

<!-- marker:Keywords="say "hi"" -->
A simple-form value cannot contain a double quote.

## Wrong -- a multiline table in a blockquote without separator rows (MDPP018)

> <!-- multiline -->
> | Term | Meaning |
> |------|---------|
> | a1   | b1      |
> | a2   | b2      |

## Wrong -- a tag in a blockquote followed by a blank quote line (MDPP009)

> <!-- style:Note -->
>
> The line holding only `>` breaks the attachment.

## Wrong -- a closing delimiter inside a simple value (MDPP020 and MDPP021)

<!-- marker:Note="a-->b" -->
The first `-->` ends the comment tag and leaves the rest of it as text.

## Right -- a fence indented under a list item

1. Step with a code block:

    ```
    $1bad; <!-- style:123Bad -->
    ```

## Right -- values with semicolons, equals signs, and empty values

<!-- marker:Note="a; b" ; #n1 -->
The semicolon is inside the quoted value.

<!-- marker:Hyperlink="https://example.com/page?id=42" ; marker:DropDownEnd="" -->
The value holds an equals sign; the second value is empty.

## Right -- a tag on a list item's marker line

1. First step.
2. <!-- style:BQ_Note ; #q -->
   > The quote opens this item and receives the style and the alias.

## Right -- a list style above a list item that starts with its own tag

<!-- style:CustomUList -->
- <!-- style:CustomParagraph -->
  The list receives CustomUList; this paragraph receives CustomParagraph.

## Right -- a tag inside a blockquote

> <!-- style:Note ; #n2 -->
> This paragraph receives the style and the alias.

## Right -- syntax quoted in inline code

Writing `<!-- style:123Bad ; #dup -->` or `-->` inside backticks is documentation,
not a directive, and `<!-- # TODO -->` is a regular comment.
