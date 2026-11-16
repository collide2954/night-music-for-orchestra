"""Write the conductor score and the parts as LilyPond files."""

from __future__ import annotations

import bisect
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import accumulate
from pathlib import Path

from . import combine, frontmatter, music, techniques
from .pitch import Interval
from .structure import Bar, global_to_lilypond
from .work import Instrument, Player, Work

LILYPOND_VERSION = "2.26.0"

FAMILY_ORDER = ["woodwinds", "brass", "percussion", "plucked", "keyboards", "strings"]

STYLE = r"""
% Style of Night Music for Orchestra. The build code writes this file.

#(define-markup-command (rehearsal layout props text) (markup?)
   "A rehearsal mark: a bold letter in a box. The size is in points."
   (interpret-markup layout props
     (markup #:override '(box-padding . 0.5) #:box #:bold #:abs-fontsize @REHEARSAL@ text)))

#(define-markup-command (tempochange layout props text) (markup?)
   "A gradual change of tempo, for example rit."
   (interpret-markup layout props
     (markup #:normal-text #:italic #:fontsize 1 text)))

#(define-markup-command (instrumentchange layout props text) (markup?)
   "A change of instrument for one player."
   (interpret-markup layout props
     (markup #:box #:pad-markup 0.3 #:fontsize -1 text)))

#(define-markup-command (players layout props text) (markup?)
   "The players of a staff for two players: 1., 2., or a 2."
   (interpret-markup layout props
     (markup #:normal-text text)))

#(define-markup-command (pairname layout props name upper lower) (markup? markup? markup?)
   "The name of a staff for two players: the name, then the two numbers, one above the other."
   (interpret-markup layout props
     #{ \markup \line {
          \vcenter #name
          \vcenter \override #'(baseline-skip . 2.3) \column { #upper #lower }
        } #}))

#(define-markup-command (extraname layout props name player) (markup? markup?)
   "The name of a staff for the second instrument of a player, with the player below it."
   (interpret-markup layout props
     #{ \markup \override #'(baseline-skip . 2.3) \right-column {
          #name
          \fontsize #-1.5 #player
        } #}))

% Dynamic marks that LilyPond does not have.
sffz = #(make-dynamic-script "sffz")
sfpp = #(make-dynamic-script "sfpp")
ffp = #(make-dynamic-script "ffp")
pf = #(make-dynamic-script "pf")
"""

SCORE_LAYOUT = r"""
\layout {
  \context {
    % A line for the tempo marks and the rehearsal marks. The score has one above the
    % woodwinds and one above the strings: a conductor reads them near each group.
    \type Engraver_group
    \name MarkLine
    \consists Axis_group_engraver
    \consists Mark_engraver
    \consists Metronome_mark_engraver
    \override VerticalAxisGroup.staff-affinity = #DOWN
    \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #1.8
    \override VerticalAxisGroup.nonstaff-unrelatedstaff-spacing.padding = #2.5
    \override MetronomeMark.font-size = #4.5
    \override RehearsalMark.self-alignment-X = #LEFT
    \override RehearsalMark.break-align-symbols = #'(left-edge staff-bar)
    \override RehearsalMark.extra-spacing-width = #'(+inf.0 . -inf.0)
    \override MetronomeMark.extra-spacing-width = #'(+inf.0 . -inf.0)
    % The marks have fixed places in this line: they do not look for a staff. The
    % tempo mark and the rehearsal mark are on the base line. A rehearsal mark at a
    % tempo mark is a part of the tempo mark: the two are side by side.
    \override RehearsalMark.outside-staff-priority = ##f
    \override MetronomeMark.outside-staff-priority = ##f
    \override MetronomeMark.Y-offset = #0
    \override RehearsalMark.Y-offset = #0
  }
  \context {
    % The first page shows all staves. The staves can be a little nearer than the
    % usual smallest distance: thus that page is not too full.
    \StaffGroup
    \override StaffGrouper.staff-staff-spacing.minimum-distance = #6.4
    \override StaffGrouper.staffgroup-staff-spacing.minimum-distance = #7.6
  }
  \context {
    \Score
    \remove Mark_engraver
    \remove Metronome_mark_engraver
    \accepts MarkLine
    \override BarNumber.font-size = #3
    \override BarNumber.font-shape = #'italic
    \override BarNumber.padding = #1.5
    \override InstrumentName.self-alignment-X = #RIGHT
    \override InstrumentName.padding = #0.8
    \override InstrumentName.font-size = #1
    \override Hairpin.minimum-length = #5
    \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/16)
    skipBars = ##f
  }
  \context {
    \Staff
    \RemoveEmptyStaves
    \override VerticalAxisGroup.remove-first = ##f
    \override TextScript.font-size = #-0.5
    \override DynamicTextSpanner.style = #'none
  }
  \context {
    \PianoStaff
    \override InstrumentName.self-alignment-X = #RIGHT
  }
}
"""

PART_LAYOUT = r"""
\layout {
  \context {
    \Score
    \override BarNumber.font-size = #0
    \override BarNumber.font-shape = #'italic
    \override MetronomeMark.font-size = #1.5
    \override MetronomeMark.padding = #2.5
    \override RehearsalMark.padding = #2.5
    \override MultiMeasureRest.expand-limit = #1
    \override Hairpin.minimum-length = #5
    \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/16)
    skipBars = ##t
  }
  \context {
    \Staff
    \override TextScript.font-size = #-0.5
    \override DynamicTextSpanner.style = #'none
    % A page turn is permitted where the player has a rest of three whole notes or
    % more: the player needs the time to turn the page.
    \consists Page_turn_engraver
    pageTurnMinimumRestLength = #3
  }
}
"""

