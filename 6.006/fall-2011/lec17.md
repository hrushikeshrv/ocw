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

## Proof of Correctness
Let $v$ be a vertex in the graph $G$, and let a path $p = \langle v_0, v_1, v_2, \ldots, v_k \rangle$ be a simple shortest path from $s$ to $v$. Then $k \leq |V|-1$, because any simple path cannot visit a vertex more than once, and there are $|V|$ vertices in the graph.

Now, during every iteration of the outer for loop, we relax all the edges in the graph. This means that after the first iteration, we relax the edge $\langle s, v_1 \rangle$ at some point. This means that we have found the shortest path from $s$ to $v_1$, since it is a subset of a shortest path from $s$ to $v$, which means it is also a shortest path by itself. Similarly, after the $k$th iteration, we will have found the shortest path upto $v_{k-1}$. This means that by $|V|$ iterations, we will have found the shortest path from $s$ to $v$.

However, there could be negative weight cycles in the graph. To detect these, we run one more iteration. If we notice that we can still relax an edge, that means that there is a negative weight cycle in the graph. This is because if we can still relax an edge, it means that the shortest path from $s$ to $v$ can be made shorter by going through the negative weight cycle. In that case, we fail and stop.