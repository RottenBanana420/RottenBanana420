# Profile README (RottenBanana420/RottenBanana420)

This repo is the GitHub profile README. It is public. Never commit anything that names a private repo.

## Goal

Make the profile self-updating and tidy:

1. Stats card with totals that include private activity (commits, PRs, issues, reviews). Totals only, no private repo names.
2. Project list generated from public repos only (description, last updated). A `featured` topic pins a repo.
3. Recent-activity feed, public events only.
4. Trimmed tech-stack badges (about 10-15 that match real work) and an intro that matches current work (RAG, multi-agent, data pipelines).

## Decisions so far

- The old widgets were removed because their free hosted servers return 402/503/404: github-readme-stats, streak stats, trophies, contributor stats and the visit counter. Do not re-add them.
- Stats card: GitHub Readme Stats Action (stats-organization/github-readme-stats-action), writes SVGs into `profile/` on a schedule. Needs a PAT with `repo` + `read:user` stored as the repo secret `PAT`. The user creates the PAT; do not reuse the `gh` keyring token.
- Profile setting "Private contributions" must be on (Profile > Contribution settings).
- Activity feed: jamesgeorge007/github-activity-readme, public events only.
- Project list: small Python script plus an Action that rewrites a marked block in README.md.
- Company work (menu-optimization) will move to the company GitHub. It may not count on this profile if the org blocks personal tokens.

## Status

- [x] User creates PAT and adds `PAT` secret (no expiry)
- [x] README rewritten (intro, trimmed badges, marker blocks): committed and pushed
- [x] Stats workflow: live, ran successfully via workflow_dispatch, writes `profile/stats.svg` and `profile/top-langs.svg`
- [x] Project-list script and workflow: live, tests pass, README block populated
- [x] Activity-feed workflow: live, pinned to commit SHA, runs green
- [x] `.gitignore` covers Python caches, venvs, env files, OS/editor files and local Claude settings
- [ ] Activity block in README is empty. The action's `FILTER_EVENTS` only matches issue, issue-comment, PR and release events, and the only public events on the account are two WatchEvents. It fills in once there is public PR/issue activity.
- [ ] No repo has the `featured` topic yet, so nothing is pinned in the project list
- [ ] Show the user the result before every push

## Rules

- Show diffs to the user before committing or pushing. Do not push without being asked.
- The workflows commit back to the repo, so give them `permissions: contents: write` and nothing broader.
