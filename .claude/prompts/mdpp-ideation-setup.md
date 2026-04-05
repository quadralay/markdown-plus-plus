# Ideation Team Setup Guide

## Prerequisites

1. Claude Code CLI with Opus 4.6 access (Pro or Max plan)
2. Agent Teams enabled in settings.json:
   ```json
   {
     "env": {
       "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
     }
   }
   ```

## Install Agent Definitions

Copy the four agent files into your project's agents directory:

```powershell
# From the markdown-plus-plus repo root
mkdir -p .claude/agents

# Copy agents (adjust source path to wherever you saved the downloads)
Copy-Item parser-spec-author.md .claude/agents/
Copy-Item spec-analyst.md .claude/agents/
Copy-Item adoption-evaluator.md .claude/agents/
Copy-Item issue-prioritizer.md .claude/agents/
```

## Launch the Ideation Session

```powershell
cd C:\Projects\markdown-plus-plus
claude
```

Once inside Claude Code, paste the team prompt from
mdpp-ideation-team-prompt.md (the content between the --- markers).

## During the Session

- Shift+Down — cycle to next teammate
- Shift+Up — cycle to previous teammate
- Ctrl+T — view shared task list
- Enter — send a message to the current teammate
- Escape — interrupt current teammate

You can talk to any teammate directly. For example, switch to
adoption-evaluator and ask follow-up questions about specific
competitive concerns, or redirect spec-analyst to dig deeper
into a particular extension's parsing rules.

## After the Session

The issue-prioritizer's output becomes your dispatch checklist.
For each issue marked "Ready for worker":

1. Verify the issue description meets your intent rubric
2. Use /windworker:dispatch to submit to the worker
3. Monitor PR activity on GitHub

For issues marked "Needs refinement":
- Update the issue description with the team's findings
- Re-run through the intent rubric
- Dispatch when ready
