"""Tests for the piano that the project renders with the Salamander samples."""

import numpy as np
import pytest

from nightmusic.audio import dsp, piano
from nightmusic.notation.work import Work, load_orchestra


def _piano_work() -> Work:
    """Three bars at 60 quarter notes in a minute: one bar is 4 s."""
    work = Work("Test", load_orchestra())
    section = work.section(3, 4, 4)
    work.structure.tempo(1, 1, 60, "Lento")
    section.write("pno.rh", r"c''8-.\mf r8 r4 r2 | c''8-.\ff r8 r4 r2 | R1 |")
    section.write("pno.lh", r"R1 | c2\ff\sustainOn r2 | r2\sustainOff r2 |")
    section.close()
    return work


def test_each_dynamic_mark_has_its_own_velocity_and_level_of_the_samples():
    marks = {"ppp": 0.18, "pp": 0.27, "p": 0.38, "mp": 0.49, "mf": 0.59, "f": 0.71, "ff": 0.83}
    values = [piano.velocity(level) for level in marks.values()]
    assert values == sorted(set(values))  # each mark is louder than the mark before it
    assert piano.velocity(0.0) == 1 and piano.velocity(1.5) == 127
    assert piano.velocity(0.59, accent=0.2) > piano.velocity(0.59)
    layers = [piano._layer(value) for value in values]
    assert layers == sorted(layers) and layers[0] == 1 and layers[-1] >= 13
    assert [piano._layer(value) for value in (1, 26, 27, 127)] == [1, 1, 2, 16]
    # A soft note is much softer than a loud note: more than the samples give.
    assert piano._gain(48) < 0.35 * piano._gain(94)


def test_the_names_of_the_sampled_keys_are_those_of_the_library():
    names = [piano._Library.name(centre) for centre in piano.CENTRES]
    assert names[:5] == ["A0", "C1", "D#1", "F#1", "A1"]
    assert names[-1] == "C8" and len(names) == 30


def test_the_pedal_and_the_short_notes_of_the_score_control_the_dampers():
    work = _piano_work()
    assert piano.pedal_spans(work) == [(4.0, 8.0)]
    notes = piano.notes_of(work)
    # A staccato note: the key goes up after a short time.
    start, key_up, midi, _value = notes[0]
    assert (start, midi) == (0.0, 72) and key_up - start <= piano.STACCATO_SECONDS
    # The low strings need more time to stop than the high strings.
    assert piano._damp_seconds(30) > piano._damp_seconds(60) > piano._damp_seconds(85)


@pytest.mark.skipif(not piano.available(), reason="the samples are not on this computer")
def test_a_note_with_the_pedal_sounds_longer_than_a_note_with_no_pedal():
    audio = piano.render(_piano_work(), 0.0, 12.0).mean(axis=1)

    def level(second: float) -> float:
        part = audio[int(second * dsp.RATE) : int((second + 0.5) * dsp.RATE)]
        return float(20 * np.log10(np.sqrt(np.mean(np.square(part))) + 1e-9))

    assert level(0.0) > -40.0  # the first note sounds
    assert level(1.0) < -80.0  # no pedal: the damper stopped it
    assert level(6.0) > -45.0  # the pedal holds the second bar
    assert level(11.0) < level(6.0) - 30.0  # after the pedal goes up, the sound stops
    assert level(4.0) > level(0.0) + 3.0  # ff is louder than mf
