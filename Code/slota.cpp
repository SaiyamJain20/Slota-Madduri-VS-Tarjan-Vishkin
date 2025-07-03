#include <bits/stdc++.h>
using namespace std;

#ifdef __linux__
#include <sys/resource.h>
#endif

size_t memoryUsage(const vector<vector<int>> &graph)
{
    size_t total = sizeof(graph);
    for (const auto &row : graph)
    {
        total += sizeof(row) + row.capacity() * sizeof(int);
    }
    return total;
}

bool bfsExcludingNode(const vector<vector<int>> &graph, const vector<int> &level,
                      vector<int> &visited, const vector<int> &parent, vector<bool> &done,
                      int excluded, int start, int excludedLevel, int stampID, int root = -1)
{
    if (excluded == root && graph[excluded].size() == 1)
        return false;

    queue<int> q;
    visited[start] = stampID;
    q.push(start);

    while (!q.empty())
    {
        int node = q.front();
        q.pop();
        if ((level[node] <= excludedLevel && node != excluded) || (done[node] && parent[node] == excluded))
            return true;

        for (int neighbor : graph[node])
        {
            if (neighbor != excluded && visited[neighbor] != stampID)
            {
                visited[neighbor] = stampID;
                q.push(neighbor);
            }
        }
    }

    return false;
}

bool isCycleGraph(const vector<vector<int>> &graph, int n)
{
    for (int i = 0; i < n; ++i)
    {
        if (graph[i].size() != 2)
            return false;
    }

    vector<bool> visited(n, false);
    queue<int> q;
    q.push(0);
    visited[0] = true;
    int visitedCount = 1;

    while (!q.empty())
    {
        int node = q.front();
        q.pop();
        for (int neighbor : graph[node])
        {
            if (!visited[neighbor])
            {
                visited[neighbor] = true;
                ++visitedCount;
                q.push(neighbor);
            }
        }
    }

    return visitedCount == n;
}

int main(int argc, char *argv[])
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string filename = (argc > 1) ? argv[1] : "graph.txt";
    ifstream file(filename);
    if (!file)
    {
        cerr << "Error: Cannot open file " << filename << "\n";
        return 1;
    }

    string line;
    int n = 0, m = 0;
    bool gotHeader = false;

    while (getline(file, line))
    {
        if (line.empty() || line[0] == '%')
            continue;
        if (!gotHeader)
        {
            stringstream ss(line);
            int dummy;
            ss >> n >> dummy >> m;
            gotHeader = true;
            break;
        }
    }

    vector<vector<int>> graph(n);
    int u, v;
    double val;
    while (file >> u >> v >> val)
    {
        --u;
        --v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }
    file.close();

    vector<int> parent(n, -2), level(n, -1), stamp(n, 0);
    vector<bool> visited(n, false), isArticulation(n, false);
    stack<pair<int, int>> edgeStack;
    vector<vector<int>> bccs;
    vector<bool> done(n, false);

    int stampID = 1;

    if (isCycleGraph(graph, n))
    {
        for (int i = 0; i < n; ++i)
        {
            bccs.push_back({i});
        }
        cout << n << " " << m << " " ; 
        cout << memoryUsage(graph) << "\n";
        return 0;
    }

    for (int root = 0; root < n; ++root)
    {
        if (visited[root])
            continue;

        queue<int> q;
        vector<int> component;
        q.push(root);
        visited[root] = true;
        parent[root] = -1;
        level[root] = 0;
        component.push_back(root);

        while (!q.empty())
        {
            int node = q.front();
            q.pop();
            for (int neighbor : graph[node])
            {
                if (!visited[neighbor])
                {
                    visited[neighbor] = true;
                    parent[neighbor] = node;
                    level[neighbor] = level[node] + 1;
                    q.push(neighbor);
                    component.push_back(neighbor);
                }
            }
        }

        for (int node : component)
        {
            vector<int> children;
            for (int neighbor : graph[node])
            {
                if (parent[neighbor] == node)
                    children.push_back(neighbor);
            }

            if (children.empty())
                continue;

            bool isArt = false;
            for (int child : children)
            {
                edgeStack.push({node, child});
                if (!bfsExcludingNode(graph, level, stamp, parent,done, node, child, level[node], ++stampID, root))
                {
                    isArt = true;
                    done[child] = true;
                    vector<int> currentBCC;
                    while (!edgeStack.empty())
                    {
                        auto [x, y] = edgeStack.top();
                        edgeStack.pop();
                        currentBCC.push_back(x);
                        currentBCC.push_back(y);
                        if ((x == node && y == child) || (x == child && y == node))
                            break;
                    }
                    bccs.push_back(currentBCC);
                }
            }

            if (isArt)
                isArticulation[node] = true;
        }
    }

    size_t totalMemory = memoryUsage(graph) + sizeof(parent) + parent.capacity() * sizeof(int) + sizeof(level) + level.capacity() * sizeof(int) + sizeof(stamp) + stamp.capacity() * sizeof(int) + sizeof(visited) + visited.capacity() * sizeof(bool) + sizeof(isArticulation) + isArticulation.capacity() * sizeof(bool) + memoryUsage(bccs);
    cout << n << " " << m << " " ; 
    cout << totalMemory << "\n";
    return 0;
}