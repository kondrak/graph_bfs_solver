#  *** BFS Graph Solver ***
#  (c) Krzysztof Kondrak (at) gmail (dot) com
import sys
import os
import itertools
import getopt
import pickle
from graph import *
from pathFinding import *
from tools import ProgressBar, usage, processGraphFile

sys.path.append(os.getcwd())

SILENT_MODE = False

def Message(msg):
    if not SILENT_MODE:
        print msg

def Warning(msg):
    if not SILENT_MODE:
        sys.stderr.write(msg + "\n")
        sys.stderr.flush()

def parseGraph(fileName):
    try:
        Message("\n* Parsing graph file: " + fileName)
        return processGraphFile(fileName)
    except IOError:
        print "*** ERROR: Could not open " + fileName + ". Aborting. (Run with -? for help) ***"
        print " "
        sys.exit(2)


def main(argv):

    pathFinder = PathFinder()
    numTravellers = 2
    combinationLimit = 1000000
    minPathLength = -1
    maxPathLength = -1
    maxEdgeRedundancy = -1
    guiFormat = False
    fileName = ""

    try:                                
        opts, args = getopt.getopt(argv, "?gst:l:f:i:a:chr:", ["help", "guiFormat", "silent", "travellers=", "limit=", "filename=", "min=", "max=", "cyclic", "allowHomes", "allowhomes", "redundancy="])

        for opt, arg in opts:
            if opt in ("-?", "--help"):
                usage()                     
                sys.exit(1)
            if opt in ("-t", "--travellers"):
                numTravellers = int(arg)
            if opt in ("-l", "--limit"):
                combinationLimit = int(arg) * 1000000

            if opt in ("-f", "--filename"):
                fileName = arg

            if opt in ("-i", "--min"):
                minPathLength = int(arg) + 1

            if opt in ("-a", "--max"):
                maxPathLength = int(arg) + 1

            if opt in ("-r", "--redundancy"):
                maxEdgeRedundancy = int(arg)

            if opt in ("-c", "--cyclic"):
                pathFinder.useCyclicBFS = True

            if opt in ("-h", "--allowHomes", "--allowhomes"):
                pathFinder.canPassHomeNodes = True

            if opt in ("-g", "--guiFormat", "--guiformat"):
                guiFormat = True

            if opt in ("-s", "--silent"):
                global SILENT_MODE 
                SILENT_MODE = True

        if len(fileName) == 0:
            usage()
            sys.exit(2)
            
    except getopt.GetoptError:
        usage()
        sys.exit(2) 

    progressBar = ProgressBar()
    testGraph = parseGraph(fileName)

    Message("\n* Solving for " + str(numTravellers) + " traveller(s)")

    if combinationLimit > 0:
        Message("* Considering at most " + str(combinationLimit) + " combinations.")
    else:
        Message("* Attempting to solve all combinations.")

    homeNodeIds = testGraph.GetHomeNodeIds()
    homeNodePairs = itertools.combinations(homeNodeIds, 2)

    solutions = []


    # FindAllPaths dla wszystkich par domkow
    for p in homeNodePairs:
        for s in pathFinder.FindAllPaths(testGraph, p[0], p[1]):
            if(minPathLength == -1 or len(s) >= minPathLength) and (maxPathLength == -1 or len(s) <= maxPathLength):
                solutions.append(s)


    #generate solution sets
    solutions.sort()
    
    Message("Discovered " + str(len(solutions)) + " paths for all home nodes.")
    combinations = itertools.combinations(solutions, numTravellers)
    
    solutionSets = []

    numMillions = 1
  
   # if combinationLimit > 0:
    currentCombination = 0
    for c in combinations:
        if currentCombination == combinationLimit and combinationLimit > 0:
            break

        if currentCombination > numMillions*1000000:
            Warning("** WARNING: over " + str(numMillions) + " million combinations.")
            numMillions = numMillions + 1

        solutionSets.append(c)
        currentCombination = currentCombination + 1
   # else:
   #     solutionSets = list(combinations)

    Message("* Spawned " + str(len(solutionSets)) + " combinations.")
    
    # get rid of gazillions duplicate entries
    Message("* Filtering combinations, this may take a while...")
    solutionSets.sort()
    solutionSets = list(solutionSets for solutionSets,_ in itertools.groupby(solutionSets))

    totalNumSets = len(solutionSets)

    Message("* Will check " + str(totalNumSets) + " unique sets")

    possibleSolutions = []
    currentSetNum = 0
    solutionNum = 1

    for s in solutionSets:

        if not SILENT_MODE:
            progressBar.draw(currentSetNum, totalNumSets)

        currentSetNum = currentSetNum + 1

        testGraph.Reset()
        possibleSolution = testGraph.IsSolvableForSet(s)

        if possibleSolution is not None:
            Message("\rSolution " + str(solutionNum) + " " + str(possibleSolution))

            # check how many edges are left unused, the less the better
            unusedEdges = testGraph.GetFreeEdges()

            possibleSolutions.append((possibleSolution, unusedEdges))
            solutionNum = solutionNum + 1

        if not SILENT_MODE:
            progressBar.draw(currentSetNum, totalNumSets)

    Message("\n")

    # sort solutions by number of unused edges
    possibleSolutions.sort(key=lambda possibleSolutions: len(possibleSolutions[1]))

    numSolutionsListed = 0

    guiFormatDataList = [] # container of guiFormatData

    for s in possibleSolutions:
        solutionString = str(s[0]) + " "

        guiFormatData = dict()
        guiFormatData['Paths'] = s[0]
        guiFormatData['PathEndNodes'] = []
        guiFormatData['MoveLimits'] = []
        for element in s[0]:
            startPoint = "(SP: " + str(element[0]) + "|" + str(element[len(element)-1]) + " ML: " + str(len(element)-1) + ") "
            solutionString += startPoint
            guiFormatData['PathEndNodes'].append((element[0], element[len(element)-1]))
            guiFormatData['MoveLimits'].append(len(element)-1)
                                                 

        solutionString += "RE: " + str(len(s[1])) + " "

        redundantEdgeIdList = []

        for e in s[1]:
            redundantEdgeIdList.append(e.id)

        guiFormatData['RedundantEdgeIds'] = redundantEdgeIdList
 
        if len(s[1]) > 0:
            unusedEdgesStr = ""
            for ue in s[1]:
                unusedEdgesStr += "(" + str(ue.connectedNodes[0].id) + "-" + str(ue.connectedNodes[1].id) + ")"

            solutionString += "[" + unusedEdgesStr + "]"        

        if maxEdgeRedundancy < 0 or len(s[1]) <= maxEdgeRedundancy:
            numSolutionsListed = numSolutionsListed + 1
            guiFormatDataList.append(guiFormatData)
            print solutionString


    guiDataOutput = open('output.txt', 'wb')
    pickle.dump(guiFormatDataList, guiDataOutput, -1)
    guiDataOutput.close()

    if len(possibleSolutions) == 0:
        Warning("*** NO SOLUTIONS FOUND. ***\n")
        sys.exit(1)
    else:
        Message("\nFound " + str(len(possibleSolutions)) + " solutions. ")
        Message("\nListed " + str(numSolutionsListed) + " solutions. ")

 

if __name__ == '__main__':
    main(sys.argv[1:])
