"""Part 4: the turn to the light, the shimmer of bells, and the main climax.

Material of this part:

- The turn: the chord of E-flat minor goes down one semitone to D major.
  The note A-flat of the motto is now G-sharp: it goes up to A. Before the
  turn it went down to G.
- The warm theme in D major. It starts with the motto in its shimmer form
  (D, E, G-sharp).
- The song theme of part 2, now in a major key, with bells that play
  interlocking patterns.
- The walking theme of part 1, now in a major key and going up.
- The keys after the turn move by major thirds: D, F-sharp, B-flat. Then
  D-flat, one semitone below the tonic, comes before the main climax.

Style profile: "Transfigured", after the turn.
"""

from __future__ import annotations

from ..compose.tools import Block, bars, double, dyn, fill, first, lines, rests, tr
from ..notation.work import Work

# The warm theme (8 bars), in D major.
WARM = r"""
    d'2( e'2 | gis'2 a'2) | b'2( a'4 fis'4 | e'1) |
    d'2( e'2 | gis'4 a'4 d''2) | cis''2( b'4 a'4 | fis'2. e'4) |
"""

# The harmony of the warm theme in four voices (from the lowest to the highest).
WARM_CHORDS = r"""
    <d a d' fis'>1 | <d b e' gis'>2 <d a d' fis'>2 | <g, b d' g'>1 | <a, a d' e'>2 <a, a cis' e'>2 |
    <fis a d' a'>1 | <b, gis d' e'>2 <a, fis d' fis'>2 | <g, b d' g'>1 |
    <a, g d' e'>2 <a, g cis' e'>2 |
"""

# The bass of the warm theme.
WARM_BASS = r"d1 | d1 | g,1 | a,1 | fis1 | b,2 a,2 | g,1 | a,1 |"

# Waves of triplets through the notes of a chord (for a full bar, and for half of a bar).
WAVE = (
    r"\tuplet 3/2 { A8( B C } \tuplet 3/2 { B8 C B } "
    r"\tuplet 3/2 { A8 B C } \tuplet 3/2 { B8 C B) }"
)
HALF_WAVE = r"\tuplet 3/2 { A8( B C } \tuplet 3/2 { B8 C B) }"

# The chords of the warm theme for the waves (three notes each).
WARM_WAVES = r"""
    <d a fis'>1 | <d b gis'>2 <d a fis'>2 | <g, d b>1 | <a, e d'>2 <a, e cis'>2 |
    <fis d' a'>1 | <b, gis e'>2 <a, fis d'>2 | <g, d b>1 | <a, g e'>2 <a, g cis'>2 |
"""

# The chords above and below the warm theme (two notes each): for the first
# violins, the second violins, and the violas.
WARM_HIGH = r"""
    <fis'' a''>1 | <gis'' b''>2 <fis'' a''>2 | <g'' b''>1 | <e'' a''>1 |
    <fis'' a''>1 | <gis'' b''>2 <fis'' a''>2 | <g'' b''>1 | <e'' g''>1 |
"""
WARM_MIDDLE = r"""
    <a' d''>1 | <b' e''>2 <a' d''>2 | <b' d''>1 | <a' e''>1 |
    <a' d''>1 | <b' e''>2 <a' d''>2 | <b' d''>1 | <a' d''>2 <a' cis''>2 |
"""
WARM_LOW = r"""
    <fis a>1 | <gis b>2 <fis a>2 | <g b>1 | <a d'>2 <a cis'>2 |
    <a d'>1 | <gis d'>2 <fis d'>2 | <g b>1 | <g d'>2 <g cis'>2 |
"""

# The song theme of part 2 in a major key (8 bars), in F-sharp.
SONG_MAJOR = r"""
    cis''2( b'4 ais'4 | gis'2. fis'4) | gis'2( fis'4 eis'4 | fis'1) |
    cis''2\<( dis''4 eis''4 | fis''2.\> eis''4 | dis''2 cis''4 b'4 | cis''1\!) |
"""

# The bells for F-sharp major, with the notes of the scale of five notes.
PENTA_ON_BEAT = r"fis'''8 cis'''' fis''' cis'''' fis''' cis'''' fis''' cis'''' |"
PENTA_OFF_BEAT = r"r16 gis'''8 dis'''' gis''' dis'''' gis''' dis'''' gis''' dis''''16 |"

# Two bell instruments play alternate notes: together they make one fast line.
# These are the notes of the motto in its shimmer form, and the note A.
BELLS_ON_BEAT = r"d'''8 gis''' d''' gis''' d''' gis''' d''' gis''' |"
BELLS_OFF_BEAT = r"r16 e'''8 a''' e''' a''' e''' a''' e''' a'''16 |"


def write(work: Work) -> None:
    _turn(work)
    _warm_theme(work)
    _shimmer(work)
    _broad(work)
    _approach(work)
    _main_climax(work)
    _calm(work)


