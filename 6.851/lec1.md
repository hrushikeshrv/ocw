---
layout: default
title: Lecture 1 - Persistent Data Structures
parent: MIT 6.851 - Advanced Data Structures
nav_order: 1
---

# Lecture 1 - Persistent Data Structures
The first two lectures discuss temporal data structures, which are data structures that allow you to access past versions of the data structure. This is useful for applications like undo functionality in text editors or version control systems. It is kind of like a time machine for data structures.

The first lecture introduces the concept of persistent data structures, which are data structures that preserve their previous versions when modified, and for which you can access any version at any time.

## Types of Persistence
There are four types of persistence:

1. **Partial Persistence**: You can access any version of the data structure, but you can only modify the most recent version. This means that the versions are ordered linearly.
2. **Full Persistence**: You can access any version and modify any version. This means that the versions form a tree structure, where each version can have multiple children.
3. **Confluent Persistence**: You can access any version and modify any version, and you can also merge two versions together. This means that the versions form a directed acyclic graph (DAG) structure, where each version can have multiple parents.
4. **Functional Persistence**: This is a special case of full persistence where the data structure is immutable, meaning that once it is created, it cannot be modified. Instead, you create a new version of the data structure with the modifications.

We will look at how to implement partial and full persistence, and discuss features of confluent and functional persistence, but some aspects of confluent and functional persistence are still open problems.

