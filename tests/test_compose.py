"""Tests for the tools of the composer."""

from nightmusic.compose.tools import (
    Block,
    bars,
    double,
    dyn,
    fill,
    first,
    invert,
    lines,
    octave,
    times,
    tr,
)
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


def _flat(text: str) -> str:
    return " ".join(text.split())


def test_first_puts_marks_on_the_first_rest_or_note():
    assert _flat(first(r"r8 d8( es4)", r"\senzasord")) == r"r8\senzasord d8( es4)"
    assert _flat(first(r"r8 d8( es4)", r"\pp", note=True)) == r"r8 d8\pp( es4)"


def test_dyn_replaces_the_dynamic_marks():
    assert _flat(dyn(r"d4\mf\< e4 f2\f", r"\pp")) == r"d4\pp e4 f2"


def test_lines_divides_chords_into_voices():
    low, high = lines(r"<d a>1\p( <c bes>1) | r1 |")
    assert _flat(low) == r"d1\p( c1) | r1 |"
    assert _flat(high) == r"a1\p( bes1) | r1 |"


def test_fill_makes_a_figure_from_each_chord():
    figure = fill(r"<c e g>1\p <d f a>1", r"A8 B C B A' X4. |")
    assert _flat(figure) == r"c8\p e g e c' <c e g>4. | d8 f a f d' <d f a>4. |"


def test_double_adds_the_octave():
    assert _flat(double(r"c4 d", -1)) == r"<c, c>4 <d, d>"
    assert _flat(double(r"c4", 1)) == r"<c c'>4"


def test_bars_puts_music_in_the_named_bars():
    assert bars(3, "R1 |", {2: "c1 |"}) == "R1 | c1 | R1 |"


def test_block_writes_phrases_and_rests():
    from nightmusic.notation.work import Work, load_orchestra

    work = Work("Test", load_orchestra())
    section = work.section(4, 4, 4)
    block = Block(section, "R1*2 |", "R1*2 |")
    block.add("fl1 ob1:-1", 2, r"c''1 | d''1 |", r"\p")
    block.spread("hn2 hn1", 1, r"<c' e'>1 | <d' f'>1 |")
    block.close()
    work.check_complete()
    assert _flat(music.body_to_lilypond(work.music_of("ob1"))) == r"R1*2 | c'1\p | d'1 |"
    assert _flat(music.body_to_lilypond(work.music_of("hn1"))) == r"e'1 | f'1 | R1*2 |"


def test_a_repeated_dynamic_mark_shows_one_time():
    from nightmusic.notation.work import Work, load_orchestra

    work = Work("Test", load_orchestra())
    section = work.section(2, 4, 4)
    section.write("fl1", times(r"c''4\p d''4 e''2 |", 2))
    section.close()
    assert _flat(music.body_to_lilypond(work.music_of("fl1"))).count(r"\p") == 1


def test_the_work_has_no_notes_out_of_range():
    from nightmusic.compose.check import check
    from nightmusic.work import build

    assert [str(problem) for problem in check(build())] == []
