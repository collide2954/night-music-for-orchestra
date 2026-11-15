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

from ..compose.tools import first, octave, tr
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

# The walking theme of part 1 in its loud form (4 bars).
WALKING_LOUD = r"""
    d'4.\ff->( es'8 f'4. g'8 | as'2.) r4 | as'4.->( g'8 f'4. es'8 | d'2.) r4 |
"""


def write(work: Work) -> None:
    _agitation(work)
    _song(work)


def _agitation(work: Work) -> None:
    structure = work.structure

    # ------------------------------------------------- bars 39 to 50: three waves
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
    s.write("perc2", r"""\switch "suspended cymbals" R1*11 | c'1:32\p\< |""")
    s.close()

    # ---------------------------------------------- bars 51 to 56: the first crest
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
    s.write("bn3", r"""d,1\ff( | c,1 | bes,,1 | a,,1) | R1*2 |""")
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

    # -------------------------------------------- bars 57 to 62: the way to the song
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

    # --------------------------------------------- bars 63 to 70: the song theme
    s = work.section(8, 4, 4)
    structure.mark(s.bar(1), "F")
    structure.tempo(s.bar(1), 1, 60, "Un poco più tranquillo")

    song = r"""
        c''2\p\dolce( bes'4 as'4 | g'2. f'4) | ges'2( f'4 es'4 | f'1) |
        c''2\<( des''4 es''4 | f''2.\mf\> es''4 | des''2 c''4 bes'4 | c''1\p) |
    """
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

    # ------------------------------------- bars 71 to 78: the song again, then unrest
    s = work.section(8, 4, 4)
    structure.change(s.bar(5), 1, "accel. poco a poco")

    first_half = r"""c''2\mp\dolce( bes'4 as'4 | g'2. f'4) | ges'2( f'4 es'4 | f'1) |"""
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
