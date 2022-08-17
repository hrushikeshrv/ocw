# Hashing with Chaining
## Dictionaries
Dictionaries in python are an implementation of hash tables. A hash table is an ADT which has the following specifications -
1. Insert a value at a given key - should be $O(1)$ time
2. Delete a key from the table - should be $O(1)$ time
3. Search if a key exists in the table - should be $O(1)$ time

Hash tables are used in a variety of applications from cryptography, to document distance, to programming compilers, and much more. Given the specifications above, one naive way to implement hash tables is to use a normal array as the data structure, limit the keys to be non-negative integers, and treat the keys as indices into the array. This would give us constant time search, insert, and delete.

There are 2 problems with this approach - the keys are limited to non negative integers, and that if the possible space of keys is huge but there aren’t many items in the dictionary, then a huge amount of space is wasted. There is also a bottleneck when initializing a giant array in memory, but that problem is secondary.

We can solve the first problem by just using a hash function. Python has a `hash()` function which returns the prehash of its argument. By default, if the argument is an integer, it just returns that integer. If the argument is a custom object, then it uses the `__hash__()` magic method to compute the hash. If the `__hash__()` method is not implemented then it just returns the `id` of the object, which is its position in memory.

Hash functions should not change value over time. This means that the hash of a value should not depend on time. This also means that you cannot use mutable objects (like lists) as keys in python dictionaries, because there is a good chance that the list you are using as a hash changes value. This solves the first problem. This is actually prehashing.

To solve the second problem of unused space, we use hashing. Let the space of all possible keys be K. Let the number of elements/keys that exist in the hash table be n. We can then limit our array to be of some size m such that $m = \Theta(n)$. This would limit the space that the array takes up in memory so that we no longer hog space, and it would make sure that we still have some room to insert and delete items. However, since there are now only m spaces in our hash table, the hash function will need to map K keys to m slots, which means that there will be a lot of collisions since K >> m. We can solve this problem in 2 ways - by chaining or by open addressing.

## Chaining
Chaining is a way to deal with collisions that occur during hashing. If the hash function gives you 2 keys that map to the same address, we just store both of the keys in a linked list. All the items that map to the same address are just stored in a linked list (or normal list/array) at that address.

One disadvantage of chaining is that you could get really unlucky and map all of the keys that you have into the same address, which would reduce your entire hash table to just a single list. However, the probability of that happening is satisfactorily small. A good hash function randomizes things enough that this almost never happens, so in practice, the length of the list at each address is constant.

## Simple Uniform Hashing
Simple uniform hashing is an assumption we make about our hashing function to analyze the complexity of the operations we can perform on our hash table. Simple uniform hashing states that any key has an equal chance of being hashed to any address in the table and the hash of any key is independent of the hash of the other keys.

This assumption is not completely true, in particular the second part about the hash function being independent, but the analysis that we can do using this assumption is correct.

If there are n items in the table, and there are m slots in the table, then the average length of the linked list at each address is n/m. If m = $\Theta$(n), then n/m = $\Theta$(1). This number is called $\alpha$, the load factor of the table. As long as $\alpha$ is $\Theta$(1), hashing with chaining is a good idea, since the complexity of insert and delete would still be O(1), but the complexity of search is O(1 + $\alpha$), which is constant if $\alpha$ is $\Theta$(1).

## Hash Functions
A hash function does not convert any arbitrary object into an integer. That is the pre-hash function. A hash function maps keys from the giant possible space of keys K to a small subset of keys m. It takes as input an integer which could be any integer from the set K and outputs another integer in set m. A few example of hash functions are -

1. Division method - Just take the modulus(m) of the integer you are given.

~~~
def division_hash(x, m):
    return x % m
~~~
{: .language-python} 

This gives you an integer between 0 and m. This method is not too good because the performance of this hash function depends on our choice of K and m. It performs well in practice when m is prime or at least not a power of 2 or 10, but this solution does not seem so robust.

2. Multiplication method - The multiplication method feels a lot more like hashing.

~~~
def multiplication_hash(x, m):
    a = os.environ.get(‘a’)
    w = os.environ.get(‘w’)
    r = math.log2(m)
    return ((a*x) % 2**w) >> (w-r)
~~~
{: .language-python}

Here a is any random number that we choose for our hash function, and w is the word size for our machine. ‘r’ is log<sub>2</sub>m. The reason this works is as follows - a$\cdot$x first gives us a number that is 2 words long (since multiplying two words will give us a number that is two words long). This number is randomized because a is random. Taking the modulus to the base 2<sup>w</sup> gets rid of the upper half bits. Shifting the number to the right by (w-r) bits leaves us with r bits, which is a number between 0 and m-1.

3. Universal hashing - Universal hashing is used in practice and is a good hash function.

~~~
def universal_hash(x, m):
    a = os.environ.get(‘a’)
    b = os.environ.get(‘b’)
    p = os.environ.get(‘p’)
    return ((a*k + b) % p) % m
~~~
{: .language-python}

Here p is a big prime number, larger than the size of your universe of keys, and a and b are any random numbers between 0 and p. Using linearity of expectation and a similar technique which we used to prove that simple uniform hashing gave us a reasonable hash function, we can prove that universal hashing gives us a O(1) time hash table implementation.