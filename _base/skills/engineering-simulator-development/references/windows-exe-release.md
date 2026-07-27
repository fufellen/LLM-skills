# Windows EXE Release

Use this workflow when delivering a Windows executable for an engineering simulator.

## Build Inputs

- Keep a reproducible build script in the simulator repository.
- Pin or document the Python/toolchain version and packaging dependencies.
- Include scenario/configuration data explicitly; prefer absolute source paths when the packager resolves data paths relative to a generated specification directory.
- Build from the committed source state that will be pushed.

## Candidate-First Workflow

1. Check whether the canonical executable is running by comparing its resolved executable path, not only its process name.
2. Build into a separate candidate directory under ignored artifacts or a temporary directory.
3. Smoke-test the candidate from a neutral working directory so it cannot depend on repository-relative files.
4. Exercise a representative application tab and create a screenshot or other deterministic artifact.
5. Inspect the artifact visually; a zero exit code alone does not prove readable UI.
6. Compute the candidate size and SHA-256 hash.
7. If the canonical executable is unlocked, copy the exact tested candidate to the canonical path and verify that the hashes match.
8. Smoke-test the canonical path once more.

## Locked Executable

- Do not wait for the user merely because the canonical simulator executable is running.
- Resolve every matching process by its full executable path. A one-file packager such as PyInstaller can expose a launcher and a child process for one visible application; close the whole exact-path group.
- Request normal closure first (`CloseMainWindow` or the platform-equivalent) so close handlers can persist settings, wait for a short bounded interval, then terminate only the exact-path processes that remain. Recheck that the canonical path is unlocked before copying.
- Apply autonomous closure only to the simulator artifact being replaced. Never use a broad process-name kill and do not close unrelated editors or engineering tools that may contain unsaved documents.
- Do not silently publish a permanent `.new.exe` as the final artifact.
- Keep the verified candidate separately until the canonical copy and hash verification succeed, then replace the canonical path during the same task.
- Report a blocker only if the verified exact-path processes cannot be closed or the file remains locked after the bounded close-and-terminate sequence.

## Qt And Visual Smoke Tests

- Run at least one smoke test on the native Windows platform.
- Treat offscreen Qt rendering as a headless functional check only. Some Windows/offscreen combinations render Cyrillic or unavailable fonts as square glyphs even when the native application is correct.
- If offscreen and native screenshots differ, inspect both and use the native run to judge Windows font rendering.
- Check table headings, Cyrillic text, units, scroll areas, initial window size, and high-density plots.

## Completion Evidence

Report:

- canonical absolute path;
- source commit and pushed branch;
- build and smoke-test result;
- executable size and SHA-256;
- whether any suffixed fallback executable remains;
- whether reference software/firmware repositories stayed unmodified.