def _turn(work: Work) -> None:
    """Bars 263 to 266: D major, very soft. The bells play the motto in its shimmer form."""
    structure = work.structure
    s = work.section(4, 4, 4)
    structure.mark(s.bar(1), "W")
    structure.tempo(s.bar(1), 1, 52, "Molto adagio, luminoso")
    block = Block(s, rests(4, 4, 4))

    block.add("vn2", 1, r"fis'1\pp ~ | fis'1 ~ | fis'1 ~ | fis'1 |", r"\ord\vib")
    block.add("va", 1, r"<a d'>1\pp ~ | <a d'>1 ~ | <a d'>1 ~ | <a d'>1 |", r"\ord\vib")
    block.add("cb", 1, r"d,1\pp ~ | d,1 ~ | d,1 ~ | d,1 |")
    block.add("vn1", 1, r"R1 | <fis'' a''>1\ppp\< ~ | <fis'' a''>1 ~ | <fis'' a''>1\pp |",
              r"\ord\vib")  # fmt: skip
    block.add("perc2", 1, r"<d' fis' a'>1\pp\motoron\lv | R1*3 |")
    block.add("harp.lh", 1, r"<d, a, d>1\pp\arpeggio\lv | R1*3 |")
    block.add("cel.rh", 1, r"R1 | d'''4\pp( e''' gis''' a''') | " + dyn(BELLS_ON_BEAT * 2, r"\ppp"))
    block.add("harp.rh", 1, r"R1*2 | " + dyn(BELLS_OFF_BEAT * 2, r"\ppp"))
    block.add("perc4", 1, r"""\switch "glockenspiel" R1*2 | r2 a''2\pp\lv | R1 |""")
    block.add("cl1", 1, r"""\switch "clarinet in B-flat" R1*4 |""")
    block.add("ob2", 1, r"""\switch "oboe" R1*4 |""")
    block.add("fl2", 1, r"""\switch "flute" R1*4 |""")
    block.close()


def _warm_theme(work: Work) -> None:
    """Bars 267 to 282: the warm theme, two times."""
    structure = work.structure
    s = work.section(16, 4, 4)
    structure.mark(s.bar(1), "X")
    eight = rests(4, 4, 8)
    block = Block(s, eight, eight)

    # The first time: the cellos sing. The violins are a soft light above.
    theme = first(WARM, r"\p\espr\tutti\senzasord\ord\vib", note=True)
    block.add("vc", 1, theme)
    block.add("hn1", 1, r"R1*4 | " + dyn(WARM.split("|", 4)[4], r"\p\dolce"))
    block.add(
        "va", 1,
        r"<fis a>1\pp( | <gis b>2 <fis a>2) | <g b>1( | <a d'>2 <a cis'>2) | "
        r"<a d'>1( | <gis d'>2 <fis d'>2) | <g b>1( | <g d'>2 <g cis'>2) |",
    )  # fmt: skip
    block.add(
        "vn2", 1,
        r"<a' d''>1\pp( | <b' e''>2 <a' d''>2) | <b' d''>1( | <a' e''>1) | "
        r"<a' d''>1( | <b' e''>2 <a' d''>2) | <b' d''>1( | <a' d''>2 <a' cis''>2) |",
    )  # fmt: skip
    block.add(
        "vn1", 1,
        r"<fis'' a''>1\pp( | <gis'' b''>2 <fis'' a''>2) | <g'' b''>1( | <e'' a''>1) | "
        r"<fis'' a''>1( | <gis'' b''>2 <fis'' a''>2) | <g'' b''>1( | <e'' g''>1) |",
    )  # fmt: skip
    block.add("cb", 1, r"d,1\pp( | d,1) | g,,1( | a,,1) | fis,1( | b,,2 a,,2) | g,,1( | a,,1) |")
    block.add("cel.rh", 1, dyn(BELLS_ON_BEAT * 2, r"\ppp") + r"R1*2 | "
              + dyn(BELLS_ON_BEAT * 2, r"\ppp") + r"R1*2 |")  # fmt: skip
    block.add("harp.rh", 1, dyn(BELLS_OFF_BEAT * 2, r"\ppp") + r"R1*2 | "
              + dyn(BELLS_OFF_BEAT * 2, r"\ppp") + r"R1*2 |")  # fmt: skip

    # The second time: the violins sing in octaves. Horns and bassoons give the harmony.
    block.add("vn1:1 vn2", 2, dyn(WARM, r"\p\espr"))
    second_half = WARM.split("|", 4)[4]
    block.add("fl1:1 ob1", 2, r"R1*4 | " + dyn(second_half, r"\p\dolce"))
    block.spread("hn4 hn3 hn2 hn1", 2, dyn(WARM_CHORDS, r"\p"))
    block.add("bn1 bn2 cb:-1", 2, dyn(WARM_BASS, r"\p"))
    block.add("vc", 2, fill(WARM_WAVES, {4: WAVE, 2: HALF_WAVE}), r"\p")
    block.add(
        "va", 2,
        r"a2\p( b2 | b2 a2) | g2( b4 d'4 | d'2 cis'2) | "
        r"a2( ais2 | b2 a2) | b2( cis'4 d'4 | d'2 cis'2) |",
    )  # fmt: skip
    block.add("perc2", 2, r"<d' fis' a'>1\p\lv | R1*3 | <d' fis' a'>1\lv | R1*3 |")
    block.close()


