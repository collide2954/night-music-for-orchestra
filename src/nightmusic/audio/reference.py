"""Measure real orchestra recordings, and match the tone balance of the mix to them.

The references are public-domain recordings of full orchestras (Musopen).
The code measures their tone balance (level in third-octave bands), their
loudness range, and their stereo width. The master of the project must be
inside the range of these values.
"""

from __future__ import annotations

import csv
import hashlib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyloudnorm
import soundfile
import soxr
from scipy import signal

from . import dsp

REFERENCE_DIR = Path(".cache/reference")
BASE_URL = "https://archive.org/download/MusopenCollectionAsFlac/"
TARGET_FILE = Path("research/measured/reference_tone_balance.csv")
SUMMARY_FILE = Path("research/measured/reference_recordings.csv")


@dataclass(frozen=True)
class Reference:
    name: str
    work: str
    path: str
    sha1: str


_T6 = "Tchaikovsky_SymphonyPathetique/PyotrIlyichTchaikovsky-SymphonyNo.6InBMinorOp.74pathtique-"
REFERENCES = [
    Reference(
        "tchaikovsky6-1",
        "Tchaikovsky, Symphony No. 6, I",
        _T6 + "01-AdagioAllegroNonTroppo.flac",
        "dfae546cacdb682477861249fafe0d564b5c0f72",
    ),
    Reference(
        "tchaikovsky6-4",
        "Tchaikovsky, Symphony No. 6, IV",
        _T6 + "04-FinaleAdagioLamentoso.flac",
        "9d146de5bbca195b1a62d0b53a3175827859b2f4",
    ),
    Reference(
        "brahms4-1",
        "Brahms, Symphony No. 4, I",
        "Brahms_SymphonyNo.4inEMinor/"
        "JohannesBrahms-SymphonyNo.4InEMinorOp.98-01-AllegroNonTroppo.flac",
        "0d9699bad6fd6b13459a77468958506f49f8018d",
    ),
    Reference(
        "smetana-vltava",
        "Smetana, Vltava",
        "Smetana_Vltava/BedichSmetana-MVlast-Vltava.flac",
        "503422b5cdbde1266b1ffd92390a0aa4d7462e27",
    ),
    Reference(
        "borodin-steppes",
        "Borodin, In the Steppes of Central Asia",
        "Borodin_InTheSteppesOfCentralAsia/AlexanderBorodin-InTheSteppesOfCentralAsia.flac",
        "a25677d7b6435f8f18475f4f7e9d1ef75a895481",
    ),
]


def fetch(reference: Reference) -> Path:
    """Download one reference recording and verify its checksum."""
    path = REFERENCE_DIR / f"{reference.name}.flac"
    if not path.exists():
        REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            BASE_URL + reference.path, headers={"User-Agent": "nightmusic/0.1"}
        )
        with urllib.request.urlopen(request, timeout=600) as response:
            path.write_bytes(response.read())
    digest = hashlib.sha1(path.read_bytes()).hexdigest()  # noqa: S324 (the archive gives SHA-1)
    if digest != reference.sha1:
        raise RuntimeError(f"{path}: wrong checksum {digest}")
    return path


def load_stereo(path: Path) -> np.ndarray:
    """Read a two-channel file at the project sample rate."""
    data, rate = soundfile.read(str(path), dtype="float32", always_2d=True)
    if data.shape[1] == 1:
        data = np.repeat(data, 2, axis=1)
    if rate != dsp.RATE:
        data = soxr.resample(data, rate, dsp.RATE, quality="HQ")
    return data[:, :2].astype(np.float32)


@dataclass
class Measurement:
    """Numbers that describe one recording."""

    seconds: float
    loudness_lufs: float
    loudness_range: float
    short_term_p10: float  # short-term loudness relative to the integrated loudness
    short_term_p50: float
    short_term_p95: float
    peak_db: float
    crest_db: float
    correlation: float  # correlation of the left and the right channel
    side_db: float  # level of the side signal relative to the mid signal
    centres: np.ndarray
    balance: np.ndarray  # level of each third-octave band relative to the total, in dB


def short_term_loudness(audio: np.ndarray) -> np.ndarray:
    """Return the short-term loudness (3 s window, 1 s step) in LUFS (ITU-R BS.1770)."""
    # K-weighting: a high shelf and a high-pass filter.
    shelf = signal.lfilter(*_k_shelf(), audio.astype(np.float64), axis=0)
    weighted = signal.lfilter(*_k_highpass(), shelf, axis=0)
    power = np.square(weighted)
    window, step = 3 * dsp.RATE, dsp.RATE
    sums = np.concatenate((np.zeros((1, power.shape[1])), np.cumsum(power, axis=0)))
    starts = np.arange(0, len(audio) - window + 1, step)
    mean = (sums[starts + window] - sums[starts]) / window
    return -0.691 + 10.0 * np.log10(np.maximum(mean.sum(axis=1), 1e-12))


def _k_shelf() -> tuple[np.ndarray, np.ndarray]:
    frequency, gain_db, q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    k = np.tan(np.pi * frequency / dsp.RATE)
    vh = 10.0 ** (gain_db / 20.0)
    vb = vh**0.4996667741545416
    a0 = 1.0 + k / q + k * k
    b = np.array([(vh + vb * k / q + k * k) / a0, 2.0 * (k * k - vh) / a0,
                  (vh - vb * k / q + k * k) / a0])  # fmt: skip
    a = np.array([1.0, 2.0 * (k * k - 1.0) / a0, (1.0 - k / q + k * k) / a0])
    return b, a


