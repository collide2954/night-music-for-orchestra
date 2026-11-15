"""Write the work as a MusicXML file, for a playback program.

MuseScore reads this file and plays it with its sample libraries. The file
is for the sound only: it is not the printed score. Thus:

- All parts are at sounding pitch.
- Each instrument of a player is one part. A player who changes the
  instrument has two or more parts.
- The tempo is given at each bar line, and at each quarter note where the
  tempo changes gradually. Thus the time of each bar is the same as in the
  tempo plan of the work.
- Rests are not written: the reader fills the empty time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from xml.sax.saxutils import escape

from . import music
from .techniques import TECHNIQUES
from .work import Work

DIVISIONS = 6720  # parts of a quarter note: 64th notes, triplets, quintuplets, septuplets

# Instrument of the work: the name of the part and the MusicXML sound identifier.
SOUNDS = {
    "piccolo": ("Piccolo", "wind.flutes.piccolo"),
    "flute": ("Flute", "wind.flutes.flute"),
    "alto flute": ("Alto Flute", "wind.flutes.flute.alto"),
    "oboe": ("Oboe", "wind.reed.oboe"),
    "English horn": ("English Horn", "wind.reed.english-horn"),
    "clarinet in E-flat": ("E♭ Clarinet", "wind.reed.clarinet.eflat"),
    "clarinet in B-flat": ("B♭ Clarinet", "wind.reed.clarinet.bflat"),
    "bass clarinet": ("Bass Clarinet", "wind.reed.clarinet.bass"),
    "contrabass clarinet": ("Contrabass Clarinet", "wind.reed.clarinet.contrabass"),
    "bassoon": ("Bassoon", "wind.reed.bassoon"),
    "contrabassoon": ("Contrabassoon", "wind.reed.contrabassoon"),
    "horn in F": ("Horn in F", "brass.french-horn"),
    "trumpet in C": ("C Trumpet", "brass.trumpet.c"),
    "tenor trombone": ("Trombone", "brass.trombone.tenor"),
    "bass trombone": ("Bass Trombone", "brass.trombone.bass"),
    "tuba": ("Tuba", "brass.tuba"),
    "timpani": ("Timpani", "drum.timpani"),
    "vibraphone": ("Vibraphone", "pitched-percussion.vibraphone"),
    "marimba": ("Marimba", "pitched-percussion.marimba"),
    "glockenspiel": ("Glockenspiel", "pitched-percussion.glockenspiel"),
    "crotales": ("Crotales", "metal.crotales"),
    "xylophone": ("Xylophone", "pitched-percussion.xylophone"),
    "tubular bells": ("Tubular Bells", "pitched-percussion.tubular-bells"),
    "harp": ("Harp", "pluck.harp"),
    "celesta": ("Celesta", "keyboard.celesta"),
    "piano": ("Piano", "keyboard.piano"),
    "violin": ("Violins", "strings.group"),
    "viola": ("Violas", "strings.group"),
    "violoncello": ("Violoncellos", "strings.group"),
    "double bass": ("Contrabasses", "strings.group"),
}

# One player of a string section alone.
SOLO_SOUNDS = {
    "violin": ("Violin", "strings.violin"),
    "viola": ("Viola", "strings.viola"),
    "violoncello": ("Violoncello", "strings.cello"),
    "double bass": ("Contrabass", "strings.contrabass"),
}

TYPE_NAMES = {
    Fraction(16): "long",
    Fraction(8): "breve",
    Fraction(4): "whole",
    Fraction(2): "half",
    Fraction(1): "quarter",
    Fraction(1, 2): "eighth",
    Fraction(1, 4): "16th",
    Fraction(1, 8): "32nd",
    Fraction(1, 16): "64th",
}
STEP_LETTERS = "CDEFGAB"
ARTICULATIONS = {
    "staccato": "staccato",
    "accent": "accent",
    "tenuto": "tenuto",
    "marcato": "strong-accent",
    "staccatissimo": "staccatissimo",
    "portato": "detached-legato",
}
DYNAMIC_ELEMENTS = {
    "ppppp", "pppp", "ppp", "pp", "p", "mp", "mf", "f", "ff", "fff", "ffff", "fffff",
    "sf", "sfz", "sffz", "fz", "rfz", "fp", "sfp", "sfpp", "pf",
}  # fmt: skip

# Playing techniques that the playback program knows: the words in the
# file, and the attribute of the `sound` element (if there is one).
TECHNIQUE_WORDS = {
    "pizz": ("pizz.", 'pizzicato="yes"'),
    "arco": ("arco", 'pizzicato="no"'),
    "collegno": ("col legno", ""),
    "sulpont": ("sul pont.", ""),
    "sultasto": ("sul tasto", ""),
    "ord": ("ord.", ""),
    "consord": ("con sord.", ""),
    "senzasord": ("senza sord.", ""),
}


def can_play(instrument: str) -> bool:
    """Return true if the playback program has a sound for the instrument."""
    return instrument in SOUNDS


@dataclass
class _Event:
    """One note of a player, with its place in the work."""

    start: Fraction  # quarter notes from the start of the work
    length: Fraction  # sounding length in quarter notes (0 for a grace note)
    written: Fraction  # written length, before the factor of a tuplet
    ratio: Fraction  # factor of the tuplet (1 = no tuplet)
    note: music.Note
    voice: int
    grace: bool
    instrument: str
    solo: bool
    tuplet: str = ""  # "start" or "stop": the first and the last note of a tuplet
    before: list[str] = field(default_factory=list)  # directions before the note


@dataclass
class _State:
    """The state of a player while the code reads the music."""

    instrument: str
    solo: bool = False
    dynamic: str = ""
    techniques: dict[str, str] = field(default_factory=dict)  # state -> technique name


def _walk(
    elements: list[music.Element],
    position: Fraction,
    scale: Fraction,
    voice: int,
    state: _State,
    events: list[_Event],
    *,
    grace: bool = False,
) -> Fraction:
    for element in elements:
        if isinstance(element, music.Command):
            if element.name == "switch":
                state.instrument = element.arguments[0].strip('"')
                state.solo = False
                state.techniques = {}
        elif isinstance(element, music.Rest):
            _read_marks(element.posts, state)
            position += element.duration * scale
        elif isinstance(element, music.Note):
            _read_marks(element.posts, state)
            length = Fraction(0) if grace else element.duration * scale
            events.append(
                _Event(position, length, element.duration, scale, element, voice, grace,
                       state.instrument, state.solo and state.instrument in SOLO_SOUNDS)
            )  # fmt: skip
            position += length
        elif isinstance(element, music.Group):
            if element.kind == "grace":
                _walk(element.children, position, scale, voice, state, events, grace=True)
            elif element.kind == "parallel":
                end = position
                for number, child in enumerate(element.children):
                    end = max(end, _walk(child.children, position, scale, number, state, events))
                position = end
            elif element.kind in ("unfold", "tremolo"):
                for _ in range(element.count):
                    position = _walk(element.children, position, scale, voice, state, events)
            elif element.kind == "tuplet":
                first = len(events)
                position = _walk(
                    element.children, position, scale * element.ratio, voice, state, events
                )
                inside = [event for event in events[first:] if not event.grace]
                if inside:
                    inside[0].tuplet = "start"
                    inside[-1].tuplet = "stop"
            else:
                position = _walk(element.children, position, scale, voice, state, events)
    return position


def _read_marks(posts: list[music.Post], state: _State) -> None:
    """Keep the dynamic mark and the techniques in effect."""
    for post in posts:
        if post.kind == "dynamic" and post.value in DYNAMIC_ELEMENTS:
            state.dynamic = post.value
        elif post.kind == "command":
            technique = TECHNIQUES.get(post.value)
            if technique and technique.state == "desk":
                state.solo = technique.value == "solo"
            elif technique and technique.state and post.value in TECHNIQUE_WORDS:
                state.techniques[technique.state] = post.value


def _note_type(written: Fraction) -> tuple[str, int]:
    """Return the note value and the number of dots for a written length."""
    for dots in range(3):
        base = written / (2 - Fraction(1, 2**dots))
        if base in TYPE_NAMES:
            return TYPE_NAMES[base], dots
    # A length with no usual note value: the nearest shorter note value.
    for base in sorted(TYPE_NAMES, reverse=True):
        if base <= written:
            return TYPE_NAMES[base], 0
    return "64th", 0


def _pitch_xml(pitch) -> str:
    alter = float(pitch.alter)
    text = f"<step>{STEP_LETTERS[pitch.step]}</step>"
    if alter:
        text += f"<alter>{alter:g}</alter>"
    return f"<pitch>{text}<octave>{pitch.octave}</octave></pitch>"


def _direction(inner: str, sound: str = "") -> str:
    tail = f"<sound {sound}/>" if sound else ""
    return f"<direction><direction-type>{inner}</direction-type>{tail}</direction>"


def _marks_before(event: _Event, hairpin_open: bool) -> tuple[list[str], bool]:
    """Return the directions before a note, and if a hairpin is open after it."""
    result: list[str] = []
    posts = event.note.posts
    dynamics = [p.value for p in posts if p.kind == "dynamic" and p.value in DYNAMIC_ELEMENTS]
    hairpins = [p.value for p in posts if p.kind == "hairpin"]
    if hairpin_open and (dynamics or hairpins):
        result.append(_direction('<wedge type="stop"/>'))
        hairpin_open = False
    for name in dynamics:
        result.append(_direction(f"<dynamics><{name}/></dynamics>"))
    for value in hairpins:
        if value in "<>":
            kind = "crescendo" if value == "<" else "diminuendo"
            result.append(_direction(f'<wedge type="{kind}"/>'))
            hairpin_open = True
    for post in posts:
        if post.kind == "command" and post.value in TECHNIQUE_WORDS:
            words, sound = TECHNIQUE_WORDS[post.value]
            result.append(_direction(f"<words>{escape(words)}</words>", sound))
    return result, hairpin_open


def _note_xml(event: _Event, index: int, length: Fraction, ties: tuple[bool, bool]) -> str:
    """Return one note of a chord (or a single note) as MusicXML."""
    note = event.note
    pitch = note.pitches[index].pitch
    kinds = {post.kind for post in note.posts}
    commands = {post.value for post in note.posts if post.kind == "command"}
    parts = ["<note>"]
    if event.grace:
        parts.append("<grace/>")
    if index:
        parts.append("<chord/>")
    parts.append(_pitch_xml(pitch))
    if not event.grace:
        parts.append(f"<duration>{int(length * DIVISIONS)}</duration>")
    tie_stop, tie_start = ties
    if tie_stop:
        parts.append('<tie type="stop"/>')
    if tie_start:
        parts.append('<tie type="start"/>')
    parts.append(f"<voice>{event.voice + 1}</voice>")
    name, dots = _note_type(event.written if length == event.length else length / event.ratio)
    parts.append(f"<type>{name}</type>" + "<dot/>" * dots)
    if event.ratio != 1:
        parts.append(
            f"<time-modification><actual-notes>{event.ratio.denominator}</actual-notes>"
            f"<normal-notes>{event.ratio.numerator}</normal-notes></time-modification>"
        )
    notations: list[str] = []
    if tie_stop:
        notations.append('<tied type="stop"/>')
    if tie_start:
        notations.append('<tied type="start"/>')
    if index == 0:
        for post in note.posts:
            if post.kind == "slur":
                kind = "start" if post.value == "(" else "stop"
                notations.append(f'<slur type="{kind}" number="1"/>')
            elif post.kind == "phrasing":
                kind = "start" if post.value == "(" else "stop"
                notations.append(f'<slur type="{kind}" number="2"/>')
        if event.tuplet:
            notations.append(f'<tuplet type="{event.tuplet}"/>')
        names = [post.value for post in note.posts if post.kind == "articulation"]
        names += [name for name in ARTICULATIONS if name in commands]
        marks = "".join(f"<{ARTICULATIONS[name]}/>" for name in dict.fromkeys(names)
                        if name in ARTICULATIONS)  # fmt: skip
        if marks:
            notations.append(f"<articulations>{marks}</articulations>")
        if "tremolo" in kinds:
            value = next(post.value for post in note.posts if post.kind == "tremolo")
            strokes = {"8": 1, "16": 2, "32": 3, "64": 4}.get(value, 3)
            notations.append(f'<ornaments><tremolo type="single">{strokes}</tremolo></ornaments>')
        technical = ""
        if "stopped" in commands or "stopped" in names:
            technical += "<stopped/>"
        if "flageolet" in commands:
            technical += "<harmonic/>"
        if technical:
            notations.append(f"<technical>{technical}</technical>")
    if notations:
        parts.append("<notations>" + "".join(notations) + "</notations>")
    parts.append("</note>")
    return "".join(parts)


def _tempo_points(work: Work, first: Fraction, last: Fraction) -> dict[Fraction, float]:
    """Return the tempo at each bar line, and at each quarter note of a gradual change.

    Each value is the mean tempo from its point to the subsequent point. Thus
    the time of each point is the same as in the tempo plan of the work.
    """
    structure = work.structure
    points: set[Fraction] = set()
    for bar in structure.bars:
        if first <= bar.start < last:
            points.add(bar.start)
    ordered = structure.tempo_points
    for index, point in enumerate(ordered):
        if first <= point.position < last:
            points.add(point.position)
        if point.glide and index + 1 < len(ordered):
            position = point.position
            while position < ordered[index + 1].position:
                if first <= position < last:
                    points.add(position)
                position += 1
    result: dict[Fraction, float] = {}
    places = sorted(points) + [last]
    for start, end in zip(places[:-1], places[1:], strict=True):
        seconds = structure.seconds(end) - structure.seconds(start)
        result[start] = 60.0 * float(end - start) / seconds
    return result


def score(
    work: Work, bars: tuple[int, int] | None = None, instruments: set[str] | None = None
) -> tuple[str, list[str]]:
    """Return the MusicXML text of the work, and the names of the parts in it.

    `bars` gives the first and the last bar (default: the full work).
    `instruments` gives the instruments that are in the file (default: all
    instruments that the playback program can play).
    """
    structure = work.structure
    first_bar, last_bar = bars or (1, len(structure.bars))
    measures = structure.bars[first_bar - 1 : last_bar]
    begin, end = measures[0].start, measures[-1].end
    tempos = _tempo_points(work, begin, end)

    # The parts: one for each instrument of each player (and one for a solo player).
    parts: dict[tuple[str, str, bool], list[_Event]] = {}
    starts: dict[tuple[str, str, bool], _State] = {}
    for player in work.orchestra.players:
        state = _State(player.instruments[0])
        events: list[_Event] = []
        _walk(work.music_of(player.id).children, Fraction(0), Fraction(1), 0, state, events)
        running = _State(player.instruments[0])
        for event in events:
            key = (player.id, event.instrument, event.solo)
            wanted = can_play(event.instrument) and (
                instruments is None or event.instrument in instruments
            )
            if event.start < begin:
                _read_marks(event.note.posts, running)
            elif event.start < end and wanted:
                if key not in parts:
                    parts[key] = []
                    starts[key] = _State(
                        event.instrument, event.solo, running.dynamic, dict(running.techniques)
                    )
                parts[key].append(event)
                _read_marks(event.note.posts, running)
            elif event.start < end:
                _read_marks(event.note.posts, running)

    names: list[str] = []
    part_list: list[str] = []
    bodies: list[str] = []
    for number, (key, events) in enumerate(parts.items(), start=1):
        player_id, instrument, solo = key
        name, sound = (SOLO_SOUNDS if solo else SOUNDS)[instrument]
        label = f"{name} ({player_id})"
        names.append(label)
        tags = "<solo/>" if solo or sound != "strings.group" else "<ensemble/>"
        part_list.append(
            f'<score-part id="P{number}"><part-name>{escape(name)}</part-name>'
            f'<score-instrument id="P{number}-I1"><instrument-name>{escape(name)}'
            f"</instrument-name><instrument-sound>{sound}</instrument-sound>{tags}"
            f"</score-instrument></score-part>"
        )
        bodies.append(
            _part_xml(number, events, measures, tempos if number == 1 else {}, starts[key])
        )
    text = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
        '"http://www.musicxml.org/dtds/partwise.dtd">\n'
        '<score-partwise version="4.0">\n'
        f"<work><work-title>{escape(work.title)}</work-title></work>\n"
        "<part-list>\n" + "\n".join(part_list) + "\n</part-list>\n" + "\n".join(bodies) + "\n"
        "</score-partwise>\n"
    )
    return text, names


def _part_xml(number: int, events: list[_Event], measures, tempos, start: _State) -> str:
    lines = [f'<part id="P{number}">']
    by_voice: dict[int, list[_Event]] = {}
    for event in events:
        by_voice.setdefault(event.voice, []).append(event)
    open_ties: dict[int, set[float]] = {voice: set() for voice in by_voice}
    hairpins: dict[int, bool] = {voice: False for voice in by_voice}
    cursors = {voice: 0 for voice in by_voice}
    previous = None
    first_note = True
    for bar in measures:
        lines.append(f'<measure number="{bar.number}">')
        metre = (bar.numerator, bar.denominator)
        if previous != metre:
            head = f"<divisions>{DIVISIONS}</divisions><key><fifths>0</fifths></key>"
            lines.append(
                f"<attributes>{head if previous is None else ''}<time><beats>{bar.numerator}"
                f"</beats><beat-type>{bar.denominator}</beat-type></time>"
                + ("<clef><sign>G</sign><line>2</line></clef>" if previous is None else "")
                + "</attributes>"
            )
            previous = metre
        # The tempo points of this bar (only the first part has them).
        moved = Fraction(0)
        for position in sorted(p for p in tempos if bar.start <= p < bar.end):
            offset = position - bar.start
            if offset > moved:
                lines.append(_forward(offset - moved))
                moved = offset
            lines.append(f'<direction><direction-type><words></words></direction-type>'
                         f'<sound tempo="{tempos[position]:.4f}"/></direction>')  # fmt: skip
        if moved:
            lines.append(_backup(moved))
        bar_length = bar.end - bar.start
        for voice, voice_events in by_voice.items():
            cursor = bar.start
            index = cursors[voice]
            wrote = False
            while index < len(voice_events) and voice_events[index].start < bar.end:
                event = voice_events[index]
                index += 1
                if event.start > cursor:
                    lines.append(_forward(event.start - cursor))
                    cursor = event.start
                before, hairpins[voice] = _marks_before(event, hairpins[voice])
                if first_note:
                    before = _state_marks(start) + before
                    first_note = False
                lines.extend(before)
                length = min(event.length, bar.end - cursor)  # a note stops at the bar line
                tie_out = any(post.kind == "tie" for post in event.note.posts)
                for pitch_index, note_pitch in enumerate(event.note.pitches):
                    midi = note_pitch.pitch.midi
                    tie_in = midi in open_ties[voice]
                    lines.append(_note_xml(event, pitch_index, length, (tie_in, tie_out)))
                still = {p.pitch.midi for p in event.note.pitches} if tie_out else set()
                if not event.grace:
                    open_ties[voice] = still
                    cursor += length
                wrote = True
            cursors[voice] = index
            if cursor < bar.end and wrote:
                lines.append(_forward(bar.end - cursor))
            if wrote or voice == 0:
                if not wrote:
                    lines.append(
                        f'<note><rest measure="yes"/><duration>{int(bar_length * DIVISIONS)}'
                        f"</duration><voice>1</voice></note>"
                    )
                lines.append(_backup(bar_length))
        if lines[-1].startswith("<backup>"):
            lines.pop()
        lines.append("</measure>")
    lines.append("</part>")
    return "\n".join(lines)


def _state_marks(state: _State) -> list[str]:
    """Return the directions for the state at the first note of an excerpt."""
    result = []
    if state.dynamic:
        result.append(_direction(f"<dynamics><{state.dynamic}/></dynamics>"))
    for name in state.techniques.values():
        words, sound = TECHNIQUE_WORDS[name]
        if name not in ("arco", "ord", "senzasord"):
            result.append(_direction(f"<words>{escape(words)}</words>", sound))
    return result


def _forward(length: Fraction) -> str:
    return f"<forward><duration>{int(length * DIVISIONS)}</duration></forward>"


def _backup(length: Fraction) -> str:
    return f"<backup><duration>{int(length * DIVISIONS)}</duration></backup>"
