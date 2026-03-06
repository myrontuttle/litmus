# 📚 Development Documentation Index

**Start here** → Links to all development workflow documentation

---

## 🎯 Pick Your Path

### 👤 "I'm a developer starting on this project"

1. Read: [GETTING_STARTED.md](GETTING_STARTED.md) (10 min)
2. Skim: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) (20 min)
3. Bookmark: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (reference)
4. Start: First feature using [TEMPLATES.md](TEMPLATES.md)

### 🤖 "I'm a coding agent working on tasks"

1. Read: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 9 (Agent Instructions)
2. Reference: [TEMPLATES.md](TEMPLATES.md) → Agent-Specific Task Format
3. Follow: [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) patterns
4. Before pushing: Run all checks from [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### 👥 "I'm handing work to an agent"

1. Create issue with: [TEMPLATES.md](TEMPLATES.md) → User Story
2. Follow protocol: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 2
3. Use template: [TEMPLATES.md](TEMPLATES.md) → Agent-Specific Task Format
4. Check: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 9

### 🔍 "I'm reviewing code"

1. Checklist: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 5
2. Template: [TEMPLATES.md](TEMPLATES.md) → Reviewer Checklist
3. Focus areas: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 5
4. Patterns: [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) (for reference)

### 📅 "It's Monday, time for sprint planning"

1. Updates: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 1
2. Planning: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) § 12
3. Create issues: [TEMPLATES.md](TEMPLATES.md) → User Story

---

## 📖 Complete Documentation Set

### [GETTING_STARTED.md](GETTING_STARTED.md)

**Purpose:** Entry point and navigator for all documentation  
**Length:** ~10-15 min read  
**Update frequency:** Rarely  
**Contains:**

- Overview of all documentation
- Quick start paths
- Common workflows
- When to reference each document
- Sprint cycle outline
- Next steps

**When to use:** First time, or when unsure where to look

---

### [WORKFLOW_VISUAL_GUIDE.md](WORKFLOW_VISUAL_GUIDE.md)

**Purpose:** Visual flowcharts and decision trees  
**Length:** ~5 min read  
**Update frequency:** Occasionally  
**Contains:**

- Sprint cycle diagram
- Feature development flowchart
- Human-agent handoff diagram
- Document map
- Decision tree
- Common questions → which document

**When to use:** Need quick visual reference of process flow

---

### [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)

**Purpose:** Comprehensive development guide  
**Length:** ~40 min initial read, reference guide after  
**Update frequency:** Monthly (as practices evolve)  
**Sections:**

1. Weekly Dependency & Framework Updates
2. Human-Agent Development Sync Protocol
3. Starting a Feature (Requirements & Planning)
4. Development Checklist (Implementation)
5. Code Review & Quality Standards
6. Completing & Merging Work
7. Commit Message Conventions
8. Continuous Updates While Working
9. Agent-Specific Instructions
10. Quick Reference Commands
11. Common Issues & Solutions
12. Agile Sprint Template

**When to use:**

- Starting any feature or task
- Handing off to an agent
- Preparing for code review
- Troubleshooting issues
- Planning sprints

---

