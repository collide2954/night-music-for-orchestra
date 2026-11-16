"""The second half of the piano interlude (the marks Y and Z).

- Mark Y, bars 1 to 16: a fast and soft scherzo. The calls of the night
  (the cricket, the bird) are now quick figures. The piano and the woodwinds
  trade them: first two bars each, then one bar, then one beat group. The
  strings pluck. All figures go up by minor thirds.
- Mark Y, bars 17 to 32: the build. The hammer theme comes back with the
  full orchestra. The bass now goes up by major thirds (E-flat, G, B): the
  interval of the bright half of the work. In the rests of the chords, the
  woodwinds and the strings trade fast figures. Then octaves of the piano in
  alternate hands above the bass note E-flat, a glissando, and one stroke of
  the full orchestra.
- Mark Z: the cadenza. The piano alone: octaves down the full keyboard, a
  memory of the night in bare octaves, waves of two chords (E-flat 7 and
  A 7: they have two notes in common), and the motto in the bass with a new
  last note: D, E-flat, A-flat, and then A. A long trill. The orchestra comes
  back below the trill and grows to a chord of all twelve notes (tritones
  and fifths). Then silence, and the turn.

The bass note E-flat of the cadenza is one semitone above the tonic D: the
turn of the work is this step down.
"""

from __future__ import annotations

import re

from ..compose.tools import Block, octave, rests, run, tr
from ..notation.work import Work
from .interlude import (
    EIGHT,
    OCT,
    REST,
    SNARE,
    TOCCATA,
    _hammer_bar,
    accents,
    hammer,
    marked,
    sixteenths,
    slurred,
)

# The scale of the two chords E-flat 7 and A 7 (semitone, whole tone, from E-flat).
PIVOT = "es e fis g a bes c des"

# The calls of the night as figures of the toccata, on E-flat (one bar each).
CRICKET = (
    "es'''16 es''' es''' es''' es''' es''' d''' es''' ges''' es''' d''' es''' as'''8-. es'''8-. |"
)
BIRD = "ges'''16 ges''' ges''' ges''' f''' es''' d''' es''' d''' c''' b'' c''' d'''8-. as''8-. |"

# Short cells for the trades of one beat group, on A-flat.
CELL_REPEAT = ["as''", "as''", "as''", "as''", "a''", "as''"]
CELL_ARCH = ["as''", "a''", "d'''", "es'''", "d'''", "a''"]
CELL_UP = ["as''", "a''", "d'''", "es'''"]
CELL_DOWN = ["es'''", "d'''", "a''", "as''"]


def write(work: Work) -> None:
    """Write the marks Y and Z."""
    _trades(work)
    _build(work)
    _cadenza(work)
    _return(work)


def _cells(first: list[str] | None, second: list[str] | None, third: list[str] | None) -> str:
    """Return one bar of 8/8: a cell or a rest in each of its three beat groups."""
    tokens: list = []
    for cell, size in ((first, 6), (second, 6), (third, 4)):
        tokens += [marked(note) for note in cell] if cell else [None] * size
    return sixteenths(tokens)


NOTE = re.compile(r"(?<![a-z])(?:<[^>]+>|[a-g](?:eses|isis|es|is|s)?[',]*)\d+\.*")


def _with(text: str, marks: str) -> str:
    """Return the music with marks on its first note (a rest does not get them)."""
    found = NOTE.search(text)
    if found is None or not marks:
        return text
    return text[: found.end()] + marks + text[found.end() :]


# ------------------------------------------------------------------ mark Y


