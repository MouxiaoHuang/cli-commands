# cli-commands

[![GitHub repo](https://img.shields.io/badge/GitHub-cli--commands-181717?logo=github)](https://github.com/MouxiaoHuang/cli-commands)
[![CI](https://github.com/MouxiaoHuang/cli-commands/actions/workflows/ci.yml/badge.svg)](https://github.com/MouxiaoHuang/cli-commands/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/cli-commands-kit)](https://pypi.org/project/cli-commands-kit/)
[![License](https://img.shields.io/pypi/l/cli-commands-kit)](https://pypi.org/project/cli-commands-kit/)
[![GitHub stars](https://img.shields.io/github/stars/MouxiaoHuang/cli-commands)](https://github.com/MouxiaoHuang/cli-commands/stargazers)

`cli-commands` provides a single entrypoint for common terminal tasks. It keeps commands short, consistent, and easy to remember.


## Package Names

- **GitHub repo**: `cli-commands`
- **PyPI package**: `cli-commands-kit` (install with `pip install cli-commands-kit`)
- **Legacy package**: `linux-command` (older name; still installable but no longer updated)


## Why cli-commands

Linux commands are powerful but easy to forget, especially for archives and process checks. `cli-commands` lowers the mental load with a unified syntax that reads like the task itself. For example, `cmd tar <source> <output.tar>` means “pack `<source>` into `<output.tar>`,” no long flags to recall.

## Installation

To install the package, run the following command:

```bash
pip install cli-commands-kit
```

## Install From Source (Development)

If you want to develop or modify the tool locally:

```bash
git clone https://github.com/MouxiaoHuang/cli-commands.git
cd cli-commands
pip install -e .
```

## Usage

Once installed, run commands with `cmd <command> [args...]` or `cli <command> [args...]`.

- `cmd -h` / `cmd --help` lists all available commands.
- `cmd <command> -h` shows usage and examples for a specific command.
- **`cli` behaves the same as `cmd` (alternate entrypoint).**

Quick examples:

```bash
cmd tar ./src out.tar.gz
cmd untar archive.tar.gz ./out
cmd ps-grep python
```

Before vs cmd:

```
tar -czvf out.tar.gz ./src        ->  cmd tar ./src out.tar.gz
tar -xzvf archive.tar.gz -C ./out ->  cmd untar archive.tar.gz ./out
ps aux | grep python              ->  cmd ps-grep python
```

Full command list, examples, and aliases live in [`USAGE.md`](USAGE.md).

## Contributing

We welcome contributions from the community! If you'd like to help improve `cli-commands`, feel free to report issues or submit pull requests.

### Guidelines for Contributors

- Follow the existing coding style where possible.
- Make sure your changes do not break existing functionality.
- Before submitting a major feature, it’s often a good idea to first discuss it by opening an issue.

### Thank you!

Thank you for your interest in contributing to `cli-commands`! Your contributions are greatly appreciated and help make this tool better for everyone. For any questions or to get started, feel free to reach out or open an issue.

---

## License

This project is licensed under the MIT License.
