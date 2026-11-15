"""Registry of the open data files that the style study measures.

The study does not keep these files in the repository. The `fetch` function
downloads each file into the local cache directory. Each entry records the
source address and the licence of the file.
"""

from __future__ import annotations

import hashlib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

CACHE_DIR = Path(".cache/corpus")
USER_AGENT = "nightmusic-study/0.1 (style study script)"


@dataclass(frozen=True)
class CorpusFile:
    """One downloadable data file."""

    key: str
    filename: str
    url: str
    licence: str
    description: str

    @property
    def path(self) -> Path:
        return CACHE_DIR / self.filename


_BAGATELLES_BASE = "https://raw.githubusercontent.com/DCMLab/bartok_bagatelles/main/notes/"

CORPUS: dict[str, CorpusFile] = {
    entry.key: entry
    for entry in [
        CorpusFile(
            key="vn-billam",
            filename="verklaerte_nacht.muscript.txt",
            url="https://peterbillam.gitlab.io/pjb_arrangements/arr/src/verklaerte_nacht.txt",
            licence="CC BY 4.0",
            description=(
                "Schoenberg, Verklärte Nacht op. 4, complete, arranged for piano by "
                "Peter Billam (2013). Text source in the muscript format."
            ),
        ),
        CorpusFile(
            key="ood-bednarek",
            filename="bartok_out_of_doors.mid",
            url=(
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                "B%C3%A9la%20Bart%C3%B3k%2C%20Out%20of%20Doors%20Suite%2C%20Sz%2081.mid"
            ),
            licence="CC0 1.0",
            description=(
                "Bartók, Out of Doors Sz. 81, complete. MIDI capture of a piano "
                "performance by Michael Bednarek (Wikimedia Commons, 2026)."
            ),
        ),
        *[
            CorpusFile(
                key=f"bagatelle-{number:02d}",
                filename=f"bartok_op06n{number:02d}.notes.tsv",
                url=f"{_BAGATELLES_BASE}op06n{number:02d}.notes.tsv",
                licence="CC BY-NC-SA 4.0",
                description=(
                    f"Bartók, Fourteen Bagatelles op. 6, no. {number}. Note list from the "
                    "DCML corpus (Digital and Cognitive Musicology Lab)."
                ),
            )
            for number in range(1, 15)
        ],
    ]
}


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(key: str, *, force: bool = False) -> Path:
    """Download one corpus file into the cache and return its path."""
    entry = CORPUS[key]
    if entry.path.exists() and not force:
        return entry.path
    entry.path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(entry.url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    entry.path.write_bytes(data)
    return entry.path


def fetch_all(*, force: bool = False) -> list[Path]:
    """Download all corpus files."""
    return [fetch(key, force=force) for key in CORPUS]
