---
layout: default
title: Lecture 9 - Table Doubling, Karp Rabin
parent: MIT 6.006 - Introduction to Algorithms
nav_order: 9
---

# Table Doubling, Karp Rabin
A key piece we are missing if we want to complete our implementation of hash tables is our choice of m. We will map from the set of all keys K, which could be infinite, to a small subset m, and we want to choose an m such that the load factor $\alpha$ remains O(1), but we also don’t want to make m too big and waste space. We want m to be $\Theta(n)$, where n is the number of elements in our hash table.

This is where table doubling comes in. We choose a small size for our table, say 8. We set m to be 8. Then, as elements keep coming in and going out, we double the size of our table if it gets completely occupied. In general, if we want to grow the table from size m to size m<sup>1</sup>, we need to follow 3 steps -

1. Allocate a new table to size m<sup>1</sup>
2. Choose a new hash function h<sup>1</sup>
3. Rehash all items from the old table of size m to the new table of size m<sup>1</sup>

The time we need to perform this operation is O(n + m + m<sup>1</sup>), which is O(n). Now, if we double the size of the table during an insert, that insert is going to take O(n) time and not O(1) time. However, since we only double the size of the table log<sub>2</sub>n times as we go from a table of size 0 to n, we can distribute the cost of doubling over all n inserts and calculate the average time needed to insert n items into the hash table.

## Amortized Cost For Inserts
You can think of the amortized cost kind of like the average cost of n operations. One way to calculate it is by redistributing the cost of all operations uniformly. For example, if you have to pay a monthly rent, you usually pay nothing for most days of the month and pay all of it at once on one day of the month. This is kind of how most inserts are O(1) and only a few need O(n) time. What you can do instead is redistribute your rent and instead of paying nothing for most days of the month, you can pay a smaller amount every day of the month. The total cost would be the same, and you would call the rent you pay each day to be the amortized cost of one day (operation).

The cost of doubling the table is O(n), and only happens log2n times. So the total cost of table doubling for n insertions is O(1 + 2 + 4 + 8 + … + n), which is O(n). The total cost of the insertions themselves is O(n). So the total cost of inserting n items into the hash table is O(n)/n, which is O(1). Hence we can say that inserting into a hash table takes constant time amortized.

We use a similar logic for deletions. If we delete items such that m = 4n, we halve the size of the table to be 2n. Using the same amortized analysis, the cost for a deletion is O(1) amortized.

This is how lists work in python. They use table doubling and table halving to provide constant time append and pop operations. So appending to a list or removing the last item from a list are actually O(1) time amortized.

## Table Doubling for Real Time Applications
For some high performance real time applications, spending O(n) time for a few operations is not ideal and can lead to spikes in performance. One way to prevent this is to keep track of the size of your table. As soon as you notice that you are starting to reach the threshold where you would want to double the size of the table, you start to build a table twice the size on the side. Then, every time you insert, you copy over some constant amount of items over to the new table. This constant needs to be big enough to be able to copy over all of the items by the time you need to double.

While this technique is not used too often in practice since it is hard to implement robustly, it does allow you to get O(1) insertions and deletions non-amortized.

## String Matching & Karp Rabin
String matching is a common problem, you want to search for a string s in a corpus or document t. The naive algorithm of checking all possible substrings of length s from the corpus is something like this -

~~~
def search(s, t):
    return any(s == t[x:x+len(s)] for x in range(len(t)-len(s))
~~~
{: .language-python}

The `==` operator in python checks for the equality of two strings by comparing all characters of the strings and returns true if all of them match. This is clearly a O(\|s\|) operation, which we do O(\|t\|) times. So the cost of searching for a substring match this way is at least O(\|t\|\|s\|), which is polynomial time. This would be really bad if we were searching for a big substring in a big corpus. We would like to bring this time down using hashing.

If, instead of comparing two strings character by character, we could hash them down to the size of a word, we will be able to compare two strings in constant time. However, hashing a string of length s still takes O(\|s\|) time, so we’re not saving any time using this approach. To fix this, we use a rolling hash function. We make use of the fact that when we are checking for substring matches in a corpus, we are effectively checking each substring of the corpus by sliding a “window” of size \|s\| and checking if the substring of the corpus in that window matches our string. However, when we slide that window over by 1 character, we don’t need to recalculate the hash value of the new string from scratch. We can use the information we had from the previous string, and define a deletion and an addition operation on the hash function that would let us compute the hash of a new string by deleting one character from the front of the string and inserting a character at the end of the string.

Now we only need to design a data structure that would let us perform the above operations in constant time. This is called the Karp Rabin algorithm, and it runs with time complexity O(\|s\| + \|t\| + #matches*\|s\|) in expectation, #matches is the number of matches you want to report.
