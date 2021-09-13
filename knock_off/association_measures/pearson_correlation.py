import numpy as np
from scipy.stats import pearsonr

def pearson_correlation(X, Y):

    X = np.squeeze(X, 1)

    return np.array([np.float32(pearsonr(X, Y)[0])])