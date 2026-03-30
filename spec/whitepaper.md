---
date: 2026-03-30
status: draft
---

# Markdown++: professional publishing power, plain text simplicity

## The documentation format dilemma

Technical writing teams face an old tension: power vs. simplicity.

On one side sit the heavyweight formats -- DITA XML, DocBook, Adobe FrameMaker. They handle structured content, conditional processing, content reuse, and multi-format output. But they demand XML expertise, specialized tooling, and complex build pipelines. Source files are hard to read, painful to diff, and hostile to contributors who aren't full-time documentation specialists.

On the other side sits Markdown. Readable, diffable, universally supported, welcoming to every contributor from junior developer to senior technical writer. But standard Markdown lacks the publishing features that professional documentation requires: no conditional content, no variables, no structured cross-references, no custom styling, no multi-format output pipeline.

Teams choose one or the other. Adopt a powerful but complex format and accept the overhead. Or adopt Markdown and accept its limitations, patching gaps with framework-specific extensions (MDX, AsciiDoc, reStructuredText) that trade portability for capability.

Markdown++ resolves this. It adds professional publishing features through extensions that are invisible to standard Markdown renderers -- every Markdown++ file is a valid CommonMark document that renders cleanly in GitHub, VS Code, MkDocs, and any other Markdown viewer. When processed by a publishing tool, those invisible extensions activate and produce multi-format output with the sophistication that technical documentation demands.

This whitepaper explains what Markdown++ is, how it compares to the formats you may be using today, and why it is a better approach to technical documentation.

## What is Markdown++?

Markdown++ is a documentation format built on the CommonMark specification. Every Markdown++ feature uses one of two extension mechanisms:

- **HTML comment directives** -- `<!-- style: -->`, `<!-- include: -->`, `<!-- condition: -->`, `<!-- markers:{} -->`
- **Inline tokens** -- `$variable_name;` (escaped with backslash when a literal dollar-semicolon sequence is needed: `\$`)

Standard Markdown renderers treat HTML comments as invisible and pass inline tokens through as plain text. This means every `.md` file authored in Markdown++ is a valid CommonMark document. There is no proprietary syntax, no custom file extension, and no build step required just to preview your content.

This is the core design decision. Authors are never locked into a proprietary format. A Markdown++ file works in every tool that supports Markdown -- and gains professional publishing capabilities when processed by a tool that understands the extensions. Because the extension syntax is openly documented and built on standard HTML comments and inline tokens, any tool or AI agent can be adapted to process Markdown++ content. That's a different proposition from proprietary binary formats that require vendor-specific parsers and are opaque to AI-assisted workflows.

## Built on three decades of publishing expertise

Markdown++ did not emerge from a startup experiment or an academic research project. Its design draws on three decades of real-world structured authoring and multi-format output generation at Quadralay / WebWorks, where publishing pipelines have been built and refined since the early 1990s.

**Structured authoring.** WebWorks began with Adobe FrameMaker integration in the early 1990s, when FrameMaker was the dominant tool for complex technical documentation. That deep understanding of structured content -- book hierarchies, conditional text, variables, cross-references, index markers -- informed every subsequent format WebWorks supported. Microsoft Word publishing support followed in 2005, and DITA XML support arrived in 2007 as the industry moved toward XML-based content reuse. By the time Markdown++ was developed, WebWorks had already built publishing pipelines for every major structured authoring format in the industry.

**Online help output.** WebWorks has shipped seven generations of web-based help output, beginning with WebWorks Help 1.0 in 1997 -- one of the earliest HTML-based help systems. Each generation addressed the limitations of the last: WebWorks Help 2.0 (2000) introduced XML-driven architecture, separating content from presentation. Help 3.0 and 4.0 brought cross-browser compatibility and template-driven publishing. Help 5.0 added dynamic JavaScript-enabled interaction. WebWorks Reverb moved to a fully web-native delivery model, and Reverb 2.0 delivers responsive HTML5 output with modern search, navigation, and accessibility. That's seven generations over nearly three decades, from static HTML help files to a full web application.

