---
date: 2026-03-29
status: active
---

<!-- style:Heading1; markers:{"Keywords": "markers, metadata, indexing, SEO", "Description": "How to use markers for search keywords, document metadata, and index entries"}; #300001 -->
# Markers and metadata

[markers-and-metadata]: #300001 "Markers and metadata"

This example demonstrates how Markdown++ markers attach metadata to document elements for search indexing, content management, and generated indexes.

<!-- style:Heading2; #300002 -->
## Document-level metadata

[document-level-metadata]: #300002 "Document-level metadata"

Place markers above the document title to attach metadata to the entire document. `Keywords` and `Description` map to HTML meta tags in web output, improving search engine visibility and content discovery.

The combined command at the top of this file shows the pattern:

```markdown
<!-- markers:{"Keywords": "markers, metadata, indexing", "Description": "How to use markers"}; #300001 -->
# Markers and metadata
```

<!-- style:Heading2; #300003 -->
## Simple vs. JSON format

[simple-vs-json]: #300003 "Simple vs. JSON format"

Use the simple format for a single key-value pair:

<!--marker:Author="Documentation Team"-->
This paragraph has an author marker attached.

Use JSON format when attaching multiple markers:

<!--markers:{"Category": "Reference", "Priority": "high", "Audience": "developers"}-->
This paragraph has three markers: category, priority, and audience.

<!-- style:Heading2; markers:{"IndexMarker": "index entries:creating"}; #300004 -->
## Index entries

[index-entries]: #300004 "Index entries"

Index markers create entries in generated indexes (back-of-book style). They use the `IndexMarker` key with a structured value format.

<!-- marker:IndexMarker="markers:simple format" -->
### Single index entry

A single index entry appears as a top-level item in the generated index.

```markdown
<!--marker:IndexMarker="configuration"-->
## Configuration
```

<!-- marker:IndexMarker="markers:nested entries,index entries:nested" -->
### Nested index entries

Use a colon to create nested entries. The text before the colon is the primary entry; the text after is the sub-entry.

```markdown
<!--marker:IndexMarker="configuration:database"-->
## Database Configuration
```

This produces an index like:

> configuration
>     database .............. 12

<!-- marker:IndexMarker="markers:multiple entries,index entries:multiple" -->
### Multiple index entries

Comma-separated values create multiple independent index entries from a single marker.

```markdown
<!--marker:IndexMarker="projects:creating,output:generating,targets"-->
## Creating Projects
```

This heading appears under three separate index entries: "projects > creating", "output > generating", and "targets".

<!-- style:Heading2; #300005 -->
## Markers combined with other commands

[markers-combined]: #300005 "Markers combined with other commands"

Markers compose with styles and aliases in combined commands. Follow the order: style, marker(s), alias.

<!-- style:Important; marker:Keywords="best practices, conventions"; #300006 -->
### Combined style, marker, and alias

This heading has a custom style, a keywords marker, and a stable alias -- all in one comment directive.

<!-- style:Heading2; #300007 -->
## Common marker keys

[common-marker-keys]: #300007 "Common marker keys"

<!-- style:DataTable -->
| Key | Purpose | Example Value |
|-----|---------|---------------|
| `Keywords` | Search keywords (maps to HTML meta) | `"api, authentication, OAuth"` |
| `Description` | Document summary (maps to HTML meta) | `"How to authenticate API requests"` |
| `IndexMarker` | Generated index entries | `"authentication:OAuth 2.0"` |
| `Author` | Document author | `"Documentation Team"` |
| `Category` | Content categorization | `"Reference"` |
| `Passthrough` | Content that bypasses processing (see [Passthrough content](#passthrough-content) below) | `"<custom-element />"` |

<!-- style:Heading2; #300008 -->
## Passthrough content

[passthrough-content]: #300008 "Passthrough content"

The `Passthrough` marker injects literal content into published output without any Markdown or Markdown++ processing. The marker value is emitted as-is.

<!-- marker:Passthrough="<a id='legacy-anchor'></a>" -->
### Injecting a custom HTML element

The heading above has a Passthrough marker that injects a legacy anchor tag into the output. The heading itself is processed normally -- only the marker value bypasses processing.

```markdown
<!-- marker:Passthrough="<a id='legacy-anchor'></a>" -->
### Injecting a custom HTML element
```

**Note:** The `Passthrough` marker is a recognized Markdown++ directive. It is distinct from regular HTML comments, which are simply ignored by Markdown++ processors. See the [Comment Disambiguation](../plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md#comment-disambiguation) section of the syntax reference for details.
