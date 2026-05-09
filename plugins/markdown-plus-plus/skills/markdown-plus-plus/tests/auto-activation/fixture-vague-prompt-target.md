---
date: 2026-05-09
status: active
mdpp-version: 1.0
---

# Setup Guide

This file is the target of the G2 vague-prompt case. A user might say:

> "Update the docs to mention the new install URL."

The prompt names no path and contains no Markdown++ signal. The routing
layer cannot match on prompt content alone; closure depends on the
consuming repo's `CLAUDE.md` guidance, not on file-content signals.

## Install

Download $product_name; from $download_url; and follow the platform-
specific instructions below.

<!--condition:windows-->
On Windows, run the `.msi` installer and accept the default install
location unless your IT policy specifies otherwise.
<!--/condition-->

<!--condition:mac-->
On macOS, drag the `.dmg` contents into `/Applications`.
<!--/condition-->
