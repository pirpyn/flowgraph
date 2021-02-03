#!/usr/bin/env python3

def display_graph(graph):
    """
        Display the graph as an adjacency matrix
    """
    for row in graph:
        print(row)

def create_graph(entrances,exits,path):
    """
        This will returns the graph as an adjacency matrix,
        with one source (row 0) and one sink (row len(path) + 2)
    """
    nrow = len(path)
    graph = [[0 for j in range(nrow+2)] for i in range(nrow+2)]

    # connect the main source to the sources with infinite capacity
    for source in entrances:
        graph[0][source+1] = -1

    # Add the connectivity flow 
    for irow, row  in enumerate(path):
        for ival, val in enumerate(path[irow]):
            graph[irow+1][ival+1] = val

    # connect the exits to the main sink with infinite capacity
    for sink in exits:
        graph[sink+1][nrow+1] = -1

    return graph

def is_connected(graph,source,dest,graph_mark=None,flowpath=None,maxflow=None):
    """
        returns true, flowpath, flow if there's a path from source to dest
    """
    # if graph_mark[i][j] = True then we already used that edge
    if graph_mark is None:
        graph_mark=[[False for j in range(len(graph))] for i in range(len(graph))]
    if flowpath is None:
        flowpath = []
    if maxflow is None:
        maxflow = 2000000
    found = False
    for j, val in enumerate(graph[source]):
        if j == source:
            continue
        if graph_mark[source][j]:
            continue
        graph_mark[source][j] = True
        if val != 0:
            if j == dest:
                flowpath.append(dest)
                found = True
            else:
                found, flowpath, maxflow = is_connected(graph,j,dest,graph_mark,flowpath,maxflow)
        if found:
            break
    if found:
        if val > 0:
            maxflow = min(maxflow,val)
        flowpath.insert(0,source)
    return found, flowpath, maxflow

def compute_flow(graph,source=0,sink=None):
    if sink is None:
        sink = len(graph)-1
    flow = 0
    found, flowpath, maxflow = is_connected(graph,source,sink)
    counter = 5
    while found and counter > 0:
        flow = flow + maxflow
        counter = counter - 1
        for i in range(len(flowpath)-2):
            graph[flowpath[i+1]][flowpath[i+2]] = graph[flowpath[i+1]][flowpath[i+2]] - maxflow
        found, flowpath, maxflow = is_connected(graph,source,sink)

    return flow

entrances = [0,1]
exits = [4,5]
path = [
    [0,0,4,6,0,0],
    [0,0,5,2,0,0],
    [0,0,0,0,4,4],
    [0,0,0,0,6,6],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
]

graph = create_graph(entrances,exits,path)

display_graph(path)

print("max flow is",compute_flow(graph))