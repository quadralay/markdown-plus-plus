# Markdown++ Public Readiness — Ideation Team Prompt

Use the following prompt to launch the agent team in your Claude Code session.
Copy everything between the --- markers.

---

Create a 4-person agent team for evaluating the markdown-plus-plus repo's
readiness for public consumption by enterprise documentation teams.

Use these agent definitions from .claude/agents/:

1. @agent-parser-spec-author — Examines the Markdown++ implementation code
   to extract actual parsing rules, extension interactions, and edge case
   behavior. Documents findings as formal specification language that a
   third party could use to build a conforming parser. Start this agent
   first since its findings inform the other two reviewers.

2. @agent-spec-analyst — Reviews the current documentation and open issues
   for completeness gaps, ambiguous parsing rules, and undefined edge
   cases. Cross-reference against parser-spec-author's findings to
   identify where documentation diverges from implementation behavior.

3. @agent-adoption-evaluator — Evaluates the repo from the perspective of
   a company deciding whether to adopt Markdown++. Assesses vendor
   independence, migration paths, ecosystem maturity, governance, and
   competitive positioning. Uses parser-spec-author's findings to assess
   how feasible it would be for a third party to build their own parser.

4. @agent-issue-prioritizer — Takes findings from the other three
   teammates and builds a prioritized dispatch plan. Groups issues into
   must-have / should-have / nice-to-have tiers, identifies dependencies,
   and flags issues that need refinement before windworker dispatch.

External sources (full file access available):

- Parser implementation:
  C:\Repo\ePublisher_debug\trunk\files\webworks\Adapters\helper\markdown
  Entry point: driver.py
  This is the authoritative source for how Markdown++ extensions are
  actually parsed and rendered by ePublisher.

- Legacy authoring documentation:
  C:\Projects\epublisher-docs\legacy\authoring-source-documents\markdown
  Entry point: _markdown.md
  This is the existing user-facing documentation for Markdown++ syntax
  as shipped with ePublisher. Useful for identifying what was documented
  versus what was left implicit.

Workflow:
- Phase 1: parser-spec-author examines the parser implementation at
  the ePublisher path above (starting from driver.py) and documents
  the actual parsing rules for each Markdown++ extension. Also review
  the legacy documentation to identify gaps between what's documented
  and what's implemented. Share findings with spec-analyst and
  adoption-evaluator when complete.
- Phase 2: spec-analyst and adoption-evaluator work in parallel, using
  parser-spec-author's findings alongside open issues and existing docs.
  Both also review open issues via `gh issue list --state open --limit 50`.
- Phase 3: issue-prioritizer synthesizes all findings into a tiered
  dispatch plan.

The parser-spec-author should also propose NEW issues for any parsing
rules or extension behaviors that are implemented but have no
corresponding documentation or open issue. These become candidates for
the dispatch plan.

The goal: a prioritized, dependency-aware list of issues ready for
windworker dispatch, with clear notes on any issues that need refinement
before they meet our intent rubric. Spec documentation issues identified
by parser-spec-author should be included alongside existing open issues.

---
