########################
# Problem Set 11: The 6.00 Social Network
# Name: Jorge Amaya
# Collaborators: none
# Time: 6:00
#

from graph import *

#
# PROBLEM 1a
#
def buildFBGraph(filename):
    """
    Reads the contents of the given file. Assumes the file contents contain
    data in the form of space-separated x y pairs of itegers. Each x y pair is
    unique and represents a pair of friends on facebook.
    
    There are 120 students in 6.00, and they are represented as integers from 0
    to 119. If a student does not have any Facebook friend in the class, her
    number will not appear in the file, but the graph returned by this function
    will include her.
    
    Parameters:
    filename - the name of the data file as a string. 

    Returns:
    a Graph structure representing the Facebook network of the 6.00 students as
    encoded in the data file, including students who are not connected to any
    other students in the class
    """
    pairs = []
    txtFile = open(filename)
    for line in txtFile:
        words = line.split()
        student0 = int(words[0])
        student1 = int(words[1])
        pairs.append([student0,student1])
    txtFile.close()
    
    nodeIndex = range(120)
    nodes = []
    for i in nodeIndex:
        nodes.append(Node(str(i)))
        
    g = Graph()
    for n in nodes:
        g.addNode(n)

    for each in pairs:
        g.addEdge(Edge(nodes[each[0]], nodes[each[1]]))

    return g

##graph = buildFBGraph('FBFriends.txt')
    
#
# PROBLEM 1b
#

def degOfSeparation(graph, student1, student2):
    """
    Takes in a graph respresenting a Facebook network of the 6.00 students and
    returns the degree of separation between two students. Returns -1 if the two
    students are not connected.

    Parameters:
    graph - a Graph structure representing a Facebook network.
    student1 - integer reprsenting student1
    student2 - integer represnting student2

    Returns: an integer representing the degree of separation between student1
    and student2, i.e. how many steps away in the friendship chain student1 is
    from student2. If student1 and student2 are not connected, returns -1.
    """
    std1 = Node(str(student1))
    std2 = Node(str(student2))
    
    path = BFS(graph, std1, std2)
    if path:
        return path.getLength()
    else:
        return -1
    

##print degOfSeparation(graph, 0, 21)
##print degOfSeparation(graph, 4, 90)
##print degOfSeparation(graph, 3, 100)

#
# PROBLEM 2a
#

def buildRatedFBGraph(filename):
    """
    Read the contents of the given file. Assumes each line in the file has three
    space separated numbers; the first two numbers represent the two students
    who are Facebook friends, and the third number is their friendship rating.

    There are 120 students in 6.00, and they are represented as integers from 0
    to 119. If a student does not have any Facebook friend in the class, her
    number will not appear in the file, but the graph returned by this function
    will include her.
    
    Parameters:
    filename - the name of the data file as a string. 

    Returns:
    a Graph structure representing the Facebook network of the 6.00 students and
    their friendship ratings as encoded in the data file, including students who
    are not be connected to any other students in the class
    """
    pairs = []
    txtFile = open(filename)
    for line in txtFile:
        words = line.split()
        student0 = int(words[0])
        student1 = int(words[1])
        connect = int(words[2])
        pairs.append([student0,student1,connect])
    txtFile.close()
    
    nodeIndex = range(120)
    nodes = []
    for i in nodeIndex:
        nodes.append(Node(str(i)))
        
    g = Graph()
    for n in nodes:
        g.addNode(n)

    print g
    
    for each in pairs:
        subNodes = [nodes[each[0]]]
        for i in range((each[2])-1):
            subNode = Node(str(each[0]) + str(each[1]) + str(i))
            g.addNode(subNode)
            subNodes.append(subNode)
        subNodes.append(nodes[each[1]])
  
        for i in range(len(subNodes)-1):
            g.addEdge(Edge(subNodes[i], subNodes[i+1]))

    return g

##graph = buildRatedFBGraph('ratedFBFriends.txt')
    

#
# PROBLEM 2b
#

def ratedDegOfSeparation(graph, student1, student2):
    """
    Takes in a rated Facebook graph and returns the rated degree of separation
    between two students. Returns -1 if the two students are not connected.

    Parameters:
    graph - a rated Graph structure representing a Facebook network.
    student1 - integer reprsenting student1
    student2 - integer represnting student2

    Returns: an integer representing rated degree of separation between student1
    and student2. If student1 and student2 are not connected, returns -1.
    """
    std1 = Node(str(student1))
    std2 = Node(str(student2))
    
    path = BFS(graph, std1, std2)
    if path:
        return path.getLength()
    else:
        return -1

##print ratedDegOfSeparation(graph, 0, 21)
##print ratedDegOfSeparation(graph, 4, 90)
##print ratedDegOfSeparation(graph, 3, 100)
   

#
# PROBLEM 3
#

def findGroups(graph):
    """
    Takes in a graph representing the Facebook network of the 6.00 students and
    returns a list of sets, where each set is a separate group of friends in the
    network. 

    Parameters:
    graph - a Graph structure representing a Facebook network.

    Returns:
    A list of sets where each set is collection of integers, representing the
    group of friends in the network. In one group of friends, each student is
    reachable from every other student in the group through some number of
    friends in the group. A member in one group cannot reach a member in another
    group.
    """
    result = []

    #build list
    nodeList = sorted(list(graph.getNodes()))
    num = range(graph.numNodes())
    
    listEdit = num
    while len(listEdit) > 0:
        #make list copy to delete used nodes
        listIter = listEdit
        #make list to add used nodes
        build = []
        for i in listIter:
            #use first node in list and check against remaining nodes
            path = BFS(graph, nodeList[listIter[0]], nodeList[i])
            if path:
                build.append(i)
                listEdit.remove(i)
        #store build list into final results as set
        result.append(set(build))
                
    return result

##findGroups(graph)


