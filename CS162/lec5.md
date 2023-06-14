# Lecture 5: Abstractions 3: IPC, Sockets

## IPC
IPC stands for inter-process communication. The process model we have seen so far
is specifically designed so that one process is not able to affect another in any way.
This is by design, but it does make inter-process communication more difficult.

Therefore, we have to have a specialized way for two processes to communicate with
each other, if both processes agree. One initial idea may be to communicate through
reading and writing to files that are shared by processes. We have seen that forking
a process creates file descriptors that are shared by both the parent and the child,
so maybe one process can write to a shared file descriptor, and another process
could read from it. The drawback to this approach is, as you might imagine, efficiency.
Communicating with disk is really slow, and this approach becomes completely impractical 
as the number of processes increases.

The approach we use is to have an in-memory queue maintained by the kernel, which provides
the same POSIX interface for reading and writing as reading and writing to a file. This is
called a "pipe". You can create a pipe using the `pipe(int filedes[2])` syscall.