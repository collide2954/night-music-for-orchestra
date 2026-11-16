"""Part 5: first light, the themes together, the calls, and the last statement.

Material of this part:

- First light: the notes of the harmonic series on D come in one after the
  other, from the lowest. Partial 11 is between G and G-sharp. Thus the
  note that was A-flat in the dark and G-sharp in the shimmer is now a part
  of the sound of D.
- The warm theme and the song theme at the same time, in D major. The
  walking theme and the chase theme go with them.
- The rhythm of the heavy section of part 2, now in D major. The riff, the
  calls of the brass, and the peal of the bells have the motto in its
  light form (D, E, A).
- The chorale of part 1 in D major, fff, and the last chord.

Style profile: "Theatre", then "Transfigured" after the turn.
"""

from __future__ import annotations

from ..compose.tools import (
    Block,
    bars,
    double,
    dyn,
    fill,
    first,
    lines,
    octave,
    plain,
    put,
    rests,
    run,
    sweep,
    times,
    tr,
)
from ..notation.work import Work
from . import heavy
from .part4 import (
    BELLS_OFF_BEAT,
    BELLS_ON_BEAT,
    WARM,
    WARM_BASS,
    WARM_CHORDS,
    WARM_MIDDLE,
)

# The song theme in D major. In bar 4 it has a suspension: thus it agrees
# with the harmony of the warm theme.
SONG_TOGETHER = r"""
    a'2( g'4 fis'4 | e'2. d'4) | e'2( d'4 cis'4 | d'2 cis'2) |
    a'2\<( b'4 cis''4 | d''2.\> cis''4 | b'2 a'4 g'4 | a'1\!) |
"""

# The walking theme in a major key, as a middle voice below the two themes.
WALK_TOGETHER = r"""
    d'4.( e'8 fis'4. g'8 | a'2.) r4 | g4.( a8 b4. cis'8 | d'2 cis'2) |
    d'4.( e'8 fis'4. g'8 | b'2 a'2) | g'4.( a'8 b'4. cis''8 | d''2 cis''2) |
"""

# The chase theme in a major key: fast notes that follow the harmony.
RUN_TOGETHER = r"""
    d''8-. e''-. fis''-. gis''-. a''-. gis''-. fis''-. e''-. |
    e''8-. gis''-. b''-. gis''-. d''-. fis''-. a''-. fis''-. |
    g'8-. a'-. b'-. cis''-. d''-. cis''-. b'-. a'-. |
    a'8-. b'-. cis''-. d''-. e''-. d''-. cis''-. b'-. |
    a''8-. gis''-. fis''-. e''-. d''-. e''-. fis''-. gis''-. |
    b''8-. gis''-. e''-. gis''-. a''-. fis''-. d''-. fis''-. |
    d''8-. cis''-. b'-. a'-. g'-. a'-. b'-. cis''-. |
    a'8-. b'-. cis''-. e''-. g''-. e''-. cis''-. a'-. |
"""

# The chorale of part 1 in D major (8 bars), and the last cadence (3 bars).
# The highest voice of the cadence is the motto in its light form.
CHORALE = r"""
    <d fis a d'>1 | <e g d' e'>1 | <fis a d' a'>1 | <b, fis d' fis'>1 |
    <g, g b d'>1 | <a, g d' e'>1 | <a, g cis' e'>1 | <d fis a d'>1 |
    <g, g b d'>1 | <a, a d' e'>1 | <d a d' a'>1 |
"""


def write(work: Work) -> None:
    _first_light(work)
    _themes_together(work)
    _engine(work)
    _last_statement(work)


