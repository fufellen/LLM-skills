# LLM Skills

Shared AI skills synchronized from the user's Obsidian vault. The repository contains durable shared-base skills, thin Codex and Claude adapters, and a corporate skills submodule.

Local paths are machine-specific. On a new PC, do not copy an example path from
another machine: ask the user where to clone the skills repository and where the
local Obsidian vault is located.

The repository intentionally excludes `secrets/`, credentials, caches, and generated logs.

## First-time Codex setup on another PC

This is a setup procedure for a person, not a list of paths that are assumed to
exist. Choose the repository clone URL, open Codex, and send the prompt below.
The agent must ask for the two local paths before it makes changes.

Codex's supported agent-writable equivalent of persistent user instructions is
the global `AGENTS.md`: `$CODEX_HOME/AGENTS.md`, or `~/.codex/AGENTS.md` when
`CODEX_HOME` is not set (`%USERPROFILE%\.codex\AGENTS.md` on Windows). The agent
may create or update that file when the setup prompt authorizes it. It must
preserve existing instructions and change only its marked block. A non-empty
global `AGENTS.override.md` takes precedence, so the agent must report it instead
of silently writing instructions that Codex will not currently load.

Copy this prompt and replace `<clone URL selected by the user>` with the chosen
HTTPS or SSH clone URL:

```text
Настрой выбранный репозиторий навыков для Codex на этом ПК.

URL для клонирования: <clone URL selected by the user>

1. До клонирования спроси меня, в какую локальную папку поместить репозиторий.
   Не предполагай, что путь совпадает с путём на другом ПК. Если папка уже
   существует, сначала безопасно проверь её и не перезаписывай чужие файлы.
2. Клонируй репозиторий вместе с подмодулями либо, если это уже корректный clone,
   безопасно обнови его и инициализируй подмодули.
3. Спроси меня, где на этом ПК находится Obsidian vault, и проверь существование
   выбранной папки.
4. Определи путь к глобальным инструкциям Codex: используй
   $CODEX_HOME/AGENTS.md, если CODEX_HOME задан, иначе ~/.codex/AGENTS.md.
   Не пытайся изменять поле «Пользовательские инструкции» в интерфейсе приложения.
5. Сохрани существующее содержимое AGENTS.md и создай или обнови только блок
   между маркерами <!-- llm-skills:start --> и <!-- llm-skills:end -->. В блоке
   запиши абсолютный путь к клонированному репозиторию навыков и указание
   загружать из него релевантные навыки; также запиши абсолютный путь к Obsidian
   vault и указание использовать его во всех задачах с Obsidian.
6. Не записывай один фиксированный способ публикации. Укажи, что перед каждым
   push или PR для этого репозитория агент обязан запустить из корня репозитория
   _base/skills/skill-management/scripts/Get-GitHubContributionMode.ps1 -AsJson
   и выбрать маршрут по фактическому доступу:
   - администратор с действующим bypass: прямой push в origin/main разрешён,
     pull request необязателен;
   - участник с правом записи без bypass: ветка main_<github-login> в исходном
     репозитории и pull request в main;
   - внешний пользователь без права записи: fork, ветка main_<github-login>,
     push в fork и pull request в fufellen/LLM-skills:main;
   - если доступ нельзя надёжно определить: не push в main, а сначала сообщить
     о проблеме с аутентификацией и повторить проверку после её устранения.
7. Если рядом с глобальным AGENTS.md есть непустой AGENTS.override.md, сообщи,
   что он временно перекрывает AGENTS.md, и не изменяй override без моего согласия.
8. Покажи мне итоговые пути, файл с инструкциями, результат проверки доступа и
   выбранный для текущей учётной записи способ публикации. После этого предложи
   начать новую задачу Codex, чтобы инструкции гарантированно загрузились.
```

The access check must be repeated before publication because the authenticated
account, repository permissions, or branch rules may change later. The detailed
decision table and commands are documented below.

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
