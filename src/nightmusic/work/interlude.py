"""The piano interlude across the turn (the marks W and X).

The owner of the project asked for an interlude with the piano as its focus,
of about 5 minutes. The owner selected its place and its sound:

- Across the turn. The interlude starts in the night music of part 3, in
  E-flat minor. The piano makes the turn to D major. Then the piano gives the
  warm theme to the cellos.
- The piano leads. A soft halo answers: string harmonics, celesta,
  vibraphone, gongs, and one or two solo winds.

Material of the first half (mark W, the end of part 3):

- The cluster of the night (five adjacent semitones around A-flat) is now a
  figure of the piano: fast notes into a held note. Each time, the figure is
  different. At the end it has only one note, A-flat.
- The calls of the night, as a piano plays them.
- A lonely melody in bare octaves. Its notes are the warm theme with the
  dark form of the motto (D, E-flat, A-flat, G; B-flat, A-flat, G-flat,
  E-flat). The listener does not know the warm theme at this time: the
  melody prepares it, and hides it. The alto flute follows the piano one
  half bar later, with small differences (heterophony).
- A distant music box in 7/8: the song theme of part 2, hidden. The eighth
  note of the 7/8 is the eighth note of the triplets before it (a tempo
  modulation).

Material of the second half (mark X, the start of part 4):

- The turn. Three voices of the piano move. The bass goes from E-flat down
  to D. The note A-flat (now G-sharp) goes up to A. The note G-flat (now
  F-sharp) stays: it is the common note of the two chords.
- Waves. Each wave of the piano goes up to one long note. These long notes
  are the notes of the warm theme, each in a different octave: the theme is
  there, but hidden. The harmony moves by major thirds (D, F-sharp, B-flat),
  as the keys of part 4 do it later.
- The chorale of part 3 comes back, changed: its semitones are now whole
  tones (the light form of the motto on A: A, B, E, then D).
- The piano asks a question with the first two notes of the warm theme. The
  cellos answer with the theme (mark Y).

The cellos do not play in the interlude: thus their theme has a new sound.
"""

from __future__ import annotations

from ..compose.tools import Block, rests, scatter
from ..notation.work import Work

NIGHT_TEMPO = 54
BOX_TEMPO = 81  # the eighth note of the 7/8 = the eighth note of a triplet at 54
LIGHT_TEMPO = 52
WAVE_TEMPO = 60
PEDAL = r"\sustainOff\sustainOn"  # a change of the sustain pedal


def write_night_piano(work: Work) -> None:
    """Mark W: the piano takes the night music. E-flat minor."""
    _entry(work)
    _lonely_octaves(work)
    _music_box(work)
    _stillness(work)


def write_light_piano(work: Work) -> None:
    """Mark X: the piano makes the turn to D major."""
    _turn(work)
    _waves(work)
    _chorale_of_light(work)
    _question(work)


# ------------------------------------------------------------------ mark W


