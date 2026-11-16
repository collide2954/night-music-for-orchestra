"""The piano interlude: a small piano concerto before the turn (the marks W to Z).

The owner of the project asked for an interlude with the piano as its focus.
The first form of the interlude was slow and soft. The owner rejected it:
the interlude must be virtuosic, "almost like a small piano concerto", and
it must give the work energy and direction. The owner selected: a toccata
and a cadenza, and a loud peak before a sudden soft arrival of D major.

What the interlude does for the form of the work: the night music of part 3
has no pulse and no direction. The interlude changes this state into energy.
It starts in the night, it becomes a fast toccata, and its cadenza goes to
the edge of D major. Thus the turn of the work is the result of a fight, not
only a change of colour. The turn is near the golden section of the work.

Material:

- The cell of the toccata is A-flat, A, D, E-flat: two tritones a semitone
  apart. The dark form of the motto (D, E-flat, A-flat) is in this cell, and
  the same form on A-flat (A-flat, A, D). The four forms of the cell on
  A-flat, B, D, and F are in one scale: the scale of the chase of part 2.
- The awakening (mark W, bars 1 to 6): the note A-flat of the night cluster
  comes again and again, faster and faster, until it is a hammer.
- The hammer theme (mark W, from bar 7): the hands alternate in sixteenth
  notes, with accents in the Bulgarian rhythm 3 + 3 + 2. The highest notes
  go D, E-flat, A-flat, and then up to A: the motto, and the step that the
  turn makes later. The bass has the motto in long steps.
- The theme in the forge (mark X): the warm theme with the dark form of the
  motto (D, E-flat, A-flat, G; B-flat, A-flat, G-flat, E-flat), in hammered
  octaves. After the turn, the cellos have the same notes in their light
  form. The piano and the orchestra change roles: one has the theme, the
  other decorates it.

The orchestra is a partner, not a background: it answers, it takes the
themes, and it trades fast figures with the piano.
"""

from __future__ import annotations

from collections.abc import Sequence

from ..compose.tools import Block, double, octave, rests, run, tr
from ..notation.work import Work

# The scale of the chase (semitone, whole tone), with the note names of the dark half.
OCT = "as a b c d es f ges"
TOCCATA = 264  # eighth notes in one minute
EIGHT = (8, 8, (3, 3, 2))  # the metre of the toccata: 3 + 3 + 2 eighth notes
REST = "R1 | "  # one bar of 8/8
# The snare drum: sixteenth notes with accents on the beat groups 3 + 3 + 2.
SNARE = "c'16 c' c' c' c' c' c'-> c' c' c' c' c' c'-> c' c' c' | "

# A note for one sixteenth of a bar: its pitch (or chord) and its marks. None is a rest.
Token = tuple[str, str] | None


def sixteenths(tokens: Sequence[Token], grouping: tuple[int, ...] = (6, 6, 4)) -> str:
    """Return one bar of sixteenth notes. Adjacent rests in one beat group become one rest."""
    if sum(grouping) != len(tokens):
        raise ValueError(f"{len(tokens)} sixteenth notes for the grouping {grouping}")
    parts: list[str] = []
    position = 0
    for size in grouping:
        group = tokens[position : position + size]
        index = 0
        while index < size:
            token = group[index]
            if token is not None:
                parts.append(f"{token[0]}16{token[1]}")
                index += 1
                continue
            count = 1
            while index + count < size and group[index + count] is None:
                count += 1
            # A rest that starts between two eighth notes goes to the subsequent eighth note.
            if index % 2 == 1:
                parts.append("r16")
                index, count = index + 1, count - 1
            for length, text in ((6, "r4."), (4, "r4"), (2, "r8"), (1, "r16")):
                while count >= length:
                    parts.append(text)
                    index, count = index + length, count - length
        position += size
    return " ".join(parts) + " |"


def hammer(
    low: Sequence[Token], high: Sequence[Token], grouping: tuple[int, ...] = (6, 6, 4)
) -> tuple[str, str]:
    """Return one bar in which the hands alternate: the right hand, then the left hand.

    The left hand plays `low` on the eighth notes. The right hand plays
    `high` one sixteenth note later. Each note is written as an eighth note,
    as in the toccatas of the repertoire: thus each hand has beams, and no
    rests between its notes. The notes are short (martellato).
    """
    if len(low) != len(high) or 2 * len(low) != sum(grouping):
        raise ValueError("the two hands must have one note for each eighth note of the bar")
    left = " ".join(f"{pitch}8{marks}" for pitch, marks in low)
    right = "r16 " + " ".join(f"{pitch}8{marks}" for pitch, marks in high[:-1])
    right += f" {high[-1][0]}16{high[-1][1]}"
    return right + " |", left + " |"