def _first_light(work: Work) -> None:
    """Mark GG: the harmonic series on D, from the lowest note up."""
    structure = work.structure
    count = 10
    s = work.section(count, 4, 4)
    structure.mark(s.bar(1), "GG")
    structure.tempo(s.bar(1), 1, 50, "Lento, come un'alba")
    block = Block(s, rests(4, 4, count))

    def enter(players: str, bar: int, half: int, chord: str, marks: str = "") -> None:
        """One note of the series: it starts in `bar` (first or second half) and stays."""
        letter = "X" if " " in chord else "A"
        parts = []
        if bar > 1:
            parts.append(rests(4, 4, bar - 1))
        start = rf"r2 {letter}2\ppp" if half == 2 else rf"{letter}1\ppp"
        parts.append(start + (r"\<" if bar >= 7 else "") + " ~ |")
        for number in range(bar + 1, count):
            parts.append(rf"{letter}1\< ~ |" if number == 7 else rf"{letter}1 ~ |")
        parts.append(rf"{letter}1\mf |")
        block.add(players, 1, fill(f"<{chord}>1", " ".join(parts)), marks)

    enter("cb bn3 cbcl", 1, 1, "d,,")
    enter("vc", 1, 2, "d, a,", r"\tutti\ord")
    enter("va", 2, 1, "d fis", r"\ord")
    enter("hn3 hn4", 2, 2, "a")
    enter("hn2", 3, 1, "c'")
    enter("vn2", 3, 2, "d' e'", r"\ord")
    enter("cl2", 4, 1, "fis'")
    enter("acc.rh", 4, 1, "d' a'")
    enter("cl1", 4, 2, "gih'")
    enter("ob2", 5, 1, "a'")
    enter("ob1", 5, 2, "beh'")
    enter("hn1", 6, 1, "c''")
    enter("vn1", 6, 2, "cis'' d''", r"\ord")
    enter("fl2", 7, 1, "e''")
    enter("fl1", 7, 2, "fis''")
    enter("fl3", 8, 1, "gih''")
    enter("cel.rh", 8, 2, "a''")
    block.add("perc4", 1, rests(4, 4, 8) + r"d'''1\pp\lv | a'''1\p\lv |")
    block.add("harp.rh", 1, rests(4, 4, 8) + r"<d'' fis'' a'' d'''>1\p\arpeggio | R1 |")
    block.add(
        "perc1", 1,
        r"""\switch "suspended cymbals" """ + rests(4, 4, 7)
        + r"c'1:32\ppp\< ~ | c'1:32 ~ | c'1:32\mp |",
    )  # fmt: skip
    block.add("timp", 1, rests(4, 4, 8) + r"d,1:32\pp\< ~ | d,1:32\mf |")
    block.close()


def _themes_together(work: Work) -> None:
    """Mark HH: the warm theme and the song theme at the same time."""
    structure = work.structure
    s = work.section(16, 4, 4)
    structure.mark(s.bar(1), "HH")
    structure.tempo(s.bar(1), 1, 60, "Andante, con moto")
    eight = rests(4, 4, 8)
    block = Block(s, eight, eight)

    # The first time: soft. The warm theme goes from one instrument to the subsequent
    # instrument, two bars each (horn, cellos, English horn, then horn and clarinet): the
    # listener gets the theme as a sequence of colours, not as one voice. (The owner of
    # the project: do not show the theme too frequently; change it or hide it.)
    block.add("hn1", 1, r"d'2\p\espr\solo( e'2 | gis'2 a'2) | R1*6 |")
    block.add("vc", 1, r"R1*2 | b'2\p\espr( a'4 fis'4 | e'1) | R1*4 |")
    block.add("ob3", 1, r"R1*4 | d'2\p\espr( e'2 | gis'4 a'4 d''2) | R1*2 |")
    block.add("hn3 cl1", 1, r"R1*6 | cis''2\p\espr( b'4 a'4 | fis'2. e'4) |")
    block.add("vn1:1", 1, first(SONG_TOGETHER, r"\p\dolce", note=True))
    block.add("fl1:1", 1, r"R1*4 | " + dyn(SONG_TOGETHER.split("|", 4)[4], r"\p"))
    block.add("va cl2", 1, dyn(WALK_TOGETHER, r"\p"))
    block.add("vn2", 1, dyn(WARM_MIDDLE, r"\p"))
    block.add("bn1 bn2 cb:-1", 1, dyn(WARM_BASS, r"\p"))
    quiet = {3: "R1 |", 4: "R1 |", 7: "R1 |", 8: "R1 |"}
    block.add("cel.rh", 1, dyn(bars(8, BELLS_ON_BEAT, quiet), r"\pp"))
    block.add("harp.rh", 1, dyn(bars(8, BELLS_OFF_BEAT, quiet), r"\pp"))

    # The second time: loud, with the chase theme in a major key.
    block.add("tpt1 tpt2 hn1 hn2 hn3 hn4 vc va", 2, dyn(WARM, r"\f\espr"))
    # The song theme, without its last bar. In the last bar, the woodwinds and the violins
    # trade short groups of thirty-second notes, and then they go up together to the first
    # stroke of the heavy section (a decision of the owner of the project).
    seven_bars = SONG_TOGETHER.replace(r"b'2 a'4 g'4 | a'1\!) |", r"b'2 a'4 g'4\!) |")
    song = octave(first(seven_bars, r"\f", note=True), 1)
    scale = "d e fis g a b cis"

    def burst(start: str, count: int, marks: str = "") -> str:
        notes = run(scale, start, count, 32).split()
        return f"{notes[0]}{marks}( {' '.join(notes[1:])})"

    together = burst("a'", 16)
    winds = burst("a''", 8, r"\ff") + " r4 " + together + " |"
    strings = "r4 " + burst("d'''", 8, r"\ff") + " " + together + " |"
    block.add("fl1 fl2", 2, song + " " + winds)
    # The oboes cannot play the low notes of the last figure: they play its second half.
    oboes = octave(burst("a''", 8, r"\ff") + " r4 r4 " + burst("b''", 8), -1) + " |"
    block.add("ob1 ob2", 2, song + " " + oboes)
    block.add("vn1", 2, song + " " + strings)
    block.add("vn2", 2, song + " " + octave(strings, -1))
    block.add("cl1 cl2 mand cimb.rh fl3:1 perc2:1 pno.rh:1", 2, dyn(RUN_TOGETHER, r"\f"))
    block.start("perc2", r'\switch "xylophone"')
    bass, tenor, alto, _top = lines(dyn(WARM_CHORDS, r"\mf"))
    block.add("btbn bn1 bn2 tuba:-1 bn3:-1 cb:-1", 2, bass)
    block.add("tbn2", 2, tenor)
    block.add("tbn1", 2, alto)
    block.add(
        "timp", 2,
        r"d,4\f r r2 | R1 | g,4 r r2 | a,4 r r2 | d,4 r r2 | R1 | g,4 r r2 | a,1:32\< |",
    )  # fmt: skip
    block.close()


