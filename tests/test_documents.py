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
