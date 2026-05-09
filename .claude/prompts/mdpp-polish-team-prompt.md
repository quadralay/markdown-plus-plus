# Markdown++ Polish Review — Team Prompt

Use the following prompt to launch the polish review team in your Claude
Code session. Copy everything between the --- markers.

Run this from inside the markdown-plus-plus repo so the agents have direct
access to the spec files.

---

Create a 4-person agent team for a final polish review of the Markdown++
specification. The spec is now considered complete — the goal of this
session is to identify what still needs polishing before public release.

This is NOT a gap-finding session. It is a readiness review.

Use these agent definitions from .claude/agents/:

1. @agent-spec-clarity-reviewer — Reads the spec as a first-time reader
   attempting to implement a parser from scratch. Flags ambiguity,
   missing examples, inconsistent terminology, and organizational
   issues that would slow down an independent implementor.

2. @agent-parser-spec-author — Returns in VERIFICATION mode. Cross-check
   the now-complete spec against the actual parser implementation to
   confirm they match. Flag any divergence, including spec rules that
   the implementation doesn't actually follow and implementation
   behavior that the spec doesn't cover.

3. @agent-adoption-evaluator — Final enterprise readiness pass.
   Re-evaluates the spec against the original adoption concerns
   (vendor independence, migration paths, governance, competitive
   positioning) and identifies anything that would still give an
   enterprise evaluator pause.

4. @agent-issue-prioritizer — Synthesizes findings from the other three
   teammates into a final polish backlog. Groups findings into
   release-blocker / pre-release-polish / post-release-improvement tiers
   and flags any items that need refinement before windworker dispatch.

External sources are defined in .claude/external-sources.conf — the
parser-spec-author agent should reference this for paths to the
ePublisher adapter code.

Workflow:
- Phase 1: spec-clarity-reviewer, parser-spec-author, and
  adoption-evaluator work in parallel. Each reviews the complete spec
  through their own lens. The clarity reviewer reads it cold. The
  spec-author verifies it against the implementation. The
  adoption-evaluator assesses enterprise readiness.
- Phase 2: issue-prioritizer collects findings and produces a tiered
  polish backlog organized by release urgency.

The goal: a focused list of remaining polish items, with clear
recommendations on which must be addressed before public release versus
which can ship after. Items marked "release-blocker" should be ready
for windworker dispatch with refined intent statements.

---
