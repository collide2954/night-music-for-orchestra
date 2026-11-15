"""Write the conductor score and the parts as LilyPond files."""

from __future__ import annotations

import bisect
from dataclasses import dataclass, replace
from pathlib import Path

from . import music, techniques
from .pitch import Interval
from .structure import global_to_lilypond
from .work import Instrument, Player, Work

LILYPOND_VERSION = "2.26.0"

FAMILY_ORDER = ["woodwinds", "brass", "percussion", "plucked", "keyboards", "strings"]

STYLE = r"""
% Style of Night Music for Orchestra. The build code writes this file.

#(define-markup-command (rehearsal layout props text) (markup?)
   "A rehearsal mark: a bold letter in a box."
   (interpret-markup layout props
     (markup #:box #:pad-markup 0.4 #:bold #:fontsize 2 text)))

#(define-markup-command (tempochange layout props text) (markup?)
   "A gradual change of tempo, for example rit."
   (interpret-markup layout props
     (markup #:normal-text #:italic #:fontsize 1 text)))

#(define-markup-command (instrumentchange layout props text) (markup?)
   "A change of instrument for one player."
   (interpret-markup layout props
     (markup #:box #:pad-markup 0.3 #:fontsize -1 text)))

% Dynamic marks that LilyPond does not have.
sffz = #(make-dynamic-script "sffz")
sfpp = #(make-dynamic-script "sfpp")
ffp = #(make-dynamic-script "ffp")
pf = #(make-dynamic-script "pf")
"""

SCORE_LAYOUT = r"""
\layout {
  \context {
    \Score
    \override BarNumber.font-size = #0
    \override BarNumber.padding = #1.5
    \override MetronomeMark.font-size = #2
    \override MetronomeMark.padding = #2.5
    \override RehearsalMark.padding = #3
    \override InstrumentName.self-alignment-X = #RIGHT
    \override InstrumentName.padding = #0.8
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
    \override BarNumber.font-size = #-1
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
    % A page turn is permitted where the player has a rest of two bars or more.
    \consists Page_turn_engraver
    pageTurnMinimumRestLength = #2
  }
}
"""

SCORE_PAPER = r"""
\paper {
  #(set-paper-size "11x17")
  top-margin = 12\mm
  bottom-margin = 12\mm
  left-margin = 14\mm
  right-margin = 12\mm
  indent = 28\mm
  short-indent = 14\mm
  system-separator-markup = \slashSeparator
  ragged-last-bottom = ##f
  print-page-number = ##t
}
"""

