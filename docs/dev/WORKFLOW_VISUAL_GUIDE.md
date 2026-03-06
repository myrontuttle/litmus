# Development Workflow Visual Guide

Quick visual reference for the development process and which documents to use.

---

## 📊 Overall Development Cycle

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    SPRINT CYCLE (Weekly)                            │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │  MONDAY MORNING  │  → Check dependencies (DEVELOPMENT_WORKFLOW.md § 1)
    │   (30 minutes)   │  → Update framework changelog
    │                  │  → Run full tests
    └────────┬─────────┘
             │
    ┌────────▼──────────────────────────────────────────┐
    │ Plan Sprint & Create Issues                       │
    │ Use templates from TEMPLATES.md                   │
    │ Set velocity estimate per story                   │
    └────────┬───────────────────────────────────────────┘
             │
    ┌────────▼──────────────────────────────────┐
    │ DAILY: Feature Development Cycle           │
    │ (See detailed workflow below)              │
    │                                            │
    │ • Human develops features                  │
    │ • Agent develops features                  │
    │ • Handoffs between human/agent            │
    │ • Daily sync on TODO status               │
    └────────┬──────────────────────────────────┘
             │
    ┌────────▼──────────────────────────────────┐
    │ FRIDAY: Review & Close Out                 │
    │ • Verify completed items                  │
    │ • Merge all PRs                           │
    │ • Document learnings                      │
    │ • Update sprint notes                     │
    └────────┬──────────────────────────────────┘
             │
    ┌────────▼────────────┐
    │ NEXT MONDAY: REPEAT │
    └─────────────────────┘
```

---

## 🔄 Feature Development Workflow (Per Feature)

```text
┌─────────────────────────────────────────────────────────────┐
│               FEATURE DEVELOPMENT CYCLE                      │
└─────────────────────────────────────────────────────────────┘

PHASE 1: REQUIREMENTS
  ├─ Create issue: Use TEMPLATES.md → User Story
  ├─ Write acceptance criteria (testable!)
  ├─ Link dependencies
  └─ Assign to human or agent
      ↓
PHASE 2: DESIGN (if complex)
  ├─ Create design doc: /docs/design-[feature].md
  ├─ Diagram architecture
  ├─ Define data models
  ├─ Plan API endpoints
  └─ Reference: DEVELOPMENT_WORKFLOW.md § 3.1
      ↓
PHASE 3: SETUP
  ├─ Create feature branch: feature/descriptive-name
  ├─ Start dev: just local-all
  ├─ Create TODO list (manage_todo_list)
  └─ Reference: DEVELOPMENT_WORKFLOW.md § 3.2
      ↓
PHASE 4: TEST PLANNING (TDD)
  ├─ Write failing tests FIRST
  ├─ Define test coverage
  ├─ Mock external services
  └─ Reference: TDD_AND_CODEGEN.md § Part 1
      ↓
PHASE 5: IMPLEMENTATION
  ├─ Write models (if needed)
  ├─ Implement services/business logic
  ├─ Create routes/API endpoints
  ├─ Build templates/UI
  ├─ Make atomic commits
  └─ Reference: TDD_AND_CODEGEN.md § Part 2 & 3
      ↓
PHASE 6: QUALITY CHECKS
  ├─ Run tests:      uv run pytest -v
  ├─ Format code:    just format
  ├─ Lint:           just lint
  ├─ Type check:     just type-check
  └─ Reference: QUICK_REFERENCE.md
      ↓
PHASE 7: CODE REVIEW
  ├─ Create PR: Use TEMPLATES.md
  ├─ Link issue: "Closes #123"
  ├─ Describe changes & testing
  ├─ Request review
  └─ Reference: DEVELOPMENT_WORKFLOW.md § 5 & 6
      ↓
PHASE 8: MERGE
  ├─ Receive approval ✓
  ├─ All CI checks pass ✓
  ├─ Squash merge to main
  └─ Reference: DEVELOPMENT_WORKFLOW.md § 6
      ↓
    FEATURE COMPLETE ✓
