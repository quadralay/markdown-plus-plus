---
date: 2026-05-09
status: active
type: docs
origin: GitHub issue #84
---

# docs: Broaden Markdown++ skill auto-trigger signals in SKILL.md description

## Summary

Rewrite the `description` frontmatter field in `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` so the Markdown++ skill auto-triggers on the full surface of distinguishing Markdown++ signals -- not just the partial list that exists today. Adds `<!--multiline-->`, the `<!--markers:-->` plural form, and `mdpp-version:` YAML frontmatter as triggers; explicitly notes whitespace inside HTML comments is irrelevant to matching; and covers the "modeled after another file" case where the skill should fire on the source file's signals rather than only the new file's contents. Description-only change -- no body edits.

## Problem Frame

The current description in `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` lines 3-7 enumerates `<!--style:-->`, `<!--condition:-->`, `$variable;`, `<!--include:-->`, `<!--marker:-->`, and `<!--#alias-->` as activation signals. The issue documents a real failure case: a user asked the agent to create `docs/guides/format-changes-since-2025.1.4655.md` modeled on an existing file using `<!-- multiline -->` before its table, and the agent produced a malformed single-row table with everything crammed into one cell because multiline-table continuation never triggered the skill. The user had to invoke the skill manually.

Three concrete gaps in the activation criteria:

1. `<!--multiline-->` is a primary distinguishing signal (no CommonMark equivalent) but is not listed.
2. The description shows `<!--style:-->` with no internal whitespace; real-world files use `<!-- style:Title -->` with whitespace. Activation should match either form.
3. `mdpp-version:` YAML frontmatter is documented in the skill body and recommended for new files, but is not in the activation criteria.

A fourth, related gap: when a user asks the agent to create a new `.md` file modeled after an existing Markdown++ file, the activation should fire on the *source* file's signals, not just the new file's contents.

## Requirements

Carried forward from GitHub issue #84:

- **R1.** Replace the `description` frontmatter value in `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` with a rewrite that names every distinguishing Markdown++ signal: `<!--style:-->`, `<!--multiline-->`, `<!--condition:-->`, `<!--include:-->`, `<!--marker:-->` and `<!--markers:-->` (both singular and plural), `<!--#alias-->`, `$variable;`, and `mdpp-version:` in YAML frontmatter.
- **R2.** Note explicitly that whitespace inside HTML comments is irrelevant to matching (so `<!--style:-->` and `<!-- style:Title -->` both trigger).
- **R3.** Cover the modeled-after-another-file case so the skill fires on a source file's signals when creating a derivative file.
- **R4.** Preserve the existing "AUTHORITATIVE REFERENCE for Markdown++ syntax" framing and the closing "Use for editing, validating, migrating, or auditing" clause -- the rewrite extends the trigger list and intent coverage; it does not redefine the skill.
- **R5.** Leave the SKILL.md body unchanged. This is a description/frontmatter-only edit.
- **R6.** Bump the plugin version (patch) per the repo's version-management workflow so the change ships through `plugin.json` and `marketplace.json` consistently.

---

## Key Technical Decisions

- **Adopt the issue's suggested rewrite verbatim, with one tweak: list `<!--marker:-->` and `<!--markers:-->` together to make the singular/plural surface explicit.** The issue's suggestion already includes both forms; keeping that explicit pairing gives the model a clear hint that both directives count as Markdown++ signals.
- **Keep the description on the existing folded YAML scalar (`description: >`).** The current frontmatter uses `>` folded style; the rewrite is one paragraph and reads naturally as folded prose. No need to switch to literal block scalar.
- **No SKILL.md body edits.** The body already documents `<!--multiline-->`, `<!--markers:-->`, and `mdpp-version:` (lines 27, 33-34, 159 in the current file). The gap is purely in the activation surface, not the reference content.
- **Patch version bump (1.1.15 → 1.1.16).** This is a description metadata change that improves activation behavior. It is not a new feature or breaking change.
- **Companion sibling skill at `webworks-claude-skills:markdown-plus-plus`** (referenced in the system skill list) is out of scope for this repo. Its description lives in another repo and is updated independently.

---

## Scope Boundaries

**In scope:**

