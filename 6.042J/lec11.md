---
layout: default
title: Lecture 11 - Relations, Partial Orders, Scheduling 
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 11
---

# Lecture 11 - Relations, Partial Orders, Scheduling

## Relations

A relation R between 2 sets A and B is a set of tuples (a, b) such that R is a subset of the cross product of A and B.

$R \subseteq A \times B$

We denote a relation between the sets A and B by the symbol aRb or a R b.

### Properties of relations

1. A relation is reflexive if $xRx ~\forall~ x \in A$
2. A relation is symmetric if $ x \sim_R y \land y \sim_R x ~\forall~ x,y \in A$
3. A relation is antisymmetric if $x \sim_R y \land y \sim_R x ~\text{iff}~ y = x$
4. A relation is transitive if $x \sim_R y \land y \sim_R z$ then $x \sim_R z ~\text{if} ~x,y,z \in A$