SCORE_PAPER = r"""
\paper {
  #(set-paper-size "11x17")
  % Pages for a print on the two sides of the paper: the inner margin is for the binding.
  two-sided = ##t
  inner-margin = 18\mm
  outer-margin = 13\mm
  top-margin = 12\mm
  bottom-margin = 14\mm
  indent = 32\mm
  short-indent = 15\mm
  system-separator-markup = \slashSeparator
  ragged-last-bottom = ##f
  print-page-number = ##t
  bookpart-level-page-numbering = ##t
  % Space between the last staff of a page and the copyright line.
  last-bottom-spacing.padding = #2.5
  % The first page of music: the type of the score on the left, the title in the
  % middle, the composer on the right. The sizes are in points.
  bookTitleMarkup = \markup \column {
    \fill-line { \abs-fontsize #25 \bold \fromproperty #'header:title }
    \vspace #0.9
    \fill-line {
      \abs-fontsize #12 \italic \fromproperty #'header:poet
      \abs-fontsize #13 \fromproperty #'header:composer
    }
    \vspace #0.4
  }
  % The page number is in the outer corner, 14 point. The title is in each header.
  oddHeaderMarkup = \markup \fill-line {
    \null
    \unless \on-first-page-of-part \abs-fontsize #9 \italic \fromproperty #'header:title
    \if \should-print-page-number \abs-fontsize #14 \fromproperty #'page:page-number-string
  }
  evenHeaderMarkup = \markup \fill-line {
    \if \should-print-page-number \abs-fontsize #14 \fromproperty #'page:page-number-string
    \unless \on-first-page-of-part \abs-fontsize #9 \italic \fromproperty #'header:title
    \null
  }
}
"""

PART_PAPER = r"""
\paper {
  #(set-paper-size "arch a")
  % 9 x 12 inches: a usual size for parts, and the largest size for a digital part.
  % The margins are those of the guidelines of the orchestra librarians (20 mm).
  two-sided = ##t
  inner-margin = 19\mm
  outer-margin = 17\mm
  top-margin = 13\mm
  bottom-margin = 15\mm
  indent = 12\mm
  ragged-last-bottom = ##t
  print-page-number = ##t
  page-breaking = #ly:page-turn-breaking
  % The first page: the instrument on the left, the title in the middle, the composer
  % on the right. The sizes are in points.
  bookTitleMarkup = \markup \column {
    \fill-line {
      \abs-fontsize #15 \bold \fromproperty #'header:instrument
      \abs-fontsize #21 \bold \fromproperty #'header:title
      \abs-fontsize #12 \fromproperty #'header:composer
    }
    \vspace #1.0
  }
  % Each subsequent page: the instrument and the title, and the page number in the
  % outer corner.
  oddHeaderMarkup = \markup \fill-line {
    \null
    \unless \on-first-page-of-part \abs-fontsize #9.5 \concat {
      \bold \fromproperty #'header:instrument "   " \italic \fromproperty #'header:title
    }
    \if \should-print-page-number \abs-fontsize #13 \fromproperty #'page:page-number-string
  }
  evenHeaderMarkup = \markup \fill-line {
    \if \should-print-page-number \abs-fontsize #13 \fromproperty #'page:page-number-string
    \unless \on-first-page-of-part \abs-fontsize #9.5 \concat {
      \bold \fromproperty #'header:instrument "   " \italic \fromproperty #'header:title
    }
    \null
  }
}
"""


def identifier(player_id: str) -> str:
    """Return a LilyPond variable name for a player (letters only)."""
    letters = "".join(
        chr(ord("A") + int(char) - 1) if char.isdigit() else char for char in player_id
    )
    return "music" + letters[0].upper() + letters[1:].replace(".", "")


@dataclass
class _Emitter:
    """Write the music of one player. The interval changes when the player changes instrument."""

    work: Work
    for_part: bool
    left_hand: bool = False
    interval: Interval | None = None
    pedal_down: bool = False  # the sustain pedal is down at this point of the file
    instrument_name: str = ""  # the instrument that the player has at this point

    def set_instrument(self, instrument: Instrument | None) -> None:
        self.instrument_name = instrument.name if instrument is not None else ""
        if instrument is None:
            self.interval = None
        else:
            self.interval = instrument.part_interval if self.for_part else instrument.score_interval

    def clef_of(self, instrument: Instrument | None) -> str:
        if instrument is None:
            return "percussion"
        clef = instrument.clef if self.for_part else instrument.score_clef
        if clef == "grand":
            return "bass" if self.left_hand else "treble"
        return clef

    def emit(self, elements: list[music.Element], *, top: bool = True) -> str:
        """Return the LilyPond text of the elements. `top` is true for all music of a player."""
        parts = []
        splits = _rest_splits(self.work) if top else frozenset()
        for element in _merge_full_bar_rests(elements, splits):
            if isinstance(element, music.Command) and element.name == "switch":
                name = element.arguments[0].strip('"')
                if name == self.instrument_name:
                    continue  # the player has this instrument: no mark
                instrument = self.work.orchestra.instruments.get(name)
                self.set_instrument(instrument)
                label = name[0].upper() + name[1:]
                parts.append(
                    f'\\clef {self.clef_of(instrument)} <>^\\markup \\instrumentchange "{label}"'
                )
            elif isinstance(element, music.Group) and element.kind == "parallel":
                voices = [
                    f"{{ {self.emit(child.children, top=False)} }}" for child in element.children
                ]
                parts.append("<< " + " \\\\ ".join(voices) + " >>")
            elif isinstance(element, music.Group):
                inner = self.emit(element.children, top=False)
                prefix = f"{element.header} " if element.kind != "sequence" else ""
                parts.append(f"{prefix}{{ {inner} }}")
            else:
                parts.append(music.to_lilypond(self._pedal(element), self.interval))
        return " ".join(parts).replace("\n ", "\n")

    def _pedal(self, element: music.Element) -> music.Element:
        """Remove a release of the sustain pedal that has no push before it in this file.

        A file with a part of the work (a page of the video) can start while the
        pedal is down. LilyPond does not print a pedal change that starts with a
        release only.
        """
        posts = getattr(element, "posts", None)
        if not posts:
            return element
        kept, changed = [], False
        for post in posts:
            if post.kind == "command" and post.value == "sustainOn":
                self.pedal_down = True
            elif post.kind == "command" and post.value == "sustainOff":
                if not self.pedal_down:
                    changed = True
                    continue
                self.pedal_down = False
            kept.append(post)
        return replace(element, posts=kept) if changed else element


def _rest_text(quarters: Fraction) -> str:
    """Return the length of a full-bar rest as LilyPond text, for example "1*7/8"."""
    whole = quarters / 4
    return f"1*{whole.numerator}" if whole.denominator == 1 else f"1*{whole}"


