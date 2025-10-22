import json
import os
import sys
import urllib.request

GH_API = "https://api.github.com/graphql"
TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GH_USERNAME", "ShubhZ06")
README_PATH = os.path.join(os.getcwd(), "README.md")

OWNED_START = "<!-- REPO-LIST:OWNED:START -->"
OWNED_END = "<!-- REPO-LIST:OWNED:END -->"
COLLAB_START = "<!-- REPO-LIST:COLLAB:START -->"
COLLAB_END = "<!-- REPO-LIST:COLLAB:END -->"


def gh_graphql(query: str, variables: dict):
    if not TOKEN:
        print("Missing GITHUB_TOKEN", file=sys.stderr)
        sys.exit(1)
    data = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(GH_API, data=data, headers={
        "Authorization": f"bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "repo-list-updater"
    })
    with urllib.request.urlopen(req) as resp:
        body = resp.read()
        return json.loads(body.decode("utf-8"))


def fetch_owned(login: str):
    q = """
    query($login: String!, $n: Int!) {
      user(login: $login) {
        repositories(first: $n, isFork: false, privacy: PUBLIC, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            nameWithOwner
            url
            description
            stargazerCount
            updatedAt
            primaryLanguage { name }
          }
        }
      }
    }
    """
    res = gh_graphql(q, {"login": login, "n": 100})
    nodes = res.get("data", {}).get("user", {}).get("repositories", {}).get("nodes", [])
    return nodes


def fetch_collab(login: str):
    q = """
    query($login: String!, $n: Int!) {
      user(login: $login) {
        repositoriesContributedTo(first: $n, includeUserRepositories: false, privacy: PUBLIC, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            nameWithOwner
            url
            description
            stargazerCount
            updatedAt
            primaryLanguage { name }
          }
        }
      }
    }
    """
    res = gh_graphql(q, {"login": login, "n": 100})
    nodes = res.get("data", {}).get("user", {}).get("repositoriesContributedTo", {}).get("nodes", [])
    # Deduplicate any that are owned
    return nodes


def to_markdown_list(repos):
    lines = []
    for r in repos:
        name = r.get("nameWithOwner")
        url = r.get("url")
        desc = (r.get("description") or "").replace("\n", " ")
        stars = r.get("stargazerCount", 0)
        lang = r.get("primaryLanguage", {}) or {}
        lang_name = lang.get("name")
        suffix = f" • ⭐ {stars}" if stars else ""
        if lang_name:
            suffix += f" • {lang_name}"
        if desc:
            lines.append(f"- [{name}]({url}) — {desc}{suffix}")
        else:
            lines.append(f"- [{name}]({url}){suffix}")
    if not lines:
        lines.append("- No repositories found yet.")
    return "\n".join(lines)


def replace_section(text: str, start: str, end: str, new_content: str) -> str:
    start_idx = text.find(start)
    end_idx = text.find(end)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        return text
    before = text[: start_idx + len(start)]
    after = text[end_idx:]
    return before + "\n" + new_content + "\n" + after


def main():
    owned = fetch_owned(USERNAME)
    collab = fetch_collab(USERNAME)

    # Remove overlap: don't repeat owned in collab
    owned_names = {r.get("nameWithOwner") for r in owned}
    collab = [r for r in collab if r.get("nameWithOwner") not in owned_names]

    owned_md = to_markdown_list(owned)
    collab_md = to_markdown_list(collab)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    updated = replace_section(content, OWNED_START, OWNED_END, owned_md)
    updated = replace_section(updated, COLLAB_START, COLLAB_END, collab_md)

    if updated != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated)
        print("README updated")
    else:
        print("No changes needed")


if __name__ == "__main__":
    main()
