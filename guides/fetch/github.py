import httpx

from ..settings import Settings
from .base import FetchedContent, QueueItem, SourceType


def fetch_github(item: QueueItem) -> FetchedContent:
    url = item.source
    parts = url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    settings = Settings()
    headers: dict[str, str] = {}
    if settings.github_token:
        headers["Authorization"] = f"token {settings.github_token}"

    source_meta: dict[str, object] = {}

    try:
        repo_resp = httpx.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers, timeout=30)
        if repo_resp.status_code == 200:
            data = repo_resp.json()
            source_meta = {
                "name": data.get("full_name", ""),
                "description": data.get("description", ""),
                "stars": data.get("stargazers_count", 0),
                "language": data.get("language", ""),
            }
        else:
            source_meta["error"] = f"github_api_status:{repo_resp.status_code}"
    except Exception as e:
        source_meta["error"] = str(e)

    readme = ""
    try:
        readme_resp = httpx.get(
            f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md",
            headers=headers,
            timeout=30,
        )
        if readme_resp.status_code == 200:
            readme = readme_resp.text
    except Exception:
        pass

    raw_text = f"# {source_meta.get('name', f'{owner}/{repo}')}\n\n"
    if source_meta.get("description"):
        raw_text += f"{source_meta['description']}\n\n"
    raw_text += f"**Stars:** {source_meta.get('stars', '?')}  \n"
    raw_text += f"**Language:** {source_meta.get('language', '?')}\n\n---\n\n"
    raw_text += readme

    return FetchedContent(raw_text=raw_text.strip(), source_type=SourceType.GITHUB_REPO, source_meta=source_meta)