```

---

## 👥 Human-Agent Handoff Protocol

```text
┌──────────────────────────────────┐
│  HUMAN DEVELOPER                 │
└──────────────────────────────────┘
        │
        ├─ 1. Complete work phase:
        │      • Write code
        │      • Commit clearly
        │      • Run all checks
        │      • Create PR (don't merge)
        │
        ├─ 2. Document handoff:
        │      • PR description: What was done
        │      • Comment: "Ready for [next phase]"
        │      • Push to feature/X branch
        │      │
        │      └──────────────────┐
        │                         │
   GIT REPOSITORY (GitHub)        │
   ├─ Branch: feature/X ◄─────────┴─ Code pushed
   └─ PR: [description] ◄──────────── Detailed context
                 │
                 ▼
   ┌──────────────────────────────────┐
   │  CODING AGENT                    │
   └──────────────────────────────────┘
        │
        ├─ 1. Review PR description & linked issue
        │      • Understand what done
        │      • Understand next steps
        │
        ├─ 2. Implement next phase:
        │      • Clone branch locally
        │      • Write tests first
        │      • Implement features
        │      • Run all checks
        │      • Commit clearly
        │
        ├─ 3. Document completion:
        │      • Push to same branch
        │      • Comment on PR: What was completed
        │      • Note any blockers
        │      │
        │      └──────────────────┐
        │                         │
   GIT REPOSITORY (GitHub)        │
   ├─ Branch: feature/X ◄─────────┴─ Code pushed
   └─ PR: [updated] ◄────────────── Ready for review
                 │
                 ▼
   ┌──────────────────────────────────┐
   │  HUMAN DEVELOPER (Review)        │
   └──────────────────────────────────┘
        │
        ├─ 1. Review agent's changes
        │      • Verify acceptance criteria met
        │      • Review new code
        │      • Check test coverage
        │
        ├─ 2. Approve & Merge (or request changes)
        │      • Squash merge to main
        │      • Update issue status
        │
        └─ Feature complete ✓
```

---

## 📖 Document Map

```text
┌─────────────────────────────────────────────────────────────────┐
│  WHERE TO FIND WHAT YOU NEED                                    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐
│ GETTING_STARTED.md           │ ← YOU ARE HERE
│ (This file)                  │
│                              │
│ Q: Where do I start?         │
│ Q: How does this all fit?    │
│ A: Read this file            │
└──────────────────────────────┘
         │
    ┌────┴────────────────┬────────────────┬──────────────────┐
    │                     │                │                  │
    ▼                     ▼                ▼                  ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
│ QUICK_          │ │ DEVELOPMENT_ │ │ TEMPLATES.   │ │ TDD_AND_        │
│ REFERENCE.md    │ │ WORKFLOW.md  │ │ md           │ │ CODEGEN.md      │
│                 │ │              │ │              │ │                 │
│ 5 min read      │ │ 40 min read  │ │ 20 min read  │ │ 30 min read     │
│ (for daily use) │ │ (comprehensive)│ │ (templates) │ │ (patterns)      │
├─────────────────┤ ├──────────────┤ ├──────────────┤ ├─────────────────┤
│ Q: What's the   │ │ Q: How do I  │ │ Q: What     │ │ Q: How do I     │
│ command again?  │ │ start a      │ │ should my   │ │ write tests?    │
│                 │ │ feature?     │ │ issue look  │ │                 │
│ Q: File         │ │              │ │ like?       │ │ Q: How do I     │
│ locations?      │ │ Q: How do I  │ │              │ │ generate API    │
│                 │ │ hand off to  │ │ Q: What     │ │ endpoints?      │
│ Q: Common       │ │ agents?      │ │ should my   │ │                 │
│ commands?       │ │              │ │ PR look     │ │ Q: What         │
│                 │ │ Q: How do I  │ │ like?       │ │ patterns work?  │
│                 │ │ review code? │ │              │ │                 │
│                 │ │              │ │ A: Copy     │ │ A: See examples │
│ A: Use this!    │ │ A: Follow    │ │ templates   │ │ & follow TDD    │
│                 │ │ sections 1-6 │ │              │ │ cycle!          │
└─────────────────┘ └──────────────┘ └──────────────┘ └─────────────────┘
```

---

## 🎯 Common Questions → Which Document?

```text
Q: How do I start developing?
→ DEVELOPMENT_WORKFLOW.md § 3

Q: What commands do I run?
→ QUICK_REFERENCE.md or DEVELOPMENT_WORKFLOW.md § 10

Q: How do I write my issue?
→ TEMPLATES.md → User Story template
→ DEVELOPMENT_WORKFLOW.md § 3.1

Q: How do I write tests first?
→ TDD_AND_CODEGEN.md § Part 1
→ DEVELOPMENT_WORKFLOW.md § 3.3

Q: Should I generate this code?
→ TDD_AND_CODEGEN.md § Part 2 & 3

Q: What should my PR look like?
→ TEMPLATES.md → Feature PR template
→ DEVELOPMENT_WORKFLOW.md § 5-6

Q: How do I hand work to an agent?
→ TEMPLATES.md → Agent-Specific Task Format
→ DEVELOPMENT_WORKFLOW.md § 2 & 9

Q: How do I review my agent's code?
→ DEVELOPMENT_WORKFLOW.md § 5
→ TEMPLATES.md → Reviewer Checklist

Q: What's the commit message format?
→ DEVELOPMENT_WORKFLOW.md § 7

Q: Something is broken, what do I do?
→ DEVELOPMENT_WORKFLOW.md § 11 (Common Issues)

Q: How do I check for updates?
→ DEVELOPMENT_WORKFLOW.md § 1

Q: How do I plan a sprint?
→ DEVELOPMENT_WORKFLOW.md § 12
→ GETTING_STARTED.md (this file) § Sprint Cycle
```

---

## 📋 Pre-Development Checklist

```text
□ Read GETTING_STARTED.md (you're here!)
□ Skim DEVELOPMENT_WORKFLOW.md § 2-3
□ Bookmark QUICK_REFERENCE.md  
□ Review TEMPLATES.md
□ Scan TDD_AND_CODEGEN.md examples
□ Copy templates into GitHub repo
□ Create first feature branch
□ Create first GitHub issue using template
□ Run: just local-all
□ Write first failing test
□ Implement to make test pass
□ Create first PR using template
□ Get first code review done
□ Success! 🎉
```

---

## ⚡ Quick Command Reference

| What | Command | Where |
|------|---------|-------|
| Start dev | `just local-all` | QUICK_REFERENCE.md |
| Run tests | `uv run pytest -v` | QUICK_REFERENCE.md |
| Format code | `just format` | QUICK_REFERENCE.md |
| Type check | `just type-check` | QUICK_REFERENCE.md |
| Update deps | `just update-repo-deps` | QUICK_REFERENCE.md |
| Create branch | `git checkout -b feature/name` | QUICK_REFERENCE.md |
| Make commit | `git commit -m "feat(scope): desc"` | DEVELOPMENT_WORKFLOW.md § 7 |
| Create PR | Use GitHub template | TEMPLATES.md |
| PR review checklist | Copy from doc | TEMPLATES.md |

---

## 🔄 Decision Tree: What to Do Next

```text
START HERE
    │
    ├─ I'm starting a NEW feature
    │  └─ DEVELOPMENT_WORKFLOW.md § 3 "Starting a Feature"
    │
    ├─ I'm IMPLEMENTING a feature
    │  ├─ Write tests first? → TDD_AND_CODEGEN.md § Part 1
    │  └─ Use auto-generation? → TDD_AND_CODEGEN.md § Part 2
    │
    ├─ I need to HAND OFF to an agent
    │  └─ TEMPLATES.md "Agent-Specific Issue Format"
    │
    ├─ I'm REVIEWING agent's code
    │  ├─ DEVELOPMENT_WORKFLOW.md § 5 "Code Review"
    │  └─ TEMPLATES.md "Reviewer Checklist"
    │
    ├─ I need to MERGE to main
    │  └─ DEVELOPMENT_WORKFLOW.md § 6 "Merging Work"
    │
    ├─ It's MONDAY (update time)
    │  └─ DEVELOPMENT_WORKFLOW.md § 1 "Weekly Updates"
    │
    ├─ I need a QUICK REMINDER
    │  └─ QUICK_REFERENCE.md
    │
    └─ Something BROKE
       └─ DEVELOPMENT_WORKFLOW.md § 11 "Common Issues"
```

---

## 📊 Workflow Statistics

**Time Commitment per Week:**

- Monday dependency check: 30 min
- Daily development: Variable per task
- Code reviews: 15-30 min per PR
- Weekly sync: 15 min

**TDD Overhead:**

- Additional ~20% first-time (writing tests)
- Saves ~40% on debugging later
- Net gain: More confidence, fewer bugs

**Agent Collaboration:**

- Handoff documentation: 10-15 min
- Code review: 15-20 min per PR
- Clear spec reduces agent mistakes by ~70%

---

## 🎓 Learning Path

If you're new to these workflows:

**Week 1:**

- [ ] Read GETTING_STARTED.md (this file)
- [ ] Skim DEVELOPMENT_WORKFLOW.md
- [ ] Complete first feature with all checks

**Week 2:**

- [ ] Try handing off a feature to an agent
- [ ] Review agent's code using checklist
- [ ] Merge completed feature

**Week 3:**

- [ ] Lead a sprint planning session
- [ ] Guide multiple features through workflow
- [ ] Coach an agent on process

**Ongoing:**

- [ ] Use QUICK_REFERENCE.md daily
- [ ] Refer to specific sections as needed
- [ ] Update documentation with team learnings

---

## ✨ Key Takeaways

1. **Three main docs for daily work:**
   - QUICK_REFERENCE.md (for commands)
   - DEVELOPMENT_WORKFLOW.md (for full process)
   - TEMPLATES.md (for issues/PRs)

2. **TDD matters:**
   - Write tests before code (RED)
   - Make tests pass (GREEN)
   - Improve code (REFACTOR)
   - See TDD_AND_CODEGEN.md for patterns

3. **Agents need context:**
   - Use templates exactly
   - Provide clear acceptance criteria
   - Show reference code
   - Link to this documentation

4. **Weekly rhythm:**
   - Monday: Update & plan
   - Daily: Develop & sync
   - Friday: Review & close
   - Repeat!

5. **Commit often:**
   - Small, atomic commits
   - Clear commit messages
   - Easy to revert if needed
   - Easy to bisect bugs

---

## 🚀 Next Step

**Pick one:**

- [ ] Read DEVELOPMENT_WORKFLOW.md § 3 (start a feature)
- [ ] Copy templates from TEMPLATES.md into GitHub
- [ ] Create your first feature branch
- [ ] Review TDD_AND_CODEGEN.md for test patterns

Then start building! 🎉

---

## 📞 Help & Resources

- **Framework docs:** https://vibetuner.alltuner.com/llms.txt
- **Report framework issues:** https://github.com/alltuner/vibetuner/issues
- **Framework guide in repo:** AGENTS.md
- **Question on doc?** Check the table at top of this file

Good luck! Build great things! 🚀
