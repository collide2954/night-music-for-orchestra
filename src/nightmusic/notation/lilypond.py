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
