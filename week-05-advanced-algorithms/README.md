# Week 5: Advanced Algorithms

> Master specialized data structures and algorithm patterns

---

## 📖 High-Level Overview

This week covers advanced topics that frequently appear in interviews:
- Tries for efficient string operations
- Heaps for priority-based processing
- Interval problems for scheduling
- Backtracking for exhaustive search
- Bit manipulation for space-efficient solutions

### Key Patterns This Week:
1. **Trie** - Prefix trees for string problems
2. **Heap/Priority Queue** - Top K, merging sorted lists
3. **Intervals** - Merge, insert, scheduling
4. **Backtracking** - Permutations, combinations, subsets
5. **Bit Manipulation** - XOR tricks, bit masking

---

## 🔬 Low-Level Details

### Trie (Prefix Tree)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

**When to use Trie:**
- Autocomplete/prefix matching
- Spell checker
- Word search in grid
- IP routing (longest prefix match)

### Heap / Priority Queue

```python
import heapq

# Min heap (default in Python)
min_heap = []
heapq.heappush(min_heap, 3)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 2)
smallest = heapq.heappop(min_heap)  # 1

# Max heap (negate values)
max_heap = []
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -1)
largest = -heapq.heappop(max_heap)  # 3

# Heapify existing list
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)  # O(n)

# K largest elements
k_largest = heapq.nlargest(3, nums)

# K smallest elements
k_smallest = heapq.nsmallest(3, nums)

# Heap with custom key (use tuple)
items = [(priority, value) for priority, value in ...]
heapq.heapify(items)
```

**Top K Pattern:**
```python
def find_k_largest(nums, k):
    # Use min heap of size k
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    for num in nums[k:]:
        if num > min_heap[0]:
            heapq.heapreplace(min_heap, num)
    
    return min_heap  # Contains k largest elements
```

**Merge K Sorted Lists Pattern:**
```python
def merge_k_sorted(lists):
    min_heap = []
    
    # Add first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))
    
    result = []
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        
        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
    
    return result
```

### Interval Problems

**Merge Intervals:**
```python
def merge_intervals(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged
```

**Insert Interval:**
```python
def insert_interval(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result
```

### Backtracking

**Template:**
```python
def backtrack(state, choices, result):
    if is_goal(state):
        result.append(state.copy())
        return
    
    for choice in choices:
        if is_valid(choice, state):
            make_choice(choice, state)
            backtrack(state, choices, result)
            undo_choice(choice, state)  # Backtrack
```

**Subsets:**
```python
def subsets(nums):
    result = []
    
    def backtrack(start, current):
        result.append(current[:])
        
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result
```

**Permutations:**
```python
def permutations(nums):
    result = []
    
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    
    backtrack([], nums)
    return result
```

**Combinations:**
```python
def combinations(n, k):
    result = []
    
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return
        
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(1, [])
    return result
```

### Bit Manipulation

**Common Operations:**
```python
# Check if bit is set
def is_bit_set(n, i):
    return (n & (1 << i)) != 0

# Set bit
def set_bit(n, i):
    return n | (1 << i)

# Clear bit
def clear_bit(n, i):
    return n & ~(1 << i)

# Toggle bit
def toggle_bit(n, i):
    return n ^ (1 << i)

# Count set bits
def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Alternative: Brian Kernighan's algorithm
def count_bits_fast(n):
    count = 0
    while n:
        n &= n - 1  # Clear lowest set bit
        count += 1
    return count
```

**XOR Tricks:**
```python
# XOR properties:
# a ^ a = 0
# a ^ 0 = a
# a ^ b ^ a = b

# Find single number (all others appear twice)
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# Find two unique numbers
def two_unique(nums):
    xor = 0
    for num in nums:
        xor ^= num
    
    # Find rightmost set bit
    diff_bit = xor & (-xor)
    
    a = b = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num
    
    return [a, b]
```

