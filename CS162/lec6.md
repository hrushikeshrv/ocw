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

## Context Switching
When the scheduler decides to run a thread, it essentially gives up control of the CPU 
to the process it decided to run. It needs some way to get that control back from the process.

This can happen because of internal events, i.e. the thread yields control voluntarily, or
because of external events like interrupts. The POSIX API provides a syscall `ptherad_yield()`
or `sched_yield()`, that give up control of the CPU.

When a process yields, it goes into the kernel, tells the scheduler to run a new thread, and then 
performs a context switch. The context switch basically saves the state of all registers and the stack
of the first thread/process into the TCB/PCB, and loads in the registers and the stack of the 
new thread/process.

Switching between threads is much faster than switching between processes (about 30x faster).