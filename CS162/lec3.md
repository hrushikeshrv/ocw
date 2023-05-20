# Lecture 3 - Abstractions 1: Threads and Processes

## Multiprocessing vs. Multiprogramming
Multiprocessing vs. Multiprogramming is similar to the idea of concurrency vs. parallelism.
Multiprocessing is when you have multiple physical cores, and you use them to perform
operations at the same time completely independently. Multiprogramming is when you divide
a program into multiple jobs/processes/threads.

Concurrency is when you are _handling_ multiple things at once, not necessarily _doing_
them. Parallelism is when you do multiple things _simultaneously_.

## Threads
A thread can be in one of 3 states - running, ready, or blocked. A running thread is a
thread whose instructions are actually being executed, a ready thread is a thread that is 
waiting for CPU time, and can be swapped out with the current running thread, and a blocked
thread is a thread that is waiting for something to happen before it can run (typically i/o).

To write a multithreaded program in C, we usually use pthreads. The "P" in pthreads stands
for POSIX. POSIX is an attempt at standardizing the programming interface that different
operating systems provide to programs running in user mode.