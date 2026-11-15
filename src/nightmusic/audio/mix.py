"""The mixer: put all players on the stage, add the hall, and make the master file."""

from __future__ import annotations

import multiprocessing
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyloudnorm
import soundfile

from ..notation.work import Work
from ..perform.events import perform
from . import dsp, sampler, space

TAIL_SECONDS = 6.0  # time after the last bar for the reverberation
SEGMENT_SECONDS = 40.0  # the render divides the work into segments of this length
SEGMENT_LEAD = 1.0  # time before a segment, for notes that start early (grace notes)
MAX_WORKERS = 8  # largest number of parallel processes
CACHE_BYTES = 4_000_000_000  # memory for samples, for all processes together
REVERB_GAIN_DB = -9.0  # level of the hall reverberation relative to the direct sound
TARGET_LUFS = -20.0  # integrated loudness of the master
PEAK_LIMIT_DB = -1.0  # largest permitted sample peak


@dataclass
class MixReport:
    """Numbers that describe the master."""

    seconds: float
    loudness_lufs: float
    peak_db: float
    gain_db: float
    players: int


# The data of the present render. The worker processes get it when they start.
_JOB: dict = {}


def _render_segment(window: tuple[float, float]) -> tuple[int, np.ndarray]:
    """Render the notes that start in one time window. Return the first sample and the sound."""
    first = max(0, int(round((window[0] - SEGMENT_LEAD) * dsp.RATE)))
    stage = space.Stage()
    for player_id, prepared in _JOB["players"]:
        for group, stem in enumerate(sampler.render_player(prepared, window, first)):
            stage.add(stem, space.seat_of(player_id, group))
    return first, stage.mix(dsp.db(REVERB_GAIN_DB))


def render(
    work: Work,
    *,
    players: list[str] | None = None,
    bars: tuple[int, int] | None = None,
    workers: int | None = None,
) -> tuple[np.ndarray, MixReport]:
    """Render the work. Return the two-channel master and its report.

    `players` gives the players that play (default: all). `bars` gives the
    first and the last bar of an excerpt (default: the full work).

    The function divides the time into segments and renders the segments in
    parallel processes. The sum of the segments is the same as one render of
    the full time, because each note is independent of the other notes.
    """
    structure = work.structure
    begin, end = 0.0, structure.duration_seconds
    if bars is not None:
        begin = structure.seconds(structure.bar(bars[0]).start)
        end = structure.seconds(structure.bar(bars[1]).end)
    prepared = []
    for player in work.orchestra.players:
        if players is not None and player.id not in players:
            continue
        entry = sampler.prepare(perform(work, player.id), structure)
        if entry is not None and np.any((entry.starts >= begin) & (entry.starts < end)):
            prepared.append((player.id, entry))

    count = max(1, int(np.ceil((end - begin) / SEGMENT_SECONDS)))
    edges = np.linspace(begin, end, count + 1)
    edges[-1] = end + 1.0  # a note at the last moment is in the last segment
    windows = [(float(a), float(b)) for a, b in zip(edges[:-1], edges[1:], strict=True)]
    workers = max(1, min(workers or os.cpu_count() or 1, MAX_WORKERS, len(windows)))

    first_sample = max(0, int(round((begin - SEGMENT_LEAD) * dsp.RATE))) if bars else 0
    length = int(np.ceil((end + TAIL_SECONDS) * dsp.RATE)) - first_sample
    mix = np.zeros((length, 2), dtype=np.float32)

    def add(first: int, sound: np.ndarray) -> None:
        start = first - first_sample
        stop = min(length, start + len(sound))
        if stop > start:
            mix[start:stop] += sound[: stop - start]

    _JOB["players"] = prepared
    sampler.CACHE.limit = CACHE_BYTES // workers
    try:
        if workers == 1:
            for window in windows:
                add(*_render_segment(window))
        else:
            # The worker processes are copies of this process: they have the job data.
            with multiprocessing.get_context("fork").Pool(workers) as pool:
                for first, sound in pool.imap_unordered(_render_segment, windows):
                    add(first, sound)
    finally:
        _JOB.clear()
    return master(mix, len(prepared))


def master(mix: np.ndarray, players: int = 0) -> tuple[np.ndarray, MixReport]:
    """Set the loudness of the mix and make sure that the peak is not too high."""
    meter = pyloudnorm.Meter(dsp.RATE)
    loudness = float(meter.integrated_loudness(mix.astype(np.float64)))
    gain_db = TARGET_LUFS - loudness if np.isfinite(loudness) else 0.0
    peak_db = dsp.to_db(float(np.max(np.abs(mix)))) + gain_db
    if peak_db > PEAK_LIMIT_DB:
        gain_db -= peak_db - PEAK_LIMIT_DB
    result = (mix * np.float32(dsp.db(gain_db))).astype(np.float32)
    report = MixReport(
        seconds=len(result) / dsp.RATE,
        loudness_lufs=float(meter.integrated_loudness(result.astype(np.float64))),
        peak_db=dsp.to_db(float(np.max(np.abs(result)))),
        gain_db=gain_db,
        players=players,
    )
    return result, report


def write(audio: np.ndarray, directory: Path, name: str = "night-music") -> list[Path]:
    """Write the master as FLAC and as MP3. Return the paths."""
    directory.mkdir(parents=True, exist_ok=True)
    flac = directory / f"{name}.flac"
    soundfile.write(str(flac), audio, dsp.RATE, subtype="PCM_24")
    mp3 = directory / f"{name}.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(flac), "-codec:a", "libmp3lame",
         "-q:a", "1", str(mp3)],
        check=True,
    )  # fmt: skip
    return [flac, mp3]
