"""Tests for the tools of the composer."""

from nightmusic.compose.tools import invert, octave, times, tr
from nightmusic.notation import music


def test_transposition_keeps_the_rhythm_and_the_marks():
    theme = r"d4.\pp( es8 f4. g8 | as2.) r4 |"
    assert tr(theme, 5) == "g4.\\pp( as8 bes4. c'8 |\ndes'2.) r4 |"
    assert octave(theme, -1).startswith("d,4.\\pp( es,8")
    assert music.length(music.parse(tr(theme, 3))) == 8


def test_inversion_is_the_mirror_form():
    # The walking theme goes up from D to A-flat. Its mirror goes down from D to G-sharp.
    up = r"d4. es8 f4. g8 | as2. r4 |"
    assert invert(up, "d") == "d4. cis8 b,4. a,8 |\ngis,2. r4 |"
    # The mirror of the mirror is the first form.
    assert invert(invert(up, "d"), "d") == "d4. es8 f4. g8 |\nas2. r4 |"


def test_times():
    assert times("c'4 d'", 3) == "c'4 d' c'4 d' c'4 d'"
