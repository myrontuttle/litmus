# Issue & PR Templates for Agent-Friendly Development

Copy these templates when creating issues and pull requests to ensure clarity for both human developers and coding agents.

---

## 📋 Issue Template: User Story

Use this for feature requests and new capabilities.

```markdown
# User Story: [Feature Name]

## Problem / User Need

As a [user type], I want to [action/feature], so that [benefit/outcome].

**Background**: [Additional context about why this is needed]

## Acceptance Criteria

- [ ] Criterion 1 (testable and specific)
- [ ] Criterion 2 (testable and specific)
- [ ] Criterion 3 (testable and specific)

## Example Scenarios

### Happy Path

**Given** [initial state]  
**When** [user action]  
**Then** [expected outcome]

### Error Handling

**Given** [edge case state]  
**When** [action that could fail]  
**Then** [handled gracefully, error message: "..."]

## Technical Details

### Data Model Changes

- New collections/tables: [list]
- Fields to add: [list]
- Indexes needed: [list]

### Dependencies

- External libraries: [list]
- Related issues: #[issue number]
- Blocks: #[issue number]

### Acceptance Tests

```python
# Pseudo-code for tests to write
@pytest.mark.asyncio
async def test_feature_requirement_1():
    """Verify acceptance criterion 1"""
    assert result == expected
```
```

## Implementation Notes

- Suggested files: `src/app/models/`, `src/app/frontend/routes/`
- Consider: [architectural decisions]
- Reference: [similar existing code]

## Definition of Done

- [ ] All acceptance criteria verified
- [ ] Tests written and passing
- [ ] Code reviewed and approved
- [ ] User documentation updated
- [ ] Works locally and on staging

```text

---

## 🐛 Issue Template: Bug Report

Use this for reporting issues.

```markdown
# Bug Report: [Short Description]

## Severity
- [ ] Critical (app broken/unusable)
- [ ] High (feature broken)
- [ ] Medium (workaround exists)
- [ ] Low (minor issue)

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

**Expected Result**: [What should happen]  
**Actual Result**: [What happens instead]

## Environment
- OS: [Linux/macOS/Windows]
- Python version: [output of `python --version`]
- Branch: [feature/X or main]

## Error Message / Logs
```

[Paste full error message]
[Include stack trace]

```text

