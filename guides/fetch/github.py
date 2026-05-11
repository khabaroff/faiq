import httpx

from guides.settings import Settings

from guides.fetch.base import FetchedContent, QueueItem, SourceType


def fetch_github_repo(item: QueueItem) -> FetchedContent:
    url = item.source.rstrip("/")
    parts = url.split("/")
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = _get_headers()
    
    try:
        resp = httpx.get(api_url, headers=headers, timeout=30)
        resp.raise_for_status()
        repo_data = resp.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch GitHub repo: {url}") from e
    
    readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
    readme_text = _try_fetch_readme(readme_url, headers)
    
    raw_text = _format_repo_text(repo_data, readme_text, url)
    
    return FetchedContent(
        raw_text=raw_text,
        source_type=SourceType.GITHUB_REPO,
        source_meta={"url": url, "owner": owner, "repo": repo},
    )


def _get_headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        token = Settings().github_token
        if token:
            headers["Authorization"] = f"token {token}"
    except Exception:
        pass
    return headers


def _try_fetch_readme(url: str, headers: dict[str, str]) -> str:
    try:
        resp = httpx.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return ""


def _format_repo_text(repo_data: dict, readme: str, url: str) -> str:
    lines = [
        f"# {repo_data.get('name', 'Unknown')}",
        "",
        f"URL: {url}",
        f"Description: {repo_data.get('description', 'N/A')}",
        f"Stars: {repo_data.get('stargazers_count', 0)}",
        f"Language: {repo_data.get('language', 'Unknown')}",
        f"Topics: {', '.join(repo_data.get('topics', []))}",
        "",
        "## README",
        "",
        readme if readme else "_No README available_",
    ]
    return "\n".join(lines)