"""Engrave one part: a fast check of its layout.

Use: uv run python tools/one_part.py PART OUTPUT_DIRECTORY   (PART is for example vn1 or pno)
"""

import subprocess
import sys
import time
from pathlib import Path

from nightmusic.notation import lilypond
from nightmusic.work import build

part, output = sys.argv[1], Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)
source = output / f"part-{part}.ly"
source.write_text(lilypond.part_file(build(), part), encoding="utf-8")
start = time.time()
result = subprocess.run(
    ["lilypond", "-dno-point-and-click", "--loglevel=WARNING", "-o",
     str(output / f"part-{part}"), str(source)],
    capture_output=True, text=True, check=False,
)  # fmt: skip
print(f"LilyPond: {time.time() - start:.0f} s, exit {result.returncode}")
print(result.stderr[-2500:])
