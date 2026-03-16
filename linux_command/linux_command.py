#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux Command Wrapper

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

For more information, visit the project page: https://github.com/MouxiaoHuang/linux-command
"""
import argparse
import glob
import os
import shutil
import signal
import subprocess
from fnmatch import fnmatch


# Define the version 
VERSION = "0.3.0"
PROJECT_URL = "https://github.com/MouxiaoHuang/linux-command" 


# Command descriptions
commands = {
    'ls': 'List contents.',
    'ls-all': 'List all files, including hidden ones.',
    'lsf': 'Count all files or filter by a specified pattern, extension or keyword. Same as `ls-file`.',
    'ls-file': 'Count all files or filter by a specified pattern, extension or keyword. Same as `lsf`.',
    'lsd': 'Count all directories. Same as `ls-dir`.',
    'ls-dir': 'Count all directories. Same as `lsd`.',
    'ls-reverse': 'List files and directories in reverse order.',
    'ls-time': 'List sorted by modification time, newest first.',
    'ls-human': 'List in human-readable format (for file sizes)',
    'ls-long': 'Long format listing',
    'ls-size': 'Sort files by size',
    'ls-recursive': 'Recursively list files in directories and subdirectories.',
    'ls-recursive-size': 'List all files and directories recursively, with sizes in human-readable format',
    'ls-bs': 'Display the size of each file in specified block size (e.g., K, M, G).',
    'ls-block-size': 'Display the size of each file in specified block size (e.g., K, M, G).',
    'ps': 'Basic process list.',
    'ps-all': 'Show all processes.',
    'ps-user': 'Show processes for a specific user',
    'ps-aux': 'Show detailed information about all processes.',
    'ps-sort-memory': 'Sort processes by memory usage.',
    'ps-sort-cpu': 'Sort processes by CPU usage.',
    'ps-grep': 'Search for a specific process by name or keyword.',
    'kill': 'Kill a process with PID or keyword in its name.',
    'df': 'Show disk usage.',
    'du': 'Show disk usage of a directory. Default: current directory.',
    'disk': 'Show disk usage of a directory. Default: current directory.',
    'rm': 'Remove file, directory, or multiple files by patterns (e.g., *.txt)',
    'grep': 'Search for a pattern in files or output.',
    'tar': 'Pack into .tar or .tar.gz file.',
    'tar-compress': 'Pack into .tar or .tar.gz file.',
    'untar': 'Unpack .tar or .tar.gz file, or batch process in a directory.',
    'tar-extract': 'Unpack .tar or .tar.gz file, or batch process in a directory.',
    'tar-list': 'List all contents in a tar file.',
    'tar-add': 'Add a file to a tar file.',
    'zip': 'Pack a folder to a .zip file.',
    'zip-compress': 'Pack a folder to a .zip file.',
    'zip-all': 'Pack a folder to a .zip file.',
    'unzip': 'Unpack all .zip files in a directory to another.',
    'unzip-all': 'Unpack all .zip files in a directory to another.',
    'convert-vid': 'Video pattern trans. Usage: convert-video [source file or pattern] [destination file or pattern]',
    'convert-video': 'Video pattern trans. Usage: convert-video [source file or pattern] [destination file or pattern]',
}


def custom_help():
    print("Available commands:")
    for command, description in commands.items():
        print(f'[{command}]: {description}')
    print(f"For more information, visit: {PROJECT_URL}")



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
        return os.listdir(path)
    except FileNotFoundError:
        print(f"Path not found: {path}")
        return []


def count_dirs(root):
    total = 0
    for _, dirs, _ in os.walk(root):
        total += len(dirs)
    return total


def count_files(root, pattern=None):
    files = [f for f in list_files_in_dir(root) if os.path.isfile(os.path.join(root, f))]
    if pattern is None:
        return len(files)
    if any(ch in pattern for ch in ['*', '?', '[']):
        return sum(1 for f in files if fnmatch(f, pattern))
    return sum(1 for f in files if pattern in f)


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
        description="Linux Command Wrapper - Execute common Linux commands easily",
        epilog=f"Project page: {PROJECT_URL}",
        add_help=False
    )

    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('-V', '--version', action='store_true', help='Show program\'s version number and exit')
    
    # Main command and subcommands
    subparsers = parser.add_subparsers(dest='command')
    for command, description in commands.items():
        subparser = subparsers.add_parser(command, help=description, add_help=True)
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
        print(f'linux-command {VERSION}')
        return
    
    if args.command is None:
        custom_help()
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
