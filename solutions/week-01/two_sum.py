"""
Problem: Two Sum (LeetCode #1)
Difficulty: Easy

Given an array of integers nums and an integer target, return indices 
of the two numbers such that they add up to target.

Example:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: nums[0] + nums[1] = 2 + 7 = 9
"""

from typing import List


def two_sum_brute_force(nums: List[int], target: int) -> List[int]:
    """
    Brute Force Approach
    Time: O(n²) - nested loops
    Space: O(1) - no extra space
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def two_sum_hashmap(nums: List[int], target: int) -> List[int]:
    """
    Optimal Approach using HashMap
    Time: O(n) - single pass
    Space: O(n) - hashmap storage
    
    Key Insight:
    - For each number, we need its complement (target - num)
    - Store seen numbers in hashmap for O(1) lookup
    """
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []


def two_sum_two_pointers(nums: List[int], target: int) -> List[int]:
    """
    Two Pointers Approach (only works if we can modify/sort)
    Time: O(n log n) - due to sorting
    Space: O(n) - to store original indices
    
    Note: This returns the original indices, not sorted indices
    """
    # Store original indices
    indexed_nums = [(num, i) for i, num in enumerate(nums)]
    indexed_nums.sort(key=lambda x: x[0])
    
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = indexed_nums[left][0] + indexed_nums[right][0]
        
        if current_sum == target:
            return [indexed_nums[left][1], indexed_nums[right][1]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ]
    
    for nums, target, expected in test_cases:
        result = two_sum_hashmap(nums, target)
        assert sorted(result) == sorted(expected), f"Failed for {nums}, {target}"
        print(f"✓ nums={nums}, target={target} -> {result}")
    
    print("\nAll tests passed!")

