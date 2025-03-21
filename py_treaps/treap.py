"""
This module contains the definition of an unimplemented Treap class.

You should fill out this implementation in treap_map.py.

"""

from __future__ import annotations
import random
import typing
from abc import ABC
from collections.abc import Iterable, Iterator
from typing import Any, Generic, List, Optional, TypeVar, cast

from py_treaps.comparable import Comparable, KT, VT
from py_treaps.treap_node import TreapNode


class Treap(ABC, Generic[KT, VT], Iterable):
    """
    A form of key-value tree map which relies on randomly generated
    priorities to stay balanced.
    """

    def get_root_node(self) -> Optional[TreapNode]:
        """Return the internal TreeNode that represents the root
        element.

        Note that a "real" Treap would not have a function like this that
        exposes the internal workings. We require you to implement this so that
        we can verify that you are actually implementing a treap and not
        simply using another data structure.

        Returns:
            The TreeNode identified as the root, or None if the Treap
            is empty.
        """
        raise NotImplementedError("unimplemented method `get_root_node`")

    def lookup(self, key: KT) -> Optional[VT]:
        """Retrieve the value associated with a key in this Treap.

        Args:
            key: The key whose associated value should be retrieved.

        Returns:
            The value associated with the key, or `None` if the key
            is not in this Treap.
        """
        raise NotImplementedError("unimplemented method `lookup`")

    def insert(self, key: KT, value: VT) -> None:
        """Add a key-value pair to this Treap.

        Any old value associated with the key is lost.

        Args:
            key: The key to add to this Treap. Cannot be None.
            value: The value to associate with the key. Cannot be None.
        """
        raise NotImplementedError("unimplemented method `insert`")

    def remove(self, key: KT) -> Optional[VT]:
        """Remove a key from this Treap.

        If the key is not present in this Treap, this method does
        nothing.

        Args:
            key: The key to remove.

        Returns:
            The value associated with the key, or `None` if the key
            is not present.
        """
        raise NotImplementedError("unimplemented method `remove`")

    def split(self, threshold: KT) -> List[Treap[KT, VT]]:
        """Split this Treap into two Treaps.

        The left Treap should contain keys less than `threshold`, while
        the right Treap should contain values greater than or equal to
        `threshold`.

        Args:
            key: The key to split this Treap with.

        Returns:
            A list containing two Treaps. The left Treap should be
            in index 0 and the right Treap should be in index 1.
        """
        raise NotImplementedError("unimplemented method `split`")

    def join(self, other: Treap[KT, VT]) -> None:
        """Join this Treap with another Treap.

        At the end of the join, this Treap will contain the result.
        This method may destructively modify both Treaps.

        Args:
            other: The Treap to join with.
        """
        raise NotImplementedError("unimplemented method `join`")

    def meld(self, other: Treap[KT, VT]) -> None:
        """Meld this Treap with another Treap.

        At the end of the meld, this Treap will contain the result.
        This method may destructively modify both Treaps.

        If you don't implement this method, raise an `AttributeError`.

        Args:
            other: The Treap to meld with.

        Raises:
            AttributeError: Signifies the intent to leave this method
                unimplemented.

        Example
        -------
        ```
        def meld(self, other: "Treap[KT, VT]") -> None:
            raise AttributeError
        ```
        """
        raise NotImplementedError("unimplemented method `meld`")

    def difference(self, other: Treap[KT, VT]) -> None:
        """Remove elements in another Treap from this Treap.

        At the end of the difference, this Treap will contain no keys
        that were present in the other Treap. This method may
        destructively modify both Treaps.

        If you don't implement this method, raise an `AttributeError`.

        Args:
            other: A Treap containing elements to remove from this
                Treap.

        Raises:
            AttributeError: Signifies the intent to leave this method
                unimplemented.

        Example
        -------
        ```
        def difference(self, other: "Treap[KT, VT]") -> None:
            raise AttributeError
        ```
        """
        raise NotImplementedError("unimplemented method `difference`")

    def balance_factor(self) -> float:
        """Return the balance factor of the Treap.

        The balance factor is the height of the Treap divided by the minimum
        possible height of a Treap of this size. A perfectly balanced Treap
        has a balance factor of 1.0.

        If you don't implement this method, raise an `AttributeError`.

        Raises:
            AttributeError: Signifies the intent to leave this method
                unimplemented.

        Example
        -------
        ```
        def balance_factor(self) -> float:
            raise AttributeError
        ```
        """
        raise NotImplementedError("unimplemented method `balance_factor`")

    def __str__(self) -> str:
        """Build a human-readable representation of this Treap.

        Each node in the Treap is represented on its own line as

            [priority] <key, value>

        Subtreaps are indented one tab over from their parent for
        formatting. This method generates the string representations
        of keys and values by using the Python built-in `str()`
        function. The representation generated by this method should
        be in pre-order traversal fashion.

        This function will not be tested against the autograder.

        Returns:
            A string containing the human-readable representation of
            this Treap, formatted according the rules above.
        """
        raise NotImplementedError("unimplemented method `__str__`")

    def __iter__(self) -> typing.Iterator[KT]:
        """Return a new iterator object over the keys in this Treap.

        The iterator returned by this method should be fresh: it points
        to the first element in this Treap.

        The iterator should iterate in sorted order.
        """
        raise NotImplementedError("unimplemented method `__iter__`")