**Power of Two:**
```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

---

## 📝 Practice Problems

### Company Tag Legend
🔵 Google | 🟠 Amazon | 🔴 Meta/Facebook | 🟣 Microsoft | 🟢 Apple | 🟡 Bloomberg | ⚫ Uber | 🔘 LinkedIn | 🔷 Airbnb | 💜 ByteDance/TikTok | 🟤 Stripe | ⭐ Frequently Asked

### Day 1: Trie

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 1 | [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | LC #208 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Basic trie with insert, search, startsWith |
| 2 | [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | LC #211 | Medium | 🔵🟠🔴🟣 ⭐ | DFS for '.' wildcard matching |
| 3 | [Word Search II](https://leetcode.com/problems/word-search-ii/) | LC #212 | Hard | 🔵🟠🔴🟣🟢🔷 ⭐ | Trie + DFS on grid |
| 4 | [Replace Words](https://leetcode.com/problems/replace-words/) | LC #648 | Medium | 🔵⚫ | Find shortest prefix in trie |

### Day 2: Heap / Priority Queue

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 5 | [Kth Largest Element in Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | LC #215 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Min heap of size k |
| 6 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | LC #347 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Count frequencies, heap or bucket sort |
| 7 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | LC #295 | Hard | 🔵🟠🔴🟣🟢🟡 ⭐ | Two heaps: max for lower, min for upper |
| 8 | [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | LC #23 | Hard | 🔵🟠🔴🟣🟢🟡 ⭐ | Min heap of list heads |
| 9 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | LC #621 | Medium | 🔵🟠🔴🟣🟡 ⭐ | Max heap for most frequent, track cooldown |

### Day 3: Intervals

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 10 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | LC #56 | Medium | 🔵🟠🔴🟣🟢🟡⚫🔷 ⭐ | Sort by start, merge if overlap |
| 11 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | LC #57 | Medium | 🔵🟠🔴🟣🔘 ⭐ | Three phases: before, overlapping, after |
| 12 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | LC #435 | Medium | 🔵🟠🔴🟣 ⭐ | Greedy: keep interval with earliest end |
| 13 | [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) | LC #252 | Easy | 🔵🟠🔴🟣🟡 ⭐ | Sort and check overlap |
| 14 | [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | LC #253 | Medium | 🔵🟠🔴🟣🟢🟡⚫🔷 ⭐ | Min heap for end times, or sweep line |

### Day 4: Backtracking Basics

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 15 | [Subsets](https://leetcode.com/problems/subsets/) | LC #78 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Include or exclude each element |
| 16 | [Subsets II](https://leetcode.com/problems/subsets-ii/) | LC #90 | Medium | 🔵🟠🔴🟣 | Sort, skip duplicates at same level |
| 17 | [Permutations](https://leetcode.com/problems/permutations/) | LC #46 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Try each element at each position |
| 18 | [Permutations II](https://leetcode.com/problems/permutations-ii/) | LC #47 | Medium | 🔵🟠🔴🟣🔘 ⭐ | Sort, skip same value at same position |
| 19 | [Combinations](https://leetcode.com/problems/combinations/) | LC #77 | Medium | 🔵🟠🟣 | Pick k from n |

### Day 5: Backtracking Advanced

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 20 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | LC #39 | Medium | 🔵🟠🔴🟣🟢🟡⚫ ⭐ | Same element can be used multiple times |
| 21 | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | LC #40 | Medium | 🔵🟠🔴🟣 | Each element used once, skip duplicates |
| 22 | [Letter Combinations of Phone](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | LC #17 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Map digits to letters, backtrack |
| 23 | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | LC #131 | Medium | 🔵🟠🔴🟣 ⭐ | Try all partition points, check palindrome |
| 24 | [N-Queens](https://leetcode.com/problems/n-queens/) | LC #51 | Hard | 🔵🟠🔴🟣🟢 ⭐ | Place queen row by row, track columns/diagonals |

### Day 6: Bit Manipulation

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 25 | [Single Number](https://leetcode.com/problems/single-number/) | LC #136 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | XOR all numbers |
| 26 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | LC #191 | Easy | 🔵🟠🟣🟢 | n & (n-1) clears lowest set bit |
| 27 | [Counting Bits](https://leetcode.com/problems/counting-bits/) | LC #338 | Easy | 🔵🟠🟣 | dp[i] = dp[i >> 1] + (i & 1) |
| 28 | [Missing Number](https://leetcode.com/problems/missing-number/) | LC #268 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | XOR with indices and values |
| 29 | [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | LC #190 | Easy | 🔵🟠🟣🟢 | Bit by bit reversal |

### Day 7: Mixed Practice

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 30 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | LC #127 | Hard | 🔵🟠🔴🟣🟢🟡⚫🔷 ⭐ | BFS, try all single-char changes |
| 31 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | LC #76 | Hard | 🔵🟠🔴🟣🟢🟡🔘 ⭐ | Sliding window with frequency map |
| 32 | [Kth Smallest Element in Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | LC #378 | Medium | 🔵🟠🔴🟣 ⭐ | Min heap or binary search |

---

## 🧩 Pattern Recognition Cheat Sheet

| Clue in Problem | Pattern to Try |
|-----------------|----------------|
| "Prefix matching" | Trie |
| "Autocomplete" | Trie |
| "K largest/smallest" | Heap (size k) |
| "Median in stream" | Two heaps |
| "Merge sorted lists" | Min heap |
| "Overlapping intervals" | Sort by start/end |
| "All possible combinations" | Backtracking |
| "Generate all permutations" | Backtracking |
| "Single element" | XOR |
| "Power of 2" | n & (n-1) == 0 |

---

## ⏱️ Time Complexity

| Data Structure/Algorithm | Insert | Delete | Search/Query |
|-------------------------|--------|--------|--------------|
| Trie | O(m) | O(m) | O(m) |
| Binary Heap | O(log n) | O(log n) | O(1) min/max |
| Backtracking | - | - | O(b^d) worst case |

m = length of word, n = number of elements, b = branching factor, d = depth

---

## ✅ Week 5 Checklist

- [ ] Implement Trie from scratch
- [ ] Master heap operations in Python
- [ ] Understand interval merge/insert patterns
- [ ] Practice backtracking template
- [ ] Know common bit manipulation tricks
- [ ] Solve all 32 practice problems

