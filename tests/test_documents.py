from nightmusic import documents
from nightmusic.compose.stats import measure
from nightmusic.work import build


def test_clock():
    assert documents.clock(0.4) == "0:00"
    assert documents.clock(453.9) == "7:33"


def test_the_sections_of_the_marks_cover_all_bars():
    work = build()
    parts = documents.sections(work)
    assert parts[""][0] == 1
    assert max(last for _, last in parts.values()) == len(work.structure.bars)
    bars = sorted(parts.values())
    for (_, last), (first, _) in zip(bars, bars[1:], strict=False):
        assert first == last + 1


def test_the_documents_have_the_numbers_of_the_music():
    """If this test fails, run `uv run nightmusic docs`."""
    work = build()
    stats = measure(work)
    for path in documents.FILES:
        text = path.read_text(encoding="utf-8")
        assert documents.update(path, text, work, stats) == text, path.name


def test_the_style_study_has_the_values_of_the_work(tmp_path, monkeypatch):
    """If this test fails, run `uv run nightmusic docs`."""
    from nightmusic.study import report, workcheck

    kept = documents.ROOT / "research" / "measured"
    monkeypatch.setattr(workcheck, "OUTPUT_DIR", tmp_path)
    for path in workcheck.write_tables(build()):
        assert path.read_text(encoding="utf-8") == (kept / path.name).read_text(encoding="utf-8")
    study = documents.ROOT / "docs" / "style-study.md"
    assert report.build() == study.read_text(encoding="utf-8")


def test_repetition_of_a_small_example():
    from fractions import Fraction

    from nightmusic.study.workcheck import REPETITION_MEASURES, repetition

    one = Fraction(1)
    # Four bars of one voice: bar 2 is the same as bar 1, bar 3 is one tone higher, bar 4 is new.
    notes = []
    for bar, pitches in ((1, (60, 62)), (2, (60, 62)), (3, (62, 64)), (4, (60, 67, 72))):
        notes += [(bar, "voice", index * one, one, midi) for index, midi in enumerate(pitches)]
    values = repetition(notes)
    assert values[REPETITION_MEASURES[0]] == 0.25  # bar 2
    assert values[REPETITION_MEASURES[1]] == 0.25  # bar 2
    assert values[REPETITION_MEASURES[2]] == 0.25  # bar 3
    assert values[REPETITION_MEASURES[4]] == 0.25
    assert values[REPETITION_MEASURES[6]] == 0.0
