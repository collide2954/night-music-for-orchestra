"""Part 2: agitation and development, a chase in uneven metres, and the first climax.

Material of this part:

- The agitated theme: the motto (D, E-flat, A-flat) as leaps, after a rest on
  the strong beat. It comes three times, each time a minor third higher
  (D, F, A-flat): the keys before the turn move by minor thirds.
- The chorale of part 1, now loud, in the full brass.
- The song theme in F: the long song of part 1 in a regular metre.

Style profile: "Transfigured", before the turn.
"""

from __future__ import annotations

from ..compose.tools import (
    Block,
    bars,
    double,
    dyn,
    figure,
    fill,
    first,
    invert,
    lines,
    octave,
    plain,
    put,
    rests,
    times,
    tr,
)
from ..notation.work import Work

# The agitated theme (4 bars), on D.
AGITATED = r"""
    r8 d8\mf\<( es4 ~ es8 as8 g4)\! |
    r8 fis8\<( g4 ~ g8 cis'8 b4)\! |
    r8 bes8\f( a4 ~ a8 es'8\> d'4 ~ |
    d'4)\! r8 cis'8\mf( d'4. es'8) |
"""

# Soft chords after each beat (4 bars), for the D form of the theme.
PULSE = r"""
    r8 <a d'>8-.\p r8 <a d'>8-. r8 <a d'>8-. r8 <a d'>8-. |
    r8 <b d'>8-. r8 <b d'>8-. r8 <gis d'>8-. r8 <gis d'>8-. |
    r8 <bes d'>8-. r8 <bes d'>8-. r8 <bes f'>8-. r8 <bes f'>8-. |
    r8 <g des'>8-. r8 <g des'>8-. r8 <bes des'>8-. r8 <bes des'>8-. |
"""

# The bass (4 bars), plucked, for the D form of the theme.
BASS = r"""
    d,4\mf\pizz r d,4 r | d,4 r d,4 r | d,4 r bes,,4 r | es,4 r es,4 r |
"""

# The song theme (8 bars), in F: the long song of part 1 in a regular metre.
SONG = r"""
    c''2\p\dolce( bes'4 as'4 | g'2. f'4) | ges'2( f'4 es'4 | f'1) |
    c''2\<( des''4 es''4 | f''2.\mf\> es''4 | des''2 c''4 bes'4 | c''1\p) |
"""

# The walking theme of part 1 in its loud form (4 bars).
WALKING_LOUD = r"""
    d'4.\ff->( es'8 f'4. g'8 | as'2.) r4 | as'4.->( g'8 f'4. es'8 | d'2.) r4 |
"""


# The chase. The metre is 7/8 with the beats 2 + 2 + 3 (a Bulgarian rhythm).
# All material is from the scale of alternate semitones and tones on B
# (B, C, D, E-flat, F, F-sharp, G-sharp, A). This scale contains the motto.

# One bar of the ostinato, on B: the notes of the motto (B, C, F).
OSTINATO = r"b,8 f c f b, c f |"

# One plucked bass note at the start of each beat.
STEPS = r"b,,8 r c,8 r b,,8 r4 |"

# The chase theme (4 bars): the walking theme, fast. Each bar is a minor third higher.
CHASE = r"""
    b8-> c' d'-> es' f'-> es' d' |
    d'8-> es' f'-> fis' gis'-> fis' f' |
    f'8-> fis' gis'-> a' b'-> a' gis' |
    a'8-> gis' fis'-> f' es'4.-> |
"""

# The answer (4 bars): the theme goes down.
ANSWER = r"""
    b'8-> a' gis'-> fis' f'-> fis' gis' |
    gis'8-> fis' f'-> es' d'-> es' f' |
    f'8-> es' d'-> c' b-> c' d' |
    es'8-> d' c'-> b c'8-> b4-> |
"""

# One bar of the theme, for the short calls.
CALL = r"b8-> c' d' es' f' es' d' |"

# The theme in changing metres (7/8, 7/8, 9/8, 5/8).
MIXED = r"""
    b8-> c' d'-> es' f'-> es' d' |
    d'8-> es' f'-> fis' gis'-> fis' f' |
    f'8-> fis' gis'-> a' b'-> a' gis'-> a' b' |
    b'8-> gis' f'4.-> |
"""
MIXED_METRES = [(7, 8, (2, 2, 3)), (7, 8, (2, 2, 3)), (9, 8, (2, 2, 2, 3)), (5, 8, (2, 3))]
MIXED_REST = r"R1*7/8 | R1*7/8 | R1*9/8 | R1*5/8 |"
MIXED_OSTINATO = OSTINATO * 2 + r"b,8 f c f b, f b, c f | b,8 f b, c f |"
MIXED_STEPS = STEPS * 2 + r"b,,8 r c,8 r b,,8 r b,,8 r4 | b,,8 r b,,8 r4 |"
MIXED_BLOCKS = (
    r"c'8 r d'8 r c'8 r d'8 | c'8 r d'8 r c'8 r d'8 | "
    r"c'8 r d'8 r c'8 r c'8 r d'8 | c'8 r c'8 r d'8 |"
)
MIXED_STABS = (
    r"r4 r4 <b c' f'>8-.-> r <b c' f'>8-. | r4 r4 <b c' f'>8-.-> r <b c' f'>8-. | "
    r"r4 r4 r4 <b c' f'>8-.-> r <b c' f'>8-. | r4 <b c' f'>8-.-> r <b c' f'>8-. |"
)

# The chord of the hammer strokes, in its D form: the motto (D, E-flat, A-flat)
# above the diminished seventh chord on D.
HAMMER_CHORD = r"<d, as, d f b es' as' d''>1"

# Short chords on the long beat (1 bar), for the horns.
STAB = r"r4 r4 <f b c' f'>8-.-> r <f b c' f'>8-. |"


def write(work: Work) -> None:
    _agitation(work)
    _song(work)
    _chase_start(work)
    _chase_episode(work)
    _chase_end(work)
    _broad_motto(work)
    _song_returns(work)
    _ascent(work)
    _first_climax(work)
    _collapse(work)


