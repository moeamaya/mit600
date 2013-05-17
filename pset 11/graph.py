## 6.00 Problem Set 11
## GRAPH

import random
from collections import deque
#-----------------------------------------------------------------------
#
# Problem Set 11
#
# Graph code
#
###

class Node(object):
    """Represents a node in the graph with a name."""

    def __init__(self, name):
        """Initializes a Node with input name converted to string."""
        self.name = str(name)
        
    def getName(self):
        """Returns name of the node"""
        return self.name
    
    def __repr__(self):
        """Returns the node name as the string representation of the node."""
        return self.name
    
    def __eq__(self, other):
        """Specifies that two nodes are equal if they have the same name."""
        return self.name == other.getName()
    
    def __hash__(self):
        """Sets the hash value of the node."""
        return hash(self.name)


class Edge(object):
    """Represents an unweighted directed edge from a source node to a
    destination node"""
    
    def __init__(self, src, dest):
        """Initializes a edge from the specified source node to the speficied
        destination node."""
        self.src = src
        self.dest = dest
        
    def getSource(self):
        """Returns the source node of the edge."""
        return self.src
    
    def getDestination(self):
        """Returns the desination node of the edge."""
        return self.dest
    
    def __eq__(self, other):
        """Speficies that two edges are equal if they have the same source and
        destination nodes"""
        return self.src == other.getSource() and self.dest == other.getDestination()

    def __repr__(self):
        """Returns a string representation of the edge."""
        return str(self.src) + '->' + str(self.dest)


class Digraph(object):
    """Represents a directed graph."""
    
    def __init__(self):
        """Initializes a graph with no node or edge."""
        self.nodes = set()
        self.edges = {}

    def addNode(self, node):
        """
        Adds the specified node to the graph.
        Raises a ValueError exception if the node already exists in the graph.
        """
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
            
    def addEdge(self, edge):
        """
        Adds the specified edge to the graph.
        Raises a ValueError exception if the source or destination node of the
        edge are not in the graph.
        """
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            print src, dest
            raise ValueError('Node not in graph')
        self.edges[src].append(edge)

    def getNodes(self):
        """Returns a set containing all the nodes in the graph."""
        return self.nodes.copy()
    
    def numNodes(self):
        """Returns an integer representing the number of nodes in the graph."""
        return len(self.nodes)
    
    def childrenOf(self, node):
        """Returns a list containing all the child nodes of the node."""
        result = []
        for e in self.edges[node]:
            if not e.getDestination() in result:
                result.append(e.getDestination())
        return result
    
    def edgesOf(self, node):
        """
        Returns a list of all the edges in the graph that leaves the specified
        node (i.e. the edges in the graph that have the specified node as the
        source node).
        """
        result = []
        for e in self.edges[node]:
            result.append(e)
        return result
    
    def hasNode(self, node):
        """
        Returns whether the graph contains the speficied node. 
        """
        return node in self.nodes
    
    def __repr__(self):
        """Returns a string representation of the graph."""
        res = ''
        for k in self.edges:
            for e in self.edges[k]:
                res = res + str(e) + '\n'
        return res[:-1]


class Graph(Digraph):
    """
    Represents an undirected graph.
    If an edge A--B is added to the graph, then node A is a child of node B, and
    node B is also a child of node A. 
    """
    
    def addEdge(self, edge):
        """Adds an edge to the undirected graph."""
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


class Path(object):
    """ Represents a series of connected directed edges from a start node to an
    end node."""
    
    def __init__(self, start):
        """Intializes a path with the specified start node."""
        assert type(start) == Node
        self.val = [start]
        
    def addStep(self, edge):
        """
        Adds the specified edge to the end of the path as a continutation of the
        path. Raises a ValueError exception if the source node of the specified
        edge is not the same as the node at the end of the path instance. 
        """
        if self.val[-1] != edge.getSource():
            raise ValueError('Not a continuation of path')
        self.val.append(edge.getDestination())
        
    def getStart(self):
        """Returns the start node of the path."""
        return self.val[0]
    
    def getLength(self):
        """Returns the length of the path, i.e. the number of edges in the path
        """
        return len(self.val) - 1
    
    def __add__(self, edge):
        """Returns a new copy of the path instance with the specified edge added
        to it. Does not mutate the path instance.
        """
        result = Path(self.getStart())
        for elem in self.val[1:]:
            result.val.append(elem)
        result.val.append(edge.getDestination())
        return result
    
    def contains(self, node):
        """Returns whether the specified node exists in the path."""
        for step in self.val:
            if step == node:
                return True
        return False
    
    def __repr__(self):
        """Returns a string representation of the path."""
        result = ''
        for step in self.val:
            result = result + '->' + str(step)
        return result[2:]


def BFS(graph, source, destination):
    """
    An iterative implementation of breadth-first search starting from the
    source node. Returns a path from the source to the destination if the
    destination is found in the graph, None otherwise.

    Parameters:
    graph - a Graph instance
    source - a Node instance
    destination - a Node instance

    Returns: a Path instance from source to destination, or None if no path
    is found
    """
    queue = deque([source])
    previous = {source: None} # dict to keep track of previous nodes on path
    while len(queue) > 0:
        node = queue.popleft()
        if node == destination: # destination found
            return findPath(previous, node)
        for childNode in graph.childrenOf(node): 
            if not childNode in previous:
                previous[childNode] = node
                queue.append(childNode) # append children at the end
    return None 


def DFS(graph, source, destination):
    """
    A recursive implementation of depth-first search starting from the source
    node. Returns a path from the source to the destiation if the destination
    is found in the graph, None otherwise.

    Parameters:
    graph - a Graph instance
    source - a Node instance
    destination - a Node instance

    Returns: a Path instance from source to destination, or None if no path
    is found
    """
    previous = {source: None} # dict to keep track of previous nodes on path
    if recursiveDFS(graph, source, destination, previous):
        return findPath(previous, destination)
    else:
        return None

def recursiveDFS(graph, node, destination, previous):
    """Helper function for the DFS implementation."""
    if node == destination: # base case
        return True
    for childNode in graph.childrenOf(node):
        if not childNode in previous:
            previous[childNode] = node
            # recursive case: look through all the children depth first
            if recursiveDFS(graph, childNode, destination, previous):
                return True
    return False


def findPath(previous, node):
    """
    Helper function to build a path from the source to the specified node. Takes
    in a dictionary called previous that maps a node to the node that was
    visited before it (i.e. its parent) during the search.

    Parameters:
    previous - dictionary with nodes as keys and their previous nodes as values.
        (Ex: previous[b] = a means that node a was visited right before node b
        in the path)
    node - node at the end of the path, i.e. the destination

    Returns: a Path instance from the source to the node
    """
    edges = []
    while previous.get(node) != None:
        previousNode = previous[node]
        edge = Edge(previousNode, node)
        edges.append(edge)
        node = previousNode
    if len(edges) == 0:
        return Path(node)
    edges.reverse()
    path = Path(edges[0].getSource())
    for edge in edges:
        path.addStep(edge)
    return path
