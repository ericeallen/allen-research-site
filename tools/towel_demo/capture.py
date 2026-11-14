"""Run Towel on the example and record exactly what a terminal shows.

    python tools/towel_demo/capture.py

Needs `towel` on PATH (pip install "code-towel[format,types]"). Writes
capture.json, which the recorder turns into the video, and the transcript the
site publishes beside the video. Nothing here is typed by hand: the video shows
this run's output and waits this run's time.
"""

from __future__ import annotations

import json
import os
import pty
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Final

HERE: Final = Path(__file__).resolve().parent
EXAMPLE: Final = HERE / "example" / "accounts.py"
CAPTURE: Final = HERE / "capture.json"
TRANSCRIPT: Final = HERE.parent.parent / "static" / "demo" / "towel-preview.txt"
COMMAND: Final = ("towel", "preview", ".", "--progress", "none")
TIMED_RUNS: Final = 3


def run_in_terminal(command: tuple[str, ...], cwd: Path) -> tuple[str, float]:
    """Run `command` under a pseudo-terminal; return what it printed and how long it took."""
    chunks: list[bytes] = []

    def read(fd: int) -> bytes:
        data = os.read(fd, 65536)
        chunks.append(data)
        return data

    previous = Path.cwd()
    os.chdir(cwd)
    try:
        start = time.monotonic()
        status = pty.spawn(list(command), read)
        seconds = time.monotonic() - start
    finally:
        os.chdir(previous)
    code = os.waitstatus_to_exitcode(status)
    if code != 0:
        raise RuntimeError(f"{' '.join(command)} exited with status {code}")
    return b"".join(chunks).decode("utf-8").replace("\r\n", "\n"), seconds


def main() -> int:
    if shutil.which(COMMAND[0]) is None:
        print('towel is not on PATH; pip install "code-towel[format,types]"', file=sys.stderr)
        return 2
    version = subprocess.run(
        [COMMAND[0], "--version"], check=True, capture_output=True, text=True
    ).stdout.strip()
    source = EXAMPLE.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as scratch:
        project = Path(scratch) / "project"
        project.mkdir()
        shutil.copy(EXAMPLE, project / EXAMPLE.name)
        # pty.spawn copies the child's output to our stdout; keep the console quiet.
        with Path(os.devnull).open("w") as quiet:
            saved = os.dup(1)
            os.dup2(quiet.fileno(), 1)
            try:
                runs = [run_in_terminal(COMMAND, project) for _ in range(TIMED_RUNS)]
            finally:
                os.dup2(saved, 1)
                os.close(saved)
        if (project / EXAMPLE.name).read_text(encoding="utf-8") != source:
            raise RuntimeError("towel preview changed the input file")

    outputs = {output for output, _ in runs}
    if len(outputs) != 1:
        raise RuntimeError("towel preview printed different output on repeated runs")
    (output,) = outputs
    if "\x1b" in output or "\r" in output:
        raise RuntimeError("the output holds terminal control codes the recorder does not draw")
    seconds = round(statistics.median(elapsed for _, elapsed in runs), 1)

    command = " ".join(COMMAND)
    capture = {
        "version": version,
        "file": EXAMPLE.name,
        "source": source,
        "command": command,
        "seconds": seconds,
        "output": output,
    }
    CAPTURE.write_text(json.dumps(capture, indent=2) + "\n", encoding="utf-8")
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT.write_text(
        f"Transcript of the Towel demo video ({version}).\n"
        f"The command took {seconds} seconds.\n\n"
        f"$ cat {EXAMPLE.name}\n{source}\n"
        f"$ {command}\n{output}",
        encoding="utf-8",
    )
    print(f"{version}: captured {len(output.splitlines())} lines in {seconds} s (median of {TIMED_RUNS})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
