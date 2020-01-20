Title: Statistics
Date: 2020-01-11
Modified: 2020-01-11
Category: Python, DataScience
Tags: code, statistics, datascience
Slug: statistics
Authors: Brian Roepke
Summary: Leverging Python to Solve Statistics Problems
Header_Cover: theme/images/cranes_night.jpg


Using some of the more powerful Python libraries on the
market like [SciPy](https://docs.scipy.org/doc/scipy/reference/index.html)
and [Sci-Kit Learn](https://scikit-learn.org/stable/)
you can translate any of your classic Probability and Statistics problems into Python Code.  

As an example, if we want to calculate the binomial thereom for the
 number of ways you can choose `k` items out of a total of `n` items
 it's as simple as the following:


```python
from scipy import special as sp

n = 10
k = 2

n_k = sp.binom(n,k)
print(n_k)

```
