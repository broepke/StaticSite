# from scipy import special as sp
from math import factorial

def binom(n,k):
	'''calculate binomial coefficient without using scipy'''

	return factorial(n) / (factorial(k) * factorial(n-k))


triangle = []
n = 0 # Column Counter
row_counter = 0 # Row counter


for n in range(12):
    row = []
    for k in range(row_counter+1):
        # n_k = sp.binom(n,k) # scipy version
        n_k = binom(n,k) # using factorial from the math package
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