def _agitation(work: Work) -> None:
    structure = work.structure

    # ------------------------------------------------- mark D: three waves
    s = work.section(12, 4, 4)
    structure.mark(s.bar(1), "D")
    structure.tempo(s.bar(1), 1, 66, "Poco più mosso, inquieto")

    theme = first(AGITATED, r"\senzasord")
    s.write("va", theme + tr(AGITATED, 3) + tr(PULSE, 6))
    s.write("vc", theme + octave(tr(AGITATED, 3), -1) + octave(tr(AGITATED, 6), -1))
    s.write("vn2", first(PULSE, r"\senzasord") + octave(tr(AGITATED, 3), 1) + tr(AGITATED, 6))
    s.write("vn1", r"R1*4\senzasord | " + tr(PULSE, 3) + octave(tr(AGITATED, 6), 1))
    s.write("cb", first(BASS, r"\senzasord") + tr(BASS, 3) + tr(BASS, 6))
    s.write(
        "timp",
        r"""
        d,4\pp r d,4 r | d,4 r d,4 r | d,4 r d,4 r | d,4 r d,4 r |
        f,4\p r f,4 r | f,4 r f,4 r | f,4 r f,4 r | f,4 r f,4 r |
        as,4\mp\< r as,4 r | as,4 r as,4 r | as,4 r as,4 r | a,1:32\f\< |
    """,
    )
    s.write(
        "hn1",
        r"""
        R1*4 | c'1\pp\senzasord( | d'1 | des'1 | des'1) |
        es'1\p\<( | f'1 | e'1\mf | f'1\f\<) |
    """,
    )
    s.write(
        "hn2",
        r"""
        R1*4 | as1\pp\senzasord( | as1 | as1 | bes1) |
        ces'1\p\<( | ces'1 | b1\mf | cis'1\f\<) |
    """,
    )
    s.write(
        "hn3",
        r"""
        R1*8 | as1\p\senzasord\<( | as1 | gis1\mf | g1\f\<) |
    """,
    )
    s.write(
        "hn4",
        r"""
        R1*8 | es1\p\senzasord\<( | d1 | e1\mf | a,1\f\<) |
    """,
    )
    s.write(
        "bn1",
        r"""
        R1*4 | f1\p( | f1 | f1 | fes1) | es1\mp\<( | d1 | e1 | f1\f\<) |
    """,
    )
    s.write(
        "bn2",
        r"""
        R1*4 | f,1\p( | f,1 | des1 | ges,1) | as,1\mp\<( | as,1 | e,1 | a,1\f\<) |
    """,
    )
    s.write("fl2", r"""\switch "flute" R1*12 |""")
    s.write("bn3", r"""\switch "contrabassoon" R1*12 |""")
    s.write("tpt1", r"""R1*11 | r2 a'2\mf\< |""")
    s.write("tpt2", r"""R1*11 | r2 f'2\mf\< |""")
    s.write("tpt3", r"""R1*11 | r2 cis'2\mf\< |""")
    s.write("perc4", r"""\switch "suspended cymbals" R1*11 | c'1:32\p\< |""")
    s.close()

    # ---------------------------------------------- mark E, bars 1 to 6: the first crest
    s = work.section(6, 4, 4)
    structure.mark(s.bar(1), "E")

    s.write("hn1", r"""d'1\ff->( | es'1 | as'1 | g'1) | e'1\p\> | d'1\pp |""")
    s.write("hn2", r"""a1\ff->( | bes1 | des'1 | cis'1) | bes1\p\> | a1\pp |""")
    s.write("hn3", r"""f1\ff->( | ges1 | f1 | f1) | gis1\p\> | a1\pp |""")
    s.write("hn4", r"""d1\ff->( | c1 | bes,1 | a,1) | bes,1\p\> | d1\pp |""")
    s.write("hn5", r"""d'1\ff->\senzasord( | es'1 | as'1 | g'1) | R1*2 |""")
    s.write("hn6", r"""f1\ff->\senzasord( | ges1 | f1 | f1) | R1*2 |""")
    s.write("tpt1", r"""d''1\ff->( | es''1 | as''1 | g''1) | R1*2 |""")
    s.write("tpt2", r"""a'1\ff->( | bes'1 | des''1 | cis''1) | R1*2 |""")
    s.write("tpt3", r"""f'1\ff->( | ges'1 | f'1 | f'1) | R1*2 |""")
    s.write("tbn1", r"""a1\ff->( | bes1 | des'1 | cis'1) | R1*2 |""")
    s.write("tbn2", r"""f1\ff->( | ges1 | f1 | f1) | R1*2 |""")
    s.write("btbn", r"""d1\ff->( | c1 | bes,1 | a,1) | R1*2 |""")
    s.write("tuba", r"""d,1\ff->( | c,1 | bes,,1 | a,,1) | R1*2 |""")
    s.write("fl1", r"""d'''1\ff( | es'''1 | as'''1 | g'''1) | R1*2 |""")
    s.write("fl2", r"""a''1\ff( | bes''1 | des'''1 | cis'''1) | R1*2 |""")
    s.write("ob1", r"""d''1\ff( | es''1 | as''1 | g''1) | R1*2 |""")
    s.write("ob2", r"""a'1\ff( | bes'1 | des''1 | cis''1) | R1*2 |""")
    s.write("cl1", r"""f''1\ff( | ges''1 | f''1 | f''1) | R1*2 |""")
    s.write("cl2", r"""d''1\ff( | c''1 | bes'1 | a'1) | R1*2 |""")
    s.write("bn1", r"""d1\ff( | c1 | bes,1 | a,1) | R1*2 |""")
    s.write("bn2", r"""d1\ff( | c1 | bes,1 | a,1) | R1*2 |""")
    put(s, "bn3 cbcl", r"""d,1\ff( | c,1 | bes,,1 | a,,1) | R1*2 |""")
    s.write(
        "vn1",
        r"""
        d'''1:32\ff | es'''1:32 | as'''1:32 | g'''1:32 | <gis'' e'''>1\p\> | <a'' d'''>1\pp |
    """,
    )
    s.write(
        "vn2",
        r"""
        a''1:32\ff | bes''1:32 | des'''1:32 | cis'''1:32 | <bes' d''>1\p\> | <a' d''>1\pp |
    """,
    )
    s.write("va", WALKING_LOUD + r"""<bes e'>1\p\> | <a d'>1\pp |""")
    s.write("vc", octave(WALKING_LOUD, -1) + r"""<e gis>1\p\> | <d a>1\pp |""")
    s.write(
        "cb",
        first(octave(WALKING_LOUD, -2), r"\arco", note=True) + r"""d,1\p\> ~ | d,1\pp |""",
    )
    s.write(
        "timp", r"""d,1:32\ff ~ | d,1:32 ~ | d,1:32 ~ | d,1:32\> | d,4\p r r2 | d,4\pp r r2 |"""
    )
    s.write("perc1", r"""c'1\ff\lv | R1*5 |""")
    s.write("perc2", r"""\switch "crash cymbals" c'4\ff\lv r4 r2 | R1*5 |""")
    s.write("perc3", r"""\switch "bass drum" c'4\ff r4 r2 | R1 | c'4\f r4 r2 | R1*3 |""")
    s.close()

    # -------------------------------------------- mark E, bars 7 to 12: the way to the song
    s = work.section(6, 4, 4)
    structure.change(s.bar(1), 1, "poco rit.")

    s.write(
        "cl1",
        r"""
        r2 c''2\p\espr( ~ | c''4. b'8 as'4 g'8 f'8) | r2 des''2( ~ |
        des''4. c''8 b'4 as'8 g'8 | as'2. g'4 | f'1) |
    """,
    )
    s.write(
        "va",
        r"""
        <des' f'>1\pp( | <c' f'>1) | <des' f'>1( | <c' f'>1) | <des' e'>1( | <c' f'>1) |
    """,
    )
    s.write(
        "vc",
        r"""
        <f bes>1\pp( | <f c'>1) | <ges bes>1( | <f c'>1) | <g bes>1( | <f c'>1) |
    """,
    )
    s.write("cb", r"""f,1\pp ~ | f,1 ~ | f,1 ~ | f,1 ~ | f,1 ~ | f,1 |""")
    s.write("timp", r"""f,4\ppp r r2 | R1 | f,4 r r2 | R1 | f,4 r r2 | R1 |""")
    s.close()


