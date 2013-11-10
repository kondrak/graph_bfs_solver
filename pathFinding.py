from graph import *


class PathFinder:
    """
    Class container for pathfinding solution.
    """
    def __init__(self):
        self.canPassHomeNodes = False
        self.useCyclicBFS = False

    # convert the complex Graph object to a simple dictionary to
    # faciliate pathfinding without cycles
    def _GraphToDictionary(self, graphToConvert):
        result = dict()

        graphNodes = graphToConvert.GetNodes()

        for n in graphNodes:
            dictKey = n.id
            nodeNeighbours = []

            for i in n.GetNeighbourNodes():
                nodeNeighbours.append(i.id)
                
            result[dictKey] = nodeNeighbours    

        return result   

    # convert the complex Graph object to a node -> GraphEdge object dictionary to
    # facilitate pathfinding with cycles
    def _GraphToEdgeDictionary(self, graphToConvert):
        result = dict()

        graphNodes = graphToConvert.GetNodes()

        for n in graphNodes:
            dictKey = n.id
            nodeNeighbourEdges = []

            for e in n.GetNeighbourEdges():
                nodeNeighbourEdges.append(e)

            result[dictKey] = nodeNeighbourEdges
        
        return result


    # core BFS pathfinding function
    def FindAllPaths(self, graph, start, end):
        if self.useCyclicBFS:
            # find all paths - allow passing through the same node more than once
            convertedGraph = self._GraphToEdgeDictionary(graph)
            return self._CycledBFS(graph, convertedGraph, start, end)
        else:
            # find all paths - don't visit the same node more than once
            convertedGraph = self._GraphToDictionary(graph)
            return self._ClassicBFS(graph, convertedGraph, start, end)


    # perform BFS between node 'start' and node 'end'
    def _ClassicBFS(self, fullGraph, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]

        if not self.canPassHomeNodes:
            # we're passing thorugh a home node that is not the end node. We don't want that
            if len(path) > 1 and fullGraph.GetNode(start).isHomeNode:
                return []

        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self._ClassicBFS(fullGraph, graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


    # perform a modified BFS which allows cyclic paths
    def _CycledBFS(self, fullGraph, graph, start, end, prevEdgeId=-1, path=[], edgePath=[]):
        path = path + [start]

        # we keep track of the passed edges to allow passing through the same node multiple times
        # if this is the start of the algorithm, prevEdgeId is set to -1 (no previous edge)
        if prevEdgeId != -1:
            edgePath = edgePath + [prevEdgeId]
    
        if start == end:
            return [path]

        if not self.canPassHomeNodes:
            # we're passing thorugh a home node that is not the end node. We don't want that
            if len(path) > 1 and fullGraph.GetNode(start).isHomeNode:
                return []
        
        if not graph.has_key(start):
            return []

        paths = []
        for edge in graph[start]:
            # get the node id on the second end of the edge
            nodeId = edge.GetSecondNodeId(start)
  
            nextNodeIsNotPrevious = True

            # skip if the algorithm tries to backtrack in the next step
            if len(path) > 1:
                nextNodeIsNotPrevious = nodeId is not path[len(path)-2]

            if edge.id not in edgePath and nextNodeIsNotPrevious:
                newpaths = self._CycledBFS(fullGraph, graph, nodeId, end, edge.id, path, edgePath)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
