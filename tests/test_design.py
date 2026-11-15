"""Tests for the design data files."""

import tomllib
from pathlib import Path

DESIGN = Path(__file__).resolve().parents[1] / "design"


def load(name: str) -> dict:
    with (DESIGN / name).open("rb") as handle:
        return tomllib.load(handle)


def test_parts_fill_the_work_with_no_gap():
    form = load("form.toml")
    parts = form["part"]
    assert [part["number"] for part in parts] == [1, 2, 3, 4, 5]
    assert parts[0]["start"] == 0.0
    assert parts[-1]["end"] == 1.0
    for earlier, later in zip(parts, parts[1:], strict=False):
        assert earlier["end"] == later["start"]
    for part in parts:
        low, high = part["tempo_quarter"]
        assert 30 <= low <= high <= 160


def test_events_are_in_sequence():
    events = load("form.toml")["events"]
    order = ["first_climax", "far_point", "turn", "main_climax", "final_arrival"]
    positions = [events[name] for name in order]
    assert positions == sorted(positions)
    assert positions[0] > 0.0 and positions[-1] < 1.0
    # The turn is the start of part 4.
    assert events["turn"] == load("form.toml")["part"][3]["start"]


def test_motto_states():
    pitch = load("pitch.toml")
    motto = pitch["motto"]
    assert motto["sequence"] == ["dark", "twilight", "shimmer", "light"]
    for state in motto["sequence"]:
        steps = motto[state]
        assert steps[0] == 0 and len(steps) == 3
        # Each state is a subset of its scale field.
        assert set(steps) <= set(pitch["fields"][state]["steps"])
    # Interval expansion: no interval becomes smaller from the dark to the light state.
    assert all(a <= b for a, b in zip(motto["dark"], motto["light"], strict=True))


def test_orchestra():
    orchestra = load("orchestra.toml")
    instruments = orchestra["instrument"]
    unpitched = {
        "singing bowls",
        "tam-tams",
        "suspended cymbals",
        "crash cymbals",
        "triangle",
        "bass drum",
        "snare drum",
        "tom-toms",
        "taiko",
        "frame drum",
        "wood blocks",
        "temple blocks",
        "claves",
        "guiro",
        "cowbells",
        "finger cymbals",
        "wind chimes",
        "waterphone",
    }
    ids = [player["id"] for player in orchestra["player"]]
    assert len(ids) == len(set(ids))
    total = 0
    for player in orchestra["player"]:
        total += player.get("count", 1)
        for name in player["instruments"]:
            assert name in instruments or name in unpitched, name
    assert total == orchestra["summary"]["total_players"]
    for name, data in instruments.items():
        low, high = data["range"]
        assert 12 <= low < high <= 108, name
        assert data["clef"] in {"treble", "alto", "bass", "grand"}, name
    # The four colour instruments of the brief are in the orchestra.
    brief = load("brief.toml")
    for colour in brief["orchestra"]["colours"]:
        assert colour.rstrip("s") in instruments, colour