def _entry(work: Work) -> None:
    """Mark W, bars 1 to 10: the piano comes out of the last note of the cello."""
    structure = work.structure
    s = work.section(10, 4, 4)
    structure.mark(s.bar(1), "W")
    structure.tempo(s.bar(1), 1, NIGHT_TEMPO, "Lento, come un notturno")
    block = Block(s, rests(4, 4, 10))

    block.add("pno.lh", 1, scatter(10, 4, 4, {
        (1, 1): r"<es,, es,>2\pp\lv\sustainOn",
        (1, 3): r"\grace { ges16( g as a } bes2)\ppp",
        (3, 2): r"\grace { bes16( a as g } ges2.)\sustainOff\sustainOn",
        (5, 2.5): r"\grace { g16( as a } bes4.)",
        (6, 1): r"<es,, es,>1\pp\lv\sustainOff\sustainOn",
        (7, 2): r"<ges g as a bes>2.\ppp\arpeggio",
        (9, 1): r"\grace { ges16( g as } a2)\sustainOff\sustainOn",
        (10, 3): r"\grace { bes16( a } as2)",
    }))  # fmt: skip
    block.add("pno.rh", 1, scatter(10, 4, 4, {
        (2, 4): r"\ottava #1 d''''8\pp( es''''8) \ottava #0",
        (4, 2): r"\grace { d'''16 } es'''8-.\p es'''8-. es'''4--",
        (6, 2): r"as''8\pp as''8 \tuplet 3/2 { as''8 as'' as'' } as''16 as'' as'' as'' | as''4--",
        (8, 3): r"<as'' as'''>4\p( <g'' g'''>4)",
        (9, 2.5): r"d'''8\pp( es'''4)",
    }))  # fmt: skip

    # The last chord of the strings (mark V) continues and goes to nothing.
    block.add("vn2", 1, r"ges'1\> ~ | ges'2 r2\! | R1*8 |")
    block.add("va", 1, r"<bes es'>1\> ~ | <bes es'>2 r2\! | R1*8 |")
    block.add("cb", 1, r"es,1\> ~ | es,2 r2\! | R1*8 |")

    # The cycle of the gongs continues, but more slowly.
    block.add("perc1", 1, scatter(10, 4, 4, {(1, 1): r"c'1\pp\lv"}))
    block.add("perc3", 1, scatter(10, 4, 4, {(4, 1): r"es'1\p\lv", (9, 3): r"g2\pp\lv"}))
    block.add("perc2", 1, scatter(10, 4, 4, {(7, 1): r"<bes d'>1\pp\lv"}))
    block.close()


def _lonely_octaves(work: Work) -> None:
    """Mark W, bars 11 to 18: the lonely melody in bare octaves. The alto flute follows."""
    s = work.section(8, 4, 4)
    block = Block(s, rests(4, 4, 8))

    # The two hands are three octaves apart. Between the phrases, the left hand
    # plays the cluster figure.
    block.add("pno.rh", 1, scatter(8, 4, 4, {
        (1, 1): r"d''2\p( es''2 ~ | es''2.)",
        (3, 2): r"\grace { bes''16 } as''2\p( g''4 ~ | g''2)",
        (5, 3): r"bes''4\mp( as''4 | ges''2. es''4 ~ | es''1)",
    }))  # fmt: skip
    block.add("pno.lh", 1, scatter(8, 4, 4, {
        (1, 1): r"d,2\p\sustainOff\sustainOn( es,2 ~ | es,2.)",
        (2, 4): r"\grace { ges16( g as a } bes4)\ppp",
        (3, 2): r"\grace { bes,16 } as,2\p\sustainOff\sustainOn( g,4 ~ | g,2)",
        (4, 3): r"\grace { bes16( a as g } ges2)\ppp",
        (5, 3): r"bes,4\mp\sustainOff\sustainOn( as,4 | ges,2. es,4 ~ | es,1)",
        # Triplets: their eighth note is the eighth note of the music box.
        (8, 1): r"\tuplet 3/2 { as8\ppp\sustainOff\sustainOn( a bes } \tuplet 3/2 { a8 as g } "
                r"\tuplet 3/2 { as8 a bes } \tuplet 3/2 { a8 as g) }",
    }))  # fmt: skip

    # The alto flute follows the melody one half bar later, with quarter-tones.
    block.add("fl2", 1, scatter(8, 4, 4, {
        (1, 3): r"d'2\pp\espr( | es'2.)",
        (3, 4): r"as'4\pp( ~ | as'4 aseh'4 g'2)",
        (6, 2): r"bes'4\p( as'4 ges'4 ~ | ges'4 geseh'4 es'2 ~ | es'2\> ~ es'4)\ppp",
    }))  # fmt: skip

    # The halo: natural harmonics of the first violins (the notes G and D of the
    # night scale), the vibraphone with a bow, a gong, the celesta.
    block.add(
        "vn1", 1,
        r"R1*2 | <g'' d'''>1\ppp\flageolet\< ~ | <g'' d'''>1\pp ~ | <g'' d'''>1 ~ | "
        r"<g'' d'''>1\> ~ | <g'' d'''>1 ~ | <g'' d'''>2 r2\! |",
        r"\senzasord\ord\nonvib",
    )  # fmt: skip
    block.add("perc2", 1, scatter(8, 4, 4, {
        (2, 1): r"es''1\pp\bowed\lv", (4, 1): r"g''1\pp\lv", (7, 1): r"es''1\pp\lv",
    }))  # fmt: skip
    block.add("perc3", 1, scatter(8, 4, 4, {(3, 1): r"as1\p\lv", (7, 1): r"es1\pp\lv"}))
    block.add("harp.lh", 1, scatter(8, 4, 4, {(1, 1): r"es,,4\pp", (5, 3): r"bes,,4\pp"}))
    block.add("cel.rh", 1, scatter(8, 4, 4, {(8, 2): r"d''''8\ppp( es''''8)"}))
    block.close()