def _song(work: Work) -> None:
    structure = work.structure

    # --------------------------------------------- mark F, bars 1 to 8: the song theme
    s = work.section(8, 4, 4)
    structure.mark(s.bar(1), "F")
    structure.tempo(s.bar(1), 1, 60, "Un poco più tranquillo")

    song = SONG
    waves = r"""
        f8\pp( c' as c' f c' as c') | f8( des' as des' f des' as des') |
        ges8( des' bes des' ges des' bes des') | f8( c' f c' f c' f c') |
        es8( c' as c' es c' as c') | f8( des' as des' f des' as des') |
        f8( des' bes des') ges8( des' bes des') | f8( c' a c' f c' a c') |
    """
    fifths = r"""
        <f, c>2\pp <f, c>2 | <des, as,>2 <des, as,>2 | <ges, des>2 <ges, des>2 | <f, c>1 |
        <as, es>2 <as, es>2 | <des, as,>2 <des, as,>2 | <bes, f>2 <ges, des>2 | <f, c>1 |
    """
    plucked = r"""
        f,4\p\pizz r4 r2 | des,4 r4 r2 | ges,4 r4 r2 | f,4 r4 r2 |
        as,4 r4 r2 | des,4 r4 r2 | bes,4 r ges,4 r | f,4 r4 r2 |
    """
    harp = r"""
        <c' f' as'>4\p\arpeggio r4 r2 | <des' f' as'>4\arpeggio r4 r2 |
        <des' ges' bes'>4\arpeggio r4 r2 | <c' f' c''>4\arpeggio r4 r2 |
        <c' es' as'>4\arpeggio r4 r2 | <des' f' as'>4\arpeggio r4 r2 |
        <des' f' bes'>4\arpeggio r4 <des' ges' bes'>4\arpeggio r4 | <c' f' a'>4\arpeggio r4 r2 |
    """
    s.write("cl1", song)
    s.write(
        "vn1",
        r"""R1*4 | c''2\pp\<( des''4 es''4 | f''2.\mp\> es''4 | des''2 c''4 bes'4 | c''1\pp) |""",
    )
    s.write("va", waves)
    s.write("vc", fifths)
    s.write("cb", plucked)
    s.write("harp.rh", harp)
    s.close()

    # ------------------------------------- mark F, bars 9 to 16: the song again, then unrest
    s = work.section(8, 4, 4)
    structure.change(s.bar(5), 1, "stringendo molto")

    first_half = r"""c''2\p\dolce( bes'4 as'4 | g'2. f'4) | ges'2( f'4 es'4 | f'1) |"""
    s.write("ob1", first_half + r" R1*4 |")
    s.write("fl1", octave(first_half, 1) + r" R1*4 |")
    s.write(
        "vn1",
        first_half
        + r"""
        f''1:32\p\< ~ | f''1:32 | ges''1:32\mf\< ~ | ges''1:32\f |
    """,
    )
    s.write(
        "vn2",
        r"""
        R1*4 | c''1:32\p\< ~ | c''1:32 | des''1:32\mf\< ~ | des''1:32\f |
    """,
    )
    s.write(
        "va",
        r"""
        f8\pp( c' as c' f c' as c') | f8( des' as des' f des' as des') |
        ges8( des' bes des' ges des' bes des') | f8( c' f c' f c' f c') |
        as1:32\p\< ~ | as1:32 | bes1:32\mf\< ~ | bes1:32\f |
    """,
    )
    s.write(
        "vc",
        r"""
        <f, c>2\pp <f, c>2 | <des, as,>2 <des, as,>2 | <ges, des>2 <ges, des>2 | <f, c>1 |
    """
        + octave(
            tr(
                r"""
        r8 d8\mp\<( es4 ~ es8 as8 g4)\! | r8 fis8\<( g4 ~ g8 cis'8 b4)\! |
        r8 d8\mf\<( es4 ~ es8 as8 g4)\! | r8 fis8\<( g4 ~ g8 cis'8 b4\f) |
    """,
                3,
            ),
            -1,
        ),
    )
    s.write(
        "bn1",
        r"R1*4 |"
        + octave(
            tr(
                r"""
        r8 d8\mp\<( es4 ~ es8 as8 g4)\! | r8 fis8\<( g4 ~ g8 cis'8 b4)\! |
        r8 d8\mf\<( es4 ~ es8 as8 g4)\! | r8 fis8\<( g4 ~ g8 cis'8 b4\f) |
    """,
                3,
            ),
            -1,
        ),
    )
    s.write(
        "cb",
        r"""
        f,4\p r4 r2 | des,4 r4 r2 | ges,4 r4 r2 | f,4 r4 r2 |
        f,1:32\p\arco\< ~ | f,1:32 | f,1:32\mf\< ~ | f,1:32\f |
    """,
    )
    s.write(
        "harp.rh",
        r"""
        <c' f' as'>4\p\arpeggio r4 r2 | <des' f' as'>4\arpeggio r4 r2 |
        <des' ges' bes'>4\arpeggio r4 r2 | <c' f' c''>4\arpeggio r4 r2 | R1*4 |
    """,
    )
    s.write("timp", r"""R1*4 | f,1:32\pp\< ~ | f,1:32 | f,1:32\mp\< ~ | f,1:32\f |""")
    s.close()


def _chase_start(work: Work) -> None:
    structure = work.structure
    seven = (7, 8, (2, 2, 3))

    # ------------------------------------------- mark G, bars 1 to 4: the ostinato alone
    s = work.section(4, *seven)
    structure.mark(s.bar(1), "G")
    structure.tempo(s.bar(1), 1, 276, "Presto, alla bulgarese", unit="8")

    # The cellos start the chase alone. The owner of the project heard no sound here.
    # A measurement showed the cause: the short notes of one string section at pp or mp
    # are 20 dB softer than the loud passage before them. Thus the ostinato is mf.
    s.write("vc", first(times(OSTINATO, 4), r"\mf\spicc", note=True))
    s.write("bn1", rests(7, 8, 2) + dyn(times(OSTINATO, 2), r"\mf\staccato"))
    s.write("cb", rests(7, 8, 2) + first(times(STEPS, 2), r"\mf\pizz", note=True))
    s.write(
        "perc4",
        r"""\switch "wood blocks" """ + rests(7, 8, 2) + r"c'8\mf r d'8 r c'8 r d'8 | "
        r"c'8 r d'8 r c'8 r d'8 |",
    )
    s.write("perc3", r"""\switch "frame drum" """ + rests(7, 8, 4))
    s.write("perc2", r"""\switch "xylophone" """ + rests(7, 8, 4))
    s.write("cl2", r"""\switch "clarinet in E-flat" """ + rests(7, 8, 4))
    s.write("fl3", r"""\switch "piccolo" """ + rests(7, 8, 4))
    s.close()

    # ------------------------------------- mark G, bars 5 to 12: the theme and its answer, on B
    s = work.section(8, *seven)
    put(s, "cl1 va", dyn(CHASE, r"\mf") + rests(7, 8, 4))
    put(s, "ob1 ob2", rests(7, 8, 4) + dyn(ANSWER, r"\mf"))
    s.write("vn2", rests(7, 8, 4) + first(dyn(ANSWER, r"\mf"), r"\spicc", note=True))
    s.write("vc", dyn(times(OSTINATO, 8), r"\mf"))
    put(s, "bn1 cl3", dyn(times(OSTINATO, 8), r"\mp"))
    s.write("cb", dyn(times(STEPS, 8), r"\mf"))
    s.write("perc4", times(r"c'8\mp r d'8 r c'8 r d'8 |", 8))
    stabs = lines(times(rests(7, 8) + dyn(STAB, r"\mf"), 4))
    for player, line in zip(["hn4", "hn3", "hn2", "hn1"], stabs, strict=True):
        s.write(player, first(line, r"\stopped", note=True))
    s.close()

    # ---------------------------------------- mark H, bars 1 to 8: a minor third higher, on D
    s = work.section(8, *seven)
    structure.mark(s.bar(1), "H")
    theme, answer = tr(CHASE, 3), tr(ANSWER, 3)
    put(s, "vn1:1 fl1:1 fl2:1 vn2", dyn(theme, r"\f") + rests(7, 8, 4))
    put(s, "tpt1 tpt2 perc2:1 mand:1 va", rests(7, 8, 4) + dyn(answer, r"\f"))
    ostinato = tr(OSTINATO, 3)
    put(s, "vc bn1 bn2 cl3 cimb.lh", dyn(times(ostinato, 8), r"\mf"))
    s.write("cb", dyn(times(tr(STEPS, 3), 8), r"\mf"))
    s.write("pno.lh", times(r"<d,, d,>8-.\mf r <es,, es,>8-. r <d,, d,>8-. r4 |", 8))
    s.write("perc4", times(r"c'8\mf r d'8 r c'8 r d'8 |", 8))
    s.write("perc3", times(r"c'8\mf r4 r8 c'8 r c'8 |", 8))
    s.write("timp", times(r"d,8->\f r r4 r4. | " + rests(7, 8), 4))
    stabs = lines(times(dyn(tr(STAB, 3), r"\f") + rests(7, 8), 4))
    for player, line in zip(["hn4", "hn3", "hn2", "hn1"], stabs, strict=True):
        s.write(player, line)
    s.close()


