"""Command line interface: build the score, the parts, the audio, and the video."""

from __future__ import annotations

import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

BUILD_DIR = Path("build")


def write_lilypond() -> list[Path]:
    """Write the LilyPond files of the score and the parts."""
    from .notation import lilypond
    from .work import build

    return lilypond.write_all(build(), BUILD_DIR / "ly")


def compile_pdf(path: Path, output: Path) -> None:
    """Compile one LilyPond file into a PDF file in the output directory."""
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["lilypond", "-dno-point-and-click", "--loglevel=WARNING", "-o", str(output / path.stem),
         str(path)],
        capture_output=True,
        text=True,
        check=False,
    )  # fmt: skip
    if result.returncode != 0:
        raise RuntimeError(f"LilyPond failed for {path}:\n{result.stderr[-2000:]}")
    for line in result.stderr.splitlines():
        if "warning" in line and "compress" not in line:
            print(f"{path.name}: {line}")


def build_pdfs(*, parts: bool = True) -> None:
    """Build the score PDF and the part PDFs."""
    paths = write_lilypond()
    score = [path for path in paths if path.name == "score.ly"]
    others = [path for path in paths if path.name != "score.ly"] if parts else []
    compile_pdf(score[0], BUILD_DIR / "score")
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        list(pool.map(lambda path: compile_pdf(path, BUILD_DIR / "parts"), others))


def build_audio() -> None:
    """Render the audio master."""
    from .audio import mix
    from .work import build

    audio, report = mix.render(build())
    for path in mix.write(audio, BUILD_DIR / "audio"):
        print(f"audio: {path}")
    print(report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nightmusic", description="Build Night Music.")
    parser.add_argument("command", choices=["ly", "score", "parts", "audio", "all"])
    args = parser.parse_args(argv)
    if args.command == "ly":
        for path in write_lilypond():
            print(path)
    elif args.command == "score":
        build_pdfs(parts=False)
    elif args.command == "parts":
        build_pdfs(parts=True)
    elif args.command == "audio":
        build_audio()
    else:
        build_pdfs(parts=True)
        build_audio()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
