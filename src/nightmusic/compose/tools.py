"""Change music text with code: transposition, inversion, repetition, and voicing.

These tools do the "developing variation" of the work. The composer writes a
theme one time. The tools make its other forms: at a different pitch, upside
down, or for a different instrument. Other tools divide a chord progression
between players, and make a figure from each chord.
"""

from __future__ import annotations

import re
from dataclasses import replace
from fractions import Fraction

from ..notation import music
from ..notation.pitch import STEP_SEMITONES, Interval, Pitch
from ..notation.work import Section


def _map_pitches(elements: list[music.Element], change) -> list[music.Element]:
    result: list[music.Element] = []
    for element in elements:
        if isinstance(element, music.Note):
            pitches = [replace(p, pitch=change(p.pitch)) for p in element.pitches]
            result.append(replace(element, pitches=pitches))
        elif isinstance(element, music.Group):
            result.append(replace(element, children=_map_pitches(element.children, change)))
        else:
            result.append(element)
    return result


def _apply(text: str, change) -> str:
    parsed = music.parse(text)
    return music.body_to_lilypond(music.Group("sequence", _map_pitches(parsed.children, change)))


def tr(text: str, semitones: int, steps: int | None = None) -> str:
    """Return the music moved by a number of semitones.

    `steps` is the number of scale steps of the interval. If it is not given,
    the function selects the usual interval for the number of semitones.
    """
    if semitones == 0 and not steps:
        return text
    interval = Interval(round(semitones * 7 / 12) if steps is None else steps, semitones)
    return _apply(text, lambda pitch: pitch.transposed(interval).simplified())


def octave(text: str, count: int) -> str:
    """Return the music moved by a number of octaves (negative = down)."""
    return tr(text, 12 * count, 7 * count)


def invert(text: str, axis: str) -> str:
    """Return the mirror of the music around the pitch `axis`.

    A step up becomes the same step down. This is the method of the mirror
    form of the walking theme.
    """
    centre = Pitch.parse(axis)

    def mirror(pitch: Pitch) -> Pitch:
        index = 2 * (centre.step + 7 * centre.octave) - (pitch.step + 7 * pitch.octave)
        octave_number, step = divmod(index, 7)
        natural = 12 * (octave_number + 1) + STEP_SEMITONES[step]
        target = 2 * centre.midi - pitch.midi
        return Pitch(
            step, Fraction(target - natural).limit_denominator(2), octave_number
        ).simplified()

    return _apply(text, mirror)


def times(text: str, count: int) -> str:
    """Return the music repeated a number of times."""
    return " ".join([text.strip()] * count)


def rests(numerator: int, denominator: int, bars: int = 1) -> str:
    """Return full-bar rests for a number of bars of one metre."""
    return f"R1*{numerator * bars}/{denominator} |"


def _first_event(elements: list[music.Element]) -> music.Note | music.Rest | None:
    for element in elements:
        if isinstance(element, music.Note | music.Rest):
            return element
        if isinstance(element, music.Group) and element.kind != "parallel":
            found = _first_event(element.children)
            if found:
                return found
    return None


def _first_note(elements: list[music.Element]) -> music.Note | None:
    for element in elements:
        if isinstance(element, music.Note):
            return element
        if isinstance(element, music.Group) and element.kind != "parallel":
            found = _first_note(element.children)
            if found:
                return found
    return None


def _posts(marks: str) -> list[music.Post]:
    """Parse marks, for example `\\pp\\senzasord`, into events."""
    if not marks.strip():
        return []
    return music.parse("c4" + marks).children[0].posts


def first(text: str, marks: str, *, note: bool = False) -> str:
    """Return the music with marks added to its first note or rest.

    If `note` is true, the marks go on the first note, not on a rest before it.
    """
    parsed = music.parse(text)
    target = _first_note(parsed.children) if note else _first_event(parsed.children)
    if target is None:
        raise ValueError("the music has no note for the marks")
    target.posts[:0] = _posts(marks)
    return music.body_to_lilypond(parsed)


def _strip(elements: list[music.Element], kinds: frozenset[str]) -> None:
    for element in elements:
        if isinstance(element, music.Note | music.Rest):
            element.posts[:] = [
                post
                for post in element.posts
                if not (
                    post.kind in kinds
                    or (post.kind == "command" and "technique" in kinds
                        and post.value in music.TECHNIQUE_NAMES)
                )
            ]  # fmt: skip
        elif isinstance(element, music.Group):
            _strip(element.children, kinds)


def plain(text: str, *kinds: str) -> str:
    """Return the music without its dynamic marks and hairpins.

    Other kinds of marks can be given: "slur", "articulation", "text",
    "technique", "tie", "phrasing".
    """
    parsed = music.parse(text)
    _strip(parsed.children, frozenset(kinds or ("dynamic", "hairpin")))
    return music.body_to_lilypond(parsed)


def dyn(text: str, marks: str) -> str:
    """Return the music with new dynamic marks on its first note, and no other dynamics."""
    return first(plain(text), marks, note=True)


