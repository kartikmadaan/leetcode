# Week 2: Linked Lists, Stacks & Queues

> Master linear data structures and their pointer manipulation patterns

---

## 📖 High-Level Overview

These data structures test your ability to:
- Manipulate pointers without losing references
- Use auxiliary data structures for tracking state
- Recognize LIFO/FIFO patterns in problems
- Handle edge cases (empty, single element)

### Key Patterns This Week:
1. **Fast & Slow Pointers** - Cycle detection, finding middle
2. **Dummy Node** - Simplify head manipulation
3. **Monotonic Stack** - Next greater/smaller element
4. **Stack for Parsing** - Parentheses, expressions
5. **Queue for BFS** - Level-order processing

---

## 🔬 Low-Level Details

### Linked List Fundamentals

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Traversal
def traverse(head):
    current = head
    while current:
        print(current.val)
        current = current.next

# Get length
def get_length(head):
    length = 0
    while head:
        length += 1
        head = head.next
    return length
```

### Dummy Node Pattern

**When to use:**
- Head of list might change
- Need to handle empty list uniformly
- Inserting/deleting at beginning

```python
def delete_elements(head, val):
    dummy = ListNode(0)
    dummy.next = head
    current = dummy
    
    while current.next:
        if current.next.val == val:
            current.next = current.next.next
        else:
            current = current.next
    
    return dummy.next
```

### Fast & Slow Pointers (Floyd's Algorithm)

**Cycle Detection:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def find_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Reset slow to head, move both at same speed
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow  # Cycle start
```

**Finding Middle:**
```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # Middle (or second middle if even length)
```

### Reversing a Linked List

```python
def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next  # Save next
        current.next = prev       # Reverse pointer
        prev = current            # Move prev forward
        current = next_node       # Move current forward
    
    return prev

# Recursive version
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head
```

### Stack Fundamentals

```python
# Python list as stack
stack = []
stack.append(1)      # Push: O(1)
top = stack[-1]      # Peek: O(1)
popped = stack.pop() # Pop: O(1)
is_empty = len(stack) == 0

# Using collections.deque (more efficient)
from collections import deque
stack = deque()
stack.append(1)
stack.pop()
```

### Monotonic Stack

**Next Greater Element:**
```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # Stores indices
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result
```

**Next Smaller Element:**
```python
def next_smaller_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[i] < nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result
```

### Queue Fundamentals

```python
from collections import deque

queue = deque()
queue.append(1)       # Enqueue (right): O(1)
front = queue[0]      # Peek front: O(1)
popped = queue.popleft()  # Dequeue (left): O(1)
```

---

## 📝 Practice Problems

### Company Tag Legend
🔵 Google | 🟠 Amazon | 🔴 Meta/Facebook | 🟣 Microsoft | 🟢 Apple | 🟡 Bloomberg | ⚫ Uber | 🔘 LinkedIn | ⭐ Frequently Asked

