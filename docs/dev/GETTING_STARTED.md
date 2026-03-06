# Getting Started with Agile Development Workflows

A quick guide to all the documentation for agile, lean development with coding agents.

---

## 📚 Documentation Overview

This project now includes comprehensive guidance for developing with agile and lean
software engineering practices. Here's what each document covers:

### [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)

**Main reference guide** (~40 min read initially, then reference during sprints)

The most important document. It covers:

- **👥 Section 1**: Weekly dependency & framework updates (30 min/week)
- **🤝 Section 2**: Human-agent sync protocols (daily/per-handoff)
- **🎯 Sections 3-7**: Feature development workflow from requirements → merge
- **📤 Section 7**: Commit message conventions
- **🤖 Section 9**: Specific instructions for agents
- **⏱️ Section 10**: Quick reference commands
- **🆘 Section 11**: Common issues & solutions
- **📋 Section 12**: Sprint template (copy for each sprint)

**When to use this**:

- Starting a new feature
- Handing work to an agent
- Receiving completed work from an agent
- Creating pull requests
- During code reviews

---

### [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Daily command reference** (~5 min read, 30 seconds lookup)

Condensed version for quick lookups:

- Common bash commands
- Git workflow
- Pre-review checklist
- File locations
- Common issues

**When to use this**:

- You're mid-development and need a quick reminder
- Checking which command to run
- Starting a new PR

---

### [TEMPLATES.md](TEMPLATES.md)

**GitHub issue & PR templates** (~20 min read initially)

Copy-paste templates for:

- User Story issues
- Bug Report issues
- Feature PR templates
- Bug Fix PR templates
- Refactoring PR templates
- Review checklists
- Agent-specific task format

**When to use this**:

- Creating a GitHub issue
- Submitting a pull request
- Requesting work from an agent
- Reviewing code

---

### [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)

**Test-Driven Development & Code Generation** (~30 min read)

Practical TDD patterns and code generation techniques:

- Red → Green → Refactor cycle with examples
- Test coverage patterns (models, services, routes, integration)
- Writing async tests properly
- Fixtures and mocking
- CRUD factory pattern (auto-generate endpoints)
- Service factory pattern
- Code generation workflow
- TDD + code generation combined

**When to use this**:

- Starting feature development
- Writing tests before code
- Using auto-generation for CRUD endpoints
- Need examples of proper test patterns

---

## �️ Prerequisites & Tool Installation

Before starting development, ensure you have these tools installed. This project uses
modern Python and JavaScript tooling that requires specific installations.

### Required Tools

| Tool | Purpose | Installation (Ubuntu/Debian) |
|------|---------|------------------------------|
| **uv** | Fast Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **bun** | Fast JavaScript runtime/package manager | `curl -fsSL https://bun.sh/install \| bash` |
| **just** | Command runner for project tasks | `curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh \| bash` |
| **git** | Version control | `sudo apt update && sudo apt install git` |
| **Python 3.11+** | Programming language (managed by uv) | Included with uv |
| **Node.js 18+** | JavaScript runtime (managed by bun) | Included with bun |

### Installation Steps

1. **Install uv** (Python package manager):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Add ~/.cargo/bin to PATH if prompted
   ```

2. **Install bun** (JavaScript runtime):

   ```bash
   curl -fsSL https://bun.sh/install | bash
   # Restart your shell or run: source ~/.bashrc
   ```

3. **Install just** (command runner):

   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash
   ```

4. **Verify installations**:

   ```bash
   uv --version
   bun --version
   just --version
   git --version
   ```

### Optional Dependencies

For full development (database, background jobs):

- **MongoDB**: `sudo apt install mongodb` or use Docker
- **Redis**: `sudo apt install redis-server` or use Docker

### Troubleshooting

- **PATH issues**: After installation, restart your terminal or run `source ~/.bashrc`
- **Permission denied**: You may need to add `~/.local/bin` to PATH
- **Old versions**: Update with the same install commands above

---

## �🚀 Quick Start: Use These Now

### First Time Setup

