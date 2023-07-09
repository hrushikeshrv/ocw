# Lecture 7 - Synchronization 2: Semaphores, Lock Implementation
This lecture gives an intuition about how locks are actually implemented in an operating
system. We want an interface which lets us acquire a lock on a critical section of code,
run the critical section, and then release the lock. 

The simple implementation is described by the acquire and release pseudocode given below -

```
int value = FREE;   // Flag describing if the critical section is being executed or not
Acquire() {
    disable interrupts;
    if (value == BUSY) {
        put thread to sleep;
        enable interrupts;
    }
    else {
        value = BUSY;
    }
    enable interrupts;
}

Release() {
    disable interrupts;
    if (thread is sleeping on this lock) {
        wake up thread;
    }
    else {
        value = FREE;
    }
    enable interrupts;
}
```