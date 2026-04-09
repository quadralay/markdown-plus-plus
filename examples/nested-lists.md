---
mdpp-version: 1.0
date: 2026-04-08
status: active
---

<!-- style:Heading1; markers:{"Keywords": "nested lists, procedures, checklists"}; #600001 -->
# Nested lists

[nested-lists]: #600001 "Nested lists"

This example demonstrates styled nested lists for procedures, checklists, and hierarchical content in Markdown++.

<!-- style:Heading2; #600002 -->
## Styled procedure

[styled-procedure]: #600002 "Styled procedure"

Custom styles on ordered lists let publishing tools render numbered procedures with consistent formatting across documents.

<!-- style:ProcedureList -->
1. **Prepare the environment**
   - Verify system requirements:
     - Operating system is supported
     - Minimum 8 GB RAM available
     - 20 GB free disk space
   - Install prerequisites:
     - Python 3.10 or later
     - Node.js 18 LTS

2. **Configure the application**
   - Copy the sample configuration file:
     1. Locate `config.sample.json` in the installation directory
     2. Copy it to `config.json`
     3. Open `config.json` in a text editor
   - Set required values:
     - `database.host` -- your database server address
     - `database.port` -- default is 5432
     - `auth.secret` -- a secure random string

3. **Verify the installation**
   - Start the application
   - Check the health endpoint:
     - HTTP 200 indicates success
     - HTTP 503 indicates a missing dependency
   - Review the startup log for warnings

<!-- style:Heading2; #600003 -->
## Feature checklist

[feature-checklist]: #600003 "Feature checklist"

Task lists with nested items track progress across a multi-phase rollout.

<!-- style:ChecklistStyle -->
- [ ] Phase 1: Core functionality
  - [ ] User authentication
    - [ ] Login and registration
    - [ ] Password reset flow
    - [ ] Session management
  - [ ] Data import
    - [ ] CSV upload
    - [ ] API ingestion
- [ ] Phase 2: Integrations
  - [ ] Email notifications
    - [ ] Transactional emails
    - [ ] Digest summaries
  - [ ] Webhook support
    - [ ] Outbound event delivery
    - [ ] Retry with backoff
- [ ] Phase 3: Administration
  - [ ] User management dashboard
  - [ ] Audit logging
  - [ ] Role-based access control

<!-- style:Heading2; #600004 -->
## Nested bullet styles

[nested-bullet-styles]: #600004 "Nested bullet styles"

Each nesting level can carry its own style for differentiated formatting in published output.

<!-- style:BulletList1 -->
- Documentation standards
  - All public APIs must have reference documentation

  <!-- style:BulletList2 -->
  - Required sections for each endpoint:
    - Description
    - Parameters
    - Request example
    - Response example

    <!-- style:BulletList3 -->
    - Response examples must include:
      - Success case (HTTP 200)
      - Validation error (HTTP 400)
      - Authentication failure (HTTP 401)

Indented style directives apply to the list item at that nesting level. Each `<!-- style: -->` must be attached directly above its target (no blank line between).
