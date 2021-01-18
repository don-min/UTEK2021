# Q2 
# imports
import json
import math

class Graph:
    '''
    Graphs Object Class
    @param self.graph_dict: dict
    @param self.directed: bool
    '''
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        '''
        Create an undirected graph
        @param self: Graph
        '''
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    
    def connect(self, A, B, distance=1):
        '''
        Given the distance, connect the nodes A and B
        If undirected, add the inverse link between A and B
        @param self: Graph
        '''
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance
   
    def get(self, a, b=None):
        '''
        Gets neighbours of the node
        @param self: Graph
        '''
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        '''
        Return a list of nodes in the graph
        @param self: Graph
        '''
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
 

class Node:
    '''
    A node class for the station
    @param self.name: str
    @param self.parent: str
    '''  
    
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to the start node (point)
        self.h = 0 # Distance to the end node (point)
        self.f = 0 # Total cost
    
    def __eq__(self, other):
        '''
        Compare nodes
        @param self: Node
        '''
        return self.name == other.name

    def __lt__(self, other):
        '''
        Sort nodes
        @param self: Node
        '''
        return self.f < other.f

    def __repr__(self):
        '''
        Print nodes
        @param self: Node
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

# A* search
def astar_search(graph, heuristics, start, end):
    '''
    Returns the shortest path and its distance from the startpoint to the endpoint
    '''
    open = [] # open nodes list
    closed = [] # closed nodes list

    start_node = Node(start, None) # start node (startpoint)
    goal_node = Node(end, None) # end node (endpoint)

    open.append(start_node) # append the start node
    
    # Loop until there are no other nodes in the open list
    while len(open) > 0:

        open.sort() # sort to determine the closest node
        
        current_node = open.pop(0) # node with the shortest distance
        
        closed.append(current_node) # append to the closed list
        
        # if reached the end node, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))

            return path[::-1] # reversed path
            
        # Get neighbours
        neighbors = graph.get(current_node.name)

        # Looping neighbors
        for key, value in neighbors.items():
            
            neighbor = Node(key, current_node) # Create a neighbor node
            
            # if the neighbor is in the closed list, just continue
            if(neighbor in closed): 
                continue

            # Calculate the full distance
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            
            # Check if neighbor is in the open list and has a lower total cost
            if(add_to_open(open, neighbor) == True):
                open.append(neighbor)
    
    return None # no path found

# Check if a neighbor should be added to the open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

def cartesian_distance(x_1,y_1,x_2,y_2):
  return math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)

def calc_heuristic(filename, startpoint, endpoint):
  
  coordinates = {}
  data = read_file(filename)["Nodes"]
  for i in data:
    coordinates.update({i["Name"]:i["Coordinates"]})
  
  heuristics = {}
  for key, value in coordinates.items():
    approx = cartesian_distance(value[0],value[1],coordinates[endpoint][0],coordinates[endpoint][1])
    heuristics.update({key:approx})
  
  return heuristics

def conditions(filename1, filename2):
  graph = makegraph(filename2)  #making the graph
  ofile = open("2.out","w")  #output file

  myfile = open(filename1, "r")
  lines = myfile.readlines()
  lst = [line.rstrip("\n") for line in lines]
  output = [element.split(',') for element in lst]
  for i in output:
    estimate = calc_heuristic(filename2, i[0], i[1])
    path = astar_search(graph, estimate, i[0], i[1]) #gives in form ['location:distance', etc...]
    stops = [location.split(': ') for location in path]
    #splits into [['location','distance'],etc...]
    for j in stops:
      ofile.write(j[0]+", ") #writes all the locations
    ofile.write(stops[-1][1]+"\n") #writes the total distance

  
# Driver Code
if __name__ == "__main__":
  conditions("2.in", "2.json")
