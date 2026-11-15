"""Part 5: first light, the themes together, the calls, and the last statement.

Material of this part:

- First light: the notes of the harmonic series on D come in one after the
  other, from the lowest. Partial 11 is between G and G-sharp. Thus the
  note that was A-flat in the dark and G-sharp in the shimmer is now a part
  of the sound of D.
- The warm theme and the song theme at the same time, in D major. The
  walking theme and the chase theme go with them.
- The calls of the brass and woodwinds: each has the motto in its light
  form (D, E, A) at its own speed. They come together on one chord.
- The chorale of part 1 in D major, fff, and the last chord.

Style profile: "Theatre", then "Transfigured" after the turn.
"""

from __future__ import annotations

from ..compose.tools import Block, bars, double, dyn, fill, first, lines, rests, scatter, times, tr
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
    d''8-. e''-. fis''-. gis''-. a''-. gis''-. fis''-. e''-. |
    e''8-. gis''-. b''-. gis''-. d''-. fis''-. a''-. fis''-. |
    g'8-. a'-. b'-. cis''-. d''-. cis''-. b'-. a'-. |
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
    _calls(work)
    _last_statement(work)


def _first_light(work: Work) -> None:
    """Bars 399 to 408: the harmonic series on D, from the lowest note up."""
    structure = work.structure
    count = 10
    s = work.section(count, 4, 4)
    structure.mark(s.bar(1), "DD")
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
    """Bars 409 to 424: the warm theme and the song theme at the same time."""
    structure = work.structure
    s = work.section(16, 4, 4)
    structure.mark(s.bar(1), "EE")
    structure.tempo(s.bar(1), 1, 60, "Andante, con moto")
    eight = rests(4, 4, 8)
    block = Block(s, eight, eight)

    # The first time: soft.
    block.add("hn1 hn3 vc", 1, dyn(WARM, r"\p\espr"))
    block.add("vn1:1", 1, first(SONG_TOGETHER, r"\p\dolce", note=True))
    block.add("fl1:1", 1, r"R1*4 | " + dyn(SONG_TOGETHER.split("|", 4)[4], r"\p"))
    block.add("va cl1 ob3", 1, dyn(WALK_TOGETHER, r"\p"))
    block.add("vn2", 1, dyn(WARM_MIDDLE, r"\p"))
    block.add("bn1 bn2 cb:-1", 1, dyn(WARM_BASS, r"\p"))
    quiet = {3: "R1 |", 4: "R1 |", 7: "R1 |", 8: "R1 |"}
    block.add("cel.rh", 1, dyn(bars(8, BELLS_ON_BEAT, quiet), r"\pp"))
    block.add("harp.rh", 1, dyn(bars(8, BELLS_OFF_BEAT, quiet), r"\pp"))

    # The second time: loud, with the chase theme in a major key.
    block.add("tpt1 tpt2 hn1 hn2 hn3 hn4 vc va", 2, dyn(WARM, r"\f\espr"))
    block.add("vn1:1 vn2:1 fl1:2 fl2:2 ob1:1 ob2:1", 2, first(SONG_TOGETHER, r"\f", note=True))
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