def marked(note: str, marks: str = "") -> Token:
    return (note, marks)


def accents(note: str, marks: str = "->", first: str = "") -> str:
    """Return one bar of 8/8 with a short note on the first eighth of each beat group."""
    return f"{note}8{marks}{first} r4 {note}8{marks} r4 {note}8{marks} r8 |"


def slurred(notes: str) -> str:
    """Return a run of notes with a slur from its first note to its last note."""
    items = notes.split()
    return f"{items[0]}( {' '.join(items[1:])})"


def write(work: Work) -> None:
    """Write the interlude: the marks W and X here, the marks Y and Z in `cadenza.py`."""
    from . import cadenza  # the module needs the tools of this module

    _awakening(work)
    _hammer_theme(work)
    _forge(work)
    cadenza.write(work)


# ------------------------------------------------------------------ mark W


def _awakening(work: Work) -> None:
    """Mark W, bars 1 to 6: one note of the night becomes a hammer."""
    structure = work.structure
    s = work.section(6, 4, 4)
    structure.mark(s.bar(1), "W")
    structure.tempo(s.bar(1), 1, 60, "Risvegliando")
    structure.change(s.bar(3), 1, "accelerando molto")
    structure.arrive(s.bar(6), 4, 126)
    block = Block(s, rests(4, 4, 6))
    four = (4, 4, 4, 4)

    # The note A-flat, slower than a pulse, then faster and faster (a written
    # acceleration). Then the hands alternate, and the cluster of the night opens:
    # first its semitones, then the notes D and E-flat of the cell.
    def bar(low: list[str], high: str, level: str, strong: str = "") -> tuple[str, str]:
        bottom = [marked(note, "->" if note == strong else "") for note in low]
        bottom[0] = (bottom[0][0], bottom[0][1] + level)
        top = [marked(high)] * 8
        top[0] = (high, level)
        return hammer(bottom, top, four)

    low_a, low_b, low_c = "<as,, as,>", "<a,, a,>", "<d, d>"
    bars = [
        bar(["as"] * 8, "<g a>", r"\mp"),
        bar(["<ges as>"] * 8, "<a bes>", r"\mf\<"),
        bar(
            [low_a, "<ges as>", "<ges as>", low_a, "<ges as>", "<ges as>", low_a, "<ges as>"],
            "<a bes d'>",
            r"\f",
            low_a,
        ),
    ]
    last_low = [low_a, "<as d'>", "<as d'>", low_b, "<as d'>", "<as d'>", low_c, "<as d'>"]
    last_high = ["<a d' es'>"] * 3 + ["<d' es' as'>"] * 3 + ["<es' as' a'>"] * 2
    last = hammer(
        [
            marked(note, "->" + (r"\ff\<" if i == 0 else "") if "," in note else "")
            for i, note in enumerate(last_low)
        ],
        [marked(note, r"\ff\<" if i == 0 else "") for i, note in enumerate(last_high)],
        four,
    )
    block.add(
        "pno.lh",
        1,
        r"as2\pp--\senzaped as4-- as4-- | "
        r"as8\<-- as-- as-- as-- \tuplet 3/2 { as8 as as } \tuplet 3/2 { as8 as as } | "
        + " ".join(left for _right, left in bars)
        + " "
        + last[1],
    )
    block.add("pno.rh", 1, "R1*2 | " + " ".join(right for right, _left in bars) + " " + last[0])

    # The last chord of the strings (mark V) continues and goes to nothing.
    block.add("vn2", 1, r"ges'1\> ~ | ges'2 r2\! | R1*4 |")
    block.add("va", 1, r"<bes es'>1\> ~ | <bes es'>2 r2\! | R1*4 |")
    block.add(
        "cb",
        1,
        r"es,1\> ~ | es,2 r2\! | R1*2 | as,,4->\mf\pizz\senzasord r4 as,,4-> r4 | "
        r"as,,4->\f r8 a,,4-> r8 d,4-> |",
    )
    block.add(
        "vc",
        1,
        r"R1*4 | as,4->\mf\pizz\tutti\senzasord r4 as,4-> r4 | "
        r"as,4->\f r8 a,4-> r8 d4-> |",
    )

    # The percussion and the low brass grow with the piano.
    block.add("perc1", 1, r"c'1\pp\lv | R1*5 |")
    block.add("timp", 1, r"R1*2 | as,1:32\ppp\< ~ | as,1:32 ~ | as,1:32\p\< ~ | as,1:32\mf |")
    block.add("perc3", 1, r"""\switch "bass drum" R1*4 | c'1:32\pp\< ~ | c'1:32\mp |""")
    block.add("perc6", 1, r"""\switch "tom-toms" R1*5 | r2 a16\mp\< a c' c' e' e' e' e'\f |""")
    block.add("perc5", 1, r"""\switch "snare drum" R1*6 |""")
    block.add("perc2", 1, r"""\switch "xylophone" R1*6 |""")
    stopped = r"R1*4 | A1\p\<\stopped ~ | A1\ff |"
    for player, note in (("hn1", "es'"), ("hn2", "d'"), ("hn3", "a"), ("hn4", "as")):
        block.add(player, 1, stopped.replace("A", note))
    for player, note in (("tbn1", "a"), ("tbn2", "d"), ("btbn", "as,"), ("tuba", "as,,")):
        block.add(player, 1, rf"R1*5 | {note}1\mp\< |")
    # The woodwinds run up to the first chord of the toccata.
    rush = "r2 r4 " + slurred(run(OCT, "d''", 8, 32)) + " |"
    block.add("fl1 fl2 cl2", 1, "R1*5 | " + rush.replace("d''32(", r"d''32\f\<("))
    block.add(
        "fl3", 1, r"""\switch "piccolo" R1*5 | """ + octave(rush, 1).replace("32(", r"32\f\<(")
    )
    block.start("fl2", r'\switch "flute"')
    block.add("cl1", 1, r"""\switch "clarinet in B-flat" R1*6 |""")
    block.add("ob2", 1, r"""\switch "oboe" R1*6 |""")
    block.add("bn2", 1, r"""\switch "bassoon" R1*6 |""")
    block.close()