def _trades(work: Work) -> None:
    """Mark Y, bars 1 to 16: the calls of the night as a fast, soft scherzo of trades."""
    structure = work.structure
    s = work.section(16, *EIGHT)
    structure.mark(s.bar(1), "Y")
    four = REST * 4
    block = Block(s, four, four, four, four)

    # ---- phrase 1: two bars of the piano, two bars of the woodwinds (a minor third higher)
    block.add("pno.rh", 1, _with(CRICKET, r"\p\leggiero") + " " + BIRD + " " + REST * 2)
    block.add(
        "pno.lh", 1,
        r"es8-.\p r4 es8-. r4 bes,8-. r8 | bes,8-. r4 es8-. r4 as,8-. r8 | " + REST * 2,
    )  # fmt: skip
    winds = _with(tr(CRICKET, 3), r"\p") + " " + tr(BIRD, 3)
    block.add("fl1 fl2 fl3 perc2", 1, REST * 2 + winds)
    block.add("cl2 ob1", 1, REST * 2 + octave(winds, -1))
    plucked = accents("ges'", "-.", r"\p\pizz") + " " + accents("bes'", "-.")
    block.add("vn1 vn2", 1, REST * 2 + plucked)
    block.add("va", 1, REST * 2 + octave(plucked, -1))
    block.add("vc", 1, REST * 2 + accents("ges,", "-.", r"\p\pizz") + " " + accents("ges,", "-."))
    block.add("perc4", 1, accents("c'", "", r"\pp") + " " + accents("d'", "") + " " + REST * 2)

    # ---------------------------- phrase 2: one bar each, on A and on C, a little louder
    block.add(
        "pno.rh", 2,
        _with(tr(CRICKET, 6), r"\mp") + " " + REST + tr(BIRD, 9) + " " + REST,
    )  # fmt: skip
    block.add(
        "pno.lh", 2,
        r"a8-.\mp r4 a8-. r4 e8-. r8 | " + REST + r"c8-. r4 c8-. r4 ges8-. r8 | " + REST,
    )  # fmt: skip
    winds = REST + _with(tr(BIRD, 6), r"\mp") + " " + REST + octave(tr(CRICKET, 9), -1)
    block.add("fl1 fl2 fl3 perc2", 2, winds)
    block.add("cl2 ob1", 2, octave(winds, -1))
    plucked = REST + accents("a'", "-.", r"\mp") + " " + REST + accents("c''", "-.")
    block.add("vn1 vn2", 2, plucked)
    block.add("va", 2, octave(plucked, -1))
    block.add("vc", 2, REST + accents("a,", "-.", r"\mp") + " " + REST + accents("c", "-."))
    block.add("perc4", 2, accents("c'", "", r"\p") + " " + REST + accents("d'", "") + " " + REST)

    # ------------- phrase 3: one beat group each. The key goes up a minor third in each bar.
    # In each bar: which cell the piano and the woodwinds have in the three beat groups.
    plan = [
        (-5, (CELL_REPEAT, None, None), (None, CELL_ARCH, None), CELL_UP),
        (-2, (None, CELL_ARCH, None), (CELL_REPEAT, None, None), CELL_DOWN),
        (1, (CELL_ARCH, None, CELL_UP), (None, CELL_REPEAT, CELL_UP), CELL_UP),
        (4, (None, CELL_REPEAT, CELL_UP), (CELL_ARCH, None, CELL_UP), CELL_UP),
    ]
    piano, wood, strings, basses = [], [], [], []
    for number, (shift, piano_cells, wood_cells, last) in enumerate(plan):
        level = r"\mf" if number == 0 else ""
        piano.append(_with(tr(_cells(*piano_cells), shift), level))
        wood.append(_with(tr(_cells(*wood_cells), shift), level))
        strings.append(_with(tr(_cells(None, None, last), shift - 12), level))
        root = tr("as,", shift).strip()
        basses.append(f"{root}8-.{level} r4 {root}8-. r4 {root}8-. r8 |")
    block.add("pno.rh", 3, " ".join(piano))
    block.add("pno.lh", 3, " ".join(basses))
    block.add("fl1 fl2 fl3 perc2", 3, " ".join(wood))
    block.add("cl2 ob1", 3, octave(" ".join(wood), -1))
    block.add("vn1 vn2", 3, " ".join(strings))
    block.add("va", 3, octave(" ".join(strings), -1))
    block.add("vc", 3, " ".join(basses))
    block.add("perc5", 3, _with(SNARE, r"\pp\<") + SNARE * 3)

    # ------------------- phrase 4: the figures become the hammer again, louder and louder
    bars = [
        ("c,", "ges,", "<ges c'>", "<g des'>"),
        ("des,", "g,", "<g des'>", "<c' ges'>"),
        ("d,", "as,", "<as d'>", "<a es'>"),
    ]
    # The right hand comes from a high figure, and it goes to a run: it has a rest at
    # the start of the first bar and at the end of the last bar.
    right, left = zip(
        *[
            _hammer_bar(
                *bar,
                r"\mf\<" if number == 0 else "",
                skip_high=int(number == 0),
                tail=number < 2,
            )
            for number, bar in enumerate(bars)
        ],
        strict=True,
    )
    up = run(OCT, "es'", 16)
    block.add("pno.rh", 4, " ".join(right) + " " + _with(slurred(octave(up, 1)), r"\ff") + " |")
    block.add("pno.lh", 4, " ".join(left) + " " + slurred(octave(up, -1)) + " |")
    twitter = [_cells(CELL_REPEAT, CELL_REPEAT, CELL_UP), _cells(CELL_ARCH, CELL_REPEAT, CELL_DOWN)]
    line = " ".join(tr(twitter[number % 2], shift) for number, shift in enumerate((4, 5, 6, 7)))
    block.add("fl1 fl2 fl3 perc2", 4, _with(line, r"\mf\<"))
    block.add("cl2 ob1 cl1", 4, _with(octave(line, -1), r"\mf\<"))
    for player, notes in (("vn1", ["<c'' ges''>", "<des'' g''>", "<d'' as''>", "<es'' a''>"]),
                          ("vn2", ["<ges' c''>", "<g' des''>", "<as' d''>", "<a' es''>"]),
                          ("va", ["<c' ges'>", "<des' g'>", "<d' as'>", "<es' a'>"])):  # fmt: skip
        text = " ".join(f"{note}1:32" + (r"\p\<\arco\sulpont" if number == 0 else "") + " |"
                        for number, note in enumerate(notes))  # fmt: skip
        block.add(player, 4, text)
    block.add("vc cb", 4, " ".join(
        accents(note, "->", r"\mf\<\pizz" if number == 0 else "")
        for number, note in enumerate(["c,", "des,", "d,", "es,"])))  # fmt: skip
    block.add("perc5", 4, r"c'1:32\p\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32\f |")
    block.add("timp", 4, REST * 2 + r"es,1:32\p\< ~ | es,1:32\f |")
    for player, note in (("hn1", "es'"), ("hn2", "a"), ("hn3", "as"), ("hn4", "d")):
        block.add(player, 4, REST * 2 + rf"{note}1\p\<\stopped ~ | {note}1\f |")
    block.close()


