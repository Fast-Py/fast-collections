from typing import Generic, TypeVar

_T = TypeVar("_T")

class Stack(Generic[_T]):
    """
    A last-in-first-out (LIFO) stack data structure.

    Provides O(1) push and pop operations on the top of the stack.
    The stack is generic: element types are determined by the ``T`` type parameter.

    Examples:
        >>> s = Stack[int]()
        >>> s.is_empty()
        True
        >>> s.push(1)
        >>> s.push(2)
        >>> s.pop()
        2
        >>> s.pick()
        1
    """

    def __init__(self) -> None:
        """
        Initialize an empty stack.

        Examples:
            >>> s = Stack[int]()
            >>> s.is_empty()
            True
        """

    def is_empty(self) -> bool:
        """
        Check whether the stack is empty.

        Returns:
            True if there are no elements on the stack, False otherwise.

        Complexity: O(1)

        Examples:
            >>> s = Stack[int]()
            >>> s.is_empty()
            True
            >>> s.push(1)
            >>> s.is_empty()
            False
        """

    def pick(self) -> _T:
        """
        Return the top element of the stack without removing it.

        Returns:
            The value at the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Complexity: O(1)

        Examples:
            >>> s = Stack[int]()
            >>> s.push(1)
            >>> s.push(2)
            >>> s.pick()
            2
            >>> s.is_empty()
            False
        """

    def pop(self) -> _T:
        """
        Remove and return the top element of the stack.

        Returns:
            The value at the top of the stack. The stack size decreases by one.

        Raises:
            IndexError: If the stack is empty.

        Complexity: O(1)

        Examples:
            >>> s = Stack[int]()
            >>> s.push(1)
            >>> s.push(2)
            >>> s.pop()
            2
            >>> s.pick()
            1
        """

    def push(self, value: _T) -> None:
        """
        Push a value onto the top of the stack.

        Args:
            value: The value to add to the stack.

        Complexity: O(1)

        Examples:
            >>> s = Stack[int]()
            >>> s.push(1)
            >>> s.pick()
            1
        """
