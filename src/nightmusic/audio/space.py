"""The stage and the hall: where each player sits, and how the sound gets to the microphones.

The model has three parts:

1. A main pair of microphones above the conductor. Each player has a seat on
   the stage. The sound of a player arrives at each microphone with the delay
   and the loss of its real distance. This gives the stereo image.
2. The first reflections from the floor, the side walls, the back wall, and
   the ceiling of the stage.
3. The late reverberation of the hall. The code makes it from noise with a
   decay time that depends on the frequency, as in a real concert hall.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import signal

from . import dsp

SPEED_OF_SOUND = 343.0  # metres in a second

# The stage, in metres. x: left (negative) to right, seen from the audience.
# y: from the front edge of the stage to the back. z: height.
SIDE_WALL = 11.5
BACK_WALL = 15.0
CEILING = 14.0
SOURCE_HEIGHT = 1.1
MICROPHONES = ((-0.85, -2.2, 3.4), (0.85, -2.2, 3.4))
REFERENCE_DISTANCE = 7.0  # a source at this distance has a gain of 1

# Decay time of the hall (seconds for a decrease of 60 dB) for each octave band.
# The values are those of a large concert hall with an audience.
DECAY_SECONDS = {
    63: 2.5,
    125: 2.35,
    250: 2.2,
    500: 2.1,
    1000: 2.0,
    2000: 1.8,
    4000: 1.45,
    8000: 1.0,
}


@dataclass(frozen=True)
class Seat:
    x: float
    y: float


# Seats of the players. The violins sit left and right of the conductor, as in
# the orchestras of Schoenberg's and Bartók's time.
SEATS: dict[str, Seat] = {
    "vn1": Seat(-5.5, 2.6), "vn2": Seat(5.2, 2.6), "va": Seat(2.4, 4.6), "vc": Seat(-2.2, 4.6),
    "cb": Seat(-6.8, 6.6),
    "fl1": Seat(-1.0, 7.0), "fl2": Seat(-2.0, 7.0), "fl3": Seat(-3.0, 7.0),
    "ob1": Seat(1.0, 7.0), "ob2": Seat(2.0, 7.0), "ob3": Seat(3.0, 7.0),
    "cl1": Seat(-1.0, 8.3), "cl2": Seat(-2.0, 8.3), "cl3": Seat(-3.0, 8.3), "cbcl": Seat(-4.0, 8.3),
    "bn1": Seat(1.0, 8.3), "bn2": Seat(2.0, 8.3), "bn3": Seat(3.0, 8.3),
    "hn1": Seat(-2.6, 9.7), "hn2": Seat(-3.6, 9.7), "hn3": Seat(-4.6, 9.7),
    "hn4": Seat(-5.6, 9.7), "hn5": Seat(-3.1, 10.8), "hn6": Seat(-4.1, 10.8),
    "tpt1": Seat(0.6, 9.8), "tpt2": Seat(1.6, 9.8), "tpt3": Seat(2.6, 9.8),
    "tbn1": Seat(3.8, 9.8), "tbn2": Seat(4.8, 9.8), "btbn": Seat(5.8, 9.8), "tuba": Seat(6.8, 9.8),
    "timp": Seat(0.0, 11.6),
    "perc1": Seat(-7.5, 11.4), "perc2": Seat(-5.5, 11.8), "perc3": Seat(-3.5, 12.0),
    "perc4": Seat(3.0, 12.0),
    "harp": Seat(-8.2, 5.6), "pno": Seat(-8.8, 8.2), "cel": Seat(-7.6, 9.4),
    "cimb": Seat(7.8, 5.6), "mand": Seat(6.6, 4.2), "acc": Seat(7.8, 7.6),
}  # fmt: skip

# A string section is some metres wide. Each group of the section has its own seat.
SECTION_OFFSETS = [(0.0, 0.0), (-1.6, 0.9), (1.6, 1.0), (0.4, 1.9)]


def seat_of(player_id: str, group: int = 0) -> Seat:
    """Return the seat of a player, or of one group of a string section."""
    base = SEATS[player_id.split(".")[0]]
    dx, dy = SECTION_OFFSETS[group % len(SECTION_OFFSETS)]
    return Seat(base.x + dx, base.y + dy)


def _paths(seat: Seat) -> list[tuple[tuple[float, float, float], float, bool]]:
    """Return the image sources of a seat: (position, reflection gain, is a reflection)."""
    x, y, z = seat.x, seat.y, SOURCE_HEIGHT
    return [
        ((x, y, z), 1.0, False),  # direct sound
        ((x, y, -z), 0.75, True),  # floor
        ((-2 * SIDE_WALL - x, y, z), 0.6, True),  # left wall
        ((2 * SIDE_WALL - x, y, z), 0.6, True),  # right wall
        ((x, 2 * BACK_WALL - y, z), 0.65, True),  # back wall
        ((x, y, 2 * CEILING - z), 0.5, True),  # ceiling
    ]


def early_response(seat: Seat) -> np.ndarray:
    """Return the two-channel impulse response from a seat to the microphones.

    The response has the direct sound and the first reflections.
    """
    length = int(0.14 * dsp.RATE)
    direct = np.zeros((length, 2), dtype=np.float64)
    reflected = np.zeros((length, 2), dtype=np.float64)
    for channel, microphone in enumerate(MICROPHONES):
        for position, gain, is_reflection in _paths(seat):
            distance = float(np.linalg.norm(np.subtract(position, microphone)))
            delay = (distance - 2.5) / SPEED_OF_SOUND  # 2.5 m: less than the nearest seat
            index = int(round(delay * dsp.RATE))
            if 0 <= index < length:
                target = reflected if is_reflection else direct
                target[index, channel] += gain * REFERENCE_DISTANCE / distance
    # A reflection loses high frequencies at the wall and in the air.
    reflected = signal.sosfilt(dsp.lowpass(5500.0, 1), reflected, axis=0)
    return (direct + reflected).astype(np.float32)


def place(stem: np.ndarray, seat: Seat) -> np.ndarray:
    """Return the two-channel sound of a one-channel signal from a seat."""
    response = early_response(seat)
    left = signal.oaconvolve(stem, response[:, 0])[: len(stem)]
    right = signal.oaconvolve(stem, response[:, 1])[: len(stem)]
    return np.stack([left, right], axis=1).astype(np.float32)


def reverb_send(seat: Seat) -> float:
    """Return how much of a seat goes to the hall reverberation.

    The reverberant sound has almost the same level for all seats. The direct
    sound decreases with the distance. Thus a far seat sounds more distant.
    """
    distance = float(np.hypot(seat.x, seat.y + 2.2))
    return float(np.clip(0.75 + 0.03 * distance, 0.75, 1.15))


def hall_response(seconds: float = 3.6, seed: int = 20261115) -> np.ndarray:
    """Return the two-channel impulse response of the late reverberation."""
    random = np.random.default_rng(seed)
    length = int(seconds * dsp.RATE)
    time = np.arange(length) / dsp.RATE
    response = np.zeros((length, 2), dtype=np.float64)
    centres = sorted(DECAY_SECONDS)
    for centre in centres:
        low, high = centre / np.sqrt(2.0), min(centre * np.sqrt(2.0), 0.45 * dsp.RATE)
        if centre == centres[0]:
            band = signal.butter(2, high, "lowpass", fs=dsp.RATE, output="sos")
        elif centre == centres[-1]:
            band = signal.butter(2, low, "highpass", fs=dsp.RATE, output="sos")
        else:
            band = signal.butter(2, [low, high], "bandpass", fs=dsp.RATE, output="sos")
        noise = random.normal(0.0, 1.0, (length, 2))
        if centre <= 125:
            # Low frequencies are almost the same at the two microphones.
            shared = random.normal(0.0, 1.0, (length, 1))
            noise = 0.6 * noise + 0.8 * shared
        decay = np.exp(-6.908 * time / DECAY_SECONDS[centre])[:, None]
        response += signal.sosfiltfilt(band, noise, axis=0) * decay
    # The reverberation builds up after the first reflections.
    build = int(0.07 * dsp.RATE)
    response[:build] *= np.linspace(0.0, 1.0, build)[:, None] ** 2
    response[-2000:] *= np.linspace(1.0, 0.0, 2000)[:, None]
    response /= np.sqrt(np.sum(response**2, axis=0, keepdims=True))
    return response.astype(np.float32)


def reverberate(send: np.ndarray, response: np.ndarray | None = None) -> np.ndarray:
    """Return the two-channel reverberation of a one-channel send signal."""
    if response is None:
        response = hall_response()
    left = signal.oaconvolve(send, response[:, 0])[: len(send)]
    right = signal.oaconvolve(send, response[:, 1])[: len(send)]
    return np.stack([left, right], axis=1).astype(np.float32)