# The chord of the accents in the build, on E-flat (the notes E-flat, E, A, B-flat).
BUILD_CHORD = {
    "tuba": "es,,", "btbn": "es,", "bn3": "es,,", "cbcl": "es,,", "cb": "es,", "vc": "es,",
    "tbn2": "bes,", "tbn1": "e", "hn4": "a", "hn3": "bes", "hn2": "e'", "hn1": "a'",
    "tpt3": "a'", "tpt2": "bes'", "tpt1": "e''", "bn2": "bes,", "bn1": "e",
}  # fmt: skip
BUILD_SCALES = ["es e fis g a bes c des", "g as bes b des d e f", "b c d es f ges as a"]


def _build(work: Work) -> None:
    """Mark Y, bars 17 to 32: the hammer theme with the full orchestra, and the peak."""
    s = work.section(16, *EIGHT)
    four = REST * 4
    block = Block(s, four, four, four, four)

    # -------- phrases 1 and 2: the bass goes up by major thirds (E-flat, G, B, E-flat)
    # In each bar: the full orchestra on the accents, and between them a trade of the
    # woodwinds (after the first accent) and the strings (after the second accent).
    reference = [
        ("es,", "bes,", "<bes es' a'>", "<e' bes' es''>"),
        ("es,", "e,", "<e' bes' es''>", "<a' es'' e''>"),
    ]
    starts = ["bes''", "e'''", "des'''", "g'''", "f'''", "b'''", "e'''", "des''''"]
    for phrase in (1, 2):
        right, left, wood, strings = [], [], [], []
        lines: dict[str, list[str]] = {player: [] for player in BUILD_CHORD}
        for step in range(2):
            level_number = 2 * (phrase - 1) + step  # 0 to 3: E-flat, G, B, E-flat
            shift = 4 * (level_number % 3)
            high = 12 if level_number == 3 else 0
            scale = BUILD_SCALES[level_number % 3]
            for index, (bass, fill, first, second) in enumerate(reference):
                loud = (r"\ff" if phrase == 1 else r"\fff") if step == 0 and index == 0 else ""
                # The very first bar comes after a run that ends high: each hand starts
                # one eighth note later.
                late = int(phrase == 1 and step == 0 and index == 0)
                bar = _hammer_bar(
                    tr(bass, shift).strip(), tr(fill, shift).strip(),
                    tr(first, shift + high).strip(), tr(second, shift + high).strip(), loud,
                    skip_low=late, skip_high=late,
                )  # fmt: skip
                right.append(bar[0])
                left.append(bar[1])
                for player, note in BUILD_CHORD.items():
                    lines[player].append(accents(tr(note, shift).strip(), "-^", loud))
                start = starts[2 * level_number + index]
                figure = run(scale, tr(start, 0).strip(), 4, down=index == 1)
                tail = run(scale, _last(figure), 3, down=index == 1).split()[1:]
                wood.append(f"r8 {_with(slurred(figure), loud)} r4. r8 {tail[0]}16( {tail[1]}) |")
                answer = run(scale, _last(figure), 5, down=index == 1).split()[1:]
                answer_text = f"{answer[0]}16( {' '.join(answer[1:])})"
                strings.append(f"r4. r8 {_with(answer_text, loud)} r8 {tail[0]}16( {tail[1]}) |")
        block.add("pno.rh", phrase, " ".join(right))
        block.add("pno.lh", phrase, " ".join(left))
        for player, bars in lines.items():
            marks = r"\arco\ord" if player in ("vc", "cb") and phrase == 1 else ""
            marks += r"\open" if player.startswith("hn") and phrase == 1 else ""
            block.add(player, phrase, _first_marks(" ".join(bars), marks))
        block.add("fl1 fl2 fl3 ob1:-1 ob2:-1 cl1:-1 cl2:-1", phrase, " ".join(wood))
        marks = r"\arco\ord" if phrase == 1 else ""
        block.add("vn1 vn2:-1 va:-2", phrase, _first_marks(" ".join(strings), marks))
        block.add(
            "timp",
            phrase,
            " ".join(accents("es,", "->", (r"\ff" if number == 0 else "")) for number in range(4)),
        )
        block.add(
            "perc3",
            phrase,
            " ".join(accents("c'", "->", (r"\ff" if number == 0 else "")) for number in range(4)),
        )
        block.add("perc5", phrase, _with(SNARE, r"\f") + SNARE * 3)
        block.add("perc6", phrase, " ".join(
            accents(note, "->", (r"\f" if number == 0 else ""))
            for number, note in enumerate(["a", "c'", "e'", "c'"])))  # fmt: skip

    # ------------ phrase 3: octaves in alternate hands, up and down, above the note E-flat
    steps_up = run(PIVOT, "es,", 33).split()
    steps_up[0] = steps_up[0].rstrip("0123456789")
    order = steps_up[:32] + steps_up[32:0:-1]  # up for two bars, then down for two bars
    right, left = [], []
    for number in range(4):
        notes = order[16 * number : 16 * number + 16]
        low = [marked(f"<{octave(note, -1).strip()} {note}>", "->" if i == 0 else "")
               for i, note in enumerate(notes[0::2])]  # fmt: skip
        high = [marked(f"<{note} {octave(note, 1).strip()}>") for note in notes[1::2]]
        if number == 0:
            low[0] = (low[0][0], r"->\ff\<")
            high[0] = (high[0][0], r"\ff\<")
        # The right hand comes from high chords: it starts with its third octave.
        bar = hammer(low, high, skip_high=2 if number == 0 else 0)
        right.append(bar[0])
        left.append(bar[1])
    block.add("pno.rh", 3, " ".join(right))
    block.add("pno.lh", 3, " ".join(left))
    # The orchestra holds the chord of E-flat 7 with a sharp ninth, and grows.
    swell = r"A1\p\< ~ | A1 ~ | A1 ~ | A1\ff |"
    held = {
        "tuba": "es,,", "btbn": "es,", "tbn2": "bes,", "tbn1": "g", "hn4": "des'", "hn3": "es'",
        "hn2": "g'", "hn1": "bes'", "tpt3": "des''", "tpt2": "fis''", "tpt1": "g''",
        "bn3": "es,,", "cbcl": "es,,", "bn2": "bes,", "bn1": "g", "cl3": "des'",
    }  # fmt: skip
    for player, note in held.items():
        block.add(player, 3, swell.replace("A", note))
    tremolo = r"A1:32\p\< ~ | A1:32 ~ | A1:32 ~ | A1:32\ff |"
    for player, note in (("vn1", "<g'' des'''>"), ("vn2", "<bes' fis''>"), ("va", "<des' g'>"),
                         ("vc", "<es bes>"), ("cb", "es,")):  # fmt: skip
        block.add(player, 3, tremolo.replace("A", note))
    block.add("timp", 3, tremolo.replace("A", "es,"))
    block.add("perc3", 3, tremolo.replace("A", "c'"))
    block.add("perc1", 3, r"""\switch "suspended cymbals" R1*2 | c'1:32\p\< ~ | c'1:32\ff |""")
    trill = r"A1:32\p\< ~ | A1:32 ~ | A1:32 ~ | A1:32\ff |"
    for players, note in (("fl1 fl3", "g'''"), ("fl2", "des'''"), ("ob1", "bes''"),
                          ("ob2", "fis''"), ("cl1", "g''"), ("cl2", "des''")):  # fmt: skip
        block.add(players, 3, trill.replace("A", note))

    # --- phrase 4: the peak. Two bars of the hammer, a glissando, one stroke, and silence.
    top = [
        ("es,", "bes,", "<es'' a'' es'''>", "<e'' bes'' e'''>"),
        ("es,", "e,", "<e'' bes'' e'''>", "<a'' es''' a'''>"),
    ]
    # The right hand comes from the low octaves, and it goes to the glissando: it starts
    # late in the first bar, and it has a rest at the end of the second bar.
    right, left = zip(
        *[
            _hammer_bar(
                *bar,
                r"\fff" if number == 0 else "",
                skip_high=2 if number == 0 else 0,
                tail=number == 0,
            )
            for number, bar in enumerate(top)
        ],
        strict=True,
    )
    block.add(
        "pno.rh", 4,
        " ".join(right) + r" c'1\glissando\< | <c''''' es'''' a''''>8-^\fff\sustainOn r4 r4. r4 |",
    )  # fmt: skip
    block.add(
        "pno.lh", 4,
        " ".join(left) + r" <es,, es,>1:32 | <es,, bes,, es,>8-^ r4 r4. r4 |",
    )  # fmt: skip
    for player, note in BUILD_CHORD.items():
        bars = accents(note, "-^", r"\fff") + " " + accents(note, "-^")
        bars += rf" {note}1\ff\< | {note}8-^\fff r4 r4. r4 |"
        block.add(player, 4, bars)
    for players, note in (
        ("fl1 fl2 fl3", "e'''"),
        ("ob1 cl1", "bes''"),
        ("ob2 cl2", "a''"),
        ("vn1", "<bes'' e'''>"),
        ("vn2", "<a' es''>"),
        ("va", "<e' bes'>"),
    ):
        bars = accents(note, "-^", r"\fff") + " " + accents(note, "-^")
        bars += rf" {note}1:32\ff\< | {note}8-^\fff r4 r4. r4 |"
        block.add(players, 4, bars)
    block.add("timp", 4, accents("es,", "->", r"\fff") + " " + accents("es,", "->")
              + r" es,1:32\ff\< | es,8->\fff r4 r4. r4 |")  # fmt: skip
    block.add("perc3", 4, accents("c'", "->", r"\fff") + " " + accents("c'", "->")
              + r" c'1:32\ff\< | c'8->\fff r4 r4. r4 |")  # fmt: skip
    block.add("perc1", 4, REST * 2 + r"c'1:32\f\< | "
              + r"c'8->\fff\lv r4 r4. r4 |")  # fmt: skip
    block.add("perc5", 4, _with(SNARE, r"\ff") + SNARE + r"c'1:32\ff\< | c'8->\fff r4 r4. r4 |")
    block.add(
        "perc6",
        4,
        accents("a", "->", r"\ff")
        + " "
        + accents("e'", "->")
        + r" a16\< a a a c' c' c' c' e' e' e' e' e' e' e' e' | e'8->\fff r4 r4. r4 |",
    )
    block.close()


