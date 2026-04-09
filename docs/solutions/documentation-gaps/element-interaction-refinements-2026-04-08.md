---
title: Element interaction refinements — list item naming sub-rule and link style placement exception
date: 2026-04-08
category: documentation-gaps
module: specification
problem_type: documentation_gap
component: documentation
symptoms:
  - "List item compound naming mechanism (ContainerStyle + 'Item') undocumented"
  - "Link style tag placement exception (inside brackets, not before them) undeclared"
  - "Authors had no reference for why link styling differs from other inline elements"
  - "List item naming appeared as a special case in examples but had no formal sub-rule"
root_cause: inadequate_documentation
resolution_type: documentation_update
severity: medium
tags:
  - element-interactions
  - list-item-naming
  - link-placement
  - inline-styles
  - compound-naming
  - attachment-rule
---

# Element interaction refinements — list item naming sub-rule and link style placement exception

## Problem

After the element interactions specification was created (issue #9), the review phase (PR #40) identified two undocumented special cases: (1) the list item compound naming mechanism where items receive a `ContainerStyle + "Item"` suffix, and (2) the link style tag placement exception where the tag goes inside the link text brackets rather than before the opening bracket.

## Symptoms

- List item naming appeared in compound naming examples but had no formal sub-rule — implementors had to infer the "Item" suffix behavior from examples alone
- The link style placement exception was undeclared — the general inline rule ("tag immediately before the element") contradicted the actual link syntax where the tag goes inside `[...]`
- The attachment rule document stated inline tags must appear "immediately before the styled element" with no link exception noted
- Authors writing `<!--style:CustomLink-->[text](url)` (before the bracket) would get incorrect behavior, with no spec guidance pointing to the correct form `[<!--style:CustomLink-->text](url)`

## What Didn't Work

The original element interactions spec (#9) documented the style type taxonomy, default names, compound naming, and heading alias generation comprehensively but left these two edge cases implicit. The list item naming was visible in examples (the table showed "OList Item" and "UList Item") but the mechanism producing those names was never formalized as a rule. The link placement was described in the Links section but was not called out as an exception to the general inline rule in the attachment rule or syntax reference.

## Solution

Three files updated with targeted additions:

**`spec/element-interactions.md`** — Two new sections added:

1. **List Item Naming Sub-Rule** (after the general compound naming rule): Formal rule `ListStyle + space + "Item"` where ListStyle is the custom name or default ("OList"/"UList"). Includes a table showing all four combinations (ordered/unordered x default/custom), clarifies that "Item" is a fixed structural suffix not independently customizable, and shows how the sub-rule interacts with the general compound naming rule (both apply simultaneously — items get "Item" suffix, content within items gets compound names).

2. **Link Placement Exception** (in the Links section): Explicit declaration that links are the one exception to the general inline placement rule. Style tags go inside the link text brackets (`[<!--style:Name-->text](url)`), not before the opening `[`. Includes a comparison table showing all inline elements' placement rules side by side.

**`spec/attachment-rule.md`** — Updated the formal statement for inline tags to note the link exception with a cross-reference to the element interactions spec.

**`plugins/.../references/syntax-reference.md`** — Updated the Inline Placement section to separate the general rule from the link exception, with corrected examples and a cross-reference to the full spec.

## Why This Works

Both issues were cases where the spec documented the *what* (examples showing correct syntax) but not the *why* (the formal rule producing that syntax). The list item naming was a pattern visible in tables but never extracted as a named rule. The link placement was correct in context but contradicted by the general inline rule stated elsewhere. Formalizing both as explicit rules with cross-references eliminates the ambiguity and prevents implementors from having to infer behavior from examples.

## Prevention

1. **Extract named rules from example patterns.** When multiple examples in a spec share a common pattern (like "Item" appearing in every list item name), extract the pattern as a named sub-rule rather than leaving it implicit. Examples demonstrate; rules specify.

2. **Audit general rules for exceptions after writing.** When a spec states a general rule ("inline tags go before the element"), systematically check whether every element type follows it. Document exceptions at both the general rule site and the element-specific site.

3. **Use comparison tables for placement rules.** The inline placement comparison table (showing all elements side by side) makes exceptions immediately visible. Future element additions should be added to this table.

4. **Cross-reference exceptions bidirectionally.** The link exception is now noted in three places: the attachment rule, the syntax reference, and the element interactions spec. This ensures an implementor finds the exception regardless of which document they read first.

## Related Issues

- [#49](https://github.com/quadralay/markdown-plus-plus/issues/49) — This issue: element interaction refinements
- [#9](https://github.com/quadralay/markdown-plus-plus/issues/9) — Document element interactions (parent issue that created the spec)
- [#10](https://github.com/quadralay/markdown-plus-plus/issues/10) — Attachment rule (updated with link exception)
- `docs/solutions/documentation-gaps/element-interactions-spec-gap-2026-04-08.md` — The parent learning documenting the initial #9 spec creation