def _engine(work: Work) -> None:
    """The rhythm of the heavy section of part 2 comes back, in D major.

    The riff of the low instruments has the motto in its light form (D, E,
    A). The calls of the brass and the peal of the bells have the same
    notes. The phrases move by major thirds (D, F-sharp, B-flat, D). The
    section ends with hammer strokes on the chord of D major.
    """
    structure = work.structure
    seven = (7, 8, (2, 2, 3))
    s = work.section(32, *seven)
    structure.mark(s.bar(1), "JJ")
    structure.tempo(s.bar(1), 1, 264, "Con slancio", unit="8")
    eight = rests(7, 8, 8)
    one = rests(7, 8)
    block = Block(s, eight, eight, eight, eight)

    # The riff has the four forms of the heavy section of part 2 (`heavy.py`), with the
    # light state of the motto: D, E, A, and the third F-sharp. Each phrase has the forms
    # in a different sequence: no unit of two bars comes two times. In the last phrase
    # the highest note of the cell is the octave D.
    orders = ["ABCD", "CADB", "BDAC", "DCBA"]
    cells = [
        {"R": "d,", "L": "e,", "M": "fis,", "H": "a,"},
        {"R": "d,", "L": "e,", "M": "fis,", "H": "a,"},
        {"R": "d,", "L": "e,", "M": "fis,", "H": "a,"},
        {"R": "d,", "L": "e,", "M": "a,", "H": "d"},
    ]
    levels = [r"\f", r"\f", r"\ff", r"\ff"]
    low_shifts = [0, 4, 8, 0]  # the riff: D, F-sharp, B-flat, D
    high_shifts = [0, 4, 8, 12]  # the chords of the strings go up
    brass_shifts = [0, 4, -4, 0]  # the calls stay in the range of the instruments
    roots = ["d,", "fis,", "bes,", "d,"]  # the notes of the timpani
    tom_notes = ["a", "c'", "e'", "c'"]
    # The chord of the gaps (the notes of the motto) has two positions: one for each
    # second unit of two bars.
    positions = [
        {"va": r"<d' a'>1", "vn2": r"<a' e''>1", "vn1": r"<e'' a''>1",
         "pno": r"<d' e' a' d''>1", "hn": r"<a d'>1"},
        {"va": r"<e' a'>1", "vn2": r"<a' d''>1", "vn1": r"<d'' e''>1",
         "pno": r"<e' a' d'' e''>1", "hn": r"<d' e'>1"},
    ]  # fmt: skip

    for phrase in (1, 2, 3, 4):
        level, shift = levels[phrase - 1], low_shifts[phrase - 1]
        music_of = heavy.layers(orders[phrase - 1], cells[phrase - 1], roots[phrase - 1], tom_notes)
        low = " ".join(tr(bar, shift) for bar in music_of["low"])
        block.add("cb tuba btbn bn3 cbcl cl3 vc bn1:1 bn2:1 cimb.lh:1", phrase, low, level)
        if phrase <= 2:
            # The trombones make the riff heavier, until they get the calls.
            block.add("tbn1:1 tbn2:1", phrase, low, level)
        block.add("pno.lh", phrase, double(low, -1), level)
        # Two horns, the high strings, and the piano play in the gaps of the riff.
        chords: dict[str, list[str]] = {name: [] for name in positions[0]}
        for unit in range(4):
            gap_bars = " ".join(music_of["gaps"][2 * unit : 2 * unit + 2])
            for name, chord in positions[unit % 2].items():
                lift = high_shifts[phrase - 1] if name in ("va", "vn2", "vn1") else shift
                chords[name].append(fill(tr(chord, lift), gap_bars))
        block.spread("hn6 hn5", phrase, " ".join(chords["hn"]), level)
        for player in ("va", "vn2", "vn1"):
            block.add(player, phrase, " ".join(chords[player]), level)
        block.add("pno.rh", phrase, " ".join(chords["pno"]), level)
        block.add("timp", phrase, " ".join(music_of["timp"]), level)
        block.add("perc3", phrase, " ".join(music_of["bass drum"]), level)
        block.add("perc6", phrase, " ".join(music_of["taiko"]), level)
        block.add("perc5", phrase, " ".join(music_of["toms"]), level)
        if phrase >= 2:
            # The snare drum plays in the other gaps, with a roll in the last bar.
            snare = music_of["snare"][:7] + [r"c'2..:32\< |"]
            block.add("perc4", phrase, " ".join(snare), level)
            block.add("perc1", phrase, r"c'8\ff\lv r r4 r4. | " + rests(7, 8, 7))
    block.start("perc6", r'\switch "taiko"')
    block.start("perc5", r'\switch "tom-toms"')
    block.add("perc4", 1, r'\switch "snare drum" ' + eight)
    block.add("perc1", 1, r'\switch "crash cymbals" ' + eight)

    # The bells and the celesta ring the three notes of the motto as bell ringers do:
    # each bar has the notes in a new sequence, and two notes change places from one
    # bar to the subsequent bar. The player of the bells comes from the xylophone: the
    # first phrase gives the time.
    changes = ["d' e' a'", "e' d' a'", "e' a' d'", "a' e' d'", "a' d' e'", "d' a' e'"]
    every = tuple(range(1, 9))
    count = 0
    for phrase in (2, 3, 4):
        numbers = (1, 3, 5, 7) if phrase == 2 else every
        peals = {}
        for number in numbers:
            first_bell, second_bell, third_bell = changes[count % len(changes)].split()
            peal = f"{first_bell}4 {second_bell}4 {third_bell}4. |"
            peals[number] = tr(peal, low_shifts[phrase - 1])
            count += 1
        block.add("perc2 cel.rh:2", phrase, bars(8, one, peals), levels[phrase - 1])
    block.start("perc2", r'\switch "tubular bells"')

    # The calls of the brass: the motto in four forms (short, late, broad, and down). A
    # call does not have the form of the call before it. When two groups call in the
    # same bar, they have different forms.
    call_forms = [
        r"d'8-> e'8-> a'4.-> r4 |",
        r"r4 d'8-> e'8-> a'4.-> |",
        r"d'4-> e'4-> a'4.-> |",
        r"a'8-> e'8-> d'4.-> r4 |",
    ]

    def calls(numbers: tuple[int, ...], shift: int, turn: int = 0) -> str:
        music = {number: tr(call_forms[(number + turn) % 4], shift) for number in numbers}
        return bars(8, one, music)

    block.add("hn1 hn3", 1, calls((3, 7), 0, 1), r"\f")
    block.add("hn1 hn2 hn3 hn4", 2, calls((3, 7), brass_shifts[1], 2), r"\f")
    block.add("tpt1 tpt2", 2, calls((1, 5), brass_shifts[1]), r"\f")
    block.add("hn1 hn2 hn3 hn4 tbn1:-1 tbn2:-1", 3, calls((2, 4, 6, 8), brass_shifts[2], 1), r"\ff")
    block.add("tpt1 tpt2 tpt3", 3, calls((1, 3, 5, 7), brass_shifts[2] + 12, 3), r"\ff")
    block.add("tpt1:1 tpt2 tpt3", 4, calls(every, 0), r"\ff")
    block.add("hn1 hn2 hn3 hn4", 4, calls(every, 0, 2), r"\ff")
    block.add("tbn1:-1 tbn2:-1", 4, calls((2, 4, 6, 8), 0, 1), r"\ff")

    # The chase theme in a major key, in the woodwinds: four forms (up and down, the
    # mirror form, from the third, and in a zigzag).
    run_forms = [
        r"d''8-> e'' fis''-> gis'' a''-> gis'' fis'' |",
        r"a''8-> gis'' fis''-> e'' d''-> e'' fis'' |",
        r"fis''8-> gis'' a''-> gis'' fis''-> e'' d'' |",
        r"d''8-> fis'' e''-> gis'' fis''-> a'' gis'' |",
    ]

    def runs(numbers: tuple[int, ...], shift: int) -> str:
        return bars(8, one, {number: tr(run_forms[number % 4], shift) for number in numbers})

    block.add("fl1:1 fl2:1 ob1 ob2 cl1 cl2", 2, runs((2, 4, 6, 8), 4), r"\f")
    block.add("fl1:1 fl2:1 fl3:1 ob1 ob2 cl1 cl2", 3, runs(every, -4), r"\ff")
    block.add("fl1:1 fl2:1 fl3:1 ob1 ob2 cl1 cl2", 4, runs(every, 0), r"\ff")
    block.close()

    # ------------------------------------------------ hammer strokes on D major (4 bars)
    s = work.section(4, *seven)
    stroke = r"X8-> r X8-> r X8-> X X |"
    run_of_strokes = r"X8-> X X-> X X-> X X |"
    last = r"X8-> X X-> X X4.-> |"

    def hammer(chord: str) -> str:
        letter = "X" if " " in chord else "A"
        patterns = [stroke, stroke, run_of_strokes, last]
        text = " ".join(fill(f"<{chord}>1", pattern.replace("X", letter)) for pattern in patterns)
        return first(text, r"\fff", note=True)

    put(s, "cb tuba btbn bn3 cbcl cl3 timp", hammer("d,"))
    put(s, "bn1 bn2 tbn2", hammer("a,"))
    put(s, "tbn1 hn4", hammer("d"))
    put(s, "hn3", hammer("fis"))
    put(s, "hn2", hammer("a"))
    put(s, "hn1 tpt3", hammer("d'"))
    put(s, "tpt2 cl2 ob2", hammer("fis'"))
    put(s, "tpt1 cl1 ob1", hammer("a'"))
    put(s, "fl2 fl3", hammer("d''"))
    put(s, "fl1", hammer("fis''"))
    s.write("vc", hammer("d a"))
    s.write("va", hammer("d' a'"))
    s.write("vn2", hammer("fis' d''"))
    s.write("vn1", hammer("a'' d'''"))
    s.write("pno.lh", hammer("d,, d,"))
    s.write("pno.rh", hammer("d' fis' a' d''"))
    strokes = r"c'8->\fff r c'8-> r c'8-> r4 |"
    s.write("perc3", times(strokes, 3) + r" c'8-> r c'8-> r c'4.-> |")
    s.write(
        "perc6", times(strokes, 2) + r" c'8-> c' c'-> c' c'-> c' c' | c'8-> c' c'-> c' c'4.-> |"
    )
    # The players of the snare drum and of the tom-toms stop in the first bar.
    # They go to the glockenspiel and to the tam-tam.
    three = rests(7, 8, 3)
    s.write("perc4", r"c'8->\fff r c'8-> r r4. | " + three)
    s.write("perc5", r"a8->\fff r c'8-> r r4. | " + three)
    s.write("perc1", r"c'8\fff\lv r r4 r4. | " + rests(7, 8, 2) + r"r4 r4 c'4.\lv |")
    s.close()


