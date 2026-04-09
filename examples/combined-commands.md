---
mdpp-version: 1.0
date: 2026-04-08
status: active
---

<!-- style:Heading1; markers:{"Keywords": "combined commands, extensions, semicolons"}; #400001 -->
# Combined commands

[combined-commands]: #400001 "Combined commands"

This example demonstrates how multiple Markdown++ extensions compose on a single line using semicolon-separated directives. Order priority: style, multiline, marker(s), alias.

<!-- style:Heading2; #400002 -->
## Style with alias

[style-with-alias]: #400002 "Style with alias"

The most common combination pairs a custom style with a stable alias for linking.

<!-- style:ChapterHeading; #400003 -->
## Project configuration

[project-configuration]: #400003 "Project configuration"

This heading has a chapter style and a stable alias. Other documents link here using the semantic slug `[project-configuration]`.

<!-- style:Heading2; #400004 -->
## Style with markers

[style-with-markers]: #400004 "Style with markers"

Add search keywords and metadata alongside a custom style.

<!-- style:Important; marker:Keywords="deployment, checklist, prerequisites" -->
Before deploying, verify that all database migrations have been applied and environment variables are set.

<!-- style:Heading2; #400005 -->
## Full combination on a heading

[full-combination]: #400005 "Full combination on a heading"

All four directive types -- style, multiline, marker, and alias -- compose in one comment.

<!-- style:SectionHeading; marker:Keywords="migration, upgrade path"; #400006 -->
## Upgrade path from v1 to v2

[upgrade-path]: #400006 "Upgrade path from v1 to v2"

This heading carries a custom style, search keywords, and a stable alias. The order follows the priority convention: style first, then markers, then alias.

<!-- style:Heading2; #400007 -->
## Styled multiline table with alias

[styled-multiline-table]: #400007 "Styled multiline table with alias"

Tables benefit from combined commands when they need custom formatting, multiline cell content, and a stable link target.

<!-- style:MigrationTable; multiline; #400008 -->
| Step           | Action                           | Notes                 |
|----------------|----------------------------------|-----------------------|
| 1. Backup      | Export current configuration     |                       |
|                | - Database schema                | Required              |
|                | - User preferences               |                       |
|                | - API keys                       |                       |
|                |                                  |                       |
| 2. Update      | Run the upgrade script           |                       |
|                | - Applies schema migrations      | Downtime expected     |
|                | - Updates configuration format   |                       |
|                |                                  |                       |
| 3. Verify      | Confirm all services are healthy |                       |
|                | - Check endpoint responses       | See monitoring guide  |
|                | - Validate user authentication   |                       |

<!-- style:Heading2; #400009 -->
## Content island with markers

[content-island-with-markers]: #400009 "Content island with markers"

Styled blockquotes (content islands) can carry markers for search indexing.

<!-- style:BQ_Learn; marker:Keywords="best practices, naming conventions" -->
> ## Naming conventions
>
> Follow these patterns when naming Markdown++ directives:
>
> - **Variables:** lowercase with underscores (`$product_name;`)
> - **Conditions:** format or platform names (`web`, `windows`)
> - **Styles:** type-based PascalCase (`WarningBox`, `DataTable`)
> - **Aliases:** numeric IDs for stability (`#400001`)

## Summary

Combined commands reduce visual clutter by merging multiple directives into a single comment. The semicolon separator and consistent ordering make documents easier to scan and maintain.
