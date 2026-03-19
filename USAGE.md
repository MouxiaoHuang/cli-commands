# Command Usage

This document groups every supported command by function and links to detailed usage blocks below.

## Directory

List & Count: [ls](#cmd-ls) · [ls-all](#cmd-ls-all) · [ls-long](#cmd-ls-long) · [ls-human](#cmd-ls-human) · [ls-size](#cmd-ls-size) · [ls-recursive](#cmd-ls-recursive) · [ls-dir](#cmd-ls-dir) · [ls-file](#cmd-ls-file) · [ls-reverse](#cmd-ls-reverse) · [ls-time](#cmd-ls-time) · [ls-recursive-size](#cmd-ls-recursive-size) · [ls-block-size](#cmd-ls-block-size)

Process: [ps](#cmd-ps) · [ps-all](#cmd-ps-all) · [ps-user](#cmd-ps-user) · [ps-aux](#cmd-ps-aux) · [ps-sort-memory](#cmd-ps-sort-memory) · [ps-sort-cpu](#cmd-ps-sort-cpu) · [ps-grep](#cmd-ps-grep) · [kill](#cmd-kill)

Disk & Space: [df](#cmd-df) · [du](#cmd-du)

Remove & Search: [rm](#cmd-rm) · [grep](#cmd-grep)

Archive (tar): [tar-compress](#cmd-tar-compress) · [tar-extract](#cmd-tar-extract) · [tar-list](#cmd-tar-list) · [tar-add](#cmd-tar-add)

Archive (zip): [unzip-all](#cmd-unzip-all) · [zip-compress](#cmd-zip-compress)

Video Convert: [convert-video](#cmd-convert-video)

Aliases: [aliases](#aliases)

---

## Quick Find

- Need archives? Jump to **Archive (tar)** or **Archive (zip)**.
- Need processes? Jump to **Process**.
- Need disk usage? Jump to **Disk & Space**.
- Need cleanup or search? Jump to **Remove & Search**.

## List & Count

<a id="cmd-ls"></a>
### `ls` - List files in the current directory

```bash
cmd ls
```

<a id="cmd-ls-all"></a>
### `ls-all` - List all files, including hidden ones

```bash
cmd ls-all
```

<a id="cmd-ls-long"></a>
### `ls-long` - Long format listing

```bash
cmd ls-long
```

<a id="cmd-ls-human"></a>
### `ls-human` - List in human-readable format (file sizes)

```bash
cmd ls-human
```

<a id="cmd-ls-size"></a>
### `ls-size` - Sort files by size

```bash
cmd ls-size
```

<a id="cmd-ls-recursive"></a>
### `ls-recursive` - Recursively list files in directories and subdirectories

```bash
cmd ls-recursive
```

<a id="cmd-ls-dir"></a>
### `ls-dir` (`lsd`) - Count the number of directories

```bash
cmd ls-dir
```

<a id="cmd-ls-file"></a>
### `ls-file` (`lsf`) - Count the number of files

```bash
cmd ls-file
```

<a id="cmd-ls-reverse"></a>
### `ls-reverse` - List files and directories in reverse order

```bash
cmd ls-reverse
```

<a id="cmd-ls-time"></a>
### `ls-time` - Sort by modification time (newest first)

```bash
cmd ls-time
```

<a id="cmd-ls-recursive-size"></a>
### `ls-recursive-size` - List files and directories recursively with human-readable sizes

```bash
cmd ls-recursive-size
```

<a id="cmd-ls-block-size"></a>
### `ls-block-size` (`ls-bs`) - Display the size of each file in a specified block size (e.g., K, M, G)

```bash
cmd ls-block-size M
```

---

## Process

<a id="cmd-ps"></a>
### `ps` - Show running processes

```bash
cmd ps
```

<a id="cmd-ps-all"></a>
### `ps-all` - Show all processes

```bash
cmd ps-all
```

<a id="cmd-ps-user"></a>
### `ps-user [username]` - Show processes for a specific user

```bash
cmd ps-user username
```

<a id="cmd-ps-aux"></a>
### `ps-aux` - Show detailed information about all processes

```bash
cmd ps-aux
```

<a id="cmd-ps-sort-memory"></a>
### `ps-sort-memory` - Sort processes by memory usage

```bash
cmd ps-sort-memory
```

<a id="cmd-ps-sort-cpu"></a>
### `ps-sort-cpu` - Sort processes by CPU usage

```bash
cmd ps-sort-cpu
```

<a id="cmd-ps-grep"></a>
### `ps-grep [keyword]` - Search for a specific process by name or keyword

```bash
cmd ps-grep python
```

<a id="cmd-kill"></a>
### `kill [process_name_or_PID]` - Kill a process by name or PID

```bash
cmd kill process_name
```

To force kill:

```bash
cmd kill --force process_name
```

---

## Disk & Space

<a id="cmd-df"></a>
### `df` - Show disk usage in human-readable format

```bash
cmd df
```

<a id="cmd-du"></a>
### `du` (`disk`) [path] - Show disk usage for a specific file or directory (default: current directory)

```bash
cmd du /path/to/directory
```

---

## Remove & Search

<a id="cmd-rm"></a>
### `rm [file_or_directory]` - Remove a file or directory with confirmation

```bash
cmd rm /path/to/file_or_directory
```

### `rm [directory] [file_patterns...]` - Remove multiple files by pattern (e.g., *.txt)

```bash
cmd rm /path/to/directory *.txt *.log
```

<a id="cmd-grep"></a>
### `grep [pattern] [file]` - Search for a pattern in a file

```bash
cmd grep "search_term" /path/to/file
```

---

## Archive (tar)

<a id="cmd-tar-compress"></a>
### `tar-compress` (`tar`) [source directory] [output file] [--exclude file_or_directory ...] - Compress directories into `.tar` or `.tar.gz` while excluding specific files or folders

```bash
cmd tar-compress /path/to/source /path/to/output.tar.gz --exclude node_modules --exclude .git
```
This command will compress `/path/to/source` into `/path/to/output.tar.gz` and exclude the `node_modules` and `.git` directories.

<a id="cmd-tar-extract"></a>
### `tar-extract` (`untar`) [source] [destination directory] - Extract a single file or all `.tar`/`.tar.gz` files from a specified directory

- To extract a single `.tar` or `.tar.gz` file:

```bash
cmd tar-extract /path/to/archive.tar.gz /path/to/destination
```

- To extract all `.tar` and `.tar.gz` files within a directory (default: all):

```bash
cmd tar-extract /path/to/directory /path/to/destination all
```

- To extract all `.tar` files within a directory:

```bash
cmd tar-extract /path/to/directory /destination/path tar
```

- To extract all `.tar.gz` files within a directory:

```bash
cmd tar-extract /path/to/directory /destination/path gz
```

<a id="cmd-tar-list"></a>
### `tar-list [archive]` - List contents of a `.tar` or `.tar.gz` archive

```bash
cmd tar-list archive.tar.gz
```

<a id="cmd-tar-add"></a>
### `tar-add [file] [archive]` - Add a file to an existing `.tar` archive

```bash
cmd tar-add newfile.txt archive.tar
```

---

## Archive (zip)

<a id="cmd-unzip-all"></a>
### `unzip-all` (`unzip`) [source directory] [target directory] - Extract all `.zip` files found in a specified directory into a target directory

```bash
cmd unzip-all /path/to/zips /path/to/extract
```
This command will find all `.zip` files in `/path/to/zips` and extract each into `/path/to/extract`.

<a id="cmd-zip-compress"></a>
### `zip-compress` (`zip`, `zip-all`) [output file.zip] [directory or file ...] - Create a `.zip` file that includes multiple specified directories or files

```bash
cmd zip-compress /path/to/output.zip /path/to/dir1 /path/to/dir2
```
This command will create a `.zip` file at `/path/to/output.zip` that contains everything in `/path/to/dir1` and `/path/to/dir2`.

---

## Video Convert

<a id="cmd-convert-video"></a>
### `convert-video` (`convert-vid`) [source file or pattern] [destination file or pattern] - Convert video file(s) or patterns

```bash
cmd convert-video "*.mov" ./out.mp4
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
