# Markdown++ Examples

Real-world examples demonstrating common patterns and use cases.

## Example 1: Product Documentation

A typical product documentation page with variables, conditions, and styles.

```markdown
<!--markers:{"Keywords": "product overview, installation, configuration", "Description": "Complete product documentation for installation and setup"} ; #product-overview-->
# $product_name; Overview

Welcome to **$product_name;** version $version;. This guide covers installation, configuration, and basic usage.

<!--condition:web-->
> **Quick Links:** [Download](#download) | [Installation](#installation) | [Support](https://support.example.com)
<!--/condition-->

<!--condition:print-->
> See the back cover for support contact information.
<!--/condition-->

## System Requirements

<!--style:RequirementsTable-->
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | $min_os; | $rec_os; |
| RAM | $min_ram; | $rec_ram; |
| Disk | $min_disk; | $rec_disk; |

<!--#installation-->
## Installation

<!--condition:windows-->
### Windows Installation

1. Download the installer from $download_url;
2. Run `$installer_name;`
3. Follow the wizard prompts

<!--/condition-->

<!--condition:mac-->
### macOS Installation

1. Download the DMG from $download_url;
2. Drag $product_name; to Applications
3. Launch from Launchpad

<!--/condition-->

<!--condition:linux-->
### Linux Installation

```bash
sudo apt-get install $package_name;
```

Or download the tarball from $download_url;.

<!--/condition-->

## Getting Help

<!--condition:web-->
Visit our [knowledge base](https://kb.example.com) or [community forum](https://forum.example.com).
<!--/condition-->

<!--condition:print-->
See Appendix B for troubleshooting guides.
<!--/condition-->
```

---

## Example 2: API Reference

API documentation with code examples and conditional content.

```markdown
<!--markers:{"Keywords": "authentication, oauth, token, api", "Description": "API authentication guide using OAuth 2.0"} ; #authentication-->
# Authentication API

<!--#api-overview-->
## Overview

The $product_name; API uses OAuth 2.0 for authentication. All API requests must include a valid access token.

## Endpoints

<!--style:EndpointTable-->
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/token` | Get access token |
| POST | `/auth/refresh` | Refresh token |
| DELETE | `/auth/revoke` | Revoke token |

<!--#get-token-->
## Get Access Token

<!--style:HTTPExample-->
```http
POST /auth/token HTTP/1.1
Host: api.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=$your_client_id;&
client_secret=$your_client_secret;
```

### Response

<!--style:CodeResponse-->
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

<!--condition:advanced-->
### Token Scopes

| Scope | Description |
|-------|-------------|
| `read` | Read-only access |
| `write` | Read and write access |
| `admin` | Full administrative access |

<!--/condition-->

## Error Handling

<!--style:WarningBox-->
> **Important:** Never expose your client secret in client-side code.

<!--condition:!production-->
### Debug Mode

In development, set `DEBUG=true` to get detailed error messages:

```bash
export DEBUG=true
```

<!--/condition-->
```

---

## Example 3: User Guide with Includes

A user guide that includes shared content from multiple files.

**Main file: `user-guide.md`**
```markdown
<!--markers:{"Keywords": "user guide, getting started, features", "Description": "End user guide for product setup and usage"} ; #user-guide-->
# $product_name; User Guide

<!--include:shared/header.md-->

## Introduction

This guide helps you get started with $product_name;.

<!--include:chapters/getting-started.md-->

<!--include:chapters/basic-features.md-->

<!--condition:advanced-->
<!--include:chapters/advanced-features.md-->
<!--/condition-->

<!--include:shared/footer.md-->
```

**Included file: `shared/header.md`**
```markdown
<!--style:DocumentHeader-->
> **Document Version:** $doc_version; | **Last Updated:** $last_updated;

---
```

**Included file: `chapters/getting-started.md`**
```markdown
<!--#getting-started-->
## Getting Started

### First Launch

When you first launch $product_name;, the setup wizard guides you through:

