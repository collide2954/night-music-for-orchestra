"""Part 3: the still centre. Night music.

Material of this part:

- A soft cluster of five adjacent semitones around A-flat, in the muted
  strings. It is always there, as the sound of the night.
- A slow cycle of gongs. One cycle is four bars. The notes of the cycle are
  a scale of five notes (G, A-flat, B-flat, D, E-flat). The motto is in
  this scale.
- Calls: short figures at irregular times (ocarinas, wood blocks, celesta).
- A lonely melody for the alto flute, with quarter-tones (the neutral
  second above A-flat is a note between the notes of the cluster).
- The motto as a distant chorale in four octaves: first with the tritone
  (the dark form), then with the fifth (the twilight form).
- A slow melody for one cello above a drone on E-flat and A-flat.
- The first half of the piano interlude (mark W): the piano takes the night
  music. The module `interlude.py` has this music.

Style profile: "Night".
"""

from __future__ import annotations

from ..compose.tools import Block, fill, scatter, times
from ..notation.work import Work
from . import interlude

BARS = 42  # the part has 42 bars of 3/2


def rest(count: int) -> str:
    """Return a rest of `count` bars of 3/2."""
    return f"R1*3/2*{count} |" if count > 1 else "R1*3/2 |"


# The calls of the night.
BIRD = r"\grace { d''16 } es''8-.\p es''8-. es''4--"
BIRD_LOW = r"\grace { a'16 } bes'8-.\p bes'8-. bes'4--"
CRICKET = r"c'16\ppp c' c' c' c'8 r8"
FROG = r"\grace { g,16 } as,8-.\p r8"
FLUTTER = r"\tuplet 3/2 { g''16\pp( bes'' d''' } es'''8-.)"
DROP = r"d''''8\pp( es''''8)"
INSECT = r"as'16\pp as' as' as' as'8-. r8"
DISTANT = r"d'4\pp\stopped ~ d'8 r8"
FLICKER = r"<d''' es'''>4:32\ppp"
FROG_LOW = r"\grace { d,16 } es,8-.\p r8"
BIRD_HIGH = r"\grace { g''16 } as''8-.\p as''8-. as''4--"

# One breath of the accordion (2 bars): a high chord of five notes, as the
# mouth organ of the Japanese court music plays it.
BREATH = r"X1.\ppp\< ~ | X1\p\> ~ X2\ppp |"
BREATH_CHORD = r"<es'' as'' bes'' des''' es'''>1"

# The swell of the cluster (2 bars and 3 bars).
SWELL_2 = r"X1.\ppp\< ~ | X1.\pp\> |"
SWELL_3 = r"X1.\ppp\< ~ | X1. ~ | X1.\pp\> |"


def _cycle(first: int, count: int) -> dict[str, dict[tuple[int, float], str]]:
    """Return the gong cycle for `count` bars. `first` is the number of the first bar in the part.

    The cycle is four bars. The large gong starts the cycle. A tuned gong is
    in the middle. Softer notes divide the halves.
    """
    events: dict[str, dict[tuple[int, float], str]] = {
        "perc1": {}, "perc3": {}, "perc2": {}, "harp.lh": {}, "pno.lh": {}, "acc.rh": {},
    }  # fmt: skip
    for number in range(1, count + 1):
        place = (first + number - 1) % 4  # 1 = the start of a cycle
        if place == 1:
            events["perc1"][(number, 1)] = r"c'1.\pp\lv"
        if place == 3:
            events["perc3"][(number, 1)] = r"es'1.\p\lv"
            if number < count:
                events["acc.rh"][(number, 1)] = fill(BREATH_CHORD, BREATH)
        if place == 2:
            events["perc2"][(number, 1)] = r"<bes d'>1.\pp\lv"
            events["pno.lh"][(number, 3)] = r"\grace { ges16( g as a } bes2)\ppp\lv"
        if place == 0:
            events["perc2"][(number, 1)] = r"<g d'>1.\pp\lv"
        if place in (1, 3):
            events["harp.lh"][(number, 4)] = r"as,,4\pp"
    return events


def _add_cycle(block: Block, first: int, count: int, skip: tuple[str, ...] = ()) -> None:
    for player, events in _cycle(first, count).items():
        if events and player not in skip:
            block.add(player, 1, scatter(count, 3, 2, events))


def write(work: Work) -> None:
    _night_begins(work)
    _lonely_melody(work)
    _distant_chorale(work)
    _drone_and_song(work)
    interlude.write(work)


