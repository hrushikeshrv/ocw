---
layout: default
title: Ford-Fulkerson Method
---

# Ford-Fulkerson Method
The Ford-Fulkerson method is a greedy algorithm used to compute the maximum flow in a flow network. A flow network is a directed graph with a source node that has edges coming out of it, and a sink node with edges going into it. We imagine a "flow" coming out from the source and going into the sink. The edges in a flow network are analogous to pipes and have a "capacity" representing the maximum flow they can accommodate. The problem we are trying to solve is to find the maximum amount of flow that can be sent from the source to the sink without exceeding the capacities of the edges.

It is called a method and not an algorithm because it does not specify how to find augmenting paths. Different algorithms can arise based on your choice of augmenting path search method. 

The most common implementations of the Ford-Fulkerson method are the Edmonds-Karp algorithm, which uses BFS to find augmenting paths, and the Dinic's algorithm, which uses DFS. The Ford-Fulkerson method is based on the following principles:

1. **Flow Conservation**: The amount of flow into a node is equal to the amount of flow out of that node, except for the source and sink nodes.
2. **Capacity Constraint**: The flow on an edge cannot exceed its capacity.

# Algorithm
The idea behind the Ford-Fulkerson method is to find any path from the source to the sink. Once we find a path $P$, we send the maximum amount of flow that can be sent through that path, which is the value of the edge with the smallest capacity.