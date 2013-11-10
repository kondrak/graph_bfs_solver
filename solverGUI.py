import wx
import getopt
import sys
import os
import pprint
import pickle
from graph import *
from tools import processGraphFile

sys.path.append(os.getcwd())

class Globals:
    WINDOW_WIDTH = 960
    WINDOW_HEIGHT = 640 
    NODE_RADIUS = 25
    GRAPH_FILENAME = 'graph.xml'
    SOLUTION_DATA = dict()

def LoadGraph(fileName):
    try:
        return processGraphFile(fileName)
    except IOError:
        sys.exit(2)

def ProcessSolutionFile(solutionFileName):
    try:
        solutionFile = open(solutionFileName, 'rb')

        solutionData = pickle.load(solutionFile)
        #pprint.pprint(solutionData)
        solutionFile.close()

        Globals.SOLUTION_DATA = solutionData

    except IOError:
        print "Could not read solution file: " + solutionFileName
        sys.exit(2)

class OptionsPanel(wx.Panel):
    """
    Left-side options panel
    """
    def __init__(self, parent, graphPanelRef, infoPanelRef):
        super(OptionsPanel, self).__init__(parent, size=(parent.GetSizeTuple()[0] * 1 / 4, parent.GetSizeTuple()[1]))

        sampleList = []

        sIdx = 0
        for element in Globals.SOLUTION_DATA:
            sampleList.append("Solution #" + str(sIdx+1))
            sIdx += 1


        wx.StaticText(self, -1, "Show Solution:", (5, 5), (75, -1))
        self.ch = wx.Choice(self, pos=(0, 20), size=(self.GetSizeTuple()[0], -1), choices = sampleList)
        self.Bind(wx.EVT_CHOICE, self.EvtChoice, self.ch)
        self.graphPanel = graphPanelRef
        self.infoPanel = infoPanelRef


    def EvtChoice(self, event):
        self.graphPanel.UpdateSolutionData(event.GetInt())
        self.infoPanel.UpdateSolutionData(event.GetInt())
        self.graphPanel.Refresh(True)
        self.infoPanel.Refresh(True)


class InfoPanel(wx.Panel):
    """
    Bottom-right information panel
    """
    def __init__(self, parent):
        super(InfoPanel, self).__init__(parent, pos=wx.Point(Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT), size=(parent.GetSizeTuple()[0] * 3 / 4, parent.GetSizeTuple()[1] / 2))

        fs = self.GetFont().GetPointSize()
        nf = wx.Font(fs+2, wx.SWISS, wx.NORMAL, wx.NORMAL)

        box = wx.StaticBox(self, -1, "Solution Summary")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.t = wx.StaticText(self, -1, "")   
        self.t.SetFont(nf)
        bsizer.Add(self.t, 0, wx.TOP|wx.LEFT, 10)

       # for i in xrange(0, 10):
       #     e = wx.StaticText(self, -1, "x")
        bsizer.Add((0, 220), 0, wx.TOP|wx.LEFT, 10)

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(bsizer, 1, wx.EXPAND|wx.ALL, 10)

        border.Add((10, 50), 1)

        self.SetSizer(border)

    def UpdateSolutionData(self, solutionDataIdx):
        solutionData = Globals.SOLUTION_DATA[solutionDataIdx]

        #pprint.pprint(solutionData)

        paths = solutionData['Paths']

        colors = ['blue', 'red', 'green', 'yellow', 'cyan', 'pink', 'plum', 'purple', 'orange', 'brown' ]
        summaryText = ""
        tIdx = 1
        
        summaryText = "Unused edges: " + str(len(solutionData['RedundantEdgeIds']))

        if len(solutionData['RedundantEdgeIds']) > 0:
            summaryText += "\nUnused edge id list: " + str(solutionData['RedundantEdgeIds'])

        summaryText += "\n\n"

        for travellerInfo in solutionData['MoveLimits']:
            summaryText += "Traveller #" + str(tIdx) + " (" + colors[tIdx-1] + "): " + str(travellerInfo) + " moves on path "
            summaryText += "between nodes: " + str(solutionData['PathEndNodes'][tIdx-1]) + "\n"
            tIdx += 1

            self.t.SetLabel(summaryText)