def _music_box(work: Work) -> None:
    """Mark W, bars 19 to 26: a distant music box in 7/8. The song theme of part 2, hidden."""
    structure = work.structure
    s = work.section(8, 7, 8)
    structure.tempo(s.bar(1), 1, BOX_TEMPO, "Poco mosso, come un carillon lontano")
    rest = "R1*7/8 |"
    block = Block(s, rests(7, 8, 8))

    block.add(
        "pno.rh", 1,
        r"bes''8-.\pp bes''8-. as''16( ges'' as''8) f''4-- es''8-. | "
        r"f''8-. ges''8-. f''8-. es''8-. des''4. | "
        r"ges''8-. ges''8-. f''16( es'' f''8) des''4-- ces''8-. | "
        r"des''8-. es''8-. des''8-. ces''8-. bes'4. | "
        r"bes'8-.\< des''8-. es''8-. f''8-. ges''4-- as''8-. | "
        r"bes''8-. as''8-. bes''8-. ces'''8-. des'''4.\mp | "
        r"ces'''8-.\> bes''8-. as''16( ges'' as''8) f''4-- d''8-. | "
        r"es''4.--\pp ~ es''2 |",
    )  # fmt: skip
    block.add(
        "pno.lh", 1,
        r"<es bes>2..\ppp\lv\sustainOff | " + rest + r" <es bes es'>2..\ppp\lv | "
        r"r4 r4 \grace { ges16( g as } a4.)\ppp | <es bes>2..\ppp\lv | " + rest
        + r" <es, bes,>2..\ppp\lv | r4 r4 \grace { g16( } as4.)\ppp |",
    )  # fmt: skip
    # The celesta doubles some bars of the tune one octave higher: the colour changes.
    block.add(
        "cel.rh", 1,
        rest * 2 + r"ges'''8-.\ppp ges'''8-. f'''16( es''' f'''8) des'''4-- ces'''8-. | "
        r"des'''8-. es'''8-. des'''8-. ces'''8-. bes''4. | " + rest
        + r" bes'''8-.\ppp as'''8-. bes'''8-. ces''''8-. des''''4. | " + rest * 2,
    )  # fmt: skip
    block.add(
        "perc4", 1,
        rest + r"r4 r4 c'16\ppp c' c' c' c'8 | " + rest * 2
        + r"c'16\ppp c' c' c' c'8 r8 r4. | " + rest * 3,
    )  # fmt: skip
    block.add(
        "vn2", 1,
        r"es'8\ppp\pizz r8 r4 r4. | " + rest + r" bes8 r8 r4 r4. | " + rest
        + r" es'8 r8 r4 r4. | " + rest + r" ges'8 r8 r4 r4. | " + rest,
    )  # fmt: skip
    block.close()


