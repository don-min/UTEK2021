import json

class Graph:
    '''
    A graph class for the entire TTC map
    '''
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        '''
        create an undirected graph
        '''
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        '''
        Given the distance, connect the node A and B
        If undirected, add the inverse link between A and B
        '''
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    def get(self, a, b=None):
        '''
        get neighbours of the node
        '''
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        '''
        return a list of nodes in the graph
        '''
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

        
class Node:
    '''
    A node class for the station
    '''  
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to the start node (point)
        self.h = 0 # Distance to the end node (point)
        self.f = 0 # Total cost

    def __eq__(self, other):
        '''
        compare nodes
        '''
        return self.name == other.name

    def __lt__(self, other):
        '''
        sort nodes
        '''
        return self.f < other.f

    def __repr__(self):
        '''
        print nodes
        '''
        return ('({0},{1})'.format(self.name, self.f))

def read_file(filename):
    '''
    Reads .json file and returns contents
    @param myParam1: str
    @return: dict
    '''
    with open(filename, "r") as myfile:
        content = json.load(myfile)
    return content  
    
def makegraph(filename):
    '''
    Creates graph structure and defines nodes from .json file
    @param myParam1: str
    @return: Graph
    '''
    content = read_file(filename)
    graph = Graph()
    node_dict = {}
    [val_list] = content.values()
    for i in range(0, len(val_list)):
        node_dict[val_list[i]["Name"]] = val_list[i]["Neighbours"]

    for each_node in node_dict:
        for each_neighbour in node_dict[each_node]:
            graph.connect(each_node, each_neighbour["Name"], each_neighbour["Distance"])
    
    graph.make_undirected()
    
    return graph
class Graph:
    '''
    A graph class for the entire TTC map
    '''
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        '''
        create an undirected graph
        '''
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        '''
        Given the distance, connect the node A and B
        If undirected, add the inverse link between A and B
        '''
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    def get(self, a, b=None):
        '''
        get neighbours of the node
        '''
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        '''
        return a list of nodes in the graph
        '''
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

        
class Node:
    '''
    A node class for the station
    '''  
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to the start node (point)
        self.h = 0 # Distance to the end node (point)
        self.f = 0 # Total cost

    def __eq__(self, other):
        '''
        compare nodes
        '''
        return self.name == other.name

    def __lt__(self, other):
        '''
        sort nodes
        '''
        return self.f < other.f

    def __repr__(self):
        '''
        print nodes
        '''
        return ('({0},{1})'.format(self.name, self.f))

def read_file(filename):
    '''
    Reads .json file and returns contents
    @param myParam1: str
    @return: dict
    '''
    with open(filename, "r") as myfile:
        content = json.load(myfile)
    return content  
    
def makegraph(filename):
    '''
    Creates graph structure and defines nodes from .json file
    @param myParam1: str
    @return: Graph
    '''
    content = read_file(filename)
    graph = Graph()
    node_dict = {}
    [val_list] = content.values()
    for i in range(0, len(val_list)):
        node_dict[val_list[i]["Name"]] = val_list[i]["Neighbours"]

    for each_node in node_dict:
        for each_neighbour in node_dict[each_node]:
            graph.connect(each_node, each_neighbour["Name"], each_neighbour["Distance"])
    
    graph.make_undirected()
    
    return graph