def _last_statement(work: Work) -> None:
    """Mark KK: the chorale in D major, and the last chord."""
    structure = work.structure
    s = work.section(21, 4, 4)
    structure.mark(s.bar(1), "KK")
    structure.tempo(s.bar(1), 1, 50, "Maestoso")
    block = Block(s, rests(4, 4, 11), rests(4, 4, 10))

    # The chorale (11 bars).
    bass, tenor, alto, top = lines(dyn(CHORALE, r"\fff"))
    block.add("tpt1:1 tpt2 ob1:1 ob2:1 fl1:2 fl2:2 fl3:2 vn1:2 vn2:1 hn5 hn6", 1, top)
    block.add("tpt3 hn1 hn3 cl1:1 cl2:1 tbn1", 1, alto)
    block.add("hn2 hn4 tbn2 va", 1, tenor)
    block.add("btbn bn1 bn2 cl3 vc tuba:-1 bn3:-1 cbcl:-1 cb:-1", 1, bass)
    block.add("pno.lh", 1, double(bass, -1))
    # Each hand has a chord that it can reach: not more than an octave.
    block.add("pno.rh", 1, fill(dyn(CHORALE, r"\fff"), r"<B' C' D'>1"))
    block.add("acc.rh", 1, fill(dyn(CHORALE, r"\ff"), r"<B C D>1"))
    block.add(
        "timp", 1,
        r"d,1:32\fff | R1 | d,1:32 | R1 | g,1:32 | a,1:32 ~ | a,1:32 | d,1:32 | "
        r"g,1:32 | a,1:32 | d,1:32 |",
    )  # fmt: skip
    block.add(
        "perc2", 1,
        r"""\switch "tubular bells" d'1\fff | e'1 | a'1 | fis'1 | d'1 | e'1 | e'1 | d'1 | """
        r"d'1 | e'1 | a'1 |",
    )  # fmt: skip
    block.add("perc5", 1, r"""\switch "tam-tams" c'1\fff\lv | R1*7 | c'1\lv | R1*2 |""")
    block.add("perc3", 1, r"c'4\fff r r2 | R1*3 | c'4 r r2 | R1*3 | c'4 r r2 | R1 | c'4 r r2 |")
    # The owner of the project: "the ending should also use crotales and chimes and such,
    # really let it sparkle". The bright instruments come in one after the other. The
    # glockenspiel rings each chord in eighth notes: the note of the highest voice is on
    # beats 1 and 3. The celesta runs through each chord, and the harp rolls each chord.
    block.add("perc4", 1, fill(dyn(CHORALE, r"\fff"), r"D''8 C''' D''' C''' D'' C''' D''' C'''"))
    block.start("perc4", r'\switch "glockenspiel"')
    sparkle = r"B'16( C' D' B'' C'' D'' C'' B'' D' C' B' D' C' D' B'' D'')"
    block.add("cel.rh", 1, fill(dyn(CHORALE, r"\ff"), sparkle))
    block.add("harp.rh", 1, fill(dyn(CHORALE, r"\fff"), r"<B' C' D'>1\arpeggio"))
    block.add("harp.lh", 1, fill(dyn(CHORALE, r"\fff"), r"<A, A>1\arpeggio"))
    # The hand cymbals have the first stroke. Then their player goes to the crotales:
    # they come in on the highest note of the first phrase, with the highest voice.
    ringing = [bar.strip() for bar in plain(octave(top, 2)).split("|") if bar.strip()]
    block.add(
        "perc1", 1,
        r"""c'1\fff\lv | R1 | \switch "crotales" """
        + first(" | ".join(ringing[2:]) + " |", r"\ff\lv"),
    )  # fmt: skip
    # The player of the taiko goes to the suspended cymbal: a roll that grows before
    # each phrase, and a stroke at the start of the phrase.
    block.add(
        "perc6", 1,
        r"""R1*3 | \switch "suspended cymbals" c'1:32\mf\< | c'4\fff\lv r4 r2 | R1*2 | """
        r"c'1:32\mf\< | c'4\fff\lv r4 r2 | c'1:32\f\< | c'4\fff\lv r4 r2 |",
    )  # fmt: skip

    # The last chord (10 bars): D major. The brass has the motto in long notes.
    motto = r"d'1\fff-^ | e'1-^ | a'1-^ ~ | a'1 | "
    block.add(
        "tpt1:1 tpt2:1 tpt3 hn1 hn3 hn5 tbn1:-1", 2,
        motto + r"a'1 ~ | a'1 ~ | a'1 ~ | a'1 | a'2.-^ r4 | a'1-^\fermata |",
    )  # fmt: skip
    block.add(
        "hn2 hn4 hn6 tbn2:-1", 2,
        motto.replace("a'1-^ ~ | a'1", "fis'1-^ ~ | fis'1")
        + r"fis'1 ~ | fis'1 ~ | fis'1 ~ | fis'1 | fis'2.-^ r4 | fis'1-^\fermata |",
    )  # fmt: skip
    hold = r"X1:32\fff ~ | " + r"X1:32 ~ | " * 6 + r"X1:32 | X2.-^ r4 | X1-^\fermata |"
    # The first violins are in their highest register (D7).
    for player, chord in [("vn1", "fis''' d''''"), ("vn2", "a'' fis'''"), ("va", "d' a'"),
                          ("vc", "d a")]:  # fmt: skip
        block.add(player, 2, fill(f"<{chord}>1", hold))
    plain_hold = hold.replace(":32", "").replace("X", "A")
    block.add("cb btbn tuba bn3 cbcl bn1:1 bn2:1 cl3:1", 2, fill(r"<d,>1", plain_hold))
    block.add("acc.rh", 2, fill(r"<d' fis' a' d''>1", plain_hold))
    block.add("cimb.lh", 2, fill(r"<d d'>1", hold))
    block.add("mand", 2, fill(r"<fis'' a''>1", hold))
    block.add("ob1:-1 ob2:-1 cl1:-1 cl2:-2", 2, fill(r"<d'''>1", plain_hold))
    # The flutes and the piccolo: a long trill on the highest D.
    trill = r"A1\fff\trill ~ | " + r"A1\trill ~ | " * 6 + r"A1\trill | A2.-^ r4 | A1-^\fermata |"
    block.add("fl1 fl2:-1 fl3", 2, fill(r"<d'''>1", trill))
    block.add(
        "timp", 2,
        times(r"d,4->\fff a,4-> d,4-> a,4-> |", 4)
        + r" d,1:32 ~ | d,1:32 ~ | d,1:32 ~ | d,1:32 | d,2.-^ r4 | d,1:32\fermata |",
    )  # fmt: skip
    peal = r"d'4\fff e' a' e' |"
    block.add("perc2", 2, times(peal, 8) + r" d'2. r4 | d'1\fermata |")
    ring = r"d'''8\fff e''' a''' e''' d''' e''' a''' e''' |"
    block.add("perc4", 2, times(ring, 4) + r" d'''8 e''' gis''' a''' " * 2 + "| "
              + times(ring, 3) + r" a'''2. r4 | a'''1\fermata |")  # fmt: skip
    block.add("cel.rh", 2, dyn(times(BELLS_ON_BEAT, 8), r"\ff") + r" R1 | R1\fermata |")
    # The harp rolls the last two chords through its two hands.
    block.add(
        "harp.rh", 2,
        dyn(times(BELLS_OFF_BEAT, 8), r"\ff")
        + r" <d'' fis'' a''>2.\arpeggio r4 | <d'' fis'' a''>1\arpeggio\fermata |",
    )  # fmt: skip
    block.add(
        "harp.lh", 2, r"R1*8 | <d' fis' a'>2.\ff\arpeggio r4 | <d' fis' a'>1\arpeggio\fermata |"
    )
    # The piano: deep bell strokes (the chord goes up from stroke to stroke), and free
    # sweeps between them, as a harp plays them. The owner of the project heard the
    # first form of these lines (equal sextuplets, the same line two times) as "rigid",
    # and they did not blend. Thus each sweep is different: its direction, its length,
    # its place in the bar, and its notes. Each sweep grows, and its groups have
    # more and more notes (a written acceleration): no group sounds as a beat.
    octave_d = r"<d,, d,>"
    pentatonic, lydian = "d e fis a b", "d e fis gis a b"
    plan = [
        # the chord, the scale, the first note, the first eighth note, the sizes of the
        # groups, down?, the marks of the two hands, the end of the bar in each hand
        (r"<d' fis' a' d''>", pentatonic, "d,", 2, (4, 5, 5, 6), False,
         r"\mf\<\quasiarpa", r"\f\<", "", r"d'''4->\ff"),
        (r"<fis' a' d'' fis''>", lydian, "b'''", 1, (6, 5, 5, 4), True,
         r"\f\>", r"\ff\>", r"r8 <d, a,>4->\mf", ""),
        (r"<a' d'' fis'' a''>", pentatonic, "a,,", 1, (4, 5, 5, 6, 6), False,
         r"\mf\<", r"\f\<", "", r"<fis''' b'''>4->\ff"),
        (r"<d'' fis'' a'' d'''>", pentatonic, "d,,", 0, (4, 4, 5, 5, 6, 6), False,
         r"\f\<", r"\ff\<", "", r"<a''' d''''>4->\fff"),
    ]  # fmt: skip
    right, left = [], []
    for chord, scale, start, slot, sizes, down, low_marks, high_marks, low_end, high_end in plan:
        groups = sweep(scale, start, sizes, down=down)
        low, high = _two_hands(groups, slot, low_marks, high_marks, low_end, high_end)
        right += [rf"{chord}1\fff", high]
        left += [rf"{octave_d}1\fff\sustainOff\sustainOn", low]
    last = r"<d'' fis'' a'' d'''>"
    block.add(
        "pno.rh", 2,
        " | ".join(right) + rf" | {last}2.-^\fff r4 | {last}1-^\fermata |",
    )  # fmt: skip
    block.add(
        "pno.lh", 2,
        " | ".join(left) + rf" | {octave_d}2.-^\fff\sustainOff\sustainOn r4 | "
        rf"{octave_d}1-^\sustainOff\sustainOn\fermata |",
    )  # fmt: skip
    # The sparkle of the last chord: four bell instruments ring the notes of the motto at
    # four speeds (tubular bells in quarter notes, glockenspiel in eighth notes, crotales
    # in triplets, celesta and harp between them). The triangle has a long roll.
    ring_three = (
        r"\tuplet 3/2 { d'''4 e''' a''' } \tuplet 3/2 { e'''4 d''' a''' } | "
        r"\tuplet 3/2 { a'''4 e''' d''' } \tuplet 3/2 { e'''4 a''' d''' } |"
    )
    block.add(
        "perc1", 2,
        first(times(ring_three, 4), r"\ff", note=True) + r" <d''' a'''>2.\lv r4 | "
        r"<d''' a'''>1\lv\fermata |",
    )  # fmt: skip
    block.add(
        "perc5", 2,
        r"""c'1\fff\lv | R1 | \switch "triangle" c'1:32\mp\< ~ | c'1:32 ~ | c'1:32 ~ | """
        r"""c'1:32 ~ | c'1:32\ff | R1 | \switch "tam-tams" c'2.\fff\lv r4 | c'1\lv\fermata |""",
    )  # fmt: skip
    block.add(
        "perc6", 2,
        r"c'4\fff\lv r4 r2 | R1*2 | c'1:32\mf\< | c'4\fff\lv r4 r2 | R1*2 | c'1:32\f\< | "
        r"c'2.\fff\lv r4 | c'1\lv\fermata |",
    )  # fmt: skip
    block.add("perc3", 2, r"c'4\fff r r2 | R1*3 | c'1:32 ~ | c'1:32 ~ | c'1:32 ~ | c'1:32 | "
              r"c'2. r4 | c'1\fermata |")  # fmt: skip
    block.close()