class RenderableGraphPanel(wx.Panel):
    """
    Graph panel
    """
    def __init__(self, parent):
        super(RenderableGraphPanel, self).__init__(parent, size=(parent.GetSizeTuple()[0] * 3 / 4, parent.GetSizeTuple()[1] / 2))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.graph = LoadGraph(Globals.GRAPH_FILENAME)
        self.pathsAsEdges = []
        graphNodes = self.graph.GetNodes()

        nodeXcoords = []
        nodeYcoords = []
        for n in graphNodes:
            nodeXcoords.append(n.x)
            nodeYcoords.append(n.y)

        minX = min(nodeXcoords)
        maxX = max(nodeXcoords) + Globals.NODE_RADIUS
        minY = min(nodeYcoords)
        maxY = max(nodeYcoords) + Globals.NODE_RADIUS

        self.graphWidth = maxX
        self.graphHeight = maxY

        self.XScaleFactor = 1.0
        self.YScaleFactor = 1.0

        if (float)(self.graphWidth) / (float)(self.GetSizeTuple()[0]) > 1.0:
            self.XScaleFactor = (float)(self.graphWidth) / (float)(self.GetSizeTuple()[0])

        if (float)(self.graphHeight) / (float)(self.GetSizeTuple()[1]) > 1.0:
            self.YScaleFactor = (float)(self.graphHeight) / (float)(self.GetSizeTuple()[1])

        radiusForX = Globals.NODE_RADIUS * self.XScaleFactor * Globals.WINDOW_WIDTH / 960
        radiusForY = Globals.NODE_RADIUS * self.YScaleFactor * Globals.WINDOW_WIDTH / 960

        for n in graphNodes:
            n.x = (n.x - minX + 2 * radiusForX) / self.XScaleFactor
            n.y = (n.y - minY + 2 * radiusForY) / self.YScaleFactor

            #GetSizeTuple() pokazuje o 10 px za duzo?
            if self.GetSizeTuple()[0] - Globals.NODE_RADIUS * Globals.WINDOW_WIDTH/960  - (n.x + Globals.NODE_RADIUS * Globals.WINDOW_WIDTH / 960) < 0:
                n.x += (self.GetSizeTuple()[0] - (n.x + Globals.NODE_RADIUS * Globals.WINDOW_WIDTH / 960)) - Globals.NODE_RADIUS * Globals.WINDOW_WIDTH/960

            if self.GetSizeTuple()[1] - Globals.NODE_RADIUS * Globals.WINDOW_WIDTH/960  - (n.y + Globals.NODE_RADIUS * Globals.WINDOW_WIDTH / 960) < 0:
                n.y += (self.GetSizeTuple()[1] - (n.y + Globals.NODE_RADIUS * Globals.WINDOW_WIDTH / 960)) - Globals.NODE_RADIUS * Globals.WINDOW_WIDTH/960


        self.graphXOffset = 0
        self.graphYOffset = 0

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.SetBrush(wx.Brush(wx.WHITE))

        graphEdges = self.graph.GetEdges()
        graphNodes = self.graph.GetNodes()

        #map edge id to line width
        coloredEdges = dict()

        for e in graphEdges:
            dc.DrawLine((float)(e.connectedNodes[0].x - self.graphXOffset), 
                        (float)(e.connectedNodes[0].y - self.graphYOffset), 
                        (float)(e.connectedNodes[1].x - self.graphXOffset),
                        (float)(e.connectedNodes[1].y - self.graphYOffset))

            #coloredEdges[e.id] = 0


        for pae in self.pathsAsEdges:
            for element in pae:
                if element not in coloredEdges:
                    coloredEdges[element] = 2
                else:
                    coloredEdges[element] <<= 1


        #pprint.pprint(coloredEdges)


        colors = ['blue', 'red', 'green', 'yellow', 'cyan', 'pink', 'plum', 'purple', 'orange', 'brown' ]
        colorIdx = 0

        for pae in self.pathsAsEdges:
            for element in pae:
                if coloredEdges[element] == 2:
                    dc.SetPen(wx.Pen(colors[colorIdx], (coloredEdges[element] )))
                else:
                    dc.SetPen(wx.Pen(colors[colorIdx], 2 * (coloredEdges[element] )))

                coloredEdges[element] >>= 1

                e = self.graph.GetEdge(element)

                dc.DrawLine((float)(e.connectedNodes[0].x - self.graphXOffset), 
                            (float)(e.connectedNodes[0].y - self.graphYOffset), 
                            (float)(e.connectedNodes[1].x - self.graphXOffset),
                            (float)(e.connectedNodes[1].y - self.graphYOffset))

            colorIdx += 1

        for n in graphNodes:
            if n.isHomeNode:
                dc.SetBrush(wx.Brush(wx.BLUE))
            else:
                dc.SetBrush(wx.Brush(wx.WHITE))

            dc.SetPen(wx.Pen(wx.BLACK, 2))
            dc.DrawCircle((float)(n.x - self.graphXOffset), (float)(n.y - self.graphYOffset), Globals.NODE_RADIUS * Globals.WINDOW_WIDTH / 960)

    def UpdateSolutionData(self, solutionDataIdx):
        solutionData = Globals.SOLUTION_DATA[solutionDataIdx]

        paths = solutionData['Paths']


        allPathEdgeList = []

        for p in paths:

            pathEdges = []

            #print p

            for i in xrange(0, len(p)-1):
                for edgeId in self.graph.GetEdgeForNodePair(p[i], p[i+1]):
                    pathEdges.append(edgeId.id)

            allPathEdgeList.append(pathEdges)

        self.pathsAsEdges = allPathEdgeList

        #pprint.pprint(solutionData)


class MainWindow(wx.Frame):
    """
    Main applicaiton window
    """
    def __init__(self, title):
        super(MainWindow, self).__init__(None, title=title, size=(Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)        
        self.InitUI()
        self.Centre()
        self.Show()


    def InitUI(self):
        rootPanel = wx.Panel(self, size=self.GetSizeTuple())
        graphPanel = RenderableGraphPanel(rootPanel)
        graphInfoPanel = InfoPanel(rootPanel)
        optionsPanel = OptionsPanel(rootPanel, graphPanel, graphInfoPanel)

        #optionsPanel.SetBackgroundColour('#00ff00') # window bg
        #graphPanel.SetBackgroundColour('#0000ff') 
        #graphInfoPanel.SetBackgroundColour('#ff0000')

        vbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(optionsPanel, 0, wx.ALIGN_LEFT, 0)
        vbox.Add(vbox2)
        vbox2.Add(graphPanel, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP, 0)
        vbox2.Add(graphInfoPanel, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM | wx.EXPAND, 0)
        rootPanel.SetSizer(vbox)
   

if __name__ == '__main__':
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "f:", ["filename="])

        for opt, arg in opts:
            if opt in ("-f", "--filename"):
                Globals.GRAPH_FILENAME = arg
    except getopt.GetoptError:
        usage()
        sys.exit(2) 

    ProcessSolutionFile('output.txt')

    guiApp = wx.App()
  
    mainWin = MainWindow('SolverGUI')
    guiApp.MainLoop()
