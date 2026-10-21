"""Shared fixtures and helpers for the trie benchmarks."""

from pathlib import Path
from typing import Final

import pytest
from pure_python import Trie as PureTrie

from fast_collections import Trie as FastTrie

DATA_DIR: Final = Path(__file__).resolve().parent / "data"

DATASET_FILES: Final = (
    pytest.param("words_real_10k.txt", id="real"),
    pytest.param("words_synth_10k.txt", id="synth"),
    pytest.param("words_chain_1k.txt", id="chain"),
)

IMPLEMENTATIONS: Final = (
    pytest.param(FastTrie, id="fast_collections"),
    pytest.param(PureTrie, id="pure_python"),
)


@pytest.fixture(scope="session", params=DATASET_FILES)
def words(request) -> list[str]:
    """Load a dataset file once per test session."""
    path = DATA_DIR / request.param
    return path.read_text(encoding="utf-8").splitlines()


@pytest.fixture(scope="session", params=IMPLEMENTATIONS)
def trie_cls(request):
    """The trie implementation class to benchmark."""
    return request.param


@pytest.fixture(scope="session")
def filled_trie(trie_cls, words):
    """A trie pre-filled with the whole dataset, plus the words."""
    trie = trie_cls()
    for word in words:
        trie.insert(word)
    return trie, words
