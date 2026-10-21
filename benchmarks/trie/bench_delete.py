"""Delete benchmarks for the trie implementations."""

import pytest


def _delete_words(trie_cls, words):
    """Delete all words from a fresh trie."""
    trie = trie_cls()
    for word in words:
        trie.insert(word)
    for word in words:
        trie.delete(word)


@pytest.mark.benchmark(group="delete")
def test_delete(benchmark, trie_cls, words) -> None:
    """Benchmark deleting the whole dataset from a fresh trie."""
    benchmark(_delete_words, trie_cls, words)
