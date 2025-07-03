#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <fstream>
#include <map>
#ifdef __linux__
#include <sys/resource.h>
#endif
using namespace std;

struct NodeInfo {
    int pre = 0, low = 0, high = 0, nd = 0, parent = -1;
};

struct DSU {
    vector<int> par;
    DSU(int n) : par(n) {
        for (int i = 0; i < n; ++i) par[i] = i;
    }
    int find(int x) {
        return (par[x] == x) ? x : (par[x] = find(par[x]));
    }
    void unite(int a, int b) {
        par[find(a)] = find(b);
    }
};

// Memory calculation helper
size_t calculateVectorMemory(const vector<vector<int>> &vec) {
    size_t memory = sizeof(vec);
    for (const auto &inner : vec)
        memory += sizeof(inner) + inner.capacity() * sizeof(int);
    return memory;
}

int n, m, timer = 0;
vector<vector<int>> g, tree;
vector<pair<int, int>> edges, backEdges;
vector<NodeInfo> info;
vector<int> mark;
int markId = 0;
map<pair<int, int>, int> edgeIndex;

void dfs(int start) {
    struct Frame {
        int v, p;
        size_t idx;
        bool resumed;
    };

    vector<Frame> stack;
    stack.push_back({start, -1, 0, false});

    while (!stack.empty()) {
        Frame &frame = stack.back();
        int v = frame.v;
        int p = frame.p;

        if (!frame.resumed) {
            info[v].pre = ++timer;
            info[v].nd = 1;
            info[v].parent = p;
            info[v].low = info[v].high = info[v].pre;
            frame.resumed = true;
        }

        bool advanced = false;
        while (frame.idx < g[v].size()) {
            int u = g[v][frame.idx++];
            if (u == p) continue;
            if (info[u].pre) {
                if (info[u].pre < info[v].pre)
                    backEdges.emplace_back(v, u);
                info[v].low = min(info[v].low, info[u].pre);
                info[v].high = max(info[v].high, info[u].pre);
            } else {
                tree[v].push_back(u);
                stack.push_back({u, v, 0, false});
                advanced = true;
                break;
            }
        }

        if (!advanced) {
            for (int u : tree[v]) {
                info[v].nd += info[u].nd;
                info[v].low = min(info[v].low, info[u].low);
                info[v].high = max(info[v].high, info[u].high);
            }
            stack.pop_back();
        }
    }
}

vector<vector<int>> computeBiconnectedComponents() {
    dfs(1);

    int numEdges = edges.size();
    DSU dsu(numEdges);

    // Case (i): back edges
    for (auto [v, u] : backEdges) {
        if (info[v].pre < info[u].pre) swap(v, u);
        int idx = edgeIndex[{v, u}];
        dsu.unite(idx, idx);  // trivial self-union but keeps consistency
    }

    // Case (ii) and (iii)
    for (int v = 1; v <= n; ++v) {
        for (int w : tree[v]) {
            int edgeVw = edgeIndex[{v, w}];
            int parentEdgeV = (info[v].parent != -1) ? edgeIndex[{info[v].parent, v}] : edgeVw;

            // Case (iii)
            if (info[w].low < info[v].pre || info[w].high >= info[v].pre + info[v].nd)
                dsu.unite(edgeVw, parentEdgeV);

            // Case (ii)
            for (int u : g[w]) {
                if (u == v || info[u].pre == 0) continue;
                bool unrelated1 = info[u].pre < info[v].pre || info[u].pre > info[v].pre + info[v].nd - 1;
                bool unrelated2 = info[w].pre < info[u].pre || info[w].pre > info[u].pre + info[u].nd - 1;
                if (unrelated1 && unrelated2)
                    dsu.unite(parentEdgeV, edgeIndex[{w, u}]);
            }
        }
    }

    vector<vector<int>> blocks(numEdges);
    for (int i = 0; i < numEdges; ++i) {
        int comp = dsu.find(i);
        blocks[comp].push_back(edges[i].first);
        blocks[comp].push_back(edges[i].second);
    }

    vector<vector<int>> bcc(numEdges);
    mark.assign(n + 1, -1);
    for (int i = 0; i < numEdges; ++i) {
        if (blocks[i].empty()) continue;
        ++markId;
        for (int v : blocks[i]) {
            if (mark[v] != markId) {
                bcc[i].push_back(v);
                mark[v] = markId;
            }
        }
    }
    return bcc;
}

int main(int argc, char *argv[]) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input_file = "graph.txt";
    if (argc > 1) input_file = argv[1];
    ifstream fin(input_file);
    if (!fin) {
        cerr << "Error: could not open " << input_file << endl;
        return 1;
    }

    string line;
    bool dimensions_read = false;
    while (getline(fin, line)) {
        if (line.empty() || line[0] == '%') continue;
        if (!dimensions_read) {
            stringstream ss(line);
            int rows, cols, nnz;
            ss >> rows >> cols >> nnz;
            n = rows;
            m = nnz;
            dimensions_read = true;
            break;
        }
    }

    g.resize(n + 1);
    tree.resize(n + 1);
    info.resize(n + 1);

    int edgeCounter = 0;
    int u, v;
    float val;
    while (fin >> u >> v >> val) {
        if (u == v) continue;
        g[u].push_back(v);
        g[v].push_back(u);
        edges.emplace_back(u, v);
        edgeIndex[{u, v}] = edgeCounter;
        edgeIndex[{v, u}] = edgeCounter;
        ++edgeCounter;
    }
    fin.close();

    auto bcc = computeBiconnectedComponents();

    // Add bcc printing
    // for (const auto &component : bcc) {
    //    if (component.empty()) continue;
    //    for (int node : component) {
    //        cout << node << ' ';
    //    }
    //    cout << '\n';
    //}

    size_t g_memory = calculateVectorMemory(g);
    size_t tree_memory = calculateVectorMemory(tree);
    size_t bcc_memory = calculateVectorMemory(bcc);
    size_t total_memory = g_memory + tree_memory + bcc_memory;

    cout << n << ' ' << m << ' ' << total_memory << '\n';
    return 0;
}
