import pytest

from fast_collections import Trie


def _insert_all(trie: Trie, words: list[str]) -> None:
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
def test_size_and_word_count(trie: Trie, words: list[str]) -> None:
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
def test_contains(
    trie: Trie, words: list[str], present: list[str], absent: list[str]
) -> None:
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
def test_starts_with(
    trie: Trie, words: list[str], prefix: str, expected: bool
) -> None:
    _insert_all(trie, words)
    assert trie.starts_with(prefix) is expected


@pytest.mark.parametrize(
    "words, to_delete, remaining",
    [
        (["app", "apple"], "apple", ["app"]),
        (["app", "apple"], "app", ["apple"]),
        (["hello", "world"], "hello", ["world"]),
        (["hello"], "hello", []),
        ([], "hello", []),
        (["hello"], "world", ["hello"]),
        (["", "a"], "", ["a"]),
    ],
)
def test_delete(
    trie: Trie, words: list[str], to_delete: str, remaining: list[str]
) -> None:
    "Test that deleting words updates the trie correctly."
    _insert_all(trie, words)

    assert trie.delete(to_delete) is (to_delete in words)
    assert not trie.search(to_delete)

    for word in remaining:
        assert trie.search(word)

    assert trie.word_count() == len(remaining)