**Markdown and Markdown++.** WebWorks added Markdown as an input format in 2017 as documentation shifted toward developer-centric and agile workflows. Markdown++ followed in 2020, evolving from that foundation: rather than building a new proprietary format, WebWorks extended CommonMark using the invisible-extension pattern (HTML comments and inline tokens) to bring the same structured authoring capabilities -- the ones refined through decades of FrameMaker, Word, and DITA processing -- to the simplest and most widely adopted authoring format in the industry.

The result is a documentation format shaped by experience processing millions of pages across every major authoring format and seven generations of publishing tools. Markdown++ is not theoretical -- it is production software with a long lineage.

## Key benefits

### 1. Full CommonMark backward compatibility

Every Markdown++ extension is syntactically invisible to standard renderers. A file containing `<!-- style:Note -->` followed by a paragraph renders in GitHub as a normal paragraph -- the style directive is hidden as an HTML comment. A variable reference like `$product_name;` appears as literal text in a preview but resolves to the configured value during publishing.

This means Markdown++ files work cleanly in:

- **GitHub** -- file views, pull request diffs, code review
- **VS Code, JetBrains, and other editors** -- standard Markdown preview
- **Documentation sites** -- MkDocs, Docusaurus, Jekyll, Hugo
- **Any CommonMark-compliant viewer** -- with no plugins or configuration

We are not aware of another documentation format with comparable publishing power that renders this cleanly in standard tools.

### 2. Dual-use files: standalone and composite

The same `.md` file works in two contexts without modification:

- **Standalone** -- viewed, edited, linked, and published as an individual document
- **Composite** -- assembled into multi-file publications using `<!-- include: -->` directives

A book structure file defines the assembly order for a publication:

```markdown
<!-- include:../content/chapter-01-overview.md -->
<!-- include:../content/chapter-02-configuration.md -->
<!-- include:../common/boilerplate/trademarks.md -->
```

The book file contains no authored content -- it is purely an assembly manifest. Each included file is a self-contained document that can be edited, previewed, and linked independently. The same chapter or boilerplate file can appear in multiple publications. Authors work on individual files without merge conflicts in a monolithic document. Add or remove `<!-- include: -->` lines to change what a publication contains. Legal notices, terminology tables, and common boilerplate live in one location.

Adopting composite publishing does not change how individual documents are authored or previewed. The transition from single-file to multi-file documentation is incremental.

### 3. Semantic cross-references that work everywhere

Cross-referencing in multi-file documentation has always been fragile. Markdown++ introduces a link reference pattern that bridges alias IDs (used by publishing tools for stable cross-file linking) with standard Markdown heading anchors (used by renderers for in-page navigation):

```markdown
<!-- style:Heading1; #316492 -->
## About IPsec Peering Connections

[about-ipsec-peering-connections]: #316492 "About IPsec Peering Connections"
```

The semantic slug (`about-ipsec-peering-connections`) is derived from the heading text. Cross-references use this slug:

```markdown
See [About IPsec Peering Connections][about-ipsec-peering-connections] for details.
```

In standard Markdown, heading links are auto-generated from the heading text -- change the heading, break every link that points to it. Across a large documentation set, a single heading rename can require dozens of edits. The semantic slug and alias ID in Markdown++ decouple the link target from the heading text, so references remain stable as content evolves.

This single reference resolves correctly in every context: standard Markdown viewers treat the slug as a heading anchor (working in-page link), standalone publishing keeps internal links intact, composite assemblies resolve the alias ID across all included files, and multi-document projects use the numeric identifier for cross-file linking.

One reference, every output context.

### 4. Professional publishing without leaving Markdown

Markdown++ adds the publishing capabilities that technical writers need without changing the authoring format:

