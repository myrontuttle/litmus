# Development Workflow Guide

This guide establishes repeatable steps for developing this app using agile and lean
software engineering best practices, with protocols for human-agent collaboration
and staying current with the framework.

---

## 1. Weekly Dependency & Framework Updates

**Frequency**: Every Monday morning (or weekly sync point)
**Time**: ~30 minutes
**Owner**: Either human or agent (assign in current sprint)

### Step 1: Check for Updates

```bash
# Update project dependencies
just update-repo-deps

# Review what changed
git diff pyproject.toml package.json
```

### Step 2: Review Framework Changelog

- Check: <https://vibetuner.alltuner.com/llms.txt> for new features or deprecations
- Check vibetuner GitHub: <https://github.com/alltuner/vibetuner/releases>
- Look for breaking changes, security patches, or relevant new features

### Step 3: Test for Compatibility

```bash
# Run full test suite to catch breaking changes early
uv run pytest -v

# Type check
just type-check

# Lint everything
just lint
```

### Step 4: Security Scanning

```bash
# Check for known vulnerabilities in dependencies
uv pip compile --check-updates pyproject.toml
```

### Step 5: Document Findings

Create/update a section in your project notes:

- **New Features**: Any vibetuner/FastAPI/MongoDB features relevant to current sprint
- **Breaking Changes**: What needs updating in our code
- **Security Updates**: Any patches needed
- **Deprecations**: What we should stop using

### Step 6: Create Issue if Needed

If refactoring or updates needed:

```text
Title: chore: update dependencies and address framework changes
- Framework version: [X.Y.Z]
- Breaking changes: [list]
- Expected effort: [2-4 hours]
```

---

## 2. Human-Agent Development Sync Protocol

### Daily Standup (Async)

**When**: End of day or before handing off to agent
**Format**: Update the project's TODO tracking (in code or project management tool)

For each active task, document:

- ✅ What was completed
- 🔄 What's in-progress (if handing off to agent)
- 🚫 Any blockers

**Example**:

```text
## Sprint Week of March 6
- [x] Design user authentication flow
- [x] Created POST /auth/login route
- [ ] Implement session management (IN PROGRESS)
  - Created session models
  - Need to implement refresh token logic
- [ ] Add email verification
```

### Branch Strategy

```text
main
├── feature/auth-flow              (human + agent collaboration)
├── feature/dashboard              (agent branch)
└── fix/mongo-connection           (human branch)
```

**Naming convention**:

- `feature/[scope]-[description]` - New features
- `fix/[scope]-[issue]` - Bug fixes
- `refactor/[scope]-[change]` - Code restructuring
- `docs/[description]` - Documentation only

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Check status before committing (important!)
git status

# Add all changes (modified files + new untracked files)
git add .

# Or add specific files/directories
git add src/app/models/user.py
git add tests/
git add docs/dev/  # For documentation changes

# Work in logical commits (small, testable units)
git commit -m "feat(models): add User model with email uniqueness"

git add src/app/frontend/routes/auth.py
git commit -m "feat(routes): add POST /auth/signup endpoint"

# Before pushing: sync with main
git fetch origin
git rebase origin/main

# Push to remote
git push origin feature/my-feature
```

**Common Git Issues:**

- **"Untracked files" error**: Run `git add .` or `git add <specific-file>` to stage new files
- **"Nothing to commit"**: Check `git status` - you may need to add files first
- **Merge conflicts**: Use `git rebase origin/main` instead of merge for cleaner history
- **Lost changes**: Use `git reflog` to find lost commits

### Handoff Between Human and Agent

**When handing work to an agent**:

1. Push current branch with descriptive commit messages
2. Create a Pull Request (don't merge yet) with detailed description:

   ```markdown
   ## Description

   [What are we building and why?]

   ## Acceptance Criteria

   - [ ] Criteria 1
   - [ ] Criteria 2

   ## Technical Notes

   - Dependencies: [list]
   - Related files: [list]
   - Known issues: [list]

   ## Next Steps

   [What should the agent focus on?]
   ```

3. Leave a comment with specific instructions for the next phase

**When agent completes work**:

1. Run all tests locally and report status
2. Leave PR comments documenting what was done
3. Mark code ready for review (don't merge)

---

## 3. Starting a Feature/Task (Best Practices)

### Phase 1: Requirements & Planning (30 min - 1 hr)

**Input**: Feature description, user story, or bug report
**Owner**: Usually the human or product person
**Output**: Clear requirements document

#### Create Issue

```markdown
# Title: [Clear, actionable title]

