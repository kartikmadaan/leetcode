#include<algorithm>
#include<iostream>
#include<vector>
#include<unordered_set>
#include<utility>
#include<queue>
#include<climits>
#include<stack>


using namespace std;

class Graph {
    private:
        vector<vector<int>> adjList;
        vector<int> parent;
        vector<pair<int,int>> timeInOut;
    public:

        Graph(vector<pair<int, vector<int>>> edgeList, int vertices, bool directed = false) {
            adjList.resize(vertices);
            parent.resize(vertices);
            for (int i = 0; i < edgeList.size(); i++) {
                cout << "i: " << i;
                int u = edgeList[i].first;
                cout << " u: " << u;
                for (int v : edgeList[i].second) {
                    cout << " v: " << v << endl;
                    addEdge(u, v, directed);
                }
            }
        }

        vector<vector<int>>& getAdjList() {
            return adjList;
        }

        void addEdge(int u, int v, bool directed = false) {
            adjList[u].push_back(v);
            if (!directed) {
                adjList[v].push_back(u);
            }
        }

        void printGraph() {
            for (int i = 0; i < adjList.size(); i++) {
                cout << i << " -> ";
                for (int neighbor : adjList[i]) {
                    cout << neighbor << ", ";
                }
                cout << endl;
            }
        }

        void bfs(int start) {
            queue<int> q;
            unordered_set<int> visited;
            parent[start] = -1;
            visited.insert(start);
            q.push(start);
            while (!q.empty()) {
                int front = q.front();
                q.pop();
                for (auto neighbor : adjList[front]) {
                    if (visited.find(neighbor) == visited.end()) {
                        visited.insert(neighbor);
                        parent[neighbor] = front;
                        cout << "Parent of " << neighbor << " = " << front << endl;
                        q.push(neighbor);
                    }
                }
            }
            cout << "Visited all " << visited.size() << " vertices in BFS" << endl;
        }

        void bft() {
            
        }
        
        void dfs(int start) {
            // stack<int> only for active vertices; next[u] is how far we scanned adj[u]
            // (same DFS tree as recursive: finish one branch before the next neighbor).
            unordered_set<int> visited;
            stack<int> st;
            st.push(start);
            visited.insert(start);
            while (!st.empty()) {
                int u = st.top();
                st.pop();

                for (auto it = adjList[u].rbegin(); it != adjList[u].rend(); it++) {
                    int neighbor = *it;
                    if (visited.find(neighbor) == visited.end()) {
                        visited.insert(neighbor);
                        parent[neighbor] = u;
                        st.push(neighbor);
                        cout << "parent of " << neighbor << " = " << u << endl;
                    }
                }
            }
            cout << "Visited all " << visited.size() << " vertices in DFS" << endl;
        }
};

class WeightedGraph{
    private:
        vector<pair<int, vector<pair<int,int>>>> weightedAdjList;
    public:
        WeightedGraph(vector<pair<int, pair<int,int>>> &weightedAdjList, int vertices, bool directed = false) {
            this->weightedAdjList.resize(vertices + 1);
            for (auto vertex: weightedAdjList) {
                int u = vertex.first;
                int v = vertex.second.first;
                int wt = vertex.second.second;
                //cout << "u: " << u << " v: " << v << endl;
                if (directed)
                    addWeightedEdge(v, u, wt);
                addWeightedEdge(u, v, wt, directed);
            }
        }

        void addWeightedEdge(int u, int v, int weight, bool directed = false) {
            this->weightedAdjList[u].second.push_back({v,weight});
        }

        int dijkstra(int start, int end) {
            cout << "Starting Dijkstra" << endl;
            vector<int> distance(weightedAdjList.size(), INT_MAX);
            unordered_set<int> visited;
            priority_queue<int> q;
            q.push(start);
            distance[start] = 0;
            while(!q.empty()) {
                int front = q.top();
                if (front == end)
                    return distance[end];
                q.pop();
                if (visited.find(front) != visited.end()){
                    cout << "Skipping " << front << " from visiting again" << endl;
                    continue;
                }

                for (auto weightedNeighbor : weightedAdjList[front].second) {
                    if (distance[weightedNeighbor.first] > distance[front] + weightedNeighbor.second){
                        // scope to add parent too
                        distance[weightedNeighbor.first] = distance[front] + weightedNeighbor.second;
                    }
                    q.push(weightedNeighbor.first);
                    cout << "pushed " << weightedNeighbor.first << "onto PQ" << endl;
                }
                visited.insert(front);
            }

            for (size_t i = 0; i < distance.size(); i++) {
                cout << distance[i] << " ";
            }
            cout << endl;
            return distance[end];
        }
};

int main() {
    cout << "In main" << endl;
    vector<pair<int, vector<int>>> undirected_graph = {
        {1, {5, 2, 4}},
        {2, { 5, 3, 4}},
        {3, {5}},
        {4, {}},
        {5, {}}
    };
    /*
    1 -> 5, 2, 4 
    2 -> 1, 5, 3, 4
    3 -> 2, 5, 4
    4 -> 2, 1
    5 -> 1, 2, 3
    */

    vector<pair<int, vector<int>>> directed_graph = {
        {1, {2, 6}},
        {2, {4}},
        {3, {}},
        {4, {5}},
        {5, {}},
        {6, {}}
    };
    /*
    1 -> 2, 6
    2 -> 4
    3 -> 
    4 -> 5
    5 -> 
    6 ->
    */

    vector<pair<int, pair<int,int>>> cyclic_weighted_graph = {
        {1, {2, 3}},
        {2, {3, 6}},
        {2, {4, 7}},
        {2, {5, 3}},
        {4, {1, 10}},
        {4, {3, 2}},
        {4, {5, 1}},
        {5, {3, 4}}
    };
    /*
    1 -> 2 = 3
    2 -> 3 = 6
    2 -> 4 = 7
    2 -> 5 = 3
    4 -> 1 = 10
    4 -> 3 = 2
    4 -> 5 = 1
    5 -> 3 = 4
    */

    vector<pair<int, pair<int,int>>> acylic_weighted_graph = {
        {1, {2, 2}},
        {2, {4, 1}},
        {2, {3, 5}},
        {4, {3, 1}}
    };
    /*
    1 -> 2 = 2
    2 -> 3 = 5
    2 -> 4 = 1
    4 -> 3 = 1
    */

    vector<pair<int, vector<int>>> directed_acyclic_graph = {
        {1, {2, 4}},
        {3, {2}},
        {4, {2, 5}},
        {5, {2}}
    };
    /*
    1 -> 2
    1 -> 4
    3 -> 2
    4 -> 2
    4 -> 5
    5 -> 2
    */

    // WeightedGraph wg(acylic_weighted_graph, 4,  true);
    // cout << "Created wg" << endl;
    // cout << "dijikstra sd b/w 1 & 3 ' " << wg.dijkstra(1, 3) << endl;

    Graph undirectedGraph(undirected_graph, 6, false);
    undirectedGraph.printGraph();
    undirectedGraph.bfs(1);
    undirectedGraph.dfs(1);

    return 0;
}