def _chase_episode(work: Work) -> None:
    structure = work.structure
    seven = (7, 8, (2, 2, 3))
    rest = rests(7, 8)

    # -------------------------------------- mark H, bars 9 to 16: the full statement, on F
    s = work.section(8, *seven)
    theme, answer = tr(CHASE, 6), tr(ANSWER, 6)
    high_ostinato = dyn(times(tr(OSTINATO, 18), 4), r"\mf")
    put(s, "vn1:1 vn2", dyn(theme, r"\ff") + high_ostinato)
    put(s, "fl1:1 fl2:1 fl3:1 cl2:1 mand:1 ob1 ob2 cl1", dyn(theme, r"\ff") + rests(7, 8, 4))
    s.write("va", dyn(theme, r"\ff") + dyn(answer, r"\ff"))
    put(s, "tpt1 tpt2 tpt3 perc2:1", rests(7, 8, 4) + dyn(answer, r"\ff"))
    put(s, "vc bn1 bn2 cl3 cimb.lh", dyn(times(tr(OSTINATO, -6), 8), r"\f"))
    s.write("cb", dyn(times(tr(STEPS, -6), 8), r"\f"))
    s.write("pno.lh", dyn(times(double(tr(STEPS, -6), 1), 8), r"\f"))
    s.write("perc4", times(r"c'8\f r d'8 r c'8 r d'8 |", 8))
    s.write("perc3", times(r"c'8\f r4 r8 c'8 r c'8 |", 8))
    s.write("timp", times(r"f,8->\f r r4 r4. | " + rest, 4))
    s.write("perc1", r"""\switch "suspended cymbals" """ + rests(7, 8, 7) + r"c'2..:32\p\< |")
    stabs = lines(times(dyn(tr(STAB, 6), r"\ff"), 4))
    for player, line in zip(["hn4", "hn3", "hn2", "hn1"], stabs, strict=True):
        s.write(player, line + octave(dyn(answer, r"\ff"), -1))
    low_stabs = lines(times(dyn(r"r4 r4 <f, b, ges>8-.-> r <f, b, ges>8-. |", r"\ff"), 4))
    for player, line in zip(["btbn", "tbn2", "tbn1"], low_stabs, strict=True):
        s.write(player, line + rests(7, 8, 4))
    s.close()

    # ------------------------------ mark J: sudden silence; calls in the dark, on E
    s = work.section(16, *seven)
    structure.mark(s.bar(1), "J")
    call = tr(CALL, 5)
    high_call = octave(call, 1)
    call_g, call_b = tr(call, 3), tr(call, 6)
    s.write("va", first(times(tr(OSTINATO, 5), 16), r"\pp\sulpont", note=True))
    s.write("vc", first(times(r"e,8 r f,8 r e,8 r4 |", 16), r"\pp\pizz", note=True))
    s.write("mand", rests(7, 8, 4) + dyn(times(tr(OSTINATO, 17), 12), r"\p"))
    s.write("cimb.lh", r"e2..:32\pp ~ | " + times(r"e2..:32 ~ |", 14) + r" e2..:32 |")
    s.write("harp.lh", times(r"<e, e>8\p r r4 r4. | " + rest, 8))
    s.write("perc4", times(r"c'8\pp r4 r4 d'8 r8 |", 16))
    s.write(
        "fl3",
        bars(
            16,
            rest,
            {3: dyn(high_call, r"\pp"), 11: dyn(high_call, r"\p"), 15: dyn(high_call, r"\mf")},
        ),
    )
    s.write(
        "cl2",
        bars(
            16,
            rest,
            {
                5: dyn(call_g, r"\pp"),
                12: dyn(call_g, r"\p"),
                16: dyn(call_g, r"\mf"),
            },
        ),
    )
    s.write(
        "perc2",
        bars(
            16,
            rest,
            {
                7: dyn(call_b, r"\pp"),
                13: dyn(call_b, r"\mp"),
                16: dyn(call_b, r"\mf"),
            },
        ),
    )
    s.write("cel.rh", bars(16, rest, {9: dyn(tr(call, 9), r"\p")}))
    put(s, "fl1 fl2", bars(16, rest, {14: dyn(tr(call, 9), r"\mp")}))
    put(s, "ob1 ob2", bars(16, rest, {15: dyn(tr(call, 12), r"\mf")}))
    s.write("tpt1", bars(16, rest, {16: dyn(call_g, r"\mf\<")}))
    swell = r"X2..:32\pp\sulpont\< ~ | " + r" ~ | ".join([r"X2..:32"] * 7) + r"\mf |"
    s.write("vn1", rests(7, 8, 8) + fill(r"<e'' f''>1", swell))
    s.write("vn2", rests(7, 8, 8) + fill(r"<bes' b'>1", swell))
    s.write("timp", rests(7, 8, 14) + r"e,2..:32\pp\< ~ | e,2..:32\mf |")
    s.write("perc3", r"""\switch "bass drum" """ + rests(7, 8, 16))
    s.close()


