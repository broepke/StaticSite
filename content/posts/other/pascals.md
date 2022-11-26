Title: Pascals Triangle
Date: 2020-01-27
Modified: 2020-01-27
Tags: math
Slug: pascals
Authors: Brian Roepke
Summary: Generating Pascals Triangle in Python using Binomial Coefficients
Header_Cover: images/covers/blue_thing.jpg
Og_Image: images/covers/blue_thing.jpg
Twitter_Image: images/covers/blue_thing.jpg


One of the many beautiful things found in mathematics are [Recurrence Relations](https://en.wikipedia.org/wiki/Recurrence_relation), or an equation that recursively defines a sequence or multidimensional array of values, once one or more initial terms are given; each further term of the sequence or array is defined as a function of the preceding terms.  My favorite one of these is [Pascal's triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle).

Pascal's triangle is a triangular array of the binomial coefficients. In much of the Western world, it is named after the French mathematician [Blaise Pascal](https://en.wikipedia.org/wiki/Blaise_Pascal),

In order to calculate this you can do it two different ways.  You can sum the two numbers above or you can use [Binomial Coefficients](https://en.wikipedia.org/wiki/Binomial_coefficient). The binomial coefficient appears as the _kth_ entry in the _nth_ row of Pascal's triangle (counting starts at 0).

$$\binom{n}{k}$$

Which can also be expressed as:

$$\binom{n}{k} = \frac{n!}{k! (n-k)!}$$

This code uses the method above to create the triangle by looping through each level and computing the binomial coefficient for each item based on it's row and column position.   

```python
from math import factorial

def binom(n,k):
	'''calculate binomial coefficient'''

	return factorial(n) / (factorial(k) * factorial(n-k))

triangle = []
n = 0 # Column Counter
row_counter = 0 # Row counter

for n in range(11):
    row = []
    for k in range(row_counter+1):
        n_k = binom(n,k)
        row.append(n_k)
    triangle.append(row)
    row_counter += 1

for tri in triangle:
    print(tri)

# [1.0]
# [1.0, 1.0]
# [1.0, 2.0, 1.0]
# [1.0, 3.0, 3.0, 1.0]
# [1.0, 4.0, 6.0, 4.0, 1.0]
# [1.0, 5.0, 10.0, 10.0, 5.0, 1.0]
# [1.0, 6.0, 15.0, 20.0, 15.0, 6.0, 1.0]
# [1.0, 7.0, 21.0, 35.0, 35.0, 21.0, 7.0, 1.0]
# [1.0, 8.0, 28.0, 56.0, 70.0, 56.0, 28.0, 8.0, 1.0]
# [1.0, 9.0, 36.0, 84.0, 126.0, 126.0, 84.0, 36.0, 9.0, 1.0]
# [1.0, 10.0, 45.0, 120.0, 210.0, 252.0, 210.0, 120.0, 45.0, 10.0, 1.0]
# [1.0, 11.0, 55.0, 165.0, 330.0, 462.0, 462.0, 330.0, 165.0, 55.0, 11.0, 1.0]
```

![Pascal's Triangle](images../../images/posts/pascals.gif)

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*
