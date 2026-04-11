---
date: 2026-04-11
status: active
---

# MDPP005 Test: Circular Include Detection

This file tests the MDPP005 validation check for circular includes.
Lines marked EXPECT MDPP005 should trigger an error when cycle detection
is implemented. Lines marked EXPECT MDPP006 trigger a missing-file warning.

**Note:** The validator currently detects missing files (MDPP006) but does
not yet implement cycle detection (MDPP005). These fixtures document the
expected behavior for future implementation.

---

## POSITIVE CASES (should trigger MDPP005)

### Case 1: Self-referencing include

<!-- include:sample-circular-includes.md -->

EXPECT MDPP005 -- this file includes itself.

### Case 2: Mutual reference (partner file)

<!-- include:sample-circular-includes-partner.md -->

EXPECT MDPP005 -- if the partner file includes this file back, the chain
forms a cycle: this file -> partner -> this file.

---

## NEGATIVE CASES (should NOT trigger MDPP005)

### Case 3: Include of a non-existent file (MDPP006, not MDPP005)

<!-- include:nonexistent-chapter.md -->

EXPECT MDPP006 -- missing file, not a circular reference.

### Case 4: Valid include pattern (no cycle)

<!-- include:sample-basic.md -->

No error expected -- sample-basic.md exists and does not include this file.

### Case 5: Include inside a fenced code block (ignored entirely)

```markdown
<!-- include:sample-circular-includes.md -->
```

No error expected -- directives inside fenced code blocks are not processed.