- **Custom styles** -- `<!-- style:Note -->`, `<!-- style:Important -->`, `<!-- style:Warning -->` map content to any output styling without embedding CSS classes or presentation markup in the source.
- **Variables** -- `$product_name;`, `$version;`, `$release_date;` define reusable values managed centrally and resolved during publishing.
- **Conditional content** -- `<!-- condition:online -->...<!-- /condition -->` shows or hides content based on output format, audience, or any defined condition.
- **Metadata markers** -- `<!-- markers:{"Keywords": "IPsec, peering", "Description": "How to configure peering connections"} -->` attaches metadata for SEO, search indexing, and content management.
- **Multiline tables** -- `<!-- multiline -->` allows table cells with block elements, lists, wrapped text, and continuation rows.

These cover the same ground as Word, FrameMaker, and DITA content enrichment features. The difference: the source files stay readable plain text.

### 5. Documentation-as-code workflow

Because Markdown++ files are plain text, they fit into development workflows without friction:

- **Version control** -- Every change produces a meaningful diff, including changes to table content when tables use readable fixed-width formatting.
- **Pull request reviews** -- Reviewers see exactly what changed in source content, not a binary diff or an opaque XML restructuring.
- **CI/CD integration** -- Command-line build tools run automated builds triggered by commits or merges.
- **Branch-based authoring** -- Feature branches for content changes, reviewed and merged through the same process as code.
- **Golden testing** -- Pretty-printed output baselines enable regression testing: generate output, compare against a known-good baseline, detect unintended changes.

These workflows work today with standard Git hosting, standard CI/CD pipelines, and standard code review tools. No documentation-specific infrastructure is required beyond the publishing tool itself.

### 6. Multi-format publishing pipeline

A publishing tool that supports Markdown++ transforms source files into multiple output formats from a single source. A Markdown++ publishing pipeline can produce:

- **Responsive HTML5 online help** -- Web-based help output with full-text search, table of contents navigation, and index.
- **PDF** -- Via XSL-FO transformation for print-ready and archival documentation.
- **Dynamic HTML** -- Generic HTML output for integration into websites and portals.
- **Microsoft HTML Help (CHM)** -- Compiled help for Windows desktop applications.
- **Eclipse Help** -- For Eclipse-based IDE documentation.

The same `<!-- style: -->` directives, variables, conditions, and markers apply across all output formats. Write once, publish to any target. The processing tool applies the project's style mappings and output configuration to produce each format.

### 7. Structured content without XML overhead

Markdown++ provides structured content capabilities comparable to DITA and DocBook, without requiring authors to write or maintain XML:

| Capability | DITA / DocBook | Markdown++ |
|---|---|---|
| Topic-based authoring | XML topics + maps | `.md` files + `<!-- include: -->` |
| Conditional content | `@audience`, `@platform` attributes | `<!-- condition: -->` |
| Content reuse | conref, conkeyref | `<!-- include: -->`, variables |
| Metadata | `<prolog>`, `<metadata>` elements | `<!-- markers:{} -->` |
| Cross-references | `<xref>`, `@href` | `[text][slug]` with link reference definitions |
| Index entries | `<indexterm>` nesting | `<!-- markers:{"IndexMarker": "..."} -->` |
| Custom styling | DITA specialization | `<!-- style: -->` directives |
| Nested structures in tables | XML nesting within `<entry>` | `<!-- multiline -->` with embedded styles |
| Content islands / callouts | `<note>`, `<hazardstatement>` | Styled blockquotes (`<!-- style:BQ_Warning -->`) |
| Nested styled lists | `<steps>`, `<substeps>` | Standard list nesting with `<!-- style: -->` |
| Source readability | XML tags throughout | Plain text with invisible comments |

For the capabilities that most technical writing teams use daily, Markdown++ covers the ground that DITA and DocBook occupy -- with dramatically simpler source files. Some advanced DITA features (relationship tables, specialization constraints, key scoping, XLIFF-based localization workflows) do not have direct Markdown++ equivalents. For teams that rely heavily on those features, DITA's ecosystem tooling remains deeper. For teams that need structured content without XML overhead, the readability gap is enormous. A DITA topic requires XML declarations, namespaces, nested elements, and closing tags. A Markdown++ file reads like a document.

### 8. Advanced content structures

