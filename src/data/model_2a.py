
import numpy as np
from simulations_X import options, produce_synthetic_data

def formula(x, n=None):
    if n is None:
        n = x.shape[0]

    x1 = x[:, 0]
    x2 = x[:, 1]
    x3 = x[:, 2]
    x4 = x[:, 3]
    
    x1 = 5 * x1
    x2 = 2 * np.sin(np.pi * x2 / 2)
    x3 = 2 * x3 * (x3 > 0).astype(int)
    x4 = 2 * np.exp(5 * x4)

    eps = np.random.normal(loc=0.0, scale=1.0, size=n)
    
    y = x1 + x2 + x3 + x4 + eps
    return y 

def main():
    opt = options()
    produce_synthetic_data(opt.n, opt.p, formula)

if __name__ == "__main__":
    main()
