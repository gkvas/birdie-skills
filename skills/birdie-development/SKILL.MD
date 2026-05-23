---
name: birdie-development
description: Development workflow for the Birdie AI agent project - branching strategy, commit discipline, and PR creation.
triggers:
  - birdie development
  - birdie workflow
  - birdie feature
  - birdie fix
  - feature branch
  - fix branch
  - squash commit
  - new version
  - release version
  - bump version
  - create version
---

# Birdie Development Workflow

This skill describes the required development process for contributing to the Birdie AI agent project.

## Branching Strategy

- All **new features** must be developed on a branch named `feature/<short-description>`.
- All **bug fixes** must be developed on a branch named `fix/<short-description>`.
- Never commit directly to `main`.

Create a branch before starting any work:

```
git checkout -b feature/my-new-feature
# or
git checkout -b fix/the-broken-thing
```

## Committing During Development

- Multiple intermediate commits are allowed and encouraged during development to save progress.
- Before each commit, **all tests must pass**. Do not commit broken code.

Run the test suite before committing:

```
pytest
```

Only commit once the tests are green.

## Preparing to Push

Before pushing, **squash all commits on the branch into a single commit**. The final push must contain exactly one commit that represents the complete, coherent change.

Steps:
1. Find how many commits are on your branch ahead of `main`:
   ```
   git log --oneline main..HEAD
   ```
2. Interactive-rebase to squash them all:
   ```
   git rebase -i main
   ```
   Mark every commit except the first as `squash` (or `s`). Write a clear, descriptive commit message for the squashed result.
3. Run the full test suite one final time after the rebase:
   ```
   pytest
   ```
4. Only push if all tests pass.

## Pushing and Creating a Pull Request

Push the branch and immediately create a PR with the `gh` CLI:

```
git push -u origin HEAD
gh pr create --title "<concise title>" --body "<description of what changed and why>"
```

The PR title and body should clearly explain the motivation and scope of the change.

## Creating a New Release

Follow this process when cutting a new version of Birdie.

### 1. Confirm the version number

Before doing anything else, **ask the user what the new version should be**. Do not assume or derive it automatically. Wait for explicit confirmation before proceeding.

### 2. Create a release branch

```
git checkout -b feature/release-<version>
```

### 3. Update `pyproject.toml`

Set the `version` field to the confirmed version string:

```toml
[project]
version = "<version>"
```

### 4. Update `CHANGELOG.md`

First, find the tag or commit of the previous release to establish the baseline:

```
git tag --sort=-version:refname | head -5        # find the last version tag
git log <last-tag>..HEAD --oneline               # list all commits since then
```

If the last release has no tag, locate its merge commit in `CHANGELOG.md` and use that commit SHA as the baseline.

Read the current `CHANGELOG.md` to check whether any of those commits have already been documented. Only add entries that are not yet present.

Add a new section at the top of `CHANGELOG.md` for the new version:

```markdown
## [<version>] - <YYYY-MM-DD>

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

Derive the entries from the actual commit messages. Group them under Added, Changed, or Fixed as appropriate. Skip pure merge commits and housekeeping commits (dependency bumps, typos) unless they are user-visible.

### 5. Review and update `README.md`

Read the changelog entries you just wrote. For each user-visible change (new feature, changed behaviour, renamed flag, removed option), locate the corresponding section in `README.md` and update it to match the current implementation.

Do not rewrite sections that are unaffected by the changelog. Focus only on the parts that describe what changed.

### 6. Run all tests

```
pytest
```

All tests must pass before continuing. Fix any failures before proceeding.

### 7. Commit, push, and open a PR

Follow the standard workflow: squash to a single commit, verify tests once more, then push and create a PR:

```
git add pyproject.toml CHANGELOG.md README.md
git commit -m "Release <version>"
git push -u origin HEAD
gh pr create --title "Release <version>" --body "Bumps version to <version>. Updates changelog and README."
```

### 8. Wait for PR checks and merge

Monitor the PR checks:

```
gh pr checks --watch
```

Once **all checks pass**, merge the PR:

```
gh pr merge --squash
```

Do not merge if any check is failing.

### 9. Tag and push to trigger PyPI publishing

After the PR is merged, switch to `main`, pull the merge commit, create a version tag, and push it. The tag push triggers the CI pipeline that publishes to PyPI.

```
git checkout main
git pull
git tag v<version>
git push origin v<version>
```

Use the `v` prefix on the tag (e.g. `v1.2.3`). Do not push the tag before the PR is merged.

## Summary Checklist

- [ ] Branch name starts with `feature/` or `fix/`
- [ ] Tests pass before every commit
- [ ] All commits squashed to one before pushing
- [ ] Tests pass after the squash rebase
- [ ] Single commit pushed
- [ ] PR created with `gh pr create`

**Release checklist:**
- [ ] Version confirmed with user
- [ ] `pyproject.toml` version updated
- [ ] `CHANGELOG.md` updated
- [ ] `README.md` reviewed and updated
- [ ] All tests pass
- [ ] Single commit pushed on `feature/release-<version>`
- [ ] PR created
- [ ] All PR checks pass
- [ ] PR merged
- [ ] Tag `v<version>` created on `main` and pushed
