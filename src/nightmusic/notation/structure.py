"""The structure of the work that all players share: bars, metres, tempo, and marks."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction


@dataclass
class Bar:
    """One bar. `start` and `length` are in quarter notes."""

    number: int
    start: Fraction
    numerator: int
    denominator: int
    grouping: tuple[int, ...] = ()  # beat groups of an uneven metre, for example (2, 2, 3)

    @property
    def length(self) -> Fraction:
        return Fraction(4 * self.numerator, self.denominator)

    @property
    def end(self) -> Fraction:
        return self.start + self.length


@dataclass
class TempoPoint:
    """A point of the tempo plan.

    `bpm` is the number of quarter notes in a minute at this point.
    If `glide` is true, the tempo changes in a straight line from this point to
    the subsequent point. If not, the tempo stays the same to the subsequent point.
    """

    position: Fraction
    bpm: float
    glide: bool = False
    text: str = ""  # the mark in the score; empty = no mark
    unit: str = ""  # note value of the metronome mark, for example "4" or "4."; empty = no number
    italic: bool = False


@dataclass
class Structure:
    """Bars, tempo plan, rehearsal marks, and double bar lines."""

    bars: list[Bar] = field(default_factory=list)
    tempo_points: list[TempoPoint] = field(default_factory=list)
    marks: dict[int, str] = field(default_factory=dict)  # bar number -> rehearsal mark
    double_bars: set[int] = field(default_factory=set)  # double bar line at the END of these bars
    breaks: set[int] = field(default_factory=set)  # line break at the END of these bars
    final_bar: bool = True

    # ------------------------------------------------------------ bars

    def add_bars(
        self, count: int, numerator: int, denominator: int, grouping: tuple[int, ...] = ()
    ) -> int:
        """Add bars at the end. Return the number of the first new bar."""
        first = len(self.bars) + 1
        for _ in range(count):
            start = self.bars[-1].end if self.bars else Fraction(0)
            self.bars.append(Bar(len(self.bars) + 1, start, numerator, denominator, grouping))
        return first

    def bar(self, number: int) -> Bar:
        return self.bars[number - 1]

    @property
    def length(self) -> Fraction:
        return self.bars[-1].end if self.bars else Fraction(0)

    def position(self, bar: int, beat: float | Fraction = 1) -> Fraction:
        """Return the position of a beat of a bar. Beat 1 is the start of the bar.

        The unit of the beat is the denominator of the time signature.
        """
        target = self.bar(bar)
        offset = (Fraction(beat) - 1) * Fraction(4, target.denominator)
        return target.start + offset

    def bar_at(self, position: Fraction) -> Bar:
        """Return the bar that contains a position."""
        low, high = 0, len(self.bars) - 1
        while low < high:
            middle = (low + high + 1) // 2
            if self.bars[middle].start <= position:
                low = middle
            else:
                high = middle - 1
        return self.bars[low]

    # ------------------------------------------------------------ tempo

    def tempo(
        self,
        bar: int,
        beat: float | Fraction,
        bpm: float,
        text: str = "",
        *,
        unit: str = "4",
        show_number: bool = True,
    ) -> None:
        """Set a new tempo at a point. `bpm` is for the note value `unit`."""
        quarter_bpm = bpm * float(_unit_quarters(unit))
        self._add(
            TempoPoint(
                self.position(bar, beat), quarter_bpm, False, text, unit if show_number else ""
            )
        )

    def change(self, bar: int, beat: float | Fraction, text: str) -> None:
        """Start a gradual tempo change (for example "rit." or "accel.").

        The tempo goes in a straight line to the tempo of the subsequent point.
        """
        position = self.position(bar, beat)
        self._add(TempoPoint(position, self.bpm_at(position), True, text, "", True))

    def arrive(self, bar: int, beat: float | Fraction, bpm: float, *, unit: str = "4") -> None:
        """End a gradual change at a tempo with no mark in the score."""
        quarter_bpm = bpm * float(_unit_quarters(unit))
        self._add(TempoPoint(self.position(bar, beat), quarter_bpm))

    def _add(self, point: TempoPoint) -> None:
        self.tempo_points = [p for p in self.tempo_points if p.position != point.position]
        self.tempo_points.append(point)
        self.tempo_points.sort(key=lambda p: p.position)

    def bpm_at(self, position: Fraction) -> float:
        """Return the tempo (quarter notes in a minute) at a position."""
        points = self.tempo_points
        if not points:
            return 60.0
        earlier = [p for p in points if p.position <= position]
        if not earlier:
            return points[0].bpm
        current = earlier[-1]
        later = [p for p in points if p.position > position]
        if current.glide and later:
            target = later[0]
            share = float(position - current.position) / float(target.position - current.position)
            return current.bpm + (target.bpm - current.bpm) * share
        return current.bpm

    def seconds(self, position: Fraction) -> float:
        """Return the time in seconds from the start of the work to a position."""
        points = self.tempo_points or [TempoPoint(Fraction(0), 60.0)]
        if points[0].position > 0:
            points = [TempoPoint(Fraction(0), points[0].bpm), *points]
        total = 0.0
        for index, point in enumerate(points):
            if point.position >= position:
                break
            following = points[index + 1] if index + 1 < len(points) else None
            end = min(position, following.position) if following else position
            quarters = float(end - point.position)
            if point.glide and following and following.bpm != point.bpm:
                span = float(following.position - point.position)
                end_bpm = point.bpm + (following.bpm - point.bpm) * quarters / span
                total += 60.0 * span / (following.bpm - point.bpm) * math.log(end_bpm / point.bpm)
            else:
                total += 60.0 * quarters / point.bpm
        return total

    @property
    def duration_seconds(self) -> float:
        return self.seconds(self.length)

    # ------------------------------------------------------------ marks

    def mark(self, bar: int, label: str) -> None:
        """Put a rehearsal mark at the start of a bar."""
        self.marks[bar] = label

    def double_bar(self, bar: int) -> None:
        """Put a double bar line at the end of a bar."""
        self.double_bars.add(bar)


def _unit_quarters(unit: str) -> Fraction:
    base = Fraction(4, int(unit.rstrip(".")))
    dots = unit.count(".")
    return base * (2 - Fraction(1, 2**dots))


def skip_text(quarters: Fraction) -> str:
    """Return a LilyPond spacer rest of a given length in quarter notes."""
    whole = quarters / 4
    if whole.denominator == 1:
        return f"s1*{whole.numerator}"
    return f"s1*{whole.numerator}/{whole.denominator}"


def global_to_lilypond(structure: Structure) -> str:
    """Write the structure as a LilyPond voice of spacer rests with all marks.

    One spacer rest goes from each mark to the subsequent mark. Thus the parts
    can show many empty bars as one rest with a number.
    """
    events: dict[Fraction, list[str]] = {}

    def add(position: Fraction, text: str) -> None:
        events.setdefault(position, []).append(text)

    previous: Bar | None = None
    for bar in structure.bars:
        if bar.number - 1 in structure.double_bars:
            add(bar.start, '\\bar "||"')
        if bar.number - 1 in structure.breaks:
            add(bar.start, "\\break")
        changed = previous is None or (
            (bar.numerator, bar.denominator, bar.grouping)
            != (previous.numerator, previous.denominator, previous.grouping)
        )
        if changed:
            if bar.grouping:
                groups = ",".join(str(g) for g in bar.grouping)
                add(bar.start, f"\\time {groups} {bar.numerator}/{bar.denominator}")
            else:
                add(bar.start, f"\\time {bar.numerator}/{bar.denominator}")
        if bar.number in structure.marks:
            add(bar.start, f'\\mark \\markup \\rehearsal "{structure.marks[bar.number]}"')
        previous = bar
    for point in structure.tempo_points:
        if point.text or point.unit:
            add(point.position, _tempo_text(point))
    add(structure.length, '\\bar "|."' if structure.final_bar else "")

    lines: list[str] = []
    positions = sorted(events)
    for index, position in enumerate(positions):
        commands = " ".join(text for text in events[position] if text)
        if index + 1 < len(positions):
            bar = structure.bar_at(position)
            skip = skip_text(positions[index + 1] - position)
            lines.append(f"{commands} {skip} % bar {bar.number}".strip())
        elif commands:
            lines.append(commands)
    return "\n".join(lines)


def _tempo_text(point: TempoPoint) -> str:
    if point.unit:
        quarters = _unit_quarters(point.unit)
        number = round(point.bpm / float(quarters))
        if point.text:
            return f'\\tempo "{point.text}" {point.unit} = {number}'
        return f"\\tempo {point.unit} = {number}"
    if point.italic:
        return f'\\tempo \\markup \\tempochange "{point.text}"'
    return f'\\tempo "{point.text}"'