def _cut_long_rests(
    elements: list[music.Element], splits: frozenset[Fraction]
) -> list[music.Element]:
    """Cut each full-bar rest of many bars at the positions of `splits` that are in it."""
    if not splits:
        return elements
    result: list[music.Element] = []
    position = Fraction(0)
    for element in elements:
        start = position
        position += music.length(element)
        inside = sorted(split for split in splits if start < split < position)
        if not (isinstance(element, music.Rest) and element.kind == "R" and inside):
            result.append(element)
            continue
        edges = [start, *inside, position]
        for number, (first, last) in enumerate(zip(edges, edges[1:], strict=False)):
            posts = list(element.posts) if number == 0 else []
            result.append(music.Rest("R", last - first, _rest_text(last - first), posts))
            if number < len(edges) - 2:
                result.append(music.BarCheck())
    return result


def _merge_full_bar_rests(
    elements: list[music.Element], splits: frozenset[Fraction] = frozenset()
) -> list[music.Element]:
    """Join adjacent full-bar rests into one rest.

    LilyPond shows one long rest as a rest with a number in the parts. It does
    not join rests that are written one bar at a time.

    `splits` are positions in the work (in quarter notes, from the first
    element) at which a new rest must start. A part shows each change of tempo
    also in a long rest: thus a long rest stops at a tempo mark.
    """
    merged: list[music.Element] = []
    run: music.Rest | None = None
    position = Fraction(0)
    for element in _cut_long_rests(elements, splits):
        start = position
        position += music.length(element)
        full_bar = isinstance(element, music.Rest) and element.kind == "R"
        plain_rest = full_bar and not element.posts
        # A full-bar rest at which a hairpin stops can be the first rest of a long rest.
        stop_only = full_bar and [(p.kind, p.value) for p in element.posts] == [("hairpin", "!")]
        if run is not None and full_bar and start in splits:
            merged.append(music.BarCheck())
            run = None
        if plain_rest or (stop_only and run is None):
            if run is None:
                run = music.Rest("R", element.duration, "", list(element.posts))
                merged.append(run)
            else:
                run.duration += element.duration
            run.duration_text = _rest_text(run.duration)
        elif isinstance(element, music.BarCheck) and run is not None:
            continue
        else:
            if run is not None:
                merged.append(music.BarCheck())
                run = None
            merged.append(element)
    if run is not None:
        merged.append(music.BarCheck())
    return merged


def _rest_splits(work: Work) -> frozenset[Fraction]:
    """Return the positions at which a long rest of a part must stop and start again.

    These are the start and the end of each bar that has a tempo mark or a
    change of tempo in words.
    """
    structure = work.structure
    positions: set[Fraction] = set()
    for point in structure.tempo_points:
        if point.text or point.unit:
            bar = structure.bar_at(min(point.position, structure.length - Fraction(1, 64)))
            positions.add(bar.start)
            if point.position > bar.start:
                positions.add(bar.end)
    return frozenset(positions)


def _pitches(elements: list[music.Element]) -> list[float]:
    """Return the MIDI numbers of all notes in the elements."""
    found: list[float] = []
    for element in elements:
        if isinstance(element, music.Note):
            found.extend(note_pitch.pitch.midi for note_pitch in element.pitches)
        elif isinstance(element, music.Group):
            found.extend(_pitches(element.children))
    return found


