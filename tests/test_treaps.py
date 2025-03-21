from random import random, randrange

from Tools.demo.sortvisu import insertionsort

from py_treaps.treap_map import TreapMap

import pytest
from typing import Any

# This file includes some starter test cases that you can use
# as a template to test your code and write your own test cases.
# You should write more tests; passing the following tests is
# NOT sufficient to guarantee that your code works.
# For example, there is no test for join(). You should write some.
# Be sure to read the test cases carefully.

def test_empty_lookup_starter() -> None: #PASS
    """Test `lookup` on an empty Treap."""

    treap: TreapMap[Any, Any] = TreapMap()

    assert not treap.lookup(6)
    assert not treap.lookup(0)
    assert not treap.lookup("hi")


def test_single_insert_starter() -> None: #PASS
    """Test minimal insert/lookup functionality."""

    treap: TreapMap[str, str] = TreapMap()
    treap.insert("one", "one")

    assert treap.lookup("one") == "one"
    assert not treap.lookup("two")
    print(treap)

def test_CUSTOM_string_number_input()->None: #PASS
    #Custom Case: string number
    treap: TreapMap[str, str] = TreapMap()
    list = ["one", "five", "ten", "eleven", "fifteen", "twenty", "twenty-five", "thirty"]
    for word in list:
        treap.insert(word, word)
        assert treap.lookup(word) == word
    print("\n", treap)

def test_multiple_insert_starter() -> None: #PASS
    """Test the insertion and lookup of multiple elements."""

    treap: TreapMap[int, str] = TreapMap()
    N = 20

    #Custom Case: random key
    for i in range(N):
        num=randrange(50)
        treap.insert(num, str(num))
        assert treap.lookup(num) == str(num)
    print("\n", treap)

    #Given Case: increasing key
    for i in range(N):
        treap.insert(i, str(i))
        assert treap.lookup(i) == str(i)
    print("\n", treap)
    # make sure all nodes are still there
    for i in range(N):
        assert treap.lookup(i) == str(i)

def test_insert_overwrite_starter() -> None: #PASS
    """Test whether multiple insertions to the same key overwrites
    the value.
    """

    treap: TreapMap[int, str] = TreapMap()
    for i in range(10):
        treap.insert(i, str(i))
    print("\n", treap)

    for value in ("hi", "foo", "bar"):
        treap.insert(2, value)
        assert treap.lookup(2) == value
    print("\n", treap)

def test_empty_remove_starter() -> None: #PASS
    """Test `remove` on an empty Treap."""
    treap_empty: TreapMap[str, int] = TreapMap()
    assert treap_empty.remove("hi") is None

    """Test 'remove' on not empty Treap"""
    N=20
    s = set()
    treap: TreapMap[int, int] = TreapMap()
    for i in range(N):
        num = randrange(N)
        s.add(num)
        treap.insert(num, num)
    print("\n", treap)
    # Remove non-existent key
    assert treap.remove(21) is None
    # Remove all inserted keys
    for i in s:
        assert treap.remove(i) == i
        print("\n", treap)
    print("\n", treap)

    """Test 'remove' on root"""
    treap: TreapMap[int, int] = TreapMap()
    for i in range(N):
        num = randrange(N)
        treap.insert(num, num)
    print("\n", treap)
    root = treap.get_root_node()
    assert treap.remove(root.key) == root.value

def test_CUSTOM_remove()->None: #PASS
    # Will error out - check manually
    treap: TreapMap[int, str] = TreapMap()
    i=0
    s = {"hi", "foo", "bar", "car", "dog", "moo"}
    for value in s:
        treap.insert(i, value)
        i = i+1
    print("\n", treap)
    i=0
    for value in s:
        assert treap.remove(i) == value
        i = i+1
        print("\n", treap)

def test_iterator_exception_starter() -> None: #PASS
    """Test that the TreapMap iterator raises a StopIteration
    when exhausted.
    """
    treap: TreapMap[int, str] = TreapMap()

    it = iter(treap)
    with pytest.raises(StopIteration):
        next(it)

def test_split_by_median_starter() -> None: #PASS
    """Test `split` with the median key."""

    original_treap = TreapMap()
    original_treap1 = TreapMap()

    #Custom Case: split & join empty tree
    new_treaps = original_treap.split(1)
    original_treap.join(original_treap1)

    #Custom Case: split with left/right subtree being empty, not-empty , split with non-existent threshold, split with existent threshold
    #Actual tree

    for i in range(11):
        if i == 6:
            continue
        original_treap.insert(i, str(i))
    print("\n", original_treap)
    # Test iterator
    keys = list(iter(original_treap))

    #new_treaps = original_treap.split(5) #existent threshold #PASS
    new_treaps = original_treap.split(6) #non-existent threshold #PASS
    # new_treaps = original_treap.split(-1) #left subtree being empty #PASS
    # new_treaps = original_treap.split(11) #right subtree being empty #PASS
    # new_treaps = original_treap.split(-1) #left subtree being empty, nonexistent threshold #PASS
    # new_treaps = original_treap.split(11) #right subtree being empty, nonexistent threshold #PASS

    # Test split & join methods
    left = new_treaps[0]
    right = new_treaps[1]
    print("\n", left)
    print("\n", right)

    for key in left:
        assert 0 <= key < 5
    for i in range(5, 11):
        assert right.lookup(i) == str(i)

    """
    # Custom Cases: join empty trees
    print("\n", original_treap)
    original_treap.join(original_treap1)
    original_treap1.join(original_treap)
    print("\n", original_treap)
    """

    #Custom Case: Join testing
    left.join(right)
    print("\n", left)

def test_get_root_node_starter() -> None: #PASS
    """Test that the root node works as expected"""

    t = TreapMap()
    for i in range(10):
        t.insert(i, i)
    root_node = t.get_root_node()
    assert root_node.key in list(range(10))
    assert root_node.value in list(range(10))
    assert root_node.parent is None
    assert root_node.left_child is not None or root_node.right_child is not None


def test_heap_property_simple_starter() -> None: #PASS
    """Test heap property in a basic way"""

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root_node = t.get_root_node()

        # Is this sufficient to test the heap property?

        if (
            root_node.key != "0"
        ):  # why does this if statement exist? What if you remove it?
            assert root_node.priority >= root_node.left_child.priority
        if root_node.key != "9":
            assert root_node.priority >= root_node.right_child.priority


def test_bst_property_simple_starter() -> None: #PASS
    """Test BST property in a basic way"""

    for _ in range(50):  # Run this test a bunch to account for randomness
        t = TreapMap()
        for i in range(10):
            t.insert(str(i), str(i))
        root_node = t.get_root_node()

        # Is this sufficient to test the BST property?

        if root_node.key != "0":
            assert root_node.key >= root_node.left_child.key
        if root_node.key != "9":
            assert root_node.key <= root_node.right_child.key

