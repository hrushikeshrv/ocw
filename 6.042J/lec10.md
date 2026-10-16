---
layout: default
title: Lecture 10 - Graph Theory 3 
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 10
---

# Lecture 10 - Graph Theory 3
## Overview

1. Euler tours
2. Directed graphs
3. Tournament graphs

## Euler Tours

An Euler tour of a graph is a special kind of walk in a graph that traverses every edge in a graph exactly once and ends at the same vertex that it started from.

### Theorem

A graph has an Euler tour iff the degree of all the vertices in the graph is even.

The proof of this theorem is of two parts, since we have to prove the forward and the backward implication. The forward implication is true because we must leave each node we arrive at, so edges to and from a node come in pairs. Therefore the degree of each node is 2 (this is a very informal proof). The reverse implication can be proved similarly, not as hard as it looks.

## Directed Graphs

### Definitions

* The tail of an edge is the vertex from which the edge originates
* The head of an edge is the vertex to which the edge goes
* The indegree of a vertex is the number of edges that come to that vertex
* The outdegree is the number of edges that start from that vertex