"""Tests for the loudness measurement and the gain riding."""

import numpy as np

from nightmusic.audio import dsp, loudness


def _tone(seconds: float, amplitude: float) -> np.ndarray:
    time = np.arange(int(seconds * dsp.RATE)) / dsp.RATE
    wave = (amplitude * np.sin(2 * np.pi * 997.0 * time)).astype(np.float32)
    return np.stack([wave, wave], axis=1)


def test_integrated_loudness_of_a_sine_tone():
    # A sine tone at -20 dBFS in two channels has a loudness of about -20 LUFS.
    power = loudness.block_power(_tone(8.0, 0.1))
    assert abs(loudness.integrated(power) - (-20.0)) < 0.3


def test_loudness_range_of_two_levels():
    audio = np.concatenate([_tone(30.0, 0.01), _tone(30.0, 0.1)])
    spread, _ = loudness.loudness_range(loudness.short_term(loudness.block_power(audio)))
    assert 17.0 < spread < 20.5


def test_gain_riding_makes_the_range_smaller_and_keeps_the_loud_part():
    audio = np.concatenate([_tone(40.0, 0.012), _tone(40.0, 0.1), _tone(40.0, 0.012)])
    before, _ = loudness.loudness_range(loudness.short_term(loudness.block_power(audio)))
    ridden, ratio, gain = loudness.ride(audio.copy(), 12.0)
    after, _ = loudness.loudness_range(loudness.short_term(loudness.block_power(ridden)))
    assert before > 17.0
    assert after <= 12.5
    assert ratio > 1.0 and 0.0 < gain <= loudness.LARGEST_GAIN_DB
    # The middle of the loud part does not change.
    start = 55 * dsp.RATE
    assert np.allclose(ridden[start : start + 1000], audio[start : start + 1000], atol=1e-4)