def _stillness(work: Work) -> None:
    """Mark W, bars 27 to 34: the end of the melody. The piano stops on three notes."""
    structure = work.structure
    s = work.section(8, 4, 4)
    structure.tempo(s.bar(1), 1, NIGHT_TEMPO, "Tempo del notturno")
    structure.change(s.bar(7), 1, "poco rit.")
    structure.arrive(s.bar(8), 4, 44)
    block = Block(s, rests(4, 4, 8))

    block.add("pno.rh", 1, scatter(8, 4, 4, {
        (1, 1): r"bes''2.\p( as''4 ~ | as''2 ges''2 ~ | ges''1 | es''1)",
        (6, 1): r"ges'4--\ppp ges'4-- ges'2--",
        (8, 1): r"ges'1--\ppp\fermata",
    }))  # fmt: skip
    block.add("pno.lh", 1, scatter(8, 4, 4, {
        (1, 1): r"bes,2.\p\sustainOn( as,4 ~ | as,2 ges,2 ~ | ges,1 | es,1)",
        (5, 2): r"\grace { g16( as } a2.)\ppp\sustainOff\sustainOn",
        (7, 1): r"\grace { g16( } as1)\ppp\sustainOff\sustainOn",
        (8, 1): r"<es,, es,>1\ppp\fermata",
    }))  # fmt: skip
    block.add("fl2", 1, scatter(8, 4, 4, {
        (2, 3): r"bes'2\pp( | as'2 ges'2 ~ | ges'2 es'2 ~ | es'1)\>",
        (7, 3): r"ges'2\ppp( ~ | ges'1)\fermata",
    }))  # fmt: skip
    block.add("vn2", 1, r"R1*5 | ges'1\ppp\arco ~ | ges'1 ~ | ges'1\fermata |", r"\consord")
    block.add("perc1", 1, scatter(8, 4, 4, {(5, 1): r"c'1\ppp\lv"}))
    block.add("perc3", 1, scatter(8, 4, 4, {(4, 1): r"es1\pp\lv"}))
    block.add("cel.rh", 1, scatter(8, 4, 4, {(5, 4): r"d''''8\ppp( es''''8)"}))
    block.close()


# ------------------------------------------------------------------ mark X


def _turn(work: Work) -> None:
    """Mark X, bars 1 to 6: the turn. The piano goes from E-flat minor to D major."""
    structure = work.structure
    s = work.section(6, 4, 4)
    structure.mark(s.bar(1), "X")
    structure.tempo(s.bar(1), 1, LIGHT_TEMPO, "Molto adagio, luminoso")
    block = Block(s, rests(4, 4, 6))

    # The bass: E-flat to D. The middle: G-sharp to A. The bell: G-flat is now F-sharp.
    block.add(
        "pno.lh", 1,
        r"<d,, d,>2\pp\lv\sustainOff\sustainOn gis2\pp( | a1) | "
        r"<d, a,>1\ppp\lv\sustainOff\sustainOn | "
        r"r2 <d a fis'>2\pp\arpeggio | <d,, d,>1\pp\lv\sustainOff\sustainOn | R1 |",
    )  # fmt: skip
    block.add(
        "pno.rh", 1,
        r"fis'4--\ppp fis'4-- fis'2-- | r2 <a'' a'''>2\pp\lv | d'''4\pp( e''' gis''' a''') | "
        r"R1 | r2 <fis'' a'' e'''>2\pp\arpeggio | R1 |",
    )  # fmt: skip

    # The halo comes in after the piano: it holds the notes that the piano played.
    block.add("vn2", 1, r"R1 | fis'1\ppp\< ~ | fis'1\pp ~ | fis'1 ~ | fis'1 ~ | fis'1 |",
              r"\senzasord\ord\vib")  # fmt: skip
    block.add("va", 1, r"R1*2 | <a d'>1\ppp ~ | <a d'>1 ~ | <a d'>1 ~ | <a d'>1 |",
              r"\senzasord\ord\vib")  # fmt: skip
    block.add("cb", 1, r"R1*2 | d,1\ppp ~ | d,1 ~ | d,1 ~ | d,1 |", r"\senzasord")
    block.add(
        "vn1",
        1,
        r"R1*3 | <a'' d'''>1\ppp\flageolet\< ~ | <a'' d'''>1\pp ~ | <a'' d'''>1 |",
    )
    block.add("perc2", 1, r"R1 | r2 <d' fis' a'>2\pp\mallets\motoron\lv | R1*4 |")
    block.add("cel.rh", 1, r"R1 | r2 a'''2\pp\lv | r4 d''''4\ppp( e'''' gis'''' | a''''2.) r4 | "
              r"R1*2 |")  # fmt: skip
    block.add("perc4", 1, r"""\switch "glockenspiel" R1 | r2 a''2\pp\lv | R1*3 | """
              r"r4 a'''2.\pp\lv |")  # fmt: skip
    block.add("harp.lh", 1, r"R1*2 | <d, a, d>1\pp\arpeggio\lv | R1*3 |")
    block.add("harp.rh", 1, r"R1*4 | r2 <a' d'' fis''>2\pp\arpeggio\lv | R1 |")
    block.add("hn1", 1, r"R1*3 | r2 a2\ppp\< ~ | a1\pp ~ | a1\> |")
    block.add("fl2", 1, r"""\switch "flute" R1*6 |""")
    block.add("cl1", 1, r"""\switch "clarinet in B-flat" R1*6 |""")
    block.add("ob2", 1, r"""\switch "oboe" R1*6 |""")
    block.add("bn2", 1, r"""\switch "bassoon" R1*6 |""")
    block.close()


