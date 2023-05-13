# Turing Recognizability, Oracles

## Turing Recognizability
We now define a new kind of language, a Turing Recognizable language - very similar
to a decidable language, with one key difference.

A Turing Recognizable language is a language for which we can construct a Turing
Machine such that, for all inputs in the language, the Turing Machine halts and accepts,
and for all inputs not in the language, the Turing Machine either halts and rejects
or goes into an infinite loop.

The only difference between a decidable and recognizable language is the very last
clause, which allows the machine to go into an infinite loop. This means that the halting 
problem can be phrased in terms of a Turing Recognizable language.

$ HALT = \{\<M\>,x : M halts on x\} $

We can clearly see that for all strings in the language, we can construct a Turing machine 
to either halt and accept (just run M on x), or go into an infinite loop (just run M on x again,
and it will go into an infinite loop if x is not in the language).

We have now seen a few classes of languages of increasing generality, shown in the diagram below -

<img src="media/lec7-1.png" alt="Classes of languages">

As you would expect, the halting problem is in the set of recognizable languages but not
in the set of decidable languages. Now if we define a new language, $\overline{HALT}$,
which is the _complement_ of $HALT$, it lies even outside the class of recognizable languages.

## Reductions
Reductions are a way of solving a problem that you don't know how to solve using
a solution to a problem that you do know how to solve. Reductions were seen before
in [6.006](../6.006/index.md) and [6.046](../6.046/index.md). Reductions are seen 
everywhere in computer science, and are especially useful while proving the NP-completeness
(or incompleteness) of some problem. Similarly, you can also use them to show that some 
problems are decidable or undecidable.

Formally, we represent a reduction as $ A \le {}_{T} B $, where the T stands for 
Turing reducibility. This denotes that problem A can be reduced to problem B, where
A is the problem that we want to solve, and B is the problem that we know how to solve.

We can also write this as - `$A$ is decided by $M^B$`, where we call B an "oracle", 
because we get to assume that the Turing Machine M has access to Turing Machine B,
which already knows how to solve its own problem
