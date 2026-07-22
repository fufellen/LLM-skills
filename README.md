# LLM Skills

Shared AI skills synchronized from the user's Obsidian vault. The repository contains durable shared-base skills, thin Codex and Claude adapters, and a corporate skills submodule.

Canonical local path on the owner's PC:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills
```

The repository intentionally excludes `secrets/`, credentials, caches, and generated logs.

## Mandatory contribution workflow for AI agents

An authenticated repository owner or administrator covered by an active ruleset bypass may push directly to `main`. A fork, separate branch, and pull request are optional for that administrator. Every other account must propose changes through a pull request, and the repository owner or administrator decides whether to merge them.

First clone the canonical repository and initialize its submodules:

```bash
git clone --recurse-submodules https://github.com/fufellen/LLM-skills.git
cd LLM-skills
```

Before choosing a contribution workflow, the local AI must determine:

1. the authenticated GitHub login;
2. whether that account is a repository owner or administrator with an effective bypass for protected `main`;
3. if it is not an administrator with bypass, whether it has push access to `fufellen/LLM-skills`.

Run the repository's access detector from the repository root:

```powershell
$access = powershell -NoProfile -ExecutionPolicy Bypass -File ".\_base\skills\skill-management\scripts\Get-GitHubContributionMode.ps1" -AsJson | ConvertFrom-Json
$access | Format-List
```

The script uses `GH_TOKEN` or `GITHUB_TOKEN` when present, otherwise it asks Git's configured credential helper (for example Git Credential Manager) for the current GitHub credential. It keeps the credential in memory and does not print it. It reads the authenticated login, effective repository permissions, active default-branch rulesets, and the administrator bypass through the GitHub APIs.

The local AI must choose the workflow from the returned fields:

- `AccessClass = administrator` and `DirectMainAllowed = True`: push directly to `origin/main`; a pull request is optional.
- `AccessClass = administrator` and `DirectMainAllowed = False`: do not push to `main`; use `main_<github-login>` in the source repository and open a pull request.
- `AccessClass = write-collaborator`: use `main_<github-login>` in the source repository and open a pull request.
- `AccessClass = external`: create or use the authenticated user's fork, push `main_<github-login>` there, and open a pull request to `fufellen:main`.

Do not infer a role from the login name, ownership of a local clone, or a successful public clone. If the detector cannot authenticate or complete the API checks, do not push to `main`; treat source-repository access as unconfirmed and use the fork workflow after authenticating the user.

GitHub CLI (`gh`) is not required for `git push`: plain Git may authenticate through Git Credential Manager or another configured credential helper. When a pull request is required, open it through an available GitHub connector, the GitHub REST API, the GitHub website, or `gh`.

Use the branch name `main_<github-login>`, replacing `<github-login>` with the actual GitHub login, for example `main_alex-user`.

| Account state | Branch location | Push destination | Pull request |
| --- | --- | --- | --- |
| Owner or administrator with active bypass | `fufellen/LLM-skills` | `origin/main` | Optional |
| Has push access but no administrator bypass | `fufellen/LLM-skills` | `origin/main_<github-login>` | `fufellen:main_<github-login> → fufellen:main` |
| Has no push access or access is unknown | User's fork | `fork/main_<github-login>` | `<github-login>:main_<github-login> → fufellen:main` |

### Account is an administrator with bypass

An administrator with a confirmed active bypass may work directly on `main`:

```bash
git fetch origin main
git switch main
git merge --ff-only origin/main
# edit and validate files
git add path/to/relevant-file
git commit -m "Describe the change"
git push origin main
```

The administrator may still use a separate branch and pull request voluntarily when review or CI isolation is useful.

### Account has push access but no administrator bypass

Keep `origin` pointed at the canonical repository:

```bash
GITHUB_LOGIN="alex-user"
BRANCH="main_${GITHUB_LOGIN}"
git fetch origin main
git switch -c "${BRANCH}" origin/main
# edit and validate files
git add path/to/relevant-file
git commit -m "Describe the change"
git push -u origin "${BRANCH}"
```

Then open a pull request from `main_<github-login>` to `main` in `fufellen/LLM-skills`.

### Account has no push access

Create a GitHub fork under the authenticated user's account. Keep `origin` pointed at the canonical repository so existing freshness checks continue to compare against `origin/main`, and add the fork as a separate remote named `fork`:

```bash
GITHUB_LOGIN="alex-user"
BRANCH="main_${GITHUB_LOGIN}"
git remote -v
git remote add fork "https://github.com/${GITHUB_LOGIN}/LLM-skills.git"
git fetch origin main
git switch -c "${BRANCH}" origin/main
# edit and validate files
git add path/to/relevant-file
git commit -m "Describe the change"
git push -u fork "${BRANCH}"
```

Then open a pull request from `<github-login>:main_<github-login>` to `fufellen:main`.

If the fork was cloned directly and currently uses `origin`, rename that remote to `fork` and restore `origin` as the canonical repository:

```bash
git remote rename origin fork
git remote add origin https://github.com/fufellen/LLM-skills.git
git fetch origin main
```

### Pull-request rules

- Do not merge or close the pull request unless the repository owner explicitly asks; the administrator performs final acceptance.
- If an open pull request already uses `main_<github-login>`, push follow-up commits to the same branch instead of opening a duplicate request.
- Stage only files related to the task. Preserve unrelated local or user changes.
- Do not commit secrets, credentials, private raw data, caches, generated logs, or AI attribution trailers.
- When changing the `nto-formatting` submodule, first commit and publish the corporate repository change; only then commit the updated submodule pointer here.

## Skill architecture

- Durable shared behavior: `_base/skills/<skill-name>/`.
- Codex adapter: `<skill-name>/SKILL.md` plus `agents/openai.yaml`.
- Claude adapter: `.claude/skills/<skill-name>/SKILL.md`.
- Corporate skills: the `nto-formatting` Git submodule.

Keep adapters thin. Store reusable rules, references, scripts, assets, and lessons in the shared base.

## Self-learning requirement

Every non-static canonical shared-base skill must either contain an actionable self-improvement or learning section or explicitly use the shared `skill-learning` policy. Save only durable, reusable lessons; never persist secrets, protected source material, private raw data, or one-off task facts.

Run the repository-wide audit after adding or changing skills:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\_base\skills\skill-learning\scripts\Test-SkillLearningCoverage.ps1"
```

The audit checks canonical shared-base skills in this repository and in initialized nested repositories such as `nto-formatting`. Thin adapters inherit the policy from their shared base and must not duplicate it.
