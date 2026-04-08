---
date: 2026-04-08
status: active
---

# Graceful Degradation in Standard Renderers

This appendix documents how each Markdown++ extension renders in a standard CommonMark viewer -- GitHub file views, VS Code preview, MkDocs, or any other tool that does not process Markdown++ extensions. Understanding this behavior helps authors make informed choices about which extensions to use and what reviewers or readers will see.

## Design Principle

Markdown++ extensions use two mechanisms:

- **HTML comment directives** (`<!-- style: -->`, `<!-- include: -->`, `<!-- condition: -->`, etc.) -- invisible in standard renderers
- **Inline tokens** (`$variable_name;`) -- pass through as literal plain text

Because HTML comments are part of the CommonMark specification, any renderer that follows the spec hides them. This makes most Markdown++ extensions truly invisible. The exceptions are inline tokens (variables) and content that depends on processing (file includes, cross-file link resolution).

## Degradation Matrix

| Extension | Syntax Example | CommonMark Rendering | Rating |
|-----------|---------------|----------------------|--------|
| Custom Styles | `<!-- style:Note -->` | Hidden. The styled element renders with default formatting. | Fully graceful |
| Custom Aliases | `<!-- #alias-name -->` | Hidden. Standard heading IDs still work for in-page navigation. | Fully graceful |
| Markers | `<!-- markers:{...} -->` | Hidden. Metadata is simply absent from the rendered view. | Fully graceful |
| Combined Commands | `<!-- style:X ; marker:Y ; #Z -->` | Hidden. Same behavior as individual comment directives. | Fully graceful |
| Inline Styles | `<!--style:Emphasis-->**text**` | Hidden. The formatted element (`**text**`) renders normally. | Fully graceful |
| Content Islands | `<!--style:BQ_Warning-->` + blockquote | Style directive hidden. Blockquote renders with default formatting. No visual distinction between Warning, Tip, and Note types. | Fully graceful |
| Conditions | `<!-- condition:web -->...<!-- /condition -->` | Opening and closing tags hidden, but **all conditional branches are visible**. Readers see every branch regardless of condition. | Partially graceful |
| Multiline Tables | `<!-- multiline -->` | Directive hidden. Table renders as standard GFM, but continuation rows (empty first cell) appear as separate rows. Content is readable but layout differs from intended structure. | Partially graceful |
| Link References | `[slug]: #id "Title"` | Standard Markdown link reference definitions work for in-page links. Cross-file resolution is lost -- links that depend on alias IDs across included files do not resolve. | Partially graceful |
| Variables | `$product_name;` | **Visible as literal text.** Readers see the raw token `$product_name;` in the rendered output. This is the most visible artifact of any extension. | Not graceful |
| File Includes | `<!-- include:path.md -->` | Hidden, but **included content is entirely missing**. A book assembly file renders as effectively blank. Individual content files render normally on their own. | Not graceful |

## Degradation Tiers

### Fully graceful

The extension is invisible or produces equivalent rendering in standard viewers. No visible artifacts. Readers are unaware that extensions are present.

**Extensions:** Custom styles, custom aliases, markers, combined commands, inline styles, content islands.

### Partially graceful

Content is present and readable, but the rendered output differs from what a Markdown++ processor would produce. The differences are visible but generally do not prevent comprehension.

**Extensions:**

- **Conditions** -- All conditional branches appear simultaneously. In a document with `web` and `print` conditions, readers see content for both audiences. This can be confusing in pull request reviews where reviewers may not realize some content is conditional.
- **Multiline tables** -- Continuation rows display as separate table rows with empty first cells. The data is present but the visual grouping is lost.
- **Link references** -- In-page links work. Cross-file links that rely on alias ID resolution across included files do not resolve, producing broken links in multi-file documentation viewed as individual files.

### Not graceful

Content is missing or raw syntax tokens are visible to readers.

**Extensions:**

- **Variables** -- The literal token (e.g., `$product_name;`) appears in rendered text. In documentation that uses variables extensively, this produces a noticeably degraded reading experience. Authors should be aware that GitHub file views, pull request diffs, and editor previews all show raw variable tokens.
- **File includes** -- The include directive is hidden (it is an HTML comment), but the referenced content does not appear. Book assembly files that consist entirely of include directives render as blank pages. Individual content files are unaffected -- they render normally when viewed directly.

## Implications for Authors

**Use freely:** Styles, aliases, markers, inline styles, content islands, and combined commands add publishing capability with zero impact on standard rendering.

**Use with awareness:** Conditions, multiline tables, and link references produce readable but different output. Pull request reviewers see all conditional branches, which may need explanation in review comments.

**Use deliberately:** Variables and file includes produce visible artifacts. Teams that rely on GitHub or editor previews as part of their review workflow should understand that variable tokens will be visible and include content will be absent. These extensions deliver their value during publishing, not during preview.