Professional documentation frequently needs more than paragraphs and flat lists -- procedure steps with nested sub-steps, warning callouts containing tables or code examples, table cells with embedded lists and styled content. Markdown++ handles all of these through natural extensions of standard Markdown constructs.

**Content islands using blockquotes.** Styled blockquotes act as self-contained content regions -- learning boxes, warnings, tips, important notices -- with full nested content including headings, lists, tables, and code blocks:

```markdown
<!--style:BQ_Warning-->
> **Warning: Data Loss Risk**
>
> Before proceeding, ensure you have:
>
> - Backed up your current configuration
> - Saved all open documents
> - Closed other applications using the database
>
> This operation cannot be undone.
```

```markdown
<!--style:BQ_Tip-->
> **Pro Tip: Keyboard Shortcuts**
>
> Speed up your workflow:
>
> | Action | Windows | macOS |
> |--------|---------|-------|
> | Save | Ctrl+S | Cmd+S |
> | Find | Ctrl+F | Cmd+F |
> | Replace | Ctrl+H | Cmd+H |
>
> See [Keyboard Reference](shortcuts.md#all-shortcuts) for the complete list.
```

In a standard Markdown viewer, these render as indented blockquotes with their full internal structure visible. When processed by a publishing tool, the style directive maps to the appropriate visual treatment -- colored borders, background shading, iconography -- for each output format.

**Nested lists with styling.** Procedures, checklists, and hierarchical content use standard Markdown list nesting with style directives that control output formatting:

```markdown
<!--style:ProcedureList-->
1. **Download the installer**
   - Select your platform:
     - Windows 10/11 (64-bit)
     - macOS 12+ (Apple Silicon or Intel)
     - Linux (deb or rpm package)

2. **Run the installer**
   - Windows:
     1. Double-click the `.exe` file
     2. Accept the UAC prompt
     3. Follow the wizard
   - macOS:
     1. Open the `.dmg` file
     2. Drag to Applications
```

The `<!-- style:ProcedureList -->` directive tells the publishing tool how to render the list -- numbered steps, lettered sub-steps, bullet formatting -- without embedding any presentation markup in the source. In a standard Markdown preview, the list renders with default nesting, which is already readable and useful.

**Rich table cells with embedded structures.** The `<!-- multiline -->` directive allows table cells to contain lists, styled content, and continuation rows -- the kind of thing you need for feature comparisons, requirements matrices, and API reference tables:

```markdown
<!-- style:DataTable ; multiline ; #comparison-table -->
| Feature        | Description              | Status      |
|----------------|--------------------------|-------------|
| Authentication | OAuth 2.0 implementation |             |
|                | Supports:                | Complete    |
|                | - Authorization Code     |             |
|                | - Client Credentials     |             |
|                | - Refresh tokens         |             |
|                |                          |             |
| Rate Limiting  | Per-endpoint limits      |             |
|                | - Default: 100 req/min   | In Progress |
|                | - Maximum: 1000 req/min  |             |
```

Multiline tables use continuation rows (empty first cell) to extend a logical row across multiple physical lines, with empty separator rows marking cell boundaries. Combined commands on a single directive -- style, multiline, and alias -- demonstrate how multiple extensions compose naturally.

In DITA, the same structures require `<note>` elements with typed attributes, `<steps>` and `<substeps>` elements with mandatory `<cmd>` children, and `<entry>` elements with nested XML block structures inside `<simpletable>` or `<table>`. The XML overhead is substantial, and the source is hard to read or review in a pull request. Markdown++ gets the same structural capability while keeping source files as plain text.

## Migration paths

### From Microsoft Word

**What you gain:** Version control with meaningful diffs, no binary format lock-in, concurrent editing without track changes conflicts, pull request reviews for content changes, and automated build pipelines.

**What you keep:** Custom paragraph and character styling (via `<!-- style: -->` directives that map to the same output styles), document structure via headings, image references, and tables.

