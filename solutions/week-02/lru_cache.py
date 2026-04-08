"""
Problem: LRU Cache (LeetCode #146)
Difficulty: Medium

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity) Initialize with positive size capacity.
- int get(int key) Return the value of the key if it exists, otherwise return -1.
- void put(int key, int value) Update or add the value. If capacity exceeded, evict LRU.

Both get and put must run in O(1) average time complexity.

Key Insight:
- HashMap for O(1) lookup
- Doubly Linked List for O(1) insert/delete
- Most recently used at front, least recently used at back
"""

from collections import OrderedDict


class DLLNode:
    """Doubly Linked List Node"""
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache with HashMap + Doubly Linked List
    
    Time Complexity: O(1) for both get and put
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> DLLNode
        
        # Dummy head and tail for easier edge case handling
        self.head = DLLNode()  # Most recently used
        self.tail = DLLNode()  # Least recently used
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_to_front(self, node: DLLNode) -> None:
        """Add node right after head (most recently used position)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: DLLNode) -> None:
        """Remove node from its current position"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_front(self, node: DLLNode) -> None:
        """Move existing node to front (mark as recently used)"""
        self._remove_node(node)
        self._add_to_front(node)
    
    def _remove_lru(self) -> DLLNode:
        """Remove and return the least recently used node (before tail)"""
        lru = self.tail.prev
        self._remove_node(lru)
        return lru
    
    def get(self, key: int) -> int:
        """Get value by key, return -1 if not found"""
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_front(node)  # Mark as recently used
        return node.val
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair"""
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.val = value
            self._move_to_front(node)
        else:
            # Insert new
            if len(self.cache) >= self.capacity:
                # Evict LRU
                lru = self._remove_lru()
                del self.cache[lru.key]
            
            # Add new node
            new_node = DLLNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)


class LRUCacheSimple:
    """
    Simplified LRU Cache using Python's OrderedDict
    
    OrderedDict maintains insertion order and supports move_to_end()
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
            self.cache[key] = value
        else:
            if len(self.cache) >= self.capacity:
                # Remove first item (least recently used)
                self.cache.popitem(last=False)
            self.cache[key] = value


# Test cases
if __name__ == "__main__":
    # Test LRU Cache implementation
    cache = LRUCache(2)
    
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, "Failed: get(1) should return 1"
    
    cache.put(3, 3)  # Evicts key 2
    assert cache.get(2) == -1, "Failed: get(2) should return -1 (evicted)"
    
    cache.put(4, 4)  # Evicts key 1
    assert cache.get(1) == -1, "Failed: get(1) should return -1 (evicted)"
    assert cache.get(3) == 3, "Failed: get(3) should return 3"
    assert cache.get(4) == 4, "Failed: get(4) should return 4"
    
    print("✓ All LRUCache tests passed!")
    
    # Test OrderedDict version
    cache2 = LRUCacheSimple(2)
    
    cache2.put(1, 1)
    cache2.put(2, 2)
    assert cache2.get(1) == 1
    cache2.put(3, 3)
    assert cache2.get(2) == -1
    
    print("✓ All LRUCacheSimple tests passed!")