# One bar of the waves: (shape, the notes for the left hand, the notes for the right
# hand, the long note, the dynamic mark or ""). The shapes are:
# A: the left hand goes up (beat 1), the right hand goes up (beat 2), the long note (beats 3, 4).
# B: as A, but the right hand goes up for two beats. The long note is on beat 4.
# C: the long note first (beats 1, 2), then the hands go down (beats 3, 4).
# F: as A, but the long note is a full chord above a bass octave (the loudest bar).
WAVES = [
    ("A", "d, a, d e fis a", "d' e' fis' a' b' cis''", "d''", r"\pp"),
    ("C", "d, a,", "cis''' a'' fis'' e'' cis'' a' | fis' e' cis' a fis e", "e'''", ""),
    ("A", "d, a, e gis b e'", "gis' a' b' cis'' e'' fis''", "gis''", ""),
    ("A", "a,, e, a, d e a", "d' e' a' d'' e'' fis''", "a'''", r"\p"),
    ("C", "b,, g, d", "a'' fis'' d'' b' a' g' | fis' d' b a g d", "b''", r"\mp"),
    ("A", "b,, fis, b, d fis a", "d' fis' a' b' d'' fis''", "a''", ""),
    (
        "B",
        "fis,, cis, fis, ais, cis fis",
        "ais cis' fis' gis' ais' cis'' | fis'' gis'' ais'' cis''' dis''' eis'''",
        "fis'''",
        r"\pp",
    ),
    (
        "C",
        "fis,, cis, fis,",
        "ais'' gis'' fis'' eis'' cis'' ais' | gis' fis' eis' cis' ais gis",
        "cis'''",
        "",
    ),
    (
        "B",
        "bes,, f, bes, d f bes",
        "d' e' f' a' bes' d'' | e'' f'' a'' bes'' c''' d'''",
        "e'''",
        r"\p",
    ),
    ("C", "bes,, f,", "bes'' a'' f'' d'' bes' a' | f' d' bes a f d", "d'''", ""),
    ("A", "bes,, fis, bes, d fis bes", "bes d' e' fis' bes' d''", "fis''", r"\mp"),
    ("F", "a,, e, a, d fis a", "d' fis' a' d'' fis'' a''", "<d''' fis''' a''' d''''>", r"\f"),
    ("A", "a,, e, a, d e g", "b d' e' g' b' d''", "e'''", r"\mp"),
    ("C", "a,, e, a,", "b'' g'' e'' cis'' b' g' | e' cis' b g e cis", "cis'''", ""),
]


