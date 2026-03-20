# Command Usage

This document groups every supported command by function and links to detailed usage blocks below.

## Directory

List & Count: [ls](#cli-ls) · [ls-all](#cli-ls-all) · [ls-long](#cli-ls-long) · [ls-human](#cli-ls-human) · [ls-size](#cli-ls-size) · [ls-recursive](#cli-ls-recursive) · [ls-dir](#cli-ls-dir) · [ls-file](#cli-ls-file) · [ls-reverse](#cli-ls-reverse) · [ls-time](#cli-ls-time) · [ls-recursive-size](#cli-ls-recursive-size) · [ls-block-size](#cli-ls-block-size)

Process: [ps](#cli-ps) · [ps-all](#cli-ps-all) · [ps-user](#cli-ps-user) · [ps-aux](#cli-ps-aux) · [ps-sort-memory](#cli-ps-sort-memory) · [ps-sort-cpu](#cli-ps-sort-cpu) · [ps-grep](#cli-ps-grep) · [kill](#cli-kill)

Disk & Space: [df](#cli-df) · [du](#cli-du)

Remove & Search: [rm](#cli-rm) · [grep](#cli-grep)

Archive (tar): [tar-compress](#cli-tar-compress) · [tar-extract](#cli-tar-extract) · [tar-list](#cli-tar-list) · [tar-add](#cli-tar-add)

Archive (zip): [unzip-all](#cli-unzip-all) · [zip-compress](#cli-zip-compress)

Video Convert: [convert-video](#cli-convert-video)

Aliases: [aliases](#aliases)

---

## Quick Find

- Need archives? Jump to **Archive (tar)** or **Archive (zip)**.
- Need processes? Jump to **Process**.
- Need disk usage? Jump to **Disk & Space**.
- Need cleanup or search? Jump to **Remove & Search**.

## List & Count

<a id="cli-ls"></a>
### `ls` - List files in the current directory

```bash
cli ls
```

<a id="cli-ls-all"></a>
### `ls-all` - List all files, including hidden ones

```bash
cli ls-all
```

<a id="cli-ls-long"></a>
### `ls-long` - Long format listing

```bash
cli ls-long
```

<a id="cli-ls-human"></a>
### `ls-human` - List in human-readable format (file sizes)

```bash
cli ls-human
```

<a id="cli-ls-size"></a>
### `ls-size` - Sort files by size

```bash
cli ls-size
```

<a id="cli-ls-recursive"></a>
### `ls-recursive` - Recursively list files in directories and subdirectories

```bash
cli ls-recursive
```

<a id="cli-ls-dir"></a>
### `ls-dir` (`lsd`) - Count the number of directories

```bash
cli ls-dir
```

<a id="cli-ls-file"></a>
### `ls-file` (`lsf`) - Count the number of files

```bash
cli ls-file
```

<a id="cli-ls-reverse"></a>
### `ls-reverse` - List files and directories in reverse order

```bash
cli ls-reverse
```

<a id="cli-ls-time"></a>
### `ls-time` - Sort by modification time (newest first)

```bash
cli ls-time
```

<a id="cli-ls-recursive-size"></a>
### `ls-recursive-size` - List files and directories recursively with human-readable sizes

```bash
cli ls-recursive-size
```

<a id="cli-ls-block-size"></a>
### `ls-block-size` (`ls-bs`) - Display the size of each file in a specified block size (e.g., K, M, G)

```bash
cli ls-block-size M
```

---

## Process

<a id="cli-ps"></a>
### `ps` - Show running processes

```bash
cli ps
```

<a id="cli-ps-all"></a>
### `ps-all` - Show all processes

```bash
cli ps-all
```

<a id="cli-ps-user"></a>
### `ps-user [username]` - Show processes for a specific user

```bash
cli ps-user username
```

<a id="cli-ps-aux"></a>
### `ps-aux` - Show detailed information about all processes

```bash
cli ps-aux
```

<a id="cli-ps-sort-memory"></a>
### `ps-sort-memory` - Sort processes by memory usage

```bash
cli ps-sort-memory
```

<a id="cli-ps-sort-cpu"></a>
### `ps-sort-cpu` - Sort processes by CPU usage

```bash
cli ps-sort-cpu
```

<a id="cli-ps-grep"></a>
### `ps-grep [keyword]` - Search for a specific process by name or keyword

```bash
cli ps-grep python
```

<a id="cli-kill"></a>
### `kill [process_name_or_PID]` - Kill a process by name or PID

```bash
cli kill process_name
```

To force kill:

```bash
cli kill --force process_name
```

---

## Disk & Space

<a id="cli-df"></a>
### `df` - Show disk usage in human-readable format

```bash
cli df
```

<a id="cli-du"></a>
### `du` (`disk`) [path] - Show disk usage for a specific file or directory (default: current directory)

```bash
cli du /path/to/directory
```

---

## Remove & Search

<a id="cli-rm"></a>
### `rm [file_or_directory]` - Remove a file or directory with confirmation

```bash
cli rm /path/to/file_or_directory
```

### `rm [directory] [file_patterns...]` - Remove multiple files by pattern (e.g., *.txt)

```bash
cli rm /path/to/directory *.txt *.log
```

<a id="cli-grep"></a>
### `grep [pattern] [file]` - Search for a pattern in a file

```bash
cli grep "search_term" /path/to/file
```

---

## Archive (tar)

<a id="cli-tar-compress"></a>
### `tar-compress` (`tar`) [source directory] [output file] [--exclude file_or_directory ...] - Compress directories into `.tar` or `.tar.gz` while excluding specific files or folders

```bash
cli tar-compress /path/to/source /path/to/output.tar.gz --exclude node_modules --exclude .git
```
This command will compress `/path/to/source` into `/path/to/output.tar.gz` and exclude the `node_modules` and `.git` directories.

<a id="cli-tar-extract"></a>
### `tar-extract` (`untar`) [source] [destination directory] - Extract a single file or all `.tar`/`.tar.gz` files from a specified directory

- To extract a single `.tar` or `.tar.gz` file:

```bash
cli tar-extract /path/to/archive.tar.gz /path/to/destination
```

- To extract all `.tar` and `.tar.gz` files within a directory (default: all):

```bash
cli tar-extract /path/to/directory /path/to/destination all
```

- To extract all `.tar` files within a directory:

```bash
cli tar-extract /path/to/directory /destination/path tar
```

- To extract all `.tar.gz` files within a directory:

```bash
cli tar-extract /path/to/directory /destination/path gz
```

<a id="cli-tar-list"></a>
### `tar-list [archive]` - List contents of a `.tar` or `.tar.gz` archive

```bash
cli tar-list archive.tar.gz
```

<a id="cli-tar-add"></a>
### `tar-add [file] [archive]` - Add a file to an existing `.tar` archive

```bash
cli tar-add newfile.txt archive.tar
```

---

## Archive (zip)

<a id="cli-unzip-all"></a>
### `unzip-all` (`unzip`) [source directory] [target directory] - Extract all `.zip` files found in a specified directory into a target directory

```bash
cli unzip-all /path/to/zips /path/to/extract
```
This command will find all `.zip` files in `/path/to/zips` and extract each into `/path/to/extract`.

<a id="cli-zip-compress"></a>
### `zip-compress` (`zip`, `zip-all`) [output file.zip] [directory or file ...] - Create a `.zip` file that includes multiple specified directories or files

```bash
cli zip-compress /path/to/output.zip /path/to/dir1 /path/to/dir2
```
This command will create a `.zip` file at `/path/to/output.zip` that contains everything in `/path/to/dir1` and `/path/to/dir2`.

---

## Video Convert

<a id="cli-convert-video"></a>
### `convert-video` (`convert-vid`) [source file or pattern] [destination file or pattern] - Convert video file(s) or patterns

```bash
cli convert-video "*.mov" ./out.mp4
```

---

## Aliases

These commands are aliases for the same behavior:

- `lsf` = `ls-file`
- `lsd` = `ls-dir`
- `ls-bs` = `ls-block-size`
- `disk` = `du`
- `tar` = `tar-compress`
- `untar` = `tar-extract`
- `zip` = `zip-compress`
- `zip-all` = `zip-compress`
- `unzip` = `unzip-all`
- `convert-vid` = `convert-video`