def _last(text: str) -> str:
    """Return the last note of a run, with no duration."""
    return text.split()[-1].rstrip("0123456789")


def _first_marks(text: str, marks: str) -> str:
    """Return the music with marks after the first note value."""
    if not marks:
        return text
    for value in ("8-^", "16("):
        if value in text:
            return text.replace(value, value + marks, 1)
    return text


# ------------------------------------------------------------------ mark Z


def _wave(chord: str, top: str, bass: str, right_ends: bool = False) -> tuple[str, str]:
    """Return one bar of 4/4: a wave through a chord, up to the note `top` and down again.

    The left hand starts and ends the wave. The right hand has its middle. Before
    the wave, the left hand plays the bass note `bass` as a short octave. If
    `right_ends` is true, the right hand has the end of the wave also: the left
    hand is then free to go to the bass of the subsequent bar.
    """
    names = chord.split()
    for name in names:
        for marks in (",,", ",", "", "'"):
            up = run(chord, name + marks, 13).split()
            up[0] = up[0].rstrip("0123456789")
            if up[12] == top:
                down = run(chord, top, 12, down=True).split()
                down[0] = down[0].rstrip("0123456789")
                low = rf"\grace {{ <{bass}, {bass}>8 }} "
                left = (
                    low + rf"\tuplet 6/4 {{ {up[0]}16( {' '.join(up[1:6])}) }} r4 r4 "
                    rf"\tuplet 6/4 {{ {down[6]}16( {' '.join(down[7:12])}) }} |"
                )
                right = (
                    rf"r4 \tuplet 6/4 {{ {up[6]}16( {' '.join(up[7:12])} }} "
                    rf"\tuplet 6/4 {{ {down[0]}16 {' '.join(down[1:6])}) }} r4 |"
                )
                if right_ends:
                    left = low + rf"\tuplet 6/4 {{ {up[0]}16( {' '.join(up[1:6])}) }} r4 r2 |"
                    right = (
                        rf"r4 \tuplet 6/4 {{ {up[6]}16( {' '.join(up[7:12])} }} "
                        rf"\tuplet 6/4 {{ {down[0]}16 {' '.join(down[1:6])} }} "
                        rf"\tuplet 6/4 {{ {down[6]}16 {' '.join(down[7:12])}) }} |"
                    )
                return right, left
    raise ValueError(f"no wave of the chord {chord} goes up to {top}")


