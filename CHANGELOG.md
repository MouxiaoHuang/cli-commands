# Changelog

## 0.3.1

- Fix: ensure deterministic ordering when converting videos with wildcard patterns.

## 0.3.0

- Security: remove shell injection risks by replacing `os.system` with `subprocess.run` and safe path handling.
- Safer `kill`: default to SIGTERM, require `--force` for SIGKILL, and confirm on name matches.
- Added `ls-all` and `ls-recursive` implementations.
- Added comprehensive pytest coverage across all commands.
- Documentation updates and alias list in README.
- Build artifacts verified for PyPI release.
