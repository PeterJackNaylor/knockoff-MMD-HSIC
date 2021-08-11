
import numpy as np
from knock_off import KnockOff

def load_npz(path):
    data = np.load(path)
    X = data['X']
    y = data['Y']
    return X, y


def knock_off_procedure():
    pass


def main():
    ## Load data
    X, y = load_npz("Xy_train.npz")
    X_test, y_test = load_npz("Xy_test.npz")

    ## Generate knock off variables
    alpha = 0.8
    n1 = 20
    d = 100
    tr = "PC"
    model = KnockOff(alpha, n1, d, measure_stat=tr)
    model.fit(X, y)
    ## Model variable selection


    ## Knock off statistics

    ## Final results


    pass

if __name__ == "__main__":
    main()