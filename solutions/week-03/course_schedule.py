"""
Problem: Course Schedule (LeetCode #207)
Difficulty: Medium

There are numCourses courses labeled from 0 to numCourses-1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] 
indicates that you must take course bi first if you want to take course ai.

Return true if you can finish all courses.

Example:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: true
    Explanation: Take course 0, then course 1.

    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output: false
    Explanation: Circular dependency.

Key Insight:
- This is a cycle detection problem in a directed graph
- If there's a cycle, we cannot complete all courses
- Use either DFS (with 3 colors) or BFS (Kahn's algorithm)
"""

from typing import List
from collections import deque, defaultdict


def can_finish_dfs(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    DFS Approach with 3-color marking
    Time: O(V + E) - visit each node and edge once
    Space: O(V + E) - adjacency list and recursion stack
    
    Colors:
    - WHITE (0): Unvisited
    - GRAY (1): Currently in DFS path (visiting)
    - BLACK (2): Completely processed
    
    Cycle exists if we encounter a GRAY node during DFS
    """
    # Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # Color states
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * numCourses
    
    def has_cycle(node: int) -> bool:
        """Returns True if cycle is detected"""
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Back edge found - cycle!
                return True
            if color[neighbor] == WHITE:
                if has_cycle(neighbor):
                    return True
        
        color[node] = BLACK
        return False
    
    # Check each unvisited node
    for course in range(numCourses):
        if color[course] == WHITE:
            if has_cycle(course):
                return False
    
    return True


def can_finish_bfs(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    BFS Approach - Kahn's Algorithm (Topological Sort)
    Time: O(V + E)
    Space: O(V + E)
    
    Key Insight:
    - Calculate in-degree for each node
    - Start with nodes having in-degree 0 (no prerequisites)
    - Process nodes and reduce in-degrees
    - If we can process all nodes, no cycle exists
    """
    # Build graph and calculate in-degrees
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Start with courses having no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        
        # Reduce in-degree for dependent courses
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # If we completed all courses, no cycle
    return completed == numCourses


def find_order(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Course Schedule II (LeetCode #210)
    Return the order to take courses, or empty if impossible.
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return order if len(order) == numCourses else []


# Visualization helper
def visualize_dependencies(numCourses: int, prerequisites: List[List[int]]):
    """Visualize course dependencies"""
    print(f"\nCourse Dependencies (numCourses={numCourses}):")
    print("-" * 40)
    
    for course, prereq in prerequisites:
        print(f"  Course {prereq} -> Course {course}")
    
    order = find_order(numCourses, prerequisites)
    if order:
        print(f"\nValid order: {' -> '.join(map(str, order))}")
    else:
        print("\nNo valid order (cycle detected)")


# Test cases
if __name__ == "__main__":
    test_cases = [
        (2, [[1, 0]], True),           # Simple chain
        (2, [[1, 0], [0, 1]], False),  # Cycle
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),  # Diamond
        (1, [], True),                  # Single course
        (3, [[0, 1], [0, 2], [1, 2]], True),  # Multiple deps
    ]
    
    print("Testing DFS approach:")
    for num, prereqs, expected in test_cases:
        result = can_finish_dfs(num, prereqs)
        status = "✓" if result == expected else "✗"
        print(f"  {status} numCourses={num}, prereqs={prereqs} -> {result}")
    
    print("\nTesting BFS approach:")
    for num, prereqs, expected in test_cases:
        result = can_finish_bfs(num, prereqs)
        status = "✓" if result == expected else "✗"
        print(f"  {status} numCourses={num}, prereqs={prereqs} -> {result}")
    
    # Visualize an example
    visualize_dependencies(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    visualize_dependencies(2, [[1, 0], [0, 1]])

