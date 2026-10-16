---
layout: default
title: Lecture 7 - Matching Problems
parent: MIT 6.042J - Mathematics For Computer Science 
nav_order: 7
---

# Lecture 7 - Matching Problems
A matching problem is one in which you have to match two nodes together such that they fulfill some condition. Usually the condition is that one node can only be matched with one other node, or n other nodes. We can only match nodes that are connected by edges. The goal of the problem is to create the maximum number of such “matchings” as possible.

If you manage to include every node in the graph in your matching, we call it a perfect matching. So the size of the matching (the number of edges involved in the matching) will be |V|/2 (there will be half as many edges as nodes, since two nodes will be joined by 1 edge).

These matching problems find applications where we have to distribute load, like deciding which person should perform which task, which student is allotted which college during the centralized admission process according to his/her preferences, or for literally matching people up with something/someone, as on dating apps.

Sometimes the graph can be weighted, in which case we have to find the match with the minimum total weight. The weight of a matching M is defined as the sum of the weights on the edges of M.

The min weight matching for a graph G is a perfect matching for G with the minimum weight.

