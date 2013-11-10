
EDGE_OCCUPIED = -1

class GraphNode:
    """
    Graph node representation
    """
    def __init__(self, nodeId, nodeX, nodeY):
        self.connectedEdges = []
        self.id = nodeId
        self.currentTraveller = None
        self.isHomeNode = False
        self.x = nodeX
        self.y = nodeY

    # check if the current node and a node specified by neighbourId are connected
    # returns the neighbourId node object if it's connected
    def IsNodeNeighbour(self, neighbourId):
        for ce in self.connectedEdges:
            if ce.weight != EDGE_OCCUPIED:
                if (ce.connectedNodes[0].id == neighbourId) or (ce.connectedNodes[1].id == neighbourId):
                    return ce

        return None

    # returns all nodes connected to the current node
    def GetNeighbourNodes(self):
        myNeighbours = []
        
        for ce in self.connectedEdges:
            if ce.weight != EDGE_OCCUPIED:
                if ce.connectedNodes[0].id != self.id:
                    myNeighbours.append(ce.connectedNodes[0])
                elif ce.connectedNodes[1].id != self.id:
                        myNeighbours.append(ce.connectedNodes[1])
        
        return myNeighbours

    # returns all edges connected to the current node
    def GetNeighbourEdges(self):
        myNeighbourEdges = []
        
        for ce in self.connectedEdges:
            if ce.weight != EDGE_OCCUPIED:
                myNeighbourEdges.append(ce)

        return myNeighbourEdges


class GraphEdge:
    """
    Graph edge representation
    """
    def __init__(self, nodeA, nodeB, edgeId):
        self.connectedNodes = [nodeA, nodeB]
        self.weight = 1
        self.id = edgeId
        nodeA.connectedEdges.append(self)
        nodeB.connectedEdges.append(self)

    # get the id of the second node belonging to the edge
    def GetSecondNodeId(self, firstNodeId):
        if self.connectedNodes[0].id == firstNodeId:
            return self.connectedNodes[1].id
        else:
            return self.connectedNodes[0].id

        print "Edge doesn't exist!"
        return None


class GraphTraveller:
    """
    The graph traveller representation
    """
    def __init__(self, startNodeRef, travellerId):
        self.id = travellerId
        self.currentNode = startNodeRef
        self.startNodeId = startNodeRef.id
        self.visitedNodeIds = []
        self.visitedNodeIds.append(self.startNodeId)
        startNodeRef.currentTraveller = self


    # Move the traveller to a node. 
    # Returns True if successful; False - otherwise
    def MoveToNode(self, nextNodeRef):

        # return if we already visited that node
        if self.visitedNodeIds.count(nextNodeRef.id) > 0:
            return False

        edgeToNeighbour = self.currentNode.IsNodeNeighbour(nextNodeRef.id)

        if edgeToNeighbour is not None:
            if (nextNodeRef.currentTraveller is None) or (nextNodeRef.isHomeNode and nextNodeRef.id != self.startNodeId):
                if self.currentNode.currentTraveller == self:
                    self.currentNode.currentTraveller = None

                self.currentNode = nextNodeRef
                self.currentNode.currentTraveller = self
            
                #self.visitedNodeIds.append(nextNodeRef.id)
                #flag edge as used
                edgeToNeighbour.weight = EDGE_OCCUPIED
                return True 

        return False

    # returns True if we arrived at the home node, False otherwise
    def ArrivedHome(self):
        if self.currentNode.isHomeNode and (self.currentNode.id != self.startNodeId):
            return True

        return False
