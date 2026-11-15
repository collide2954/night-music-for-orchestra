"""Tests for the muscript parser."""

from fractions import Fraction

from nightmusic.study import muscript

EXAMPLE = """\
title Example
/
2 bars | 1b 4/4 1 | 1 |
| 4/4 6.0
b0.5 .02 Sehr langsam
=1' treble 1b 4/4 4 c 8. [b 16 a] 2 <F A c(1>
I0.5 .02 pp .80 f
=2, bass 1b 4/4 2 d D
| 3.0 1.0
=1' 2 <F A c)1> 83 [c# c d] 4 rest
=2, 1 D_
"""


def test_bars_and_timing():
    score = muscript.parse(EXAMPLE)
    assert len(score.bars) == 2
    assert score.bars[0].time_signature == (4, 4)
    assert score.bars[0].duration_seconds == 6.0
    assert score.bars[0].quarter_bpm == 40.0
    assert score.bars[1].seconds == (3.0, 1.0)
    assert score.bars[1].start == Fraction(4)
    assert score.duration_seconds == 10.0
    assert score.warnings == []


def test_pitches_follow_clef_and_key_signature():
    score = muscript.parse(EXAMPLE)
    upper = [n for n in score.notes if n.stave == 1 and n.bar == 1]
    # Treble clef: c is C5. The key signature has one flat, thus b is B-flat.
    assert [n.midi for n in upper[:3]] == [72, 82, 81]
    lower = [n for n in score.notes if n.stave == 2]
    # Bass clef: d is D3, D is D2, D_ is D1.
    assert [n.midi for n in lower] == [50, 38, 26]


def test_tie_joins_two_notes():
    score = muscript.parse(EXAMPLE)
    tied = [n for n in score.notes if n.midi == 72 and n.start == Fraction(2)]
    assert len(tied) == 1
    assert tied[0].duration == Fraction(4)


def test_accidental_stays_in_effect_to_the_end_of_the_bar():
    score = muscript.parse(EXAMPLE)
    triplet = [n for n in score.notes if n.bar == 2 and n.duration == Fraction(1, 3)]
    # c-sharp, then c with no sign (still c-sharp), then d.
    assert [n.midi for n in triplet] == [73, 73, 74]


def test_text_marks():
    score = muscript.parse(EXAMPLE)
    marks = [(m.font, m.x, m.text) for m in score.bars[0].texts]
    assert ("b", 0.02, "Sehr langsam") in marks
    assert ("I", 0.02, "pp") in marks
    assert ("I", 0.80, "f") in marks


def test_rhythm_tokens():
    assert muscript.parse_rhythm("4") == (Fraction(1), False)
    assert muscript.parse_rhythm("8.") == (Fraction(3, 4), False)
    assert muscript.parse_rhythm("4..") == (Fraction(7, 4), False)
    assert muscript.parse_rhythm("83") == (Fraction(1, 3), False)
    assert muscript.parse_rhythm("165") == (Fraction(1, 5), False)
    assert muscript.parse_rhythm("163-s") == (Fraction(1, 6), True)
    assert muscript.parse_rhythm("bass") is None
