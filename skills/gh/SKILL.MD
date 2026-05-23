---
name: gh
description: Interact with GitHub from the command line using the gh CLI. Use when working with pull requests, issues, repositories, releases, GitHub Actions workflows, or any other GitHub resource directly from the terminal.
enabled_by_default: false
triggers:
- gh
- github cli
- pull request
- open a pr
- create a pr
- merge a pr
- github issue
- github repo
- github actions
- github workflow
- github release
---

# GitHub CLI (gh) Skill

This skill provides capabilities for interacting with GitHub repositories, pull requests, issues, workflows, and more — directly from the terminal using the `gh` CLI.

## Capabilities

- Authenticate with GitHub
- Create, view, list, review, and merge pull requests
- Create, view, list, and close issues
- Clone, create, fork, and manage repositories
- Trigger and monitor GitHub Actions workflows
- Manage releases
- Make raw GitHub API calls

## Authentication

```bash
# Authenticate interactively
gh auth login

# Check current auth status
gh auth status

# Log out
gh auth logout
```

## Pull Requests

```bash
# Create a PR (interactive)
gh pr create

# Create a PR with flags
gh pr create --title "My feature" --body "Description" --base main

# Create a draft PR
gh pr create --draft --title "WIP: My feature" --body "Description"

# List open PRs
gh pr list

# View a PR (in terminal)
gh pr view 123

# View a PR in the browser
gh pr view 123 --web

# Check out a PR branch locally
gh pr checkout 123

# Review a PR
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"
gh pr review 123 --comment --body "Looks good overall"

# Merge a PR
gh pr merge 123 --merge
gh pr merge 123 --squash
gh pr merge 123 --rebase

# Close a PR without merging
gh pr close 123

# Check PR status / CI checks
gh pr checks 123

# Watch CI checks until they complete
gh pr checks 123 --watch
```

## Issues

```bash
# Create an issue (interactive)
gh issue create

# Create an issue with flags
gh issue create --title "Bug: something broken" --body "Steps to reproduce..."

# List open issues
gh issue list

# View an issue
gh issue view 456

# Close an issue
gh issue close 456

# Reopen an issue
gh issue reopen 456

# Add a comment to an issue
gh issue comment 456 --body "This is still happening on v2.1"
```

## Repositories

```bash
# Clone a repository
gh repo clone owner/repo

# Create a new repository
gh repo create my-new-repo --public
gh repo create my-new-repo --private --clone

# Fork a repository
gh repo fork owner/repo --clone

# View repository info
gh repo view owner/repo

# Open repository in browser
gh repo view owner/repo --web

# List repositories for a user or org
gh repo list myorg --limit 50
```

## GitHub Actions Workflows

```bash
# List workflows
gh workflow list

# Run a workflow manually
gh workflow run my-workflow.yml

# Run a workflow with inputs
gh workflow run my-workflow.yml --field environment=production

# List recent workflow runs
gh run list

# View a specific run
gh run view 789

# Watch a run in real time
gh run watch 789

# View logs for a run
gh run view 789 --log

# Re-run a failed run
gh run rerun 789
```

## Releases

```bash
# Create a release
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes here"

# Create a release and upload assets
gh release create v1.0.0 ./dist/binary.tar.gz --title "v1.0.0"

# List releases
gh release list

# View a release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0
```

## GitHub API (Raw Access)

```bash
# GET request
gh api repos/owner/repo

# POST request with JSON body
gh api repos/owner/repo/issues --method POST --field title="New issue" --field body="Body text"

# Use jq to filter JSON output
gh api repos/owner/repo/pulls | jq '.[].title'

# Paginate through all results
gh api --paginate repos/owner/repo/issues
```

## Common Options

- `--web`: Open the result in the browser
- `--json <fields>`: Output specific fields as JSON (e.g. `--json number,title,url`)
- `--jq <expr>`: Filter JSON output with a jq expression
- `--limit <n>`: Limit the number of results returned
- `--repo <owner/repo>`: Target a specific repo instead of the current directory's repo

## Troubleshooting

- Check authentication: `gh auth status`
- Re-authenticate if token is expired: `gh auth login`
- Ensure you are inside a git repository when running repo-scoped commands, or pass `--repo owner/repo` explicitly
- Use `--help` on any command for full flag reference: `gh pr create --help`