def _chase_end(work: Work) -> None:
    structure = work.structure
    seven = (7, 8, (2, 2, 3))
    rest = rests(7, 8)

    # ------------------------------- mark K: the theme in changing metres, on C
    s = work.section_of(MIXED_METRES * 2)
    structure.mark(s.bar(1), "K")
    theme, higher = tr(MIXED, 1), tr(MIXED, 4)
    put(s, "tpt1 tpt2 cl1 hn1:-1 hn2:-1 hn3:-1 hn4:-1", dyn(theme, r"\f") + MIXED_REST)
    s.write("va", first(dyn(theme, r"\f"), r"\ord", note=True) + dyn(higher, r"\ff"))
    s.write("vn1", MIXED_REST + first(dyn(octave(higher, 1), r"\ff"), r"\ord", note=True))
    s.write("vn2", MIXED_REST + first(dyn(higher, r"\ff"), r"\ord", note=True))
    put(s, "fl1:1 fl2:1 fl3:1 cl2:1 perc2:1 ob1 ob2", MIXED_REST + dyn(higher, r"\ff"))
    ostinato = dyn(tr(MIXED_OSTINATO, 1), r"\f") + dyn(tr(MIXED_OSTINATO, 4), r"\ff")
    put(s, "bn1 bn2 cl3 cimb.lh", ostinato)
    s.write("vc", first(ostinato, r"\arco\spicc", note=True))
    steps = dyn(tr(MIXED_STEPS, 1), r"\f") + dyn(tr(MIXED_STEPS, 4), r"\ff")
    s.write("cb", steps)
    s.write("pno.lh", double(steps))
    s.write("perc4", dyn(MIXED_BLOCKS, r"\f") + MIXED_BLOCKS)
    s.write("perc3", times(r"c'8->\f r r4 r4. | R1*7/8 | R1*9/8 | R1*5/8 |", 2))
    stabs = lines(dyn(tr(MIXED_STABS, 4), r"\ff"))
    for player, line in zip(["tbn2", "tbn1", "tpt3"], stabs, strict=True):
        s.write(player, MIXED_REST + line)
    s.close()

    # ---------------------------------- mark L: three voices, one bar apart, on F
    s = work.section(12, *seven)
    structure.mark(s.bar(1), "L")
    call = tr(CALL, 6)  # the call on F (above middle C)

    def voice(first_bar: int, shift: int) -> str:
        """Return the voice that starts in `first_bar`. Each bar is a minor third higher."""
        text = rests(7, 8, first_bar - 1) if first_bar > 1 else ""
        count = 12 - first_bar + 1
        for number in range(count):
            bar = tr(call, shift + 3 * (number % 4))
            if number == 0:
                bar = dyn(bar, r"\f")
            elif number == count - 4:
                bar = first(bar, r"\<", note=True)
            elif number == count - 1:
                bar = first(bar, r"\ff", note=True)
            text += bar + " "
        return text

    put(s, "vc bn1 bn2 cl3 tbn1 tbn2 cb:-1 btbn:-1 pno.rh pno.lh:-1", voice(1, -24))
    put(s, "va hn1 hn2 hn3 hn4 cl1", voice(2, -12))
    put(s, "vn2 ob1 ob2 tpt1 tpt2 tpt3 vn1:1 fl1:1 fl2:1 fl3:1 cl2:1 perc2:1", voice(3, 0))
    s.write("timp", times(r"f,8->\f r r4 r4. |", 12))
    s.write("perc3", times(r"c'8->\f r r4 r4. | " + rest, 6))
    s.write("perc4", times(r"c'8\f r d'8 r c'8 r d'8 |", 12))
    s.write("perc1", rests(7, 8, 10) + r"c'2..:32\p\< ~ | c'2..:32\f |")
    s.close()

    # ------------------------------------------------ the heavy section (32 bars)
    # The low instruments hammer a riff of the motto notes. The riff has four
    # forms of two bars, and each phrase has the forms in a different sequence:
    # no unit of two bars comes two times. All other parts come from the riff:
    # - The high strings, the horns, and the piano play where the riff has a rest.
    #   Together they fill all eighth notes.
    # - The taiko has the rhythm of the riff. The bass drum and the timpani have
    #   its accents. The snare drum and the tom-toms play in its rests.
    # Each phrase of 8 bars is a minor third higher. In phrases 3 and 4 the
    # leaps of the riff become larger. All notes are in the scale of the chase.
    s = work.section(32, *seven)
    structure.mark(s.bar(1), "M")
    structure.tempo(s.bar(1), 1, 276, "Pesante e feroce", unit="8")
    eight = rests(7, 8, 8)
    block = Block(s, eight, eight, eight, eight)

    # R = the root. L, M, H = the low, the middle, and the high note of the cell.
    # ">" = an accent. "." = a rest.
    forms = {
        "A": "R> . R> . H> M L | R> R . L> . R> H",
        "B": "R> R . H> . M> L | R> . L R> . H> M",
        "C": "R> . H R> . L M> | . R> R . H> . R>",
        "D": "R> L M H> . R> . | H> M L R> R . R>",
    }
    orders = ["ABCD", "BDAC", "CADB", "DCBA"]
    cells = [
        {"R": "b,,", "L": "c,", "M": "es,", "H": "f,"},
        {"R": "b,,", "L": "c,", "M": "es,", "H": "f,"},
        {"R": "b,,", "L": "c,", "M": "f,", "H": "fis,"},
        {"R": "b,,", "L": "d,", "M": "fis,", "H": "gis,"},
    ]
    # The theme in long notes (8 bars), on F: the cell of the walking theme, four times.
    theme = r"""
        f4-> ges4-> as4.-> | a4-> b4-> a4.-> | as4-> a4-> b4.-> | c'4-> d'4-> c'4.-> |
        b4-> c'4-> d'4.-> | es'4-> f'4-> es'4.-> | d'4-> es'4-> f'4.-> | ges'4-> as'4-> ges'4.-> |
    """
    levels = [r"\f", r"\f", r"\ff", r"\ff"]
    roots = ["b,", "d", "f", "as,"]  # the notes of the timpani
    tom_notes = ["a", "c'", "e'", "c'"]
    for phrase in (1, 2, 3, 4):
        level, root, cell = levels[phrase - 1], roots[phrase - 1], cells[phrase - 1]
        shift = 3 * (phrase - 1)
        music_of: dict[str, list[str]] = {
            name: [] for name in ("low", "gaps", "taiko", "bass drum", "timp", "toms", "snare")
        }
        chords: dict[str, list[str]] = {name: [] for name in ("va", "vn2", "vn1", "pno", "one")}
        tom = 0
        for unit, letter in enumerate(orders[phrase - 1]):
            for bar_text in forms[letter].split("|"):
                marks = bar_text.split()
                riff = [
                    None if m == "." else (cell[m[0]], "->" if m.endswith(">") else "")
                    for m in marks
                ]
                music_of["low"].append(tr(figure(riff), shift))
                music_of["gaps"].append(figure([("X", "->") if m == "." else None for m in marks]))
                music_of["taiko"].append(
                    figure(
                        [
                            None if m == "." else ("c'", "->" if m.endswith(">") else "")
                            for m in marks
                        ]
                    )
                )
                # The bass drum: the accents of the root at the start of a beat group.
                beat = [
                    ("c'", "->") if m == "R>" and i in (0, 2, 4) else None
                    for i, m in enumerate(marks)
                ]
                music_of["bass drum"].append(figure(beat))
                music_of["timp"].append(
                    figure([(root, "->") if m == "R>" else None for m in marks])
                )
                # The tom-toms: the rests of the riff in the last beat group.
                # The snare drum: the other rests.
                toms: list[tuple[str, str] | None] = []
                snare: list[tuple[str, str] | None] = []
                for index, mark in enumerate(marks):
                    free = mark == "."
                    toms.append((tom_notes[tom % 4], "") if free and index >= 4 else None)
                    snare.append(("c'", "->") if free and index < 4 else None)
                    tom += 1 if free and index >= 4 else 0
                music_of["toms"].append(figure(toms))
                music_of["snare"].append(figure(snare))
            # The chords: a different position of the same notes in each second unit.
            lift = shift + (3 if unit % 2 else 0)
            gap_bars = " ".join(music_of["gaps"][-2:])
            chords["va"].append(fill(tr(r"<f b>1", lift), gap_bars))
            chords["vn2"].append(fill(tr(r"<d' gis'>1", lift), gap_bars))
            chords["vn1"].append(fill(tr(r"<b' f''>1", lift), gap_bars))
            chords["pno"].append(fill(tr(r"<f b d' gis'>1", lift), gap_bars))
        text = {name: " ".join(parts) for name, parts in music_of.items()}
        block.add(
            "cb tuba btbn bn3 cbcl cl3 vc:1 bn1:1 bn2:1 cimb.lh:1", phrase, text["low"], level
        )
        if phrase <= 2:
            # The trombones make the riff heavier, until they get the theme.
            block.add("tbn1:1 tbn2:1", phrase, text["low"], level)
        block.add("pno.lh", phrase, double(text["low"], -1), level)
        for player in ("va", "vn2", "vn1"):
            block.add(player, phrase, " ".join(chords[player]), level)
        block.add("pno.rh", phrase, " ".join(chords["pno"]), level)
        block.add("timp", phrase, text["timp"], level)
        block.add("perc3", phrase, text["bass drum"], level)
        block.add("perc6", phrase, text["taiko"], level)
        block.add("perc5", phrase, text["toms"], level)
        gaps = text["gaps"]
        if phrase >= 2:
            # The snare drum, with a roll in the last bar of the phrase.
            bars_of_snare = music_of["snare"][:7] + [r"c'2..:32\< |"]
            block.add("perc4", phrase, " ".join(bars_of_snare), level)
        if phrase in (2, 3):
            # The horns play with the high strings.
            block.spread("hn4 hn3 hn2 hn1", phrase, fill(r"<as b d' f'>1", gaps), level)
        if phrase == 3:
            block.spread("tpt3 tpt2 tpt1", phrase, fill(r"<as' b' d''>1", gaps), level)
        if phrase >= 3:
            note = r"<f''>1" if phrase == 3 else r"<as''>1"
            players = (
                "fl1:1 fl2:1 ob1 ob2 cl1 cl2"
                if phrase == 3
                else "fl1:1 fl2:1 fl3:1 ob1 ob2 cl1 cl2"
            )
            block.add(players, phrase, fill(note, gaps.replace("X", "A")), level)
    block.start("perc6", r'\switch "taiko"')
    block.start("perc5", r'\switch "tom-toms"')
    block.add("perc4", 1, r'\switch "snare drum" ' + eight)

    # The third phrase: the theme in the trombones.
    block.add("tbn1 tbn2", 3, theme, r"\ff")
    # The fourth phrase: the theme one octave higher in the trumpets. The horns
    # answer one bar later with the mirror form of the theme (a canon).
    block.add("tpt1:1 tpt2:1 tpt3:1 tbn1 tbn2 perc2:2", 4, theme, r"\ff")
    mirror = [bar.strip() for bar in invert(theme, "bes").split("|") if bar.strip()]
    block.add("hn1 hn2 hn3 hn4", 4, rest + " " + " | ".join(mirror[:7]) + " |", r"\ff")
    block.add("perc1", 2, rests(7, 8, 6) + r"c'2..:32\p\< ~ | c'2..:32\f |")
    block.add("perc1", 4, rests(7, 8, 6) + r"c'2..:32\mf\< ~ | c'2..:32\ff |")
    block.close()

    # ------------------------------------------------- the hammer strokes (8 bars)
    s = work.section(8, *seven)

    def hammer(chord: str, letter: str = "X") -> str:
        """Return the 8 bars of hammer strokes for a chord in its D form."""
        stroke = r"X8-> r X8-> r X8-> X X |"
        run = r"X8-> X X-> X X-> X X |"
        last = r"X8-> X X-> X X4.->\fff |"
        shifts = [-6, -6, -3, -3, 0, 0, 3, 6]
        patterns = [stroke] * 4 + [run] * 3 + [last]
        text = ""
        for number, (shift, pattern) in enumerate(zip(shifts, patterns, strict=True)):
            bar = fill(tr(chord, shift), pattern.replace("X", letter))
            if number == 0:
                bar = first(bar, r"\ff", note=True)
            if number == 4:
                bar = first(bar, r"\<", note=True)
            text += bar + " "
        return text

    voices = lines(hammer(HAMMER_CHORD))  # 8 voices, from the lowest to the highest
    put(s, "cb tuba bn3 cbcl", voices[0])
    put(s, "btbn bn2", voices[1])
    put(s, "tbn2 bn1 cl3", voices[2])
    put(s, "tbn1 hn4 hn2", voices[3])
    put(s, "hn3 hn1 cl1", voices[4])
    put(s, "tpt3 ob2:1", voices[5])
    put(s, "tpt2 ob1 cl2:1 fl2:1", voices[6])
    put(s, "tpt1 fl1:1 fl3:1", voices[7])
    s.write("vc", first(hammer(r"<as, d>1"), r"\ord", note=True))
    s.write("va", hammer(r"<b f'>1"))
    s.write("vn2", hammer(r"<es' as'>1"))
    s.write("vn1", hammer(r"<d'' d'''>1"))
    s.write("pno.lh", hammer(r"<d, d>1"))
    s.write("pno.rh", hammer(r"<b es' as' d''>1"))
    s.write("timp", hammer(r"<d>1", "A"))
    strokes = r"c'8->\ff r c'8-> r c'8-> r4 |"
    # The bass drum, the taiko, and the snare drum have the rhythm of the strokes.
    put(s, "perc3 perc6 perc4", times(strokes, 7) + r" c'8-> r c'8-> r c'4.->\fff |")
    s.write(
        "perc5", times(r"a8->\ff r c'8-> r e'8-> c'8 a8 |", 7) + r" a8-> c'8 e'8-> c'8 a4.->\fff |"
    )
    # The roll of the suspended cymbal ends with one stroke. Then the player goes to the tam-tam.
    s.write("perc1", r"c'8\ff\lv r r4 r4. | " + rests(7, 8, 7))
    s.close()


