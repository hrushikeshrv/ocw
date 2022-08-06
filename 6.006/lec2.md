# Lecture 2 - Models of Computation, Document Distance
## Models of Computation
A model of computation gives you the set of operations that you can perform in constant time.
It is like the set of axioms or physical laws that govern our algorithm's execution. It gives 
you the set of operations you can use to run an algorithm, and is just the mathematical analog
of a computer. There are 2 main models of computation - the random access machine, and the 
pointer machine. The random access machine gives you constant time access to any memory location 
in an array. The pointer machine is simpler and doesn’t give you random access.

## Random Access Machine
The random access machine model gives you a constant number of registers (O(1)). In O(1) time, 
you can -

- Access or load O(1) machine words
- Perform O(1) computations on words that are already loaded
- Write or store O(1) machine words

A word is the quantum of data you can store in one memory location, usually 64 bits as of the 2020s.

## Pointer Machine
A pointer machine model corresponds very closely to OOP. It gives you dynamic memory allocation, 
and it consists of dynamically allocated objects which can have a constant (O(1)) number of fields. 
Each field either contains a word of data or contains a pointer to some other object.

A good example of an application of this model is an implementation of a linked list. In this model, 
in O(1) time, you can -

- Read or access a field of an object
- Follow a pointer
- Change a pointer
- Change a field if it contains a value

You can implement a pointer machine model using a RAM model.

## Python Cost Model
Python implements both the random access machine, and the pointer machine models for different 
data structures. Some important properties of python’s built in data structures are -

1. Accessing any element in a list takes O(1) time
2. Appending to a list uses table doubling and so takes amortized O(1) time
3. Adding 2 lists and returning takes linear time or O(\|L1\| + \|L2\|) time
4. Extending a list L1 with a list L2 takes O(1+\|L2\|) time (l1.extend(l2))
5. Retrieving the length of a list takes O(1) time because python keeps track of the length of a list as it’s being built
6. The in operator takes linear time
7. The sorted() function and List.sort() takes O(nlogn) time, and uses a comparison sort (quick sort)
8. Inserting a key into a dictionary takes O(1) time
9. Checking if a key is in a dictionary takes O(1) time

## Document Distance
We define a document as a sequence of words, and a word as a sequence of alphanumeric characters. A 
document does not have to be a huge list of words, any list of words is a document (for our purposes 
in this lecture). The document distance problem is about finding if two given documents are “similar.”

We can have different definitions of similarity, and if you implement a document distance function 
you may want to choose a definition that fits your use case, but for now we can call two documents 
similar if they have a lot of words in common. We can set the threshold for the exact number of 
common words for two documents to classify as similar dynamically.

There are a lot of motivations for solving this problem, most of which involve searching, duplicate 
matching, and now also machine learning and NLP.

We find the distance between two documents using a vector representation of the documents. We 
represent each document as an n dimensional vector, where n is the number of words in your dictionary. 
Each element of the vector represents the frequency of that word in that document. So we represent 
document D1 as an n dimensional vector - $ <d_1, d_2, d_3, ..., d_n> $ where di is the number of 
times the ith word in the dictionary appeared in D1. We then calculate the angle between the two 
documents by taking the inverse cosine of the dot product of the two document vectors and define the 
angle as the similarity. A smaller angle means closely similar documents and a larger angle means 
dissimilar documents.

Implementing this algorithm has 3 steps -
1. Split the document into words
2. Count the frequency of the words
3. Compute the dot product and the angle

The first two steps are the slowest steps, and asymptotic as well as constant factors in the 
different algorithms you could write to do these steps will affect performance dramatically. 
Eric tested 8 different implementations, and the difference between the least efficient and the 
most efficient algorithm was a 1000x improvement.

P.S - Don’t use the `re` module unless you absolutely need to use regexes, and when you do, be sure 
to know the time complexities of the methods you use, since the `re` module has a lot of functions 
that need exponential time to run.
