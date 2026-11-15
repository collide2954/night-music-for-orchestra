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

import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from ..compose import stats
from ..notation import musicxml, playback
from ..notation.work import Work
from . import dsp, reference, stemtone

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
PART = re.compile(r'<Part id="(\d+)">.*?<Instrument id="([^"]+)"', re.DOTALL)

# The level of some instruments of Muse Sounds in relation to the orchestra, in dB.
# The mixer of MuseScore gets these values. They come from measurements of each
# instrument alone, in the heavy section of part 2 and in the first climax:
# - One stroke of the taiko was 8 dB louder than one stroke of the bass drum.
# - The snare drum was 4 dB louder than the bass drum.
# - One stroke of the tom-toms was 16 dB softer than one stroke of the bass drum.
# - A stroke of the tam-tam (fff) was 11 dB softer than the hand cymbals.
TRIM_DB = {"Taiko": -9.0, "Snare Drum": -3.0, "Concert Toms": 8.0, "Tam-tam": 6.0}
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
    players: set[str] | None = None,
    levels: dict[str, playback.Levels] | None = None,
) -> tuple[np.ndarray, list[str]]:
    """Render the work (or some bars) with MuseScore.

    Return the two-channel sound at the sample rate of the project, and the
    names of the parts that MuseScore played. The sound starts at the start
    of the first bar.
    """
    directory.mkdir(parents=True, exist_ok=True)
    log = directory / "musescore.log"
    log.write_text("", encoding="utf-8")
    text, names = musicxml.score(work, bars, instruments, players, levels)
    source = directory / "score.musicxml"
    source.write_text(text, encoding="utf-8")
    packed = directory / "score.mscz"
    packed.unlink(missing_ok=True)
    _run(["-o", str(packed), str(source)], log)
    count = prepare_file(packed, profile, names)
    sound = directory / "score.wav"
    sound.unlink(missing_ok=True)
    _run(["-o", str(sound), str(packed)], log)
    print(f"musescore: {len(names)} parts, {count} playing technique marks, profile {profile}")
    return _load(sound), names


# The highest note (MIDI number) that Muse Sounds play, for the instruments whose
# range in the orchestra file goes higher. A higher note has no sound. A test score
# with all notes of each range gave these values.
HIGHEST_NOTE = {
    "flute": 97, "alto flute": 87, "bass clarinet": 80, "contrabass clarinet": 64,
    "bassoon": 75, "harp": 102, "violin": 101, "viola": 86, "double bass": 61,
}  # fmt: skip


def silent_notes(work: Work) -> list[tuple[str, int, float]]:
    """Return the notes of the work that Muse Sounds do not play: player, bar, MIDI number."""
    from ..perform.events import perform

    found = []
    for player in work.orchestra.players:
        for note in perform(work, player.id):
            if note.midi > HIGHEST_NOTE.get(note.instrument, 1000):
                found.append((player.id, work.structure.bar_at(note.start).number, note.midi))
    return found


def continuous_slides(score: str) -> str:
    """Make each slide between two notes a continuous change of pitch.

    MuseScore plays a slide from a MusicXML file as a sequence of semitones.
    The play style "portamento" gives the slide of a string player.
    """
    return score.replace("<Glissando>", "<Glissando><glissandoStyle>portamento</glissandoStyle>")


def mixer_tracks(score: str, names: list[str]) -> list[dict]:
    """Return the mixer settings for the parts that have a level in `TRIM_DB`.

    `score` is the text of the MuseScore file. `names` are the names of its
    parts, in the sequence of the file, for example "Taiko (perc6)".
    """
    tracks = []
    for (part, instrument), name in zip(PART.findall(score), names, strict=True):
        trim = TRIM_DB.get(name.rsplit(" (", 1)[0], 0.0)
        if trim:
            out = {"volumeDb": trim, "balance": 0, "fxChain": {}}
            tracks.append({"partId": part, "instrumentId": instrument, "out": out})
    return tracks


