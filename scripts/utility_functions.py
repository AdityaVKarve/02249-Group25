class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
    
    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def is_mst(vertex_count, graph, candidate_edges):
    # Convert the adjacency list to an edge list
    all_edges = []
    for u in graph:
        for v, weight in graph[u].items():
            if u < v:  # Avoid duplicating edges
                all_edges.append((u, v, weight))

    # Step 1: Check if candidate_edges has exactly |V| - 1 edges
    if len(candidate_edges) != vertex_count - 1:
        return False

    # Step 2: Check if candidate_edges forms a connected acyclic graph
    uf = UnionFind(vertex_count)
    for u, v, weight in candidate_edges:
        if uf.find(u) == uf.find(v):
            return False  # Cycle detected
        uf.union(u, v)

    # Step 3: Calculate the weight of candidate_edges and compare it to MST of all_edges
    candidate_weight = sum(weight for _, _, weight in candidate_edges)

    # Calculate MST weight using Kruskal's algorithm on all_edges
    sorted_edges = sorted(all_edges, key=lambda x: x[2])  # Sort edges by weight
    uf = UnionFind(vertex_count)
    mst_weight = 0
    edges_in_mst = 0
    
    for u, v, weight in sorted_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_weight += weight
            edges_in_mst += 1
            if edges_in_mst == vertex_count - 1:
                break

    return candidate_weight == mst_weight


def kruskal_mst_with_exclusions(vertex_count, graph, excluded_edges=None):
    if excluded_edges is None:
        excluded_edges = set()
    else:
        excluded_edges = set(excluded_edges)  # Convert to set for faster lookup
    # Convert the adjacency list into an edge list with IDs
    edge_id = 1
    all_edges = {}
    for u in graph:
        for v, weight in graph[u].items():
            if u < v:  # To avoid duplicate edges (u, v) and (v, u)
                all_edges[edge_id] = (u, v, weight)
                edge_id += 1

    # Sort edges by weight, excluding specified edges
    sorted_edges = sorted(
        ((eid, u, v, weight) for eid, (u, v, weight) in all_edges.items() if eid not in excluded_edges),
        key=lambda x: x[3]
    )

    # Initialize Union-Find structure
    uf = UnionFind(vertex_count)
    mst_weight = 0
    mst_edges = []

    # Build the MST using Kruskal's algorithm
    for eid, u, v, weight in sorted_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_weight += weight
            mst_edges.append(eid)
            if len(mst_edges) == vertex_count - 1:
                break
    # Ensure MST has |V| - 1 edges; if not, the graph is disconnected with exclusions
    if len(mst_edges) != vertex_count - 1:
        return -1

    # Calculate the mirror MST weight
    all_edge_ids = list(all_edges.keys())
    mirror_edges = [all_edge_ids[len(all_edge_ids) - 1 - all_edge_ids.index(eid)] for eid in mst_edges]
    mirror_weight = sum(all_edges[eid][2] for eid in mirror_edges)

    return mst_weight, mirror_weight


def calculate_mirror_weight(mst_edges, all_edges):
    # Find the mirror edges
    all_edge_ids = list(all_edges.keys())
    mirror_edges = [all_edge_ids[len(all_edge_ids) - 1 - all_edge_ids.index(eid)] for eid in mst_edges]

    # Calculate mirror MST weight
    mirror_weight = sum(all_edges[eid][2] for eid in mirror_edges)
    return mirror_weight