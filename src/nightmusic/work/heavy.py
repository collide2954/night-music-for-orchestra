"""The riff of the two heavy sections (mark M in part 2, mark JJ in part 5).

The low instruments hammer a riff in the metre 7/8 (2 + 2 + 3). The riff has
four forms of two bars. A phrase of 8 bars has the four forms in a sequence,
and each phrase has a different sequence: no unit of two bars comes two times.

All other layers of the texture come from the riff:

- The instruments of the gaps play where the riff has a rest.
- The taiko has the rhythm of the riff.
- The bass drum and the timpani have the accents of the root.
- The snare drum and the tom-toms play in the rests of the riff.
"""

from __future__ import annotations

from ..compose.tools import figure

# The four forms of the riff. R = the root. L, M, H = the low, the middle, and the
# high note of the cell. ">" = an accent. "." = a rest. Each form has two bars.
FORMS = {
    "A": "R> . R> . H> M L | R> R . L> . R> H",
    "B": "R> R . H> . M> L | R> . L R> . H> M",
    "C": "R> . H R> . L M> | . R> R . H> . R>",
    "D": "R> L M H> . R> . | H> M L R> R . R>",
}
LAYERS = ("low", "gaps", "taiko", "bass drum", "timp", "toms", "snare")


def layers(
    letters: str, cell: dict[str, str], root: str, tom_notes: list[str]
) -> dict[str, list[str]]:
    """Return the bars of each layer for a sequence of forms of the riff.

    `letters` names the forms, for example "ABCD" (8 bars). `cell` gives the
    notes of the riff for the letters R, L, M, and H. `root` is the note of
    the timpani. `tom_notes` are the written notes of the tom-toms: the
    strokes go through them in a cycle.

    The result has a list of bars for each name in `LAYERS`. In the layer
    "gaps", the letter X is in the place of the chord of the caller.
    """
    music_of: dict[str, list[str]] = {name: [] for name in LAYERS}
    tom = 0
    for letter in letters:
        for bar_text in FORMS[letter].split("|"):
            marks = bar_text.split()
            riff = [
                None if mark == "." else (cell[mark[0]], "->" if mark.endswith(">") else "")
                for mark in marks
            ]
            music_of["low"].append(figure(riff))
            music_of["gaps"].append(
                figure([("X", "->") if mark == "." else None for mark in marks])
            )
            music_of["taiko"].append(
                figure(
                    [
                        None if mark == "." else ("c'", "->" if mark.endswith(">") else "")
                        for mark in marks
                    ]
                )
            )
            # The bass drum: the accents of the root at the start of a beat group.
            beat = [
                ("c'", "->") if mark == "R>" and index in (0, 2, 4) else None
                for index, mark in enumerate(marks)
            ]
            music_of["bass drum"].append(figure(beat))
            music_of["timp"].append(
                figure([(root, "->") if mark == "R>" else None for mark in marks])
            )
            # The tom-toms: the rests of the riff in the last beat group.
            # The snare drum: the other rests.
            toms: list[tuple[str, str] | None] = []
            snare: list[tuple[str, str] | None] = []
            for index, mark in enumerate(marks):
                free = mark == "."
                toms.append((tom_notes[tom % len(tom_notes)], "") if free and index >= 4 else None)
                snare.append(("c'", "->") if free and index < 4 else None)
                tom += 1 if free and index >= 4 else 0
            music_of["toms"].append(figure(toms))
            music_of["snare"].append(figure(snare))
    return music_of
