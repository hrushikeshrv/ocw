---
layout: default
title: Lecture 15 - Single Source Shortest Paths Problem
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 15
---

# Lecture 15 - Single Source Shortest Paths Problem
This lecture discusses the single source shortest paths problem and presents the general strategies algorithms follow to solve it.

The single source shortest paths problem is defined as follows: given a graph $G = (V, E)$ and a source vertex $s \in V$, find the shortest path from $s$ to every other vertex in $V$.

## General Strategies
Given that your graph does not have any negative weight cycles, there is a general approach to solve the single source shortest paths problem:

```
Initialize the distance of the source vertex to 0 and the distance of all other vertices to infinity.
Repeat until no more updates are possible:
    For each edge (u, v) in E:
        Relax the edge (u, v)
```

"Relaxing" an edge means updating the distance of the destination vertex $v$ to the minimum of its current distance and the sum of the distance of the source vertex $u$ and the weight of the edge $(u, v)$.

```python
if d[v] > d[u] + w(u, v):
    d[v] = d[u] + w(u, v)
```