PART_PAPER = r"""
\paper {
  #(set-paper-size "arch a")
  top-margin = 12\mm
  bottom-margin = 14\mm
  left-margin = 14\mm
  right-margin = 14\mm
  indent = 0\mm
  ragged-last-bottom = ##t
  print-page-number = ##t
  page-breaking = #ly:page-turn-breaking
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

    def set_instrument(self, instrument: Instrument | None) -> None:
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

    def emit(self, elements: list[music.Element]) -> str:
        parts = []
        for element in _merge_full_bar_rests(elements):
            if isinstance(element, music.Command) and element.name == "switch":
                name = element.arguments[0].strip('"')
                instrument = self.work.orchestra.instruments.get(name)
                self.set_instrument(instrument)
                label = name[0].upper() + name[1:]
                parts.append(
                    f'\\clef {self.clef_of(instrument)} <>^\\markup \\instrumentchange "{label}"'
                )
            elif isinstance(element, music.Group) and element.kind == "parallel":
                voices = [f"{{ {self.emit(child.children)} }}" for child in element.children]
                parts.append("<< " + " \\\\ ".join(voices) + " >>")
            elif isinstance(element, music.Group):
                inner = self.emit(element.children)
                prefix = f"{element.header} " if element.kind != "sequence" else ""
                parts.append(f"{prefix}{{ {inner} }}")
            else:
                parts.append(music.to_lilypond(element, self.interval))
        return " ".join(parts).replace("\n ", "\n")


def _merge_full_bar_rests(elements: list[music.Element]) -> list[music.Element]:
    """Join adjacent full-bar rests into one rest.

    LilyPond shows one long rest as a rest with a number in the parts. It does
    not join rests that are written one bar at a time.
    """
    merged: list[music.Element] = []
    run: music.Rest | None = None
    for element in elements:
        plain_rest = isinstance(element, music.Rest) and element.kind == "R" and not element.posts
        if plain_rest:
            if run is None:
                run = music.Rest("R", element.duration, "")
                merged.append(run)
            else:
                run.duration += element.duration
            whole = run.duration / 4
            run.duration_text = (
                f"1*{whole.numerator}"
                if whole.denominator == 1
                else f"1*{whole.numerator}/{whole.denominator}"
            )
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


def _pitches(elements: list[music.Element]) -> list[float]:
    """Return the MIDI numbers of all notes in the elements."""
    found: list[float] = []
    for element in elements:
        if isinstance(element, music.Note):
            found.extend(note_pitch.pitch.midi for note_pitch in element.pitches)
        elif isinstance(element, music.Group):
            found.extend(_pitches(element.children))
    return found


def best_clef(base: str, instrument: Instrument | None, written: list[float]) -> str:
    """Return the clef for a passage: the usual clef, or a better clef for its range."""
    if not written or instrument is None or base in ("percussion", "grand"):
        return base
    ordered = sorted(written)
    median, lowest = ordered[len(ordered) // 2], ordered[0]
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
    current = ""
    ottava = 0
    for chunk in chunks:
        shift = emitter.interval.semitones if emitter.interval else 0
        written = [midi + shift for midi in _pitches(chunk.children)]
        clef = best_clef(emitter.clef_of(instrument), instrument, written)
        if clef != current:
            elements.append(music.Command("clef", [clef]))
            current = clef
        octave = best_ottava(clef, instrument, written)
        if octave != ottava:
            elements.append(music.Command("ottava", [f"#{octave}"]))
            ottava = octave
        elements.extend(chunk.children)
        # A change of instrument in the chunk changes the usual clef.
        for command in _walk_commands(chunk.children):
            if command.name == "switch":
                instrument = work.orchestra.instruments.get(command.arguments[0].strip('"'))
                emitter.set_instrument(instrument)
                current = emitter.clef_of(instrument)
    emitter.set_instrument(work.orchestra.first_instrument(player.id))
    return elements


def _player_music(work: Work, player: Player, *, for_part: bool) -> str:
    emitter = _Emitter(work, for_part, left_hand=player.id.endswith(".lh"))
    instrument = work.orchestra.first_instrument(player.id)
    emitter.set_instrument(instrument)
    chunks = [chunk for _first_bar, chunk in work.chunks.get(player.id, [])]
    return emitter.emit(_with_clefs(work, player, chunks, emitter, instrument))


def _header(work: Work, instrument_line: str = "") -> str:
    lines = [
        "\\header {",
        f'  title = "{work.title}"',
        f'  subtitle = "{work.subtitle}"' if work.subtitle else "",
        f'  composer = "{work.composer}"' if work.composer else "",
        f'  instrument = "{instrument_line}"' if instrument_line else "",
        "  tagline = ##f",
        "}",
    ]
    return "\n".join(line for line in lines if line)


def _definitions(
    work: Work, players: list[Player], *, for_part: bool, breaks: set[int] | None = None
) -> str:
    structure = work.structure if breaks is None else replace(work.structure, breaks=breaks)
    blocks = [
        "global = {\n\\accidentalStyle Score.modern\n\\numericTimeSignature\n"
        + global_to_lilypond(structure)
        + "\n}"
    ]
    for player in players:
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


def _score_staves(work: Work) -> str:
    blocks = []
    for family, members in _groups(work):
        staves = []
        index = 0
        while index < len(members):
            player = members[index]
            if player.id.endswith(".rh"):
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
        blocks.append(f'\\new StaffGroup = "{family}" <<\n  {joined}\n>>')
    return "\n".join(blocks)


FAMILY_TITLES = {
    "woodwinds": "Woodwinds",
    "brass": "Brass",
    "percussion": "Percussion",
    "plucked": "Harp and plucked instruments",
    "keyboards": "Keyboards",
    "strings": "Strings",
}


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


def _instrument_lines(work: Work) -> dict[str, list[str]]:
    """Return the list of the players for the first page: one line for each player."""
    from ..perform.events import perform

    lines: dict[str, list[str]] = {family: [] for family in FAMILY_ORDER}
    for player in work.orchestra.players:
        if player.id.endswith(".lh"):
            continue
        hands = [player.id]
        if player.id.endswith(".rh"):
            hands.append(player.id[: -len(".rh")] + ".lh")
        used: list[str] = []
        for hand in hands:
            for note in perform(work, hand):
                if note.instrument not in used:
                    used.append(note.instrument)
        if not used:
            continue
        first = player.instruments[0]
        if player.family == "percussion" and len(player.instruments) > 1:
            line = f"{player.name}: {', '.join(used)}"
        else:
            others = [name for name in used if name != first]
            also = "also " if first in used else ""
            line = player.name + (f" ({also}{', '.join(others)})" if others else "")
        if player.count > 1 and player.family == "strings":
            line += f" ({player.count} players)"
        lines[player.family].append(line)
    return lines


def _front_page(work: Work) -> str:
    """Return the first page of the score: the list of the players and the notes."""

    def text(value: str) -> str:
        return '"' + value.replace("\\", "").replace('"', "'") + '"'

    def wrapped(value: str) -> str:
        words = " ".join(text(word) for word in value.split())
        return f"\\wordwrap {{ {words} }}"

    families = _instrument_lines(work)
    columns: list[list[str]] = [[], []]
    for family in FAMILY_ORDER:
        if not families[family]:
            continue
        target = columns[0] if family in ("woodwinds", "brass") else columns[1]
        target.append(f"\\vspace #1 \\line {{ \\bold {text(FAMILY_TITLES[family])} }}")
        target.extend(f"\\line {{ {text(line)} }}" for line in families[family])
    left = "\n      ".join(columns[0])
    right = "\n      ".join(columns[1])
    notes = "\n    ".join(f"\\vspace #0.4 {wrapped(note)}" for note in score_notes(work))
    return (
        "\\markup \\fontsize #4 \\column {\n"
        '  \\vspace #2 \\line { \\bold \\fontsize #2 "Orchestra" }\n'
        "  \\line {\n"
        f"    \\column {{\n      {left}\n    }}\n"
        "    \\hspace #14\n"
        f"    \\column {{\n      {right}\n    }}\n"
        "  }\n"
        '  \\vspace #2 \\line { \\bold \\fontsize #2 "Notes for the performance" }\n'
        f"  \\override #'(line-width . 110) \\column {{\n    {notes}\n  }}\n"
        "}\n\n\\pageBreak"
    )


def score_breaks(work: Work, capacity: float = 56.0, most_bars: int = 10) -> set[int]:
    """Return the bars after which the conductor score starts a new system.

    The width of a bar depends on the number of different moments at which
    a note starts. A system gets bars until it is full.
    """
    from ..perform.events import perform

    structure = work.structure
    starts = [float(bar.start) for bar in structure.bars]
    moments: list[set[float]] = [set() for _ in structure.bars]
    for player in work.orchestra.players:
        for note in perform(work, player.id):
            position = float(note.start)
            moments[bisect.bisect_right(starts, position) - 1].add(position)
    breaks: set[int] = set()
    load, count = 0.0, 0
    for bar, columns in zip(structure.bars, moments, strict=True):
        width = max(len(columns), 2) + 1.5
        if count and (load + width > capacity or count >= most_bars):
            breaks.add(bar.number - 1)
            load, count = 0.0, 0
        load += width
        count += 1
    return breaks


def score_file(work: Work) -> str:
    """Return the LilyPond text of the conductor score."""
    breaks = score_breaks(work)
    return (
        "\n\n".join(
            [
                f'\\version "{LILYPOND_VERSION}"',
                STYLE.strip(),
                techniques.lilypond_definitions(),
                "#(set-global-staff-size 13)",
                SCORE_PAPER.strip(),
                _header(work, "Score in C"),
                _front_page(work),
                _definitions(work, work.orchestra.players, for_part=False, breaks=breaks),
                "\\score {\n<<\n" + _score_staves(work) + "\n>>\n" + SCORE_LAYOUT.strip() + "\n}",
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
                STYLE.strip(),
                techniques.lilypond_definitions(),
                "#(set-global-staff-size 19)",
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
        body = emitter.emit(children)
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
                STYLE.strip(),
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
