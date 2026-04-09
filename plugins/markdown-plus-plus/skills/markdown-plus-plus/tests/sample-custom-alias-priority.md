---
date: 2026-04-08
status: active
---

# Custom Alias Priority Test

This file tests custom alias priority over auto-generated heading aliases.
A custom alias always takes priority over an auto-generated alias on a different element.
The displaced auto-generated alias receives a counter suffix. No MDPP008 error should be emitted.

## Scenario 1: Basic collision (custom alias before colliding heading)

<!-- #setup -->
## Installation

Install the required packages.

## Setup

Configure the application.

Expected aliases:
- `## Installation` -> `installation` (auto-generated), `setup` (custom alias)
- `## Setup` -> `setup-2` (suffixed auto-generated, displaced by custom alias)

## Scenario 2: Reverse document order (colliding heading before custom alias)

This scenario proves that custom aliases always win regardless of document order.
The auto-generated alias appears first, but the custom alias still takes priority.

## Configuration

Configure the system.

<!-- #configuration -->
## API Reference

Document the API endpoints.

Expected aliases:
- `## Configuration` -> `configuration-2` (suffixed auto-generated, displaced by custom alias)
- `## API Reference` -> `api-reference` (auto-generated), `configuration` (custom alias)

## Scenario 3: Composed collision (custom alias priority + duplicate auto-generated)

<!-- #troubleshooting -->
## Quick Start

Get up and running quickly.

## Troubleshooting

Fix common issues.

## Troubleshooting

Advanced troubleshooting steps.

Expected aliases:
- `## Quick Start` -> `quick-start` (auto-generated), `troubleshooting` (custom alias)
- `## Troubleshooting` (first) -> `troubleshooting-2` (suffixed, displaced by custom alias)
- `## Troubleshooting` (second) -> `troubleshooting-3` (suffixed, next available counter)

This file should report 0 errors. All collisions are custom-vs-auto-generated
and are silently resolved per the Custom Alias Priority spec.
