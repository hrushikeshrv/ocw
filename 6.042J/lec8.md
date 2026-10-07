---
layout: default
title: Lecture 8 - Graph Theory 2 - Minimum Spanning Trees 
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 8
---

# Lecture 8 - Graph Theory 2 - Minimum Spanning Trees
## Definitions
- A walk is defined as a sequence of edges joining one vertex to another.
- A path is a special case of a walk in which each vertex appears only once.
- We call a graph connected if every vertex is reachable from every vertex in the graph.
- A closed walk is a walk which starts and ends at the same vertex.
- A cycle is a closed walk in which all vertices are distinct.
- A tree is defined as a graph that is connected and that does not have cycles or closed walks. (A connected and acyclic graph)
- A spanning tree is a tree which is a subgraph of a connected graph which is connected to all the vertices in the graph. In other words, a spanning tree is a selection of edges from a connected graph that is connected to all the nodes in the original graph. A spanning tree satisfies the tree condition and is connected to all the nodes in the graph.
- A minimum weight spanning tree is a spanning tree in a weighted graph that has the minimum weight. The weight of the tree is just the sum of weights of the edges of the tree.

## Lemmas
1. It is always possible to construct a path from a walk. (Proven by contradiction)
2. A subgraph of a tree is also a tree. (Proven by contradiction)
3. In a tree with n vertices, there exist n-1 edges. (Proven by induction)
   a. 3 $\implies$ there are |V| - 1 edges in all connected acyclic graphs. (undirected)
4. It is always possible to construct a spanning tree from a connected graph. (Proven by contradiction)

## Minimum Spanning Tree Problem
A minimum spanning tree of an edge weighted graph G is defined as a spanning tree of G such that it has the smallest possible sum of edge weights. The minimum spanning tree problem can be solved with a simple greedy algorithm.

The algorithm can be summarized in a single line -
Keep choosing edges of the graph with minimum weights as long as you don’t create any cycles.
