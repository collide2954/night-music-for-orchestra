"""Find music that a player cannot play.

The checks are:

- Each note must be in the range of the instrument.
- A wind instrument plays one note at a time.
- A player who changes to a different instrument must have the time to do it.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from ..notation.pitch import from_midi
from ..notation.work import Work
from ..perform.events import PerfNote, perform

ONE_NOTE_FAMILIES = ("woodwinds", "brass")

# The smallest time in seconds for a change of instrument.
CHANGE_SECONDS = {"percussion": 4.0}
CHANGE_SECONDS_DEFAULT = 8.0


@dataclass(frozen=True)
class Problem:
    """One problem in the music of a player."""

    player: str
    bar: int
    text: str

    def __str__(self) -> str:
        return f"{self.player}, bar {self.bar}: {self.text}"


def _free_after(note: PerfNote, percussion: bool) -> Fraction:
    """Return the time (in quarter notes) at which the player is free after a note.

    A percussion player is free immediately after a stroke: the instrument
    continues to sound without the player. A roll occupies the player to
    its end.
    """
    if percussion and not note.tremolo:
        return note.start
    return note.start + note.duration


def check(work: Work) -> list[Problem]:
    """Return the problems in the work, in the sequence of the score."""
    problems: list[Problem] = []
    structure = work.structure
    for player in work.orchestra.players:
        seen: set[tuple[int, str]] = set()
        percussion = player.family == "percussion"
        smallest = CHANGE_SECONDS.get(player.family, CHANGE_SECONDS_DEFAULT)
        last_instrument = ""
        free = Fraction(0)
        for note in sorted(perform(work, player.id), key=lambda item: item.start):
            bar = structure.bar_at(note.start).number
            if last_instrument and note.instrument != last_instrument:
                seconds = structure.seconds(note.start) - structure.seconds(free)
                if seconds < smallest:
                    text = (
                        f"only {max(seconds, 0.0):.1f} s for the change from the "
                        f"{last_instrument} to the {note.instrument}"
                    )
                    problems.append(Problem(player.id, bar, text))
                free = Fraction(0)
            last_instrument = note.instrument
            free = max(free, _free_after(note, percussion))
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
