---
date: 2026-04-10
topic: passthrough-marker-injection
---

# Fix Unrecognized Combined Command Segment Behavior

## Problem Frame

The spec incorrectly describes unrecognized segments in combined commands as "silently discarded, functioning as inline comments." The implementation treats them as PassThrough markers — injecting unrecognized segment content as PassThrough markers attached to the target element. This is the intentional design: it provides an invisible means for authors to track status and other metadata in rendered output.

Six locations across `spec/specification.md` and `spec/formal-grammar.md` describe the wrong behavior.

## Requirements

- R1. All references to "silently discarded" or "inline comments" for unrecognized combined command segments must be replaced with PassThrough marker injection behavior.
- R2. The formal grammar's `unrecognized_text` production comment must reflect PassThrough injection rather than inline comments.
- R3. The validation table example must describe the correct behavior (PassThrough marker, not discarded inline comment).
- R4. The spec must state that rendering of PassThrough marker content from unrecognized segments is implementation-defined.

## Success Criteria

- No instance of "silently discarded" or "inline comments" appears in reference to unrecognized combined command segments.
- All six identified locations describe PassThrough marker injection.
- Spec language is consistent with existing Passthrough marker terminology in section 11.3.

## Scope Boundaries

- No changes to PassThrough marker behavior itself.
- No changes to combined command parsing rules.
- No changes to the `unrecognized_text` grammar production (only its descriptive comment).

## Next Steps

→ Proceed directly to work — scope is lightweight and fully specified.
