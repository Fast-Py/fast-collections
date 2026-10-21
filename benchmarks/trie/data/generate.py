"""Generate deterministic benchmark datasets for the trie benchmarks.

Run from the project root:

    python benchmarks/trie/data/generate.py

The script produces three files, committed to the repository:

- ``words_real_10k.txt``: 10,000 real English words sampled from the
  system dictionary (``/usr/share/dict/words``), filtered to lowercase
  ``a-z``, length 3-15. Represents a realistic production workload.
- ``words_synth_10k.txt``: 10,000 synthetic words built from short roots
  plus suffixes, so that words share realistic prefixes. Lets you control
  the workload profile (length distribution, prefix sharing).
- ``words_chain_1k.txt``: 1,000 adversarial words forming a deep shared
  chain with branches. Stresses trie depth and memory usage.

Each dataset is validated (no duplicates, no empty strings) and its
statistics are logged: word count, average length, unique prefixes.

All randomness is seeded (``SEED``), so the output is fully reproducible.
Generation parameters are module-level constants; change them and re-run
to regenerate the datasets.
"""

from __future__ import annotations

import logging
import random
import string
import sys
from pathlib import Path
from typing import Final

LOGGER: Final = logging.getLogger(__name__)
"""Module logger used to report dataset statistics."""

DATA_DIR: Final = Path(__file__).resolve().parent
"""Directory where the generated data files are stored."""

REAL_SOURCE: Final = Path("/usr/share/dict/words")
"""System dictionary used as the source of real English words."""

REAL_OUTPUT: Final = DATA_DIR / "words_real_10k.txt"
"""Output file for the real-words dataset."""

SYNTH_OUTPUT: Final = DATA_DIR / "words_synth_10k.txt"
"""Output file for the synthetic-words dataset."""

CHAIN_OUTPUT: Final = DATA_DIR / "words_chain_1k.txt"
"""Output file for the adversarial chain dataset."""

REAL_COUNT: Final = 10_000
"""Number of real words to sample from the dictionary."""

SYNTH_COUNT: Final = 10_000
"""Number of synthetic words to generate."""

CHAIN_COUNT: Final = 1_000
"""Number of adversarial chain words to generate."""

MIN_LEN: Final = 3
"""Minimum word length for real and synthetic words."""

MAX_LEN: Final = 15
"""Maximum word length for real and synthetic words."""

ALPHABET: Final = string.ascii_lowercase
"""Alphabet used to build synthetic words and chain suffixes."""

SEED: Final = 42
"""Seed for the random generator, makes the output reproducible."""

ROOT_COUNT: Final = 500
"""Number of short roots used as shared prefixes in synthetic words."""

ROOT_MIN_LEN: Final = 2
"""Minimum length of a synthetic word root."""

ROOT_MAX_LEN: Final = 4
"""Maximum length of a synthetic word root."""

MEAN_LEN: Final = 8
"""Mean of the normal distribution for synthetic word lengths."""

STD_LEN: Final = 3
"""Standard deviation of the normal distribution for word lengths."""

NESTED_COUNT: Final = 50
"""Number of nested prefixes (a, aa, aaa, ...) in the chain dataset."""

CHAIN_PREFIX_LEN: Final = 45
"""Length of the shared prefix in deep chain words."""

CHAIN_SUFFIX_LEN: Final = 5
"""Length of the random suffix appended to deep chain words."""


class _Generator:
    """Generate deterministic word datasets."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def real_words(self, count: int) -> list[str]:
        """Sample real English words from the system dictionary."""
        unique = self._read_dictionary()
        sample_size = min(count, len(unique))
        return sorted(self._rng.sample(unique, sample_size))

    def synthetic_words(self, count: int) -> list[str]:
        """Generate words with realistic shared prefixes."""
        roots = [
            self._random_word(self._rng.randint(ROOT_MIN_LEN, ROOT_MAX_LEN))
            for _ in range(ROOT_COUNT)
        ]
        words: set[str] = set()
        while len(words) < count:
            words.add(self._make_word(roots))
        return sorted(words)

    def chain_words(self, count: int) -> list[str]:
        """Generate adversarial data: a deep shared chain with branches."""
        words = {"a" * length for length in range(1, NESTED_COUNT + 1)}
        while len(words) < count:
            suffix = self._random_word(CHAIN_SUFFIX_LEN)
            words.add("a" * CHAIN_PREFIX_LEN + suffix)
        return sorted(words)

    def _read_dictionary(self) -> list[str]:
        """Read and filter words from the system dictionary."""
        if not REAL_SOURCE.exists():
            sys.exit(f"Dictionary not found: {REAL_SOURCE}")
        text = REAL_SOURCE.read_text(encoding="utf-8")
        words = [line.lower() for line in text.splitlines()]
        return sorted({word for word in words if _is_valid_word(word)})

    def _random_word(self, length: int) -> str:
        """Build a random word of the given length from the alphabet."""
        return "".join(self._rng.choice(ALPHABET) for _ in range(length))

    def _make_word(self, roots: list[str]) -> str:
        """Build one synthetic word from a random root."""
        root = self._rng.choice(roots)
        length = round(self._rng.gauss(MEAN_LEN, STD_LEN))
        length = min(max(length, max(MIN_LEN, len(root))), MAX_LEN)
        return root + self._random_word(length - len(root))


def _is_valid_word(word: str) -> bool:
    """Check that a word is lowercase a-z with realistic length."""
    if not (MIN_LEN <= len(word) <= MAX_LEN):
        return False
    return all(letter in ALPHABET for letter in word)


def _validate(words: list[str], dataset_name: str) -> None:
    """Raise an error if a dataset is malformed."""
    if not words:
        sys.exit(f"ERROR: {dataset_name} is empty")
    if len(set(words)) != len(words):
        sys.exit(f"ERROR: {dataset_name} contains duplicates")
    if any(not word for word in words):
        sys.exit(f"ERROR: {dataset_name} contains empty strings")


def _count_prefixes(words: list[str]) -> int:
    """Count unique prefixes across all words."""
    prefixes: set[str] = set()
    for word in words:
        for index in range(1, len(word) + 1):
            prefixes.add(word[:index])
    return len(prefixes)


def _report(words: list[str], dataset_name: str) -> None:
    """Validate a dataset and log its statistics."""
    _validate(words, dataset_name)
    total_len = sum(len(word) for word in words)
    avg_len = total_len / len(words)
    prefix_count = _count_prefixes(words)
    LOGGER.info(
        f"{dataset_name}: {len(words)} words, avg length {avg_len:.1f}, "
        f"unique prefixes {prefix_count}",
    )


def _write(words: list[str], output_path: Path) -> None:
    """Write a dataset to a file, one word per line."""
    joined_words = "\n".join(words)
    output_path.write_text(f"{joined_words}\n", encoding="utf-8")


def main() -> None:
    """Generate all three datasets and write them to files."""
    logging.basicConfig(level=logging.INFO)
    generator = _Generator(random.Random(SEED))

    real_words = generator.real_words(REAL_COUNT)
    _report(real_words, REAL_OUTPUT.name)
    _write(real_words, REAL_OUTPUT)

    synth_words = generator.synthetic_words(SYNTH_COUNT)
    _report(synth_words, SYNTH_OUTPUT.name)
    _write(synth_words, SYNTH_OUTPUT)

    chain_words = generator.chain_words(CHAIN_COUNT)
    _report(chain_words, CHAIN_OUTPUT.name)
    _write(chain_words, CHAIN_OUTPUT)


if __name__ == "__main__":
    main()