**How you migrate:** If you use a publishing tool that supports both Word input and Markdown++/Markdown output, the migration path is direct. The tool generates Markdown++/Markdown from your Word documents, preserving style mappings (Markdown++) and publishing pipeline configuration. The generated Markdown++/Markdown files become your new source documents -- same output quality, but now plain text and version controlled. If your tool only generates Markdown, you can post-edit the Markdown files to insert specific features as needed. Markdown++ was designed to be minimalistic -- add the Markdown++ syntax only where you need it.

### From Adobe FrameMaker

**What you gain:** A modern, cross-platform toolchain with no proprietary binary format, Git-based workflows, and an editing experience open to any text editor or IDE.

**What you keep:** Book structure (FrameMaker `.book` files map directly to Markdown++ book assembly files using `<!-- include: -->` directives), conditional text, variables, cross-references, and index markers.

**How you migrate:** The structural mapping is direct. A FrameMaker book file that defines chapter order becomes a Markdown++ book file with `<!-- include: -->` lines. Chapter files become individual `.md` files. Conditional text expressions become `<!-- condition: -->` directives. Variables become `$variable;` tokens. The chapter structure and content hierarchy are preserved; the authoring format becomes dramatically simpler.

### From DITA XML

**What you gain:** Dramatically simpler syntax, no XML overhead, readable source files, and a lower barrier to entry for contributors who are not XML specialists.

**What you keep:** Topic-based authoring, content reuse, conditional processing, metadata, and multi-format output.

**How you migrate:** DITA maps become Markdown++ book structure files with `<!-- include: -->` directives. DITA topics become `.md` files. Topic specialization maps to `<!-- style: -->` directives. Conref and conkeyref reuse patterns map to `<!-- include: -->` for file-level reuse and `$variable;` for value-level reuse. Where DITA conref provides element-level reuse (pulling a single paragraph or list item from within a topic), Markdown++ operates at the file level -- granular reuse requires restructuring shared content into its own files, which is typically a limited refactoring effort. The conceptual model -- topics assembled into maps with conditional processing and metadata -- remains the same. The syntax becomes plain text.

### From Other Markdown Systems (MDX, AsciiDoc, rST)

**What you gain:** Full CommonMark compatibility (no JSX expressions, no custom block syntax, no build step required for preview), and access to a professional multi-format publishing pipeline.

**What you keep:** Plain text authoring, Git-based workflows, and standard Markdown syntax for all content structure (headings, lists, tables, code blocks, links, images).