def _shimmer(work: Work) -> None:
    """Bars 283 to 306: the song theme in F-sharp major, with interlocking bells."""
    structure = work.structure
    s = work.section(24, 4, 4)
    structure.mark(s.bar(1), "Y")
    structure.tempo(s.bar(1), 1, 66, "Più mosso, scintillante")
    two, four, eight = rests(4, 4, 2), rests(4, 4, 4), rests(4, 4, 8)
    block = Block(s, two, two, eight, eight, four)

    # Phrase 1 (2 bars): the theme arrives on D. The bells continue.
    block.add("vn1:1 vn2 fl1:1 ob1", 1, r"d''1\mf\> ~ | d''1\pp |")
    block.spread("hn4 hn3 hn2 hn1", 1, r"<d a d' fis'>1\p\> ~ | <d a d' fis'>1\pp |")
    block.add("bn1 bn2 cb:-1", 1, r"d1\p\> ~ | d1\pp |")
    block.add("vc", 1, first(fill(r"<d a fis'>1 |", WAVE), r"\p\>", note=True)
              + first(fill(r"<d a fis'>1 |", WAVE), r"\pp", note=True))  # fmt: skip
    block.add("va", 1, r"a2\mp\>( fis2 ~ | fis1)\pp |")
    block.add("cel.rh", 1, dyn(BELLS_ON_BEAT * 2, r"\pp"))
    block.add("harp.rh", 1, dyn(BELLS_OFF_BEAT * 2, r"\pp"))
    block.add("perc2", 1, r"<d' fis' a'>1\p\lv | R1 |")

    # Phrase 2 (2 bars): the harmony moves a major third up, to F-sharp.
    on_beat, off_beat = tr(PENTA_ON_BEAT, 0), tr(PENTA_OFF_BEAT, 0)
    block.add("vn2", 2, r"<fis' ais'>1\pp ~ | <fis' ais'>1 |")
    block.add("vc", 2, r"<fis cis'>1\pp ~ | <fis cis'>1 |")
    block.add("cb", 2, r"fis,1\pp ~ | fis,1 |")
    block.add("cel.rh", 2, dyn(tr(BELLS_ON_BEAT, 4) * 2, r"\pp"))
    block.add("harp.rh", 2, dyn(tr(BELLS_OFF_BEAT, 4) * 2, r"\pp"))
    block.add("perc4", 2, r"fis'''4\pp ais''' cis'''' ais''' | fis'''4 ais''' cis'''' ais''' |")
    block.add("perc2", 2, r"<fis' cis''>2\pp <gis' dis''>2 | <fis' cis''>2 <gis' dis''>2 |")
    block.add("perc3", 2, r"""\switch "tubular bells" fis'1\p\lv | R1 |""")
    block.add("mand", 2, r"ais''1:32\ppp ~ | ais''1:32 |")
    block.add("cimb.lh", 2, r"<fis cis'>1:32\ppp ~ | <fis cis'>1:32 |")

    # Phrase 3 (8 bars): the song theme in the clarinet.
    block.add("cl1", 3, first(SONG_MAJOR, r"\p\dolce", note=True))
    block.add("fl1:1", 3, r"R1*4 | " + dyn(SONG_MAJOR.split("|", 4)[4], r"\pp"))
    rocking = {4: r"A8( B A B A B A B)", 2: r"A8( B A B)"}
    block.add(
        "va", 3,
        fill(
            r"<ais cis'>1\pp | <b dis'>1 | <b eis'>1 | <ais cis'>1 | "
            r"<ais cis'>1 | <b dis'>1 | <b dis'>2 <b eis'>2 | <ais cis'>1 |",
            rocking,
        ),
        r"\senzasord",
    )  # fmt: skip
    block.add("vc", 3, r"fis1\pp( | b,1) | cis1( | fis1) | ais,1( | b,1) | gis,2( cis2 | fis,1) |")
    block.add(
        "cb", 3,
        r"fis,4\p\pizz\senzasord r r2 | b,,4 r r2 | cis,4 r r2 | fis,4 r r2 | "
        r"ais,,4 r r2 | b,,4 r r2 | gis,,4 r cis,4 r | fis,4 r r2 |",
    )  # fmt: skip
    quiet = {3: "R1 |", 7: "R1 |"}
    block.add("cel.rh", 3, dyn(bars(8, on_beat, quiet), r"\pp"))
    block.add("harp.rh", 3, dyn(bars(8, off_beat, quiet), r"\pp"))
    chime = r"fis'''4\pp ais''' cis'''' ais''' |"
    block.add("perc4", 3, bars(8, "R1 |", {1: chime, 4: chime, 8: chime}))
    block.add(
        "perc2", 3,
        r"<fis' ais'>1\pp\lv | <fis' b'>1 | <eis' gis'>1 | <fis' ais'>1 | "
        r"<eis' ais'>1 | <fis' b'>1 | <gis' b'>1 | <fis' ais'>1 |",
    )  # fmt: skip
    block.add("perc3", 3, r"fis'1\p\lv | R1*3 | fis'1\lv | R1*3 |")

    # Phrase 4 (8 bars): the song theme in the violins and the oboe. The horns answer.
    block.add("ob1 fl1:1", 4, first(SONG_MAJOR, r"\p\cantabile", note=True))
    block.add("vn1 vn2", 4, first(SONG_MAJOR, r"\p\cantabile\senzasord", note=True))
    block.add(
        "hn1 hn3", 4,
        r"fis'2\p( gis'2 | b'1) | gis'2( eis'2 | fis'1) | "
        r"cis''2( b'2 | ais'2 gis'2) | gis'2( eis'2 | fis'1) |",
    )  # fmt: skip
    block.add(
        "vc", 4,
        fill(
            r"<fis, cis ais>1 | <b, fis dis'>1 | <cis gis eis'>1 | <fis, cis ais>1 | "
            r"<ais, eis cis'>1 | <b, fis dis'>1 | <gis, dis b>2 <cis gis eis'>2 | "
            r"<fis, cis ais>1 |",
            {4: WAVE, 2: HALF_WAVE},
        ),
        r"\p",
    )  # fmt: skip
    block.add(
        "va", 4,
        r"<ais cis'>1\p( | <b dis'>1) | <b eis'>1( | <ais cis'>1) | "
        r"<cis' eis'>1( | <b dis'>1) | <b dis'>2( <b eis'>2 | <ais cis'>1) |",
    )  # fmt: skip
    block.add(
        "cb",
        4,
        r"fis,1\p\arco( | b,,1) | cis,1( | fis,1) | ais,,1( | b,,1) | gis,,2( cis,2 | fis,1) |",
    )
    block.add("bn1", 4, r"ais1\p( | b1) | b1( | ais1) | cis'1( | b1) | b2( b2 | ais1) |")
    block.add("bn2", 4, r"fis1\p( | dis1) | eis1( | fis1) | eis1( | fis1) | dis2( eis2 | cis1) |")
    block.add("cel.rh", 4, dyn(bars(8, on_beat, quiet), r"\p"))
    block.add("harp.rh", 4, dyn(bars(8, off_beat, quiet), r"\p"))
    peal = r"fis'''8\p gis''' ais''' cis'''' dis'''' cis'''' ais''' gis''' |"
    block.add("perc4", 4, bars(8, peal, quiet))
    block.add(
        "perc2", 4,
        r"<fis' ais'>1\p\lv | <fis' b'>1 | <eis' gis'>1 | <fis' ais'>1 | "
        r"<eis' ais'>1 | <fis' b'>1 | <gis' b'>1 | <fis' ais'>1 |",
    )  # fmt: skip
    block.add("perc3", 4, r"fis'1\mp\lv | R1*3 | fis'1\lv | R1*3 |")
    high = r"<cis''' cis''''>4\p r4 r2 |"
    block.add("pno.rh", 4, bars(8, "R1 |", {1: high, 3: high, 5: high, 7: high}))
    block.add(
        "mand", 4, r"cis'''1:32\pp ~ | cis'''1:32 | R1*2 | cis'''1:32 ~ | cis'''1:32 | R1*2 |"
    )

    # Phrase 5 (4 bars): the way to B-flat major.
    block.add(
        "vn1 vn2:-1 fl1:1 ob1", 5,
        r"des''2\mf\<( es''4 f''4 | ges''1) | ges''2\f( f''2 ~ | f''1) |",
    )  # fmt: skip
    block.add("va", 5, r"<bes des'>1\mf ~ | <bes des'>1 | <a es'>1\< ~ | <a es'>1\f |")
    block.add(
        "vc", 5,
        fill(r"<ges, des bes>1 | <ges, des bes>1 | <f, c a>1 | <f, c a>1 |", WAVE), r"\mf",
    )  # fmt: skip
    block.add("cb", 5, r"ges,1\mf ~ | ges,1 | f,1\< ~ | f,1\f |")
    block.spread("hn4 hn3 hn2 hn1", 5, r"R1*2 | <f c' es' a'>1\mp\< ~ | <f c' es' a'>1\f |")
    block.add("bn1 bn2", 5, r"ges1\mp ~ | ges1 | f1\< ~ | f1\f |")
    block.add("timp", 5, r"R1*2 | f,1:32\p\< ~ | f,1:32\f |")
    block.add("cel.rh", 5, dyn(on_beat * 2, r"\p") + r"R1*2 |")
    block.add("harp.rh", 5, dyn(off_beat * 2, r"\p") + r"R1*2 |")
    block.close()


