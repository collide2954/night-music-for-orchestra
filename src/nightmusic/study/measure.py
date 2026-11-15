"""Measure the open reference data and write the measured tables as CSV files."""

from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from fractions import Fraction
from pathlib import Path

import mido

from . import corpus, metrics, muscript, pcsets, workcheck
from .metrics import Tone

OUTPUT_DIR = Path("research/measured")

# ----------------------------------------------------------------------------
# Verklärte Nacht
# ----------------------------------------------------------------------------

# Formal sections. Bar numbers from Frisch 1993, chapter 5 (after Wellesz 1925
# and Pfannkuch 1963).
VN_PARTS = [
    ("1", "Stanza 1. Narrator: the walk in the cold wood", 1, 28),
    ("2", "Stanza 2. The woman speaks", 29, 187),
    ("3", "Stanza 3. Narrator", 188, 228),
    ("4", "Stanza 4. The man speaks", 229, 369),
    ("5", "Stanza 5. Narrator: the transfigured night", 370, 418),
]
VN_SEGMENTS = [
    ("1", "Theme group 1, D minor", 1, 28),
    ("2a", "Theme group 2", 29, 49),
    ("2b", "Theme groups 3 and 4, B-flat minor, then transition", 50, 104),
    ("2c", "Theme group 5, E major", 105, 131),
    ("2d", "Development", 132, 180),
    ("2e", "Return of theme 2a at the first large climax", 181, 187),
    ("3", "Transition and return of theme 1, to E-flat minor", 188, 228),
    ("4a", "Themes 6 to 10: D major, F-sharp major, D-flat major, F major", 229, 319),
    ("4b", "Theme 11 in D-flat major, climax, theme 6 again in D major", 320, 369),
    ("5", "Reprise of themes in D major, second climax, coda", 370, 418),
]

DYNAMIC_LEVELS = ["pppp", "ppp", "pp", "p", "mp", "mf", "f", "ff", "fff"]
ACCENT_MARKS = {"sf", "sff", "sfz", "sffz", "fz", "fp", "sfp", "sfpp", "ffp"}
PEDAL_WORDS = {"una", "corda", "tre", "corde", "ped", "ped.", "*"}


