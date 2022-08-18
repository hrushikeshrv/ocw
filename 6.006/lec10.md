# Open Addressing, Cryptographic Hashing
## Open Addressing & Probing
Open addressing is another method of dealing with collisions in a hash table. Instead of simply chaining collisions, we use the notion of probing to compute a slightly different hash if the first hash caused a collision.

We modify our hash function, h, a little such that it now takes the universe of keys as well as the ‘trial count’, which is an integer between 1 and m-1, as input and returns an integer between 1 and m-1 as output. Also, we have to make sure that the set of hashed values {h(k,1), h(k,2), ..., h(k,m-1)} is a permutation of {0, 1, 2, ..., m} so that each item has an opportunity to be hashed into any slot of the table.

Inserting into this table would then involve first hashing the given key into a slot. If that slot is occupied, we hash again by incrementing the trial count, otherwise we insert the item into the slot we found. We store each item in the table as a tuple of the form (key, value), where key is the original key from the universe of keys, and value is the value to be stored at that key. This is to make search possible.

Searching for a key ks in this table would then involve two steps. We hash ks into a slot and look at the key stored in that slot. If that key is not ks, we hash ks once more by incrementing the trial count. This then hashes ks into a new slot. If we look at the new slot and find that ks is indeed stored in that slot, we return the value stored in that slot. Otherwise, if we find an empty slot, we conclude that ks does not exist in the table.

This approach would work if we were not deleting any keys. However, if we inserted a key into a slot after, say, the third trial, and we end up deleting the item stored at the key we hashed into in the second trial, search would wrongly return that the key we are searching for does not exist.

To fix this we introduce a “deleted” flag. When we delete a key from the table, we replace it with a `(deleted, value)` tuple instead of the `(None, value)` tuple. Then, during search, if you encounter a deleted flag you just keep going and treat it as an occupied slot. During insert, we treat the deleted flag the same as None and overwrite the value stored in that slot.

## Choosing a Hash Function
We now need to choose a good hash function that will take the trial count as an additional input and produce an integer between 0 and m-1. It also needs to produce a permutation of {0, 1, …, m-1} as the trial count goes from 1 to m.

A bad hash function to use would be

~~~
# m = size of table
def linear_probing_hash(x, i):
    return (some_other_hash(x) + i) % m
~~~
{: .language-python}

This just computes the hash of the key with a standard hash function, adds the trial count to it and takes its modulus to the base m. This approach is bad because it leads to clustering. What this will do in case of a collision is just hash the key (in subsequent executions) to the empty slot closest to the collision. Over time, this will lead to there being clusters of items near the very first collisions of the table, and these clusters will continue to grow. This is bad for load balancing of the table, and will lead to poorer search and delete run times.

A better choice of hash function is called the double hash function.

~~~
def double_hash(x, i):
    return (h1(x) + i*h2(x)) % m
~~~
{: .language-python}

Here h1 and h2 are ordinary hash functions. There is a restriction on h2 to make sure that you get a permutation of {0, 1, …, m-1}, which is that h2(x) and m should be relatively prime. To ensure this, we can define m to be 2i and h2(x) to be odd for all x. This function works pretty well in practice.

With this, if you also implement table doubling (which works a little differently for an open addressing table than a chaining table), you can prove that you can have O(1) insert, delete, and search time  w.h.p, as long as the load factor  is a small number (<0.5).
