---
layout: default
title: Lecture 5 - Binary Search Trees, BST Sort
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 5
---

# Binary Search Trees, BST Sort
## Scheduling problem   
Imagine we have an airport with 1 runway that needs to schedule the landing and take off times of a lot of planes. We start at t = 0, and increase time monotonically. No plane can land or take off $k$ minutes within any other plane. We have to write an algorithm to take as input a landing/take off time and insert it into a table of landing/take off times if it is a valid time.

There are a variety of data structures we could use to solve this problem, but the optimal data structure is a binary search tree. A BST can solve this problem in $O(log\,n)$ time, while an unsorted or even sorted array needs at least linear time. This is because it would take us linear time to check if the given time is valid for an unsorted array, and it would take us log n time to check for validity but would take us linear time to insert for a sorted array. Heaps also don’t work because finding the insertion point would take $O(n)$ time.

## BST Specifications
A BST structure has nodes. Each node has a parent pointer, a left child pointer, and a right child pointer. A BST maintains the invariant that any descendant node in the left subtree of an ancestor has a eky less than or equal to the key of the ancestor, and any descendant node in the right subtree of an ancestor has a key greater than or equal to the key of the ancestor.

However, a vanilla BST doesn't always solve the scheduling problem with $O(log\,n)$ time. It solves the problem in $O(h)$ time, where $h$ is the height of the tree. In some cases, $h$ can be $log\,n$, but as you keep on inserting into the tree, there is a high probability that $h$ will be much greater than $log\,n$ and approach n. This still leads to an $O(n)$ complexity in the long run. However, there are some operations that are still useful on a BST.

## BST Methods
1. find_min() - finding the minimum element of the tree takes $O(h)$ time, just keep going towards the left child starting from the root. The leftmost child of the tree (which is a leaf) will be the minimum element of the tree.
2. find_max() - same as find min, just keep going right.
3. next_larger() - finding the smallest element larger than a given x. Do binary search. $O(h)$ time.
4. next_smaller() - same as next_larger. $O(h)$ time.
