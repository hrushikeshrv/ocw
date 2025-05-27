---
layout: default
title: Ford-Fulkerson Method
parent: Algorithm Index
---

# Ford-Fulkerson Method
The Ford-Fulkerson method is a greedy algorithm used to compute the maximum flow in a flow network. A flow network is a directed graph with a source node that has edges coming out of it, and a sink node with edges going into it. We imagine a "flow" coming out from the source and going into the sink. The edges in a flow network are analogous to pipes and have a "capacity" representing the maximum flow they can accommodate. The problem we are trying to solve is to find the maximum amount of flow that can be sent from the source to the sink without exceeding the capacities of the edges.

It is called a method and not an algorithm because it does not specify how to find augmenting paths. Different algorithms can arise based on your choice of augmenting path search algorithm. 

The most common implementations of the Ford-Fulkerson method are the Edmonds-Karp algorithm, which uses BFS to find augmenting paths, and the Dinic's algorithm, which uses DFS. The Ford-Fulkerson method is based on the following principles:

1. **Flow Conservation**: The amount of flow into a node is equal to the amount of flow out of that node, except for the source and sink nodes.
2. **Capacity Constraint**: The flow on an edge cannot exceed its capacity.

By the max-flow min-cut theorem, the maximum flow in a flow network is equal to the capacity of the minimum cut that separates the source and sink. A cut is a partition of the vertices into two disjoint subsets such that the source is in one subset and the sink is in the other. The capacity of a cut is the sum of the capacities of the edges crossing from the source side to the sink side.

The Ford-Fulkerson method can also be used to find the min-cut of a graph. We simply run the algorithm to find the max flow. Once the max flow has been found, we run a [BFS]({% link algorithms/bfs.md %}) or [DFS]({% link algorithms/dfs.md %}) from the source in the residual graph. The vertices reachable from the source in the residual graph form one side of the cut, and the other side consists of all vertices not reachable from the source.

# Algorithm
The idea behind the Ford-Fulkerson method is to find any path from the source to the sink. Once we find a path $P$, we send the maximum amount of flow that can be sent through that path, which is the value of the edge with the smallest capacity. We then replace the edges in the path with their residual capacities (if they have any capacity left), and add an edge going in the reverse direction with a capacity equal to the flow we just sent. We repeat this process until there are no more augmenting paths from the source to the sink.

# Runtime Complexity
The runtime complexity of the Ford-Fulkerson method depends on the method used to find augmenting paths. If we use BFS to find augmenting paths, the complexity is $O(VE^2)$, where $V$ is the number of vertices and $E$ is the number of edges in the graph. If we use DFS, the complexity can be as bad as $O(E^3)$ in some cases.

# Pseudocode
```
While there is a path $p$ from $s$ to $t$ in the residual graph $G_f$:
    Find the minimum capacity $c_{min}$ of the edges in path $p$
    For each edge $(u, v)$ in path $p$:
        Decrease the capacity of edge $(u, v)$ by $c_{min}$
        Increase the capacity of edge $(v, u)$ by $c_{min}$
Return the sum of flow coming out from the source $s$ as the max flow
```

# Implementation
```python

```