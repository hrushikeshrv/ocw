---
layout: default
title: Breadth First Search (BFS)
parent: Algorithm Index
---

# Breadth First Search (BFS)
BFS is a simple graph traversal algorithm that explores all vertices of a graph reachable from the source. It has the following common applications:

1. Finding the shortest path between two nodes in an unweighted graph
2. As a subroutine in the [Ford-Fulkerson]({% link algorithms/ford-fulkerson.md %}) method to compute the max flow in a flow network
3. Testing the bipartite-ness of a graph

# Algorithm
The idea behind BFS is to explore/visit all the neighbours of a node before moving on to the next level of nodes. We maintain a queue of nodes to process. We start from the root node, mark it as visited, and then add all of its neighbours that are not yet visited into the queue to be explored. We repeat this process as long as there are nodes in the queue.

# Runtime Complexity
The runtime complexity of BFS is $O(V + E)$, where $V$ is the number of vertices and $E$ is the number of edges in the graph. This is because we visit each vertex once and check each edge once.

# Pseudocode
```
procedure BFS(G, root) is
    let Q be a queue
    label root as explored
    Q.enqueue(root)
    while Q is not empty do
        v := Q.dequeue()
        if v is the goal then
            return v
        for all edges from v to w in G.adjacentEdges(v) do
            if w is not labeled as explored then
                label w as explored
                w.parent := v
                Q.enqueue(w)
```

# Implementation
```python
from collections import deque

def bfs(graph, root, process=None):
    """
    Visits all nodes in a graph using BFS
    """
    visited = set()
    queue = deque([root])
    visited.add(root)

    while queue:
        node = queue.popleft()
        if process:
            process(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited
```