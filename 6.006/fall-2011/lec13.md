---
layout: default
title: Lecture 13 - Breadth-First Search
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 13
---

# Lecture 13 - Breadth-First Search
BFS is a graph search algorithm that explores a graph one "level" at a time. It starts at some pre-defined start node and explores all the neighbours of that node. Then it moves on to the neighbours of the neighbours and so on. It is a very simple and intuitive algorithm that is used to find the shortest path in an unweighted graph. It runs in $O(V + E)$ time, where $V$ is the number of vertices and $E$ is the number of edges in the graph.

This is a simple implementation in Python:

~~~
def BFS(graph, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node])
    return visited
~~~
{:.language-python}

This is the Python code covered in the lecture that gives you the "level" of each node as well as the actual path in the form of parent pointers:

~~~
def BFS(start, graph):
    level = {start: 0}
    parent = {start: None}
    i = 1
    frontier = [start]
    while frontier:
        next = []
        for u in frontier:
            for v in graph[u]:
                if v not in level:
                    level[v] = i
                    parent[v] = u
                    next.append(v)
        frontier = next
        i += 1
    return level, parent
~~~
{:.language-python}