from collections import defaultdict
from copy import deepcopy

class PreProcessing:
    #Pre processing computes all nessecary stuff on the graph to ready it up for future work
    def __init__(self, graph, edge_list) -> None:
        self.CRITICAL_EDGES = self.find_critical_edges(graph, edge_list)
        
    def find_critical_edges(self, graph, edge_list):
        mandatory_edges = []
        for e in edge_list:
            edge = edge_list[e]
            tgraph = deepcopy(graph)
            del tgraph[edge[0]][edge[1]]
            del tgraph[edge[1]][edge[0]]
            if not self.check_dfs(tgraph):
                mandatory_edges.append(e)
        return mandatory_edges
            
    
    def check_dfs(self, graph: dict):
        visited = [False]*len(graph)
        stack = []
        stack.append(list(graph.keys())[0])
        visited[stack[-1]] = True
        while len(stack) > 0:
            current_node = stack[-1]
            pop = True
            for node in graph[current_node]:
                if not visited[node]:
                    visited[node] = True
                    stack.append(node)
                    pop = False
                    break
            if pop:
                stack.remove(current_node)
        for v in visited:
            if not v:
                return False
        return True