def _broad(work: Work) -> None:
    """Bars 307 to 330: the warm theme in B-flat major, then the way to D-flat."""
    structure = work.structure
    s = work.section(24, 4, 4)
    structure.mark(s.bar(1), "Z")
    structure.tempo(s.bar(1), 1, 58, "Largamente, con calore")
    four, eight = rests(4, 4, 4), rests(4, 4, 8)
    block = Block(s, eight, eight, four, four)

    theme, chords, bass = tr(WARM, -4), tr(WARM_CHORDS, -4), tr(WARM_BASS, -4)
    throb = {4: r"r8 X4 X4 X4 X8", 2: r"r8 X4 X8"}

    # Phrase 1 (8 bars): the theme in the four horns and the cellos.
    block.add("hn1 hn2 hn3 hn4 vc", 1, dyn(theme, r"\mf\espr"))
    block.add("vn1", 1, fill(tr(WARM_HIGH, -4), throb), r"\p")
    block.add("vn2", 1, fill(tr(WARM_MIDDLE, -4), throb), r"\p")
    block.add("va", 1, fill(tr(WARM_LOW, 8), throb), r"\p")
    block.add("cb:-1 bn1 bn2 bn3:-1", 1, dyn(bass, r"\mp"))
    low, middle, upper, _top = lines(chords)
    block.add("btbn tuba:-1", 1, dyn(low, r"\p"))
    block.add("tbn2", 1, dyn(middle, r"\p"))
    block.add("tbn1", 1, dyn(upper, r"\p"))
    block.add("timp", 1, r"bes,2:32\mp\> r2\! | R1*7 |")

    # Phrase 2 (8 bars): the theme in the violins and woodwinds. The agitated
    # theme of part 2 is now a warm line in the cellos.
    high_theme = tr(WARM, 8)
    block.add("vn1 vn2 fl1:1 fl2:1 ob1 ob2 cl1 cl2", 2, dyn(high_theme, r"\f\espr"))
    block.add(
        "vc bn1 cl3:-1", 2,
        r"r8 bes8\mf\espr( c'4 ~ c'8 f'8 d'4) | r8 c'8( e'4 ~ e'8 d'8 bes4) | "
        r"r8 bes8( c'4 ~ c'8 g'8 es'4) | r8 c'8( d'4 ~ d'8 c'8 a4) | "
        r"r8 d'8( f'4 ~ f'8 bes'8 f'4) | r8 e'8( g'4) r8 d'8( f'4) | "
        r"r8 es'8( g'4 ~ g'8 bes'8 g'4) | r8 f'8( es'4 ~ es'8 d'8 c'4) |",
    )  # fmt: skip
    block.spread("hn4 hn3 hn2 hn1", 2, dyn(chords, r"\mf"))
    block.add("va", 2, fill(tr(WARM_LOW, 8), throb), r"\mf")
    block.add("cb:-1 bn2 bn3:-1 tuba:-1", 2, dyn(bass, r"\mf"))
    block.add("tbn2", 2, dyn(middle, r"\mp"))
    block.add("tbn1", 2, dyn(upper, r"\mp"))
    block.add(
        "timp", 2, r"bes,4\mf r r2 | R1*2 | f,1:32\p\< | bes,4\mf r r2 | R1*2 | f,1:32\mp\< |"
    )

    # Phrase 3 (4 bars): the motto in its shimmer form, on G-flat and on D-flat.
    block.add("fl1:1 fl2:1 ob1 ob2 cl1", 3, r"ges'2\mf( as'2 | c''2 des''2) | R1*2 |")
    block.add("hn1 hn2 hn3 hn4", 3, r"R1*2 | des'2\mf( es'2 | g'2 as'2) |")
    block.add("vn1", 3, r"<des'' ges''>1\mp( ~ | <des'' ges''>1 | <des'' f''>1 ~ | <des'' f''>1) |")
    block.add("vn2", 3, r"<bes' des''>1\mp( ~ | <bes' des''>1 | <as' des''>1 ~ | <as' des''>1) |")
    block.add("va", 3, r"<ges bes>1\mp( ~ | <ges bes>1 | <f as>1 ~ | <f as>1) |")
    block.add("vc", 3, r"<ges, des>1\mp( ~ | <ges, des>1 | <as, f>1 ~ | <as, f>1) |")
    block.add("cb", 3, r"ges,,1\mp( ~ | ges,,1 | as,,1 ~ | as,,1) |")

    # Phrase 4 (4 bars): the dominant of D-flat. The sound grows.
    swell = r"X1:32\p\< ~ | X1:32 ~ | X1:32 ~ | X1:32\f |"
    block.add("vn1", 4, fill(r"<c'' ges''>1", swell))
    block.add("vn2", 4, fill(r"<as' es''>1", swell))
    block.add("va", 4, fill(r"<ges c'>1", swell))
    block.add("vc", 4, fill(r"<as, es>1", swell))
    block.add("cb", 4, fill(r"<as,,>1", swell.replace("X", "A")))
    block.add("timp", 4, fill(r"<as,>1", swell.replace("X", "A")))
    block.add("tpt1", 4, r"R1*2 | as'8->\mf bes'8-> es''2.-> | R1 |", r"\senzasord")
    block.spread("hn4 hn3 hn2 hn1", 4, r"<as, es ges c'>1\p\< ~ | <as, es ges c'>1 ~ | "
                 r"<as, es ges c'>1 ~ | <as, es ges c'>1\f |")  # fmt: skip
    block.close()


