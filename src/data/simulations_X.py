
import numpy as np
import argparse

def options():
    # options
    parser = argparse.ArgumentParser(description="simulating data")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--p", type=lambda x: int(float(x)), default=4)
    args = parser.parse_args()
    return args

def generate_X(n, p, correlated):
    sigma = generate_S(p, correlated)
    mean = np.zeros(p)
    x = np.random.multivariate_normal(mean, sigma, size=n)
    return x

def generate_S(p, correlated, power=2):
    if correlated:
        dist_diagonal = np.zeros(shape=(p, p))
        for i in range(1, p):
            l_indices = np.arange(p-i)
            r_indices = l_indices + i 
            dist_diagonal[l_indices, r_indices] = i
        output = 1 / np.power(power, dist_diagonal + dist_diagonal.T)
    else:
        output = np.eye(p)
    return output

def produce_synthetic_data(n, p, formula, correlated=True):
    X = generate_X(n, p, correlated)
    y = formula(X, n=n)
    np.savez("Xy.npz", X=X, Y=y)


if __name__ == "__main__":
    print(generate_X(2, 200))
