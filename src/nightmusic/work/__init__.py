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
    work.check_complete()
    return work
