
import numpy as np
from simulations_X import options, produce_synthetic_data

def formula(x, n=None):
    if n is None:
        n = x.shape[0]

    # eps = np.random.normal(loc=0.0, scale=1.0, size=n)
    t = np.exp(x[:, 0:10].sum(axis=1))

    y = ((t / (t + 1)) > 0.5).astype(float)
    
    return y 

def main():
    opt = options()
    produce_synthetic_data(opt.n, opt.p, formula, correlated=False)

if __name__ == "__main__":
    main()
