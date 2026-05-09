---
date: 2026-05-09
status: active
---

# API Reference Overview

This fixture demonstrates the G3 "buried directive" case. The frontmatter
deliberately omits `mdpp-version:` so the only Markdown++ signal in the
file is the `<!-- multiline -->` directive that appears below line 30.
A partial-read excerpt that stops short of the directive line will not
surface any Markdown++ signal to the routing layer.

## Background

The reference described here covers the public HTTP API. It is intended
for integrators who want to build automation, dashboards, or third-party
tooling on top of the platform.

The API follows REST conventions. Endpoints accept and return JSON. All
requests require an authentication token issued through the developer
console. Tokens may be scoped to specific projects or to the entire
account.

Rate limits apply per token. Default limits are sufficient for most
integrations; teams with higher throughput requirements can request a
quota increase through support.

Versioning follows semantic versioning. Breaking changes appear only in
major-version bumps and are announced at least 90 days in advance.

## Reading the Tables Below

Each endpoint table lists the route, the supported methods, and notes on
authentication or scoping requirements. Refer to the per-endpoint pages
for full request and response schemas.

## Endpoint Index

<!-- multiline -->
| Route               | Methods    | Notes                          |
|---------------------|------------|--------------------------------|
| `/projects`         | GET, POST  | List and create projects.      |
|                     |            | Requires account-level token.  |
|                     |            |                                |
| `/projects/{id}`    | GET, PATCH | Retrieve or update one.        |
|                     |            | Requires project-level token.  |
|                     |            |                                |
| `/projects/{id}/runs` | GET      | List builds for a project.     |
|                     |            | Cursor-paginated.              |

## Errors

Standard HTTP status codes apply. The response body for any 4xx or 5xx
error includes a JSON object with `code`, `message`, and `request_id`
fields. Use the `request_id` when contacting support.

## Changelog

Recent changes to the API surface are documented in the platform
changelog. Subscribe to the changelog feed to receive notifications
when new versions ship.
