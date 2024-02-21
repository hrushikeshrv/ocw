---
layout: default
title: Lecture 8 - Turing Degrees, Dovetailing, Godel
parent: MIT 6.045J - Automata, Computability, Complexity
nav_order: 8
---

# Turing Degrees, Dovetailing, Godel

In the last lecture we defined Turing degrees, which are basically sets of languages.
A Turing degree consists of a set of languages that can all be reduced to another 
language in the same set using a Turing reduction.

The set of computable languages is called degree 0. The set of languages equivalent
to the halting problem is just above degree 0. A natural question to now ask is are
there degrees between these two?

It turns out the answer is yes. There are infinitely many Turing degrees between 
degree 0 and the halting degree. What it means to be "between" these two degrees
is that if we have a language L in this intermediate degree, the following relation
holds -

$$ L \le {}_{T} HALT $$

$$ L \nle {}_{T} \text{degree} 0 $$

$$ HALT \nle {}_{T} L $$

This means that the language L is reducible to the halting problem. That is, you 
can build a Turing machine to recognize L given an oracle for the halting problem.
However, the language is not reducible to any language in degree 0, and the halting
problem is not reducible to language L.