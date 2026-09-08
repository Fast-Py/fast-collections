import pytest


def _insert_all(trie, words):
    for word in words:
        trie.insert(word)


@pytest.mark.parametrize(
    "words",
    [
        [],
        ["fast-collections"],
        ["hi", "honey"],
        ["", "abc", "def", "ghi"],
    ],
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
            ["hello!"],
        ),
        ([], [], ["hello"]),
        (
            ["cat", "car", "cart"],
            ["cat", "car", "cart"],
            ["card", "cas", "cal"],
        ),
        (["programming", "program"], ["program", "programming"], ["programme"]),
    ],
)
def test_contains(trie, words, present, absent):
    "Test that the trie contains the correct words"
    _insert_all(trie, words)

    for word in present:
        assert word in trie

    for word in absent:
        assert word not in trie
        assert not trie.search(word)


@pytest.mark.parametrize(
    "words, prefix, expected",
    [
        (["abc"], "ab", True),
        (["spaces"], "paces", False),
        (["complexity"], "complex", True),
        (["some_string"], "some_value", False),
        (["foo", "bar"], "bar", True),
        (["i", "love", "python"], "pyt", True),
        (["i", "love", "python"], "foo", False),
    ],
)
def test_starts_with(trie, words, prefix, expected):
    _insert_all(trie, words)
    assert trie.starts_with(prefix) is expected