def _wave(shape: str, left: str, right: str, long: str, mark: str) -> tuple[str, str]:
    """Return one bar of a wave: the music of the right hand and of the left hand."""
    if shape in ("A", "F"):
        first = left.split()
        tail = rf"<{first[0]} {first[2]}>2" if shape == "F" else "r2"
        low = rf"\tuplet 6/4 {{ {first[0]}16{mark}{PEDAL}( {' '.join(first[1:])}) }} r4 {tail} |"
        notes = right.split()
        top = rf"\ottava #1 {long}2) \ottava #0" if shape == "F" else rf"{long}2)"
        high = rf"r4 \tuplet 6/4 {{ {notes[0]}16( {' '.join(notes[1:])} }} {top} |"
        return high, low
    if shape == "B":
        first = left.split()
        low = rf"\tuplet 6/4 {{ {first[0]}16{mark}{PEDAL}( {' '.join(first[1:])}) }} r4 r2 |"
        one, two = (part.split() for part in right.split("|"))
        high = (
            rf"r4 \tuplet 6/4 {{ {one[0]}16( {' '.join(one[1:])} }} "
            rf"\tuplet 6/4 {{ {two[0]}16 {' '.join(two[1:])} }} {long}4) |"
        )
        return high, low
    one, two = (part.split() for part in right.split("|"))
    high = rf"{long}2{mark}( \tuplet 6/4 {{ {one[0]}16 {' '.join(one[1:])}) }} r4 |"
    low = rf"<{left}>2{PEDAL}\arpeggio r4 \tuplet 6/4 {{ {two[0]}16( {' '.join(two[1:])}) }} |"
    return high, low


def _waves(work: Work) -> None:
    """Mark X, bars 7 to 22: waves of the piano. The warm theme is in the long notes, hidden."""
    structure = work.structure
    s = work.section(16, 4, 4)
    structure.tempo(s.bar(1), 1, WAVE_TEMPO, "Poco più mosso, fluido")
    block = Block(s, rests(4, 4, 16))

    right, left = [], []
    for wave in WAVES:
        high, low = _wave(*wave)
        right.append(high)
        left.append(low)
    # The last two bars: the long notes only, above the last waves of the left hand.
    right.append(r"b''2\mp( a''2) |")
    left.append(
        r"\tuplet 6/4 { a,,16\sustainOff\sustainOn( e, a, b, d g) } r4 "
        r"\tuplet 6/4 { a,,16\sustainOff\sustainOn( e, a, cis e g) } r4 |"
    )
    right.append(r"fis''2\>( e''2)\pp |")
    left.append(r"<a,, a,>1\pp\lv\sustainOff\sustainOn |")
    block.add("pno.rh", 1, " ".join(right))
    block.add("pno.lh", 1, " ".join(left))

    # The flute: the lonely melody of part 3, now with major intervals.
    block.add("fl1", 1, scatter(16, 4, 4, {
        (4, 3): r"a'4\p\dolce( b'4 | cis''2.)",
        (8, 2): r"fis''4\p( gis''4 ais''4)",
        (9, 1): r"bes''2\pp ~ bes''4",
        (12, 1): r"a'4\mf( b'4 cis''2 | \grace { d''16 } cis''4 d''4 cis''4 b'4 | "
                 r"a'2.\>) r4\!",
    }))  # fmt: skip
    block.add(
        "hn1",
        1,
        r"a1\pp ~ | a1 ~ | a1\> ~ | a1\ppp | R1*2 | cis'1\pp ~ | cis'1 | d'1 ~ | d'1 | R1 | "
        r"a1\mf\> ~ | a1 ~ | a1\pp ~ | a1 | R1 |",
    )

    # The strings hold the harmony. The first violins: natural harmonics, and their
    # highest register for the keys that have no natural harmonics.
    block.add(
        "vn1", 1,
        r"<a'' d'''>1\pp\flageolet ~ | <a'' d'''>1 | <b'' e'''>1\flageolet ~ | <b'' e'''>1 | "
        r"<d''' a'''>1\flageolet ~ | <d''' a'''>1 | <ais''' cis''''>1\ppp\sultasto ~ | "
        r"<ais''' cis''''>1 | <bes''' d''''>1\pp ~ | <bes''' d''''>1 ~ | <bes''' d''''>1\< | "
        r"<a''' d''''>1\mf\ord\> ~ | <a''' d''''>1 | <e''' a'''>1\pp\flageolet ~ | "
        r"<e''' a'''>1 ~ | <e''' a'''>1 |",
        r"\div",
    )  # fmt: skip
    block.add(
        "vn2", 1,
        r"<fis' a'>1\pp( ~ | <fis' a'>1 | <gis' b'>1 | <e' a'>1) | <fis' a'>1( ~ | <fis' a'>1) | "
        r"<fis' ais'>1\ppp( | <eis' ais'>1) | <f' bes'>1\pp( | <f' a'>1 | <fis' bes'>1\< | "
        r"<fis' a'>1\mp\>) | <e' g'>1\pp( ~ | <e' g'>1 | <d' g'>2 <cis' fis'>2 | <cis' e'>1) |",
    )  # fmt: skip
    block.add(
        "va", 1,
        r"<d' e'>1\pp( | <cis' e'>1 | <d' e'>1 | <d' e'>2 <cis' e'>2) | <b d'>1( ~ | <b d'>1) | "
        r"<ais cis'>1\ppp( ~ | <ais cis'>1) | <d' e'>1\pp( | <bes d'>1 ~ | <bes d'>1\< | "
        r"<a d'>1\mp\>) | <b d'>1\pp( | <b cis'>1 | <a b>1 | <g a>1) |",
    )  # fmt: skip
    block.add("cb", 1, scatter(16, 4, 4, {
        (1, 1): r"d,4\pp\pizz", (3, 1): r"d,4", (4, 1): r"a,,4", (5, 1): r"b,,4",
        (7, 1): r"fis,,4\ppp", (9, 1): r"bes,,4\pp", (12, 1): r"a,,4\mp", (13, 1): r"a,,4\pp",
        (16, 1): r"a,,4",
    }))  # fmt: skip

    # Bells.
    block.add("cel.rh", 1, scatter(16, 4, 4, {
        (2, 3): r"r16 cis''''8\ppp a''' cis'''' a'''16",
        (6, 3): r"r16 d''''8\ppp b''' d'''' b'''16",
        (10, 3): r"r16 d''''8\ppp a''' d'''' a'''16",
        (14, 3): r"r16 e''''8\ppp cis'''' e'''' cis''''16",
    }))  # fmt: skip
    block.add("perc2", 1, scatter(16, 4, 4, {
        (1, 1): r"<d' fis' a' e''>1\pp\lv", (3, 1): r"<e' gis' b'>1\lv",
        (5, 1): r"<b d' fis' a'>1\lv", (7, 1): r"<fis' ais' cis''>1\ppp\lv",
        (9, 1): r"<f' bes' d'' e''>1\pp\lv", (12, 1): r"<d' fis' a' d''>1\mf\lv",
        (14, 1): r"<e' g' b' cis''>1\pp\lv",
    }))  # fmt: skip
    block.add("harp.lh", 1, scatter(16, 4, 4, {
        (1, 1): r"<d,, d,>4\pp", (5, 1): r"<b,, b,>4", (7, 1): r"<fis,, fis,>4\ppp",
        (9, 1): r"<bes,, bes,>4\pp", (12, 1): r"<a,, a,>4\mp",
    }))  # fmt: skip
    block.add("perc3", 1, scatter(16, 4, 4, {(1, 1): r"d1\p\lv", (12, 1): r"d1\mp\lv"}))
    block.add("perc1", 1, scatter(16, 4, 4, {(7, 1): r"c'1\ppp\lv"}))
    block.close()


