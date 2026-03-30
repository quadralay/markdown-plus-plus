---
date: 2026-03-29
status: active
---

# MDPP009 Test: Orphaned Comment Tags

This file tests the MDPP009 validation check for orphaned comment tags.
Lines marked EXPECT MDPP009 should trigger a warning.

---

## POSITIVE CASES (should trigger MDPP009)

### Case 1: Style tag with blank line before content

<!-- style:CustomHeading -->

## This heading is NOT styled (blank line breaks attachment)

### Case 2: Alias tag with blank lines on both sides

<!-- #orphaned-alias -->

This paragraph does not receive the alias.

### Case 3: Marker between heading and paragraph (blank line above content)

## Some Heading

<!-- marker:IndexMarker="orphaned" -->

This paragraph has a gap above.

### Case 4: Combined tag orphaned by blank line

<!-- style:Note ; #my-alias ; marker:Keywords="test" -->

This paragraph is not reached by the combined tag.

### Case 5: Tag at end of file section with no following content nearby

## Another Section

Some content here.

<!-- style:Trailing -->

### Case 6: Tag followed by only blank lines

<!-- style:Dangling -->



More content much later (but blank lines already broke it).

### Case 7: Multiple orphaned tags in sequence (each warns independently)

<!-- style:First -->

<!-- style:Second -->

Paragraph after two orphaned tags.

### Case 8: Separate tags on consecutive lines (top tag is orphaned)

<!-- style:TopTag -->
<!-- #bottom-tag -->
## Heading below two separate tags

---

## NEGATIVE CASES (should NOT trigger MDPP009)

### Case 9: Style tag directly above heading

<!-- style:ValidHeading -->
## This heading IS styled

### Case 10: Alias tag directly above paragraph

<!-- #valid-alias -->
This paragraph receives the alias.

### Case 11: Marker at file start position directly above content

<!-- marker:IndexMarker="valid" -->
Paragraph with a valid marker attachment.

### Case 12: Combined tag directly above element

<!-- style:Callout ; #combined ; marker:Keywords="valid" -->
This paragraph receives all three commands.

### Case 13: Condition tags (exempt -- wraps content)

<!--condition:web-->
This content only appears in web output.
<!--/condition-->

### Case 14: Include directive (exempt -- standalone)

<!-- include:shared-header.md -->

### Case 15: Inline style tag on same line as content

This has <!--style:Emphasis-->**inline styled bold** text.

### Case 16: Multiline tag directly above table

<!-- multiline -->
| Header 1 | Header 2 |
|----------|----------|
| Cell with
  multiple lines | Another cell |

### Case 17: Style tag inside a condition block, directly above content

<!--condition:print-->
<!-- style:PrintHeading -->
## Print-Only Heading
<!--/condition-->

### Case 18: Tag inside a fenced code block (ignored entirely)

```markdown
<!-- style:InsideCodeFence -->

This is just an example, not real MDPP processing.
```

### Case 19: Regular HTML comment (not an MDPP pattern)

<!-- This is a regular comment, not a Markdown++ tag -->
## Heading after regular comment
