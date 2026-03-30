---
date: 2026-03-29
status: active
---

# Duplicate Alias Test

This file tests detection of duplicate alias values (should produce MDPP008 errors).

<!--#introduction-->
## Introduction

First use of the "introduction" alias.

<!--#getting-started-->
## Getting Started

First use of the "getting-started" alias.

<!--#introduction-->
## Another Introduction

This is a DUPLICATE of the "introduction" alias - should trigger error MDPP008.

<!--#features-->
## Features

Unique alias - should be fine.

<!--#getting-started-->
## Getting Started Again

This is a DUPLICATE of the "getting-started" alias - should trigger error MDPP008.

## Summary

This file should report 2 duplicate alias errors.