## Problem / User Story

As a [user], I want [feature] so that [benefit].

Or:

## Task Description

[Clear description of what needs to be done]

## Acceptance Criteria

- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

## Dependencies

- Related issues: #123
- External libraries: [list]
- Database changes: [yes/no]

## Notes

- [Any architectural decisions]
- [Constraints or gotchas]
```

#### Create Design Document (for complex features)

Create `/docs/design-[feature-name].md`:

```markdown
# [Feature Name] Design

## Overview

[1-2 paragraph description]

## Architecture

[Diagram or ASCII art showing components]

## Data Models

[Tables, collections, relationships]

## API Endpoints

- POST /api/endpoint - [description]
- GET /api/endpoint - [description]

## UI Components

- [Component 1] - [description]
- [Component 2] - [description]

## Risks & Mitigations

- [Risk 1]: [How to mitigate]

## Testing Strategy

- [Integration tests]
- [E2E scenarios]
```

### Phase 2: Development Setup (10 min)

```bash
# Create feature branch
git checkout -b feature/user-story-name

# Update TODO list (use manage_todo_list)
# Create tasks for:
# 1. Write tests (TDD)
# 2. Implement feature
# 3. Integration testing
# 4. Documentation
# 5. Code review

# Ensure fresh environment
uv run python --version    # Verify venv works
just local-all             # Start dev server
```

### Phase 3: Test Planning (TDD Approach)

**Before writing code**: Write failing tests

```python
# tests/test_user_auth.py
import pytest
from app.services.auth import create_user, authenticate_user
from app.models import User

@pytest.mark.asyncio
async def test_create_user_with_valid_email():
    """User should be created with unique email."""
    user = await create_user(email="alice@example.com", password="secure123")
    assert user.email == "alice@example.com"
    assert user.id is not None

@pytest.mark.asyncio
async def test_create_user_duplicate_email_fails():
    """Creating user with duplicate email should raise error."""
    await create_user(email="bob@example.com", password="secure123")
    with pytest.raises(ValueError, match="Email already exists"):
        await create_user(email="bob@example.com", password="other123")

@pytest.mark.asyncio
async def test_authenticate_user_returns_user_on_valid_credentials():
    """Valid credentials should return user object."""
    await create_user(email="charlie@example.com", password="secure123")
    user = await authenticate_user("charlie@example.com", "secure123")
    assert user.email == "charlie@example.com"

@pytest.mark.asyncio
async def test_authenticate_user_fails_on_wrong_password():
    """Wrong password should return None."""
    await create_user(email="diana@example.com", password="secure123")
    user = await authenticate_user("diana@example.com", "wrongpass")
    assert user is None
```

Run to confirm tests fail:

```bash
uv run pytest -v tests/test_user_auth.py
# Should show 4 FAILED
```

---

## 4. Feature Development Checklist

### Implementation Phase

Use this checklist while developing (update with each logical step):

```markdown
## Implementation Checklist

### Models

- [ ] Define Beanie models (if needed)
- [ ] Add indexes for queries
- [ ] Add validation (Pydantic)
- [ ] Write model tests

### Business Logic / Services

- [ ] Write service functions
- [ ] Add error handling
- [ ] Write service tests
- [ ] Document assumptions

### API Routes

- [ ] Define endpoints
- [ ] Add request/response schemas
- [ ] Implement error responses
- [ ] Write route tests

### Frontend / UI

- [ ] Create templates
- [ ] Add HTMX interactions
- [ ] Style with Tailwind
- [ ] Test in browser