### Day 1: Linked List Basics

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 1 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | LC #206 | Easy | 🔵🟠🔴🟣🟢 ⭐ | Track prev, curr, next pointers |
| 2 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | LC #21 | Easy | 🔵🟠🔴🟣🟢 ⭐ | Use dummy node, compare and advance |
| 3 | [Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | LC #19 | Medium | 🔵🟠🔴🟣 ⭐ | Two pointers, n nodes apart |
| 4 | [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | LC #876 | Easy | 🔵🟠🔴🟣 | Fast & slow pointers |

### Day 2: Linked List Advanced

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 5 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | LC #141 | Easy | 🔵🟠🔴🟣🟢 ⭐ | Floyd's fast & slow |
| 6 | [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | LC #142 | Medium | 🔵🟠🔴🟣 | After meeting, reset slow to head |
| 7 | [Reorder List](https://leetcode.com/problems/reorder-list/) | LC #143 | Medium | 🔴🟠🔘 ⭐ | Find middle, reverse second half, merge |
| 8 | [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | LC #234 | Easy | 🔴🟠🟣 | Find middle, reverse second half, compare |

### Day 3: Linked List Medium/Hard

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 9 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | LC #2 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Handle carry, watch for different lengths |
| 10 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | LC #138 | Medium | 🔵🟠🔴🟣 ⭐ | Use hashmap old→new or interleave nodes |
| 11 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | LC #23 | Hard | 🔵🟠🔴🟣🟢 ⭐ | Divide and conquer, or use min-heap |
| 12 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | LC #25 | Hard | 🔵🟠🔴🟣 ⭐ | Count k nodes, reverse, connect |

### Day 4: Stack Basics

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 13 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | LC #20 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | Push open, pop and match for close |
| 14 | [Min Stack](https://leetcode.com/problems/min-stack/) | LC #155 | Medium | 🔵🟠🔴🟣🟡 ⭐ | Track min with each element pushed |
| 15 | [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | LC #232 | Easy | 🔵🟠🟣🟢 | Two stacks: input and output |
| 16 | [Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) | LC #225 | Easy | 🟣🟠 | One queue, rotate on push |

### Day 5: Monotonic Stack

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 17 | [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | LC #496 | Easy | 🔵🟠🟡 | Precompute NGE for nums2, use hashmap |
| 18 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | LC #739 | Medium | 🔵🟠🔴🟣 ⭐ | Monotonic decreasing stack of indices |
| 19 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | LC #84 | Hard | 🔵🟠🔴🟣 ⭐ | Stack of increasing heights, calculate on pop |
| 20 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | LC #42 | Hard | 🔵🟠🔴🟣🟢 ⭐ | Stack approach: store bars that can trap water |

### Day 6: Expression Evaluation

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 21 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | LC #150 | Medium | 🔵🟠🔘 | Pop two operands for each operator |
| 22 | [Basic Calculator](https://leetcode.com/problems/basic-calculator/) | LC #224 | Hard | 🔵🟠🔴🟣 ⭐ | Stack to handle parentheses, track sign |
| 23 | [Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/) | LC #227 | Medium | 🔵🟠🔴🟣 ⭐ | Stack for + and -, immediate calc for * and / |
| 24 | [Decode String](https://leetcode.com/problems/decode-string/) | LC #394 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Stack of (string, count) pairs for nesting |

### Day 7: Mixed Queue Problems

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 25 | [Moving Average from Data Stream](https://leetcode.com/problems/moving-average-from-data-stream/) | LC #346 | Easy | 🔵🔴🟣 | Queue with fixed size |
| 26 | [Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls/) | LC #933 | Easy | 🔵 | Queue, remove old calls outside window |
| 27 | [Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) | LC #622 | Medium | 🔵🟠🔴 | Array with head/tail pointers, modulo |
| 28 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | LC #239 | Hard | 🔵🟠🔴🟣 ⭐ | Monotonic decreasing deque |

---

## 🧩 Pattern Recognition Cheat Sheet

| Clue in Problem | Pattern to Try |
|-----------------|----------------|
| "Cycle in linked list" | Fast & Slow Pointers |
| "Middle of list" | Fast & Slow Pointers |
| "Reverse linked list" | Three pointer technique |
| "kth from end" | Two pointers, k apart |
| "Merge lists" | Dummy node + compare |
| "Matching brackets" | Stack |
| "Next greater/smaller" | Monotonic Stack |
| "Expression evaluation" | Stack for operands and operators |
| "Level-order" | Queue (BFS) |
| "Sliding window max/min" | Monotonic Deque |

---

## ⏱️ Time & Space Complexity

| Operation | Singly Linked List | Doubly Linked List | Stack | Queue |
|-----------|-------------------|-------------------|-------|-------|
| Access by index | O(n) | O(n) | O(n) | O(n) |
| Insert at head | O(1) | O(1) | N/A | N/A |
| Insert at tail | O(n)* | O(1) | O(1) | O(1) |
| Delete at head | O(1) | O(1) | N/A | O(1) |
| Search | O(n) | O(n) | O(n) | O(n) |

*O(1) if tail pointer is maintained

---

## 📌 Common Mistakes to Avoid

1. **Losing pointer references** - Always save `.next` before modifying
2. **Not handling null/empty** - Check `if head` before accessing
3. **Off-by-one in k operations** - Count carefully
4. **Stack underflow** - Check if stack is empty before pop
5. **Circular list infinite loop** - Use visited set or modify nodes

---

## ✅ Week 2 Checklist

- [ ] Master linked list reversal (iterative + recursive)
- [ ] Understand fast & slow pointer applications
- [ ] Implement monotonic stack pattern
- [ ] Practice parentheses/expression problems
- [ ] Solve all 28 practice problems
- [ ] Time yourself on at least 5 problems

