"""The mixer: put all players on the stage, add the hall, and make the master file."""

from __future__ import annotations

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


def render(work: Work, *, players: list[str] | None = None) -> tuple[np.ndarray, MixReport]:
    """Render the work. Return the two-channel master and its report."""
    structure = work.structure
    total = structure.duration_seconds + TAIL_SECONDS
    length = int(np.ceil(total * dsp.RATE))
    dry = np.zeros((length, 2), dtype=np.float32)
    send = np.zeros(length, dtype=np.float32)
    count = 0
    for player in work.orchestra.players:
        if players is not None and player.id not in players:
            continue
        notes = perform(work, player.id)
        if not notes:
            continue
        count += 1
        for group, stem in enumerate(sampler.render_player(notes, structure, total)):
            seat = space.seat_of(player.id, group)
            dry += space.place(stem, seat)
            send += stem * np.float32(space.reverb_send(seat))
    wet = space.reverberate(send)
    mix = dry + wet * np.float32(dsp.db(REVERB_GAIN_DB))
    return master(mix, count)


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
