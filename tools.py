import sys
from xml.dom import minidom
from graph import *

class ProgressBar:
    """
    Simple progress bar
    """

    def __init__(self):
        self.progressChar = 0;

    def draw(self, elapsed, total):
        percentage = (float)(elapsed * 100) / total
       
        if self.progressChar == 0:
            sys.stderr.write("\r| %d/%d (%.2f%%)" % (elapsed, total, percentage))

        if self.progressChar == 1:
            sys.stderr.write("\r/ %d/%d (%.2f%%)" % (elapsed, total, percentage))
            
        if self.progressChar == 2:
            sys.stderr.write("\r- %d/%d (%.2f%%)" % (elapsed, total, percentage))

        if self.progressChar == 3:
            sys.stderr.write("\r\\ %d/%d (%.2f%%)" % (elapsed, total, percentage))


        self.progressChar = self.progressChar + 1

        if self.progressChar > 3:
            self.progressChar = 0

        sys.stderr.flush()

def processGraphFile(fileName):
    xmlTree = minidom.parse(fileName)

    graphToSolve = Graph()

    for i in xmlTree.childNodes:
        if i.nodeName == 'graph':
            for elements in i.childNodes:
                # process graph node element
                if elements.nodeName == 'node':
                    nodeId = int(elements.getAttribute('id'))
                    nodeX = int(elements.getAttribute('x'))
                    nodeY = int(elements.getAttribute('y'))
                    graphToSolve.CreateNode(nodeId, nodeX, nodeY)

                    if elements.getAttribute('home') == 'true':
                        graphToSolve.GetNode(nodeId).isHomeNode = True

                #process graph edge element
                if elements.nodeName == 'edge':
                    edgeStartNode = int(elements.getAttribute('nodeA'))
                    edgeEndNode = int(elements.getAttribute('nodeB'))

                    graphToSolve.CreateEdge(edgeStartNode, edgeEndNode)

    return graphToSolve


def usage():
    print "-?/--help          - this help message"
    print "-s/--silent        - silent mode (no messages, except final solution list)"
    print "-fX/--filename=X   - specify X as the graph filename (default: graph.xml)"
    print "-tX/--travellers=X - solve the graph for X travellers (default: 2)"
    print "-iX/--min=X        - minimum path length/move limit for a traveller (default: no limit)"
    print "-aX/--max=X        - maximum path length/move limit for a traveller (default: no limit)"
    print "-lX/--limit=X      - consider up to X millions possible combinations. Use -l0 to calculate all of them (default: 1)"
    print "-rX/--redundancy=X - display solutions with at most X unused edges (default: display all solutions)"
    print "-c/--cyclic        - include cyclic paths in solutions (default: off)"
    print "-g/--guiFormat     - produce results suitable for the GUI display"
    print "-h/--allowHomes    - allow the algorithm to pass through home nodes (default: off)"
    print " "
