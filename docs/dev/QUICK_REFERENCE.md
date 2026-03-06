# Development Quick Reference

Print this or keep it handy while coding. For detailed guidance, see `DEVELOPMENT_WORKFLOW.md`.

---

## 🚀 Starting a New Feature

```bash
# 1. Create issue with acceptance criteria on GitHub

# 2. Create feature branch
git checkout -b feature/descriptive-name

# 3. Start dev environment
just local-all

# 4. Write failing tests FIRST
uv run pytest -v tests/test_feature.py

# 5. Implement feature

# 6. Run checks before committing
just format-py
uv run pytest -v
just type-check
just lint
```

---

## ✅ Commit Workflow

```bash
# Check status first (important!)
git status

# Add all changes (modified + untracked files)
git add .

# Or add specific files
git add src/app/models/new_model.py
git add tests/
git add docs/dev/  # For documentation

# Make atomic commits
git commit -m "feat(models): add new model with validation"

git add src/app/frontend/routes/endpoint.py
git commit -m "feat(routes): add POST /api/endpoint"

# Sync with main before pushing
git fetch origin
git rebase origin/main

# Push
git push origin feature/name
```

**Common Issues:**

- **Untracked files error**: Run `git add .` first
- **Nothing to commit**: Check `git status` - files may need adding

**Commit Format**: `type(scope): description`

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `chore:` maintenance
- `refactor:` code restructuring

---

## 📤 Before Requesting Review

```bash
# Run full test suite
uv run pytest -v

# Type checking
just type-check

# Code quality
just format
just lint

# Framework diagnostics
uv run vibetuner doctor

# Create PR on GitHub with:
# - Clear description
# - Acceptance criteria marked as [ ]
# - Related issue link
# - Testing notes
```

---

## 🔄 Human-Agent Handoff

**Handing OFF to agent**:

1. Push current branch
2. Create PR (don't merge) with detailed description
3. Comment: "Ready for [specific next step]"

**Receiving FROM agent**:

1. Review PR description
2. Local test: `uv run pytest -v`
3. Verify acceptance criteria met
4. Approve or request changes

---

## 📦 Weekly Dependency Update

```bash
# Every Monday
just update-repo-deps

# Test for issues
uv run pytest -v
just type-check
just lint

# Check framework changelog
# https://vibetuner.alltuner.com/llms.txt

# Commit if all good
git add pyproject.toml package.json
git commit -m "chore: update dependencies"
```

---

## 🆘 Common Commands

| Task | Command |
|------|---------|
| Start dev server | `just local-all` |
| Run tests | `uv run pytest -v` |
| Format code | `just format` |
| Lint code | `just lint` |
| Type check | `just type-check` |
| Update deps | `just update-repo-deps` |
| Add Python package | `uv add package-name` |
| Add JS package | `bun add package-name` |
| Doctor check | `uv run vibetuner doctor` |

---

## 🎯 PR Checklist (Copy & Use)

```markdown
## Pre-Review Checklist

- [ ] All tests passing: `uv run pytest -v`
- [ ] No type errors: `just type-check`
- [ ] Code formatted: `just format`
- [ ] Linting passes: `just lint`
- [ ] Acceptance criteria met
- [ ] Docstrings added
- [ ] No debug statements

## PR Title Format

- `feat(scope): description` for new features
- `fix(scope): description` for bug fixes

## Description

[What was changed and why?]

## Closes

Closes #[issue number]
```

---

## 📍 File Locations

| What | Where |
|------|-------|
| Routes | `src/litmus/frontend/routes.py` |
| Models | `src/litmus/models/` |
| Services/Logic | `src/litmus/services/` |
| Tests | `tests/` |
| Templates | `templates/frontend/` |
| Assets/CSS | `config.css` |
| Assets/JS | `config.js` |
| Config | `src/litmus/tune.py` |

---

## 🔐 Security Reminders

- ✅ Never commit `.env` (use `.env.example`)
- ✅ Always hash passwords
- ✅ Validate all user input
- ✅ Use Beanie operators for queries (no string concatenation)
- ✅ Check for: SQL injection, XSS, CSRF, authentication
- ✅ Keep secrets in environment variables

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **Untracked files error** | `git add .` then commit |
| **Tests failing** | `uv run pytest -v` to see details |
| **Import errors** | Check `src/litmus/__init__.py` |
| **Server not starting** | `just local-all` (not just `uv run`) |
| **Code formatting issues** | `just format` |
| **Type errors** | `just type-check` |

---

## 📞 Getting Help

- Framework docs: <https://vibetuner.alltuner.com/llms.txt>
- Report bugs: <https://github.com/alltuner/vibetuner/issues>
- Framework guide: See `AGENTS.md` in this repo
- Development guide: See `DEVELOPMENT_WORKFLOW.md` in this repo