def _chorale_of_light(work: Work) -> None:
    """Mark X, bars 23 to 30: the distant chorale of part 3, now near and with whole tones."""
    structure = work.structure
    s = work.section(8, 4, 4)
    structure.tempo(s.bar(1), 1, LIGHT_TEMPO, "Tempo I, come un corale")
    block = Block(s, rests(4, 4, 8))

    block.add(
        "pno.rh", 1,
        r"<fis b e' a'>2\pp\arpeggio( <fis a d' b'>2\arpeggio | "
        r"<e' a' cis'' e''>2\arpeggio <d' fis' a' d''>2)\arpeggio | "
        r"<e a cis' a'>2\arpeggio( <fis a d' b'>2\arpeggio | "
        r"<d' fis' bes' fis''>2\p\arpeggio <cis' g' b' e''>2)\arpeggio | "
        r"<a d' fis' a'>2\pp\arpeggio( <d' e' fis' b'>2\arpeggio | "
        r"<d' fis' b' fis''>1\mp\arpeggio ~ | <d' g' b' fis''>1\>\arpeggio | "
        r"<cis' g' b' e''>1)\pp\arpeggio |",
    )  # fmt: skip
    block.add(
        "pno.lh", 1,
        r"<d, a,>2\pp\sustainOff\sustainOn <d, b,>2\sustainOff\sustainOn | "
        r"<cis, a,>2\sustainOff\sustainOn <b,, fis,>2\sustainOff\sustainOn | "
        r"<fis, cis>2\sustainOff\sustainOn <g, d>2\sustainOff\sustainOn | "
        r"<bes,, bes,>2\p\sustainOff\sustainOn <a,, a,>2\sustainOff\sustainOn | "
        r"<a,, a,>2\pp\sustainOff\sustainOn <gis,, gis,>2\sustainOff\sustainOn | "
        r"<g,, d, g,>1\mp\sustainOff\sustainOn | <a,, e, a,>1\>\sustainOff\sustainOn | "
        r"<a,, a,>1\pp\sustainOff\sustainOn |",
    )  # fmt: skip

    # The clarinet follows the highest voice one beat later, as the alto flute did it.
    block.add("cl2", 1, scatter(8, 4, 4, {
        (2, 2): r"e''2\pp\dolce( d''4 ~ | d''2)",
        (4, 2): r"fis''2\pp( e''4 ~ | e''2)",
    }))  # fmt: skip
    block.add("hn1", 1, r"R1*5 | fis'1\pp ~ | fis'1\> ~ | fis'2 e'2\ppp |")
    block.add(
        "vn1",
        1,
        r"<a'' d'''>1\ppp\flageolet ~ | <a'' d'''>1 ~ | <a'' d'''>1 ~ | <a'' d'''>1 ~ | "
        r"<a'' d'''>1 ~ | <a'' d'''>1 ~ | <a'' d'''>1 ~ | <a'' d'''>1 |",
    )
    block.add("cb", 1, r"d,1\ppp\arco ~ | d,1 ~ | d,1 ~ | d,1 | R1*4 |")
    block.close()


