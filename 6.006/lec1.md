# Lecture 1 - Algorithmic Thinking, Peak Finding
## 1D Peak Finding
In a one dimensional case, peak finding is trivial. You just parse through all the elements
in the array, look to the left and the right element, if both of them are lesser than the 
current element, we have found a peak. For the edges of the array we just check the one neighbor.

This algorithm is clearly O(n).

A faster algorithm would use binary search. We jump to the middle of the array, compare the 
left and right neighbors, and recurse on the half of the array which has the higher number. 
If both the elements are smaller than the middle element, we found a peak. We can prove the 
correctness of this algorithm, and its time complexity is clearly O(log n). This recursive 
algorithm returns one peak, and not all.

For this problem, and most others in this course, O(log n) is the optimal complexity.

## 2D Peak Finding
In two dimensions, we define a peak if all the neighbors (left, right, top, bottom) of a cell
are less than or equal to the current cell. You could also define a peak to be strictly less 
than the current cell, which makes more sense to me.

An efficient and correct algorithm for a 2D peak finder is as follows.

Start with the middle column in the 2D matrix, and find the global peak on the single column. 
This is O(log n) complexity. We then look to the elements on the left and the right of the global 
maximum, and we recurse on the half-matrix which has the higher element. If both the left, and the 
right elements are smaller or equal to the global max, we have found a peak, and we return.

The recurrence for the time complexity of this algorithm is -

$$ T(n,m) = \Theta(n) + T(n, m/2) $$

Where the matrix has n rows and m columns. Solving this recurrence gives us the time complexity 
of this algorithm as O(n log m). The proof of correctness is left as an exercise, and as a question 
in the problem set. Intuitively, it makes sense because it follows the same pattern as the recursive 
algorithm for 1D peak finding.