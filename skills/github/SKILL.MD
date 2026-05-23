---
name: GitHub
version: 1.0.0
description: Query the GitHub API - search repos and issues, get repo info, read files. Set GITHUB_TOKEN for authenticated access (5000 req/hour vs 60 unauthenticated).
tags: [github, search, code, api]
enabled_by_default: false
triggers: [github, repo, repository, pull request, issue, PR, open source, star]
---

## Tools

### github_search_repos
description: Search GitHub repositories by keyword, language, or other qualifiers (e.g. "language:python stars:>1000").
entrypoint: python:github.tools.search_repos
schema:
  type: object
  properties:
    query:
      type: string
      description: GitHub search query (supports qualifiers like language:python, stars:>100, user:gkvas)
    max_results:
      type: integer
      description: Number of results to return (default 5)
      default: 5
  required: [query]

### github_search_issues
description: Search GitHub issues and pull requests (e.g. "repo:owner/repo is:open label:bug").
entrypoint: python:github.tools.search_issues
schema:
  type: object
  properties:
    query:
      type: string
      description: GitHub issue search query (supports is:open, is:pr, label:bug, repo:owner/repo, etc.)
    max_results:
      type: integer
      description: Number of results to return (default 5)
      default: 5
  required: [query]

### github_get_repo
description: Get details about a specific GitHub repository including stars, forks, open issues, and description.
entrypoint: python:github.tools.get_repo
schema:
  type: object
  properties:
    owner:
      type: string
      description: Repository owner (user or organisation)
    repo:
      type: string
      description: Repository name
  required: [owner, repo]

### github_get_file
description: Read the content of a file in a GitHub repository, or list directory contents if path is a directory.
entrypoint: python:github.tools.get_file
schema:
  type: object
  properties:
    owner:
      type: string
      description: Repository owner
    repo:
      type: string
      description: Repository name
    path:
      type: string
      description: Path to the file or directory within the repository
    ref:
      type: string
      description: Branch, tag, or commit SHA (defaults to the default branch)
  required: [owner, repo, path]
