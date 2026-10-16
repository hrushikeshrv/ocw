---
layout: default
title: Lecture 22 - Expectation 
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 22
---

# Lecture 22 - Expectation

The expected value of a random variable is just the mean value that the random variable takes over all points in the sample space.

## Calculating Expectation

The expected value of a random variable is

$$Exp(R)=\sum_{i \in S}^{}{i P(R=i)}$$

When the range of the random variable is the natural numbers, we can simplify this equation into -

$$Exp(R)=\sum_{i=0}^{\infty}{P(R>i)}$$

## Mean Time To Failure Problem

A mean time to failure problem is any problem that needs us to calculate the expected number of (mutually independent) steps till failure occurs in a system. A system may be running in mutually independent steps, each with a probability of failure equal to p.

Then the expected number of steps the system will take before it fails can be calculated by using the above definition of expected value when the range of the random variable is the natural numbers.

We define the random variable to be the number of steps we take before failure occurs. This random variable can clearly only take natural numbers as values.
$$
\begin{aligned}
	R&=\text{number of steps the system takes before failure}  \\
	Exp (R) &= \sum_{i=0}^{\infty}{P(R>i)}  \\
\end{aligned}
$$
Now,
$$
\begin{aligned}
	P(R>i) &= (1-p)^i  \\
	\therefore Exp (R) &= \sum_{i=0}^{\infty}{(1-p)^i}  \\
		&= \frac{1}{1-(1-p)}  \\
\end{aligned}
$$
Therefore,  
$$Exp (R) =\frac{1}{p}$$

So the expected number of steps we expect to take before we fail is $\frac{1}{p}$.

A lot of problems can be simplified down to a MTTF problem, for example, if a couple wants to have a girl, then the number of children they expect to have by the time they have their first girl is 2 ($\frac{1}{0.5}$), assuming mutual independence.

If a couple wants to have at least one boy and one girl, then the expected number of children they will have by the time they have at least one boy and at least one girl is 3. Imagine they have their first child, then this problem reduces to the previous problem of the expected number of children they have before they have a child of the other sex.

## Linearity of Expectation

Linearity of expectation says that expectation of a random variable is a linear function. That is,

$$Exp(R_1+R_2) = Exp(R_1) + Exp(R_2)$$

This theorem is true whether or not the random variables are independent.

Example -  

$$
\begin{aligned}
&\text{R1 = The number rolled on dice 1} \\
&\text{R2 = The number rolled on dice 2}  \\
&\text{R = R1 + R2} \\
Exp(R) &= Exp(R1) + Exp(R2) \\  
Exp(R1) &= Exp(R2) = 3.5 \\ 
Exp(R) &= 7 \\
\end{aligned}
$$

## Using The Linearity of Expectation

We can use the linearity of expectation to greatly simplify some complicated problems.

Imagine n men go to a theater where they have to deposit their hats at the entrance. Once the movie starts, something happens at the entrance which results in all the hats getting randomly shuffled. Once the movie ends, the men come back to take their hats, and each one of them is handed a random one back. What is the expected number of men who will get their own correct hat back?

The natural way to solve this problem might be to set the random variable R as the number of men who got their hat back.

$$\text{R = number of men who got their hat back}$$

Then the expected value is

$$Exp (R) = \sum_{i=0}^{n}{iP(R=i)}$$

We can figure out $P(R = i)$ to be  

$$
P(R=k) =
\begin{cases}
    \frac{1}{k!(n-k)} & \text{if} k \leq n-2 \\
    \frac{1}{n!} & \text{if} k > n-2
\end{cases}
$$

Substituting this into the sum will be very difficult to solve. Instead, we use the linearity of expectation.

We define our random variable Ri to be the indicator variable that the ith man got his hat back. We define R to be R1 + R2 + … + Rn. Since Ri can only take values 1 or 0, we can take the sum of all Ris to get the total number of men who get their hat back. The value we are looking for is only Exp(R).

$$Exp(R) = Exp(R1) + Exp(R2) + … + Exp(Rn)$$

Since all Ris are indicators, Exp(Ri) = P(Ri = 1). Also, P(Ri = 1) = 1/n (since there is a one in n chance that the ith man gets his hat back out of n hats)

Therefore, $Exp(R) = 1/n + 1/n + … + 1/n = n/n$, so the expected value of R is 1.
