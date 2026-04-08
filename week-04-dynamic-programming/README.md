# Week 4: Dynamic Programming

> Master the art of breaking problems into overlapping subproblems

---

## 📖 High-Level Overview

Dynamic Programming tests your ability to:
- Identify optimal substructure
- Define state transitions clearly
- Recognize overlapping subproblems
- Optimize space when possible

### Key Patterns This Week:
1. **1D DP** - Climbing stairs, fibonacci-style
2. **2D DP** - Grid paths, string matching
3. **Knapsack** - Subset sum, bounded/unbounded
4. **LCS/LIS** - Longest common/increasing subsequence
5. **Interval DP** - Matrix chain multiplication style

---

## 🔬 Low-Level Details

### DP Problem-Solving Framework

```
1. DEFINE STATE
   - What information do we need to uniquely identify a subproblem?
   - Usually: dp[i], dp[i][j], dp[i][j][k]

2. DEFINE BASE CASES
   - What are the smallest subproblems we can solve directly?
   - Usually: dp[0], dp[0][0], empty string, etc.

3. DEFINE RECURRENCE RELATION
   - How do we build solution from smaller subproblems?
   - dp[i] = f(dp[i-1], dp[i-2], ...)

4. DETERMINE ORDER
   - In what order should we solve subproblems?
   - Usually: left to right, bottom-up

5. EXTRACT ANSWER
   - Where is the final answer stored?
   - Usually: dp[n] or dp[n-1]
```

### Top-Down (Memoization) Template

```python
def solve(n):
    memo = {}
    
    def dp(state):
        # Base case
        if base_condition:
            return base_value
        
        # Check memo
        if state in memo:
            return memo[state]
        
        # Recurrence
        result = compute_from_subproblems()
        
        # Store in memo
        memo[state] = result
        return result
    
    return dp(initial_state)
```

### Bottom-Up (Tabulation) Template

```python
def solve(n):
    # Initialize DP table
    dp = [0] * (n + 1)
    
    # Base cases
    dp[0] = base_value_0
    dp[1] = base_value_1
    
    # Fill table
    for i in range(2, n + 1):
        dp[i] = compute_from(dp[i-1], dp[i-2], ...)
    
    return dp[n]
```

### Pattern 1: Fibonacci-Style (1D DP)

**Example: Climbing Stairs**
```python
def climb_stairs(n):
    if n <= 2:
        return n
    
    # Space optimized - only need last 2 values
    prev2, prev1 = 1, 2
    
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    
    return prev1
```

### Pattern 2: Grid DP (2D)

**Example: Unique Paths**
```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]

# Space optimized
def unique_paths_optimized(m, n):
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    
    return dp[n-1]
```

### Pattern 3: 0/1 Knapsack

```python
def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i-1][w]
            
            # Take item i (if it fits)
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                               dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

# Space optimized (iterate backwards)
def knapsack_01_optimized(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

### Pattern 4: Unbounded Knapsack

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Pattern 5: Longest Common Subsequence (LCS)

```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### Pattern 6: Longest Increasing Subsequence (LIS)

```python
# O(n²) DP solution
def lis_dp(nums):
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# O(n log n) with binary search
def lis_binary_search(nums):
    from bisect import bisect_left
    
    tails = []
    
    for num in nums:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)
```

### Pattern 7: Edit Distance

```python
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # Delete
                    dp[i][j-1],     # Insert
                    dp[i-1][j-1]    # Replace
                )
    
    return dp[m][n]
```

### Pattern 8: Interval DP

```python
def min_cost_to_burst_balloons(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    
    # Length of interval
    for length in range(2, n):
        for left in range(n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + dp[k][right] + 
                    nums[left] * nums[k] * nums[right]
                )
    
    return dp[0][n-1]
```

### Pattern 9: Decision Making (Buy/Sell Stock)

```python
def max_profit_with_cooldown(prices):
    n = len(prices)
    if n < 2:
        return 0
    
    # hold[i] = max profit if holding stock at day i
    # sold[i] = max profit if just sold at day i
    # rest[i] = max profit if resting (not holding) at day i
    
    hold = [0] * n
    sold = [0] * n
    rest = [0] * n
    
    hold[0] = -prices[0]
    
    for i in range(1, n):
        hold[i] = max(hold[i-1], rest[i-1] - prices[i])
        sold[i] = hold[i-1] + prices[i]
        rest[i] = max(rest[i-1], sold[i-1])
    
    return max(sold[n-1], rest[n-1])
```

---

## 📝 Practice Problems

### Company Tag Legend
🔵 Google | 🟠 Amazon | 🔴 Meta/Facebook | 🟣 Microsoft | 🟢 Apple | 🟡 Bloomberg | ⚫ Uber | 🔘 LinkedIn | 🔷 Airbnb | 💜 ByteDance/TikTok | ⭐ Frequently Asked