def _night_begins(work: Work) -> None:
    """Mark S: the cluster grows from the note A-flat. The first calls."""
    structure = work.structure
    s = work.section(10, 3, 2)
    structure.mark(s.bar(1), "S")
    structure.tempo(s.bar(1), 1, 60, "Lento, immobile")
    block = Block(s, rest(10))

    muted = r"\consord\sultasto\nonvib"
    block.add("va", 1, r"as1.\ppp | " + times(fill(r"<as a>1", SWELL_2), 4) + r" <as a>1.\ppp |",
              muted)  # fmt: skip
    block.add("vn2", 1, rest(1) + times(fill(r"<bes>1", SWELL_3.replace("X", "A")), 3), muted)
    block.add("vc", 1, rest(2) + times(fill(r"<ges g>1", SWELL_2), 4), muted)
    _add_cycle(block, 1, 10)
    block.start("perc3", r'\switch "tuned gongs"')
    block.start("perc1", r'\switch "tam-tams"')

    def calls(player: str, events: dict[tuple[int, float], str], marks: str = "") -> None:
        block.add(player, 1, scatter(10, 3, 2, events), marks)

    calls("cl1", {(2, 4): BIRD, (6, 1): BIRD, (9, 2): BIRD})
    block.start("cl1", r'\switch "ocarina"')
    calls("ob2", {(4, 1.5): BIRD_LOW, (7, 4): BIRD_LOW, (9, 3): BIRD_LOW})
    block.start("ob2", r'\switch "ocarina"')
    calls("cl3", {(5, 2): FROG, (8, 1): FROG, (10, 5): FROG})
    calls("fl3", {(5, 4): FLUTTER, (8, 5): FLUTTER})
    calls("cbcl", {(6, 2): FROG_LOW, (9, 1): FROG_LOW})
    calls("bn2", {(8, 2): BIRD_HIGH})
    block.start("bn2", r'\switch "ocarina"')
    calls("perc4", {(3, 3): CRICKET, (6, 3): CRICKET, (9, 5): CRICKET})
    block.start("perc4", r'\switch "wood blocks"')
    calls("cel.rh", {(4, 5): DROP, (7, 5.5): DROP})
    calls("hn1", {(6, 5): DISTANT})
    calls("tpt1", {(8, 3): INSECT}, r"\consord")
    calls("vn1", {(7, 2): FLICKER, (10, 2): FLICKER}, r"\consord\sulpont")
    calls("cimb.rh", {(10, 1): r"d'8:32\pp es'8:32 d'4:32"})
    calls("harp.rh", {(10, 3): r"\tuplet 3/2 { d'''8\pp es''' d''' } es'''4"})
    calls("mand", {(9, 4): r"as''8\pp as''8 as''4:32"})
    block.close()


def _lonely_melody(work: Work) -> None:
    """Mark T: a melody for the alto flute, in the manner of a night call."""
    structure = work.structure
    s = work.section(12, 3, 2)
    structure.mark(s.bar(1), "T")
    block = Block(s, rest(12))

    block.add(
        "fl2", 1,
        r"""\switch "alto flute"
        r2 as'1\pp\espr\<( ~ | as'2\p\> beseh'4 as'4 ges'2 | as'1.)\pp |
        r2 as'4\p( beseh'4 ces''2 | \grace { des''16 } ces''4 des''4 ces''4 beseh'4 as'2 ~ |
        as'1) r2 |
        r2 ces''4\p\<( des''4 es''2 ~ | es''1\mp ~ es''4 fes''4 |
        \grace { fes''16 } es''4\> des''4 ces''2 beseh'4 as'4 | beseh'2 as'1)\pp |
        R1*3/2*2 |""",
    )  # fmt: skip
    block.add("cimb.rh", 1, rest(10) + r"r2 ces''4:32\pp( bes'4:32 as'2:32 ~ | as'1.:32) |")

    block.add("va", 1, times(fill(r"<as a>1", SWELL_2), 6))
    block.add("vn2", 1, times(fill(r"<bes>1", SWELL_3.replace("X", "A")), 4))
    block.add("vc", 1, times(fill(r"<ges g>1", SWELL_2), 6))
    _add_cycle(block, 11, 12)

    block.add("cl1", 1, scatter(12, 3, 2, {(3, 4): BIRD, (6, 4): BIRD, (11, 2): BIRD}))
    block.add("ob2", 1, scatter(12, 3, 2, {(6, 5): BIRD_LOW, (12, 4): BIRD_LOW}))
    block.add("perc4", 1, scatter(12, 3, 2, {(1, 3): CRICKET, (7, 1): CRICKET, (11, 4): CRICKET}))
    block.add("cl3", 1, scatter(12, 3, 2, {(3, 2): FROG, (11, 5): FROG}))
    block.add("cbcl", 1, scatter(12, 3, 2, {(7, 4): FROG_LOW}))
    block.add("bn2", 1, scatter(12, 3, 2, {(9, 5): BIRD_HIGH}))
    block.add("cel.rh", 1, scatter(12, 3, 2, {(6, 3): DROP, (12, 2): DROP}))
    block.add("vn1", 1, scatter(12, 3, 2, {(3, 5): FLICKER, (10, 5): FLICKER}))
    block.close()