def prepare_file(packed: Path, profile: str, names: list[str] | None = None) -> int:
    """Change the MuseScore file for the render. Return the number of technique marks.

    The file is a ZIP archive. The function changes two files in it:

    - The score: the words of the playing techniques become technique marks,
      and a slide between two notes becomes a continuous change of pitch.
    - The audio settings: the sound profile, a lower level of the master
      control, and the levels of `TRIM_DB`. With the master control at 0 dB,
      a loud passage of the full orchestra is too loud for the output of
      MuseScore and has distortion.
    """
    count = 0
    tracks: list[dict] = []
    contents: dict[str, bytes] = {}
    with zipfile.ZipFile(packed) as archive:
        for name in archive.namelist():
            contents[name] = archive.read(name)
    for name, data in contents.items():
        if name.endswith(".mscx"):
            changed, count = play_techniques(data.decode("utf-8"))
            changed = continuous_slides(changed)
            contents[name] = changed.encode("utf-8")
            if names is not None:
                tracks = mixer_tracks(changed, names)
    for name, data in contents.items():
        if name == "audiosettings.json":
            settings = json.loads(data.decode("utf-8"))
            settings["activeSoundProfile"] = profile
            settings.setdefault("master", {})["volumeDb"] = MASTER_VOLUME_DB
            if tracks:
                settings["tracks"] = tracks
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


# The groups of the orchestra. MuseScore renders each group as one file (a
# stem). The sum of the stems is the same as one render of all groups. The
# stems make three things possible: parallel renders, a new render of one
# group only, and a change of the balance between the groups.
STEMS = {
    "woodwinds": ("woodwinds",),
    "brass": ("brass",),
    "percussion": ("percussion",),
    "keys": ("plucked", "keyboards"),
    "strings": ("strings",),
}

# Level of each stem in the mix, in dB.
STEM_GAIN_DB = {"woodwinds": 0.0, "brass": 0.0, "percussion": 0.0, "keys": 0.0, "strings": 0.0}

# The equalization of the mix. The loud passages of the mix (the loudest tenth of its
# seconds) were compared with those of the five reference recordings of real
# orchestras, in bands of one octave, in relation to the band 250 Hz to 1 kHz:
# - 125 to 250 Hz: the mix was 2 to 3 dB above the middle of the recordings.
# - 1 to 4 kHz: the mix was 1.5 to 2 dB below the middle of the recordings.
# - 8 to 16 kHz: the mix was 5 dB above the middle, and above four of the five.
# The soft and the medium passages gave almost the same differences.
# The microphones of Muse Sounds are near the instruments. In a hall, the air and the
# distance take away much of the sound above 8 kHz. Too much sound in that range makes
# loud brass and cymbals hard. Each row is: the type, the frequency in Hz, the gain
# in dB, and (for a bell filter) the quality factor.
MASTER_EQ: tuple[tuple, ...] = (
    ("bell", 170.0, -2.0, 0.8),
    ("bell", 2000.0, 2.0, 0.7),
    ("high shelf", 6000.0, -4.0),
)

PARALLEL_RENDERS = 3  # number of MuseScore programs that run at the same time

# The sound of MuseScore is much wider than a recording of a real orchestra:
# the left and the right channel are almost independent, and the brass has
# more difference signal than sum signal. The measured recordings have a
# correlation of 0.39 to 0.69. A stem with a smaller correlation than this
# value gets a smaller difference signal.
SMALLEST_CORRELATION = 0.35

# Limits of the gain riding of the master for this source of sound.
RIDING_GAIN_DB = 26.0
RIDING_RATIO = 4.0
RENDER_VERSION = 3  # a change of this number makes all kept stems invalid


def render_stems(
    work: Work, directory: Path, bars: tuple[int, int] | None = None, profile: str = PROFILE
) -> dict[str, np.ndarray]:
    """Render each group of the orchestra with MuseScore. Return the sound of each group.

    A stem that is in the directory from an earlier render stays, if its
    music did not change.
    """

    def one(name: str) -> tuple[str, np.ndarray | None]:
        families = STEMS[name]
        players = {p.id for p in work.orchestra.players if p.family in families}
        text, names = musicxml.score(work, bars, players=players)
        if not names:
            return name, None
        # An excerpt has its own folder: thus the stems of the full work stay.
        folder = directory / (name if bars is None else f"{name}-{bars[0]}-{bars[1]}")
        record = folder / "stem.json"
        sound = folder / "score.wav"
        key = hashlib.sha256(
            f"{RENDER_VERSION}|{profile}|{MASTER_VOLUME_DB}|{sorted(TRIM_DB.items())}|{text}".encode()
        ).hexdigest()
        kept = json.loads(record.read_text(encoding="utf-8")) if record.exists() else {}
        if sound.exists() and kept.get("key") == key:
            print(f"musescore: stem {name}: kept from the last render")
            return name, _load(sound)
        audio, _names = render(work, folder, bars, profile, players=players)
        record.write_text(json.dumps({"key": key, "parts": names}), encoding="utf-8")
        return name, audio

    with ThreadPoolExecutor(max_workers=PARALLEL_RENDERS) as pool:
        results = list(pool.map(one, STEMS))
    return {name: audio for name, audio in results if audio is not None}