**Key differentiator:** Other Markdown-based systems add capabilities by introducing non-standard syntax. MDX adds JSX expressions that break standard renderers. AsciiDoc uses its own syntax that is not Markdown. reStructuredText has a different markup language entirely. Markdown++ adds capabilities through HTML comments and inline tokens that standard renderers handle gracefully. For AsciiDoc, an open-source converter ([asciidoctor-mdpp](https://github.com/quadralay/asciidoctor-mdpp)) automates the migration to Markdown++. For MDX and rST, migration is manual -- but the target format is maximally compatible with the Markdown ecosystem you already use.

## Worked example

### Part A: DITA XML vs. Markdown++

Consider a documentation section describing IPsec peering connections for a network security appliance. Here is the same content expressed in DITA XML and Markdown++:

**DITA XML:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Topic//EN" "topic.dtd">
<topic id="about-ipsec-peering">
  <title>About IPsec Peering Connections</title>
  <prolog>
    <metadata>
      <keywords>
        <keyword>IPsec</keyword>
        <keyword>peering</keyword>
        <indexterm>IPsec<indexterm>peering connections</indexterm></indexterm>
      </keywords>
    </metadata>
  </prolog>
  <body>
    <p>The NetGuard Controller communicates with server-side StreamEdge appliances
    through an encrypted peering connection using IPsec.</p>
    <p>To enable peering, configure these settings:</p>
    <ul>
      <li>SSL certificate exists &#x2014; StreamEdge appliances are supplied
      with a self-signed certificate during manufacturing.</li>
      <li>Primary interface is configured &#x2014; The primary interface on
      both appliances is used for the peering connection.</li>
      <li>IPsec is enabled on the primary interface &#x2014; Secure peering
      requires IPsec to be enabled.</li>
      <li>IKE authentication mode is configured:
        <ul>
          <li>Shared secret &#x2014; Uses a shared secret between peers.</li>
          <li>Certificate &#x2014; Uses self-signed certificates.</li>
        </ul>
      </li>
    </ul>
    <p>For details, see
    <xref href="configuring-netguard.dita#configuring-netguard"
          format="dita">Configuring NetGuard Controller</xref>.</p>
  </body>
</topic>
```

**Markdown++:**

```markdown
<!-- style:Heading1; markers:{"IndexMarker": "IPsec: peering connections"}; #316492 -->
## About IPsec Peering Connections

[about-ipsec-peering-connections]: #316492 "About IPsec Peering Connections"

The NetGuard Controller communicates with server-side StreamEdge appliances through an encrypted peering connection using IPsec.

To enable peering, configure these settings:

- SSL certificate exists -- StreamEdge appliances are supplied with a self-signed certificate during manufacturing.

- Primary interface is configured -- The primary interface on both appliances is used for the peering connection.

- IPsec is enabled on the primary interface -- Secure peering requires IPsec to be enabled.

- IKE authentication mode is configured:

  - Shared secret -- Uses a shared secret between peers.

  - Certificate -- Uses self-signed certificates.

See [Configuring NetGuard Controller][configuring-netguard-controller] for details.
```

The content is identical. The Markdown++ version is readable as plain text. The DITA version requires understanding XML document type declarations, nested element structures, entity references, and `xref` linking syntax. The Markdown++ style directive, markers, and link reference definition are invisible in a standard Markdown preview -- the reader sees a heading, paragraphs, and a bulleted list.

### Part B: Markdown++ best-practice refactoring

The following examples come from a real refactoring session on the NetGuard Controller User Guide. They show how Markdown++ authoring practices improve source file quality within the format itself.

**1. HTML entities to backtick code spans:**

```markdown
<!-- Before -->
1. Go to https://&lt;hostname&gt;.
Click **Accept &amp; Proceed**.

<!-- After -->
1. Go to `https://<hostname>`.
Click **Accept & Proceed**.
```

HTML entity encoding (`&lt;`, `&gt;`, `&amp;`) is unnecessary in Markdown. Backtick code spans handle literal angle brackets cleanly, and ampersands are safe in running text. The refactored version is shorter and immediately readable.

**2. Raw alias IDs to semantic slug references:**

```markdown
<!-- Before -->
[About NetGuard Controller IPsec peering connections](#316492 "About NetGuard Controller")

<!-- After -->
[About NetGuard Controller IPsec peering connections][about-netguard-controller-ipsec-peering-connections]
```

The numeric alias ID (`#316492`) is opaque -- a reader cannot guess what it links to without looking it up. The semantic slug (`about-netguard-controller-ipsec-peering-connections`) is self-documenting and resolves as a heading anchor in standard Markdown viewers.

**3. Inline figure captions to separated lines:**

```markdown
<!-- Before -->
NetGuard Controller topology ![](../graphics-artifacts/graphics-netguard/topology.png)

<!-- After -->
NetGuard Controller topology

![](../graphics-artifacts/graphics-netguard/topology.png "Title")
```

Separating the caption from the image onto its own line improves readability in source editors and produces cleaner diffs when either the caption or the image path changes.

**4. Backslash paths to forward slash paths:**

```markdown
<!-- Before -->
<!-- include:..\content-development\netguard-controller\netguard-ug\netguard-ug-title.md -->

<!-- After -->
<!-- include:../content-development/netguard-controller/netguard-ug/netguard-ug-title.md -->
```

Forward slashes are portable across all operating systems and tools. Backslashes can cause failures in Unix-based CI/CD environments and are not necessary even on Windows.

These are not cosmetic changes. Each one makes the source files more readable, more diffable, and more portable.

## The AI advantage

AI tools and agents have changed the economics of working with documentation formats, and Markdown++ is well positioned for this shift.

AI language models are good at reading and generating Markdown. It is the format they encounter most in training data, the format they use in their own output, and the format with the highest ratio of content to markup. When an AI agent reads a DITA XML topic, it has to parse through document type declarations, namespace attributes, nested element structures, and closing tags to find the actual content. When it reads a Markdown++ file, it just reads a document -- the extensions are invisible HTML comments that don't interfere with comprehension.

In practice:

- **AI-assisted authoring.** Writers using AI coding tools (Claude Code, GitHub Copilot, Cursor) can draft and edit Markdown++ content with high accuracy. The AI understands Markdown natively, and Markdown++ extensions follow consistent, predictable patterns that models learn quickly. AI-generated DITA or FrameMaker content, by contrast, tends to contain structural errors -- mismatched elements, incorrect nesting, missing required attributes -- that need manual correction.

- **Automated content migration.** AI agents can convert documentation from legacy formats to Markdown++ with less supervision than conversions to or from XML-based formats. The target format is simpler, the error surface is smaller, and results are immediately verifiable in any Markdown viewer.

- **Content review and quality.** AI tools can meaningfully evaluate Markdown++ diffs because the format is readable -- they can assess whether content is correct, complete, and well structured. XML diffs are harder for both humans and AI to evaluate at a glance.

- **Agent-driven publishing workflows.** AI agents can orchestrate the full documentation pipeline -- authoring, assembly, validation, publishing -- when the source format is one they can read and write reliably. Markdown++ keeps the source format in the AI's comfort zone while the build pipeline handles professional publishing output.

For teams evaluating DITA or FrameMaker today, this matters. The tooling ecosystem is moving toward AI-augmented workflows, and the formats that benefit most are the ones AI models handle most naturally. Markdown is that format. Markdown++ extends it without giving up that advantage.

## Publishing workflow

The path from Markdown++ source to published output:

1. **Author** -- Write content in any text editor or IDE using standard Markdown syntax with Markdown++ extensions. Preview content in your editor's Markdown viewer at any time.

2. **Assemble** -- Define publication structure using book files with `<!-- include: -->` directives. Each book file is a manifest that pulls together individual content files, shared boilerplate, and common assets.

3. **Configure** -- Set up a publishing project that maps Markdown++ style directives to output formatting, defines variable values, specifies conditions for each output format, and configures output-specific settings.

4. **Generate** -- Process the source through the publishing pipeline to produce one or more output formats. The pipeline resolves all includes, variables, conditions, cross-references, and style mappings to produce the final output.

5. **Validate** -- Compare generated output against baselines to verify that source changes produce the expected results. Pretty-printed HTML output enables meaningful diffs for regression testing.

6. **Publish** -- Deploy the generated output to its target destination -- a web server for online help, a file share for PDF distribution, or a build artifact repository for integration with other systems.

This pipeline can be fully automated. Command-line build tools enable generation as part of CI/CD workflows, triggered by commits, merges, or scheduled builds. The same source files produce consistent output across all formats without manual intervention.

## Getting started

Markdown++ is an open documentation format built on CommonMark. To start working with it:

- **Learn the syntax** -- The [syntax reference](plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md) provides the complete Markdown++ syntax with examples for every extension.

- **Author** -- Open any text editor and start writing. Markdown++ files are standard `.md` files. Add `<!-- style: -->` directives, `<!-- include: -->` assembly, and other extensions as your documentation needs require.

- **Publish** -- Publishing tools that support Markdown++/Markdown can produce multiple output formats from a single source -- responsive HTML5 online help, PDF, Dynamic HTML, CHM, Eclipse Help, and more.

- **Tooling** -- The [markdown-plus-plus](https://github.com/quadralay/markdown-plus-plus) plugin for Claude Code provides AI-assisted authoring with Markdown++ syntax awareness.

- **Community** -- The [Markdown++ specification and examples](https://github.com/quadralay/markdown-plus-plus) are hosted publicly on GitHub. Markdown++ is an open documentation format that welcomes third-party tool support and community contributions.

You don't have to choose between documentation power and authoring simplicity. That's what Markdown++ is for.
