# LeetCode Tips & Common Patterns 💡

## Before You Start Solving

### The UMPIRE Method
1. **U**nderstand - Read carefully, ask clarifying questions
2. **M**atch - Match to known patterns
3. **P**lan - Write pseudocode, think through edge cases
4. **I**mplement - Code cleanly
5. **R**eview - Trace through with examples
6. **E**valuate - Analyze time/space complexity

---

## Pattern Recognition Quick Guide

### When to Use What

| If You See... | Think... |
|---------------|----------|
| Sorted array | Binary Search |
| Find pair/triplet | Two Pointers |
| Contiguous subarray | Sliding Window |
| Finding k-th element | Heap / QuickSelect |
| Need O(1) lookup | HashMap/HashSet |
| Tree traversal | DFS (recursion/stack) |
| Shortest path (unweighted) | BFS |
| Shortest path (weighted) | Dijkstra |
| All possible combinations | Backtracking |
| Optimal value (subproblems) | Dynamic Programming |
| Connectivity | Union-Find |
| String prefix matching | Trie |
| Range queries | Prefix Sum / Segment Tree |

---

## Pattern Templates

### 1. Two Pointers (Opposite Ends)
```
left, right = 0, n-1
while left < right:
    if condition: left++
    else: right--
```
**Problems:** Two Sum II, 3Sum, Container With Most Water

### 2. Sliding Window (Variable)
```
left = 0
for right in range(n):
    add nums[right] to window
    while window invalid:
        remove nums[left], left++
    update answer
```
**Problems:** Longest Substring, Minimum Window Substring

### 3. Binary Search (Find Boundary)
```
left, right = min, max
while left < right:
    mid = left + (right - left) / 2
    if condition(mid): right = mid
    else: left = mid + 1
return left
```
**Problems:** Search in Rotated Array, Koko Eating Bananas

### 4. BFS (Level by Level)
```
queue = [start]
while queue:
    level_size = len(queue)
    for i in range(level_size):
        node = queue.pop(0)
        process(node)
        add neighbors to queue
```
**Problems:** Level Order Traversal, Shortest Path

### 5. DFS (Backtracking)
```
def backtrack(path, choices):
    if is_solution(path):
        add to result
        return
    for choice in choices:
        if valid(choice):
            path.add(choice)
            backtrack(path, remaining_choices)
            path.remove(choice)
```
**Problems:** Permutations, Subsets, N-Queens

### 6. Dynamic Programming
```
# 1. Define state: dp[i] = optimal answer for subproblem i
# 2. Base case: dp[0] = ...
# 3. Recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)
# 4. Return: dp[n] or max(dp)
```
**Problems:** Climbing Stairs, Coin Change, LCS

---

## Time Complexity Cheat Sheet

| n | Max Viable Complexity |
|---|----------------------|
| ≤ 10 | O(n!) |
| ≤ 20 | O(2^n) |
| ≤ 500 | O(n³) |
| ≤ 5000 | O(n²) |
| ≤ 10^6 | O(n log n) |
| ≤ 10^8 | O(n) |
| > 10^8 | O(log n) or O(1) |

---

## Common Edge Cases

### Arrays
- Empty array
- Single element
- Two elements
- All same elements
- Sorted / reverse sorted
- Contains duplicates
- Negative numbers

### Strings
- Empty string
- Single character
- All same characters
- Unicode characters

### Trees
- Null root
- Single node
- Skewed (like a linked list)
- Complete vs incomplete

### Graphs
- Disconnected components
- Self loops
- Cycles
- Single node

### Numbers
- Zero
- Negative
- INT_MAX / INT_MIN
- Overflow

---

## Debugging Checklist

1. ☐ Off-by-one errors in loops
2. ☐ Array index out of bounds
3. ☐ Integer overflow
4. ☐ Null/nil pointer access
5. ☐ Unhandled edge cases
6. ☐ Wrong comparison operator (< vs <=)
7. ☐ Forgetting to update loop variable
8. ☐ Returning wrong variable
9. ☐ Not resetting state between test cases

---

## Interview Tips

### During the Interview
1. **Clarify** - Ask about input size, constraints, edge cases
2. **Think aloud** - Explain your thought process
3. **Start simple** - Brute force first, then optimize
4. **Test** - Walk through with examples before running

### When Stuck
1. Try a simpler version of the problem
2. Think about related problems you've solved
3. Consider all data structures
4. Draw it out!
5. Ask for a hint (it's okay!)

### After Solving
1. Analyze complexity (time & space)
2. Discuss trade-offs
3. Mention potential optimizations
4. Think about follow-ups

---

## Go-Specific Tips

```go
// Avoid common Go gotchas:

// 1. Slice append modifies underlying array
original := []int{1, 2, 3}
modified := append(original[:2], 4)  // original is now [1, 2, 4]!
// Fix: make a copy first

// 2. Range loop variable reuse
for _, v := range items {
    go func() { process(v) }()  // Bug: all goroutines see last v
}
// Fix: for _, v := range items { v := v; go func() { process(v) }() }

// 3. Map iteration order is random
// Don't rely on map order

// 4. Nil slice vs empty slice
var s1 []int          // nil
s2 := []int{}         // empty but not nil
// Both work with append, but json.Marshal differs
```

---

## C++ Specific Tips

```cpp
// Common C++ gotchas:

// 1. Integer overflow
int result = INT_MAX + 1;  // Undefined behavior!
// Fix: Use long long or check before adding

// 2. Vector iterator invalidation
for (auto it = v.begin(); it != v.end(); ++it) {
    if (*it == target) v.erase(it);  // Bug: iterator invalidated
}
// Fix: it = v.erase(it) or use remove_if

// 3. Unordered map default value
unordered_map<int, int> m;
cout << m[5];  // Creates entry with value 0!
// Fix: Use count() or find() to check existence

// 4. Comparing signed and unsigned
vector<int> v;
for (int i = 0; i < v.size() - 1; i++)  // Bug if v.size() == 0
// Fix: Use size_t or check size first
```

---

## Quick Reference Cards

### Must-Know STL (C++)
```cpp
// Containers
vector, deque, list
set, map, unordered_set, unordered_map
stack, queue, priority_queue

// Algorithms
sort, stable_sort, partial_sort
binary_search, lower_bound, upper_bound
find, count, accumulate
min_element, max_element
reverse, rotate, unique
next_permutation
```

### Must-Know Go Packages
```go
import (
    "sort"           // Sort, Search, Slice
    "strings"        // Split, Join, Contains
    "strconv"        // Atoi, Itoa
    "container/heap" // Priority queue
    "container/list" // Doubly linked list
    "math"           // Max, Min, Abs
    "math/bits"      // OnesCount, LeadingZeros
)
```

---

Good luck! 🚀 Remember: consistency > intensity

