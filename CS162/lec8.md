# Lecture 8 - Synchronization 3: Atomic Instructions, Monitors, Readers/Writers

The previous lock implementation we saw was impractical because it involved a system
call every time we wanted to acquire or release a lock. A system call is at least 25x
more expensive than a normal function call, so this approach limited our performance
severely.

What we need is just to be able to read a value (of the lock), check if it is 0 or 1,
and then write to the value atomically. If we removed the need to disable and re-enable 
interrupts for this operation, we would be able to implement locks at the user level.

Therefore, all architectures provide atomic instructions for this purpose. These instructions
can read, modify, and write data atomically, such that they cannot be interleaved. Some of
these instructions are -

```
// Return the value stored at address, and store a 1 there
test&set(&address) {
    result = M[address];
    M[address] = 1;
    return result;
}

// Swap "value" with value stored at address
swap(&address, value) {
    temp = M[address];
    M[address] = value;
    value = temp;
}

// If value at address == reg1, store reg2 there and return success, else failure
compare&swap(&address, reg1, reg2) {
    if (reg1 == M[address]) {
        M[address] = reg2;
        return success;
    }
    else return failure;
}
```

## Implementing Locks With test&set
The lecture gives a few ways in which we can implement locks using `test&set()`, but I won't 
write about them here because they are very intuitive to come up with but result in busy waiting, so we don't
use those implementations anyway.