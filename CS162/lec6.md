# Lecture 6: Synchronization 1: Concurrency, Mutual Exclusion

## Concurrency
One of the most important and central parts of the operating system is the scheduler.
The scheduler maintains a queue of the active processes in the system and chooses which
process gets to go next.

The scheduler maintains a data structure containing the process control blocks, and distributes
CPU time to the different PCBs it contains according to some policy. It can also distribute
access to other hardware resources like memory, IO, etc.

The lifecycle of a process is shown in the diagram below -

<img src="media/lec6-1.png" alt="Lifecycle of a process/thread">

The pseudocode of the scheduler basically looks like this -

```
while (1) {
    RunThread();
    ChooseNextThread();
    SaveStateOfCPU(currPCB);
    LoadStateOfCPU(nextPCB);
 }
```

One can even argue that this is all that the operating system does.