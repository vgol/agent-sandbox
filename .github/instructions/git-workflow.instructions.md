---
description: "Use when creating or renaming branches, writing or rewording commits, opening or updating pull requests, or linking work to GitHub issues."
---

# Issue-linked Git workflow

- Identify the GitHub issue before starting issue-related work. Do not invent an
  issue number or associate unrelated work with an issue.
- Name branches `<type>/<issue-number>-<short-kebab-case-description>`, for
  example `feat/6-hermes-docker-image`. Use `feat`, `fix`, `docs`, `refactor`,
  `test`, `build`, `ci`, or `chore` consistently with the work.
- Use Conventional Commit subjects:
  `<type>(<optional-scope>): <imperative summary> (#<issue-number>)`.
  Omit the parentheses when there is no scope. For example:
  `feat(docker): add Hermes agent image (#6)`.
- Preserve existing authorship and trailers when rewording commits. Include
  `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` for
  Copilot-assisted commits.
- Use the same subject format for PR titles. Add `Closes #<issue-number>` to the
  PR body only when merging the PR should complete the issue; otherwise use
  `Refs #<issue-number>`. Use `owner/repo#<issue-number>` for cross-repository
  references.
- Branch names provide traceability, but do not create GitHub issue links by
  themselves. Commit references create links; closing keywords in PR bodies
  establish automatic closure when merged into the default branch.
- Do not invent a future PR number. GitHub associates commits with the PR that
  contains them; reference an existing PR only when relevant.
- Rewrite published history only with explicit authorization. Preserve file
  contents when only rewording, verify the remote tip, and use
  `--force-with-lease` with the expected commit rather than `--force`.
- Renaming an open PR's head branch on GitHub closes that PR. Account for this
  before renaming: preserve its description and review history, and link any
  replacement PR back to the original.
- After publishing, verify local and remote branch tips, commit messages,
  upstream tracking, and the PR's issue link.
