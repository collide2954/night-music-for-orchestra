"""Find music that a player cannot play.

The checks are:

- Each note must be in the range of the instrument.
- A wind instrument plays one note at a time.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..notation.pitch import from_midi
from ..notation.work import Work
from ..perform.events import perform

ONE_NOTE_FAMILIES = ("woodwinds", "brass")


@dataclass(frozen=True)
class Problem:
    """One problem in the music of a player."""

    player: str
    bar: int
    text: str

    def __str__(self) -> str:
        return f"{self.player}, bar {self.bar}: {self.text}"


def check(work: Work) -> list[Problem]:
    """Return the problems in the work, in the sequence of the score."""
    problems: list[Problem] = []
    structure = work.structure
    for player in work.orchestra.players:
        seen: set[tuple[int, str]] = set()
        for note in perform(work, player.id):
            bar = structure.bar_at(note.start).number
            instrument = work.orchestra.instruments.get(note.instrument)
            if instrument is not None and not note.harmonic:
                name = from_midi(note.midi).name
                if note.midi < instrument.low:
                    text = f"{name} is below the range of the {note.instrument}"
                elif note.midi > instrument.high:
                    text = f"{name} is above the range of the {note.instrument}"
                else:
                    text = ""
                if text and (bar, text) not in seen:
                    seen.add((bar, text))
                    problems.append(Problem(player.id, bar, text))
            if player.family in ONE_NOTE_FAMILIES and note.chord_size > 1:
                text = f"a chord for the {note.instrument}"
                if (bar, text) not in seen:
                    seen.add((bar, text))
                    problems.append(Problem(player.id, bar, text))
    return problems
