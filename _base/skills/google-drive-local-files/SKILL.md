---
name: google-drive-local-files
description: Work with the user's Google Drive through the local synced Windows filesystem, especially `C:\Users\User\Мой диск`, instead of the native Google Drive connector. Use when the user asks about Google Drive, "Мой диск", Google storage, Drive cleanup, junk files, duplicates, large files, local Drive organization, or skills/files stored in Google Drive, unless the user explicitly asks for cloud-native Drive metadata, sharing, comments, revisions, or connector/API access.
---

# Google Drive Local Files

## Default Access Mode

Treat the user's Google Drive as a local synced filesystem on this PC.

Default roots:

- Drive root: `C:\Users\User\Мой диск`
- Obsidian vault: `C:\Users\User\Мой диск\Obsidian`
- Personal skill repository: `C:\Users\User\Мой диск\Obsidian\.codex\skills`

Prefer filesystem tools such as `rg`, `Get-ChildItem`, `Get-Item`, `Select-String`, file metadata, and hashes. Do not use the native Google Drive connector for ordinary Drive search, cleanup, organization, local file inspection, or skill edits.

Use the native Drive connector only when the user explicitly asks for cloud-native Drive behavior, or when the task truly requires data unavailable from the synced filesystem: sharing permissions, comments, revisions, Drive labels, ownership metadata, cloud-only files that are not present locally, or direct Google Workspace edits.

## Workflow

1. Ground the target root first. If the user says "Google Drive", "Мой диск", or "хранилище", start from `C:\Users\User\Мой диск` unless they gave a narrower path.
2. Inspect before judging. Use `Get-ChildItem -Force`, `rg --files`, sizes, timestamps, extensions, and nearby folder context before calling anything junk.
3. Report candidates, not verdicts, when user asks for cleanup. Group findings by confidence and explain why each category looks disposable or worth review.
4. Do not delete, move, rename, or bulk-edit Drive files unless the user explicitly asks for that action after seeing the candidates.
5. Before recursive delete or move, resolve absolute paths and verify every target stays inside the intended Drive subtree. Avoid touching active sync temp files while Google Drive is currently downloading or uploading.

## Junk Heuristics

Usually safe to flag as likely junk:

- Office lock files: `~$*`, especially zero-byte `.doc`, `.docx`, `.pptx`, `.xlsx` files left after editing.
- Temporary download/upload remnants: `.tmp.drivedownload`, `.tmp.driveupload`, `.crdownload`, `.part`, `.tmp`, `.temp`, after checking they are stale and sync is not active.
- Cache/build byproducts: `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.ipynb_checkpoints`, `.cache`, `dist`, `build`, when they are not the only copy of source work.
- Logs and recoveries: `.log`, `.class.recovery`, compiler clean logs, empty `.old` solution/project backups, when context shows they are generated artifacts.
- Obsidian `.trash` contents, but still report before deleting because the user may intentionally keep recoverable notes there.

Flag as review candidates, not automatic junk:

- Large archives and installers: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.tgz`, `.iso`, `.exe`, `.msi`.
- Duplicate-looking names: `copy`, `Copy`, `копия`, `дубликат`, `duplicate`, `(1)`, `(2)`, ` - Copy`, `_copy`.
- Big media, raw captures, datasets, COMSOL models, CSV captures, or photos. These may be valuable research or personal records even when huge.

Treat as harmless system noise unless the user asks to remove all of it:

- `desktop.ini` and `Thumbs.db`. `desktop.ini` in Google Drive/Windows folders can store folder icon/view metadata and may be regenerated.

## Useful Commands

List root items:

```powershell
Get-ChildItem -LiteralPath 'C:\Users\User\Мой диск' -Force | Select-Object Name,Mode,Length,LastWriteTime
```

Find largest files:

```powershell
Get-ChildItem -LiteralPath 'C:\Users\User\Мой диск' -Recurse -Force -File -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First 50 @{n='SizeMB';e={[math]::Round($_.Length/1MB,2)}}, LastWriteTime, FullName
```

Find common junk candidates:

```powershell
$root = 'C:\Users\User\Мой диск'
$rx = '(?i)(^desktop\.ini$|^thumbs\.db$|^\.ds_store$|\.tmp$|\.temp$|\.bak$|\.old$|\.orig$|\.crdownload$|\.part$|^~\$|~$|\.log$)'
Get-ChildItem -LiteralPath $root -Recurse -Force -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match $rx } |
  Sort-Object Length -Descending
```

Find duplicate-looking names:

```powershell
$root = 'C:\Users\User\Мой диск'
$rx = '(?i)(copy|копия|дубликат|duplicate|\(\d+\)| - Copy|_copy|backup|резерв|old|untitled|без названия|tmp|temp|test)'
Get-ChildItem -LiteralPath $root -Recurse -Force -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match $rx } |
  Sort-Object Length -Descending
```

## Skill Files

When the user says that skills are on Google Drive, use the synced skill repository at `C:\Users\User\Мой диск\Obsidian\.codex\skills`. Do not switch to local plugin caches or non-synced bootstrap copies for durable user-owned skill edits.

For creating or updating user-owned skills, also use `skill-authoring`, `skill-management`, and `skill-learning` as applicable. Store durable behavior in `_base/skills/<skill-name>/` and keep AI-specific adapters thin.

## Reporting

In cleanup reports, separate:

- likely disposable generated junk;
- large files to review;
- duplicates or suspected duplicates;
- items that are not junk by default but may be storage-heavy.

Mention that the result reflects the locally synced Drive view. Cloud-only metadata, sharing state, comments, and revision history are outside this filesystem-only view.

## Learning

When work reveals a durable Google Drive filesystem preference, cleanup heuristic, safety rule, or reusable command, use the `skill-learning` policy and save the compact rule here or in a focused reference file. Do not store personal file contents, secrets, private data, or one-off cleanup lists.