def _broad_motto(work: Work) -> None:
    """Mark N: the motto in long notes, three times (D, F, A-flat)."""
    structure = work.structure
    s = work.section(12, 4, 4)
    structure.mark(s.bar(1), "N")
    structure.tempo(s.bar(1), 1, 72, "Pesante")
    block = Block(s, rests(4, 4, 4), rests(4, 4, 4), rests(4, 4, 4))

    motto = r"d'1-^ | es'1-^ | as'1-^ ~ | as'1 |"
    # The cell of the ostinato as fast notes: groups of 7 against the beat.
    figure = r"d'16 as' es' as' d' es' as' d' as' es' as' d' es' as' d' as' |"

    # Phrase 1, on D: the motto in the low instruments, the fast notes above it.
    low = "tuba:-2 btbn:-2 bn3:-2 cbcl:-2 cl3:-2 vc:-2 cb:-2 tbn1:-1 tbn2:-1 bn1:-1 bn2:-1"
    block.add(low + " hn1 hn2 hn3 hn4", 1, motto, r"\ff")
    block.add("va:-1 vn2 vn1:1", 1, times(figure, 4), r"\ff")
    block.add("cb", 2, r"f,4\f\pizz r f,4 r | f,4 r f,4 r | f,4 r f,4 r | f,4 r f,4 r |")
    block.add("perc2", 1, r"""\switch "tubular bells" d'1\ff | es'1 | as'1 | R1 |""")
    block.add("perc1", 1, r"""\switch "tam-tams" c'1\ff\lv | R1*3 |""")
    block.add("perc3", 1, r"c'4\ff r4 r2 | R1*3 |")
    block.add("timp", 1, r"d,1:32\ff\> ~ | d,1:32 ~ | d,1:32\p ~ | d,1:32 |")
    block.add("pno.lh", 1, r"<d,, d,>1\ff | <es,, es,>1 | <as,, as,>1 ~ | <as,, as,>1 |")

    # Phrase 2, on F: the motto in the trumpets and horns, the fast notes below it.
    block.add("tpt1 tpt2 tpt3 ob1 ob2 cl1 fl1:1 fl2:1 hn1:-1 hn2:-1 hn3:-1 hn4:-1", 2,
              tr(motto, 3), r"\f")  # fmt: skip
    block.add("vc:-1 va:-1 bn1:-1 bn2:-1 cl3:-1", 2, times(tr(figure, 3), 4), r"\f")
    block.add("vn2:1 vn1:2", 2, dyn(tr(AGITATED, 3), r"\f"))
    block.add("timp", 2, r"f,4\f r r2 | R1*3 |")
    block.add("perc2", 2, r"f'1\f | ges'1 | ces''1 | R1 |")

    # Phrase 3, on A-flat: the motto high and soft. The harmony goes to B minor.
    block.add("fl1:1 fl2:1 cl2:1 vn1:1 ob1 cl1 vn2", 3, r"as'1\mf\> | a'1 | d''1\p ~ | d''1 |")
    block.spread(
        "hn4 hn3 hn2 hn1", 3,
        r"<as, es ces' es'>1\p( | <a, fis cis' fis'>1 | <g, g b d'>1 | <fis, e ais d'>1) |",
    )  # fmt: skip
    block.add("vc cb:-1", 3, r"as,1\p\arco( | a,1 | g,1 | fis,1) |")
    block.add("va:-1", 3, first(times(tr(figure, 6), 2), r"\mf\>", note=True)
              + r"<g' b'>1\pp( | <fis' ais'>1) |")  # fmt: skip
    block.add(
        "harp.rh", 3,
        r"<as es' as' ces''>2\p\arpeggio r2 | <a fis' a' cis''>2\arpeggio r2 | "
        r"<g d' g' b'>2\arpeggio r2 | <fis e' ais' d''>2\arpeggio r2 |",
    )  # fmt: skip
    block.close()


def _song_returns(work: Work) -> None:
    """Mark O: the song theme in B minor, then a rise by minor thirds."""
    structure = work.structure
    s = work.section(16, 4, 4)
    structure.mark(s.bar(1), "O")
    structure.tempo(s.bar(1), 1, 58, "Meno mosso, molto espressivo")
    block = Block(s, rests(4, 4, 8), rests(4, 4, 8))

    wave = (
        r"\tuplet 3/2 { A8( B C } \tuplet 3/2 { B8 C B } "
        r"\tuplet 3/2 { A8 B C } \tuplet 3/2 { B8 C B) } |"
    )
    half_wave = r"\tuplet 3/2 { A8( B C } \tuplet 3/2 { B8 C B) }"

    # Phrase 1: the song theme (8 bars).
    song = tr(SONG, 6)
    block.add("vn1", 1, song)
    block.add("vn2:-1 fl1", 1, r"R1*4 | " + plain(song.split("|", 4)[4]), r"\p")
    chords = r"<b, fis d'>1\pp <g, d b>1 <c g e'>1 <b, fis d'>1 <d a fis'>1 <g, d b>1"
    block.add(
        "vc", 1,
        fill(chords, wave)
        + fill(r"<e, b, g>1", half_wave) + fill(r"<c g e'>1", half_wave) + " | "
        + fill(r"<b, fis dis'>1", wave),
    )  # fmt: skip
    block.add(
        "va", 1,
        r"<d' fis'>1\pp( | <d' fis'>1) | <e' g'>1( | <d' fis'>1) | "
        r"<fis' a'>1( | <d' g'>1) | <e' g'>1( | <dis' fis'>1) |",
    )  # fmt: skip
    block.add(
        "cb", 1,
        r"b,4\p\pizz r r2 | g,4 r r2 | c4 r r2 | b,4 r r2 | "
        r"d4 r r2 | g,4 r r2 | e,4 r c4 r | b,4 r r2 |",
    )  # fmt: skip
    block.add("hn1", 1, r"b1\pp ~ | b1 | c'1( | b1) | R1*4 |")
    block.add("hn2", 1, r"fis1\pp ~ | fis1 | g1( | fis1) | R1*4 |")
    block.add(
        "harp.rh", 1,
        r"<b fis' b' d''>4\p\arpeggio r4 r2 | <b d' g' b'>4\arpeggio r4 r2 | "
        r"<c' e' g' c''>4\arpeggio r4 r2 | <b fis' b'>4\arpeggio r4 r2 | "
        r"<a d' fis' a'>4\arpeggio r4 r2 | <b d' g' b'>4\arpeggio r4 r2 | "
        r"<b e' g' b'>4\arpeggio r4 <c' e' g' c''>4\arpeggio r4 | "
        r"<b dis' fis' b'>4\arpeggio r4 r2 |",
    )  # fmt: skip

    # Phrase 2: the rising half of the theme, each time a minor third higher.
    rise = (
        r"fis''2\mf\<( g''4 a''4 | b''2. a''4) | a''2( bes''4 c'''4 | d'''2. c'''4) | "
        r"c'''2\f\<( des'''4 es'''4 | f'''2. es'''4) | des'''2\ff( c'''4 bes''4 | a''1\>) |"
    )
    block.add("vn1 vn2:-1 fl1", 2, rise)
    last_half = rise.split("|", 4)[4]
    block.add("ob1:-1", 2, r"R1*2 | " + rise.split("|", 2)[2])
    block.add("fl2 cl1:-1 tpt1:-1", 2, r"R1*4 | " + last_half)
    block.spread(
        "hn4 hn3 hn2 hn1", 2,
        r"<b, fis b d'>1\p\<( | <g, g b d'>1) | <d a d' f'>1\mf\<( | <bes, f bes d'>1) | "
        r"<f c' f' as'>1\f\<( | <des as des' f'>1) | <bes, f bes des'>1\ff( | <a, e g cis'>1) |",
    )  # fmt: skip
    block.spread(
        "btbn tbn2 tbn1", 2,
        r"R1*4 | <f, c as>1\mf\<( | <des, des as>1) | <bes,, des bes>1\f\<( | <a,, e cis'>1\ff) |",
    )  # fmt: skip
    bass = r"b,1\mp\<( | g,1) | d1\mf\<( | bes,1) | f1\f\<( | des1) | bes,1\ff( | a,1) |"
    block.add("bn1 bn2 bn3:-1 cb:-1", 2, bass)
    chords = (
        r"<b, fis d'>1\mp <g, d b>1 <d a f'>1 <bes, f d'>1 "
        r"<f c' as'>1 <des as f'>1 <bes, f des'>1 <a, e cis'>1"
    )
    block.add("vc", 2, fill(chords, wave))
    block.add("va", 2, r"R1*4 | " + fill(
        r"<f' c'' as''>1\mf <des' as' f''>1 <bes f' des''>1 <a e' cis''>1", wave))  # fmt: skip
    block.add("timp", 2, r"R1*7 | a,1:32\mp\< |")
    block.close()


