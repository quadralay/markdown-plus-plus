---
mdpp-version: 1.0
date: 2026-04-08
status: active
---

<!-- style:Heading1; #500001 -->
# Inline image and link styles

[inline-image-and-link-styles]: #500001 "Inline image and link styles"

This example demonstrates how Markdown++ inline styles apply custom formatting to images and links without affecting surrounding content.

<!-- style:Heading2; #500002 -->
## Styled images

[styled-images]: #500002 "Styled images"

Inline styles placed immediately before an image tag control its presentation in published output. In a standard Markdown viewer, the images render normally.

### Hero image

A full-width banner at the top of a page:

<!--style:HeroImage-->![Product dashboard overview](images/dashboard-hero.png "Dashboard Overview")

### Logo image

A constrained logo sized for headers or footers:

<!--style:LogoImage-->![Acme Corp logo](images/acme-logo.svg "Acme Corp")

### Screenshot with border

Screenshots styled with a visible border and drop shadow:

<!--style:ScreenshotImage-->![Settings panel showing notification preferences](images/settings-notifications.png)

### Thumbnail image

A small preview image that links to the full-size version:

<!--style:ThumbnailImage-->![Architecture diagram thumbnail](images/architecture-thumb.png "Click to enlarge")

<!-- style:Heading2; #500003 -->
## Styled links

[styled-links]: #500003 "Styled links"

Inline styles inside the link text brackets apply custom formatting to links. The style directive goes inside the `[ ]`, immediately before the styled text element.

### External link

Visual distinction for links leaving the current site:

Visit the [<!--style:ExternalLink-->*Markdown++ specification*](https://example.com/spec) for the formal syntax definition.

### Important link

Emphasis on a critical reference:

Read the [<!--style:ImportantLink-->**Migration Guide**](migration-guide.md#overview) before upgrading.

### Download link

A styled call-to-action for downloadable resources:

Get the [<!--style:DownloadLink-->*latest release package*]($download_url; "Download Now") from the releases page.

### UI element link

Navigation references styled to match the application interface:

Open [<!--style:UILink-->**Settings > Notifications**](app-settings.md#notifications) to configure alerts.

<!-- style:Heading2; #500004 -->
## Combining image styles with other directives

[combining-image-styles]: #500004 "Combining image styles with other directives"

Image styles work alongside block-level directives. The block directive applies to the paragraph containing the image; the inline style applies to the image itself.

<!-- style:FigureBlock; marker:Keywords="architecture, diagram" -->
<!--style:DiagramImage-->![System architecture showing three service layers](images/architecture-full.png "System Architecture")

The paragraph above has a block style (`FigureBlock`) and a search keyword marker, while the image within it has its own inline style (`DiagramImage`).