### Integration

- [ ] Full feature flow test
- [ ] Edge cases & error paths
- [ ] Performance check (if relevant)
- [ ] Database migrations (if needed)

### Code Quality

- [ ] Type hints complete
- [ ] Docstrings added
- [ ] Code formatted: `just format-py`
- [ ] Linting passes: `just lint-py`
- [ ] Type checking passes: `just type-check`

### Documentation

- [ ] README updated (if applicable)
- [ ] Code comments for complex logic
- [ ] API documentation added
- [ ] Design decisions documented
```

### Incremental Commits

Make atomic commits (one logical change per commit):

```bash
# Good commits
git commit -m "feat(models): add User document with email field"
git commit -m "feat(services): implement create_user with validation"
git commit -m "feat(routes): add POST /auth/signup endpoint"

# Bad commits (too big, mixing concerns)
git commit -m "feat: add auth system"
```

---

## 5. Code Review & Quality Standards

Before requesting review, verify:

### Local Testing

```bash
# Run all tests
uv run pytest -v

# Type checking
just type-check

# Code formatting
just format

# Linting
just lint

# Doctor check (framework diagnostics)
uv run vibetuner doctor
```

### Pre-Review Checklist

- [ ] All tests passing locally
- [ ] No type errors
- [ ] Code formatted and linted
- [ ] Commits are atomic and well-messeged
- [ ] No console.log/print debugging statements
- [ ] No secrets/credentials in code
- [ ] Docstrings on public functions
- [ ] Related tests added (not just implementation)

### Review PR Template

```markdown
## Changes

[What was changed and why?]

## Testing

- [ ] Added/updated tests
- [ ] All tests passing
- [ ] Tested in browser (if frontend)
- [ ] Edge cases handled

## Breaking Changes

None / [list if any]

## Related Issues

Closes #123
Related: #124, #125

## Review Notes

[Anything specific you want reviewed?]
[Known limitations?]
```

### Code Review Focus Areas

**Reviewer should check**:

1. **Requirements Met**: Do all acceptance criteria pass?
2. **Tests**: Sufficient coverage? Are tests meaningful?
3. **Error Handling**: What happens when things go wrong?
4. **Security**: Input validation? SQL injection? XSS risks?
5. **Performance**: Any N+1 queries? Large data loads?
6. **Code Quality**: Type hints? Docstrings? Consistency?
7. **Framework Best Practices**: Following vibetuner patterns?

---

## 6. Completing & Merging Work

### Final Checklist

```markdown
## Merge Checklist

- [ ] All CI/CD checks passing
- [ ] Code review approved
- [ ] Tests passing on CI
- [ ] No merge conflicts
- [ ] Conventional commit title on PR
- [ ] Related issues mentioned
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Merge Strategy

1. **Review approval obtained**
2. **CI passes** (all tests, linting, type checks)
3. **Rebase on main** (keep history clean):

   ```bash
   git fetch origin
   git rebase origin/main
   git push origin feature/X -f
   ```

4. **Squash merge** (clean history):

   ```bash
   git switch main
   git pull origin main
   git merge --squash origin/feature/X
   git commit -m "feat(scope): description"
   git push origin main
   ```

### Post-Merge

```bash
# Pull latest
git pull origin main

# Verify on production/staging (if applicable)
# Document in sprint notes what was completed
# Close related issues
```

---

## 6.5 Branch Cleanup & Maintenance

**Why**: Long-lived branches create merge conflicts and make it harder to track active work. Clean up merged branches regularly.

### After Merging a Feature Branch

```bash
# Delete local branch (after merge)
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature

# Or use GitHub CLI
gh pr merge --delete-branch
```

### Weekly Branch Cleanup

**Frequency**: Every Friday or end of sprint
**Time**: ~5 minutes

```bash
# List all branches
git branch -a

# Delete merged local branches
git branch --merged main | grep -v main | xargs git branch -d

# Delete merged remote branches (be careful!)
git branch -r --merged origin/main | grep -v main | sed 's/origin\///' | xargs -I {} git push origin --delete {}
```

