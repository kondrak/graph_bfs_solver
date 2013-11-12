graph_bfs_solver
============

Solver utility for The Graph Game prototype. I can't post it here, but checkout http://www.gameshot.org/?id=4147 to get the idea.

This tool takes an xml constructed graph (format used by the prototype and additional tools) and finds all possible paths between home nodes for a set amount of graph travellers using Breadth-first search algorithm. A "home node" is defined as a starting point for each traveller, so if the graph has 3 home nodes called A,B,C and 2 travellers called X,Y, then the solver will find all possible paths between all home nodes for all possible traveller placements. The search is performed using Breadth-first search algorithm and depending on the parameters (size of graph, number of home nodes and travellers) it may take quite a while to find all possible solutions (by default a limit on solution number is set which you can disable using cmd line parameters).

By default the algorithm passes through each node only once, so no "cyclic" solutions are taken into account. You can use a flag to switch to "cyclic-BFS" variant which disable this constraint.

For detailed usage information run solver.py. Start.bat launches the GUI, which requires wxPython installed on your computer.

Example usage (cmd line):
python solver.py -filename=graph.xml