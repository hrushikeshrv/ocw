# Lecture 2: Four Fundamental OS Concepts

This lecture introduces four fundamental concepts of an operating system -
1. Threads: Execution Context
2. Address Spaces
3. Processes
4. Dual mode operation

## Threads
A thread is a single unique execution context that has its own program counter, 
registers, execution flags, stack, and so on. This means that the block diagram 
you have studied for how a processor executes a program is really one single 
thread executing its own code.

<img src="media/lec2-1.png" alt="Instruction execution cycle">

A thread is said to be executing when it is "resident" in a core. Resident means
that the PC of the core is pointing at the next executable instruction for the 
thread and the instructions of the thread are stored in memory. A resident thread's 
stack pointer holds the address of the top of the stack for that thread.

A thread is said to be suspended when its data (everything we have seen above) is
not in memory.

The OS gives the user the illusion of multiple processors by multiplexing the 
execution of threads in time. All threads that want to run on the processor
are stored in a chunk of memory called the Thread Control Block, and the data
for each thread is swapped in and out of the hardware registers over time.

Swapping out the data of one thread for another takes some time, which is called
context switching. We have to be careful not to swap between executing threads
so often that majority of the time is spent in context switching, since the 
more context switching we perform, the more time is "wasted". However, if we don't
context switch fast enough, we might get the feeling that our machine is unresponsive,
since only one process would be running on the CPU for a long time, making all other
processes hang.

Context switching can also happen because the thread voluntarily gave up control,
or it asked for some i/o, and so on.