def _approach(work: Work) -> None:
    """Bars 331 to 358: the way up to the main climax, above the bass note D-flat.

    The walking theme of part 1 is now in a major key and goes up. The calls
    of the brass have the motto in its light form (D-flat, E-flat, A-flat).
    In the last bars, all voices go up one semitone, to the dominant of D.
    """
    structure = work.structure
    s = work.section(28, 4, 4)
    structure.mark(s.bar(1), "AA")
    structure.tempo(s.bar(1), 1, 60, "Con moto")
    structure.change(s.bar(5), 1, "poco a poco più mosso")
    structure.arrive(s.bar(21), 1, 76)
    structure.change(s.bar(27), 1, "allargando")
    block = Block(s, *[rests(4, 4, 4)] * 7)

    walk = r"des4.( es8 f4. ges8 | as2.) r4 | as4.( bes8 c'4. des'8 | es'2.) r4 |"
    walk_on_e_flat = (
        r"es'4.( f'8 ges'4. as'8 | bes'2.) r4 | bes'4.( c''8 des''4. es''8 | f''2.) r4 |"
    )
    walk_on_a_flat = (
        r"as'4.( bes'8 c''4. des''8 | es''2.) r4 | es''4.( f''8 ges''4. as''8 | bes''2.) r4 |"
    )
    call = r"des'8-> es'8-> as'2.-> |"
    song = r"as''2( ges''4 f''4 | es''2. des''4) |"
    held = r"X1 ~ | X1 ~ | X1 ~ | X1 |"
    pedal = r"A1 ~ | A1 ~ | A1 ~ | A1 |"

    # Unit 1: the walking theme in the cellos, soft.
    block.add("vc bn1 cl3", 1, walk, r"\p\espr")
    block.spread("hn4 hn3 hn2 hn1", 1, fill(r"<des as des' f'>1", held), r"\pp")
    block.add("cb", 1, fill(r"<des,>1", pedal), r"\pp\arco")
    block.add("timp", 1, r"des4\pp r r2 | R1 | des4 r r2 | R1 |")

    # Unit 2: the theme a fourth higher. The woodwinds have the song theme.
    block.add("va cl1", 2, tr(walk, 5), r"\p\espr")
    block.add("vc", 2, fill(r"<des bes>1", held), r"\p")
    block.spread("hn4 hn3 hn2 hn1", 2, fill(r"<des ges bes des'>1", held), r"\p")
    block.add("cb", 2, fill(r"<des,>1", pedal), r"\p")
    block.add("timp", 2, r"des4\p r r2 | R1 | des4 r r2 | R1 |")
    block.add("fl1 ob1:-1", 2, r"R1*2 | " + song, r"\p")

    # Unit 3: the theme on E-flat. The first calls.
    block.add("vn2 va", 3, walk_on_e_flat, r"\mp\espr")
    block.add("vc", 3, fill(r"<ges bes>1", held), r"\mp")
    block.spread("hn4 hn3 hn2 hn1", 3, fill(r"<des ges bes es'>1", held), r"\mp")
    block.add("cb bn3", 3, fill(r"<des,>1", pedal), r"\mp")
    block.add("timp", 3, r"des4\mp r des4 r | des4 r des4 r | des4 r des4 r | des4 r des4 r |")
    block.add("tpt1", 3, bars(4, "R1 |", {3: tr(call, 7)}), r"\mp")
    block.add("tbn1", 3, bars(4, "R1 |", {4: tr(call, -10)}), r"\mp")

    # Unit 4: the theme in the violins, on A-flat. A call in each bar.
    block.add("vn1:1 vn2", 4, walk_on_a_flat, r"\mf\<")
    block.add("va", 4, fill(r"<ges c'>1", held), r"\mf\<")
    block.add("vc", 4, fill(r"<as es'>1", held), r"\mf\<")
    block.spread("hn4 hn3 hn2 hn1", 4, fill(r"<as c' es' ges'>1", held), r"\mf\<")
    block.add("cb bn3 tuba", 4, fill(r"<des,>1", pedal), r"\mf\<")
    block.add("timp", 4, r"des1:32\mp\< ~ | des1:32 ~ | des1:32 ~ | des1:32 |")
    block.add("tpt1 tpt2", 4, bars(4, "R1 |", {1: tr(call, 7), 3: tr(call, 14)}), r"\mf")
    block.add("tbn1 tbn2", 4, bars(4, "R1 |", {2: tr(call, -10), 4: tr(call, -5)}), r"\mf")
    block.add(
        "fl1:1 fl2:1 ob1 ob2 cl1 cl2", 4,
        r"es''2( des''4 c''4 | bes'2. as'4) | ges''2( f''4 es''4 | des''2. c''4) |", r"\mf",
    )  # fmt: skip

    # Unit 5: the walking theme in all strings, loud: a hymn.
    block.add("vn1:2 vn2:1 va:1 vc cb:-1", 5, walk, r"\f")
    block.add(
        "fl1 fl2 fl3:1 ob1:-1 ob2:-1 cl1:-1 cl2:-1", 5,
        song + r"f''2( es''4 des''4 | c''2. des''4) |", r"\f",
    )  # fmt: skip
    block.spread("hn4 hn3 hn2 hn1", 5, fill(r"<des as des' f'>1", held), r"\f")
    block.add("tuba bn3 bn2:1 bn1:1", 5, fill(r"<des,>1", pedal), r"\f")
    block.add("timp", 5, r"des1:32\f ~ | des1:32 ~ | des1:32 ~ | des1:32 |")
    block.add("tpt1 tpt2 tpt3", 5, bars(4, "R1 |", {1: tr(call, 12), 3: tr(call, 7)}), r"\f")
    block.add("tbn1 tbn2 hn5 hn6", 5, bars(4, "R1 |", {2: tr(call, -5), 4: call}), r"\f")

    # Unit 6: the theme two times faster. Each bar is one step higher.
    fast = (
        r"des'8( es' f' ges' as'2) | es'8( f' ges' as' bes'2) | "
        r"f'8( ges' as' bes' c''2) | ges'8( as' bes' c'' des''2) |"
    )
    block.add("vn1:1 vn2:1 va vc:-1 cb:-2", 6, fast, r"\ff")
    block.add("fl1:2 fl2:2 fl3:2 ob1:1 ob2:1 cl1:1 cl2:1", 6, fast, r"\ff")
    chords = fill(r"<ges, des ges bes>1", held)
    block.spread("hn4 hn3 hn2 hn1", 6, chords, r"\ff")
    block.add("tuba bn3 bn2:1 bn1:1 btbn", 6, r"ges,1 ~ | ges,1 | es,1 ~ | es,1 |", r"\ff")
    block.add("timp", 6, r"ges,1:32\f ~ | ges,1:32 | es1:32 ~ | es1:32 |")
    block.add("tpt1 tpt2 tpt3", 6, bars(4, "R1 |", {1: tr(call, 5), 3: tr(call, 9)}), r"\ff")
    block.add("tbn1 tbn2 hn5 hn6", 6, bars(4, "R1 |", {2: tr(call, -7), 4: tr(call, -3)}), r"\ff")
    block.add("perc3", 6, r"""\switch "bass drum" R1*2 | c'1:32\p\< ~ | c'1:32\f |""")

    # Unit 7: the dominant of D-flat, then all voices one semitone up: the dominant of D.
    lift = r"X1:32 ~ | X1:32 |"
    for players, chord in [("vn1", r"<c''' ges'''>1"), ("vn2", r"<es'' as''>1"),
                           ("va", r"<ges' c''>1"), ("vc", r"<as es'>1")]:  # fmt: skip
        block.add(players, 7, first(fill(chord, lift), r"\ff\<", note=True)
                  + first(fill(tr(chord, 1), lift), r"\fff", note=True))  # fmt: skip
    brass = r"<as, es ges c' es' as' c''>1-^ ~ | <as, es ges c' es' as' c''>1 |"
    voices_flat, voices_up = lines(brass), lines(tr(brass, 1))
    names = ["btbn", "tbn2", "tbn1", "hn2", "tpt3", "tpt2", "tpt1"]
    for name, before, after in zip(names, voices_flat, voices_up, strict=True):
        block.add(name, 7, first(before, r"\ff\<", note=True) + first(after, r"\fff", note=True))
    block.add("hn1 hn3", 7, first(voices_flat[4], r"\ff\<", note=True)
              + first(voices_up[4], r"\fff", note=True))  # fmt: skip
    block.add("hn4 hn5 hn6", 7, first(voices_flat[2], r"\ff\<", note=True)
              + first(voices_up[2], r"\fff", note=True))  # fmt: skip
    block.add("cb tuba bn3 bn2:1 bn1:1 cl3:1", 7, r"as,,1\ff\< ~ | as,,1 | a,,1\fff ~ | a,,1 |")
    block.add("timp", 7, r"as,1:32\ff\< ~ | as,1:32 | a,1:32\fff ~ | a,1:32 |")
    block.add(
        "fl1 fl2 fl3 ob1:-1 ob2:-1 cl1:-1 cl2:-1", 7,
        r"c'''1\ff\< ~ | c'''1 | cis'''1\fff ~ | cis'''2 "
        r"a''16( b'' cis''' d''' e''' fis''' g''' a''') |",
    )  # fmt: skip
    block.add("perc3", 7, r"c'1:32\f\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32\fff |")
    block.add(
        "perc1", 7,
        r"""\switch "suspended cymbals" c'1:32\p\< ~ | c'1:32 ~ | c'1:32 ~ | c'1:32\fff |""",
    )  # fmt: skip
    block.close()