1. Creating your account
2. Configuring preferences
3. Connecting integrations

<!--style:TipBox-->
> **Tip:** You can skip the wizard and configure settings later from Preferences.
```

---

## Example 4: Multiline Tables

Complex tables with rich content in cells. Each row uses continuation lines (empty first cell) and is separated by an empty row with cell borders.

```markdown
# Feature Comparison

<!-- style:ComparisonTable ; multiline -->
| Plan       | Features                         |
|------------|----------------------------------|
| Free       | Basic access:                    |
|            | - Up to 5 users                  |
|            | - 5 GB storage                   |
|            | - Community support              |
|            |                                  |
| Pro        | Everything in Free, plus:        |
|            | - Up to 50 users                 |
|            | - 100 GB storage                 |
|            | - Email support (24hr response)  |
|            | - API access                     |
|            |                                  |
| Enterprise | Everything in Pro, plus:         |
|            | - Unlimited users                |
|            | - Unlimited storage              |
|            | - Dedicated support              |
|            | - Custom development             |
|            | - SLA guarantee                  |
```

### Multi-Column Multiline Example

```markdown
<!-- multiline -->
| Component | Requirements             | Notes                    |
|-----------|--------------------------|--------------------------|
| Database  | PostgreSQL 14+           | Required for production. |
|           | - 4 GB RAM minimum       | > **Tip:** Use SSD for   |
|           | - 50 GB disk space       | > better performance.    |
|           |                          |                          |
| Web Server| Nginx or Apache          | Optional reverse proxy.  |
|           | - SSL certificate        | - Handles HTTPS          |
|           | - Gzip compression       | - Static file caching    |
```

---

## Example 5: Conditional Platform Content

Documentation that adapts to different platforms.

```markdown
# Installation Guide

## Download

<!--condition:windows-->
Download the Windows installer (.exe) from the [downloads page]($download_url;).
<!--/condition-->

<!--condition:mac-->
Download the macOS disk image (.dmg) from the [downloads page]($download_url;).
<!--/condition-->

<!--condition:linux-->
### Package Managers

**Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install $package_name;
```

**Fedora/RHEL:**
```bash
sudo dnf install $package_name;
```

**Arch Linux:**
```bash
sudo pacman -S $package_name;
```
<!--/condition-->

## Configuration

The configuration file location depends on your platform:

<!--style:ConfigTable-->
| Platform | Config Location |
|----------|-----------------|
<!--condition:windows-->
| Windows | `%APPDATA%\$product_name;\config.json` |
<!--/condition-->
<!--condition:mac-->
| macOS | `~/Library/Application Support/$product_name;/config.json` |
<!--/condition-->
<!--condition:linux-->
| Linux | `~/.config/$product_name;/config.json` |
<!--/condition-->

## Verify Installation

<!--condition:windows-->
Open PowerShell and run:
```powershell
$product_name; --version
```
<!--/condition-->

<!--condition:mac,linux-->
Open Terminal and run:
```bash
$product_name; --version
```
<!--/condition-->

You should see: `$product_name; version $version;`
```

---

## Example 6: Release Notes

Release notes with version-specific content.

```markdown
<!--markers:{"Keywords": "release notes, changelog, version", "Description": "Release notes and changelog for latest version"} ; #release-notes-->
# $product_name; Release Notes

## Version $version;

**Release Date:** $release_date;

### New Features

<!--style:FeatureList-->
- **Feature A**: Description of feature A
- **Feature B**: Description of feature B
- **Feature C**: Description of feature C

### Improvements

- Improved performance of $component_name;
- Enhanced UI for $feature_name;
- Better error messages for common issues

### Bug Fixes

<!--style:BugFixList-->
| Issue | Description |
|-------|-------------|
| #1234 | Fixed crash when opening large files |
| #1235 | Resolved memory leak in background process |
| #1236 | Corrected timezone handling for scheduled tasks |

### Known Issues

<!--style:WarningBox-->
> **Known Issue:** Some users may experience slow startup on first launch after update. This resolves after initial indexing completes.

<!--condition:!production-->
### Internal Notes

These notes are for internal review only:

- Performance benchmarks: See JIRA-4567
- QA sign-off: Pending
- Documentation status: In progress

<!--/condition-->

### Upgrade Instructions

<!--condition:web-->
The application updates automatically. No action required.
<!--/condition-->

<!--condition:print-->
See Section 5.2 for manual upgrade instructions.
<!--/condition-->
```