LEFT_HAND_TOP = 64  # E4: a group of a sweep with no higher note is in the left hand


def _two_hands(
    groups: list[tuple[str, int, int]],
    slot: int,
    low_marks: str,
    high_marks: str,
    low_end: str = "",
    high_end: str = "",
) -> tuple[str, str]:
    """Return one bar of 4/4 for the two hands of the piano, with a sweep.

    `groups` is the result of `sweep()`: each group fills one eighth note, and
    the first group is at the eighth note `slot` of the bar (0 to 7). A low
    group goes to the left hand, a high group to the right hand. The marks go
    on the first note of each hand, and a slur is above the notes of each hand.
    `low_end` and `high_end` are the music of each hand after the sweep, to
    the end of the bar (default: rests). If a hand has a hairpin and no music
    after the sweep, the hairpin stops on its last note.

    The result is the bar of the left hand, then the bar of the right hand,
    each with no bar line.
    """
    after = slot + len(groups)
    bars = []
    for right, marks, end in ((False, low_marks, low_end), (True, high_marks, high_end)):
        mine = {
            slot + number: group
            for number, (group, _lowest, highest) in enumerate(groups)
            if (highest > LEFT_HAND_TOP) == right
        }
        tokens: list[str] = []
        position = 0
        for number in sorted(mine):
            tokens += _rests(position, number)
            group = mine[number]
            if number == min(mine):
                group = group.replace("32", "32" + marks + "(", 1)
            if number == max(mine):
                stop = r"\!" if not end and ("<" in marks or ">" in marks) else ""
                head, brace, tail = group.rpartition(" }")
                group = head + ")" + stop + brace + tail if brace else group + ")" + stop
            tokens.append(group)
            position = number + 1
        # After the notes of this hand: rests to the music after the sweep, or to the
        # end of the bar.
        tokens += _rests(position, after if end else 8)
        bars.append(" ".join([*tokens, end]).strip())
    return bars[0], bars[1]


def _rests(first: int, last: int) -> list[str]:
    """Return rests for the eighth notes `first` to before `last` of a bar of 4/4."""
    result = []
    while first < last:
        if first % 4 == 0 and last - first >= 4:
            result.append("r2")
            first += 4
        elif first % 2 == 0 and last - first >= 2:
            result.append("r4")
            first += 2
        else:
            result.append("r8")
            first += 1
    return result
