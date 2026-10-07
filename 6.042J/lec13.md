---
layout: default
title: Lecture 13 - Sums and Asymptotics
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 13
---

# Lecture 13 - Sums and Asymptotics

First half of the lecture was deriving bounds for the sum $\sum_{i=1}^{n}{\frac{1}{i}}$ , the Harmonic numbers, using the integration bounds method. We also derived bounds for the product $\prod_{i=1}^{n}{i}$, or $n!$ by taking the log on both sides and converting it into a sum, and then using the integration bounds method.

## Asymptotic Notation

We use asymptotic notation to describe how a function grows/the value a function approaches as n grows larger. There are 5 or 6 main asymptotic notations \-

1. Tilde \- We say a function $f(x) \sim g(x)$ if $\lim_{x\rightarrow\infty}{\frac{g(x)}{f(x)} = 1}$
2. Big-Oh \- We say a function $f(x) = O(g(x))$ if $f$ grows no faster than $g$. i.e., $\lim_{x\rightarrow\infty}{\left|\frac{f(x)}{g(x)}\right| \lt \infty}$. $f(x)$ cannot be greater than $g(x)$ as $x$ grows to infinity, or $f(x)$ is upper bounded by $g(x)$.  
   Note that $x^c = O(c^x) ~\forall~ c \in R$, since $\lim_{x\rightarrow\infty}{\frac{x^c}{c^x}} = 0$. So any polynomial grows slower than any exponential.
3. Omega \- We say a function $f(x) = \Omega(g(x))$ if $f$ grows at least as fast as $g$.  
   $\lim_{x\rightarrow\infty}{\frac{f(x)}{g(x)}} \gt 0$  
   Therefore, $f(x) = \Omega(g(x))$ iff $g(x) = O(f(x))$
4. Theta \- We say a function $f(x) = \Theta(g(x))$ if $f$ is lower and upper bounded by $g$.  
   $\lim_{x\rightarrow\infty}{\frac{f(x)}{g(x)}} \gt 0$ and  $\lim_{x\rightarrow\infty}{\frac{f(x)}{g(x)}} \lt \infty$  
   Therefore, $f(x)=\Theta(g(x))$ iff $f(x) = O(g(x))$ and $f(x) =\Omega(g(x))$, i.e. $f$ is both lower bounded by $g$ and upper bounded by $g$.
5. little o \- If $f(x)$ grows strictly slowly than $g(x)$, $f(x) = o(g(x))$
6. little omega \- If $f(x)$ grows strictly greater than $g(x)$, $f(x) = \omega(g(x))$

Formal notations aside, we can say that if two functions are related by the tilde, they approach equality in the limit. Similarly, $f(n) = O(g(n))$ implies that $f \leq g$ in the limit. $f(n) = \Omega(g(n))$ implies $f \geq g$ in the limit, $f(n) = \Theta(g(n))$ implies $f == g$ in the limit, $f(n) = o(g(n))$ implies $f \lt g$ in the limit, $f(n) = \\omega(g(n))$ implies $f \gt g$ in the limit.
