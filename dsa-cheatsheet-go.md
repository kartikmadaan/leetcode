# DSA Cheatsheet - Go Implementations

## Table of Contents
1. [Slices & Arrays](#slices--arrays)
2. [Strings](#strings)
3. [Maps & Sets](#maps--sets)
4. [Linked Lists](#linked-lists)
5. [Stacks & Queues](#stacks--queues)
6. [Trees](#trees)
7. [Heaps](#heaps)
8. [Graphs](#graphs)
9. [Sorting](#sorting)
10. [Searching](#searching)
11. [Dynamic Programming](#dynamic-programming)
12. [Common Patterns](#common-patterns)

---

## Slices & Arrays

### Basics
```go
package main

import (
    "sort"
    "slices" // Go 1.21+
)

// Declaration
arr := []int{1, 2, 3, 4, 5}
arr := make([]int, 5)        // length 5, all zeros
arr := make([]int, 0, 10)    // length 0, capacity 10

// Access
first := arr[0]
last := arr[len(arr)-1]

// Modify
arr = append(arr, 6)         // O(1) amortized
arr = append(arr[:i], arr[i+1:]...)  // delete at index i
arr = append(arr[:i], append([]int{val}, arr[i:]...)...)  // insert at i

// Slice operations
sub := arr[1:4]              // elements 1, 2, 3
copy(dst, src)               // copy src to dst

// Sorting
sort.Ints(arr)               // ascending
sort.Sort(sort.Reverse(sort.IntSlice(arr)))  // descending
slices.Sort(arr)             // Go 1.21+

// Other operations
slices.Reverse(arr)          // Go 1.21+
slices.Max(arr)              // Go 1.21+
slices.Min(arr)              // Go 1.21+
slices.Contains(arr, val)    // Go 1.21+

// Sum (no built-in)
func sum(arr []int) int {
    total := 0
    for _, v := range arr {
        total += v
    }
    return total
}
```

### Two Pointers
```go
// Two Sum (sorted array)
func twoSum(nums []int, target int) []int {
    left, right := 0, len(nums)-1
    for left < right {
        sum := nums[left] + nums[right]
        if sum == target {
            return []int{left, right}
        } else if sum < target {
            left++
        } else {
            right--
        }
    }
    return []int{-1, -1}
}

// Remove duplicates in-place
func removeDuplicates(nums []int) int {
    if len(nums) == 0 {
        return 0
    }
    slow := 0
    for fast := 1; fast < len(nums); fast++ {
        if nums[fast] != nums[slow] {
            slow++
            nums[slow] = nums[fast]
        }
    }
    return slow + 1
}
```

### Sliding Window
```go
// Fixed size window - max sum of k elements
func maxSumSubarray(nums []int, k int) int {
    windowSum, maxSum := 0, math.MinInt32
    for i := 0; i < len(nums); i++ {
        windowSum += nums[i]
        if i >= k-1 {
            if windowSum > maxSum {
                maxSum = windowSum
            }
            windowSum -= nums[i-k+1]
        }
    }
    return maxSum
}

// Variable size window - longest subarray with sum <= k
func longestSubarray(nums []int, k int) int {
    left, sum, maxLen := 0, 0, 0
    for right := 0; right < len(nums); right++ {
        sum += nums[right]
        for sum > k {
            sum -= nums[left]
            left++
        }
        if right-left+1 > maxLen {
            maxLen = right - left + 1
        }
    }
    return maxLen
}
```

---

## Strings

### Basics
```go
import (
    "strings"
    "strconv"
)

s := "hello"

// Access
ch := s[0]                    // byte
runes := []rune(s)            // for Unicode

// Substring
sub := s[1:4]                 // "ell"

// Find
idx := strings.Index(s, "ll") // 2, or -1 if not found
contains := strings.Contains(s, "ll")

// Modify (strings are immutable, creates new string)
upper := strings.ToUpper(s)
lower := strings.ToLower(s)
replaced := strings.Replace(s, "l", "L", -1)  // replace all
trimmed := strings.TrimSpace("  hello  ")

// Split & Join
parts := strings.Split("a,b,c", ",")  // []string{"a", "b", "c"}
joined := strings.Join(parts, "-")     // "a-b-c"

// Convert
numStr := strconv.Itoa(123)            // int to string
num, _ := strconv.Atoi("123")          // string to int
floatNum, _ := strconv.ParseFloat("12.3", 64)

// String builder (efficient concatenation)
var sb strings.Builder
sb.WriteString("hello")
sb.WriteByte(' ')
sb.WriteString("world")
result := sb.String()

// Check palindrome
func isPalindrome(s string) bool {
    runes := []rune(s)
    left, right := 0, len(runes)-1
    for left < right {
        if runes[left] != runes[right] {
            return false
        }
        left++
        right--
    }
    return true
}
```

---

## Maps & Sets

### Map (HashMap)
```go
// Declaration
mp := make(map[string]int)
mp := map[string]int{"key": 10}

// Insert/Update
mp["key"] = 10

// Access
val := mp["key"]              // returns zero value if not exists
val, exists := mp["key"]      // check existence

// Delete
delete(mp, "key")

// Iterate
for key, val := range mp {
    fmt.Println(key, val)
}

// Frequency counter pattern
freq := make(map[int]int)
for _, num := range nums {
    freq[num]++
}
```

### Set (using map[T]struct{})
```go
// Set using map
set := make(map[int]struct{})

// Add
set[1] = struct{}{}

// Remove
delete(set, 1)

// Check existence
_, exists := set[1]

// Size
size := len(set)

// Convert slice to set (remove duplicates)
unique := make(map[int]struct{})
for _, num := range nums {
    unique[num] = struct{}{}
}
```

### Ordered Map (using slice of keys)
```go
// For ordered iteration, maintain separate slice of keys
keys := []string{}
mp := make(map[string]int)

// Add
if _, exists := mp[key]; !exists {
    keys = append(keys, key)
}
mp[key] = val

// Iterate in order
for _, key := range keys {
    val := mp[key]
    // ...
}
```

---

## Linked Lists

### Node Definition
```go
type ListNode struct {
    Val  int
    Next *ListNode
}

func NewListNode(val int) *ListNode {
    return &ListNode{Val: val}
}
```

### Common Operations
```go
// Reverse Linked List
func reverseList(head *ListNode) *ListNode {
    var prev *ListNode
    curr := head
    for curr != nil {
        next := curr.Next
        curr.Next = prev
        prev = curr
        curr = next
    }
    return prev
}

// Find middle (slow-fast pointers)
func findMiddle(head *ListNode) *ListNode {
    slow, fast := head, head
    for fast != nil && fast.Next != nil {
        slow = slow.Next
        fast = fast.Next.Next
    }
    return slow
}

// Detect cycle
func hasCycle(head *ListNode) bool {
    slow, fast := head, head
    for fast != nil && fast.Next != nil {
        slow = slow.Next
        fast = fast.Next.Next
        if slow == fast {
            return true
        }
    }
    return false
}

// Merge two sorted lists
func mergeTwoLists(l1, l2 *ListNode) *ListNode {
    dummy := &ListNode{}
    tail := dummy
    for l1 != nil && l2 != nil {
        if l1.Val < l2.Val {
            tail.Next = l1
            l1 = l1.Next
        } else {
            tail.Next = l2
            l2 = l2.Next
        }
        tail = tail.Next
    }
    if l1 != nil {
        tail.Next = l1
    } else {
        tail.Next = l2
    }
    return dummy.Next
}
```

---

## Stacks & Queues

### Stack (using slice)
```go
type Stack []int

func (s *Stack) Push(val int) {
    *s = append(*s, val)
}

func (s *Stack) Pop() int {
    if len(*s) == 0 {
        return -1 // or panic
    }
    val := (*s)[len(*s)-1]
    *s = (*s)[:len(*s)-1]
    return val
}

func (s *Stack) Top() int {
    if len(*s) == 0 {
        return -1
    }
    return (*s)[len(*s)-1]
}

func (s *Stack) IsEmpty() bool {
    return len(*s) == 0
}

// Monotonic Stack - Next Greater Element
func nextGreater(nums []int) []int {
    n := len(nums)
    result := make([]int, n)
    for i := range result {
        result[i] = -1
    }
    stack := []int{} // stores indices
    
    for i := 0; i < n; i++ {
        for len(stack) > 0 && nums[stack[len(stack)-1]] < nums[i] {
            idx := stack[len(stack)-1]
            stack = stack[:len(stack)-1]
            result[idx] = nums[i]
        }
        stack = append(stack, i)
    }
    return result
}

// Valid Parentheses
func isValid(s string) bool {
    stack := []rune{}
    pairs := map[rune]rune{')': '(', ']': '[', '}': '{'}
    
    for _, c := range s {
        if match, exists := pairs[c]; exists {
            if len(stack) == 0 || stack[len(stack)-1] != match {
                return false
            }
            stack = stack[:len(stack)-1]
        } else {
            stack = append(stack, c)
        }
    }
    return len(stack) == 0
}
```

### Queue (using slice)
```go
type Queue []int

func (q *Queue) Push(val int) {
    *q = append(*q, val)
}

func (q *Queue) Pop() int {
    if len(*q) == 0 {
        return -1
    }
    val := (*q)[0]
    *q = (*q)[1:]
    return val
}

func (q *Queue) Front() int {
    if len(*q) == 0 {
        return -1
    }
    return (*q)[0]
}

func (q *Queue) IsEmpty() bool {
    return len(*q) == 0
}
```

### Deque (using container/list)
```go
import "container/list"

dq := list.New()
dq.PushFront(1)
dq.PushBack(2)
front := dq.Front().Value.(int)
back := dq.Back().Value.(int)
dq.Remove(dq.Front())
dq.Remove(dq.Back())

// Sliding Window Maximum
func maxSlidingWindow(nums []int, k int) []int {
    dq := []int{} // stores indices
    result := []int{}
    
    for i := 0; i < len(nums); i++ {
        // Remove indices outside window
        for len(dq) > 0 && dq[0] < i-k+1 {
            dq = dq[1:]
        }
        // Remove smaller elements
        for len(dq) > 0 && nums[dq[len(dq)-1]] < nums[i] {
            dq = dq[:len(dq)-1]
        }
        dq = append(dq, i)
        if i >= k-1 {
            result = append(result, nums[dq[0]])
        }
    }
    return result
}
```

---

## Trees

### Node Definition
```go
type TreeNode struct {
    Val   int
    Left  *TreeNode
    Right *TreeNode
}

func NewTreeNode(val int) *TreeNode {
    return &TreeNode{Val: val}
}
```

### Traversals
```go
// DFS - Recursive
func preorder(root *TreeNode, result *[]int) {
    if root == nil {
        return
    }
    *result = append(*result, root.Val)
    preorder(root.Left, result)
    preorder(root.Right, result)
}

func inorder(root *TreeNode, result *[]int) {
    if root == nil {
        return
    }
    inorder(root.Left, result)
    *result = append(*result, root.Val)
    inorder(root.Right, result)
}

func postorder(root *TreeNode, result *[]int) {
    if root == nil {
        return
    }
    postorder(root.Left, result)
    postorder(root.Right, result)
    *result = append(*result, root.Val)
}

// DFS - Iterative (Preorder)
func preorderIterative(root *TreeNode) []int {
    result := []int{}
    if root == nil {
        return result
    }
    stack := []*TreeNode{root}
    for len(stack) > 0 {
        node := stack[len(stack)-1]
        stack = stack[:len(stack)-1]
        result = append(result, node.Val)
        if node.Right != nil {
            stack = append(stack, node.Right)
        }
        if node.Left != nil {
            stack = append(stack, node.Left)
        }
    }
    return result
}

// BFS - Level Order
func levelOrder(root *TreeNode) [][]int {
    result := [][]int{}
    if root == nil {
        return result
    }
    queue := []*TreeNode{root}
    for len(queue) > 0 {
        levelSize := len(queue)
        level := []int{}
        for i := 0; i < levelSize; i++ {
            node := queue[0]
            queue = queue[1:]
            level = append(level, node.Val)
            if node.Left != nil {
                queue = append(queue, node.Left)
            }
            if node.Right != nil {
                queue = append(queue, node.Right)
            }
        }
        result = append(result, level)
    }
    return result
}
```

### Common Operations
```go
// Max Depth
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }
    left := maxDepth(root.Left)
    right := maxDepth(root.Right)
    if left > right {
        return 1 + left
    }
    return 1 + right
}

// Validate BST
func isValidBST(root *TreeNode) bool {
    return validate(root, math.MinInt64, math.MaxInt64)
}

func validate(node *TreeNode, min, max int) bool {
    if node == nil {
        return true
    }
    if node.Val <= min || node.Val >= max {
        return false
    }
    return validate(node.Left, min, node.Val) && validate(node.Right, node.Val, max)
}

// Lowest Common Ancestor
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
    if root == nil || root == p || root == q {
        return root
    }
    left := lowestCommonAncestor(root.Left, p, q)
    right := lowestCommonAncestor(root.Right, p, q)
    if left != nil && right != nil {
        return root
    }
    if left != nil {
        return left
    }
    return right
}
```

---

## Heaps

### Using container/heap
```go
import "container/heap"

// Min Heap implementation
type MinHeap []int

func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *MinHeap) Push(x interface{}) {
    *h = append(*h, x.(int))
}

func (h *MinHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}

// Usage
func main() {
    h := &MinHeap{3, 1, 2}
    heap.Init(h)
    heap.Push(h, 0)
    min := heap.Pop(h).(int)  // 0
}

// Max Heap - just change Less
func (h MaxHeap) Less(i, j int) bool { return h[i] > h[j] }

// Priority Queue with custom type
type Item struct {
    value    int
    priority int
    index    int
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool {
    return pq[i].priority < pq[j].priority // min heap by priority
}
func (pq PriorityQueue) Swap(i, j int) {
    pq[i], pq[j] = pq[j], pq[i]
    pq[i].index = i
    pq[j].index = j
}
func (pq *PriorityQueue) Push(x interface{}) {
    n := len(*pq)
    item := x.(*Item)
    item.index = n
    *pq = append(*pq, item)
}
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq
    n := len(old)
    item := old[n-1]
    old[n-1] = nil
    item.index = -1
    *pq = old[0 : n-1]
    return item
}

// Top K Frequent Elements
func topKFrequent(nums []int, k int) []int {
    freq := make(map[int]int)
    for _, num := range nums {
        freq[num]++
    }
    
    h := &MinHeap{}
    heap.Init(h)
    
    for num := range freq {
        heap.Push(h, num)
        if h.Len() > k {
            heap.Pop(h)
        }
    }
    
    result := make([]int, k)
    for i := k - 1; i >= 0; i-- {
        result[i] = heap.Pop(h).(int)
    }
    return result
}
```

---

## Graphs

### Representations
```go
// Adjacency List
type Graph [][]int
graph := make([][]int, n)  // n nodes
graph[u] = append(graph[u], v)  // edge u -> v

// Adjacency List with weights
type Edge struct {
    to, weight int
}
graph := make([][]Edge, n)
graph[u] = append(graph[u], Edge{v, weight})

// Edge List
type EdgeInfo struct {
    from, to, weight int
}
edges := []EdgeInfo{}
```

### BFS
```go
func bfs(graph [][]int, start int) []int {
    n := len(graph)
    dist := make([]int, n)
    for i := range dist {
        dist[i] = -1
    }
    
    queue := []int{start}
    dist[start] = 0
    
    for len(queue) > 0 {
        node := queue[0]
        queue = queue[1:]
        for _, neighbor := range graph[node] {
            if dist[neighbor] == -1 {
                dist[neighbor] = dist[node] + 1
                queue = append(queue, neighbor)
            }
        }
    }
    return dist
}
```

### DFS
```go
func dfs(graph [][]int, node int, visited []bool) {
    visited[node] = true
    for _, neighbor := range graph[node] {
        if !visited[neighbor] {
            dfs(graph, neighbor, visited)
        }
    }
}

// Number of Connected Components
func countComponents(n int, graph [][]int) int {
    visited := make([]bool, n)
    count := 0
    for i := 0; i < n; i++ {
        if !visited[i] {
            dfs(graph, i, visited)
            count++
        }
    }
    return count
}
```

### Topological Sort (Kahn's Algorithm)
```go
func topologicalSort(n int, graph [][]int) []int {
    inDegree := make([]int, n)
    for u := 0; u < n; u++ {
        for _, v := range graph[u] {
            inDegree[v]++
        }
    }
    
    queue := []int{}
    for i := 0; i < n; i++ {
        if inDegree[i] == 0 {
            queue = append(queue, i)
        }
    }
    
    order := []int{}
    for len(queue) > 0 {
        node := queue[0]
        queue = queue[1:]
        order = append(order, node)
        for _, neighbor := range graph[node] {
            inDegree[neighbor]--
            if inDegree[neighbor] == 0 {
                queue = append(queue, neighbor)
            }
        }
    }
    
    if len(order) != n {
        return []int{} // cycle detected
    }
    return order
}
```

### Dijkstra's Algorithm
```go
import "container/heap"

type Edge struct {
    to, weight int
}

type Item struct {
    node, dist int
}

type MinHeap []Item

func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i].dist < h[j].dist }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x interface{}) { *h = append(*h, x.(Item)) }
func (h *MinHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}

func dijkstra(graph [][]Edge, start int) []int {
    n := len(graph)
    dist := make([]int, n)
    for i := range dist {
        dist[i] = math.MaxInt32
    }
    
    h := &MinHeap{Item{start, 0}}
    heap.Init(h)
    dist[start] = 0
    
    for h.Len() > 0 {
        item := heap.Pop(h).(Item)
        u, d := item.node, item.dist
        if d > dist[u] {
            continue
        }
        for _, edge := range graph[u] {
            v, w := edge.to, edge.weight
            if dist[u]+w < dist[v] {
                dist[v] = dist[u] + w
                heap.Push(h, Item{v, dist[v]})
            }
        }
    }
    return dist
}
```

### Union-Find (Disjoint Set Union)
```go
type UnionFind struct {
    parent, rank []int
}

func NewUnionFind(n int) *UnionFind {
    parent := make([]int, n)
    rank := make([]int, n)
    for i := range parent {
        parent[i] = i
    }
    return &UnionFind{parent, rank}
}

func (uf *UnionFind) Find(x int) int {
    if uf.parent[x] != x {
        uf.parent[x] = uf.Find(uf.parent[x]) // path compression
    }
    return uf.parent[x]
}

func (uf *UnionFind) Unite(x, y int) bool {
    px, py := uf.Find(x), uf.Find(y)
    if px == py {
        return false
    }
    // Union by rank
    if uf.rank[px] < uf.rank[py] {
        px, py = py, px
    }
    uf.parent[py] = px
    if uf.rank[px] == uf.rank[py] {
        uf.rank[px]++
    }
    return true
}

func (uf *UnionFind) Connected(x, y int) bool {
    return uf.Find(x) == uf.Find(y)
}
```

---

## Sorting

### Quick Reference
| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable |
|-----------|-------------|------------|--------------|-------|--------|
| Go's sort | O(n log n)  | O(n log n) | O(n log n)   | O(log n) | No  |

### Built-in Sorting
```go
import "sort"

// Sort integers
nums := []int{3, 1, 2}
sort.Ints(nums)  // ascending

// Sort descending
sort.Sort(sort.Reverse(sort.IntSlice(nums)))

// Sort strings
strs := []string{"c", "a", "b"}
sort.Strings(strs)

// Sort with custom comparator
sort.Slice(nums, func(i, j int) bool {
    return nums[i] > nums[j]  // descending
})

// Sort structs
type Person struct {
    Name string
    Age  int
}
people := []Person{{"Bob", 30}, {"Alice", 25}}
sort.Slice(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})

// Stable sort
sort.SliceStable(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})
```

### Merge Sort
```go
func mergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    mid := len(arr) / 2
    left := mergeSort(arr[:mid])
    right := mergeSort(arr[mid:])
    return merge(left, right)
}

func merge(left, right []int) []int {
    result := make([]int, 0, len(left)+len(right))
    i, j := 0, 0
    for i < len(left) && j < len(right) {
        if left[i] <= right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    return result
}
```

### Quick Sort
```go
func quickSort(arr []int, left, right int) {
    if left >= right {
        return
    }
    pivot := partition(arr, left, right)
    quickSort(arr, left, pivot-1)
    quickSort(arr, pivot+1, right)
}

func partition(arr []int, left, right int) int {
    pivot := arr[right]
    i := left - 1
    for j := left; j < right; j++ {
        if arr[j] < pivot {
            i++
            arr[i], arr[j] = arr[j], arr[i]
        }
    }
    arr[i+1], arr[right] = arr[right], arr[i+1]
    return i + 1
}
```

---

## Searching

### Binary Search
```go
import "sort"

// Standard - find exact value
func binarySearch(arr []int, target int) int {
    left, right := 0, len(arr)-1
    for left <= right {
        mid := left + (right-left)/2
        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}

// Lower bound - first element >= target
func lowerBound(arr []int, target int) int {
    left, right := 0, len(arr)
    for left < right {
        mid := left + (right-left)/2
        if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid
        }
    }
    return left
}

// Upper bound - first element > target
func upperBound(arr []int, target int) int {
    left, right := 0, len(arr)
    for left < right {
        mid := left + (right-left)/2
        if arr[mid] <= target {
            left = mid + 1
        } else {
            right = mid
        }
    }
    return left
}

// Built-in search
idx := sort.SearchInts(arr, target)  // like lower_bound
```

### Binary Search on Answer
```go
// Koko Eating Bananas pattern
func minEatingSpeed(piles []int, h int) int {
    maxPile := 0
    for _, pile := range piles {
        if pile > maxPile {
            maxPile = pile
        }
    }
    
    left, right := 1, maxPile
    for left < right {
        mid := left + (right-left)/2
        if canFinish(piles, mid, h) {
            right = mid
        } else {
            left = mid + 1
        }
    }
    return left
}

func canFinish(piles []int, speed, h int) bool {
    hours := 0
    for _, pile := range piles {
        hours += (pile + speed - 1) / speed  // ceiling division
    }
    return hours <= h
}
```

---

## Dynamic Programming

### 1D DP
```go
// Fibonacci
func fib(n int) int {
    if n <= 1 {
        return n
    }
    prev2, prev1 := 0, 1
    for i := 2; i <= n; i++ {
        curr := prev1 + prev2
        prev2 = prev1
        prev1 = curr
    }
    return prev1
}

// Climbing Stairs
func climbStairs(n int) int {
    if n <= 2 {
        return n
    }
    prev2, prev1 := 1, 2
    for i := 3; i <= n; i++ {
        curr := prev1 + prev2
        prev2 = prev1
        prev1 = curr
    }
    return prev1
}

// House Robber
func rob(nums []int) int {
    prev2, prev1 := 0, 0
    for _, num := range nums {
        curr := max(prev1, prev2+num)
        prev2 = prev1
        prev1 = curr
    }
    return prev1
}

// Coin Change
func coinChange(coins []int, amount int) int {
    dp := make([]int, amount+1)
    for i := range dp {
        dp[i] = amount + 1
    }
    dp[0] = 0
    
    for i := 1; i <= amount; i++ {
        for _, coin := range coins {
            if coin <= i && dp[i-coin]+1 < dp[i] {
                dp[i] = dp[i-coin] + 1
            }
        }
    }
    
    if dp[amount] > amount {
        return -1
    }
    return dp[amount]
}

// Longest Increasing Subsequence
func lengthOfLIS(nums []int) int {
    tails := []int{}
    for _, num := range nums {
        pos := sort.SearchInts(tails, num)
        if pos == len(tails) {
            tails = append(tails, num)
        } else {
            tails[pos] = num
        }
    }
    return len(tails)
}
```

### 2D DP
```go
// Unique Paths
func uniquePaths(m, n int) int {
    dp := make([][]int, m)
    for i := range dp {
        dp[i] = make([]int, n)
        for j := range dp[i] {
            dp[i][j] = 1
        }
    }
    
    for i := 1; i < m; i++ {
        for j := 1; j < n; j++ {
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
        }
    }
    return dp[m-1][n-1]
}

// Longest Common Subsequence
func longestCommonSubsequence(s1, s2 string) int {
    m, n := len(s1), len(s2)
    dp := make([][]int, m+1)
    for i := range dp {
        dp[i] = make([]int, n+1)
    }
    
    for i := 1; i <= m; i++ {
        for j := 1; j <= n; j++ {
            if s1[i-1] == s2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            }
        }
    }
    return dp[m][n]
}

// Edit Distance
func minDistance(s1, s2 string) int {
    m, n := len(s1), len(s2)
    dp := make([][]int, m+1)
    for i := range dp {
        dp[i] = make([]int, n+1)
    }
    
    for i := 0; i <= m; i++ {
        dp[i][0] = i
    }
    for j := 0; j <= n; j++ {
        dp[0][j] = j
    }
    
    for i := 1; i <= m; i++ {
        for j := 1; j <= n; j++ {
            if s1[i-1] == s2[j-1] {
                dp[i][j] = dp[i-1][j-1]
            } else {
                dp[i][j] = 1 + min(dp[i-1][j], min(dp[i][j-1], dp[i-1][j-1]))
            }
        }
    }
    return dp[m][n]
}
```

---

## Common Patterns

### Backtracking Template
```go
func backtrack(result *[][]int, current []int, nums []int, start int) {
    // Make a copy for subsets
    temp := make([]int, len(current))
    copy(temp, current)
    *result = append(*result, temp)
    
    for i := start; i < len(nums); i++ {
        // Skip duplicates if needed: if i > start && nums[i] == nums[i-1] { continue }
        current = append(current, nums[i])
        backtrack(result, current, nums, i+1)
        current = current[:len(current)-1]
    }
}

// Subsets
func subsets(nums []int) [][]int {
    result := [][]int{}
    backtrack(&result, []int{}, nums, 0)
    return result
}

// Permutations
func permute(nums []int) [][]int {
    result := [][]int{}
    permuteHelper(&result, nums, 0)
    return result
}

func permuteHelper(result *[][]int, nums []int, start int) {
    if start == len(nums) {
        temp := make([]int, len(nums))
        copy(temp, nums)
        *result = append(*result, temp)
        return
    }
    for i := start; i < len(nums); i++ {
        nums[start], nums[i] = nums[i], nums[start]
        permuteHelper(result, nums, start+1)
        nums[start], nums[i] = nums[i], nums[start]
    }
}
```

### Prefix Sum
```go
// Build prefix sum
prefix := make([]int, len(nums)+1)
for i := 0; i < len(nums); i++ {
    prefix[i+1] = prefix[i] + nums[i]
}

// Sum of range [l, r]
rangeSum := prefix[r+1] - prefix[l]
```

### Bit Manipulation
```go
import "math/bits"

// Check if bit is set
isSet := (n >> i) & 1 == 1

// Set bit
n |= (1 << i)

// Clear bit
n &= ^(1 << i)

// Toggle bit
n ^= (1 << i)

// Count set bits
count := bits.OnesCount(uint(n))

// Check power of 2
isPowerOf2 := n > 0 && (n&(n-1)) == 0

// Get lowest set bit
lowest := n & (-n)

// Iterate through all subsets of a bitmask
for subset := mask; subset > 0; subset = (subset - 1) & mask {
    // process subset
}
```

### Helper Functions (Go doesn't have generics for all)
```go
func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}

func abs(a int) int {
    if a < 0 {
        return -a
    }
    return a
}
```

