# 📁 Solutions Directory

This directory contains reference solutions for practice problems from each week.

## Structure

```
solutions/
├── week-01/           # Arrays & Strings
│   ├── two_sum.py
│   └── sliding_window_maximum.py
├── week-02/           # Linked Lists, Stacks & Queues
│   └── lru_cache.py
├── week-03/           # Trees & Graphs
│   └── course_schedule.py
├── week-04/           # Dynamic Programming
│   └── coin_change.py
├── week-05/           # Advanced Algorithms
│   └── trie.py
├── week-06/           # System Design (diagrams/notes)
├── week-07/           # Databases & Caching
├── week-08/           # Distributed Systems
├── week-09/           # Kubernetes
├── week-10/           # Kafka
├── week-11/           # Cloud Services
└── week-12/           # Mock Interviews
```

## How to Use These Solutions

### ❌ Don't

- Look at solutions before attempting problems
- Copy solutions without understanding
- Memorize solutions verbatim

### ✅ Do

1. **Attempt the problem first** - Spend at least 30-45 minutes
2. **Write your own solution** - Even if incomplete
3. **Compare approaches** - Learn from differences
4. **Understand the patterns** - Focus on transferable techniques
5. **Re-solve without looking** - After reviewing, close the solution and re-implement

## Solution Template

Each solution file follows this structure:

```python
"""
Problem: [Name] (LeetCode #XXX)
Difficulty: Easy/Medium/Hard

[Problem description]

Example:
    Input: ...
    Output: ...
"""

def solution_brute_force(args):
    """
    Brute Force Approach
    Time: O(...)
    Space: O(...)
    """
    pass

def solution_optimal(args):
    """
    Optimal Approach
    Time: O(...)
    Space: O(...)
    
    Key Insight:
    - ...
    """
    pass

# Test cases
if __name__ == "__main__":
    # Tests with assertions
    pass
```

## Running Solutions

```bash
# Navigate to solutions directory
cd solutions/week-01

# Run a specific solution
python two_sum.py

# Run with verbose output (if available)
python -v sliding_window_maximum.py
```

## Adding Your Own Solutions

Feel free to add your own solutions! Follow the template above and include:

1. **Problem statement** in docstring
2. **Multiple approaches** (brute force → optimal)
3. **Time/Space complexity** analysis
4. **Test cases** with assertions
5. **Comments** explaining key insights

## Problem Difficulty Guide

| Difficulty | Time to Solve | Approaches |
|------------|---------------|------------|
| Easy | 15-20 min | 1-2 approaches |
| Medium | 25-35 min | 2-3 approaches |
| Hard | 40-60 min | 2-4 approaches |

---

*Remember: The goal is understanding, not memorization!*

