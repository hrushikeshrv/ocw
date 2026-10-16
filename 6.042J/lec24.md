---
layout: default
title: Lecture 24 - Large Deviations
parent: MIT 6.042J - Mathematics For Computer Science
nav_order: 24
---

# Lecture 24 - Large Deviations

In this lecture we develop specific tools to estimate or bound the probability that the random variable deviates from its expectation.

## Markov’s Theorem

Markov’s theorem says that if R is a non-negative random variable, then the probability that R is a lot bigger than the expected value of R is small. In other words, it says that if R is a random variable that is always positive, then it is likely to be less than or equal to the expected value of R.  

More formally, we can express the probability that R is greater than or equal to some value x as

$$Pr(R \geq x) \leq \frac{Ex(R)}{x}$$

## Corollary 1 to Markov’s Theorem

This gives us a nice corollary saying that the probability that a non-negative random variable is c times the expected value of that variable is at most 1/c.

$$Pr(R \geq cEx(R)) \leq \frac{1}{c}$$

If you assume that the average weight of all people in India is 60kg, the probability that a randomly selected person will weigh more than 120 kg is at most $\frac{1}{2}$. We can do this because a person cannot have negative weight.

Markov’s theorem can help you in all situations where you know the expected value of some random variable and you want to calculate the probability that the random variable is some other value (either the theorem or the corollary). This is what makes the theorem extremely powerful, especially since it does not assume anything about the distribution.

But this fact means that a Markov bound is not always a tight bound. For example, if we consider the chinese appetizer problem in which n peoples’ appetizers are kept in a circle, then someone comes along and spins the whole table, the expected number of people who get the appetizer that they ordered is 1 (using the linearity of expectation). The probability that all n people get their own appetizer back is at most 1/n, according to the Markov bound. Also, we can calculate that the probability that all n people get their appetizers back is also 1/n (since they are arranged in a table, we can visualize the appetizers being “phase shifted” by some number modulo n, and the probability that the modulus is 0 is 1/n). In this case, the Markov bound was the right answer.

However, in case of the hat problem in which n men deposit their hat in a box, their hats are randomly shuffled and given back to them, the expected number of men who get their own hat back is 1\. The probability that all n men get their hat back is again at most 1/n, according to the Markov bound, but the actual probability that all n men get their hat back is 1/n\! (which is easy to see). In this case, the Markov bound is way off the correct answer.

Since Marov’s theorem is only true if R is always non-negative, if we have a random variable that does take negative values but has a lower bound, then we can define a new random variable shifted to make all the values non-negative, and Markov’s theorem would still hold.

## Corollary 2 to Markov’s Theorem

We can also get a corollary to estimate the probability that the random variable takes a value less than some non-negative number, but only if we know that the random variable has a hard upper bound in values.

If the random variable R $\leq$ u, then $\forall$ x \< u, the probability that R is less than or equal to x is given by

$$Pr(R \leq x) \leq \frac{u-Ex(R)}{u-x}$$

This works because $Pr(R \leq x)$ is the same as $Pr(u-R \geq u-x)$, we can then apply Markov’s theorem to $Pr(u-R \geq u-x)$ and get the result.

## Chebyshev’s Theorem

Chebyshev’s theorem is an analog to Markov’s Theorem but uses the variance of the distribution instead of the expectation. If you know the variance of the distribution, you can bound the probability that the random variable deviates from the expectation by a certain amount, just like in Markov you can bound the probability that the random variable takes a certain value if you know the expectation. The statement of the theorem is \-  

$$Pr(|R - Ex(R)| \geq x) \leq \frac{Var(R)}{x^2}$$

The proof of the theorem actually uses the Markov theorem. It is just another version of the Markov theorem.  

$$
\begin{aligned}
Pr(|R - Ex(R)| >  x) &= Pr((R-Ex(R))^2 > x^2)  \\
Pr((R-Ex(R))^2>x^2) &\leq Ex((R-Ex(R))^2)/x^2  \\
Ex((R-Ex(R))^2) &= Var(R) \\
\end{aligned}
$$

We have the same corollaries to this theorem as Markov’s theorem. One thing to be careful of when using Chebyshev’s theorem is that it gives you the probability that the random variable deviates from the expected value by a certain amount. Therefore, it gives you the probability that the random variable is either greater than the expectation by that amount OR the random variable is lower than the expectation by that amount. In cases where you want to bound the value of the random variable on one side, you have to be careful if you don’t know if the distribution is symmetric.

If you want to bound the probability that the value of the random variable deviates from the expectation on one side, if you don’t know anything else about the distribution that the variance, the probability that the random variable deviates at least c times the standard deviation on the high side OR on the low side is $1/c^2+1$.

## Chernoff Bounds

The problem with Markov and Chebyshev’s theorem is that they can be way off the real value of the probability. In which case the bound is almost useless. Chernoff gives you way tighter bounds than Markov or Chebyshev. The catch is that Chernoff bounds are defined for a special case, but it is usually possible to convert a problem into that special case.

Chernoff bounds are defined for a type of random variable that itself is a sum of n other mutually independent random variables. Let T1, T2, …, Tn be n random variables that only take values from 0 to 1 (if they don’t, we can always normalize them such that they do). Then we define T to be the sum of all n random variables. Then the probability that T is greater than c times its expected value is $exp(-z Ex(T))$ where $z$ is $(c \ln{c}) + 1 - c$.

$$Pr(T \geq c Ex(T)) \leq e^{-z Ex(T)}$$

For example, if you have a lottery where each person has a one in ten thousand chance of winning, and a total of ten million people play. Then we can define a random variable T as the total number of winners, which will be the expected number of winners, which is just the sum of probabilities that each person wins.
$$
\begin{aligned}
T &= T_1+T_2+... +T_{10M}  \\
Ex(T) &=10M/10,000 = 1,000  \\
Pr(\geq 2000 \text{ winners}) &\leq exp(-(2ln(2)-1)*1000) = e^{-380} \approx 0 \\
\end{aligned}
$$

This bound is according to Chernoff. However, if we did not know if the random variables Ti were independent, then the best we could do would be a Markov bound, which would give us $\frac{1}{2}$.

## Bounds with General Functions

Using Markov’s theorem, we can arrive at Chebyshev’s as well as Chernoff bounds. This is because Chebyshev and Chernoff are actually just using Markov’s theorem, along with some function to modify the random variable in order to get different kinds of bounds.

If we want to calculate the probability that a random variable A is greater than a random variable B, P(A \> B), that is the same as P(f(A) \> f(B)), as long as f does not switch the inequality. Then, using markov, we can write

$$Pr(f(A)>f(B)) = \frac{Ex(f(A))}{f(B)}$$

What Chebyshev and Chernoff were doing was choosing different functions for f. Chebyshev used variance, which was the square function, and Chernoff used the exponentiation function.

Of all the functions you could choose to get different bounds, it turns out that Chernoff’s exponentiation is the optimal choice of functions.