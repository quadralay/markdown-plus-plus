---
date: 2026-05-13
status: active
issue: 93
plan_type: docs
---

# docs: Strengthen Markdown++ Skill Command Block Syntax Patterns

## Summary

Add a high-visibility **Command Block Syntax** anchor section near the
top of the `markdown-plus-plus` skill that gives Claude (and human
authors) a memorable MUST/ALWAYS/NEVER block for the two highest-
frequency combined directive patterns — `style + alias` and
`markers + alias` — plus an explicit short list of "NEVER" mistakes.

The skill already covers attachment, ordering, and combined-command
rules in detail across `<syntax_examples>`, `<common_mistakes>`, and
`references/syntax-reference.md`. The gap is **presentation**: the
canonical combined patterns are not surfaced as a single copy-paste
block with imperative framing, so AI agents drift on the syntax (blank
lines after directives, aliases on their own line, inconsistent
spacing) when authoring from vague prompts. This plan adds the anchor
block, leaves the detailed reference content unchanged, and bumps the
plugin minor version.

---

## Problem Frame

Per issue #93, downstream authoring sessions (referenced PR
`quadralay/epublisher-express-trial#1`, four+ syntax fix commits)
show recurring drift on Markdown++ command block syntax:

- Blank lines inserted between directive comment and target content
- Aliases placed on separate lines from `style:` or `markers:`
- Spacing variations inside `<!-- ... -->` tags
- Workaround: users hand-author `TOPIC-TEMPLATE.md`-style files in the
  consumer repo to teach Claude the patterns, instead of relying on the
  skill

The skill's current content is **technically complete** — the
`<common_mistakes>` section in `SKILL.md` and the Attachment Rules
section in `references/syntax-reference.md` cover every rule. The
problem is that the canonical combined patterns (`style + alias`,
`markers + alias`) are not surfaced as a single high-visibility
"anchor" with imperative language. Authors and AI agents looking for
a copy-paste pattern have to assemble it from multiple sections.

This plan addresses the presentation gap. It does not change any
Markdown++ syntax rule.

---

## Requirements

- **R1.** Add a single, high-visibility **Command Block Syntax**
  section to `SKILL.md` positioned where it is read early in the
  document — after `<overview>` (which already names the directives)
  and before `<syntax_examples>` (which goes deep on each one).
