#include<iostream>
#include<vector>
#include<unordered_set>
#include<utility>
#include<queue>
#include<climits>


using namespace std;

class Graph {
    private:
        vector<pair<int, vector<int>>> adjList;
    public:

        Graph(bool directed = false) {
            for (auto vertex: adjList) {
                int u = vertex.first;
                vector<int> neighbors = vertex.second;
                for (int v : neighbors) {
                    addEdge(u, v, directed);
                }
            }
        }

        vector<pair<int, vector<int>>>& getAdjList() {
            return adjList;
        }

        void addEdge(int u, int v, bool directed = false) {
            adjList[u].second.push_back(v);
            if (!directed) {
                adjList[v].second.push_back(u);
            }
        }

        void printGraph() {
            for (auto vertex: adjList) {
                cout << vertex.first << " -> ";
                for (int neighbor: vertex.second) {
                    cout << neighbor << " ";
                }
                cout << endl;
            }
        }

        void bfs() {
            // breadth first search
        }

        void bft() {
            // breadth first tree
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
        {2, {1, 5, 3, 4}},
        {3, {2, 5, 4}},
        {4, {2, 1}},
        {5, {1, 2, 3}}
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

    WeightedGraph wg(acylic_weighted_graph, 4,  true);
    cout << "Created wg" << endl;
    cout << "dijikstra sd b/w 1 & 3 ' " << wg.dijkstra(1, 3) << endl;


    return 0;
}