import math
import sys

class FibonacciHeap:


    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.deg = 0
            self.marked = False
            self.parent = None
            self.child = None
            self.lneighbor = None
            self.rneighbor = None
     
           
    rootList = None
    minNode = None

    nodeTotal = 0

    # to iterate through linked lists
    def iterThrough(self, head):
        node = head
        end = head
        flag = False
        while True:
            if flag is True and node == end:
                    break
            elif node == end:
                flag = True
            yield node
            node = node.rneighbor

 

    def get_minNode(self):
        return self.minNode

    # delete minimum node node from the heap 

    def extract_min(self):
        currentMin = self.minNode
        if currentMin is not None:
            if currentMin.child is not None:
                childNodes = [x for x in self.iterThrough(currentMin.child)]
                for i in range(0, len(childNodes)):
                    self.mergeRootList(childNodes[i])
                    childNodes[i].parent = None
            self.rootListDelete(currentMin)
            
            if currentMin == currentMin.rneighbor:
                self.minNode = self.rootList = None
            else:
                self.minNode = currentMin.rneighbor # update min node  
                self.consolidateHeap()
            self.nodeTotal -= 1
        return currentMin

    # insert new node into unordered list of roots 
    def insert(self, key, value=None):
        newNode = self.Node(key, value)
        newNode.lneighbor = newNode
        newNode.rneighbor = newNode
        self.mergeRootList(newNode)
        if self.minNode is None or newNode.key < self.minNode.key:
            self.minNode = newNode
        self.nodeTotal += 1
        return newNode

    # Modify a key in the heap
    def decrease_key(self, x, k):
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascade_cut(y)
        if x.key < self.minNode.key:
            self.minNode = x

  
    def merge(self, h2):
        tempHeap = FibonacciHeap()
        tempHeap.rootList, tempHeap.minNode = self.rootList, self.minNode
        last = h2.rootList.lneighbor
        h2.rootList.lneighbor = tempHeap.rootList.lneighbor
        tempHeap.rootList.lneighbor.rneighbor = h2.rootList
        tempHeap.rootList.lneighbor = last
        tempHeap.rootList.lneighbor.rneighbor = tempHeap.rootList
   
        if h2.minNode.key < tempHeap.minNode.key:
            tempHeap.minNode = h2.minNode
        # update node total for heap
        tempHeap.nodeTotal = self.nodeTotal + h2.total_nodes
        return tempHeap


    def cut(self, x, y):
        self.childListDelete(y, x)
        y.deg -= 1
        self.mergeRootList(x)
        x.parent = None
        x.marked = False

    def cascade_cut(self, a_node):
        parentNode = a_node.parent
        if parentNode is not None:
            if a_node.marked is False:
                a_node.marked = True
            else:
                self.cut(a_node, parentNode)
                self.cascade_cut(parentNode)

    # combine root nodes of equal deg to consolidate the heap
    # by creating a list of unordered binomial trees
    def consolidateHeap(self):
        tempList = [None] * self.nodeTotal
        nodes = [weight for weight in self.iterThrough(self.rootList)]


        for weight in range(0, len(nodes)):
            currentWeight = nodes[weight]
            degree = currentWeight.deg

            while tempList[degree] != None:
                currentDegree = tempList[degree]
                if currentWeight.key > currentDegree.key:
                    temp = currentWeight
                    currentWeight, currentDegree = currentDegree, temp
                self.linkHeap(currentDegree, currentWeight)
                tempList[degree] = None
                degree += 1
            tempList[degree] = currentWeight
        for i in range(0, len(tempList)):
            if tempList[i] is not None:
                if tempList[i].key < self.minNode.key:
                    self.minNode = tempList[i]

   #link one node in heap to another 
    def linkHeap(self, node1, node2):
        self.rootListDelete(node1)
        node1.lneighbor =node1
        node1.rneighbor = node1
        self.mergeChildList(node2, node1)
        node2.deg += 1
        node1.parent = node2
        node1.marked = False

    # merge node with the root list
    def mergeRootList(self, node):
        if self.rootList is None:
            self.rootList = node
        else:
            node.rneighbor = self.rootList.rneighbor
            node.lneighbor = self.rootList
            self.rootList.rneighbor.lneighbor = node
            self.rootList.rneighbor = node

    def mergeChildList(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.rneighbor = parent.child.rneighbor
            node.lneighbor = parent.child
            parent.child.rneighbor.lneighbor = node
            parent.child.rneighbor = node

   #delete node from list
    def rootListDelete(self, node):
        if node == self.rootList:
            self.rootList = node.rneighbor
        node.lneighbor.rneighbor = node.rneighbor
        node.rneighbor.lneighbor = node.lneighbor


    def childListDelete(self, parent, node):
        if parent.child == parent.child.rneighbor:
            parent.child = None
        elif parent.child == node:
            parent.child = node.rneighbor
            node.rneighbor.parent = parent
        node.lneighbor.rneighbor = node.rneighbor
        node.rneighbor.lneighbor = node.lneighbor 

def dijkstra(adjList, start, end = None): #apply dijkstra to find minimum distance to treasure 
    totalVertices = len(adjList)    
    visited = [False]*totalVertices
    distance = [math.inf]*totalVertices

    Nodes = [None]*totalVertices
    heap = FibonacciHeap()
    for i in range(totalVertices):
        Nodes[i] = heap.insert(math.inf, i)     

    distance[start] = 0
    heap.decrease_key(Nodes[start], 0)

    while heap.nodeTotal:
        currentNode = heap.extract_min().value
        visited[currentNode] = True

        #early exit
        if end and currentNode == end:
            break

        for (neighbor, weight) in adjList[currentNode]:
            if not visited[neighbor]:
                if distance[currentNode] + weight < distance[neighbor]:
                    distance[neighbor] = distance[currentNode] + weight
                    heap.decrease_key(Nodes[neighbor], distance[neighbor])


    return distance

def createAdjacencyList(graph,vertices):
    adjacencyList = [[],]

    for i in range (vertices):
        for j in graph:
            if graph[j][0]==i:
                adjacencyList.append([graph[j][1],graph[j][2]])
    print(adjacencyList)
    return adjacencyList





if __name__ == '__main__':

    filename = sys.argv[0]
    vertices = int(sys.argv[1])
    treasureIndex = sys.argv[2]
    graphFile = sys.argv[3]

    graph = open(graphFile, "r")



    


    graph = open("graph.txt", "r")


    edges = []

    for line in graph:
        if len(line)<5:
            start = int(line)
        else:
            req = line.split(' ')
            if req[2].endswith('\n'):
                req[2] = req[2][:-1]
            u =int(req[0])    
            v =int(req[1])
            w =int(req[2])
            edges.append((w,u,v))

    print(edges)
    createAdjacencyList(edges,vertices)
    f=open("output_adventure.txt", "a")
    



    