"""Search benchmarks for the trie implementations."""

import pytest


def _search_words(trie, words):
    """Search all words in the pre-filled trie."""
    for word in words:
        trie.search(word)


@pytest.mark.benchmark(group="search")
def test_search(benchmark, filled_trie) -> None:
    """Benchmark searching all words in the pre-filled trie."""
    trie, words = filled_trie
    benchmark(_search_words, trie, words)