def best_clef(
    base: str, instrument: Instrument | None, written: list[float], current: str = ""
) -> str:
    """Return the clef for a passage: the usual clef, or a better clef for its range.

    `current` is the clef before the passage. A hand of a keyboard instrument
    keeps its clef until the notes are clearly in the range of the other clef.
    """
    if not written or instrument is None or base in ("percussion", "grand"):
        return current or base
    ordered = sorted(written)
    median, lowest = ordered[len(ordered) // 2], ordered[0]
    if instrument.clef == "grand":
        # Between A-flat 3 and E4 (the notes near middle C), the hand keeps its clef.
        # A passage with a very low note is in the bass clef (for example a low grace
        # note before a figure that goes up).
        if (current or base) == "bass":
            return "treble" if median >= 64 and lowest >= 55 else "bass"
        return "bass" if (median <= 56 and ordered[-1] <= 65) or lowest < 45 else "treble"
    if base == "treble" and instrument.name == "horn in F" and median < 55:
        return "bass"
    if base == "bass" and instrument.name == "bass clarinet" and median > 62:
        return "treble"
    tenor_instruments = ("bassoon", "violoncello", "tenor trombone")
    if base == "bass" and instrument.name in tenor_instruments and median > 66 and lowest >= 55:
        return "tenor"
    if base == "alto" and median > 81 and lowest > 67:
        return "treble"
    return base


def best_ottava(clef: str, instrument: Instrument | None, written: list[float]) -> int:
    """Return the octave sign for a passage: 1 = one octave higher, -1 = lower, 0 = none.

    A passage that is all very high is easier to read with an octave sign.
    The low octaves of a keyboard instrument get the sign for the lower octave.
    """
    if not written or instrument is None:
        return 0
    ordered = sorted(written)
    low_part = ordered[len(ordered) // 10]
    if clef == "treble" and ordered[-1] >= 93 and low_part >= 81:
        return 1
    if clef == "bass" and instrument.clef == "grand" and ordered[0] < 31 and ordered[-1] <= 55:
        return -1
    return 0


def _with_clefs(
    work: Work, player: Player, chunks: list[music.Group], emitter: _Emitter, instrument
) -> list[music.Element]:
    """Return the music of the chunks with a clef command where the best clef changes."""
    elements: list[music.Element] = []
    first_instrument = instrument
    # A staff starts with its usual clef, also if the player starts with rests.
    current = emitter.clef_of(instrument)
    elements.append(music.Command("clef", [current]))
    ottava = 0
    position = Fraction(0)  # the start of the unit in the work, in quarter notes
    for chunk in chunks:
        # A hand of a keyboard instrument can change its clef in each bar: its music
        # moves through the full keyboard. Other instruments have one clef for a section.
        grand = instrument is not None and instrument.clef == "grand"
        units = _bars_of(chunk.children) if grand else [chunk.children]
        for unit in units:
            start = position
            position += sum((music.length(element) for element in unit), Fraction(0))
            shift = emitter.interval.semitones if emitter.interval else 0
            written = [midi + shift for midi in _pitches(unit)]
            if grand and not written:
                elements.extend(unit)
                continue
            pieces = [unit]
            if grand and max(written) - min(written) > WIDE_BAR:
                # A line that goes through much of the keyboard in one bar: each beat
                # group of the bar can have its own clef and its own octave sign.
                pieces = _beat_pieces(unit, _beat_groups(work.structure.bar_at(start)))
            for piece in pieces:
                notes = [midi + shift for midi in _pitches(piece)]
                if not notes:
                    elements.extend(piece)
                    continue
                clef = best_clef(emitter.clef_of(instrument), instrument, notes, current)
                if clef != current:
                    elements.append(music.Command("clef", [clef]))
                    current = clef
                octave = best_ottava(clef, instrument, notes)
                if octave != ottava:
                    elements.append(music.Command("ottava", [f"#{octave}"]))
                    ottava = octave
                elements.extend(piece)
        # A change of instrument in the chunk changes the usual clef.
        for command in _walk_commands(chunk.children):
            if command.name == "switch":
                instrument = work.orchestra.instruments.get(command.arguments[0].strip('"'))
                emitter.set_instrument(instrument)
                current = emitter.clef_of(instrument)
    emitter.set_instrument(first_instrument)
    return elements


# A bar of one hand of a keyboard instrument that is wider than this (in semitones)
# can have more than one clef.
WIDE_BAR = 19


def _beat_groups(bar: Bar) -> list[Fraction]:
    """Return the length of each beat group of a bar, in quarter notes."""
    if bar.grouping:
        return [Fraction(4 * size, bar.denominator) for size in bar.grouping]
    beat = Fraction(3, 2) if bar.denominator == 8 and bar.numerator % 3 == 0 else Fraction(1)
    count = int(bar.length / beat)
    groups = [beat] * count
    if bar.length > beat * count:
        groups.append(bar.length - beat * count)
    return groups


def _beat_pieces(
    elements: list[music.Element], groups: list[Fraction]
) -> list[list[music.Element]]:
    """Divide the music of one bar at the ends of its beat groups.

    A tuplet or a different group stays in one piece. A grace note or a
    command at the start of a beat group goes with that beat group.
    """
    edges = list(accumulate(groups))
    pieces: list[list[music.Element]] = [[]]
    position = Fraction(0)
    has_time = False
    for element in elements:
        if has_time and edges and position >= edges[0]:
            pieces.append([])
            has_time = False
        while edges and position >= edges[0]:
            edges.pop(0)
        pieces[-1].append(element)
        duration = music.length(element)
        position += duration
        has_time = has_time or duration > 0
    return pieces


def _bars_of(elements: list[music.Element]) -> list[list[music.Element]]:
    """Divide the music of a section into bars. Each bar ends with its bar check."""
    bars: list[list[music.Element]] = []
    current: list[music.Element] = []
    for element in elements:
        current.append(element)
        if isinstance(element, music.BarCheck):
            bars.append(current)
            current = []
    if current:
        bars.append(current)
    return bars


def _player_music(work: Work, player: Player, *, for_part: bool) -> str:
    emitter = _Emitter(work, for_part, left_hand=player.id.endswith(".lh"))
    instrument = work.orchestra.first_instrument(player.id)
    emitter.set_instrument(instrument)
    chunks = [chunk for _first_bar, chunk in work.chunks.get(player.id, [])]
    return emitter.emit(_with_clefs(work, player, chunks, emitter, instrument))


def _header(work: Work, instrument_line: str = "", document: str = "") -> str:
    """Return the header of the music: title, composer, and the name of the part.

    `document` is the type of a score ("Score in C" or "Transposed score"): it
    is in the upper left corner of the first page of music.
    """
    lines = [
        "\\header {",
        f'  title = "{work.title}"',
        f'  subtitle = "{work.subtitle}"' if work.subtitle else "",
        f'  composer = "{work.composer}"' if work.composer else "",
        f'  instrument = "{instrument_line}"' if instrument_line else "",
        f'  poet = "{document}"' if document else "",
        f'  copyright = "{frontmatter.copyright_line(work)}"',
        "  tagline = ##f",
        "}",
    ]
    return "\n".join(line for line in lines if line)


def shared_staves(work: Work, breaks: set[int]) -> dict[str, combine.SharedStaff]:
    """Return the staves of the conductor score that two players share.

    The key is the identifier of player 1. `breaks` are the bars after which a
    system of the score ends.
    """
    present = {player.id for player in work.orchestra.players}
    system_bars = frozenset({1} | {bar + 1 for bar in breaks})
    return {
        first: combine.shared_staff(work, first, second, system_bars)
        for first, second in combine.PAIRS
        if first in present and second in present
    }


def _shared_identifier(player_id: str, voice: int) -> str:
    return identifier(player_id).replace("music", "shared", 1) + ("One", "Two")[voice]


def _extra_identifier(extra: combine.Extra) -> str:
    letters = "".join(char for char in extra.instrument.title() if char.isalpha())
    return identifier(extra.player).replace("music", "extra", 1) + letters


def _shared_music(work: Work, staff: combine.SharedStaff, *, for_part: bool) -> tuple[str, str]:
    """Return the LilyPond text of the two voices of a shared staff."""
    instrument = work.orchestra.first_instrument(staff.first)
    emitters = [_Emitter(work, for_part), _Emitter(work, for_part)]
    for emitter in emitters:
        emitter.set_instrument(instrument)
    shift = emitters[0].interval.semitones if emitters[0].interval else 0
    current = emitters[0].clef_of(instrument)
    one: list[music.Element] = [music.Command("clef", [current])]
    two: list[music.Element] = []
    ottava = 0
    for first, second in staff.chunks:
        # One clef for a section, for the notes of the two players.
        notes = [midi + shift for midi in _pitches(first) + _pitches(second)]
        if notes:
            clef = best_clef(emitters[0].clef_of(instrument), instrument, notes, current)
            if clef != current:
                one.append(music.Command("clef", [clef]))
                current = clef
            octave = best_ottava(clef, instrument, notes)
            if octave != ottava:
                one.append(music.Command("ottava", [f"#{octave}"]))
                ottava = octave
        one.extend(first)
        two.extend(second)
    return emitters[0].emit(one), emitters[1].emit(two)


def _extra_music(work: Work, extra: combine.Extra, *, for_part: bool) -> str:
    """Return the LilyPond text of the staff for the second instrument of a player."""
    instrument = work.orchestra.instruments.get(extra.instrument)
    emitter = _Emitter(work, for_part)
    emitter.set_instrument(instrument)
    player = work.orchestra.player(extra.player)
    return emitter.emit(_with_clefs(work, player, extra.chunks, emitter, instrument))


def _definitions(
    work: Work,
    players: list[Player],
    *,
    for_part: bool,
    breaks: set[int] | None = None,
    shared: dict[str, combine.SharedStaff] | None = None,
) -> str:
    structure = work.structure if breaks is None else replace(work.structure, breaks=breaks)
    score = breaks is not None
    shared = shared or {}
    second_players = {staff.second for staff in shared.values()}
    blocks = [
        "global = {\n\\accidentalStyle Score.modern\n\\numericTimeSignature\n"
        + global_to_lilypond(
            structure, change_context=None if score else "Score.", marks="none" if score else "all"
        )
        + "\n}"
    ]
    if score:
        # A score: the lines for the tempo marks and the rehearsal marks.
        blocks.append(
            "globalMarks = {\n"
            + global_to_lilypond(structure, change_context="", marks="line")
            + "\n}"
        )
    for player in players:
        if player.id in second_players:
            continue  # the music is in the staff of player 1
        if player.id in shared:
            staff = shared[player.id]
            for voice, text in enumerate(_shared_music(work, staff, for_part=for_part)):
                blocks.append(f"{_shared_identifier(player.id, voice)} = {{\n{text}\n}}")
            for extra in staff.extras:
                text = _extra_music(work, extra, for_part=for_part)
                blocks.append(f"{_extra_identifier(extra)} = {{\n{text}\n}}")
            continue
        text = _player_music(work, player, for_part=for_part)
        blocks.append(f"{identifier(player.id)} = {{\n{text}\n}}")
    return "\n\n".join(blocks)


def _staff(player: Player, *, names: bool = True) -> str:
    with_block = (
        f'\\with {{ instrumentName = "{player.name}" shortInstrumentName = "{player.short}" }} '
        if names
        else ""
    )
    return f'\\new Staff = "{player.id}" {with_block}<< \\global \\{identifier(player.id)} >>'


def _groups(work: Work) -> list[tuple[str, list[Player]]]:
    """Return the players in families, in the sequence of the score."""
    groups: dict[str, list[Player]] = {family: [] for family in FAMILY_ORDER}
    for player in work.orchestra.players:
        groups[player.family].append(player)
    return [(family, members) for family, members in groups.items() if members]


# The names of the instruments that have a staff of their own in the score when a
# player of a shared staff changes to them: the full name and the short name.
EXTRA_NAMES = {
    "alto flute": ("Alto Flute", "A. Fl."),
    "ocarina": ("Ocarina", "Oc."),
    "clarinet in E-flat": ("Clarinet in E-flat", "E-fl. Cl."),
}


def _pair_names(player: Player) -> tuple[str, str]:
    """Divide the name of a player into the instrument and the number: "Flute 1" -> "Flute", "1"."""
    name, _, number = player.name.rpartition(" ")
    return name, number


def _shared_staff_text(work: Work, staff: combine.SharedStaff) -> list[str]:
    """Return the LilyPond staves for a pair: the shared staff, then the extra staves."""
    first, second = work.orchestra.player(staff.first), work.orchestra.player(staff.second)
    name, upper = _pair_names(first)
    lower = _pair_names(second)[1]
    short = first.short.rpartition(" ")[0]
    staves = [
        f'\\new Staff = "{first.id}+{second.id}" \\with {{\n'
        f'    instrumentName = \\markup \\pairname "{name}" "{upper}" "{lower}"\n'
        f'    shortInstrumentName = \\markup \\pairname "{short}" "{upper}" "{lower}"\n'
        "    \\consists Merge_rests_engraver\n"
        "  } <<\n"
        "    \\global\n"
        f"    \\new Voice {{ \\{_shared_identifier(first.id, 0)} }}\n"
        f"    \\new Voice {{ \\{_shared_identifier(first.id, 1)} }}\n"
        "  >>"
    ]
    for extra in staff.extras:
        player = work.orchestra.player(extra.player)
        full, brief = EXTRA_NAMES.get(extra.instrument, (extra.instrument.title(),) * 2)
        staves.append(
            f'\\new Staff = "{extra.player} {extra.instrument}" \\with {{\n'
            f'    instrumentName = \\markup \\extraname "{full}" "({player.name})"\n'
            f'    shortInstrumentName = \\markup \\extraname "{brief}" "({player.short})"\n'
            "    \\override VerticalAxisGroup.remove-first = ##t\n"
            f"  }} << \\global \\{_extra_identifier(extra)} >>"
        )
    return staves


def _score_staves(work: Work, shared: dict[str, combine.SharedStaff] | None = None) -> str:
    shared = shared or {}
    second_players = {staff.second for staff in shared.values()}
    blocks = []
    for family, members in _groups(work):
        staves = []
        index = 0
        while index < len(members):
            player = members[index]
            if player.id in second_players:
                index += 1
            elif player.id in shared:
                staves.extend(_shared_staff_text(work, shared[player.id]))
                index += 1
            elif player.id.endswith(".rh"):
                lower = members[index + 1]
                base = player.id[: -len(".rh")]
                staves.append(
                    f'\\new PianoStaff = "{base}" \\with {{ instrumentName = "{player.name}" '
                    f'shortInstrumentName = "{player.short}" }} <<\n'
                    f"    {_staff(player, names=False)}\n    {_staff(lower, names=False)}\n  >>"
                )
                index += 2
            else:
                staves.append(_staff(player))
                index += 1
        joined = "\n  ".join(staves)
        if family in MARK_LINE_FAMILIES:
            blocks.append("\\new MarkLine { \\globalMarks }")
        blocks.append(f'\\new StaffGroup = "{family}" <<\n  {joined}\n>>')
    return "\n".join(blocks)


def score_notes(work: Work) -> list[str]:
    """Return the notes for the performance on the first page of the score.

    The bar numbers come from the music. Thus they stay correct when the
    music changes.
    """
    from ..perform.events import perform  # at call time: that module imports this package

    structure = work.structure
    quarter: dict[str, set[int]] = {"alto flute": set(), "violoncello": set(), "woodwinds": set()}
    ocarina: set[int] = set()
    for player in work.orchestra.players:
        for note in perform(work, player.id):
            bar = structure.bar_at(note.start).number
            if note.instrument == "ocarina":
                ocarina.add(bar)
            if note.midi != round(note.midi):
                if note.instrument in quarter:
                    quarter[note.instrument].add(bar)
                elif player.family == "woodwinds":
                    quarter["woodwinds"].add(bar)
                else:
                    raise ValueError(f"no note about the quarter-tones of the {player.id}")

    def bars(numbers: set[int]) -> str:
        first, last = min(numbers), max(numbers)
        return f"bar {first}" if first == last else f"bars {first} to {last}"

    notes = [
        "The score is in C. The parts are transposed.",
        "Piccolo, celesta, and glockenspiel sound higher than written, by one or two octaves. "
        "Contrabassoon, contrabass clarinet, and double basses sound one octave lower than "
        "written.",
        "An accidental is for one bar and one octave only.",
    ]
    places = []
    if quarter["alto flute"]:
        places.append(f"the alto flute ({bars(quarter['alto flute'])})")
    if quarter["violoncello"]:
        places.append(f"one cello ({bars(quarter['violoncello'])})")
    series = ""
    if quarter["woodwinds"]:
        # The woodwinds hold their quarter-tones to the end of the section.
        marks = sorted(structure.marks)
        before = [number for number in marks if number <= min(quarter["woodwinds"])]
        after = [number for number in marks if number > max(quarter["woodwinds"])]
        first = before[-1] if before else 1
        last = after[0] - 1 if after else len(structure.bars)
        series = f"bars {first} to {last}"
        places.append(f"the woodwinds ({series})")
    if places:
        text = "Quarter-tones are in these parts: "
        text += places[0] if len(places) == 1 else ", ".join(places[:-1]) + ", and " + places[-1]
        text += "."
        if series:
            text += (
                f" In {series}, the quarter-tones are the notes of the harmonic series on D: "
                "play them with no vibrato."
            )
        notes.append(text)
    notes.append("l.v.: let the sound ring.")
    if ocarina:
        notes.append(
            f"Three players have an ocarina in C ({bars(ocarina)}): oboe 2, clarinet 1, and "
            "bassoon 2."
        )
    notes.append(
        "Seating: the first violins are on the left of the conductor, the second violins on "
        "the right."
    )
    minutes = round(structure.duration_seconds / 60)
    if minutes >= 1:
        notes.append(f"Duration: {minutes} minutes.")
    return notes


OVERFULL = 0.12  # a system can have this much more than its capacity


def system_breaks(widths: list[float], capacity: float, most_bars: int) -> set[int]:
    """Return the bars after which a new system starts, for the widths of the bars.

    The systems are as equally full as possible: the function finds the
    division with the lowest sum of the costs of the systems. A system that
    is not full costs the square of its empty share. A system can be a little
    more than full (`OVERFULL`): this costs more. The last system can be
    empty in part at no cost. Thus a short bar does not stay alone between
    two long bars.
    """
    count = len(widths)
    best = [0.0] + [float("inf")] * count  # the lowest cost for the first bars
    cut = [0] * (count + 1)  # the last bar of the system before
    for last in range(1, count + 1):
        load = 0.0
        for first in range(last, max(last - most_bars, 0), -1):
            load += widths[first - 1]
            if load > capacity * (1.0 + OVERFULL) and first < last:
                break
            if load > capacity:
                cost = (3.0 * (load - capacity) / capacity) ** 2
            else:
                cost = 0.0 if last == count else ((capacity - load) / capacity) ** 2
            if best[first - 1] + cost < best[last]:
                best[last], cut[last] = best[first - 1] + cost, first - 1
    breaks: set[int] = set()
    last = count
    while cut[last]:
        last = cut[last]
        breaks.add(last)
    return breaks


def score_breaks(work: Work, capacity: float = 56.0, most_bars: int = 10) -> set[int]:
    """Return the bars after which the conductor score starts a new system.

    The width of a bar depends on the number of different moments at which
    a note starts. The function `system_breaks` divides the bars into systems.
    """
    from ..perform.events import perform

    structure = work.structure
    starts = [float(bar.start) for bar in structure.bars]
    moments: list[set[float]] = [set() for _ in structure.bars]
    for player in work.orchestra.players:
        for note in perform(work, player.id):
            position = float(note.start)
            moments[bisect.bisect_right(starts, position) - 1].add(position)
    widths = [max(len(columns), 2) + 1.5 for columns in moments]
    return system_breaks(widths, capacity, most_bars)


# The families that have a line for the tempo marks and the rehearsal marks above them.
MARK_LINE_FAMILIES = ("woodwinds", "strings")
SCORE_PAGE = frontmatter.Page(279.4, 431.8, 13.0)  # 11 x 17 inches, staff of 4.6 mm
SCORE_REHEARSAL_POINTS = 20.0
PART_REHEARSAL_POINTS = 15.0


def style(rehearsal_points: float) -> str:
    """Return the style definitions for a document."""
    return STYLE.replace("@REHEARSAL@", f"{rehearsal_points:g}").strip()


def front_part(work: Work, page: frontmatter.Page, edition: str) -> str:
    """Return the pages before the music as one part of the book, with no page numbers."""
    pages = frontmatter.pages(work, page, edition, score_notes(work))
    body = "\n\n\\pageBreak\n\n".join(pages)
    return (
        "\\bookpart {\n"
        "\\paper {\n"
        "  two-sided = ##f\n"
        f"  left-margin = {page.margin_mm:g}\\mm\n"
        f"  right-margin = {page.margin_mm:g}\\mm\n"
        "  top-margin = 18\\mm\n"
        "  bottom-margin = 18\\mm\n"
        "  print-page-number = ##f\n"
        "  oddHeaderMarkup = ##f\n"
        "  evenHeaderMarkup = ##f\n"
        "  oddFooterMarkup = ##f\n"
        "  evenFooterMarkup = ##f\n"
        "}\n"
        "\\header { tagline = ##f }\n\n" + body + "\n}"
    )


def score_file(work: Work, *, transposed: bool = False) -> str:
    """Return the LilyPond text of the conductor score.

    The usual score is in C. If `transposed` is true, each instrument has the
    notes of its part: some orchestras ask for such a score.
    """
    breaks = score_breaks(work)
    shared = shared_staves(work, breaks)
    document = "Transposed score" if transposed else "Score in C"
    edition = "Full score, transposed" if transposed else "Full score in C"
    music_part = (
        "\\bookpart {\n"
        + _header(work, document=document)
        + "\n\\score {\n<<\n"
        + _score_staves(work, shared)
        + "\n>>\n"
        + SCORE_LAYOUT.strip()
        + "\n}\n}"
    )
    return (
        "\n\n".join(
            [
                f'\\version "{LILYPOND_VERSION}"',
                style(SCORE_REHEARSAL_POINTS),
                techniques.lilypond_definitions(),
                f"#(set-global-staff-size {SCORE_PAGE.staff_size:g})",
                SCORE_PAPER.strip(),
                _definitions(
                    work, work.orchestra.players, for_part=transposed, breaks=breaks, shared=shared
                ),
                front_part(work, SCORE_PAGE, edition),
                music_part,
            ]
        )
        + "\n"
    )


def part_players(work: Work) -> dict[str, list[Player]]:
    """Return the staves of each part. A keyboard part has two staves."""
    parts: dict[str, list[Player]] = {}
    for player in work.orchestra.players:
        base = player.id.split(".")[0]
        parts.setdefault(base, []).append(player)
    return parts


# The height of a staff in a part, in points. The guidelines of the orchestra
# librarians: 7.5 mm is the best, 7.0 mm is possible for winds, and less is not
# acceptable. Two string players read one part: they get the larger staff.
PART_STAFF_POINTS = 20.0  # 7.1 mm
STRING_PART_STAFF_POINTS = 21.0  # 7.4 mm


def part_staff_size(family: str) -> float:
    return STRING_PART_STAFF_POINTS if family == "strings" else PART_STAFF_POINTS


def part_file(work: Work, part_id: str) -> str:
    """Return the LilyPond text of one part."""
    players = part_players(work)[part_id]
    first = players[0]
    name = first.name
    instrument = work.orchestra.first_instrument(first.id)
    line = name
    if instrument and instrument.transposition % 12 and " in " in instrument.name:
        line = f"{name} in {instrument.name.split(' in ')[1]}"
    if len(players) == 1:
        staves = f"\\new Staff << \\global \\{identifier(first.id)} >>"
    else:
        inner = "\n  ".join(_staff(player, names=False) for player in players)
        staves = f"\\new PianoStaff <<\n  {inner}\n>>"
    return (
        "\n\n".join(
            [
                f'\\version "{LILYPOND_VERSION}"',
                style(PART_REHEARSAL_POINTS),
                techniques.lilypond_definitions(),
                f"#(set-global-staff-size {part_staff_size(first.family):g})",
                PART_PAPER.strip(),
                _header(work, line),
                _definitions(work, players, for_part=True),
                "\\score {\n" + staves + "\n" + PART_LAYOUT.strip() + "\n}",
            ]
        )
        + "\n"
    )


# ----------------------------------------------------------------------------
# Score pages for the video: one file for each section of the work
# ----------------------------------------------------------------------------

VIDEO_PAGE_MM = (480.0, 270.0)
VIDEO_REHEARSAL_POINTS = 16.0
VIDEO_SECONDS_PER_SCREEN = 15.0
# The video for a telephone: the screen is tall and narrow. A screen shows less
# time, and the notes are larger.
MOBILE_PAGE_MM = (270.0, 480.0)
MOBILE_SECONDS_PER_SCREEN = 7.0

VIDEO_SCHEME = r"""
#(define (tag-when class)
   (lambda (grob)
     (let* ((column (ly:item-get-column grob))
            (when (ly:grob-property column 'when)))
       (list (cons 'class class)
             (cons 'data-when
                   (number->string (exact->inexact (ly:moment-main when))))))))
"""

VIDEO_LAYOUT = r"""
\layout {
  \context {
    \Score
    \override NoteHead.output-attributes = #(tag-when "nh")
    \override Rest.output-attributes = #(tag-when "rest")
    \override BarLine.output-attributes = #(tag-when "bar")
    \override BarNumber.font-size = #0
    \override MetronomeMark.font-size = #2
    \override MetronomeMark.padding = #2.5
    \override RehearsalMark.padding = #3
    \override InstrumentName.self-alignment-X = #RIGHT
    \override Hairpin.minimum-length = #5
  }
  \context {
    \Staff
    \RemoveAllEmptyStaves
    \override TextScript.font-size = #-0.5
    \override DynamicTextSpanner.style = #'none
  }
}
""".replace("\\\\", "\\")


# The names of the instruments are smaller on the narrow page: the staves are large.
MOBILE_LAYOUT = VIDEO_LAYOUT.replace(
    "\\override InstrumentName.self-alignment-X = #RIGHT",
    "\\override InstrumentName.self-alignment-X = #RIGHT\n"
    "    \\override InstrumentName.font-size = #-3",
)


def chunk_count(work: Work) -> int:
    """Return the number of sections of the work."""
    return max(len(chunks) for chunks in work.chunks.values())


def chunk_bars(work: Work, index: int) -> tuple[int, int]:
    """Return the first bar and the last bar of a section."""
    some_player = next(iter(work.chunks.values()))
    first = some_player[index][0]
    last = (
        some_player[index + 1][0] - 1 if index + 1 < len(some_player) else len(work.structure.bars)
    )
    return first, last


def _instrument_at(work: Work, player: Player, index: int) -> Instrument | None:
    """Return the instrument that a player has at the start of a section."""
    name = player.instruments[0]
    for _first_bar, chunk in work.chunks[player.id][:index]:
        for element in _walk_commands(chunk.children):
            if element.name == "switch":
                name = element.arguments[0].strip('"')
    return work.orchestra.instruments.get(name)


def _walk_commands(elements: list[music.Element]):
    for element in elements:
        if isinstance(element, music.Command):
            yield element
        elif isinstance(element, music.Group):
            yield from _walk_commands(element.children)


def _is_silent(elements: list[music.Element]) -> bool:
    """Return True if the music has no notes."""
    for element in elements:
        if isinstance(element, music.Note):
            return False
        if isinstance(element, music.Group) and not _is_silent(element.children):
            return False
    return True


def active_players(work: Work, index: int) -> list[Player]:
    """Return the players that have notes in a section."""
    return [
        player
        for player in work.orchestra.players
        if not _is_silent(work.chunks[player.id][index][1].children)
    ]


def video_file(work: Work, index: int, staff_size: float, *, mobile: bool = False) -> str:
    """Return the LilyPond text of one section, as a page for the video.

    If `mobile` is true, the page is for the video for a telephone.
    """
    from .structure import Structure, global_to_lilypond

    first, last = chunk_bars(work, index)
    source = work.structure
    part = Structure(final_bar=last == len(source.bars))
    for bar in source.bars[first - 1 : last]:
        part.add_bars(1, bar.numerator, bar.denominator, bar.grouping)
    start = source.bar(first).start
    end = source.bar(last).end
    for point in source.tempo_points:
        if start <= point.position < end:
            shifted = type(point)(**{**point.__dict__, "position": point.position - start})
            part.tempo_points.append(shifted)
    part.marks = {
        bar - first + 1: label for bar, label in source.marks.items() if first <= bar <= last
    }
    part.double_bars = {bar - first + 1 for bar in source.double_bars if first <= bar <= last}
    # A screen of the video shows about 15 seconds of music.
    shown_from = start
    for bar in source.bars[first - 1 : last - 1]:
        seconds = source.seconds(bar.end) - source.seconds(shown_from)
        if seconds >= (MOBILE_SECONDS_PER_SCREEN if mobile else VIDEO_SECONDS_PER_SCREEN):
            part.breaks.add(bar.number - first + 1)
            shown_from = bar.end

    blocks = [
        "global = {\n\\accidentalStyle Score.modern\n\\numericTimeSignature\n"
        f"\\set Score.currentBarNumber = #{first}\n" + global_to_lilypond(part) + "\n}"
    ]
    staves: dict[str, list[str]] = {family: [] for family in FAMILY_ORDER}
    players = work.orchestra.players
    shown = {player.id for player in active_players(work, index)}
    # A keyboard instrument shows its two staves if one of them has notes.
    for player in players:
        base = player.id.split(".")[0]
        if "." in player.id and any(other.split(".")[0] == base for other in shown):
            shown.add(player.id)
    position = 0
    while position < len(players):
        player = players[position]
        position += 1
        if player.id not in shown:
            continue
        emitter = _Emitter(work, for_part=False, left_hand=player.id.endswith(".lh"))
        instrument = _instrument_at(work, player, index)
        emitter.set_instrument(instrument)
        children = work.chunks[player.id][index][1].children
        shift = emitter.interval.semitones if emitter.interval else 0
        clef = best_clef(
            emitter.clef_of(instrument), instrument, [midi + shift for midi in _pitches(children)]
        )
        body = emitter.emit(children, top=False)  # a page of the video: no long rests
        blocks.append(f"{identifier(player.id)} = {{\n\\clef {clef}\n{body}\n}}")
        tag = (
            f"\\override StaffSymbol.output-attributes = "
            f'#\'((class . "staff") (data-staff . "{player.id}"))'
        )
        names = f'instrumentName = "{player.short}" shortInstrumentName = "{player.short}"'
        own_names = "" if "." in player.id else names + " "
        staff = (
            f'\\new Staff = "{player.id}" \\with {{ {own_names}{tag} }} '
            f"<< \\global \\{identifier(player.id)} >>"
        )
        if player.id.endswith(".rh"):
            staves[player.family].append(f"\\new PianoStaff \\with {{ {names} }} <<\n    {staff}")
        elif player.id.endswith(".lh"):
            staves[player.family].append(f"    {staff}\n  >>")
        else:
            staves[player.family].append(staff)
    groups = [
        f'\\new StaffGroup = "{family}" <<\n  ' + "\n  ".join(members) + "\n>>"
        for family, members in staves.items()
        if members
    ]
    width, height = MOBILE_PAGE_MM if mobile else VIDEO_PAGE_MM
    side = 6 if mobile else 10
    paper = (
        "\\paper {\n"
        f"  #(set-paper-size '(cons (* {width} mm) (* {height} mm)))\n"
        f"  top-margin = 8\\mm\n  bottom-margin = 8\\mm\n  left-margin = {side}\\mm\n"
        f"  right-margin = {side}\\mm\n  indent = 20\\mm\n  short-indent = 20\\mm\n"
        "  max-systems-per-page = 1\n  ragged-last = ##f\n  ragged-bottom = ##t\n"
        "  print-page-number = ##f\n  oddHeaderMarkup = ##f\n  evenHeaderMarkup = ##f\n"
        "  oddFooterMarkup = ##f\n  evenFooterMarkup = ##f\n}"
    )
    return (
        "\n\n".join(
            [
                f'\\version "{LILYPOND_VERSION}"',
                style(VIDEO_REHEARSAL_POINTS),
                VIDEO_SCHEME.strip(),
                techniques.lilypond_definitions(),
                f"#(set-global-staff-size {staff_size:.2f})",
                paper,
                "\n\n".join(blocks),
                "\\score {\n<<\n"
                + "\n".join(groups)
                + "\n>>\n"
                + (MOBILE_LAYOUT if mobile else VIDEO_LAYOUT).strip()
                + "\n}",
            ]
        )
        + "\n"
    )


def write_all(work: Work, directory: Path) -> list[Path]:
    """Write the score file and all part files. Return the paths."""
    directory.mkdir(parents=True, exist_ok=True)
    paths = [directory / "score.ly"]
    paths[0].write_text(score_file(work), encoding="utf-8")
    for part_id in part_players(work):
        path = directory / f"part-{part_id}.ly"
        path.write_text(part_file(work, part_id), encoding="utf-8")
        paths.append(path)
    return paths
