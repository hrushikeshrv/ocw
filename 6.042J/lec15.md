---
layout: default
title: Lecture 15 - Linear Recurrences
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 15
---

# Lecture 15 - Linear Recurrences

Linear recurrences are recurrences of the form -

$$f(n) = a_1f(n-1) + a_2f(n-2) + ... + a_kf(n-k)$$

Which can be expressed in sigma-notation as -

$$f(n) = i = 1kaif(n-i)$$

## Fibonacci Recurrence

The constant k is known as the order of the recurrence. The Fibonacci recurrence is a linear recurrence of order 2.

We can get a closed form expression of the fibonacci recurrence by guessing that we can express the recurrence in this form - $f(n) = \alpha^n$. That is, the nth fibonacci number is $\alpha^n$.

$$
\begin{aligned}
    &f(n) = f(n-1) + f(n-2) \\
    &\implies \alpha^n = \alpha^{n-1} + \alpha^{n-2} \\
    &\implies \alpha^2= \alpha + 1
\end{aligned}
$$

Solving the above quadratic equation, we get

$$\alpha = \left(\frac{1\pm\sqrt{5}}{2}\right)$$

Which is the golden ratio $\varphi$.  

However, this is not a complete expression of the fibonacci series. The fibonacci series in general is represented by

$$f(n) = c_1\alpha_1^{n-1} + c_2\alpha_2^{n-2}$$

The constants $c_1$ and $c_2$ depend on the starting conditions/boundary conditions of the series. Once we know those, we can substitute the values of $f(0)$ and $f(1)$ and find the values of $c_1$ and $c_2$. If $f(0) = 0$ and $f(1) = 1$, then $c_1 = c2 = \frac{1}{\sqrt{5}}$.

## General Linear Recurrence

The solution to a general linear recurrence can be obtained using the same method we used to obtain a solution for the fibonacci recurrence - by substituting $f(n) = \alpha^n$ in the recurrence expression. On substitution, we get the following equation, which we call the characteristic equation of the recurrence -

$$
\begin{aligned}
    f(n) &= a_1f(n-1) + a_2f(n-2) + a_3f(n-3) + ... + a_df(n-d)  \\
    \alpha^{n} &= a_1\alpha^{n-1} + a_2\alpha^{n-2} + a_3\alpha^{n-3} + ... + a_d\alpha^{n-d} \\
    \alpha^{d} &= a_1\alpha^{d-1} + a_2\alpha^{d-2} + a_3\alpha^{d-3} + ... + a_d \\
\end{aligned}
$$

This is a polynomial of order d, which we need to solve. This polynomial can have any number of roots  d. In case it has d roots, the solution to the recurrence is easy -

$$f(n) = c_1\alpha^{n} + c_2\alpha^{n} + c_3\alpha^{n} + ... + c_d\alpha^{n}$$

This applies to the fibonacci recurrence. This solution is a general solution. We get the particular solution when we substitute the base cases and calculate the values of the c constants.

The system of equations we will get by substituting the base case into the polynomial is never degenerate.

In case some root of the polynomial is repeated r times, then $\alpha^{n}$, $n\alpha^{n}$, $n^2\alpha^{n}$, … , $n^{r-1}\alpha^{n}$ are all solutions to the recurrence, and we find the general solution by taking a linear combination of these solutions and solving the system of linear equations by substituting in the base case.

## Non-Homogeneous Linear Recurrences

A linear recurrence is called homogeneous if the current term *only* depends on the previous terms, and not any other function of n or any constant. That is, the linear recurrence that looks like -

$$f(n) = c_1f(n-1) + c_2f(n-2) + c_3f(n-3) + ... + c_df(n-d)$$

A non-homogeneous recurrence is one that depends on both the previous terms and some function of n. That is, the linear recurrence that looks like -

$$f(n) = c_1f(n-1) + c+2f(n-2) + c_3f(n-3) + ... + c_df(n-d) + g(n)$$

Where g(n) can also be a constant.

The solution to a non-homogeneous linear recurrence can be found in 3 steps -

1. Ignore $g(n)$ and find the general solution for the resulting homogeneous recurrence.
2. Guess a solution for the non-homogeneous recurrence.
3. Add the two solutions together and solve them by treating them as a system of linear equations by substituting the base case.
