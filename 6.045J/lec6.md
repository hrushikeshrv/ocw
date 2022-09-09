# Decidability
An important theorem regarding Turing machines is that a Turing machine can simulate other Turing 
machines, which can potentially be more complicated than itself. That is, a Turing machine A can
act as an _interpreter_ for Turing machine B, and B can be much more complicated than A.

Alan Turing actually gave such an example of an interpreter in his 1936 paper, but it turned out to 
have a mistake, so he had to publish a correction in 1937. Regardless, it can be done.

## Halting Problem
A question you might have now is what can Turing machines not do? One famous example of a problem
Turing machines can't solve is the halting problem - given a description of a Turing machine, return 
whether the machine will halt on an empty input.

For some Turing machines (and some computer programs), we can easily tell if the machine will halt
or get stuck in an infinite loop. However, we cannot know that for sure for all Turing machines.

If we did know how to solve the halting problem, we would also be able to solve many unsolved 
problems in mathematics, like the Reimann hypothesis, or Goldbach's conjecture.

The proof that we can't solve the halting problem is given by contradiction as follows. Say you have
a Turing machine P that takes the description of a Turing machine as input and tells you whether the 
input will halt on an empty input. This is not a special case, as we can always convert a Turing
machine that takes some non-empty input into another Turing machine that takes an empty input
but performs the same operations as the first Turing machine on the specific non-empty input.

Now, say we have another machine Q that takes the description of a Turing machine M, runs P on it, 
and goes into an infinite loop if M halts, and halts if M loops. If we pass the description of Q into
Q itself, we get a paradox. Therefore, we contradict ourselves and we cannot have a Turing machine P.

- busy beaver