"""Change music text with code: transposition, inversion, and repetition.

These tools do the "developing variation" of the work. The composer writes a
theme one time. The tools make its other forms: at a different pitch, upside
down, or for a different instrument.
"""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

from ..notation import music
from ..notation.pitch import STEP_SEMITONES, Interval, Pitch


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
