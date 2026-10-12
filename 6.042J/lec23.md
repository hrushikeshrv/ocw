---
layout: default
title: Lecture 23 -Expectation 2 
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 23
---

# Lecture 23 - Expectation 2

## Theorem 1

Given a probability space $S$ and $n$ events $A_1, A_2, \ldots, A_n$, the expected number of events to occur is $\sum_{i=1}^{n}{Pr(A_i)}$.

This theorem says that given $n$ events, the number of expected events to occur is the sum of probabilities of all events. This can be proved just like we solved the hat problem in the last lecture, using the linearity of expectation. This theorem also does not need the events to be independent at all.

## Theorem 2

When the expected value of the number of events happening is less than 1, we can say that the probability that one or more events occurs is less than or equal to the expected number of events that occur.

$$Pr(T\geq1) \leq Ex(T)$$

For example, if you have a 100 ways in which a system can fail, each with probability one in a million, we can say that the system will fail at most with a probability one in ten thousand. Here, the probability that the system will fail is upper-bounded by the expected number of events to occur, which, by theorem 1, is one in ten thousand.

## Murphy’s Law

The famous statement of Murphy’s Law is that if something can go wrong, it will go wrong. The formal statement is that if the expected number of events to occur is $n$ (i.e, $Ex(T) = n$), then the probability that none of the events occur is at most $e^{-n}$.

$$Pr(T=0) = e^{-Ex(T)}$$

The probability that no event occurs ($Pr(T=0)$) when you expect $Ex(T)$ events to occur is at most $e^{-Ex(T)}$.

## Product Of Expectations

Given two mutually independent random variables R1 and R2, the expected value of a new random variable R1xR2, Exp(R1R2) is the same as the product of the expected values of the two random variables.

$$Ex(R_1R_2) = Ex(R_1) Ex(R_2)$$

This is only for mutually independent events, however.  
By corollary, this also works for more than 2 random variables provided they are mutually independent, and also means that $Ex(aR + b) = aEx(R) + b$.

## Deviation & Variance

Deviation is a measure of how far from or how close to the expected value your random variable is likely to land. If your expected value of the random variable is $Ex(R)$, in what range is $R$ likely to fall in the next trial?

You can have random variables that will almost certainly be extremely far from the expected value and you can have random variables which will almost certainly be very close to the expected value.

For example, let $R$ be an indicator random variable that is either 1000 or -1000 with probability $\frac{1}{2}$. The expected value of the random variable is 0, but the random variable will be extremely far from 0.

To capture this quantity, we can look at the expected value of the deviations of the random variable from the mean. We define the variance as the expected value of the square of deviation of the random variable from the mean.

$$\sigma^2(R)=Ex((R-Ex(R)^2)$$

Think of this as first looking at how much the value of the random variable differs from the expected value, then squaring it (to eliminate negative values and also to penalize high deviations), then averaging it. This is the mean-square value. If you then take the square root of this, we get the root mean square value, which we define as the standard deviation of the random variable.