def _distant_chorale(work: Work) -> None:
    """Mark U: the motto as a chorale in four octaves, from far away.

    This is the point of the work that is the most distant from the tonic.
    """
    structure = work.structure
    s = work.section(10, 3, 2)
    structure.mark(s.bar(1), "U")
    block = Block(s, rest(10))

    chorale = (
        r"R1*3/2 | as2\ppp( a2 d'2 | des'1.) | R1*3/2 | as2( a2 es'2 | d'1.) | "
        r"R1*3/2 | as2( a2 es'2 ~ | es'1.) | R1*3/2 |"
    )
    block.add("fl3:2 fl1:1 cl2 cl3:-1", 1, chorale, r"\lontano")
    block.start("cl2", r'\switch "clarinet in B-flat"')

    block.add("va", 1, times(fill(r"<as a>1", SWELL_2), 4) + r" as1.\ppp ~ | as1. |")
    block.add("vn2", 1, times(fill(r"<bes>1", SWELL_3.replace("X", "A")), 2) + rest(4))
    block.add("vc", 1, times(fill(r"<ges g>1", SWELL_2), 2) + rest(6))
    _add_cycle(block, 23, 10)

    block.add("cl1", 1, scatter(10, 3, 2, {(4, 3): BIRD, (10, 3): BIRD}))
    block.add("bn2", 1, scatter(10, 3, 2, {(7, 4): BIRD_HIGH}))
    block.add("perc4", 1, scatter(10, 3, 2, {(3, 5): CRICKET, (7, 5): CRICKET}))
    block.add("cel.rh", 1, scatter(10, 3, 2, {(7, 2): DROP}))
    block.close()


def _drone_and_song(work: Work) -> None:
    """Mark V: one cello sings above a drone. The harmony goes to E-flat minor."""
    structure = work.structure
    s = work.section(10, 3, 2)
    structure.mark(s.bar(1), "V")
    structure.change(s.bar(9), 1, "poco rit.")
    structure.arrive(s.bar(10), 4, 48)
    block = Block(s, rest(10))

    # The drone: the fourth and the tonic, as the lute of the Indian night music plays it.
    block.add("harp.lh", 1, times(r"as,4\pp es4 es4 es,2. |", 10))
    block.add("cimb.lh", 1, r"es1.:32\ppp ~ | " + times(r"es1.:32 ~ |", 8) + r" es1.:32 |")
    block.add("mand", 1, rest(5) + r"es'1.:32\ppp ~ | " + times(r"es'1.:32 ~ |", 3)
              + r" es'1.:32 |")  # fmt: skip

    block.add(
        "vc", 1,
        r"""R1*3/2 |
        r2 es1\pp\espr\<( ~ | es2\p des4 es4 ges2 ~ |
        ges4\> geseh4 ges4 geseh4 ges2\glissando | es1.)\p |
        r2 ges4\p\<( as4 ces'2 ~ | ces'2\mp des'4 ces'4 as2 ~ |
        as2\> ges4 es4 des2 | es1.\pp ~ | es1.) |""",
        r"\solo\senzasord\ord\vib",
    )  # fmt: skip
    block.add("fl2", 1, rest(4) + r"r2 ces''4\pp( beseh'4 as'2 ~ | as'1.) | " + rest(4))

    block.add("va", 1, r"as1.\ppp ~ | as1. ~ | as1. ~ | as1. | " + rest(1)
              + r"<bes es'>1.\ppp\< ~ | <bes es'>1. ~ | <bes es'>1.\pp ~ | <bes es'>1.\> ~ | "
              r"<bes es'>1.\ppp ~ |")  # fmt: skip
    block.add("vn2", 1, rest(5) + r"ges'1.\ppp\< ~ | ges'1. ~ | ges'1.\pp ~ | ges'1.\> ~ | "
              r"ges'1.\ppp ~ |")  # fmt: skip
    block.add("cb", 1, rest(5) + r"es,1.\ppp\< ~ | es,1. ~ | es,1.\pp ~ | es,1.\> ~ | "
              r"es,1.\ppp ~ |", r"\consord\arco")  # fmt: skip
    _add_cycle(block, 33, 10, skip=("harp.lh", "acc.rh", "pno.lh"))

    block.add("cl1", 1, scatter(10, 3, 2, {(5, 4): BIRD}))
    block.add("perc4", 1, scatter(10, 3, 2, {(2, 5): CRICKET, (8, 3): CRICKET}))
    block.close()
