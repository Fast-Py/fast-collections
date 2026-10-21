"""Insert benchmarks for the trie implementations."""

import pytest


def _insert_words(trie_cls, words):
    """Insert all words into a fresh trie and return it."""
    trie = trie_cls()
    for word in words:
        trie.insert(word)
    return trie


@pytest.mark.benchmark(group="insert")
def test_insert(benchmark, trie_cls, words) -> None:
    """Benchmark inserting the whole dataset into a fresh trie."""
    benchmark(_insert_words, trie_cls, words)