def lines(text: str) -> list[str]:
    """Divide a chord progression into its voices, from the lowest to the highest.

    Each chord must have the same number of notes. A single note or a rest
    goes to all voices. Each voice keeps the marks of the chords.
    """
    parsed = music.parse(text)
    sizes = {len(e.pitches) for e in _notes(parsed.children) if len(e.pitches) > 1}
    if len(sizes) > 1:
        raise ValueError(f"the chords have different numbers of notes: {sorted(sizes)}")
    count = sizes.pop() if sizes else 1
    result = []
    for index in range(count):
        voice = _pick(parsed.children, index)
        result.append(music.body_to_lilypond(music.Group("sequence", voice)))
    return result


def _notes(elements: list[music.Element]) -> list[music.Note]:
    found: list[music.Note] = []
    for element in elements:
        if isinstance(element, music.Note):
            found.append(element)
        elif isinstance(element, music.Group):
            found.extend(_notes(element.children))
    return found


def _pick(elements: list[music.Element], index: int) -> list[music.Element]:
    result: list[music.Element] = []
    for element in elements:
        if isinstance(element, music.Note):
            pitch = element.pitches[index if len(element.pitches) > 1 else 0]
            result.append(replace(element, pitches=[pitch], chord=False))
        elif isinstance(element, music.Group):
            result.append(replace(element, children=_pick(element.children, index)))
        else:
            result.append(element)
    return result


_PLACEHOLDER = re.compile(r"(?<![A-Za-z\\\"])([A-HX])([',]*)(?![A-Za-z\"])")


def _shifted(pitch: Pitch, marks: str) -> str:
    moved = replace(pitch, octave=pitch.octave + marks.count("'") - marks.count(","))
    return moved.name


def fill(chords: str, pattern: str) -> str:
    """Make a figure from each chord of a progression.

    In the pattern, the letters A to H are the notes of the chord from the
    lowest to the highest, and X is the full chord. A `'` or a `,` after a
    letter moves the note by an octave. The marks of each chord go on the
    first note of its figure. Rests and bar checks of the progression stay.
    """
    parsed = music.parse(chords)
    parts: list[str] = []
    for element in parsed.children:
        if isinstance(element, music.Note):
            pitches = [p.pitch for p in element.pitches]

            def substitute(match: re.Match[str], pitches: list[Pitch] = pitches) -> str:
                letter, marks = match.group(1), match.group(2)
                if letter == "X":
                    names = " ".join(_shifted(pitch, marks) for pitch in pitches)
                    return f"<{names}>"
                number = ord(letter) - ord("A")
                if number >= len(pitches):
                    raise ValueError(f"the chord has no note {letter}")
                return _shifted(pitches[number], marks)

            figure = music.parse(_PLACEHOLDER.sub(substitute, pattern))
            marks = [p for p in element.posts if p.kind in ("dynamic", "hairpin", "command")]
            target = _first_note(figure.children)
            if marks and target is not None:
                target.posts[:0] = marks
            parts.append(music.body_to_lilypond(figure))
        elif isinstance(element, music.Rest | music.BarCheck):
            parts.append(music.body_to_lilypond(music.Group("sequence", [element])))
        else:
            raise ValueError("fill() accepts only chords, rests, and bar checks")
    return " ".join(parts)


def put(section: Section, players: str, text: str, marks: str = "") -> None:
    """Write the same music for some players.

    `players` is a list of player identifiers with spaces between them. A
    number after a colon moves the music of that player by octaves, for
    example "fl1:1 ob1 bn1:-1". `marks` go on the first note of each player.
    """
    for entry in players.split():
        player, _, shift = entry.partition(":")
        music_text = octave(text, int(shift)) if shift else text
        if marks:
            music_text = first(music_text, marks, note=True)
        section.write(player, music_text)


def spread(section: Section, players: str, chords: str, marks: str = "") -> None:
    """Divide a chord progression between players: the first player gets the lowest voice."""
    names = players.split()
    voices = lines(chords)
    if len(voices) != len(names):
        raise ValueError(f"{len(voices)} voices for {len(names)} players")
    for entry, voice in zip(names, voices, strict=True):
        put(section, entry, voice, marks)


def _doubled(elements: list[music.Element], shift: int) -> list[music.Element]:
    result: list[music.Element] = []
    for element in elements:
        if isinstance(element, music.Note):
            extra = [
                replace(p, pitch=replace(p.pitch, octave=p.pitch.octave + shift), posts=[])
                for p in element.pitches
            ]
            pitches = extra + element.pitches if shift < 0 else element.pitches + extra
            result.append(replace(element, pitches=pitches, chord=True))
        elif isinstance(element, music.Group):
            result.append(replace(element, children=_doubled(element.children, shift)))
        else:
            result.append(element)
    return result


def double(text: str, shift: int = -1) -> str:
    """Return the music in octaves: each note gets a second note `shift` octaves from it."""
    parsed = music.parse(text)
    return music.body_to_lilypond(music.Group("sequence", _doubled(parsed.children, shift)))


