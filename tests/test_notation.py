"""Tests for the music language, the structure, and the LilyPond writer."""

import re
import shutil
import subprocess
from fractions import Fraction

import pytest

from nightmusic.notation import lilypond, music
from nightmusic.notation.pitch import Interval, Pitch, from_midi
from nightmusic.notation.structure import Structure, global_to_lilypond
from nightmusic.notation.work import Work, WorkError, load_orchestra


def test_pitch_names_and_midi():
    assert Pitch.parse("c'").midi == 60
    assert Pitch.parse("bes,").midi == 46
    assert Pitch.parse("fis''").midi == 78
    assert Pitch.parse("es'").midi == 63
    assert Pitch.parse("as").midi == 56
    assert Pitch.parse("deh'").midi == 61.5
    assert Pitch.parse("cih'").midi == 60.5
    for name in ["c'", "bes,", "fis''", "es'", "as", "deh'", "eeseh", "aisis,,", "eeh'"]:
        assert Pitch.parse(name).name == name
    assert from_midi(61).name == "des'"
    assert from_midi(61, prefer_sharps=True).name == "cis'"
    assert from_midi(60.5).midi == 60.5


def test_transposition_gives_a_good_spelling():
    major_second = Interval(1, 2)
    fifth = Interval(4, 7)
    assert Pitch.parse("bes").transposed(major_second).name == "c'"
    assert Pitch.parse("cis'").transposed(major_second).name == "dis'"
    assert Pitch.parse("a").transposed(fifth).name == "e'"
    # A-sharp up a major second is B-sharp. The simple spelling is C.
    assert Pitch.parse("ais").transposed(major_second).simplified().name == "c'"
    assert Pitch.parse("deh'").transposed(major_second).name == "eeh'"


def test_parser_reads_durations_and_events():
    parsed = music.parse(r"""d'4\pp( e'8. f'16) <g' b'>2-> ~ | <g' b'>1\fermata |""")
    notes = [e for e in parsed.children if isinstance(e, music.Note)]
    assert [n.duration for n in notes] == [1, Fraction(3, 4), Fraction(1, 4), 2, 4]
    assert notes[0].posts[0].kind == "dynamic" and notes[0].posts[0].value == "pp"
    assert notes[3].chord and [p.pitch.midi for p in notes[3].pitches] == [67, 71]
    assert [p.kind for p in notes[3].posts] == ["articulation", "tie"]
    assert music.length(parsed) == 8


def test_parser_handles_groups():
    parsed = music.parse(
        r"""\tuplet 3/2 { c'8 d' e' } \grace { f'16 g' } a'4 << { c''2 } \\ { e'4 f' } >>"""
    )
    assert music.length(parsed) == 4
    assert music.length(music.parse(r"\repeat tremolo 8 { c'16 e' }")) == 4
    assert music.length(music.parse(r"R1*3/4 R1*4")) == 19
    # A duration with a multiplier does not change the duration of the subsequent notes.
    assert music.length(music.parse(r"s4*5 c'")) == 6


def test_parser_reports_errors():
    with pytest.raises(music.MusicSyntaxError):
        music.parse(r"c'4 \unknowncommand d'4")
    with pytest.raises(music.MusicSyntaxError):
        music.length(music.parse(r"<< { c'2 } \\ { c'4 } >>"))


def test_output_is_the_same_music():
    text = r"""d'4\pp( e'8. f'16) <g' b'>2->~ |
\tuplet 3/2 { c'8 d' e' } r4 r2\fermata |"""
    parsed = music.parse(text)
    again = music.parse(music.body_to_lilypond(parsed))
    assert music.body_to_lilypond(again) == music.body_to_lilypond(parsed)
    transposed = music.body_to_lilypond(parsed, Interval(1, 2))
    assert transposed.startswith("e'4\\pp( fis'8. g'16) <a' cis''>2->~")


def test_structure_times():
    structure = Structure()
    structure.add_bars(4, 4, 4)
    structure.add_bars(2, 7, 8, (2, 2, 3))
    structure.tempo(1, 1, 60, "Lento")
    assert structure.length == 23
    assert structure.position(2, 3) == 6
    assert structure.position(5, 3) == 17
    assert structure.seconds(Fraction(16)) == pytest.approx(16.0)
    # A gradual change from 60 to 120 in bars 3 and 4.
    structure.change(3, 1, "accel.")
    structure.tempo(5, 1, 120, "Allegro")
    assert structure.bpm_at(Fraction(12)) == pytest.approx(90.0)
    assert structure.seconds(Fraction(16)) == pytest.approx(8.0 + 8 * 0.6931, rel=1e-3)
    text = global_to_lilypond(structure)
    assert "\\time 2,2,3 7/8" in text
    assert '\\tempo "Lento" 4 = 60' in text
    assert "s1*2 " in text  # bars 1 and 2 are one spacer rest


