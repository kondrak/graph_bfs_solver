from graphComponents import *

class Graph:
    """
    Graph representation
    """
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.travellers = []
        self._nextEdgeId = 0
        self._nextTravellerId = 0


    # perform graph reset
    def Reset(self):

        self.travellers = []

        for n in self.nodes:
            n.currentTraveller = None

        for e in self.edges:
            e.weight = 1


    # return node object idenfitied by nodeId
    def GetNode(self, nodeId):
        for n in self.nodes:
            if n.id == nodeId:
                return n

        return None

    def GetEdge(self, edgeId):
        for e in self.edges:
            if e.id == edgeId:
                return e

        return None

    # return all existing edges between node A and B
    def GetEdgeForNodePair(self, nodeAId, nodeBId):
        edgeList = []
        for e in self.edges:
            if (nodeAId == e.connectedNodes[0].id and nodeBId == e.connectedNodes[1].id) or (nodeAId == e.connectedNodes[1].id and nodeBId == e.connectedNodes[0].id):
                return [e] #edgeList.append(e)

        return edgeList

    # return unused edges (ie. weight != -1)
    def GetFreeEdges(self):
        edgeList = []
        for e in self.edges:
            if e.weight != EDGE_OCCUPIED:
                edgeList.append(e)

        return edgeList
        

    # return a list of home nodes in graph
    def GetHomeNodeIds(self):
        homeNodes = []

        for n in self.nodes:
            if n.isHomeNode:
                homeNodes.append(n.id)

        return homeNodes



    # returns all nodes
    def GetNodes(self):
        return self.nodes

    # returns all edges
    def GetEdges(self):
        return self.edges

    # create a new node object with specified nodeId
    def CreateNode(self, nodeId, nodeX, nodeY):
        self.nodes.append(GraphNode(nodeId, nodeX, nodeY))

    # create a new edge object connecting startNodeId and endNodeId
    def CreateEdge(self, startNodeId, endNodeId):
        startNode = None
        endNode = None

        for n in self.nodes:
            if n.id == startNodeId:
                startNode = n      

            if n.id == endNodeId:
                endNode = n

        newEdge = GraphEdge(startNode, endNode, self._nextEdgeId)
        self.edges.append(newEdge)
        self._nextEdgeId += 1


    # create a traveller object at startNodeId
    def AddTraveller(self, startNodeId):
        for n in self.nodes:
            if n.id == startNodeId:
                newTraveller = GraphTraveller(n, self._nextTravellerId)
                self.travellers.append(newTraveller)
                self._nextTravellerId += 1


    # set the EDGE_OCCUPIED flag for a specified edge
    def RemoveEdge(self, edgeId):
        for e in self.edges:
            if e.id == edgeId:
                e.weight = EDGE_OCCUPIED


    def IsSolvableForSet(self, solutionSet):
        #print "Solving set " + str(solutionSet)
        for s in solutionSet:
            success = self.WalkPath(s)
            if not success:
                return None

        return solutionSet


    def WalkPath(self, NodeIdList):

        if len(NodeIdList) == 0:
            print "Attempting to walk an empty path. Aborting!"
            return False

        self.AddTraveller(NodeIdList[0])


        for n in NodeIdList:
            nextNode = self.GetNode(n)

            if nextNode.id == NodeIdList[0]:
                continue

            if nextNode is None:
                print "Node " + str(n) + " does not exist. Aborting!"
                return False

            #print "Moving to " + str(n)
            moveSuccessful = self.travellers[len(self.travellers)-1].MoveToNode(nextNode)

            if not moveSuccessful:
                #print "Failed at " + str(nextNode.id)
                return False

        return True

    # debug information about all nodes
    def NodeInfo(self):
        for n in self.nodes:
            neighbourIds = []
            nodeNeighbours = n.GetNeighbourNodes()

            for i in nodeNeighbours:
                neighbourIds.append(i.id)

            infoText = 'Node ' + str(n.id) + ' '

            if n.isHomeNode:
                infoText += '(HOME) '

            infoText += 'has ' + str(len(nodeNeighbours)) + ' neighbours (' + str(neighbourIds) + ')'
    
            if n.currentTraveller is not None:
                infoText += ' and traveller ' + str(n.currentTraveller.id)

            print infoText


    # debug information about all edges
    def EdgeInfo(self):
        for e in self.edges:
            print 'Edge ' + str(e.id) + ' has nodes ' + str(e.connectedNodes[0].id) + ' and ' + str(e.connectedNodes[1].id)

        
    # debug information about all travellers
    def TravellerInfo(self):
        for t in self.travellers:
            print 'Traveller at node ' + str(t.currentNode.id)
