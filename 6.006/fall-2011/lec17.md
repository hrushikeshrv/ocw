---
layout: default
title: Lecture 17 - Bellman-Form Algorithm
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 17
---

# Bellman-Ford Algorithm
Bellman-Ford should be able to-
1. Correctly calculate the (u,v) values for all vertices v that are not part of negative cycles and can be reached without encountering a negative cycle.
2. Mark all vertices which are part of a negative cycle or can be reached from a negative cycle as having a (u,v) value of undefined.
3. Mark all the vertices that cannot be reached from the start vertex as having a (u,v) value of infinity.

~~~
bellman_ford(G, w, s):
    for i in range(1, len(V)-1):
        # For all the vertices in the graph except the first and the last, do
        for edge in E:
            # For each edge in the set of edges
            # assume the edge goes from u to v
            relax(u, v, w)
    
    # Check for negative cycles
    for edge in E:
        # If we can relax further, that means that a -ve cycle exists, and we have just found one
        if d[v] > d[u] + w(u, v):
            print(“Negative weight cycle(s) exist”)
            return False
~~~
{: .language-python}

The first nested for loop would be $\Theta$(VE) and the second for loop would be $\Theta$(E), so the overall dominating complexity is $\Theta$(VE).