from __future__ import annotations
import random
import typing
from collections.abc import Iterator
from logging import currentframe
from mailcap import lookup
from pickle import FALSE
from typing import List, Optional, cast

from py_treaps.treap import KT, VT, Treap
from py_treaps.treap_node import TreapNode


# Example usage found in test_treaps.py
class TreapMap(Treap[KT, VT]):
    # Add an __init__ if you want. Make the parameters optional, though.
    def __init__(self, key: Optional[KT] = None, value: Optional[VT] = None):
        # If the key & value are provided, then create a TreapNode object & make it the root
        if key is not None and value is not None:
            self.root = TreapNode(key, value)
        # No root node
        else:
            self.root = None

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
        return self.root

    def _lookup_node(self, key:KT) -> Optional[TreapNode]:
        """Retrieve the TreapNode object associated with a key in this Treap.

        Args:
            key: The key whose associated value should be retrieved.

        Returns:
            The TreapNode object associated with the key, or `None` if the key
            is not in this Treap.
        """
        current = self.root
        while current is not None:
            # Go to the right side of tree
            if current.key < key:
                # Traverse down the tree with the newly assigned current node
                current = current.right_child
                if current is None:
                    break
            # Go to the left side of tree
            elif current.key > key:
                current = current.left_child
                if current is None:
                    break
            # Found the node ('if current.key = key')
            else:
                return current
        # Did not find the node
        return None

    def lookup(self, key: KT) -> Optional[VT]:
        """Retrieve the value associated with a key in this Treap.

        Args:
            key: The key whose associated value should be retrieved.

        Returns:
            The value associated with the key, or `None` if the key
            is not in this Treap.
        """
        node = self._lookup_node(key)
        return node.value if node else None

    def insert(self, key: KT, value: VT) -> None:
        """
        Add a key-value pair to this Treap.
        """
        # Create object for new node 'x = TreapNode(key, value)'
        x = TreapNode(key, value)
        # call insert function to insert new node 'x' with a (key-value) pair
        self._generic_insert(x, False)

    def insert_priority(self, key: KT, value: VT, priority) -> None:
        """
        Add a key-value-priority pair to this Treap.
        """
        # Create object for new node 'x = TreapNode(key, value)'
        x = TreapNode(key, value)
        # Assign priority value to the new node 'x'
        x.priority = priority
        # call insert function to insert new node 'x' with a (key-value) pair
        self._generic_insert(x, True)

    def _generic_insert(self, x: TreapNode, priorityBool: bool) -> None:
        """Add a (key-value) or a (key-value-priority) to this Treap.
        Any old value associated with the key is lost.

        Insert node, with properties key & value, into appropriate position on tree. We first
        (1) insert at the appropriate leaf position using property 'key' & following BST rules, and then
        (2) fix property 'value' following Heap rules by rotating up the treap & reiterating with while loop until the parents have higher values

        Args:
            key: The key to add to this Treap. Cannot be None.
            value: The value to associate with the key. Cannot be None.
        """
        # Part 0) Make the node the root if there's no tree
        if self.root is None:
            self.root = x
            return

        # Part 1a) Check if a node with the same key already exists
        # Go to (2) Heap property if it does already exist
        existing_node = self._lookup_node(x.key)
        if existing_node:
            # Replace the value of the existing node
            existing_node.value = x.value
            if priorityBool:
                existing_node.priority = x.priority
            # Proceed to Part 2 with `existing_node` instead of `x`
            x = existing_node  # Set x to the existing node for priority correction
        # Part 1b) If key doesn't exist
        # Insert new node 'x' into the correct location for property 'key' following BST rules
        else:
            # Traverse the tree to find the correct position of the new node 'x'
            current = self.root
            while True:
                # Go to left child if new node's key is less
                if x.key < current.key:
                    # Assign the left child & parent (as its own) if there's no left child
                    if current.left_child is None:
                        current.left_child = x
                        x.parent = current
                        break # Once the new node is inserted, there's no need to continue to traverse the tree
                    # Moves to the next node if the current node already has a left child
                    else:
                        current = current.left_child
                # Go to right child if new node's key is greater
                elif x.key > current.key:
                    # Assign the right child & parent (as its own) if there's no right child
                    if current.right_child is None:
                        current.right_child = x
                        x.parent = current
                        break
                    else:
                        current = current.right_child

        # Part 2) Correct new node 'x' into the correct location for property 'priority' following Heap rules
        # Check's if new node 'x' is not the root & Heap property violated if 'x' priority is larger than its parent's priority
        while x.parent and x.priority > x.parent.priority:
            # if the new node 'x' is the left child
            if x == x.parent.left_child:
                self._rotate_right(x.parent)
            # if the new node 'x' is the right child
            else:
                self._rotate_left(x.parent)


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
        # Part 1) Find the deleted node x
        x = self._lookup_node(key)
        # Key is not found
        if x is None:
            return None

        # Part 2) Repeatedly rotate until the node becomes a leaf node
        # Not a leaf node if one of the child nodes exist
        while x.left_child or x.right_child:
            # If both children exist on the deleted node x
            if x.left_child and x.right_child:
                # Left child has higher priority --> rotate x right --> reiterate until 1 child left on x
                if x.left_child.priority > x.right_child.priority:
                    self._rotate_right(x)
                # Right child has higher priority --> rotate x left --> reiterate until 1 child left on x
                else:
                    self._rotate_left(x)
            # Left child exists only --> rotate x right
            elif x.left_child:
                self._rotate_right(x)
            # Right child exists only --> rotate x left
            elif x.right_child:
                self._rotate_left(x)

        # Part 3) Remove node x by updating the parent's pointer
        # The deleted node x is the root, therefore delete the root & tree
        if x.parent is None:
            self.root = None
        # Removes x from the tree by setting the parent's left child to None
        elif x == x.parent.left_child:
            x.parent.left_child = None
        # Removes x from the tree by setting the parent's right child to None
        else:
            x.parent.right_child = None

        return x.value

    def _rotate_left(self, node: TreapNode):
        """
        Rotates left around node
        """
        # New node 'x' is the right child of the node. This will be the new root when rotating left on the node
        new_root = node.right_child

        # Node adopts new root's left subtree whether it has a left child or is None
        node.right_child = new_root.left_child
        # Need to make sure that the new node 'x' left child has its parent set to node
        if new_root.left_child:
            new_root.left_child.parent = node
        # The new root's left child is the node
        new_root.left_child = node
        # Update parent's attribute
        self._update_parents(node, new_root)

    def _rotate_right(self, node: TreapNode):
        """
        Rotates right around node
        """
        # New node 'x' is the left child of the node. This will be the new root when rotating left on the node
        new_root = node.left_child

        # Node adopts new root's left subtree whether it has a left child or is None
        node.left_child = new_root.right_child
        # Need to make sure that the new node 'x' right child has its parent set to node
        if new_root.right_child:
            new_root.right_child.parent = node
        # The new root's right child is the node
        new_root.right_child = node
        # Update parent's attribute
        self._update_parents(node, new_root)

    def _update_parents(self, node:TreapNode, new_root:TreapNode):
        """
        Update's the parent's attributes: new_root, node parent's left or right child, and node
        """
        # The new root's parent is the node's parent
        new_root.parent = node.parent

        # if the node is the root, update to the new root
        if node.parent is None:
            self.root = new_root
        # if the node was the left child of its parent, assign new_root as the new left child of node's parent
        elif node == node.parent.left_child:
            node.parent.left_child = new_root
        # if the node was the right child of its parent, assign new_root as the new right child of node's parent
        else:
            node.parent.right_child = new_root

        # Node sets new parent to the new root
        node.parent = new_root

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
        # Part 0) Splitting an empty tree
        if self.root is None:
            return [TreapMap(), TreapMap()]

        # Part 1) Looking up if the node exists in the Treap. If it does, will return its own value. If it doesn't exist, will return None.
        existing_node = self._lookup_node(threshold)
        existing_node_value = existing_node.value
        existing_node_priority = existing_node.priority

        #Part 2) Insert the split node if it doesn't exist. If it does exist, save settings
        # Node doesn't exist -> value set as None -> deletes node after splitting since 'None' indicates a temp node
        if existing_node is None:
            split_node = TreapNode(threshold, None)
        # Node exists -> set value as itself
        else:
            split_node = TreapNode(threshold, existing_node.value)
        #split_node.priority = TreapNode.MAX_PRIORITY
        # Insert the split node because it doesn't exist -> makes it easier for splitting the tree b/c split_node will be new root due to MAX_PRIORITY
        self.insert_priority(split_node.key, split_node.value, TreapNode.MAX_PRIORITY)

        # Part 3) Split the Treap into 2 Treaps (t1, t2)
        # Objects for left & right trees
        t1 = TreapMap()
        t2 = TreapMap()
        # Split from the newly inserted node, which is the root now b/c MAX_PRIORITY
        # If there's no left child, t1 = None
        # Split into the left subtree
        if self.root.left_child:
            # Assign the left child of the root as the new root of t1
            t1.root = self.root.left_child
            # Disconnects from the original parent
            t1.root.parent = None
        # If there's no right child, t2 = None
        # Split into the right subtree
        if self.root.right_child:
            # Assign the right child of the root as the new root of t2
            t2.root = self.root.right_child
            # Disconnects from the original parent
            t2.root.parent = None

        if existing_node:
            t2.insert_priority(existing_node.key, existing_node_value, existing_node_priority)
        return [t1, t2]

    def join(self, other: Treap[KT, VT]) -> None:
        """Join this Treap with another Treap.

        At the end of the join, this Treap will contain the result.
        This method may destructively modify both Treaps.

        Args:
            other: The Treap to join with.
        """

        # Part 0) Handle an empty left or right tree
        # If both trees are empty
        if self.root is None and other.root is None:
            return
        # If the left tree is empty
        if self.root is None:
            self.root = other.root
            return
        # If the right tree is empty
        if other.root is None:
            return

        # Part 1) Create new node 'x' with MAX_PRIORITY to set it as the root in order to join self and _other
        x = TreapNode(float('inf'), None)
        x.priority = TreapNode.MAX_PRIORITY
        x.left_child = self.root
        x.right_child = other.root

        # Part 2) Assign join node 'x' as the parent of each of the roots
        # If the left tree exists
        self.root.parent = x
        other.root.parent = x

        # Part 3) Self and _other are joined under one (temp) root, which allows the remove operation to properly merge the two treaps
        # Set the join node 'x' as the current root
        self.root = x
        # Remove the join node 'x' since its temporary to merge self and _other root
        self.remove(x.key)

    def meld(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError
    def difference(self, other: Treap[KT, VT]) -> None: # KARMA
        raise AttributeError
    def balance_factor(self) -> float: # KARMA
        raise AttributeError
    def __str__(self) -> str:
        # (optional method, ungraded)
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
        # If the treap is empty
        if self.root is None:
            return "<empty treap>"

        def recurse(node: TreapNode, prefix: str = "") -> List[str]:
            # Base case: if the node is None, return an empty list
            if node is None:
                return []

            result = []
            # Add the current node's representation to the result list
            result.append(f"{prefix}[{node.priority}]<{node.key}, {node.value}>")

            # Check if the current node has children to include their representation
            if node.left_child is not None or node.right_child is not None:
                # Recursively add the left child with updated prefix
                if node.left_child:
                    result.extend(recurse(node.left_child, prefix + "L---"))
                else:
                    # If there is no left child, add a placeholder to indicate this
                    result.append(f"{prefix}L---<empty>")

                # Recursively add the right child with updated prefix
                if node.right_child:
                    result.extend(recurse(node.right_child, prefix + "R---"))
                else:
                    # If there is no right child, add a placeholder to indicate this
                    result.append(f"{prefix}R---<empty>")

            # Return the list of strings representing the current node and its children
            return result

        # Join all lines into a single string separated by newlines
        return "\n".join(recurse(self.root))

    def __iter__(self) -> typing.Iterator[KT]:
        """Return a new iterator object over the keys in this Treap.

        The iterator returned by this method should be fresh: it points
        to the first element in this Treap.

        The iterator should iterate in sorted order.

        In-Order Traversal: left subtree --> root --> right subtree
        """
        def inorderTraversal(node):
            if node is not None:
                # First recur on left subtree
                yield from inorderTraversal(node.left_child)

                # Now deal with the node
                yield node.key

                # Then recur on right subtree
                yield from inorderTraversal(node.right_child)

        yield from inorderTraversal(self.root)