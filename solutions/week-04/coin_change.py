"""
Problem: Coin Change (LeetCode #322)
Difficulty: Medium

You are given an integer array coins representing coins of different 
denominations and an integer amount representing a total amount of money.

Return the fewest number of coins needed to make up that amount.
If that amount cannot be made up, return -1.

Example:
    Input: coins = [1,2,5], amount = 11
    Output: 3
    Explanation: 11 = 5 + 5 + 1

This is the UNBOUNDED KNAPSACK pattern - each coin can be used unlimited times.
"""

from typing import List
from functools import lru_cache


def coin_change_dp(coins: List[int], amount: int) -> int:
    """
    Bottom-Up Dynamic Programming
    Time: O(amount * len(coins))
    Space: O(amount)
    
    State: dp[i] = minimum coins needed to make amount i
    Recurrence: dp[i] = min(dp[i - coin] + 1) for each valid coin
    """
    # dp[i] = min coins to make amount i
    # Initialize with infinity (impossible)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed for amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_memo(coins: List[int], amount: int) -> int:
    """
    Top-Down Dynamic Programming with Memoization
    Time: O(amount * len(coins))
    Space: O(amount) for memoization + recursion stack
    """
    @lru_cache(maxsize=None)
    def dp(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')
        
        min_coins = float('inf')
        for coin in coins:
            result = dp(remaining - coin)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)
        
        return min_coins
    
    result = dp(amount)
    return result if result != float('inf') else -1


def coin_change_bfs(coins: List[int], amount: int) -> int:
    """
    BFS Approach - Finding shortest path
    Time: O(amount * len(coins))
    Space: O(amount)
    
    Think of it as a graph where:
    - Each node is an amount
    - Edges connect amounts that differ by a coin value
    - Find shortest path from 0 to target amount
    """
    if amount == 0:
        return 0
    
    from collections import deque
    
    queue = deque([(0, 0)])  # (current_amount, num_coins)
    visited = {0}
    
    while queue:
        current, num_coins = queue.popleft()
        
        for coin in coins:
            next_amount = current + coin
            
            if next_amount == amount:
                return num_coins + 1
            
            if next_amount < amount and next_amount not in visited:
                visited.add(next_amount)
                queue.append((next_amount, num_coins + 1))
    
    return -1


def coin_change_count_ways(coins: List[int], amount: int) -> int:
    """
    Coin Change II (LeetCode #518)
    Count the number of combinations to make up the amount.
    
    Different from counting min coins!
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make 0: use no coins
    
    # Important: iterate coins first to avoid counting permutations
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]


# Visualization helper
def visualize_dp(coins: List[int], amount: int):
    """Show the DP table being filled"""
    print(f"\nCoins: {coins}, Amount: {amount}")
    print("-" * 50)
    
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
    
    # Print DP table
    print("DP Table (min coins for each amount):")
    row = ""
    for i in range(min(amount + 1, 20)):
        val = dp[i] if dp[i] != float('inf') else "∞"
        row += f"{val:3} "
    print(f"  Amount: {' '.join(f'{i:3}' for i in range(min(amount + 1, 20)))}")
    print(f"  Coins:  {row}")
    
    # Reconstruct solution
    if dp[amount] != float('inf'):
        coins_used = []
        current = amount
        while current > 0:
            coins_used.append(parent[current])
            current -= parent[current]
        print(f"\nSolution: {' + '.join(map(str, coins_used))} = {amount}")
        print(f"Number of coins: {len(coins_used)}")
    else:
        print(f"\nNo solution possible")


# Test cases
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 2, 5], 100, 20),
        ([186, 419, 83, 408], 6249, 20),
    ]
    
    print("Testing Coin Change:")
    for coins, amount, expected in test_cases:
        result_dp = coin_change_dp(coins, amount)
        result_memo = coin_change_memo(coins, amount)
        
        status = "✓" if result_dp == expected else "✗"
        print(f"  {status} coins={coins}, amount={amount}")
        print(f"      DP: {result_dp}, Memo: {result_memo}, Expected: {expected}")
    
    # Visualize
    visualize_dp([1, 2, 5], 11)
    
    # Test counting ways
    print("\n" + "=" * 50)
    print("Coin Change II (Count Ways):")
    print(f"  Ways to make 5 with coins [1,2,5]: {coin_change_count_ways([1,2,5], 5)}")

