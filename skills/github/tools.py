"""
Entrypoints for the GitHub skill.

Reads GITHUB_TOKEN from the environment for authentication (5000 req/hour).
Falls back to unauthenticated if not set (60 req/hour).
"""

import base64
import os
import requests


def _session() -> requests.Session:
    s = requests.Session()
    s.headers["Accept"] = "application/vnd.github+json"
    s.headers["X-GitHub-Api-Version"] = "2022-11-28"
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


def _get(path: str, params: dict = None) -> dict | list:
    url = f"https://api.github.com{path}"
    r = _session().get(url, params=params)
    r.raise_for_status()
    return r.json()


def search_repos(query: str, max_results: int = 5, **_) -> str:
    data = _get("/search/repositories", {"q": query, "per_page": max_results})
    items = data.get("items", [])
    if not items:
        return "No repositories found."
    lines = []
    for r in items:
        lines.append(
            f"{r['full_name']}  ★{r['stargazers_count']}  {r['language'] or ''}\n"
            f"  {r['description'] or '(no description)'}\n"
            f"  {r['html_url']}"
        )
    return "\n\n".join(lines)


def search_issues(query: str, max_results: int = 5, **_) -> str:
    data = _get("/search/issues", {"q": query, "per_page": max_results})
    items = data.get("items", [])
    if not items:
        return "No issues or pull requests found."
    lines = []
    for i in items:
        kind = "PR" if i.get("pull_request") else "Issue"
        lines.append(
            f"[{kind} #{i['number']}] {i['title']}  ({i['state']})\n"
            f"  {i['html_url']}"
        )
    return "\n\n".join(lines)


def get_repo(owner: str, repo: str, **_) -> str:
    r = _get(f"/repos/{owner}/{repo}")
    return (
        f"{r['full_name']}  ★{r['stargazers_count']}  "
        f"Forks: {r['forks_count']}  Open issues: {r['open_issues_count']}\n"
        f"Language: {r.get('language') or 'N/A'}\n"
        f"Description: {r.get('description') or '(none)'}\n"
        f"Default branch: {r['default_branch']}\n"
        f"URL: {r['html_url']}"
    )


def get_file(owner: str, repo: str, path: str, ref: str = None, **_) -> str:
    params = {"ref": ref} if ref else None
    data = _get(f"/repos/{owner}/{repo}/contents/{path}", params)
    if isinstance(data, list):
        # Directory listing
        entries = [f"{'d' if e['type'] == 'dir' else 'f'}  {e['name']}" for e in data]
        return "\n".join(entries)
    content = data.get("content", "")
    encoding = data.get("encoding", "")
    if encoding == "base64":
        return base64.b64decode(content).decode("utf-8", errors="replace")
    return content