## Possible Cause
[Your hypothesis about what's wrong, if known]

## Related Issues
Duplicates: #[issue]  
Related: #[issue]
```

---

## 🔀 Pull Request Template: New Feature

Use this when submitting a feature implementation.

```markdown
# PR: [Feature Name]

## Description

What was implemented and why?

[Clear, concise description of changes]

## Related Issues

Closes #[issue number]
Related: #[related issue]

## Acceptance Criteria Verification

- [ ] Criterion 1 from issue [link results or test output]
- [ ] Criterion 2 from issue [link results or test output]
- [ ] Criterion 3 from issue [link results or test output]

## Testing

### Tests Added

- `tests/test_models/test_new_model.py` - Model initialization and validation
- `tests/test_routes/test_endpoint.py` - Endpoint behavior and error handling
- `tests/test_services/test_logic.py` - Service business logic

### Test Results

```bash
# Run this command to reproduce tests:
uv run pytest -v tests/test_new_feature.py

# Output:
# ✅ 8 passed in 0.45s
```
```

### Manual Testing

- [ ] Tested in browser: [URL or description]
- [ ] Tested error paths: [list edge cases tested]
- [ ] Tested with existing features: [what was verified]

## Code Quality

- [ ] All tests passing locally: `uv run pytest -v`
- [ ] Type checking passes: `just type-check`
- [ ] Code formatted: `just format`
- [ ] Linting passes: `just lint`
- [ ] No debug statements or console.log
- [ ] Docstrings added for public functions
- [ ] Code follows project conventions

## Breaking Changes

- [ ] No breaking changes
- [ ] Breaking changes: [list what breaks]

## Dependencies

- [ ] No new dependencies added
- [ ] New dependencies: [list]
  - Why needed: [explanation]
  - Version: [pinned version]

## Database Changes

- [ ] No database changes
- [ ] New collections/tables: [list]
- [ ] Migrations needed: [describe]
- [ ] Indexes added: [list]

## Documentation

- [ ] README updated: [if applicable]
- [ ] Docstrings added to code
- [ ] API docs updated: [if applicable]
- [ ] No documentation needed

## Architecture Decisions

[Explain any non-obvious implementation choices]

## Screenshots / Examples

[If UI changes, include before/after]

## Deployment Notes

- Zero-downtime compatible: Yes/No
- Requires configuration: Yes/No
- Requires database migration: Yes/No

## Reviewer Checklist (for reviewer, not author)

- [ ] Code implements requirements from linked issue
- [ ] All acceptance criteria verified
- [ ] Tests are meaningful and adequate
- [ ] Error handling is appropriate
- [ ] Security concerns addressed (input validation, auth, etc.)
- [ ] Performance implications checked
- [ ] Code quality is good
- [ ] Documentation is clear
- [ ] No merge conflicts

```text

---

## 🔧 Pull Request Template: Bug Fix

Use this when submitting a bug fix.

```markdown
# PR: Fix [Bug Description]

## Problem
What was broken?

[Reference to bug report issue #XXX]

**Reproduction**: [Steps that would show the bug]

## Solution
How was it fixed?

[Explanation of the fix]

## Root Cause
Why did this happen?

[Analysis of what caused the issue]

## Code Changes
- File 1: [What changed and why]
- File 2: [What changed and why]

## Testing
### Verification of Fix
```bash
# Before fix:
[Show that bug manifests]

# After fix:
uv run pytest -v -k "test_bugfix"
# ✅ All tests pass
```

## Code Quality

- [ ] All tests passing: `uv run pytest -v`
- [ ] Type checking passes: `just type-check`
- [ ] Code formatted: `just format`
- [ ] Linting passes: `just lint`

## Regression Testing

- [ ] Existing tests still pass
- [ ] Related features tested: [what was verified]
- [ ] Edge cases covered: [list]

## Breaking Changes

None / [list if any]

## Deployment Notes

- Safe to deploy immediately: Yes/No
- Requires configuration: Yes/No

```text

---

## 📝 Pull Request Template: Refactoring

Use this for code restructuring and improvements.

```markdown
# PR: Refactor [Component/Feature]

## Motivation
Why is this refactoring needed?

- [ ] Improved readability
- [ ] Reduced duplication
- [ ] Performance improvement
- [ ] Better testability
- [ ] Preparatory for [feature/fix]

## Changes
What was refactored?

[Overview of changes]

## Before / After

### Before
[Snippet of old code]

### After
[Snippet of new code]

## Impact Analysis
- [ ] No functional changes
- [ ] Tests pass unchanged: `uv run pytest -v`
- [ ] Performance: [same/improved/tested]
- [ ] Public API: [unchanged/documented]

## Code Quality
- [ ] All tests passing
- [ ] Type checking passes
- [ ] Code formatted
- [ ] Linting passes
- [ ] No functional regressions

## Review Focus
- [Specific areas to focus review on]
```

---

## 📤 PR Description Best Practices

### ✅ DO

- **Be specific**: "Add email validation to signup endpoint" not "Add auth stuff"
- **Link issues**: Always reference the issue you're closing
- **Show test results**: Include pytest output
- **Explain WHY**: Focus on intent, not just what changed
- **Be thorough**: Checklist completeness helps reviewers
- **Reference code**: Use file paths and line numbers

### ❌ DON'T

- Don't skip acceptance criteria verification
- Don't say "ready to merge" (let reviewers decide)
- Don't include unrelated changes in one PR
- Don't mix refactoring with feature implementation
- Don't leave TODOs in code
- Don't forget docstrings or type hints

---

## 🤖 Agent-Specific Issue Format

When requesting work from a coding agent, use this format for maximum clarity:

```markdown
# Task: [Clear Title]

## Objective

[What needs to be done in 1-2 sentences]

## Acceptance Criteria

- [ ] Criterion 1 (specific and testable)
- [ ] Criterion 2 (specific and testable)

## Implementation Details

### Files to Create/Modify

- `src/app/models/item.py` - Create Item model
- `src/app/frontend/routes/items.py` - Create items endpoints
- `tests/test_items.py` - Add test suite

### Reference Code

To see the pattern, check:

- Similar feature: `src/app/frontend/routes/users.py`
- Model example: `src/app/models/user.py`

### Technical Requirements

- Use Beanie for MongoDB
- Validate input with Pydantic
- Return 201 on success, 400 on validation error
- Include docstrings on all functions
- Write tests using pytest

### Expected Output

```python
# Example of what implementation should look like:
@router.post("/api/items", status_code=201)
async def create_item(item: CreateItemSchema, request: Request):
    """Create a new item."""
    # Implementation here
    return {"id": item.id, "status": "created"}
```
```

## Testing

Agent should verify:

- [ ] `uv run pytest tests/test_items.py -v` passes
- [ ] `just type-check` passes
- [ ] `just lint` passes
- [ ] Feature works when calling via HTTP

## Notes

[Any caveats, gotchas, or additional context]

```text

---

## 📋 Commit Message Best Practices

### Format (Conventional Commits)
```

<type>(<scope>): <subject>

<body>

<footer>
```

### Good Examples

```text
feat(auth): add email verification endpoint

Users can now verify their email by clicking a link in the verify email.
Verification tokens expire after 24 hours.

Closes #123
```

```text
fix(models): handle null email field in User.from_dict()

Previously, Users with null email would raise KeyError when converting
from MongoDB document. Now safely defaults to empty string.

Fixes #456
```

```text
refactor(routes): consolidate auth endpoints

Moved repeated auth logic into shared middleware to reduce duplication.
No functional changes, improves maintainability.
```

### Avoid

```text
feat: changes         # Too vague

feat: fixed some bug and added feature and updated readme  # Too much, too vague

fix bug in line 42    # No scope or clear description
```

---

## 🔍 Code Review Checklist for Reviewers

```markdown
# Code Review Checklist

## Requirements Verification

- [ ] All acceptance criteria from issue are met
- [ ] Tests verify the acceptance criteria
- [ ] Feature behaves as described in the PR

## Functionality

- [ ] Happy path works
- [ ] Error handling is appropriate
- [ ] Edge cases are handled
- [ ] No regressions in related features

## Code Quality

- [ ] Type hints present and correct
- [ ] Docstrings on public functions
- [ ] No debug statements
- [ ] Code formatting is correct
- [ ] Variable/function names are clear

## Testing

- [ ] Tests are comprehensive
- [ ] Tests actually verify the code works
- [ ] Mocks are used appropriately
- [ ] All tests pass locally

## Security

- [ ] Input validation present
- [ ] No hardcoded secrets/credentials
- [ ] Permissions/auth checked
- [ ] SQL injection/XSS risks mitigated

## Performance

- [ ] No obvious N+1 queries
- [ ] Large data operations optimized
- [ ] No unnecessary loops or recursion

## Architecture

- [ ] Follows project patterns
- [ ] Reasonable separation of concerns
- [ ] Consistent with existing code style
- [ ] No unnecessary dependencies added

## Documentation

- [ ] Code comments for complex logic
- [ ] README updated if needed
- [ ] API docs updated if needed
- [ ] Docstrings are accurate

## Sign-Off

- [ ] Approved for merge
- [ ] Request changes (comment with specifics)
```

---

## 🚀 Using These Templates

1. **Copy templates into GitHub**: Settings → Code & automation → Template → Paste
2. **Reference in PRs/Issues**: Manually copy or use GitHub template selection when creating
3. **Share with agents**: Include the relevant template in your instructions to coding agents
4. **Customize**: Projects often add custom sections - adapt as needed

**Key for agents**: When you see these templates in instructions, follow the structure and fill out all sections completely.
