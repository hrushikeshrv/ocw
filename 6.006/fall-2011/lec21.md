---
layout: default
title: Lecture 21 - Dynamic Programming 3
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 21
---

# Lecture 21 - Dynamic Programming 3: Parenthesization, Edit Distance, Knapsack
Dynamic programming is a powerful algorithm design paradigm that can be used to solve a variety of problems efficiently. In this lecture, we will explore three important applications of dynamic programming: parenthesization, edit distance, and the knapsack problem.

## Parenthesization
The parenthesization problem involves determining the optimal way to parenthesize a sequence of matrices to minimize the total number of scalar multiplications required to compute the product. The key idea is to use dynamic programming to find the optimal split points for the matrices.

Consider you have $n$ matrices $A_1, A_2, \ldots, A_n$ with dimensions $d_0 \times d_1$, $d_1 \times d_2$, ..., $d_{n-1} \times d_n$. The cost of multiplying two matrices $A_i$ and $A_j$ is given by the product of their dimensions: $d_i \times d_j \times d_k$, where $k$ is the index of the matrix that splits the multiplication. We want to find the optimal way to parenthesize the product of these matrices to minimize the total cost.

For example, if you have matrices $A_1, A_2, A_3$ with dimensions $n \times 1$, $1 \times n$, and $n \times 1$. Then it is better to multiply $A_2$ and $A_3$ first, as it results in just one scalar, and then multiply that scalar with $A_1$.

Let $DP[i, j]$ be the minimum cost of multiplying matrices from $A_i$ to $A_j$. The recurrence relation can be defined as follows:

$$ DP[i, j] = \min_{i \lt k \lt j }{\left(DP[i, k] + DP[k, j] + cost(A_i, A_k) + cost(A_k, A_j)\right)} $$

The base case is when $i = j$, where the cost is zero since there is only one matrix.