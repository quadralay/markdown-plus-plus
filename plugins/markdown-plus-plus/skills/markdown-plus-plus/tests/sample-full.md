<!--markers:{"Keywords": "test, sample, complete, all-features", "Description": "Complete feature test for all Markdown++ extensions"} ; #document-start-->
# $product_name; Complete Feature Test

This document tests all Markdown++ extensions for validation purposes.

## Variables Test

Basic variable: $product_name;

Multiple variables: $product_name; version $version; by $author;

Variable in formatting: **$product_name;** and *$version;*

Variable in link text: [$product_name; Download]($download_url;)

Variables with special chars: $my-var; and $my_var; and $var2;

## Custom Styles Test

### Block-Level Styles

<!--style:CustomHeading-->
# Styled Heading Level 1

<!--style:CustomHeading2-->
## Styled Heading Level 2

<!--style:NoteBlock-->
> This blockquote has a custom style applied.
> It spans multiple lines.

<!--style:CodeExample-->
```python
def hello():
    """A styled code block."""
    print("Hello, $product_name;")
```

<!--style:CustomList-->
- Styled list item 1
- Styled list item 2
- Styled list item 3

<!--style:CustomParagraph-->
This entire paragraph has a custom style. It contains **bold**, *italic*, and `code` formatting.

### Inline Styles

Text with <!--style:Emphasis-->**inline styled bold**.

Text with <!--style:ProductName-->*$product_name;* inline.