def _ascent(work: Work) -> None:
    """Mark P: the way up to the first climax.

    The bass goes up by semitones from A to C-sharp. Above each bass note is
    the diminished seventh chord one semitone higher. The head of the
    agitated theme goes up through the notes of this chord. The motto calls
    in the brass come nearer and nearer together.
    """
    structure = work.structure
    s = work.section(28, 4, 4)
    structure.mark(s.bar(1), "P")
    structure.tempo(s.bar(1), 1, 72, "Agitato")
    structure.change(s.bar(5), 1, "poco a poco accelerando")
    structure.arrive(s.bar(25), 1, 100)
    structure.change(s.bar(27), 1, "allargando")
    block = Block(s, *[rests(4, 4, 4)] * 7)

    head = r"r8 c'8\<( des'4 ~ des'8 ges'8 f'4)\! |"
    fast = r"r16 c'16( des'8 ~ des'16 ges'16 f'8)"
    call = r"c'8-> des'8-> ges'2.-> |"
    rush = r"r2 c''16\<( des'' es'' e'' fis'' g'' a'' bes''\!) |"
    pedals = [-3, -3, -2, -1, 0, 1, 1]  # the bass of each unit, in semitones from C
    tones = [4, 7, 10, 13]  # the chord notes above the bass
    levels = [r"\p", r"\p", r"\mp", r"\mf", r"\mf", r"\f", r"\ff"]

    # The head of the agitated theme: one time in each bar, then two times.
    def line(pedal: int) -> str:
        return " ".join(tr(head, pedal + tone) for tone in tones)

    block.add("va:-1 vc:-1", 1, line(-3), r"\p")
    block.add("vn2 va vc:-1", 2, line(-3), r"\p")
    block.add("vn1:1 vn2 va vc:-1", 3, line(-2), r"\mp")
    block.add("vn1:1 vn2:1 va vc", 4, line(-1), r"\mf")
    halves = [tr(fast, tone) for tone in (4, 7, 10, 13, 16, 19, 22, 25)]
    double_speed = " ".join(
        f"{first_half} {second_half} |"
        for first_half, second_half in zip(halves[0::2], halves[1::2], strict=True)
    )
    block.add("vn1 vn2 va:-1 vc:-2", 5, double_speed, r"\mf")
    rise = r"d'2:32 f'2:32 | as'2:32 b'2:32 | d''2:32 f''2:32 | as''2:32 b''2:32 |"
    block.add("vn1:1 vn2 va:-1 vc:-1", 6, rise, r"\f\<")
    hold = r"X1:32\ff\< ~ | X1:32 ~ | X1:32 ~ | X1:32\fff |"
    block.add("vn1", 7, fill(r"<b'' d'''>1", hold))
    block.add("vn2", 7, fill(r"<f'' as''>1", hold))
    block.add("va", 7, fill(r"<f' as'>1", hold))
    block.add("vc", 7, fill(r"<d b>1", hold))

    # The bass, and the pulse of the timpani that gets faster.
    held = r"A1 ~ | A1 ~ | A1 ~ | A1 |"
    pulses = [
        r"A4 r A4 r |",
        r"A4 A A A |",
        r"A8 A A4 A8 A A4 |",
        r"A8 A A A A A A A |",
        r"\tuplet 3/2 { A8 A A } \tuplet 3/2 { A8 A A } \tuplet 3/2 { A8 A A } "
        r"\tuplet 3/2 { A8 A A } |",
    ]
    for unit, (pedal, level) in enumerate(zip(pedals, levels, strict=True), start=1):
        low = "cb bn3 bn1:1 bn2:1" + (" cbcl" if unit >= 3 else "")
        if unit >= 5:
            # The tuba and the bass trombone hammer the bass note.
            strokes = r"A4-> A4-> A4-> A4-> |" if unit == 5 else r"A8-> A A-> A A-> A A-> A |"
            block.add("tuba btbn", unit, fill(tr(r"<c,>1", pedal), times(strokes, 4)), level)
        marks = level + (r"\arco" if unit == 1 else "")
        block.add("cb", unit, fill(tr(r"<c,>1", pedal), held), marks)
        block.add(low.replace("cb ", ""), unit, fill(tr(r"<c,>1", pedal), held), level)
        if unit <= 5:
            beat = fill(tr(r"<c>1", pedal), times(pulses[unit - 1], 4))
        else:
            beat = fill(tr(r"<c>1", pedal), r"A1:32 ~ | A1:32 ~ | A1:32 ~ | A1:32 |")
        block.add("timp", unit, beat, level)
        if unit >= 5:
            tremolo = r"X1:32 ~ | X1:32 ~ | X1:32 ~ | X1:32 |"
            block.add("pno.lh", unit, fill(tr(r"<c,, c,>1", pedal), tremolo), level)
    block.add("perc3", 3, times(r"c'4\p r c'4 r |", 4))
    block.add("perc3", 4, times(r"c'4\mp r c'4 r |", 4))
    block.add("perc3", 5, times(r"c'4\mf c'4 c'4 c'4 |", 4))
    block.add("perc3", 6, r"c'1:32\mf\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32 |")
    block.add("perc3", 7, r"c'1:32\f\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32\fff |")
    block.add(
        "perc4", 6, r"""\switch "suspended cymbals" c'1:32\p\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32 |"""
    )
    # The tom-toms and the taiko: their strokes come nearer and nearer together.
    block.add("perc5", 3, times(r"r8 a8\p r8 a8 r8 c'8 r8 c'8 |", 4))
    block.add("perc5", 4, times(r"r8 a8\mp c'8 a8 r8 c'8 e'8 c'8 |", 4))
    block.add("perc5", 5, times(r"a8\mf a c' c' e' e' c' a |", 4))
    fast_toms = r"a16 a a a c' c' c' c' e' e' e' e' c' c' a a |"
    block.add("perc5", 6, first(times(fast_toms, 4), r"\f\<", note=True))
    block.add("perc5", 7, first(times(fast_toms, 4), r"\ff\<", note=True))
    block.add("perc6", 4, times(r"c'4->\mp r c'4-> r |", 4))
    block.add("perc6", 5, times(r"c'4->\mf c'4-> c'4-> c'4-> |", 4))
    block.add("perc6", 6, times(r"c'8->\f c' c'-> c' c'-> c' c'-> c' |", 4))
    block.add(
        "perc6", 7, first(times(r"c'8-> c' c'-> c' c'-> c' c'-> c' |", 4), r"\ff\<", note=True)
    )
    block.add("perc4", 7, r"c'1:32\mf\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32\fff |")

    # The diminished seventh chord in the horns and woodwinds: a swell in each unit.
    swells = {
        1: r"X1\pp\< ~ | X1 ~ | X1\mp\> ~ | X1\! |",
        3: r"X1\p\< ~ | X1 ~ | X1\mf\> ~ | X1\! |",
        5: r"X1\mf\< ~ | X1 ~ | X1 ~ | X1\f |",
        6: r"X1\f ~ | X1 ~ | X1 ~ | X1 |",
        7: r"X1\f\< ~ | X1 ~ | X1 ~ | X1\fff |",
    }
    for unit, pedal in enumerate(pedals, start=1):
        swell = swells[max(key for key in swells if key <= unit)]
        voices = lines(fill(tr(r"<e g bes cis'>1", pedal), swell))
        for player, voice in zip(["hn4", "hn3", "hn2", "hn1"], voices, strict=True):
            block.add(player, unit, voice)
        if unit >= 3:
            block.add("cl1:1", unit, voices[1])
            block.add("ob2:1", unit, voices[2])
            block.add("ob1:1", unit, voices[3])
        if unit >= 6:
            block.add("fl2:2 cl2:1", unit, voices[2])
            block.add("fl1:2 fl3:2", unit, voices[3])

    # The motto calls in the brass.
    def calls(pedal: int, numbers: tuple[int, ...]) -> str:
        entries = {number: tr(call, pedal + tones[number - 1]) for number in numbers}
        return bars(4, "R1 |", entries)

    block.add("hn5 hn6", 1, calls(-3, (3,)), r"\mp")
    block.add("hn5 hn6", 2, calls(-3, (3,)), r"\mf")
    for unit in (3, 4, 5):
        pedal, level = pedals[unit - 1], levels[unit - 1]
        block.add("tpt1 tpt2", unit, calls(pedal, (1, 3)), level)
        block.add("tbn1:-1 tbn2:-1 hn5:-1 hn6:-1", unit, calls(pedal, (2, 4)), level)
    block.add("tpt1 tpt2 tpt3 tbn1:-1 tbn2:-1 hn5:-1 hn6:-1", 6, calls(1, (1, 2, 3, 4)), r"\f")
    last = r"A1\ff\<-^ ~ | A1 ~ | A1 ~ | A1\fff |"
    for player, note in [("tpt1", "d''"), ("tpt2", "b'"), ("tpt3", "as'"), ("hn5", "as'"),
                         ("hn6", "f'"), ("tbn1", "f"), ("tbn2", "d")]:  # fmt: skip
        block.add(player, 7, fill(f"<{note}>1", last))

    # Fast scales up in the high woodwinds.
    block.add("fl1 fl2", 2, bars(4, "R1 |", {4: tr(rush, -3)}), r"\p")
    block.add("fl1 fl2 cl2", 3, bars(4, "R1 |", {4: tr(rush, -2)}), r"\mf")
    block.add("fl1:1 fl2:1 fl3:1 cl2", 4, bars(4, "R1 |", {2: tr(rush, -1), 4: tr(rush, -1)}),
              r"\f")  # fmt: skip
    every_bar = " ".join(tr(rush, 0) for _ in range(4))
    block.add("fl1:1 fl2:1 fl3:1 cl2", 5, every_bar, r"\f")
    block.close()


