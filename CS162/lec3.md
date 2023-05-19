# Lecture 3 - Abstractions 1: Threads and Processes

## Multiprocessing vs. Multiprogramming
Multiprocessing vs. Multiprogramming is similar to the idea of concurrency vs. parallelism.
Multiprocessing is when you have multiple physical cores, and you use them to perform
operations at the same time completely independently. Multiprogramming is when you divide
a program into multiple jobs/processes/threads.

Concurrency is when you are _handling_ multiple things at once, not necessarily _doing_
them. Parallelism is when you do multiple things _simultaneously_.