def write_csv(name: str, header: Sequence[str], rows: Iterable[Sequence[object]]) -> Path:
    """Write one measured table."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow([_format(value) for value in row])
    return path


def _format(value: object) -> object:
    if isinstance(value, float):
        return f"{value:.4g}" if abs(value) < 1000 else f"{value:.1f}"
    if isinstance(value, Fraction):
        return f"{float(value):.4g}"
    return value


def load_vn() -> muscript.Score:
    """Download and parse the Verklärte Nacht source."""
    return muscript.parse(corpus.fetch("vn-billam").read_text(encoding="utf-8"))


def vn_tones(score: muscript.Score, first: int = 1, last: int = 10**6) -> list[Tone]:
    """Return the notes of a bar range as tones. The time unit is the quarter note."""
    return [
        Tone(float(n.start), float(n.duration), n.midi, f"{n.stave}{n.voice}", float(n.volume))
        for n in score.notes
        if first <= n.bar <= last
    ]


def _vn_line(tones: Sequence[Tone]) -> list[Tone]:
    """Return the top line of the upper stave."""
    return metrics.skyline([t for t in tones if t.layer.startswith("1")])


def _dynamic_tokens(text: str) -> list[str]:
    known = {*DYNAMIC_LEVELS, *ACCENT_MARKS}
    return [token.strip(".,") for token in text.split() if token.strip(".,") in known]


def measure_vn() -> dict[str, dict[str, float]]:
    """Measure Verklärte Nacht. Return the fingerprints for the comparison table."""
    score = load_vn()
    bars = score.bars
    total_seconds = score.duration_seconds
    notes_by_bar: dict[int, list[muscript.Note]] = defaultdict(list)
    for note in score.notes:
        notes_by_bar[note.bar].append(note)

    # Dynamic level of each bar: the last level mark stays in effect.
    level = ""
    level_by_bar: dict[int, str] = {}
    marks_by_bar: dict[int, list[str]] = defaultdict(list)
    dynamic_counts: Counter[str] = Counter()
    for bar in bars:
        for mark in sorted(bar.texts, key=lambda m: m.x):
            if mark.font != "I":
                continue
            for token in _dynamic_tokens(mark.text):
                dynamic_counts[token] += 1
                marks_by_bar[bar.number].append(token)
                if token in DYNAMIC_LEVELS:
                    level = token
        level_by_bar[bar.number] = level

    # Table: one row for each bar.
    tempo_by_bar = {
        bar.number: "; ".join(m.text for m in bar.texts if m.font == "b") for bar in bars
    }
    write_csv(
        "vn_bars.csv",
        [
            "bar",
            "time_signature",
            "key_signature",
            "seconds",
            "quarter_bpm",
            "note_starts",
            "mean_midi_volume",
            "dynamic_level",
            "dynamic_marks",
            "tempo_mark",
        ],
        [
            [
                bar.number,
                f"{bar.time_signature[0]}/{bar.time_signature[1]}",
                bar.key_signature,
                bar.duration_seconds,
                bar.quarter_bpm,
                len(notes_by_bar[bar.number]),
                statistics.fmean(n.volume for n in notes_by_bar[bar.number])
                if notes_by_bar[bar.number]
                else "",
                level_by_bar[bar.number],
                " ".join(marks_by_bar[bar.number]),
                tempo_by_bar[bar.number],
            ]
            for bar in bars
        ],
    )

    # Table: tempo and expression marks.
    mark_rows = []
    for bar in bars:
        for mark in sorted(bar.texts, key=lambda m: m.x):
            words = {w.lower() for w in mark.text.split()}
            if mark.font == "b":
                kind = "tempo"
            elif mark.font == "i" and not words & PEDAL_WORDS:
                kind = "expression"
            else:
                continue
            mark_rows.append([bar.number, kind, mark.text.replace(" . . .", "").strip()])
    write_csv("vn_marks.csv", ["bar", "kind", "text"], mark_rows)

    # Table: how frequently each tempo or expression word occurs.
    word_counts: Counter[tuple[str, str]] = Counter()
    for _bar, kind, text in mark_rows:
        word = text.lower().strip("., ()")
        if word not in DYNAMIC_LEVELS:
            word_counts[(kind, word)] += 1
    write_csv(
        "vn_mark_counts.csv",
        ["kind", "text", "count"],
        [[kind, text, count] for (kind, text), count in word_counts.most_common()],
    )

    # Table: dynamic marks.
    bars_at_level = Counter(level_by_bar.values())
    seconds_at_level: Counter[str] = Counter()
    for bar in bars:
        seconds_at_level[level_by_bar[bar.number]] += bar.duration_seconds
    write_csv(
        "vn_dynamics.csv",
        ["mark", "kind", "count_of_marks", "bars_in_effect", "share_of_time_in_effect"],
        [
            [
                name,
                "level" if name in DYNAMIC_LEVELS else "accent",
                dynamic_counts[name],
                bars_at_level[name] if name in DYNAMIC_LEVELS else "",
                seconds_at_level[name] / total_seconds if name in DYNAMIC_LEVELS else "",
            ]
            for name in DYNAMIC_LEVELS + sorted(ACCENT_MARKS)
            if dynamic_counts[name]
        ],
    )

    # Table: metres.
    metre_bars = Counter(f"{b.time_signature[0]}/{b.time_signature[1]}" for b in bars)
    metre_changes = sum(
        1 for a, b in zip(bars, bars[1:], strict=False) if a.time_signature != b.time_signature
    )
    write_csv(
        "vn_metres.csv",
        ["time_signature", "bars", "share_of_bars"],
        [[name, count, count / len(bars)] for name, count in metre_bars.most_common()]
        + [["(changes of metre)", metre_changes, ""]],
    )

    # Table: formal sections.
    def section_rows(sections):
        rows = []
        elapsed = 0.0
        starts = score.bar_start_seconds()
        for code, label, first, last in sections:
            chosen = bars[first - 1 : last]
            seconds = sum(b.duration_seconds + b.pause_before for b in chosen)
            quarters = sum(float(b.length) for b in chosen)
            volumes = [n.volume for b in chosen for n in notes_by_bar[b.number]]
            starts_count = sum(len(notes_by_bar[b.number]) for b in chosen)
            bpms = [b.quarter_bpm for b in chosen]
            elapsed = starts[first - 1]
            rows.append(
                [
                    code,
                    label,
                    first,
                    last,
                    last - first + 1,
                    seconds / 60,
                    seconds / total_seconds,
                    elapsed / total_seconds,
                    60 * quarters / seconds,
                    min(bpms),
                    max(bpms),
                    starts_count / seconds,
                    statistics.fmean(volumes),
                    min(volumes),
                    max(volumes),
                ]
            )
        return rows

    header = [
        "section",
        "content",
        "first_bar",
        "last_bar",
        "bars",
        "minutes",
        "share_of_time",
        "start_position",
        "mean_quarter_bpm",
        "slowest_bar_bpm",
        "fastest_bar_bpm",
        "note_starts_per_second",
        "mean_midi_volume",
        "lowest_midi_volume",
        "highest_midi_volume",
    ]
    write_csv("vn_parts.csv", header, section_rows(VN_PARTS))
    write_csv("vn_segments.csv", header, section_rows(VN_SEGMENTS))

    # Table: general numbers.
    starts = score.bar_start_seconds()
    loud_bars = [b.number for b in bars if level_by_bar[b.number] == "fff"]
    overview = [
        ["bars", len(bars)],
        ["note starts in the arrangement", len(score.notes)],
        ["duration with the timing of the arrangement (minutes)", total_seconds / 60],
        ["slowest bar (quarter notes in a minute)", min(b.quarter_bpm for b in bars)],
        ["median bar (quarter notes in a minute)", statistics.median(b.quarter_bpm for b in bars)],
        ["fastest bar (quarter notes in a minute)", max(b.quarter_bpm for b in bars)],
        ["tempo marks", sum(1 for row in mark_rows if row[1] == "tempo")],
        ["bars for each tempo mark", len(bars) / sum(1 for row in mark_rows if row[1] == "tempo")],
        ["dynamic level marks", sum(dynamic_counts[d] for d in DYNAMIC_LEVELS)],
        [
            "dynamic level marks for each 10 bars",
            10 * sum(dynamic_counts[d] for d in DYNAMIC_LEVELS) / len(bars),
        ],
        ["changes of metre", metre_changes],
        ["first bar with the level fff", loud_bars[0] if loud_bars else ""],
        ["bars with the level fff in effect", len(loud_bars)],
        ["position of bar 229 (arrival of D major), share of time", starts[228] / total_seconds],
        ["position of bar 338 (largest climax), share of time", starts[337] / total_seconds],
        ["position of bar 391 (second climax), share of time", starts[390] / total_seconds],
        ["position of bar 229, share of bars", 228 / len(bars)],
        ["position of bar 338, share of bars", 337 / len(bars)],
    ]
    write_csv("vn_overview.csv", ["measure", "value"], overview)

    # Bass motion: the lowest note at each quarter-note beat.
    bass_moves: Counter[int] = Counter()
    tones = vn_tones(score)
    ordered = sorted(tones, key=lambda t: t.start)
    beat, index, active, previous_bass = 0.0, 0, [], None
    end_time = max(t.end for t in tones)
    while beat < end_time:
        while index < len(ordered) and ordered[index].start <= beat:
            active.append(ordered[index])
            index += 1
        active = [t for t in active if t.end > beat]
        if active:
            bass = min(t.midi for t in active)
            if previous_bass is not None and bass != previous_bass:
                distance = abs(bass - previous_bass) % 12
                bass_moves[min(distance, 12 - distance)] += 1
            previous_bass = bass
        beat += 1.0
    total_moves = sum(bass_moves.values())
    write_csv(
        "vn_bass_motion.csv",
        ["interval_class", "name", "moves", "share"],
        [
            [ic, pcsets.INTERVAL_NAMES[ic], bass_moves[ic], bass_moves[ic] / total_moves]
            for ic in range(0, 7)
        ],
    )

    # Fingerprints for the full work and for its two parts.
    prints: dict[str, dict[str, float]] = {}
    for label, first, last in [
        ("Schoenberg: Verklärte Nacht, complete", 1, 418),
        ("Schoenberg: Verklärte Nacht, part 1 (bars 1-228)", 1, 228),
        ("Schoenberg: Verklärte Nacht, part 2 (bars 229-418)", 229, 418),
    ]:
        chosen = vn_tones(score, first, last)
        prints[label] = metrics.fingerprint(chosen, line=_vn_line(chosen), max_gap=1.0, window=4.0)
        prints[label]["note starts in one second"] = len(chosen) / sum(
            b.duration_seconds for b in bars[first - 1 : last]
        )
        _SONORITIES[label] = metrics.sonority_shares(chosen)
    return prints


# ----------------------------------------------------------------------------
# Bartók: Out of Doors (performance MIDI)
# ----------------------------------------------------------------------------

OOD_PIECES = [
    "1. With Drums and Pipes",
    "2. Barcarolla",
    "3. Musettes",
    "4. The Night's Music",
    "5. The Chase",
]
PIECE_GAP_SECONDS = 5.0


def load_ood() -> list[list[Tone]]:
    """Read the performance MIDI file. Return the tones of each of the five pieces.

    The time unit is the second. The sustain pedal makes a note longer: the note
    sounds until the pedal goes up or the same key goes down again.
    """
    midi = mido.MidiFile(corpus.fetch("ood-bednarek"))
    clock = 0.0
    pedal_down = False
    held: dict[int, Tone] = {}  # key is down
    sustained: dict[int, Tone] = {}  # key is up, pedal keeps the note
    tones: list[Tone] = []
    key_gaps: list[tuple[float, float]] = []
    last_key_up = 0.0

    def stop(tone: Tone) -> None:
        tone.duration = max(clock - tone.start, 0.0)

    for message in midi:
        clock += message.time
        if message.type == "control_change" and message.control == 64:
            now_down = message.value >= 64
            if pedal_down and not now_down:
                for tone in sustained.values():
                    stop(tone)
                sustained.clear()
            pedal_down = now_down
        elif message.type == "note_on" and message.velocity > 0:
            if message.note in sustained:
                stop(sustained.pop(message.note))
            if not held and clock - last_key_up > PIECE_GAP_SECONDS and tones:
                key_gaps.append((last_key_up, clock))
            tone = Tone(clock, 0.0, message.note, "piano", float(message.velocity))
            held[message.note] = tone
            tones.append(tone)
        elif message.type in ("note_off", "note_on") and message.note in held:
            tone = held.pop(message.note)
            last_key_up = clock
            if pedal_down:
                sustained[message.note] = tone
            else:
                stop(tone)
    for tone in [*held.values(), *sustained.values()]:
        stop(tone)

    boundaries = [0.0, *[(a + b) / 2 for a, b in key_gaps], clock + 1.0]
    pieces = []
    for low, high in zip(boundaries, boundaries[1:], strict=False):
        piece = [t for t in tones if low <= t.start < high]
        # A pedal can hold a note into the next piece. Cut the note at the boundary.
        for tone in piece:
            tone.duration = min(tone.duration, high - tone.start)
        pieces.append(piece)
    return pieces


def measure_ood() -> dict[str, dict[str, float]]:
    """Measure the five pieces of Out of Doors."""
    pieces = load_ood()
    if len(pieces) != len(OOD_PIECES):
        raise RuntimeError(f"expected {len(OOD_PIECES)} pieces, found {len(pieces)}")
    prints: dict[str, dict[str, float]] = {}
    rows = []
    for name, tones in zip(OOD_PIECES, pieces, strict=True):
        label = f"Bartók: Out of Doors, {name}"
        start = min(t.start for t in tones)
        end = max(t.end for t in tones)
        line = metrics.skyline(tones, window=0.05)
        result = metrics.fingerprint(tones, line=line, max_gap=1.0, window=4.0)
        velocities = sorted(t.loudness for t in tones)
        result["note starts in one second"] = len(tones) / (end - start)
        prints[label] = result
        _SONORITIES[label] = metrics.sonority_shares(tones)
        rows.append(
            [
                name,
                (end - start) / 60,
                len(tones),
                len(tones) / (end - start),
                statistics.fmean(velocities),
                velocities[int(0.05 * len(velocities))],
                velocities[int(0.95 * len(velocities))],
                min(t.midi for t in tones),
                max(t.midi for t in tones),
            ]
        )
    write_csv(
        "ood_pieces.csv",
        [
            "piece",
            "minutes",
            "note_starts",
            "note_starts_per_second",
            "mean_key_velocity",
            "key_velocity_5th_percentile",
            "key_velocity_95th_percentile",
            "lowest_midi_pitch",
            "highest_midi_pitch",
        ],
        rows,
    )
    return prints


# ----------------------------------------------------------------------------
# Bartók: Fourteen Bagatelles op. 6 (DCML note lists)
# ----------------------------------------------------------------------------


def load_bagatelle(number: int) -> tuple[list[Tone], Counter[str], int]:
    """Read one bagatelle. Return its tones, its metres (bars for each), and its bar count.

    The time unit is the quarter note. Tied notes are one tone.
    """
    path = corpus.fetch(f"bagatelle-{number:02d}")
    tones: list[Tone] = []
    open_ties: dict[tuple[str, int], Tone] = {}
    metres: dict[str, set[str]] = defaultdict(set)
    bars: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            position = row["quarterbeats"] or row["quarterbeats_all_endings"]
            if not position:
                continue
            start = float(Fraction(position))
            duration = float(row["duration_qb"])
            midi = int(row["midi"])
            metres[row["timesig"]].add(row["mc"])
            bars.add(row["mc"])
            key = (row["staff"], midi)
            if row["tied"] in ("0", "-1") and key in open_ties:
                open_ties[key].duration += duration
                if row["tied"] == "-1":
                    del open_ties[key]
                continue
            tone = Tone(start, duration, midi, f"{row['staff']}.{row['voice']}")
            tones.append(tone)
            if row["tied"] == "1":
                open_ties[key] = tone
    return tones, Counter({name: len(items) for name, items in metres.items()}), len(bars)


def measure_bagatelles() -> dict[str, dict[str, float]]:
    """Measure the Fourteen Bagatelles."""
    prints: dict[str, dict[str, float]] = {}
    all_tones: list[Tone] = []
    all_line: list[Tone] = []
    offset = 0.0
    rows = []
    for number in range(1, 15):
        tones, metres, bar_count = load_bagatelle(number)
        line = metrics.skyline([t for t in tones if t.layer.startswith("1")])
        result = metrics.fingerprint(tones, line=line, max_gap=1.0, window=4.0)
        rows.append(
            [
                number,
                bar_count,
                len(tones),
                "; ".join(f"{name} ({count})" for name, count in metres.most_common()),
                len(metres),
                result.get("chords: share built from thirds", ""),
                result.get("chords: share with a semitone clash", ""),
                result["pitch-class entropy (bits, maximum 3.585)"],
            ]
        )
        if number == 12:
            label = "Bartók: Bagatelle op. 6 no. 12 (early night music)"
            prints[label] = result
            _SONORITIES[label] = metrics.sonority_shares(tones)
        # Put the pieces one after the other for the totals.
        end = max(t.end for t in tones)
        for tone in tones:
            all_tones.append(Tone(tone.start + offset, tone.duration, tone.midi, tone.layer))
        for tone in line:
            all_line.append(Tone(tone.start + offset, tone.duration, tone.midi, tone.layer))
        offset += end + 8.0
    write_csv(
        "bagatelles.csv",
        [
            "number",
            "bars",
            "notes",
            "metres_with_bar_counts",
            "different_metres",
            "chords_share_built_from_thirds",
            "chords_share_with_semitone_clash",
            "pitch_class_entropy_bits",
        ],
        rows,
    )
    label = "Bartók: Fourteen Bagatelles op. 6, complete"
    prints[label] = metrics.fingerprint(all_tones, line=all_line, max_gap=1.0, window=4.0)
    _SONORITIES[label] = metrics.sonority_shares(all_tones)
    return prints


# ----------------------------------------------------------------------------
# Comparison tables
# ----------------------------------------------------------------------------

_SONORITIES: dict[str, dict[str, float]] = {}


def measure_all() -> None:
    """Measure all data and write all measured tables."""
    _SONORITIES.clear()
    prints: dict[str, dict[str, float]] = {}
    prints.update(measure_vn())
    prints.update(measure_ood())
    prints.update(measure_bagatelles())

    works = list(prints)
    measures: list[str] = []
    for result in prints.values():
        for name in result:
            if name not in measures:
                measures.append(name)
    write_csv(
        "fingerprints.csv",
        ["measure", *works],
        [[name, *[prints[work].get(name, "") for work in works]] for name in measures],
    )

    rows = []
    for work, shares in _SONORITIES.items():
        ranked = sorted(shares.items(), key=lambda item: -item[1])
        for rank, (name, value) in enumerate(ranked[:20], 1):
            rows.append([work, rank, name, value])
    write_csv("sonorities.csv", ["work", "rank", "sonority", "share_of_sounding_time"], rows)
    measure_repetition()


def measure_repetition() -> None:
    """Measure the literal repetition of Verklärte Nacht and of the new work."""
    from ..work import build

    score = load_vn()
    starts = {bar.number: bar.start for bar in score.bars}
    workcheck.write_reference_repetition(
        "Schoenberg: Verklärte Nacht (piano arrangement)",
        (
            (note.bar, f"{note.stave}{note.voice}", note.start - starts[note.bar], note.duration,
             note.midi)
            for note in score.notes
            if not note.small
        ),
    )  # fmt: skip
    workcheck.write_tables(build())