# The hammer theme. For each bar: the bass note of the accents, the note that the left
# hand plays between the accents, and the two chords of the right hand. In each beat
# group the right hand plays the first chord, and the second chord on its last note.
HAMMER_BARS = [
    # Phrase 1: the cell on A-flat. The highest notes go D, E-flat, A-flat, A.
    ("d,", "as,", "<as d'>", "<a es'>"),
    ("es,", "a,", "<a es'>", "<d' as'>"),
    ("as,", "d", "<d' as'>", "<es' a'>"),
    # Phrase 2: a minor third higher (the cell on B). The highest notes go F, G-flat, B, C.
    ("f,", "b,", "<b f'>", "<c' ges'>"),
    ("ges,", "c", "<c' ges'>", "<f' b'>"),
    ("b,", "f", "<f' b'>", "<ges' c''>"),
]


def _hammer_bar(bass: str, fill: str, first: str, second: str, level: str) -> tuple[str, str]:
    """Return one bar of the hammer theme: the right hand and the left hand."""
    low_octave = f"<{bass}, {bass}>"
    low = [
        marked(low_octave, "->" + level),
        marked(fill),
        marked(fill),
        marked(low_octave, "->"),
        marked(fill),
        marked(fill),
        marked(low_octave, "->"),
        marked(fill),
    ]
    high = [
        marked(first, level),
        marked(first),
        marked(second, "->"),
        marked(first),
        marked(first),
        marked(second, "->"),
        marked(first),
        marked(second, "->"),
    ]
    return hammer(low, high)


