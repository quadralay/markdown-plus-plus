---
date: 2026-05-13
status: active
issue: 99
origin: docs/brainstorms/2026-05-13-terminology-surfacing-audit-requirements.md
plan_type: docs
---

# docs: Terminology Surfacing Audit — `triple` and Adjacent Terms

## Summary

Surface the **alias+slug+linkref "triple"** and five adjacent Markdown++ terms
(`Unset` / pass-through condition, `attachment rule`, `content island`,
`block content` in multiline cells) consistently across the repo by
(1) creating a canonical `GLOSSARY.md` at the repo root, (2) making
minimal, targeted edits to surfaces that already discuss each pattern in
prose, and (3) adding a PR-template terminology checkbox to keep the gap
from reopening on future term-introducing PRs.

This is a documentation surfacing pass. It does not change the meaning,
syntax, or behavior of any term.

---

## Problem Frame

PR #94 introduced the term `triple` for the alias+slug+linkref cross-
reference pattern. The term lives in
`plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings`
and is already used (with link) in
`plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`. Every
other surface that discusses the pattern uses different language ("three
parts", "three elements", "the recommended Markdown++ cross-reference
idiom", "the semantic cross-reference pattern"). The same uneven
coverage exists for `Unset`, `attachment rule`, `content island`, and
`block content` in multiline cells.

Downstream consumers (the WebWorks brain repo's Reverb 2026.1 blog
draft, the marketing whitepaper) are starting to reference Markdown++
patterns by name. Without a canonical upstream surface, downstream
content drifts. This plan establishes that canonical surface and
backfills the term on every entry point that already discusses each
pattern, while leaving the meaning of every term unchanged.

(see origin: `docs/brainstorms/2026-05-13-terminology-surfacing-audit-requirements.md`)

---

## Requirements (carried from origin)

- **R1.** Create `GLOSSARY.md` at the repo root with five initial entries
  (`triple`/`alias+slug+linkref` as a single synonym entry, `Unset`,
  `attachment rule`, `content island`, `block content`), each pointing
  to its canonical definition surface.
- **R2.** Surface-by-surface audit — minimal, targeted edits. Add the
  term **only where the pattern is already discussed in prose**.
  Surfaces that don't currently cover a pattern are not edited.
- **R3.** Create `.github/PULL_REQUEST_TEMPLATE.md` with a minimal
  summary section and a terminology checkbox.
- **R4.** Repeatability — `GLOSSARY.md` documents the audit's
  repeatable form (grep the term across the surface list, decide
  per (term, surface) pair).
- **R-bump.** Bump plugin version to 1.5.0 via
  `scripts/bump-version.sh minor` and record a 1.5.0 entry in
  `CHANGELOG.md`. Minor: new doc surface, no behavior change.

---

## Scope Boundaries

### In scope

- New file: `GLOSSARY.md` at repo root.
- New file: `.github/PULL_REQUEST_TEMPLATE.md`.
- Targeted edits to surfaces enumerated in U3-U9 below.
- Version bump to 1.5.0 and `CHANGELOG.md` entry.

### Deferred to Follow-Up Work

- Adding a cross-reference pattern scenario to
  `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md`.
  That catalog has no entry for the pattern today; adding one is
  authoring, not surfacing.
- A `CONTRIBUTING.md` paragraph pointing to the PR template. Optional;
  the template itself is the discipline mechanism.

### Outside this product's identity (per origin)

- Changing the meaning, behavior, or syntax of any term.
- Renaming `triple`, `Unset`, `attachment rule`, `content island`, or
  any other established term.
- Cross-repo propagation (the WebWorks brain repo, the marketing
  whitepaper, the website). Those follow once the upstream canonical
  surface lands.
- Adding glossary entries for terms with **zero current presence** in
  this repo. Example: `Source ID` (Reverb 2026.1; lives only in
  downstream drafts today). Defer until the term lands upstream.

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Canonical home = `GLOSSARY.md` (not "elevate best-practices section") | Six other terms are in the same state. A single glossary scales better than canonicalizing one section. (see origin R1) |
| One synonym entry for `triple` + `alias+slug+linkref` | They name the same thing. Both forms appear in the entry title; a single anchor (`#triple`) is the canonical link target. |
| Glossary entries are pointers, not textbook content | Each entry has term + one-paragraph definition + "Full treatment" link to the canonical surface. No new prose is authored in `GLOSSARY.md`. |
| Discipline mechanism = PR template (not CONTRIBUTING addition) | The check fires at PR-open time, which is where the gap was discovered. PR templates appear every time; CONTRIBUTING is read once. (see origin R3) |
| Whitepaper edit is conditional, not pre-committed | Origin reported "no current mention" but `spec/whitepaper.md` line 83 has the heading "Semantic cross-references that work everywhere". U-audit unit will decide during implementation whether the section names the pattern strongly enough to warrant the term. |
| `examples.md` (skill scenario catalog) gets no edit | It has no current cross-reference pattern entry. Adding one is authoring, not surfacing. Deferred to follow-up. |

---

## Implementation Units

### U1. Create `GLOSSARY.md` at repo root

**Goal:** Establish the canonical home for Markdown++ terminology.

**Requirements:** R1, R4.

**Dependencies:** None.

**Files:**
- `GLOSSARY.md` (new)

**Approach:**
- Frontmatter: `date: 2026-05-13`, `status: active`.
- Short `## Conventions` paragraph describing entry shape (term, one-
  paragraph definition extracted from the canonical surface, "Full
  treatment" link).
- Short `## Repeatable Audit` paragraph documenting R4 — how to add a
  new term: grep the term across the surface list, decide per (term,
  surface) pair whether to use the term + link to glossary or leave
  untouched.
- Six entries, each as a level-3 heading with a stable anchor:

| Entry heading (anchor) | Synonym(s) | Canonical surface |
|------------------------|------------|-------------------|
| `### triple` (`#triple`) | `alias+slug+linkref` | `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md#semantic-cross-references-on-topic-defining-headings` |
| `### Unset` (`#unset`) | pass-through condition | `spec/specification.md` Section 11.3 (Condition State Model) |
| `### attachment rule` (`#attachment-rule`) | — | `spec/attachment-rule.md` |
| `### content island` (`#content-island`) | — | `spec/specification.md` Section 15 |
| `### block content` in multiline cells (`#block-content`) | — | `spec/multiline-cell-extensions.md` |

- Each entry: term in bold, synonym in parentheses if any, one-paragraph
  definition extracted (not paraphrased loosely) from the canonical
  surface, then a "Full treatment: [link text](path)" line.
- Repo-relative paths only. No prose changes upstream.

**Patterns to follow:**
- `CHANGELOG.md` and other repo-root docs for frontmatter style.
- Anchor format = kebab-cased lowercased headings (GitHub default).

**Test scenarios:**
- File parses as valid Markdown (preview renders without errors).
- All "Full treatment" links resolve (no broken links to files or
  anchors). Verify via `validate-mdpp.py` if available, otherwise by
  manual click-through in a Markdown previewer.
- Anchors `#triple`, `#unset`, `#attachment-rule`, `#content-island`,
  `#block-content` are reachable from the file (used by downstream
  units U2-U7).

**Verification:** File exists; all six entries present; all "Full
treatment" links resolve to existing files and anchors.

---

### U2. SKILL.md — add explicit glossary link

**Goal:** Point the existing `triple` reference at the canonical
definition.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`

**Approach:**
- SKILL.md line 112 already uses the phrase "the **alias+slug+linkref**
  triple". Add a parenthetical glossary link on first use: `(see
  [GLOSSARY.md](../../../../GLOSSARY.md#triple))`. No rewrite of
  surrounding prose.
- Verify the repo-relative path depth from `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md`
  to `GLOSSARY.md` during implementation (four `../` segments).

**Patterns to follow:** Existing cross-file links in SKILL.md (e.g.,
references to `../../../../spec/attachment-rule.md`).

**Test scenarios:**
- The glossary link resolves to `GLOSSARY.md#triple` from the SKILL.md
  location.
- The existing description of the pattern is unchanged.

**Verification:** One-line addition; no other prose modified;
link click-through succeeds.

---

### U3. spec/specification.md — name the pattern in Section 17.3

**Goal:** Use `alias+slug+linkref triple` in the formal-spec recommended-
idiom section.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `spec/specification.md`

**Approach:**
- Section 17.3 contains the heading "The Semantic Cross-Reference
  Pattern" (around line 1181). The lead-in says "The recommended pattern
  for cross-referenceable headings combines three elements:". Rewrite
  that line minimally to introduce the term: e.g., "The recommended
  pattern for cross-referenceable headings — the **alias+slug+linkref
  triple** (see [GLOSSARY.md](../GLOSSARY.md#triple)) — combines three
  elements:". No structural changes; just the term name and link.

**Patterns to follow:** Existing spec cross-links such as
`[Cross-File Link Reference Resolution](cross-file-link-resolution.md)`.

**Test scenarios:**
- Term `alias+slug+linkref triple` appears once on first use in this
  section.
- Glossary link resolves.
- No other content in Section 17 is modified.

**Verification:** Single-line edit; `grep -n "triple" spec/specification.md`
shows the new occurrence on the targeted line; other paragraphs unchanged.

---

### U4. spec/cross-file-link-resolution.md — name the pattern on first use

**Goal:** Replace one prose-only use of "the semantic cross-reference
pattern" with the named term + glossary link.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `spec/cross-file-link-resolution.md`

**Approach:**
- Line 163 currently reads "The semantic cross-reference pattern in
  Markdown++ uses link reference definitions...". Add `(the **triple**)`
  immediately after "pattern" on first use, plus a glossary link.
- Subsequent uses of the prose phrase in the same file may be left
  alone — the goal is first-use naming, not global substitution.

**Test scenarios:**
- First-use line names the pattern as `the triple` with a link to
  `GLOSSARY.md#triple`.
- Spec semantics unchanged.

**Verification:** One-line edit; link resolves.

---

### U5. examples/semantic-cross-references.md — label the demo as the triple

**Goal:** Make the standalone example label itself with the term it
demonstrates.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `examples/semantic-cross-references.md`

**Approach:**
- Line 16 currently reads "Every linkable heading uses three parts:".
  Replace with: "Every linkable heading uses the **alias+slug+linkref
  triple** (see [GLOSSARY.md](../GLOSSARY.md#triple)):". The numbered
  list that follows continues to enumerate the three parts and remains
  unchanged.

**Patterns to follow:** Existing intra-repo links in `examples/`.

**Test scenarios:**
- The example loads as valid Markdown++ (it already uses combined
  commands, aliases, and link references — verify with
  `validate-mdpp.py`).
- The new term wording renders correctly.
- Glossary link resolves from `examples/`.

**Verification:** Single-line replacement on line 16; rest of file
unchanged.

---

### U6. plugins/.../references/syntax-reference.md — name the idiom

**Goal:** Backfill the term on the existing "recommended cross-reference
idiom" note.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`

**Approach:**
- Line 464 ("This is the recommended Markdown++ cross-reference idiom —
  see ...") already links to the best-practices canonical surface. Add
  `(the **triple**)` after "idiom" and add a glossary link to
  `../../../../../GLOSSARY.md#triple`. Verify path depth during
  implementation.

**Test scenarios:**
- Glossary link resolves from the syntax-reference path.
- The existing link to best-practices is preserved.

**Verification:** One-line edit at line 464; both links resolve.

---

### U7. README.md — add a terminology pointer

**Goal:** Give first-time readers a discoverable entry to the glossary.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `README.md`

**Approach:**
- README does not discuss the cross-reference pattern in prose, so no
  term naming is needed. Add a single short line pointing to
  `GLOSSARY.md` in a natural location — wherever specs, contributing,
  or "learn more" links are introduced. Wording: `See [GLOSSARY.md](GLOSSARY.md)
  for Markdown++ terminology.`
- During implementation, choose the placement that fits the README's
  existing section structure (typically near a "Documentation" or
  "Specification" link cluster). Do not invent a new section.

**Test scenarios:**
- Glossary link resolves.
- No other README content is modified.

**Verification:** One-line addition; rest of README untouched.

---

### U8. Add glossary links for adjacent terms where the term is already used

**Goal:** Backfill `(see [GLOSSARY.md](path#anchor))` links for `Unset`,
`attachment rule`, `content island`, and `block content` where the term
is already used in prose and the link is missing. No new prose.

**Requirements:** R2.

**Dependencies:** U1.

**Files (candidates — final list determined by implementation grep):**
- `spec/specification.md` (multiple uses of `Unset`, `content island`)
- `spec/attachment-rule.md` (self-reference — skip)
- `spec/multiline-cell-extensions.md` (`block content`)
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/syntax-reference.md`
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/best-practices.md`
- `plugins/markdown-plus-plus/skills/markdown-plus-plus/references/examples.md`

**Approach:**
- Per term, grep the term across the surface list. For each surface,
  add a glossary link on **first prose use only** if one is not already
  present and the link adds discovery value. Skip when:
  - The surface IS the canonical surface for the term (don't link a
    document to itself).
  - The term appears only inside a code block (no need to link).
  - The first use is already adjacent to a link to the canonical
    surface (no need to double-link).
- Editing pattern: append `(see [GLOSSARY.md](relative-path#anchor))` to
  the sentence containing the first prose use. Repo-relative paths only.

**Test scenarios:**
- After edits, each of the four terms has at least one surface that
  links to its glossary anchor besides the glossary itself.
- No surface is edited in a way that changes semantics.
- All glossary links resolve from the editing surface.

**Verification:** Diff is exclusively additive (parentheticals or
trailing notes); spec rules and skill guidance unchanged.

---

### U9. Audit + decide for `spec/whitepaper.md`

**Goal:** Apply the (term, surface) decision rule from R2 to the
whitepaper, which origin flagged ambiguously.

**Requirements:** R2.

**Dependencies:** U1.

**Files:**
- `spec/whitepaper.md` (possibly)

**Approach:**
- Origin reported "no current mention", but `spec/whitepaper.md` line 83
  has the heading "Semantic cross-references that work everywhere" and
  the section discusses the pattern in marketing prose.
- During implementation: read the section. If it names the pattern in a
  way that benefits from the term + glossary link (e.g., "Markdown++
  introduces a link reference pattern that bridges..."), add `(the
  **alias+slug+linkref triple** — see [GLOSSARY.md](../GLOSSARY.md#triple))`
  on first use. If the section is pure marketing framing and the term
  would feel out of place, leave it untouched and record the decision
  in the PR description.
- This unit's purpose is to apply the decision rule, not to commit to
  an edit ahead of time.

**Test scenarios:**
- Either: a single-line addition is present with a working glossary
  link, or: no edit is made and the PR description notes the
  "leave untouched" decision.

**Verification:** Decision applied with rationale logged in PR
description.

---

### U10. Create `.github/PULL_REQUEST_TEMPLATE.md`

**Goal:** Add a PR-open-time discipline check to prevent the same
terminology gap from reopening.

**Requirements:** R3.

**Dependencies:** U1 (template references `GLOSSARY.md`).

**Files:**
- `.github/PULL_REQUEST_TEMPLATE.md` (new)
- `.github/` (new directory — `.github/PULL_REQUEST_TEMPLATE.md`
  parent does not exist today)

**Approach:**
- Minimal usable template structure:

  ```markdown
  ## Summary

  ## Terminology

  - [ ] If this PR introduces or renames a Markdown++ term,
        `GLOSSARY.md` and at least one entry-point surface (README,
        spec, or skill) have been updated.
  ```

- Keep the summary section deliberately minimal so the template is
  usable for routine PRs. The terminology check is the only checkbox.
- No GitHub-action wiring is required; the template is rendered by
  default when `gh pr create` or the GitHub web UI opens a new PR.

**Patterns to follow:**
- Standard GitHub PR template conventions
  (`.github/PULL_REQUEST_TEMPLATE.md`).

**Test scenarios:**
- File is parsed as the default PR body when opening a new PR (GitHub
  contract — verified by observing the next PR's pre-populated body).
- Template renders cleanly in GitHub's PR-create UI (no broken
  markdown).

**Verification:** File exists at the right path; next PR opened in
this repo shows the template as the default body.

---

### U11. Version bump + CHANGELOG entry

**Goal:** Record the change as a minor release.

**Requirements:** R-bump (Success Criterion 4, 5).

**Dependencies:** U1-U10 substantively complete (so the CHANGELOG entry
accurately describes what shipped).

**Files:**
- `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (bumped by
  `scripts/bump-version.sh minor`)
- `.claude-plugin/marketplace.json` (bumped by same script)
- `CHANGELOG.md`

**Approach:**
- Run `scripts/bump-version.sh minor`. Current version is 1.4.0; this
  takes the plugin to 1.5.0 and keeps `plugin.json` and
  `marketplace.json` in sync (per the script's contract documented in
  `CLAUDE.md`).
- Add a 1.5.0 entry to `CHANGELOG.md` describing:
  - New `GLOSSARY.md` at repo root with six initial entries.
  - Terminology surfacing across spec, skill, and examples.
  - New `.github/PULL_REQUEST_TEMPLATE.md` with terminology checkbox.
  - Closes #99.
- No behavior or semantics change — emphasize this in the entry so the
  release notes are unambiguous.

**Patterns to follow:** Existing `CHANGELOG.md` entry format (see the
1.4.0 entry added in commit `eabff1d`).

**Test scenarios:**
- `plugin.json` version is `1.5.0`.
- `marketplace.json` version is `1.5.0`.
- `CHANGELOG.md` has a 1.5.0 entry referencing #99.

**Verification:** Versions match; CHANGELOG entry present.

---

## System-Wide Impact

- **Downstream consumers** (WebWorks brain repo, marketing whitepaper):
  gain a stable upstream anchor to link to (`GLOSSARY.md#triple` and the
  other five anchors). No coordinated edits required in this PR —
  downstream propagation is explicitly out of scope.
- **AI agents authoring Markdown++ via the skill**: the skill now has a
  glossary pointer from `SKILL.md` and `syntax-reference.md`, so routing
  context is more likely to surface the canonical term.
- **PR authors going forward**: the new PR template introduces a check
  at the right moment.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Broken anchors in `GLOSSARY.md` "Full treatment" links if upstream sections move | Use heading-text anchors (GitHub default) — they break loudly under preview; verified at U1 test scenarios. Add validation as a follow-up if drift becomes a pattern. |
| README placement of the glossary pointer feels forced | U7 explicitly defers placement to implementation judgment; if no natural location exists, the pointer may be added in a docs/contributing cluster or omitted with rationale recorded in the PR. |
| Whitepaper edit decision is ambiguous | U9 is structured as "apply the decision rule" rather than a pre-committed edit. The rationale (edit or skip) goes in the PR description. |
| PR template appears on PRs where it's irrelevant | The terminology checkbox is one line and explicitly conditional ("If this PR introduces or renames..."). Low cognitive load. |
| Version bump applied before all units land | U11 is sequenced last and depends on U1-U10 being substantively complete. |

---

## Success Criteria (carried from origin)

1. `GLOSSARY.md` exists at the repo root with five initial entries
   (triple/alias+slug+linkref, Unset, attachment rule, content island,
   block content), each linking to its canonical surface.
2. Every surface in U3-U9 that currently discusses a pattern names the
   term and links to its glossary anchor.
3. `.github/PULL_REQUEST_TEMPLATE.md` exists with a terminology
   checkbox.
4. `CHANGELOG.md` records the addition under a 1.5.0 entry.
5. Plugin version is bumped to 1.5.0 via `scripts/bump-version.sh
   minor` before PR.
6. The change closes #99 and does not modify the meaning of any
   existing term.

---

## Sequencing

```
U1 (GLOSSARY.md)
  ├── U2 (SKILL.md)
  ├── U3 (spec/specification.md)
  ├── U4 (spec/cross-file-link-resolution.md)
  ├── U5 (examples/semantic-cross-references.md)
  ├── U6 (syntax-reference.md)
  ├── U7 (README.md)
  ├── U8 (adjacent terms backfill)
  └── U9 (whitepaper audit decision)
U10 (PR template) — independent of U2-U9; can land in parallel with U1
U11 (version + CHANGELOG) — last; depends on U1-U10
```

U2-U9 are independent of each other once U1 lands; they may be applied
in a single commit or grouped per-surface. U10 is independent of U2-U9.
U11 is sequenced last.

---

## Open Questions Deferred to Implementation

- Exact placement of the README glossary pointer (U7).
- Final wording of the whitepaper edit, or the decision to skip (U9).
- Whether to also add a single `CONTRIBUTING.md` line pointing to the
  PR template (optional; origin assumption notes this is reasonable but
  not required). Default: skip; revisit if the PR review surfaces a
  need.
