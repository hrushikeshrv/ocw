---
layout: default
title: Lecture 14 - Divide and Conquer Recurrences 
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 14
---

# Lecture 14 - Divide and Conquer Recurrences

The first 3/4ths of the lecture was solving recurrences from merge sort and the Tower of Hanoi problem using the plug and chug method from the first recitation of 6.006 or the first pset for 6.006.

## General Form Of Divide and Conquer Recurrences

A standard divide and conquer recurrence that we see, for example, in the recurrence for some sorting algorithms is

$$T(n) = 2T(n/2) + n-1$$

The general form of any such divide and conquer recurrence can be represented as \-

$$T(n) = a_1T(b_1x + \epsilon_1) + a_2T(b_2x + \epsilon_2) + \dots + a_kT(b_kx + \epsilon_k) + g(x)$$

The general solution of such an ugly recurrence was discovered by two students from Beirut who came to Prof. Tom in 1996 or something, named Akra and Bazzi. The general solution for a recurrence that looks like the one above is \-

$$T(n) = \Theta\left(n^p + n^p\int_{1}^{n}{\frac{g(u)}{u^{p+1}}du}\right)$$

Where p is given by

$$\sum_{i=1}^{k}{a_ib_i} = 1$$

Finding p is easy when there aren’t many terms in the recurrence expression. However, if you can prove that p is less than the degree of g, then the answer to the recurrence expression simplifies to

$$T(n) = \Theta(g(x))$$

You can prove the upper limit of p by taking p to be some integer and plugging it into the formula to compute p. If the sum comes out less than 1 for that value of p, you know that p has to be less than the value you have just considered, since b is always \< 1, so raising b to a smaller power will get a slightly bigger value.