# Lecture 3 - Finite State Automata & Regular Languages

## Finite Automata
A finite automata is the same as a finite state machine. It has a finite set of states
that it can be in, and it takes input from a set called its alphabet. It has a transition
function that takes one alphabet and the current state as input and transitions to the next
state.

The notation we will use for these quantities is the following -

| $ Q $ | Finite set of states |  
| $ \Sigma $ | Finite alphabet |  
| $ \delta: Q \times \Sigma \rightarrow Q $ | Transition function |  
| $ q_0 $ | Start state |
| $ F \subset Q $ | Accepted states |

We call $ L = \{{0, 1}\}^{*} $ a _language_. In this case, a language is the set of all binary
strings of length 0 or more. A language is just any set of strings. We say that a language is 
_accepted_ or _recognized_ by an automaton if the automaton ends up in an accepting state for 
all strings in the language, and we denote that as $ L(M) $, meaning $L$ is a language recognized 
by the finite automaton $M$. We say that $L$ is a _regular_ language if we can design an automaton
to accept that language.