### Day 1: 1D DP Basics

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 1 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | LC #70 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | dp[i] = dp[i-1] + dp[i-2] |
| 2 | [House Robber](https://leetcode.com/problems/house-robber/) | LC #198 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | dp[i] = max(dp[i-1], dp[i-2] + nums[i]) |
| 3 | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | LC #213 | Medium | 🔵🟠🔴🟣 | Circular: solve for [0:n-1] and [1:n], take max |
| 4 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | LC #91 | Medium | 🔵🟠🔴🟣🟡 ⭐ | Check 1-digit and 2-digit valid decodings |

### Day 2: Grid DP

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 5 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | LC #62 | Medium | 🔵🟠🔴🟣🟡 ⭐ | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| 6 | [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | LC #63 | Medium | 🔵🟠🔴🟣 | Set dp to 0 for obstacles |
| 7 | [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | LC #64 | Medium | 🔵🟠🔴🟣🟡 ⭐ | dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]) |
| 8 | [Triangle](https://leetcode.com/problems/triangle/) | LC #120 | Medium | 🔵🟠🔴🟣 | Bottom-up: dp[j] = triangle[i][j] + min(dp[j], dp[j+1]) |

### Day 3: Knapsack Variants

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 9 | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | LC #416 | Medium | 🔵🟠🔴🟣 ⭐ | 0/1 knapsack: can we make sum/2? |
| 10 | [Target Sum](https://leetcode.com/problems/target-sum/) | LC #494 | Medium | 🔵🟠🔴🟣 ⭐ | Subset sum: P - N = target, P + N = sum |
| 11 | [Coin Change](https://leetcode.com/problems/coin-change/) | LC #322 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Unbounded knapsack |
| 12 | [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | LC #518 | Medium | 🔵🟠🔴🟣 ⭐ | Count ways, not min coins |

### Day 4: String DP

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 13 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | LC #1143 | Medium | 🔵🟠🔴🟣 ⭐ | If match: dp[i-1][j-1] + 1, else max |
| 14 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | LC #72 | Medium | 🔵🟠🔴🟣🟢 ⭐ | 3 operations: insert, delete, replace |
| 15 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | LC #5 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Expand from center, or dp[i][j] = true if palindrome |
| 16 | [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | LC #516 | Medium | 🔵🟠🔘 | LCS of string and its reverse |

### Day 5: LIS Variants

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 17 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | LC #300 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | dp[i] = max(dp[j] + 1) for j < i where nums[j] < nums[i] |
| 18 | [Number of LIS](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) | LC #673 | Medium | 🔵🟠🔴 | Track count along with length |
| 19 | [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | LC #354 | Hard | 🔵🟠🔴🟣 ⭐ | Sort by width, LIS on height |
| 20 | [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | LC #646 | Medium | 🟠 | Sort by end, greedy or DP |

### Day 6: Decision Making DP

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 21 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | LC #121 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | Track min price, max profit |
| 22 | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | LC #122 | Medium | 🔵🟠🔴🟣 ⭐ | Sum all positive differences |
| 23 | [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | LC #309 | Medium | 🔵🟠🔴 ⭐ | States: hold, sold, rest |
| 24 | [Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) | LC #714 | Medium | 🔵🟠🔴 | Subtract fee when selling |

### Day 7: Advanced DP

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 25 | [Word Break](https://leetcode.com/problems/word-break/) | LC #139 | Medium | 🔵🟠🔴🟣🟢🟡⚫ ⭐ | dp[i] = true if s[:i] can be segmented |
| 26 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | LC #97 | Medium | 🔵🟠🔴🟣 | 2D DP: dp[i][j] for s1[:i] and s2[:j] |
| 27 | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | LC #312 | Hard | 🔵🟠🔴🟣 ⭐ | Interval DP: think about last balloon to burst |
| 28 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | LC #10 | Hard | 🔵🟠🔴🟣🟢 ⭐ | Handle . and * cases carefully |

---

## 🧩 Pattern Recognition Cheat Sheet

| Clue in Problem | Pattern to Try |
|-----------------|----------------|
| "Maximum/minimum ways" | DP with counting/optimization |
| "Is it possible to..." | Boolean DP |
| "Partition into subsets" | Subset sum / Knapsack |
| "Longest/shortest subsequence" | LCS/LIS pattern |
| "String transformation" | Edit distance style |
| "Grid paths" | 2D DP |
| "Decision at each step" | State machine DP |
| "Intervals/ranges" | Interval DP |

---

## 💡 DP State Design Tips

1. **Start with brute force** - What choices do you make at each step?
2. **Identify what changes** - Those become your state dimensions
3. **What do you need from the past?** - That determines your recurrence
4. **Can you reduce dimensions?** - Often last 1-2 states are enough

---

## ✅ Week 4 Checklist

- [ ] Understand top-down vs bottom-up approaches
- [ ] Master space optimization techniques
- [ ] Recognize common DP patterns
- [ ] Practice state design for new problems
- [ ] Solve all 28 practice problems
- [ ] Re-solve hard problems without hints