def _main_climax(work: Work) -> None:
    """Bars 359 to 370: the warm theme in D major with the full orchestra, fff."""
    structure = work.structure
    s = work.section(12, 4, 4)
    structure.mark(s.bar(1), "BB")
    structure.tempo(s.bar(1), 1, 54, "Maestoso, con tutta la forza")
    block = Block(s, rests(4, 4, 8), rests(4, 4, 4))

    # Phrase 1 (8 bars): the theme.
    theme = dyn(WARM, r"\fff")
    block.add("vn1:1 vn2:1 va vc tpt1 tpt2 hn5 hn6", 1, theme)
    block.add("fl1:2 fl2:2 fl3:2 ob1:1 ob2:1 cl1:1 cl2:1 perc4:2", 1, theme)
    bass, tenor, alto, top = lines(dyn(WARM_CHORDS, r"\fff"))
    block.add("hn4 btbn bn1 bn2 cl3 tuba:-1 bn3:-1 cb:-1", 1, bass)
    block.add("hn3 tbn2", 1, tenor)
    block.add("hn2 tbn1", 1, alto)
    block.add("hn1 tpt3", 1, top)
    block.add("pno.lh", 1, double(dyn(WARM_BASS, r"\fff"), -1))
    full = {4: r"<B C D B' C' D'>1", 2: r"<B C D B' C' D'>2"}
    rolled = {4: full[4] + r"\arpeggio", 2: full[2] + r"\arpeggio"}
    block.add("pno.rh", 1, fill(dyn(WARM_CHORDS, r"\fff"), full))
    block.add("harp.rh", 1, fill(dyn(WARM_CHORDS, r"\ff"), rolled))
    block.add(
        "timp", 1,
        r"d,1:32\fff | d,1:32 | g,1:32 | a,1:32 | d,1:32 | a,1:32 | g,1:32 | a,1:32 |",
    )  # fmt: skip
    block.add(
        "perc2", 1,
        r"""\switch "tubular bells" d'1\fff | gis'1 | b'1 | e'1 | """
        r"d'1 | gis'2 d''2 | cis''1 | fis'1 |",
    )  # fmt: skip
    block.add("perc1", 1, r"""\switch "tam-tams" c'1\fff\lv | R1*7 |""")
    block.add("perc3", 1, r"c'4\fff r r2 | R1 | c'4 r r2 | R1 | c'4 r r2 | R1 | c'4 r r2 | R1 |")
    block.start("perc4", r'\switch "glockenspiel"')

    # Phrase 2 (4 bars): the tonic. The motto in its light form, in long notes.
    motto = r"d'1\fff-^ | e'1-^ | a'1-^\> ~ | a'1\mf |"
    block.add("tpt1 tpt2 tpt3 hn1 hn2 hn3 hn4 hn5 hn6 tbn1:-1 tbn2:-1", 2, motto)
    fade = r"X1:32\fff ~ | X1:32\> ~ | X1:32 ~ | X1:32\mf |"
    block.add("vn1", 2, fill(r"<fis'' d'''>1", fade))
    block.add("vn2", 2, fill(r"<a' fis''>1", fade))
    block.add("va", 2, fill(r"<d' a'>1", fade))
    block.add("vc", 2, fill(r"<d a>1", fade))
    block.add(
        "cb btbn tuba bn3 bn1:1 bn2:1", 2, fill(r"<d,>1", r"A1\fff ~ | A1\> ~ | A1 ~ | A1\mf |")
    )
    block.add("timp", 2, r"d,1:32\fff ~ | d,1:32\> ~ | d,1:32 ~ | d,1:32\mp |")
    block.add("fl1:1 fl2:1 fl3:1 ob1 ob2 cl1 cl2", 2, r"d''1\fff ~ | d''1\> ~ | d''1 ~ | d''1\mf |")
    block.add("perc2", 2, r"d'1\fff | e'1 | a'1 | R1 |")
    block.add("perc4", 2, r"d'''1\ff | e'''1 | a'''1 | R1 |")
    block.add("perc1", 2, r"c'1\ff\lv | R1*3 |")
    block.add("perc3", 2, r"c'4\fff r r2 | R1*3 |")
    block.add("pno.lh", 2, r"<d,, d,>1\fff | R1*3 |")
    block.add("harp.rh", 2, r"<d' fis' a' d'' fis'' a''>1\ff\arpeggio | R1*3 |")
    block.close()


