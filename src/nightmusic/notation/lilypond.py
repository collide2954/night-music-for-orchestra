"""Write the conductor score and the parts as LilyPond files."""

from __future__ import annotations

from dataclasses import dataclass
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
    skipBars = ##t
  }
  \context {
    \Staff
    \override TextScript.font-size = #-0.5
    \override DynamicTextSpanner.style = #'none
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


def _player_music(work: Work, player: Player, *, for_part: bool) -> str:
    emitter = _Emitter(work, for_part, left_hand=player.id.endswith(".lh"))
    instrument = work.orchestra.first_instrument(player.id)
    emitter.set_instrument(instrument)
    body = emitter.emit(work.music_of(player.id).children)
    return f"\\clef {emitter.clef_of(instrument)}\n{body}"


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


def _definitions(work: Work, players: list[Player], *, for_part: bool) -> str:
    blocks = [
        "global = {\n\\accidentalStyle Score.modern\n" + global_to_lilypond(work.structure) + "\n}"
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


def score_file(work: Work) -> str:
    """Return the LilyPond text of the conductor score."""
    return (
        "\n\n".join(
            [
                f'\\version "{LILYPOND_VERSION}"',
                STYLE.strip(),
                techniques.lilypond_definitions(),
                "#(set-global-staff-size 13)",
                SCORE_PAPER.strip(),
                _header(work, "Score in C"),
                _definitions(work, work.orchestra.players, for_part=False),
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


def video_file(work: Work, index: int, staff_size: float) -> str:
    """Return the LilyPond text of one section, as a page for the video."""
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
        if seconds >= VIDEO_SECONDS_PER_SCREEN:
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
        body = emitter.emit(work.chunks[player.id][index][1].children)
        blocks.append(
            f"{identifier(player.id)} = {{\n\\clef {emitter.clef_of(instrument)}\n{body}\n}}"
        )
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
    width, height = VIDEO_PAGE_MM
    paper = (
        "\\paper {\n"
        f"  #(set-paper-size '(cons (* {width} mm) (* {height} mm)))\n"
        "  top-margin = 8\\mm\n  bottom-margin = 8\\mm\n  left-margin = 10\\mm\n"
        "  right-margin = 10\\mm\n  indent = 20\\mm\n  short-indent = 20\\mm\n"
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
                "\\score {\n<<\n" + "\n".join(groups) + "\n>>\n" + VIDEO_LAYOUT.strip() + "\n}",
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
