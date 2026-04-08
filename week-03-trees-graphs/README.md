# Week 3: Trees & Graphs

> Master hierarchical and networked data structures

---

## 📖 High-Level Overview

Trees and graphs test your ability to:
- Navigate recursive structures
- Choose between DFS and BFS appropriately
- Handle edge cases (empty, single node, disconnected)
- Apply dynamic programming on trees

### Key Patterns This Week:
1. **Tree Traversals** - Preorder, Inorder, Postorder, Level-order
2. **DFS on Trees** - Recursive and iterative
3. **BFS on Trees/Graphs** - Level-order, shortest path
4. **Graph DFS/BFS** - Connected components, cycles
5. **Topological Sort** - Dependency ordering

---

## 🔬 Low-Level Details

### Binary Tree Node

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Tree Traversals

```python
# Preorder: Root → Left → Right
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Inorder: Left → Root → Right (sorted order for BST)
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Postorder: Left → Right → Root
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# Level-order (BFS)
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    
    return result
```

### Iterative Traversals (Using Stack)

```python
def preorder_iterative(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        # Push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result

def inorder_iterative(root):
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Go to leftmost
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        result.append(current.val)
        current = current.right
    
    return result
```

### Tree DFS Patterns

**Path Sum Pattern:**
```python
def has_path_sum(root, target_sum):
    if not root:
        return False
    
    # Leaf node check
    if not root.left and not root.right:
        return target_sum == root.val
    
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or 
            has_path_sum(root.right, remaining))
```

**Tree Height/Diameter Pattern:**
```python
def diameter_of_tree(root):
    diameter = 0
    
    def height(node):
        nonlocal diameter
        if not node:
            return 0
        
        left_h = height(node.left)
        right_h = height(node.right)
        
        # Update diameter
        diameter = max(diameter, left_h + right_h)
        
        return 1 + max(left_h, right_h)
    
    height(root)
    return diameter
```

### Binary Search Tree Operations

```python
def search_bst(root, val):
    if not root or root.val == val:
        return root
    
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)

def insert_bst(root, val):
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    
    return root

def delete_bst(root, key):
    if not root:
        return None
    
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:
        # Node to delete found
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        # Find inorder successor (smallest in right subtree)
        successor = root.right
        while successor.left:
            successor = successor.left
        
        root.val = successor.val
        root.right = delete_bst(root.right, successor.val)
    
    return root
```

### Graph Representation

```python
# Adjacency List (most common)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# From edge list
def build_graph(edges, directed=False):
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph
```

### Graph DFS

```python
def dfs(graph, start):
    visited = set()
    result = []
    
    def explore(node):
        if node in visited:
            return
        
        visited.add(node)
        result.append(node)
        
        for neighbor in graph.get(node, []):
            explore(neighbor)
    
    explore(start)
    return result

# Iterative DFS
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        
        visited.add(node)
        result.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return result
```

### Graph BFS (Shortest Path)

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

def shortest_path(graph, start, end):
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []  # No path found
```

### Cycle Detection

```python
# Undirected graph - DFS
def has_cycle_undirected(graph):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # Back edge = cycle
        
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    return False

# Directed graph - DFS with colors
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                return True  # Back edge = cycle
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False
```

### Topological Sort

```python
from collections import deque