### [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Purpose:** Fast command/checklist lookup during development  
**Length:** ~5 min read (but you'll reference sections often)  
**Update frequency:** Quarterly  
**Contains:**

- Starting new feature (steps)
- Commit workflow
- Pre-review checklist
- Human-agent handoff
- Weekly dependency updates
- Common commands table
- File locations table
- Security reminders
- Getting help links

**When to use:**

- Mid-development (checking a command)
- Quick reminder of checklist
- Looking up file locations
- Verifying correct procedure

---

### [TEMPLATES.md](TEMPLATES.md)

**Purpose:** Copy-paste templates for issues and PRs  
**Length:** ~20 min initial read  
**Update frequency:** Quarterly  
**Contains:**

- User Story issue template
- Bug Report issue template
- Feature PR template
- Bug Fix PR template
- Refactoring PR template
- Code Review checklist
- Commit message best practices
- Agent-specific task format
- Using these templates guide

**When to use:**

- Creating any GitHub issue
- Creating any GitHub PR
- Requesting task from agent
- Reviewing code

---

### [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)

**Purpose:** Test-Driven Development patterns & code generation techniques  
**Length:** ~30 min read  
**Update frequency:** Quarterly  
**Sections:**

1. TDD Workflow (Red → Green → Refactor)
2. Comprehensive Test Coverage (Models, Services, Routes, Integration)
3. TDD Best Practices
4. Code Generation Patterns
5. TDD + Code Generation Combined
6. Checklist: TDD Development Cycle

**When to use:**

- Before implementing a feature (write tests first)
- Need example test for MongoDB async code
- Wondering if you should use CRUD factory
- Need template for service/route tests
- Reviewing code for test adequacy

---

## 🔀 Document Relationships

```text
GETTING_STARTED.md (Entry point)
├─ Points to WORKFLOW_VISUAL_GUIDE.md (Visual understanding)
│   ├─ References DEVELOPMENT_WORKFLOW.md (Process details)
│   ├─ References TEMPLATES.md (Issue/PR format)
│   └─ References TDD_AND_CODEGEN.md (Code patterns)
│
├─ Points to QUICK_REFERENCE.md (Daily commands)
│   └─ Summarizes DEVELOPMENT_WORKFLOW.md § 10
│
├─ Points to DEVELOPMENT_WORKFLOW.md (Main guide)
│   ├─ § 1: Dependency updates (use weekly)
│   ├─ § 2-6: Feature dev cycle (use per feature)
│   ├─ § 7: Commit format (always use)
│   ├─ § 9: Agent instructions (if using agents)
│   ├─ § 11: Troubleshooting (when stuck)
│   └─ § 12: Sprint planning (use weekly)
│
├─ Points to TEMPLATES.md (Copy-paste templates)
│   ├─ For issues: User Story, Bug Report templates
│   ├─ For PRs: Feature, Fix, Refactor templates
│   ├─ For review: Reviewer Checklist
│   └─ For agents: Agent-Specific Task Format
│
└─ Points to TDD_AND_CODEGEN.md (Code patterns)
    ├─ Part 1: TDD patterns with examples
    ├─ Part 2: Code generation techniques
    └─ Part 3: Combined approach
```

---

## 📋 Quick Checklist Method

### Starting a New Feature

```text
1. [ ] Read: DEVELOPMENT_WORKFLOW.md § 3
2. [ ] Create issue: Use TEMPLATES.md User Story
3. [ ] Plan tests: Review TDD_AND_CODEGEN.md § Part 1
4. [ ] Implement: Follow DEVELOPMENT_WORKFLOW.md § 4
5. [ ] Review: Use TEMPLATES.md Pre-Review Checklist
6. [ ] Submit PR: Use TEMPLATES.md Feature PR Template
```

### Handing Off to Agent

```text
1. [ ] Follow: TEMPLATES.md Agent-Specific Task Format
2. [ ] Reference: DEVELOPMENT_WORKFLOW.md § 9
3. [ ] Push code with clear commits
4. [ ] Create PR (don't merge)
5. [ ] Leave detailed instructions in PR comment
```

### Reviewing Agent's Work

```text
1. [ ] Use: TEMPLATES.md Reviewer Checklist
2. [ ] Follow: DEVELOPMENT_WORKFLOW.md § 5
3. [ ] Check: Code patterns reference TDD_AND_CODEGEN.md
4. [ ] Approve or request changes
5. [ ] Merge using: DEVELOPMENT_WORKFLOW.md § 6
```

---

## 🎓 Learning Resources

| Need | Document | Section |
|------|----------|---------|
| **Getting Started** |  |  |
| Where do I begin? | GETTING_STARTED.md | Entire doc |
| Visual process? | WORKFLOW_VISUAL_GUIDE.md | Entire doc |
| **Daily Development** |  |  |
| What command? | QUICK_REFERENCE.md | Entire doc |
| Start feature? | DEVELOPMENT_WORKFLOW.md | § 3 |
| Write tests? | TDD_AND_CODEGEN.md | Part 1 |
| **Code Quality** |  |  |
| Format/lint? | DEVELOPMENT_WORKFLOW.md | § 4 |
| Code review? | DEVELOPMENT_WORKFLOW.md | § 5 |
| Test patterns? | TDD_AND_CODEGEN.md | Entire doc |
| **Collaboration** |  |  |
| Hand off to agent? | DEVELOPMENT_WORKFLOW.md | § 2 & 9 |
| Task format? | TEMPLATES.md | Agent-Specific |
| Review code? | TEMPLATES.md | Reviewer Checklist |
| **Sprints & Planning** |  |  |
| Weekly updates? | DEVELOPMENT_WORKFLOW.md | § 1 |
| Sprint plan? | DEVELOPMENT_WORKFLOW.md | § 12 |
| Create issue? | TEMPLATES.md | User Story |
| **Troubleshooting** |  |  |
| Tests failing? | TDD_AND_CODEGEN.md | § 3 |
| Merge conflict? | DEVELOPMENT_WORKFLOW.md | § 11 |
| Dep issue? | DEVELOPMENT_WORKFLOW.md | § 1 & 11 |

---

## 🚀 Getting Started Right Now

### 5-Minute Quick Start

1. Read the **"Pick Your Path"** section above (your role)
2. Open the first recommended document
3. Skim the first section
4. You're ready!

### 30-Minute Setup

1. Read: GETTING_STARTED.md
2. Skim: DEVELOPMENT_WORKFLOW.md § 2-3
3. Save: QUICK_REFERENCE.md bookmark
4. Review: TEMPLATES.md templates
5. Copy templates into GitHub

### 1-Hour Complete Onboarding

1. Read: [GETTING_STARTED.md](GETTING_STARTED.md)
2. Skim: [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) (all sections)
3. Review: [TEMPLATES.md](TEMPLATES.md)
4. Scan: [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) examples
5. Create first feature branch
6. Create first issue using template

---

## 📊 Documentation Overview Table

| Document | Type | Length | Use Frequency | Best For |
|----------|------|--------|---------------|----------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Guide | 10-15 min | First time + occasional | Orientation & navigation |
| [WORKFLOW_VISUAL_GUIDE.md](WORKFLOW_VISUAL_GUIDE.md) | Reference | 5 min | Weekly | Flowcharts & decision trees |
| [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) | Guide | 40 min | Multiple times per sprint | Main development process |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Cheat sheet | 5 min | Daily | Commands & quick reminders |
| [TEMPLATES.md](TEMPLATES.md) | Templates | 20 min | Per issue/PR | Issues, PRs, code review |
| [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md) | Guide | 30 min | Per feature | Test patterns & generation |

---

## 💡 Pro Tips

1. **Bookmark QUICK_REFERENCE.md** - You'll use it constantly
2. **Copy templates into GitHub** - Makes compliance automatic
3. **Review TDD patterns** - Before each feature, pick a pattern
4. **Follow the section numbers** - DEVELOPMENT_WORKFLOW.md is organized sequentially
5. **Update docs monthly** - Add team learnings and new patterns
6. **Reference when unsure** - Better to check than guess
7. **Share with agents** - Agents follow these patterns
8. **Print WORKFLOW_VISUAL_GUIDE.md** - Hang in team space

---

## 🎯 Success Criteria

You're using these docs effectively when:

- ✅ All team members (human + agents) follow the same patterns
- ✅ Issues & PRs use consistent templates
- ✅ Sprints are planned Monday morning
- ✅ Code reviews are fast & thorough
- ✅ Tests are written before code
- ✅ Dependencies updated weekly
- ✅ Commits are atomic & clear
- ✅ Handoffs between human/agent are smooth
- ✅ Zero broken builds
- ✅ New features deployed confidently

---

## 📞 Questions or Issues?

| Question | Answer |
|----------|--------|
| Which doc? | Use table above or WORKFLOW_VISUAL_GUIDE.md decision tree |
| How do I...? | Check QUICK_REFERENCE.md first, then DEVELOPMENT_WORKFLOW.md |
| What pattern? | See TDD_AND_CODEGEN.md for code patterns |
| Help with template? | See TEMPLATES.md section that matches your need |
| Issue with process? | Check DEVELOPMENT_WORKFLOW.md § 11 (Common Issues) |
| Framework question? | See AGENTS.md (framework guide) or https://vibetuner.alltuner.com/llms.txt |
| Bug in vibetuner? | File at https://github.com/alltuner/vibetuner/issues |

---

## 🚀 Next Steps

**Right now, pick ONE:**

1. [ ] Read [GETTING_STARTED.md](GETTING_STARTED.md)
2. [ ] Skim [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)
3. [ ] Copy templates from [TEMPLATES.md](TEMPLATES.md)
4. [ ] Review [TDD_AND_CODEGEN.md](TDD_AND_CODEGEN.md)
5. [ ] Bookmark [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

Then start building! 🎉

---

**Last Updated:** March 6, 2026  
**Version:** 1.0  
**Framework:** vibetuner + FastAPI + MongoDB + HTMX  

Enjoy using these workflows! They'll help you build great software efficiently with or without agents.