1. **Read this section** (you're reading it now) ✅

2. **Skim [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)** - Get familiar with sections:
   - Section 2 (Human-Agent Sync)
   - Section 3 (Starting a Feature)
   - Section 6 (Code Review)

3. **Bookmark [QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - You'll reference this constantly

4. **Copy templates from [TEMPLATES.md](TEMPLATES.md)** into GitHub:
   - Go to your repo settings
   - Under "Code & automation" → "Templates"
   - Paste issue and PR templates

5. **Review [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)** - Focus on patterns that apply to current work

### For Your First Feature

```bash
# 1. Create a well-structured GitHub issue using [TEMPLATES.md](TEMPLATES.md)

# 2. Create feature branch
git checkout -b feature/name

# 3. Plan tests using [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) patterns

# 4. Reference [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) Section 4-6 while implementing

# 5. Before pushing:
just format && just lint && uv run pytest -v

# 6. Create PR using template from [TEMPLATES.md](TEMPLATES.md)

# 7. Use Section 5 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) for review
```

---

## 🎯 Common Workflows

### "I'm Starting a New Feature"

1. Read [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → Section 3 (Starting a Feature)
2. Use template from [TEMPLATES.md](TEMPLATES.md) → User Story
3. Use patterns from [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)

### "I Need to Hand Off Work to an Agent"

1. Push code with clear commits
2. Create PR with template from [TEMPLATES.md](TEMPLATES.md)
3. Section 2 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → "Handoff Between Human and Agent"
4. Follow "Agent-Specific Format" from [TEMPLATES.md](TEMPLATES.md)

### "I'm Reviewing an Agent's Code"

1. Section 5 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → Code Review
2. Use checklist from [TEMPLATES.md](TEMPLATES.md) → Reviewer Checklist
3. Reference [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) for code patterns

### "My Tests Are Failing"

1. Check [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) → Common patterns
2. Check [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → Section 11 (Common Issues)

### "I Need to Update Dependencies"

1. [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → Section 1 (Weekly Updates)
2. Use commands from [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### "It's Monday Morning"

1. [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → Section 1 (30 min protocol)
2. [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) → Section 12 (Plan sprint)

---

## 📋 Checklist: Before Sending Work to Agent

Always provide agents with:

- [ ] Link to GitHub issue (or full requirements text)
- [ ] Expected file locations (copied from [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) Section 4)
- [ ] Reference similar code in codebase (show examples)
- [ ] Specific acceptance criteria (from issue)
- [ ] Template from [TEMPLATES.md](TEMPLATES.md) → Agent-Specific Task Format
- [ ] Expected test scenarios

Example:

```text
Issue: #123 - Implement user authentication

Acceptance Criteria (from issue):
- POST /auth/signup should accept {email, password}
- Should validate email format
- Should hash password before storing
- Should return 201 with user ID on success

File locations (from DEVELOPMENT_WORKFLOW.md):
- Models: src/app/models/user.py
- Routes: src/app/frontend/routes/auth.py
- Tests: tests/test_auth_routes.py

Reference code:
- Similar endpoint: src/app/frontend/routes/login.py
- Model example: src/app/models/user.py

Test patterns (from TDD_AND_CODEGEN.md):
- Use @pytest.mark.asyncio
- Use fixtures for setup
- Test one thing per test
- Include error path tests

Ready for implementation!
```

---

## 🏃 Sprint Cycle (Weekly)

### Monday - Planning & Updates (1 hour)

1. **Update dependencies** (Section 1 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md))

   ```bash
   just update-repo-deps
   uv run pytest -v
   ```

2. **Review framework changelog**
   - Check: https://vibetuner.alltuner.com/llms.txt

3. **Plan sprint** (Section 12 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md))

   ```text
   # Sprint: Week of [DATE]
   ## Sprint Goal: [...]
   ## Stories: [...]
   ```

4. **Create GitHub issues** using [TEMPLATES.md](TEMPLATES.md) templates

### Daily - Development & Sync

1. **Pull latest main** before starting work

   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Follow development workflow** (Section 3 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md))
   - Write tests first ([TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md))
   - Implement feature
   - Run checks before commit

3. **Commit atomically** with proper messages

   ```bash
   git commit -m "feat(scope): description"
   ```

4. **Update TODO/status** (Section 2 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md))

### Before Pull Request

1. **Run all checks**

   ```bash
   uv run pytest -v
   just type-check
   just format
   just lint
   ```

2. **Use PR template** from [TEMPLATES.md](TEMPLATES.md)

3. **Reference issue** in PR description

### During Code Review (Section 5 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md))

1. Follow review checklist from [TEMPLATES.md](TEMPLATES.md)

2. Check:
   - Requirements met
   - Tests adequate
   - Code quality
   - Security
   - Performance

3. Approve or request changes

### Friday - Reflection

- Document what was completed
- Note blockers or learnings
- Update sprint notes (Section 12 of [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md))

---

## 🤖 For Coding Agents

When working with AI coding agents, always:

1. **Provide clear context** using templates from [TEMPLATES.md](TEMPLATES.md)
2. **Reference this documentation** (e.g., "Follow Section 4 of DEVELOPMENT_WORKFLOW.md")
3. **Use specific patterns** from [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)
4. **Expect this format** in responses:
   - ✅ Acceptance criteria verified
   - 🔄 Status of what was completed
   - 📝 PR with proper template
   - 🚫 Any blockers faced

Agents should:

- Always run `just format && just lint && uv run pytest -v` before pushing
- Use templates provided, not their own format
- Follow TDD patterns from [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)
- Document decisions clearly in PR descriptions

---

## 📊 Metrics to Track

Setup weekly tracking to measure progress:

```markdown
# Sprint Metrics - Week of [DATE]

## Velocity

- Issues completed: N
- Features delivered: N
- Bugs fixed: N
- Points completed: N

## Code Quality

- Test coverage: X%
- Type check pass rate: Y%
- Lint failures fixed: Z%

## Collaboration

- PRs merged: N
- Code review time: X hours
- Handoffs with agents: N

## Dependencies

- Packages updated: N
- Security patches: N
- Breaking changes: N
```

---

## 🔄 Continuous Improvement

These guidelines should evolve with your project:

1. **Every sprint**: Review what worked and what didn't
2. **Monthly**: Update documentation with team learnings
3. **Document gotchas**: Add Section 11 items to guide future work
4. **Discover patterns**: Identify repeated work that could be automated
5. **Share with agents**: Update instructions based on issues discovered

---

## ✅ Final Checklist

Before starting development with agents:

- [ ] Read this file (10 min)
- [ ] Skim DEVELOPMENT_WORKFLOW.md (20 min)
- [ ] Save QUICK_REFERENCE.md bookmark (1 min)
- [ ] Review TEMPLATES.md (15 min)
- [ ] Scan TDD_AND_CODEGEN.md examples (10 min)
- [ ] Create first GitHub issue using templates
- [ ] Assign first task and give agent context
- [ ] Run first dev cycle

---

## 📞 When to Reference Each Doc

| Situation | Reference |
|-----------|-----------|
| Starting feature | DEVELOPMENT_WORKFLOW.md → Section 3 |
| Writing tests | TDD_AND_CODEGEN.md → Part 1 & 2 |
| Quick command lookup | QUICK_REFERENCE.md |
| Creating issues/PRs | TEMPLATES.md |
| Reviewing code | DEVELOPMENT_WORKFLOW.md → Section 5 |
| Handing off to agent | TEMPLATES.md → Agent-Specific Format |
| Weekly dependencies | DEVELOPMENT_WORKFLOW.md → Section 1 |
| Common problems | DEVELOPMENT_WORKFLOW.md → Section 11 |
| Code generation | TDD_AND_CODEGEN.md → Part 2 |
| Sprint planning | DEVELOPMENT_WORKFLOW.md → Section 12 |

---

## 🎓 Key Principles

All these documents follow these core principles:

1. **Repeatability**: Use the same process every time (consistency)
2. **Clarity**: Everyone (human + agents) understands the workflow
3. **Testability**: Everything testable before merging (TDD)
4. **Traceability**: Each change linked to an issue
5. **Automation**: Let tools enforce standards (format/lint/type)
6. **Lean**: Minimal overhead, maximum progress
7. **Agile**: Quick feedback loops, continuous improvement

---

## Next Steps

1. **Right now**: Send links to these docs to your team/agents
2. **This week**: Try first workflow using DEVELOPMENT_WORKFLOW.md
3. **This sprint**: Use templates for all issues/PRs
4. **Next sprint**: Update docs with team learnings

Good luck building! 🚀

---

**Questions?** Refer back to the specific section, or check:

- Framework guide: AGENTS.md
- Framework docs: https://vibetuner.alltuner.com/llms.txt
- File issues: https://github.com/alltuner/vibetuner/issues
