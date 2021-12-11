import heapq 
import sys

class Graph:
    def __init__(self,totalEdges): #create list for vertices ranks and parent vertices
        self.rank = [1] * totalEdges
        self.parent = [i for i in range(totalEdges)]
        self.total = totalEdges #used to decrement until all edges have been compared 
    
    def search(self,x): #return particular vertex
        if x!=self.parent[x]:
            self.parent[x]=self.search(self.parent[x])
        return self.parent[x]
    
    def union(self,x,y): #union by rank to merge lists to complete list of ranks 
        rootx = self.search(x)
        rooty = self.search(y)  
        if rooty==rootx:
            return False
        self.total-=1
        if self.rank[rootx]>self.rank[rooty]: #link lower ranked tree
            self.parent[rooty]=rootx
            self.rank[rootx]+=self.rank[rooty]
        else:
            self.parent[rootx]=rooty #if rank same set to root 
            self.rank[rooty]+=self.rank[rootx]
        return True
                
class MST:


    def findMinSpanningTree(self, vertices,edges):

        totalWeight = 0
        tree = Graph(vertices)
        mstEdges = []
        heapq.heapify(edges) #make edge list a heap to form a sorted graph representation 
       
        while edges and tree.total> 1:
            weight,u,v = heapq.heappop(edges)
            if tree.union(u,v):
                mstEdges.append((u,v,weight))
                totalWeight += weight

        f=open("output kruskals.txt", "a")

        f.write(str(totalWeight)+"\n" )

      
        for i in mstEdges:
            f.write(str(i[0])+" "+str(i[1])+" "+str(i[2])+"\n")
        return totalWeight


if __name__ == '__main__':


   
    
    filename = sys.argv[0]
    verts = int(sys.argv[1])
    graphFile = sys.argv[2]

    graph = open(graphFile, "r")
    

    sol = MST()



    edges = []

    for line in graph:
        req = line.split(' ')
        if req[2].endswith('\n'):
            req[2] = req[2][:-1]
        u =int(req[0])
        v =int(req[1])
        w =int(req[2])
        edges.append((w,u,v))
       
    sol.findMinSpanningTree(verts,edges)