---

## Example 7: Troubleshooting Guide

Troubleshooting content with conditional visibility.

```markdown
<!--#troubleshooting-->
# Troubleshooting

## Common Issues

<!--#connection-errors-->
### Connection Errors

<!--style:ProblemBox-->
> **Problem:** Cannot connect to server

**Possible Causes:**
1. Network connectivity issues
2. Firewall blocking connection
3. Server maintenance

**Solutions:**

<!--condition:windows-->
1. Check Windows Firewall settings
2. Run `netsh winsock reset` in Admin PowerShell
3. Verify proxy settings in Internet Options
<!--/condition-->

<!--condition:mac-->
1. Check System Preferences > Security & Privacy > Firewall
2. Reset network settings: `sudo dscacheutil -flushcache`
3. Verify proxy in System Preferences > Network
<!--/condition-->

<!--condition:linux-->
1. Check iptables rules: `sudo iptables -L`
2. Verify DNS: `nslookup $server_hostname;`
3. Test connection: `curl -v https://$server_hostname;`
<!--/condition-->

<!--#performance-issues-->
### Performance Issues

<!--style:ProblemBox-->
> **Problem:** Application running slowly

**Diagnostic Steps:**

1. Check system resources
   <!--condition:windows-->
   Open Task Manager (Ctrl+Shift+Esc)
   <!--/condition-->
   <!--condition:mac-->
   Open Activity Monitor
   <!--/condition-->
   <!--condition:linux-->
   Run `top` or `htop`
   <!--/condition-->

2. Clear application cache
   <!--condition:windows-->
   Delete `%APPDATA%\$product_name;\cache\*`
   <!--/condition-->
   <!--condition:mac-->
   Delete `~/Library/Caches/$product_name;/*`
   <!--/condition-->
   <!--condition:linux-->
   Delete `~/.cache/$product_name;/*`
   <!--/condition-->

3. Restart the application
```

---

## Example 8: Inline Styling for Images and Links

Using custom styles for images and links within content.

```markdown
<!--markers:{"Keywords": "images, links, styling", "Description": "Examples of styled images and links"} ; #media-examples-->
# Media and Link Styling Examples

## Styled Images

Use inline styles to control image presentation:

<!--style:HeroImage-->![Product Hero](images/hero.png "Product Overview")

Here's our logo: <!--style:LogoImage-->![Logo](images/logo.svg "Company Logo")

Screenshots use a special style:

<!--style:ScreenshotImage-->![Settings Panel](images/settings-screenshot.png)

## Styled Links

Apply styles inside link text for consistent link formatting:

