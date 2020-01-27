from scipy import special as sp

triangle = []
n = 0 # Column Counter
row_counter = 0 # Row counter


for n in range(11):
    row = []
    for k in range(row_counter+1):
        n_k = sp.binom(n,k)
        row.append(n_k)
    triangle.append(row)
    row_counter += 1


for tri in triangle:
    print(tri)