def _calls(work: Work) -> None:
    """Bars 425 to 436: many calls, each at its own speed. They come together.

    Each call is the motto in its light form (D, E, A). The strings hold
    the same three notes as a chord of fifths.
    """
    structure = work.structure
    s = work.section(12, 4, 4)
    structure.mark(s.bar(1), "FF")
    structure.tempo(s.bar(1), 1, 66, "Poco più mosso")
    block = Block(s, rests(4, 4, 9), rests(4, 4, 3))

    call = r"d'8-> e'8-> a'4->"
    levels = [r"\p", r"\p", r"\mp", r"\mp", r"\mf", r"\mf", r"\f", r"\f", r"\f"]
    # For each group of players: the first call (in quarter notes from the
    # start), the time between two calls, and the octave.
    groups = [
        ("hn1", 0.0, 5.0, 0),
        ("tpt1", 2.0, 7.0, 1),
        ("tbn1", 5.0, 6.0, -1),
        ("cl1", 8.0, 4.5, 1),
        ("ob1", 10.5, 5.5, 1),
        ("fl1", 12.0, 6.5, 2),
        ("hn3", 14.0, 5.5, 0),
        ("tpt2", 16.5, 6.0, 0),
        ("tbn2", 18.0, 5.0, -1),
        ("cl2", 19.5, 4.0, 0),
        ("ob2", 21.0, 4.5, 1),
        ("fl2", 22.5, 5.0, 2),
        ("hn2", 24.0, 4.0, 0),
        ("hn4", 25.0, 3.5, -1),
        ("tpt3", 26.5, 3.0, 0),
        ("bn1", 27.0, 3.5, -1),
        ("fl3", 28.5, 3.0, 2),
        ("perc2", 29.0, 2.5, 2),
    ]
    together = (
        r"A8->\ff B8-> C4-> A8-> B8-> C4-> | A8-> B8-> C4-> A8-> B8-> C4-> | "
        r"A4->\fff B4-> C2-> |"
    )
    for player, start, period, shift in groups:
        events = {}
        position = start
        while position < 36.0 - 1.9:
            bar = int(position // 4)
            figure = tr(call, 12 * shift) if shift else call
            events[(bar + 1, position - 4 * bar + 1)] = first(figure, levels[bar], note=True)
            position += period
        block.add(player, 1, scatter(9, 4, 4, events))
        chord = tr(r"<d' e' a'>1", 12 * shift) if shift else r"<d' e' a'>1"
        block.add(player, 2, fill(chord, together))
    extra = "hn5 hn6 btbn:-1 tuba:-2 bn2:-1 bn3:-2 cbcl:-2 cimb.rh mand:1 acc.rh pno.rh:1 pno.lh:-1"
    block.add(extra, 2, fill(r"<d' e' a'>1", together))

    # The chord of fifths (D, A, E) in the strings: it grows through the section.
    grow = r"X1:32\pp\< ~ | " + r"X1:32 ~ | " * 7 + r"X1:32\f |"
    last = r"X1:32\ff\< ~ | X1:32 ~ | X1:32\fff |"
    for player, chord in [("vn1", "e'' a''"), ("vn2", "a' e''"), ("va", "d' a'"),
                          ("vc", "d a"), ("cb", "d,")]:  # fmt: skip
        letter = "X" if " " in chord else "A"
        block.add(player, 1, fill(f"<{chord}>1", grow.replace("X", letter)))
        block.add(player, 2, fill(f"<{chord}>1", last.replace("X", letter)))
    block.add("timp", 1, r"d,1:32\pp\< ~ | " + r"d,1:32 ~ | " * 7 + r"d,1:32\f |")
    block.add("timp", 2, r"d,1:32\ff\< ~ | d,1:32 ~ | d,1:32\fff |")
    block.add("perc1", 2, r"c'1:32\p\< ~ | c'1:32 ~ | c'1:32\ff |")
    block.add("perc3", 2, r"R1 | c'1:32\mf\< ~ | c'1:32\fff |")
    block.close()


def _last_statement(work: Work) -> None:
    """Bars 437 to 457: the chorale in D major, and the last chord."""
    structure = work.structure
    s = work.section(21, 4, 4)
    structure.mark(s.bar(1), "GG")
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
    block.add("perc1", 1, r"""\switch "tam-tams" c'1\fff\lv | R1*7 | c'1\lv | R1*2 |""")
    block.add("perc3", 1, r"c'4\fff r r2 | R1*3 | c'4 r r2 | R1*3 | c'4 r r2 | R1 | c'4 r r2 |")
    block.start("perc4", r'\switch "glockenspiel"')

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
    block.add("perc1", 2, r"c'1\fff\lv | R1*3 | c'1\lv | R1*3 | c'2.\lv r4 | c'1\lv\fermata |")
    block.add("perc3", 2, r"c'4\fff r r2 | R1*3 | c'1:32 ~ | c'1:32 ~ | c'1:32 ~ | c'1:32 | "
              r"c'2. r4 | c'1\fermata |")  # fmt: skip
    block.close()
