BFS graph solver
============

This tool takes an xml constructed graph and finds all possible paths between home nodes for a set amount of graph travellers using Breadth-first search algorithm. A "home node" is defined as a starting point for each traveller, so if the graph has 3 home nodes called A,B,C and 2 travellers called X,Y, then the solver will find all possible paths between all home nodes for all possible traveller placements. The search is performed using Breadth-first search algorithm and depending on the parameters (size of graph, number of home nodes and travellers) it may take quite a while to find all possible solutions (by default a limit on number of solutions is set which you can disable using <code>--limit 0</code>).

By default the algorithm passes through each node only once, so no "cyclic" solutions are taken into account. You can use a flag to switch to "cyclic-BFS" variant which disable this constraint.

For detailed usage information run <code>solver.py</code> with no cmd line arguments. <code>start.bat</code> launches the GUI, which requires wxPython installed on your computer.

Usage (cmd line)
------

<code>python solver.py -filename=graph.xml</code>

where: graph.xml - contains a graph representation in xml format

or simply run:
<code>python solver.py</code>

for a proper help message.