### Branch Health Checks

```bash
# See branch age (old branches to review)
git for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:relative)%09%(refname:short)'

# Find branches not pushed to remote
git branch -r | grep -v origin/main | sed 's/origin\///' > remote_branches.txt
git branch | sed 's/*//' | xargs > local_branches.txt
comm -23 local_branches.txt remote_branches.txt
```

### Best Practices

- **Delete after merge**: Always delete feature branches after successful merge
- **No long-lived branches**: Feature branches should live 1-7 days max
- **Regular cleanup**: Weekly branch audit prevents accumulation
- **Stale branch policy**: Delete branches older than 30 days without activity
- **Branch naming**: Use descriptive names that indicate completion status

---

## 7. Commit Message Conventions

**Format**: Follows Release Please conventions (already in project)

```text
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

**Types**:

- `feat:` New feature (MINOR version bump)
- `fix:` Bug fix (PATCH version bump)
- `docs:` Documentation only
- `chore:` Maintenance, deps (PATCH version bump)
- `refactor:` Code refactoring (PATCH version bump)
- `style:` Formatting (PATCH version bump)
- `test:` Test changes (PATCH version bump)
- `perf:` Performance (MINOR version bump)

**Examples**:

```text
feat(auth): add email verification flow
fix(models): handle null fields in User.from_db()
chore: upgrade FastAPI to 0.104.0
feat!: require authentication for all routes (BREAKING)
```

**Body**: Explain *why*, not *what*:

```text
feat(auth): add email verification flow

Previously, users could sign up without email verification.
This allowed invalid emails and spam registration attempts.

Now users receive a verification email and cannot log in
until they verify their email address.

Closes #123
```

---

## 8. Continuous Updates While Working

### Each Day

```bash
# Start of day
git pull origin main
git rebase origin/main  # Keep feature branch up to date

# During work
just format-py  # After writing code
uv run pytest -v  # Run tests frequently
```

### Before Pushing

```bash
# Ensure latest main is included
git fetch origin
git rebase origin/main

# Run full checks
uv run pytest -v
just type-check
just lint

# Push
git push origin feature/X
```

### Weekly Sync

```bash
# Update dependencies
just update-repo-deps

# Check for framework updates
# (See Section 1: Weekly Updates)

# If breaking changes, create issue to address
```

---

## 9. Agent-Specific Instructions

When working with a coding agent:

### Starting a Task

**Always provide the agent with**:

1. **Linked issue/requirements** (link to GitHub issue or include full requirements)
2. **Architecture decision context** (design doc or "follow existing patterns")
3. **Acceptance criteria** (numbered list)
4. **File locations** (where code should go)
5. **Example patterns** (reference similar code in codebase)
6. **Test expectations** (what tests should verify)

**Example**:

```text
Issue: Implement user signup endpoint

Acceptance Criteria:
- POST /auth/signup accepts {email, password}
- Validates email format and password strength
- Returns 201 with user ID on success
- Returns 400 with error on validation failure
- Creates entry in User collection

Location: src/app/frontend/routes/auth.py
Tests: tests/test_auth_routes.py

Related patterns:
- See src/app/models/user.py for model definition
- See src/app/frontend/routes/login.py for similar endpoint

Design decisions:
- Use Beanie for MongoDB
- Password hashed with bcrypt
- Email must be unique
```

### Receiving Completed Work

**Agent provides**:

1. ✅ All tests passing locally
2. 🔄 Status of what was completed
3. 📝 PR with description and notes
4. 🚫 Any blockers or decisions made

**You verify**:

- [ ] Acceptance criteria all met
- [ ] Tests pass on your machine
- [ ] Code follows project conventions
- [ ] Matches design/architecture decisions
- [ ] No security concerns

---

## 10. Quick Reference Commands

### Development

```bash
# Start development (frontend + assets)
just local-all

# Run with worker
just local-all-with-worker

# Run tests
uv run pytest -v
uv run pytest -v -k "test_auth"  # Specific test

