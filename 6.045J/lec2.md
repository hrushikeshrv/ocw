# Lecture 2 - Logic, Circuits, and Gates
## Gates and Universality
This lecture introduces the fundamental logic gates - AND, OR, and NOT, and then talks about 
their universality.

Universality in this case means that we can construct any boolean function using a combination 
of these gates. In computer science, universality is the norm, and most sets are usually universal.
You have to work a little to get a set that is not universal. Some examples for non-universal sets
in logic gates are - $ \{AND, OR\} $, $ \{XOR, NOT\} $.

This is because AND gates and OR gates are monotonic functions. That is, changing one of the inputs
from a 0 to a 1 can only change the output from a 0 to a 1, or leave it unaffected. Whereas to 
represent a NOT gate, we would need to change the output from a 1 to a 0 when the input went
from 0 to 1, which is not possible to do with monotonic gates.