def _calm(work: Work) -> None:
    """Bars 371 to 398: calm after the climax. The themes come back as soft solos."""
    structure = work.structure
    s = work.section(28, 4, 4)
    structure.mark(s.bar(1), "CC")
    structure.tempo(s.bar(1), 1, 52, "Tranquillo")
    structure.change(s.bar(25), 1, "poco rit.")
    structure.arrive(s.bar(28), 1, 44)
    four, eight = rests(4, 4, 4), rests(4, 4, 8)
    block = Block(s, eight, eight, eight, four)

    # Phrase 1 (8 bars): one violin has the motto: the shimmer form, then the light form.
    block.add(
        "vn1", 1,
        r"d'''2\p\dolce\solo( e'''2 | gis'''2 a'''2) | b'''2( a'''4 fis'''4 | e'''1) | "
        r"d'''2( e'''2 | a'''1 ~ | a'''1\>) | R1\! |",
    )  # fmt: skip
    block.add(
        "vn2", 1,
        r"<fis' a'>1\pp( | <g' b'>1) | <fis' a'>1( | <e' g'>1) | "
        r"<fis' a'>1( | <g' b'>1) | <fis' a'>1 ~ | <fis' a'>1 |",
    )  # fmt: skip
    block.add(
        "va", 1,
        r"<a d'>1\pp( | <b d'>1) | <a d'>1( | <b d'>1) | <a d'>1( | <b d'>1) | "
        r"<a d'>1 ~ | <a d'>1 |",
    )  # fmt: skip
    block.add(
        "vc", 1,
        r"<d a>1\pp( | <d g>1) | <d a>1( | <d g>1) | <d a>1( | <d g>1) | <d a>1 ~ | <d a>1 |",
    )  # fmt: skip
    block.add("cb", 1, r"d,1\pp ~ | " + r"d,1 ~ | " * 6 + r"d,1 |")
    chime = r"<d'' a''>4\pp r r2 |"
    block.add("harp.rh", 1, bars(8, "R1 |", {1: chime, 3: chime, 5: chime, 7: chime}))

    # Phrase 2 (8 bars): one horn has the song theme.
    block.add("hn1", 2, first(tr(SONG_MAJOR, -4), r"\p\dolce\solo", note=True))
    block.add(
        "vn1", 2,
        r"<fis'' a''>1\pp\tutti( | <g'' b''>1) | <e'' g''>1( | <fis'' a''>1) | "
        r"<fis'' a''>1( | <g'' b''>1) | <e'' g''>1( | <fis'' a''>1) |",
    )  # fmt: skip
    block.add(
        "vn2", 2,
        r"<a' d''>1\pp( | <b' d''>1) | <a' cis''>1( | <a' d''>1) | "
        r"<a' cis''>1( | <b' d''>1) | <b' d''>2( <a' cis''>2 | <a' d''>1) |",
    )  # fmt: skip
    block.add(
        "va", 2,
        r"<fis a>1\pp( | <g b>1) | <g a>1( | <fis a>1) | "
        r"<fis a>1( | <g b>1) | <g b>2( <g a>2 | <fis a>1) |",
    )  # fmt: skip
    block.add("vc", 2, r"d1\pp( | g,1) | a,1( | d1) | fis1( | g1) | e2( a,2 | d1) |")
    block.add(
        "cb", 2,
        r"d,4\p\pizz r r2 | g,,4 r r2 | a,,4 r r2 | d,4 r r2 | "
        r"fis,4 r r2 | g,4 r r2 | e,4 r a,,4 r | d,4 r r2 |",
    )  # fmt: skip
    quiet = {3: "R1 |", 7: "R1 |"}
    block.add("cel.rh", 2, dyn(bars(8, tr(PENTA_ON_BEAT, -4), quiet), r"\ppp"))
    block.add("harp.rh", 2, dyn(bars(8, tr(PENTA_OFF_BEAT, -4), quiet), r"\ppp"))

    # Phrase 3 (8 bars): the chorale of part 1 in the horns, now in D major.
    # The clarinet has the walking theme, the flute answers.
    block.spread(
        "hn4 hn3 hn2 hn1", 3,
        r"<d fis a d'>1\pp\tutti( | <e g d' e'>1 | <fis a d' a'>1 | <b, fis d' fis'>1) | "
        r"<g, g b d'>1( | <a, g d' e'>1 | <a, g cis' e'>1 | <d fis a d'>1) |",
    )  # fmt: skip
    block.add(
        "cl1", 3,
        r"d'4.\p\dolce( e'8 fis'4. g'8 | a'2.) r4 | a'4.( b'8 cis''4. d''8 | e''2.) r4 | R1*4 |",
    )  # fmt: skip
    block.add(
        "fl1", 3,
        r"R1*4 | e''4.\p\dolce( d''8 cis''4. b'8 | a'2.) r4 | a'4.( g'8 fis'4. e'8 | d'1) |",
    )  # fmt: skip
    block.add("vc", 3, r"<d a>1\ppp ~ | " + r"<d a>1 ~ | " * 6 + r"<d a>1 |")
    block.add("cb", 3, r"d,1\ppp\arco ~ | " + r"d,1 ~ | " * 6 + r"d,1 |")

    # Phrase 4 (4 bars): D major, very soft. The bells: the shimmer form, then the light form.
    last = r"X1\ppp ~ | X1 ~ | X1 ~ | X1\fermata |"
    block.add("vn1", 4, fill(r"<fis'' a''>1", last))
    block.add("vn2", 4, fill(r"<a' d''>1", last))
    block.add("va", 4, fill(r"<fis a>1", last))
    block.add("vc", 4, fill(r"<d a>1", last))
    block.add("cb", 4, fill(r"<d,>1", last.replace("X", "A")))
    block.add(
        "cel.rh", 4, r"d'''4\pp( e''' gis''' a''') | R1 | d'''4\ppp( e''' a'''2) | R1\fermata |"
    )
    block.add("harp.rh", 4, r"R1 | <d' a' d'' fis''>2\pp\arpeggio r2 | R1 | R1\fermata |")
    block.add("perc2", 4, r"""\switch "vibraphone" <d' fis' a'>1\pp\lv | R1*2 | R1\fermata |""")
    block.add("timp", 4, r"R1*2 | d,4\ppp r r2 | R1\fermata |")
    block.close()