def _hammer_theme(work: Work) -> None:
    """Mark W, bars 7 to 22: the hammer theme, and the answer of the full orchestra."""
    structure = work.structure
    s = work.section(16, *EIGHT)
    structure.tempo(s.bar(1), 1, TOCCATA, "Allegro barbaro, martellato", unit="8")
    four = REST * 4
    block = Block(s, four, four, four, four)

    # ------------------------------------------------------- phrase 1: the piano alone
    right, left = zip(
        *[
            _hammer_bar(*bar, r"\f" if number == 0 else "")
            for number, bar in enumerate(HAMMER_BARS[:3])
        ],
        strict=True,
    )
    down = run(OCT, "a''", 16, down=True)
    block.add(
        "pno.rh", 1, " ".join(right) + " " + slurred(down).replace("a''16(", r"a''16\<(") + " |"
    )
    block.add("pno.lh", 1, " ".join(left) + " " + slurred(octave(down, -2)) + " |")
    # The first chord: all four notes of the cell, in the full orchestra.
    chord = {
        "tuba": "d,,",
        "btbn": "d,",
        "tbn2": "as,",
        "tbn1": "d",
        "hn4": "as",
        "hn3": "a",
        "hn2": "d'",
        "hn1": "es'",
        "tpt3": "a'",
        "tpt2": "d''",
        "tpt1": "es''",
        "bn3": "d,",
        "bn2": "as,",
        "bn1": "d",
        "cl3": "as",
        "cl1": "d'",
        "cl2": "as'",
        "ob2": "a'",
        "ob1": "es''",
        "fl2": "a''",
        "fl1": "d'''",
        "fl3": "es''''",
        "vn1": "<d'' a''>",
        "vn2": "<es' as'>",
        "va": "<d a>",
    }
    for player, note in chord.items():
        marks = r"\senzasord\ord" if player in ("vn1", "vn2", "va") else ""
        marks += r"\open" if player.startswith("hn") else ""
        block.add(player, 1, rf"{note}8-^\ff{marks} r4 r4. r4 | " + REST * 3)
    block.add("perc1", 1, r"""\switch "crash cymbals" c'8\ff\lv r4 r4. r4 | """ + REST * 3)
    block.add("perc3", 1, r"c'8->\ff r4 r4. r4 | " + REST * 3)
    # The low strings and the timpani have the bass of the accents: the motto in long steps.
    bass = " ".join(
        accents(note, "->", r"\f" if number == 0 else "")
        for number, note in enumerate(["d,", "es,", "as,"])
    )
    block.add("timp", 1, bass + " " + REST)
    block.add("vc", 1, bass + " " + REST)
    block.add("cb", 1, bass + " " + REST)
    block.add(
        "perc2",
        1,
        " ".join(
            accents(note, "->", r"\f" if number == 0 else "")
            for number, note in enumerate(["d''", "es''", "as''"])
        )
        + " r4. r4. a''8-> r8 |",
    )
    block.add(
        "perc4",
        1,
        accents("c'", "", r"\mf")
        + " "
        + accents("d'", "")
        + " "
        + accents("c'", "")
        + " c'16 c' d' d' c' c' d' d' c' c' d' d' c' d' c' d' |",
    )

    # --------------------------- phrase 2: a minor third higher, with the woodwinds
    right, left = zip(
        *[
            _hammer_bar(*bar, r"\ff" if number == 0 else "")
            for number, bar in enumerate(HAMMER_BARS[3:])
        ],
        strict=True,
    )
    up = run(OCT, "c'", 16)
    block.add(
        "pno.rh",
        2,
        " ".join(right) + " " + slurred(octave(up, 1)).replace("16(", r"16\<(", 1) + " |",
    )
    block.add("pno.lh", 2, " ".join(left) + " " + slurred(octave(up, -1)) + " |")
    low_notes = ["f,", "ges,", "b,"]
    bass = " ".join(
        accents(note, "->", r"\f" if number == 0 else "") for number, note in enumerate(low_notes)
    )
    block.add("vc cb bn3 cbcl", 2, bass + " " + REST)
    block.add("timp", 2, accents("f,", "->", r"\f") + " " + REST * 3)
    block.add(
        "perc6",
        2,
        REST
        + " "
        + accents("a", "->", r"\f")
        + " "
        + accents("c'", "->")
        + " a16\\< a a a c' c' c' c' e' e' e' e' e'\\ff e' e' e' |",
    )
    # The woodwinds have the chords of the right hand on the accents.
    for players, notes in (
        ("ob1 cl1", ["b'", "c''", "f''"]),
        ("ob2 cl2", ["f'", "ges'", "b'"]),
        ("bn1 bn2", ["b", "c'", "f'"]),
    ):
        line = " ".join(
            accents(note, "-.", r"\f" if number == 0 else "") for number, note in enumerate(notes)
        )
        block.add(players, 2, line + " " + REST)
    # The strings hit the strings with the wood of the bow, in the rhythm 3 + 3 + 2.
    block.add(
        "vn2",
        2,
        accents("<f' b'>", "-.", r"\mf\collegno")
        + " "
        + accents("<ges' c''>", "-.")
        + " "
        + accents("<b' f''>", "-.")
        + " "
        + REST,
    )
    block.add(
        "va",
        2,
        accents("<b f'>", "-.", r"\mf\collegno")
        + " "
        + accents("<c' ges'>", "-.")
        + " "
        + accents("<f' b'>", "-.")
        + " "
        + REST,
    )
    block.add(
        "perc2",
        2,
        " ".join(
            accents(note, "->", r"\f" if number == 0 else "")
            for number, note in enumerate(["f''", "ges''", "b''"])
        )
        + " "
        + slurred(octave(up, 2)).replace("16(", r"16\ff(", 1)
        + " |",
    )
    block.add(
        "perc4",
        2,
        accents("c'", "", r"\mf") + " " + accents("d'", "") + " " + accents("c'", "") + " " + REST,
    )
    block.add(
        "fl1 fl2 fl3:1",
        2,
        REST * 3 + r"r4. r4. " + slurred(run(OCT, "es'''", 4)).replace("16(", r"16\ff(", 1) + " |",
    )

    # ---------------- phrase 3: the full orchestra has the accents, the piano answers
    # The orchestra plays the chords of the cell on the accents. Between the accents
    # the piano runs up: a confrontation of equal partners.
    steps = [
        ("as,", "<as d' es'>", "as'"),
        ("a,", "<a d' es'>", "a'"),
        ("d", "<d' es' as'>", "d''"),
    ]
    piano_right, piano_left = [], []
    for number, (bass_note, chord_text, start) in enumerate(steps):
        level = r"\ff" if number == 0 else ""
        first = slurred(run(OCT, start, 4))
        second = slurred(run(OCT, _up(start, 4), 4))
        third = slurred(run(OCT, _up(start, 8), 2))
        high_chord = octave(chord_text, 1)
        piano_right.append(
            f"{high_chord}8->{level} {octave(first, 1)} {high_chord}8-> {octave(second, 1)} "
            f"{high_chord}8-> {octave(third, 1)} |"
        )
        low_chord = f"<{bass_note}, {bass_note}>"
        piano_left.append(
            f"{low_chord}8->{level} {octave(first, -1)} {low_chord}8-> {octave(second, -1)} "
            f"{low_chord}8-> {octave(third, -1)} |"
        )
    # Bar 4 of the phrase: the piano alone, octaves in the two hands, down through the scale.
    fall = run(OCT, "es''''", 8, 8, down=True)
    block.add(
        "pno.rh",
        3,
        " ".join(piano_right) + " " + double(fall, -1).replace("8", r"8->\fff", 1) + " |",
    )
    block.add(
        "pno.lh",
        3,
        " ".join(piano_left) + " " + double(octave(fall, -2), -1).replace("8", "8->", 1) + " |",
    )
    tutti = {
        "tuba": ["as,,", "a,,", "d,"],
        "btbn": ["as,", "a,", "d"],
        "bn3": ["as,,", "a,,", "d,"],
        "cbcl": ["as,,", "a,,", "d,"],
        "cb": ["as,,", "a,,", "d,"],
        "vc": ["as,", "a,", "d"],
        "tbn2": ["d", "d", "as"],
        "tbn1": ["as", "a", "d'"],
        "hn4": ["d'", "d'", "es'"],
        "hn3": ["es'", "es'", "as'"],
        "hn2": ["as'", "a'", "d''"],
        "hn1": ["as'", "a'", "d''"],
        "tpt3": ["d''", "d''", "es''"],
        "tpt2": ["es''", "es''", "as''"],
        "tpt1": ["as''", "a''", "as''"],
        "bn1": ["d", "d", "as"],
        "bn2": ["as,", "a,", "d"],
        "cl3": ["as", "a", "d'"],
        "cl1": ["d''", "d''", "es''"],
        "cl2": ["es''", "es''", "as''"],
        "ob2": ["d''", "d''", "es''"],
        "ob1": ["as''", "a''", "d'''"],
        "fl2": ["es'''", "es'''", "as'''"],
        "fl1": ["as'''", "a'''", "as'''"],
        "fl3": ["as'''", "a'''", "d''''"],
        "va": ["<d' as'>", "<d' a'>", "<es' as'>"],
        "vn2": ["<es'' as''>", "<es'' a''>", "<as'' d'''>"],
        "vn1": ["<d''' as'''>", "<d''' a'''>", "<es''' as'''>"],
    }
    for player, notes in tutti.items():
        arco = r"\arco\ord" if player in ("vc", "cb", "va", "vn2") else ""
        line = " ".join(
            accents(note, "-^", (r"\ff" + arco) if number == 0 else "")
            for number, note in enumerate(notes)
        )
        block.add(player, 3, line + " " + REST)
    block.add(
        "timp",
        3,
        " ".join(
            accents(note, "->", r"\ff" if number == 0 else "")
            for number, note in enumerate(["as,", "d,", "d,"])
        )
        + " "
        + REST,
    )
    block.add(
        "perc3",
        3,
        accents("c'", "->", r"\ff")
        + " "
        + accents("c'", "->")
        + " "
        + accents("c'", "->")
        + " "
        + REST,
    )
    block.add("perc5", 3, SNARE.replace("16", r"16->\f", 1) + SNARE * 2 + REST)
    block.add("perc1", 3, REST * 2 + r"c'8\ff\lv r4 r4. r4 | " + REST)

    # ----------------------- phrase 4: the way to the theme, above the bass note E-flat
    forge = [
        ("es,", "bes,", "<bes es'>", "<a d'>"),
        ("es,", "bes,", "<bes es'>", "<d' as'>"),
    ]
    right, left = zip(
        *[_hammer_bar(*bar, r"\mf\<" if number == 0 else "") for number, bar in enumerate(forge)],
        strict=True,
    )
    zigzag = [
        "es'",
        "ges'",
        "f'",
        "as'",
        "ges'",
        "a'",
        "as'",
        "b'",
        "a'",
        "c''",
        "b'",
        "d''",
        "c''",
        "es''",
        "d''",
        "f''",
    ]
    line = " ".join(zigzag).replace("es'", "es'16", 1)
    higher = "es'' ges'' f'' as'' ges'' a'' as'' b'' a'' c''' b'' d''' c''' es''' d''' es'''"
    line2 = higher.replace("es''", "es''16", 1)
    block.add(
        "pno.rh",
        4,
        " ".join(right)
        + " "
        + slurred(line).replace("16(", r"16\f\<(", 1)
        + " | "
        + slurred(line2)
        + " |",
    )
    block.add(
        "pno.lh",
        4,
        " ".join(left)
        + " "
        + slurred(octave(line, -2))
        + " | "
        + slurred(octave(line2, -2))
        + " |",
    )
    # The strings start the motor of the subsequent section. The horns hold E-flat minor.
    motor = "es'16 es' bes es' es' bes es' es' bes es' es' bes es' es' bes es' |"
    block.add(
        "va",
        4,
        REST * 2
        + motor.replace("es'16", r"es'16\p\<\spicc", 1)
        + " "
        + motor.replace("es'16", r"es'16\mf", 1),
    )
    block.add(
        "vn2",
        4,
        REST * 2
        + octave(motor, 1).replace("es''16", r"es''16\p\<\arco\spicc", 1)
        + " "
        + octave(motor, 1).replace("es''16", r"es''16\mf", 1),
    )
    for player, note in (("hn1", "ges'"), ("hn2", "es'"), ("hn3", "bes"), ("hn4", "es")):
        block.add(player, 4, rf"{note}1\p\< ~ | {note}1 ~ | {note}1 ~ | {note}1\f |")
    block.add(
        "vc cb",
        4,
        " ".join(accents("es,", "->", (r"\mf\pizz" if number == 0 else "")) for number in range(4)),
    )
    block.add(
        "timp",
        4,
        accents("es,", "->", r"\mp\<")
        + " "
        + accents("es,")
        + " "
        + accents("es,")
        + " es,8->\\f es, es, es,-> es, es, es,-> es, |",
    )
    block.add(
        "perc5",
        4,
        accents("c'", "", r"\p\<")
        + " "
        + accents("c'", "")
        + " "
        + SNARE.replace("16", r"16\mf", 1)
        + SNARE,
    )
    block.close()


