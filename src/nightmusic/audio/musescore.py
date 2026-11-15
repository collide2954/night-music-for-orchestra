"""Render the audio with MuseScore Studio and its Muse Sounds libraries.

Muse Sounds are free sample libraries of an orchestra. They are much more
realistic than the open sample libraries of this project. They are not open:
only MuseScore Studio can play them, and a build server cannot install them.
Thus this render is for the computer of the owner of the project.

The steps are:

1. Write the work as a MusicXML file (`notation/musicxml.py`).
2. MuseScore changes the MusicXML file into its own format.
3. The playing techniques in that file get the form that MuseScore plays
   (for example pizzicato, sul ponticello, mute).
4. MuseScore renders the file to audio with the sound profile "Muse Sounds".
5. The sampler of this project renders the instruments that Muse Sounds do
   not have (for example cimbalom, accordion, ocarina, and the unpitched
   percussion). The mixer adds them.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import numpy as np

from ..notation import musicxml
from ..notation.work import Work
from . import dsp, reference

PROFILE = "Muse Sounds"
MASTER_VOLUME_DB = -18.0  # level of the master control of MuseScore for the render
SAMPLER_HOME = Path.home() / ".local/share/MuseSampler"
# The Muse Sounds libraries play only in the official build of MuseScore Studio.
OFFICIAL_PROGRAM = Path.home() / ".local/opt/musescore-studio/squashfs-root/AppRun"
PROGRAM_VARIABLE = "NIGHTMUSIC_MUSESCORE"


def program() -> str:
    """Return the MuseScore program: the official build if it is there."""
    if os.environ.get(PROGRAM_VARIABLE):
        return os.environ[PROGRAM_VARIABLE]
    return str(OFFICIAL_PROGRAM) if OFFICIAL_PROGRAM.exists() else "mscore"


# Words of a playing technique in the score -> the technique of MuseScore.
PLAY_TECHNIQUES = {
    "pizz.": "pizzicato",
    "arco": "natural",
    "ord.": "natural",
    "col legno": "col_legno",
    "sul pont.": "sul_ponticello",
    "sul tasto": "sul_tasto",
    "con sord.": "mute",
    "senza sord.": "open",
}

STAFF_TEXT = re.compile(r"<StaffText>(.*?)</StaffText>", re.DOTALL)
TEXT = re.compile(r"<text>(.*?)</text>", re.DOTALL)


def available() -> bool:
    """Return true if MuseScore and the Muse Sounds libraries are on this computer."""
    return shutil.which(program()) is not None and any(SAMPLER_HOME.rglob("*.so"))


def _run(arguments: list[str], log: Path) -> None:
    environment = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    with log.open("a", encoding="utf-8") as handle:
        result = subprocess.run(
            [program(), *arguments], env=environment, stdout=handle, stderr=handle, check=False
        )
    if result.returncode != 0:
        raise RuntimeError(f"MuseScore failed ({' '.join(arguments)}). See {log}.")


def play_techniques(text: str) -> tuple[str, int]:
    """Change the staff texts of playing techniques into playing technique marks.

    MuseScore reads the words of a MusicXML file as plain text. A plain text
    has no effect on the sound. Return the new text and the number of changes.
    """
    count = 0

    def change(match: re.Match[str]) -> str:
        nonlocal count
        words = TEXT.search(match.group(1))
        technique = PLAY_TECHNIQUES.get(words.group(1).strip()) if words else None
        if technique is None:
            return match.group(0)
        count += 1
        body = match.group(1).rstrip()
        return (
            f"<PlayTechAnnotation>{body}\n            <playTechType>{technique}</playTechType>"
            f"\n            </PlayTechAnnotation>"
        )

    return STAFF_TEXT.sub(change, text), count


def render(
    work: Work,
    directory: Path,
    bars: tuple[int, int] | None = None,
    profile: str = PROFILE,
    instruments: set[str] | None = None,
) -> tuple[np.ndarray, list[str]]:
    """Render the work (or some bars) with MuseScore.

    Return the two-channel sound at the sample rate of the project, and the
    names of the parts that MuseScore played. The sound starts at the start
    of the first bar.
    """
    directory.mkdir(parents=True, exist_ok=True)
    log = directory / "musescore.log"
    log.write_text("", encoding="utf-8")
    text, names = musicxml.score(work, bars, instruments)
    source = directory / "score.musicxml"
    source.write_text(text, encoding="utf-8")
    packed = directory / "score.mscz"
    packed.unlink(missing_ok=True)
    _run(["-o", str(packed), str(source)], log)
    count = prepare_file(packed, profile)
    sound = directory / "score.wav"
    sound.unlink(missing_ok=True)
    _run(["-o", str(sound), str(packed)], log)
    print(f"musescore: {len(names)} parts, {count} playing technique marks, profile {profile}")
    audio = reference.load_stereo(sound)
    # Give the sound the level that it has with the master control at 0 dB.
    audio *= np.float32(dsp.db(-MASTER_VOLUME_DB))
    return audio, names


def prepare_file(packed: Path, profile: str) -> int:
    """Change the MuseScore file for the render. Return the number of technique marks.

    The file is a ZIP archive. The function changes two files in it:

    - The score: the words of the playing techniques become technique marks.
    - The audio settings: the sound profile, and a lower level of the master
      control. With the control at 0 dB, a loud passage of the full
      orchestra is too loud for the output of MuseScore and has distortion.
    """
    count = 0
    contents: dict[str, bytes] = {}
    with zipfile.ZipFile(packed) as archive:
        for name in archive.namelist():
            contents[name] = archive.read(name)
    for name, data in contents.items():
        if name.endswith(".mscx"):
            changed, count = play_techniques(data.decode("utf-8"))
            contents[name] = changed.encode("utf-8")
        elif name == "audiosettings.json":
            settings = json.loads(data.decode("utf-8"))
            settings["activeSoundProfile"] = profile
            settings.setdefault("master", {})["volumeDb"] = MASTER_VOLUME_DB
            contents[name] = json.dumps(settings, indent=4).encode("utf-8")
    with zipfile.ZipFile(packed, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in contents.items():
            archive.writestr(name, data)
    return count


def other_instruments(work: Work) -> set[str]:
    """Return the instruments of the work that MuseScore does not play."""
    names = {name for player in work.orchestra.players for name in player.instruments}
    return {name for name in names if not musicxml.can_play(name)}


CALIBRATION_INSTRUMENT = "timpani"  # an instrument that the two sound sources have
CALIBRATION_BARS = (1, 8)


def calibration_gain(work: Work, directory: Path, profile: str) -> float:
    """Return the gain in dB for the sampler of this project, to agree with MuseScore.

    The two sound sources play the same notes of one instrument. The gain
    gives the sound of the sampler the level of the sound of MuseScore. The
    result is kept in a file: the measurement is necessary only one time.
    """
    from . import mix

    record = directory / "calibration.json"
    if record.exists():
        known = json.loads(record.read_text(encoding="utf-8"))
        if known.get("profile") == profile:
            return float(known["gain_db"])
    instruments = {CALIBRATION_INSTRUMENT}
    theirs, _names = render(
        work, directory / "calibration", CALIBRATION_BARS, profile, instruments=instruments
    )
    ours, _count = mix.render_mix(work, bars=CALIBRATION_BARS, instruments=instruments)
    gain_db = dsp.to_db(dsp.rms(theirs) / max(dsp.rms(ours), 1e-12))
    record.write_text(json.dumps({"profile": profile, "gain_db": gain_db}), encoding="utf-8")
    return gain_db


def render_master(
    work: Work, directory: Path, bars: tuple[int, int] | None = None, profile: str = PROFILE
):
    """Render the master: MuseScore plays, the sampler adds the other instruments."""
    from . import mix

    played, names = render(work, directory, bars, profile)
    others, count = mix.render_mix(work, bars=bars, instruments=other_instruments(work))
    # The mix of an excerpt starts some time before its first bar.
    begin = work.structure.seconds(work.structure.bar(bars[0]).start) if bars else 0.0
    lead = int(round(min(begin, mix.SEGMENT_LEAD) * dsp.RATE)) if bars else 0
    others = others[lead:]
    gain = dsp.db(calibration_gain(work, directory, profile))
    total = np.zeros((max(len(played), len(others)), 2), dtype=np.float32)
    total[: len(played)] += played
    total[: len(others)] += np.float32(gain) * others
    return mix.master(total, len(names) + count, full=bars is None, tone=False)
