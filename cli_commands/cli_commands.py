#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Command Wrapper

Copyright (c) 2024 Mouxiao Huang (huangmouxiao@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

For more information, visit the project page: https://github.com/MouxiaoHuang/cli-commands
"""
import argparse
import glob
import os
import shutil
import signal
import subprocess
from fnmatch import fnmatch


# Define the version 
VERSION = "1.0.2"
PROJECT_URL = "https://github.com/MouxiaoHuang/cli-commands" 


# Command descriptions (short and precise)
commands = {
    'ls': 'List files in current directory.',
    'ls-all': 'List files including hidden.',
    'lsf': 'Count files; optionally filter by pattern.',
    'ls-file': 'Count files; optionally filter by pattern.',
    'lsd': 'Count directories in current directory.',
    'ls-dir': 'Count directories in current directory.',
    'ls-reverse': 'List files in reverse order.',
    'ls-time': 'List by modified time (newest first).',
    'ls-human': 'List with human-readable sizes.',
    'ls-long': 'List in long format.',
    'ls-size': 'List by size (largest first).',
    'ls-recursive': 'List files recursively.',
    'ls-recursive-size': 'Recursive list with human-readable sizes.',
    'ls-bs': 'List with custom block size.',
    'ls-block-size': 'List with custom block size.',
    'ps': 'Show basic process list.',
    'ps-all': 'Show all processes.',
    'ps-user': 'Show processes for a user.',
    'ps-aux': 'Show detailed process list.',
    'ps-sort-memory': 'Sort processes by memory usage.',
    'ps-sort-cpu': 'Sort processes by CPU usage.',
    'ps-grep': 'Search processes by keyword.',
    'kill': 'Kill process by PID or keyword.',
    'df': 'Show disk free space.',
    'du': 'Show directory size (default: current).',
    'disk': 'Show directory size (default: current).',
    'rm': 'Remove file or directory with confirmation.',
    'grep': 'Search pattern in a file.',
    'tar': 'Create .tar/.tar.gz archive.',
    'tar-compress': 'Create .tar/.tar.gz archive.',
    'untar': 'Extract .tar/.tar.gz or batch from dir.',
    'tar-extract': 'Extract .tar/.tar.gz or batch from dir.',
    'tar-list': 'List contents of a tar file.',
    'tar-add': 'Add file to a tar archive.',
    'zip': 'Create .zip archive.',
    'zip-compress': 'Create .zip archive.',
    'zip-all': 'Create .zip archive.',
    'unzip': 'Extract all zips in a directory.',
    'unzip-all': 'Extract all zips in a directory.',
    'convert-vid': 'Convert video file(s) or patterns.',
    'convert-video': 'Convert video file(s) or patterns.',
}

aliases = {
    'ls-file': ['lsf'],
    'ls-dir': ['lsd'],
    'ls-block-size': ['ls-bs'],
    'du': ['disk'],
    'tar-compress': ['tar'],
    'tar-extract': ['untar'],
    'zip-compress': ['zip', 'zip-all'],
    'unzip-all': ['unzip'],
    'convert-video': ['convert-vid'],
}

alias_to_primary = {}
for primary, alias_list in aliases.items():
    for alias in alias_list:
        alias_to_primary[alias] = primary

# One-line usage examples for help output
command_usage = {
    'ls': 'cmd ls',
    'ls-all': 'cmd ls-all',
    'lsf': 'cmd lsf *.py',
    'ls-file': 'cmd ls-file report*',
    'lsd': 'cmd lsd',
    'ls-dir': 'cmd ls-dir',
    'ls-reverse': 'cmd ls-reverse',
    'ls-time': 'cmd ls-time',
    'ls-human': 'cmd ls-human',
    'ls-long': 'cmd ls-long',
    'ls-size': 'cmd ls-size',
    'ls-recursive': 'cmd ls-recursive',
    'ls-recursive-size': 'cmd ls-recursive-size',
    'ls-bs': 'cmd ls-bs M',
    'ls-block-size': 'cmd ls-block-size K',
    'ps': 'cmd ps',
    'ps-all': 'cmd ps-all',
    'ps-user': 'cmd ps-user alice',
    'ps-aux': 'cmd ps-aux',
    'ps-sort-memory': 'cmd ps-sort-memory',
    'ps-sort-cpu': 'cmd ps-sort-cpu',
    'ps-grep': 'cmd ps-grep python',
    'kill': 'cmd kill 1234',
    'df': 'cmd df',
    'du': 'cmd du /path',
    'disk': 'cmd disk /path',
    'rm': 'cmd rm ./tmp *.log',
    'grep': 'cmd grep \"TODO\" README.md',
    'tar': 'cmd tar ./src out.tar.gz',
    'tar-compress': 'cmd tar-compress ./src out.tar.gz',
    'untar': 'cmd untar archive.tar.gz ./out',
    'tar-extract': 'cmd tar-extract archive.tar ./out',
    'tar-list': 'cmd tar-list archive.tar',
    'tar-add': 'cmd tar-add file.txt archive.tar',
    'zip': 'cmd zip out.zip src1 src2',
    'zip-compress': 'cmd zip-compress out.zip src1',
    'zip-all': 'cmd zip-all out.zip src1',
    'unzip': 'cmd unzip ./zips ./out',
    'unzip-all': 'cmd unzip-all ./zips ./out',
    'convert-vid': 'cmd convert-vid \"*.mov\" ./out.mp4',
    'convert-video': 'cmd convert-video \"*.mov\" ./out.mp4',
}

# Optional detailed help per command
command_help_details = {
    'ls': {
        'usage': 'cmd ls [path]',
        'examples': [
            'cmd ls',
            'cmd ls ./src',
        ],
    },
    'ls-all': {
        'usage': 'cmd ls-all [path]',
        'examples': [
            'cmd ls-all',
            'cmd ls-all ./src',
        ],
    },
    'lsf': {
        'usage': 'cmd lsf [pattern]',
        'examples': [
            'cmd lsf',
            'cmd lsf *.py',
        ],
    },
    'ls-file': {
        'usage': 'cmd ls-file [pattern]',
        'examples': [
            'cmd ls-file',
            'cmd ls-file report*',
        ],
    },
    'lsd': {
        'usage': 'cmd lsd',
        'examples': [
            'cmd lsd',
        ],
    },
    'ls-dir': {
        'usage': 'cmd ls-dir',
        'examples': [
            'cmd ls-dir',
        ],
    },
    'ls-reverse': {
        'usage': 'cmd ls-reverse [path]',
        'examples': [
            'cmd ls-reverse',
            'cmd ls-reverse ./src',
        ],
    },
    'ls-time': {
        'usage': 'cmd ls-time [path]',
        'examples': [
            'cmd ls-time',
            'cmd ls-time ./src',
        ],
    },
    'ls-human': {
        'usage': 'cmd ls-human [path]',
        'examples': [
            'cmd ls-human',
            'cmd ls-human ./src',
        ],
    },
    'ls-long': {
        'usage': 'cmd ls-long [path]',
        'examples': [
            'cmd ls-long',
            'cmd ls-long ./src',
        ],
    },
    'ls-size': {
        'usage': 'cmd ls-size [path]',
        'examples': [
            'cmd ls-size',
            'cmd ls-size ./src',
        ],
    },
    'ls-recursive': {
        'usage': 'cmd ls-recursive [path]',
        'examples': [
            'cmd ls-recursive',
            'cmd ls-recursive ./src',
        ],
    },
    'ls-recursive-size': {
        'usage': 'cmd ls-recursive-size [path]',
        'examples': [
            'cmd ls-recursive-size',
            'cmd ls-recursive-size ./src',
        ],
    },
    'ls-bs': {
        'usage': 'cmd ls-bs <K|M|G>',
        'examples': [
            'cmd ls-bs M',
        ],
    },
    'ls-block-size': {
        'usage': 'cmd ls-block-size <K|M|G>',
        'examples': [
            'cmd ls-block-size K',
        ],
    },
    'ps': {
        'usage': 'cmd ps',
        'examples': [
            'cmd ps',
        ],
    },
    'ps-all': {
        'usage': 'cmd ps-all',
        'examples': [
            'cmd ps-all',
        ],
    },
    'ps-user': {
        'usage': 'cmd ps-user <username>',
        'examples': [
            'cmd ps-user alice',
        ],
    },
    'ps-aux': {
        'usage': 'cmd ps-aux',
        'examples': [
            'cmd ps-aux',
        ],
    },
    'ps-sort-memory': {
        'usage': 'cmd ps-sort-memory',
        'examples': [
            'cmd ps-sort-memory',
        ],
    },
    'ps-sort-cpu': {
        'usage': 'cmd ps-sort-cpu',
        'examples': [
            'cmd ps-sort-cpu',
        ],
    },
    'ps-grep': {
        'usage': 'cmd ps-grep <keyword>',
        'examples': [
            'cmd ps-grep python',
        ],
    },
    'kill': {
        'usage': 'cmd kill <pid|keyword> [--force|-9]',
        'examples': [
            'cmd kill 1234',
            'cmd kill python --force',
        ],
    },
    'df': {
        'usage': 'cmd df',
        'examples': [
            'cmd df',
        ],
    },
    'du': {
        'usage': 'cmd du [path]',
        'examples': [
            'cmd du',
            'cmd du /var/log',
        ],
    },
    'disk': {
        'usage': 'cmd disk [path]',
        'examples': [
            'cmd disk',
            'cmd disk /var/log',
        ],
    },
    'rm': {
        'usage': 'cmd rm <path> [patterns...]',
        'examples': [
            'cmd rm ./tmp',
            'cmd rm ./logs *.log *.tmp',
        ],
    },
    'grep': {
        'usage': 'cmd grep <pattern> <file>',
        'examples': [
            'cmd grep \"TODO\" README.md',
        ],
    },
    'tar': {
        'usage': 'cmd tar <source> <output.tar|output.tar.gz> [--exclude <pattern>...]',
        'examples': [
            'cmd tar ./src out.tar.gz',
            'cmd tar ./src out.tar --exclude node_modules --exclude *.log',
        ],
    },
    'tar-compress': {
        'usage': 'cmd tar-compress <source> <output.tar|output.tar.gz> [--exclude <pattern>...]',
        'examples': [
            'cmd tar-compress ./src out.tar.gz',
            'cmd tar-compress ./src out.tar --exclude node_modules',
        ],
    },
    'untar': {
        'usage': 'cmd untar <archive|dir> <dest> [tar|gz|all]',
        'examples': [
            'cmd untar archive.tar.gz ./out',
            'cmd untar ./archives ./out gz',
        ],
    },
    'tar-extract': {
        'usage': 'cmd tar-extract <archive|dir> <dest> [tar|gz|all]',
        'examples': [
            'cmd tar-extract archive.tar ./out',
            'cmd tar-extract ./archives ./out tar',
        ],
    },
    'tar-list': {
        'usage': 'cmd tar-list <archive.tar|archive.tar.gz>',
        'examples': [
            'cmd tar-list archive.tar',
        ],
    },
    'tar-add': {
        'usage': 'cmd tar-add <file> <archive.tar>',
        'examples': [
            'cmd tar-add file.txt archive.tar',
        ],
    },
    'zip': {
        'usage': 'cmd zip <output.zip> <source...>',
        'examples': [
            'cmd zip out.zip src1 src2',
            'cmd zip out.zip \"*.txt\"',
        ],
    },
    'zip-compress': {
        'usage': 'cmd zip-compress <output.zip> <source...>',
        'examples': [
            'cmd zip-compress out.zip ./src',
        ],
    },
    'zip-all': {
        'usage': 'cmd zip-all <output.zip> <source...>',
        'examples': [
            'cmd zip-all out.zip ./src',
        ],
    },
    'unzip': {
        'usage': 'cmd unzip <source_dir> <dest_dir>',
        'examples': [
            'cmd unzip ./zips ./out',
        ],
    },
    'unzip-all': {
        'usage': 'cmd unzip-all <source_dir> <dest_dir>',
        'examples': [
            'cmd unzip-all ./zips ./out',
        ],
    },
    'convert-vid': {
        'usage': 'cmd convert-vid <source|pattern> <dest|pattern>',
        'examples': [
            'cmd convert-vid input.mov output.mp4',
            'cmd convert-vid \"*.mov\" ./out.mp4',
        ],
    },
    'convert-video': {
        'usage': 'cmd convert-video <source|pattern> <dest|pattern>',
        'examples': [
            'cmd convert-video input.mov output.mp4',
            'cmd convert-video \"*.mov\" ./out.mp4',
        ],
    },
}


def custom_help():
    print("Usage: cmd|cli <command> [args...]")
    print("Tip: run cmd <command> -h for command-specific usage.")
    print("Note: cli is an alternate entrypoint with the same behavior.")
    print("")
    max_len = max(len(cmd) for cmd in commands)
    groups = [
        ("List & Count", [
            "ls", "ls-all", "lsf", "ls-file", "lsd", "ls-dir", "ls-reverse",
            "ls-time", "ls-human", "ls-long", "ls-size", "ls-recursive",
            "ls-recursive-size", "ls-bs", "ls-block-size",
        ]),
        ("Process", [
            "ps", "ps-all", "ps-user", "ps-aux", "ps-sort-memory",
            "ps-sort-cpu", "ps-grep", "kill",
        ]),
        ("Disk & Space", ["df", "du", "disk"]),
        ("Remove & Search", ["rm", "grep"]),
        ("Archive (tar)", ["tar", "tar-compress", "untar", "tar-extract", "tar-list", "tar-add"]),
        ("Archive (zip)", ["zip", "zip-compress", "zip-all", "unzip", "unzip-all"]),
        ("Video Convert", ["convert-vid", "convert-video"]),
    ]
    print("Commands:")
    for title, items in groups:
        print(f"{title}:")
        for command in items:
            description = commands.get(command)
            if description is None:
                continue
            usage = command_usage.get(command)
            alias_list = aliases.get(command)
            alias_suffix = f" ({', '.join(alias_list)})" if alias_list else ""
            alias_of = alias_to_primary.get(command)
            alias_of_suffix = f" (alias: {alias_of})" if alias_of else ""
            if usage:
                print(f"{command.ljust(max_len)}  {description}{alias_suffix}{alias_of_suffix}  e.g. {usage}")
            else:
                print(f"{command.ljust(max_len)}  {description}{alias_suffix}{alias_of_suffix}")
        print("")
    print(f"Project: {PROJECT_URL}")


def custom_command_help(command):
    primary = alias_to_primary.get(command, command)
    description = commands.get(primary, "No description available.")
    details = command_help_details.get(primary, {})
    usage = details.get('usage') or command_usage.get(primary, f"cmd {primary} [args...]")
    print(f"Usage: {usage}")
    print("Entrypoints: cmd, cli")
    print(f"About: {description}")
    alias_list = aliases.get(primary)
    if alias_list:
        print(f"Aliases: {', '.join(alias_list)}")
    if command != primary:
        print(f"Alias: {primary}")
    examples = details.get('examples')
    if examples:
        print("Examples:")
        for ex in examples:
            print(f"  {ex}")
    elif command in command_usage:
        print("Example:")
        print(f"  {command_usage[command]}")
    print("Note: arguments are passed to the underlying system command when applicable.")



def confirm_action(message):
    """Ask the user to confirm an action, accepting y/n or yes/no"""
    confirmation = input(f"{message} (yes/no or y/n): ").strip().lower()
    return confirmation in ['yes', 'y']


def run_cmd(cmd_args):
    """Run a command safely without invoking a shell."""
    try:
        subprocess.run(cmd_args, check=False)
    except FileNotFoundError:
        print(f"Command not found: {cmd_args[0]}")


def parse_excludes(args):
    excludes = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--exclude':
            if i + 1 < len(args):
                excludes.append(args[i + 1])
                i += 2
            else:
                break
        elif arg.startswith('--exclude='):
            excludes.append(arg.split('=', 1)[1])
            i += 1
        else:
            excludes.append(arg)
            i += 1
    return excludes


def expand_globs(args):
    expanded = []
    for arg in args:
        if any(ch in arg for ch in ['*', '?', '[']):
            matches = glob.glob(arg)
            if matches:
                expanded.extend(matches)
            else:
                expanded.append(arg)
        else:
            expanded.append(arg)
    return expanded


def list_files_in_dir(path):
    try:
        with os.scandir(path) as it:
            return [entry.name for entry in it]
    except FileNotFoundError:
        print(f"Path not found: {path}")
        return []


def count_dirs(root):
    try:
        return sum(1 for entry in os.scandir(root) if entry.is_dir(follow_symlinks=False))
    except FileNotFoundError:
        print(f"Path not found: {root}")
        return 0


def count_files(root, pattern=None):
    try:
        with os.scandir(root) as it:
            names = [entry.name for entry in it if entry.is_file(follow_symlinks=False)]
    except FileNotFoundError:
        print(f"Path not found: {root}")
        return 0
    if pattern is None:
        return len(names)
    if any(ch in pattern for ch in ['*', '?', '[']):
        return sum(1 for name in names if fnmatch(name, pattern))
    return sum(1 for name in names if pattern in name)


def filter_ps(keyword):
    try:
        result = subprocess.run(['ps', 'aux'], check=False, capture_output=True, text=True)
    except FileNotFoundError:
        print("Command not found: ps")
        return []
    lines = result.stdout.splitlines()
    matches = []
    for line in lines:
        if keyword in line and 'ps aux' not in line:
            matches.append(line)
    return matches


def kill_processes(target, force=False):
    sig = signal.SIGKILL if force else signal.SIGTERM
    if target.isdigit():
        try:
            os.kill(int(target), sig)
            print(f"Killed PID {target} with signal {sig}.")
        except ProcessLookupError:
            print(f"No such process: {target}")
        except PermissionError:
            print(f"Permission denied to kill PID {target}")
        return

    matches = filter_ps(target)
    if not matches:
        print(f"No processes found matching: {target}")
        return

    pids = []
    for line in matches:
        parts = line.split()
        if len(parts) >= 2 and parts[1].isdigit():
            pids.append(parts[1])

    if not pids:
        print(f"No processes found matching: {target}")
        return

    print("Matched processes:")
    for line in matches:
        print(line)

    if confirm_action(f"Kill {len(pids)} process(es) matching '{target}'?"):
        for pid in pids:
            try:
                os.kill(int(pid), sig)
            except ProcessLookupError:
                print(f"No such process: {pid}")
            except PermissionError:
                print(f"Permission denied to kill PID {pid}")
        print("Kill completed.")
    else:
        print("Operation canceled.")


def main():
    # Set up argparse
    parser = argparse.ArgumentParser(
        description="CLI Command Wrapper - Execute common Linux commands easily",
        epilog=f"Project page: {PROJECT_URL}",
        add_help=False
    )

    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-V', '--version', action='store_true', help='Show program\'s version number and exit')
    
    # Main command and subcommands
    subparsers = parser.add_subparsers(dest='command')
    for command, description in commands.items():
        subparser = subparsers.add_parser(command, help=description, add_help=False)
        subparser.add_argument('extra', nargs=argparse.REMAINDER, help='Additional arguments for the command')

    # Parse the arguments
    args, unknown = parser.parse_known_args()
    if unknown:
        if not hasattr(args, 'extra') or args.extra is None:
            args.extra = []
        args.extra.extend(unknown)

    if args.help:
        custom_help()
        return

    if args.version:
        print(f'cli-commands {VERSION}')
        return
    
    if args.command is None:
        custom_help()
        return

    if hasattr(args, 'extra') and args.extra:
        if '-h' in args.extra or '--help' in args.extra:
            custom_command_help(args.command)
            return

    ls_simple = {
        'ls': [],
        'ls-all': ['-a'],
        'ls-reverse': ['-r'],
        'ls-time': ['-lt'],
        'ls-long': ['-l'],
        'ls-human': ['-lh'],
        'ls-recursive': ['-R'],
        'ls-recursive-size': ['-lRh'],
        'ls-size': ['-lS'],
    }

    ps_simple = {
        'ps': [],
        'ps-all': ['-A'],
        'ps-aux': ['aux'],
        'ps-sort-memory': ['aux', '--sort=-%mem'],
        'ps-sort-cpu': ['aux', '--sort=-%cpu'],
    }

    # `ls` commands
    if args.command in ls_simple:
        run_cmd(['ls', *ls_simple[args.command], *expand_globs(args.extra)])

    # Advanced `ls` commands
    elif args.command == 'ls-dir' or args.command == 'lsd':
        # Count the number of directories
        print(count_dirs('.'))
    
    elif args.command == 'ls-file' or args.command == 'lsf':
        if len(args.extra) == 0:
            # Count the number of all files
            print(count_files('.'))
        else:
            # Count files of a specific type based on provided extension or pattern
            pattern = args.extra[0]  # First extra argument as file pattern
            print(count_files('.', pattern=pattern))
    
    elif args.command == 'ls-block-size' or args.command == 'ls-bs':
        # Display the size of each file in specified block size
        if len(args.extra) == 1:
            block_size = args.extra[0]
            run_cmd(['ls', f'--block-size={block_size}'])
        else:
            print('Please provide a valid block size (e.g., K, M, G).')
    
    # `ps` commands
    elif args.command in ps_simple:
        run_cmd(['ps', *ps_simple[args.command]])
    
    elif args.command == 'ps-user':
        # Show processes for a specific user
        if len(args.extra) > 0:
            user = args.extra[0]
            run_cmd(['ps', '-u', user])
        else:
            print('Please provide a username to show processes for that user')

    elif args.command == 'ps-grep':
        # Search for a specific process by name or keyword
        if len(args.extra) > 0:
            keyword = args.extra[0]
            matches = filter_ps(keyword)
            for line in matches:
                print(line)
        else:
            print('Please provide a keyword to search for in process list')

    # `kill` command
    elif args.command == 'kill':
        if len(args.extra) == 0:
            print('Please provide a process name or PID for kill command')
        else:
            force = False
            extras = list(args.extra)
            if '-9' in extras:
                extras.remove('-9')
                force = True
            if '--force' in extras:
                extras.remove('--force')
                force = True
            if len(extras) == 0:
                print('Please provide a process name or PID for kill command')
                return
            target = extras[0]
            kill_processes(target, force=force)

    # Disk usage and free space commands
    elif args.command == 'df':
        run_cmd(['df', '-h'])

    elif args.command == 'du' or args.command == 'disk':
        if len(args.extra) > 0:
            run_cmd(['du', '-sh', args.extra[0]])
        else:
            run_cmd(['du', '-sh', '.'])

    # Remove files or directories with confirmation and support for bulk removal
    elif args.command == 'rm':
        if len(args.extra) == 1:
            target = args.extra[0]
            if confirm_action(f"Are you sure you want to remove '{target}'?"):
                if os.path.isdir(target):
                    shutil.rmtree(target)
                elif os.path.isfile(target):
                    os.remove(target)
                else:
                    print(f"Path not found: {target}")
                    return
                print(f"'{target}' has been removed.")
            else:
                print(f"Operation canceled. '{target}' was not removed.")
        elif len(args.extra) > 1:
            path = args.extra[0]
            patterns = args.extra[1:]
            for pattern in patterns:
                files_to_remove = glob.glob(os.path.join(path, pattern))
                if files_to_remove:
                    print(f"Found {len(files_to_remove)} files to remove: {files_to_remove}")
                    if confirm_action(f"Are you sure you want to remove these files?"):
                        for file in files_to_remove:
                            if os.path.isdir(file):
                                shutil.rmtree(file)
                            elif os.path.isfile(file):
                                os.remove(file)
                        print(f"Removed files matching {pattern}.")
                    else:
                        print(f"Operation canceled for files matching {pattern}.")
                else:
                    print(f"No files found for pattern '{pattern}' in '{path}'.")

    # Search for a pattern in files or output
    elif args.command == 'grep':
        if len(args.extra) == 2:
            run_cmd(['grep', args.extra[0], args.extra[1]])
        else:
            print('Please provide a keyword and file path for grep command')

    # Tar compression and decompression
    elif args.command == 'tar-compress' or args.command == 'tar':
        if len(args.extra) >= 2:
            source = args.extra[0]
            output = args.extra[1]
            exclude = parse_excludes(args.extra[2:])  # Additional arguments as exclude patterns
            if output.endswith('.tar.gz'):
                run_cmd(['tar', '-czvf', output, *[f'--exclude={x}' for x in exclude], source])
            elif output.endswith('.tar'):
                run_cmd(['tar', '-cvf', output, *[f'--exclude={x}' for x in exclude], source])
            else:
                print('Unsupported output format. Please provide .tar or .tar.gz as the output file extension.')
        else:
            print('Please provide a source and output file for tar compression')

    elif args.command == 'tar-extract' or args.command == 'untar':
        if len(args.extra) >= 2:
            source = args.extra[0]
            destination = args.extra[1]
            file_type = args.extra[2] if len(args.extra) > 2 else "all"  # Optional file type filter

            if os.path.isdir(source):  # Check if source is a directory
                if file_type[-3:] == "tar":
                    tar_files = glob.glob(os.path.join(source, '*.tar'))
                elif file_type[-2:] == "gz":
                    tar_files = glob.glob(os.path.join(source, '*.tar.gz'))
                else:  # Extract all tar and tar.gz files
                    tar_files = glob.glob(os.path.join(source, '*.tar')) + glob.glob(os.path.join(source, '*.tar.gz'))

                for tar_file in tar_files:
                    if tar_file.endswith('.tar'):
                        run_cmd(['tar', '-xvf', tar_file, '-C', destination])
                    elif tar_file.endswith('.tar.gz'):
                        run_cmd(['tar', '-xzvf', tar_file, '-C', destination])
            # Extract a single tar file
            elif source.endswith('.tar.gz'):
                run_cmd(['tar', '-xzvf', source, '-C', destination])
            elif source.endswith('.tar'):
                run_cmd(['tar', '-xvf', source, '-C', destination])
            else:
                print('Please provide a valid .tar or .tar.gz file, or a directory containing such files.')



    elif args.command == 'tar-list':
        if len(args.extra) > 0:
            run_cmd(['tar', '-tvf', args.extra[0]])
        else:
            print('Please provide a tar file to list contents')

    elif args.command == 'tar-add':
        if len(args.extra) == 2:
            run_cmd(['tar', '-rvf', args.extra[1], args.extra[0]])
        else:
            print('Please provide a file to add and the target tar file')
    
    # Unzip
    elif args.command == 'unzip-all' or args.command == 'unzip':
        if len(args.extra) == 2:
            source_dir = args.extra[0]
            target_dir = args.extra[1]
            for root, _, files in os.walk(source_dir):
                for name in files:
                    if name.endswith('.zip'):
                        run_cmd(['unzip', os.path.join(root, name), '-d', target_dir])
        else:
            print('Please provide both a source and a target directory.')
    
    # Zip compress
    elif args.command == 'zip-all' or args.command == 'zip' or args.command == 'zip-compress':
        if len(args.extra) >= 2:
            output = args.extra[0]
            sources = expand_globs(args.extra[1:])  # All other arguments as sources to be zipped
            run_cmd(['zip', '-r', output, *sources])
        else:
            print('Please provide an output file name and at least one source to compress.')

    # ffmpeg
    elif args.command == 'convert-video' or args.command == 'convert-vid':
        if len(args.extra) == 2:
            source = args.extra[0]
            destination = args.extra[1]

            if '*' in source:
                # Handle wildcard batch conversion
                source_files = sorted(glob.glob(source))
                destination_dir = os.path.dirname(destination)
                file_extension = destination.split('.')[-1]

                for src_file in source_files:
                    basename = os.path.splitext(os.path.basename(src_file))[0]
                    dest_file = os.path.join(destination_dir, f'{basename}.{file_extension}')
                    run_cmd(['ffmpeg', '-i', src_file, '-c', 'copy', dest_file, '-y'])
            else:
                # Handle single file conversion
                run_cmd(['ffmpeg', '-i', source, '-c', 'copy', destination, '-y'])
        else:
            print('Usage: convert-video [source file or pattern] [destination file or pattern]')



if __name__ == '__main__':
    main()