# Kahn's Algorithm (BFS-based)
def topological_sort(graph, num_nodes):
    # Calculate in-degrees
    in_degree = {i: 0 for i in range(num_nodes)}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # Start with nodes having 0 in-degree
    queue = deque([n for n in in_degree if in_degree[n] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes are processed (no cycle)
    if len(result) != num_nodes:
        return []  # Cycle detected
    
    return result

# DFS-based Topological Sort
def topological_sort_dfs(graph, num_nodes):
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)
    
    for node in range(num_nodes):
        if node not in visited:
            dfs(node)
    
    return stack[::-1]
```

---

## 📝 Practice Problems

### Company Tag Legend
🔵 Google | 🟠 Amazon | 🔴 Meta/Facebook | 🟣 Microsoft | 🟢 Apple | 🟡 Bloomberg | ⚫ Uber | 🔘 LinkedIn | 🔷 Airbnb | ⭐ Frequently Asked

### Day 1: Tree Traversals

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 1 | [Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) | LC #94 | Easy | 🔵🟠🔴🟣 | Recursive or iterative with stack |
| 2 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | LC #102 | Medium | 🔵🟠🔴🟣🟢 ⭐ | BFS with queue, track level size |
| 3 | [Binary Tree Zigzag Level Order](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | LC #103 | Medium | 🔵🟠🔴🟣🟡 ⭐ | Alternate direction each level |
| 4 | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | LC #199 | Medium | 🔵🟠🔴🟣 ⭐ | BFS, take last element of each level |

### Day 2: Tree DFS

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 5 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | LC #104 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | 1 + max(left, right) |
| 6 | [Same Tree](https://leetcode.com/problems/same-tree/) | LC #100 | Easy | 🔵🟠🟣🟡 | Compare values and recurse |
| 7 | [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | LC #101 | Easy | 🔵🟠🔴🟣🟢🟡 ⭐ | Compare left subtree with mirror of right |
| 8 | [Path Sum](https://leetcode.com/problems/path-sum/) | LC #112 | Easy | 🔵🟠🔴🟣 | Subtract value, check at leaf |
| 9 | [Path Sum II](https://leetcode.com/problems/path-sum-ii/) | LC #113 | Medium | 🔵🟠🔴🟣 | Backtracking to collect all paths |

### Day 3: Tree Construction & Manipulation

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 10 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | LC #226 | Easy | 🔵🟠🔴🟣🟢 ⭐ | Swap left and right recursively |
| 11 | [Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | LC #105 | Medium | 🔵🟠🔴🟣 ⭐ | First of preorder is root, find in inorder |
| 12 | [Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) | LC #114 | Medium | 🔵🟠🔴🟣 ⭐ | Morris traversal or recursion |
| 13 | [Lowest Common Ancestor of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | LC #235 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Use BST property to go left/right |
| 14 | [Lowest Common Ancestor of Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | LC #236 | Medium | 🔵🟠🔴🟣🟢🔘 ⭐ | Return node if found, check both subtrees |

### Day 4: BST Operations

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 15 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | LC #98 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Pass min/max bounds, or inorder check |
| 16 | [Kth Smallest Element in BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | LC #230 | Medium | 🔵🟠🔴🟣 ⭐ | Inorder traversal, count to k |
| 17 | [Convert Sorted Array to BST](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | LC #108 | Easy | 🔵🟠🔴🟣🟢 | Middle element as root, recurse |
| 18 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | LC #297 | Hard | 🔵🟠🔴🟣🟢🔘 ⭐ | Preorder with null markers |

### Day 5: Graph Basics

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 19 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | LC #200 | Medium | 🔵🟠🔴🟣🟢🟡⚫ ⭐ | DFS/BFS from each unvisited '1' |
| 20 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | LC #133 | Medium | 🔵🟠🔴🟣🟢 ⭐ | HashMap old→new, DFS/BFS |
| 21 | [Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | LC #695 | Medium | 🔵🟠🔴🟣 | DFS counting cells |
| 22 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | LC #417 | Medium | 🔵🟠🔴🟣 | BFS from edges, find intersection |

### Day 6: Graph BFS

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 23 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | LC #994 | Medium | 🔵🟠🔴🟣 ⭐ | Multi-source BFS from all rotten |
| 24 | [Walls and Gates](https://leetcode.com/problems/walls-and-gates/) | LC #286 | Medium | 🔵🔴🟣🔷 ⭐ | Multi-source BFS from gates |
| 25 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | LC #127 | Hard | 🔵🟠🔴🟣🟢🟡 ⭐ | BFS, try all single-char changes |
| 26 | [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | LC #1091 | Medium | 🔵🟠🔴🟣 | BFS, 8 directions |

### Day 7: Graph Advanced

| # | Problem | Source | Difficulty | Companies | Hint |
|---|---------|--------|------------|-----------|------|
| 27 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | LC #207 | Medium | 🔵🟠🔴🟣🟢🟡 ⭐ | Topological sort, detect cycle |
| 28 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | LC #210 | Medium | 🔵🟠🔴🟣🟢 ⭐ | Return topological order |
| 29 | [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | LC #269 | Hard | 🔵🟠🔴🟣🟢🔷⚫ ⭐ | Build graph from word order, topo sort |
| 30 | [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | LC #261 | Medium | 🔵🔴🟣🔘 ⭐ | n-1 edges, no cycle, connected |

---

## 🧩 Pattern Recognition Cheat Sheet

| Clue in Problem | Pattern to Try |
|-----------------|----------------|
| "Level by level" | BFS |
| "Depth first" | DFS (recursion or stack) |
| "Shortest path (unweighted)" | BFS |
| "Connected components" | DFS/BFS from each unvisited |
| "Cycle in graph" | DFS with visited states |
| "Ordering with dependencies" | Topological Sort |
| "BST operations" | Use BST property (left < root < right) |
| "LCA" | Recursively check both subtrees |
| "Path in tree" | DFS with backtracking |
| "Diameter/height" | Post-order DFS |

---

## ⏱️ Time Complexity

| Operation | Binary Tree | BST (balanced) | BST (unbalanced) | Graph |
|-----------|-------------|----------------|------------------|-------|
| Search | O(n) | O(log n) | O(n) | O(V+E) |
| Insert | O(n)* | O(log n) | O(n) | O(1) |
| Delete | O(n)* | O(log n) | O(n) | O(V) |
| Traversal | O(n) | O(n) | O(n) | O(V+E) |

*Finding position takes O(n), insertion itself is O(1)

---

## ✅ Week 3 Checklist

- [ ] Master all tree traversals (recursive + iterative)
- [ ] Understand DFS patterns for trees
- [ ] Implement graph BFS for shortest path
- [ ] Practice cycle detection algorithms
- [ ] Implement topological sort both ways
- [ ] Solve all 30 practice problems

