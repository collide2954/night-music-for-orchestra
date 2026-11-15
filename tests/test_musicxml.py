"""Tests for the MusicXML file and for the MuseScore steps that need no program."""

import xml.etree.ElementTree as ElementTree
from fractions import Fraction

from nightmusic.audio import musescore
from nightmusic.notation import musicxml
from nightmusic.notation.work import Work, load_orchestra


def _small_work() -> Work:
    work = Work("Test", load_orchestra())
    section = work.section(2, 4, 4)
    work.structure.tempo(1, 1, 60, "Lento")
    work.structure.change(2, 1, "rit.")
    section.write("fl1", r"c''4\p\<( d''8 e''8) \tuplet 3/2 { f''8 g'' a'' } r4 | c'''1\f ~ |")
    section.write("vn1", r"<d' a'>2\pp\pizz r2 | d''1:32\arco |")
    section.write("perc1", r"""\switch "tam-tams" c'1\p | R1 |""")
    section.close()
    section = work.section(1, 3, 4)
    work.structure.tempo(3, 1, 40, "Largo")
    section.write("fl1", r"c'''2. |")
    section.close()
    return work


def test_the_file_is_xml_and_has_one_part_for_each_instrument():
    text, names = musicxml.score(_small_work())
    root = ElementTree.fromstring(text.split("\n", 2)[2])
    assert names == ["Flute (fl1)", "Violins (vn1)"]  # MuseScore does not play the tam-tam
    assert [len(part.findall("measure")) for part in root.findall("part")] == [3, 3]


def test_each_bar_of_each_voice_has_the_length_of_the_bar():
    text, _names = musicxml.score(_small_work())
    root = ElementTree.fromstring(text.split("\n", 2)[2])
    for part in root.findall("part"):
        for measure, quarters in zip(part.findall("measure"), [4, 4, 3], strict=True):
            position, longest = 0, 0
            for element in measure:
                if element.tag == "backup":
                    position -= int(element.findtext("duration"))
                elif element.tag == "forward" or (
                    element.tag == "note"
                    and element.find("chord") is None
                    and element.find("grace") is None
                ):
                    position += int(element.findtext("duration"))
                longest = max(longest, position)
            assert longest == quarters * musicxml.DIVISIONS


def test_the_tempo_points_keep_the_time_of_the_tempo_plan():
    work = _small_work()
    structure = work.structure
    points = musicxml._tempo_points(work, Fraction(0), structure.length)
    places = sorted(points) + [structure.length]
    seconds = sum(
        60.0 * float(end - start) / points[start]
        for start, end in zip(places[:-1], places[1:], strict=True)
    )
    assert abs(seconds - structure.duration_seconds) < 1e-6
    assert len(points) > 3  # the gradual change has a point at each quarter note


def test_marks_of_the_notes():
    text, _names = musicxml.score(_small_work())
    assert '<wedge type="crescendo"/>' in text and '<wedge type="stop"/>' in text
    assert "<dynamics><p/></dynamics>" in text and "<dynamics><f/></dynamics>" in text
    assert '<tremolo type="single">3</tremolo>' in text
    assert 'pizzicato="yes"' in text and 'pizzicato="no"' in text
    assert "<actual-notes>3</actual-notes><normal-notes>2</normal-notes>" in text
    assert '<tie type="start"/>' in text and '<tie type="stop"/>' in text


def test_staff_texts_of_techniques_become_playing_techniques():
    before = (
        "<StaffText>\n  <eid>x</eid>\n  <text>sul pont.</text>\n  </StaffText>"
        "<StaffText>\n  <text>dolce</text>\n  </StaffText>"
    )
    after, count = musescore.play_techniques(before)
    assert count == 1
    assert "<playTechType>sul_ponticello</playTechType>" in after
    assert "<StaffText>\n  <text>dolce</text>" in after
