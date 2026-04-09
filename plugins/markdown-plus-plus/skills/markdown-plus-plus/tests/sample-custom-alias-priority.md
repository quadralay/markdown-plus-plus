---
date: 2026-04-08
status: active
---

# Custom Alias Priority Test

This file tests custom alias priority over auto-generated heading aliases.
Custom aliases and auto-generated aliases occupy separate namespaces. When both
produce the same identifier, the custom alias wins at link resolution time.
The auto-generated alias still exists -- it is de-prioritized, not displaced or
suffixed. No MDPP008 error should be emitted.

## Scenario 1: Basic overlap (custom alias before heading with same slug)

<!-- #setup -->
## Installation

Install the required packages.

## Setup

Configure the application.

Expected aliases:
- `## Installation` -> `installation` (auto-generated), `setup` (custom alias)
- `## Setup` -> `setup` (auto-generated, de-prioritized by custom alias)
- A link to `#setup` resolves to `## Installation` (custom alias priority)

## Scenario 2: Reverse document order (heading with same slug before custom alias)

This scenario proves that custom aliases always win at resolution time regardless
of document order. The auto-generated alias appears first, but the custom alias
still takes resolution priority.

## Configuration

Configure the system.

<!-- #configuration -->
## API Reference

Document the API endpoints.

Expected aliases:
- `## Configuration` -> `configuration` (auto-generated, de-prioritized by custom alias)
- `## API Reference` -> `api-reference` (auto-generated), `configuration` (custom alias)
- A link to `#configuration` resolves to `## API Reference` (custom alias priority)

## Scenario 3: Composed overlap (custom alias priority + duplicate auto-generated)

<!-- #troubleshooting -->
## Quick Start

Get up and running quickly.

## Troubleshooting

Fix common issues.

## Troubleshooting

Advanced troubleshooting steps.

Expected aliases:
- `## Quick Start` -> `quick-start` (auto-generated), `troubleshooting` (custom alias)
- `## Troubleshooting` (first) -> `troubleshooting` (auto-generated, de-prioritized by custom alias)
- `## Troubleshooting` (second) -> `troubleshooting-2` (suffixed -- duplicate auto-generated resolution)
- A link to `#troubleshooting` resolves to `## Quick Start` (custom alias priority)

This file should report 0 errors. Custom-vs-auto-generated overlaps are resolved
by priority at link resolution time per the Custom Alias Priority spec.
