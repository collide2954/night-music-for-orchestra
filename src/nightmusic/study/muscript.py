"""Parser for the muscript text score format.

Peter Billam wrote the muscript format. The format manual is at
https://peterbillam.gitlab.io/muscript/ . This parser reads the subset of the
format that the style study needs: bars, time signatures, key signatures,
clefs, rhythms, notes, chords, ties, text marks, and MIDI timing data.

Pitch rule of the format: each clef has a note `c` near its middle. Lower-case
letters `c` to `b` are the octave that starts at that note. Upper-case letters
`C` to `B` are the octave below. Each `~` moves a note up one octave and each
`_` moves a note down one octave.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from fractions import Fraction

# MIDI number of the note `c` for each clef.
CLEF_C = {
    "treble": 72,
    "treble8va": 84,
    "treble8vab": 60,
    "alto": 60,
    "tenor": 60,
    "bass": 48,
    "bass8va": 60,
    "bass8vab": 36,
}
LETTER_SEMITONES = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
ACCIDENTAL_SEMITONES = {"bb": -2, "b": -1, "n": 0, "#": 1, "##": 2}
SHARP_ORDER = "fcgdaeb"
FLAT_ORDER = "beadgcf"

# Number of notes in a tuplet group -> duration factor.
TUPLET_FACTOR = {
    "2": Fraction(3, 4),
    "3": Fraction(2, 3),
    "4": Fraction(3, 4),
    "5": Fraction(4, 5),
    "6": Fraction(4, 6),
    "7": Fraction(4, 7),
    "9": Fraction(8, 9),
}
BASE_QUARTERS = {
    "bre": Fraction(8),
    "1": Fraction(4),
    "2": Fraction(2),
    "4": Fraction(1),
    "8": Fraction(1, 2),
    "16": Fraction(1, 4),
    "32": Fraction(1, 8),
    "64": Fraction(1, 16),
}

RHYTHM_RE = re.compile(r"^(bre|64|32|16|8|4|2|1)([2345679])?(\.{0,3})(/{0,3})((?:-[a-z]+)*)$")
NOTE_RE = re.compile(
    r"^(?P<beam_start>\[*)(?P<chord_start><?)"
    r"(?P<letter>[A-Ga-g])(?P<octave>[~_]*)(?P<accidental>bb|##|b|#|n)?"
    r"(?P<layout>[xrl',]*)"
    r"(?P<curves>(?:[({][',]*\d|[)}][',]*\d)*)"
    r"(?P<options>(?:-[^\s<>\[\]]*)*)"
    r"(?P<chord_end>>?)(?P<options_after>(?:-[^\s<>\[\]]*)*)(?P<beam_end>\]*)$"
)
REST_RE = re.compile(r"^\[*(rest|blank)[',]*(?:-[^\s\]]*)*\]*$")
MIDI_RE = re.compile(
    r"^(cha|vol|leg|pan|pat|tra|pau|ben|ban|cc|rev|vib|cho|sus)[a-z]*[+\-]?[\d.+=\-]*$"
)
VOLUME_RE = re.compile(r"^vol[a-z]*([+\-]?)(\d+)$")
KEY_RE = re.compile(r"^(\d)([b#])$")
TIME_RE = re.compile(r"^(\d+)/(\d+)$")
STAVE_RE = re.compile(r"^=(\d+)([',]?)\s*(.*)$")
TEXT_RE = re.compile(r"^(b|r|i|I)([ls]?)(-?\d*\.?\d+)\s+(.*)$")
X_POSITION_RE = re.compile(r"^-?\d?\.\d+$")
TIE_START_RE = re.compile(r"\([',]*(\d)")
TIE_END_RE = re.compile(r"\)[',]*(\d)")


@dataclass
class TextMark:
    """A text mark in a bar. `x` is the horizontal position (0 = bar start, 1 = bar end)."""

    bar: int
    font: str
    x: float
    text: str


@dataclass
class Note:
    """One sounding note. The parser merges tied notes into one note."""

    bar: int
    start: Fraction  # quarter notes from the start of the piece
    duration: Fraction  # quarter notes
    midi: int
    stave: int
    voice: str
    small: bool
    volume: int

    @property
    def end(self) -> Fraction:
        return self.start + self.duration


@dataclass
class Bar:
    """One bar with its metre and its timing data."""

    number: int
    start: Fraction  # quarter notes from the start of the piece
    time_signature: tuple[int, int]
    seconds: tuple[float, ...]  # durations of the equal parts of the bar
    pause_before: float = 0.0  # silence before the bar, in seconds
    key_signature: int = 0  # number of sharps (positive) or flats (negative) on stave 1
    texts: list[TextMark] = field(default_factory=list)
    voice_fill: dict[str, Fraction] = field(default_factory=dict)

    @property
    def length(self) -> Fraction:
        numerator, denominator = self.time_signature
        return Fraction(numerator * 4, denominator)

    @property
    def duration_seconds(self) -> float:
        return sum(self.seconds)

    @property
    def quarter_bpm(self) -> float:
        """Mean tempo of the bar in quarter notes for each minute."""
        return 60.0 * float(self.length) / self.duration_seconds


@dataclass
class Score:
    """A parsed score."""

    bars: list[Bar]
    notes: list[Note]
    warnings: list[str]

    def bar_start_seconds(self) -> list[float]:
        """Return the start time of each bar in seconds."""
        times, clock = [], 0.0
        for bar in self.bars:
            clock += bar.pause_before
            times.append(clock)
            clock += bar.duration_seconds
        return times

    @property
    def duration_seconds(self) -> float:
        return sum(bar.pause_before + bar.duration_seconds for bar in self.bars)


@dataclass
class _StaveState:
    clef: str = "treble"
    key: int = 0
    volume: int = 100
    rhythm: Fraction = Fraction(1)
    small: bool = False
    accidentals: dict[tuple[str, int], int] = field(default_factory=dict)
    ties: dict[str, Note] = field(default_factory=dict)


def _join_continuations(text: str) -> list[str]:
    lines, pending = [], ""
    for raw in text.splitlines():
        stripped = raw.rstrip()
        if stripped.endswith("\\"):
            pending += stripped[:-1] + " "
        else:
            lines.append(pending + raw)
            pending = ""
    if pending:
        lines.append(pending)
    return lines


def _strip_comment(line: str) -> str:
    """Remove a trailing comment. A `#` that follows a note letter is a sharp sign."""
    match = re.search(r"(^|\s)#(\s|$)", line)
    if line.lstrip().startswith("#"):
        return ""
    return line[: match.start()] if match else line


def _key_alteration(letter: str, key: int) -> int:
    if key > 0 and letter in SHARP_ORDER[:key]:
        return 1
    if key < 0 and letter in FLAT_ORDER[:-key]:
        return -1
    return 0


def parse_rhythm(token: str) -> tuple[Fraction, bool] | None:
    """Return the duration in quarter notes and the small-note flag, or None."""
    match = RHYTHM_RE.match(token)
    if not match:
        return None
    base, tuplet, dots, _tremolo, options = match.groups()
    duration = BASE_QUARTERS[base]
    if tuplet:
        duration *= TUPLET_FACTOR[tuplet]
    duration *= 2 - Fraction(1, 2 ** len(dots))
    small = "-s" in options
    return duration, small


def parse(text: str) -> Score:
    """Parse muscript text into bars and notes."""
    bars: list[Bar] = []
    notes: list[Note] = []
    warnings: list[str] = []
    staves: dict[int, _StaveState] = {}
    time_signature = (4, 4)
    seconds: tuple[float, ...] = (2.0,)
    pending_pause = 0.0
    position = Fraction(0)

    for line_number, raw in enumerate(_join_continuations(text), 1):
        line = _strip_comment(raw).strip()
        if not line:
            continue

        if line.startswith("|"):
            if bars:
                position = bars[-1].start + bars[-1].length
            for token in line[1:].split():
                time_match = TIME_RE.match(token)
                if time_match:
                    time_signature = (int(time_match.group(1)), int(time_match.group(2)))
            numbers = [float(t) for t in line[1:].split() if re.fullmatch(r"\d*\.?\d+", t)]
            if numbers:
                seconds = tuple(numbers)
            bar = Bar(
                number=len(bars) + 1,
                start=position,
                time_signature=time_signature,
                seconds=seconds,
                pause_before=pending_pause,
                key_signature=staves[1].key if 1 in staves else 0,
            )
            pending_pause = 0.0
            bars.append(bar)
            for state in staves.values():
                state.accidentals.clear()
            continue

        if line.startswith("midi pause"):
            pending_pause += float(line.split()[2])
            continue

        stave_match = STAVE_RE.match(line)
        if stave_match and bars:
            bar = bars[-1]
            stave = int(stave_match.group(1))
            voice = stave_match.group(2)
            state = staves.setdefault(stave, _StaveState())
            cursor = Fraction(0)
            chord_open = False
            in_quote = False
            line_notes: list[Note] = []
            for token in stave_match.group(3).split():
                if in_quote:
                    if '"' in token:
                        in_quote = False
                    continue
                if token.count('"') % 2 == 1:
                    in_quote = True
                if token in CLEF_C:
                    state.clef = token
                    continue
                if token == "clefspace":
                    continue
                key_match = KEY_RE.match(token)
                if key_match or token == "0":
                    state.key = 0
                    if key_match:
                        count = int(key_match.group(1))
                        state.key = count if key_match.group(2) == "#" else -count
                    if stave == 1:
                        bar.key_signature = state.key
                    continue
                time_match = TIME_RE.match(token)
                if time_match:
                    printed = (int(time_match.group(1)), int(time_match.group(2)))
                    if printed != bar.time_signature:
                        bar.time_signature = printed
                        time_signature = printed
                    continue
                volume_match = VOLUME_RE.match(token)
                if volume_match:
                    sign, amount = volume_match.group(1), int(volume_match.group(2))
                    if sign == "+":
                        state.volume += amount
                    elif sign == "-":
                        state.volume -= amount
                    else:
                        state.volume = amount
                    continue
                if MIDI_RE.match(token):
                    continue
                rhythm = parse_rhythm(token)
                if rhythm:
                    state.rhythm, state.small = rhythm
                    continue
                if REST_RE.match(token):
                    cursor += state.rhythm
                    continue
                note_match = NOTE_RE.match(token)
                if not note_match:
                    warnings.append(f"line {line_number}: unknown token {token!r}")
                    continue

                if note_match["chord_start"]:
                    chord_open = True
                letter = note_match["letter"]
                octave_marks = note_match["octave"]
                level = (0 if letter.islower() else -1) + octave_marks.count("~")
                level -= octave_marks.count("_")
                letter = letter.lower()
                accidental = note_match["accidental"]
                if accidental is not None:
                    alteration = ACCIDENTAL_SEMITONES[accidental]
                    state.accidentals[(letter, level)] = alteration
                elif (letter, level) in state.accidentals:
                    alteration = state.accidentals[(letter, level)]
                else:
                    alteration = _key_alteration(letter, state.key)
                midi = CLEF_C[state.clef] + 12 * level + LETTER_SEMITONES[letter] + alteration

                curves = note_match["curves"]
                tie_ends = TIE_END_RE.findall(curves)
                tie_starts = TIE_START_RE.findall(curves)
                note: Note | None = None
                for tie_id in tie_ends:
                    earlier = state.ties.pop(tie_id, None)
                    if earlier is not None and earlier.end == bar.start + cursor:
                        # The tied note keeps the pitch of the note that started the tie.
                        earlier.duration += state.rhythm
                        note = earlier
                        break
                if note is None:
                    note = Note(
                        bar=bar.number,
                        start=bar.start + cursor,
                        duration=state.rhythm,
                        midi=midi,
                        stave=stave,
                        voice=voice,
                        small=state.small,
                        volume=state.volume,
                    )
                    notes.append(note)
                    line_notes.append(note)
                for tie_id in tie_starts:
                    state.ties[tie_id] = note

                if note_match["chord_end"]:
                    chord_open = False
                if not chord_open:
                    cursor += state.rhythm
            if cursor > bar.length:
                # The line is longer than the bar (a tuplet group without its ratio).
                # Compress the line so that it fills the bar exactly.
                factor = bar.length / cursor
                for note in line_notes:
                    note.start = bar.start + (note.start - bar.start) * factor
                    note.duration *= factor
                warnings.append(f"bar {bar.number}: line compressed by the factor {factor}")
                cursor = bar.length
            voice_key = f"{stave}{voice}"
            bar.voice_fill[voice_key] = max(bar.voice_fill.get(voice_key, Fraction(0)), cursor)
            continue

        text_match = TEXT_RE.match(line)
        if text_match and bars:
            font = text_match.group(1) + text_match.group(2)
            x, words = 0.0, []
            for token in text_match.group(4).split():
                if X_POSITION_RE.match(token):
                    if words:
                        bars[-1].texts.append(TextMark(len(bars), font, x, " ".join(words)))
                        words = []
                    x = float(token)
                else:
                    words.append(token)
            if words:
                bars[-1].texts.append(TextMark(len(bars), font, x, " ".join(words)))
            continue
        # All other lines are page layout commands. The study does not use them.

    notes.sort(key=lambda n: (n.start, n.midi))
    return Score(bars=bars, notes=notes, warnings=warnings)