# Code quality
just format          # Format all
just lint            # Lint all
just type-check      # Type check

# Framework updates
just update-repo-deps
```

### Git Workflow

```bash
# Create feature
git checkout -b feature/name
git push origin feature/name

# Sync with main
git fetch origin
git rebase origin/main
git push origin feature/name -f

# Create PR (GitHub CLI)
gh pr create --title "feat: description"

# Merge squash-style
git merge --squash origin/feature/name
git commit -m "feat(scope): description"
git push origin main
```

### Database

```bash
# Create schema (if using SQL models)
uv run vibetuner db create-schema

# Run migrations
uv run vibetuner db migrate
```

---

## 11. Common Issues & Solutions

### ⚠️ Stale Dependencies

**Problem**: Local tests pass, CI fails
**Solution**: Update and test locally

```bash
git fetch origin
git rebase origin/main
just update-repo-deps
uv run pytest -v
```

### ⚠️ Git Untracked Files Error

**Problem**: "Untracked files" error when trying to commit
**Solution**: Add untracked files to git staging first

```bash
# Check what files are untracked
git status

# Add all untracked files
git add .

# Or add specific files/directories
git add docs/dev/          # Add documentation
git add src/app/models/    # Add new models
git add tests/             # Add test files

# Then commit
git commit -m "feat: add new feature"
```

**Prevention**: Always run `git status` before committing to see what needs to be added.

### ⚠️ Human-Agent Code Conflicts

**Problem**: Agent changed files you're also working on
**Solution**: Communicate in GitHub before starting

- Comment on issue with your intent
- Use separate features branches
- Merge completed work before starting new work

### ⚠️ Tests Failing After Update

**Problem**: Dependencies updated, tests break
**Solution**: Identify breaking change

```bash
# Check git log for what changed
git log --oneline -10

# Run failing test with verbose output
uv run pytest -vv tests/test_file.py::test_name

# Check framework changelog for migration guide
```

### ⚠️ Framework Deprecations

**Problem**: Vibetuner library changed API
**Solution**: Refer to framework docs

- Check: <https://vibetuner.alltuner.com/llms.txt>
- Search: GitHub issues/discussions
- File issue if unclear: <https://github.com/alltuner/vibetuner/issues>

---

## 12. Agile Sprint Template

Use this for weekly sprint planning:

```markdown
# Sprint: Week of [DATE]

## Sprint Goal

[One sentence describing the sprint's focus]

## Stories / Tasks

- [ ] Story 1: [Description] - [Estimate: 2-4 hours]
- [ ] Story 2: [Description] - [Estimate: 4-8 hours]
- [ ] Chore: Update dependencies - [1 hour]

## In Progress

- ⚙️ [Story being worked on by human/agent]

## Completed

- ✅ [Completed story from this sprint]

## Blockers

- [Any issues preventing progress]

## Notes

- [Important decisions made]
- [Learnings from the week]
```

---

## Summary: The Repeatable Process

### 📋 Weekly Update Cycle (30 min)

1. Check for dependency updates → `just update-repo-deps`
2. Review framework changelog
3. Run tests → `uv run pytest -v`
4. Document findings

### 🤝 Human-Agent Sync (Daily)

1. Push progress with clear commits
2. Update TODO/issue status
3. Create PR with acceptance criteria
4. Leave specific next-step comments

### 🎯 Feature Workflow (Per Feature)

1. Write requirements & design doc
2. Plan tests (TDD)
3. Write failing tests first
4. Implement feature
5. Code quality checks → `just format && just lint && uv run pytest`
6. Create PR with context
7. Review → Merge

### ✅ Code Review (Before Merge)

1. Tests passing locally
2. All checks passing
3. Commit messages follow conventions
4. Docs updated
5. No security concerns

---

## Next Steps

1. **Bookmark this document** - Reference during development
2. **Create a sprint template** - Pin in your project management tool
3. **Add team-specific rules** - Customize for your workflows
4. **Integrate with CI/CD** - Automate what you can check
5. **Review with agents** - Share these patterns so AI stays aligned
