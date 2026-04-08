# DSA Cheatsheet - C++ Implementations

## Table of Contents
1. [Arrays & Vectors](#arrays--vectors)
2. [Strings](#strings)
3. [Hash Maps & Sets](#hash-maps--sets)
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

## Arrays & Vectors

### Basics
```cpp
#include <vector>
#include <algorithm>

vector<int> arr = {1, 2, 3, 4, 5};

// Access
arr[0];           // O(1)
arr.front();      // first element
arr.back();       // last element

// Modify
arr.push_back(6);     // O(1) amortized
arr.pop_back();       // O(1)
arr.insert(arr.begin() + 2, 10);  // O(n)
arr.erase(arr.begin() + 2);       // O(n)

// Size
arr.size();       // current size
arr.empty();      // check if empty
arr.resize(10);   // resize
arr.clear();      // remove all

// Algorithms
sort(arr.begin(), arr.end());                    // ascending
sort(arr.begin(), arr.end(), greater<int>());    // descending
reverse(arr.begin(), arr.end());
auto it = find(arr.begin(), arr.end(), 3);       // find element
int maxVal = *max_element(arr.begin(), arr.end());
int minVal = *min_element(arr.begin(), arr.end());
int sum = accumulate(arr.begin(), arr.end(), 0);
```

### Two Pointers
```cpp
// Two Sum (sorted array)
pair<int, int> twoSum(vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    while (left < right) {
        int sum = nums[left] + nums[right];
        if (sum == target) return {left, right};
        else if (sum < target) left++;
        else right--;
    }
    return {-1, -1};
}

// Remove duplicates in-place
int removeDuplicates(vector<int>& nums) {
    if (nums.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.size(); fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
```

### Sliding Window
```cpp
// Fixed size window - max sum of k elements
int maxSumSubarray(vector<int>& nums, int k) {
    int windowSum = 0, maxSum = INT_MIN;
    for (int i = 0; i < nums.size(); i++) {
        windowSum += nums[i];
        if (i >= k - 1) {
            maxSum = max(maxSum, windowSum);
            windowSum -= nums[i - k + 1];
        }
    }
    return maxSum;
}

// Variable size window - longest subarray with sum <= k
int longestSubarray(vector<int>& nums, int k) {
    int left = 0, sum = 0, maxLen = 0;
    for (int right = 0; right < nums.size(); right++) {
        sum += nums[right];
        while (sum > k) {
            sum -= nums[left++];
        }
        maxLen = max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

---

## Strings

### Basics
```cpp
#include <string>
#include <sstream>

string s = "hello";

// Access
s[0];              // 'h'
s.substr(1, 3);    // "ell" (start, length)
s.find("ll");      // 2 (position, or string::npos if not found)

// Modify
s += " world";     // append
s.insert(5, "!");  // insert at position
s.erase(5, 1);     // erase from pos, length
s.replace(0, 5, "hi");  // replace

// Convert
to_string(123);    // int to string
stoi("123");       // string to int
stol("123");       // string to long
stod("12.3");      // string to double

// Split by delimiter
vector<string> split(const string& s, char delim) {
    vector<string> tokens;
    stringstream ss(s);
    string token;
    while (getline(ss, token, delim)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Check palindrome
bool isPalindrome(const string& s) {
    int left = 0, right = s.size() - 1;
    while (left < right) {
        if (s[left++] != s[right--]) return false;
    }
    return true;
}
```

---

## Hash Maps & Sets

### Unordered Map (HashMap)
```cpp
#include <unordered_map>

unordered_map<string, int> mp;

// Insert/Update
mp["key"] = 10;
mp.insert({"key2", 20});

// Access
mp["key"];                    // returns value (creates if not exists!)
mp.at("key");                 // throws if not exists
mp.count("key");              // 1 if exists, 0 otherwise
mp.find("key") != mp.end();   // check existence

// Delete
mp.erase("key");

// Iterate
for (auto& [key, val] : mp) {
    cout << key << ": " << val << endl;
}

// Frequency counter pattern
unordered_map<int, int> freq;
for (int num : nums) freq[num]++;
```

### Unordered Set (HashSet)
```cpp
#include <unordered_set>

unordered_set<int> st;

st.insert(1);
st.erase(1);
st.count(1);      // 1 if exists
st.find(1) != st.end();  // check existence
st.size();
st.clear();

// Convert vector to set (remove duplicates)
unordered_set<int> unique(nums.begin(), nums.end());
```

### Ordered Map/Set (TreeMap/TreeSet)
```cpp
#include <map>
#include <set>

map<int, int> ordered_map;      // sorted by keys
set<int> ordered_set;           // sorted elements

// Lower/Upper bound (logarithmic)
auto it = ordered_set.lower_bound(5);  // >= 5
auto it = ordered_set.upper_bound(5);  // > 5
```

---

## Linked Lists

### Node Definition
```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};
```

### Common Operations
```cpp
// Reverse Linked List
ListNode* reverse(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;
    while (curr) {
        ListNode* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

// Find middle (slow-fast pointers)
ListNode* findMiddle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

// Detect cycle
bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

// Merge two sorted lists
ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* tail = &dummy;
    while (l1 && l2) {
        if (l1->val < l2->val) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }
    tail->next = l1 ? l1 : l2;
    return dummy.next;
}
```

---

## Stacks & Queues

### Stack
```cpp
#include <stack>

stack<int> st;

st.push(1);
st.pop();         // void, just removes
st.top();         // peek
st.empty();
st.size();

// Monotonic Stack - Next Greater Element
vector<int> nextGreater(vector<int>& nums) {
    int n = nums.size();
    vector<int> result(n, -1);
    stack<int> st;  // stores indices
    
    for (int i = 0; i < n; i++) {
        while (!st.empty() && nums[st.top()] < nums[i]) {
            result[st.top()] = nums[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}

// Valid Parentheses
bool isValid(string s) {
    stack<char> st;
    unordered_map<char, char> pairs = {{')', '('}, {']', '['}, {'}', '{'}};
    
    for (char c : s) {
        if (pairs.count(c)) {
            if (st.empty() || st.top() != pairs[c]) return false;
            st.pop();
        } else {
            st.push(c);
        }
    }
    return st.empty();
}
```

### Queue
```cpp
#include <queue>

queue<int> q;

q.push(1);
q.pop();          // void, removes front
q.front();        // peek front
q.back();         // peek back
q.empty();
q.size();
```

### Deque (Double-ended queue)
```cpp
#include <deque>

deque<int> dq;

dq.push_front(1);
dq.push_back(2);
dq.pop_front();
dq.pop_back();
dq.front();
dq.back();
dq[0];            // random access O(1)

// Sliding Window Maximum
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq;  // stores indices, values in decreasing order
    vector<int> result;
    
    for (int i = 0; i < nums.size(); i++) {
        // Remove indices outside window
        while (!dq.empty() && dq.front() < i - k + 1) dq.pop_front();
        // Remove smaller elements
        while (!dq.empty() && nums[dq.back()] < nums[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) result.push_back(nums[dq.front()]);
    }
    return result;
}
```

---

## Trees

### Node Definition
```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
```

### Traversals
```cpp
// DFS - Recursive
void preorder(TreeNode* root, vector<int>& result) {
    if (!root) return;
    result.push_back(root->val);    // Visit
    preorder(root->left, result);   // Left
    preorder(root->right, result);  // Right
}

void inorder(TreeNode* root, vector<int>& result) {
    if (!root) return;
    inorder(root->left, result);    // Left
    result.push_back(root->val);    // Visit
    inorder(root->right, result);   // Right
}

void postorder(TreeNode* root, vector<int>& result) {
    if (!root) return;
    postorder(root->left, result);  // Left
    postorder(root->right, result); // Right
    result.push_back(root->val);    // Visit
}

// DFS - Iterative (Preorder)
vector<int> preorderIterative(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    stack<TreeNode*> st;
    st.push(root);
    while (!st.empty()) {
        TreeNode* node = st.top(); st.pop();
        result.push_back(node->val);
        if (node->right) st.push(node->right);
        if (node->left) st.push(node->left);
    }
    return result;
}

// BFS - Level Order
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    if (!root) return result;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int levelSize = q.size();
        vector<int> level;
        for (int i = 0; i < levelSize; i++) {
            TreeNode* node = q.front(); q.pop();
            level.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        result.push_back(level);
    }
    return result;
}
```

### Common Operations
```cpp
// Max Depth
int maxDepth(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(maxDepth(root->left), maxDepth(root->right));
}

// Validate BST
bool isValidBST(TreeNode* root, long minVal = LONG_MIN, long maxVal = LONG_MAX) {
    if (!root) return true;
    if (root->val <= minVal || root->val >= maxVal) return false;
    return isValidBST(root->left, minVal, root->val) &&
           isValidBST(root->right, root->val, maxVal);
}

// Lowest Common Ancestor
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}
```

---

## Heaps

### Priority Queue (Max Heap by default)
```cpp
#include <queue>

// Max Heap
priority_queue<int> maxHeap;
maxHeap.push(3);
maxHeap.push(1);
maxHeap.push(2);
maxHeap.top();    // 3
maxHeap.pop();

// Min Heap
priority_queue<int, vector<int>, greater<int>> minHeap;
minHeap.push(3);
minHeap.push(1);
minHeap.push(2);
minHeap.top();    // 1

// Custom comparator (for pairs, etc.)
auto cmp = [](pair<int,int>& a, pair<int,int>& b) {
    return a.second > b.second;  // min heap by second element
};
priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> pq(cmp);

// Top K Frequent Elements
vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> freq;
    for (int n : nums) freq[n]++;
    
    // Min heap of size k
    auto cmp = [&](int a, int b) { return freq[a] > freq[b]; };
    priority_queue<int, vector<int>, decltype(cmp)> pq(cmp);
    
    for (auto& [num, count] : freq) {
        pq.push(num);
        if (pq.size() > k) pq.pop();
    }
    
    vector<int> result;
    while (!pq.empty()) {
        result.push_back(pq.top());
        pq.pop();
    }
    return result;
}
```

---

## Graphs

### Representations
```cpp
// Adjacency List
vector<vector<int>> adjList(n);  // n nodes
adjList[u].push_back(v);         // edge u -> v

// Adjacency List with weights
vector<vector<pair<int, int>>> adjList(n);
adjList[u].push_back({v, weight});

// Edge List
vector<tuple<int, int, int>> edges;  // {u, v, weight}
```

### BFS
```cpp
vector<int> bfs(vector<vector<int>>& graph, int start) {
    int n = graph.size();
    vector<int> dist(n, -1);
    queue<int> q;
    
    dist[start] = 0;
    q.push(start);
    
    while (!q.empty()) {
        int node = q.front(); q.pop();
        for (int neighbor : graph[node]) {
            if (dist[neighbor] == -1) {
                dist[neighbor] = dist[node] + 1;
                q.push(neighbor);
            }
        }
    }
    return dist;
}
```

### DFS
```cpp
void dfs(vector<vector<int>>& graph, int node, vector<bool>& visited) {
    visited[node] = true;
    for (int neighbor : graph[node]) {
        if (!visited[neighbor]) {
            dfs(graph, neighbor, visited);
        }
    }
}

// Number of Connected Components
int countComponents(int n, vector<vector<int>>& graph) {
    vector<bool> visited(n, false);
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(graph, i, visited);
            count++;
        }
    }
    return count;
}
```

### Topological Sort (Kahn's Algorithm)
```cpp
vector<int> topologicalSort(int n, vector<vector<int>>& graph) {
    vector<int> inDegree(n, 0);
    for (int u = 0; u < n; u++) {
        for (int v : graph[u]) {
            inDegree[v]++;
        }
    }
    
    queue<int> q;
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) q.push(i);
    }
    
    vector<int> order;
    while (!q.empty()) {
        int node = q.front(); q.pop();
        order.push_back(node);
        for (int neighbor : graph[node]) {
            if (--inDegree[neighbor] == 0) {
                q.push(neighbor);
            }
        }
    }
    
    return order.size() == n ? order : vector<int>();  // empty if cycle
}
```

### Dijkstra's Algorithm
```cpp
vector<int> dijkstra(vector<vector<pair<int,int>>>& graph, int start) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

### Union-Find (Disjoint Set Union)
```cpp
class UnionFind {
    vector<int> parent, rank;
public:
    UnionFind(int n) : parent(n), rank(n, 0) {
        iota(parent.begin(), parent.end(), 0);  // parent[i] = i
    }
    
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);  // path compression
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        
        // Union by rank
        if (rank[px] < rank[py]) swap(px, py);
        parent[py] = px;
        if (rank[px] == rank[py]) rank[px]++;
        return true;
    }
    
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};
```

---

## Sorting

### Quick Reference
| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable |
|-----------|-------------|------------|--------------|-------|--------|
| Bubble    | O(n)        | O(n²)      | O(n²)        | O(1)  | Yes    |
| Selection | O(n²)       | O(n²)      | O(n²)        | O(1)  | No     |
| Insertion | O(n)        | O(n²)      | O(n²)        | O(1)  | Yes    |
| Merge     | O(n log n)  | O(n log n) | O(n log n)   | O(n)  | Yes    |
| Quick     | O(n log n)  | O(n log n) | O(n²)        | O(log n) | No  |
| Heap      | O(n log n)  | O(n log n) | O(n log n)   | O(1)  | No     |

### Merge Sort
```cpp
void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    
    while (i <= mid && j <= right) {
        temp[k++] = (arr[i] <= arr[j]) ? arr[i++] : arr[j++];
    }
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    
    for (int i = 0; i < k; i++) arr[left + i] = temp[i];
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}
```

### Quick Sort
```cpp
int partition(vector<int>& arr, int left, int right) {
    int pivot = arr[right];
    int i = left - 1;
    
    for (int j = left; j < right; j++) {
        if (arr[j] < pivot) {
            swap(arr[++i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[right]);
    return i + 1;
}

void quickSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int pivot = partition(arr, left, right);
    quickSort(arr, left, pivot - 1);
    quickSort(arr, pivot + 1, right);
}
```

---

## Searching

### Binary Search
```cpp
// Standard - find exact value
int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;  // not found
}

// Lower bound - first element >= target
int lowerBound(vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] < target) left = mid + 1;
        else right = mid;
    }
    return left;
}

// Upper bound - first element > target
int upperBound(vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] <= target) left = mid + 1;
        else right = mid;
    }
    return left;
}

// STL versions
auto it = lower_bound(arr.begin(), arr.end(), target);
auto it = upper_bound(arr.begin(), arr.end(), target);
bool found = binary_search(arr.begin(), arr.end(), target);
```

### Binary Search on Answer
```cpp
// Koko Eating Bananas pattern
int minEatingSpeed(vector<int>& piles, int h) {
    int left = 1, right = *max_element(piles.begin(), piles.end());
    
    auto canFinish = [&](int speed) {
        long hours = 0;
        for (int pile : piles) {
            hours += (pile + speed - 1) / speed;  // ceiling division
        }
        return hours <= h;
    };
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (canFinish(mid)) right = mid;
        else left = mid + 1;
    }
    return left;
}
```

---

## Dynamic Programming

### 1D DP
```cpp
// Fibonacci
int fib(int n) {
    if (n <= 1) return n;
    int prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

// Climbing Stairs
int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

// House Robber
int rob(vector<int>& nums) {
    int prev2 = 0, prev1 = 0;
    for (int num : nums) {
        int curr = max(prev1, prev2 + num);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

// Coin Change
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}

// Longest Increasing Subsequence
int lengthOfLIS(vector<int>& nums) {
    vector<int> tails;
    for (int num : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), num);
        if (it == tails.end()) tails.push_back(num);
        else *it = num;
    }
    return tails.size();
}
```

### 2D DP
```cpp
// Unique Paths
int uniquePaths(int m, int n) {
    vector<vector<int>> dp(m, vector<int>(n, 1));
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i-1][j] + dp[i][j-1];
        }
    }
    return dp[m-1][n-1];
}

// Longest Common Subsequence
int longestCommonSubsequence(string& s1, string& s2) {
    int m = s1.size(), n = s2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    return dp[m][n];
}

// Edit Distance
int minDistance(string& s1, string& s2) {
    int m = s1.size(), n = s2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
            }
        }
    }
    return dp[m][n];
}
```

---

## Common Patterns

### Backtracking Template
```cpp
void backtrack(vector<vector<int>>& result, vector<int>& current, 
               vector<int>& nums, int start) {
    result.push_back(current);  // for subsets
    // if (current.size() == k) { result.push_back(current); return; }  // for combinations
    
    for (int i = start; i < nums.size(); i++) {
        // Skip duplicates if needed: if (i > start && nums[i] == nums[i-1]) continue;
        current.push_back(nums[i]);
        backtrack(result, current, nums, i + 1);  // i for combinations, i+1 for subsets
        current.pop_back();
    }
}

// Subsets
vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> current;
    backtrack(result, current, nums, 0);
    return result;
}

// Permutations
void permuteHelper(vector<vector<int>>& result, vector<int>& nums, int start) {
    if (start == nums.size()) {
        result.push_back(nums);
        return;
    }
    for (int i = start; i < nums.size(); i++) {
        swap(nums[start], nums[i]);
        permuteHelper(result, nums, start + 1);
        swap(nums[start], nums[i]);
    }
}
```

### Prefix Sum
```cpp
// Build prefix sum
vector<int> prefix(nums.size() + 1, 0);
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}

// Sum of range [l, r]
int rangeSum = prefix[r + 1] - prefix[l];
```

### Bit Manipulation
```cpp
// Check if bit is set
bool isSet = (n >> i) & 1;

// Set bit
n |= (1 << i);

// Clear bit
n &= ~(1 << i);

// Toggle bit
n ^= (1 << i);

// Count set bits
int count = __builtin_popcount(n);

// Check power of 2
bool isPowerOf2 = n > 0 && (n & (n - 1)) == 0;

// Get lowest set bit
int lowest = n & (-n);

// Iterate through all subsets of a bitmask
for (int subset = mask; subset > 0; subset = (subset - 1) & mask) {
    // process subset
}
```

