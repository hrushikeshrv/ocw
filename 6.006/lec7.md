# Counting Sort, Radix Sort, Lower Bounds for Sorting
## Lower bounds for sorting
We can represent the execution of an algorithm as a decision tree. The leaves of the tree are the endpoints or the “answers” of the algorithm, and the path to a leaf is one execution of the algorithm. In this case, we can define the worst case running time of an algorithm to be the height of the tree.

Using this representation, we can prove that we need at least $O(log\,n) $ 
time for searching and at least $O(n \cdot {log}_{2}\,n)$ time for sorting (except for some special cases in which we can sort in linear time).

The number of leaves in the tree for a searching algorithm is at least n, since in a data structure containing n items, the item to search for can be in any of the n different spots. For a binary tree containing at least n leaves, the height of the tree has to be at least ${log}_{2}\,n$.

Similarly for sorting, the number of leaves has to be at least $\Theta(n!)$. So the height of the tree has to be at least $log_2\,(n!)$, which, if you calculate, is at least $\Omega(n \cdot log\,n)$.

## Counting Sort
For sorting n integers in `range(k)`, when k is not too big, we can sort in linear time.

Let there be n items that you want to sort. Initialize a list L of length k, where each element in the list is an empty list, and k is the maximum key that can be assigned to any item (using a hashing function). The key is assigned by a key() function which maps the given item to a positive integer.

Go through the n items you want to sort one by one, convert them into their keys, and append the item itself to the list L in the index given by the key. Then go through the list L and keep concatenating the lists that you see.

~~~
def counting_sort(A, key):
    “””
    A is the array to be sorted, key is a function that maps the 
    elements in A to a non-negative integer.
    “””
    L = [[] for i in range(k)]
    for j in range(n):
        L[key(A[j])].append(A[j])
    
    output = []
    for k in range(k):
        output.extend(L[k])
    
    return output

~~~
{: .language-python}

The time complexity of this algorithm is $O(n + k)$, most of the time being taken up by the last for loop (since extend takes linear time). If k is $O(n)$, then counting sort is practical, if k gets even a little bigger than n, then counting sort starts becoming sub-optimal.

## Radix Sort
Radix sort can deal with a bigger range of k than counting sort. Radix sort requires k to be $O({n}^{O(1)})$, i.e. k can be to the order of a polynomial in n, and it uses counting sort as a subroutine.

The setup is the same. Let there be n items you want to sort. Visualize whichever integer the key function will give you as an integer in some base b. In this representation, the number of digits in the base b number is ${log}_b\,k$.

We then consider only the least significant bits of the keys and use counting sort to sort the items. We then consider only the next most significant bit and use counting sort to sort the items. We do this for all the digits in the representation, which is $log_b\,k$ iterations of counting sort. Therefore, the time complexity of this algorithm is $O((n+b) \cdot log_b\,k)$. To get the minimum complexity, we want $(n+b) \cdot log_b\,k$ to be minimum, which is when we choose b = n. When b = n and k is $O(n^{O(1)})$, the complexity reduces to

$$ O((n+b) \cdot log_b\,k) = O((n+n) \cdot log_n\,n^{O(1)}) = O(n+n) = O(n) $$

Which is linear time.