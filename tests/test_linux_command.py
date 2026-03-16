import builtins
import signal
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import linux_command.linux_command as lc


class RunSpy:
    def __init__(self):
        self.calls = []

    def __call__(self, cmd_args, check=False, **kwargs):
        # Mimic subprocess.run signature used in code.
        self.calls.append(list(cmd_args))
        class Result:
            stdout = ""
        return Result()


class RunCmdSpy:
    def __init__(self):
        self.calls = []

    def __call__(self, cmd_args):
        self.calls.append(list(cmd_args))


def run_main_with_args(monkeypatch, argv, run_spy=None):
    monkeypatch.setattr(sys, "argv", ["cmd", *argv])
    if run_spy is not None:
        monkeypatch.setattr(lc.subprocess, "run", run_spy)
    lc.main()


def test_ls_and_ls_all(monkeypatch):
    run_spy = RunSpy()
    run_main_with_args(monkeypatch, ["ls"], run_spy)
    run_main_with_args(monkeypatch, ["ls-all"], run_spy)
    assert run_spy.calls[0] == ["ls"]
    assert run_spy.calls[1] == ["ls", "-a"]


def test_ls_variants(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    for cmd, expected in [
        ("ls-reverse", ["ls", "-r"]),
        ("ls-time", ["ls", "-lt"]),
        ("ls-long", ["ls", "-l"]),
        ("ls-human", ["ls", "-lh"]),
        ("ls-recursive", ["ls", "-R"]),
        ("ls-recursive-size", ["ls", "-lRh"]),
        ("ls-size", ["ls", "-lS"]),
    ]:
        run_main_with_args(monkeypatch, [cmd])
        assert run_cmd_spy.calls[-1] == expected


def test_ls_block_size_ok(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["ls-block-size", "M"])
    assert run_cmd_spy.calls[0] == ["ls", "--block-size=M"]


def test_ls_block_size_missing_arg(monkeypatch, capsys):
    run_spy = RunSpy()
    run_main_with_args(monkeypatch, ["ls-block-size"], run_spy)
    out = capsys.readouterr().out
    assert "Please provide a valid block size" in out


def test_ps_user(monkeypatch):
    run_spy = RunSpy()
    run_main_with_args(monkeypatch, ["ps-user", "root"], run_spy)
    assert run_spy.calls[0] == ["ps", "-u", "root"]


def test_ps_variants(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    for cmd, expected in [
        ("ps", ["ps"]),
        ("ps-all", ["ps", "-A"]),
        ("ps-aux", ["ps", "aux"]),
        ("ps-sort-memory", ["ps", "aux", "--sort=-%mem"]),
        ("ps-sort-cpu", ["ps", "aux", "--sort=-%cpu"]),
    ]:
        run_main_with_args(monkeypatch, [cmd])
        assert run_cmd_spy.calls[-1] == expected


def test_ps_grep_filters(monkeypatch, capsys):
    def fake_run(cmd_args, check=False, capture_output=False, text=False):
        class Result:
            stdout = "root 1 0.0 0.1 ? Ss 00:00 python\nuser 2 0.0 0.1 ? Ss 00:00 bash\n"
        return Result()

    monkeypatch.setattr(lc.subprocess, "run", fake_run)
    run_main_with_args(monkeypatch, ["ps-grep", "python"])
    out = capsys.readouterr().out
    assert "python" in out
    assert "bash" not in out


def test_kill_pid(monkeypatch, capsys):
    killed = []

    def fake_kill(pid, sig):
        killed.append((pid, sig))

    monkeypatch.setattr(lc.os, "kill", fake_kill)
    run_main_with_args(monkeypatch, ["kill", "1234"])
    assert killed == [(1234, signal.SIGTERM)]


def test_kill_force_pid(monkeypatch):
    killed = []

    def fake_kill(pid, sig):
        killed.append((pid, sig))

    monkeypatch.setattr(lc.os, "kill", fake_kill)
    run_main_with_args(monkeypatch, ["kill", "--force", "999"])
    assert killed == [(999, signal.SIGKILL)]


def test_kill_name_confirm(monkeypatch, capsys):
    def fake_run(cmd_args, check=False, capture_output=False, text=False):
        class Result:
            stdout = "root 10 0.0 0.1 ? Ss 00:00 myproc\n"
        return Result()

    killed = []

    def fake_kill(pid, sig):
        killed.append((pid, sig))

    monkeypatch.setattr(lc.subprocess, "run", fake_run)
    monkeypatch.setattr(lc.os, "kill", fake_kill)
    monkeypatch.setattr(builtins, "input", lambda _: "y")
    run_main_with_args(monkeypatch, ["kill", "myproc"])
    assert killed == [(10, signal.SIGTERM)]


def test_du_default(monkeypatch):
    run_spy = RunSpy()
    run_main_with_args(monkeypatch, ["du"], run_spy)
    assert run_spy.calls[0] == ["du", "-sh", "."]


def test_disk_alias(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["disk", "/tmp"])
    assert run_cmd_spy.calls[0] == ["du", "-sh", "/tmp"]


def test_rm_single_file(monkeypatch, tmp_path):
    target = tmp_path / "a.txt"
    target.write_text("x")
    monkeypatch.setattr(builtins, "input", lambda _: "y")
    run_main_with_args(monkeypatch, ["rm", str(target)])
    assert not target.exists()


def test_rm_pattern(monkeypatch, tmp_path):
    (tmp_path / "a.log").write_text("x")
    (tmp_path / "b.log").write_text("x")
    (tmp_path / "c.txt").write_text("x")
    monkeypatch.setattr(builtins, "input", lambda _: "y")
    run_main_with_args(monkeypatch, ["rm", str(tmp_path), "*.log"])
    assert not (tmp_path / "a.log").exists()
    assert not (tmp_path / "b.log").exists()
    assert (tmp_path / "c.txt").exists()


def test_expand_globs(tmp_path):
    (tmp_path / "x.txt").write_text("x")
    (tmp_path / "y.txt").write_text("x")
    args = [str(tmp_path / "*.txt")]
    expanded = lc.expand_globs(args)
    assert len(expanded) == 2


def test_ls_dir_and_ls_file(monkeypatch, tmp_path, capsys):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.log").write_text("x")
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    monkeypatch.chdir(tmp_path)

    run_main_with_args(monkeypatch, ["ls-dir"])
    out = capsys.readouterr().out.strip()
    assert out == "2"

    run_main_with_args(monkeypatch, ["ls-file"])
    out = capsys.readouterr().out.strip()
    assert out == "2"

    run_main_with_args(monkeypatch, ["lsf", "*.log"])
    out = capsys.readouterr().out.strip()
    assert out == "1"

    run_main_with_args(monkeypatch, ["lsd"])
    out = capsys.readouterr().out.strip()
    assert out == "2"


def test_grep_command(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["grep", "needle", "file.txt"])
    assert run_cmd_spy.calls[0] == ["grep", "needle", "file.txt"]


def test_tar_compress(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["tar-compress", "src", "out.tar"])
    run_main_with_args(monkeypatch, ["tar", "src", "out.tar.gz", "--exclude", "node_modules"])
    assert run_cmd_spy.calls[0] == ["tar", "-cvf", "out.tar", "src"]
    assert run_cmd_spy.calls[1] == ["tar", "-czvf", "out.tar.gz", "--exclude=node_modules", "src"]


def test_tar_compress_bad_ext(monkeypatch, capsys):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["tar-compress", "src", "out.zip"])
    out = capsys.readouterr().out
    assert "Unsupported output format" in out


def test_tar_extract_single(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["tar-extract", "a.tar.gz", "dest"])
    run_main_with_args(monkeypatch, ["untar", "b.tar", "dest"])
    assert run_cmd_spy.calls[0] == ["tar", "-xzvf", "a.tar.gz", "-C", "dest"]
    assert run_cmd_spy.calls[1] == ["tar", "-xvf", "b.tar", "-C", "dest"]


def test_tar_extract_dir(monkeypatch, tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.tar").write_text("x")
    (src / "b.tar.gz").write_text("x")
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["tar-extract", str(src), str(tmp_path / "dest"), "all"])
    assert run_cmd_spy.calls[0] == ["tar", "-xvf", str(src / "a.tar"), "-C", str(tmp_path / "dest")]
    assert run_cmd_spy.calls[1] == ["tar", "-xzvf", str(src / "b.tar.gz"), "-C", str(tmp_path / "dest")]


def test_tar_list_and_add(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["tar-list", "a.tar"])
    run_main_with_args(monkeypatch, ["tar-add", "file.txt", "a.tar"])
    assert run_cmd_spy.calls[0] == ["tar", "-tvf", "a.tar"]
    assert run_cmd_spy.calls[1] == ["tar", "-rvf", "a.tar", "file.txt"]


def test_unzip_all(monkeypatch, tmp_path):
    src = tmp_path / "zips"
    src.mkdir()
    (src / "a.zip").write_text("x")
    (src / "b.txt").write_text("x")
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["unzip-all", str(src), str(tmp_path / "out")])
    assert run_cmd_spy.calls[0] == ["unzip", str(src / "a.zip"), "-d", str(tmp_path / "out")]


