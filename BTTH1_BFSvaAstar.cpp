#include <bits/stdc++.h>
using namespace std;

struct Node {
    int vertex;
    int distance;
    int heuristic;
    bool operator<(const Node& other) const {
        return distance + heuristic > other.distance + other.heuristic;
    }
};

vector<int> G[10000];
vector<int> H; // Heuristic values

int main() {
    int n;
    cout << "Nhap so dinh: ";
    cin >> n;
    int edges;
    cout << "Nhap so canh: ";
    cin >> edges;
    cout << "Nhap vao danh sach cac canh:" << endl;
    while (edges--) {
        int x, y;
        cin >> x >> y;
        G[x].push_back(y);
        G[y].push_back(x);
    }

    int choice;
    cout << "Chon thuat toan tim kiem (1 - BFS, 2 - A*): ";
    cin >> choice;

    if (choice == 1) {
        // Implement BFS
        int visited[n] = {0};
        int d[n], p[n];
        int s = 0;
        visited[s] = 1;
        d[s] = 0;
        p[s] = -1;
        queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : G[v]) {
                if (!visited[u]) {
                    visited[u] = 1;
                    q.push(u);
                    d[u] = d[v] + 1;
                    p[u] = v;
                }
            }
        }

        for (int i = 0; i < n; i++) {
            cout << d[i] << " ";
        }
        cout << endl;

        int dest = 5;
        vector<int> path;

        if (visited[dest] == 0) {
            cout << "NO path" << endl;
        } else {
            int x = dest;
            while (x != -1) {
                path.push_back(x);
                x = p[x];
            }

            reverse(path.begin(), path.end());
        }
        for (int i = 0; i < path.size(); i++) {
            cout << path[i] << " ";
        }
        cout << endl;

    } else if (choice == 2) {
        // Nhap gia tri heuristic chi khi chon A*
        H.resize(n); // Resize heuristic vector
        cout << "Nhap gia tri heuristic cho tung dinh:" << endl;
        for (int i = 0; i < n; ++i) {
            cin >> H[i];
        }

        // Implement A* Algorithm
        priority_queue<Node> pq;
        vector<int> d(n, INT_MAX);
        vector<int> p(n, -1);
        int s = 0;
        pq.push({s, 0, H[s]});
        d[s] = 0;

        while (!pq.empty()) {
            int v = pq.top().vertex;
            pq.pop();

            for (int u : G[v]) {
                int cost = 1; // Assuming all edges have the same cost
                if (d[v] + cost < d[u]) {
                    d[u] = d[v] + cost;
                    p[u] = v;
                    pq.push({u, d[u], H[u]});
                }
            }
        }

        for (int i = 0; i < n; i++) {
            cout << d[i] << " ";
        }
        cout << endl;

        int dest = 5;
        vector<int> path;

        if (d[dest] == INT_MAX) {
            cout << "NO path" << endl;
        } else {
            int x = dest;
            while (x != -1) {
                path.push_back(x);
                x = p[x];
            }

            reverse(path.begin(), path.end());
        }
        for (int i = 0; i < path.size(); i++) {
            cout << path[i] << " ";
        }
        cout << endl;
    } else {
        cout << "Invalid choice!" << endl;
    }
}
