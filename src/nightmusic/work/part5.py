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
    put,
    rests,
    run,
    times,
    tr,
)
from ..notation.work import Work
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
    """Mark EE: the harmonic series on D, from the lowest note up."""
    structure = work.structure
    count = 10
    s = work.section(count, 4, 4)
    structure.mark(s.bar(1), "EE")
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
    enter("cl1", 4, 1, "fis'")
    enter("acc.rh", 4, 1, "d' a'")
    enter("cl2", 4, 2, "gih'")
    enter("ob1", 5, 1, "a'")
    enter("ob2", 5, 2, "beh'")
    enter("hn1", 6, 1, "c''")
    enter("vn1", 6, 2, "cis'' d''", r"\ord")
    enter("fl1", 7, 1, "e''")
    enter("fl2", 7, 2, "fis''")
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
    """Mark FF: the warm theme and the song theme at the same time."""
    structure = work.structure
    s = work.section(16, 4, 4)
    structure.mark(s.bar(1), "FF")
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
    structure.mark(s.bar(1), "GG")
    structure.tempo(s.bar(1), 1, 264, "Con slancio", unit="8")
    eight = rests(7, 8, 8)
    one = rests(7, 8)
    block = Block(s, eight, eight, eight, eight)

    riff = r"d,8-> r d,8-> r a,8-> e,8 d,8 | d,8-> d,8 r e,8-> r d,8-> a,8 |"
    gaps = r"r8 X8-> r X8-> r4 X8-> | r4 X8-> r X8-> r4 |"
    call = r"d'8-> e'8-> a'4.-> r4 |"
    peal = r"d'4 e'4 a'4. |"
    run = r"d''8-> e'' fis''-> gis'' a''-> gis'' fis'' |"
    levels = [r"\f", r"\f", r"\ff", r"\ff"]
    low_shifts = [0, 4, 8, 0]  # the riff: D, F-sharp, B-flat, D
    high_shifts = [0, 4, 8, 12]  # the chords of the strings go up
    brass_shifts = [0, 4, -4, 0]  # the calls stay in the range of the instruments
    bell_shifts = [0, 4, 8, 0]
    drums = [("d,", "a,"), ("fis,", "cis"), ("bes,", "f"), ("d,", "a,")]

    for phrase in (1, 2, 3, 4):
        level = levels[phrase - 1]
        low = times(tr(riff, low_shifts[phrase - 1]), 4)
        block.add("cb tuba btbn bn3 cbcl cl3 vc bn1:1 bn2:1 cimb.lh:1", phrase, low, level)
        if phrase <= 2:
            # The trombones make the riff heavier, until they get the calls.
            block.add("tbn1:1 tbn2:1", phrase, low, level)
        block.add("pno.lh", phrase, double(low, -1), level)
        # Two horns play in the gaps of the riff, with the high strings.
        horns = times(fill(tr(r"<a d'>1", low_shifts[phrase - 1]), gaps), 4)
        block.spread("hn6 hn5", phrase, horns, level)
        shift = high_shifts[phrase - 1]
        for player, chord in [("va", r"<d' a'>1"), ("vn2", r"<a' e''>1"), ("vn1", r"<e'' a''>1")]:
            block.add(player, phrase, times(fill(tr(chord, shift), gaps), 4), level)
        block.add(
            "pno.rh", phrase,
            times(fill(tr(r"<d' e' a' d''>1", low_shifts[phrase - 1]), gaps), 4), level,
        )  # fmt: skip
        root, fifth = drums[phrase - 1]
        beat = f"{root}8-> r {root}8-> r {fifth}8-> r4 | {root}8-> {root}8 r4 r8 {fifth}8-> r |"
        block.add("timp", phrase, times(beat, 4), level)
        block.add("perc3", phrase, times(r"c'8-> r r4 c'8-> r4 | c'8-> r r4 r4. |", 4), level)
        block.add(
            "perc6", phrase,
            times(r"c'8-> r c'8-> r c'8-> r4 | c'8-> c'8 r c'8-> r c'8-> r |", 4), level,
        )  # fmt: skip
        block.add("perc5", phrase, times(r"r4 r4 r8 a8 c'8 | r4 r8 e'8 r c'8 a8 |", 4), level)
    # The bells and the celesta peal the motto: from the second phrase, then in each bar.
    # The player of the bells comes from the xylophone: the first phrase gives the time.
    every = tuple(range(1, 9))
    for phrase in (2, 3, 4):
        bell = tr(peal, bell_shifts[phrase - 1])
        numbers = (1, 3, 5, 7) if phrase == 2 else every
        text = bars(8, one, dict.fromkeys(numbers, bell))
        block.add("perc2 cel.rh:2", phrase, text, levels[phrase - 1])
    block.start("perc2", r'\switch "tubular bells"')
    block.start("perc6", r'\switch "taiko"')
    block.start("perc5", r'\switch "tom-toms"')

    # The snare drum from the second phrase. Hand cymbals at the start of each phrase.
    snare = r"r4 c'8-> r r4 c'8-> | r4 c'8-> r r4. |"
    roll = r"r4 c'8-> r r4 c'8-> | c'2..:32\< |"
    block.add("perc4", 1, r'\switch "snare drum" ' + eight)
    for phrase in (2, 3, 4):
        block.add("perc4", phrase, times(snare, 3) + roll, levels[phrase - 1])
        block.add("perc1", phrase, r"c'8\ff\lv r r4 r4. | " + rests(7, 8, 7))
    block.add("perc1", 1, r'\switch "crash cymbals" ' + eight)

    # The calls: at first two in a phrase, then one in each bar.
    def calls(numbers: tuple[int, ...], shift: int) -> str:
        return bars(8, one, {number: tr(call, shift) for number in numbers})

    block.add("hn1 hn3", 1, calls((3, 7), 0), r"\f")
    block.add("hn1 hn2 hn3 hn4", 2, calls((3, 7), brass_shifts[1]), r"\f")
    block.add("tpt1 tpt2", 2, calls((1, 5), brass_shifts[1]), r"\f")
    block.add("hn1 hn2 hn3 hn4 tbn1:-1 tbn2:-1", 3, calls((2, 4, 6, 8), brass_shifts[2]), r"\ff")
    block.add("tpt1 tpt2 tpt3", 3, calls((1, 3, 5, 7), brass_shifts[2] + 12), r"\ff")
    block.add("tpt1:1 tpt2 tpt3", 4, calls(every, 0), r"\ff")
    block.add("hn1 hn2 hn3 hn4", 4, calls(every, 0), r"\ff")
    block.add("tbn1:-1 tbn2:-1", 4, calls((2, 4, 6, 8), 0), r"\ff")

    # The chase theme in a major key, in the woodwinds and the xylophone part of the piano.
    def runs(numbers: tuple[int, ...], shift: int) -> str:
        return bars(8, one, {number: tr(run, shift) for number in numbers})

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
    """Mark HH: the chorale in D major, and the last chord."""
    structure = work.structure
    s = work.section(21, 4, 4)
    structure.mark(s.bar(1), "HH")
    structure.tempo(s.bar(1), 1, 50, "Maestoso")
    block = Block(s, rests(4, 4, 11), rests(4, 4, 10))

    # The chorale (11 bars).
    bass, tenor, alto, top = lines(dyn(CHORALE, r"\fff"))
    block.add("tpt1:1 tpt2 ob1:1 ob2:1 fl1:2 fl2:2 fl3:2 vn1:2 vn2:1 hn5 hn6 perc4:2", 1, top)
    block.add("tpt3 hn1 hn3 cl1:1 cl2:1 tbn1", 1, alto)
    block.add("hn2 hn4 tbn2 va", 1, tenor)
    block.add("btbn bn1 bn2 cl3 vc tuba:-1 bn3:-1 cbcl:-1 cb:-1", 1, bass)
    block.add("pno.lh", 1, double(bass, -1))
    block.add("pno.rh", 1, fill(dyn(CHORALE, r"\fff"), r"<B C D B' C' D'>1"))
    block.add("acc.rh", 1, fill(dyn(CHORALE, r"\ff"), r"<B C D B' C' D'>1"))
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
    block.start("perc4", r'\switch "glockenspiel"')
    # Hand cymbals at the start of each phrase. The suspended cymbal grows into them.
    block.add(
        "perc1", 1,
        r"c'4\fff\lv r4 r2 | R1*3 | c'4\lv r4 r2 | R1*3 | c'4\lv r4 r2 | R1 | c'4\lv r4 r2 |",
    )  # fmt: skip
    block.add(
        "perc6", 1,
        r"""\switch "suspended cymbals" R1*3 | c'1:32\mf\< | R1*3 | c'1:32\mf\< | """
        r"R1 | c'1:32\f\< | R1 |",
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
    for player, chord in [("vn1", "fis'' d'''"), ("vn2", "a' fis''"), ("va", "d' a'"),
                          ("vc", "d a")]:  # fmt: skip
        block.add(player, 2, fill(f"<{chord}>1", hold))
    plain_hold = hold.replace(":32", "").replace("X", "A")
    block.add("cb btbn tuba bn3 cbcl bn1:1 bn2:1 cl3:1", 2, fill(r"<d,>1", plain_hold))
    block.add("acc.rh", 2, fill(r"<d' fis' a' d''>1", plain_hold))
    block.add("cimb.lh", 2, fill(r"<d d'>1", hold))
    block.add("mand", 2, fill(r"<fis'' a''>1", hold))
    block.add("fl1 fl2:-1 fl3 ob1:-1 ob2:-1 cl1:-1 cl2:-2", 2, fill(r"<d'''>1", plain_hold))
    block.add(
        "timp", 2,
        times(r"d,4->\fff a,4-> d,4-> a,4-> |", 4)
        + r" d,1:32 ~ | d,1:32 ~ | d,1:32 ~ | d,1:32 | d,2.-^ r4 | d,1:32\fermata |",
    )  # fmt: skip
    peal = r"d'4\fff e' a' e' |"
    block.add("perc2", 2, times(peal, 8) + r" d'2. r4 | d'1\fermata |")
    ring = r"d'''8\ff e''' a''' e''' d''' e''' a''' e''' |"
    block.add("perc4", 2, times(ring, 4) + r" d'''8 e''' gis''' a''' " * 2 + "| "
              + times(ring, 3) + r" a'''2. r4 | a'''1\fermata |")  # fmt: skip
    block.add("cel.rh", 2, dyn(times(BELLS_ON_BEAT, 8), r"\ff") + r" R1 | R1\fermata |")
    block.add("harp.rh", 2, dyn(times(BELLS_OFF_BEAT, 8), r"\ff")
              + r" <d' fis' a' d'' fis'' a''>2.\arpeggio r4 | "
              r"<d' fis' a' d'' fis'' a''>1\arpeggio\fermata |")  # fmt: skip
    chord = r"<d' fis' a' d'' fis'' a''>"
    block.add("pno.rh", 2, rf"{chord}1\fff | R1 | {chord}1 | R1 | {chord}1 | R1 | {chord}1 | R1 | "
              rf"{chord}2.-^ r4 | {chord}1-^\fermata |")  # fmt: skip
    octave_d = r"<d,, d,>"
    block.add("pno.lh", 2, rf"{octave_d}1\fff | R1 | {octave_d}1 | R1 | {octave_d}1 | R1 | "
              rf"{octave_d}1 | R1 | {octave_d}2.-^ r4 | {octave_d}1-^\fermata |")  # fmt: skip
    block.add("perc5", 2, r"c'1\fff\lv | R1*3 | c'1\lv | R1*3 | c'2.\lv r4 | c'1\lv\fermata |")
    block.add(
        "perc1", 2,
        r"c'4\fff\lv r4 r2 | R1*3 | c'4\lv r4 r2 | R1*3 | c'2.\lv r4 | c'1\lv\fermata |",
    )  # fmt: skip
    block.add(
        "perc6", 2,
        r"""\switch "taiko" """
        + times(r"c'4->\fff c'4-> c'4-> c'4-> |", 4)
        + times(r" c'8-> c' c'-> c' c'-> c' c'-> c' |", 4)
        + r" c'2.-> r4 | c'1->\fermata |",
    )  # fmt: skip
    block.add("perc3", 2, r"c'4\fff r r2 | R1*3 | c'1:32 ~ | c'1:32 ~ | c'1:32 ~ | c'1:32 | "
              r"c'2. r4 | c'1\fermata |")  # fmt: skip
    block.close()
