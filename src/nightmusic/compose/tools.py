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