A <!--style:ImportantLink-->[styled link](https://example.com) in text.

## Custom Aliases Test

<!--#introduction-->
## Introduction Section

This section has a custom alias.

<!--#getting-started-->
## Getting Started Section

Another aliased section.

<!--#detailed-alias-name-with-hyphens-->
### Section with Long Alias

<!--#alias_with_underscores-->
Aliases can have hyphens and underscores.

### Links to Aliases

- See [Introduction](#introduction)
- See [Getting Started](#getting-started)
- See [Document Start](#document-start)

## Conditions Test

### Basic Conditions

<!--condition:web-->
Web-only content block.

This entire section only appears in web output.
<!--/condition-->

<!--condition:print-->
Print-only content block.

This section is for printed documentation.
<!--/condition-->

### NOT Operator

<!--condition:!internal-->
This appears when "internal" condition is hidden (external users).
<!--/condition-->

<!--condition:!draft-->
This appears when NOT in draft mode.
<!--/condition-->

### AND Operator (space)

<!--condition:web production-->
This appears when BOTH "web" AND "production" are visible.
<!--/condition-->

### OR Operator (comma)

<!--condition:web,print-->
This appears in EITHER web OR print output.
<!--/condition-->

### Complex Expressions

<!--condition:!internal,web-->
This means: NOT internal OR web
Appears if internal is hidden OR web is visible.
<!--/condition-->

<!--condition:!draft,web production-->
This means: (!draft) OR (web AND production)
Complex precedence example.
<!--/condition-->

### Nested Conditions

<!--condition:web-->
Web content starts here.

<!--condition:advanced-->
Advanced web content (nested condition).
<!--/condition-->

Regular web content continues.
<!--/condition-->

### Inline Conditions

Contact: <!--condition:web-->[email@example.com](mailto:email@example.com)<!--/condition--><!--condition:print-->see back cover<!--/condition-->.

Version: $version; <!--condition:!production-->(Development Build)<!--/condition-->

## File Includes Test

The following would include files (commented for testing):

<!-- Note: These are example includes - files don't exist in test -->
<!-- <!--include:shared/header.md--> -->
<!-- <!--include:../common/footer.md--> -->
<!-- <!--include:chapters/introduction.md--> -->

## Markers Test

<!--markers:{"Keywords": "test, sample, full", "Priority": "high"} ; #json-format-->
### JSON Format

This section demonstrates JSON format for multiple markers.

<!--marker:Keywords="api, documentation"-->
### Simple Format

This section demonstrates simple format for a single marker.

<!--markers:{"Keywords": "multiple, test", "Category": "Test"} ; #multiple-markers-->
### Multiple Markers (JSON Format Required)

This section demonstrates that multiple markers require JSON format.

<!--marker:Section="features"-->
## Features Section

This section has an associated marker.

## Multiline Tables Test

### Basic Multiline

<!-- multiline -->
| Feature   | Description              |
|-----------|--------------------------|
| Variables | Store reusable values.   |
|           | Use `$name;` syntax.     |
|           |                          |
| Styles    | Apply formatting.        |
|           | Supports block & inline. |

### Multiline with Lists

<!-- multiline -->
| Step | Actions                  |
|------|--------------------------|
| 1    | First step:              |
|      | - Sub-action A           |
|      | - Sub-action B           |
|      | - Sub-action C           |
|      |                          |
| 2    | Second step:             |
|      | 1. Do this first         |
|      | 2. Then do this          |
|      | 3. Finally do this       |

### Multiline with Blockquotes

<!-- multiline -->
| Topic   | Notes                    |
|---------|--------------------------|
| Warning | Important:               |
|         | > **Note:** Be careful   |
|         | > when making changes.   |
|         |                          |
| Tip     | Helpful hint:            |
|         | > Use aliases for stable |
|         | > URL endpoints.         |

### Multiline with Block Styling

<!-- multiline -->
| Name | Details                  |
|------|--------------------------|
| Bob  | Lives in Dallas.         |
|      | <!-- style:Hobbies -->   |
|      | - Enjoys cycling         |
|      | - Loves cooking          |
|      |                          |
| Mary | Lives in El Paso.        |
|      | - Works as a teacher     |
|      | - Likes painting         |

### Multiline with Inline Styling

<!-- multiline -->
| Topic | Description              |
|-------|--------------------------|
| Intro | This paragraph has       |
|       | <!--style:Emphasis-->**important** inline styling. |

### Multiline with Alignment

<!-- multiline -->
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| L-align  | Centered | R-align  |
|          | text     | content  |

## Combined Commands Test

### Order Priority (style, multiline, marker(s), #alias)

<!-- style:CustomHeading ; marker:Keywords="intro" ; #combined-example -->
## Combined Style, Marker, and Alias Heading

<!-- style:DataTable ; multiline ; #feature-table -->
| Column | Data                     |
|--------|--------------------------|
| Cell   | Multi-line content       |
|        | - Item 1                 |
|        | - Item 2                 |

### Style + Marker

<!-- style:ImportantSection ; marker:Priority="high" -->
## Important Section with Marker

### Style + Alias + Marker

<!-- style:FeatureBox ; marker:Keywords="feature, priority" ; #feature-1 -->
### Feature with All Attributes

## Inline Styling Test

### Styled Images

<!--style:CustomImage-->![Logo](images/logo.png "Company Logo")

<!--style:ScreenshotStyle-->![Settings Screen](images/settings.png)

### Styled Links

See the [<!--style:ImportantLink-->**API Reference**](api.md#auth) for details.

Visit [<!--style:ExternalLink-->*documentation*](https://docs.example.com).

## Content Islands Test

<!--style:BQ_Learn-->
> ## Learning Section
>
> This blockquote contains multiple elements:
>
> - Bullet point 1
> - Bullet point 2
>
> ```python
> def example():
>     return "Code inside blockquote"
> ```
>
> Final paragraph in the content island.

<!--style:BQ_Warning-->
> **Warning:** This is a styled warning block.
>
> Take note of the following:
> 1. First consideration
> 2. Second consideration

## Nested Lists Test

### Basic Nested List with Single Style

<!--style:ProcedureList-->
1. First step
   - Sub-item A
   - Sub-item B
2. Second step
   1. Nested numbered item
   2. Another nested item
3. Third step

### Nested List with Multiple Styles (Proper Indentation)

<!-- style:BulletList1 -->
- Bullet 1

  <!-- style:BulletList2 -->
  - Bullet 2

    <!-- style:BulletList3 -->
    - Bullet 3

## Edge Cases

### Variable-like Text

Not a variable: $ standalone dollar sign
Not a variable: $no-semicolon
Not a variable: $with space;

### Empty Condition

<!--condition:test-->
<!--/condition-->

### Condition with Only Whitespace

<!--condition:whitespace-->

<!--/condition-->

### Style with Extra Whitespace

<!-- style:SpacedStyle -->
## Heading with Spaced Style Tag

## Document End

This completes the full Markdown++ feature test document.