Visit our [<!--style:ExternalLink-->*documentation portal*](https://docs.example.com) for more information.

See the [<!--style:ImportantLink-->**Getting Started Guide**](getting-started.md#introduction) to begin.

Download the [<!--style:DownloadLink-->*latest release*]($download_url; "Download Now").
```

---

## Example 9: Content Islands with Blockquotes

Using styled blockquotes as "content islands" for rich callout boxes and learning sections.

```markdown
<!--markers:{"Keywords": "blockquotes, callouts, layout", "Description": "Content islands using styled blockquotes"} ; #content-islands-->
# Using Content Islands

Content islands are styled blockquotes that contain complex content structures.

## Learning Box

<!--style:BQ_Learn-->
> ## Key Concepts
>
> This learning box explains important concepts:
>
> 1. **Variables** - Use `$name;` syntax for reusable values
> 2. **Conditions** - Wrap content with `<!--condition:name-->...<!--/condition-->`
> 3. **Styles** - Apply with `<!--style:StyleName-->`
>
> ```python
> # Example code in a content island
> def process_document(content):
>     return apply_extensions(content)
> ```
>
> Try these concepts in your own documents!

## Warning Box

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

## Tip Box with Mixed Content

<!--style:BQ_Tip-->
> **Pro Tip: Keyboard Shortcuts**
>
> Speed up your workflow with these shortcuts:
>
> | Action | Windows | macOS |
> |--------|---------|-------|
> | Save | Ctrl+S | Cmd+S |
> | Find | Ctrl+F | Cmd+F |
> | Replace | Ctrl+H | Cmd+H |
>
> See [Keyboard Reference](shortcuts.md#all-shortcuts) for the complete list.
```

---

## Example 10: Nested Lists with Styling

Complex nested lists with custom styling for procedures and hierarchical content.

```markdown
<!--markers:{"Keywords": "procedures, lists, installation", "Description": "Nested list examples for procedures and checklists"} ; #nested-lists-->
# Procedures and Nested Lists

## Installation Procedure

<!--style:ProcedureList-->
1. **Download the installer**
   - Go to $download_url;
   - Select your platform:
     - Windows 10/11 (64-bit)
     - macOS 12+ (Apple Silicon or Intel)
     - Linux (deb or rpm package)
   - Click Download

2. **Run the installer**
   - Windows:
     1. Double-click the `.exe` file
     2. Accept the UAC prompt
     3. Follow the wizard
   - macOS:
     1. Open the `.dmg` file
     2. Drag to Applications
     3. Eject the disk image
   - Linux:
     1. Open terminal in download folder
     2. Run: `sudo dpkg -i $package_name;.deb`
     3. Resolve dependencies: `sudo apt-get install -f`

3. **Configure initial settings**
   - Launch the application
   - Complete the setup wizard:
     - Enter license key
     - Choose installation type:
       - Typical (recommended)
       - Custom
       - Minimal
     - Select components

## Feature Checklist

<!--style:ChecklistStyle-->
- [ ] Core installation complete
  - [ ] Main application installed
  - [ ] Command-line tools installed
  - [ ] Documentation installed
- [ ] Configuration verified
  - [ ] Database connection tested
  - [ ] API credentials validated
  - [ ] Notifications enabled
- [ ] Integration setup
  - [ ] SSO configured
  - [ ] Webhooks registered
  - [ ] Third-party apps connected
```

---

## Example 11: Combined Commands

Using multiple extensions together in single comments.

```markdown
<!--markers:{"Keywords": "combined commands, extensions", "Description": "Examples of using multiple extensions together"} ; #combined-examples-->
# Combined Extension Examples

## Heading with Everything

<!-- style:ImportantHeading ; marker:Keywords="critical, configuration" ; #critical-section -->
## Critical Configuration Steps

This section has a custom style, marker metadata, and a stable alias for linking.

## Styled Multiline Table with Alias

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

## Styled Content Island with Metadata

<!-- style:BQ_Important ; marker:Keywords="important, notice" ; #important-notice -->
> **Important Notice**
>
> This document describes features in version $version;.
>
> For earlier versions, see the [archive](archive.md#versions).
```

---

## Tips for Writing Markdown++

1. **Use variables for repeated content** - Product names, versions, URLs
2. **Use conditions for platform-specific content** - Installation, configuration
3. **Use includes for shared content** - Headers, footers, common sections
4. **Use styles for consistent formatting** - Tables, code blocks, callouts
5. **Use aliases for stable links** - Section links that survive restructuring
6. **Use markers for searchability** - Keywords, categories, metadata
7. **Use content islands** - Blockquotes for rich callout boxes
8. **Use combined commands** - Multiple extensions in one comment
9. **Follow order priority** - style, multiline, marker(s), #alias
