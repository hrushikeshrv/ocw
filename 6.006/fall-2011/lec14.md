---
layout: default
title: Lecture 14 - Depth-First Search, Topological Sort
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 14
---

# Lecture 14 - Depth-First Search, Topological Sort
Depth-First search is a fundamental algorithm for traversing or searching tree or graph data structures. It starts at the root node and explores as far as possible along each branch before backtracking. It does visit all nodes reachable from a vertex, but tt does not find shortest paths. However, it has a few properties that make it useful in other applications.

~~~
def dfs_visit(graph: dict[str, list[str]], start: str, parents={}):
    """
    Recursively visit all nodes in the graph starting from the given node.
    """
    for neighbor in graph[start]:
        if neighbor not in parents:
            parents[neighbor] = start
            dfs_visit(graph, neighbor, parents)

def dfs(graph: dict[str, list[str]]):
    """
    parents = {}
    for node in graph:
        if node not in parents:
            parents[node] = None
            dfs_visit(graph, node, parents)
~~~
{:.language-python}

## DFS Edge Classification
DFS can be used to classify edges in a graph. There are four types of edges in a graph:
1. **Tree edges**: Edges that are in the DFS tree (formed by the parent pointers).
2. **Back edges**: Edges that point from a node to one of its ancestors in the DFS tree.
3. **Forward edges**: Edges that point from a node to one of its descendants in the DFS tree.
4. **Cross edges**: Edges that do not fall into any of the above categories.

These edges can be used to detect cycles in a graph. If there is a back edge in the graph, then there is a cycle in the graph. This gives us a simple algorithm for cycle detection. We just run DFS on the graph and check if there are any back edges.

## Topological Sort
Topological sort is an ordering of the nodes in a directed acyclic graph (DAG) such that for every edge $(u, v)$, $u$ comes before $v$ in some ordering that we care about. Topological sort can be used to solve a variety of problems, such as scheduling tasks with dependencies, and solving linear programming problems. For task scheduling with dependencies, it makes sure that all tasks that depend on other tasks are only done after the tasks they depend on are completed.

All we have to do to get a topological ordering is to run DFS on the graph and output the nodes in reverse order of when they finish. This is because the nodes that finish last are the ones that have no outgoing edges, and thus can be done first.