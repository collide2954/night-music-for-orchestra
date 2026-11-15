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


# The ends of the phrases where the tempo goes slower for a short time:
# the bar, the beat where the change starts, and the tempo at the end of the bar.
RITARDANDI = [
    (20, 3, 38),  # part 1: the end of the long song
    (70, 3, 52),  # part 2: the end of the song theme
    (170, 3, 50),  # part 2: the song theme in B minor
    (274, 3, 44),  # part 4: the warm theme, the first time
    (302, 3, 56),  # part 4: the song theme in F-sharp major
    (322, 3, 50),  # part 4: the warm theme in B-flat major
    (378, 3, 44),  # part 4: the solo of the violin
    (386, 3, 44),  # part 4: the solo of the horn
    (416, 3, 52),  # part 5: the themes together, the first time
]


def _inflections(work: Work) -> None:
    """Add the small changes of tempo at the ends of phrases."""
    structure = work.structure
    for bar, beat, slow in RITARDANDI:
        structure.ritardando(bar, beat, slow)
    # The end of the warm theme (second time): the tempo of the subsequent section follows.
    structure.ritardando(282, 3, 44, resume="")