- **R2.** The new section MUST contain:
  - A short imperative lead-in ("ALWAYS use this format — no
    variations.")
  - Canonical copy-paste-ready patterns for the two highest-frequency
    combined cases: `style + alias`, `markers + alias`.
  - A pattern for the single-directive cases (`style` alone,
    `markers` alone, `#alias` alone) showing the same no-blank-line
    rule.
  - An explicit **NEVER** list covering: blank line between directive
    and content; alias on a separate line from style or markers;
    inconsistent spacing inside `<!-- ... -->`.
  - A "see also" line pointing to the existing detailed sections
    (`references/syntax-reference.md#attachment-rules`, the
    `<common_mistakes>` section, `spec/attachment-rule.md`).
- **R3.** The new section MUST NOT duplicate the existing detailed
  content in `<syntax_examples>`, `<common_mistakes>`, or
  `references/syntax-reference.md`. It is an anchor, not a rewrite.
- **R4.** The two canonical patterns MUST follow the existing repo
  convention of spaces around `;` (per the "more readable" guidance
  in `references/syntax-reference.md` Combined Commands → Whitespace),
  while noting that the no-space form is also valid.
- **R-bump.** Bump plugin version `1.5.0 → 1.6.0` via
  `scripts/bump-version.sh minor` and record a 1.6.0 entry in
  `CHANGELOG.md` under **Tooling**. Minor: new skill-content section,
  no behavior change.

---

## Scope Boundaries

### In scope

- One new section added to
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`.
- Version bump to 1.6.0 (`plugin.json` + `marketplace.json` via the
  bump script) and a `CHANGELOG.md` entry.

### Deferred to Follow-Up Work

- Mirroring the imperative MUST/ALWAYS/NEVER framing into
  `references/best-practices.md` (Common Mistakes section) and
  `references/syntax-reference.md` (Attachment Rules section). The
  SKILL.md anchor is the highest-leverage change — it loads first and
  is where the gap shows up in practice. If the SKILL.md change does
  not fully resolve the drift, a follow-up issue can broaden the
  imperative framing across the references.
- A `TOPIC-TEMPLATE.md`-style template file in the skill (the
  consumer's hand-authored workaround). The anchor section is the
  skill-side equivalent; the consumer template can be retired or kept
  by the downstream repo as they choose.

### Outside this product's identity

- Changing any Markdown++ syntax rule, naming rule, or attachment
  rule.
- Renaming or reordering combined-command priority (`style, multiline,
  marker(s), #alias` remains the order).
- Adding new directive types or new combined-command forms.

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Place the anchor section between `<overview>` and `<syntax_examples>` | The overview names the directives; the syntax examples go deep on each. The anchor sits in between and surfaces the canonical combined patterns at the seam where readers transition from "what exists" to "how to use it". |
| Two canonical patterns, not all combinations | `style + alias` and `markers + alias` are the two combinations cited in the issue as where drift happens. Showing every possible combination dilutes the anchor. Single-directive forms get one compact illustration each. |
| MUST / ALWAYS / NEVER imperative voice | The issue calls this out explicitly. The existing skill content uses softer "must" / "should". Imperative voice in the anchor section makes the rules harder to skim past without changing the underlying spec language elsewhere. |
| Spaces around `;` in canonical patterns | Existing repo convention (`references/syntax-reference.md` Combined Commands → Whitespace says "Spaces around semicolons are optional but recommended for readability"). The canonical patterns should match the recommended form. A short parenthetical notes that the no-space form is also valid. |
| No duplication of detailed content | The anchor is a navigational landmark, not a replacement for the detail. Duplicate content drifts out of sync. The new section ends with a "see also" line that points to the existing detailed sections. |
| Minor version bump (1.5.0 → 1.6.0) | New skill content (a new section) is a minor change under the repo's bump-script semantics ("New skills, new features, enhancements"). No syntax or behavior change → not a major bump; not a patch either since it adds substantive author-facing guidance. |

---

## Implementation Units

### U1. Add Command Block Syntax anchor section to SKILL.md

**Goal:** Add a single high-visibility section that gives Claude and
human authors a memorable canonical-pattern block with imperative
MUST/ALWAYS/NEVER framing.

**Requirements:** R1, R2, R3, R4.

**Dependencies:** None.

**Files:**

- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
  (modify — add one new section)

**Approach:**

- Insert a new section between the closing `</overview>` tag and the
  opening `<syntax_examples>` tag. Wrap the new section in its own
  semantic block tag: `<command_block_syntax>` … `</command_block_syntax>`.
  This matches the existing pattern of named sections (`<overview>`,
  `<syntax_examples>`, `<validation>`, `<common_mistakes>`, etc.).
- The section MUST follow this shape (the exact wording is decided at
  authoring time; the structure below is the directional guide):

  ```text
  <command_block_syntax>

  ## Command Block Syntax (MUST follow exactly)

  ALWAYS use this format — no variations. Content MUST follow the
  directive on the very next line with no blank line between them.

  ### Style + alias (combined)

      <!-- style:StyleName ; #anchor-name -->
      Content immediately follows (NO blank line).

  ### Markers + alias (combined)

      <!-- markers:{"Keywords": "...", "Description": "..."} ; #anchor-name -->
      ## Heading immediately follows (NO blank line).

  ### Single-directive forms

      <!-- style:StyleName -->
      Content immediately follows.

      <!-- marker:Keywords="..." -->
      Content immediately follows.

      <!-- #anchor-name -->
      Content immediately follows.

  ### NEVER

  - Put a blank line between a directive comment and its target
    content. The blank line silently breaks the attachment; the
    directive passes through as a regular HTML comment with no effect.
  - Place the alias on a separate line from `style:` or `markers:`.
    Stacked HTML comments leave the top one orphaned. Combine them
    with `;` in a single directive instead.
  - Vary the spacing inside `<!-- ... -->` or around `;` arbitrarily.
    The canonical form has a space after `<!--`, a space before `-->`,
    and spaces around each `;`. The no-space form (`<!--style:A;#b-->`)
    is also valid, but pick one and stay consistent within a document.

  See `references/syntax-reference.md` (Attachment Rules, Combined
  Commands) and the `<common_mistakes>` section below for the full
  rule set and edge cases. See `spec/attachment-rule.md` for the
  normative definition.

  </command_block_syntax>
  ```

  The pseudo-code above is **directional guidance** for the
  implementer, not a verbatim spec. The implementer should adjust the
  prose for readability, keep the section under ~50 lines, and ensure
  the see-also paths are repo-relative and resolve from the SKILL.md
  location.

- Do **not** modify `<overview>`, `<syntax_examples>`, `<common_mistakes>`,
  or any other existing section. The new section is purely additive.
- Verify the section is reachable from anyone reading SKILL.md
  top-to-bottom (Claude reads the file in order during skill
  activation; a section between `<overview>` and `<syntax_examples>`
  is encountered early).

**Patterns to follow:**

- Existing named semantic blocks in `SKILL.md` (`<objective>`,
  `<overview>`, `<syntax_examples>`, `<validation>`,
  `<common_mistakes>`, `<references>`, `<success_criteria>`).
- The "**Wrong** / **Right**" example pairs already used in the
  `<common_mistakes>` section — but the new section uses a different
  shape (canonical patterns + NEVER list, not Wrong/Right pairs)
  because its job is to be a copy-paste mental anchor, not a
  teaching pass.
- Repo-relative paths for cross-references (e.g.,
  `references/syntax-reference.md`,
  `../../../../spec/attachment-rule.md`).

**Test scenarios:**

- The section renders as valid Markdown in a previewer (no broken
  fences, no stray tags).
- The section sits between `</overview>` and `<syntax_examples>` (line
  ordering preserved; no other section moved).
- Cross-reference paths in the "see also" line resolve from the
  SKILL.md location:
  - `references/syntax-reference.md#attachment-rules` resolves to the
    Attachment Rules heading in
    `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`.
  - `../../../../spec/attachment-rule.md` resolves to `spec/attachment-rule.md`.
- The two canonical patterns in the section use spaces around `;` per
  R4.
- The NEVER list contains exactly the three items called out in R2
  (blank line, separate alias line, inconsistent spacing).
- `python plugins/markdown-plus-plus/skills/markdown-plus-plus/scripts/validate-mdpp.py
  plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` exits 0
  (no new validation errors introduced).

**Verification:**

- New section is present in SKILL.md.
- File parses cleanly in a Markdown previewer.
- Cross-reference paths resolve.
- No content removed or modified outside the new section.

---

### U2. Bump plugin version to 1.6.0 and update CHANGELOG

**Goal:** Record the skill enhancement in the version and CHANGELOG so
the change is visible to anyone tracking plugin versions or release
history.

**Requirements:** R-bump.

**Dependencies:** U1 (the section must exist before the version
documenting it is bumped).

**Files:**

- `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (modify via
  bump script)
- `.claude-plugin/marketplace.json` (modify via bump script)
- `CHANGELOG.md` (modify — new 1.6.0 entry)

**Approach:**

- Run `scripts/bump-version.sh minor` from the repo root. This updates
  both `plugin.json` and `marketplace.json` to 1.6.0.
- Add a new `## [1.6.0] - 2026-05-13` entry to `CHANGELOG.md` above
  the existing `## [1.5.0]` entry. Under a single **Tooling**
  subsection, record:

  > Added a high-visibility Command Block Syntax anchor section to
  > `SKILL.md` with MUST/ALWAYS/NEVER framing for the canonical
  > `style + alias` and `markers + alias` combined directive
  > patterns, plus a NEVER list for the three most common
  > authoring mistakes (blank line after directive, alias on a
  > separate line, inconsistent spacing). The new section is
  > additive — existing detailed sections in `<syntax_examples>`,
  > `<common_mistakes>`, and `references/syntax-reference.md` are
  > unchanged.
  > ([#93](https://github.com/quadralay/markdown-plus-plus/issues/93))

- Match the existing CHANGELOG entry style (line ending in
  `([#NN](url))`, no trailing period inside the parenthesis).

**Patterns to follow:**

- The 1.5.0 entry (immediately above) for shape, grouping
  (**Tooling**), and link format.
- The 1.4.0 entry for similar "single-section skill enhancement"
  framing.

**Test scenarios:**

- `plugin.json` version equals `1.6.0` after the bump.
- `marketplace.json` version equals `1.6.0` after the bump.
- `CHANGELOG.md` contains a `## [1.6.0] - 2026-05-13` heading above
  the `## [1.5.0]` heading.
- The 1.6.0 entry references issue #93 with a working link.
- No unrelated CHANGELOG entries are reordered or modified.

**Verification:**

- Bump script exits 0 and both JSON files reflect 1.6.0.
- CHANGELOG entry is present, correctly placed, and follows the
  existing entry style.

---

## System-Wide Impact

- **Skill consumers (downstream repos authoring Markdown++).** The
  new anchor section gives Claude an early, imperative landmark when
  it activates the skill. This should reduce the drift observed in
  the consumer repo cited in the issue. No breaking change —
  consumers who rely on existing skill content see no removal or
  rename.
- **Manual-verification fixtures** (`tests/auto-activation/cases.md`).
  No update needed. The new section adds content; it does not change
  any signal the auto-activation routing depends on. The fixtures
  exercise file-content signals (`<!-- style: -->`, `mdpp-version:`,
  etc.), which are unaffected.
- **Validation script** (`scripts/validate-mdpp.py`). No change. The
  new section is plain prose and fenced code blocks — no new
  validation logic needed.
- **`GLOSSARY.md`** (added in #99). No new terms introduced; the
  anchor section uses existing terminology (`attachment rule`,
  `combined commands`) and can link to glossary entries if the
  implementer judges it helpful for the see-also line. Optional, not
  required.

---

## Risk Analysis

| Risk | Mitigation |
|------|------------|
| The new section duplicates existing content and drifts out of sync | R3 explicitly forbids duplication. The section is structured as an anchor — canonical patterns + NEVER list — not a teaching pass. The see-also line points to the existing detail. |
| The imperative MUST/ALWAYS/NEVER voice clashes with surrounding softer language | The new section is the only place using imperative voice. Surrounding sections retain their existing tone. This is intentional: the anchor is meant to stand out. |
| The section makes SKILL.md too long, reducing the load-priority of later sections | Section is capped at ~50 lines (one screen). SKILL.md is already ~400 lines; adding 50 is a 12% increase, well within reasonable bounds. |
| Cross-reference paths break (relative-path miscount) | Verified against existing paths in SKILL.md (`references/...` is one level down; `../../../../spec/...` is four levels up). Test scenarios in U1 explicitly check both resolve. |
| Version bump conflicts with concurrent work | The bump script is the canonical mechanism; both `plugin.json` and `marketplace.json` are updated atomically by one script invocation. No other in-flight PR is bumping the version per `git log`. |

---

## Verification

| Criterion | How verified |
|-----------|--------------|
| New Command Block Syntax section present in SKILL.md, between `</overview>` and `<syntax_examples>` | Read SKILL.md; check section ordering |
| Section contains canonical `style + alias` and `markers + alias` patterns with spaces around `;` | Visual inspection of the new section |
| Section contains a NEVER list with the three items required by R2 | Visual inspection of the new section |
| Section has a see-also line pointing to `references/syntax-reference.md` and `spec/attachment-rule.md` | Cross-reference path click-through from SKILL.md |
| `plugin.json` and `marketplace.json` both at 1.6.0 | `grep -n "version" plugins/markdown-plus-plus/.claude-plugin/plugin.json .claude-plugin/marketplace.json` |
| `CHANGELOG.md` has a 1.6.0 entry referencing #93 | Read CHANGELOG.md |
| `validate-mdpp.py` exits 0 on the updated SKILL.md | Run the validator |
| No existing skill content modified | `git diff` shows additions only in SKILL.md (within the new section), in the JSON version fields, and in CHANGELOG.md |

---

## Deferred Implementation Notes

- The exact prose wording of the new section (lead-in sentence,
  NEVER-list phrasing, see-also line) is decided at implementation
  time. The structure above is the directional spec.
- Whether the see-also line links to `GLOSSARY.md` entries
  (e.g., `[attachment rule](../../../../GLOSSARY.md#attachment-rule)`)
  is an implementer judgment. The plan does not require it.
- If the implementer discovers, during U1, that the section reads
  better with a different placement (e.g., immediately inside
  `<overview>` rather than as a separate sibling tag), they MAY
  adjust. The plan's R1 specifies "early in the document" as the
  intent, not a precise byte offset.
