Title: Statistics
Date: 2020-01-11
Modified: 2020-01-11
Category: Python, DataScience
Tags: code, statistics, datascience
Slug: statistics
Authors: Brian Roepke
Summary: Leverging Python to Solve Statistics Problems
Header_Cover: images/cranes_night.jpg


Using some of the more powerful Python libraries on the
market like [SciPy](https://docs.scipy.org/doc/scipy/reference/index.html)
and [Sci-Kit Learn](https://scikit-learn.org/stable/)
you can translate any of your classic Probability and Statistics problems into Python Code.  

As an example, if we want to calculate the number of ways you can
choose `k` items out of a total of `n` items it's as simple as the following:


```python
from scipy import special as sp

n = 10
k = 2

n_k = sp.binom(n,k)
print(n_k)

```
Another example is using Numpy to build a Confusion Matrix:  

```python
import numpy as np

x = [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1,
     1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 2, 1, 0, 2, 0, 0, 0, 0, 0]

y = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

confusion_numpy = np.zeros((3, 3), dtype=int)
np.add.at(confusion_numpy, (x, y), 1)

print()
print('using the np.add.at method')
print(confusion_numpy)
```
