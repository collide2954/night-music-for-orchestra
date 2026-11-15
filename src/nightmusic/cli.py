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


def build_audio(bars: tuple[int, int] | None = None) -> None:
    """Render the audio master, or an excerpt of it."""
    from .audio import mix
    from .work import build

    audio, report = mix.render(build(), bars=bars)
    name = "night-music" if bars is None else f"excerpt-{bars[0]}-{bars[1]}"
    for path in mix.write(audio, BUILD_DIR / "audio", name):
        print(f"audio: {path}")
    print(report)


def check_work() -> int:
    """Find music that a player cannot play. Return the number of problems."""
    from .compose.check import check
    from .work import build

    work = build()
    problems = check(work)
    for problem in problems:
        print(problem)
    seconds = work.structure.duration_seconds
    print(f"{len(work.structure.bars)} bars, {seconds / 60:.1f} minutes, {len(problems)} problems")
    return len(problems)


def build_video() -> None:
    """Render the score video. The audio master must exist."""
    from .video import pages, render
    from .work import build

    work = build()
    screens = pages.build_pages(work, BUILD_DIR / "video" / "pages")
    audio = BUILD_DIR / "audio" / "night-music.flac"
    path = render.render(work, screens, audio, BUILD_DIR / "video" / "night-music.mp4")
    print(f"video: {path}")


def show_stats() -> None:
    """Print the numbers of the work as a table."""
    from .compose.stats import measure
    from .work import build

    for name, value in measure(build()).rows():
        print(f"{name:45s} {value}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nightmusic", description="Build Night Music.")
    parser.add_argument(
        "command", choices=["check", "stats", "ly", "score", "parts", "audio", "video", "all"]
    )
    parser.add_argument(
        "--bars", metavar="FIRST-LAST", help="render only these bars (command: audio)"
    )
    args = parser.parse_args(argv)
    bars = None
    if args.bars:
        first, _, last = args.bars.partition("-")
        bars = (int(first), int(last or first))
    if args.command == "check":
        return 1 if check_work() else 0
    if args.command == "stats":
        show_stats()
        return 0
    if args.command == "ly":
        for path in write_lilypond():
            print(path)
    elif args.command == "score":
        build_pdfs(parts=False)
    elif args.command == "parts":
        build_pdfs(parts=True)
    elif args.command == "audio":
        build_audio(bars)
    elif args.command == "video":
        build_video()
    else:
        build_pdfs(parts=True)
        build_audio()
        build_video()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
