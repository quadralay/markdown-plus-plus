---
date: 2026-04-06
status: active
---

# MDPP002 Test: Invalid Names Across All Entity Types

This file tests the MDPP002 validation check for invalid names on variables, styles, aliases, and marker keys. Lines marked EXPECT MDPP002 should trigger an error.

---

## POSITIVE CASES (should trigger MDPP002)

### Case 1: Variable with digit-first name -- EXPECT MDPP002

$123start;

### Case 2: Style with digit-first name -- EXPECT MDPP002

<!--style:123BadStyle-->
### Styled Heading Case 2

### Case 3: Style with space in name -- EXPECT MDPP002

<!--style:Bad Style-->
### Styled Heading Case 3

### Case 4: Alias starting with hyphen -- EXPECT MDPP002

<!--#-bad-start-->
### Aliased Heading Case 4

### Case 5: Simple marker with digit-first key -- EXPECT MDPP002

<!--marker:123Key="value"-->
### Marker Heading Case 5

### Case 6: JSON marker with digit-first key -- EXPECT MDPP002

<!--markers:{"123Bad": "val"}-->
### Marker Heading Case 6

### Case 16: Alias with special characters -- EXPECT MDPP002

<!--#bad.alias-->
### Aliased Heading Case 16

### Case 17: Style with special characters -- EXPECT MDPP002

<!--style:Bad!Style-->
### Styled Heading Case 17

---

## NEGATIVE CASES (should NOT trigger MDPP002)

### Case 7: Variable with underscore-first name -- EXPECT no error

$_internal_var;

### Case 8: Style with PascalCase name -- EXPECT no error

<!--style:CustomHeading-->
### Styled Heading Case 8

### Case 9: Alias with digit-first name (valid exception) -- EXPECT no error

<!--#04499224-->
### Aliased Heading Case 9

### Case 10: Alias with numeric-only name -- EXPECT no error

<!--#316492-->
### Aliased Heading Case 10

### Case 11: Condition with hyphenated name -- EXPECT no error

<!--condition:print-only-->
This content is conditioned.
<!--/condition-->

### Case 12: Simple marker with PascalCase key -- EXPECT no error

<!--marker:Keywords="api, documentation"-->
### Marker Heading Case 12

### Case 13: JSON marker with valid keys -- EXPECT no error

<!--markers:{"Keywords": "api", "Description": "API guide"}-->
### Marker Heading Case 13

### Case 14: Style with underscores and hyphens -- EXPECT no error

<!--style:BQ_Warning-Box-->
### Styled Heading Case 14

### Case 15: Alias with underscore-first name -- EXPECT no error

<!--#_private_anchor-->
### Aliased Heading Case 15
