---
date: 2026-04-11
status: active
---

# Unset Condition Pass-Through Sample

This file exercises Unset condition pass-through behavior. The expected condition set for evaluating this file is `{web: Visible, print: Hidden}`. The condition names `mobile`, `tablet`, and `kiosk` are intentionally **not** defined — they are Unset.

## Simple Unset Pass-Through

The block below uses an undefined condition name. A conformant processor MUST preserve the opening tag, content, and closing tag unchanged.

<!--condition:mobile-->
This content is for mobile users. It should pass through with its condition tags intact.
<!--/condition-->

## Hidden Condition (Control)

The block below uses a defined Hidden condition. It should be removed entirely.

<!--condition:print-->
This content is for print. It should NOT appear in the output.
<!--/condition-->

## Visible Condition (Control)

The block below uses a defined Visible condition. Tags should be removed and content included.

<!--condition:web-->
This content is for the web. Only this paragraph should appear — no condition tags in output.
<!--/condition-->

## Unset with Variable Inside

The block below is Unset and contains a variable reference. The `mobile` condition passes through, but `$product_name;` MUST be resolved by variable substitution (Phase 1, Step 2).

<!--condition:mobile-->
Download $product_name; for your mobile device.
<!--/condition-->

## Compound AND Expression — One Operand Unset

Both `web` (Visible) and `mobile` (Unset) appear in an AND expression. Because `mobile` is Unset, the entire block MUST pass through regardless of `web`'s assigned state.

<!--condition:web mobile-->
This appears on both web and mobile platforms.
<!--/condition-->

## Compound OR Expression — One Operand Unset

Both `print` (Hidden) and `mobile` (Unset) appear in an OR expression. Because `mobile` is Unset, the entire block MUST pass through regardless of `print`'s assigned state.

<!--condition:print,mobile-->
This appears in print or mobile output.
<!--/condition-->

## Compound AND Expression — All Operands Unset

Both `mobile` and `tablet` are Unset. The block passes through.

<!--condition:mobile tablet-->
This targets users on mobile or tablet devices simultaneously.
<!--/condition-->

## NOT with Unset Operand

`kiosk` is Unset. The NOT expression `!kiosk` MUST force pass-through — the block is not evaluated.

<!--condition:!kiosk-->
This content appears when the kiosk condition is Hidden.
<!--/condition-->

## Include Inside Unset Block

The include directive below is inside an Unset condition block. The include MUST NOT be processed; the entire block — condition tags, include directive, and surrounding content — passes through as literal text.

<!--condition:mobile-->
Mobile-specific preamble.
<!--include:mobile-appendix.md-->
Mobile-specific postamble.
<!--/condition-->