def _small_work() -> Work:
    work = Work("Test", load_orchestra())
    section = work.section(2, 4, 4)
    work.structure.tempo(1, 1, 60, "Lento")
    section.write("cl1", r"""R1 | d'2\p( e'2) |""")
    section.write("vc", r"""d1\pp ~ | d1 |""")
    section.close()
    return work


def test_section_checks_the_length_and_the_bar_lines():
    work = _small_work()
    work.check_complete()
    section = work.section(1, 3, 4)
    with pytest.raises(WorkError, match="quarter notes"):
        section.write("vc", r"d1 |")
    with pytest.raises(WorkError, match="bar check"):
        work.section(2, 4, 4).write("vc", r"d2. | d4 d1 |")


def test_score_and_part_text():
    work = _small_work()
    score = lilypond.score_file(work)
    assert "Score in C" in score
    assert "musicClA = { \\clef treble R1*1 | d'2\\p( e'2) |" in " ".join(score.split())
    part = lilypond.part_file(work, "cl1")
    assert "Clarinet 1 in B-flat" in part
    assert "e'2\\p( fis'2)" in part  # the part is a major second higher
    assert "R1*2 |" in lilypond.part_file(work, "fl1")  # two empty bars are one rest


@pytest.mark.skipif(shutil.which("lilypond") is None, reason="LilyPond is not installed")
def test_lilypond_compiles_the_files(tmp_path):
    work = _small_work()
    paths = lilypond.write_all(work, tmp_path)
    for name in ["score.ly", "part-cl1.ly", "part-harp.ly"]:
        result = subprocess.run(
            ["lilypond", "-dno-point-and-click", "--loglevel=ERROR", name],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
    assert len(paths) == 45
    assert (tmp_path / "score.pdf").exists()


def test_the_notes_of_the_score_have_the_bar_numbers_of_the_music():
    from nightmusic.work import build

    work = build()
    marks = {label: number for number, label in work.structure.marks.items()}
    notes = " ".join(lilypond.score_notes(work))
    # The harmonic series on D is the section at the mark GG.
    assert f"the woodwinds (bars {marks['GG']} to {marks['HH'] - 1})" in notes
    # The ocarinas play in the night music only: between the mark S and the mark W.
    found = re.search(r"an ocarina in C \(bars (\d+) to (\d+)\)", notes)
    assert found is not None
    assert marks["S"] <= int(found[1]) < int(found[2]) < marks["W"]
    assert f"Duration: {round(work.structure.duration_seconds / 60)} minutes." in notes
    # A work with no quarter-tones and no ocarinas has no notes about them.
    small = " ".join(lilypond.score_notes(_small_work()))
    assert "Quarter-tones" not in small
    assert "ocarina" not in small


def test_three_quarter_flat_names_are_valid_in_lilypond():
    from fractions import Fraction

    from nightmusic.notation.pitch import Interval, Pitch

    low = Pitch.parse("beseh'").transposed(Interval(3, 5))  # a fourth higher
    assert low.alter == Fraction(-3, 2)
    assert low.name == "eeseh''"
    assert Pitch.parse("es'").name == "es'"
    assert Pitch.parse("aeseh").name == "aeseh"


def test_a_fermata_adds_time_to_the_end_of_a_bar():
    from nightmusic.notation.structure import Structure

    structure = Structure()
    structure.add_bars(3, 4, 4)
    structure.tempo(1, 1, 60, "Lento")
    structure.fermata(2, 3.0)
    assert structure.seconds(structure.bar(2).start) == pytest.approx(4.0)
    assert structure.seconds(structure.bar(3).start) == pytest.approx(11.0)  # 4 s and 3 s more
    assert structure.seconds(structure.length) == pytest.approx(15.0)  # the tempo comes back
    # A gradual change of tempo before the fermata keeps its own speed.
    slower = Structure()
    slower.add_bars(3, 4, 4)
    slower.tempo(1, 1, 60, "Lento")
    slower.change(1, 1, "rit.")
    slower.tempo(3, 1, 30, "Largo")
    plain = slower.seconds(slower.bar(2).start)
    slower.fermata(2, 3.0)
    assert slower.seconds(slower.bar(2).start) == pytest.approx(plain)
