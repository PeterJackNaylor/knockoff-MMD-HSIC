
import numpy as np
import argparse

def options():
    # options
    parser = argparse.ArgumentParser(description="simulating data")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--p", type=lambda x: int(float(x)), default=4)
    args = parser.parse_args()
    return args

def generate_X(n, p):
    sigma = generate_S(p)
    mean = np.zeros(p)
    x = np.random.multivariate_normal(mean, sigma, size=n)
    return x

def generate_S(p):
    output = np.zeros(shape=(p, p)) + 0.5
    sigma_mat_power = np.zeros(shape=(p, p))
    for i in range(1, p):
        l_indices = np.arange(p-i)
        r_indices = l_indices + i 
        sigma_mat_power[l_indices, r_indices] = i
    output = np.power(output, sigma_mat_power + sigma_mat_power.T)
    return output

def produce_synthetic_data(n, p, formula):
    X = generate_X(n, p)
    y = formula(X, n=n)
    np.savez("Xy.npz", X=X, Y=y)


if __name__ == "__main__":
    print(generate_X(2, 200))