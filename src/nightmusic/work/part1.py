"""Part 1 (bars 1 to 38): very slow. A walk in the dark, and one lonely melody.

Material of this part:

- The walking theme: five notes that go up from D to A-flat (the dark state of
  the motto: D, E-flat, A-flat), and its mirror, which goes down from D to
  G-sharp. The two lines meet on the same note, one octave apart.
- The long song: a free solo line for the English horn, with long notes on the
  fifth (A) and on the raised fourth (G-sharp).
- The chorale: four chords for muted horns. The top voice is the motto.
- The footsteps: soft timpani strokes on beats 1 and 3.

Style profile: "Transfigured", before the turn (see research/tables/profiles.csv).
"""

from __future__ import annotations

from ..notation.work import Work


def write(work: Work) -> None:
    structure = work.structure

    # ------------------------------------------------------------ bars 1 to 8
    s = work.section(8, 4, 4)
    structure.tempo(s.bar(1), 1, 44, "Molto lento, misterioso")

    s.write(
        "cb",
        r"""
        <d,, d,>1\pppp\sultasto\div ~ | <d,, d,>1 ~ | <d,, d,>1\< ~ | <d,, d,>1\ppp\> ~ |
        <d,, d,>1\pppp ~ | <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 |
    """,
    )
    s.write("perc1", r"""\switch "tam-tams" c'1\ppp\lv | R1*7 |""")
    s.write("pno.lh", r"""<d,, d,>1\pppp\lv | R1*7 |""")
    s.write(
        "timp",
        r"""
        R1*2 |
        d,4\ppp\softmallets r d,4 r | d,4 r d,4 r | d,4 r d,4 r | d,4 r d,4 r |
        d,4 r d,4 r | d,4 r d,4 r |
    """,
    )
    s.write(
        "va",
        r"""
        R1*2 |
        d4.\pp\consord( es8 f4. g8 | as2.) r4 |
        as1\ppp ~ | as2. r4 |
        as4.\pp( g8 f4. es8 | d2.) r4 |
    """,
    )
    s.write(
        "vc",
        r"""
        R1*4 |
        d4.\pp\consord( cis8 b,4. a,8 | gis,2.) r4 |
        gis,4.( a,8 b,4. cis8 | d2.) r4 |
    """,
    )
    s.write("ob3", r"""\switch "English horn" R1*8 |""")
    s.write("fl2", r"""\switch "alto flute" R1*8 |""")
    s.write("cl3", r"""\switch "bass clarinet" R1*8 |""")
    s.close()

    # ----------------------------------------------------------- bars 9 to 20
    s = work.section(12, 4, 4)
    structure.mark(s.bar(1), "A")

    s.write(
        "ob3",
        r"""
        r2 a'2\p\espr\<( ~ |
        a'4.\mp\> \grace { b'16 } a'8 gis'4 a'8 b'8\! |
        c''4. b'8 a'4 gis'8 f'8) |
        e'2\p( ~ e'8 f'8 gis'8 a'8 |
        bes'4. a'8 g'4 f'8 es'8) |
        d'2. r4 |
        r4 a'4\mp\<( d''4. es''8 |
        as''2\mf\> ~ as''8 g''8 f''8 es''8 |
        d''4. c''8 bes'4 a'8 g'8) |
        gis'2\p( ~ gis'8 a'8 f'8 e'8 |
        d'2.\>) r4\! |
        R1 |
    """,
    )
    s.write(
        "vc",
        r"""
        <d a>1\ppp\div ~ | <d a>1 | <d gis>1 | <d a>2 <d gis>2 |
        <d g>2 <es g>2 | <d a>1 | <d bes>2 <es bes>2 | <es as>1\< |
        <e g>1\mp\> | <e gis>1\pp | <d a>1\ppp ~ | <d a>1 |
    """,
    )
    s.write(
        "va",
        r"""
        <d' f'>1\ppp\div ~ | <d' f'>1 | <b f'>1 | <d' f'>2 <b f'>2 |
        <bes d'>2 <bes es'>2 | <a d'>1 | <d' f'>2 <d' g'>2 | <c' es'>1\< |
        <bes d'>1\mp\> | <bes d'>1\pp | <a d'>1\ppp ~ | <a d'>1 |
    """,
    )
    s.write(
        "vn2",
        r"""
        R1*7 |
        <as' c''>1\ppp\consord\div\< | <g' bes'>1\p\> | <gis' bes'>1\ppp | R1*2 |
    """,
    )
    s.write(
        "cb",
        r"""
        <d,, d,>1\pppp ~ | <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 ~ |
        <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1\< ~ |
        <d,, d,>1\pp\> ~ | <d,, d,>1\pppp ~ | <d,, d,>1 ~ | <d,, d,>1 |
    """,
    )
    s.write(
        "timp",
        r"""
        d,4\ppp r d,4 r | d,4 r d,4 r | d,4 r d,4 r | d,4 r d,4 r |
        d,4 r d,4 r | d,4 r d,4 r | d,4 r d,4 r | d,4\< r d,4 r |
        d,4\p\> r r2 | d,4\ppp r r2 | d,4 r r2 | d,4 r r2 |
    """,
    )
    s.write(
        "fl2",
        r"""
        R1*5 |
        r4 r8 bes8\pp( a8 g8 f8 es8 | d2.) r4 | R1*5 |
    """,
    )
    s.write(
        "cel.rh",
        r"""
        R1*5 |
        r2 r8 \tuplet 3/2 { d'''16\ppp es''' as''' } r4 | R1*5 |
        r4 r8 \tuplet 3/2 { d'''16\ppp es''' as''' } r2 |
    """,
    )
    s.write(
        "harp.lh",
        r"""
        d,4\pp\lv r4 r2 | R1 | d,4 r4 r2 | R1 | d,4 r4 r2 | R1 |
        d,4 r4 r2 | <d,, d,>4\p r4 r2 | R1 | d,4\pp r4 r2 | R1 | d,4 r4 r2 |
    """,
    )
    s.write(
        "cimb.rh",
        r"""
        R1*7 |
        as'1:32\ppp\< | <g' bes'>1:32\p\> | gis'1:32\ppp | R1*2 |
    """,
    )
    s.close()

    # ---------------------------------------------------------- bars 21 to 28
    s = work.section(8, 4, 4)
    structure.mark(s.bar(1), "B")

    s.write(
        "hn1",
        r"""
        d'1\pp\consord( | es'1 | as'1 | g'1) |
        d'1\pp( | es'1\< | e'1\mp\> | d'1\pp) |
    """,
    )
    s.write(
        "hn2",
        r"""
        a1\pp\consord( | bes1 | des'1 | cis'1) |
        a1\pp( | bes1\< | bes1\mp\> | a1\pp) |
    """,
    )
    s.write(
        "hn3",
        r"""
        f1\pp\consord( | ges1 | f1 | f1) |
        f1\pp( | ges1\< | gis1\mp\> | a1\pp) |
    """,
    )
    s.write(
        "hn4",
        r"""
        d1\pp\consord( | c1 | bes,1 | a,1) |
        d1\pp( | c1\< | bes,1\mp\> | d1\pp) |
    """,
    )
    s.write(
        "vn1",
        r"""
        <a'' d'''>1:32\ppp\consord\sulpont\div ~ | <a'' d'''>1:32 ~ | <a'' d'''>1:32 ~ |
        <a'' d'''>1:32 |
        <a'' e'''>1:32\ppp ~ | <a'' e'''>1:32\< ~ | <a'' e'''>1:32\p\> ~ | <a'' e'''>1:32\ppp |
    """,
    )
    s.write(
        "cl3",
        r"""
        R1*4 |
        d,4.\p( es,8 f,4. g,8 | as,2.) r4 | R1*2 |
    """,
    )
    s.write(
        "vc",
        r"""
        R1*6 |
        as4.\mp\unis( g8 f4. es8 | d2.\>) r4\! |
    """,
    )
    s.write(
        "va",
        r"""
        R1*6 |
        gis4.\mp\unis( a8 b4. cis'8 | d'2.\>) r4\! |
    """,
    )
    s.write(
        "cb",
        r"""
        <d,, d,>1\pppp ~ | <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 ~ |
        <d,, d,>1 ~ | <d,, d,>1\< ~ | <d,, d,>1\pp\> ~ | <d,, d,>1\pppp |
    """,
    )
    s.write(
        "timp",
        r"""
        d,4\ppp r d,4 r | d,4 r d,4 r | d,4 r d,4 r | d,4 r d,4 r |
        d,4 r d,4 r | d,4\< r d,4 r | d,4\p\> r d,4 r | d,4\ppp r r2 |
    """,
    )
    s.write(
        "fl2",
        r"""
        R1*2 |
        r2 a'4.\pp( gis'8 | f'4 e'8 d'8 ~ d'2) | R1*4 |
    """,
    )
    s.write(
        "cel.rh",
        r"""
        R1 | r2 \tuplet 3/2 { es'''16\ppp e''' a''' } r8 r4 | R1 |
        r4 \tuplet 3/2 { a''16 bes'' es''' } r8 r2 | R1*4 |
    """,
    )
    s.close()

    # ---------------------------------------------------------- bars 29 to 38
    s = work.section(10, 4, 4)
    structure.mark(s.bar(1), "C")
    structure.change(s.bar(9), 1, "poco rit.")
    structure.arrive(s.bar(10), 1, 34)

    s.write(
        "ob3",
        r"""
        r2 a2\pp( ~ | a4. gis8 f4 e4 | es2.) r4 | R1*7 |
    """,
    )
    s.write(
        "va",
        r"""
        <d' f'>1\ppp\div ~ | <d' f'>1 | <d' g'>1 ~ | <d' g'>1 |
        <b f'>1 ~ | <b f'>1 | <a d'>1 ~ | <a d'>1\> |
        a1\pppp\unis ~ | a1\fermata |
    """,
    )
    s.write(
        "vc",
        r"""
        <d a>1\ppp\div ~ | <d a>1 | <es bes>1 ~ | <es bes>1 |
        <d gis>1 ~ | <d gis>1 | <d a>1 ~ | <d a>1\> |
        a,1\pppp\unis ~ | a,1\fermata |
    """,
    )
    s.write(
        "vn2",
        r"""
        R1*3 |
        r2 a'2\p\espr( ~ | a'4. gis'8 f'4 e'8 d'8 ~ | d'1)\> |
        R1*2\! |
        a'1\pppp ~ | a'1\fermata |
    """,
    )
    s.write(
        "vn1",
        r"""
        R1*8 |
        a''1\pppp\ord ~ | a''1\fermata |
    """,
    )
    s.write(
        "cb",
        r"""
        <d,, d,>1\pppp ~ | <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 ~ |
        <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 ~ | <d,, d,>1 |
        <a,, a,>1\pppp ~ | <a,, a,>1\fermata |
    """,
    )
    s.write(
        "timp",
        r"""
        d,4\ppp r r2 | d,4 r r2 | d,4 r r2 | d,4 r r2 |
        d,4 r r2 | d,4 r r2 | d,4 r r2 | R1 |
        a,4\pppp r r2 | R1 |
    """,
    )
    s.write(
        "cl3",
        r"""
        R1*6 |
        d,2\pp( es,2 | as,1\>) |
        a,1\pppp ~ | a,1\fermata |
    """,
    )
    s.write(
        "cel.rh",
        r"""
        R1*7 |
        r2 r8 \tuplet 3/2 { d'''16\ppp es''' as''' } r4 | R1*2 |
    """,
    )
    s.write("perc1", r"""R1*8 | c'1\pppp\lv | R1 |""")
    s.close()
    structure.double_bar(s.last_bar)
