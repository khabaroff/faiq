import httpx

from guides.settings import Settings

from guides.fetch.base import FetchedContent, QueueItem, SourceType


def fetch_github_gist(item: QueueItem) -> FetchedContent:
    url = item.source.rstrip("/")
    gist_id = url.split("/")[-1]
    headers = _get_headers()

    try:
        resp = httpx.get(f"https://api.github.com/gists/{gist_id}", headers=headers, timeout=30)
        resp.raise_for_status()
        gist_data = resp.json()
        raw_text = _format_gist_text(gist_data, url)
        owner = gist_data.get("owner", {}).get("login", "unknown")
        return FetchedContent(
            raw_text=raw_text,
            source_type=SourceType.GITHUB_GIST,
            source_meta={"url": url, "gist_id": gist_id, "owner": owner},
        )
    except Exception:
        pass

    # Fallback: fetch via Jina reader when API is unavailable
    raw_text = _fetch_gist_via_jina(url)
    if not raw_text:
        raise RuntimeError(f"Failed to fetch GitHub gist: {url}")
    return FetchedContent(
        raw_text=raw_text,
        source_type=SourceType.GITHUB_GIST,
        source_meta={"url": url, "gist_id": gist_id, "fetcher": "jina"},
    )


def _fetch_gist_via_jina(url: str) -> str:
    try:
        resp = httpx.get(f"https://r.jina.ai/{url}", headers={"Accept": "text/markdown"}, timeout=30, follow_redirects=True)
        if resp.status_code == 200 and len(resp.text.strip()) > 100:
            return resp.text.strip()
    except Exception:
        pass
    return ""


def _format_gist_text(gist_data: dict, url: str) -> str:
    description = gist_data.get("description") or "Untitled Gist"
    owner = gist_data.get("owner", {}).get("login", "unknown")
    files = gist_data.get("files", {})
    lines = [
        f"# {description}",
        "",
        f"URL: {url}",
        f"Author: {owner}",
        f"Files: {', '.join(files.keys())}",
        "",
    ]
    for filename, fdata in files.items():
        lang = fdata.get("language") or "text"
        content = fdata.get("content") or ""
        lines += [f"## {filename}", "", f"```{lang.lower()}", content, "```", ""]
    return "\n".join(lines)


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