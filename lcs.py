import sys
from operator import attrgetter

leafNodeEnd = -1



class Node:


    def __init__(self, leafnode):
        # self.__identifier = identifier
        self.children = [None]*28
        # for leaf nodes, it stores the index of suffix for
        # the path  from root to leaf
        self.leafnode = leafnode #boolean if node is leaf or not 
        self.suffixIndex = None #index of suffix of path from root to leaf
        self.suffixLink = None  #index of node with same suffix, forms suffix link 
        self.start = None
        self.end = None
        
    
    def __repr__(self):
        return "Node(suffix link: %d)"%self.suffixIndex

    def __getattribute__(self, n):
        if n == 'end':
            if self.leafnode:
                return leafNodeEnd
        return super(Node, self).__getattribute__(n)
    
    def __ne__(self, node):
        attr = attrgetter('start', 'end', 'suffixIndex')
        return attr(self) != attr(node)


    def __eq__(self, node):
        attr = attrgetter('start', 'end', 'suffixIndex')
        return attr(self) == attr(node)




class SuffixTree:


    def __init__(self, string1,string2):

        self.str = string1+'#'+string2+'$'
        self.string1 = string1
        self.string2 = string2
        self.finalNewNode = None
        self.actNode = None
        self.rootFinal = None
        self.splitFinal = None
        self.actEdge = -1 #input string index reference 
        self.actLength = 0
        self.size = -1  # string length 
        self.suffixesLeft = 0 # int to track suffixes left to add to complete building tree
        self.root = None # will be set to a special node to represent the root 
        self.dfslist = []
        self.alphabet =  ['#','$','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.suffixArray = None
        self.size1ststr = len(string1) + 1
        self.maxLen = 0
        self.substrstartindex = 0

    def length_edge(self, node):
        edgelength = node.end - node.start + 1
        return edgelength


    
    def create_node(self, start, end=None, isLeaf=False):
        
        node = Node(isLeaf)
        node.suffixLink = self.root
     

        node.suffixIndex = -1  #initialized at -1 and set later for leaf nodes 

        node.start = start
        node.end = end #end is None as this is a new child node 
        return node


   

    def traverse_tree(self, a_node):
       #set node as the activeNode and adjust active edge variables 
        
        currentLen = self.length_edge(a_node)

        if (self.actLength >= currentLen):  #traverse using skip/count trick



            self.actLength -= currentLen 
            self.actEdge += currentLen
            
            self.actNode = a_node
            return True #return true if active length larger than given length of edge



        return False



    def extend_suffix_tree(self, startPosition): #extend suffix tree using ukkonen's algorithm
        global leafNodeEnd
     
        leafNodeEnd = startPosition   #extension rule 1: if current path from root ends at leaf edge then the next character is added to the label

        self.suffixesLeft += 1

        self.lastNewNode = None  
     

        while(self.suffixesLeft > 0): #add suffixes to tree until all suffix of curent iteration adde


            if (self.actLength == 0):
                self.actEdge = startPosition 

            tempPosition = self.alphabet.index(self.str[self.actEdge])
            
            if (self.actNode.children[tempPosition] is None):
                
                self.actNode.children[tempPosition] = self.create_node(startPosition, isLeaf=True)

                # Extension rule 2. If cur  rent path from the root  ends at edge that is not leaf, new leaf edge is made from character S[i+1].
                #if there is any internal node thats suffix link hasnt been reset yet, point the suffix link from that last
                #node to the current active node.lastNewNode set to none once suffix link is reset. 
                
               
                if (self.lastNewNode is not None):

                    self.lastNewNode.suffixLink = self.actNode
                    self.lastNewNode = None
      
            else: # there exists an edge/child node from the current active node
                nxtNode = self.actNode.children[tempPosition]


                if self.traverse_tree(nxtNode):  
                    continue # start once again now that the next node is set as the active node 
   
                if (self.str[startPosition] == self.str[self.actLength+nxtNode.start]):
                    
            # extension rule 3, if the path from the root ends at non-leaf 
            # and next character is already in tree then break        

                    if((self.lastNewNode is not None) and (self.actNode != self.root)):

            #############################################################                    
                        self.lastNewNode.suffixLink = self.actNode
                        self.lastNewNode = None
                
                    self.actLength += 1
                    
                    break
                
                self.splitFinal = nxtNode.start + self.actLength - 1
              
                splitNode = self.create_node(nxtNode.start, self.splitFinal)
                self.actNode.children[tempPosition] = splitNode
                # New leaf coming out of new internal node
                splitNode.children[self.alphabet.index(self.str[startPosition])] = self.create_node(startPosition, isLeaf=True)
                nxtNode.start += self.actLength
                splitNode.children[self.alphabet.index(self.str[nxtNode.start])] = nxtNode
              

                if (self.lastNewNode is not None):
                    # suffixLink of lastNewNode points to current newly
                    # created internal node
                    self.lastNewNode.suffixLink = splitNode
                
                self.lastNewNode = splitNode
           
            self.suffixesLeft -= 1
            if ((self.actNode == self.root) and (self.actLength > 0)):
                self.actLength -= 1
                self.actEdge = startPosition - self.suffixesLeft + 1

            elif (self.actNode != self.root):  
                self.actNode = self.actNode.suffixLink


    def setSuffixIndex(self,a_Node, H):

        if a_Node is None:
            return
    
        leaf = 1
      
        for node in a_Node.children:
            if (node is not None):
                leaf = 0
                self.setSuffixIndex(node, H + self.length_edge(node))
            
         
        if (leaf == 1):
            a_Node.suffixIndex = self.size - H
     
             
         



    def walk_dfs(self, current):
        start = current.start
        end = current.end
        print(current.children)
        self.dfslist.append([self.str[start: end + 1],current.suffixIndex])
        yield self.str[start: end + 1]

        # sort children lexicographically

        for node in current.children:
            if node:
                yield from self.walk_dfs(node)

    def doTraversal(self,Node, array):
        if Node is None:
            return

 
        if Node.suffixIndex == -1:
            # sort children lexicographically
            for node in Node.children:
                if node is not None:
                    self.doTraversal(node,array)

        elif (Node.suffixIndex > -1 and Node.suffixIndex < self.size):
            array.append((Node.suffixIndex))
    
    def lcsTraversal(self,a_Node, labelH,maxLen,subString_startIndex):
        if Node is None:
            return

        retval = -1
        
        if a_Node.suffixIndex < 0:
            for node in a_Node.children:
                if node is not None:
                    retval = self.lcsTraversal(node, labelH +self.length_edge(node),  
                    self.maxLen, self.substrstartindex)

                    if a_Node.suffixIndex ==-1:
                        a_Node.suffixIndex = retval
                    elif a_Node.suffixIndex == -3 and retval == -2 or a_Node.suffixIndex == -2 and retval == -3 or a_Node.suffixIndex == -4:
                        a_Node.suffixIndex = -4

                        if(maxLen < labelH):
                            self.maxLen = labelH
                            self.substrstartindex = a_Node.end - labelH + 1      
        elif(a_Node.suffixIndex >= self.size1ststr): 
            return -3
        elif(a_Node.suffixIndex > -1 and a_Node.suffixIndex < self.size1ststr):
            return -2

        return a_Node.suffixIndex

            
    def build_suffix_array(self):
        suffixArray = [] 
        self.doTraversal(self.root, suffixArray)
        self.suffixArray = suffixArray


    def build_suffix_tree(self):
        self.size = len(self.str)
        self.rootFinal = -1
        self.root = self.create_node(-1, self.rootFinal)
        self.actNode = self.root  # First activeNode will be root, root has no parent and has start and end set to -1
        for i in range(self.size):
            self.extend_suffix_tree(i)
            
        

    
    def print_dfs(self):
        for sub in self.walk_dfs(self.root):
            print(sub)
    
    def lcs(self):
      
        

        substring = ''
        allsubsStrfound = False
        self.lcsTraversal(self.root,0,self.maxLen,self.substrstartindex)

        #size of longest common substring found, use list comphrehension to find any other substrings
        for k in range (self.maxLen):
            substring+=(self.str[k + self.substrstartindex]) 
        
        f=open("output_lcs.txt", "a")

        f.write(str(self.maxLen)+"\n" )

  
        
        startIndex1 = self.substrstartindex
        startIndex2 = self.string2.index(substring[0])
        string1 = self.string1
        string2 = self.string2
  
        offsetIndex1 = 0
        offsetIndex2 = 0

        f.write((str(startIndex1)+" "+str(startIndex2)+"\n"))

        ''' #approach to get multiple matches of lcs is bugged 
        while allsubsStrfound == False:
            if (len(string1) - (startIndex1+1) < self.maxLen or len(string2) - (startIndex2+1)< self.maxLen):
       
                allsubsStrfound = True
                return
            else:
                substring = ''

                string1 = string1[(startIndex1+1):len(string1)]
                string2 = string2[(startIndex2+1):len(string2)]
                offsetIndex1 += len(self.string1)-len(string1)
                offsetIndex2 += len(self.string2)-len(string2)

                self.str = string1+'#'+string2+'$'
                print(self.str)
                self.build_suffix_tree()
                self.setSuffixIndex(self.root,0)
                self.maxLen = 0
                self.substrstartindex = 0
                self.lcsTraversal(self.root,0,self.maxLen,self.substrstartindex)
                for k in range (self.maxLen):
                    substring+=(self.str[k + self.substrstartindex])

                startIndex1 = self.substrstartindex
                startIndex2 = string2.index(substring)
                f.write((str(startIndex1+offsetIndex1)+" "+str(startIndex2+offsetIndex2)))
'''

                
               
                
        

       








if __name__ == '__main__':


    
    filename = sys.argv[0]
    txtFile1 = sys.argv[1]
    txtFile2 = sys.argv[2]

    text1 = open(txtFile1, "r").read()
    text2 = open(txtFile1, "r").read()

    txtFile1.close()
    txtFile2.close()
    


    

    st = SuffixTree(text1,text2)
    st.build_suffix_tree()
    st.setSuffixIndex(st.root,0)
    st.lcs()






'''
Used as reference


'''