def _up(note: str, steps: int) -> str:
    """Return the note that is a number of steps of the toccata scale above a note."""
    return run(OCT, note, steps + 1).split()[-1].rstrip("0123456789")


# ------------------------------------------------------------------ mark X

# The warm theme with the dark form of the motto, in the rhythm 3 + 3 + 2 (4 bars).
FORGE_THEME = r"d''4.-> es''4.-> as''4-> | g''2.-> r4 | bes''4.-> as''4.-> ges''4-> | es''2.-> r4 |"


def _forge(work: Work) -> None:
    """Mark X: the warm theme with the dark form of the motto, in hammered octaves."""
    structure = work.structure
    s = work.section(16, *EIGHT)
    structure.mark(s.bar(1), "X")
    four = REST * 4
    block = Block(s, four, four, four, four)

    # --------------------------------------------- phrase 1: the piano has the theme
    block.add("pno.rh", 1, double(FORGE_THEME, 1).replace("4.->", r"4.->\ff", 1))
    # The left hand: a motor of sixteenth notes on the chord of E-flat minor. In bar 2
    # the theme has the note G above the G-flat of the left hand (major and minor together).
    motors = [
        "es, bes, es a es bes, es, bes, es a es bes, es, bes, es a",
        "es, bes, es ges es bes, es, bes, es ges es bes, es, bes, es ges",
        "es, bes, es bes es bes, es, bes, es as es bes, es, bes, es ges",
        "es, bes, es ges es bes, es, bes, es ges es bes, es, ges, bes, es",
    ]
    block.add(
        "pno.lh",
        1,
        " ".join(
            slurred(motor.replace("es,", r"es,16" + (r"\f" if number == 0 else ""), 1)) + " |"
            for number, motor in enumerate(motors)
        ),
    )
    string_motor = "es'16 es' bes es' es' bes es' es' bes es' es' bes es' es' bes es' |"
    block.add("va", 1, (string_motor * 4).replace("es'16", r"es'16\mp", 1))
    block.add("vn2", 1, (octave(string_motor, 1) * 4).replace("es''16", r"es''16\mp", 1))
    for player, note in (("hn1", "ges'"), ("hn2", "es'"), ("hn3", "bes"), ("hn4", "es")):
        block.add(player, 1, rf"{note}1\mp\> ~ | {note}1\p\< ~ | {note}1\mp\> ~ | {note}1\p |")
    block.add(
        "vc cb",
        1,
        " ".join(accents("es,", "->", (r"\f" if number == 0 else "")) for number in range(4)),
    )
    block.add(
        "timp",
        1,
        " ".join(accents("es,", "->", (r"\f" if number == 0 else "")) for number in range(4)),
    )
    # The woodwinds and the xylophone answer where the theme has a rest (a trade).
    call_one = "r4. r4. " + slurred(run(OCT, "as''", 4)).replace("16(", r"16\f(", 1) + " |"
    call_two = (
        "r4. r4. " + slurred(run(OCT, "es'''", 4, down=True)).replace("16(", r"16\f(", 1) + " |"
    )
    block.add("fl1 fl2 ob1:-1 cl1:-1", 1, REST + call_one + REST + call_two)
    block.add("perc2", 1, REST + call_one + REST + call_two)
    block.add("perc5", 1, SNARE.replace("16", r"16\p", 1) + SNARE * 3)

    # ------------------- phrase 2: the orchestra has the theme, the piano decorates it
    # The theme is a minor third higher (F, G-flat, B, B-flat; D-flat, B, A, G-flat).
    theme_two = r"f'4.-> ges'4.-> b'4-> | bes'2.-> r4 | des''4.-> b'4.-> a'4-> | ges'2.-> r4 |"
    block.add("hn1 hn2 hn3 hn4", 2, theme_two.replace("4.->", r"4.->\f", 1))
    block.add("va vc", 2, theme_two.replace("4.->", r"4.->\ff\arco\ord", 1))
    block.add("tpt1 tpt2", 2, theme_two.replace("4.->", r"4.->\mf", 1))
    block.add("tbn1 tbn2", 2, octave(theme_two, -1).replace("4.->", r"4.->\mf", 1))
    # The piano: fast figures in the two hands, two octaves apart, above the theme.
    figures = [
        run(OCT, "f''", 8) + " " + run(OCT, "f'''", 8, down=True),
        run(OCT, "ges''", 6) + " " + run(OCT, "es'''", 6, down=True) + " " + run(OCT, "ges''", 4),
        run(OCT, "as''", 8) + " " + run(OCT, "as'''", 8, down=True),
        run(OCT, "ges''", 4) + " " + run(OCT, "c'''", 4) + " " + run(OCT, "ges'''", 8, down=True),
    ]
    lines = [
        " ".join(
            part.rstrip("0123456789") if index else part
            for index, part in enumerate(figure.split())
        )
        for figure in figures
    ]
    block.add(
        "pno.rh",
        2,
        " ".join(
            slurred(line).replace("16(", r"16\ff(" if number == 0 else "16(", 1) + " |"
            for number, line in enumerate(lines)
        ),
    )
    block.add("pno.lh", 2, " ".join(slurred(octave(line, -2)) + " |" for line in lines))
    block.add(
        "cb bn3 cbcl tuba",
        2,
        " ".join(accents("ges,", "->", (r"\f" if number == 0 else "")) for number in range(4)),
    )
    block.add(
        "perc6",
        2,
        " ".join(
            accents(note, "->", (r"\f" if number == 0 else ""))
            for number, note in enumerate(["a", "c'", "a", "e'"])
        ),
    )
    block.add("perc5", 2, SNARE * 4)
    block.add(
        "vn1 vn2",
        2,
        (
            octave(
                "ges'16 ges' des' ges' ges' des' ges' ges' des' ges' ges' des' "
                "ges' ges' des' ges' |",
                1,
            )
            * 4
        ).replace("16", r"16\mp\spicc", 1),
    )

    # ---------- phrase 3: the last notes of the theme, one after the other, higher and higher
    # The piano and the brass take the three notes that go down (from D-flat, E, G, and
    # B-flat: a minor third higher each time). While the brass plays, the piano hammers
    # the note at which its own line arrived, in broken octaves.
    def tail(first: str, second: str, third: str) -> str:
        return f"{first}4.-> {second}4.-> {third}4-> |"

    def broken(note: str) -> str:
        high = octave(note, 1).strip()
        return " ".join([f"{note}16", high] + [note, high] * 7) + " |"

    piano_one, piano_two = tail("des'''", "b''", "a''"), tail("g'''", "f'''", "es'''")
    block.add(
        "pno.rh", 3,
        double(piano_one, 1).replace("4.->", r"4.->\ff", 1) + " " + broken("ges''") + " "
        + double(piano_two, 1) + " " + broken("c'''"),
    )  # fmt: skip
    block.add(
        "pno.lh", 3,
        double(octave(piano_one, -2), -1).replace("4.->", r"4.->\ff", 1) + " " + broken("ges,")
        + " " + double(octave(piano_two, -2), -1) + " " + broken("c"),
    )  # fmt: skip
    brass_one, brass_two = tail("e''", "d''", "c''"), tail("bes''", "as''", "ges''")
    block.add(
        "tpt1 tpt2", 3, REST + brass_one.replace("4.->", r"4.->\ff", 1) + " " + REST + brass_two
    )
    block.add(
        "hn1 hn2 hn3 hn4 tbn1:-1 tbn2:-1", 3,
        REST + octave(brass_one, -1).replace("4.->", r"4.->\ff", 1) + " " + REST
        + octave(brass_two, -1),
    )  # fmt: skip
    motor = "ges'16 ges' des' ges' ges' des' ges' ges' des' ges' ges' des' ges' ges' des' ges' |"
    block.add(
        "vn1 vn2",
        3,
        (octave(motor, 1) * 2 + octave(tr(motor, 3), 1) * 2).replace("16", r"16\mf", 1),
    )
    block.add("va", 3, (motor * 2 + tr(motor, 3) * 2).replace("16", r"16\mf\spicc", 1))
    low_line = " ".join(
        accents(note, "->", r"\f" if number == 0 else "")
        for number, note in enumerate(["ges,", "g,", "as,", "a,"])
    )
    block.add("cb bn3 cbcl tuba", 3, low_line)
    block.add("vc", 3, low_line.replace("8->", r"8->\pizz", 1))
    block.add("perc5", 3, SNARE.replace("16", r"16\mf\<", 1) + SNARE * 3)
    block.add("perc6", 3, " ".join(accents(note, "->") for note in ["c'", "e'", "c'", "e'"]))

    # ----- phrase 4: the hammer again, with the full orchestra in octaves; then a sudden stop
    bars = [
        ("a,", "es", "<es' a'>", "<e' bes'>"),
        ("bes,", "e", "<e' bes'>", "<a' es''>"),
        ("b,", "f", "<f' b'>", "<ges' c''>"),
    ]
    right, left = zip(
        *[_hammer_bar(*bar, r"\ff\<" if number == 0 else "") for number, bar in enumerate(bars)],
        strict=True,
    )
    rush = run(OCT, "c'", 12)
    block.add(
        "pno.rh",
        4,
        " ".join(right) + " " + slurred(octave(rush, 1)).replace("16(", r"16\fff(", 1) + " r4 |",
    )
    block.add("pno.lh", 4, " ".join(left) + " " + slurred(octave(rush, -1)) + " r4 |")
    octaves = {
        "tuba": -2, "btbn": -1, "bn3": -2, "cbcl": -2, "cb": -1, "vc": -1, "tbn2": -1, "tbn1": 0,
        "bn1": -1, "bn2": -1, "hn4": 0, "hn3": 0, "hn2": 1, "hn1": 1, "tpt3": 1, "tpt2": 1,
        "tpt1": 2, "cl3": 0, "cl1": 1, "cl2": 2, "ob2": 1, "ob1": 2, "fl2": 2, "fl1": 3,
        "va": 0, "vn2": 1, "vn1": 2,
    }  # fmt: skip
    unison = " ".join(
        accents(note, "-^", r"\ff\<" if number == 0 else "")
        for number, note in enumerate(["a", "bes", "b"])
    )
    for player, shift in octaves.items():
        marks = r"\arco\ord" if player in ("va", "vc", "vn1", "vn2") else ""
        line = octave(unison, shift) if shift else unison
        block.add(player, 4, line.replace("8-^", "8-^" + marks, 1) + " " + REST)
    block.add("timp", 4, REST * 3 + r"es,2.:32\f\< es,8->\fff r8 |")
    block.add(
        "perc3",
        4,
        " ".join(accents("c'", "->", r"\ff" if n == 0 else "") for n in range(3)) + " " + REST,
    )
    block.add("perc5", 4, SNARE.replace("16", r"16\f\<", 1) + SNARE * 2 + r"c'2.:32 c'8->\fff r8 |")
    block.close()
