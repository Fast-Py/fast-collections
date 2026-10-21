"""Pure Python reference implementation of the trie.

Mirrors the public API of ``fast_collections.Trie`` (the Rust
implementation) so that benchmarks can compare the two fairly. Uses
plain ``dict`` objects for children, the idiomatic Python equivalent
of the Rust ``HashMap<char, Box<Trie>>``.
"""

from __future__ import annotations


class Trie:
    """A prefix tree (trie) implemented in pure Python."""

    def __init__(self) -> None:
        self._root = _Node()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self._root
        for char in word:
            node = node.children.setdefault(char, _Node())
        node.is_end = True

    def search(self, word: str) -> bool:
        """Check if a word has been inserted into the trie."""
        node = _find_node(self._root, word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any inserted word starts with the given prefix."""
        return _find_node(self._root, prefix) is not None

    def delete(self, word: str) -> bool:
        """Delete a word from the trie, returning whether it existed."""
        return self._root.delete_rec(word)

    def word_count(self) -> int:
        """Return the number of words stored in the trie."""
        return self._root.count_words()

    def collect_words(self) -> list[str]:
        """Return all words stored in the trie."""
        words: list[str] = []
        self._root.collect_rec("", words)
        return words

    def __contains__(self, word: str) -> bool:
        """Support the ``in`` operator."""
        return self.search(word)

    def __len__(self) -> int:
        """Support the ``len()`` function."""
        return self.word_count()


class _Node:
    """A single node of the trie."""

    def __init__(self) -> None:
        self.children: dict[str, _Node] = {}
        self.is_end = False

    def delete_rec(self, word: str) -> bool:
        """Recursively delete a word, returning whether it was found."""
        if not word:
            return self._unmark_end()
        child = self.children.get(word[0])
        if child is None:
            return False
        return self._delete_and_prune(word[0], child, word[1:])

    def count_words(self) -> int:
        """Count words in the subtree rooted at this node."""
        subtotal = sum(child.count_words() for child in self.children.values())
        return subtotal + int(self.is_end)

    def collect_rec(self, prefix: str, words: list[str]) -> None:
        """Collect all words in the subtree into the result list."""
        if self.is_end:
            words.append(prefix)
        for char, child in self.children.items():
            child.collect_rec(prefix + char, words)

    def _unmark_end(self) -> bool:
        """Unmark the end-of-word flag, returning whether it was set."""
        if not self.is_end:
            return False
        self.is_end = False
        return True

    def _is_empty(self) -> bool:
        """Check whether the node has no children and is not a word end."""
        return not self.children and not self.is_end

    def _delete_and_prune(self, char: str, child: _Node, word: str) -> bool:
        """Delete from the child subtree and prune it if empty."""
        found = child.delete_rec(word)
        if found and child._is_empty():
            self.children.pop(char)
        return found


def _find_node(root: _Node, word: str) -> _Node | None:
    """Return the node at the end of the word, or None."""
    node = root
    for char in word:
        node = node.children.get(char)
        if node is None:
            return None
    return node