def _load(sound: Path) -> np.ndarray:
    """Read the sound of MuseScore, at the level of a master control at 0 dB."""
    audio = reference.load_stereo(sound)
    audio *= np.float32(dsp.db(-MASTER_VOLUME_DB))
    return audio


def narrow(audio: np.ndarray, smallest: float = SMALLEST_CORRELATION) -> tuple[np.ndarray, float]:
    """Make a stem less wide, if its channels are too independent.

    The function changes `audio` in place. It returns the audio and the gain
    of the difference signal in dB (0 = no change).
    """
    sum_power, difference_power = 0.0, 0.0
    step = 60 * dsp.RATE
    for start in range(0, len(audio), step):
        part = audio[start : start + step].astype(np.float64)
        sum_power += float(np.sum(np.square(part[:, 0] + part[:, 1])))
        difference_power += float(np.sum(np.square(part[:, 0] - part[:, 1])))
    if sum_power <= 0.0 or difference_power <= 0.0:
        return audio, 0.0
    correlation = (sum_power - difference_power) / (sum_power + difference_power)
    if correlation >= smallest:
        return audio, 0.0
    wanted = (1.0 - smallest) / (1.0 + smallest)  # difference power / sum power
    gain = float(np.sqrt(wanted * sum_power / difference_power))
    for start in range(0, len(audio), step):
        part = audio[start : start + step]
        middle = 0.5 * (part[:, 0] + part[:, 1])
        side = 0.5 * (part[:, 0] - part[:, 1]) * np.float32(gain)
        part[:, 0] = middle + side
        part[:, 1] = middle - side
    return audio, dsp.to_db(gain)


def equalize(audio: np.ndarray, rows: tuple[tuple, ...] | None = None) -> np.ndarray:
    """Apply the equalization of the mix (`MASTER_EQ`). The function changes `audio`."""
    filters = []
    for kind, frequency, gain_db, *more in MASTER_EQ if rows is None else rows:
        if kind == "bell":
            filters.append(dsp.peaking(frequency, gain_db, *more))
        else:
            filters.append(dsp.shelf(frequency, gain_db, high=kind == "high shelf"))
    for channel in range(audio.shape[1]):
        audio[:, channel] = dsp.apply(audio[:, channel], *filters)
    return audio


def render_master(
    work: Work, directory: Path, bars: tuple[int, int] | None = None, profile: str = PROFILE
):
    """Render the master: MuseScore plays, the sampler adds the other instruments."""
    from . import mix

    stems = render_stems(work, directory, bars, profile)
    others, count = mix.render_mix(work, bars=bars, instruments=other_instruments(work))
    # The mix of an excerpt starts some time before its first bar.
    begin = work.structure.seconds(work.structure.bar(bars[0]).start) if bars else 0.0
    lead = int(round(min(begin, mix.SEGMENT_LEAD) * dsp.RATE)) if bars else 0
    others = others[lead:]
    gain = dsp.db(calibration_gain(work, directory, profile))
    length = max([len(others), *(len(audio) for audio in stems.values())])
    total = np.zeros((length, 2), dtype=np.float32)
    for name, audio in stems.items():
        audio, side_db = narrow(audio)
        print(f"musescore: stem {name}: difference signal {side_db:+.1f} dB")
        if name in stemtone.TABLES:
            # The loud marks of this group get their difference again (see `stemtone`).
            players = [p.id for p in work.orchestra.players if p.family in STEMS[name]]
            level = stemtone.written_level(work, players, begin, len(audio) / dsp.RATE)
            stemtone.shape(audio, level, stemtone.TABLES[name])
        if name in stemtone.RIDES:
            audio, largest = stemtone.ride(audio, *stemtone.RIDES[name])
            print(f"musescore: stem {name}: largest slow level change {largest:+.1f} dB")
        total[: len(audio)] += np.float32(dsp.db(STEM_GAIN_DB[name])) * audio
    total[: len(others)] += np.float32(gain) * others
    equalize(total)
    # The soft passages of Muse Sounds are much softer than those of the open
    # samples: the gain riding of the master can do more.
    return mix.master(
        total,
        len(stems) + count,
        full=bars is None,
        tone=False,
        largest_gain_db=RIDING_GAIN_DB,
        largest_ratio=RIDING_RATIO,
        passages=stats.passages(work),
    )
