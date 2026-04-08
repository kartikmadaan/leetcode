# Week 1: Arrays & Strings

> Foundation week - Master the building blocks of coding interviews

---

## 📖 High-Level Overview

Arrays and strings are the most common data structures in coding interviews. They test your ability to:
- Manipulate data in-place
- Use multiple pointers efficiently
- Apply sliding window techniques
- Understand time-space tradeoffs

### Key Patterns This Week:
1. **Two Pointers** - Converging from both ends or moving together
2. **Sliding Window** - Fixed or variable size windows
3. **Hash Maps** - O(1) lookups for frequency counting
4. **Prefix Sum** - Precompute cumulative sums

---

## 🔬 Low-Level Details

### Two Pointers Technique

**When to use:**
- Sorted arrays where you need to find pairs
- Reversing/swapping elements
- Removing duplicates in-place

**Template:**
```python
def two_pointers_converging(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # Process based on condition
        if condition_met(arr[left], arr[right]):
            left += 1
        else:
            right -= 1
    return result

def two_pointers_same_direction(arr):
    slow = fast = 0
    while fast < len(arr):
        if condition(arr[fast]):
            arr[slow] = arr[fast]
            slow += 1
        fast += 1
    return slow  # new length
```

### Sliding Window Technique

**When to use:**
- Finding subarray/substring with specific property
- Maximum/minimum of all subarrays of size k
- Longest substring with certain constraint

**Fixed Window Template:**
```python
def fixed_sliding_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

**Variable Window Template:**
```python
def variable_sliding_window(s):
    left = 0
    window = {}  # or set, counter, etc.
    result = 0
    
    for right in range(len(s)):
        # Expand window - add s[right]
        window[s[right]] = window.get(s[right], 0) + 1
        
        # Shrink window while invalid
        while window_is_invalid():
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        # Update result
        result = max(result, right - left + 1)
    
    return result
```

### HashMap for Frequency Counting

**Template:**
```python
from collections import Counter, defaultdict

def frequency_count(arr):
    freq = Counter(arr)  # or defaultdict(int)
    # Process frequencies
    for key, count in freq.items():
        pass
```

### Prefix Sum

**When to use:**
- Range sum queries
- Finding subarray with specific sum
- Product of array except self

**Template:**
```python
def prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Sum of arr[i:j] = prefix[j] - prefix[i]
    return prefix
```

---

## 📝 Practice Problems

### Company Tag Legend
🔵 Google | 🟠 Amazon | 🔴 Meta/Facebook | 🟣 Microsoft | 🟢 Apple | 🟡 Bloomberg | ⚫ Uber | 🔘 LinkedIn | ⭐ Frequently Asked

### Day 1-2: Two Pointers (Easy)

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | LC #1 | Easy | 🔵🟠🔴🟣🟢 ⭐ | Use a hashmap to store complement |
| 2 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | LC #125 | Easy | 🔴🟣🟢 | Two pointers from ends, skip non-alphanumeric |
| 3 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | LC #88 | Easy | 🔴🟣🟠 | Start from the end to avoid overwriting |
| 4 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | LC #26 | Easy | 🔴🟣🟡 | Slow/fast pointer - slow tracks unique position |

### Day 3-4: Two Pointers (Medium)

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 5 | [3Sum](https://leetcode.com/problems/3sum/) | LC #15 | Medium | 🔵🟠🔴🟣 ⭐ | Fix one element, use two pointers for remaining two |
| 6 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | LC #11 | Medium | 🔵🟠🔴🟣 ⭐ | Move pointer with smaller height inward |
| 7 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | LC #42 | Hard | 🔵🟠🔴🟣🟢 ⭐ | Track max from left and right, water = min(max) - height |

### Day 5: Sliding Window (Easy → Medium)

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 8 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | LC #121 | Easy | 🔵🟠🔴🟣 ⭐ | Track minimum price seen so far |
| 9 | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | LC #643 | Easy | 🔴🟣 | Fixed window of size k |
| 10 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | LC #3 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Variable window with set/hashmap |

### Day 6: Sliding Window (Medium → Hard)

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 11 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | LC #76 | Hard | 🔵🟠🔴🟣🟢 ⭐ | Expand to include all chars, shrink to minimize |
| 12 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | LC #239 | Hard | 🔵🟠🟣 ⭐ | Use deque to maintain decreasing order |
| 13 | [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | LC #438 | Medium | 🔵🟠🔴🟣 | Fixed window with frequency matching |

### Day 7: Mixed Practice

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 14 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | LC #238 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Prefix and suffix products |
| 15 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | LC #560 | Medium | 🔵🟠🔴🟣 ⭐ | Prefix sum with hashmap storing count |
| 16 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | LC #49 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Use sorted string or char count as key |

---

## 🧩 Pattern Recognition Cheat Sheet

| Clue in Problem | Pattern to Try |
|-----------------|----------------|
| "Sorted array" | Two Pointers |
| "In-place modification" | Two Pointers (same direction) |
| "Subarray/substring of size k" | Fixed Sliding Window |
| "Longest/shortest subarray with property" | Variable Sliding Window |
| "Contiguous subarray sum" | Prefix Sum + HashMap |
| "Find pairs/triplets" | Two Pointers (after sorting) or HashMap |
| "Anagrams/permutations" | HashMap frequency count |

---

## ⏱️ Time Complexity Reference

| Operation | Array | String |
|-----------|-------|--------|
| Access by index | O(1) | O(1) |
| Search | O(n) | O(n) |
| Insert/Delete at end | O(1)* | O(n) - strings are immutable |
| Insert/Delete at beginning | O(n) | O(n) |
| Slice | O(k) | O(k) |

*Amortized for dynamic arrays

---

## 📌 Common Mistakes to Avoid

1. **Off-by-one errors** - Be careful with loop bounds and indices
2. **Not handling empty arrays** - Always check edge cases
3. **Mutating while iterating** - Use a copy or iterate backwards
4. **Integer overflow** - Use `left + (right - left) // 2` instead of `(left + right) // 2`
5. **Forgetting strings are immutable** - Convert to list for modifications

---

## ✅ Week 1 Checklist

- [ ] Understand and implement Two Pointers pattern
- [ ] Master Fixed and Variable Sliding Window
- [ ] Practice HashMap for frequency problems
- [ ] Solve all 16 practice problems
- [ ] Review and understand optimal solutions
- [ ] Time yourself on at least 5 problems (45 min each)

