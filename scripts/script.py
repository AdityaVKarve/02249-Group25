import time
import random
from utility_functions import is_mst, kruskal_mst_with_exclusions, calculate_mirror_weight
from pre_processing import PreProcessing
from copy import deepcopy
from tqdm import tqdm

class Assignment:
    def __init__(self, graph:str) -> None:
        self.GRAPH_PATH = "../graphs/"+graph+".uwg"
        self.initialise_graph()
        self.PRE_PROCESSED_OBJECTS = PreProcessing(self.GRAPH, self.EDGE_LIST)
        self.CURRENT_B = None
        self.CURRENT_B = max(kruskal_mst_with_exclusions(self.VERTICE_COUNT,self.GRAPH))
        print("Current B:{}".format(self.CURRENT_B))
        self.run()
    
    def initialise_graph(self):
        '''
        This method produces 2 things:
        1. The graph. The structure is {vertex a:{vertex b:weight}, vertex b:{vertex a:weight}}
        2. A list of edges: {1. (vertex a, vertex b, weight)}
        '''
        with open(self.GRAPH_PATH, 'r') as file:
            raw_data = file.read()
        lines = raw_data.split('\n')
        
        #Get vertice and edge count
        self.VERTICE_COUNT = int(lines[0])
        self.EDGE_COUNT = int(lines[1])
        self.SPANNING_TREE_SIZE = self.VERTICE_COUNT - 1
        #Get adjacency matrix
        self.GRAPH = {}
        self.EDGE_LIST = {}
        self.EDGES = {}
        for lineno in range(2,len(lines)-1):
            line = lines[lineno].split(' ')
            vertex_a = int(line[0]) - 1
            vertex_b = int(line[1]) - 1
            weight = int(line[2])
            if vertex_a not in self.GRAPH:
                self.GRAPH[vertex_a] = {}
            if vertex_b not in self.GRAPH:
                self.GRAPH[vertex_b] = {}
                
            self.GRAPH[vertex_a][vertex_b] = weight
            self.GRAPH[vertex_b][vertex_a] = weight
            self.EDGE_LIST[lineno - 2] = ((vertex_a, vertex_b, weight))

    def check_solution(self, R:list):
        #Check if solution is a spanning tree
        removed_edges = []
        tgraph = deepcopy(self.GRAPH)
        for i in range(len(R)):
            if R[i] == 1:
                removed_edge = self.EDGE_LIST[i]
                del tgraph[removed_edge[0]][removed_edge[1]]
                del tgraph[removed_edge[1]][removed_edge[0]]
                
        try:
            new_b = max(kruskal_mst_with_exclusions(self.VERTICE_COUNT,tgraph))
            if new_b < self.CURRENT_B:
                print("Lower B found, B:{}".format(new_b))
                self.CURRENT_B = new_b
        except Exception as e:
            pass
        
    
    def generate_r(self, num_edges, tree_size, mandatory_indices):
        # Initialize array with all 0s
        k = random.randint(1,num_edges - tree_size)
        binary_array = [0] * num_edges
        
        # Ensure indices in zero_indices are 0
        mandatory_indices = set(mandatory_indices)
        
        # List of available indices where 1s can be placed
        available_indices = [i for i in range(num_edges) if i not in mandatory_indices]
        
        # Check if k is feasible with the available indices
        if k > len(available_indices):
            raise ValueError("Not enough available indices to place all 1s.")

        # Randomly select k indices from the available_indices
        one_indices = random.sample(available_indices, k)
        # Set the selected indices to 1
        for i in one_indices:
            binary_array[i] = 1
        return binary_array 
    
    def run(self):
        start = time.time()
        while time.time() - start < 600:
            R = self.generate_r(self.EDGE_COUNT, self.VERTICE_COUNT - 1, self.PRE_PROCESSED_OBJECTS.CRITICAL_EDGES)
            self.check_solution(R)
        
        end = time.time()
        print("Time taken:{}".format(end - start))    
        
a = Assignment('test01')
