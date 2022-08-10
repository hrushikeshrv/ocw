# Lecture 3 - Insertion Sort, Merge Sort
## Insertion Sort
Insertion sort is an $O(n^2)$ algorithm. The pseudocode for insertion sort is -

1. Consider you have already sorted a prefix of the array A[:i-1] and are considering
key i.
2. Take key i and insert it into the right place in the sorted array A[:i-1] by doing pairwise swaps with adjacent elements.

For example, if you had the array $A = [5, 3, 4, 1, 2, 6]$ and you were somewhere in the middle of your sorting process -

$$A = [3, 4, 5, 1, 2, 6]$$

If you were considering the key 1, then you would first swap its place with 5, then compare with 4, then swap it with 4 (since 1 belongs to the left of 4), then compare 1 with 3, then swap it with 3, then stop since 1 would be in the right place. At the end of this step you would get

$$A = [1, 3, 4, 5, 2, 6]$$

You would then do the same thing for 2 and 6.

## Complexity
Since insertion sort requires an entire iteration through the array, and since in each step of the iteration you may have to do $\Theta(n)$ compares and swaps, insertion sort is a $O(n^2)$ algorithm.

One optimization we could perform is to the number of comparisons. To find the right place in which we have to insert the current key, we could use binary search to find the right index and then do pairwise swaps to insert it into the right place. This would reduce the complexity w.r.t. the number of comparisons but we would still need to do a linear number of swaps to get the key into the right place.

This still doesn’t change the asymptotic time complexity of insertion sort, because we still have to do $O(n)$ swaps for each step. So we have a total of $O(n \cdot log\,n)$ comparisons but we have a total of $O(n^2)$ swaps. This helps you improve the total runtime if comparing two items in the array is expensive (like one or more database lookups), but if comparison and swapping are both $O(1)$ operations, insertion sort remains a $O(n^2)$ algorithm.

## Merge Sort
Merge sort is a recursive sorting algorithm. Instead of sorting an array as is, it splits the array into 2 halves, sorts them, and then merges them. Of course, it doesn’t explicitly sort the two half arrays either - it splits them into two more arrays, tries to sort them, and merges them together.

The pseudocode for merge sort is -
1. Given an array, split it into 2 half-arrays.
2. If the arrays are not of size 1, split them further and recurse on both halves of the array.
3. Else, the two half-arrays have been sorted (since they only have 1 element), combine them together by running the merge routine.

The pseudocode for the merge routine is -
1. Consider the first element in both the sorted arrays.
2. Add the minimum of the considered elements to the merged sorted array.
3. Remove the added element from the half-array.

~~~
# Untested, rough merge sort implementation
def merge_sort(arr):
    if len(arr) == 1:
        return arr
    left = arr[:len(arr)//2]
    right = arr[len(arr)//2:]
return merge(merge_sort(left), merge_sort(right))

def merge(left, right):
    i, j = 0, 0
    ans = []
    while True:
        if i >= len(left) and j >= len(right):
            break
        elif i >= len(left):
            ans.append(right[j])
            j += 1
        elif j >= len(right):
            ans.append(left[i])
            i += 1
        else:
            if left[i] > right[j]:
                ans.append(right[j])
                j += 1
            else:
                ans.append(left[i])
                i += 1
    return ans
~~~
{: .language-python}

## Complexity
Merge sort involves dividing the arrays ${log}_{2}(n)$ times, and the merge routine for each division takes $\Theta(n)$ steps. Therefore, merge sort is a $\Theta(n \cdot log\,n)$ algorithm. More formally, we can write the recurrence for merge sort as -

$$ T(n) = \Theta(1) + \Theta(n) + 2 \cdot T(n/2) $$

The $O(1)$ comes from splitting the array into two halves, and the $O(n)$ comes from the work required to merge the two half-arrays after they have been sorted. Solving this recurrence using the techniques given in [6.042J lecture 15](../6.042J/lec15.md), we get the time complexity of merge sort to be $O(n \cdot log\,n)$.

One disadvantage of merge sort is that it is not in place. To sort an array you have to essentially create a sorted copy of it in memory, which may not be possible if the array is too big to fit twice into memory. In this case, insertion sort may be preferred, since even though it is $O(n^2)$, it is in place. There does exist an in place version of merge sort, but it doesn’t do too well on the constant factors, so we prefer quick sort, or any other in place algorithm instead of merge sort.