def bars(count: int, rest: str, entries: dict[int, str]) -> str:
    """Return `count` bars: the music of `entries` (bar number: music), and rests.

    `rest` is the full-bar rest of the metre, for example "R1*7/8 |".
    """
    return " ".join(entries.get(number, rest) for number in range(1, count + 1))


class Block:
    """Collect the music of a section phrase by phrase, then write it.

    A section has one or more phrases. For each phrase, the composer gives
    the music of some players. A player with no music in a phrase gets the
    rest of that phrase.
    """

    def __init__(self, section: Section, *phrase_rests: str) -> None:
        self.section = section
        self.phrase_rests = phrase_rests
        self.music: dict[str, dict[int, str]] = {}

    def add(self, players: str, phrase: int, text: str, marks: str = "") -> None:
        """Give the music of some players for one phrase (the first phrase is 1).

        `players` and `marks` are the same as for `put()`.
        """
        if not 1 <= phrase <= len(self.phrase_rests):
            raise ValueError(f"the section has no phrase {phrase}")
        for entry in players.split():
            player, _, shift = entry.partition(":")
            music_text = octave(text, int(shift)) if shift else text
            if marks:
                music_text = first(music_text, marks, note=True)
            phrases = self.music.setdefault(player, {})
            if phrase in phrases:
                raise ValueError(f"{player}: music written two times for phrase {phrase}")
            phrases[phrase] = music_text

    def spread(self, players: str, phrase: int, chords: str, marks: str = "") -> None:
        """Divide a chord progression between players: the first player gets the lowest voice."""
        names = players.split()
        voices = lines(chords)
        if len(voices) != len(names):
            raise ValueError(f"{len(voices)} voices for {len(names)} players")
        for entry, voice in zip(names, voices, strict=True):
            self.add(entry, phrase, voice, marks)

    def start(self, player: str, prefix: str) -> None:
        """Put a command (for example a change of instrument) before the music of a player."""
        phrases = self.music.setdefault(player, {})
        phrases[1] = prefix + " " + phrases.get(1, self.phrase_rests[0])

    def close(self) -> None:
        """Write the music of all players and close the section."""
        for player, phrases in self.music.items():
            text = " ".join(
                phrases.get(number, rest) for number, rest in enumerate(self.phrase_rests, start=1)
            )
            self.section.write(player, text)
        self.section.close()


_REST_NAMES = {
    Fraction(4): "1",
    Fraction(2): "2",
    Fraction(1): "4",
    Fraction(1, 2): "8",
    Fraction(1, 4): "16",
    Fraction(1, 8): "32",
}


def _rests_between(
    start: Fraction, end: Fraction, bar: Fraction, beat: Fraction, metre: str
) -> str:
    """Return rests from `start` to `end` (quarter notes). Each bar ends with a bar check."""
    parts: list[str] = []
    position = start
    while position < end:
        in_bar = position % bar
        if in_bar == 0 and end - position >= bar:
            count = (end - position) // bar
            parts.append(f"R1*{metre}*{count} |" if count > 1 else f"R1*{metre} |")
            position += count * bar
            continue
        bar_end = position - in_bar + bar
        limit = min(end, bar_end)
        for value in _REST_NAMES:
            fits = in_bar % value == 0 and position + value <= limit
            # A rest longer than one beat starts on a beat.
            if fits and (value <= beat or in_bar % beat == 0):
                parts.append(f"r{_REST_NAMES[value]}")
                position += value
                break
        else:
            raise ValueError(f"no rest fits at {position} quarter notes")
        if position == bar_end:
            parts.append("|")
    return " ".join(parts)


def scatter(
    count: int, numerator: int, denominator: int, events: dict[tuple[int, float], str]
) -> str:
    """Return `count` bars with short figures at the given places, and rests between them.

    A key of `events` is (bar, beat). The bar is the bar number in the
    section (the first bar is 1). The beat is in quarter notes: 1 is the
    start of the bar, 1.5 is one eighth note later. The first note of each
    figure must have a duration.
    """
    bar = Fraction(4 * numerator, denominator)
    beat = Fraction(4, denominator)
    metre = f"{numerator}/{denominator}"
    total = count * bar
    placed = sorted(
        ((number - 1) * bar + Fraction(position - 1).limit_denominator(8), text)
        for (number, position), text in events.items()
    )
    parts: list[str] = []
    cursor = Fraction(0)
    for start, text in placed:
        if start < cursor:
            raise ValueError(f"two figures at the same time ({float(start)} quarter notes)")
        parts.append(_rests_between(cursor, start, bar, beat, metre))
        parts.append(text.strip())
        cursor = start + music.length(music.parse(text))
        if cursor % bar == 0 and not text.strip().endswith("|"):
            parts.append("|")
    if cursor > total:
        raise ValueError("the last figure is longer than the section")
    parts.append(_rests_between(cursor, total, bar, beat, metre))
    return " ".join(part for part in parts if part)
