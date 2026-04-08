"""
Problem: Sliding Window Maximum (LeetCode #239)
Difficulty: Hard

Given an array nums and sliding window size k, return the max of each window.

Example:
    Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
    Output: [3,3,5,5,6,7]
    
    Window positions:
    [1  3  -1] -3  5  3  6  7       -> max = 3
     1 [3  -1  -3] 5  3  6  7       -> max = 3
     1  3 [-1  -3  5] 3  6  7       -> max = 5
     1  3  -1 [-3  5  3] 6  7       -> max = 5
     1  3  -1  -3 [5  3  6] 7       -> max = 6
     1  3  -1  -3  5 [3  6  7]      -> max = 7
"""

from typing import List
from collections import deque
import heapq


def max_sliding_window_brute(nums: List[int], k: int) -> List[int]:
    """
    Brute Force Approach
    Time: O(n * k) - for each window, find max
    Space: O(1)
    """
    if not nums or k == 0:
        return []
    
    result = []
    for i in range(len(nums) - k + 1):
        result.append(max(nums[i:i + k]))
    return result


def max_sliding_window_deque(nums: List[int], k: int) -> List[int]:
    """
    Optimal Approach using Monotonic Deque
    Time: O(n) - each element added and removed at most once
    Space: O(k) - deque stores at most k indices
    
    Key Insight:
    - Maintain a decreasing deque of indices
    - Front of deque is always the maximum
    - Remove elements outside the window
    - Remove smaller elements from back (they can never be max)
    """
    if not nums or k == 0:
        return []
    
    # Deque stores indices, maintaining decreasing order of values
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back (they can't be max)
        # If current element is larger, previous smaller elements are useless
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # First window complete at index k-1
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result


def max_sliding_window_heap(nums: List[int], k: int) -> List[int]:
    """
    Heap Approach (Max Heap)
    Time: O(n log n) - heap operations
    Space: O(n) - heap can grow to n elements
    
    Note: Python has min-heap, so we negate values for max-heap
    """
    if not nums or k == 0:
        return []
    
    # Max heap: store (-value, index)
    heap = []
    result = []
    
    for i in range(len(nums)):
        # Add current element
        heapq.heappush(heap, (-nums[i], i))
        
        # Remove elements outside window (lazy deletion)
        while heap[0][1] < i - k + 1:
            heapq.heappop(heap)
        
        # Add max to result after first window
        if i >= k - 1:
            result.append(-heap[0][0])
    
    return result


# Visual demonstration
def visualize_sliding_window(nums: List[int], k: int):
    """Visualize the sliding window process"""
    print(f"\nNums: {nums}, k={k}")
    print("-" * 50)
    
    for i in range(len(nums) - k + 1):
        window = nums[i:i + k]
        
        # Create visualization
        before = nums[:i]
        after = nums[i + k:]
        
        vis = "  ".join(str(x) for x in before)
        if before:
            vis += "  "
        vis += "[" + "  ".join(str(x) for x in window) + "]"
        if after:
            vis += "  " + "  ".join(str(x) for x in after)
        
        print(f"{vis:40} -> max = {max(window)}")


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1], 1, [1]),
        ([1, -1], 1, [1, -1]),
        ([9, 11], 2, [11]),
        ([4, -2], 2, [4]),
    ]
    
    for nums, k, expected in test_cases:
        result = max_sliding_window_deque(nums, k)
        assert result == expected, f"Failed: got {result}, expected {expected}"
        print(f"✓ nums={nums}, k={k} -> {result}")
    
    # Visualize an example
    visualize_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)
    
    print("\nAll tests passed!")