def _first_climax(work: Work) -> None:
    """Mark Q: the chorale of part 1, fff. It stops on the motto as a chord."""
    structure = work.structure
    s = work.section(8, 4, 4)
    structure.mark(s.bar(1), "Q")
    structure.tempo(s.bar(1), 1, 54, "Largamente, con tutta la forza")
    block = Block(s, rests(4, 4, 8))

    chorale = (
        r"<d f' a' d''>1-^ <c ges' bes' es''>1-^ <bes, f' des'' as''>1-^ <a, f' cis'' g''>1-^ "
        r"<d f' a' d''>1-^ <c ges' bes' es''>1-^ <d d' es'' as''>1-^ ~ <d d' es'' as''>1"
    )
    bass, tenor, alto, top = lines(chorale)
    block.add("tpt1 ob1 fl1:1 fl2:1 fl3:1 cl2:1 hn5:-1 hn6:-1 perc2:-1", 1, top, r"\fff")
    block.add("tpt2 ob2 cl1 hn1 hn3:-1", 1, alto, r"\fff")
    block.add("tpt3 hn2 hn4:-1 tbn1:-1", 1, tenor, r"\fff")
    block.add("tbn2 bn1 bn2 cl3 btbn:-1 tuba:-1 bn3:-1 cbcl:-1", 1, bass, r"\fff")
    block.add("vn1", 1, fill(double(top, 1), r"X1:32"), r"\fff")
    block.add("vn2", 1, fill(double(alto, 1), r"X1:32"), r"\fff")
    walking = dyn(WALKING_LOUD, r"\fff")
    motto_tremolo = r"X1:32 ~ | X1:32 |"
    low = walking + r"d'4.->( es'8 f'4. g'8 | as'2.) r4 | "
    block.add("va", 1, low + fill(r"<d' as'>1", motto_tremolo))
    block.add("vc", 1, octave(low, -1) + fill(r"<d as>1", motto_tremolo))
    block.add("cb", 1, octave(low, -2) + fill(r"<d,>1", motto_tremolo))
    block.add("timp", 1, r"d,1:32\fff-> | " + times(r"d,1:32-> |", 7))
    block.add("perc3", 1, times(r"c'4\fff r4 r2 |", 6) + r" c'1:32 ~ | c'1:32 |")
    # Hand cymbals at the start of each second bar.
    block.add("perc1", 1, r"""\switch "crash cymbals" """ + r"c'4\fff\lv r4 r2 | R1 | " * 4)
    # The suspended cymbal: a stroke, then a roll that grows into the subsequent stroke.
    block.add("perc4", 1, r"c'4\fff\lv r4 r2 | c'1:32\mf\< | " * 4)
    # The player of the tom-toms goes to the tam-tam: it starts the second half of the chorale.
    block.add("perc5", 1, r"""\switch "tam-tams" R1*4 | c'1\fff\lv | R1 | c'1\lv | R1 |""")
    block.add(
        "perc6", 1,
        times(r"c'4->\fff r c'4-> r |", 6)
        + r" c'4-> c'4-> c'4-> c'4-> | c'8-> c' c'-> c' c'-> c' c'-> c' |",
    )  # fmt: skip
    block.add("pno.lh", 1, times(r"<d,, d,>1\fff-^ |", 8))
    block.add(
        "pno.rh", 1,
        r"<f' a' d''>1\fff-^ | <ges' bes' es''>1-^ | <f' des'' as''>1-^ | <f' cis'' g''>1-^ | "
        r"<f' a' d''>1-^ | <ges' bes' es''>1-^ | <d' es'' as''>1-^ | <d' es'' as''>1-^ |",
    )  # fmt: skip
    block.close()


def _collapse(work: Work) -> None:
    """Mark R: one stroke, then only the tritone and the note A-flat stay."""
    structure = work.structure
    s = work.section(6, 4, 4)
    structure.mark(s.bar(1), "R")
    structure.tempo(s.bar(1), 1, 50, "Lento")
    structure.change(s.bar(3), 1, "rit.")
    structure.arrive(s.bar(6), 1, 40)
    block = Block(s, rests(4, 4, 6))

    stroke = r"d'8-^\sffz r8 r4 r2 | R1*5 |"
    block.add(
        "tpt1:1 tpt2 tpt3 hn1 hn2 hn3 hn4 hn5 hn6 tbn1:-1 tbn2:-1 btbn:-2 tuba:-2 "
        "fl1:2 fl2:2 fl3:2 ob1:1 ob2:1 cl1:1 cl2:1 bn1:-1 bn2:-1 bn3:-2 cbcl:-2 vn2:1 cb:-2",
        1, stroke,
    )  # fmt: skip
    block.add("perc3 perc1 perc5 perc6", 1, r"c'4\sffz\lv r4 r2 | R1*5 |")
    block.add("timp", 1, r"d,4\sffz r4 r2 | R1*5 |")
    block.add("pno.lh", 1, r"<d,, d,>1\sffz\lv | R1*5 |")
    block.add("harp.lh", 1, r"<d,, d,>4\ff\lv r4 r2 | R1*5 |")
    tritone = (
        r"X8-^\sffz r8 X2.:32\ppp\sulpont ~ | X1:32 ~ | X1:32\> ~ | X1:32 ~ | X2:32 r2\! | R1 |"
    )
    block.add("va", 1, fill(r"<d' as'>1", tritone))
    block.add("vc", 1, fill(r"<d as>1", tritone))
    block.add(
        "cl3", 1,
        r"d'8-^\sffz r8 r4 r2 | d,2\p\espr( es,2 | as,1 ~ | as,2.)\> r4\! | R1*2 |",
    )  # fmt: skip
    block.add(
        "perc2", 1,
        r"""\switch "vibraphone" R1*3 | r2 as'2\pp\motoron\lv ~ | as'1 ~ | as'1\fermata |""",
    )  # fmt: skip
    block.add("cel.rh", 1, r"R1*4 | r4 as''4\pp r2 | R1\fermata |")
    block.add("vn1", 1, r"d'''8-^\sffz r8 r4 r2 | R1*3 | as'''1\ppp\flageolet ~ | as'''1\fermata |")
    block.close()