def _k_highpass() -> tuple[np.ndarray, np.ndarray]:
    frequency, q = 38.13547087602444, 0.5003270373238773
    k = np.tan(np.pi * frequency / dsp.RATE)
    a0 = 1.0 + k / q + k * k
    b = np.array([1.0, -2.0, 1.0])
    a = np.array([1.0, 2.0 * (k * k - 1.0) / a0, (1.0 - k / q + k * k) / a0])
    return b, a


def loudness_range(short_term: np.ndarray) -> tuple[float, np.ndarray]:
    """Return the loudness range (EBU Tech 3342) and the gated short-term values."""
    gated = short_term[short_term > -70.0]
    if len(gated) == 0:
        return 0.0, gated
    mean = 10.0 * np.log10(np.mean(10.0 ** (gated / 10.0)))
    gated = gated[gated > mean - 20.0]
    if len(gated) == 0:
        return 0.0, gated
    return float(np.percentile(gated, 95) - np.percentile(gated, 10)), gated


def measure(audio: np.ndarray) -> Measurement:
    """Measure a two-channel recording."""
    meter = pyloudnorm.Meter(dsp.RATE)
    integrated = float(meter.integrated_loudness(audio.astype(np.float64)))
    short_term = short_term_loudness(audio)
    spread, gated = loudness_range(short_term)
    relative = gated - integrated if len(gated) else np.zeros(1)
    peak = float(np.max(np.abs(audio)))
    left, right = audio[:, 0].astype(np.float64), audio[:, 1].astype(np.float64)
    mid, side = 0.5 * (left + right), 0.5 * (left - right)
    centres, levels = dsp.third_octave_levels(mid.astype(np.float32))
    total = 10.0 * np.log10(np.sum(10.0 ** (levels / 10.0)))
    return Measurement(
        seconds=len(audio) / dsp.RATE,
        loudness_lufs=integrated,
        loudness_range=spread,
        short_term_p10=float(np.percentile(relative, 10)),
        short_term_p50=float(np.percentile(relative, 50)),
        short_term_p95=float(np.percentile(relative, 95)),
        peak_db=dsp.to_db(peak),
        crest_db=dsp.to_db(peak / max(dsp.rms(audio), 1e-12)),
        correlation=float(np.corrcoef(left, right)[0, 1]),
        side_db=dsp.to_db(dsp.rms(side) / max(dsp.rms(mid), 1e-12)),
        centres=centres,
        balance=levels - total,
    )


def measure_references() -> None:
    """Measure all reference recordings and write the two tables."""
    results = [(reference, measure(load_stereo(fetch(reference)))) for reference in REFERENCES]
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "recording",
                "minutes",
                "integrated_loudness_lufs",
                "loudness_range_lu",
                "short_term_10th_percentile_lu",
                "short_term_median_lu",
                "short_term_95th_percentile_lu",
                "peak_db",
                "crest_factor_db",
                "left_right_correlation",
                "side_level_db",
            ]  # fmt: skip
        )
        for reference, m in results:
            writer.writerow(
                [
                    reference.work,
                    f"{m.seconds / 60:.2f}",
                    f"{m.loudness_lufs:.1f}",
                    f"{m.loudness_range:.1f}",
                    f"{m.short_term_p10:.1f}",
                    f"{m.short_term_p50:.1f}",
                    f"{m.short_term_p95:.1f}",
                    f"{m.peak_db:.1f}",
                    f"{m.crest_db:.1f}",
                    f"{m.correlation:.2f}",
                    f"{m.side_db:.1f}",
                ]  # fmt: skip
            )
    balances = np.array([m.balance for _, m in results])
    with TARGET_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["band_hz", "mean_db", "lowest_db", "highest_db"])
        for index, centre in enumerate(results[0][1].centres):
            column = balances[:, index]
            writer.writerow(
                [
                    f"{centre:.0f}",
                    f"{column.mean():.1f}",
                    f"{column.min():.1f}",
                    f"{column.max():.1f}",
                ]  # fmt: skip
            )


def target_balance() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Read the target tone balance: centres, mean, lowest, highest (dB re total)."""
    with TARGET_FILE.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    columns = ["band_hz", "mean_db", "lowest_db", "highest_db"]
    return tuple(np.array([float(row[c]) for row in rows]) for c in columns)  # type: ignore[return-value]


def matching_filter(audio: np.ndarray, strength: float = 0.8, limit_db: float = 6.0) -> np.ndarray:
    """Return a linear-phase filter that moves the tone balance of a mix to the target.

    The filter changes only the bands from 50 Hz to 8 kHz: the references are
    not reliable outside these bands. The change in one band is not more than
    `limit_db`.
    """
    centres, mean, _low, _high = target_balance()
    measured = measure(audio).balance
    difference = np.clip((mean - measured) * strength, -limit_db, limit_db)
    # A smooth curve: mean of each band and its two adjacent bands.
    smooth = np.convolve(np.pad(difference, 1, mode="edge"), np.ones(3) / 3, mode="valid")
    smooth[(centres < 48) | (centres > 8200)] = 0.0
    frequencies = np.concatenate(([0.0], centres, [dsp.RATE / 2]))
    gains = np.concatenate(([smooth[0]], smooth, [smooth[-1]]))
    grid = np.linspace(0.0, dsp.RATE / 2, 2049)
    log_grid = np.log10(np.maximum(grid, 1.0))
    log_frequencies = np.log10(np.maximum(frequencies, 1.0))
    response = 10.0 ** (np.interp(log_grid, log_frequencies, gains) / 20.0)
    return signal.firwin2(4097, grid, response, fs=dsp.RATE)


def match_tone_balance(audio: np.ndarray) -> np.ndarray:
    """Return the mix with the tone balance of the reference recordings."""
    taps = matching_filter(audio)
    channels = [signal.oaconvolve(audio[:, c], taps, mode="same") for c in range(audio.shape[1])]
    return np.stack(channels, axis=1).astype(np.float32)