def _cadenza(work: Work) -> None:
    """Mark Z: the cadenza of the piano."""
    structure = work.structure

    # ---------------------------------- bars 1 to 4: octaves down the keyboard, and up
    s = work.section(4, *EIGHT)
    structure.mark(s.bar(1), "Z")
    structure.tempo(s.bar(1), 1, TOCCATA, "Cadenza. Feroce", unit="8")
    block = Block(s, REST * 4)
    down = run(PIVOT, "es''''", 32, down=True).split()
    down[0] = down[0].rstrip("0123456789")
    right, left = [], []
    for number in range(2):
        notes = down[16 * number : 16 * number + 16]
        low = [marked(f"<{octave(note, -1).strip()} {note}>", "->" if i == 0 else "")
               for i, note in enumerate(notes[1::2])]  # fmt: skip
        high = [marked(f"<{octave(note, -1).strip()} {note}>") for note in notes[0::2]]
        # The right hand starts: it has the notes on the eighth notes. The left hand
        # has a rest at the end of the second bar: it must go to the lowest E-flat.
        bar = hammer(high, low, tail=number == 0)
        left.append(bar[0])
        right.append(bar[1])
    # Two sweeps through the chords E-flat 7 and A 7. The first sweep fills its bar. The
    # second sweep starts after a rest (the hands go down again), and it arrives at the
    # high chord of the subsequent bar. The left hand stops earlier: it goes to the bass.
    sweep_one = run("es g bes des fis", "es", 16)
    sweep_two = run("a cis e g bes", "a'", 10)
    low_two = run("a cis e g bes", "a,", 6)
    block.add(
        "pno.rh", 1,
        _with(" ".join(right), r"\fff") + " " + _with(slurred(sweep_one), r"\<") + " | r4. "
        + slurred(sweep_two) + " |",
    )  # fmt: skip
    block.add(
        "pno.lh", 1,
        _with(" ".join(left), r"\fff\sustainOff") + " "
        + _with(slurred(octave(sweep_one, -2)), r"\sustainOn") + " | r4. "
        + _with(slurred(low_two), r"\sustainOff\sustainOn") + " r4 |",
    )  # fmt: skip
    block.close()

    # ------------------------------- bars 5 to 7: a memory of the night, in bare octaves
    s = work.section(3, 4, 4)
    structure.tempo(s.bar(1), 1, 54, "Recitativo: la notte ricordata")
    structure.change(s.bar(3), 1, "stringendo")
    block = Block(s, rests(4, 4, 3))
    block.add(
        "pno.rh", 1,
        r"<a''' cis'''' g''''>2\ff\> r2\! | d''2\p\espr( es''2 | \grace { bes''16 } as''2 g''2) |",
    )  # fmt: skip
    block.add(
        "pno.lh", 1,
        r"<a,, a,>2\ff\sustainOff\sustainOn r2 | d,2\p\sustainOff\sustainOn( es,2 | "
        r"\grace { bes,16 } as,2 g,4) \grace { ges16\sustainOff( g as a } bes4)\ppp |",
    )  # fmt: skip
    block.close()

    # ------------- bars 8 to 13: waves of two chords. Their highest notes go up by semitones.
    s = work.section(6, 4, 4)
    structure.tempo(s.bar(1), 1, 66, "Stringendo")
    structure.change(s.bar(1), 1, "accelerando")
    structure.arrive(s.bar(6), 4, 132)
    block = Block(s, rests(4, 4, 6))
    waves = [
        ("es g bes des", "g'''", "es,"),
        ("es as bes des", "as'''", "es,"),
        ("a cis e g", "a'''", "a,"),
        ("es g bes des", "bes'''", "es,"),
        ("b cis e g", "b'''", "a,"),
        ("a cis e g", "cis''''", "a,"),
    ]
    # In the last wave the right hand has the end: the left hand goes to the low D.
    right, left = zip(
        *[_wave(*wave, right_ends=number == len(waves) - 1) for number, wave in enumerate(waves)],
        strict=True,
    )
    levels = [r"\p\<", "", r"\mf\<", "", r"\f\<", r"\ff"]
    block.add("pno.rh", 1, " ".join(right))
    block.add(
        "pno.lh", 1,
        " ".join(
            low.replace("16(", "16" + level + r"\sustainOff\sustainOn(", 1)
            for low, level in zip(left, levels, strict=True)
        ),
    )  # fmt: skip
    block.close()

    # ---- bars 14 to 17: the motto in the bass, with a new last note: D, E-flat, A-flat, A
    s = work.section(4, *EIGHT)
    structure.tempo(s.bar(1), 1, 276, "Martellato, con tutta la forza", unit="8")
    block = Block(s, REST * 4)
    bars = [
        ("d,", "a,", "<g cis' es'>", "<a des' g'>"),
        ("es,", "bes,", "<a des' g'>", "<cis' g' a'>"),
        ("as,", "es", "<cis' g' a'>", "<es' a' cis''>"),
        ("a,", "e", "<es' a' cis''>", "<g' cis'' es''>"),
    ]
    right, left = zip(
        *[_hammer_bar(*bar, r"\fff" if number == 0 else "") for number, bar in enumerate(bars)],
        strict=True,
    )
    block.add("pno.rh", 1, " ".join(right))
    block.add("pno.lh", 1, _with(" ".join(left), r"\sustainOff"))
    block.close()


