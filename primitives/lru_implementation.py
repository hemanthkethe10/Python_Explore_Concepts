class Node:
    """A node in the doubly linked list."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Hash Map: key -> Node
        
        # Initialize dummy head and tail nodes to simplify edge cases
        # Real list is between head and tail
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        """Always add new node right after head (MRU position)."""
        head_next = self.head.next
        node.next = head_next
        node.prev = self.head
        self.head.next = node
        head_next.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # Move the accessed node to the front (MRU)
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing node and move to front
            self._remove(self.cache[key])
        
        # Create new node
        new_node = Node(key, value)
        self._add(new_node)
        self.cache[key] = new_node
        
        # Check capacity
        if len(self.cache) > self.capacity:
            # Evict the LRU node (the one right before the dummy tail)
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

from collections import OrderedDict

class LRUCacheUsingOrderedDict:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        # Move the accessed item to the end (MRU position)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update value and mark as MRU
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        # Check capacity
        if len(self.cache) > self.capacity:
            # popitem(last=False) removes the first item (FIFO), 
            # which corresponds to the LRU in this design.
            self.cache.popitem(last=False)