def _question(work: Work) -> None:
    """Mark X, bars 31 to 36: the piano asks with the first two notes of the warm theme."""
    structure = work.structure
    s = work.section(6, 4, 4)
    structure.change(s.bar(5), 1, "poco rit.")
    structure.arrive(s.bar(6), 4, 46)
    block = Block(s, rests(4, 4, 6))

    block.add(
        "pno.rh",
        1,
        r"<fis a d' e'>1\pp\arpeggio | R1*3 | r2 d'2\pp--( | e'1--) |",
    )
    block.add(
        "pno.lh",
        1,
        r"<d,, d,>1\pp\lv\sustainOff\sustainOn | R1*3 | <d,, d,>1\ppp\lv\sustainOff\sustainOn | "
        r"R1\sustainOff |",
    )
    block.add("fl1", 1, r"r2 a'4\pp( b'4 | cis''2.\>) r4\! | R1*4 |")
    # The call of the night was D and E-flat. Now it is D and E.
    block.add("cel.rh", 1, r"R1*2 | r2 r4 d''''8\pp( e''''8) | R1*3 |")
    block.add("perc2", 1, r"R1*2 | <d' a' e''>1\ppp\lv | R1*3 |")
    block.add("perc3", 1, r"R1*3 | d1\pp\lv | R1*2 |")
    block.add("harp.rh", 1, r"R1*3 | r2 <d'' a''>2\pp\flageolet | R1*2 |")
    block.add(
        "vn1",
        1,
        r"<a'' d'''>1\ppp\flageolet ~ | <a'' d'''>1 ~ | <a'' d'''>1 ~ | <a'' d'''>1 ~ | "
        r"<a'' d'''>1\> ~ | <a'' d'''>1 |",
    )
    block.add("vn2", 1, r"R1*2 | fis'1\ppp ~ | fis'1 ~ | fis'1 ~ | fis'1 |")
    block.add("va", 1, r"R1*2 | <a d'>1\ppp ~ | <a d'>1 ~ | <a d'>1 ~ | <a d'>1 |")
    block.add("cb", 1, r"R1*2 | d,1\ppp ~ | d,1 ~ | d,1 ~ | d,1 |")
    block.close()