def test_zip_commands(monkeypatch, tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("x")
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["zip", "out.zip", str(tmp_path / "*.txt")])
    run_main_with_args(monkeypatch, ["zip-compress", "out.zip", str(tmp_path / "a.txt")])
    assert run_cmd_spy.calls[0][0:3] == ["zip", "-r", "out.zip"]
    assert run_cmd_spy.calls[1] == ["zip", "-r", "out.zip", str(tmp_path / "a.txt")]


def test_convert_video_single(monkeypatch):
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["convert-video", "a.mp4", "b.mkv"])
    assert run_cmd_spy.calls[0] == ["ffmpeg", "-i", "a.mp4", "-c", "copy", "b.mkv", "-y"]


def test_convert_video_wildcard(monkeypatch, tmp_path):
    src_dir = tmp_path / "src"
    out_dir = tmp_path / "out"
    src_dir.mkdir()
    out_dir.mkdir()
    (src_dir / "a.mp4").write_text("x")
    (src_dir / "b.mp4").write_text("x")
    run_cmd_spy = RunCmdSpy()
    monkeypatch.setattr(lc, "run_cmd", run_cmd_spy)
    run_main_with_args(monkeypatch, ["convert-vid", str(src_dir / "*.mp4"), str(out_dir / "out.mkv")])
    assert run_cmd_spy.calls[0] == ["ffmpeg", "-i", str(src_dir / "a.mp4"), "-c", "copy", str(out_dir / "a.mkv"), "-y"]
    assert run_cmd_spy.calls[1] == ["ffmpeg", "-i", str(src_dir / "b.mp4"), "-c", "copy", str(out_dir / "b.mkv"), "-y"]