def _return(work: Work) -> None:
    """Mark Z, the last 7 bars: a trill, the return of the orchestra, the chord of 12 notes."""
    structure = work.structure
    s = work.section(7, 4, 4)
    structure.tempo(s.bar(1), 1, 60, "Largo")
    structure.change(s.bar(5), 1, "allargando")
    structure.arrive(s.bar(6), 4, 46)
    block = Block(s, rests(4, 4, 2), rests(4, 4, 4), r"R1\fermata |")

    # The trill on A with B-flat, in written notes. Below it, the orchestra comes back.
    trill = "a''32 bes'' a'' bes'' a'' bes'' a'' bes'' a'' bes'' a'' bes'' a'' bes'' a'' bes''"
    half = trill.replace("a''32", "a''32(", 1) + ")"
    block.add("pno.rh", 1, _with32(half, r"\ff\>") + " " + half + " | "
              + _with32(half, r"\p\<") + " " + half + " |")  # fmt: skip
    block.add("pno.lh", 1, r"<a,, a,>1\ff\sustainOn | R1 |")
    block.add("timp", 1, r"r2 es,2:32\pp\< ~ | es,1:32\mp |")
    block.add("vc", 1, r"r2 <es, bes,>2:32\pp\<\arco\sulpont ~ | <es, bes,>1:32\mp |")
    block.add("cb", 1, r"r2 es,2:32\pp\<\arco ~ | es,1:32\mp |")
    block.add("cbcl bn3", 1, r"R1 | es,,1\pp\< |")
    block.add("perc3", 1, r"R1 | c'1:32\ppp\< |")

    # The chord of all twelve notes: tritones and fifths, from E-flat. It grows for
    # three bars, and it stops on the fourth beat of the fourth bar.
    grow = r"A1\p\< ~ | A1\f\< ~ | A1\fff ~ | A2. r4 |"
    wall = {
        "tuba": "es,,", "cbcl": "es,,", "bn3": "es,,", "cb": "es,", "btbn": "a,,", "bn2": "e,",
        "tbn2": "e,", "bn1": "bes,", "tbn1": "bes,", "cl3": "bes,", "hn4": "g", "hn3": "des'",
        "hn2": "as'", "hn1": "d''", "tpt3": "g'", "tpt2": "des''", "tpt1": "as''",
        "cl1": "d''", "cl2": "b'", "ob2": "f''", "ob1": "b''", "fl2": "f'''", "fl1": "c''''",
        "fl3": "fis''''",
    }  # fmt: skip
    for player, note in wall.items():
        marks = r"\open" if player.startswith("hn") else ""
        block.add(player, 2, _first_note(grow.replace("A", note), marks))
    shake = r"A1:32\mp\< ~ | A1:32\f\< ~ | A1:32\fff ~ | A2.:32 r4 |"
    for player, note in (("vn1", "<f''' c''''>"), ("vn2", "<b'' f'''>"), ("va", "<as' d''>"),
                         ("vc", "<g des'>")):  # fmt: skip
        marks = r"\ord" if player == "vc" else ""
        block.add(player, 2, _first_note(shake.replace("A", note), marks))
    block.add("timp", 2, shake.replace("A", "es,"))
    block.add("perc3", 2, shake.replace("A", "c'"))
    block.add("perc1", 2, r"""R1 | \switch "suspended cymbals" c'1:32\p\< ~ | c'1:32\fff ~ | """
              r"c'2.:32 r4 |")  # fmt: skip
    block.add("perc5", 2, r"R1*2 | c'1:32\mf\< ~ | c'2.:32\fff r4 |")
    block.add("perc6", 2, r"""\switch "tam-tams" R1*2 | c'1\ff\lv | R1 |""")
    # The piano: the trill becomes a tremolo of two chords, one chord in each hand (the
    # chords A 7 and E-flat of the cadenza). The left hand plays on the sixteenth notes,
    # and the right hand plays between them: together they make thirty-second notes.
    # The first form of this passage had the two chords in each hand, with octaves that
    # leap in the left hand. The owner of the project found that a pianist cannot play
    # such music. The orchestra has the bass notes.
    low_chord, high_chord = "<a cis' g'>", "<bes' es'' g''>"

    def tremolo(strokes: int, marks: str) -> tuple[str, str]:
        """Return the two hands for a number of sixteenth notes: the right, then the left."""
        low = " ".join([f"{low_chord}16{marks}"] + [low_chord] * (strokes - 1))
        between = [f"{high_chord}16{marks}"] + [high_chord] * (strokes - 2)
        return "r32 " + " ".join(between) + f" {high_chord}32", low

    bars = [tremolo(16, r"\mf\<"), tremolo(16, ""), tremolo(16, r"\ff"), tremolo(12, "")]
    block.add("pno.rh", 2, " | ".join(right for right, _left in bars) + " r4 |")
    left_bars = [left for _right, left in bars]
    left_bars[0] = left_bars[0].replace(r"\mf\<", r"\mf\<\sustainOff", 1)
    block.add("pno.lh", 2, " | ".join(left_bars) + " r4 |")
    block.close()


def _with32(text: str, marks: str) -> str:
    """Return the music with marks on its first thirty-second note."""
    return text.replace("32", "32" + marks, 1)


def _first_note(text: str, marks: str) -> str:
    """Return the music with marks after its first whole note."""
    return text.replace("1", "1" + marks, 1) if marks else text
