#!/usr/bin/env python3
"""Rewrite the PROJECTS block in README.md from the owner's public repos.

Only /users/{owner}/repos is queried, which never returns private repos, and
anything with private=true is dropped again as a second guard. Repos with the
`featured` topic are listed first and marked.
"""
import json
import os
import re
import sys
import urllib.request

OWNER = os.environ.get("PROFILE_OWNER", "RottenBanana420")
README = os.environ.get("README_PATH", "README.md")
START, END = "<!-- PROJECTS:START -->", "<!-- PROJECTS:END -->"
FEATURED_TOPIC = "featured"


def fetch_repos(owner, token=None):
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/users/{owner}/repos?type=owner&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.load(resp)
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1


def select(repos, owner):
    """Public, non-fork, non-archived repos, excluding the profile repo itself."""
    return [
        r for r in repos
        if not r["private"] and not r["fork"] and not r["archived"]
        and r["name"].lower() != owner.lower()
    ]


def last_activity(repo):
    """ISO timestamp of the last push; empty repos have pushed_at null."""
    return repo.get("pushed_at") or repo.get("updated_at") or ""


def order(repos):
    """Featured first, then most recently pushed (ISO timestamps sort as strings)."""
    newest_first = sorted(repos, key=last_activity, reverse=True)
    return sorted(newest_first, key=lambda r: FEATURED_TOPIC not in r.get("topics", []))


def render(repos):
    if not repos:
        return "_No public projects yet._"
    lines = []
    for r in order(repos):
        star = "⭐ " if FEATURED_TOPIC in r.get("topics", []) else ""
        desc = (r.get("description") or "").strip()
        updated = last_activity(r)[:10]
        meta = " · ".join(filter(None, [r.get("language"), f"updated {updated}" if updated else ""]))
        line = f"- {star}**[{r['name']}]({r['html_url']})**"
        if desc:
            line += f": {desc}"
        lines.append(f"{line}  \n  <sub>{meta}</sub>")
    return "\n".join(lines)


def replace_block(text, body):
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        raise ValueError(f"markers {START} / {END} not found")
    return pattern.sub(lambda _: f"{START}\n{body}\n{END}", text, count=1)


def main():
    repos = select(fetch_repos(OWNER, os.environ.get("GITHUB_TOKEN")), OWNER)
    with open(README, encoding="utf-8") as f:
        text = f.read()
    new = replace_block(text, render(repos))
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
    print(f"{len(repos)} public project(s); README {'updated' if new != text else 'unchanged'}")


if __name__ == "__main__":
    sys.exit(main())
