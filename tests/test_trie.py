import pytest


def _insert_all(trie, words):
    for w in words:
        trie.insert(w)


@pytest.mark.parametrize(
    "words", [[], ["hello"], ["hello", "world"], ["", "a", "b", "c"], ["a", "a", "b"]]
)
def test_size_and_word_count(trie, words):
    "Test that the trie has the correct size and word count"
    _insert_all(trie, words)
    expected = len(set(words))
    assert len(trie) == expected
    assert trie.word_count() == expected


@pytest.mark.parametrize(
    "words, present, absent",
    [
        (
            [
                "hello",
            ],
            [
                "hello",
            ],
            ["hell", "world"],
        ),
        ([], [], ["hello"]),
        (["a", "b", "c"], ["a", "b", "c"], []),
        (["a", "a", "b"], ["a", "b"], ["c"]),
    ],
)
def test_contains(trie, words, present, absent):
    "Test that the trie contains the correct words"
    _insert_all(trie, words)

    for w in present:
        assert w in trie

    for w in absent:
        assert w not in trie
        assert not trie.search(w)


@pytest.mark.parametrize(
    "words, prefix, expected",
    [
        (["hello"], "hello", True),
        (["hello"], "hell", True),
        (["hello"], "h", True),
        (["hello"], "", True),
        (["hello"], "help", False),
        (["hello", "world"], "wo", True),
        (["hello", "world"], "worl", True),
        (["hello", "world"], "x", False),
    ],
)
def test_starts_with(trie, words, prefix, expected):
    _insert_all(trie, words)
    assert trie.starts_with(prefix) is expected
