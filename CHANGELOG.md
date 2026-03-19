# Changelog

## Unreleased

- Added:
- Changed:
- Fixed:



## 1.0.1

- Changed: README clarifies repo vs PyPI package names and legacy package note.

## 1.0.0

- Added: `cli` entrypoint (alias of `cmd`).
- Changed: package/repo/module renamed to `cli-commands`/`cli_commands`.
- Changed: help output grouped by function with alias hints.
- Changed: README and USAGE refreshed; quick examples and directory links.
- Changed: file counting now uses `os.scandir` for performance.
- Fixed: expanded tests and renamed test module for new package layout.

## 0.3.2

- Added: grouped `cmd -h` output with alias hints; alias-aware command help.
- Added: USAGE directory with categories and alias inline labels.
- Changed: README copy refreshed with clearer positioning and quick examples.
- Changed: file counting now uses `os.scandir` for better performance.
- Fixed: test coverage expanded to include `df`, `ls-bs`, and `zip-all`.

## 0.3.1

- Fix: ensure deterministic ordering when converting videos with wildcard patterns.

## 0.3.0

- Security: remove shell injection risks by replacing `os.system` with `subprocess.run` and safe path handling.
- Safer `kill`: default to SIGTERM, require `--force` for SIGKILL, and confirm on name matches.
- Added `ls-all` and `ls-recursive` implementations.
- Added comprehensive pytest coverage across all commands.
- Documentation updates and alias list in README.
- Build artifacts verified for PyPI release.