- Description rewrite in `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` frontmatter (lines 3-7).
- Patch version bump via `scripts/bump-version.sh patch` -- updates `plugins/markdown-plus-plus/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

**Out of scope:**

- Any edits to the SKILL.md body (`<objective>`, `<overview>`, `<syntax_examples>`, etc.).
- Any edits to `references/syntax-reference.md`, `references/examples.md`, `references/best-practices.md`, or other skill reference files.
- Changes to the `webworks-claude-skills:markdown-plus-plus` skill in the WebWorks plugin repo. That repo manages its own description; coordination is a follow-up if needed.
- Changes to the validation script, alias generator, or skill tests.

### Deferred to Follow-Up Work

- A future audit could verify the WebWorks-side `webworks-claude-skills:markdown-plus-plus` skill description aligns with this repo's after the change ships. Out of scope for this PR because the WebWorks skill lives in a separate repo with its own release cadence.

---

## Implementation Units

### U1. Rewrite SKILL.md description frontmatter

- **Goal:** Replace the activation-signal list in the `description` field of `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` with a comprehensive list that names every distinguishing Markdown++ signal, addresses whitespace variants, includes `mdpp-version:` YAML frontmatter, and covers modeled-after-another-file cases.
- **Requirements:** R1, R2, R3, R4, R5
- **Dependencies:** none
- **Files:**
  - `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` (modify lines 3-7 only)
- **Approach:** Edit only the `description: >` folded scalar value. Final text:

  > AUTHORITATIVE REFERENCE for Markdown++ syntax. Use when reading or writing `.md` files that contain any of these signals (whitespace inside the HTML comment is irrelevant): `<!--style:-->` directives, `<!--multiline-->` table directives, `<!--condition:-->` blocks, `<!--include:-->` directives, `<!--marker:-->` or `<!--markers:-->`, `<!--#alias-->` anchors, `$variable;` tokens, or `mdpp-version:` in YAML frontmatter. Also use when creating a `.md` file modeled after another file containing any of these signals. Use for editing, validating, migrating, or auditing Markdown++ source documents.

  Preserve the existing `name:` field and the `---` frontmatter delimiters above and below. No body edits.

- **Patterns to follow:** The current frontmatter at `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` lines 1-8 already uses YAML folded scalar (`description: >`) -- mirror that style for the rewrite.
- **Test scenarios:**
  - Verify the `name:` field is unchanged (`name: markdown-plus-plus`).
  - Verify the description begins with "AUTHORITATIVE REFERENCE for Markdown++ syntax" and ends with "editing, validating, migrating, or auditing Markdown++ source documents."
  - Verify the description names all of: `<!--style:-->`, `<!--multiline-->`, `<!--condition:-->`, `<!--include:-->`, `<!--marker:-->`, `<!--markers:-->`, `<!--#alias-->`, `$variable;`, and `mdpp-version:`.
  - Verify the description includes the whitespace-irrelevance clause and the modeled-after-another-file clause.
  - Verify the body content (lines 9 onward in the original) is unchanged.
- **Verification:** Open SKILL.md and confirm only the description frontmatter changed; the rest of the file is byte-identical to the prior revision. `git diff` on the file should show changes only inside the `---`/`---` frontmatter block.

### U2. Bump plugin version (patch)

- **Goal:** Run `scripts/bump-version.sh patch` to bump the version from `1.1.15` to `1.1.16` in both `plugins/markdown-plus-plus/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Per repo convention (see `CLAUDE.md` § Version Management), patch bumps cover documentation updates and minor improvements like this description rewrite.
- **Requirements:** R6
- **Dependencies:** U1 (so the version bump ships alongside the change it represents)
- **Files:**
  - `plugins/markdown-plus-plus/.claude-plugin/plugin.json` (modified by script)
  - `.claude-plugin/marketplace.json` (modified by script)
- **Approach:** Execute the existing script. Do not hand-edit version strings. The script's purpose is to keep the two manifests synchronized.
- **Patterns to follow:** Repo convention documented in `CLAUDE.md` § Version Management.
- **Test scenarios:**
  - Verify `plugins/markdown-plus-plus/.claude-plugin/plugin.json` `version` field reads `1.1.16`.
  - Verify `.claude-plugin/marketplace.json` top-level `version` field reads `1.1.16`.
  - Verify both files have only the version line changed (no incidental formatting drift).
- **Verification:** `git diff` on both manifests shows a single one-line version change in each.

---

## Verification Strategy

This change has no runtime behavior to test. Validation is structural:

1. Visual inspection of the SKILL.md frontmatter confirms the rewrite landed and the body is unchanged.
2. `git diff plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` confirms changes are confined to the frontmatter.
3. `git diff` on the two manifests confirms only the version field changed.
4. The new description preserves the YAML folded scalar form and parses as valid YAML. (No tooling exists in this repo to lint skill frontmatter; visual inspection is sufficient.)

The activation behavior change cannot be unit-tested in this repo -- it is a hint to the LLM's skill-routing layer. The qualitative test is the issue's failure case: when the agent next encounters a file containing `<!-- multiline -->` or `mdpp-version:` in YAML frontmatter, the skill should auto-activate without manual invocation.

---

## Risks

- **WebWorks sibling skill drift.** The system skill list shows two near-duplicate skills: `markdown-plus-plus:markdown-plus-plus` (this repo) and `webworks-claude-skills:markdown-plus-plus` (separate repo). After this PR, the two descriptions will diverge until the WebWorks repo updates. Acceptable -- the WebWorks repo manages its own release cadence and a follow-up audit can sync them.
- **Description-only changes can still affect activation in unexpected ways.** A longer, signal-rich description may compete with sibling skills for high-priority routing in some contexts. Mitigation: the rewrite preserves the "AUTHORITATIVE REFERENCE for Markdown++ syntax" lede that the routing layer keys on, and the additions are all genuine Markdown++ signals that should not over-trigger on plain CommonMark.

---

## References

- Origin issue: GitHub #84
- Current SKILL.md: `plugins/markdown-plus-plus/skills/markdown-plus-plus/SKILL.md` lines 3-7
- Version management workflow: `CLAUDE.md` § "Version Management"
- Bump script: `scripts/bump-version.sh`
