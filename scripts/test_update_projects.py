import update_projects as up


def repo(name, pushed="2026-01-01T00:00:00Z", **kw):
    base = {"name": name, "html_url": f"https://github.com/o/{name}", "description": "d",
            "language": "Python", "pushed_at": pushed, "private": False, "fork": False,
            "archived": False, "topics": []}
    return base | kw


def test_select_drops_private_forks_archived_and_profile_repo():
    repos = [repo("a"), repo("b", private=True), repo("c", fork=True),
             repo("d", archived=True), repo("O")]
    assert [r["name"] for r in up.select(repos, "o")] == ["a"]


def test_featured_first_then_newest():
    repos = [repo("old", "2025-01-01T00:00:00Z"), repo("new", "2026-06-01T00:00:00Z"),
             repo("pin", "2024-01-01T00:00:00Z", topics=["featured"])]
    out = up.render(repos)
    assert out.index("pin") < out.index("new") < out.index("old")
    assert "⭐" in out.split("\n")[0]


def test_replace_block_is_idempotent_and_keeps_surroundings():
    text = f"before\n{up.START}\nstale\n{up.END}\nafter"
    once = up.replace_block(text, "fresh")
    assert once == f"before\n{up.START}\nfresh\n{up.END}\nafter"
    assert up.replace_block(once, "fresh") == once


def test_missing_markers_raises():
    try:
        up.replace_block("no markers", "x")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_repo_with_null_pushed_at_does_not_crash():
    repos = [repo("empty", pushed=None, updated_at="2026-02-02T00:00:00Z"), repo("full")]
    out = up.render(repos)
    assert "empty" in out and "updated 2026-02-02" in out
    assert "updated" not in up.render([repo("bare", pushed=None)])
