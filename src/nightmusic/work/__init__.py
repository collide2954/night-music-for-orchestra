"""The work: Night Music for Orchestra, written as code."""

from __future__ import annotations

from ..notation.work import Work, load_orchestra
from . import part1, part2, part3, part4, part5

TITLE = "Night Music for Orchestra"
COMPOSER = "Brett Gilio"


def build() -> Work:
    """Build the full work from its parts."""
    work = Work(TITLE, load_orchestra(), composer=COMPOSER)
    part1.write(work)
    part2.write(work)
    part3.write(work)
    part4.write(work)
    part5.write(work)
    _inflections(work)
    work.check_complete()
    return work


# The ends of the phrases where the tempo goes slower for a short time: the
# rehearsal mark of the section, the bar in the section (1 = its first bar),
# the beat where the change starts, and the tempo at the end of the bar.
RITARDANDI = [
    ("A", 12, 3, 38),  # part 1: the end of the long song
    ("F", 8, 3, 52),  # part 2: the end of the song theme
    ("O", 8, 3, 50),  # part 2: the song theme in B minor
    ("X", 8, 3, 44),  # part 4: the warm theme, the first time
    ("Y", 20, 3, 56),  # part 4: the song theme in F-sharp major
    ("Z", 16, 3, 50),  # part 4: the warm theme in B-flat major
    ("CC", 8, 3, 44),  # part 4: the solo of the violin
    ("CC", 16, 3, 44),  # part 4: the solo of the horn
    ("EE", 8, 3, 52),  # part 5: the themes together, the first time
]


# The fermatas at the ends of the parts: the mark after the bar that has the
# fermata, and the time in seconds that the fermata adds to the bar.
FERMATAS = [
    ("D", 3.0),  # the end of part 1: the note A
    ("S", 3.0),  # the end of part 2: the note A-flat
    ("W", 3.0),  # the end of part 3: E-flat minor
    ("DD", 3.0),  # the end of part 4: D major, very soft
]
LAST_FERMATA = 5.0  # the last chord of the work


def _inflections(work: Work) -> None:
    """Add the small changes of tempo at the ends of phrases."""
    structure = work.structure
    marks = {label: bar for bar, label in structure.marks.items()}
    for label, number, beat, slow in RITARDANDI:
        structure.ritardando(marks[label] + number - 1, beat, slow)
    # The end of the warm theme (second time): the tempo of the subsequent section follows.
    structure.ritardando(marks["X"] + 15, 3, 44, resume="")
    # The fermatas: the last bar before each of these marks, and the last bar of the work.
    for label, seconds in FERMATAS:
        structure.fermata(marks[label] - 1, seconds)
    structure.fermata(len(structure.bars), LAST_FERMATA)
